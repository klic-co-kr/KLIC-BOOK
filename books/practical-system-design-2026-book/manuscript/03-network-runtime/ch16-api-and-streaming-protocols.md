---
id: ch16
title: REST·gRPC·GraphQL·WebSocket·SSE
part: network-runtime
order: 16
status: draft
freshness: current
last_verified: '2026-08-06'
review_due: '2027-02-06'
upstream_lineage:
- source: system-design-primer
  file: README.md
  anchor: application-layer
  action: REPLACE
audiences:
- backend-engineer
- platform-engineer
prerequisites:
- ch14
- ch15
learning_objectives:
- 요청·스트리밍·구독 패턴에 맞춰 통신 방식을 선택한다.
- deadline·취소·버전·오류 계약을 protocol보다 먼저 설계한다.
- 실시간 연결의 재연결·순서·backpressure를 다룬다.
figures:
- fig-ch16-01
- fig-ch16-02
sources:
- rfc9110
- grpc-core
- graphql-spec
- rfc6455
- html-sse
draft_notice: 기술·편집·접근성 검수 전 초고
---

## 16. REST·gRPC·GraphQL·WebSocket·SSE

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

### 이 장에서 해결할 문제

REST, gRPC, GraphQL, WebSocket, SSE는 서로를 완전히 대체하는 경쟁 제품이 아니다. 자원 중심 공개 API, 타입이 강한 내부 RPC, 클라이언트 조합 조회, 양방향 실시간 연결, 서버 단방향 이벤트라는 서로 다른 상호작용을 해결한다.

이 절의 기준 출처: [@rfc9110; @grpc-core].

#### 학습 목표

- 요청·스트리밍·구독 패턴에 맞춰 통신 방식을 선택한다.
- deadline·취소·버전·오류 계약을 protocol보다 먼저 설계한다.
- 실시간 연결의 재연결·순서·backpressure를 다룬다.

### 먼저 결론

- protocol 이름보다 호출 방향, 메시지 빈도, 연결 수명, 브라우저 지원, 캐시, 실패 복구 요구를 먼저 적는다.
- deadline·취소·idempotency·오류 의미는 어떤 protocol에서도 필요하다.
- GraphQL은 over/under-fetch를 줄일 수 있지만 비용 제한과 field-level 권한이 필요하다.
- WebSocket과 SSE는 연결이 끊어지는 것을 정상 조건으로 보고 resume·중복·순서 계약을 둔다.

::: current-note
**2026-08-06 확인:** 이 장은 변화 가능한 표준·프로젝트·AI 구현을 포함한다. 기본 재검토일은 `2027-02-06`이며, 출판 직전 공식 문서를 다시 확인한다.
:::

### 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | REST·gRPC·GraphQL·WebSocket·SSE에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | protocol 이름보다 호출 방향, 메시지 빈도, 연결 수명, 브라우저 지원, 캐시, 실패 복구 요구를 먼저 적는다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | realtime connection state를 stateless gateway와 shared subscription index로 분리한다. |
| 실패·복구 | “Schema breaking change” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | additive evolution, deprecation, compatibility CI를 사용한다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | field·method 단위 권한을 schema와 함께 검증한다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | method/operation별 p95·오류 code·deadline exceeded |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

### 핵심 개념

#### REST 스타일

HTTP method와 resource representation을 활용하는 API 설계 방식이다.

#### gRPC

IDL 기반 service/method와 unary·streaming RPC를 제공한다.

#### GraphQL

클라이언트가 schema의 field를 선택해 query/mutation/subscription을 수행한다.

#### WebSocket

HTTP handshake 후 양방향 message channel을 제공한다.

#### SSE

HTTP response를 유지하며 서버가 text event stream을 단방향 전송한다.

#### Deadline propagation

상위 요청의 남은 시간을 하위 호출에 전달하는 계약이다.

#### Resume token

재연결 시 마지막으로 처리한 위치에서 이어받기 위한 cursor·event ID다.

핵심 개념의 정의와 범위는 [@rfc9110; @grpc-core; @graphql-spec; @rfc6455; @html-sse]를 기준으로 재검토해야 한다.

