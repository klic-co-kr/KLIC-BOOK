---
id: ch13
title: DNS·CDN·Edge와 전역 트래픽
part: network-runtime
order: 13
status: draft
freshness: current
last_verified: '2026-08-06'
review_due: '2027-02-06'
upstream_lineage:
- source: system-design-primer
  file: README.md
  anchor: domain-name-system
  action: REWRITE
audiences:
- backend-engineer
- platform-engineer
prerequisites:
- ch05
- ch06
learning_objectives:
- DNS와 CDN이 요청 경로와 장애 복구에 미치는 영향을 설명한다.
- 전역 라우팅 정책을 지연·건강·데이터 위치 요구로 선택한다.
- 캐시·원본·purge 실패를 포함한 edge 운영을 설계한다.
figures:
- fig-ch13-01
- fig-ch13-02
sources:
- rfc1034
- rfc1035
- rfc9111
draft_notice: 기술·편집·접근성 검수 전 초고
---

# 13. DNS·CDN·Edge와 전역 트래픽

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

## 이 장에서 해결할 문제

전역 트래픽은 “가장 가까운 리전”으로 보내는 문제만이 아니다. DNS TTL, resolver cache, CDN cache key, 원본 건강, 데이터 주권, failover 수렴 시간을 함께 설계해야 사용자가 실제로 안전한 리전에 도달한다.

이 절의 기준 출처: [@rfc1034; @rfc1035].

### 학습 목표

- DNS와 CDN이 요청 경로와 장애 복구에 미치는 영향을 설명한다.
- 전역 라우팅 정책을 지연·건강·데이터 위치 요구로 선택한다.
- 캐시·원본·purge 실패를 포함한 edge 운영을 설계한다.

## 먼저 결론

- DNS 변경은 즉시 전파되지 않으므로 TTL과 resolver 행동을 복구 시간에 포함한다.
- CDN cache key와 개인화 경계를 잘못 잡으면 정보가 섞이거나 적중률이 붕괴한다.
- edge는 정적 자산뿐 아니라 인증 전 검증·rate limit·간단한 계산을 수행할 수 있지만 원본과 정책 일관성을 관리해야 한다.
- 전역 failover는 트래픽 전환 후 데이터 쓰기 권한과 용량까지 검증해야 한다.

::: current-note
**2026-08-06 확인:** 이 장은 변화 가능한 표준·프로젝트·AI 구현을 포함한다. 기본 재검토일은 `2027-02-06`이며, 출판 직전 공식 문서를 다시 확인한다.
:::

## 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | DNS·CDN·Edge와 전역 트래픽에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | DNS 변경은 즉시 전파되지 않으므로 TTL과 resolver 행동을 복구 시간에 포함한다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | 정적·공개·개인화·쓰기 요청을 서로 다른 edge 정책으로 분리한다. |
| 실패·복구 | “DNS stale cache” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | 짧은 TTL만 믿지 말고 endpoint 자체의 redirect·proxy fallback을 둔다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | TLS 개인키와 인증서 배포 범위를 최소화하고 갱신 실패를 감시한다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | DNS 응답·TTL·resolver별 stale 비율 |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

## 핵심 개념

### Authoritative DNS

도메인에 대한 권한 있는 레코드를 제공한다.

### Recursive resolver

클라이언트를 대신해 DNS 계층을 조회하고 TTL 동안 캐시한다.

### TTL

레코드를 재조회하기 전 캐시할 수 있는 시간이다.

### Anycast

여러 위치가 같은 IP prefix를 광고해 네트워크 경로상 가까운 곳으로 라우팅한다.

### CDN cache key

어떤 요청을 같은 객체로 취급할지 정하는 키다.

### Origin shield

edge miss를 한 단계에서 모아 원본 fan-in과 burst를 줄인다.

### Edge compute

사용자 가까이에서 제한된 요청 처리·정책·변환을 수행한다.

핵심 개념의 정의와 범위는 [@rfc1034; @rfc1035; @rfc9111]를 기준으로 재검토해야 한다.

