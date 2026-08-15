---
id: ch10
title: 복제·Quorum·Failover
part: distributed-foundations
order: 10
status: draft
freshness: durable
last_verified: '2026-08-06'
review_due: '2028-08-06'
upstream_lineage:
- source: system-design-primer
  file: README.md
  anchor: replication
  action: REPLACE
audiences:
- backend-engineer
- platform-engineer
prerequisites:
- ch06
- ch07
- ch09
learning_objectives:
- 복제의 목적과 acknowledgement 조건을 구분한다.
- read/write quorum과 복제 지연을 계산한다.
- failover에서 데이터 손실·중복 leader·재동기화를 다룬다.
figures:
- chart-ch10-01
- fig-ch10-01
- fig-ch10-02
sources:
- raft-paper
- dynamo-paper
- spanner-paper
draft_notice: 기술·편집·접근성 검수 전 초고
---

## 10. 복제·Quorum·Failover

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

### 이 장에서 해결할 문제

복제는 읽기 확장, 장애 대응, 지역 지연, 내구성을 위해 사용되지만 이 목적들은 같은 구성을 요구하지 않는다. 쓰기 성공 시점, replica 적용 시점, leader 승격 조건을 명시하지 않으면 장애 중 데이터 손실과 split brain을 설명할 수 없다.

이 절의 기준 출처: [@raft-paper; @dynamo-paper].

#### 학습 목표

- 복제의 목적과 acknowledgement 조건을 구분한다.
- read/write quorum과 복제 지연을 계산한다.
- failover에서 데이터 손실·중복 leader·재동기화를 다룬다.

### 먼저 결론

- Primary/Replica 또는 Leader/Follower 용어로 역할과 쓰기 소유권을 명확히 한다.
- 동기 복제는 acknowledgement 지연을 늘리고 비동기 복제는 데이터 손실 창을 만든다.
- `R + W > N` 같은 식은 replica 집합과 실패 모델이 동일할 때만 의미가 있다.
- failover는 선출뿐 아니라 fencing·client 재연결·재동기화·failback을 포함한다.

### 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | 복제·Quorum·Failover에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | Primary/Replica 또는 Leader/Follower 용어로 역할과 쓰기 소유권을 명확히 한다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | 읽기 replica를 늘리기 전에 복제 로그·leader I/O·connection fan-out 한계를 확인한다. |
| 실패·복구 | “미복제 커밋 손실” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | 동기 acknowledgement 또는 손실 허용 RPO를 명시한다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | 승격 권한과 membership 변경 권한을 최소화하고 감사한다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | replica apply/flush lag와 WAL backlog |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

<!-- figure-spec
id: chart-ch10-01
chapter: ch10
role: replication-lag-rpo
kind: data-chart
generator: python-matplotlib
output: assets/charts/chart-ch10-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 쓰기율과 복제 지연 증가가 비동기 failover 시 손실 가능 record 수를 어떻게 늘리는지 보여준다.
required_labels_ko:
- 복제 지연(초)
- 손실 노출 record 수
- 1k writes/s
- 10k writes/s
prohibited:
- 출처 없는 실측 수치
- 3D chart
- 잘린 축
- 색상만으로 구분
source_refs:
- raft-paper
- dynamo-paper
alt_ko: 쓰기율과 복제 지연 증가가 비동기 failover 시 손실 가능 record 수를 어떻게 늘리는지 보여준다.
caption_ko: 복제 지연과 데이터 손실 노출 창
status: specified
spec_file: assets/specs/charts/chart-ch10-01.md
-->

> **시각자료 제작 위치 — 복제 지연과 데이터 손실 노출 창**  
> 종류: `data-chart` · 상태: `specified` · 산출 경로: `assets/charts/chart-ch10-01.svg`  
> 제작 명세: `assets/specs/charts/chart-ch10-01.md`  
> 대체 텍스트: 쓰기율과 복제 지연 증가가 비동기 failover 시 손실 가능 record 수를 어떻게 늘리는지 보여준다.


### 핵심 개념

#### 복제 계수 N

하나의 데이터 항목을 보유하는 replica 수다.

#### 쓰기 quorum W

성공 응답 전에 확인받아야 하는 replica 수다.

#### 읽기 quorum R

읽기에서 조회하거나 비교하는 replica 수다.

#### 복제 지연

leader 커밋과 follower 적용 사이 시간이다.

#### Commit index

합의된 로그에서 안전하게 적용할 수 있는 위치다.