### 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| 외부 API gateway | 인증·quota·version·HTTP 정책을 적용한다. |
| REST/GraphQL facade | 클라이언트 요구를 도메인 호출로 조합한다. |
| gRPC service | 내부 타입 계약과 streaming을 제공한다. |
| Realtime gateway | WebSocket/SSE connection과 subscription을 관리한다. |
| Event backbone | 실시간 fan-out 전에 내구성 있는 순서와 replay를 제공한다. |
| Schema registry | IDL·GraphQL schema·event contract 호환성을 검증한다. |

<!-- figure-spec
id: fig-ch16-01
chapter: ch16
role: interaction-patterns
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch16-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: unary·server streaming·client streaming·bidirectional과 REST/gRPC/GraphQL/WebSocket/SSE의 적합도를 비교한다.
required_labels_ko:
- Unary
- Server Stream
- Client Stream
- Bidirectional
- REST
- gRPC
- GraphQL
- WebSocket
- SSE
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- rfc9110
- grpc-core
- graphql-spec
alt_ko: unary·server streaming·client streaming·bidirectional과 REST/gRPC/GraphQL/WebSocket/SSE의 적합도를 비교한다.
caption_ko: unary·server streaming·client streaming·bidirectional과 REST/gRPC/GraphQL/WebSocket/SSE의 적합도를 비교한다
status: specified
spec_file: assets/specs/svg/fig-ch16-01.md
-->

> **시각자료 제작 위치 — unary·server streaming·client streaming·bidirectional과 REST/gRPC/GraphQL/WebSocket/SSE의 적합도를 비교한다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch16-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch16-01.md`  
> 대체 텍스트: unary·server streaming·client streaming·bidirectional과 REST/gRPC/GraphQL/WebSocket/SSE의 적합도를 비교한다.


### 요청·데이터 흐름

1. 클라이언트의 상호작용 패턴을 unary·server stream·client stream·bidirectional로 분류한다.
2. 공개·내부·브라우저 경계에 맞는 protocol을 선택한다.
3. 요청 ID, deadline, auth context, idempotency를 전달한다.
4. 서버가 오류를 retryable·permanent·auth·quota로 구분한다.
5. stream은 sequence/cursor와 backpressure를 관리한다.
6. 재연결 시 resume token으로 누락·중복을 보정한다.
7. schema 변경을 compatibility test로 배포한다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

### 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| REST/HTTP JSON | 브라우저·도구·캐시 친화적이고 공개 계약이 쉽다. | 타입·streaming·세밀한 조합에 추가 규칙이 필요하다. | 공개 API·CRUD |
| gRPC | 강한 schema와 효율적 streaming·codegen을 제공한다. | 브라우저·proxy·디버깅 경로를 준비해야 한다. | 내부 서비스·고빈도 RPC |
| GraphQL | 클라이언트별 화면 조합과 schema 탐색성이 좋다. | query 비용·N+1·권한·cache가 복잡하다. | 다양한 UI의 aggregation |
| WebSocket/SSE | 낮은 지연의 지속 업데이트를 제공한다. | connection state·재연결·fan-out 운영이 필요하다. | 채팅·알림·진행 상태 |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@rfc9110; @grpc-core; @graphql-spec]를 참조한다.

### 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| Schema breaking change | 필드 삭제·의미 변경이 오래된 client를 깨뜨린다. | additive evolution, deprecation, compatibility CI를 사용한다. |
| Unbounded query | GraphQL 깊이·fan-out이 DB와 downstream을 포화시킨다. | cost budget, depth/field limit, persisted query를 둔다. |
| Zombie stream | 모바일 단절 후 서버가 connection을 오래 유지한다. | heartbeat, idle timeout, lease, disconnect cleanup을 적용한다. |
| Resume gap | 재연결 동안 이벤트가 유실되거나 중복된다. | durable cursor, sequence, replay window, idempotent consumer를 사용한다. |
| Deadline loss | gateway가 timeout을 새로 시작해 하위 작업이 사용자 취소 후에도 계속된다. | absolute deadline 또는 남은 budget을 hop마다 전달한다. |

<!-- figure-spec
id: fig-ch16-02
chapter: ch16
role: realtime-resume
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch16-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 실시간 연결 단절 후 cursor·replay window·deduplication으로 이어받는 흐름을 보여준다.
required_labels_ko:
- 클라이언트
- Realtime Gateway
- Event Log
- Cursor
- 재연결
- Replay
- 중복 제거
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- rfc9110
- grpc-core
- graphql-spec
alt_ko: 실시간 연결 단절 후 cursor·replay window·deduplication으로 이어받는 흐름을 보여준다.
caption_ko: 실시간 연결 단절 후 cursor·replay window·deduplication으로 이어받는 흐름을 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch16-02.md
-->

> **시각자료 제작 위치 — 실시간 연결 단절 후 cursor·replay window·deduplication으로 이어받는 흐름을 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch16-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch16-02.md`  
> 대체 텍스트: 실시간 연결 단절 후 cursor·replay window·deduplication으로 이어받는 흐름을 보여준다.


