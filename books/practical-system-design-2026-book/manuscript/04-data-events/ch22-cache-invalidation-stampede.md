---
id: ch22
title: 캐시·무효화·Stampede·Hot Key
part: data-events
order: 22
status: draft
freshness: durable
last_verified: '2026-08-06'
review_due: '2028-08-06'
upstream_lineage:
- source: system-design-primer
  file: README.md
  anchor: cache
  action: REWRITE
audiences:
- backend-engineer
- platform-engineer
prerequisites:
- ch05
- ch18
learning_objectives:
- cache 역할과 일관성 경계를 정의한다.
- cache-aside·write-through·refresh 전략을 비교한다.
- stampede·hot key·negative cache 실패를 완화한다.
figures:
- chart-ch22-01
- fig-ch22-01
- fig-ch22-02
sources:
- rfc9111
- redis-cache
- memcached-docs
draft_notice: 기술·편집·접근성 검수 전 초고
---

## 22. 캐시·무효화·Stampede·Hot Key

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

### 이 장에서 해결할 문제

캐시는 느린 원본을 가리는 마법이 아니라 복제된 파생 상태다. 어떤 데이터를 얼마 동안 오래되게 보여도 되는지, miss가 몰릴 때 원본을 어떻게 보호할지, 삭제·권한 변경을 얼마나 빨리 반영할지를 먼저 정해야 한다.

이 절의 기준 출처: [@rfc9111; @redis-cache].

#### 학습 목표

- cache 역할과 일관성 경계를 정의한다.
- cache-aside·write-through·refresh 전략을 비교한다.
- stampede·hot key·negative cache 실패를 완화한다.

### 먼저 결론

- cache hit ratio만이 아니라 miss cost와 원본 보호 효과를 본다.
- TTL은 무효화 정책의 대체물이 아니라 최대 staleness·정리 수단이다.
- hot key와 동시에 만료되는 key가 전체 원본을 무너뜨릴 수 있다.
- 권한·잔액·재고 같은 상태는 stale 허용 범위와 실패 시 행동을 별도로 정한다.

### 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | 캐시·무효화·Stampede·Hot Key에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | cache hit ratio만이 아니라 miss cost와 원본 보호 효과를 본다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | cache key cardinality와 value size를 함께 관리한다. |
| 실패·복구 | “Stampede” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | single-flight, TTL jitter, stale fallback을 사용한다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | tenant·locale·권한 scope를 cache key에 포함한다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | hit/miss/stale/negative 비율과 key cardinality |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

<!-- figure-spec
id: chart-ch22-01
chapter: ch22
role: cache-hit-origin-load
kind: data-chart
generator: python-matplotlib
output: assets/charts/chart-ch22-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 전체 요청률이 고정일 때 hit ratio가 낮아질수록 origin QPS가 비선형적으로 체감상 커지는 관계를 보여준다.
required_labels_ko:
- Cache Hit Ratio (%)
- Origin QPS
- 총 10,000 RPS
prohibited:
- 출처 없는 실측 수치
- 3D chart
- 잘린 축
- 색상만으로 구분
source_refs:
- rfc9111
- redis-cache
alt_ko: 전체 요청률이 고정일 때 hit ratio가 낮아질수록 origin QPS가 비선형적으로 체감상 커지는 관계를 보여준다.
caption_ko: 캐시 적중률과 원본 부하
status: specified
spec_file: assets/specs/charts/chart-ch22-01.md
-->

> **시각자료 제작 위치 — 캐시 적중률과 원본 부하**  
> 종류: `data-chart` · 상태: `specified` · 산출 경로: `assets/charts/chart-ch22-01.svg`  
> 제작 명세: `assets/specs/charts/chart-ch22-01.md`  
> 대체 텍스트: 전체 요청률이 고정일 때 hit ratio가 낮아질수록 origin QPS가 비선형적으로 체감상 커지는 관계를 보여준다.

### 핵심 개념

#### Cache-aside

애플리케이션이 cache를 먼저 읽고 miss 시 원본에서 가져와 채운다.

#### Write-through

쓰기 경로가 cache와 원본을 함께 갱신한다.

#### Write-behind

cache가 먼저 변경을 받아 원본에 나중에 반영하며 데이터 손실·순서 위험이 있다.

