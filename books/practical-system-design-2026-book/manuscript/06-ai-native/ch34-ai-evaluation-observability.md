---
id: ch34
title: AI 평가·관측 가능성·보안·비용
part: ai-native
order: 34
status: draft
freshness: volatile
last_verified: '2026-08-06'
review_due: '2026-11-06'
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
- ch27
- ch28
- ch31
- ch32
- ch33
learning_objectives:
- offline·online·human 평가를 하나의 품질 체계로 연결한다.
- AI telemetry를 품질·안전·지연·비용 지표로 구성한다.
- 위협·회귀·모델 변경을 risk-based release gate로 관리한다.
figures:
- chart-ch34-01
- fig-ch34-01
- fig-ch34-02
sources:
- nist-ai-rmf
- nist-genai-profile
- owasp-llm
- ragas-paper
draft_notice: 기술·편집·접근성 검수 전 초고
---

## 34. AI 평가·관측 가능성·보안·비용

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

### 이 장에서 해결할 문제

AI 시스템의 “정확도”는 단일 숫자가 아니다. task success, retrieval, factual support, policy compliance, latency, cost, user segment를 함께 봐야 한다. 평가 데이터와 운영 telemetry의 계보가 없으면 model이나 prompt 변경의 실제 효과를 설명할 수 없다.

이 절의 기준 출처: [@nist-ai-rmf; @nist-genai-profile].

#### 학습 목표

- offline·online·human 평가를 하나의 품질 체계로 연결한다.
- AI telemetry를 품질·안전·지연·비용 지표로 구성한다.
- 위협·회귀·모델 변경을 risk-based release gate로 관리한다.

### 먼저 결론

- golden set는 실제 실패 분포와 중요 사용자군을 반영하고 versioning한다.
- 자동 judge는 편향·불안정성이 있으므로 규칙·원문 검증·사람 평가와 교차한다.
- offline 점수가 좋아도 online latency·abstention·사용자 행동·안전 결과를 canary로 검증한다.
- 비용은 call당이 아니라 품질 기준을 통과한 업무 결과당 계산한다.

::: current-note
**2026-08-06 확인:** 이 장은 변화 가능한 표준·프로젝트·AI 구현을 포함한다. 기본 재검토일은 `2026-11-06`이며, 출판 직전 공식 문서를 다시 확인한다.
:::

### 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | AI 평가·관측 가능성·보안·비용에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | golden set는 실제 실패 분포와 중요 사용자군을 반영하고 versioning한다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | evaluation workload를 batch·cache하되 non-determinism과 model version을 기록한다. |
| 실패·복구 | “Benchmark overfit” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | holdout·fresh failure set·online canary를 사용한다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | 평가 dataset에 개인정보·저작권·기밀 문서가 포함되는지 provenance와 consent를 관리한다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | offline task/retrieval/grounding/safety score |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

<!-- figure-spec
id: chart-ch34-01
chapter: ch34
role: ai-quality-cost-frontier
kind: data-chart
generator: python-matplotlib
output: assets/charts/chart-ch34-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 여러 model/routing 정책을 품질, latency, accepted outcome당 비용으로 비교하고 지배되는 선택을 표시한다.
required_labels_ko:
- Accepted Outcome당 비용
- 품질 점수
- 정책 후보
- Pareto frontier
prohibited:
- 출처 없는 실측 수치
- 3D chart
- 잘린 축
- 색상만으로 구분
source_refs:
- nist-ai-rmf
- nist-genai-profile
alt_ko: 여러 model/routing 정책을 품질, latency, accepted outcome당 비용으로 비교하고 지배되는 선택을 표시한다.
caption_ko: AI 품질·지연·비용 Pareto
status: specified
spec_file: assets/specs/charts/chart-ch34-01.md
-->

> **시각자료 제작 위치 — AI 품질·지연·비용 Pareto**  
> 종류: `data-chart` · 상태: `specified` · 산출 경로: `assets/charts/chart-ch34-01.svg`  
> 제작 명세: `assets/specs/charts/chart-ch34-01.md`  
> 대체 텍스트: 여러 model/routing 정책을 품질, latency, accepted outcome당 비용으로 비교하고 지배되는 선택을 표시한다.

### 핵심 개념

#### Task success

사용자가 의도한 업무를 완료했는지 평가하는 최종 지표다.

#### Golden dataset

입력, 기대 기준, segment, provenance를 가진 재현 가능한 평가 집합이다.

#### Model-based judge

모델을 사용해 answer를 평가하는 방법이며 calibration과 독립 검증이 필요하다.

