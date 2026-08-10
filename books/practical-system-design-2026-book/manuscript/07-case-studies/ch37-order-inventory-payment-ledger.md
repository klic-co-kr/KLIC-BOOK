---
id: ch37
title: 주문·재고·결제 원장 시스템
part: case-studies
order: 37
status: draft
freshness: durable
last_verified: '2026-08-06'
review_due: '2028-08-06'
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
- ch24
- ch25
- ch29
learning_objectives:
- 주문·재고·결제의 원장과 불변조건을 분리한다.
- idempotency와 saga로 장기 transaction을 처리한다.
- 금액·상태·정산을 append-only 증거로 검증한다.
figures:
- fig-ch37-01
- fig-ch37-02
- fig-ch37-03
- fig-ch37-04
- fig-ch37-05
sources:
- postgres-transaction-iso
- saga-paper
- stripe-idempotency
- debezium-docs
draft_notice: 기술·편집·접근성 검수 전 초고
---

# 37. 주문·재고·결제 원장 시스템

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

## 이 장에서 해결할 문제

전자상거래 transaction은 하나의 거대한 분산 ACID transaction으로 묶기 어렵다. 주문, 재고, 결제는 각자의 원장과 불변조건을 유지하고, reservation·authorization·capture·release·refund를 명시적 상태 기계와 idempotent command로 연결해야 한다.

이 절의 기준 출처: [@postgres-transaction-iso; @saga-paper].

### 학습 목표

- 주문·재고·결제의 원장과 불변조건을 분리한다.
- idempotency와 saga로 장기 transaction을 처리한다.
- 금액·상태·정산을 append-only 증거로 검증한다.

## 먼저 결론

- 주문 총액은 가격 snapshot과 조정 내역으로 재현 가능해야 한다.
- 재고는 가용 수량보다 reservation 원장과 만료를 명확히 한다.
- 결제 요청의 unknown outcome은 동일 idempotency key로 결과를 조회한다.
- saga 완료와 실패는 수동 개입 가능한 terminal state를 가진다.
- 회계성 금액 변화는 기존 행 덮어쓰기보다 append-only entry와 균형 검증을 사용한다.

## 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | 주문·재고·결제 원장 시스템에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | 주문 총액은 가격 snapshot과 조정 내역으로 재현 가능해야 한다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | order ID 또는 merchant/tenant로 partition하되 inventory SKU hotspot을 별도 처리한다. |
| 실패·복구 | “Double charge” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | 업무 idempotency key를 provider 요청과 내부 UNIQUE에 묶는다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | 카드 원문을 저장하지 않고 tokenized provider reference와 최소 metadata를 사용한다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | 주문 상태별 체류 시간·saga timeout |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

## 핵심 개념

### Order aggregate

상품 snapshot, 금액, 상태 전이를 소유한다.

### Inventory reservation

특정 주문을 위해 수량을 일정 시간 묶는 기록이다.

### Authorization

결제 수단의 금액 사용 가능성을 승인하는 단계다.

### Capture

승인된 금액을 실제 청구로 확정하는 단계다.

### Idempotency key

같은 업무 요청의 중복 효과를 막고 기존 결과를 찾는 키다.

### Saga state

여러 local transaction의 진행·보상·timeout을 기록한다.

### Ledger entry

금액 증감의 이유·계정·currency·reference를 append-only로 기록한다.

### Reconciliation

내부 주문·결제·공급자 정산을 비교해 차이를 찾는 과정이다.

핵심 개념의 정의와 범위는 [@postgres-transaction-iso; @saga-paper; @stripe-idempotency; @debezium-docs]를 기준으로 재검토해야 한다.

### 핵심 불변조건 예시

```text
주문 총액 = 상품 가격 snapshot 합 + 세금 + 배송비 - 할인 + 조정
재고 가용량 = 실물/논리 재고 - 활성 reservation 합
결제 잔액 = 승인/청구/환불/수수료 ledger entry의 대수적 합
```

이 식들은 구현 코드 한 곳의 계산이 아니라 DB 제약, 상태 전이 guard, reconciliation query, 운영 경보가 함께 지켜야 하는 규칙이다. 통화가 다르면 단순 합산하지 않고 currency와 minor unit을 모든 금액 entry에 보존한다.

