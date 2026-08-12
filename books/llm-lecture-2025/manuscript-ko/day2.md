# Day 2

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실 — CC BY-NC-ND 4.0

본 한국어 역문은 교육 목적의 번역이며, 원본 라이선스(CC BY-NC-ND 4.0)를 따릅니다. 파생 저작물(역문)의 생성은 원저작자의 표기와 동일한 라이선스 조건 아래에서만 허용됩니다. 원문의 의미를 변경하거나 추가하지 않았습니다.

---

## 주의사항: 본 자료의 재이용(2차 이용)에 대하여

### 본 자료에 대하여
- 본 자료는 도쿄대학교 마츠오·이와사와 연구실이 작성한 것으로, 2025년 10월부터 11월에 걸쳐 개최된 LLM 대규모 언어 모델 강좌 기초편의 강의 자료입니다.
- 크리에이티브 커먼즈 CC BY-NC-SA 4.0 DEED(저작자표시–비영리–동일조건변경허락 4.0 국제) 라이선스로 등록되어 있습니다.

### 라이선스 표기에 대하여
- 각 슬라이드의 페이지 하단에 라이선스가 명시되어 있습니다. 재이용 시에는 반드시 본 라이선스 표기를 기재해 주세요.
- 재이용 시 복제가 어려운 경우, 아래의 텍스트 박스를 이용하여 하이퍼링크를 포함해 라이선스를 표기해 주세요.
- 재이용하는 페이지에 참고 논문 등의 인용이 있는 경우, 권막의 References에서 해당 인용 위치를 게재해 주세요.

### 비영리 목적 이용
- 재이용(2차 이용)이 허락됩니다.

### 영리 목적 재이용
- 별도 문의 바랍니다.

### 기타
- 원문의 표현이 바뀌지 않는 범위(글꼴, 크기 등)에서는 개변이 가능합니다.
- 그 외의 개변이나 기타 라이선스에 관한 자세한 내용은 해당 페이지를 참고하여 적절히 취급해 주세요.

도쿄대학교 마츠오·이와사와 연구실

---

## 추론 (Prompting, In-context Learning)

원다 켄노우(原田憲旺)

※ 허가 없는 촬영 및 제3자에 대한 공개를 금지합니다.

대규모 언어 모델 강좌 2025

---

## 강사 소개 — 원다 켄노우(原田憲旺) @KH_ls_ippon

- 마츠오·이와사와 연구실 박사과정 3년 차
- LLM 강좌 개설 시 강좌 자료 제작·콘테스트 제작 담당
- GENIAC에서 평가 담당
- AI 백서 2025 생성AI 에디션 집필 협력
- DeepLearning.ai의 생성AI 강의 번역
- 기시다 총리·이시바 총리 생성AI 강의 TA·강사

### 연구 테마
- 대규모 언어 모델의 평가, 대규모 언어 모델에 의한 평가
- 대규모 언어 모델의 지시 추종 능력에 관한 연구
- Web Agent를 활용한 UI/UX 평가
- 교육 현장에서의 대규모 언어 모델 응용

### 담당 강좌
- 기초편 제2회 강의·연습

(자연어처리학회 2024 발표 모습)

---

## ChatGPT 이용 확대 (주당 7억 명 이용, 180억 메시지)

- 업무 용도는 27%, 이용자의 약 절반이 26세 이하, 남녀 비율은 1:1
- 전체 이용 용도의 80%는 Practical Guidance, Seeking Information, Writing

[1] Chatterji et al., 2025, How People Use ChatGPT

---

## 강사의 LLM 사용 예

- 연구자 대담이나 인터뷰 팟캐스트의 번역·요약(Writing)
  - 1시간짜리 팟캐스트라도 Gemini에서 원하는 부분만 물어볼 수 있다
  - 음성·동영상도 대응하는 멀티모달
- 연구 분야의 첫 서베이(Information Seeking)
  - 수십 건의 논문을 조사하는 Deep Research(Gemini, ChatGPT)
  - 같은 질문을 여러 서비스에 던지면서 캐치업
- 해외 강의 자료의 설명 보충(Writing)
  - 슬라이드 자료만 공개된 경우에도 추가 검색이나 문맥 추가로 내용을 따라갈 수 있다
- 요점 개조식 → 글(Writing)
- 코딩 보조 및 데이터 정형(Writing/Practical Guidance)
  - 자작 워크플로: https://github.com/kenoharada/labudy

---

## 모델에 대한 지시 방법과 모델의 응답 선택 방법을 공략하여 모델을 활용한다

(예시: LLM에게 "Generative AI"를 일본어로 번역하게 하거나, 5세 아이도 이해할 수 있도록 설명하게 하는 프롬프트)

---

## 목차

- Decoding의 기초(greedy decoding, top-p sampling)
- Prompting의 기초(Few-shot, CoT)
- Meta-generation(Best-of-N, Self-refine, LLM-as-a-Judge)
- 발전적인 프롬프트 예
- LLM을 활용한 서비스 사례
- 모델의 선택

---

## Decoding(디코딩)의 기초

Decode는 복호·해독을 의미한다.

- Decoding algorithms: Token-level generation algorithms (Welleck et al., 2024)
- Decoding as a choice of Algorithm + Scoring Function (Amini et al., 2023)

즉, 모델의 출력에서 "원하는" 출력을 얻기 위한 다양한 기법을 가리킨다.

---

## 언어 모델(Language Model)이란

- 어떤 단어 열(≒ 문장)이 얼마나 발생하기 쉬운지를 모델화한 것이다.
- 단어 열 (x₁, x₂, …, x_L)에 그 생성 확률 p(x₁, x₂, …, x_L)을 할당하는 확률 모델 p를 말한다.

