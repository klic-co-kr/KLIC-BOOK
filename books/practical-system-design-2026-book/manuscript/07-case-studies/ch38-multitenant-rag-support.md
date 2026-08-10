---
id: ch38
title: 멀티테넌트 RAG·AI 고객지원 플랫폼
part: case-studies
order: 38
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
- ch28
- ch31
- ch32
- ch33
- ch34
learning_objectives:
- 멀티테넌트 문서·검색·model·agent 경계를 종합 설계한다.
- tenant별 권한·품질·비용·데이터 위치를 강제한다.
- human handoff와 감사 가능한 고객지원 workflow를 만든다.
figures:
- fig-ch38-01
- fig-ch38-02
- fig-ch38-03
- fig-ch38-04
- fig-ch38-05
sources:
- azure-multitenant
- rag-paper
- nist-genai-profile
- owasp-llm
- otel-spec
draft_notice: 기술·편집·접근성 검수 전 초고
---

# 38. 멀티테넌트 RAG·AI 고객지원 플랫폼

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

## 이 장에서 해결할 문제

AI 고객지원 플랫폼은 챗봇 화면 하나가 아니라 tenant onboarding, 문서 수집, ACL, RAG, model routing, conversation, tool action, human handoff, evaluation, billing, deletion을 결합한 플랫폼이다. shared infrastructure에서도 모든 단계가 tenant context를 잃지 않아야 한다.

이 절의 기준 출처: [@azure-multitenant; @rag-paper].

### 학습 목표

- 멀티테넌트 문서·검색·model·agent 경계를 종합 설계한다.
- tenant별 권한·품질·비용·데이터 위치를 강제한다.
- human handoff와 감사 가능한 고객지원 workflow를 만든다.

## 먼저 결론

- tenant context는 gateway에서 생성해 문서·index·cache·model·tool·telemetry까지 전달하고 각 계층이 검증한다.
- 답변 생성과 고객 계정 변경·환불 같은 tool action은 별도 권한·승인 경계다.
- 품질·latency·cost를 tenant·language·intent·channel별로 분해한다.
- shared index와 dedicated index, shared model과 dedicated endpoint를 tenant 위험·규모·지역 정책에 따라 tiering한다.

::: current-note
**2026-08-06 확인:** 이 장은 변화 가능한 표준·프로젝트·AI 구현을 포함한다. 기본 재검토일은 `2026-11-06`이며, 출판 직전 공식 문서를 다시 확인한다.
:::

## 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | 멀티테넌트 RAG·AI 고객지원 플랫폼에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | tenant context는 gateway에서 생성해 문서·index·cache·model·tool·telemetry까지 전달하고 각 계층이 검증한다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | ingestion·retrieval·inference·tool을 tenant별 별도 quota와 bulkhead로 나눈다. |
| 실패·복구 | “Tenant context loss” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | 모든 key·event·span·policy에 signed tenant context와 server validation을 적용한다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | tenant identity를 모든 저장·event·cache·trace key에 포함하고 서버가 파생한다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | tenant별 answer success·grounding·handoff·CSAT |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

## 핵심 개념

### Tenant control plane

계약·region·quota·model policy·connector·retention을 관리한다.

### Tenant context

검증된 tenant ID, user, role, region, policy version을 가진 요청 범위다.

### Knowledge plane

문서 원장·ingestion·chunk·index·ACL을 제공한다.

### Conversation plane

session·message·summary·handoff 상태를 관리한다.

### Inference plane

retrieval·rerank·model route·streaming을 수행한다.

### Action plane

CRM·ticket·refund 등 tool을 policy와 approval 아래 실행한다.

### Human handoff

AI가 중단·escalate할 때 evidence와 context를 상담원에게 전달한다.

### Evaluation plane

tenant별 golden set·online quality·safety·cost를 관리한다.

### Metering

token·retrieval·tool·storage·human review 사용량을 계약 단위로 집계한다.

핵심 개념의 정의와 범위는 [@azure-multitenant; @rag-paper; @nist-genai-profile; @owasp-llm; @otel-spec]를 기준으로 재검토해야 한다.

### 서비스 계층 제안

| 계층 | 기본 격리 | 승격 조건 | 주요 제한 |
|---|---|---|---|
| Shared | 논리 tenant 격리, 공용 index/GPU | 지속적인 quota 초과, 규제, 품질 간섭 | 표준 model·보존·connector |
| Isolated Data | 공용 app, tenant 전용 DB/index | 대형 문서·강한 ACL·지역 요구 | 별도 lifecycle 비용 |
| Dedicated | 전용 data/index/inference | 계약상 강한 격리·성능 보장 | 높은 최소 비용·표준 운영만 허용 |