#### Groundedness

답변 claim이 제공된 evidence에 의해 지지되는 정도다.

#### Safety evaluation

금지 행동, 데이터 노출, prompt injection, 도구 오용 같은 위험을 시험한다.

#### Online experiment

실제 traffic 일부에서 변경을 비교하는 canary/A-B/shadow 방식이다.

#### Drift

입력·문서·사용자·model 행동 분포가 기준에서 변하는 현상이다.

#### Unit cost

요청, token, 성공 업무, 승인된 답변 등 의미 있는 단위당 비용이다.

핵심 개념의 정의와 범위는 [@nist-ai-rmf; @nist-genai-profile; @owasp-llm; @ragas-paper]를 기준으로 재검토해야 한다.

### 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| Evaluation registry | dataset·rubric·judge·threshold·version을 관리한다. |
| Offline runner | 재현 가능한 model/prompt/retrieval 조합을 실행한다. |
| Safety red-team suite | 공격·오용·권한 경계 시나리오를 검증한다. |
| Release gate | segment별 품질·안전·latency·cost 기준을 평가한다. |
| Online telemetry | trace·token·route·citation·feedback을 기록한다. |
| Human review queue | 고위험·불확실·분쟁 sample을 평가한다. |
| Drift monitor | 입력·검색·답변·비용 분포 변화를 감지한다. |
| Incident workflow | rollback·disable tool·model fallback·사용자 통지를 수행한다. |

<!-- figure-spec
id: fig-ch34-01
chapter: ch34
role: ai-evaluation-loop
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch34-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: dataset·offline eval·safety test·release gate·canary·online telemetry·human review·failure feedback loop를 보여준다.
required_labels_ko:
- Evaluation Dataset
- Offline Eval
- Safety Test
- Release Gate
- Canary
- Online Telemetry
- Human Review
- Failure Set
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- nist-ai-rmf
- nist-genai-profile
- owasp-llm
alt_ko: dataset·offline eval·safety test·release gate·canary·online telemetry·human review·failure feedback loop를 보여준다.
caption_ko: dataset·offline eval·safety test·release gate·canary·online telemetry·human review·failure feedback loop를 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch34-01.md
-->

> **시각자료 제작 위치 — dataset·offline eval·safety test·release gate·canary·online telemetry·human review·failure feedback loop를 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch34-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch34-01.md`  
> 대체 텍스트: dataset·offline eval·safety test·release gate·canary·online telemetry·human review·failure feedback loop를 보여준다.

### 요청·데이터 흐름

1. 변경마다 대상 task·risk·segment와 성공 기준을 정의한다.
2. 고정된 dataset과 새 failure set에서 offline 평가한다.
3. retrieval·generation·tool·policy 결과를 단계별로 기록한다.
4. 자동 judge와 규칙 결과를 human calibration sample로 검증한다.
5. release gate 통과 후 shadow 또는 작은 canary traffic을 사용한다.
6. online 품질·안전·latency·cost를 baseline과 비교한다.
7. drift·incident 시 route·prompt·tool을 독립 rollback한다.
8. 실제 failure를 redacted evaluation case로 환류한다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

### 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| 정적 golden set | 재현성과 회귀 비교가 좋다. | 운영 분포 변화와 미지 failure를 놓친다. | CI regression |
| Online feedback | 실사용 가치와 segment 차이를 반영한다. | 선택 편향·노이즈·개인정보가 있다. | 제품 개선 |
| Human expert review | 고위험 domain과 미묘한 정확성을 평가한다. | 비용·속도·평가자 일관성 문제가 있다. | 법률·의료·정책 |
| Model judge | 대규모 평가를 빠르게 확장한다. | judge 편향·self-preference·prompt sensitivity가 있다. | 보조 평가와 triage |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@nist-ai-rmf; @nist-genai-profile; @owasp-llm]를 참조한다.

### 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| Benchmark overfit | golden set에만 맞춰 실제 query 품질이 악화된다. | holdout·fresh failure set·online canary를 사용한다. |
| Judge drift | judge model/version 변경으로 점수 기준이 달라진다. | judge version pinning·calibration·human anchor를 둔다. |
| Telemetry leakage | prompt·문서·답변 원문이 관측 backend에 광범위 저장된다. | redaction·hash·selective capture·access control을 적용한다. |
| Silent safety regression | 새 model route가 특정 언어에서 정책을 우회한다. | segment별 adversarial suite와 canary deny metric을 둔다. |
| Cost-quality inversion | 저렴한 model이 재질문·human review를 늘려 전체 비용이 커진다. | accepted outcome당 비용과 rework를 계산한다. |
| Feedback poisoning | 악의적 사용자가 학습·평가 feedback을 조작한다. | source weighting·abuse detection·human validation을 적용한다. |

<!-- figure-spec
id: fig-ch34-02
chapter: ch34
role: ai-quality-scorecard
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch34-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 품질·grounding·안전·지연·비용·segment를 하나의 release scorecard로 보여준다.
required_labels_ko:
- Task Success
- Grounding
- Safety
- Latency
- Cost
- Segment
- Threshold
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- nist-ai-rmf
- nist-genai-profile
- owasp-llm
alt_ko: 품질·grounding·안전·지연·비용·segment를 하나의 release scorecard로 보여준다.
caption_ko: 품질·grounding·안전·지연·비용·segment를 하나의 release scorecard로 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch34-02.md
-->

> **시각자료 제작 위치 — 품질·grounding·안전·지연·비용·segment를 하나의 release scorecard로 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch34-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch34-02.md`  
> 대체 텍스트: 품질·grounding·안전·지연·비용·segment를 하나의 release scorecard로 보여준다.