예시:
- p(일본, 의, 수도, 는, 도쿄) = 0.02
- p(일본, 의, 수도, 는, 파리) = 0.00001
- p(도쿄, 의, 수도, 는, 일본) = 0.0005

"좋은" 언어 모델에 대한 기대: 문법적·상식적 관점에서 오류가 있는 문장에는 낮은 확률을 할당한다.

---

## 자기회귀 언어 모델(Autoregressive Language Models)

- p(x₁, x₂, …, x_L)을 조건부 분포의 곱으로 표현한다.

p(x₁, x₂, …, x_L) = p(x₁) · p(x₂|x₁) · … · p(x_L | x₁, x₂, …, x_{L−1})

예: p(일본, 의, 수도) = p(일본) · p(의|일본) · p(수도|일본, 의)

- 이와 같이 확률의 연쇄법칙으로 분해한 모델을 특히 자기회귀 언어 모델(autoregressive language model)이라 부른다.
- 조건부 확률을 알면 생성하는 것도 가능하다.

예:
- p(도쿄 | 일본, 의, 수도, 는) = 0.2
- p(파리 | 일본, 의, 수도, 는) = 0.001
- p(카이로 | 일본, 의, 수도, 는) = 0.0005

→ "일본의 수도는" 다음에는 "도쿄"가 생성된다.

---

## 언어 모델의 활용: 조건부 확률에 기반해 과제를 푼다

| 과제 | 모델에 대한 입력 | 모델의 출력 |
|------|------------------|-------------|
| 번역 | 영어 문장 | 일본어 문장 |
| 질의응답 | 질문 | 답변 |
| 요약 | 문서 | 짧은 서술 |

p(x_{i+1:L} | x₁, x₂, …, x_i) = ∏_{j=i+1}^{L} p(x_j | x_{1:i}, x_{i+1:j−1})

어떻게 모델에서 출력을 얻을 것인가? → Decoding

---

## 언어 모델을 사용할 때의 설정

---

## Decoding: 언어 모델의 출력에서 "원하는" 출력을 얻기 위한 다양한 기법

- Greedy decoding: 매 스텝마다 가장 확률이 높은 것을 선택
- Beam search: 여러 후보를 남겨두고, 여러 스텝 단위로 점수가 높은 것을 선택
- Ancestral sampling: 전체 후보에서 확률에 기반해 샘플링
- Top-k sampling: 상위 k개에서 샘플링
- Top-p sampling (nucleus sampling): 상위부터 누적하여 p×100%가 되는 후보 안에서 샘플링

---

## Greedy decoding

- 매 스텝마다 가장 확률이 높은 것을 선택
- 문장 전체로서 반드시 확률이 가장 높아지는 것은 아니다
- 반복이 자주 관찰된다

[2] How to generate text: using different decoding methods for language generation with Transformers, https://huggingface.co/blog/how-to-generate

---

## Beam search

- 여러 후보를 남겨두고, 여러 스텝 단위로 점수가 높은 것을 선택
- 지정한 빔 수(num_beams)만큼의 후보를 남겨 다음 깊이를 탐색
- 계산량이 많다
- 출력이 지루하다 (무난하고 평이함)
- 출력이 짧아진다

[2] How to generate text: using different decoding methods for language generation with Transformers, https://huggingface.co/blog/how-to-generate

---

## Top-k sampling

- Top-k: 상위 k개에서 샘플링
- Long-tail 문제, 유망한 선택지가 배제될 수 있음

[2] How to generate text: using different decoding methods for language generation with Transformers, https://huggingface.co/blog/how-to-generate

---

## Top-p sampling / nucleus sampling (Holtzman et al., 2020)

- Top-p: 상위부터 누적하여 p×100%가 되는 후보 안에서 샘플링
- Top-k보다 유연성이 있다

[2] How to generate text: using different decoding methods for language generation with Transformers, https://huggingface.co/blog/how-to-generate

---

## 샘플링을 좌우하는 Temperature

- 분포의 뾰족함을 조정하는 파라미터로, 아래 식의 T에 해당하는 값이다.
- T 값을 0에 가깝게 할수록 분포가 뾰족해지고, 크게 할수록 무작위성이 높아진다.

softmax 식: p(w) = exp(z_w / T) / Σ_{j=1}^{|V|} exp(z_j / T)

[3] Cohere (2024), "Parameters for Controlling Outputs", Cohere LLMU, https://cohere.com/llmu/parameters-for-controlling-outputs

---

## 보충: temperature를 0으로 해도 결정적이지 않은 경우가 있다

- 부동소수점 연산은 순서에 따라 결과가 달라질 수 있다
- 동시에 여러 요청을 처리하는 경우(배치 처리)에 처리 분할 방식이 달라진다
  - → 연산 순서가 달라진다 → 결정적이지 않다
- GPU 처리를 수정하면 결정적으로 만들 수 있다

[4] Thinking Machines (2024), "Defeating Nondeterminism in LLM Inference", https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/

---

## 어떤 Decoding 기법을 사용하면 좋을까?

- 과제의 성질에 기반한 검토 → 다양성이 필요한가?
  - 이야기 생성·아이디어 발산 → 샘플링 기반 기법
  - 지식 질의·번역 → Greedy decoding, Beam Search
- Greedy decoding의 생성 결과와, temperature·Top-p를 바꿔 여러 번 생성해 비교해 본다

참고 문헌:
- A Thorough Examination of Decoding Methods in the Era of LLMs
- The Curious Case of Neural Text Degeneration
- Is GPT-3 Text Indistinguishable from Human Text? Scarecrow: A Framework for Scrutinizing Machine Text
- Trading Off Diversity and Quality in Natural Language Generation
- It's MBR All the Way Down: Modern Generation Techniques Through the Lens of Minimum Bayes Risk

- 계열의 평가: 확률이 높은 것이 정말로 원하는 출력인가?
  - → Reward model / LLMs-as-Judge를 활용한 Best-of-N (후술)

