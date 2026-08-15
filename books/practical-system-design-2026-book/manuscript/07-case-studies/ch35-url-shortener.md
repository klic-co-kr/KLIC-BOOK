---
id: ch35
title: 'URL 단축 서비스: 단일 노드에서 전역 서비스까지'
part: case-studies
order: 35
status: draft
freshness: durable
last_verified: '2026-08-06'
review_due: '2028-08-06'
upstream_lineage:
- source: system-design-primer
  file: README.md
  anchor: design-a-url-shortener
  action: REWRITE
audiences:
- backend-engineer
- platform-engineer
prerequisites:
- ch02
- ch10
- ch11
- ch13
- ch22
- ch25
learning_objectives:
- URL 단축 서비스의 규모·키·redirect 요구를 계산한다.
- 쓰기 원장과 전역 read path를 단계적으로 확장한다.
- abuse·삭제·analytics·region failover를 설계한다.
figures:
- fig-ch35-01
- fig-ch35-02
- fig-ch35-03
- fig-ch35-04
- fig-ch35-05
sources:
- rfc3986
- rfc9110
- rfc9111
- consistent-hashing
- upstream-primer
draft_notice: 기술·편집·접근성 검수 전 초고
---

## 35. URL 단축 서비스: 단일 노드에서 전역 서비스까지

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

### 이 장에서 해결할 문제

URL 단축 서비스는 단순 key-value 조회처럼 보이지만 공개 식별자 생성, 영구 redirect 의미, hot link, 악성 URL, 삭제, cache, 전역 지연, 분석 이벤트가 결합된다. 처음부터 모든 기능을 동기 경로에 넣지 않고 redirect 핵심 경로를 가장 작게 보호해야 한다.

이 절의 기준 출처: [@rfc3986; @rfc9110].

#### 학습 목표

- URL 단축 서비스의 규모·키·redirect 요구를 계산한다.
- 쓰기 원장과 전역 read path를 단계적으로 확장한다.
- abuse·삭제·analytics·region failover를 설계한다.

### 먼저 결론

- 핵심 경로는 `short code → 활성 destination` 조회와 redirect 응답이다.
- code는 충분한 공간·충돌 처리·예측 가능성·삭제 후 재사용 정책을 가져야 한다.
- analytics는 redirect와 분리된 비동기 event로 수집한다.
- 전역 cache와 read replica는 지연을 낮추지만 차단·삭제 전파 SLO를 요구한다.

### 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | URL 단축 서비스: 단일 노드에서 전역 서비스까지에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | 핵심 경로는 `short code → 활성 destination` 조회와 redirect 응답이다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | redirect read path는 edge→regional cache→read replica/owner로 단계화한다. |
| 실패·복구 | “Code collision” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | DB UNIQUE 제약과 bounded regeneration을 사용한다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | 허용 scheme을 제한하고 `javascript:`, credential 포함 URL, 내부 IP/metadata endpoint를 차단한다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | redirect p50/p95/p99·cache hit·origin fallback |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

### 핵심 개념

#### Short code

긴 URL을 가리키는 공개 식별자다.

#### Redirect semantics

301/308 같은 영구 redirect와 302/307 같은 임시 redirect의 cache·method 의미를 선택한다.

#### Canonicalization

URL의 scheme·host·encoding·fragment를 저장·비교하는 규칙이다.

#### Collision handling

생성한 code가 이미 존재할 때 재시도·예약·중앙 할당으로 해결한다.

#### Hot link

소수 code에 redirect가 집중되는 분포다.

#### Abuse screening

phishing·malware·spam·open redirect 악용을 탐지·차단하는 경로다.

#### Tombstone

삭제된 code가 다시 잘못 사용되지 않도록 상태를 보존하는 record다.

핵심 개념의 정의와 범위는 [@rfc3986; @rfc9110; @rfc9111; @consistent-hashing; @upstream-primer]를 기준으로 재검토해야 한다.

#### 단계별 확장

**1단계 — 단일 리전 원장:** `short_code`에 UNIQUE 제약을 둔 관계형 DB와 cache-aside만으로 시작한다. 이 단계의 목표는 code 생성, redirect 의미, 삭제·만료 상태를 검증하는 것이다.