승격은 영업 요청만으로 결정하지 않는다. 실제 사용량, noisy-neighbor 지표, 데이터 지역, 보안 위험, unit economics를 함께 판단하고 되돌림·export 경로를 유지한다.

## 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| Tenant API gateway | auth·tenant resolution·quota·data region을 강제한다. |
| Control plane | tenant configuration과 policy version을 원장으로 관리한다. |
| Connector workers | tenant credential로 source를 수집한다. |
| Knowledge store/index | tenant ACL과 version을 가진 chunk·text/vector index를 제공한다. |
| Conversation service | channel message·summary·consent·handoff state를 저장한다. |
| RAG orchestrator | retrieval·rerank·context·citation을 수행한다. |
| Model router | tenant policy·risk·language·capacity로 model을 선택한다. |
| Tool gateway | capability·approval·idempotency·audit로 action을 실행한다. |
| Agent desktop | evidence·AI suggestion·customer state를 상담원에게 제공한다. |
| Evaluation/metering | quality·safety·cost·usage를 tenant별로 집계한다. |

<!-- figure-spec
id: fig-ch38-01
chapter: ch38
role: multitenant-ai-platform
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch38-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: control plane·knowledge·conversation·inference·action·evaluation plane과 tenant 경계를 보여준다.
required_labels_ko:
- Tenant Control Plane
- Knowledge Plane
- Conversation Plane
- Inference Plane
- Action Plane
- Evaluation Plane
- Tenant Boundary
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- azure-multitenant
- rag-paper
- nist-genai-profile
alt_ko: control plane·knowledge·conversation·inference·action·evaluation plane과 tenant 경계를 보여준다.
caption_ko: control plane·knowledge·conversation·inference·action·evaluation plane과 tenant 경계를 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch38-01.md
-->

> **시각자료 제작 위치 — control plane·knowledge·conversation·inference·action·evaluation plane과 tenant 경계를 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch38-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch38-01.md`  
> 대체 텍스트: control plane·knowledge·conversation·inference·action·evaluation plane과 tenant 경계를 보여준다.


## 요청·데이터 흐름

1. tenant admin이 region·connector·retention·model/tool policy를 설정한다.
2. connector가 tenant-scoped credential로 문서를 수집하고 ACL·version을 보존한다.
3. user message가 channel identity와 tenant context로 gateway에 도착한다.
4. conversation service가 consent·history·summary version을 불러온다.
5. RAG가 tenant/ACL filter로 evidence를 검색·rerank한다.
6. router가 intent·risk·language·SLO·budget으로 model을 선택한다.
7. answer는 citation·policy·PII 검사를 거쳐 streaming된다.
8. 계정 변경 등 action은 tool gateway와 필요 시 사용자/상담원 승인을 거친다.
9. uncertainty·policy·감정·요청에 따라 상담원에게 handoff한다.
10. 모든 단계의 사용량·품질·근거·action을 tenant scope로 기록한다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

## 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| Shared everything | 자원 효율과 onboarding 속도가 좋다. | noisy neighbor·격리·customization 위험이 크다. | 소규모 표준 tenant |
| Shared app, isolated data/index | 애플리케이션 효율과 데이터 격리를 균형 있게 제공한다. | tenant별 lifecycle·connection·cost 관리가 필요하다. | 중간/규제 tenant |
| Dedicated stack | 강한 격리·region·custom model 정책을 제공한다. | 비용·upgrade·운영 편차가 크다. | 대형·고위험 tenant |
| AI answer only | 안전하고 도입이 단순하다. | 업무 자동화 가치가 제한된다. | 초기/고위험 support |
| Tool-capable agent | 해결률과 자동화가 높다. | 권한·approval·사고 위험이 크다. | 제한된 반복 업무 |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@azure-multitenant; @rag-paper; @nist-genai-profile]를 참조한다.

## 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| Tenant context loss | 비동기 job·cache·trace에서 tenant ID가 빠져 데이터가 섞인다. | 모든 key·event·span·policy에 signed tenant context와 server validation을 적용한다. |
| Noisy neighbor | 한 tenant의 대량 ingestion/long prompt가 shared GPU·index를 포화시킨다. | tenant quota·bulkhead·weighted fair scheduling·dedicated tier를 사용한다. |
| ACL stale | source 권한 변경이 vector index에 늦게 반영된다. | change cursor·policy version·pre/post filter·deny fallback을 둔다. |
| Unsafe tool action | AI가 잘못된 고객에게 환불/변경을 실행한다. | resource lookup·preview·approval·idempotency·postcondition을 적용한다. |
| Model/provider outage | 특정 model route가 실패해 모든 tenant 응답이 중단된다. | policy-compatible fallback·queue·human handoff·status를 둔다. |
| Data deletion gap | tenant 탈퇴 후 backup·index·eval sample에 데이터가 남는다. | deletion workflow와 per-store completion evidence를 둔다. |
| Quality disparity | 평균 품질은 좋지만 특정 언어·제품군에서 반복 실패한다. | tenant/segment evaluation gate와 targeted human review를 사용한다. |

<!-- figure-spec
id: fig-ch38-02
chapter: ch38
role: ai-support-request-flow
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch38-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 사용자 message가 tenant auth·RAG·model·citation·tool approval·human handoff를 거치는 end-to-end 흐름을 보여준다.
required_labels_ko:
- 사용자
- Tenant Gateway
- RAG
- Model Router
- Citation Check
- Tool Approval
- Human Handoff
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- azure-multitenant
- rag-paper
- nist-genai-profile
alt_ko: 사용자 message가 tenant auth·RAG·model·citation·tool approval·human handoff를 거치는 end-to-end 흐름을 보여준다.
caption_ko: 사용자 message가 tenant auth·RAG·model·citation·tool approval·human handoff를 거치는 end-to-end 흐름을 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch38-02.md
-->

> **시각자료 제작 위치 — 사용자 message가 tenant auth·RAG·model·citation·tool approval·human handoff를 거치는 end-to-end 흐름을 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch38-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch38-02.md`  
> 대체 텍스트: 사용자 message가 tenant auth·RAG·model·citation·tool approval·human handoff를 거치는 end-to-end 흐름을 보여준다.


