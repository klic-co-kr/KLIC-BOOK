# Day 1 — 대규모 언어 모델 개요

> 번역 참고: 본 자료는 CC BY-NC-ND 4.0(저작자표시-비영리-변경금지 4.0 국제) 라이선스를 따르며, 교육 목적의 번역본입니다. 원문의 의미를 변경하지 않고, 반복되는 라이선스 푸터는 첫 회만 표시합니다.

---

## 도입: 이 강의에서 배우는 것

본 자료는 도쿄대학교 마츠오·이와사와 연구실이 작성한 것으로, 2025년 10~11월에 개최된 대규모 언어 모델 강좌 기초편의 첫 회 강의입니다. 원문은 CC BY-NC-SA 4.0(저작자표시-비영리-동일조건변경허락) 라이선스로, 비영리 목적의 재이용이 허락되어 있습니다. 재이용 시 라이선스 표시를 기재하고, 참고 논문 인용은 권말 Reference에 게재해 주세요. 상세한 조건은 원문 링크를 확인해 주세요.

이번 시간은 개별 기술을 깊이 파고들기보다 전체 개요를 파악하는 것이 목적입니다. 많은 용어가 등장하지만, 모두 이번 회에 외워야 하는 것은 아닙니다. 강의는 이와사와 유스케(岩澤有祐) 준교수가 LLM 개황과 강좌 전체 개요를 맡고, 고지마 타케시(小島武) 특임조교가 각 회차와 일본의 LLM 환경을 맡습니다.

이와사와 유스케는 2017년 마츠오 연구실에서 박사과정을 수료한 뒤 특임연구원·특임조교를 거쳐 2024년 1월부터 기술경영전략학 전공 준교수를 맡고 있습니다. 석사까지는 장애인 지원을 위한 머신러닝 응용을, 박사부터는 딥러닝 전이학습을 연구했습니다. 생성AI 분야에서는 "Large-Language Models are Zero-Shot Reasoners"(NeurIPS 2022)를 비롯해, LLM 강좌 전체 설계, 기시다 총리 등에 대한 LLM 특강, DL 독서회 주관(2015년~ 누적 350회 이상), Goodfellow 딥러닝 교과서 감역·번역(2018) 등의 활동을 해왔습니다.

고지마 타케시는 2023년 도쿄대학교 TMI 박사과정을 수료하고 동 연구과 특임조교를 맡고 있으며, 이전에는 IT 엔지니어 출신입니다. Weblab-10B 개발, 기시다·이시바 총리 LLM 특강 강사, LLM 개발 콘테스트 2024·2025 운영, AI 백서 2025 Safety 장 집필을 담당했고, 연구 테마는 LLM 동작 원리 이해와 제어(Reasoning Model, 다언어), Safety(Unlearning, 지시 추종 능력, 로봇), 트랜스포머 구조 개선입니다.

오늘 다룰 내용은 세 축입니다. 첫째, LLM 개요, 즉 왜 지금 LLM을 배워야 하는가. 둘째, 이번 강좌 각 회차의 개요. 셋째, 일본의 LLM을 둘러싼 환경.

---

## 언어 모델이란 무엇인가

지금 자연어를 다루는 어시스턴트 AI를 만들고 싶다고 가정해 봅시다. 질문에 올바른 답을 출력해 주길 원하고("일본의 수도는?" → "도쿄"), "글을 영어로 번역해 줘"라는 요청에는 번역문을, "테트리스 앱을 만들어 줘"라는 요청에는 코드를 생성해 주길 원합니다. 오늘날 이런 기능들은 웹상이나 간단한 프로그램으로 실현되고 있으며, Hugging Face에는 언어·이미지·음성·멀티모달 등 100만 개를 넘는 모델이 공개되어 있습니다.



![수식](eq-svg/eq-0de59347c9.svg)



```


![수식](eq-svg/eq-a0bd4f169b.svg)




![수식](eq-svg/eq-86a74c5a4c.svg)




![수식](eq-svg/eq-944ca7a819.svg)


```

다양한 언어 과업 — QA, 번역, 코드 생성 — 이 모두 이 생성 확률의 추정 문제로 다루어질 수 있으며, 이 생성 확률을 어떻게 구하는가가 언어 모델의 핵심 기술적 문제입니다.

가장 널리 쓰이는 접근이 자기회귀 언어 모델(Autoregressive Language Model)로, 확률의 연쇄 법칙에 따라 결합 확률을 조건부 분포의 곱으로 분해합니다.

```


![수식](eq-svg/eq-67444e169f.svg)


```

조건부 확률을 알면 생성도 가능합니다. 예컨대 "일본의 수도는 → 도쿄"라는 접속에서 조건부 확률이 다음 단어를 고릅니다.

```


![수식](eq-svg/eq-7cfd09212c.svg)




![수식](eq-svg/eq-856427f869.svg)




![수식](eq-svg/eq-96d11618f0.svg)


```

신경망 언어 모델(Neural Language Model)은 이 조건부 확률을 신경망으로 추정한 모델로, 웹 데이터를 모의하도록(가능도를 최대화하도록) 학습합니다.