---

## Decoding 기초 정리

- 조건부 확률로 다음 단어의 후보가 결정된다
- 모델은 과거 문맥을 바탕으로 다음 단어의 그럴듯함(plausibility)을 출력
  - 과거 문맥을 반영하기 위한 기법, 언어 모델 학습의 기법 → 제3회 강의
- 후보에서 어떻게 다음 단어를 선택할지
  - Greedy decoding, Top-p sampling 등의 Decoding 기법
  - 과제에 따라 적합한 기법이 다르다
- 모델에 대한 입력(과거 문맥)을 공략하여 모델에게 과제를 풀게 한다
  - → 프롬프팅(Prompting)

---

## 기타 참고 자료

- Generating Text from Language Models, https://rycolab.io/classes/acl-2023-tutorial/
- Stanford CS324 Introduction, https://stanford-cs324.github.io/winter2022/lectures/introduction/
- CMU Advanced NLP Inference I Decoding and Generation Algorithms, https://cmu-l3.github.io/anlp-spring2025/static_files/anlp-s2025-07-decoding.pdf
- From Decoding to Meta-Generation: Inference-time Algorithms for Large Language Models, https://arxiv.org/abs/2406.16838
- Generation strategies, https://huggingface.co/docs/transformers/v4.56.0/en/generation_strategies

---

## Prompting(프롬프팅)의 기초

- 커맨드 프롬프트(command prompt): 인간의 입력을 촉구하는 표시 (예: `C:\>`, `~$`)
- 근년의 prompt: AI의 출력을 촉구하는 문자열 (예: "질문: 일본의 수도는?", "답변:")

---

## GPT-3의 등장 (Brown et al., 2020)

> "Here we show that scaling up language models greatly improves task-agnostic, few-shot performance, sometimes even reaching competitiveness with prior state-of-the-art finetuning approaches. Specifically, we train GPT-3, an autoregressive language model with 175 billion parameters, 10x more than any previous non-sparse language model, and test its performance in the few-shot setting. For all tasks, GPT-3 is applied without any gradient updates or fine-tuning, with tasks and few-shot demonstrations specified purely via text interaction with the model."

(요지: 언어 모델의 규모를 키우면 과제에 무관한 few-shot 성능이 크게 향상되며, 종래의 최고 수준 파인튜닝 접근과 맞먹는 수준에 이르기도 한다. 1,750억 매개변수의 자기회귀 언어 모델 GPT-3를 학습시키고, few-shot 설정에서 성능을 시험했다. 모든 과제에서 기울기 갱신이나 파인튜닝 없이, 과제와 few-shot 시연을 순전히 텍스트 상호작용으로만 지정해 적용했다.)

- 기존: 과제 전용 모델을 대량의 데이터로 가중치를 갱신하며 학습
- GPT-3: 가중치의 재학습 없이, 과제 정보와 몇 가지 예를 담은 prompt를 바꾸는 것만으로 다양한 과제에서 고성능 달성

[5] Brown et al., 2020, Language Models are Few-Shot Learners

---

## Before prompt (Before GPT-3) — 시대의 변천

- (NN 이외) 과제마다 모델을 학습
- (NN) 과제마다 모델을 학습
- (fine-tuning) 모델을 공유하여 학습
- (Prompting) 모델을 고정하고 지시만 변경

종래 → 현대

[6] Liu et al., 2021, Pre-train, Prompt, and Predict: A Systematic Survey of Prompting Methods in Natural Language Processing

---

## GPT-2에서의 전조 (Radford et al., 2019)

- 질문 뒤에 "A: "를 넣으면 어느 정도 답할 수 있었다
- 요약 과제에서 "TL;DR:"을 넣으면 요약을 생성했다
  - "Too Long, Didn't Read"(TL;DR)은 요약을 가리키는 슬랭
- "english sentence = french sentence, english sentence =" 형태로 번역이 가능했다

[7] Radford et al., 2019, Language Models are Unsupervised Multitask Learners

---

## In-context learning(ICL, 문맥 내 학습)으로 가중치 갱신 없이 고성능

- 가중치를 고정한 언어 모델이 프롬프트에 의한 조건 부여를 통해 과제를 수행하는 것
- 하나의 모델이 가중치 매개변수의 재학습 없이, 프롬프트 문의 변경만으로 다양한 과제를 고성능으로 수행할 수 있다는 점이 당시의 충격이었다

[5] Brown et al., 2020, Language Models are Few-Shot Learners

---

## 프롬프팅(prompting)이란?

- 특정 기능의 발생을 촉진(prompt)하도록 언어 모델에 입력하는 컨텍스트 문(맥락 문)
- Zero-shot: 과제의 설명문·지시문만
- Few-shot: 풀게 할 과제의 시연(demonstration) 예를 몇 개 준비
  - 예가 하나뿐인 경우는 one-shot
- ※ LLM 이전의 Few-shot learning과는 의미가 다르다는 점에 주의

[5] Brown et al., 2020, Language Models are Few-Shot Learners

---

## 시연 예시 수를 늘리면 성능이 향상한다

- 특히 모델이 대규모인 경우, Few-shot 시연의 추가로 성능이 크게 오르는 일이 많다

[5] Brown et al., 2020, Language Models are Few-Shot Learners

---

## 시연 예시 수를 늘리면 성능이 향상한다 (계속)

- 100만 토큰의 입력을 받아들이는 long context 모델의 활용
  - GPT-3는 2048 토큰만 받아들였다
- 컨텍스트 길이가 늘면 계산량이 증가하며, 더 한층의 성능 향상을 노리고 싶다
  - → 파인튜닝, 모델이 크므로 효율적으로 → 제6회 강의

[8] Agarwal et al., 2024, Many-Shot In-Context Learning

---

