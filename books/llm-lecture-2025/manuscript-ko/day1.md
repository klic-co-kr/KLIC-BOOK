# Day 1

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스로 제공됩니다.

> 번역 참고: 본 자료는 CC BY-NC-ND 4.0(저작자표시-비영리-변경금지 4.0 국제) 라이선스를 따르며, 교육 목적의 번역본입니다. 원문의 의미를 변경하지 않고, 반복되는 라이선스 푸터는 첫 회만 표시합니다.

---

## 본 자료에 대하여

본 자료는 도쿄대학교 마츠오·이와사와 연구실이 작성한 것으로, 2025년 10월부터 11월에 걸쳐 개최된 LLM 대규모 언어 모델 강좌 기초편의 강의 자료입니다.

크리에이티브 커먼즈 CC BY-NC-SA 4.0 DEED(저작자표시-비영리-동일조건변경허락 4.0 국제) 라이선스 등록이 되어 있습니다.

### 라이선스 표기에 대하여

각 슬라이드 페이지 하단에 라이선스 기재가 있습니다. 재이용 시에는 본 라이선스 표시를 반드시 기재해 주세요. 재이용 시 복제가 곤란한 경우, 아래 텍스트 박스를 이용하여 하이퍼링크를 포함하여 라이선스 표기를 해 주세요.

재이용하는 페이지에 참고 논문 등의 인용이 있는 경우, 권말의 Reference에서 인용 부분을 게재해 주세요.

### 비영리 목적 이용에 대하여

재이용(2차 이용)이 허락되어 있습니다.

### 영리 목적 재이용에 대하여

문의해 주세요.

### 기타

원래의 표현이 바뀌지 않는 범위(폰트, 사이즈 등)라면 개변이 가능합니다. 그 외의 개변 및 기타 라이선스에 관한 상세 내용은 링크를 확인하여 적절히 취급해 주세요.

---

## 대규모 언어 모델 개요 (Overview of Large Language Models)

준교수 이와사와 유스케

> ※ 허가 없는 촬영 및 제3자에 대한 공개를 금지합니다.
> 대규모 언어 모델 강좌 2025

※ 이번 시간은 개별 기술을 깊이 파고들기보다 전체 개요를 파악하는 것이 목적입니다. 많은 용어가 등장하지만, 모두 이번 회에 외워야 하는 것은 아닙니다.

---

## 이와사와 유스케 (岩澤有祐)

2017년 도쿄대학교 공학계열 연구과 박사과정 수료(마츠오 연구실). 졸업 후 특임연구원, 특임조교를 거쳐 2024년 1월부터 기술경영전략학 전공에서 준교수.

### 연구 테마

- 석사까지는 장애인 지원에 대한 머신러닝 기술 응용
- 박사부터는 딥러닝, 주로 전이학습 기술 관련 연구

### 생성AI 관련 활동

- "Large-Language Models are Zero-Shot Reasoners", NeurIPS2022 등
- JSAI2023, CSS2023에서 "파운데이션 모델의 기술과 전망" 튜토리얼 [Speaker Deck]
- 마츠오 연구실 주관 대규모 언어 모델 강좌 전체 설계
- 기시다 총리 등에 대한 대규모 언어 모델 특강(180분)
- DL 독서회: 마츠오 연구실 멤버, 강의 수강생 등이 참가하는 스터디 주관. 2015년~ 누적 350회 이상 실시(매주 금요일 아침 10:00)
- DL책(감역, 번역): Goodfellow 등이 집필한 딥러닝 교과서의 감역·번역. 2018년 출간.

---

## 목차

- LLM 개요 (왜 지금 LLM을 배워야 하는가?)
- 각 회차 개요
- 일본의 LLM을 둘러싼 환경

---

## 동기 (Motivation)

지금, 자연어를 다루는 어시스턴트 AI를 만들고 싶다고 가정해 봅시다.

예를 들어, 질문에 대해 올바른 답을 출력해 주길 원합니다.
- 예: Q. 일본의 수도는? A. 도쿄
- 예: "글을 영어로 번역해 줘"라고 하면 번역한 글을 출력해 주길 원합니다.
- 예: "테트리스 앱을 만들어 줘"라고 하면 그 코드를 생성해 주길 원합니다.

이제 이러한 것들은 웹상이나 간단한 프로그램으로 실현할 수 있게 되었습니다.

---

## AI + 생태계 발전의 예 | Hugging Face

① 100만 개를 넘는 모델
② 언어/이미지/음성/멀티모달 등

---

## 이것들은 어떻게 실현되는가? - 언어 모델의 역사

단어의 열(문장)을 𝑥₁, 𝑥₂, ⋯, 𝑥_𝐿이라 할 때, 그 생성 확률 𝑝(𝑥₁, 𝑥₂, ⋯, 𝑥_𝐿)을 할당하는 확률 모델 𝑝를 말합니다.

```
𝑝(일본, 의, 수도, 는, 도쿄) = 0.02
𝑝(일본, 의, 수도, 는, 파리) = 0.00001
𝑝(도쿄, 의, 수도, 는, 일본) = 0.0005
```

다양한 언어 과업이 이 생성 확률의 추정 문제로 다루어질 수 있습니다.

- 예: QA(어떤 질문에 이어지기에 적절한 답은?)
- 예: 번역(어떤 영어 문장에 이어지기에 적절한 일본어는?)
- 예: 코드 생성(어떤 지시문에 적절한 코드는?)

이 생성 확률을 어떻게 구하는가?가 언어 모델 기술적 문제 중 하나입니다.

---

## 자기회귀 언어 모델 (Autoregressive Language Models)

𝑝(𝑥₁, 𝑥₂, ⋯, 𝑥_𝐿)을 조건부 분포의 곱으로 표현합니다.

```
𝑝(𝑥₁, 𝑥₂, ⋯, 𝑥_𝐿) = 𝑝(𝑥₁) · 𝑝(𝑥₂|𝑥₁) · ⋯ · 𝑝(𝑥_𝐿|𝑥₁, 𝑥₂, ⋯, 𝑥_{𝐿−1})
```

이와 같이 확률의 연쇄 법칙으로 분해한 모델을 특히 자기회귀 언어 모델(Autoregressive Language Model)이라 부릅니다.

조건부 확률을 알면 생성하는 것도 가능합니다.

```
𝑝(도쿄 | 일본, 의, 수도, 는) = 0.2
𝑝(파리 | 일본, 의, 수도, 는) = 0.001
𝑝(카이로 | 일본, 의, 수도, 는) = 0.0005
```

이 조건부 확률을 어떻게 구하는가?

"일본의 수도는 → 도쿄"

---

## 신경망 언어 모델 (Neural Language Model)

조건부 확률을 어떤 신경망으로 추정한 모델입니다.

웹의 데이터를 모의하도록(가능도를 최대화하도록) 학습합니다.

(일본 → 의 → 수도 → 는 → 도쿄/교토)

---

## 트랜스포머 이전의 신경망 언어 모델의 과제

합성곱 신경망이나 MLP 등에서는 긴 문맥의 처리가 어렵습니다.
- 예를 들어 번역에서는 원문을 충실히 반영하여 번역문을 결정해야 합니다.
- 어느 정도 긴 계열 정보를 처리하지 못하면 풀 수 없는 과업이 있습니다.

RNN 계열 모델은 학습이 병렬화되지 않아 스케일화가 곤란합니다.
- 데이터를 순차적으로 처리하는 성질상, 학습이나 추론의 병렬화가 어렵습니다.
- 그 밖에도 학습이 어렵다는 문제가 있습니다(기울기 소실 문제).

---

## 트랜스포머 (Transformer)

"Attention is All You Need", NeurIPS 2017

- Google을 중심으로 한 연구팀이 2017년에 발표
- Self Attention을 중심으로 한 네트워크 구조(좌측 그림)
  - ※ 구조의 상세는 별도 일정에서 다룹니다
- 주로 번역 등의 지도학습에서 성능 검증(우측 그림)
  - 예: 영어 문장 → 트랜스포머 → 독일어 문장이 되도록 오차 역전파로 학습

[1] Ashish Vaswani et al. (2017) "Attention Is All You Need" NeurIPS 2017에서 인용

---

## GPT (Generative Pretraining Transformer)

"Improving Language Understanding by Generative Pre-training", 2018

### Pre-training (사전학습)

트랜스포머를 활용한 언어 모델로, Input으로 "Language models determine [mask]"를 넣으면 Output으로 단어 확률 "by analyzing text data"를 출력합니다.

- OpenAI에 의해 2018년에 발표된 모델
- 사전학습에 트랜스포머를 이용(트랜스포머를 사용한 언어 모델)
- 구체적으로는 다음에 올 단어를 트랜스포머로 예측하도록 학습(좌측 그림). Book Corpus라는 미공간 서적을 이용
- GPT, GPT-2, GPT-3로 버전을 거듭하며 학습 데이터 수와 모델 크기가 증가

[2] Alec Radford et al. (2018) "Improving Language Understanding by Generative Pre-training"를 참고

---

## 2020년 GPT-3 등장 후, 대규모 모델의 발표는 가속적으로 증가

[3] Wayne Xin Zhao et al. (2023), "A Survey of Large Language Models" arXiv:2303.18223에서 인용

---

## GPT-4가 가진 지식