트랜스포머 이전의 신경망 언어 모델에는 두 가지 과제가 있었습니다. 합성곱 신경망이나 MLP에서는 긴 문맥 처리가 어려웠고(번역처럼 원문을 충실히 반영해야 하는 과업에서 치명적입니다), RNN 계열은 데이터를 순차 처리하는 탓에 학습·추론의 병렬화가 안 되어 스케일업이 곤란하고 기울기 소실 문제까지 겹쳤습니다.

이를 해결한 것이 2017년 Vaswani 등의 "Attention is All You Need"(NeurIPS 2017)가 제안한 트랜스포머(Transformer)입니다 [1]. Google 중심의 연구팀이 발표한 이 구조는 Self-Attention을 핵심으로 삼아, 번역 등 지도학습에서 성능이 검증되었습니다(영어 문장 → 트랜스포머 → 독일어 문장이 되도록 오차 역전파로 학습). 구조의 상세는 별도 일정에서 다룹니다.

트랜스포머를 언어 모델의 사전학습에 본격 적용한 것이 OpenAI의 GPT(Generative Pretraining Transformer)입니다. Radford 등이 2018년에 발표한 GPT는 [2], 다음에 올 단어를 트랜스포머로 예측하도록 Book Corpus라는 미공간 서적 데이터로 학습했으며, 이후 GPT, GPT-2, GPT-3로 버전을 거듭하며 학습 데이터 수와 모델 크기를 증가시켜 왔습니다.

---

## 대규모 언어 모델의 발전과 2025년 현황

GPT-3가 등장한 2020년 이후, 대규모 모델의 발표는 가속적으로 증가했습니다 [3]. OpenAI는 2023년 GPT-4를 발표합니다. 상세는 미공개이나 누출 정보는 있고, 사법시험이나 SAT/GRE 등 다양한 시험에서 좋은 성적을 거두었습니다. 예컨대 Uniform Bar Exam에서 298/400(약 90백분위), GRE Quantitative 163/179(약 80백분위)이며, 한편 코딩 능력 등에서는 아직 낮은 점수를 받았습니다(현재는 대폭 개선됨) [4].

일본어 평가 사례도 있습니다. Kasai 등(2023)은 GPT-4와 ChatGPT를 일본 의료 면허 시험 6년 분량의 새 데이터셋 Igaku-QA로 벤치마크했습니다. 인간 평균 응시자보다는 나쁘고 금기술을 선택하는 경향이 있는 등의 문제는 있으나, 시험 합격선은 돌파했습니다 [5].

모델 자체의 발전뿐 아니라 활용 기술도 진전했습니다. "A Survey of Context Engineering for Large Language Models"(2025)이 정리하듯, 언어 모델이 가진 지식을 사용할 뿐만 아니라 필요한 컨텍스트를 선택하고 처리하는 기술 — RAG, 도구 이용(검색), Deep Research, Memory 등 — 이 활발히 연구되고 있습니다.

2025년 한 해에만 표에 정리한 수십 개의 유력 모델이 등장했습니다.

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

세 가지 흐름이 두드러집니다. 첫째, 추론(Reasoning) 모델이라 불리는, 기존보다 추론 능력이 현저히 높은 모델의 등장입니다. 스스로 오류를 깨닫는 "Aha Moment"가 보고되면서, 기존보다 복잡한 벤치마크 정비와 추론 프로세스 분석이 진전하고 있습니다. 둘째, 성능이 높은 공개 모델의 증가입니다. 셋째, 확산 언어 모델 등 다양한 의미에서 효율이 좋은 모델 구조의 모색입니다.

이에 맞춰 평가도 고도화되고 있습니다. **SWE Bench**는 이슈에 대한 PR 작성 능력을 평가하고, **Humanity's Last Exam**은 등장 시점 SoTA 9%(현재 21.6%) 수준의 챌린징한 문제로 모델의 한계를 측정합니다. 문제 예시를 하나 옮기면 이렇습니다.

> "칼새목의 벌새는 꼬리 깃털 하제근(下制筋)의 퍼진 교차상 건막(腱膜)의 미측 외측 부분에 매립된, 좌우 한 쌍의 타원형 종자골(種子骨)을 가진다. 이 종자골에 의해 지지되는 건 쌍은 몇 개인가? 숫자로 답하시오."

---

## 스케일이 가져온 범용성 — 왜 지금 언어 모델인가

지금까지를 한 줄로 정리하면: 언어 모델이란 단어열의 생성 확률을 모델화한 것(자기회귀·신경망·GPT)이며, 2025년이 된 지금도 활용 방법, 모델 자체(대규모 추론 모델, 확산 언어 모델), 평가 방법에 대한 연구개발은 진전 중입니다. 원리는 매우 심플합니다. 그렇다면 왜 지금 언어 모델인가? 두 가지 이유가 있습니다. 하나는 대규모화에 수반하는 범용성, 다른 하나는 언어 이외의 도메인에 대한 영향입니다.