#### Fencing

이전 leader가 뒤늦게 쓰기를 계속하지 못하도록 epoch·term·token으로 차단하는 방법이다.

#### Failover

새 writer 선택, 트래픽 전환, 데이터 검증, 이전 writer 격리를 포함한 복구 과정이다.

핵심 개념의 정의와 범위는 [@raft-paper; @dynamo-paper; @spanner-paper]를 기준으로 재검토해야 한다.

### 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| 쓰기 leader | 순서를 부여하고 로그를 append한다. |
| 복제 로그 | 변경을 내구성 있게 전달한다. |
| Follower 집합 | 로그를 저장하고 적용해 읽기·승격 후보가 된다. |
| Membership/term 저장소 | 현재 구성과 leader epoch를 관리한다. |
| 라우터 | leader 또는 허용된 replica로 요청을 보낸다. |
| Repair/재동기화 | 누락 로그나 snapshot으로 replica를 복구한다. |
| Failover 제어 | 건강 판단, 승격, fencing, 트래픽 변경을 수행한다. |

<!-- figure-spec
id: fig-ch10-01
chapter: ch10
role: replication-ack-path
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch10-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: leader와 세 replica 사이 쓰기 로그·ack·commit 경로를 동기/비동기로 비교한다.
required_labels_ko:
- 클라이언트
- Leader
- Replica 1
- Replica 2
- Replica 3
- ACK
- Commit
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- raft-paper
- dynamo-paper
- spanner-paper
alt_ko: leader와 세 replica 사이 쓰기 로그·ack·commit 경로를 동기/비동기로 비교한다.
caption_ko: leader와 세 replica 사이 쓰기 로그·ack·commit 경로를 동기/비동기로 비교한다
status: specified
spec_file: assets/specs/svg/fig-ch10-01.md
-->

> **시각자료 제작 위치 — leader와 세 replica 사이 쓰기 로그·ack·commit 경로를 동기/비동기로 비교한다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch10-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch10-01.md`  
> 대체 텍스트: leader와 세 replica 사이 쓰기 로그·ack·commit 경로를 동기/비동기로 비교한다.


### 요청·데이터 흐름

1. 클라이언트가 idempotency key와 쓰기 요청을 보낸다.
2. leader가 현재 term을 확인하고 로그 위치를 할당한다.
3. 설정된 W 또는 다수 replica가 로그를 내구성 있게 확인한다.
4. commit 조건을 만족하면 적용하고 성공을 응답한다.
5. 읽기는 요구 일관성에 따라 leader·R replica·stale replica를 선택한다.
6. leader 장애 시 새 term을 획득한 후보만 승격한다.
7. 복구된 이전 leader는 follower로 재동기화한 뒤 트래픽을 받는다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

### 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| 비동기 Primary/Replica | 쓰기 지연이 낮고 읽기 확장이 쉽다. | 승격 시 미복제 쓰기 손실과 stale read가 가능하다. | 일반 OLTP 읽기 replica |
| 동기 다수 복제 | 승인된 쓰기의 손실 범위를 줄인다. | 느린 replica·zone 장애가 쓰기 지연과 가용성에 영향을 준다. | 원장·메타데이터 |
| Leaderless quorum | 단일 leader 병목과 일부 장애를 피한다. | 충돌·repair·sloppy quorum 의미가 복잡하다. | 분산 KV·가용성 중심 쓰기 |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@raft-paper; @dynamo-paper; @spanner-paper]를 참조한다.

### 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| 미복제 커밋 손실 | leader가 성공 응답 후 follower 전송 전 실패한다. | 동기 acknowledgement 또는 손실 허용 RPO를 명시한다. |
| Split brain | 네트워크 분할 양쪽이 writer로 동작한다. | quorum lease·term·fencing으로 단일 writer를 강제한다. |
| 복제 지연 폭증 | 대량 쓰기나 느린 replica가 적용 backlog를 만든다. | lag 기반 읽기 차단, WAL 보존, replica 재구축을 준비한다. |
| Failover 반복 | 불안정한 감지로 leader가 계속 바뀌고 처리량이 붕괴한다. | 히스테리시스, 최소 안정 시간, 수동 승인 단계를 둔다. |
| 재동기화 포화 | 복구 replica의 snapshot 전송이 정상 트래픽 I/O를 압박한다. | 속도 제한, 별도 네트워크, 점진 재가입을 사용한다. |

<!-- figure-spec
id: fig-ch10-02
chapter: ch10
role: failover-fencing
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch10-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: leader 장애 감지부터 새 term 획득·fencing·트래픽 전환·재동기화까지 보여준다.
required_labels_ko:
- 이전 Leader
- 새 Leader
- Term
- Fencing Token
- 라우터
- 재동기화
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- raft-paper
- dynamo-paper
- spanner-paper
alt_ko: leader 장애 감지부터 새 term 획득·fencing·트래픽 전환·재동기화까지 보여준다.
caption_ko: leader 장애 감지부터 새 term 획득·fencing·트래픽 전환·재동기화까지 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch10-02.md
-->

> **시각자료 제작 위치 — leader 장애 감지부터 새 term 획득·fencing·트래픽 전환·재동기화까지 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch10-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch10-02.md`  
> 대체 텍스트: leader 장애 감지부터 새 term 획득·fencing·트래픽 전환·재동기화까지 보여준다.


