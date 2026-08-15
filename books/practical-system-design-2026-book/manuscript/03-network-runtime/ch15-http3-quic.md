---
id: ch15
title: HTTP/1.1·HTTP/2·HTTP/3와 QUIC
part: network-runtime
order: 15
status: draft
freshness: current
last_verified: '2026-08-06'
review_due: '2027-02-06'
upstream_lineage:
- source: system-design-primer
  file: README.md
  anchor: communication
  action: REPLACE
audiences:
- backend-engineer
- platform-engineer
prerequisites:
- ch05
- ch13
- ch14
learning_objectives:
- HTTP 세대별 연결·스트림·head-of-line 특성을 비교한다.
- QUIC의 연결 설정·암호화·경로 변경이 운영에 미치는 영향을 설명한다.
- 프로토콜 선택을 실제 client·network·proxy 지원 조건과 연결한다.
figures:
- fig-ch15-01
- fig-ch15-02
sources:
- rfc9110
- rfc9112
- rfc9113
- rfc9000
- rfc9114
- rfc9204
draft_notice: 기술·편집·접근성 검수 전 초고
---

## 15. HTTP/1.1·HTTP/2·HTTP/3와 QUIC

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

### 이 장에서 해결할 문제

HTTP/3가 항상 더 빠른 것은 아니다. HTTP semantics는 유지되지만 전송은 QUIC 위에서 이루어지고, 독립 스트림·TLS 통합·connection migration 같은 특성을 얻는 대신 UDP 경로, 관측 도구, proxy 지원, QPACK 동작을 함께 검증해야 한다.

이 절의 기준 출처: [@rfc9110; @rfc9112].

#### 학습 목표

- HTTP 세대별 연결·스트림·head-of-line 특성을 비교한다.
- QUIC의 연결 설정·암호화·경로 변경이 운영에 미치는 영향을 설명한다.
- 프로토콜 선택을 실제 client·network·proxy 지원 조건과 연결한다.

### 먼저 결론

- HTTP/1.1은 여러 연결과 순차 요청, HTTP/2는 한 TCP 연결의 다중 스트림, HTTP/3는 QUIC 연결의 다중 스트림을 사용한다.
- HTTP/2의 서로 다른 스트림도 TCP packet loss 때문에 전송 계층 head-of-line 영향을 함께 받을 수 있다.
- HTTP/3는 QUIC stream 간 손실 격리를 제공하지만 congestion과 네트워크 경로는 공유한다.
- 0-RTT는 재전송 가능성을 고려해 안전한 요청에만 사용한다.

::: current-note
**2026-08-06 확인:** 이 장은 변화 가능한 표준·프로젝트·AI 구현을 포함한다. 기본 재검토일은 `2027-02-06`이며, 출판 직전 공식 문서를 다시 확인한다.
:::

### 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | HTTP/1.1·HTTP/2·HTTP/3와 QUIC에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | HTTP/1.1은 여러 연결과 순차 요청, HTTP/2는 한 TCP 연결의 다중 스트림, HTTP/3는 QUIC 연결의 다중 스트림을 사용한다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | 연결 수보다 stream 수·congestion·CPU 암호화 비용을 함께 본다. |
| 실패·복구 | “UDP 차단/제한” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | 빠른 fallback과 protocol별 성공률을 측정한다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | QUIC은 기본적으로 암호화되지만 endpoint 인증과 애플리케이션 권한은 여전히 필요하다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | protocol별 연결 성공·fallback·handshake 시간 |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

### 핵심 개념

#### HTTP semantics

method, status, field, representation 같은 의미는 HTTP 버전 간 공유된다.

#### Multiplexing

한 연결에서 여러 요청·응답 스트림을 동시에 진행하는 방식이다.

#### Head-of-line blocking

앞선 손실이나 작업 때문에 뒤의 독립 작업도 대기하는 현상이다.

#### QUIC connection

UDP 위에서 암호화·신뢰성·혼잡 제어·다중 스트림을 제공한다.

#### Connection ID

IP·port 변경과 독립적으로 연결을 식별해 경로 변경을 지원한다.

#### QPACK

HTTP/3에서 field compression을 수행하며 동적 table 의존과 blocking 한계를 관리한다.

#### 0-RTT

이전 연결 상태를 이용해 handshake 완료 전 application data를 보내는 방식으로 replay 위험이 있다.

핵심 개념의 정의와 범위는 [@rfc9110; @rfc9112; @rfc9113; @rfc9000; @rfc9114; @rfc9204]를 기준으로 재검토해야 한다.