- OpenAI에 의해 2023년에 발표된 모델(상세는 미공개, 누출 정보는 있음)
- 사법시험이나 SAT/GRE 등 다양한 시험에서 좋은 성적
  - 예: Uniform Bar Exam에서 298/400 (~90th)
  - 예: GRE (Quantitative) 163/179 (~80th)
- 한편 코딩 능력 등에서는 아직 낮은 점수(현재는 대폭 개선됨)

[4] OpenAI 2023 "GPT-4 Technical Report"에서 인용, 일부 개변

---

## 의료 QA (Igaku QA)

"Evaluating GPT-4 and ChatGPT on Japanese medical licensing examinations", 2023

- 언어 모델(GPT-4 및 ChatGPT)을 새롭게 작성한 일본 의료 면허 시험 6년 분량의 데이터셋(Igaku-QA)으로 벤치마크
- (1) 인간 평균 응시자보다는 나쁘다, (2) 금기술을 선택하는 경향이 있다, 등의 문제는 있으나 시험 합격선은 돌파

[5] Jungo Kasai et al. (2023), "Evaluating GPT-4 and ChatGPT on Japanese medical licensing examinations"에서 인용

---

## 대규모 언어 모델을 활용하는 기술도 진전 | 컨텍스트 엔지니어링 (Context Engineering)

"A Survey of Context Engineering for Large Language Models", 2025

- 언어 모델이 가진 지식을 사용할 뿐만 아니라, 필요한 컨텍스트를 선택하고 처리하는 기술
- RAG / 도구 이용(검색) / Deep Research / Memory 등 다양한 기술이 연구되고 있음

---

## 2025년에 등장한 대규모 언어 모델 (Generated by GPT-5)

| 모델명 | 개발사 | 공개 시기(2025) | 오픈/클로즈드 |
|--------|--------|-----------------|---------------|
| GPT-5 | OpenAI | 8월 | 클로즈드 |
| GPT-4.5 | OpenAI | 2월 | 클로즈드 |
| GPT-OSS | OpenAI | 8월 | 오픈 |
| Llama 4 Scout | Meta | 4월 | 오픈 |
| Llama 4 Maverick | Meta | 4월 | 오픈 |
| DeepSeek-R1 | DeepSeek | 1월 | 오픈 |
| DeepSeek-V3 | DeepSeek | 3월경 | 오픈 |
| Qwen3 (Think) | Alibaba/Qwen | 4월 | 오픈 |
| Qwen2.5-Max | Alibaba/Qwen | 초두 | 오픈 |
| Claude 3.7 Sonnet | Anthropic | 2월 | 클로즈드 |
| Grok-3 | xAI | 2월 | 클로즈드 |
| BitNet b1.58 2B4T | Ma 외 | 4월 | 오픈 |
| LLaDA | ML-GSAI 외 | 2월 | 오픈 |
| MMaDA | 연구팀 | 5월 | 오픈 |

---

## 모델 관련 트렌드

① 추론(Reasoning) 모델이라 불리는, 기존보다 추론 능력이 현저히 높은 모델의 등장(스스로 오류를 깨닫는 "Aha Moment") ⇒ 기존보다 복잡한 벤치마크 정비, 추론 프로세스 분석 등이 진전

② 성능이 높은 공개 모델의 증가

③ (다양한 의미에서) 효율이 좋은 모델 구조(확산 언어 모델 등)

---

## 벤치마크의 고도화

- **SWE Bench**: 이슈에 대한 PR을 작성하는 능력을 평가
- **Humanity's Last Exam**: Humanity's Last Exam이라는 챌린징한 문제(등장 시점 SoTA는 9%, 현재 21.6%)

문제 예시:
> "칼새목의 벌새는 꼬리 깃털 하제근(下制筋)의 퍼진 교차상 건막(腱膜)의 미측 외측 부분에 매립된, 좌우 한 쌍의 타원형 종자골(種子骨)을 가진다. 이 종자골에 의해 지지되는 건 쌍은 몇 개인가? 숫자로 답하시오."

---

## 여기까지의 정리 및 본 강좌의 취지

### 여기까지의 정리

- 언어 모델이란 단어열의 생성 확률을 모델화한 것(자기회귀 언어 모델 / 신경망 언어 모델 / GPT)
- 2025년이 된 지금도 그 활용 방법 / 모델 자체(대규모 추론 모델, 확산 언어 모델) / 평가 방법에 관한 연구개발은 진전 중
- 원리는 매우 심플. 왜 지금 언어 모델인가?

### 이후 내용

원리는 매우 단순합니다. 그렇다면 왜 지금 언어 모델인가?

---

## 왜 지금 언어 모델인가

[1] 대규모화에 수반하는 범용성
[2] 언어 이외의 도메인에 대한 영향

---

## 트랜스포머를 사용한 언어 모델의 거대화

기본적으로 어느 쪽이든 2017년에 발명된 트랜스포머라 불리는 구조를 이용합니다.

2018년 OpenAI의 GPT-1, 2019년, 2020년 GPT-3, 2023년 등 시기별로 스케일이 커졌습니다. GPT-3 등장 이후, 미국 기업을 중심으로 복수의 연구기관이 독자적인 대규모 언어 모델을 개발했습니다.

[6] Momentum Works 2023 "The future by ChatGPT"에서 인용, 일부 개변

---

## 왜 지금 LLM을 배워야 하는가? 1. Scaling and Emergence

### Scaling Law (스케일링 법칙)

3가지 변수에 대한 거듭제곱에 따라 성능이 올라갑니다: 계산 자원 C, 데이터셋 크기 D, 파라미터 수 N

### Emergent Ability (창발 능력)

모델 크기가 거대할 때만 풀 수 있는 과업이 존재합니다.

[7] Jared Kaplan et al. (2020), "Scaling Laws for Neural Language Models"에서 인용(좌측 그림)
[8] Jason Wei et al. (2022), "Emergent Abilities of Large Language Models"에서 인용(우측 그림)

---

## GPT-3의 학습 데이터량

"Language Models are Few-Shot Learners", 2020

GPT-3의 사전학습 토큰 수:
- 약 5,000억 토큰의 텍스트를 이용
  - ※ 토큰이란, 언어 AI가 처리하는 단위. 일본어의 경우 대략 1글자 1토큰
- 책으로 치면 GPT-3는 약 500만 권에 상당
  - 참고: 도쿄대 도서관이 약 130만 권, 국회도서관이 약 4,700만 권
- ※ 누출 정보에 따르면 GPT-4는 약 1.3억 권에 상당

[9] Tom Brown et al. (2020), "Language Models are Few-Shot Learners", NeurIPS2020에서 인용

---

## 대규모 연산을 위한 도구: GPU

---

## 대규모 모델/데이터를 지탱하는 대규모 연산 자원(GPU)

AI 개발에는 방대한 데이터를 고속으로 처리하는 연산 자원이 필요합니다. 현재 자주 쓰이는 연산 자원은 GPU라 불리는 것이며, 지배적인 점유율을 가진 NVIDIA도 급성장했습니다. 일본도 GPU 확보에 나서고 있으나, 해외 세력과의 격차는 큽니다.

### GPU 종류 (H100, A100, V100 등)

- GPT-3 상당의 경우: A100 × 1,200대 × 30일
- GPT-4 상당의 경우: A100 × 25,000대 × 100일(*)
- 이번 연습의 경우: A100 × 8대 × 1시간

(*) 누출 정보. OpenAI의 공식 발표가 아님

### 세계 GPU 점유율의 90%를 차지하는 NVIDIA(미국)

AI 수요를 순풍으로 삼아 급성장. 일시적으로 세계 시가총액 1위에.

### 국내외 대표적인 GPU 클러스터(*)

(*) GPU를 탑재한 복수의 컴퓨터를 묶어 제공하는 시스템

**해외**(단일 기업으로 수십만~백만 기의 H100 GPU 보유, 이하 24년 단년도 구매 수):
- Google: 169,000대
- Amazon: 196,000대
- Meta: 224,000대
- Microsoft: 485,000대

**국내(일본)**:
- 산업기술종합연구소(産総研)의 ABCI: 960대의 A100 GPU → 6,128대의 H200 GPU(*2025년 1월 업그레이드)
- SoftBank: 6,000대의 GPU
- 사쿠라 인터넷: 2,000대의 H100 GPU

이 격차는 근본적으로 전술한 구조적 문제, 즉 IT 서비스와 생성AI 사이의 선순환이 만들어지고 있는가, 에서 비롯됩니다.

[10] Dan Swinhoe (2024), "Microsoft bought twice as many Nvidia Hopper GPUs as other big tech companies - report", DataCenterDynamics

---

## 스케일이 가져온 것 - 범용성 -

사전학습을 마친 LLM(트랜스포머)을 통해 다음이 가능해집니다:
- Translation (Few-Shot)
- Translation (Zero-Shot)
- Summarization (Zero-Shot) - "TL;DR"로 시작하면 성능이 대폭 향상됨
- 그 밖에도 다수 예시 존재

[9] Tom Brown et al. (2020), "Language Models are Few-Shot Learners"에서 인용

---

## 보충 | 파운데이션 모델 (Foundation Model)

"On the Opportunities and Risks of Foundation Models", 2021

- 2021/8/16 초출의 백서(White Paper)에서 등장한 용어
- Stanford의 연구기관 명칭에도 사용됨(청색 테두리)
- 다양한 과업에 적용 가능한 거대 모델에 의한 패러다임 시프트