어느 모델이든 기본적으로 2017년에 발명된 트랜스포머라는 구조를 이용합니다. 2018년 OpenAI의 GPT-1, 2019년·2020년 GPT-3, 2023년으로 이어지며 시기별로 스케일이 커졌고, GPT-3 등장 이후 미국 기업을 중심으로 복수의 연구기관이 독자적인 대규모 언어 모델을 개발했습니다 [6]. 핵심은 스케일링 법칙(Scaling Law)과 창발 능력(Emergent Ability)입니다.

**스케일링 법칙**이란, 계산 자원 C, 데이터셋 크기 D, 파라미터 수 N이라는 세 변수에 대한 거듭제곱에 따라 사전학습 성능이 올라간다는 경험칙입니다 [7]. **창발 능력**이란, 모델 크기가 거대할 때만 풀 수 있는 과업이 존재한다는 현상입니다 [8]. 보다 큰 파라미터의 트랜스포머로 보다 대규모 데이터를 이용한 사전학습을 진행하는 과정에서 스케일 법칙이 발견되었고, 자원을 투하할수록 고성능 LLM을 만들 수 있다는 사실이 밝혀진 것은 크게 흐름이 바뀐 순간이었습니다. OpenAI는 일찍이 스케일 법칙에 주목하여 대규모 개발을 시작했고, 그 후 세계적인 투자 경쟁이 시작되었습니다.

스케일의 체감을 학습 데이터량으로 보면, GPT-3는 약 5,000억 토큰의 텍스트를 이용했습니다(토큰이란 언어 AI가 처리하는 단위로, 일본어의 경우 대략 1글자 1토큰) [9]. 책으로 치면 약 500만 권에 상당합니다. 참고로 도쿄대 도서관이 약 130만 권, 국회도서관이 약 4,700만 권이며, 누출 정보에 따르면 GPT-4는 약 1.3억 권에 해당합니다.

이런 대규모 학습을 지탱하는 것이 GPU라 불리는 대규모 연산 자원입니다. 현재 주된 연산 자원은 GPU이며, 지배적 점유율(세계 약 90%)을 가진 NVIDIA가 급성장해 일시적으로 세계 시가총액 1위에 올랐습니다. 학습에 필요한 GPU 수를 짚으면, GPT-3 상당은 A100 1,200대로 약 30일, GPT-4 상당(*누출 정보)은 A100 25,000대로 약 100일이 걸리고, 이번 강의 연습은 A100 8대로 1시간 수준입니다.

글로벌 GPU 클러스터 규모에서 격차는 더 벌어집니다. 2024년 단년도 구매 수 기준으로 Microsoft 485,000대, Meta 224,000대, Amazon 196,000대, Google 169,000대 등 단일 기업이 수십만~백만 기의 H100급 GPU를 보유합니다. 이에 비해 일본은 산업기술종합연구소 ABCI의 6,128대 H200(2025년 1월 업그레이드), SoftBank 약 6,000대, 사쿠라 인터넷 2,000대 H100 수준입니다 [10]. 이 격차는 근본적으로 IT 서비스와 생성AI 사이에 선순환이 만들어지고 있는가라는 구조적 문제에서 비롯됩니다.

이런 스케일이 가져온 가장 큰 결실은 범용성입니다. Brown 등(2020)이 보인 대로 [9], 사전학습을 마친 트랜스포머 하나로 번역(Zero-shot, Few-shot), 요약("TL;DR"로 시작하면 성능이 대폭 향상됨) 등 다양한 과업이 소수 예시나 지시만으로 가능해졌습니다. 이것이 "파운데이션 모델"이라는 개념으로 정식화됩니다. 2021년 8월 Stanford의 백서 "On the Opportunities and Risks of Foundation Models"에서 초출된 이 용어는 [11], 광범위한 데이터를 대규모로 학습하고 다양한 다운스트림 과업에 적응할 수 있는 모델(BERT, DALL-E, GPT-3 등)을 가리킵니다. 초록은 이 모델들이 "임계적으로 핵심적이면서도 미완성" — 즉 중심적이 되면서도 위험과 한계를 안고 있음 — 이라는 성격을 강조합니다.

---

## 언어를 넘어선 파운데이션 모델 — 멀티모달과 로봇

두 번째 이유, 즉 언어 이외의 도메인에 대한 영향을 살펴봅시다. GPT-4는 텍스트뿐 아니라 이미지 인식 능력을 갖추고 있으며 [4][13], 이는 로봇 응용으로까지 이어집니다.

로봇 분야에서는 언어 모델을 어떻게 '행동'으로 이어붙일까가 과제입니다. Ahn 등(2022)의 Say-Can(Say-Can-PaLM)은 [14], 언어 모델이 출력한 스킬의 실행 가능성(Skill Affordance)을 고려해 스킬을 선택합니다. 실행 가능성은 TD(강화학습)로 학습하며, 언어 모델을 개선하면(PaLM 사용) 성능이 향상됩니다(다만 실행 가능한 저수준 정책은 사전에 준비되어 있다는 점에 주의). 마츠오 연구실의 행동 계열 생성 연구도 이 흐름에 있으며, RoboCup Japan Open 2023 우승, RoboCup 세계대회 3위 등의 성과를 거두었습니다.

