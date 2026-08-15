---
id: ch33
title: Agent 상태·메모리·도구 실행·승인 경계
part: ai-native
order: 33
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
- ch24
- ch28
- ch31
- ch32
learning_objectives:
- 에이전트를 상태 기계와 외부 도구 실행 시스템으로 설계한다.
- 대화 메모리·업무 상태·장기 지식을 구분한다.
- 위험 도구에 승인·sandbox·idempotency·감사를 적용한다.
figures:
- fig-ch33-01
- fig-ch33-02
sources:
- react-paper
- toolformer-paper
- nist-ai-rmf
- owasp-llm
draft_notice: 기술·편집·접근성 검수 전 초고
---

## 33. Agent 상태·메모리·도구 실행·승인 경계

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

### 이 장에서 해결할 문제

에이전트는 “스스로 생각하는 챗봇”이 아니라 불확실한 model 출력이 상태를 읽고 도구를 호출하는 orchestration 시스템이다. 따라서 각 step의 입력·권한·예산·승인·결과를 명시적으로 기록하고, side effect는 일반 분산 transaction처럼 다뤄야 한다.

이 절의 기준 출처: [@react-paper; @toolformer-paper].

#### 학습 목표

- 에이전트를 상태 기계와 외부 도구 실행 시스템으로 설계한다.
- 대화 메모리·업무 상태·장기 지식을 구분한다.
- 위험 도구에 승인·sandbox·idempotency·감사를 적용한다.

### 먼저 결론

- 모델의 자연어 계획을 직접 권한으로 취급하지 않는다.
- 대화 context, 작업 상태, 사용자 선호, 장기 지식을 서로 다른 저장소와 수명으로 관리한다.
- 읽기 도구와 쓰기 도구, 되돌릴 수 있는 action과 비가역 action을 구분한다.
- 도구 호출은 schema validation·policy·idempotency·approval을 통과한 뒤 실행한다.

::: current-note
**2026-08-06 확인:** 이 장은 변화 가능한 표준·프로젝트·AI 구현을 포함한다. 기본 재검토일은 `2026-11-06`이며, 출판 직전 공식 문서를 다시 확인한다.
:::

### 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | Agent 상태·메모리·도구 실행·승인 경계에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | 모델의 자연어 계획을 직접 권한으로 취급하지 않는다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | run은 독립 partition으로 scale하되 한 run의 state update는 optimistic concurrency로 직렬화한다. |
| 실패·복구 | “Prompt injection” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | data/instruction 경계를 유지하고 tool 권한을 정책이 결정한다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | agent에 사용자의 전체 권한을 전달하지 않고 작업별 capability를 발급한다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | run success·abstain·manual handoff·step count |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

### 핵심 개념

#### Agent loop

관찰→계획/선택→도구 호출→결과 반영을 제한된 step 안에서 반복하는 실행 구조다.

#### Run state

목표, 현재 step, 도구 결과, budget, terminal status를 가진 업무 상태다.

#### Conversation memory

현재 대화의 최근 맥락으로 수명이 짧다.

#### Long-term memory

사용자 선호·사실·요약 등을 별도 승인과 provenance로 저장한 데이터다.

#### Tool contract

도구 이름, input/output schema, 권한, idempotency, timeout, side effect를 정의한다.

#### Approval gate

고위험 action 전에 사용자 또는 정책 승인 증거를 요구하는 단계다.

#### Sandbox

파일·네트워크·프로세스 접근을 제한한 실행 환경이다.

#### Compensation

이미 수행된 action을 상쇄하거나 수동 복구하는 후속 작업이다.

핵심 개념의 정의와 범위는 [@react-paper; @toolformer-paper; @nist-ai-rmf; @owasp-llm]를 기준으로 재검토해야 한다.

### 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| Agent API | 사용자 목표와 session identity를 받는다. |
| Run state store | step·version·status·budget을 원장으로 보존한다. |
| Planner/model | 다음 action 후보와 인자를 생성한다. |
| Policy engine | tool·resource·tenant·risk·approval을 평가한다. |
| Tool gateway | schema·timeout·idempotency·sandbox를 강제한다. |
| Approval service | 사람 승인과 scope·expiry를 기록한다. |
| Memory service | 수명·provenance·삭제 정책별 memory를 관리한다. |
| Audit/evaluation | 모든 결정·호출·결과·override를 추적한다. |

