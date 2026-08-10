---
id: ch14
title: L4/L7 Load Balancing·Proxy·Gateway
part: network-runtime
order: 14
status: draft
freshness: current
last_verified: '2026-08-06'
review_due: '2027-02-06'
upstream_lineage:
- source: system-design-primer
  file: README.md
  anchor: load-balancer
  action: REWRITE
audiences:
- backend-engineer
- platform-engineer
prerequisites:
- ch05
- ch13
learning_objectives:
- L4와 L7 분산의 관측·정책 차이를 설명한다.
- reverse proxy·API gateway·service proxy의 책임을 구분한다.
- 건강 검사·connection draining·재시도가 장애에 미치는 영향을 설계한다.
figures:
- fig-ch14-01
- fig-ch14-02
sources:
- rfc9110
- rfc9112
- google-sre-overload
draft_notice: 기술·편집·접근성 검수 전 초고
---

# 14. L4/L7 Load Balancing·Proxy·Gateway

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

## 이 장에서 해결할 문제

트래픽 분산 계층은 단순한 round-robin 장치가 아니다. 연결과 요청의 수명, 건강 상태, 정책, 재시도, TLS, 헤더 신뢰, 배포 전환을 다루기 때문에 계층을 늘릴 때마다 책임과 중복 기능을 명확히 해야 한다.

이 절의 기준 출처: [@rfc9110; @rfc9112].

### 학습 목표

- L4와 L7 분산의 관측·정책 차이를 설명한다.
- reverse proxy·API gateway·service proxy의 책임을 구분한다.
- 건강 검사·connection draining·재시도가 장애에 미치는 영향을 설계한다.

## 먼저 결론

- L4는 연결 단위, L7은 HTTP 요청 의미를 활용해 라우팅한다.
- health check 통과와 실제 사용자 요청 성공은 다를 수 있다.
- gateway가 무제한 재시도하면 하위 서비스 과부하를 확대한다.
- proxy가 추가한 identity·client IP 헤더는 신뢰 가능한 hop에서만 받아들인다.

::: current-note
**2026-08-06 확인:** 이 장은 변화 가능한 표준·프로젝트·AI 구현을 포함한다. 기본 재검토일은 `2027-02-06`이며, 출판 직전 공식 문서를 다시 확인한다.
:::

## 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | L4/L7 Load Balancing·Proxy·Gateway에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | L4는 연결 단위, L7은 HTTP 요청 의미를 활용해 라우팅한다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | 연결 수와 요청 수를 모두 고려해 endpoint 부하를 계산한다. |
| 실패·복구 | “거짓 건강” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | readiness에 핵심 의존성을 제한적으로 반영하고 passive health를 사용한다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | TLS 종료 지점마다 평문 구간과 키 보유 범위를 기록한다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | 계층별 active connection·request rate·queue |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

## 핵심 개념

### L4 load balancing

IP·포트·연결 정보를 중심으로 전달한다.

### L7 load balancing

Host, path, method, header 등 애플리케이션 프로토콜 정보를 활용한다.

### Reverse proxy

서버 앞에서 연결 종료·라우팅·캐시·정책을 수행한다.

### API gateway

외부 API의 인증, quota, 버전, routing, 변환 같은 공통 경계를 제공한다.

### Connection draining

배포·제거 중 신규 연결을 막고 기존 요청을 제한 시간 동안 마치는 절차다.

### Passive health

실제 요청 오류를 건강 판단에 반영하는 방식이다.

### Outlier detection

비정상 endpoint를 일시 격리하는 정책이다.

핵심 개념의 정의와 범위는 [@rfc9110; @rfc9112; @google-sre-overload]를 기준으로 재검토해야 한다.