## 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| 권한 DNS | 지역·건강·정책에 따라 endpoint를 반환한다. |
| CDN/Edge PoP | TLS 종료, cache, WAF, 요청 정규화를 수행한다. |
| Origin shield | 원본 요청을 집계하고 재검증한다. |
| 지역 ingress | 해당 리전의 gateway로 요청을 받는다. |
| 데이터 소유 리전 | 쓰기 권한과 일관성 정책을 보유한다. |
| 전역 제어면 | 설정, 인증서, purge, 라우팅 정책을 배포한다. |
| 합성 검사 | 외부 관점의 DNS·TLS·콘텐츠 건강을 확인한다. |

<!-- figure-spec
id: fig-ch13-01
chapter: ch13
role: global-request-path
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch13-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: resolver·authoritative DNS·edge·shield·region·data owner를 지나는 전역 요청 경로를 보여준다.
required_labels_ko:
- 클라이언트
- Resolver
- Authoritative DNS
- Edge PoP
- Origin Shield
- 리전
- 데이터 소유 리전
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- rfc1034
- rfc1035
- rfc9111
alt_ko: resolver·authoritative DNS·edge·shield·region·data owner를 지나는 전역 요청 경로를 보여준다.
caption_ko: resolver·authoritative DNS·edge·shield·region·data owner를 지나는 전역 요청 경로를 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch13-01.md
-->

> **시각자료 제작 위치 — resolver·authoritative DNS·edge·shield·region·data owner를 지나는 전역 요청 경로를 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch13-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch13-01.md`  
> 대체 텍스트: resolver·authoritative DNS·edge·shield·region·data owner를 지나는 전역 요청 경로를 보여준다.


## 요청·데이터 흐름

1. 클라이언트가 recursive resolver를 통해 도메인을 조회한다.
2. resolver가 TTL과 정책에 따라 endpoint를 캐시한다.
3. 요청이 edge PoP에 도착해 TLS·보안·cache key를 평가한다.
4. hit이면 edge에서 응답하고 miss면 shield 또는 origin으로 전달한다.
5. 지역 ingress가 쓰기 소유권과 데이터 위치를 확인한다.
6. 응답 cacheability와 vary 조건을 명시한다.
7. 건강 저하 시 DNS·anycast·CDN 정책이 단계적으로 우회한다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

## 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| DNS 지리 라우팅 | 단순하고 다양한 endpoint로 유도할 수 있다. | 캐시된 응답 때문에 전환이 느리고 세밀한 요청 판단이 어렵다. | 리전 단위 전환 |
| Anycast/Global proxy | 빠른 네트워크 우회와 단일 IP 경험을 제공한다. | 공급자 제어면과 경로 정책에 의존한다. | 글로벌 HTTP ingress |
| 애플리케이션 리다이렉트 | 사용자·tenant·데이터 위치를 정밀하게 반영한다. | 첫 요청 왕복과 redirect loop 위험이 있다. | 로그인 후 home region 고정 |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@rfc1034; @rfc1035; @rfc9111]를 참조한다.

## 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| DNS stale cache | 장애 리전 주소가 TTL 동안 계속 사용된다. | 짧은 TTL만 믿지 말고 endpoint 자체의 redirect·proxy fallback을 둔다. |
| Cache poisoning/키 오류 | 인증 헤더·쿠키가 cache key에서 빠져 사용자 응답이 섞인다. | 기본 비공개, 명시적 cache key, 보안 테스트를 적용한다. |
| Thundering miss | 인기 객체 만료와 함께 모든 PoP가 원본을 호출한다. | request coalescing, stale-while-revalidate, shield를 사용한다. |
| Purge 지연 | 잘못된 콘텐츠나 보안 패치가 일부 PoP에 남는다. | versioned URL, purge 상태 관측, 짧은 비상 TTL을 둔다. |
| 전환 후 원본 포화 | 장애 리전 트래픽이 남은 리전 용량을 초과한다. | failover capacity와 admission policy를 사전 검증한다. |

<!-- figure-spec
id: fig-ch13-02
chapter: ch13
role: cdn-cache-decision
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch13-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: cache key 생성·hit/miss·revalidation·stale fallback·purge 흐름을 보여준다.
required_labels_ko:
- 요청
- Cache Key
- Hit
- Miss
- 재검증
- Stale
- Origin
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- rfc1034
- rfc1035
- rfc9111
alt_ko: cache key 생성·hit/miss·revalidation·stale fallback·purge 흐름을 보여준다.
caption_ko: cache key 생성·hit/miss·revalidation·stale fallback·purge 흐름을 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch13-02.md
-->

> **시각자료 제작 위치 — cache key 생성·hit/miss·revalidation·stale fallback·purge 흐름을 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch13-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch13-02.md`  
> 대체 텍스트: cache key 생성·hit/miss·revalidation·stale fallback·purge 흐름을 보여준다.


