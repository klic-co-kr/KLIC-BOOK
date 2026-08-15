---
id: ch23
title: Queue·Durable Log·Delivery Semantics
part: data-events
order: 23
status: draft
freshness: durable
last_verified: '2026-08-06'
review_due: '2028-08-06'
upstream_lineage:
- source: system-design-primer
  file: README.md
  anchor: asynchronism
  action: REWRITE
audiences:
- backend-engineer
- platform-engineer
prerequisites:
- ch08
- ch09
- ch18
learning_objectives:
- 작업 queue와 durable log의 목적을 구분한다.
- at-most/at-least/effectively-once 의미를 설명한다.
- consumer lag·retry·dead-letter·순서를 운영한다.
figures:
- fig-ch23-01
- fig-ch23-02
sources:
- kafka-docs
- rabbitmq-reliability
- kafka-transactions
draft_notice: 기술·편집·접근성 검수 전 초고
---

## 23. Queue·Durable Log·Delivery Semantics

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

### 이 장에서 해결할 문제

메시징 시스템이 “exactly once”를 광고해도 외부 DB·API의 업무 효과까지 자동으로 한 번만 일어나지는 않는다. broker 전달 의미, consumer 상태 commit, 외부 부작용을 하나의 처리 프로토콜로 설계해야 한다.

이 절의 기준 출처: [@kafka-docs; @rabbitmq-reliability].

#### 학습 목표

- 작업 queue와 durable log의 목적을 구분한다.
- at-most/at-least/effectively-once 의미를 설명한다.
- consumer lag·retry·dead-letter·순서를 운영한다.

### 먼저 결론

- queue는 작업 분배와 경쟁 소비, durable log는 순서 보존·replay·다중 소비에 강하다.
- at-least-once는 중복을 정상 조건으로 보며 consumer 멱등성이 필요하다.
- 순서는 전체가 아니라 partition/key 범위로 정의한다.
- dead-letter queue는 최종 저장소가 아니라 원인·재처리·소유자가 있는 운영 workflow다.

### 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | Queue·Durable Log·Delivery Semantics에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | queue는 작업 분배와 경쟁 소비, durable log는 순서 보존·replay·다중 소비에 강하다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | partition key가 순서와 병렬성의 단위이므로 cardinality와 skew를 분석한다. |
| 실패·복구 | “Poison message” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | 시도 한도, 격리, skip 정책과 수동 승인 replay를 둔다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | 메시지에 필요한 최소 개인정보만 넣고 payload 암호화·retention을 적용한다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | publish latency·error·duplicate producer |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

### 핵심 개념

#### Work queue

메시지 하나를 대개 한 consumer가 처리하도록 작업을 분배한다.

#### Durable log

append된 record를 offset 순서로 보존하고 여러 consumer가 각자 읽는다.

#### At-most-once

중복은 줄지만 실패 시 유실될 수 있는 전달 의미다.

#### At-least-once

유실을 줄이기 위해 확인 전 재전달하며 중복이 가능하다.

#### Effectively-once

중복 전달이 있어도 idempotency·transaction·dedup으로 업무 결과를 한 번처럼 만든다.

#### Consumer group

partition을 consumer 집합에 할당해 병렬 처리한다.

#### Dead-letter

정책상 자동 재시도를 멈춘 메시지를 조사·수정·재처리하기 위한 격리 경로다.

핵심 개념의 정의와 범위는 [@kafka-docs; @rabbitmq-reliability; @kafka-transactions]를 기준으로 재검토해야 한다.

### 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| Producer | message ID·key·schema·timestamp를 포함해 발행한다. |
| Broker/Log | 내구성·복제·partition 순서를 제공한다. |
| Consumer group | partition을 나눠 처리한다. |
| Inbox/Dedup store | 처리한 message ID와 결과를 보존한다. |
| Side-effect target | DB·외부 API·파일 등 실제 업무 효과를 수행한다. |
| Retry scheduler | backoff와 시도 횟수를 관리한다. |
| DLQ workflow | 분류·수정·승인·replay를 수행한다. |

<!-- figure-spec
id: fig-ch23-01
chapter: ch23
role: delivery-timeline
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch23-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: effect·ack·crash 순서에 따라 유실·중복이 생기는 세 시나리오를 비교한다.
required_labels_ko:
- Producer
- Broker
- Consumer
- DB/API
- ACK
- Crash
- 중복
- 유실
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- kafka-docs
- rabbitmq-reliability
- kafka-transactions
alt_ko: effect·ack·crash 순서에 따라 유실·중복이 생기는 세 시나리오를 비교한다.
caption_ko: effect·ack·crash 순서에 따라 유실·중복이 생기는 세 시나리오를 비교한다
status: specified
spec_file: assets/specs/svg/fig-ch23-01.md
-->