## 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| 전역 ingress | 공용 endpoint와 DDoS·TLS 정책을 담당한다. |
| L7 gateway | API 인증·라우팅·request limit을 수행한다. |
| L4 balancer | 연결을 지역 서비스 endpoint로 분산한다. |
| 서비스 proxy | retry·timeout·mTLS·관측을 하위 서비스 호출에 적용한다. |
| Endpoint registry | 건강한 인스턴스와 배포 버전을 제공한다. |
| Policy store | route·quota·header 신뢰 정책을 버전 관리한다. |

<!-- figure-spec
id: fig-ch14-01
chapter: ch14
role: proxy-layers
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch14-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 전역 ingress·L7 gateway·L4 balancer·service proxy·endpoint의 책임을 계층별로 보여준다.
required_labels_ko:
- 전역 Ingress
- L7 Gateway
- L4 Balancer
- Service Proxy
- Endpoint
- TLS 경계
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- rfc9110
- rfc9112
- google-sre-overload
alt_ko: 전역 ingress·L7 gateway·L4 balancer·service proxy·endpoint의 책임을 계층별로 보여준다.
caption_ko: 전역 ingress·L7 gateway·L4 balancer·service proxy·endpoint의 책임을 계층별로 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch14-01.md
-->

> **시각자료 제작 위치 — 전역 ingress·L7 gateway·L4 balancer·service proxy·endpoint의 책임을 계층별로 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch14-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch14-01.md`  
> 대체 텍스트: 전역 ingress·L7 gateway·L4 balancer·service proxy·endpoint의 책임을 계층별로 보여준다.


## 요청·데이터 흐름

1. 연결이 L4 또는 L7 ingress에 도착한다.
2. TLS 종료 위치와 client identity 전달 방식을 결정한다.
3. L7 계층이 route·권한·크기·quota를 검증한다.
4. healthy endpoint 집합에서 locality·load·hash 정책으로 대상을 선택한다.
5. 남은 deadline과 재시도 예산을 전달한다.
6. 응답·reset·timeout을 passive health에 반영한다.
7. 배포 제거 시 endpoint를 먼저 제외하고 연결을 drain한다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

## 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| L4 중심 | 프로토콜 독립적이고 처리 오버헤드가 낮다. | 요청 단위 정책·관측·세밀한 라우팅이 어렵다. | TCP/UDP 서비스·고성능 ingress |
| L7 중심 | 콘텐츠 기반 routing과 공통 보안 정책이 풍부하다. | CPU·메모리·설정 복잡도와 새로운 장애 지점이 생긴다. | HTTP API·점진 배포 |
| Client-side balancing | 중간 hop을 줄이고 서비스별 판단이 가능하다. | 클라이언트 라이브러리·서비스 발견 일관성이 필요하다. | 내부 RPC |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@rfc9110; @rfc9112; @google-sre-overload]를 참조한다.

## 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| 거짓 건강 | 얕은 `/health`는 성공하지만 DB·thread pool이 포화됐다. | readiness에 핵심 의존성을 제한적으로 반영하고 passive health를 사용한다. |
| Retry amplification | gateway와 client와 service proxy가 각각 재시도한다. | 한 계층이 retry budget을 소유하고 시도 횟수를 전달한다. |
| Drain 실패 | 종료 신호 직후 기존 연결이 끊기고 긴 요청이 유실된다. | endpoint 제거→drain→종료 순서와 최대 요청 시간을 정한다. |
| Sticky overload | 세션 affinity가 일부 endpoint에 부하를 고정한다. | bounded-load hashing과 세션 상태 외부화를 검토한다. |
| Header spoofing | 외부 사용자가 내부 identity·IP 헤더를 직접 보낸다. | edge에서 제거 후 신뢰된 proxy가 재작성한다. |

<!-- figure-spec
id: fig-ch14-02
chapter: ch14
role: draining-sequence
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch14-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 배포 중 endpoint 제외·기존 연결 drain·deadline 대기·강제 종료 순서를 보여준다.
required_labels_ko:
- Registry
- Load Balancer
- 기존 연결
- 신규 요청
- Drain
- 종료
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- rfc9110
- rfc9112
- google-sre-overload
alt_ko: 배포 중 endpoint 제외·기존 연결 drain·deadline 대기·강제 종료 순서를 보여준다.
caption_ko: 배포 중 endpoint 제외·기존 연결 drain·deadline 대기·강제 종료 순서를 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch14-02.md
-->

> **시각자료 제작 위치 — 배포 중 endpoint 제외·기존 연결 drain·deadline 대기·강제 종료 순서를 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch14-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch14-02.md`  
> 대체 텍스트: 배포 중 endpoint 제외·기존 연결 drain·deadline 대기·강제 종료 순서를 보여준다.


