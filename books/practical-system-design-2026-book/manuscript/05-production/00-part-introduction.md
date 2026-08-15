---
id: part-05
title: "Part 5. 프로덕션 시스템"
status: draft

---

## Part 5. 프로덕션 시스템

정상 동작만이 아니라 과부하, 침해, 배포, 재해, 비용까지 포함해 운영 가능한 구조를 만든다.

이 Part에서는 특정 제품의 설정법보다 반복해서 적용할 수 있는 설계 질문과 실패 모델을 먼저 익힌다. 각 장의 체크리스트를 실제 시스템의 ADR·런북·대시보드와 연결해 읽는 것이 목표다.

### 포함 장

| ID | 장 제목 | 최신성 | 원본 관계 |
|---|---|---|---|
| ch25 | Timeout·Deadline·Retry·Backoff·Jitter | durable | ADD |
| ch26 | Circuit Breaker·Bulkhead·Backpressure·Load Shedding | durable | ADD |
| ch27 | Metrics·Logs·Traces와 OpenTelemetry | current | ADD |
| ch28 | 인증·인가·Zero Trust·Secrets·공급망 보안 | current | REPLACE |
| ch29 | Multi-region·Backup·재해 복구 | durable | ADD |
| ch30 | Container·Kubernetes·Serverless·IaC·GitOps·FinOps | current | ADD |

### 읽는 방법

1. 먼저 각 장의 **요구사항과 실패 모델**을 자신의 시스템에 대입한다.
2. **대안과 트레이드오프**에서 현재 선택이 어떤 비용을 감수하는지 확인한다.
3. **장애 시나리오**를 게임데이 또는 설계 리뷰 질문으로 바꾼다.
4. 시각자료는 설명을 대신하지 않고 책임·흐름·복구 경계를 검증하는 용도로 사용한다.