### 확장 전략

- 읽기 replica를 늘리기 전에 복제 로그·leader I/O·connection fan-out 한계를 확인한다.
- geo replica는 사용자 지연을 줄이지만 데이터 전송과 staleness를 늘린다.
- 재구축 시간이 RTO보다 길어지지 않도록 snapshot 주기와 데이터 크기를 관리한다.
- hot shard는 replica 수보다 파티셔닝·쓰기 분산이 먼저 필요할 수 있다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

### 보안과 개인정보

- 승격 권한과 membership 변경 권한을 최소화하고 감사한다.
- 복제 채널을 상호 인증·암호화한다.
- 삭제·권한 변경이 stale replica에서 되살아나지 않도록 tombstone과 버전 정책을 둔다.
- backup용 replica가 운영 접근 통제를 우회하지 않게 한다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

### 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- replica apply/flush lag와 WAL backlog
- quorum 성공·timeout·unavailable 비율
- leader term 변경·failover·fencing 거부 건수
- 읽기 staleness와 read repair
- snapshot 전송량·재구축 예상 시간

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

### 비용과 운영 복잡도

- 동기 replica를 먼 region에 두면 지연과 전송 비용이 커진다.
- 읽기 replica는 쿼리 부하를 분산하지만 저장·백업·patch 비용을 늘린다.
- 빠른 failover를 위해 상시 대기 용량과 자동화에 투자해야 한다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

### 흔한 오해와 안티패턴

- replication factor 3이면 데이터 손실이 불가능하다고 말한다.
- health check 실패만으로 즉시 다른 writer를 승격한다.
- replica lag를 보지 않고 모든 읽기를 follower로 보낸다.
- failover 성공만 확인하고 이전 leader fencing과 failback을 생략한다.

### 설계 리뷰

- [ ] 쓰기 성공 응답이 의미하는 내구성 범위가 명확한가?
- [ ] R·W·N과 failure domain 배치가 일치하는가?
- [ ] 이전 leader가 쓰지 못하도록 fencing되는가?
- [ ] 복제 지연과 WAL 보존이 재구축 시간을 감당하는가?
- [ ] failover·재동기화·failback을 실제로 연습했는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

### 연습문제

1. N=3에서 W=2, R=2인 경우와 W=1, R=1인 경우의 보장 차이를 설명하라.
2. 비동기 replica 승격 시 최대 데이터 손실량을 복제 지연과 쓰기율로 계산하라.
3. 두 데이터센터 간 네트워크 분할에서 단일 writer를 유지하는 fencing 절차를 설계하라.

### 핵심 요약

- 복제 목적에 따라 acknowledgement·읽기·failover 정책이 달라진다.
- 동기와 비동기는 지연과 데이터 손실 창을 교환한다.
- quorum 식은 실제 replica 집합과 장애 모델을 함께 봐야 한다.
- failover에는 fencing과 재동기화가 필수다.
- replica lag와 재구축 시간은 핵심 운영 지표다.

### 출처

- [@raft-paper] Diego Ongaro and John Ousterhout. **In Search of an Understandable Consensus Algorithm** (2014). https://raft.github.io/raft.pdf
- [@dynamo-paper] Giuseppe DeCandia et al.. **Dynamo: Amazon's Highly Available Key-value Store** (2007). https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf
- [@spanner-paper] James C. Corbett et al.. **Spanner: Google's Globally-Distributed Database** (2012). https://research.google/pubs/spanner-googles-globally-distributed-database/

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
