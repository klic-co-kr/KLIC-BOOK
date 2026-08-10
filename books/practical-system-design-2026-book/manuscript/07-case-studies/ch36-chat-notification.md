---
id: ch36
title: 실시간 채팅과 알림 플랫폼
part: case-studies
order: 36
status: draft
freshness: current
last_verified: '2026-08-06'
review_due: '2027-02-06'
upstream_lineage:
- source: new-2026-edition
  file: null
  anchor: null
  action: ADD
audiences:
- backend-engineer
- platform-engineer
prerequisites:
- ch09
- ch16
- ch23
- ch25
- ch26
learning_objectives:
- 실시간 연결과 내구 메시지 원장을 분리한다.
- 방·사용자 단위 순서, 전송 상태, offline sync를 설계한다.
- 알림 채널의 provider 실패·중복·사용자 선호를 다룬다.
figures:
- fig-ch36-01
- fig-ch36-02
- fig-ch36-03
- fig-ch36-04
- fig-ch36-05
sources:
- rfc6455
- html-sse
- kafka-docs
- aws-timeouts-retries
draft_notice: 기술·편집·접근성 검수 전 초고
---

# 36. 실시간 채팅과 알림 플랫폼

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

## 이 장에서 해결할 문제

채팅은 WebSocket 연결만으로 완성되지 않는다. 연결은 일시적이고 메시지는 내구성이 있어야 하며, 방 단위 순서·중복·읽음 상태·offline sync·push provider·차단·보존 정책이 별도 상태 기계로 동작한다.

이 절의 기준 출처: [@rfc6455; @html-sse].

### 학습 목표

- 실시간 연결과 내구 메시지 원장을 분리한다.
- 방·사용자 단위 순서, 전송 상태, offline sync를 설계한다.
- 알림 채널의 provider 실패·중복·사용자 선호를 다룬다.

## 먼저 결론

- gateway connection state와 message history 원장을 분리한다.
- 전역 순서 대신 conversation별 sequence를 제공한다.
- client-generated message ID로 재전송과 중복을 처리한다.
- 실시간 delivery 실패는 offline sync와 push notification으로 보완하되 같은 메시지 효과를 중복시키지 않는다.

::: current-note
**2026-08-06 확인:** 이 장은 변화 가능한 표준·프로젝트·AI 구현을 포함한다. 기본 재검토일은 `2027-02-06`이며, 출판 직전 공식 문서를 다시 확인한다.
:::

## 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | 실시간 채팅과 알림 플랫폼에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | gateway connection state와 message history 원장을 분리한다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | conversation ID를 event partition key로 사용하되 초대형 방은 별도 broadcast 경로를 둔다. |
| 실패·복구 | “Duplicate send” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | client message ID+conversation UNIQUE로 결과를 재사용한다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | 대화 membership과 메시지 접근은 fan-out과 sync 단계 모두 검증한다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | active connection·reconnect·heartbeat timeout |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

## 핵심 개념

### Connection session

한 장치의 WebSocket/SSE 연결과 heartbeat·auth 상태다.

### Conversation sequence

한 대화방 안에서 메시지 순서를 결정하는 증가 version이다.

### Message state

accepted, persisted, delivered, read, failed 같은 단계다.

### Fan-out

한 메시지를 다수 참가자 connection·inbox로 전달하는 과정이다.

### Presence

사용자 장치의 최근 활동과 연결 상태에 대한 근사 정보다.

### Offline cursor

마지막으로 동기화한 conversation 위치다.

### Notification intent

메시지 자체와 분리된 “이 사용자에게 이 채널로 알림” 요청이다.

### Channel provider

APNs/FCM/SMS/email 등 외부 전달 시스템이다.

핵심 개념의 정의와 범위는 [@rfc6455; @html-sse; @kafka-docs; @aws-timeouts-retries]를 기준으로 재검토해야 한다.

### 메시지 상태와 사용자에게 보이는 의미