### 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| 클라이언트 | 지원 protocol을 협상하고 연결·stream을 관리한다. |
| DNS/Alt-Svc 계층 | HTTP/3 endpoint 사용 가능성을 알린다. |
| Edge/QUIC endpoint | UDP 수신, TLS 1.3, QUIC transport를 처리한다. |
| HTTP gateway | 버전 간 변환과 request policy를 적용한다. |
| Origin service | HTTP semantics에 따라 요청을 처리한다. |
| Telemetry pipeline | protocol, handshake, loss, fallback을 기록한다. |

<!-- figure-spec
id: fig-ch15-01
chapter: ch15
role: http-generation-stack
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch15-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: HTTP/1.1·HTTP/2·HTTP/3의 application·compression·transport·security stack을 비교한다.
required_labels_ko:
- HTTP/1.1
- HTTP/2
- HTTP/3
- TCP
- QUIC
- TLS
- QPACK
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- rfc9110
- rfc9112
- rfc9113
alt_ko: HTTP/1.1·HTTP/2·HTTP/3의 application·compression·transport·security stack을 비교한다.
caption_ko: HTTP/1.1·HTTP/2·HTTP/3의 application·compression·transport·security stack을 비교한다
status: specified
spec_file: assets/specs/svg/fig-ch15-01.md
-->

> **시각자료 제작 위치 — HTTP/1.1·HTTP/2·HTTP/3의 application·compression·transport·security stack을 비교한다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch15-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch15-01.md`  
> 대체 텍스트: HTTP/1.1·HTTP/2·HTTP/3의 application·compression·transport·security stack을 비교한다.

### 요청·데이터 흐름

1. 클라이언트가 DNS와 이전 Alt-Svc 정보를 확인한다.
2. HTTP/3 가능 시 QUIC handshake와 TLS 인증을 수행한다.
3. 요청마다 독립 stream을 열고 HTTP field를 QPACK으로 표현한다.
4. packet loss는 해당 stream 데이터 재전송에 영향을 주되 다른 stream 전송은 계속될 수 있다.
5. gateway가 필요하면 origin의 HTTP/2 또는 HTTP/1.1로 변환한다.
6. 경로 변경 시 connection ID로 연결을 유지한다.
7. 실패 시 정책에 따라 다른 protocol로 fallback하고 이유를 기록한다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

### 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| HTTP/1.1 | 도구·서버·중간장비 호환성이 넓고 단순하다. | 병렬 처리를 위해 여러 연결이 필요하고 순차화 문제가 있다. | 단순 origin·legacy path |
| HTTP/2 | 한 TCP 연결에서 다중 스트림과 header compression을 제공한다. | TCP loss가 연결 내 모든 stream 전송을 지연시킬 수 있다. | 안정된 네트워크·내부 RPC |
| HTTP/3 | stream 손실 격리, 빠른 handshake, 경로 변경을 제공한다. | UDP 차단·CPU·관측·proxy 지원을 검증해야 한다. | 모바일·장거리·손실 네트워크 |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@rfc9110; @rfc9112; @rfc9113]를 참조한다.

### 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| UDP 차단/제한 | 기업망·방화벽이 QUIC을 차단하거나 낮은 timeout을 적용한다. | 빠른 fallback과 protocol별 성공률을 측정한다. |
| Handshake 실패 | 인증서·TLS·version negotiation 문제로 연결이 성립하지 않는다. | failure reason과 client/network 구간을 구분한다. |
| 0-RTT replay | 재전송된 초기 요청이 부작용을 두 번 만든다. | 멱등·안전한 요청만 허용하고 anti-replay 정책을 둔다. |
| QPACK blocking | 동적 table 참조가 도착하지 않아 header decoding이 기다린다. | blocked stream 한도와 table 전략을 조정한다. |
| Version translation mismatch | edge와 origin 사이 protocol 변환에서 timeout·stream reset 의미가 달라진다. | hop별 deadline·error mapping을 테스트한다. |

<!-- figure-spec
id: fig-ch15-02
chapter: ch15
role: stream-loss-comparison
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch15-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: HTTP/2 TCP packet loss와 HTTP/3 QUIC stream 손실의 영향 범위를 비교한다.
required_labels_ko:
- 연결
- Stream A
- Stream B
- Packet Loss
- 재전송
- 영향 범위
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- rfc9110
- rfc9112
- rfc9113
alt_ko: HTTP/2 TCP packet loss와 HTTP/3 QUIC stream 손실의 영향 범위를 비교한다.
caption_ko: HTTP/2 TCP packet loss와 HTTP/3 QUIC stream 손실의 영향 범위를 비교한다
status: specified
spec_file: assets/specs/svg/fig-ch15-02.md
-->

> **시각자료 제작 위치 — HTTP/2 TCP packet loss와 HTTP/3 QUIC stream 손실의 영향 범위를 비교한다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch15-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch15-02.md`  
> 대체 텍스트: HTTP/2 TCP packet loss와 HTTP/3 QUIC stream 손실의 영향 범위를 비교한다.

