---
id: part-03
title: "Part 3. 네트워크와 서비스 실행 구조"
status: draft

---

# Part 3. 네트워크와 서비스 실행 구조

사용자 요청이 전역 네트워크와 서비스 계층을 지나 응답으로 돌아오는 전체 경로를 설계한다.

이 Part에서는 특정 제품의 설정법보다 반복해서 적용할 수 있는 설계 질문과 실패 모델을 먼저 익힌다. 각 장의 체크리스트를 실제 시스템의 ADR·런북·대시보드와 연결해 읽는 것이 목표다.

## 포함 장

| ID | 장 제목 | 최신성 | 원본 관계 |
|---|---|---|---|
| ch13 | DNS·CDN·Edge와 전역 트래픽 | current | REWRITE |
| ch14 | L4/L7 Load Balancing·Proxy·Gateway | current | REWRITE |
| ch15 | HTTP/1.1·HTTP/2·HTTP/3와 QUIC | current | REPLACE |
| ch16 | REST·gRPC·GraphQL·WebSocket·SSE | current | REPLACE |
| ch17 | 모듈러 모놀리스·마이크로서비스·Service Mesh | current | REPLACE |

## 읽는 방법

1. 먼저 각 장의 **요구사항과 실패 모델**을 자신의 시스템에 대입한다.
2. **대안과 트레이드오프**에서 현재 선택이 어떤 비용을 감수하는지 확인한다.
3. **장애 시나리오**를 게임데이 또는 설계 리뷰 질문으로 바꾼다.
4. 시각자료는 설명을 대신하지 않고 책임·흐름·복구 경계를 검증하는 용도로 사용한다.
