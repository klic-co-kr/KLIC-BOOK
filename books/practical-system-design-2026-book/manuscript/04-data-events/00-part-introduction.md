---
id: part-04
title: "Part 4. 데이터·캐시·이벤트"
status: draft

---

## Part 4. 데이터·캐시·이벤트

데이터의 형태와 접근 패턴에 따라 저장소, 캐시, 이벤트 경로를 선택한다.

이 Part에서는 특정 제품의 설정법보다 반복해서 적용할 수 있는 설계 질문과 실패 모델을 먼저 익힌다. 각 장의 체크리스트를 실제 시스템의 ADR·런북·대시보드와 연결해 읽는 것이 목표다.

### 포함 장

| ID | 장 제목 | 최신성 | 원본 관계 |
|---|---|---|---|
| ch18 | 워크로드에서 저장소 선택하기 | durable | REWRITE |
| ch19 | 관계형 DB·분산 SQL·인덱스 | current | REWRITE |
| ch20 | Key-Value·Document·Wide-column·Graph | current | REWRITE |
| ch21 | Object Storage·Search·Vector Store | current | ADD |
| ch22 | 캐시·무효화·Stampede·Hot Key | durable | REWRITE |
| ch23 | Queue·Durable Log·Delivery Semantics | durable | REWRITE |
| ch24 | Event Streaming·CDC·Outbox·Saga | current | ADD |

### 읽는 방법

1. 먼저 각 장의 **요구사항과 실패 모델**을 자신의 시스템에 대입한다.
2. **대안과 트레이드오프**에서 현재 선택이 어떤 비용을 감수하는지 확인한다.
3. **장애 시나리오**를 게임데이 또는 설계 리뷰 질문으로 바꾼다.
4. 시각자료는 설명을 대신하지 않고 책임·흐름·복구 경계를 검증하는 용도로 사용한다.