> (초록에서 발췌) "AI is undergoing a paradigm shift with the rise of models (e.g., BERT, DALL-E, GPT-3) that are trained on broad data at scale and are adaptable to a wide range of downstream tasks. We call these models foundation models to underscore their critically central yet incomplete character."

(AI는 광범위한 데이터를 대규모로 학습하고 다양한 다운스트림 과업에 적응할 수 있는 모델(BERT, DALL-E, GPT-3 등)의 부상과 함께 패러다임 전환을 겪고 있습니다. 우리는 이 모델들을 파운데이션 모델이라 부르며, 그 임계적으로 핵심적이면서도 미완성인 성격을 강조합니다.)

[11] Rishi Bommasani et al. (2021) "On the Opportunities and Risks of Foundation Models"에서 인용, 일부 개변

---

## 왜 지금 언어 모델인가

[1] 대규모화에 수반하는 범용성
[2] 언어 이외의 도메인에 대한 영향

---

## GPT-4에 의한 이미지 인식(및 로봇 응용) - 멀티모달 파운데이션 모델

"GPT-4 Technical Report", 2024

[13] Figure AI Inc. (2024), "Figure Official Website" https://www.figure.ai/

---

## LLM 활용 | Say-Can and Say-Can-PaLM

"Do As I Can, Not As I Say: Grounding Language in Robotic Affordances", 2022

- 언어 모델이 출력한 스킬의 실행 가능성(Skill Affordance)을 고려하여 선택
  - 실행 가능성은 TD(강화학습)로 학습
- 언어 모델을 개선하면(PaLM 사용) 성능이 향상됨
- ※ 실행 가능한 스킬(저수준 정책)은 사전에 준비되어 있다는 점에 주의

[14] Michael Ahn et al. (2022), "Do As I Can, Not As I Say: Grounding Language in Robotic Affordances"에서 인용

---

## 행동 계열의 생성(실행 결과) - 마츠오 연구실 연구 예

성과 예: RoboCup Japan Open 2023 우승, RoboCup 세계대회 3위

---

## 로보틱스 파운데이션 모델 (Robotics Foundation Model)

실제 세계 환경(Real World Environment)과 로보틱스 파운데이션 모델(Robotics Foundation Model)이 action/observation 쌍의 대규모·다양한 데이터로 학습하며, 산업 응용(Industrial Application), 자율주행(Autonomous Driving), 생활 지원(Life Support) 등에 활용됩니다.

---

## 로봇 트랜스포머 (RT-1)

"RT-1: Robotics Transformer for Real-World Control at Scale", 2022

### 모델
- EfficientNet과 트랜스포머의 조합
- 인스트럭션에 따라 동작 생성

### 데이터
- EDR 13대, 17개월, 744 과업, 13만 데모
- 학습: 97%에서 동작
- 일반화: 다양한 의미에서 대폭 향상(미지 과업, 미지 소스 등)
- Long Horizon 과업도 가능
- ※ 유사 연구로 Gato, BC-Z 등

[15] Anthony Brohan et al. (2022), "RT-1: Robotics Transformer for Real-World Control at Scale"에서 인용

---

## Google과의 협업 - RT-X Project

- ICRA 2024 최우수 논문상 수상
- Google Deepmind 및 21개 연구기관이 통일된 포맷의 오프라인 로봇 데이터셋을 수집
- 22가지 로봇 타입, 527개 스킬(160,266 과업), 100만 에피소드 이상
- 개별 데이터로 학습한 모델보다 더 나은 성능

[16] O'Neill, Abby, et al. (2023), "Open x-embodiment: Robotic learning datasets and rt-x models.", arXiv:2310.08864

---

## 비전-언어-액션 모델 (Vision Language Action Model)

- 𝜋₀ [Black+ 2024]
- VLA(Vision-Language-Action) 모델
- 세탁물을 개다, 달걀을 깨지 않게 케이스에 넣는 등, 다양한 과업을 수행할 수 있음

[17] Physical Intelligence (2024), "π0: A Generalist Model for Physical Intelligence", Physical Intelligence Blog

---

## AIRoA | AI Robot Association

특징(Uniqueness):
- 학계 주도(Led by academia)
- 개방성(Openness)
- 보상 설계(Reward design)

---

## 세계 시뮬레이터 | Sora (OpenAI)

- Prompt: A young man at his 20s is sitting on a piece of cloud in the sky, reading a book.
- Prompt: Photorealistic closeup video of two pirate ships battling each other as they sail inside a cup of coffee.

[18] OpenAI (2024), "Sora: Creating video from text"
[19] OpenAI (2024), "Video generation models as world simulators"

---

## 여기까지의 정리와 본 강좌의 취지

### 정리
- 언어 모델이란 단어열의 생성 확률을 모델화한 것(자기회귀 언어 모델 / 신경망 언어 모델 / GPT)
- 2025년이 된 지금도 그 활용 방법 / 모델 자체(대규모 추론 모델, 확산 언어 모델) / 평가 방법에 관한 연구개발은 진전 중
- 원리는 매우 심플. 왜 지금 언어 모델인가?
  1. 모델, 데이터, 계산량의 스케일에 의해 할 수 있는 것이 급속히 넓어지고 있음(일반화성)
  2. 언어 모델의 발전이 다른 영역에도 영향을 주고 있음

### 본 강좌의 취지
- LLM의 기술적 배경, 원리와 한계를 이해한다
- 히프(Hype)가 아닌 활용 기술로서 파악할 수 있게 된다

---

## 고지마 타케시 (小島武)

### 약력
- 2023.3 도쿄대학교 대학원 공학계열 연구과 TMI 박사과정 수료
- 2023.4~ 동 연구과 특임연구원
- 2025.1~ 동 연구과 특임조교
- ※ 이전에는 IT 엔지니어 출신

### 활동
Weblab-10B 개발, 기시다 총리·이시바 총리의 LLM 특별강좌 강사, LLM 개발 콘테스트 2024·2025 운영 콘텐츠 리더, AI 백서 2025에서 Safety 장 집필

### 연구
LLM의 동작 원리 이해와 제어(Reasoning Model, 다언어 등), Safety(Unlearning, 지시 추종 능력, 로봇), 트랜스포머 모델 구조 개선 등

[20] Takeshi Kojima, et al. (2025), "A Comprehensive Survey on Physical Risk Control in the Era of Foundation Model-enabled Robotics", arXiv:2505.12583
[21] https://github.com/kojima-takeshi188/zero_shot_cot

---

## 목차

- LLM 개황
- 각 회차 개요
- 일본의 LLM을 둘러싼 환경

---

## 강좌를 구성함에 있어

올해도는 "대규모 언어 모델 기초"와 "대규모 언어 모델 응용"으로 강좌를 나눕니다.

**대규모 언어 모델 기초(10~11월)**:
- LLM의 전체상을 이해하기 위해, 사전학습·사후학습·데이터 수집 가공·벤치마크 평가 등 학습 파이프라인을 망라적으로 해설
- 공개 모델이나 API를 활용하여 추론 성능을 향상시키는 기법도 친절하게 소개

**대규모 언어 모델 응용(12월~2월)**:
- 경량화·안전 대책·해석성·도메인 특화·LLM 에이전트 등, LLM의 사회 구현에 불가결한 기술을 본격적으로 학습
- 최전선에서 LLM을 연구개발하는 제1인자에 의한 특별 강연 진행
- 매년 행사가 된 "개인형 LLM 개발 콘테스트"도 파워업하여 개최 예정. 수강생 간의 열띤 기술 경쟁이 학습을 더욱 깊게 합니다

---

## LLM 학습 파이프라인에서 본 강좌 구성

- **Step 1. 사전학습**: 대규모 코퍼스에 의한 자기지도학습을 통해 언어 모델에 어휘·문법·지식 등 기본적인 언어 이해를 획득시키는 단계
- **Step 2. 파인튜닝**: 라벨링된 데이터에 의한 지도학습을 통해 언어 모델의 성능을 개선하거나, 특정 과업이나 도메인에 대한 적응을 실현하는 단계
- **Step 3. 강화학습**: (인간의) 피드백을 이용한 강화학습을 통해 언어 모델의 출력이 인간의 가치관에 보다 부합하도록 조정하는 단계 (Step 2~3을 묶어 "사후학습"이라 부름)
- **Step 4. 데이터 수집·가공**: 사전학습이나 사후학습에 사용할 학습 데이터를 수집·가공하는 단계. 최근에는 LLM 자체를 이용한 데이터 합성도 성행
- **Step 5. 추론**: 사전학습·사후학습이 완료된 모델에 대해 프롬프팅을 구사하여 추가로 성능을 향상시키는 단계
- **Step 6. 벤치마크 평가**: 학습에 사용되지 않은 샘플로 구성된 벤치마크를 이용해 모델 성능을 평가하는 단계

매핑: Day2(추론) / Day3~5(사전학습) / Day6(파인튜닝) / Day7(강화학습) / Day8(데이터·벤치마크) / 차회·신회

[22] 도쿄대학교 마츠오·이와사와 연구실(2026), "대규모 언어 모델 사회구현 강좌"

---

## LLM 강좌 2025【기초편】전체상

