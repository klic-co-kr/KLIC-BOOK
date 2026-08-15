---
id: ch11
title: 파티셔닝·Sharding·Consistent Hashing
part: distributed-foundations
order: 11
status: draft
freshness: durable
last_verified: '2026-08-06'
review_due: '2028-08-06'
upstream_lineage:
- source: system-design-primer
  file: README.md
  anchor: partitioning
  action: REWRITE
audiences:
- backend-engineer
- platform-engineer
prerequisites:
- ch02
- ch07
- ch10
learning_objectives:
- 파티션 키를 접근 패턴과 불변조건으로 선택한다.
- range·hash·directory 기반 분할을 비교한다.
- 재분배·hot partition·cross-shard 작업을 설계한다.
figures:
- chart-ch11-01
- fig-ch11-01
- fig-ch11-02
sources:
- consistent-hashing
- dynamo-paper
- bigtable-paper
draft_notice: 기술·편집·접근성 검수 전 초고
---

## 11. 파티셔닝·Sharding·Consistent Hashing

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

### 이 장에서 해결할 문제

샤딩은 저장공간을 여러 서버에 나누는 기술이 아니라 데이터·부하·실패를 어떤 키로 분리할지 결정하는 모델이다. 잘못된 파티션 키는 노드를 추가해도 hot key와 cross-shard transaction을 해결하지 못한다.

이 절의 기준 출처: [@consistent-hashing; @dynamo-paper].

#### 학습 목표

- 파티션 키를 접근 패턴과 불변조건으로 선택한다.
- range·hash·directory 기반 분할을 비교한다.
- 재분배·hot partition·cross-shard 작업을 설계한다.

### 먼저 결론

- 파티션 키는 분포뿐 아니라 함께 읽고 쓰는 데이터와 트랜잭션 경계를 결정한다.
- 균등 hash는 hotspot을 줄이지만 범위 조회와 지역성을 희생한다.
- range는 순차 조회에 좋지만 최신 구간·대형 tenant가 뜨거워질 수 있다.
- 재샤딩은 정상 트래픽과 경쟁하므로 온라인 이동·검증·rollback을 설계한다.

### 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | 파티셔닝·Sharding·Consistent Hashing에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | 파티션 키는 분포뿐 아니라 함께 읽고 쓰는 데이터와 트랜잭션 경계를 결정한다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | 통계 기반 자동 split은 최대 파티션 크기와 요청률을 함께 고려한다. |
| 실패·복구 | “Hot key” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | key salting, 읽기 복제, tenant 전용 shard를 사용한다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | tenant ID가 파티션 키일 때 라우팅 메타데이터가 고객 목록을 노출하지 않게 보호한다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | shard별 데이터 크기·QPS·p99·queue depth |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

<!-- figure-spec
id: chart-ch11-01
chapter: ch11
role: shard-skew
kind: data-chart
generator: python-matplotlib
output: assets/charts/chart-ch11-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 평균 QPS는 같아도 hot tenant 때문에 상위 shard가 과부하되는 분포를 보여준다.
required_labels_ko:
- Shard ID
- QPS
- 균등 분포
- Skew 분포
prohibited:
- 출처 없는 실측 수치
- 3D chart
- 잘린 축
- 색상만으로 구분
source_refs:
- consistent-hashing
- dynamo-paper
alt_ko: 평균 QPS는 같아도 hot tenant 때문에 상위 shard가 과부하되는 분포를 보여준다.
caption_ko: 샤드 부하 불균형
status: specified
spec_file: assets/specs/charts/chart-ch11-01.md
-->

> **시각자료 제작 위치 — 샤드 부하 불균형**  
> 종류: `data-chart` · 상태: `specified` · 산출 경로: `assets/charts/chart-ch11-01.svg`  
> 제작 명세: `assets/specs/charts/chart-ch11-01.md`  
> 대체 텍스트: 평균 QPS는 같아도 hot tenant 때문에 상위 shard가 과부하되는 분포를 보여준다.


### 핵심 개념

#### 파티션

데이터와 요청을 독립적으로 배치·복제·이동할 수 있는 단위다.

#### 샤드 키

요청을 어떤 파티션으로 라우팅할지 결정하는 값이다.

#### Range partition

키 구간을 연속 범위로 나눈다.