- `local`: 장치에만 존재하며 서버가 보지 못했다.
- `accepted`: 서버가 형식과 권한을 확인했지만 아직 내구 commit 의미를 명확히 해야 한다.
- `persisted`: message 원장에 commit됐고 재연결 후 복구할 수 있다.
- `delivered`: 하나 이상의 수신 장치 gateway가 받았다. 이것은 사용자가 읽었다는 뜻이 아니다.
- `read`: 특정 장치 또는 사용자가 sequence까지 읽었다고 보고했다.

UI의 체크 표시를 설계하기 전에 각 상태의 증거와 실패 시 되돌림을 정의해야 한다.

## 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| Realtime gateway | 연결·heartbeat·subscription·backpressure를 관리한다. |
| Session registry | user-device와 gateway 위치를 TTL로 추적한다. |
| Message service | 권한·sequence·message 원장을 커밋한다. |
| Conversation store | 대화별 ordered history와 membership을 보존한다. |
| Event log | persisted message를 fan-out·notification으로 전달한다. |
| Fan-out workers | online session과 offline inbox에 배포한다. |
| Notification service | 선호·quiet hours·dedup·provider routing을 적용한다. |
| Presence service | 근사 online 상태를 제공한다. |
| Sync API | cursor 이후 누락 메시지를 반환한다. |

<!-- figure-spec
id: fig-ch36-01
chapter: ch36
role: chat-message-path
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch36-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: client·gateway·message service·conversation store·event log·fan-out·sync 경로를 보여준다.
required_labels_ko:
- Client
- Realtime Gateway
- Message Service
- Conversation Store
- Event Log
- Fan-out
- Sync API
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- rfc6455
- html-sse
- kafka-docs
alt_ko: client·gateway·message service·conversation store·event log·fan-out·sync 경로를 보여준다.
caption_ko: client·gateway·message service·conversation store·event log·fan-out·sync 경로를 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch36-01.md
-->

> **시각자료 제작 위치 — client·gateway·message service·conversation store·event log·fan-out·sync 경로를 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch36-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch36-01.md`  
> 대체 텍스트: client·gateway·message service·conversation store·event log·fan-out·sync 경로를 보여준다.


## 요청·데이터 흐름

1. 클라이언트가 device session과 auth로 gateway에 연결한다.
2. 메시지를 client message ID와 conversation ID로 전송한다.
3. message service가 membership을 검증하고 conversation sequence를 할당해 원장에 커밋한다.
4. 성공 ack가 원장 ID와 sequence를 반환한다.
5. event log가 online fan-out과 notification intent를 분기한다.
6. gateway는 slow consumer에게 bounded queue·drop/resync 신호를 적용한다.
7. offline 장치는 reconnect 후 cursor로 history를 동기화한다.
8. notification service는 사용자 선호와 이미 읽은 상태를 확인한 뒤 provider로 보낸다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

## 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| Fan-out on write | 보낼 때 수신자 inbox를 미리 갱신해 읽기가 빠르다. | 대형 방·유명 사용자에서 쓰기 fan-out이 크다. | 소규모 대화·일반 채팅 |
| Fan-out on read | 메시지 원장을 저장하고 읽을 때 조합해 쓰기가 단순하다. | 읽기·정렬·unread 계산 비용이 크다. | 대형 broadcast 방 |
| 하이브리드 | 일반 대화는 write, 대형 방은 read로 분리한다. | 두 경로와 상태 일관성이 복잡하다. | 다양한 방 크기 |
| WebSocket | 양방향 낮은 지연을 제공한다. | connection 운영과 mobile reconnect가 필요하다. | 채팅 |
| SSE+HTTP send | 서버→client stream과 기존 HTTP 쓰기를 분리한다. | 양방향 단일 channel은 아니다. | 알림·상태 업데이트 |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@rfc6455; @html-sse; @kafka-docs]를 참조한다.

## 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| Duplicate send | ack 유실 후 client가 같은 메시지를 다시 보낸다. | client message ID+conversation UNIQUE로 결과를 재사용한다. |
| Gateway loss | 수천 connection이 동시에 끊겨 reconnect storm이 발생한다. | exponential jitter, session TTL, regional admission을 적용한다. |
| Slow consumer | 한 장치가 읽지 못해 gateway memory queue가 커진다. | bounded queue, gap marker, sync API 전환을 사용한다. |
| Out-of-order fan-out | 다른 worker가 같은 방 메시지를 순서 다르게 전송한다. | conversation partition·sequence와 client reorder buffer를 사용한다. |
| Provider outage | push provider가 실패해 retry가 쌓이고 메시지가 늦어진다. | 채널별 circuit·retry budget·expiry·fallback 정책을 둔다. |
| Notification duplication | 여러 장치·재시도로 같은 push가 반복된다. | notification intent ID와 user-message-channel dedup을 사용한다. |

<!-- figure-spec
id: fig-ch36-02
chapter: ch36
role: notification-routing
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch36-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: notification intent가 사용자 선호·quiet hours·dedup·provider·fallback을 거치는 흐름을 보여준다.
required_labels_ko:
- Notification Intent
- Preference
- Quiet Hours
- Dedup
- Push Provider
- SMS/Email
- Expiry
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- rfc6455
- html-sse
- kafka-docs
alt_ko: notification intent가 사용자 선호·quiet hours·dedup·provider·fallback을 거치는 흐름을 보여준다.
caption_ko: notification intent가 사용자 선호·quiet hours·dedup·provider·fallback을 거치는 흐름을 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch36-02.md
-->

> **시각자료 제작 위치 — notification intent가 사용자 선호·quiet hours·dedup·provider·fallback을 거치는 흐름을 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch36-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch36-02.md`  
> 대체 텍스트: notification intent가 사용자 선호·quiet hours·dedup·provider·fallback을 거치는 흐름을 보여준다.