<!-- figure-spec
id: fig-ch33-01
chapter: ch33
role: agent-control-loop
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch33-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 사용자 목표·run state·model·policy·approval·tool gateway·audit의 제어 루프를 보여준다.
required_labels_ko:
- 사용자 목표
- Run State
- Model
- Policy Engine
- Approval
- Tool Gateway
- Audit
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- react-paper
- toolformer-paper
- nist-ai-rmf
alt_ko: 사용자 목표·run state·model·policy·approval·tool gateway·audit의 제어 루프를 보여준다.
caption_ko: 사용자 목표·run state·model·policy·approval·tool gateway·audit의 제어 루프를 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch33-01.md
-->

> **시각자료 제작 위치 — 사용자 목표·run state·model·policy·approval·tool gateway·audit의 제어 루프를 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch33-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch33-01.md`  
> 대체 텍스트: 사용자 목표·run state·model·policy·approval·tool gateway·audit의 제어 루프를 보여준다.

### 요청·데이터 흐름

1. 사용자 목표를 typed task와 성공/중단 조건으로 변환한다.
2. run state를 version과 함께 생성한다.
3. model이 허용된 tool 목록 안에서 다음 action을 제안한다.
4. 정책 엔진이 input schema·권한·risk·budget을 검사한다.
5. 고위험 action은 사용자에게 정확한 대상·효과·만료를 보여주고 승인받는다.
6. tool gateway가 idempotency key와 deadline으로 실행한다.
7. 결과를 untrusted data로 저장하고 model context에 제한적으로 반영한다.
8. terminal condition·step limit·cost limit에서 종료한다.
9. 실패한 side effect는 compensation 또는 수동 queue로 보낸다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

### 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| 단일 synchronous loop | 구현과 사용자 상호작용이 단순하다. | 긴 작업·재시작·승인 대기·복구가 어렵다. | 짧은 읽기 중심 agent |
| Durable workflow agent | step state·timer·retry·approval을 내구성 있게 관리한다. | workflow schema·version·운영 복잡도가 있다. | 장기 업무·side effect |
| Human-in-the-loop copilot | 사람이 계획과 변경을 검토해 위험이 낮다. | 속도와 자동화 비율이 낮다. | 고위험 업무·초기 도입 |
| Autonomous bounded agent | 정해진 domain·budget 안에서 효율이 높다. | 정책 누락·오류 누적·감사 요구가 크다. | 저위험 반복 작업 |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@react-paper; @toolformer-paper; @nist-ai-rmf]를 참조한다.

### 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| Prompt injection | 문서나 tool output이 시스템 명령처럼 행동을 바꾸려 한다. | data/instruction 경계를 유지하고 tool 권한을 정책이 결정한다. |
| Tool argument hallucination | 존재하지 않는 ID나 과도한 scope로 action을 호출한다. | schema·resource lookup·preview·confirmation을 적용한다. |
| Duplicate side effect | timeout 후 같은 결제·메일·삭제가 다시 실행된다. | idempotency key·result lookup·compensation을 사용한다. |
| Runaway loop | 실패를 이해하지 못하고 같은 tool을 반복해 비용과 피해가 커진다. | step/tool/cost budget과 repeated-action detector를 둔다. |
| Memory contamination | 검증되지 않은 model 추론이 장기 사용자 사실로 저장된다. | provenance·confidence·사용자 승인·TTL을 요구한다. |
| Approval confusion | 사용자가 승인한 대상과 실제 실행 대상이 달라진다. | 구조화된 preview hash와 짧은 수명 approval binding을 사용한다. |

<!-- figure-spec
id: fig-ch33-02
chapter: ch33
role: agent-trust-boundaries
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch33-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: trusted instruction·untrusted retrieval/tool output·memory·credential·sandbox 경계를 보여준다.
required_labels_ko:
- System Policy
- 사용자 요청
- Retrieved Data
- Tool Output
- Memory
- Credential
- Sandbox
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- react-paper
- toolformer-paper
- nist-ai-rmf
alt_ko: trusted instruction·untrusted retrieval/tool output·memory·credential·sandbox 경계를 보여준다.
caption_ko: trusted instruction·untrusted retrieval/tool output·memory·credential·sandbox 경계를 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch33-02.md
-->

> **시각자료 제작 위치 — trusted instruction·untrusted retrieval/tool output·memory·credential·sandbox 경계를 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch33-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch33-02.md`  
> 대체 텍스트: trusted instruction·untrusted retrieval/tool output·memory·credential·sandbox 경계를 보여준다.