#### TTL

entry가 자동 만료되기까지의 시간이다.

#### Stampede

인기 key가 만료되자 다수 요청이 동시에 원본을 조회하는 현상이다.

#### Hot key

일부 key에 요청이 지나치게 집중되는 현상이다.

#### Negative cache

존재하지 않음·오류 같은 결과를 제한 시간 저장해 반복 miss를 줄이는 방식이다.

#### Stale-while-revalidate

오래된 값을 잠시 제공하면서 백그라운드에서 갱신한다.

핵심 개념의 정의와 범위는 [@rfc9111; @redis-cache; @memcached-docs]를 기준으로 재검토해야 한다.

### 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| Client/local cache | 네트워크 왕복을 줄이지만 invalidation 범위가 넓다. |
| Distributed cache | 공유 key/value와 TTL을 제공한다. |
| Origin store | 진실의 원천과 transaction을 소유한다. |
| Refresh coordinator | single-flight·lease로 한 요청만 값을 갱신한다. |
| Invalidation channel | 변경·삭제·권한 사건을 cache 계층에 전달한다. |
| Hot-key shield | 복제·local cache·request coalescing으로 집중을 완화한다. |

<!-- figure-spec
id: fig-ch22-01
chapter: ch22
role: cache-patterns
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch22-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: cache-aside·write-through·refresh-ahead의 읽기·쓰기·실패 경로를 비교한다.
required_labels_ko:
- 애플리케이션
- Cache
- Origin
- Hit
- Miss
- Write
- Refresh
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- rfc9111
- redis-cache
- memcached-docs
alt_ko: cache-aside·write-through·refresh-ahead의 읽기·쓰기·실패 경로를 비교한다.
caption_ko: cache-aside·write-through·refresh-ahead의 읽기·쓰기·실패 경로를 비교한다
status: specified
spec_file: assets/specs/svg/fig-ch22-01.md
-->

> **시각자료 제작 위치 — cache-aside·write-through·refresh-ahead의 읽기·쓰기·실패 경로를 비교한다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch22-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch22-01.md`  
> 대체 텍스트: cache-aside·write-through·refresh-ahead의 읽기·쓰기·실패 경로를 비교한다.

### 요청·데이터 흐름

1. 요청이 cache key와 version/tenant scope를 구성한다.
2. hit이면 staleness 정책을 확인해 값을 반환한다.
3. miss 또는 refresh 필요 시 single-flight lock을 시도한다.
4. 승자만 원본을 읽고 나머지는 bounded wait 또는 stale 응답을 사용한다.
5. 새 값에 TTL jitter와 version을 붙여 저장한다.
6. 원본 변경 이벤트가 관련 key를 삭제·새 version으로 전환한다.
7. cache 장애 시 원본 보호를 위한 rate limit·degradation을 적용한다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

### 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| Cache-aside | 구현이 단순하고 원본을 명확히 유지한다. | stale·race·cold miss를 애플리케이션이 처리한다. | 일반 읽기 cache |
| Write-through | 쓰기 후 cache 일관성이 좋다. | 쓰기 latency와 이중 실패 처리가 복잡하다. | 높은 read-after-write 요구 |
| Refresh-ahead/SWR | 사용자 latency와 stampede를 줄인다. | 오래된 응답과 refresh worker 운영이 필요하다. | 인기 콘텐츠·설정 |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@rfc9111; @redis-cache; @memcached-docs]를 참조한다.

### 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| Stampede | 동일 key miss가 원본에 수천 번 전달된다. | single-flight, TTL jitter, stale fallback을 사용한다. |
| Cache outage | 모든 요청이 원본으로 우회해 DB가 포화된다. | origin admission control, local cache, 기능 축소를 둔다. |
| Stale authorization | 권한 회수 후 cache가 허용 결과를 계속 반환한다. | 짧은 TTL, versioned policy, 강한 revoke path를 사용한다. |
| Hot key node overload | 특정 key가 한 cache shard의 네트워크/CPU를 초과한다. | replicated hot key, client cache, key splitting을 사용한다. |
| Negative cache poisoning | 일시 오류를 장시간 “없음”으로 cache한다. | 오류 종류별 짧은 TTL과 success/absence 구분을 둔다. |

<!-- figure-spec
id: fig-ch22-02
chapter: ch22
role: stampede-protection
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch22-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 동시 miss가 single-flight·stale fallback·TTL jitter로 원본 한 요청으로 합쳐지는 모습을 보여준다.
required_labels_ko:
- 동시 요청
- 만료
- Single Flight
- Stale 응답
- Origin
- TTL Jitter
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- rfc9111
- redis-cache
- memcached-docs
alt_ko: 동시 miss가 single-flight·stale fallback·TTL jitter로 원본 한 요청으로 합쳐지는 모습을 보여준다.
caption_ko: 동시 miss가 single-flight·stale fallback·TTL jitter로 원본 한 요청으로 합쳐지는 모습을 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch22-02.md
-->

> **시각자료 제작 위치 — 동시 miss가 single-flight·stale fallback·TTL jitter로 원본 한 요청으로 합쳐지는 모습을 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch22-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch22-02.md`  
> 대체 텍스트: 동시 miss가 single-flight·stale fallback·TTL jitter로 원본 한 요청으로 합쳐지는 모습을 보여준다.

