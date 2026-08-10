---
id: ch24
title: Event Streaming·CDC·Outbox·Saga
part: data-events
order: 24
status: draft
freshness: current
last_verified: '2026-08-06'
review_due: '2027-02-06'
upstream_lineage:
- source: new-2026-edition
  file: null
  anchor: null
  action: ADD
audiences:
- backend-engineer
- platform-engineer
prerequisites:
- ch08
- ch23
learning_objectives:
- DB 변경을 이벤트로 전달하는 안전한 경로를 설계한다.
- outbox와 CDC의 원자성 경계를 설명한다.
- saga의 보상·timeout·관찰 가능성을 구현한다.
figures:
- fig-ch24-01
- fig-ch24-02
sources:
- debezium-docs
- kafka-docs
- saga-paper
draft_notice: 기술·편집·접근성 검수 전 초고
---

# 24. Event Streaming·CDC·Outbox·Saga

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

## 이 장에서 해결할 문제

이벤트 기반 아키텍처는 transaction을 없애지 않는다. 각 서비스 내부 transaction은 유지하고, 경계를 넘는 상태 변화는 outbox·CDC·멱등 consumer·보상으로 연결한다. 이벤트는 사실의 기록이어야 하며 명령과 통지의 의미를 구분해야 한다.

이 절의 기준 출처: [@debezium-docs; @kafka-docs].

### 학습 목표

- DB 변경을 이벤트로 전달하는 안전한 경로를 설계한다.
- outbox와 CDC의 원자성 경계를 설명한다.
- saga의 보상·timeout·관찰 가능성을 구현한다.

## 먼저 결론

- DB commit과 event publish를 별도 dual write로 수행하지 않는다.
- outbox는 업무 상태와 발행할 record를 같은 local transaction에 저장한다.
- CDC는 DB log에서 변경을 읽지만 schema·snapshot·순서·삭제 의미를 관리해야 한다.
- saga 보상은 rollback이 아니라 이미 일어난 업무를 상쇄하는 새 업무다.

::: current-note
**2026-08-06 확인:** 이 장은 변화 가능한 표준·프로젝트·AI 구현을 포함한다. 기본 재검토일은 `2027-02-06`이며, 출판 직전 공식 문서를 다시 확인한다.
:::

## 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | Event Streaming·CDC·Outbox·Saga에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | DB commit과 event publish를 별도 dual write로 수행하지 않는다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | aggregate key와 event partition을 맞춰 필요한 순서만 유지한다. |
| 실패·복구 | “Dual-write gap” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | transactional outbox 또는 log CDC를 사용한다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | CDC 계정은 필요한 table/log 권한만 갖고 secret rotation을 지원한다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | outbox age·pending row·publish latency |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

## 핵심 개념

### Domain event

도메인에서 이미 발생한 사실을 과거형으로 표현한 record다.

### Command

특정 수신자에게 작업 수행을 요청하며 거부될 수 있다.

### Transactional outbox

업무 변경과 발행 record를 같은 DB transaction에 저장하는 패턴이다.

### CDC

database change log를 읽어 삽입·수정·삭제를 event stream으로 전달하는 방식이다.

### Saga

여러 local transaction과 보상 action을 순서·이벤트로 조정하는 장기 업무 과정이다.

### Orchestration

중앙 coordinator가 다음 단계와 보상을 결정한다.

### Choreography

서비스들이 event에 반응해 분산적으로 다음 단계를 진행한다.

### Reconciliation

최종 상태와 원장 증거를 비교해 누락·불일치를 찾는 과정이다.

핵심 개념의 정의와 범위는 [@debezium-docs; @kafka-docs; @saga-paper]를 기준으로 재검토해야 한다.