## 보다 어려운 과제를 모델에게 풀게 하기 위해

- 답에 이르기까지 여러 단계의 처리가 필요한, 다단계 추론이 요구되는 과제

[9] Wei et al., 2022, Chain-of-Thought Prompting Elicits Reasoning in Large Language Models

---

## Chain-of-Thought Prompting (Few-shot CoT)

- 답에 이르기까지 여러 단계의 처리가 필요한, 다단계 추론 과제
- 답에 이르기까지의 사고의 연쇄(Chain-of-Thought)를 예시로 제공

[9] Wei et al., 2022, Chain-of-Thought Prompting Elicits Reasoning in Large Language Models

---

## Chain-of-Thought Prompting (Few-shot CoT) — 효과

- 다양한 수학 데이터셋에서 검증한 결과
- 특히 모델 크기가 클 때 성능 개선이 크다

[9] Wei et al., 2022, Chain-of-Thought Prompting Elicits Reasoning in Large Language Models

---

## "Let's think step by step" (Zero-shot CoT)

- Chain-of-Thought의 예를 주지 않고, 모델 스스로 생각하게 한다
- "파이프라인 등을 인간이 설계하지 않고, 모델 스스로 생각시키는 편이 낫지 않을까?"
  - → "Let's think step by step"라는 구절이 떠올랐다 (by 코지마 씨)

[10] Kojima et al., 2022, Large Language Models are Zero-Shot Reasoners

---

## "Let's think step by step" (Zero-shot CoT)의 추론 능력

- 단일 스텝 추론으로 풀리는 과제 (CoT가 불필요)
  - 상식 추론 (생각이 지나쳐 실패하는 사례가 많음)
  - ※ 특히 가능한 해를 여럿 선택해 버리는 경우가 있음
- 다단계 추론이 필요한 과제
  - 2022년 논문에서 만들어진 과제 (사용한 모델은 2021년까지의 데이터로 학습)

[10] Kojima et al., 2022, Large Language Models are Zero-Shot Reasoners

---

## CoT(사고의 연쇄) / Intermediate token(중간 토큰)의 효과

- CoT·중간 토큰에 의해 표현력이 향상한다
  - → 순차적 처리를 필요로 하는 과제의 성능이 향상한다

[11] Li et al., 2024, Chain of Thought Empowers Transformers to Solve Inherently Serial Problems

---

## 프롬프트 차이에 따른 성능 차이

(같은 과제라도 프롬프트에 따라 정확도가 낮거나 높거나 한다)

[12] Gonen et al., 2023, Demystifying Prompts in Language Models via Perplexity Estimation
[13] Sclar et al., 2024, Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design or: How I learned to start worrying about prompt formatting

---

## 프롬프트 차이에 따른 성능 차이 (계속)

- 수동으로 설정

[10] Kojima et al., 2022, Large Language Models are Zero-Shot Reasoners

---

## Prompt engineering(프롬프트 엔지니어링)

원하는 출력을 얻도록 프롬프트를 시행착오한다.

