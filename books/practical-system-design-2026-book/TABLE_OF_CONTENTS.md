# 목차

장별 파일로 바로 이동할 수 있는 링크형 목차다.

## Part 1. 설계 문제를 푸는 방법

1. [01. 요구사항에서 시스템 경계까지](manuscript/01-design-method/ch01-requirements-and-boundaries.md)
2. [02. 트래픽·저장공간·대역폭 계산](manuscript/01-design-method/ch02-capacity-estimation.md)
3. [03. 트레이드오프와 Architecture Decision Record](manuscript/01-design-method/ch03-tradeoffs-and-adr.md)
4. [04. SLI·SLO·SLA와 Error Budget](manuscript/01-design-method/ch04-sli-slo-sla-error-budget.md)

## Part 2. 분산 시스템의 기본 원리

5. [05. 지연시간·처리량·동시성과 Tail Latency](manuscript/02-distributed-foundations/ch05-latency-throughput-tail.md)
6. [06. 가용성·신뢰성·내구성과 장애 도메인](manuscript/02-distributed-foundations/ch06-availability-reliability-durability.md)
7. [07. CAP를 넘어선 일관성 모델](manuscript/02-distributed-foundations/ch07-consistency-beyond-cap.md)
8. [08. 트랜잭션·격리 수준·MVCC](manuscript/02-distributed-foundations/ch08-transactions-isolation-mvcc.md)
9. [09. 시간·순서·논리 시계·분산 ID](manuscript/02-distributed-foundations/ch09-time-ordering-distributed-id.md)
10. [10. 복제·Quorum·Failover](manuscript/02-distributed-foundations/ch10-replication-quorum-failover.md)
11. [11. 파티셔닝·Sharding·Consistent Hashing](manuscript/02-distributed-foundations/ch11-partitioning-sharding.md)
12. [12. Consensus·Leader Election·Fencing](manuscript/02-distributed-foundations/ch12-consensus-leader-fencing.md)

## Part 3. 네트워크와 서비스 실행 구조

13. [13. DNS·CDN·Edge와 전역 트래픽](manuscript/03-network-runtime/ch13-dns-cdn-edge.md)
14. [14. L4/L7 Load Balancing·Proxy·Gateway](manuscript/03-network-runtime/ch14-load-balancing-proxy-gateway.md)
15. [15. HTTP/1.1·HTTP/2·HTTP/3와 QUIC](manuscript/03-network-runtime/ch15-http3-quic.md)
16. [16. REST·gRPC·GraphQL·WebSocket·SSE](manuscript/03-network-runtime/ch16-api-and-streaming-protocols.md)
17. [17. 모듈러 모놀리스·마이크로서비스·Service Mesh](manuscript/03-network-runtime/ch17-monolith-microservices-mesh.md)

## Part 4. 데이터·캐시·이벤트

18. [18. 워크로드에서 저장소 선택하기](manuscript/04-data-events/ch18-choosing-data-store.md)
19. [19. 관계형 DB·분산 SQL·인덱스](manuscript/04-data-events/ch19-relational-distributed-sql-indexes.md)
20. [20. Key-Value·Document·Wide-column·Graph](manuscript/04-data-events/ch20-kv-document-widecolumn-graph.md)
21. [21. Object Storage·Search·Vector Store](manuscript/04-data-events/ch21-object-search-vector.md)
22. [22. 캐시·무효화·Stampede·Hot Key](manuscript/04-data-events/ch22-cache-invalidation-stampede.md)
23. [23. Queue·Durable Log·Delivery Semantics](manuscript/04-data-events/ch23-queue-log-delivery.md)
24. [24. Event Streaming·CDC·Outbox·Saga](manuscript/04-data-events/ch24-streaming-cdc-outbox-saga.md)

## Part 5. 프로덕션 시스템

25. [25. Timeout·Deadline·Retry·Backoff·Jitter](manuscript/05-production/ch25-timeout-deadline-retry.md)
26. [26. Circuit Breaker·Bulkhead·Backpressure·Load Shedding](manuscript/05-production/ch26-resilience-overload-control.md)
27. [27. Metrics·Logs·Traces와 OpenTelemetry](manuscript/05-production/ch27-observability-opentelemetry.md)
28. [28. 인증·인가·Zero Trust·Secrets·공급망 보안](manuscript/05-production/ch28-identity-zero-trust-supply-chain.md)
29. [29. Multi-region·Backup·재해 복구](manuscript/05-production/ch29-multi-region-disaster-recovery.md)
30. [30. Container·Kubernetes·Serverless·IaC·GitOps·FinOps](manuscript/05-production/ch30-cloud-native-platform-finops.md)

## Part 6. AI 네이티브 시스템

31. [31. RAG 데이터 파이프라인과 Retrieval 품질](manuscript/06-ai-native/ch31-rag-pipeline-retrieval.md)
32. [32. LLM Inference·Batching·KV Cache·Model Routing](manuscript/06-ai-native/ch32-llm-serving-routing.md)
33. [33. Agent 상태·메모리·도구 실행·승인 경계](manuscript/06-ai-native/ch33-agent-state-tools-approval.md)
34. [34. AI 평가·관측 가능성·보안·비용](manuscript/06-ai-native/ch34-ai-evaluation-observability.md)

## Part 7. 단계별 종합 설계

35. [35. URL 단축 서비스: 단일 노드에서 전역 서비스까지](manuscript/07-case-studies/ch35-url-shortener.md)
36. [36. 실시간 채팅과 알림 플랫폼](manuscript/07-case-studies/ch36-chat-notification.md)
37. [37. 주문·재고·결제 원장 시스템](manuscript/07-case-studies/ch37-order-inventory-payment-ledger.md)
38. [38. 멀티테넌트 RAG·AI 고객지원 플랫폼](manuscript/07-case-studies/ch38-multitenant-rag-support.md)

## 부록

- [부록 A. 시스템 설계 리뷰 체크리스트](manuscript/99-appendices/appendix-a-design-review.md)
- [부록 B. 용량 계산 공식](manuscript/99-appendices/appendix-b-capacity-formulas.md)
- [부록 C. 이미지 제작과 검수 흐름](manuscript/99-appendices/appendix-c-visual-workflow.md)