## 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| Service DB | local transaction과 outbox를 보존한다. |
| CDC connector | log position을 추적하며 outbox 변경을 읽는다. |
| Event log | schema·key·ordering을 가진 record를 보존한다. |
| Consumer inbox | 중복 event와 처리 상태를 기록한다. |
| Saga coordinator | 상태·deadline·보상 순서를 관리한다. |
| Participant service | 각 local transaction과 idempotent command를 수행한다. |
| Reconciler | 장기 미완료·불일치·DLQ를 탐지하고 복구한다. |

<!-- figure-spec
id: fig-ch24-01
chapter: ch24
role: outbox-cdc-flow
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch24-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 서비스 transaction이 업무 row와 outbox를 커밋하고 CDC·broker·inbox로 전달되는 흐름을 보여준다.
required_labels_ko:
- Service DB
- 업무 Row
- Outbox
- CDC
- Event Log
- Consumer Inbox
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- debezium-docs
- kafka-docs
- saga-paper
alt_ko: 서비스 transaction이 업무 row와 outbox를 커밋하고 CDC·broker·inbox로 전달되는 흐름을 보여준다.
caption_ko: 서비스 transaction이 업무 row와 outbox를 커밋하고 CDC·broker·inbox로 전달되는 흐름을 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch24-01.md
-->

> **시각자료 제작 위치 — 서비스 transaction이 업무 row와 outbox를 커밋하고 CDC·broker·inbox로 전달되는 흐름을 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch24-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch24-01.md`  
> 대체 텍스트: 서비스 transaction이 업무 row와 outbox를 커밋하고 CDC·broker·inbox로 전달되는 흐름을 보여준다.


## 요청·데이터 흐름

1. 업무 service가 상태 변경과 outbox insert를 한 transaction으로 커밋한다.
2. CDC가 log position을 보존하며 outbox row를 event로 변환한다.
3. broker가 aggregate key 기준 순서를 유지한다.
4. consumer가 inbox에서 event ID를 확인하고 local transaction을 수행한다.
5. saga coordinator가 성공·실패·timeout에 따라 다음 command를 보낸다.
6. 보상은 별도 idempotency key와 상태 전이를 가진다.
7. 완료·실패·수동 개입 상태를 end-to-end로 관측한다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

## 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| Outbox polling | DB 기능 의존이 낮고 구현을 이해하기 쉽다. | poll latency·lock·청소·중복을 관리해야 한다. | 보통 규모와 단순 운영 |
| Log-based CDC | 낮은 지연과 전체 변경 capture에 유리하다. | DB별 connector·schema·snapshot·권한이 복잡하다. | 대규모 event integration |
| Saga orchestration | 상태와 장애 경로가 중앙에서 명확하다. | coordinator 의존과 결합이 생긴다. | 결제·재고처럼 단계가 중요 |
| Saga choreography | 서비스 자율성과 확장이 좋다. | 전체 흐름·loop·보상 추적이 어렵다. | 단순 반응형 통합 |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@debezium-docs; @kafka-docs; @saga-paper]를 참조한다.

## 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| Dual-write gap | DB는 커밋됐지만 publish가 실패해 event가 영구 누락된다. | transactional outbox 또는 log CDC를 사용한다. |
| CDC position loss | connector가 잘못된 offset에서 재시작해 누락·대량 중복이 생긴다. | position checkpoint·snapshot 모드·reconciliation을 검증한다. |
| Schema drift | DB column 변경이 downstream consumer를 깨뜨린다. | event envelope과 compatibility policy를 DB schema와 분리한다. |
| Compensation failure | 재고 복구나 환불 보상도 실패해 saga가 멈춘다. | 보상 retry·수동 queue·불변 원장을 둔다. |
| Event loop | 서비스들이 서로의 event에 반응해 무한 갱신한다. | causation/correlation ID와 state transition guard를 사용한다. |

<!-- figure-spec
id: fig-ch24-02
chapter: ch24
role: saga-state-machine
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch24-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 주문·재고·결제 단계의 성공·실패·timeout·보상 상태 전이를 보여준다.
required_labels_ko:
- 주문
- 재고 예약
- 결제 승인
- 완료
- Timeout
- 보상
- 수동 개입
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- debezium-docs
- kafka-docs
- saga-paper
alt_ko: 주문·재고·결제 단계의 성공·실패·timeout·보상 상태 전이를 보여준다.
caption_ko: 주문·재고·결제 단계의 성공·실패·timeout·보상 상태 전이를 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch24-02.md
-->

> **시각자료 제작 위치 — 주문·재고·결제 단계의 성공·실패·timeout·보상 상태 전이를 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch24-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch24-02.md`  
> 대체 텍스트: 주문·재고·결제 단계의 성공·실패·timeout·보상 상태 전이를 보여준다.