## 종합 설계 보조 도표

이 장은 앞의 원리를 하나의 서비스로 연결하므로 다음 보조 도표까지 제작한다.

<!-- figure-spec
id: fig-ch36-03
chapter: ch36
role: conversation-sequence
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch36-03.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: client ID·conversation sequence·dedup·reorder buffer를 보여준다.
required_labels_ko:
- Client Message ID
- Conversation Sequence
- Dedup
- Reorder Buffer
- ACK
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- rfc6455
- html-sse
- kafka-docs
alt_ko: client ID·conversation sequence·dedup·reorder buffer를 보여준다.
caption_ko: client ID·conversation sequence·dedup·reorder buffer를 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch36-03.md
-->

> **시각자료 제작 위치 — client ID·conversation sequence·dedup·reorder buffer를 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch36-03.svg`  
> 제작 명세: `assets/specs/svg/fig-ch36-03.md`  
> 대체 텍스트: client ID·conversation sequence·dedup·reorder buffer를 보여준다.


<!-- figure-spec
id: fig-ch36-04
chapter: ch36
role: fanout-strategies
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch36-04.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: fan-out-on-write, fan-out-on-read, 대형 broadcast 하이브리드를 비교한다.
required_labels_ko:
- Fan-out on Write
- Fan-out on Read
- 대형 방
- Inbox
- Message Log
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- rfc6455
- html-sse
- kafka-docs
alt_ko: fan-out-on-write, fan-out-on-read, 대형 broadcast 하이브리드를 비교한다.
caption_ko: fan-out-on-write, fan-out-on-read, 대형 broadcast 하이브리드를 비교한다
status: specified
spec_file: assets/specs/svg/fig-ch36-04.md
-->

> **시각자료 제작 위치 — fan-out-on-write, fan-out-on-read, 대형 broadcast 하이브리드를 비교한다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch36-04.svg`  
> 제작 명세: `assets/specs/svg/fig-ch36-04.md`  
> 대체 텍스트: fan-out-on-write, fan-out-on-read, 대형 broadcast 하이브리드를 비교한다.


<!-- figure-spec
id: fig-ch36-05
chapter: ch36
role: reconnect-sync
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch36-05.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: gateway 장애 후 jitter reconnect·cursor sync·gap recovery를 보여준다.
required_labels_ko:
- Gateway 장애
- Jitter Reconnect
- Cursor
- Sync API
- Gap Recovery
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- rfc6455
- html-sse
- kafka-docs
alt_ko: gateway 장애 후 jitter reconnect·cursor sync·gap recovery를 보여준다.
caption_ko: gateway 장애 후 jitter reconnect·cursor sync·gap recovery를 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch36-05.md
-->

