---
id: ch08
title: 트랜잭션·격리 수준·MVCC
part: distributed-foundations
order: 8
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
- ch07
learning_objectives:
- 원자성·격리·내구성을 실제 실패와 연결한다.
- 격리 수준별 이상 현상을 설명한다.
- MVCC가 읽기와 쓰기 충돌을 관리하는 방식을 이해한다.
figures:
- fig-ch08-01
- fig-ch08-02
sources:
- postgres-transaction-iso
- postgres-mvcc
draft_notice: 기술·편집·접근성 검수 전 초고
---

## 08. 트랜잭션·격리 수준·MVCC

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

### 이 장에서 해결할 문제

트랜잭션은 여러 SQL 문을 한 묶음으로 만드는 문법이 아니라 실패 중에도 불변조건을 보존하는 계약이다. 격리 수준 이름만 믿지 말고 애플리케이션이 막아야 할 write skew, lost update, phantom을 구체적 테스트로 확인해야 한다.

이 절의 기준 출처: [@postgres-transaction-iso; @postgres-mvcc].

#### 학습 목표

- 원자성·격리·내구성을 실제 실패와 연결한다.
- 격리 수준별 이상 현상을 설명한다.
- MVCC가 읽기와 쓰기 충돌을 관리하는 방식을 이해한다.

### 먼저 결론

- 원자성은 중간 상태 노출을 막지만 외부 부작용까지 자동으로 되돌리지 않는다.
- 격리 수준은 동시 실행이 어떤 순서로 보이는지 결정한다.
- MVCC는 읽기 스냅샷을 제공하지만 오래 열린 트랜잭션과 vacuum 지연 비용을 만든다.
- 유일성·잔액·재고 같은 불변조건은 제약·잠금·직렬화 재시도로 지킨다.

### 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | 트랜잭션·격리 수준·MVCC에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | 원자성은 중간 상태 노출을 막지만 외부 부작용까지 자동으로 되돌리지 않는다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | 트랜잭션 범위를 최소 불변조건 단위로 좁힌다. |
| 실패·복구 | “Lost update” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | 조건부 update, 버전 열, 행 잠금을 사용한다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | 행 수준 권한과 애플리케이션 권한이 같은 트랜잭션 스냅샷에서 평가되는지 확인한다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | 트랜잭션 시간과 active transaction 수 |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

### 핵심 개념

#### 원자성

트랜잭션의 변경이 모두 반영되거나 모두 반영되지 않는 성질이다.

#### 격리

동시 트랜잭션이 서로의 중간 상태를 어떻게 관찰하는지에 대한 성질이다.

#### 내구성

커밋이 성공했다고 응답한 상태가 약속된 실패 범위에서 보존되는 성질이다.

#### MVCC

여러 버전의 행을 유지해 읽기 스냅샷과 동시 쓰기를 조정하는 방식이다.

#### Write skew

서로 다른 행을 수정하지만 함께 보는 조건이 깨지는 이상 현상이다.

#### 직렬화 가능성

동시 실행 결과가 어떤 직렬 실행 순서와 동등하도록 보장하는 격리 수준이다.

핵심 개념의 정의와 범위는 [@postgres-transaction-iso; @postgres-mvcc]를 기준으로 재검토해야 한다.

### 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| 트랜잭션 경계 | 하나의 불변조건을 지켜야 하는 작업 범위를 정의한다. |
| 제약 조건 | UNIQUE, CHECK, FK 등 DB가 직접 검증하는 규칙이다. |
| 버전 저장소 | 스냅샷별로 보이는 행 버전을 관리한다. |
| 잠금 관리자 | 행·범위·predicate 충돌을 조정한다. |
| WAL/로그 | 커밋 복구와 복제를 위한 순서를 기록한다. |
| 재시도 계층 | serialization failure·deadlock을 안전하게 다시 실행한다. |

<!-- figure-spec
id: fig-ch08-01
chapter: ch08
role: isolation-anomalies
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch08-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 격리 수준별 dirty read·nonrepeatable read·phantom·write skew 가능성을 비교한다.
required_labels_ko:
- Read Committed
- Repeatable Read
- Serializable
- Lost Update
- Write Skew
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- postgres-transaction-iso
- postgres-mvcc
alt_ko: 격리 수준별 dirty read·nonrepeatable read·phantom·write skew 가능성을 비교한다.
caption_ko: 격리 수준별 dirty read·nonrepeatable read·phantom·write skew 가능성을 비교한다
status: specified
spec_file: assets/specs/svg/fig-ch08-01.md
-->