**2단계 — 읽기 확장:** redirect가 create보다 훨씬 많다는 실제 관측이 확인되면 regional cache와 read replica를 추가한다. `active`, `blocked`, `deleted`, `expired` 상태를 version과 함께 cache하고, 보안 차단은 일반 TTL보다 높은 우선순위의 purge를 사용한다.

**3단계 — 전역 edge:** 공개 redirect를 edge에 배치한다. 생성·수정은 여전히 쓰기 소유 리전으로 보내고, 장애 중에는 이미 존재하는 링크 redirect를 유지하되 신규 생성은 명시적으로 제한할 수 있다.

**4단계 — 분석 분리:** click event는 redirect 응답과 독립적으로 event log에 보낸다. broker 장애가 redirect를 막지 않게 유한 buffer와 drop metric을 사용하고, 정확한 과금·정산이 필요한 이벤트라면 별도의 내구 경로를 설계한다.

### 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| Create API | URL 검증·정책·custom alias·idempotency를 처리한다. |
| ID/code generator | 고유 내부 ID와 공개 code를 만든다. |
| URL metadata DB | destination·owner·status·expiry·version을 원장으로 저장한다. |
| Redirect edge | code lookup, cache, policy, redirect를 수행한다. |
| Cache tier | 인기 code와 negative/tombstone을 저장한다. |
| Abuse service | 동기 최소 검증과 비동기 심층 분석을 수행한다. |
| Event log | click event를 비동기 분석으로 전달한다. |
| Analytics store | 집계·bot filtering·report를 제공한다. |
| Global control | region route·blocklist·purge·failover를 관리한다. |

<!-- figure-spec
id: fig-ch35-01
chapter: ch35
role: url-shortener-v1
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch35-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 단일 API·DB에서 시작하는 최소 URL 단축 서비스와 create/redirect 경로를 보여준다.
required_labels_ko:
- 사용자
- Create API
- Redirect API
- URL DB
- Short Code
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- rfc3986
- rfc9110
- rfc9111
alt_ko: 단일 API·DB에서 시작하는 최소 URL 단축 서비스와 create/redirect 경로를 보여준다.
caption_ko: 단일 API·DB에서 시작하는 최소 URL 단축 서비스와 create/redirect 경로를 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch35-01.md
-->

> **시각자료 제작 위치 — 단일 API·DB에서 시작하는 최소 URL 단축 서비스와 create/redirect 경로를 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch35-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch35-01.md`  
> 대체 텍스트: 단일 API·DB에서 시작하는 최소 URL 단축 서비스와 create/redirect 경로를 보여준다.


### 요청·데이터 흐름

1. 사용자가 destination과 선택적 custom alias를 idempotency key로 제출한다.
2. API가 scheme·길이·정책을 검증하고 normalized form과 원문을 구분해 저장한다.
3. generator가 code를 만들고 UNIQUE 제약으로 충돌을 확정한다.
4. 원장 DB가 active record를 commit한 뒤 cache를 채운다.
5. redirect 요청이 edge cache에서 code 상태를 읽는다.
6. active이면 목적지로 redirect하고 click event를 비동기 발행한다.
7. 차단·삭제·만료는 tombstone과 purge version을 모든 region에 전파한다.
8. analytics는 중복·bot·늦은 event를 별도로 처리한다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

### 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| 무작위 code | 예측이 어렵고 중앙 sequence가 필요 없다. | 충돌 검사와 index locality가 필요하다. | 공개 단축 URL |
| 순차 ID+Base62 | 충돌이 없고 짧은 code를 만들기 쉽다. | 생성량 추정·enumeration·중앙/구간 할당이 필요하다. | 내부/인증된 링크 |
| Content hash | 같은 URL dedup이 가능하다. | URL normalization·충돌·소유자별 정책이 복잡하다. | 공용 canonical link |
| 301/308 | browser/CDN cache 효율이 높다. | destination 변경·차단이 느리게 반영될 수 있다. | 불변 링크 |
| 302/307 | 매 요청 제어와 변경 반영이 쉽다. | origin 조회·latency·비용이 증가한다. | 동적·관리 링크 |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@rfc3986; @rfc9110; @rfc9111]를 참조한다.

### 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| Code collision | 동시에 같은 code가 생성된다. | DB UNIQUE 제약과 bounded regeneration을 사용한다. |
| Hot celebrity link | 한 code가 edge/cache shard와 analytics를 포화시킨다. | edge replication·request coalescing·sampled analytics를 사용한다. |
| Cache stale block | 악성 링크 차단 후 edge가 오래된 active 값을 반환한다. | block version·priority purge·짧은 deny cache를 둔다. |
| Redirect loop | destination이 자신 또는 redirect chain을 가리킨다. | create 시 hop 제한 검사와 runtime loop guard를 둔다. |
| Analytics backpressure | event broker 장애가 redirect를 지연시킨다. | best-effort bounded buffer·sampling·drop metric으로 핵심 경로와 분리한다. |
| Region failover | 새 region cache는 비어 있고 원장 쓰기 권한이 없다. | read-only redirect 유지, create 제한, warm cache·single writer epoch를 사용한다. |

<!-- figure-spec
id: fig-ch35-02
chapter: ch35
role: url-shortener-global
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch35-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: edge·regional cache·single writer·event log·analytics를 포함한 전역 구조를 보여준다.
required_labels_ko:
- Edge
- Regional Cache
- URL DB
- Single Writer
- Event Log
- Analytics
- Abuse Service
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- rfc3986
- rfc9110
- rfc9111
alt_ko: edge·regional cache·single writer·event log·analytics를 포함한 전역 구조를 보여준다.
caption_ko: edge·regional cache·single writer·event log·analytics를 포함한 전역 구조를 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch35-02.md
-->

> **시각자료 제작 위치 — edge·regional cache·single writer·event log·analytics를 포함한 전역 구조를 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch35-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch35-02.md`  
> 대체 텍스트: edge·regional cache·single writer·event log·analytics를 포함한 전역 구조를 보여준다.