### 확장 전략

- evaluation workload를 batch·cache하되 non-determinism과 model version을 기록한다.
- 전체 traffic 원문을 저장하지 않고 위험 기반 sample과 privacy-safe aggregate를 사용한다.
- segment 수를 무제한 늘리지 않고 business/risk에 중요한 slice를 고정한다.
- human review는 uncertainty·risk·novelty로 우선순위를 정한다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

### 보안과 개인정보

- 평가 dataset에 개인정보·저작권·기밀 문서가 포함되는지 provenance와 consent를 관리한다.
- red-team 결과와 exploit prompt는 제한된 접근으로 보존한다.
- tool-capable agent는 read-only sandbox와 synthetic resource에서 공격 평가한다.
- 사용자 피드백을 자동 장기 memory나 학습 데이터로 승격하지 않는다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

### 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- offline task/retrieval/grounding/safety score
- segment별 abstention·escalation·user correction
- TTFT·end latency·tool success·route
- input/output/retrieval/tool token과 unit cost
- policy deny·prompt injection·data leak test
- judge-human agreement·drift·evaluation coverage

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

### 비용과 운영 복잡도

- 평가 비용 자체가 model call·expert 시간·dataset 유지 비용을 만든다.
- 모든 query를 고비용 model과 human으로 검사하지 않고 risk tiering을 사용한다.
- 단순 call당 비용 최적화가 rework·지원·안전 사고 비용을 키울 수 있다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

### 흔한 오해와 안티패턴

- 한 개 benchmark 점수를 제품 품질로 동일시한다.
- LLM judge 결과를 정답처럼 사용한다.
- 전체 prompt와 응답을 무기한 로그로 남긴다.
- 평균 품질 향상으로 취약 사용자 segment 회귀를 숨긴다.

### 설계 리뷰

- [ ] task·risk·segment별 합격 기준이 명확한가?
- [ ] dataset·prompt·model·retrieval·judge version이 재현 가능한가?
- [ ] 자동 평가가 human anchor와 교정되는가?
- [ ] online canary와 독립 rollback 단위가 있는가?
- [ ] 품질·안전·지연·비용을 accepted outcome으로 함께 보는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

### 연습문제

1. RAG 변경을 retrieval recall, groundedness, answer utility로 분리한 평가표를 만들라.
2. judge model 교체 전후 점수 기준을 calibration하는 방법을 설계하라.
3. 고위험 agent tool 기능을 synthetic environment에서 red-team하는 계획을 작성하라.

### 핵심 요약

- AI 품질은 다차원이고 segment별이다.
- offline·online·human 평가를 연결한다.
- 평가 도구와 judge도 version·calibration이 필요하다.
- telemetry는 개인정보와 비용 통제를 받는다.
- accepted outcome당 품질·안전·비용으로 release를 결정한다.

### 출처

- [@nist-ai-rmf] NIST. **Artificial Intelligence Risk Management Framework (AI RMF 1.0)** (2023). https://www.nist.gov/itl/ai-risk-management-framework
- [@nist-genai-profile] NIST. **Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile** (2024). https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- [@owasp-llm] OWASP Foundation. **OWASP Top 10 for LLM Applications** (2025). https://genai.owasp.org/llm-top-10/
- [@ragas-paper] Shahul Es et al.. **RAGAS: Automated Evaluation of Retrieval Augmented Generation** (2023). https://arxiv.org/abs/2309.15217

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