### 확장 전략

- cache key cardinality와 value size를 함께 관리한다.
- 다단 cache는 각 계층의 TTL·version·invalidation 책임을 명시한다.
- hot key 자동 탐지 후 local replication 또는 별도 tier로 승격한다.
- hit ratio가 높아도 miss가 고비용이면 원본 capacity를 계산한다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

### 보안과 개인정보

- tenant·locale·권한 scope를 cache key에 포함한다.
- 민감 데이터는 client/shared cache 저장 금지와 암호화 정책을 따른다.
- purge/invalidation 권한을 제한하고 감사한다.
- cache key에 원문 개인정보를 직접 넣지 않고 해시·내부 ID를 사용한다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

### 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- hit/miss/stale/negative 비율과 key cardinality
- miss 원본 latency·origin QPS·coalesced waiters
- hot key top-N·shard skew·eviction
- invalidation lag·stale read 탐지
- cache outage 시 fallback·shed 비율

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

### 비용과 운영 복잡도

- memory cache는 낮은 latency를 사지만 replication·network·reserved capacity 비용이 크다.
- 과도한 TTL은 비용을 줄여도 데이터 신선도와 보안 위험을 키운다.
- 다단 cache는 egress를 줄이지만 invalidation·디버깅 비용을 늘린다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

### 흔한 오해와 안티패턴

- hit ratio 99%면 원본이 안전하다고 결론낸다.
- 모든 key에 동일 TTL을 설정한다.
- cache를 원장처럼 수정한다.
- cache 장애 시 무조건 원본으로 fail-open한다.

### 설계 리뷰

- [ ] stale 허용 시간과 사용자 영향이 데이터별로 정의됐는가?
- [ ] stampede와 hot key가 원본을 넘지 않게 제한되는가?
- [ ] cache outage 시 원본 보호와 기능 축소 정책이 있는가?
- [ ] 권한·삭제 invalidation이 더 강하게 처리되는가?
- [ ] hit ratio 외에 miss cost와 invalidation lag를 보는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

### 연습문제

1. 캐시 적중률 95%가 85%로 떨어질 때 원본 요청률 변화 배수를 계산하라.
2. 인기 상품 페이지 만료 시 single-flight와 stale 응답 흐름을 설계하라.
3. 권한 회수 이벤트가 local·distributed·edge cache에 전파되는 정책을 작성하라.

### 핵심 요약

- 캐시는 파생 상태이며 원장이 아니다.
- TTL과 invalidation·version을 함께 설계한다.
- stampede와 cache outage에서 원본을 보호한다.
- hot key는 shard 수만 늘려 해결되지 않는다.
- 보안 상태에는 더 엄격한 stale 정책을 적용한다.

### 출처

- [@rfc9111] IETF. **RFC 9111 — HTTP Caching** (2022). https://www.rfc-editor.org/rfc/rfc9111.html
- [@redis-cache] Redis. **Redis Documentation — Client-side caching and cache patterns** (2026). https://redis.io/docs/latest/develop/use/client-side-caching/
- [@memcached-docs] Memcached Authors. **Memcached Documentation** (2026). https://docs.memcached.org/

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