### 종합 설계 보조 도표

이 장은 앞의 원리를 하나의 서비스로 연결하므로 다음 보조 도표까지 제작한다.

<!-- figure-spec
id: fig-ch35-03
chapter: ch35
role: capacity-and-keyspace
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch35-03.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: URL 생성·redirect 비율, Base62 keyspace, 저장량 계산을 한 장에 보여준다.
required_labels_ko:
- Create RPS
- Redirect RPS
- Base62 공간
- 저장량
- 성장률
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- rfc3986
- rfc9110
- rfc9111
alt_ko: URL 생성·redirect 비율, Base62 keyspace, 저장량 계산을 한 장에 보여준다.
caption_ko: URL 생성·redirect 비율, Base62 keyspace, 저장량 계산을 한 장에 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch35-03.md
-->

> **시각자료 제작 위치 — URL 생성·redirect 비율, Base62 keyspace, 저장량 계산을 한 장에 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch35-03.svg`  
> 제작 명세: `assets/specs/svg/fig-ch35-03.md`  
> 대체 텍스트: URL 생성·redirect 비율, Base62 keyspace, 저장량 계산을 한 장에 보여준다.


<!-- figure-spec
id: fig-ch35-04
chapter: ch35
role: abuse-and-blocking
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch35-04.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: URL 생성 전·후 scan, blocklist, 긴급 purge, 신고 처리 흐름을 보여준다.
required_labels_ko:
- URL 검증
- Sandbox Scan
- Blocklist
- 긴급 Purge
- 신고
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- rfc3986
- rfc9110
- rfc9111
alt_ko: URL 생성 전·후 scan, blocklist, 긴급 purge, 신고 처리 흐름을 보여준다.
caption_ko: URL 생성 전·후 scan, blocklist, 긴급 purge, 신고 처리 흐름을 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch35-04.md
-->

> **시각자료 제작 위치 — URL 생성 전·후 scan, blocklist, 긴급 purge, 신고 처리 흐름을 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch35-04.svg`  
> 제작 명세: `assets/specs/svg/fig-ch35-04.md`  
> 대체 텍스트: URL 생성 전·후 scan, blocklist, 긴급 purge, 신고 처리 흐름을 보여준다.


<!-- figure-spec
id: fig-ch35-05
chapter: ch35
role: regional-failover
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch35-05.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 쓰기 소유 리전 장애 중 read redirect 유지·create 제한·복구·failback을 보여준다.
required_labels_ko:
- Primary Region
- Secondary Region
- Edge Cache
- Create 제한
- Read 유지
- Failback
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- rfc3986
- rfc9110
- rfc9111
alt_ko: 쓰기 소유 리전 장애 중 read redirect 유지·create 제한·복구·failback을 보여준다.
caption_ko: 쓰기 소유 리전 장애 중 read redirect 유지·create 제한·복구·failback을 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch35-05.md
-->

