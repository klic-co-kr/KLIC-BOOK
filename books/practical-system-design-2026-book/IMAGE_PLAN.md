# 시각자료 제작 계획

## 전체 예산

- 기술 SVG: 88개 (`38장×2 + 종합 설계 4장×3`)
- 데이터 차트: 12개
- 합계: **100개** (ill 19종은 품질 불량으로 제외·삭제, 2026-08-09)

현재 모든 항목은 `specified` 상태다. 실제 SVG·PNG·차트 binary는 아직 생성하지 않았으며, 본문과 manifest에 제작 위치·프롬프트·대체 텍스트를 연결했다.

## 장별 배치

| 장 | 제목 | SVG | Image2.0 | 차트 | Asset IDs |
|---|---|---|---|---|---|
| ch01 | 요구사항에서 시스템 경계까지 | 2 | 0 | 0 | fig-ch01-01, fig-ch01-02 |
| ch02 | 트래픽·저장공간·대역폭 계산 | 2 | 0 | 1 | chart-ch02-01, fig-ch02-01, fig-ch02-02 |
| ch03 | 트레이드오프와 Architecture Decision Record | 2 | 0 | 0 | fig-ch03-01, fig-ch03-02 |
| ch04 | SLI·SLO·SLA와 Error Budget | 2 | 0 | 1 | chart-ch04-01, fig-ch04-01, fig-ch04-02 |
| ch05 | 지연시간·처리량·동시성과 Tail Latency | 2 | 0 | 1 | chart-ch05-01, fig-ch05-01, fig-ch05-02 |
| ch06 | 가용성·신뢰성·내구성과 장애 도메인 | 2 | 0 | 1 | chart-ch06-01, fig-ch06-01, fig-ch06-02 |
| ch07 | CAP를 넘어선 일관성 모델 | 2 | 0 | 0 | fig-ch07-01, fig-ch07-02 |
| ch08 | 트랜잭션·격리 수준·MVCC | 2 | 0 | 0 | fig-ch08-01, fig-ch08-02 |
| ch09 | 시간·순서·논리 시계·분산 ID | 2 | 0 | 0 | fig-ch09-01, fig-ch09-02 |
| ch10 | 복제·Quorum·Failover | 2 | 0 | 1 | chart-ch10-01, fig-ch10-01, fig-ch10-02 |
| ch11 | 파티셔닝·Sharding·Consistent Hashing | 2 | 0 | 1 | chart-ch11-01, fig-ch11-01, fig-ch11-02 |
| ch12 | Consensus·Leader Election·Fencing | 2 | 0 | 0 | fig-ch12-01, fig-ch12-02 |
| ch13 | DNS·CDN·Edge와 전역 트래픽 | 2 | 0 | 0 | fig-ch13-01, fig-ch13-02 |
| ch14 | L4/L7 Load Balancing·Proxy·Gateway | 2 | 0 | 0 | fig-ch14-01, fig-ch14-02 |
| ch15 | HTTP/1.1·HTTP/2·HTTP/3와 QUIC | 2 | 0 | 0 | fig-ch15-01, fig-ch15-02 |
| ch16 | REST·gRPC·GraphQL·WebSocket·SSE | 2 | 0 | 0 | fig-ch16-01, fig-ch16-02 |
| ch17 | 모듈러 모놀리스·마이크로서비스·Service Mesh | 2 | 0 | 0 | fig-ch17-01, fig-ch17-02 |
| ch18 | 워크로드에서 저장소 선택하기 | 2 | 0 | 0 | fig-ch18-01, fig-ch18-02 |
| ch19 | 관계형 DB·분산 SQL·인덱스 | 2 | 0 | 0 | fig-ch19-01, fig-ch19-02 |
| ch20 | Key-Value·Document·Wide-column·Graph | 2 | 0 | 0 | fig-ch20-01, fig-ch20-02 |
| ch21 | Object Storage·Search·Vector Store | 2 | 0 | 0 | fig-ch21-01, fig-ch21-02 |
| ch22 | 캐시·무효화·Stampede·Hot Key | 2 | 0 | 1 | chart-ch22-01, fig-ch22-01, fig-ch22-02 |
| ch23 | Queue·Durable Log·Delivery Semantics | 2 | 0 | 0 | fig-ch23-01, fig-ch23-02 |
| ch24 | Event Streaming·CDC·Outbox·Saga | 2 | 0 | 0 | fig-ch24-01, fig-ch24-02 |
| ch25 | Timeout·Deadline·Retry·Backoff·Jitter | 2 | 0 | 1 | chart-ch25-01, fig-ch25-01, fig-ch25-02 |
| ch26 | Circuit Breaker·Bulkhead·Backpressure·Load Shedding | 2 | 0 | 0 | fig-ch26-01, fig-ch26-02 |
| ch27 | Metrics·Logs·Traces와 OpenTelemetry | 2 | 0 | 1 | chart-ch27-01, fig-ch27-01, fig-ch27-02 |
| ch28 | 인증·인가·Zero Trust·Secrets·공급망 보안 | 2 | 0 | 0 | fig-ch28-01, fig-ch28-02 |
| ch29 | Multi-region·Backup·재해 복구 | 2 | 0 | 1 | chart-ch29-01, fig-ch29-01, fig-ch29-02 |
| ch30 | Container·Kubernetes·Serverless·IaC·GitOps·FinOps | 2 | 0 | 0 | fig-ch30-01, fig-ch30-02 |
| ch31 | RAG 데이터 파이프라인과 Retrieval 품질 | 2 | 0 | 0 | fig-ch31-01, fig-ch31-02 |
| ch32 | LLM Inference·Batching·KV Cache·Model Routing | 2 | 0 | 1 | chart-ch32-01, fig-ch32-01, fig-ch32-02 |
| ch33 | Agent 상태·메모리·도구 실행·승인 경계 | 2 | 0 | 0 | fig-ch33-01, fig-ch33-02 |
| ch34 | AI 평가·관측 가능성·보안·비용 | 2 | 0 | 1 | chart-ch34-01, fig-ch34-01, fig-ch34-02 |
| ch35 | URL 단축 서비스: 단일 노드에서 전역 서비스까지 | 5 | 0 | 0 | fig-ch35-01, fig-ch35-02, fig-ch35-03, fig-ch35-04, fig-ch35-05 |
| ch36 | 실시간 채팅과 알림 플랫폼 | 5 | 0 | 0 | fig-ch36-01, fig-ch36-02, fig-ch36-03, fig-ch36-04, fig-ch36-05 |
| ch37 | 주문·재고·결제 원장 시스템 | 5 | 0 | 0 | fig-ch37-01, fig-ch37-02, fig-ch37-03, fig-ch37-04, fig-ch37-05 |
| ch38 | 멀티테넌트 RAG·AI 고객지원 플랫폼 | 5 | 0 | 0 | fig-ch38-01, fig-ch38-02, fig-ch38-03, fig-ch38-04, fig-ch38-05 |

## 제작 순서

1. `ch07`, `ch15`, `ch31`의 SVG·Image2.0·차트를 파일럿으로 제작한다.
2. 화살표·한글·출처·접근성 검수 기준을 고정한다.
3. Part 오프닝 일러스트는 제외(2026-08-09).
4. 나머지 기술 SVG를 장 단위로 제작하고 본문 검수와 함께 승인한다.
5. 차트는 synthetic 산식에서 시작해 실측 데이터가 확보된 경우에만 교체한다.