## 종합 설계 보조 도표

이 장은 앞의 원리를 하나의 서비스로 연결하므로 다음 보조 도표까지 제작한다.

<!-- figure-spec
id: fig-ch38-03
chapter: ch38
role: tenant-isolation-tiers
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch38-03.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: shared·isolated-data·dedicated tier의 자원·데이터·model 경계를 비교한다.
required_labels_ko:
- Shared
- Isolated Data
- Dedicated
- Tenant Boundary
- GPU
- Index
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- azure-multitenant
- rag-paper
- nist-genai-profile
alt_ko: shared·isolated-data·dedicated tier의 자원·데이터·model 경계를 비교한다.
caption_ko: shared·isolated-data·dedicated tier의 자원·데이터·model 경계를 비교한다
status: specified
spec_file: assets/specs/svg/fig-ch38-03.md
-->

> **시각자료 제작 위치 — shared·isolated-data·dedicated tier의 자원·데이터·model 경계를 비교한다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch38-03.svg`  
> 제작 명세: `assets/specs/svg/fig-ch38-03.md`  
> 대체 텍스트: shared·isolated-data·dedicated tier의 자원·데이터·model 경계를 비교한다.


<!-- figure-spec
id: fig-ch38-04
chapter: ch38
role: evaluation-and-metering
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch38-04.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: tenant별 품질·안전·latency·token·tool·human handoff를 집계하는 흐름을 보여준다.
required_labels_ko:
- Quality
- Safety
- Latency
- Token
- Tool
- Human Handoff
- Metering
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- azure-multitenant
- rag-paper
- nist-genai-profile
alt_ko: tenant별 품질·안전·latency·token·tool·human handoff를 집계하는 흐름을 보여준다.
caption_ko: tenant별 품질·안전·latency·token·tool·human handoff를 집계하는 흐름을 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch38-04.md
-->

> **시각자료 제작 위치 — tenant별 품질·안전·latency·token·tool·human handoff를 집계하는 흐름을 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch38-04.svg`  
> 제작 명세: `assets/specs/svg/fig-ch38-04.md`  
> 대체 텍스트: tenant별 품질·안전·latency·token·tool·human handoff를 집계하는 흐름을 보여준다.


<!-- figure-spec
id: fig-ch38-05
chapter: ch38
role: tenant-deletion-lifecycle
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch38-05.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 탈퇴 요청이 원문·index·cache·conversation·evaluation·backup에 전파되고 증거가 남는 흐름을 보여준다.
required_labels_ko:
- 삭제 요청
- 원문
- Index
- Cache
- Conversation
- Evaluation
- Backup
- 완료 증거
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- azure-multitenant
- rag-paper
- nist-genai-profile
alt_ko: 탈퇴 요청이 원문·index·cache·conversation·evaluation·backup에 전파되고 증거가 남는 흐름을 보여준다.
caption_ko: 탈퇴 요청이 원문·index·cache·conversation·evaluation·backup에 전파되고 증거가 남는 흐름을 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch38-05.md
-->