### 확장 전략

- realtime connection state를 stateless gateway와 shared subscription index로 분리한다.
- fan-out은 연결별 반복 DB query 대신 event backbone과 batch delivery를 사용한다.
- GraphQL resolver는 DataLoader/배치와 field cost를 적용한다.
- 큰 payload와 slow consumer를 별도 queue·drop 정책으로 격리한다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

### 보안과 개인정보

- field·method 단위 권한을 schema와 함께 검증한다.
- WebSocket upgrade 이후에도 token 만료·권한 변경을 재평가한다.
- GraphQL introspection·error가 내부 schema·데이터를 과도하게 노출하지 않게 한다.
- message size·compression bomb·subscription 수를 제한한다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

### 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- method/operation별 p95·오류 code·deadline exceeded
- GraphQL complexity·resolver fan-out·N+1
- active connection·reconnect·heartbeat timeout
- stream lag·resume gap·duplicate event
- schema version·deprecated field 사용률

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

### 비용과 운영 복잡도

- IDL/codegen은 개발 효율을 높이지만 다언어 toolchain 유지 비용이 있다.
- 실시간 연결은 요청 수보다 동시 연결·메모리·egress 비용이 중요하다.
- GraphQL facade는 클라이언트 개발을 줄여도 backend aggregation과 관측 비용을 만든다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

### 흔한 오해와 안티패턴

- 모든 내부 호출을 REST로 해야 단순하다고 단정한다.
- GraphQL 하나로 서비스 경계를 대체한다.
- WebSocket이면 메시지가 자동으로 내구성 있고 순서 보장된다고 생각한다.
- streaming API에 deadline과 backpressure를 두지 않는다.

### 설계 리뷰

- [ ] 상호작용 방향과 연결 수명이 protocol 선택 근거인가?
- [ ] 오류·deadline·취소·idempotency가 계약에 포함됐는가?
- [ ] schema evolution과 오래된 client를 시험하는가?
- [ ] 재연결·resume·중복·slow consumer가 정의됐는가?
- [ ] query·message·subscription 비용이 제한되는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

### 연습문제

1. 배송 진행 상태를 SSE와 WebSocket으로 각각 설계하고 선택 근거를 쓰라.
2. GraphQL query 하나가 1만 개 DB 호출을 만드는 경로를 비용 모델로 차단하라.
3. gRPC deadline이 REST gateway를 거쳐 하위 서비스까지 전달되는 규칙을 정의하라.

### 핵심 요약

- 통신 방식은 상호작용 패턴에 맞춰 선택한다.
- deadline·오류·idempotency는 protocol 공통 계약이다.
- GraphQL에는 query 비용과 field 권한이 필요하다.
- 실시간 연결은 단절·resume·중복을 정상 조건으로 처리한다.
- schema compatibility는 배포 전 자동 검증한다.

### 출처

- [@rfc9110] IETF. **RFC 9110 — HTTP Semantics** (2022). https://www.rfc-editor.org/rfc/rfc9110.html
- [@grpc-core] gRPC Authors. **gRPC Core Concepts** (2026). https://grpc.io/docs/what-is-grpc/core-concepts/
- [@graphql-spec] GraphQL Foundation. **GraphQL Specification** (2025). https://spec.graphql.org/
- [@rfc6455] IETF. **RFC 6455 — The WebSocket Protocol** (2011). https://www.rfc-editor.org/rfc/rfc6455.html
- [@html-sse] WHATWG. **HTML Living Standard — Server-sent events** (2026). https://html.spec.whatwg.org/multipage/server-sent-events.html

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