#### Hash partition

키 hash 공간을 분할해 분포를 균등하게 만든다.

#### Consistent hashing

노드 변화 시 이동하는 키 범위를 줄이기 위해 hash ring 또는 유사한 토큰 공간을 사용한다.

#### Virtual node

물리 노드 하나가 여러 작은 token 범위를 소유해 균형과 이동 단위를 개선한다.

#### Directory routing

별도 메타데이터가 키·tenant의 위치를 직접 가리킨다.

핵심 개념의 정의와 범위는 [@consistent-hashing; @dynamo-paper; @bigtable-paper]를 기준으로 재검토해야 한다.

### 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| 파티션 맵 | 키 범위·token·tenant와 소유 노드를 관리한다. |
| 라우터 | 요청 키를 읽고 올바른 shard로 보낸다. |
| Shard replica set | 각 파티션의 저장·복제·leader를 제공한다. |
| Rebalancer | 부하·용량·장애 도메인에 따라 파티션을 이동한다. |
| Global index | 파티션 키가 아닌 조건의 검색을 지원한다. |
| Cross-shard coordinator | 불가피한 다중 shard 작업의 순서·보상·결과를 관리한다. |

<!-- figure-spec
id: fig-ch11-01
chapter: ch11
role: partition-strategies
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch11-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: range·hash·directory 파티셔닝의 라우팅과 데이터 배치를 비교한다.
required_labels_ko:
- Range
- Hash
- Directory
- 라우터
- Shard
- Global Index
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- consistent-hashing
- dynamo-paper
- bigtable-paper
alt_ko: range·hash·directory 파티셔닝의 라우팅과 데이터 배치를 비교한다.
caption_ko: range·hash·directory 파티셔닝의 라우팅과 데이터 배치를 비교한다
status: specified
spec_file: assets/specs/svg/fig-ch11-01.md
-->

> **시각자료 제작 위치 — range·hash·directory 파티셔닝의 라우팅과 데이터 배치를 비교한다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch11-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch11-01.md`  
> 대체 텍스트: range·hash·directory 파티셔닝의 라우팅과 데이터 배치를 비교한다.


### 요청·데이터 흐름

1. 접근 패턴과 함께 변경되는 aggregate를 식별한다.
2. 후보 키의 cardinality·skew·성장·tenant 크기를 분석한다.
3. range/hash/directory 방식과 secondary index 비용을 비교한다.
4. 라우터가 파티션 맵 버전과 이동 상태를 확인한다.
5. 이동 중 dual-read/forwarding 또는 ownership epoch를 적용한다.
6. 검증 후 이전 소유권을 해제하고 stale writer를 fencing한다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

### 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| Range | 범위 조회와 순차 스캔이 효율적이다. | 최신 키·특정 구간에 쓰기가 집중될 수 있다. | 시간 구간·정렬 조회 |
| Hash | 분포가 균등하고 단일 키 lookup이 단순하다. | 범위 조회와 같은 tenant 데이터 모으기가 어렵다. | 대규모 KV |
| Directory/Tenant | 대형 tenant를 독립 배치하고 이동하기 쉽다. | 메타데이터 가용성과 라우팅 cache 일관성이 필요하다. | 멀티테넌트 SaaS |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@consistent-hashing; @dynamo-paper; @bigtable-paper]를 참조한다.

### 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| Hot key | 유명 콘텐츠·대형 tenant 한 키가 한 shard 처리량을 초과한다. | key salting, 읽기 복제, tenant 전용 shard를 사용한다. |
| 재분배 폭풍 | 노드 추가 후 너무 많은 데이터가 동시에 이동한다. | 이동 budget, 우선순위, 작은 단위 migration을 적용한다. |
| Stale routing | 클라이언트가 이전 shard로 쓰기를 보낸다. | ownership epoch와 redirect, idempotency를 사용한다. |
| Cross-shard 불변조건 | 유일성·잔액·재고가 여러 shard에 걸쳐 깨진다. | 파티션 경계를 바꾸거나 조정된 원장·saga를 둔다. |
| Global index 불일치 | 원본 이동·삭제와 색인 업데이트가 어긋난다. | 버전·CDC·reconciliation으로 수렴을 검증한다. |

<!-- figure-spec
id: fig-ch11-02
chapter: ch11
role: online-resharding
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch11-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: source shard에서 target shard로 복사·변경 동기화·검증·소유권 전환하는 단계를 보여준다.
required_labels_ko:
- Source Shard
- Target Shard
- Snapshot
- 변경 로그
- 검증
- Ownership Epoch
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- consistent-hashing
- dynamo-paper
- bigtable-paper
alt_ko: source shard에서 target shard로 복사·변경 동기화·검증·소유권 전환하는 단계를 보여준다.
caption_ko: source shard에서 target shard로 복사·변경 동기화·검증·소유권 전환하는 단계를 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch11-02.md
-->

> **시각자료 제작 위치 — source shard에서 target shard로 복사·변경 동기화·검증·소유권 전환하는 단계를 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch11-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch11-02.md`  
> 대체 텍스트: source shard에서 target shard로 복사·변경 동기화·검증·소유권 전환하는 단계를 보여준다.