> **시각자료 제작 위치 — 탈퇴 요청이 원문·index·cache·conversation·evaluation·backup에 전파되고 증거가 남는 흐름을 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch38-05.svg`  
> 제작 명세: `assets/specs/svg/fig-ch38-05.md`  
> 대체 텍스트: 탈퇴 요청이 원문·index·cache·conversation·evaluation·backup에 전파되고 증거가 남는 흐름을 보여준다.


## 확장 전략

- ingestion·retrieval·inference·tool을 tenant별 별도 quota와 bulkhead로 나눈다.
- shared index는 tenant filter selectivity와 shard hotspot을 관측하고 대형 tenant를 전용 index로 이동한다.
- conversation summary와 retrieved context를 token budget으로 관리한다.
- model capacity는 tenant priority·SLO·contract에 따라 예약하고 overflow 정책을 둔다.
- control plane과 data plane을 분리해 tenant 설정 변경이 runtime 전체를 막지 않게 한다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

## 보안과 개인정보

- tenant identity를 모든 저장·event·cache·trace key에 포함하고 서버가 파생한다.
- connector credential과 tool capability는 tenant·source·action에 한정하고 짧은 수명으로 발급한다.
- retrieved 문서와 고객 message를 untrusted content로 취급해 system policy와 tool 권한을 분리한다.
- human agent와 AI가 본 개인정보를 role·purpose·case 기준으로 감사한다.
- data residency·retention·deletion·model provider 전송 정책을 tenant 계약에 반영한다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

## 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- tenant별 answer success·grounding·handoff·CSAT
- ingestion freshness·ACL lag·failed source
- retrieval zero-result·citation coverage·leak test
- model route·TTFT·token·fallback·quality
- tool allow/deny/approval/error/compensation
- quota·noisy-neighbor·dedicated tier migration
- tenant unit cost·gross margin·budget
- deletion workflow completion·audit gap

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

## 비용과 운영 복잡도

- tenant별 cost는 storage·index·embedding·retrieval·model token·tool API·human handoff를 합쳐야 한다.
- shared tier는 효율이 높지만 noisy-neighbor 방지용 여유와 격리 control 비용이 있다.
- dedicated stack은 높은 가격과 강한 요구에만 제공하고 운영 표준에서 벗어나는 customization을 제한한다.
- 답변 자동화율보다 해결된 case당 비용과 human rework를 본다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

## 흔한 오해와 안티패턴

- tenant ID를 prompt 문자열에만 넣고 인프라 key와 권한에서 강제하지 않는다.
- shared vector index의 post-filter만으로 격리가 충분하다고 생각한다.
- AI가 생성한 답변과 실제 고객 계정 action을 같은 권한으로 처리한다.
- 평균 품질과 전체 token 비용만 보고 tenant별 불공정·손실을 숨긴다.

## 설계 리뷰

- [ ] tenant context가 모든 sync/async 경계에서 보존·검증되는가?
- [ ] shared와 dedicated tier의 승격 조건이 객관적인가?
- [ ] ACL·삭제·지역 정책이 원문부터 telemetry까지 적용되는가?
- [ ] tool action이 capability·preview·approval·idempotency를 갖는가?
- [ ] tenant별 품질·SLO·비용·human handoff가 함께 관측되는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

## 연습문제

1. 공유 vector index에서 tenant ACL을 pre-filter·post-filter·citation 검증으로 구현하라.
2. 대형 tenant를 dedicated index와 model endpoint로 무중단 이동하는 계획을 작성하라.
3. 환불 tool을 호출할 수 있는 고객지원 agent의 승인·감사·보상 흐름을 설계하라.

## 핵심 요약

- 멀티테넌트 AI는 모든 계층에서 tenant context를 강제한다.
- knowledge·conversation·inference·action·evaluation plane을 분리한다.
- tool action은 답변 생성보다 강한 승인 경계가 필요하다.
- shared와 dedicated tier를 규모·위험·지역에 따라 선택한다.
- 품질·안전·비용을 tenant와 사용자 segment별로 운영한다.

## 출처

- [@azure-multitenant] Microsoft. **Azure Architecture Center — Multitenant solutions** (2026). https://learn.microsoft.com/azure/architecture/guide/multitenant/overview
- [@rag-paper] Patrick Lewis et al.. **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks** (2020). https://arxiv.org/abs/2005.11401
- [@nist-genai-profile] NIST. **Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile** (2024). https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- [@owasp-llm] OWASP Foundation. **OWASP Top 10 for LLM Applications** (2025). https://genai.owasp.org/llm-top-10/
- [@otel-spec] OpenTelemetry Authors. **OpenTelemetry Specification** (2026). https://opentelemetry.io/docs/specs/otel/

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