$$더 나아가 '로보틱스 파운데이션 모델'이 등장했습니다. 실제 세계 환경의 action/observation 쌍을 대규모·다양한 데이터로 학습해 산업 응용, 자율주행, 생활 지원 등에 활용하는 모델입니다. 구글의 RT-1(2022)은 EfficientNet과 트랜스포머의 조합으로 인스트럭션에 따라 동작을 생성하며 [15], 13대의 로봇으로 17개월간 744 과업, 13만 데모를 수집해 학습했습니다. 학습 데이터에 대해서는 97%에서 동작하고, 미지 과업·미지 소스 등 다양한 의미에서 일반화가 대폭 향상되며 Long Horizon 과업도 가능합니다(유사 연구로 Gato, BC-Z 등). RT-X 프로젝트는 이 방향을 더 확장해 [16], Google DeepMind 및 21개 연구기관이 통일된 포맷의 오프라인 로봇 데이터셋을 수집했습니다 — 22가지 로봇 타입, 527개 스킬(160,266 과업), 100만 에피소드 이상을 확보해 개별 데이터로 학습한 모델보다 더 나은 성능을 보이며 ICRA 2024 최우수 논문상을 수상했습니다. 최근의 비전-언어-액션(Vision-Language-Action, VLA) 모델인 π0 [17]은 세탁물을 개거나 달걀을 깨지 않게 케이스에 넣는 등 다양한 과업을 수행하고, 일본의 AIRoA(AI Robot Association)는 학계 주도·개방성·보상 설계를 특징으로 삼습니다$$

언어를 넘어선 확장은 비디오 생성에까지 닿습니다. OpenAI의 Sora는 텍스트 프롬프트에서 사진 풍질의 영상을 생성하며 [18][19], "비디오 생성 모델을 세계 시뮬레이터로 본다"는 관점까지 제시합니다.

지금까지의 정리를 종합하면: 언어 모델이란 단어열의 생성 확률을 모델화한 것이며, 2025년이 된 지금도 활용 방법·모델 자체(대규모 추론 모델, 확산 언어 모델)·평가 방법에 대한 연구개발은 진행 중이고, 원리는 매우 심플합니다. 왜 지금 언어 모델인가? (1) 모델·데이터·계산량의 스케일에 의해 할 수 있는 것이 급속히 넓어지고 있고(일반화성), (2) 언어 모델의 발전이 다른 영역에도 영향을 주고 있습니다. 본 강좌는 이 LLM의 기술적 배경, 원리와 한계를 이해하고, 히프(Hype)가 아닌 활용 기술로서 파악하는 것을 취지로 합니다.

---

## 강좌 구성과 학습 파이프라인

올해 강좌는 '대규모 언어 모델 기초'와 '대규모 언어 모델 응용'으로 나뉩니다. **기초편(10~11월)**은 LLM의 전체상을 이해하기 위해 사전학습·사후학습·데이터 수집 가공·벤치마크 평가 등 학습 파이프라인을 망라적으로 해설하고, 공개 모델이나 API로 추론 성능을 끌어올리는 기법도 소개합니다. **응용편(12월~2월)**은 경량화·안전 대책·해석성·도메인 특화·LLM 에이전트 등 사회 구현에 불가결한 기술을 본격적으로 다루고, 최전선 연구자의 특별 강연과 '개인형 LLM 개발 콘테스트'가 진행됩니다.

학습 파이프라인은 여섯 단계로 정리됩니다 [22]. **Step 1. 사전학습**은 대규모 코퍼스에 의한 자기지도학습을 통해 언어 모델에 어휘·문법·지식 등 기본적인 언어 이해를 획득시키는 단계입니다. **Step 2. 파인튜닝**은 라벨링된 데이터에 의한 지도학습을 통해 성능을 개선하거나 특정 과업·도메인에 대한 적응을 실현합니다. **Step 3. 강화학습**은 (인간의) 피드백을 이용한 강화학습을 통해 출력이 인간의 가치관에 보다 부합하도록 조정합니다(Step 2~3을 묶어 "사후학습"이라 부릅니다). **Step 4. 데이터 수집·가공**은 사전학습이나 사후학습에 사용할 학습 데이터를 수집·가공하며, 최근에는 LLM 자체를 이용한 데이터 합성도 성행합니다. **Step 5. 추론**은 학습 완료 모델에 프롬프팅을 구사하여 추가로 성능을 향상시킵니다. **Step 6. 벤치마크 평가**는 학습에 사용되지 않은 샘플로 구성된 벤치마크로 성능을 평가합니다. 기초편의 각 회차는 이 파이프라인에 매핑됩니다: Day 2(추론) / Day 3~5(사전학습) / Day 6(파인튜닝) / Day 7(강화학습) / Day 8(데이터·벤치마크).

### 제2회 추론: Prompting, In-context Learning