## 확장 전략

- 연결 수와 요청 수를 모두 고려해 endpoint 부하를 계산한다.
- long-lived connection은 신규 endpoint에 자동 재분배되지 않으므로 reconnect 정책을 둔다.
- route config가 커질수록 계층별 ownership과 validation을 자동화한다.
- gateway를 비즈니스 orchestration 계층으로 키우지 않고 공통 경계 책임에 제한한다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

## 보안과 개인정보

- TLS 종료 지점마다 평문 구간과 키 보유 범위를 기록한다.
- gateway 인증 결과를 서명·mTLS·짧은 수명 토큰으로 하위에 전달한다.
- request smuggling을 막기 위해 hop 간 HTTP parsing과 header 정규화를 일치시킨다.
- 관리 API와 데이터면 endpoint를 분리하고 최소 권한을 적용한다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

## 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- 계층별 active connection·request rate·queue
- endpoint별 p95/p99·reset·5xx·ejection
- route match·no route·auth·quota 거부
- retry attempts와 amplification factor
- drain 중 강제 종료된 요청 수

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

## 비용과 운영 복잡도

- proxy hop은 컴퓨팅·TLS·네트워크 비용을 추가한다.
- 중복 gateway·mesh 기능은 라이선스보다 설정·디버깅 인력 비용이 더 클 수 있다.
- client-side balancing은 인프라 hop을 줄이지만 SDK 배포·호환 비용을 만든다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

## 흔한 오해와 안티패턴

- L4와 L7을 “빠름/느림” 한 문장으로만 비교한다.
- 모든 공통 로직을 gateway에 넣는다.
- health check endpoint 하나로 실제 사용자 경로를 대표한다.
- 재시도와 timeout을 각 계층이 독립 설정한다.

## 설계 리뷰

- [ ] 각 proxy 계층의 단일 책임이 명확한가?
- [ ] TLS와 identity 신뢰 경계가 hop별로 문서화됐는가?
- [ ] 건강·drain·retry 정책이 실제 요청 수명과 맞는가?
- [ ] long-lived connection과 sticky routing을 고려했는가?
- [ ] 설정 오류를 canary·검증·rollback할 수 있는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

## 연습문제

1. WebSocket 서비스의 L4/L7 분산과 배포 drain 절차를 설계하라.
2. client·gateway·service가 모두 3회 재시도할 때 최대 시도 수를 계산하고 단일 retry budget으로 바꾸라.
3. 신뢰할 수 있는 client IP 전달 헤더 체인을 설계하라.

## 핵심 요약

- L4는 연결, L7은 요청 의미를 중심으로 분산한다.
- proxy 계층마다 책임과 재시도 소유자를 하나로 둔다.
- health check와 실제 사용자 건강을 분리해 본다.
- 배포에는 endpoint 제거와 connection draining이 필요하다.
- 전달 헤더와 TLS 종료는 보안 경계다.

## 출처

- [@rfc9110] IETF. **RFC 9110 — HTTP Semantics** (2022). https://www.rfc-editor.org/rfc/rfc9110.html
- [@rfc9112] IETF. **RFC 9112 — HTTP/1.1** (2022). https://www.rfc-editor.org/rfc/rfc9112.html
- [@google-sre-overload] Google. **Site Reliability Engineering — Handling Overload** (2016). https://sre.google/sre-book/handling-overload/

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