- 제1회: 강좌 개요
- 제2회: 추론(Prompting, In-context Learning)
- 제3회: 사전학습
- 제4회: 스케일 법칙
- 제5회: 사전학습(상신편)
- 제6회: 파인튜닝
- 제7회: 강화학습
- 제8회: 학습 데이터와 평가 벤치마크 정비

> **지금 여기(いまココ)**

---

## 각 회차 개요【제2회: 추론(Prompting, In-context Learning)】

LLM의 활용법에 대해 배웁니다. 학습 완료 후 LLM의 성능을 끌어내는 기술을 습득합니다.

- Zero-Shot / Few-Shot
- Prompting
- 기타 등

[8] Tom Brown et al. (2020), "Language Models are Few-Shot Learners"에서 인용
[23] Sander Schulhoff, et al. (2024), "The Prompt Report: A Systematic Survey of Prompt Engineering Techniques", arXiv:2406.06608

---

## 각 회차 개요【제2회: 추론 - Chain-of-Thought Prompting (CoT)】

- 정답에 도달할 때까지 복수 스텝의 처리가 필요한, 다단계 추론이 필요한 과업
- 정답에 도달하기까지의 사고의 연쇄(Chain-of-Thought)를 예시로 제공

[24] Wei et al., 2022, "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"

---

## 각 회차 개요【제2회: 추론 - Zero-shot CoT】

Chain-of-Thought의 예를 주지 않고, 모델 스스로 생각하게 합니다. "Let's think step by step."

※ 참고: 공동 저자인 Shane 선생님이 최근 "Video Models are zero-shot learners and reasoners"를 발표했습니다.

[25] Kojima et al., 2022, "Large Language Models are Zero-Shot Reasoners"
[26] Shane Gu (2025), "X Post (status/1972309771610100179)"

---

## 각 회차 개요【제2회: 추론 - Self-Consistency, Majority Voting】

- CoT를 전제로 한 추가 성능 개선 예: Self-Consistency, 다수결(Majority Voting)
- Top-k, Top-p sampling하여 복수의 답안을 얻은 뒤, 가장 많았던 답안을 채택

[27] Wang et al., 2023, "Self-Consistency Improves Chain of Thought Reasoning in Language Models"

---

## 각 회차 개요【제2회: 추론 - GEPA】

- **Genetic-Pareto (GEPA)**: 프롬프트 자동 개선 기법
  - 과업을 실제로 수행하여 성공·실패의 궤적 데이터를 기반으로 언어 피드백으로 프롬프트를 개선하거나, 다른 유력한 프롬프트 후보와 조합
  - 개선할 프롬프트를 고를 때 다양성 확보를 위해 1문제에서만 가장 좋은 점수를 낸 프롬프트도 후보에 포함

[28] Agrawal et al., 2025, "GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning"

---

## 각 회차 개요【제3회: 사전학습】

LLM의 주류 모델 구조인 트랜스포머와 그 사전학습 메커니즘에 대해 배웁니다.

- Embedding
- Multi-Head Attention(어텐션)
- Feed Forward
- 기타

[1] Ashish Vaswani et al. (2017), "Attention Is All You Need", NeurIPS2017에서 인용

---

## 각 회차 개요【제3회: 사전학습 - 어텐션 기구】

어텐션 기구: 모든 단어(토큰) 간의 유사도를 측정함으로써, 장거리 의존 관계를 파악하는 메커니즘.
※ 유사도는 벡터의 내적으로 측정.
⇒ 필요한 토큰의 정보를 유연하게 취사선택 + 병렬 계산의 고속화

[29] Raimi Karim (2019), "Illustrated: Self-Attention", Towards Data Science

---

## 각 회차 개요【제3회: 사전학습 - 어텐션 기구(계속)】

어텐션 기구: 모든 단어(토큰) 간의 유사도를 측정함으로써, 장거리 의존 관계를 파악하는 메커니즘.
※ 유사도는 벡터의 내적으로 측정.
⇒ 필요한 토큰의 정보를 유연하게 취사선택 + 병렬 계산의 고속화

[29] Raimi Karim (2019), "Illustrated: Self-Attention", Towards Data Science

---

## 각 회차 개요【제3회: 사전학습 - 어텐션 시각화 예】

- "it"은 "The", "animal"에 대해 강한 어텐션이 걸려 있음을 알 수 있음
- 명시적으로 가르치지 않았는데도, 사전학습 과정에서 모델 스스로 이 관계성을 도출함
- ※ 실제로는 이렇게까지 명확하지는 않음

[30] Jay Alammar (2018), "The Illustrated Transformer"

---

## 각 회차 개요【제3회: 사전학습 - 트랜스포머 구조 분류】

[Vaswani+ 17], 일부 개변

- **Encoder-only**: BERT, RoBERTa 등 - 인식 계열(클래스 분류)
- **Encoder-Decoder**: BART, T5 등 - 생성 계열
- **Decoder-only**: GPT, Llama, Qwen, DeepSeek 등 - 생성 계열

---

## 각 회차 개요【제3회: 사전학습 - LLM의 큰 특징】

LLM의 큰 특징은 번역, 요약, 채팅 등 다양한 언어 과업에 대한 범용성입니다. 대량의 텍스트에서 세계의 지식을 사전학습함으로써 언어에 관한 범용성을 획득하고, 추가로 사후학습(파인튜닝이나 강화학습)으로 특정 기능이나 전문 분야에 특화합니다.

범용 모델 하나만 있으면 언어에 관한 다양한 기능을 개발할 수 있습니다(번역 앱, 의사록 요약 앱, 채팅 봇 등).

---

## 각 회차 개요【제3회: 사전학습 - 학습 원리】

사전학습은 웹에서 수집한 대량의 글을 사용해 다음 단어 예측을 쉬지 않고 수행합니다.

사전학습 과정에서 읽기·쓰기·셈하기 및 세계의 모든 지식을 학습합니다.

- GPT 시리즈를 대표로 하는 현대 LLM은 반드시 이 사전학습을 수행
- 예를 들어 아래 그림처럼 "봄은 벚꽃이 예쁘다"라는 텍스트의 사전학습에 의해 "봄", "벚꽃", "예쁘다"라는 말 사이에 강한 관계성이 있다는 것(=세계의 지식)을 학습

- 입력 단어의 다음에 올 단어를 예측
- 예측과 정답의 오차(=교차 엔트로피)가 작아지도록 모델을 학습
  - P(는|봄), P(벚꽃|봄, 는), P(가|...), P(예쁘다|...) 등

---

## 각 회차 개요【제4회: 스케일 법칙 (Scaling Law)】

스케일 법칙(Scaling Law)이란, 계산 자원, 학습 데이터량, 파라미터 수의 증가에 비례하여 사전학습 성능이 오른다는 경험칙입니다. 단순히 말하면, 자원을 투입할수록 LLM 성능이 좋아진다는 것.

- 발견 경위: 보다 큰 파라미터 크기의 "트랜스포머"로, 보다 대규모 데이터를 이용한 "사전학습"에 의해 LLM을 개발하는 과정에서 스케일 법칙이 발견됨
- 즉, 자원을 투하할수록 고성능 LLM을 만들 수 있다는 것이 밝혀짐. 크게 흐름이 바뀐 순간
- OpenAI는 일찍이 스케일 법칙에 주목하여 대규모 개발을 시작했고, 그 후 세계적인 투자 경쟁이 시작됨

[31] Tom Henighan, Jared Kaplan, et al. (2020), "Scaling Laws for Autoregressive Generative Modeling"

---

## 각 회차 개요【제4회: 스케일 법칙 - 다른 도메인 적용】

이미지 생성, 멀티모달, 동영상, 수리 등에서도 계산량에 관한 스케일 법칙이 성립합니다.

"Scaling Laws for Autoregressive Generative Modeling"

[31] Tom Henighan, Jared Kaplan, et al. (2020), "Scaling Laws for Autoregressive Generative Modeling", arXiv:2010.14701

---

## 보충: LLM 개발에 필요한 3요소

스케일 법칙에 기초하면, ① 대규모 연산 자원, ② 대규모 데이터, ③ 우수한 인재가 LLM 성능을 좌우하는 중요 자원임이 도출됩니다. 각각 하드웨어 투자, 법 정비, 인적 자본 투자가 필요합니다.

스케일 법칙 → 생성AI 개발을 좌우하는 "세 종의 신기(三種の神器)":
- ② 대규모 데이터: 방대한 학습용 데이터가 필요. 이를 모으기 위해 저작권이나 개인정보 등 취급 방침의 정비가 필요 → 법 정비의 중요성
- ③ 우수한 인재: 예 - 트랜스포머나 학습 기법의 개발, 하이퍼파라미터 조정 등 → 인적 자본 투자의 중요성
- ① 대규모 연산 자원: GPU라 불리는, 학습을 고속으로 수행하는 서버 확보가 필요 → 하드웨어 투자의 중요성

거대한 파라미터의 모델은 사람이 연산 자원·데이터를 사용하고, 하이퍼파라미터 조정과 시행착오를 반복하여 만드는 것입니다.

---

## 각 회차 개요【제4회: 스케일 법칙 - 사후학습·추론】

- 최근에는 사전학습의 스케일 법칙뿐 아니라 사후학습과 추론의 스케일 법칙에 대한 연구도 성행
  - 사전학습의 스케일 법칙
  - 사후학습의 스케일 법칙
  - 추론의 스케일 법칙

"Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters", 2024

[32] Daisuke Okanohara, "X Post (status/1972421341988225340)"

---

## 각 회차 개요【제5회: 사전학습(상신편)】

언어 모델을 스케일(=대규모화)하여 사전학습할 때의 과제와 해결 방법에 대해 배웁니다.

- 계산량(C): 충분한 계산량/메모리량을 확보하여 효율적으로 학습할 필요
- 파라미터 수(N): 모델이 스케일함에 따라 증가하는 비용을 억제할 필요
- 데이터(D): 성능을 발휘하기 위한 학습용 데이터를 준비할 필요

[7] Jared Kaplan et al. (2020), "Scaling Laws for Neural Language Models", arXiv:2001.08361

---

## 각 회차 개요【제5회: Sparse Transformer】

- Sparse(희소)한 Attention의 제안
- Attention을 계산하는 부분을 한정(계산하지 않는 부분은 마스크)하여 계산량을 삭감
- 이미지나 음성과 같은 모달리티에서도 트랜스포머의 이용이 가능해짐

[33] Child, Rewon, et al. (2019), "Generating Long Sequences with Sparse Transformers", arXiv:1904.10509

---

## 각 회차 개요【제5회: Sparse Transformer(계속)】

2회 어텐션 기구를 통과시키면 모든 토큰에 어텐션이 도달함.

[34] sunbluesome (2022), "Sparse Transformer를 이해하고 싶다", Zenn

---

## 각 회차 개요【제5회: Switch Transformer】

1조 6,000억 파라미터의 MoE(Mixture of Experts) 모델

피드포워드 네트워크를 복수 엑스퍼트화하고, 데이터에 따라 엑스퍼트를 선택합니다.

[35] William Fedus et al. (2022), "Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity", JMLR 23

---

## 각 회차 개요【제5회: LLM.int8()】

성능 열화 없이 가능한 양자화(Quantization) 방법

- Step1. 입력된 은닉 상태에서, 열 단위로 이상치(어떤 임계값보다 큰 값)를 추출
- Step2. 이상치 행렬은 FP16 그대로 행렬 연산. 이상치가 아닌 행렬은 INT8로 변환(양자화)하여 행렬 연산
- Step3. 2개의 출력값이 존재. INT8 출력값은 FP16으로 되돌려, 2개의 출력값을 가산하여 FP16으로 반환

[36] Tim Dettmers, et al. (2022), "A Gentle Summary of LLM.int8(): Zero Degradation Matrix Multiplication for Large Language Models", Hugging Face Blog

---

## 각 회차 개요【제5회: 대규모 분산 학습】

멀티 노드·멀티 GPU를 이용한 대규모 분산 학습

[37] Microsoft Deep Speed Team (2023), DeepSpeed: 딥러닝 학습과 추론을 획기적으로 고속화하는 프레임워크

---

## 각 회차 개요【제6회: 파인튜닝】

사전학습 완료 후에 수행하는 추가 학습 = 파인튜닝에 대해 배웁니다.

- 사후학습(파인튜닝)
  - 인간과 대화할 수 있도록, QA 데이터·채팅 데이터로 학습
  - 사전학습과 마찬가지로 다음 단어를 쉬지 않고 예측하는 학습 기법(※ A 부분만)

예시:
- Q: 일본에서 가장 높은 산은? / A: 후지산
- Q: 건강 유지를 위한 3가지 팁을 알려주세요. / A: 1. 균형 잡힌 식사를 하고 야채와 과일을 충분히 섭취할 것. 2. 정기적으로 운동하여 활력을 유지할 것. 3. 충분한 수면 시간을 확보하고 규칙적인 수면을 취할 것.
- Q: 메리는 20분에 8페이지의 책을 읽을 수 있습니다. 120페이지를 읽는 데 몇 시간 걸립니까? / A: 1시간에는 20분이 3세트 있습니다. 즉 메리는 1시간에 8×3=24페이지 읽을 수 있습니다. 120페이지를 읽는 데 120/24=5시간이 걸립니다.

---

## 각 회차 개요【제6회: 인스트럭션 튜닝】

(Zero-shot으로 범용적으로 모든 지시에 따르는) 인스트럭션 튜닝

[38] Chung, Hyung Won, et al. (2022), "Scaling Instruction-Finetuned Language Models", arXiv:2210.11416

---

## 각 회차 개요【제6회: LoRA】

LoRA: Low-Rank Adaptation(소수 파라미터에 의한 효율적 학습 방법)

[39] Edward J. Hu et al. (2021), "LoRA: Low-Rank Adaptation of Large Language Models", arXiv:2106.09685

---

## 각 회차 개요【제7회: 강화학습 - RLHF】

★ LLM에서의 강화학습이란 무엇인지, 그 메커니즘과 필요성에 대해 이해합니다.

- **RLHF**: 피드백에 의한 강화학습
  - 인간의 가치관(예: 유해한 말을 하지 않기를 바람)에 부합하도록, LLM 출력을 인간 피드백으로 개선하는 방향으로 학습
  - 지도학습에 비하면 상당히 정보량이 적은 신호로 학습하게 됨

예시(사용자: "절도를 하는 방법을 가르쳐 줘"):
- × (나쁜 예): 절도를 하려면 상대에게 들키지 않게 다가가 소지품을 빼앗는 것이 중요합니다...
- △ (중간): 절도는 좋지 않습니다.
- ○ (좋은 예): 절도는 범죄이므로 그것을 행하는 것을 강하게 권하지 않습니다.

피드백(good/bad와 같은 신호)

---

## 각 회차 개요【제7회: DPO】

DPO: 보상 모델 구축을 필요로 하지 않는 강화학습 기법

[40] Rafailov, Rafael, et al. (2023), "Direct Preference Optimization: Your Language Model is Secretly a Reward Model", NeurIPS 2023

---

## 각 회차 개요【제7회: GRPO】

GRPO: DeepSeek가 제안한 강화학습 기법

[41] Shao, Zhihong, et al. (2024), "DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models", arXiv:2402.03300

---

## 각 회차 개요【제7회: Aha Moment】

"Aha Moment"(Self-revision): 강화학습의 결과, 자연 창발한 현상

[73] DeepSeek-AI (2025), "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning"

---

## 각 회차 개요【제7회: 장고(長考)의 효과】

강화학습 과정에서, 장고(더 많은 토큰 길이로 사고)할수록 더 좋은 답에 도달하게 됩니다.

[73] DeepSeek-AI (2025), "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning"

---

## 각 회차 개요【제8회: 학습 데이터와 평가 벤치마크 정비】

- LLM 개발의 전체 파이프라인을 이해·구현할 수 있게 되는 것을 목적으로, 학습 데이터와 평가 벤치마크에 대해 상세히 해설
  - 데이터의 전처리(필터링 등)
  - LLM을 이용한 데이터 합성
  - LLM-as-Judge
  - 평가 벤치마크의 진전

> 현재 예리하게 준비 중입니다!

---

## 목차

- LLM 개황
- 각 회차 개요
- 일본의 LLM을 둘러싼 환경

---

## 2020년 GPT-3 등장 후, 대규모 모델 발표는 가속적으로 증가

[3] Wayne Xin Zhao et al. (2023), "A Survey of Large Language Models"(버전 16), arXiv:2303.18223

---

## 세계의 대규모 언어 모델 개발 현황(~2023년)

2018년 OpenAI의 GPT-1 등장 이후, LLM의 파라미터 크기는 스케일 법칙에 따라 비약적으로 증대했습니다.

(2018년 → 2019년 → 2020년 → 2023년 순서로 스케일 확대)

---

## 일본 발 모델과 그 모델 크기(@LLM 강좌 2023)

2023년부터 개발 경쟁이 가속(※ 2023년 이전에도 rinna, ABEJA, RICOH 등이 개발하고 있었음).

- ※ 2023.3 OpenAI가 GPT-4 공개
- 2023.5 사이버에이전트의 OpenCALM(7B)
- 2023.5 rinna의 일본어 특화형 GPT 모델(3.6B)
- 2023.7 NEC의 일본어 LLM(13B, 비공개)
- 2023.8 Stability AI의 Japanese StableLM Alpha(7B)
- 2023.8 LINE의 일본어 대규모 언어 모델(3.6B)
- 2023.8 도쿄대학교 마츠오 연구실의 Weblab-10B(10B)
- 2023.8 ELYZA-japanese-Llama(7B)

[42]-[48] (각 사 press release)

---

## 일본 발 모델과 그 모델 크기(@LLM 강좌 2024)

- 2023.9 PFN의 PLaMo-13B(13B)
- 2023.10 rinna의 Youri(7B)
- 2023.11 NTT의 tsuzumi(7B)
- 2023.12 도쿄공대의 Swallow(70B)
- 2024.3 ELYZA-japanese-Llama-2(70B)
- 2024.3 라쿠텐의 Rakuten AI(7B)
- 2024.4 NEC의 cotomi Pro / Light(?B)
- 2024.4 LLM 스터디회의 LLM-jp-13B(13B)
- 2024.5 Fujitsu의 Fugaku-LLM(13B)
- 2024.5 Stockmark-LLM-100b(100B)
- 2024.6 SB Intuitions의 Sarashina1-65B(65B)
- 2024.6 PFN의 PLaMo-100B(100B)
- 2024.7 CyberAgent의 CALM3(22B)
- 2024.7 도쿄공대의 Llama-3-Swallow(70B)
- 2024.8 SB Intuitions의 Sarashina2-70B(70B)
- 2024.8 마츠오·이와사와 연구실 Geniac 기획의 tanuki-8x8b(47B)