학습 완료 후 LLM의 성능을 끌어내는 활용법을 배웁니다 [9][23]. Zero-Shot·Few-Shot 프롬프팅을 시작으로, 다단계 추론이 필요한 과업에서는 사고의 연쇄(Chain-of-Thought)를 예시로 제공하는 CoT prompting이 유효합니다 [24]. 나아가 예시 없이 모델 스스로 생각하게 하는 Zero-shot CoT("Let's think step by step.")도 제안되었습니다 [25](공동 저자 Shane Gu가 최근 "Video Models are zero-shot learners and reasoners"를 발표한 점도 참고 [26]). CoT를 전제로 한 추가 개선으로는 top-k/top-p 샘플링으로 복수 답안을 얻어 다수결을 취하는 Self-Consistency [27], 성공·실패 궤적 데이터를 기반으로 언어 피드백으로 프롬프트를 개선하거나 다른 유력 후보와 조합하는 GEPA(Genetic-Pareto)가 있습니다(다양성 확보를 위해 1문제에서만 가장 좋은 점수를 낸 프롬프트도 후보에 포함) [28].

### 제3회 사전학습: 트랜스포머와 학습 원리

LLM의 주류 모델 구조인 트랜스포머와 그 사전학습 메커니즘(Embedding, Multi-Head Attention, Feed Forward 등)을 배웁니다 [1]. 핵심인 어텐션(attention) 기구는 모든 단어(토큰) 간의 유사도를 벡터의 내적으로 측정하여 장거리 의존 관계를 파악하는 메커니즘으로, 필요한 토큰의 정보를 유연하게 취사선택하면서 병렬 계산의 고속화를 이룹니다 [29]. 어텐션 시각화 예에서는 "it"이 "The", "animal"에 강한 어텐션이 걸려 있음을 볼 수 있는데 [30], 명시적으로 가르치지 않았는데도 사전학습 과정에서 모델 스스로 이 관계성을 도출합니다(실제로는 이렇게까지 명확하지는 않음). 트랜스포머 구조는 크게 세 종류로 분류됩니다 — Encoder-only(BERT, RoBERTa 등, 인식 계열·클래스 분류), Encoder-Decoder(BART, T5 등, 생성 계열), Decoder-only(GPT, Llama, Qwen, DeepSeek 등, 생성 계열).

LLM의 큰 특징은 번역·요약·채팅 등 다양한 언어 과업에 대한 범용성입니다. 대량의 텍스트에서 세계의 지식을 사전학습해 범용성을 획득하고, 사후학습으로 특정 기능이나 전문 분야에 특화합니다. 범용 모델 하나만 있으면 번역 앱, 의사록 요약 앱, 채팅 봇 등 다양한 기능을 개발할 수 있습니다. 학습 원리는 단순합니다. 웹에서 수집한 대량의 글로 다음 단어 예측을 쉬지 않고 수행하며, 그 과정에서 읽기·쓰기·셈하기와 세계 지식을 학습합니다. 예컨대 "봄은 벚꽃이 예쁘다"라는 텍스트로 "봄", "벚꽃", "예쁘다" 사이의 강한 관계성(=세계 지식)을 학습하고, 예측과 정답의 교차 엔트로피가 작아지도록 모델을 갱신합니다(P(는|봄), P(벚꽃|봄, 는), P(가|…), P(예쁘다|…) 등).

### 제4회 스케일 법칙: 자원이 성능을 좌우한다

스케일 법칙(Scaling Law)이란 계산 자원, 학습 데이터량, 파라미터 수의 증가에 비례하여 사전학습 성능이 오른다는 경험칙입니다 [31]. 보다 큰 파라미터 크기의 트랜스포머로 보다 대규모 데이터를 이용한 사전학습 과정에서 발견되었고, 자원을 투하할수록 고성능 LLM을 만들 수 있다는 것이 밝혀진 것은 크게 흐름이 바뀐 순간이었습니다. OpenAI는 일찍이 스케일 법칙에 주목하여 대규모 개발을 시작했고, 그 후 세계적인 투자 경쟁이 시작되었습니다. 이미지 생성·멀티모달·동영상·수리 등에서도 계산량에 관한 스케일 법칙이 성립합니다.

스케일 법칙에 기초하면 LLM 성능을 좌우하는 세 가지 자원 — ① 대규모 연산 자원, ② 대규모 데이터, ③ 우수한 인재 — 이 도출됩니다. ② 대규모 데이터를 모으기 위해서는 저작권·개인정보 등 취급 방침의 정비가 필요하고(법 정비의 중요성), ③ 우수한 인재는 트랜스포머나 학습 기법의 개발, 하이퍼파라미터 조정 등에 필요하며(인적 자본 투자의 중요성), ① 대규모 연산 자원은 GPU라 불리는 학습용 서버 확보로 이어집니다(하드웨어 투자의 중요성). 거대한 파라미터의 모델은 사람이 연산 자원·데이터를 사용하고 하이퍼파라미터 조정과 시행착오를 반복하여 만드는 것입니다. 최근에는 사전학습의 스케일 법칙뿐 아니라 사후학습과 추론의 스케일 법칙에 대한 연구도 성행하고 있습니다 [32].

### 제5회 사전학습(상신편): 대규모화의 과제와 해법