> **시각자료 제작 위치 — 쓰기 소유 리전 장애 중 read redirect 유지·create 제한·복구·failback을 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch35-05.svg`  
> 제작 명세: `assets/specs/svg/fig-ch35-05.md`  
> 대체 텍스트: 쓰기 소유 리전 장애 중 read redirect 유지·create 제한·복구·failback을 보여준다.


### 확장 전략

- redirect read path는 edge→regional cache→read replica/owner로 단계화한다.
- create write path는 단일 writer 또는 region별 ID namespace로 단순화한다.
- hot code는 일반 cache eviction 정책과 분리해 pin·replicate한다.
- analytics는 event partition을 code보다 시간/tenant와 조합해 hotspot을 피한다.
- custom domain TLS·DNS를 비동기 provisioning workflow로 분리한다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

### 보안과 개인정보

- 허용 scheme을 제한하고 `javascript:`, credential 포함 URL, 내부 IP/metadata endpoint를 차단한다.
- URL preview·scan은 sandboxed fetch와 SSRF 방어를 사용한다.
- 소유자만 목적지를 변경하고 변경·차단을 감사한다.
- public analytics는 개인 IP·user agent를 최소화·집계하고 retention을 제한한다.
- enumeration·brute force·phishing campaign에 rate limit과 abuse response를 둔다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

### 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- redirect p50/p95/p99·cache hit·origin fallback
- create success·collision·custom alias conflict
- code별 hotness·cache shard skew
- block/delete propagation·stale redirect
- event publish/drop·analytics lag
- region failover read/create availability

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

### 비용과 운영 복잡도

- edge request와 egress가 대부분의 가변 비용이 된다.
- analytics 원시 이벤트 보존은 redirect metadata보다 훨씬 크게 성장할 수 있다.
- 301 cache는 비용을 줄이지만 목적지 제어·차단 민첩성을 낮춘다.
- 사용자 정의 domain은 인증서·DNS·지원 운영 비용을 추가한다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

### 흔한 오해와 안티패턴

- code 생성기를 DB 제약 없이 메모리 random으로만 구현한다.
- click analytics 저장을 redirect transaction 안에서 수행한다.
- 모든 redirect를 영구 cache해 abuse 차단이 늦어진다.
- URL 문자열만 보고 SSRF·phishing 위험을 검토하지 않는다.

### 설계 리뷰

- [ ] redirect 핵심 경로가 analytics·scan 실패와 격리됐는가?
- [ ] code 고유성과 재사용·삭제 정책이 명확한가?
- [ ] hot link와 cache miss가 원장을 보호하는가?
- [ ] block/delete 전파 시간이 측정되는가?
- [ ] region 장애 중 create와 redirect 동작이 구분되는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

### 연습문제

1. 하루 1억 redirect, 100만 create, 평균 URL 500B인 서비스의 1년 논리 저장량과 평균 RPS를 계산하라.
2. 7자 Base62 공간 크기와 예상 생성량을 비교하고 collision 전략을 제시하라.
3. 악성 링크 긴급 차단이 edge에 30초 안에 반영되는 경로를 설계하라.

### 핵심 요약

- redirect와 analytics 경로를 분리한다.
- 공개 code의 고유성·예측 가능성·삭제 의미를 설계한다.
- edge cache는 지연을 낮추지만 차단 전파 정책이 필요하다.
- hot link는 키 단위 복제와 분석 sampling으로 다룬다.
- 전역 장애에서 read redirect와 create write를 분리한다.

### 출처

- [@rfc3986] IETF. **RFC 3986 — Uniform Resource Identifier (URI): Generic Syntax** (2005). https://www.rfc-editor.org/rfc/rfc3986.html
- [@rfc9110] IETF. **RFC 9110 — HTTP Semantics** (2022). https://www.rfc-editor.org/rfc/rfc9110.html
- [@rfc9111] IETF. **RFC 9111 — HTTP Caching** (2022). https://www.rfc-editor.org/rfc/rfc9111.html
- [@consistent-hashing] David Karger et al.. **Consistent Hashing and Random Trees** (1997). https://doi.org/10.1145/258533.258660
- [@upstream-primer] Donne Martin. **The System Design Primer** (2026). https://github.com/donnemartin/system-design-primer

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