## 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| Order service/DB | 주문 상태·가격 snapshot·workflow reference를 원장으로 관리한다. |
| Inventory service | stock movement·reservation·expiry를 관리한다. |
| Payment service | provider token·authorization·capture·refund 상태를 관리한다. |
| Saga orchestrator | command·timeout·compensation과 전체 상태를 관리한다. |
| Outbox/event log | local commit을 다른 서비스에 전달한다. |
| Ledger | 금액 entry와 balance 검증을 보존한다. |
| Reconciliation workers | provider statement·inventory count와 차이를 탐지한다. |
| Admin console | 수동 승인·보상·evidence 조회를 제공한다. |

<!-- figure-spec
id: fig-ch37-01
chapter: ch37
role: commerce-saga
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch37-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 주문 생성·재고 예약·결제 승인·확정과 실패 보상 흐름을 보여준다.
required_labels_ko:
- Order
- Inventory Reservation
- Payment Authorization
- Confirm
- Release
- Void/Refund
- Manual Review
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- postgres-transaction-iso
- saga-paper
- stripe-idempotency
alt_ko: 주문 생성·재고 예약·결제 승인·확정과 실패 보상 흐름을 보여준다.
caption_ko: 주문 생성·재고 예약·결제 승인·확정과 실패 보상 흐름을 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch37-01.md
-->

> **시각자료 제작 위치 — 주문 생성·재고 예약·결제 승인·확정과 실패 보상 흐름을 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch37-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch37-01.md`  
> 대체 텍스트: 주문 생성·재고 예약·결제 승인·확정과 실패 보상 흐름을 보여준다.


## 요청·데이터 흐름

1. client가 cart snapshot과 idempotency key로 주문 생성을 요청한다.
2. order service가 가격·세금·할인 snapshot과 pending order를 commit한다.
3. saga가 inventory reservation command를 보낸다.
4. inventory가 조건부 수량 감소 또는 reservation entry를 commit한다.
5. payment가 provider에 authorization을 같은 key로 요청한다.
6. 성공하면 주문을 confirmed하고 필요 시 capture를 진행한다.
7. 실패·timeout이면 reservation release와 authorization void/refund를 실행한다.
8. 모든 단계가 outbox로 사실 event를 발행한다.
9. reconciliation이 주문·ledger·provider 결과를 주기적으로 비교한다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

## 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| 재고 선점 후 결제 | oversell을 줄이고 결제 전에 수량을 보장한다. | 결제 실패 동안 재고가 잠기며 expiry가 필요하다. | 희소 상품 |
| 결제 승인 후 재고 | 재고 lock 시간을 줄인다. | 재고 실패 시 승인 취소·고객 경험 문제가 있다. | 재고 여유가 큰 상품 |
| 동기 orchestration | 사용자에게 빠른 최종 상태를 제공한다. | 외부 provider 지연과 timeout이 request를 길게 만든다. | 짧은 결제 flow |
| 비동기 주문 접수 | 긴 처리와 재시도를 내구 workflow로 다룬다. | pending UX·상태 조회·알림이 필요하다. | 복잡한 주문·외부 의존성 |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@postgres-transaction-iso; @saga-paper; @stripe-idempotency]를 참조한다.

## 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| Double charge | client/gateway retry가 결제 provider를 두 번 호출한다. | 업무 idempotency key를 provider 요청과 내부 UNIQUE에 묶는다. |
| Unknown payment | timeout 후 provider 승인 여부를 모른다. | 같은 key 조회·webhook·reconciliation 전에는 재청구하지 않는다. |
| Oversell | 동시 reservation이 가용 수량을 초과한다. | 조건부 update·serializable·reservation ledger를 사용한다. |
| Expired reservation race | 만료 worker와 결제 완료가 동시에 상태를 바꾼다. | versioned state transition과 terminal guard를 사용한다. |
| Partial refund | 일부 상품만 취소됐지만 ledger와 order 금액이 어긋난다. | line-level adjustment entry와 balance invariant를 둔다. |
| Provider webhook duplicate/out-of-order | 이전 상태 event가 새 상태를 덮는다. | provider event ID dedup과 monotonic state guard를 사용한다. |

<!-- figure-spec
id: fig-ch37-02
chapter: ch37
role: payment-ledger
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch37-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 결제·수수료·환불·정산이 append-only ledger entry와 balance 검증으로 연결되는 모습을 보여준다.
required_labels_ko:
- 결제 계정
- 판매자 계정
- 수수료 계정
- 환불
- 정산
- Ledger Entry
- Balance Check
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- postgres-transaction-iso
- saga-paper
- stripe-idempotency
alt_ko: 결제·수수료·환불·정산이 append-only ledger entry와 balance 검증으로 연결되는 모습을 보여준다.
caption_ko: 결제·수수료·환불·정산이 append-only ledger entry와 balance 검증으로 연결되는 모습을 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch37-02.md
-->

> **시각자료 제작 위치 — 결제·수수료·환불·정산이 append-only ledger entry와 balance 검증으로 연결되는 모습을 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch37-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch37-02.md`  
> 대체 텍스트: 결제·수수료·환불·정산이 append-only ledger entry와 balance 검증으로 연결되는 모습을 보여준다.