언어 모델을 스케일(=대규모화)하여 사전학습할 때의 과제와 해결 방법을 배웁니다 [7]. 세 축이 있습니다 — 충분한 계산량(C)·메모리량 확보, 모델이 스케일함에 따른 비용 억제(파라미터 수 N), 성능 발휘를 위한 학습용 데이터(D). Sparse Transformer는 Attention을 계산하는 부분을 한정(계산하지 않는 부분은 마스크)해 계산량을 삭감하며, 이미지·음성 모달리티에서도 트랜스포머 이용을 가능하게 합니다 [33](2회 통과로 모든 토큰에 어텐션이 도달 [34]). Switch Transformer는 1조 6,000억 파라미터의 MoE(Mixture of Experts) 모델로, 피드포워드 네트워크를 복수 엑스퍼트화해 데이터에 따라 엑스퍼트를 선택합니다 [35]. LLM.int8()은 성능 열화 없이 가능한 양자화(Quantization) 방법으로, 은닉 상태에서 열 단위로 이상치를 추출해 이상치 행렬은 FP16 그대로, 이상치가 아닌 행렬은 INT8로 변환하여 연산한 뒤 가산해 반환합니다 [36]. 멀티 노드·멀티 GPU를 이용한 대규모 분산 학습(DeepSpeed 등 [37])도 핵심 기반입니다.

### 제6회 파인튜닝: 사전학습 이후의 학습

사전학습 완료 후에 수행하는 추가 학습 = 파인튜닝에 대해 배웁니다. 인간과 대화할 수 있도록 QA 데이터·채팅 데이터로 학습하며, 사전학습과 마찬가지로 다음 단어를 쉬지 않고 예측하는 학습 기법입니다. 예시로는 "Q: 일본에서 가장 높은 산은? / A: 후지산", "Q: 건강 유지를 위한 3가지 팁을 알려주세요 / A: 1. 균형 잡힌 식사를 하고 야채와 과일을 충분히 섭취할 것 …", "Q: 메리는 20분에 8페이지의 책을 읽을 수 있습니다. 120페이지를 읽는 데 몇 시간 걸립니까? / A: 1시간에 8×3=24페이지 읽을 수 있으므로 120/24=5시간" 등이 있습니다. Zero-shot으로 범용적으로 모든 지시에 따르도록 하는 인스트럭션 튜닝 [38], 소수 파라미터에 의한 효율적 학습 방법인 LoRA(Low-Rank Adaptation) [39]가 핵심 기법입니다.

### 제7회 강화학습: 인간 가치관에의 정렬

LLM에서의 강화학습이란 무엇인지, 그 메커니즘과 필요성에 대해 이해합니다. **RLHF**(Reinforcement Learning from Human Feedback)는 인간의 가치관(예: 유해한 말을 하지 않기를 바람)에 부합하도록 LLM 출력을 인간 피드백으로 개선하는 방향으로 학습하며, 지도학습에 비하면 상당히 정보량이 적은 신호로 학습합니다. 예컨대 사용자가 "절도를 하는 방법을 가르쳐 줘"라고 했을 때, × 나쁜 예("절도를 하려면 상대에게 들키지 않게 다가가 소지품을 빼앗는 것이 중요합니다…")와 △ 중간("절도는 좋지 않습니다."), ○ 좋은 예("절도는 범죄이므로 그것을 행하는 것을 강하게 권하지 않습니다.") 사이를 good/bad 피드백 신호로 구분합니다. 이후 보상 모델 구축이 필요 없는 DPO(Direct Preference Optimization) [40], DeepSeek가 제안한 GRPO [41]로 이어지고, 강화학습 결과로 자연 창발한 "Aha Moment"(Self-revision) [73]과 장고(더 많은 토큰 길이로 사고할수록 더 좋은 답에 도달)의 효과가 보고됩니다.

### 제8회 학습 데이터와 평가 벤치마크 정비

LLM 개발의 전체 파이프라인을 이해·구현할 수 있게 되는 것을 목적으로, 학습 데이터와 평가 벤치마크에 대해 상세히 해설합니다. 데이터의 전처리(필터링 등), LLM을 이용한 데이터 합성, LLM-as-Judge, 평가 벤치마크의 진전 등을 다룹니다.

---

## 일본의 LLM 생태계

2018년 OpenAI의 GPT-1 등장 이후, LLM의 파라미터 크기는 스케일 법칙에 따라 비약적으로 증대했습니다 [3]. 일본에서는 2023년부터 개발 경쟁이 본격 가속했습니다(2023년 이전에도 rinna, ABEJA, RICOH 등이 개발하고 있었음). 2023.3 OpenAI가 GPT-4를 공개한 뒤, 같은 해 5월 사이버에이전트 OpenCALM(7B), rinna의 일본어 특화 GPT(3.6B); 7월 NEC의 일본어 LLM(13B, 비공개); 8월 Stability AI Japanese StableLM Alpha(7B), LINE 일본어 LLM(3.6B), 도쿄대학교 마츠오 연구실 Weblab-10B(10B), ELYZA-japanese-Llama(7B)가 잇따랐습니다 [42]~[48]. 2023년 하반기~2024년에는 PFN PLaMo-13B, rinna Youri(7B), NTT tsuzumi(7B), 도쿄공대 Swallow(70B), ELYZA-japanese-Llama-2(70B), 라쿠텐 Rakuten AI(7B), NEC cotomi Pro/Light, LLM-jp-13B, Fujitsu Fugaku-LLM(13B), Stockmark-LLM-100b(100B), SB Intuitions Sarashina1-65B, PFN PLaMo-100B, CyberAgent CALM3(22B), 도쿄공대 Llama-3-Swallow(70B), Sarashina2-70B, 마츠오·이와사와 연구실 Geniac 기획 tanuki-8x8b(47B) 등 수십억~수백억 파라미터 모델이 쏟아졌습니다 [49]~[63].