[49]-[63] (각 사 press release)

---

## 일본 발 모델과 그 모델 크기(@LLM 강좌 2025)

- 2024.08 PLaMo-10x100B(1T=1000B)
- 2024.09 llm-jp-3-172b(172B)
- 2024.10 PFN PLaMo-100B(100B)
- 2024.11 Sarashina2-8x70B(465B)
- 2025.01 CA DeepSeek-R1-Distill-Qwen-32B-Japanese(32B)
- 2025.03 Stockmark-2-100B-Instruct-beta(100B)
- 2025.03 Llama 3.3 Swallow 70B(70B)
- 2025.05 ELYZA-Thinking-1.0-Qwen-32B(32B)
- 2025.05 ABEJA-Qwen2.5-32b-Japanese-v1.0(32B)

참고: 최근에는 수B 정도의 경량 언어 모델(Small Language Model: SLM)을 개발하는 조직도 증가 추세.
- 예: Rakuten AI 2.0 mini(1.5B), PLaMo 2 8B, PLaMo 2.1 2B(2B), Sarashina2.2(0.5~3B), Llama 3.1 Swallow 8B(8B)
- 배경 ①: 작은 모델이라도(스케일 법칙적으로 학습 효율은 나쁘지만) 더 많은 데이터로 더 오래 학습하여 높은 성능을 달성할 수 있음
- 배경 ②: 개발(학습) 완료 후의 추론 비용(운용 비용)까지 고려하면 작은 모델의 비용 대비 효과가 높음

※ (참고) [64] llm-jp (2024), "Awesome Japanese LLM", GitHub Pages

---

## Small Language Model(SLM)에 관한 보충

"Go smol or go home, Why we should train smaller LLMs on more tokens"에서 발췌

- **Chinchilla Trap**: Chinchilla 모델 크기(70B)는 크기 때문에 추론 비용이 높음. 추론 비용도 고려해 더 작은 모델을 장시간 학습해야 한다는 의견
- 최적 모델 크기의 40-60% 이내 모델 크기를 선택해, 10-42% 계산량 추가로 동일 성능 모델을 학습할 수 있다는 지적
- 같은 성능을 달성하기 위해 필요한 파라미터 크기(횡축)와 계산량(종축)의 관계

---

## 일본 발 모델의 대략적 분류

### 사전학습부터 시작하는 풀스크래치 개발

- 특징: 학습 완전 제어 가능, 라이선스도 독자적으로 결정, 학습 비용 높음, 기술적 난이도 높음
- 대표 모델: CALM3-22B, Weblab-10B, PLaMo-100B, LLM-jp-13B, Sarashina2-70B, tanuki-8x8b

### 사전학습 완료 영어 모델을 일본어로 지속 사전학습하여 개발

- 특징: 학습 비용 낮음, 언어 간 지식 전이에 의한 효율적 학습 기대, 학습 방식에 제한 발생, 라이선스 제약 가능성
- 대표 모델: ELYZA-japanese-Llama-70B, Swallow-70B, Llama-3-Swallow-70B
- ※ 이용하는 사전학습 완료 모델은 성능이 높은 모델이 선택되는 경향. Llama 기반이 많음

---

## 마츠오·이와사와 연구실의 성과(GENIAC 프로젝트)

[63] 도쿄대학교 마츠오·이와사와 연구실(2024), "마츠오·이와사와 연구실, 경산성·NEDO의 'GENIAC' 프로젝트에서 국내 최초 대규모 언어 모델(LLM)의 멀티모달화 등 개발 성과 공개"

---

## 마츠오·이와사와 연구실 Tanuki 모델

[63] 동일 (GENIAC 프로젝트 성과)

---

## Tanuki 모델의 특징

> "해외 모델은 어느 쪽인가 하면 무기질적이고 형식적인 답변을 하는 경향이 있습니다만, 그와 대조적으로 당해 모델은 공감성이나 배려가 있는 답변이나, 자연스러운 말투로의 작문이 뛰어났습니다."

[63] 동일 (GENIAC 프로젝트 성과)

---

## Tanuki-8B 데모

> "「Tanuki-8×8B」의 경량판인 「Tanuki-8B」를 채팅 형식으로 이용할 수 있는 데모를 아래 URL에 공개하고 있습니다. 아래 URL에 접속하여 실제 대화를 시도해 보세요."

[58] weblab-GENIAC (2024), "Tanuki-8B-dpo-v1.0", Hugging Face Spaces

---

## 연산 자원(GPU)

AI 개발에는 방대한 데이터를 고속으로 처리하는 연산 자원이 필요합니다. 현재 자주 쓰이는 연산 자원은 GPU이며, 지배적 점유율을 가진 NVIDIA도 급성장했습니다. 일본도 GPU 확보에 나서고 있으나, 해외 세력과의 격차는 큽니다.

### GPU 종류(H100, A100, V100 등)

- GPT-3 상당: A100 × 1,200대 × 30일
- GPT-4 상당: A100 × 25,000대 × 100일(*)
- (*) 누출 정보. OpenAI 공식 발표가 아님

### 세계 GPU 점유율 90%를 차지하는 NVIDIA(미국)

AI 수요를 순풍으로 삼아 급성장. 일시적으로 세계 시가총액 1위.

### 국내외 대표적 GPU 클러스터(*)

(*) GPU를 탑재한 복수 컴퓨터를 묶어 제공하는 시스템

**해외**(단일 기업 수십만~백만 기의 H100 GPU 보유, 24년 단년도 구매 수):
- Google: 169,000대
- Amazon: 196,000대
- Meta: 224,000대
- Microsoft: 485,000대

**국내(일본)**:
- 산업기술종합연구소 ABCI: 960대 A100 GPU → 6,128대 H200 GPU(*2025년 1월 업그레이드)
- SoftBank: 6,000대 GPU
- 사쿠라 인터넷: 2,000대 H100 GPU

[66] Dan Swinhoe (2024), "Microsoft bought twice as many Nvidia Hopper GPUs as other big tech companies - report", DataCenterDynamics

---

## 연산 환경(GPU) - GPU의 고속 진화

- 고속한 세대 교체
- 후속 세대일수록 계산 속도가 빠르고(좌측 그림), 전력 소비=비용도 낮음(우측 그림)
- 일본에는 후발의 이점이 있을지도?

(P100 → V100 → A100 → H100 → B100 순서로 발전)

[67] Timothy Prickett Morgan (2024), "Nvidia Unfolds GPU, Interconnect Roadmaps Out To 2027", The Next Platform

---

## 학습 데이터(사전학습용 일본어 데이터)

- 사전학습에서 대량의 텍스트 데이터를 학습
  - 범용성과 고성능의 원천
  - 인터넷에서 수집한 대량의 텍스트 데이터를 사용
  - 그 텍스트 데이터의 대부분은 일부 주요 언어(예: 영어)로 구성되어 있으며, 그 이외 언어(예: 일본어)의 텍스트 데이터를 대량 수집하는 것은 현재 한계가 있음

[68] Linting Xue et al. (2021), "mT5: A massively multilingual pre-trained text-to-text transformer" ACL2021에서 인용, 일부 개변

---

## 학습 데이터(사전학습용 일본어 데이터) - 데이터 원천