## 종합 설계 보조 도표

이 장은 앞의 원리를 하나의 서비스로 연결하므로 다음 보조 도표까지 제작한다.

<!-- figure-spec
id: fig-ch37-03
chapter: ch37
role: order-state-machine
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch37-03.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: pending·reserved·authorized·confirmed·cancelled·manual-review 상태 전이를 보여준다.
required_labels_ko:
- Pending
- Reserved
- Authorized
- Confirmed
- Cancelled
- Manual Review
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- postgres-transaction-iso
- saga-paper
- stripe-idempotency
alt_ko: pending·reserved·authorized·confirmed·cancelled·manual-review 상태 전이를 보여준다.
caption_ko: pending·reserved·authorized·confirmed·cancelled·manual-review 상태 전이를 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch37-03.md
-->

> **시각자료 제작 위치 — pending·reserved·authorized·confirmed·cancelled·manual-review 상태 전이를 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch37-03.svg`  
> 제작 명세: `assets/specs/svg/fig-ch37-03.md`  
> 대체 텍스트: pending·reserved·authorized·confirmed·cancelled·manual-review 상태 전이를 보여준다.


<!-- figure-spec
id: fig-ch37-04
chapter: ch37
role: idempotency-and-unknown
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch37-04.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 중복 주문·결제 timeout·결과 조회·webhook reconciliation을 보여준다.
required_labels_ko:
- Idempotency Key
- Timeout
- Unknown Outcome
- Result Lookup
- Webhook
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- postgres-transaction-iso
- saga-paper
- stripe-idempotency
alt_ko: 중복 주문·결제 timeout·결과 조회·webhook reconciliation을 보여준다.
caption_ko: 중복 주문·결제 timeout·결과 조회·webhook reconciliation을 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch37-04.md
-->

> **시각자료 제작 위치 — 중복 주문·결제 timeout·결과 조회·webhook reconciliation을 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch37-04.svg`  
> 제작 명세: `assets/specs/svg/fig-ch37-04.md`  
> 대체 텍스트: 중복 주문·결제 timeout·결과 조회·webhook reconciliation을 보여준다.


<!-- figure-spec
id: fig-ch37-05
chapter: ch37
role: reconciliation
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch37-05.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 주문·재고·결제 provider·ledger를 비교해 mismatch를 수리하는 흐름을 보여준다.
required_labels_ko:
- Order DB
- Inventory Ledger
- Payment Provider
- Internal Ledger
- Mismatch
- Repair
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- postgres-transaction-iso
- saga-paper
- stripe-idempotency
alt_ko: 주문·재고·결제 provider·ledger를 비교해 mismatch를 수리하는 흐름을 보여준다.
caption_ko: 주문·재고·결제 provider·ledger를 비교해 mismatch를 수리하는 흐름을 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch37-05.md
-->

