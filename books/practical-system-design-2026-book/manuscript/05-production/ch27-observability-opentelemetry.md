---
id: ch27
title: Metrics·Logs·Traces와 OpenTelemetry
part: production
order: 27
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
- ch04
- ch05
learning_objectives:
- metrics·logs·traces의 서로 다른 질문을 구분한다.
- OpenTelemetry 계측·수집·export 경계를 설계한다.
- cardinality·sampling·민감 데이터 비용을 통제한다.
figures:
- chart-ch27-01
- fig-ch27-01
- fig-ch27-02
sources:
- otel-spec
- w3c-trace-context
- google-sre-slo
draft_notice: 기술·편집·접근성 검수 전 초고
---

# 27. Metrics·Logs·Traces와 OpenTelemetry

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

## 이 장에서 해결할 문제

관측 가능성은 telemetry를 많이 저장하는 것이 아니라 내부 상태를 외부 신호로 설명할 수 있게 만드는 능력이다. SLO와 장애 질문에서 출발해 metrics, logs, traces를 최소한으로 연결하고, correlation ID와 semantic convention을 일관되게 사용해야 한다.

이 절의 기준 출처: [@otel-spec; @w3c-trace-context].

### 학습 목표

- metrics·logs·traces의 서로 다른 질문을 구분한다.
- OpenTelemetry 계측·수집·export 경계를 설계한다.
- cardinality·sampling·민감 데이터 비용을 통제한다.

## 먼저 결론

- metrics는 집계 추세, logs는 개별 사건, traces는 분산 요청의 인과 경로에 강하다.
- OpenTelemetry는 계측과 telemetry 파이프라인의 vendor-neutral 경계를 제공하지만 backend·보존·경보 설계까지 자동으로 결정하지 않는다.
- 고 cardinality attribute를 metric label로 사용하면 비용과 안정성이 무너질 수 있다.
- sampling은 비용 절감과 rare failure 보존 사이의 정책이다.

::: current-note
**2026-08-06 확인:** 이 장은 변화 가능한 표준·프로젝트·AI 구현을 포함한다. 기본 재검토일은 `2027-02-06`이며, 출판 직전 공식 문서를 다시 확인한다.
:::

## 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | Metrics·Logs·Traces와 OpenTelemetry에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | metrics는 집계 추세, logs는 개별 사건, traces는 분산 요청의 인과 경로에 강하다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | collector를 지역·cluster 단위로 계층화하되 제어 설정과 pipeline version을 관리한다. |
| 실패·복구 | “Cardinality explosion” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | bounded dimension만 metric에 사용하고 상세 값은 trace/log로 보낸다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | telemetry는 운영 데이터이지만 개인정보·비밀·인증 token을 포함할 수 있어 별도 보안 영역으로 다룬다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | telemetry ingest·drop·retry·queue |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

<!-- figure-spec
id: chart-ch27-01
chapter: ch27
role: telemetry-cardinality
kind: data-chart
generator: python-matplotlib
output: assets/charts/chart-ch27-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: label dimension을 추가할 때 조합 가능한 time series 수가 곱셈으로 증가하는 모습을 보여준다.
required_labels_ko:
- 추가 Dimension 수
- 예상 Series 수(로그 축)
- bounded labels
- user_id 포함
prohibited:
- 출처 없는 실측 수치
- 3D chart
- 잘린 축
- 색상만으로 구분
source_refs:
- otel-spec
- w3c-trace-context
alt_ko: label dimension을 추가할 때 조합 가능한 time series 수가 곱셈으로 증가하는 모습을 보여준다.
caption_ko: Metric cardinality와 비용
status: specified
spec_file: assets/specs/charts/chart-ch27-01.md
-->

> **시각자료 제작 위치 — Metric cardinality와 비용**  
> 종류: `data-chart` · 상태: `specified` · 산출 경로: `assets/charts/chart-ch27-01.svg`  
> 제작 명세: `assets/specs/charts/chart-ch27-01.md`  
> 대체 텍스트: label dimension을 추가할 때 조합 가능한 time series 수가 곱셈으로 증가하는 모습을 보여준다.


## 핵심 개념

### Metric

시간에 따른 수치 집계로 rate·histogram·gauge 등을 표현한다.

### Log

특정 시점의 구조화된 사건 record다.

### Trace