> **시각자료 제작 위치 — 격리 수준별 dirty read·nonrepeatable read·phantom·write skew 가능성을 비교한다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch08-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch08-01.md`  
> 대체 텍스트: 격리 수준별 dirty read·nonrepeatable read·phantom·write skew 가능성을 비교한다.


### 요청·데이터 흐름

1. 요청을 idempotency key와 함께 받는다.
2. 현재 상태를 적절한 스냅샷 또는 잠금으로 읽는다.
3. 불변조건을 DB 제약과 애플리케이션 검증으로 확인한다.
4. 변경을 수행하고 커밋한다.
5. 충돌·deadlock·serialization failure는 전체 단위를 재시도한다.
6. 외부 이벤트는 outbox 등 커밋 후 전달 가능한 기록으로 분리한다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

### 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| Read Committed | 기본 비용이 낮고 각 문장은 커밋된 값만 본다. | 같은 트랜잭션 안에서도 값이 바뀌고 복합 불변조건이 깨질 수 있다. | 짧은 단일 행 CRUD |
| Repeatable Read/Snapshot | 일관된 스냅샷으로 읽기가 안정적이다. | 구현에 따라 write skew가 가능하다. | 리포트·복수 읽기 |
| Serializable | 가장 강한 격리로 복잡한 불변조건을 단순화한다. | 충돌 시 abort·재시도가 늘고 긴 트랜잭션에 불리하다. | 금융·재고·정책 변경 |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@postgres-transaction-iso; @postgres-mvcc]를 참조한다.

### 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| Lost update | 두 요청이 같은 값을 읽고 각자 계산한 뒤 하나를 덮어쓴다. | 조건부 update, 버전 열, 행 잠금을 사용한다. |
| Write skew | 두 의사가 서로가 근무 중임을 보고 각각 퇴근해 최소 인원 규칙이 깨진다. | serializable, predicate lock, 별도 집계 행을 사용한다. |
| 긴 스냅샷 | 오래 열린 트랜잭션이 오래된 버전 정리를 막아 저장량과 I/O가 증가한다. | 트랜잭션 시간을 제한하고 배치 읽기를 페이지화한다. |
| Deadlock | 서로 다른 순서로 잠금을 획득한 작업이 대기한다. | 잠금 순서를 통일하고 전체 트랜잭션을 재시도한다. |
| 외부 부작용 불일치 | DB rollback은 이미 보낸 이메일·결제 호출을 취소하지 못한다. | outbox, idempotency, 보상 워크플로를 사용한다. |

<!-- figure-spec
id: fig-ch08-02
chapter: ch08
role: mvcc-versions
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch08-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 두 트랜잭션의 스냅샷이 여러 행 버전을 다르게 보는 과정을 시간축으로 보여준다.
required_labels_ko:
- 트랜잭션 A
- 트랜잭션 B
- 행 버전
- 스냅샷
- 커밋
- 정리
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- postgres-transaction-iso
- postgres-mvcc
alt_ko: 두 트랜잭션의 스냅샷이 여러 행 버전을 다르게 보는 과정을 시간축으로 보여준다.
caption_ko: 두 트랜잭션의 스냅샷이 여러 행 버전을 다르게 보는 과정을 시간축으로 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch08-02.md
-->

> **시각자료 제작 위치 — 두 트랜잭션의 스냅샷이 여러 행 버전을 다르게 보는 과정을 시간축으로 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch08-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch08-02.md`  
> 대체 텍스트: 두 트랜잭션의 스냅샷이 여러 행 버전을 다르게 보는 과정을 시간축으로 보여준다.


### 확장 전략

- 트랜잭션 범위를 최소 불변조건 단위로 좁힌다.
- hot row를 분할하거나 append-only 원장과 비동기 집계를 사용한다.
- 읽기 전용 분석은 replica·snapshot export로 OLTP 경로와 격리한다.
- 재시도율과 lock wait가 임계치를 넘으면 데이터 모델과 경합 지점을 재설계한다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

### 보안과 개인정보

- 행 수준 권한과 애플리케이션 권한이 같은 트랜잭션 스냅샷에서 평가되는지 확인한다.
- 감사 로그는 원본 변경과 인과 관계를 유지하고 임의 수정이 어렵게 한다.
- 오류 로그에 SQL 파라미터와 개인정보를 그대로 남기지 않는다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

### 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- 트랜잭션 시간과 active transaction 수
- lock wait·deadlock·serialization failure 비율
- 오래된 snapshot age와 vacuum/compaction backlog
- 불변조건 제약 위반과 재시도 성공률
- WAL 생성량과 commit latency

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

### 비용과 운영 복잡도

- 강한 격리와 큰 트랜잭션은 경합과 로그 비용을 높인다.
- 애플리케이션에서 불변조건을 재현하면 코드·테스트·복구 비용이 늘어난다.
- OLTP와 분석을 분리하면 인프라 비용은 늘지만 장애 격리와 예측 가능성이 좋아진다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

### 흔한 오해와 안티패턴

- “ACID DB면 모든 동시성 문제가 해결된다”고 생각한다.
- 트랜잭션 안에서 외부 API를 오래 기다린다.
- serialization failure를 500 오류로 그대로 노출한다.
- read-modify-write를 조건 없는 UPDATE로 구현한다.

### 설계 리뷰

- [ ] 불변조건이 DB가 검증할 수 있는 형태인가?
- [ ] 선택한 격리 수준에서 가능한 이상 현상을 테스트했는가?
- [ ] 재시도 단위가 멱등적이며 전체 트랜잭션을 포함하는가?
- [ ] 외부 부작용과 DB 커밋의 불일치를 처리하는가?
- [ ] 오래 열린 트랜잭션과 lock wait를 관측하는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

### 연습문제

1. 좌석 1개를 두 사용자가 동시에 예약하는 시나리오를 세 가지 방식으로 구현하라.
2. write skew가 발생하는 온콜 근무표 예제를 구성하고 serializable로 해결하라.
3. DB 업데이트와 메시지 발행 사이 장애를 outbox로 처리하는 흐름을 그려라.

### 핵심 요약

- 트랜잭션은 불변조건을 실패 중에도 지키는 계약이다.
- 격리 수준은 가능한 동시성 이상 현상으로 이해한다.
- MVCC는 읽기 동시성을 높이지만 버전 정리 비용이 있다.
- 강한 격리도 충돌 재시도 설계가 필요하다.
- 외부 부작용은 DB 트랜잭션과 별도 조정해야 한다.

### 출처

- [@postgres-transaction-iso] PostgreSQL Global Development Group. **PostgreSQL Documentation — Transaction Isolation** (2026). https://www.postgresql.org/docs/current/transaction-iso.html
- [@postgres-mvcc] PostgreSQL Global Development Group. **PostgreSQL Documentation — Concurrency Control** (2026). https://www.postgresql.org/docs/current/mvcc.html

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