> **시각자료 제작 위치 — 주문·재고·결제 provider·ledger를 비교해 mismatch를 수리하는 흐름을 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch37-05.svg`  
> 제작 명세: `assets/specs/svg/fig-ch37-05.md`  
> 대체 텍스트: 주문·재고·결제 provider·ledger를 비교해 mismatch를 수리하는 흐름을 보여준다.


## 확장 전략

- order ID 또는 merchant/tenant로 partition하되 inventory SKU hotspot을 별도 처리한다.
- 예약은 bucket·warehouse·SKU 단위로 분산하고 매우 hot한 flash sale은 token/preallocation을 사용한다.
- payment provider 호출은 channel별 bulkhead·rate limit·fallback을 둔다.
- ledger append와 reconciliation query를 분리해 원장 쓰기를 보호한다.
- saga terminal state를 archive하되 감사 증거는 보존 정책에 따라 유지한다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

## 보안과 개인정보

- 카드 원문을 저장하지 않고 tokenized provider reference와 최소 metadata를 사용한다.
- 금액·수취인·환불 같은 고위험 action은 강한 권한·승인·감사를 요구한다.
- admin console은 사용자 서비스와 별도 trust zone과 break-glass를 둔다.
- webhook signature·timestamp·replay를 검증한다.
- 개인정보 삭제와 금융·세무 보존 의무의 우선순위를 정책으로 관리한다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

## 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- 주문 상태별 체류 시간·saga timeout
- inventory available/reserved/expired·oversell guard
- payment authorization/capture/refund·unknown outcome
- idempotency duplicate/conflict
- ledger imbalance·reconciliation mismatch
- provider latency·webhook lag·manual intervention

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

## 비용과 운영 복잡도

- 결제 provider fee·retry·fraud review·chargeback이 transaction 비용에 포함된다.
- 재고 reservation을 길게 유지하면 판매 기회 비용이 생긴다.
- 강한 원장·audit·reconciliation은 인프라와 인력 비용이지만 금액 불일치 기대 손실을 줄인다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

## 흔한 오해와 안티패턴

- 주문 상태 열 하나를 여러 서비스가 직접 수정한다.
- timeout이면 결제가 실패했다고 단정해 새 요청을 보낸다.
- 재고 수량 하나만 감소시키고 reservation 증거를 남기지 않는다.
- 환불을 기존 결제 row 금액 덮어쓰기로 표현한다.

## 설계 리뷰

- [ ] 주문·재고·결제 각각의 원장과 불변조건이 명확한가?
- [ ] 모든 command와 webhook이 idempotent한가?
- [ ] unknown outcome·timeout·보상 실패 상태가 있는가?
- [ ] ledger와 provider reconciliation이 자동화됐는가?
- [ ] 수동 개입이 권한·증거·재실행 안전성을 갖는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

## 연습문제

1. 동일 주문이 3번 제출돼도 한 번만 결제되는 idempotency table을 설계하라.
2. 재고 reservation과 결제 authorization의 timeout race를 상태 기계로 해결하라.
3. 부분 환불을 double-entry 형태의 append-only entry로 표현하라.

## 핵심 요약

- 주문·재고·결제는 각자의 원장과 불변조건을 가진다.
- 장기 업무는 saga와 idempotent command로 연결한다.
- 결제 timeout은 unknown outcome일 수 있다.
- reservation·authorization·capture·refund를 상태로 모델링한다.
- ledger와 reconciliation이 금액 정확성을 증명한다.

## 출처

- [@postgres-transaction-iso] PostgreSQL Global Development Group. **PostgreSQL Documentation — Transaction Isolation** (2026). https://www.postgresql.org/docs/current/transaction-iso.html
- [@saga-paper] Hector Garcia-Molina and Kenneth Salem. **Sagas** (1987). https://doi.org/10.1145/38713.38742
- [@stripe-idempotency] Stripe. **Stripe API — Idempotent requests** (2026). https://docs.stripe.com/api/idempotent_requests
- [@debezium-docs] Debezium Authors. **Debezium Documentation** (2026). https://debezium.io/documentation/reference/stable/

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