> **시각자료 제작 위치 — effect·ack·crash 순서에 따라 유실·중복이 생기는 세 시나리오를 비교한다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch23-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch23-01.md`  
> 대체 텍스트: effect·ack·crash 순서에 따라 유실·중복이 생기는 세 시나리오를 비교한다.


### 요청·데이터 흐름

1. producer가 stable message ID와 partition key를 만든다.
2. broker가 configured durability 조건으로 record를 저장한다.
3. consumer가 message와 현재 offset을 읽는다.
4. dedup/inbox에서 이미 처리됐는지 확인한다.
5. 업무 transaction과 처리 표시를 가능한 한 원자적으로 커밋한다.
6. 성공 후 offset/ack를 전진시킨다.
7. 실패는 retry class와 backoff를 적용하고 한도 초과 시 DLQ workflow로 보낸다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

### 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| Work queue | 작업 분배·ack·redelivery가 단순하다. | 긴 replay·여러 독립 구독자·과거 재처리에 제한이 있다. | email·thumbnail·batch job |
| Durable log | replay·다중 consumer·partition 순서에 강하다. | offset·retention·rebalancing·hot partition 운영이 필요하다. | event streaming·CDC |
| DB-backed queue | 업무 transaction과 enqueue를 같은 DB에서 처리하기 쉽다. | 대규모 fan-out·retention·broker 기능이 제한될 수 있다. | 초기 시스템·outbox dispatcher |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@kafka-docs; @rabbitmq-reliability; @kafka-transactions]를 참조한다.

### 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| Poison message | 항상 실패하는 record가 partition 진전을 막는다. | 시도 한도, 격리, skip 정책과 수동 승인 replay를 둔다. |
| Ack before effect | 업무 처리 전에 ack해 consumer crash 시 유실된다. | effect와 처리 표시 후 ack한다. |
| Effect before ack | 업무 처리 후 ack 전 crash로 중복 실행된다. | idempotency key와 dedup store를 사용한다. |
| Rebalance storm | 느린 처리·불안정 consumer로 partition 소유권이 계속 바뀐다. | 처리 시간을 제한하고 heartbeat·static membership을 조정한다. |
| Lag runaway | 도착률이 처리율을 넘어 retention 전에 따라잡지 못한다. | backpressure, scale, priority, load shedding, retention 경보를 둔다. |

<!-- figure-spec
id: fig-ch23-02
chapter: ch23
role: queue-vs-log
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch23-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: work queue의 경쟁 소비와 durable log의 partition·offset·다중 consumer를 비교한다.
required_labels_ko:
- Work Queue
- Durable Log
- Consumer Group
- Partition
- Offset
- Replay
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- kafka-docs
- rabbitmq-reliability
- kafka-transactions
alt_ko: work queue의 경쟁 소비와 durable log의 partition·offset·다중 consumer를 비교한다.
caption_ko: work queue의 경쟁 소비와 durable log의 partition·offset·다중 consumer를 비교한다
status: specified
spec_file: assets/specs/svg/fig-ch23-02.md
-->

> **시각자료 제작 위치 — work queue의 경쟁 소비와 durable log의 partition·offset·다중 consumer를 비교한다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch23-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch23-02.md`  
> 대체 텍스트: work queue의 경쟁 소비와 durable log의 partition·offset·다중 consumer를 비교한다.


### 확장 전략

- partition key가 순서와 병렬성의 단위이므로 cardinality와 skew를 분석한다.
- consumer scale-out보다 downstream capacity와 transaction 시간을 먼저 확인한다.
- 큰 message는 object storage 참조로 분리한다.
- replay는 정상 트래픽과 격리하고 side effect가 다시 안전한지 검증한다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

### 보안과 개인정보

- 메시지에 필요한 최소 개인정보만 넣고 payload 암호화·retention을 적용한다.
- producer·consumer 권한을 topic·queue·operation 단위로 제한한다.
- DLQ가 보안 통제를 우회한 장기 개인정보 저장소가 되지 않게 한다.
- schema와 deserializer를 악성 payload·크기 공격에 대비한다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

### 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- publish latency·error·duplicate producer
- consumer lag·oldest message age·throughput
- processing latency·retry·DLQ·poison rate
- rebalance·partition skew·hot key
- dedup hit·idempotency conflict·replay 결과

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

### 비용과 운영 복잡도

- durable log retention과 replication은 저장·network 비용을 만든다.
- 긴 backlog는 처리 비용뿐 아니라 recovery 시간과 downstream burst를 키운다.
- DLQ 수동 운영은 숨은 인건비이므로 원인별 자동화와 소유권이 필요하다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

### 흔한 오해와 안티패턴

- broker가 exactly-once라면 외부 API도 한 번만 호출된다고 생각한다.
- DLQ로 보내면 문제가 해결됐다고 본다.
- 모든 메시지에 전역 순서를 요구한다.
- consumer 수만 늘리면 lag가 줄어든다고 가정한다.

### 설계 리뷰

- [ ] 업무 효과의 멱등성 경계가 어디인가?
- [ ] ack/offset과 DB commit 순서가 crash 시나리오에서 안전한가?
- [ ] partition key가 순서와 병렬성 요구를 만족하는가?
- [ ] retry·DLQ·replay에 소유자와 정책이 있는가?
- [ ] lag가 retention과 복구 목표 안에 있는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

### 연습문제

1. 결제 완료 webhook을 at-least-once로 처리하는 inbox/dedup transaction을 설계하라.
2. 순서가 필요한 고객별 이벤트와 순서가 필요 없는 이미지 작업의 partition 전략을 비교하라.
3. DLQ 10만 건을 안전하게 replay하는 rate limit·검증 절차를 작성하라.

### 핵심 요약

- queue와 durable log는 다른 소비·replay 모델을 가진다.
- at-least-once에서는 중복이 정상이다.
- effectively-once는 업무 경계의 idempotency로 만든다.
- 순서는 partition 범위로 제한한다.
- DLQ와 replay는 운영 workflow다.

### 출처

- [@kafka-docs] Apache Software Foundation. **Apache Kafka Documentation** (2026). https://kafka.apache.org/documentation/
- [@rabbitmq-reliability] Broadcom. **RabbitMQ Reliability Guide** (2026). https://www.rabbitmq.com/docs/reliability
- [@kafka-transactions] Apache Software Foundation. **Apache Kafka — Design: Transactions** (2026). https://kafka.apache.org/documentation/#semantics

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