> **시각자료 제작 위치 — gateway 장애 후 jitter reconnect·cursor sync·gap recovery를 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch36-05.svg`  
> 제작 명세: `assets/specs/svg/fig-ch36-05.md`  
> 대체 텍스트: gateway 장애 후 jitter reconnect·cursor sync·gap recovery를 보여준다.


## 확장 전략

- conversation ID를 event partition key로 사용하되 초대형 방은 별도 broadcast 경로를 둔다.
- connection gateway는 state를 최소화하고 session registry와 durable sync로 재연결을 허용한다.
- presence는 강한 일관성을 요구하지 않고 TTL·last-seen으로 근사한다.
- unread count는 파생 상태로 보고 reconciliation할 수 있게 한다.
- 알림은 priority·expiry·quiet hours로 backlog 가치를 제한한다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

## 보안과 개인정보

- 대화 membership과 메시지 접근은 fan-out과 sync 단계 모두 검증한다.
- 차단·방 탈퇴·계정 정지 변경이 오래된 session에 반영되게 version을 확인한다.
- 메시지 encryption을 적용할 경우 server search·moderation·multi-device key recovery 요구를 함께 평가한다.
- push payload에 민감 본문을 최소화한다.
- 보존·삭제·legal hold를 message와 파생 index에 적용한다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

## 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- active connection·reconnect·heartbeat timeout
- message accept/persist/ack latency와 duplicate
- conversation partition lag·fan-out delay
- gateway queue·gap/resync·slow consumer
- offline sync gap·cursor age
- channel별 notification success·provider latency·expiry

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

## 비용과 운영 복잡도

- 동시 connection이 gateway memory와 file descriptor의 주요 비용이다.
- fan-out event와 notification provider 호출·egress가 message 저장보다 크게 비용이 들 수 있다.
- 대형 방과 모든 장치 push는 별도 제품 tier·rate policy가 필요하다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

## 흔한 오해와 안티패턴

- WebSocket 연결 자체를 메시지 원장으로 취급한다.
- presence를 강한 실시간 사실로 표시한다.
- 읽음 상태를 모든 참가자에게 동기 transaction으로 fan-out한다.
- push provider 오류를 무기한 재시도한다.

## 설계 리뷰

- [ ] 메시지 성공 ack가 어떤 내구성을 의미하는가?
- [ ] conversation 순서와 client dedup이 정의됐는가?
- [ ] gateway 장애 후 reconnect·offline sync가 안전한가?
- [ ] slow consumer와 대형 방이 다른 사용자에게 영향을 주지 않는가?
- [ ] 알림 선호·expiry·provider 실패가 message 원장과 분리되는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

## 연습문제

1. 1:1 채팅의 메시지 상태 기계와 client retry를 설계하라.
2. 100만 명 broadcast 방을 fan-out-on-read로 처리하는 구조를 설계하라.
3. push provider 2시간 장애 시 오래된 알림을 보내지 않는 expiry 정책을 작성하라.

## 핵심 요약

- 실시간 연결은 일시적이고 메시지 원장은 내구적이어야 한다.
- 순서는 conversation 범위로 제한한다.
- client ID와 sequence로 중복·재정렬을 처리한다.
- slow consumer는 gap 후 sync API로 전환한다.
- 알림은 별도 intent·선호·expiry workflow다.

## 출처

- [@rfc6455] IETF. **RFC 6455 — The WebSocket Protocol** (2011). https://www.rfc-editor.org/rfc/rfc6455.html
- [@html-sse] WHATWG. **HTML Living Standard — Server-sent events** (2026). https://html.spec.whatwg.org/multipage/server-sent-events.html
- [@kafka-docs] Apache Software Foundation. **Apache Kafka Documentation** (2026). https://kafka.apache.org/documentation/
- [@aws-timeouts-retries] Amazon Web Services. **Timeouts, retries, and backoff with jitter** (2026). https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