- 수동 시행착오
  - Few-shot prompting, CoT prompting
  - LLM 개발사의 가이드라인 참고 (예: https://platform.openai.com/docs/guides/prompt-engineering)
- 자동 조정
  - 특수한 토큰을 학습: Prefix tuning / Prompt tuning (파인튜닝 강의 회차)
  - 프롬프트 문 자체를 수정

---

## Automatic Prompt Engineer

- 입출력 쌍을 사용해, 지시문을 LLM 스스로 여러 개 예측하게 한다
- 지시문 후보를 이용해 과제 성능 또는 답의 우도를 측정하고, 점수가 높은 것을 선택
- 지시문에 변형을 주기 위해 LLM에게 지시문의 서술을 바꾸게 한다

[14] Zhou et al., 2023, Large Language Models Are Human-Level Prompt Engineers

---

## Demonstrate-Search-Predict

- 질문 분해 방법이나 Follow-up 질문 등의 중간 과정을 LLM의 시행착오로 생성
- 중간 과정이 옳은지는, 그 과정을 거쳐 얻은 LLM의 출력과 시연 예의 출력이 일치하는지를 기준으로 판단

[15] Khattab et al., 2022, Demonstrate-Search-Predict: Combining Retrieval and Language Models for Knowledge-Intensive NLP Tasks

---

## Optimization by PROmpting (OPRO)

- 과거 프롬프트와 그 점수 변천과 함께, 점수가 더 높아지도록 프롬프트를 LLM에게 생성시킨다
- 한 번의 생성으로 8개 정도의 후보를 만들고, 점수가 좋은 것을 선택

[16] Yang et al., 2024, Large Language Models as Optimizers

---

## Genetic-Pareto (GEPA)

- 과제를 실제로 수행해 성공·실패의 궤적 데이터로부터 언어 피드백을 작성해 프롬프트를 개선하거나, 다른 유망한 프롬프트 후보와 결합한다
- 개선할 프롬프트를 고를 때, 다양성 확보를 위해 단 한 문제에서만 가장 좋은 점수를 낸 프롬프트도 후보에 넣는다

[17] Agrawal et al., 2025, GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning

---

## Genetic-Pareto (GEPA) — 개념도

[17] Agrawal et al., 2025, GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning

---

## 프롬프팅 기초 정리

- 모델에 대한 입력문을, 특정 기능의 발생을 촉진(prompt)하도록 공략함으로써 다양한 과제에서 가중치 재학습 없이 고성능을 달성
- 시연 예를 포함하는 Few-shot prompting, 순차적 처리·사고 과정을 촉진하는 Chain-of-Thought prompting이 유효
- 표현이나 포맷의 차이로 성능이 크게 달라지므로, prompt engineering이라 불리는 시행착오가 필요

---

## 발전: Meta-generation algorithms (Welleck et al., 2024)

모델을 여러 번 추론시킨 뒤에 출력을 얻는 기법군.

[18] Welleck et al., 2024, From Decoding to Meta-Generation: Inference-time Algorithms for Large Language Models

---

## Self-Consistency, Majority Voting(다수결)

Top-k, Top-p 샘플링으로 여러 답을 얻고 → 가장 많이 나온 답을 채택

[19] Wang et al., 2023, Self-Consistency Improves Chain of Thought Reasoning in Language Models

---

## Best-of-N

여러 답을 얻은 뒤 점수화하여, 가장 높은 점수의 것을 선택

[20] Snell et al., 2024, Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters

---

## 어떻게 점수를 매길 것인가?

- 전용 분류기를 학습
  - Reward model, Process Reward Model (자세히는 제7회 강화학습)
- LLM이 점수를 내도록 프롬프팅
  - LLM-as-a-Judge (Zheng et al., 2023)
  - 세부 평가 관점을 프롬프트에 넣는다 (Cook et al., 2024)

---

## LLM-as-a-Judge: 프롬프팅으로 LLM에게 문장을 평가시킨다

- 긴 글을 높게 평가하려는 경향(편향)은 있으나
- 인간의 평가와 어느 정도 일치한다

[21] Zheng et al., 2023, Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena

---

## SELF-REFINE

- 답 생성 → 답에 대한 피드백 → 답 수정의 루프를 반복
- 생성·피드백·수정은 같은 모델로, 프롬프팅만 바꾼다

[22] Madaan et al., 2023, Self-Refine: Iterative Refinement with Self-Feedback

---

## 발전적인 프롬프트 예: Claude에서 실제로 사용되는 프롬프트

2,500단어에 이르는, 속성 정보(검색해서 사용하는 이름·제품 정보), 특정 장르에 대한 응답 태도 지정, 포맷 지정, knowledge cut-off 정보, 미국 대통령 선거 결과 정보 등을 포함

[23] Anthropic Release notes, System prompts

---

## 발전적인 프롬프트 예: 적대적 프롬프트(Adversarial Prompt)

- 프롬프트 공략에 의한 공격
- 예: 탈옥(jailbreak)
  - (페르소나를 부여하면 본래 답하지 않을 것도 답하게 된다. "Do Anything Now".)
- 더하면 공격성이 높아지는 토큰이 존재한다는 점도 알려져 있다

[24] Adversarial Prompting in LLMs

---

## 발전적인 프롬프트 예: 생성AI를 사용하는 사용자에 대한 대응

- 강의 자료와는 전혀 다른 취지의 보고서를 작성하도록 투명 색 글자(숨은 지시)를 심는 사례
- 논문 심사 결과가 긍정적으로 나오도록 유도하는 사례

[25] 시마다 타쿠(2025), "AI에 과제를 쓰게 하면 자료에 없는 내용을 출력 — 게이오대의 AI 대책이 화제, 의도를 들었다", ITmedia AI+, 2025/05/01 공개, https://www.itmedia.co.jp/aiplus/articles/2504/30/news214.html
[26] 니혼게이자이신문(2025), "논문 내에 비밀 명령문, AI에게 '높게 평가하라' 일한미 등 주요 14개 대학에서", 니혼게이자이신문, 2025/06/29 공개, https://www.nikkei.com/article/DGXZQOUC13BCW0T10C25A6000000/

---

## 발전적인 프롬프트 예: DeepResearch를 프롬프팅으로 구현

검색 쿼리 작성·검색 충분성 점검(회고)·답 생성을 프롬프팅으로 구성

[27] Gemini Fullstack LangGraph Quickstart

---

## 발전적인 프롬프트 예: 논문에서 포스터 생성

그림 잘라내기 처리·파워포인트를 다루는 라이브러리와의 적절한 조합

(검색 엔진이나 코드 이용에 관해서는 응용편 제2회)

[28] Pang et al., 2025, Paper2Poster: Towards Multimodal Poster Automation from Scientific Papers

---

## 발전적인 프롬프트 예: 합성 데이터(Synthetic data)

LLM 학습에 사용하는 데이터를 인공적으로(특히 LLM을 사용해) 만드는 것.

- 제어 가능한(controllable) 실험을 위해: TinyStories, Physics of LM
- 보다 복잡한 데이터셋을 만들기 위해: WizardLM, Alpaca
- 크고 우수한 모델의 능력을 작은 모델로: s1K, NaturalThoughts
- 고품질 사전학습 데이터: Textbooks Are All You Need

[29] Taori et al., 2023, Alpaca: A Strong, Replicable Instruction-Following Model

---

## 발전적인 프롬프트 예: 시뮬레이션(Simulation)

LLM에게 특정 인격·특성을 부여해 인간을 모의(simulate)한다

[30] Park et al., 2024, Generative Agent Simulations of 1,000 People

---

## 기타 참고 자료 (GPT-2, GPT-3 개발 뒷이야기)

- Ilya Sutskever - GPT-2, https://www.youtube.com/watch?v=T0I88NhR_9M
- L11 Language Models — guest instructor: Alec Radford (OpenAI) — Deep Unsupervised Learning SP20, https://www.youtube.com/watch?v=BnpB3GrpsfM
- An Observation on Generalization, https://www.youtube.com/watch?v=AKMuA_TVz3A

---

## 기타 참고 자료 (Prompting)

- Stanford CS224U In-context learning, https://web.stanford.edu/class/cs224u/slides/cs224u-incontextlearning-2023-handout.pdf
- Weng, Lilian. (Mar 2023). Prompt Engineering. Lil'Log. https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/.
- Prompt Engineering Guide, https://www.promptingguide.ai/
- Stanford CS224N Lecture 11: Efficient Adaptation, https://web.stanford.edu/class/cs224n/slides_w25/cs224n-2025-lecture11-adapatation.pdf
- CMU CS11-711 Advanced NLP Prompting and In-Context Learning, https://cmu-l3.github.io/anlp-spring2025/static_files/anlp-s2025-08-prompting.pdf

---

## 기타 참고 자료 (문맥 내 학습의 수수께끼·메커니즘)

- 대규모 언어 모델 응용 제5회 LLM의 분석·해석 가능성
- In-context Learning and Induction Heads, https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html
- Dai et al., 2023, Why Can GPT Learn In-Context? Language Models Secretly Perform Gradient Descent as Meta-Optimizers
- Min et al., 2022, Rethinking the Role of Demonstrations: What Makes In-Context Learning Work?
- Razeghi et al., 2022, Impact of Pretraining Term Frequencies on Few-Shot Numerical Reasoning
- Wei et al., 2023, Larger language models do in-context learning differently

---

## 기타 참고 자료 (Chain-of-Thought)

- Stanford CS 25 LLM Reasoning, https://dennyzhou.github.io/LLM-Reasoning-Stanford-CS-25.pdf
- Wang et al., 2024, Chain-of-Thought Reasoning Without Prompting
- Yao et al., 2023, Tree of Thoughts: Deliberate Problem Solving with Large Language Models

---

## 기타 참고 자료 (Meta-generation)

- Beyond Decoding: Meta-Generation Algorithms for Large Language Models, https://cmu-l3.github.io/neurips2024-inference-tutorial/
- CMU Advanced NLP Advanced Inference Strategies, https://cmu-l3.github.io/anlp-spring2025/static_files/anlp-s2025-21-inference.pdf
- Brown et al., 2024, Large Language Monkeys: Scaling Inference Compute with Repeated Sampling
- Wu et al., 2024, Inference Scaling Laws: An Empirical Analysis of Compute-Optimal Inference for Problem-Solving with Language Models
- Gu et al., 2024, A Survey on LLM-as-a-Judge
- Kamoi et al., 2024, When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs
- 2024 Fall 대규모 언어 모델(LLM) 강좌 특별회: LLM의 자기 수정 — OpenAI o1 관련 연구

---

## 기타 참고 자료 (발전적인 프롬프트)

- Grok prompts, https://github.com/xai-org/grok-prompts
- Zou et al., 2023, Universal and Transferable Adversarial Attacks on Aligned Language Models
- How we built our multi-agent research system, https://www.anthropic.com/engineering/multi-agent-research-system
- OpenAI Codex CLI, https://github.com/openai/codex/blob/main/codex-rs/core/prompt.md

---

## LLM을 활용한 서비스 사례

---

## 코딩 지원 서비스(코드도 언어)

GitHub Copilot, Claude Code, Cursor, Cline, Windsurf, Devin 등

- Cursor는 2023년 릴리스, 2025년 6월 기준 500 million USD ARR, 900 million USD 조달

[31] Cursor at $100M ARR, https://sacra.com/research/cursor-at-100m-arr/
[32] Anysphere (2026), "Cursor - The AI-first Code Editor", Cursor, https://cursor.com/ja

---

## Y Combinator(미국의 유명 VC) 투자처로 보는 AI 서비스

- AI를 활용해 개발 속도를 높이고, AI 활용으로 새로운 가치를 창출

[33] Startup Directory, https://www.ycombinator.com/companies
[34] 10 People + AI = Billion Dollar Company?, https://www.youtube.com/watch?v=CKvo_kQbakU

---

## LLM을 다루기 위한 "context engineering"

> "다음 단계·처리를 위해, 컨텍스트 윈도우(LLM이 한 번에 읽어들일 수 있는 정보)를 최적의 정보로 채우는, 정밀한 예술이자 과학"

- 기본적인 프롬프팅 기술 (이번 회)
- RAG·Tool-use (응용편 제2회)
- 상태 관리·멀티모달 (응용편 제7회)

[35] Andrej Karpathy (2025), "X Post (status/1937902205765607626)", X (formerly Twitter), https://x.com/karpathy/status/1937902205765607626
[36] Gemini_Plays_Pokemon, https://www.twitch.tv/gemini_plays_pokemon
[37] Google (2025), "Gemini 2.5: Pushing the Frontier with Advanced Reasoning, Multimodality, Long Context, and Next Generation Agentic Capabilities", Google Keyword Blog, https://blog.google/technology/ai/google-gemini-next-generation-december-2025/

---

## LLM 활용을 코딩하면서 배울 수 있는 강의를 번역했습니다

일본어 번역이 완료된 코스:
- ChatGPT Prompt Engineering for Developers
- Building Systems with the ChatGPT API
- How Diffusion Models Work
- LangChain for LLM Application Development
- LangChain Chat with Your Data

자세한 내용은 https://www.deeplearning.ai/courses/

[38] DeepLearning.AI, "Courses", DeepLearning.AI Official Website, https://www.deeplearning.ai/courses/

---

## 기타 참고 자료

- Andrej Karpathy: Software Is Changing (Again), https://www.youtube.com/watch?v=LCEmiRjPEtQ&list=PLQ-uHSnFig5NPx4adxl97CZb8vU4numwi&index=12
- Andrew Ng: AI is Accelerating Startups, https://www.youtube.com/watch?v=RNJCfif1dPY
- Vibe coding MenuGen, https://karpathy.bearblog.dev/vibe-coding-menugen/

---

## 모델의 선택

---

## 모델의 접근 수단에 따른 차이

### API 전용
- 가중치는 공개되지 않으며, 데이터를 입력한 뒤 출력을 얻는 형태
- 자체 컴퓨터를 마련하지 않고도 이용 가능, 사용량 기반 과금
- GPT(OpenAI), Gemini(Google), Claude(Anthropic) 등

### 공개 모델
- 가중치까지 공개되어 있어 (분석에도 적합)
- 자신의 로컬 컴퓨터에서 실행할 수 있고, 입력 데이터를 외부로 보내지 않아도 된다
- Llama, Mistral, DeepSeek, Qwen, gpt-oss 등

### 비공개 모델
- 일부 연구기관만 이용 가능
- PaLM(Google), Gopher(DeepMind) 등

---

## API를 통한 모델 이용 (GPT 예시)

- 1M 토큰 입력당 $1.25, 1M 토큰 출력당 $10

---

## 공개 모델 이용을 편하게 해주는 라이브러리

- Transformers
  - HuggingFace라는 서비스에 모델·데이터셋이 날마다 업로드된다
  - 모델·데이터셋 판의 GitHub 같은 존재
  - 다양한 모델과 편의 기능을 바로 이용할 수 있다
  - 연습에서도 다룹니다
  - 성가신 버그가 내장되는 일도 있으니, 문제가 생기면 버전을 확인
- vLLM
  - 모델 추론을 고속으로 수행할 수 있다

---

## 공개 모델을 이용할 때의 계산 자원

- 자체 GPU 구매
  - H100(80GB) 1장 약 600만엔 + 전력 소비 + 유지보수 + 환경 설정
  - 양자화(모델을 경량화하는 기법)를 적용한 gpt-oss-120b를 이용 가능
- 클라우드 GPU
  - 이용한 시간에 따라 과금 발생
  - H100 1장을 시간당 $1.49에 이용할 수 있는 경우도
  - 유명 서비스: AWS, GCP, Azure, Lambda, HPC-AI, Hyperbolic
- 모델 호스팅 서비스
  - 모델 이름만 선택하면 이용 가능
  - GPT/Gemini 등을 이용할 때와 마찬가지로, 입출력 계산량 기반으로 과금 발생
  - 유명 서비스: Cerebras, Groq, Together.ai, Fireworks

---

## 모델 호스팅 서비스의 차이

각 사가 독자적인 고속화·경량화 기술을 개발하고 있다

[40] Cerebras Systems (2026), "Cerebras - AI Supercomputing at Unprecedented Speed", https://www.cerebras.ai/
[39] Artificial Analysis (2026), "GPT-OSS-120B Model Providers and Performance Analysis", https://artificialanalysis.ai/models/gpt-oss-120b/providers

---

## 모델 성능의 차이

- lmarena(사용자 투표형), HELM(복수 벤치마크 종합 점수)
- 개별 벤치마크 성능은 Technical Report 참고

[41] LMSYS Org (2026), "Arena AI Leaderboard (formerly LMSYS Chatbot Arena)", Arena AI, https://lmarena.ai/leaderboard/
[42] Stanford CRFM, "Holistic Evaluation of Language Models (HELM)", Center for Research on Foundation Models (CRFM), https://crfm.stanford.edu/helm/capabilities/latest/

---

## 모델 성능의 차이 (일본어)

[43] Nejumi LLM 리더보드 4, https://wandb.ai/llm-leaderboard/nejumi-leaderboard4/reports/Nejumi-LLM-4--VmlldzoxMzc1OTk1MA

---

## 직접 평가할 때의 도구와, 평가 시 주의점

도구:
- simple-evals / evals (OpenAI)
- llm-jp-eval (LLM-jp)
- Lighteval (HuggingFace)

주의: 프롬프트의 차이나 선택지 좁히기 방식의 차이로, 같은 모델에서도 크게 다른 점수가 나올 수 있다. 같은 모델이라도 설정 차이로 성능이 크게 달라진다.

[44] Hugging Face (2024), "What's going on with the Open LLM Leaderboard and MMLU?", Hugging Face Blog, https://huggingface.co/blog/open-llm-leaderboard-mmlu
[45] Artificial Analysis (2026), "GPT-OSS-120B Model Providers and Performance Analysis", https://artificialanalysis.ai/models/gpt-oss-120b/providers

---

## 성능·가격·처리 속도의 트레이드오프

- 우선은 가장 성능이 좋은 모델(가장 비싼 모델)의 사용을 권장
- ChatGPT, Gemini 앱의 무료판이 아닌 유료판
- 혹은 API playground에서 시도

[45] Google DeepMind (2026), "Gemini - Google's Next-Generation AI Models", Google DeepMind, https://deepmind.google/models/gemini/
[39] Artificial Analysis (2026), "GPT-OSS-120B Model Providers and Performance Analysis", https://artificialanalysis.ai/models/gpt-oss-120b/providers

---

## OpenRouter를 사용해 다양한 모델을 빠르게 시도

- 동일한 인터페이스로 여러 모델을 간단히 시도할 수 있다
- 정답은 '오루루키 사우나', 모든 모델이 오답

[46] OpenRouter (2026), "OpenRouter - A unified API for AI models", OpenRouter Official Website, https://openrouter.ai/

---

## 기타 참고 자료

- The Second Half, https://ysymyth.github.io/The-Second-Half/
- Successful language model evals, https://www.jasonwei.net/blog/evals
- How to Build Good Language Modeling Benchmarks, https://ofir.io/How-to-Build-Good-Language-Modeling-Benchmarks/
- Why You Should Stop Using HotpotQA for AI Agents Evaluation in 2025, https://qipeng.me/blog/stop-using-hotpotqa/
- Singh et al., The Leaderboard Illusion, https://arxiv.org/abs/2504.20879
- TinyML and Efficient Deep Learning Computing, https://hanlab.mit.edu/courses/2024-fall-65940
- The Ultra-Scale Playbook: Training LLMs on GPU Clusters, https://huggingface.co/spaces/nanotron/ultrascale-playbook
- How to Scale Your Model, https://jax-ml.github.io/scaling-book/
- Stanford CS336 Lecture 5~7, https://stanford-cs336.github.io/spring2025/
- AI와 반도체 AI 반도체 강좌, https://weblab.t.u-tokyo.ac.jp/lecture/course-list/ai-and-semiconductors/

---

## Reference

[1] Chatterji et al., 2025, How People Use ChatGPT
[2] How to generate text: using different decoding methods for language generation with Transformers, https://huggingface.co/blog/how-to-generate
[3] Cohere (2024), "Parameters for Controlling Outputs", Cohere LLMU, Available at: https://cohere.com/llmu/parameters-for-controlling-outputs ,
[4] Thinking Machines (2024), "Defeating Nondeterminism in LLM Inference", Thinking Machines Blog, Available at: https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/
[5] Brown et al., 2020, Language Models are Few-Shot Learners
[6] Liu et al., 2021, Pre-train, Prompt, and Predict: A Systematic Survey of Prompting Methods in Natural Language Processing
[7] Radford et al., 2019, Language Models are Unsupervised Multitask Learners
[8] Agarwal et al., 2024, Many-Shot In-Context Learning
[9] Wei et al., 2022, Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
[10] Kojima et al., 2022, Large Language Models are Zero-Shot Reasoners
[11] Li et al., 2024, Chain of Thought Empowers Transformers to Solve Inherently Serial Problems
[12] Gonen et al., 2023, Demystifying Prompts in Language Models via Perplexity Estimation
[13] Sclar et al., 2024, Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design or: How I learned to start worrying about prompt formatting
[14] Zhou et al., 2023, Large Language Models Are Human-Level Prompt Engineers
[15] Khattab et al., 2022, Demonstrate-Search-Predict: Combining Retrieval and Language Models for Knowledge-Intensive NLP Tasks
[16] Yang et al., 2024, Large Language Models as Optimizers
[17] Agrawal et al., 2025, GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning
[18] Welleck et al., 2024, From Decoding to Meta-Generation: Inference-time Algorithms for Large Language Models
[19] Wang et al., 2023, Self-Consistency Improves Chain of Thought Reasoning in Language Models
[20] Snell et al., 2024, Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters
[21] Zheng et al., 2023, Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena
[22] Madaan et al., 2023, Self-Refine: Iterative Refinement with Self-Feedback
[23] Anthropic Release notes, System prompts
[24] Adversarial Prompting in LLMs
[25] 시마다 타쿠(2025), "AI에 과제를 쓰게 하면 자료에 없는 내용을 출력 ― 게이오대의 AI 대책이 화제, 의도를 들었다", ITmedia AI+, 2025/05/01 공개, Available at: https://www.itmedia.co.jp/aiplus/articles/2504/30/news214.html
[26] 니혼게이자이신문(2025), "논문 내에 비밀 명령문, AI에게 '높게 평가하라' 일한미 등 주요 14개 대학에서", 니혼게이자이신문, 2025/06/29 공개, Available at: https://www.nikkei.com/article/DGXZQOUC13BCW0T10C25A6000000/
[27] Gemini Fullstack LangGraph Quickstart
[28] Pang et al., 2025, Paper2Poster: Towards Multimodal Poster Automation from Scientific Papers
[29] Taori et al., 2023, Alpaca: A Strong, Replicable Instruction-Following Model
[30] Park et al., 2024, Generative Agent Simulations of 1,000 People
[31] Cursor at $100M ARR, https://sacra.com/research/cursor-at-100m-arr/
[32] Anysphere (2026), "Cursor - The AI-first Code Editor", Cursor, Available at: https://cursor.com/ja
[33] Startup Directory, https://www.ycombinator.com/companies
[34] 10 People + AI = Billion Dollar Company?, https://www.youtube.com/watch?v=CKvo_kQbakU
[35] Andrej Karpathy (2025), "X Post (status/1937902205765607626)", X (formerly Twitter), Available at: https://x.com/karpathy/status/1937902205765607626
[36] Gemini_Plays_Pokemon, https://www.twitch.tv/gemini_plays_pokemon
[37] Google (2025), "Gemini 2.5: Pushing the Frontier with Advanced Reasoning, Multimodality, Long Context, and Next Generation Agentic Capabilities", Google Keyword Blog, Available at: https://blog.google/technology/ai/google-gemini-next-generation-december-2025/
[38] DeepLearning.AI, "Courses", DeepLearning.AI Official Website, Available at: https://www.deeplearning.ai/courses/
[39] Artificial Analysis (2026), "GPT-OSS-120B Model Providers and Performance Analysis", Artificial Analysis, Available at: https://artificialanalysis.ai/models/gpt-oss-120b/providers
[40] Cerebras Systems (2026), "Cerebras - AI Supercomputing at Unprecedented Speed", Cerebras Official Website, Available at: https://www.cerebras.ai/
[41] LMSYS Org (2026), "Arena AI Leaderboard (formerly LMSYS Chatbot Arena)", Arena AI, Available at: https://lmarena.ai/leaderboard/
[42] Stanford CRFM, "Holistic Evaluation of Language Models (HELM)", Center for Research on Foundation Models (CRFM), Available at: https://crfm.stanford.edu/helm/capabilities/latest/
[43] Nejumi LLM 리더보드 4, https://wandb.ai/llm-leaderboard/nejumi-leaderboard4/reports/Nejumi-LLM-4--VmlldzoxMzc1OTk1MA
[44] Hugging Face (2024), "What's going on with the Open LLM Leaderboard and MMLU?", Hugging Face Blog, Available at: https://huggingface.co/blog/open-llm-leaderboard-mmlu
[45] Google DeepMind (2026), "Gemini - Google's Next-Generation AI Models", Google DeepMind, Available at: https://deepmind.google/models/gemini/
[46] OpenRouter (2026), "OpenRouter - A unified API for AI models", OpenRouter Official Website, Available at: https://openrouter.ai/