### 확장 전략

- 연결 수보다 stream 수·congestion·CPU 암호화 비용을 함께 본다.
- 모바일 경로 변경과 NAT rebinding을 실제 환경에서 시험한다.
- protocol rollout은 client·ASN·region별 canary로 시행한다.
- 큰 업로드·다운로드와 작은 API 요청이 같은 connection에서 경쟁할 때 우선순위 정책을 검토한다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

### 보안과 개인정보

- QUIC은 기본적으로 암호화되지만 endpoint 인증과 애플리케이션 권한은 여전히 필요하다.
- 0-RTT 데이터는 replay 가능성을 전제로 민감한 부작용 요청에서 금지한다.
- UDP flood와 connection ID abuse에 대한 rate limit·retry token·DDoS 보호를 둔다.
- 암호화로 전통적 네트워크 관측이 어려워지므로 endpoint telemetry를 강화한다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

### 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- protocol별 연결 성공·fallback·handshake 시간
- stream별 p95/p99와 packet loss·retransmission
- 0-RTT 시도·승인·거부·재시도
- QUIC CPU·메모리·connection migration
- edge-origin version 조합별 오류

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

### 비용과 운영 복잡도

- HTTP/3는 지연을 줄일 수 있지만 edge·CPU·관측·운영 도구 비용을 늘릴 수 있다.
- 한 connection의 효율은 좋아져도 장거리 egress 비용 자체는 줄지 않는다.
- 두 protocol을 장기간 동시에 운영하면 테스트 행렬과 장애 분석 비용이 증가한다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

### 흔한 오해와 안티패턴

- HTTP/3를 UDP 기반이라 신뢰성이 없다고 설명한다.
- HTTP/2면 애플리케이션의 모든 head-of-line 문제가 사라진다고 생각한다.
- 0-RTT를 모든 POST 요청에 허용한다.
- 벤치마크 한 번으로 모든 네트워크에서 HTTP/3가 빠르다고 결론낸다.

### 설계 리뷰

- [ ] 지원 client·network·proxy 조합이 실제 트래픽으로 검증됐는가?
- [ ] fallback이 빠르고 이유를 관측할 수 있는가?
- [ ] 0-RTT 허용 요청이 replay-safe한가?
- [ ] protocol 변환 hop에서 deadline·reset 의미가 보존되는가?
- [ ] CPU·loss·mobile 경로에서 p99 효과를 측정했는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

### 연습문제

1. 같은 리전 내부 RPC와 모바일 글로벌 API에 서로 다른 HTTP 버전 전략을 선택하라.
2. 0-RTT로 중복 결제가 발생할 수 있는 요청 흐름을 그리고 방지책을 제시하라.
3. HTTP/2 TCP loss와 HTTP/3 stream loss 격리를 시간축으로 비교하라.

### 핵심 요약

- HTTP semantics는 버전 간 공유되지만 transport 특성이 다르다.
- HTTP/2는 TCP, HTTP/3는 QUIC 위에서 다중 stream을 제공한다.
- HTTP/3는 stream 손실 격리와 경로 변경을 제공한다.
- 0-RTT는 replay 위험 때문에 제한적으로 사용한다.
- 실제 이득은 client·network·proxy별 관측으로 판단한다.

### 출처

- [@rfc9110] IETF. **RFC 9110 — HTTP Semantics** (2022). https://www.rfc-editor.org/rfc/rfc9110.html
- [@rfc9112] IETF. **RFC 9112 — HTTP/1.1** (2022). https://www.rfc-editor.org/rfc/rfc9112.html
- [@rfc9113] IETF. **RFC 9113 — HTTP/2** (2022). https://www.rfc-editor.org/rfc/rfc9113.html
- [@rfc9000] IETF. **RFC 9000 — QUIC: A UDP-Based Multiplexed and Secure Transport** (2021). https://www.rfc-editor.org/rfc/rfc9000.html
- [@rfc9114] IETF. **RFC 9114 — HTTP/3** (2022). https://www.rfc-editor.org/rfc/rfc9114.html
- [@rfc9204] IETF. **RFC 9204 — QPACK: Field Compression for HTTP/3** (2022). https://www.rfc-editor.org/rfc/rfc9204.html

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