### 확장 전략

- 통계 기반 자동 split은 최대 파티션 크기와 요청률을 함께 고려한다.
- 대형 tenant는 shared pool에서 전용 shard로 승격 가능한 경로를 둔다.
- scatter-gather 쿼리는 fan-out 한도·timeout·partial result 정책을 갖는다.
- 파티션 수를 노드 수와 동일시하지 말고 이동 가능한 작은 단위로 유지한다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

### 보안과 개인정보

- tenant ID가 파티션 키일 때 라우팅 메타데이터가 고객 목록을 노출하지 않게 보호한다.
- 파티션 이동 중 암호화 키와 데이터 지역 정책을 보존한다.
- 삭제가 global index·cache·이전 replica에 남는 시간을 추적한다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

### 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- shard별 데이터 크기·QPS·p99·queue depth
- 키/tenant skew와 상위 hot key
- rebalance backlog·전송량·예상 완료 시간
- cross-shard 요청 비율과 fan-out 폭
- routing redirect·epoch mismatch

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

### 비용과 운영 복잡도

- 샤드 수 증가는 인스턴스 비용 외에 연결·백업·메타데이터·운영 자동화 비용을 늘린다.
- 균등 분포를 위해 over-partitioning하면 작은 파티션 관리 비용이 생긴다.
- global secondary index는 읽기 편의 대신 쓰기 증폭과 저장 비용을 만든다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

### 흔한 오해와 안티패턴

- 사용자 ID를 습관적으로 샤드 키로 선택한다.
- 노드 수만큼 샤드를 만들어 이동 단위를 지나치게 크게 만든다.
- consistent hashing이 hot key를 해결한다고 생각한다.
- 재샤딩을 offline maintenance로만 가정한다.

### 설계 리뷰

- [ ] 파티션 키가 핵심 aggregate와 불변조건을 함께 보존하는가?
- [ ] 키 분포의 p99 tenant와 hot key를 분석했는가?
- [ ] 재분배 중 stale routing과 이중 쓰기를 처리하는가?
- [ ] scatter-gather와 global index 비용이 제한되는가?
- [ ] 데이터 지역·삭제 정책이 이동 중 유지되는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

### 연습문제

1. 시간 기반 이벤트를 range partition할 때 최신 파티션 hotspot을 완화하는 방법을 설계하라.
2. tenant 크기가 1MB에서 10TB까지 분포하는 SaaS의 shard 정책을 작성하라.
3. 4개 노드에서 5개 노드로 consistent hash ring을 확장할 때 이동 단위를 설명하라.

### 핵심 요약

- 샤딩의 핵심은 파티션 키와 데이터 경계다.
- range·hash·directory는 서로 다른 조회와 운영 비용을 가진다.
- hot key는 균등 hash만으로 해결되지 않는다.
- 온라인 재분배와 ownership fencing이 필요하다.
- cross-shard 작업은 데이터 모델 문제로 되돌아가 검토한다.

### 출처

- [@consistent-hashing] David Karger et al.. **Consistent Hashing and Random Trees** (1997). https://doi.org/10.1145/258533.258660
- [@dynamo-paper] Giuseppe DeCandia et al.. **Dynamo: Amazon's Highly Available Key-value Store** (2007). https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf
- [@bigtable-paper] Fay Chang et al.. **Bigtable: A Distributed Storage System for Structured Data** (2006). https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