하나의 분산 작업을 span과 parent-child 관계로 표현한다.

### Context propagation

trace ID, baggage, deadline 같은 context를 hop 사이 전달하는 과정이다.

### Collector

telemetry를 수신·처리·batch·filter·export하는 구성 요소다.

### Cardinality

label/attribute 값 조합의 수로 metric storage와 query 비용에 큰 영향을 준다.

### Sampling

전체 trace 중 일부를 선택하는 정책으로 head·tail·rule-based 방식이 있다.

### Semantic convention

HTTP, DB, messaging 등 공통 attribute 이름과 의미를 정의하는 규칙이다.

핵심 개념의 정의와 범위는 [@otel-spec; @w3c-trace-context; @google-sre-slo]를 기준으로 재검토해야 한다.

## 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| Instrumentation | 애플리케이션과 library가 span·metric·log를 생성한다. |
| SDK/agent | context·processor·exporter를 관리한다. |
| Local/central collector | batch·retry·redaction·sampling을 수행한다. |
| Telemetry backend | 시계열·로그·trace를 저장·조회한다. |
| SLO/alert engine | 사용자 지표와 burn rate를 평가한다. |
| Investigation workflow | alert에서 trace·log·deployment·profile로 이동한다. |
| Governance | schema·retention·PII·cost budget을 관리한다. |

<!-- figure-spec
id: fig-ch27-01
chapter: ch27
role: observability-pipeline
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch27-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 애플리케이션 instrumentation에서 collector 처리와 metrics/logs/traces backend로 가는 흐름을 보여준다.
required_labels_ko:
- Instrumentation
- SDK
- Collector
- Metrics
- Logs
- Traces
- SLO Alert
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- otel-spec
- w3c-trace-context
- google-sre-slo
alt_ko: 애플리케이션 instrumentation에서 collector 처리와 metrics/logs/traces backend로 가는 흐름을 보여준다.
caption_ko: 애플리케이션 instrumentation에서 collector 처리와 metrics/logs/traces backend로 가는 흐름을 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch27-01.md
-->

> **시각자료 제작 위치 — 애플리케이션 instrumentation에서 collector 처리와 metrics/logs/traces backend로 가는 흐름을 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch27-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch27-01.md`  
> 대체 텍스트: 애플리케이션 instrumentation에서 collector 처리와 metrics/logs/traces backend로 가는 흐름을 보여준다.


## 요청·데이터 흐름

1. 사용자 여정과 장애 질문에서 필요한 신호를 정한다.
2. 공통 resource·service·deployment 식별자를 정의한다.
3. entry에서 trace context를 만들거나 신뢰된 parent를 검증한다.
4. 주요 경계와 고비용 작업에 span과 metric을 기록한다.
5. collector에서 redaction·batch·sampling·retry를 수행한다.
6. SLO alert가 exemplar/trace로 조사 경로를 제공한다.
7. telemetry 비용과 query 사용률로 schema를 지속 정리한다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

## 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| 직접 backend SDK | 구성이 단순하고 backend 기능을 빠르게 사용한다. | vendor lock-in과 계측 중복이 커질 수 있다. | 작은 단일 backend 시스템 |
| OpenTelemetry SDK+Collector | 계측·export 경계를 표준화하고 pipeline 제어가 가능하다. | collector 운영과 semantic version 관리가 필요하다. | 다언어·다중 backend 시스템 |
| Agent/eBPF 중심 | 코드 변경 없이 넓은 가시성을 얻는다. | 업무 의미·사용자 context가 부족할 수 있다. | legacy·인프라 관측 보완 |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@otel-spec; @w3c-trace-context; @google-sre-slo]를 참조한다.

## 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| Cardinality explosion | user ID·URL 원문·request ID를 metric label로 넣어 시계열 수가 폭증한다. | bounded dimension만 metric에 사용하고 상세 값은 trace/log로 보낸다. |
| Telemetry outage | collector 장애가 app thread를 막거나 memory queue를 채운다. | 비차단 export, 유한 queue, drop metric, local buffering 한도를 둔다. |
| Broken context | async·queue 경계에서 trace parent가 유실된다. | 표준 propagation과 message link/correlation을 사용한다. |
| Sampling blind spot | head sampling이 드문 오류 trace를 버린다. | tail sampling·error keep rule·exemplar를 적용한다. |
| PII leakage | header·SQL·prompt·document 내용이 telemetry에 복사된다. | allowlist·redaction·classification·access control을 둔다. |

<!-- figure-spec
id: fig-ch27-02
chapter: ch27
role: signal-correlation
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch27-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: SLO 경보에서 exemplar·trace·span log·deployment change로 조사하는 경로를 보여준다.
required_labels_ko:
- SLO Alert
- Metric Exemplar
- Trace
- Span
- Structured Log
- Deployment
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- otel-spec
- w3c-trace-context
- google-sre-slo
alt_ko: SLO 경보에서 exemplar·trace·span log·deployment change로 조사하는 경로를 보여준다.
caption_ko: SLO 경보에서 exemplar·trace·span log·deployment change로 조사하는 경로를 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch27-02.md
-->

> **시각자료 제작 위치 — SLO 경보에서 exemplar·trace·span log·deployment change로 조사하는 경로를 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch27-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch27-02.md`  
> 대체 텍스트: SLO 경보에서 exemplar·trace·span log·deployment change로 조사하는 경로를 보여준다.


