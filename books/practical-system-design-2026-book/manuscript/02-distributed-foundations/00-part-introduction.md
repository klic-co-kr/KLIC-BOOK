---
id: part-02
title: "Part 2. 분산 시스템의 기본 원리"
status: draft

---

## Part 2. 분산 시스템의 기본 원리

시간, 실패, 복제, 일관성, 합의처럼 분산 시스템을 어렵게 만드는 조건을 다룬다.

이 Part에서는 특정 제품의 설정법보다 반복해서 적용할 수 있는 설계 질문과 실패 모델을 먼저 익힌다. 각 장의 체크리스트를 실제 시스템의 ADR·런북·대시보드와 연결해 읽는 것이 목표다.

### 포함 장

| ID | 장 제목 | 최신성 | 원본 관계 |
|---|---|---|---|
| ch05 | 지연시간·처리량·동시성과 Tail Latency | durable | REWRITE |
| ch06 | 가용성·신뢰성·내구성과 장애 도메인 | durable | REWRITE |
| ch07 | CAP를 넘어선 일관성 모델 | durable | REWRITE |
| ch08 | 트랜잭션·격리 수준·MVCC | durable | ADD |
| ch09 | 시간·순서·논리 시계·분산 ID | durable | ADD |
| ch10 | 복제·Quorum·Failover | durable | REPLACE |
| ch11 | 파티셔닝·Sharding·Consistent Hashing | durable | REWRITE |
| ch12 | Consensus·Leader Election·Fencing | durable | ADD |

### 읽는 방법

1. 먼저 각 장의 **요구사항과 실패 모델**을 자신의 시스템에 대입한다.
2. **대안과 트레이드오프**에서 현재 선택이 어떤 비용을 감수하는지 확인한다.
3. **장애 시나리오**를 게임데이 또는 설계 리뷰 질문으로 바꾼다.
4. 시각자료는 설명을 대신하지 않고 책임·흐름·복구 경계를 검증하는 용도로 사용한다.
