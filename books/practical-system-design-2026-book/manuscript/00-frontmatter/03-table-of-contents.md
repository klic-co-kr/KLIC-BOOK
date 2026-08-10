# 목차

## Part 1. 설계 문제를 푸는 방법

1. 요구사항에서 시스템 경계까지
2. 트래픽·저장공간·대역폭 계산
3. 트레이드오프와 Architecture Decision Record
4. SLI·SLO·SLA와 Error Budget

## Part 2. 분산 시스템의 기본 원리

5. 지연시간·처리량·동시성과 Tail Latency
6. 가용성·신뢰성·내구성과 장애 도메인
7. CAP를 넘어선 일관성 모델
8. 트랜잭션·격리 수준·MVCC
9. 시간·순서·논리 시계·분산 ID
10. 복제·Quorum·Failover
11. 파티셔닝·Sharding·Consistent Hashing
12. Consensus·Leader Election·Fencing

## Part 3. 네트워크와 서비스 실행 구조

13. DNS·CDN·Edge와 전역 트래픽
14. L4/L7 Load Balancing·Proxy·Gateway
15. HTTP/1.1·HTTP/2·HTTP/3와 QUIC
16. REST·gRPC·GraphQL·WebSocket·SSE
17. 모듈러 모놀리스·마이크로서비스·Service Mesh

## Part 4. 데이터·캐시·이벤트

18. 워크로드에서 저장소 선택하기
19. 관계형 DB·분산 SQL·인덱스
20. Key-Value·Document·Wide-column·Graph
21. Object Storage·Search·Vector Store
22. 캐시·무효화·Stampede·Hot Key
23. Queue·Durable Log·Delivery Semantics
24. Event Streaming·CDC·Outbox·Saga

## Part 5. 프로덕션 시스템

25. Timeout·Deadline·Retry·Backoff·Jitter
26. Circuit Breaker·Bulkhead·Backpressure·Load Shedding
27. Metrics·Logs·Traces와 OpenTelemetry
28. 인증·인가·Zero Trust·Secrets·공급망 보안
29. Multi-region·Backup·재해 복구
30. Container·Kubernetes·Serverless·IaC·GitOps·FinOps

## Part 6. AI 네이티브 시스템

31. RAG 데이터 파이프라인과 Retrieval 품질
32. LLM Inference·Batching·KV Cache·Model Routing
33. Agent 상태·메모리·도구 실행·승인 경계
34. AI 평가·관측 가능성·보안·비용

## Part 7. 단계별 종합 설계

35. URL 단축 서비스: 단일 노드에서 전역 서비스까지
36. 실시간 채팅과 알림 플랫폼
37. 주문·재고·결제 원장 시스템
38. 멀티테넌트 RAG·AI 고객지원 플랫폼

## 부록

- 부록 A. 시스템 설계 리뷰 체크리스트
- 부록 B. 용량 계산 공식
- 부록 C. 이미지 제작과 검수 흐름