## 확장 전략

- aggregate key와 event partition을 맞춰 필요한 순서만 유지한다.
- CDC connector와 broker를 scale-out하기 전에 DB log retention과 source I/O를 확인한다.
- saga state는 무한히 커지지 않게 terminal state archive와 retention을 둔다.
- replay 시 신규 side effect를 차단하거나 별도 sandbox consumer를 사용한다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

## 보안과 개인정보

- CDC 계정은 필요한 table/log 권한만 갖고 secret rotation을 지원한다.
- event payload의 개인정보를 최소화하고 삭제·암호화·retention 정책을 적용한다.
- 보상·수동 승인 작업은 강한 권한과 감사 trail을 요구한다.
- event provenance와 schema signature로 위조·오염을 탐지한다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

## 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- outbox age·pending row·publish latency
- CDC lag·source log retention margin·snapshot status
- consumer inbox duplicate·processing latency
- saga state별 체류 시간·timeout·compensation failure
- reconciliation mismatch·manual intervention

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

## 비용과 운영 복잡도

- outbox/CDC는 broker·connector·storage·on-call 비용을 추가한다.
- saga는 lock을 오래 잡지 않지만 상태 기계·보상·수동 처리 비용을 만든다.
- 모든 DB 변경을 event로 내보내면 저장·보안·consumer 결합 비용이 폭증한다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

## 흔한 오해와 안티패턴

- dual write에 재시도만 추가해 안전하다고 생각한다.
- DB row 변경을 그대로 domain event로 공개한다.
- 보상을 원래 transaction의 완전한 rollback으로 가정한다.
- choreography가 중앙 결합이 없으니 항상 단순하다고 생각한다.

## 설계 리뷰

- [ ] 업무 commit과 event 생성이 같은 원자 경계에 있는가?
- [ ] event가 사실·명령·통지 중 무엇인지 명확한가?
- [ ] CDC schema·snapshot·offset 복구가 시험됐는가?
- [ ] saga의 timeout·보상 실패·수동 개입 상태가 정의됐는가?
- [ ] reconciliation이 최종 불일치를 찾는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

## 연습문제

1. 주문·결제·재고 saga를 orchestration 상태 기계로 설계하라.
2. DB schema 변경과 event schema 변경을 분리하는 envelope을 작성하라.
3. outbox dispatcher가 같은 row를 두 번 발행해도 안전한 consumer를 설계하라.

## 핵심 요약

- 이벤트 아키텍처도 local transaction을 필요로 한다.
- outbox는 상태 변경과 발행 record를 원자적으로 저장한다.
- CDC에는 schema·offset·snapshot·복구 운영이 필요하다.
- saga 보상은 새로운 업무 action이다.
- end-to-end reconciliation과 수동 개입이 필수다.

## 출처

- [@debezium-docs] Debezium Authors. **Debezium Documentation** (2026). https://debezium.io/documentation/reference/stable/
- [@kafka-docs] Apache Software Foundation. **Apache Kafka Documentation** (2026). https://kafka.apache.org/documentation/
- [@saga-paper] Hector Garcia-Molina and Kenneth Salem. **Sagas** (1987). https://doi.org/10.1145/38713.38742

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