어느 쪽이든 데이터 원천은 "Common Crawl"(https://commoncrawl.org/, 인터넷상 사이트를 크롤링한 아카이브)입니다.

※ 그 밖에 Wikipedia(ja)의 덤프가 자주 사용됨.

개산: 상기 합계로 약 1.3TB, 1토큰 2문자 ≒ 4바이트로 하면 약 0.3T 토큰.
※ Llama2의 2T 토큰, GPT-4의 13T 토큰(누출 정보)과 비교하면 상당한 괴리가 있음.

[69] 사쿠라이 아키오(2022), "세계에서 개발이 진행되는 대규모 언어 모델이란(후편)" | NTT 데이터 첨단기술 주식회사에서 인용

---

## 학습 데이터(사전학습용 일본어 데이터) - LLM-jp 코퍼스

일본어 6,880억 토큰.

구성 데이터:
- 청공문고의 텍스트
- Common Crawl 전체에서 추출·필터링한 일본어 코퍼스
- e-Gov 법령 텍스트
- FineWeb 2의 일본어 부분
- 과학연구비 조성사업 데이터베이스의 각 연구 프로젝트 개요 텍스트
- 국회 회의록 텍스트
- 특허청이 공개하는 데이터 파일에서 추출한 일본어 특허 텍스트
- 국립국회도서관 WARP에서 수집된 URL에서 크롤·추출한 텍스트
- 일본어 Wikipedia 등

[70] LLM-jp (2024), "llm-jp-corpus-v4", GitLab Datasets

---

## 학습 데이터 수집 시 주의점

### 저작권
- 저작권법에 의해 규정됨
- 위반 시 저작권 침해(형사벌)
- 저작권법 30조의4 제2호에서 AI 학습 데이터에 대해 규정
- ※ 일본은 구미에 비해 모델 학습에 이용 가능한 데이터의 자유도가 높다고 알려져 있음

### 라이선스/이용 약관
- 작성자와 이용자 간의 계약
- 위반 시 양자 간에 손해 배상 문제 등이 발생할 가능성

### 개인정보
- 개인정보보호위원회: 생성AI 서비스 이용에 관한 주의 환기 등
- ※ 상세는 법률 사무소에 상담하세요

[71] 개인정보보호위원회(2023), "생성AI 서비스 이용에 관한 주의 환기 등에 대해"

---

## 보충: 학습 데이터 수집 시 주의점 - 웹 크롤링

- 웹 크롤 시의 주의점
  - 웹 사이트 내에 robots.txt가 있는 경우, 그 내용에 따를 필요가 있음. 따르지 않고 웹 크롤링할 경우 저작권 침해에 해당할 가능성
  - 사례: The New York Times가 자사 기사를 게재하는 웹사이트의 robots.txt에서 AI 학습 데이터 수집용 크롤러를 차단하고, 별도 텍스트 데이터 마이닝용 라이선스 및 API를 판매하고 있음

(robots.txt 기재 내용 샘플 - RFC 9309 Robots Exclusion Protocol에서 인용)

---

## 보충: 학습 데이터 수집 시 주의점 - 이용 약관

- ChatGPT의 이용 약관 예시
- OpenAI의 이용 약관에서 일부 발췌

[72] OpenAI (2026), "Terms of Use", OpenAI Policies

---

## 보충: 학습 데이터 수집 시 주의점 - 라이선스 종류

OSS, CC 라이선스는 비교적 자유도가 높은 라이선스이지만, 다양한 종류가 있으므로 각각 이해가 필요합니다.

### Creative Commons (CC) 라이선스

| 라이선스 | 기호 | 명칭 | 상업 이용 | 개변 | 개변물 조건 | 크레딧 표기 | 비고 |
|----------|------|------|-----------|------|-------------|-------------|------|
| PD (CC0) | - | 퍼블릭 도메인 선언 | ○ | ○ | 제한 없음 | 불필요 | 모든 권리 포기 |
| CC BY | BY | 저작자표시 | ○ | ○ | 제한 없음 | 필요 | 이용원 명시 필요 |
| CC BY-SA | BY-SA | 저작자표시-동일조건 | ○ | ○ | 같은 라이선스로 공개 | 필요 | Wikipedia 채택 |
| CC BY-ND | BY-ND | 저작자표시-변경금지 | ○ | × | 개변 불가 | 필요 | 번역도 불가 |
| CC BY-NC | BY-NC | 저작자표시-비영리 | × | ○ | 제한 없음 | 필요 | 상업 이용 불가 |
| CC BY-NC-SA | BY-NC-SA | 저작자표시-비영리-동일조건 | × | ○ | 같은 라이선스로 공개 | 필요 | 상업 이용 불가 |
| CC BY-NC-ND | BY-NC-ND | 저작자표시-비영리-변경금지 | × | × | 개변 불가 | 필요 | 권리 지키면 자유로운 재배포 가능 |
| C | © | All rights reserved | × | × | 개변 불가 | 필요 | 권리자 사후 70년까지 보호 |

### OSS(Open Source Software) 라이선스

| 라이선스 | 특징 | 재배포 시 의무 |
|----------|------|----------------|
| MIT License | 저작권 표시와 라이선스 문구를 남기면 사용 가능 | 저작권 표시와 라이선스 문구 기재 |
| Apache License 2.0 | MIT보다 약간 엄격. 특허 권리도 커버 | 저작권 표시, 라이선스 문구, 변경점 명시 |
| GPL (GNU General Public License) | 강한 카피레프트. 개변·재배포하면 같은 GPL 라이선스로 공개 필수 | 소스 공개 + GPL 계승 |
| LGPL (Lesser GPL) | 라이브러리로서의 이용은 가능, 본체에는 강제하지 않음 | 개변 시에만 소스 공개 의무 |
| BSD License | MIT과 거의 동일. 상업 이용 가능. 선전 금지 조항이 있는 경우도 있음 | 저작권 표시와 면책 사항 기재 |

> Meta Llama 3 License: Meta가 독자적으로 정하는 라이선스. 월간 액티브 사용자 7억 명 이상의 기업에는 별도 라이선스 계약이 필요하므로, OSS 라이선스는 아님.

---

## 오늘의 정리

대규모 언어 모델(LLM)의 개요에 대해 소개했습니다.

1. **LLM 개황**을 설명했습니다.
   - 언어 모델이란 단어열의 생성 확률을 모델화한 것
   - 왜 지금 언어 모델인가? → 스케일, 범용성(Agent 등), 다른 영역으로의 영향(멀티모달·로봇)

2. **LLM 강좌 각 회차 개요**를 설명했습니다.
   - 기초편에서 LLM 개발의 기본 파이프라인 이해와 구현
   - 응용편에서 LLM 사회 구현까지를 고려한 기술의 이해와 구현

3. **일본의 LLM을 둘러싼 환경**을 설명했습니다.
   - 2023년 이후 본격적으로 개발 경쟁 가속
   - 데이터, 모델, 연산 환경을 스케일할 수 있는가가 관건

---

## 들어 주셔서 감사합니다.

---

## Reference

[1] Ashish Vaswani, et al. (2017), "Attention Is All You Need", NeurIPS 2017, https://arxiv.org/abs/1706.03762

[2] Alec Radford, et al. (2018), "Improving Language Understanding by Generative Pre-training", OpenAI Technical Report, https://openai.com/research/language-unsupervised

[3] Wayne Xin Zhao, et al. (2023), "A Survey of Large Language Models", arXiv:2303.18223, https://arxiv.org/abs/2303.18223

[4] OpenAI (2023), "GPT-4 Technical Report", arXiv:2303.08774, https://arxiv.org/abs/2303.08774

[5] Jungo Kasai, et al. (2023), "Evaluating GPT-4 and ChatGPT on Japanese medical licensing examinations", arXiv:2303.18027, https://arxiv.org/abs/2303.18027

[6] Momentum Works (2023), "The future by ChatGPT", https://momentum.asia/product/the-future-by-chatgpt/

[7] Jared Kaplan, et al. (2020), "Scaling Laws for Neural Language Models", arXiv:2001.08361, https://arxiv.org/abs/2001.08361

[8] Jason Wei, et al. (2022), "Emergent Abilities of Large Language Models", arXiv:2206.07682, https://arxiv.org/abs/2206.07682

[9] Tom Brown, et al. (2020), "Language Models are Few-Shot Learners", NeurIPS 2020, https://arxiv.org/abs/2005.14165

[10] Dan Swinhoe (2024), "Microsoft bought twice as many Nvidia Hopper GPUs as other big tech companies - report", DataCenterDynamics, https://www.datacenterdynamics.com/en/news/microsoft-bought-twice-as-many-nvidia-hopper-gpus-as-other-big-tech-companies-report/

[11] Rishi Bommasani, et al. (2021), "On the Opportunities and Risks of Foundation Models", arXiv:2108.07258, https://arxiv.org/abs/2108.07258

[12] Pengfei Liu, et al. (2021), "Pre-train, Prompt, and Predict: A Systematic Survey of Prompting Methods in Natural Language Processing", arXiv:2107.13586, https://arxiv.org/abs/2107.13586

[13] Figure AI Inc. (2024), "Figure Official Website", https://www.figure.ai/

[14] Michael Ahn, et al. (2022), "Do As I Can, Not As I Say: Grounding Language in Robotic Affordances", arXiv:2204.01691, https://arxiv.org/abs/2204.01691

[15] Anthony Brohan, et al. (2022), "RT-1: Robotics Transformer for Real-World Control at Scale", arXiv:2212.06817, https://arxiv.org/abs/2212.06817

[16] Abby O'Neill, et al. (2023), "Open X-Embodiment: Robotic learning datasets and rt-x models", arXiv:2310.08864, https://arxiv.org/abs/2310.08864

[17] Physical Intelligence (2024), "π0: A Generalist Model for Physical Intelligence", https://www.physicalintelligence.company/blog/pi0

[18] OpenAI (2024), "Sora: Creating video from text", https://openai.com/sora

[19] OpenAI (2024), "Video generation models as world simulators", https://openai.com/research/video-generation-models-as-world-simulators

[20] Takeshi Kojima, et al. (2025), "A Comprehensive Survey on Physical Risk Control in the Era of Foundation Model-enabled Robotics", arXiv:2505.12583, https://arxiv.org/abs/2505.12583

[21] Takeshi Kojima (2022), "zero_shot_cot", GitHub Repository, https://github.com/kojima-takeshi188/zero_shot_cot

[22] 도쿄대학교 마츠오·이와사와 연구실(2026), "대규모 언어 모델 사회구현 강좌", https://weblab.t.u-tokyo.ac.jp/education/large-language-model/

[23] Sander Schulhoff, et al. (2024), "The Prompt Report: A Systematic Survey of Prompt Engineering Techniques", arXiv:2406.06608, https://arxiv.org/abs/2406.06608

[24] Jason Wei, et al. (2022), "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models", arXiv:2201.11903, https://arxiv.org/abs/2201.11903

[25] Takeshi Kojima, et al. (2022), "Large Language Models are Zero-Shot Reasoners", arXiv:2205.11916, https://arxiv.org/abs/2205.11916

[26] Shane Gu (2025), "X Post (status/1972309771610100179)", https://x.com/shaneguML/status/1972309771610100179

[27] Xuezhi Wang, et al. (2023), "Self-Consistency Improves Chain of Thought Reasoning in Language Models", arXiv:2203.11171, https://arxiv.org/abs/2203.11171

[28] Sweta Agrawal, et al. (2025), "GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning", arXiv:2502.14856, https://arxiv.org/abs/2502.14856

[29] Raimi Karim (2019), "Illustrated: Self-Attention", Towards Data Science, https://towardsdatascience.com/illustrated-self-attention-2d627e33b20a

[30] Jay Alammar (2018), "The Illustrated Transformer", http://jalammar.github.io/illustrated-transformer/

[31] Tom Henighan, Jared Kaplan, et al. (2020), "Scaling Laws for Autoregressive Generative Modeling", arXiv:2010.14701, https://arxiv.org/abs/2010.14701

[32] Daisuke Okanohara, "X Post (status/1972421341988225340)", https://x.com/hillbig/status/1972421341988225340

[33] Rewon Child, et al. (2019), "Generating Long Sequences with Sparse Transformers", arXiv:1904.10509, https://arxiv.org/abs/1904.10509

[34] sunbluesome (2022), "Sparse Transformer를 이해하고 싶다", Zenn, https://zenn.dev/sunbluesome/articles/5f6a86dfa1e1be

[35] William Fedus et al. (2022), "Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity", JMLR 23, https://jmlr.org/papers/v23/21-0998.html

[36] Tim Dettmers, et al. (2022), "A Gentle Summary of LLM.int8(): Zero Degradation Matrix Multiplication for Large Language Models", Hugging Face Blog, https://huggingface.co/blog/hf-bitsandbytes-integration

[37] Microsoft Deep Speed Team (2023), "DeepSpeed: 딥러닝 학습과 추론을 획기적으로 고속화하는 프레임워크", https://www.deepspeed.ai/assets/files/DeepSpeed_Overview_Japanese_2023Jun7th.pdf

[38] Chung, Hyung Won, et al. (2022), "Scaling Instruction-Finetuned Language Models", arXiv:2210.11416, https://arxiv.org/abs/2210.11416

[39] Edward J. Hu et al. (2021), "LoRA: Low-Rank Adaptation of Large Language Models", arXiv:2106.09685, https://arxiv.org/abs/2106.09685

[40] Rafailov, Rafael, et al. (2023), "Direct Preference Optimization: Your Language Model is Secretly a Reward Model", NeurIPS 2023, https://arxiv.org/abs/2305.18290

[41] Shao, Zhihong, et al. (2024), "DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models", arXiv:2402.03300, https://arxiv.org/abs/2402.03300

[42] 주식회사 사이버에이전트(2023), "사이버에이전트, 최대 68억 파라미터의 일본어 LLM(대규모 언어 모델)을 일반 공개", https://www.cyberagent.co.jp/news/detail/id=28817

[43] rinna 주식회사(2023), "rinna, 일본어에 특화한 36억 파라미터의 GPT 언어 모델을 공개", https://rinna.co.jp/news/2023/05/20230507.html

[44] Stability AI Japan (2023), "일본어 언어 모델 「Japanese StableLM Alpha」를 릴리스했습니다", https://ja.stability.ai/blog/japanese-stablelm-alpha

[45] Ledge.ai 편집부(2023), "LINE 36억 파라미터의 일본어 LLM을 공개, 상업 이용도 가능", https://ledge.ai/articles/line_japanese_large_lm

[46] 일본전기주식회사(2023), "NEC, 130억 파라미터로 세계 톱클래스의 일본어 성능을 보유한 경량 LLM을 개발", https://jpn.nec.com/press/202307/20230706_02.html

[47] OpenAI (2023), "GPT-4", https://openai.com/research/gpt-4

[48] ELYZA (2023), "70억 파라미터의 상업 이용 가능 일본어 LLM 「ELYZA-japanese-Llama-2-7b」를 일반 공개했습니다", https://elyza.ai/news/2023/08/29/

[49] 일본전신전화주식회사(2023), "NTT판 LLM 「tsuzumi」", https://www.rd.ntt/research/LLM_tsuzumi.html

[50] 주식회사 ELYZA (2024), "700억 파라미터의 일본어 LLM 「ELYZA-japanese-Llama-2-70b」를 개발, 데모 공개", https://note.com/elyza/n/n0ea755ca3e7b

[51] 라쿠텐 그룹 주식회사(2024), "라쿠텐, 일본어에 최적화한 오픈형 고성능 LLM을 공개", https://corp.rakuten.co.jp/news/press/2024/0321_01.html

[52] rinna 주식회사(2023), "rinna, Llama 2의 일본어 지속 사전학습 모델 「Youri 7B」 시리즈를 공개", https://rinna.co.jp/news/2023/10/20231031.html

[53] 주식회사 사이버에이전트(2024), "독자 일본어 LLM 버전 3를 일반 공개 - 225억 파라미터 상업 이용 가능 모델 제공", https://www.cyberagent.co.jp/news/detail/id=30463

[54] Swallow-LLM Project (2024), "Llama 3 Swallow", https://swallow-llm.github.io/llama3-swallow.ja.html

[55] LLM-jp (2024), "대규모 언어 모델 「LLM-jp-13B v2.0」을 구축·공개", https://llm-jp.nii.ac.jp/blog/2024/04/30/v2.0-release.html

[56] 주식회사 Preferred Networks (2024), "GENIAC 제1사이클 개발 성과로 대규모 언어 모델 PLaMo-100B-Pretrained를 공개", https://www.preferred.jp/ja/news/pr20241015

[57] 주식회사 Preferred Networks (2023), "PLaMo-13B를 공개했습니다", https://tech.preferred.jp/ja/blog/llm-plamo/

[58] 일본전기주식회사(2024), "NEC, 세계 톱레벨 성능의 고속 대규모 언어 모델(LLM) cotomi Pro / cotomi Light를 개발", https://jpn.nec.com/press/202404/20240424_01.html

[59] 스톡마크 주식회사(2024), "할루시네이션을 대폭 억제하고 전문적 질문에도 정확한 답변이 가능한 생성AI - 스톡마크, 독자 130억 파라미터 LLM을 개발해 상업 이용 가능 오픈소스로 공개", https://stockmark.co.jp/news/20240516

[60] SB Intuitions 주식회사(2024), "SB Intuitions, 독자 일본어 LLM을 구축 - 70억·130억·650억 파라미터 일본어 LLM을 공개", https://www.sbintuitions.co.jp/news/press/20240614_01/

[61] 후지쯔 주식회사(2024), "슈퍼컴퓨터 「도쿄(富岳)」로 학습한 대규모 언어 모델 「Fugaku-LLM」을 공개", https://pr.fujitsu.com/jp/news/2024/05/10.html

[62] 도쿄공업대학(2023), "일본어에 강한 대규모 언어 모델 「Swallow」를 공개", https://www.titech.ac.jp/news/2023/068089

[63] 도쿄대학교 마츠오·이와사와 연구실(2024), "마츠오·이와사와 연구실, 경산성·NEDO의 「GENIAC」 프로젝트에서 국내 최초 대규모 언어 모델(LLM) 멀티모달화 등 개발 성과 공개", https://weblab.t.u-tokyo.ac.jp/2024-08-30/

[64] llm-jp (2024), "Awesome Japanese LLM", GitHub Pages, https://llm-jp.github.io/awesome-japanese-llm/

[65] weblab-GENIAC (2024), "Tanuki-8B-dpo-v1.0", Hugging Face Spaces, https://huggingface.co/spaces/weblab-GENIAC/Tanuki-8B-dpo-v1.0

[66] Dan Swinhoe (2024), "Microsoft bought twice as many Nvidia Hopper GPUs as other big tech companies - report", DataCenterDynamics, https://www.datacenterdynamics.com/en/news/microsoft-bought-twice-as-many-nvidia-hopper-gpus-as-other-big-tech-companies-report/

[67] Timothy Prickett Morgan (2024), "Nvidia Unfolds GPU, Interconnect Roadmaps Out To 2027", The Next Platform, https://www.nextplatform.com/2024/06/02/nvidia-unfolds-gpu-interconnect-roadmaps-out-to-2027/

[68] Linting Xue, et al. (2021), "mT5: A massively multilingual pre-trained text-to-text transformer", NAACL-HLT 2021, https://aclanthology.org/2021.naacl-main.41/

[69] 사쿠라이 아키오(2022), "세계에서 개발이 진행되는 대규모 언어 모델이란(후편)", NTT 데이터 첨단기술 주식회사 칼럼, https://www.intellilink.co.jp/column/ai/2022/072800.aspx

[70] LLM-jp (2024), "llm-jp-corpus-v4", GitLab Datasets, https://gitlab.llm-jp.nii.ac.jp/datasets/llm-jp-corpus-v4

[71] 개인정보보호위원회(2023), "생성AI 서비스 이용에 관한 주의 환기 등에 대해", https://www.ppc.go.jp/news/careful_information/230602_AI_utilize_alert/

[72] OpenAI (2026), "Terms of Use", OpenAI Policies, https://openai.com/ja-JP/policies/row-terms-of-use/

[73] DeepSeek-AI (2025), "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning", https://arxiv.org/abs/2501.12948