## 확장 전략

- collector를 지역·cluster 단위로 계층화하되 제어 설정과 pipeline version을 관리한다.
- high-volume signal은 aggregation·sampling·short retention을 사용한다.
- trace sampling은 service별이 아니라 end-to-end decision 일관성을 유지한다.
- log와 trace를 같은 ID로 연결하되 모든 log에 trace가 있을 필요는 없다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

## 보안과 개인정보

- telemetry는 운영 데이터이지만 개인정보·비밀·인증 token을 포함할 수 있어 별도 보안 영역으로 다룬다.
- collector와 backend 사이를 인증·암호화하고 tenant 접근을 분리한다.
- baggage는 downstream에 전파되므로 민감 정보를 넣지 않는다.
- 보존·삭제·export 정책을 원본 데이터와 일치시킨다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

## 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- telemetry ingest·drop·retry·queue
- metric series cardinality와 top attributes
- trace sampling rate·error kept·broken context
- log bytes·query rate·retention
- SLO alert에서 원인 trace까지 연결 성공률
- 계측 overhead CPU·memory·latency

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

## 비용과 운영 복잡도

- observability 비용은 ingest×retention×index cardinality×query로 커진다.
- 모든 trace를 영구 저장하기보다 목적별 sampling과 tiered retention을 사용한다.
- 표준화는 초기 platform 비용이 들지만 중복 agent·SDK·dashboard를 줄인다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

## 흔한 오해와 안티패턴

- 로그가 많으면 관측 가능하다고 생각한다.
- 모든 값을 metric label로 넣는다.
- trace sampling을 각 서비스가 독립 결정한다.
- telemetry pipeline 실패가 서비스 요청을 실패시키게 한다.

## 설계 리뷰

- [ ] 각 signal이 답하려는 운영 질문이 명확한가?
- [ ] SLO에서 trace·log로 내려가는 조사 경로가 있는가?
- [ ] cardinality와 PII가 schema 수준에서 제한되는가?
- [ ] collector 장애가 app에 backpressure를 주지 않는가?
- [ ] sampling이 rare failure와 비용 목표를 함께 만족하는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

## 연습문제

1. 사용자 ID를 metric label로 쓰지 않고 고객별 장애를 조사하는 방식을 설계하라.
2. 비동기 queue consumer trace를 producer trace와 link하는 context를 설계하라.
3. 월 telemetry 예산을 기준으로 trace sampling·retention 정책을 작성하라.

## 핵심 요약

- metrics·logs·traces는 서로 다른 질문에 답한다.
- OpenTelemetry는 계측·수집 경계를 표준화한다.
- cardinality·sampling·retention은 비용과 품질을 결정한다.
- context propagation이 end-to-end 인과 관계를 만든다.
- telemetry 자체도 장애·보안·SLO 대상이다.

## 출처

- [@otel-spec] OpenTelemetry Authors. **OpenTelemetry Specification** (2026). https://opentelemetry.io/docs/specs/otel/
- [@w3c-trace-context] W3C. **Trace Context** (2021). https://www.w3.org/TR/trace-context/
- [@google-sre-slo] Google. **SRE Workbook — Implementing SLOs** (2018). https://sre.google/workbook/implementing-slos/

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