## 확장 전략

- 정적·공개·개인화·쓰기 요청을 서로 다른 edge 정책으로 분리한다.
- cache key cardinality와 객체 크기 분포를 관리한다.
- 리전 전환은 트래픽 비율을 단계적으로 올리고 데이터 소유권을 함께 이동한다.
- edge 설정 배포도 canary와 rollback을 지원해야 한다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

## 보안과 개인정보

- TLS 개인키와 인증서 배포 범위를 최소화하고 갱신 실패를 감시한다.
- 개인화 응답은 기본적으로 공유 cache에 저장하지 않는다.
- 지역별 데이터 주권과 로그 반출 정책을 edge까지 적용한다.
- Host, X-Forwarded-For 같은 전달 헤더의 신뢰 경계를 명확히 한다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

## 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- DNS 응답·TTL·resolver별 stale 비율
- edge hit/miss/revalidation과 cache key cardinality
- PoP·region별 p95/p99와 origin fetch 지연
- purge 전파 시간과 stale object 수
- failover 후 트래픽·용량·오류 분포

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

## 비용과 운영 복잡도

- CDN은 origin egress와 compute 비용을 줄일 수 있지만 request·purge·edge compute 비용을 만든다.
- 짧은 TTL은 DNS 조회량을 늘리고 반드시 빠른 전환을 보장하지 않는다.
- 다중 CDN은 공급자 장애를 줄일 수 있으나 설정·로그·인증서·계약 비용이 크게 늘어난다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

## 흔한 오해와 안티패턴

- TTL을 0으로 하면 즉시 failover된다고 믿는다.
- 모든 GET 응답을 안전하게 공유 cache할 수 있다고 생각한다.
- edge 건강만 보고 데이터 쓰기 가능 여부를 확인하지 않는다.
- CDN purge를 배포 전략 대신 사용한다.

## 설계 리뷰

- [ ] DNS cache 수렴 시간이 RTO에 포함됐는가?
- [ ] cache key가 인증·언어·압축·query 의미를 정확히 반영하는가?
- [ ] origin shield와 stale 정책이 원본 burst를 줄이는가?
- [ ] 전환 대상 리전의 데이터 권한과 여유 용량이 검증됐는가?
- [ ] edge 설정과 인증서의 제어면 장애를 고려했는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

## 연습문제

1. 개인화된 뉴스 홈과 공개 기사 본문에 서로 다른 CDN cache key 정책을 설계하라.
2. TTL 300초인 레코드의 리전 failover가 사용자에게 보이는 최악 경로를 그려라.
3. 인기 파일 1개가 동시에 만료될 때 origin 요청을 제한하는 계층을 설계하라.

## 핵심 요약

- DNS와 CDN cache는 복구 시간을 지연시킬 수 있다.
- cache key는 성능뿐 아니라 데이터 격리 규칙이다.
- edge와 origin의 책임·설정·관측을 분리한다.
- 전역 failover는 트래픽과 데이터 쓰기 권한을 함께 전환한다.
- TTL·purge·origin capacity를 실제로 시험한다.

## 출처

- [@rfc1034] IETF. **RFC 1034 — Domain Names: Concepts and Facilities** (1987). https://www.rfc-editor.org/rfc/rfc1034.html
- [@rfc1035] IETF. **RFC 1035 — Domain Names: Implementation and Specification** (1987). https://www.rfc-editor.org/rfc/rfc1035.html
- [@rfc9111] IETF. **RFC 9111 — HTTP Caching** (2022). https://www.rfc-editor.org/rfc/rfc9111.html

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