2024년 말~2025년에는 더 큰 규모와 더 작은 규모가 공존합니다. PLaMo-10x100B(1T), llm-jp-3-172b(172B), Sarashina2-8x70B(465B) 같은 초대형 모델이 나오는가 하면 [64], CA DeepSeek-R1-Distill-Qwen-32B-Japanese(32B), Stockmark-2-100B-Instruct-beta(100B), Llama 3.3 Swallow 70B, ELYZA-Thinking-1.0-Qwen-32B, ABEJA-Qwen2.5-32b-Japanese-v1.0(이상 32B) 등 특화·추론 지향 모델도 등장했습니다. 최근에는 수B 정도의 경량 언어 모델(Small Language Model: SLM)을 개발하는 조직도 증가 추세입니다 — Rakuten AI 2.0 mini(1.5B), PLaMo 2 8B·PLaMo 2.1 2B(2B), Sarashina2.2(0.5~3B), Llama 3.1 Swallow 8B(8B) 등. 배경은 두 가지입니다. (1) 작은 모델이라도 더 많은 데이터로 더 오래 학습하면 높은 성능을 달성할 수 있다는 점(스케일 법칙적으로 학습 효율은 나쁘더라도), (2) 학습 완료 후의 추론 비용(운용 비용)까지 고려하면 작은 모델의 비용 대비 효과가 높다는 점입니다.

"Go smol or go home" 논의에서 지적되는 **Chinchilla Trap**이란, Chinchilla 수준(70B) 모델은 크기 때문에 추론 비용이 높으므로 추론 비용까지 고려해 더 작은 모델을 장시간 학습해야 한다는 지적입니다. 최적 모델 크기의 40~60% 이내 모델을 선택해 10~42% 계산량 추가로 동일 성능 모델을 학습할 수 있다는 분석도 있습니다.

일본 발 모델은 대략 두 갈래로 분류됩니다. 첫째, **사전학습부터 시작하는 풀스크래치 개발**입니다. 학습을 완전히 제어할 수 있고 라이선스도 독자적으로 결정할 수 있지만 학습 비용이 높고 기술적 난이도도 높습니다. 대표 모델로 CALM3-22B, Weblab-10B, PLaMo-100B, LLM-jp-13B, Sarashina2-70B, tanuki-8x8b 등이 있습니다. 둘째, **사전학습 완료 영어 모델을 일본어로 지속 사전학습하여 개발**하는 방식입니다. 학습 비용이 낮고 언어 간 지식 전이에 의한 효율적 학습이 기대되지만, 학습 방식에 제한이 발생하고 라이선스 제약이 있을 수 있습니다. 대표 모델로 ELYZA-japanese-Llama-70B, Swallow-70B, Llama-3-Swallow-70B 등이 있으며, 이용하는 사전학습 완료 모델은 성능이 높은 모델이 선택되는 경향으로 Llama 기반이 많습니다.

마츠오·이와사와 연구실은 경산성·NEDO의 'GENIAC' 프로젝트에서 Tanuki 모델을 개발했습니다 [63]. "해외 모델은 어느 쪽인가 하면 무기질적이고 형식적인 답변을 하는 경향이 있습니다만, 그와 대조적으로 당해 모델은 공감성이나 배려가 있는 답변이나, 자연스러운 말투로의 작문이 뛰어났습니다"라는 평가를 받습니다. 「Tanuki-8×8B」의 경량판인 「Tanuki-8B」를 채팅 형식으로 이용할 수 있는 데모도 공개되어 있습니다 [65].

연산 환경은 여전히 엄격합니다. 학습에 필요한 GPU 수는 GPT-3 상당이 A100 1,200대×30일, GPT-4 상당(*누출 정보)이 A100 25,000대×100일에 달합니다. 일본 국내 대표 GPU 클러스터는 산업기술종합연구소 ABCI의 960대 A100 → 6,128대 H200(2025년 1월 업그레이드), SoftBank 약 6,000대, 사쿠라 인터넷 2,000대 H100 수준이고 [66], 해외(단일 기업이 수십만~백만 기의 H100 보유, 24년 단년도 구매 수: Google 169,000대, Amazon 196,000대, Meta 224,000대, Microsoft 485,000대)와 큰 격차가 있습니다. 다만 GPU는 고속으로 세대 교체를 거듭해(P100 → V100 → A100 → H100 → B100) 후속 세대일수록 계산 속도가 빠르고 비용도 낮아, 일본에는 후발의 이점이 있을지도 모릅니다 [67].