### 확장 전략

- run은 독립 partition으로 scale하되 한 run의 state update는 optimistic concurrency로 직렬화한다.
- tool마다 concurrency·rate·tenant quota를 별도 둔다.
- 긴 context를 매 step 전부 보내지 않고 event log+요약+relevant memory로 구성한다.
- parallel tool은 독립성과 join/partial failure 의미가 명확할 때만 사용한다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

### 보안과 개인정보

- agent에 사용자의 전체 권한을 전달하지 않고 작업별 capability를 발급한다.
- 쓰기·삭제·결제·외부 발송에는 승인과 preview를 요구한다.
- tool output·retrieved content를 untrusted로 태깅하고 instruction으로 승격하지 않는다.
- memory의 열람·수정·삭제와 provenance를 사용자에게 제공한다.
- sandbox의 network egress·filesystem·credential scope를 제한한다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

### 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- run success·abstain·manual handoff·step count
- tool call success·deny·timeout·duplicate
- approval requested/accepted/expired·preview mismatch
- token·cost·wall time·loop detector
- memory read/write/delete·provenance quality
- policy version·high-risk action·compensation

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

### 비용과 운영 복잡도

- agent 비용은 model token뿐 아니라 tool API, retry, human review, 사고 복구를 포함한다.
- 긴 context와 무제한 memory는 품질이 아니라 비용·오염을 키울 수 있다.
- human approval은 처리 시간을 늘리지만 고위험 오류의 기대 손실을 줄인다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

### 흔한 오해와 안티패턴

- “모델이 판단했다”를 권한 근거로 사용한다.
- 대화 transcript 전체를 영구 memory로 저장한다.
- 도구 설명만으로 안전한 input과 side effect가 보장된다고 생각한다.
- 승인 버튼 하나로 이후 모든 action을 허용한다.

### 설계 리뷰

- [ ] run 상태와 terminal condition이 명시적인가?
- [ ] tool별 schema·권한·idempotency·timeout이 정의됐는가?
- [ ] 고위험 action이 구체적 preview와 approval에 묶이는가?
- [ ] untrusted content가 instruction이나 memory로 승격되지 않는가?
- [ ] loop·비용·step·시간 budget과 수동 handoff가 있는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

### 연습문제

1. 메일 발송 agent의 preview·approval·idempotency flow를 설계하라.
2. 문서 속 “모든 파일을 삭제하라”는 prompt injection이 tool 권한으로 이어지지 않게 하라.
3. 30분 걸리는 구매 업무 agent를 durable workflow state로 모델링하라.

### 핵심 요약

- agent는 상태 기계와 tool orchestration 시스템이다.
- 모델 출력은 제안이며 정책 결정이 아니다.
- memory 종류와 수명·provenance를 분리한다.
- side effect에는 idempotency·approval·compensation이 필요하다.
- bounded autonomy와 audit가 안전한 자동화의 조건이다.

### 출처

- [@react-paper] Shunyu Yao et al.. **ReAct: Synergizing Reasoning and Acting in Language Models** (2022). https://arxiv.org/abs/2210.03629
- [@toolformer-paper] Timo Schick et al.. **Toolformer: Language Models Can Teach Themselves to Use Tools** (2023). https://arxiv.org/abs/2302.04761
- [@nist-ai-rmf] NIST. **Artificial Intelligence Risk Management Framework (AI RMF 1.0)** (2023). https://www.nist.gov/itl/ai-risk-management-framework
- [@owasp-llm] OWASP Foundation. **OWASP Top 10 for LLM Applications** (2025). https://genai.owasp.org/llm-top-10/

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