학습 데이터, 특히 사전학습용 일본어 데이터는 범용성과 고성능의 원천입니다. 인터넷에서 수집한 대량의 텍스트를 사용하지만 [68], 그 대부분은 영어 등 주요 언어로 구성되어 있어, 일본어 등의 텍스트를 대량 수집하는 것은 현재 한계가 있습니다. 데이터 원천은 어느 쪽이든 "Common Crawl"(https://commoncrawl.org/, 인터넷 사이트 크롤링 아카이브)이며, Wikipedia(ja) 덤프도 자주 사용됩니다 [69]. 개산으로 상기 합계 약 1.3TB, 1토큰 2문자 ≒ 4바이트로 하면 약 0.3T 토큰으로, Llama 2의 2T 토큰, GPT-4의 13T 토큰(누출 정보)과 비교하면 상당한 격차가 있습니다. 이를 보완하기 위해 LLM-jp 코퍼스는 일본어 6,880억 토큰을 확보했습니다 — 구성 데이터는 청공문고 텍스트, Common Crawl에서 추출·필터링한 일본어 코퍼스, e-Gov 법령, FineWeb 2 일본어 부분, 과학연구비 조성사업 데이터베이스 개요, 국회 회의록, 특허청 공개 데이터의 일본어 특허, 국립국회도서관 WARP URL에서 크롤한 텍스트, 일본어 Wikipedia 등입니다 [70].

학습 데이터 수집 시에는 세 가지에 주의해야 합니다. **저작권**은 저작권법(30조의4 제2호에서 AI 학습 데이터를 규정)에 의해 위반 시 저작권 침해(형사벌)에 해당하며, 일본은 구미에 비해 모델 학습에 이용 가능한 데이터의 자유도가 높다고 알려져 있습니다. **라이선스/이용 약관**은 작성자와 이용자 간의 계약으로 위반 시 손해 배상 문제가 발생할 수 있습니다. **개인정보**는 개인정보보호위원회가 생성AI 서비스 이용에 관한 주의 환기 등을 안내하며 [71], 상세는 법률 사무소에 상담할 것을 권합니다. 보충으로, 웹 크롤 시에는 robots.txt(RFC 9309)의 내용에 따를 필요가 있으며 따르지 않을 경우 저작권 침해에 해당할 가능성이 있습니다(The New York Times가 자사 기사 웹사이트의 robots.txt에서 AI 학습용 크롤러를 차단하고 별도 라이선스·API를 판매하는 사례가 있습니다). 이용 약관 예시로는 ChatGPT(OpenAI)의 약관이 자주 인용됩니다 [72].

라이선스 종류도 이해가 필요합니다. OSS, CC 라이선스는 비교적 자유도가 높은 라이선스이지만 다양한 종류가 있으므로 각각 이해가 필요합니다.

**Creative Commons (CC) 라이선스:**

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

**OSS(Open Source Software) 라이선스:**

| 라이선스 | 특징 | 재배포 시 의무 |
|----------|------|----------------|
| MIT License | 저작권 표시와 라이선스 문구를 남기면 사용 가능 | 저작권 표시와 라이선스 문구 기재 |
| Apache License 2.0 | MIT보다 약간 엄격. 특허 권리도 커버 | 저작권 표시, 라이선스 문구, 변경점 명시 |
| GPL (GNU General Public License) | 강한 카피레프트. 개변·재배포하면 같은 GPL 라이선스로 공개 필수 | 소스 공개 + GPL 계승 |
| LGPL (Lesser GPL) | 라이브러리로서의 이용은 가능, 본체에는 강제하지 않음 | 개변 시에만 소스 공개 의무 |
| BSD License | MIT과 거의 동일. 상업 이용 가능. 선전 금지 조항이 있는 경우도 있음 | 저작권 표시와 면책 사항 기재 |

> Meta Llama 3 License: Meta가 독자적으로 정하는 라이선스입니다. 월간 액티브 사용자 7억 명 이상의 기업에는 별도 라이선스 계약이 필요하므로, OSS 라이선스는 아닙니다.

---

## 맺음말

대규모 언어 모델(LLM)의 개요를 세 축에서 소개했습니다.

첫째, **LLM 개황**. 언어 모델이란 단어열의 생성 확률을 모델화한 것이며, "왜 지금 언어 모델인가"에 대한 답은 스케일과 범용성(Agent 등), 그리고 다른 영역으로의 영향(멀티모달·로봇)에서 찾을 수 있습니다.

둘째, **LLM 강좌 각 회차 개요**. 기초편에서 LLM 개발의 기본 파이프라인을 이해하고 구현하며, 응용편에서 LLM 사회 구현까지를 고려한 기술을 이해하고 구현합니다.

셋째, **일본의 LLM을 둘러싼 환경**. 2023년 이후 본격적으로 개발 경쟁이 가속했고, 데이터·모델·연산 환경을 스케일할 수 있는가가 관건입니다.

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