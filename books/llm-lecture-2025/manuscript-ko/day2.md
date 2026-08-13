# 제2회: 추론 — 프롬프팅과 문맥 내 학습

> 본 한국어 역문은 교육 목적의 번역이며, 원본 라이선스(CC BY-NC-ND 4.0)를 따릅니다. 원자료는 도쿄대학교 마츠오·이와사와 연구실이 작성한 「대규모 언어 모델 강좌 2025」 기초편(2025년 10–11월 개최) 제2회 강의 자료로, CC BY-NC-SA 4.0으로 등록되어 있습니다. 비영리 목적의 2차 이용이 허락되며, 영리 목적은 별도 문의가 필요합니다. 재이용 시 본 라이선스 표기를 기재해 주세요. 원문의 의미를 변경하거나 추가하지 않았습니다.

---

## 도입: LLM 시대의 활용과 본 강의의 목표

강사 원다 켄노우(原田憲旺)는 마츠오·이와사와 연구실 박사과정 3년 차로, LLM 강좌 자료 제작·콘테스트 제작, GENIAC 평가, AI 백서 2025 생성AI 에디션 집필 협력, DeepLearning.ai 생성AI 강의 번역, 기시다·이시바 총리 생성AI 강의 TA·강사를 맡았다. 연구 테마는 LLM의 평가와 모델에 의한 평가, 지시 추종 능력, Web Agent를 활용한 UI/UX 평가, 교육 현장에서의 LLM 응용이다.

ChatGPT는 주당 7억 명이 이용하고 180억 메시지가 오가며, 업무 용도가 27%, 이용자의 약 절반이 26세 이하, 남녀 비율은 1:1이다. 전체 이용 용도의 80%는 실용적 안내(Practical Guidance), 정보 탐구(Seeking Information), 작문(Writing)에 집중된다[1]. 강사 본인도 1시간짜리 팟캐스트를 Gemini에서 부분 질의하며 번역·요약하고, 수십 건의 논문은 Deep Research로 조사하며, 같은 질문을 여러 서비스에 던져 교차 검증한다. 슬라이드만 공개된 해외 강의 자료도 추가 검색과 문맥 보충으로 따라갈 수 있고, 개조식 노트를 글로 풀거나 코딩·데이터 정형에도 쓴다.

이처럼 LLM을 활용한다는 것은 모델에 대한 지시(프롬프트)와 응답 선택(디코딩·메타 생성)을 공략하는 일이다. 본 강의는 디코딩 기초, 프롬프팅 기초, 메타 생성, 발전 프롬프트 예, 서비스 사례, 모델 선택을 다룬다.

---

## 디코딩의 기초: 언어 모델에서 출력을 얻는 방법

**언어 모델**이란 단어 열(문장)이 얼마나 발생하기 쉬운지를 모델화한 확률 모델로, 단어 열 $(x_1, x_2, \ldots, x_L)$ 에 생성 확률 $p(x_1, x_2, \ldots, x_L)$ 을 할당한다. "좋은" 언어 모델은 문법적·상식적 오류가 있는 문장에는 낮은 확률을 준다. 예컨대 $p(\text{일본, 의, 수도, 는, 도쿄}) = 0.02$, $p(\text{일본, 의, 수도, 는, 파리}) = 0.00001$, $p(\text{도쿄, 의, 수도, 는, 일본}) = 0.0005$ 와 같다.

이 결합 확률은 확률의 연쇄법칙으로 조건부 분포의 곱으로 분해할 수 있으며, 이렇게 분해한 모델을 **자기회귀 언어 모델**(autoregressive language model)이라 한다.

$$p(x_1, x_2, \ldots, x_L) = p(x_1) \cdot p(x_2 \mid x_1) \cdot \ldots \cdot p(x_L \mid x_1, x_2, \ldots, x_{L-1})$$

예로 $p(\text{일본, 의, 수도}) = p(\text{일본}) \cdot p(\text{의} \mid \text{일본}) \cdot p(\text{수도} \mid \text{일본, 의})$ 이다. 조건부 확률을 알면 생성도 가능하다. $p(\text{도쿄} \mid \text{일본, 의, 수도, 는}) = 0.2$, $p(\text{파리} \mid \ldots) = 0.001$, $p(\text{카이로} \mid \ldots) = 0.0005$ 이므로 "일본의 수도는" 다음에는 "도쿄"가 생성된다. 이 조건부 확률은 번역(영어 문장 → 일본어 문장), 질의응답(질문 → 답변), 요약(문서 → 짧은 서술) 등 다양한 과제로 일반화되며, 수식으로는 $p(x_{i+1:L} \mid x_1, \ldots, x_i) = \prod_{j=i+1}^{L} p(x_j \mid x_{1:i}, x_{i+1:j-1})$ 로 쓴다.

모델에서 어떻게 출력을 얻을 것인가가 **디코딩**(Decoding)의 문제이며, 이는 알고리즘과 스코어 함수의 선택이라는 관점으로도 정의된다[2]. 대표적 기법은 다섯 가지다. **Greedy decoding**은 매 스텝 가장 확률이 높은 토큰을 선택하지만, 문장 전체로는 최적이 아닐 수 있고 반복이 잦다[2]. **Beam search**는 빔 수(num_beams)만큼 후보를 남겨 여러 스텝 단위로 점수가 높은 것을 선택하나, 계산량이 많고 출력이 지루하며 짧아지는 경향이 있다[2]. **Top-k sampling**은 상위 k개에서 샘플링하지만 long-tail 문제가 있고 유망 선택지가 배제될 수 있다[2]. **Top-p sampling**(핵 샘플링, Holtzman et al., 2020)은 상위부터 누적해 누적 확률이 $p \times 100\%$ 가 되는 후보 안에서 샘플링하며, Top-k보다 유연하다[2].

샘플링의 무작위성은 **temperature** $T$ 로 조절한다. softmax 식 $p(w) = \exp(z_w / T) / \sum_{j=1}^{|V|} \exp(z_j / T)$ 에서 $T$를 0에 가깝게 하면 분포가 뾰족해져 거의 결정적이 되고, 크게 하면 무작위성이 높아진다[3]. 다만 $T=0$으로 설정해도 완전히 결정적이지 않은 경우가 있는데, 부동소수점 연산 순서와 배치 처리의 분할 방식 차이 때문이며, GPU 처리를 수정하면 결정적으로 만들 수 있다[4].

어떤 기법을 선택할까. 기준은 다양성이 필요한지이다. 이야기 생성·아이디어 발산에는 샘플링 기반 기법이, 지식 질의·번역에는 Greedy decoding이나 Beam search가 적합하다. 실제로는 Greedy 결과와 temperature·Top-p를 바꿔 여러 번 비교해 보는 것이 좋다(참고: *A Thorough Examination of Decoding Methods in the Era of LLMs*, *The Curious Case of Neural Text Degeneration*, *It's MBR All the Way Down*). "확률이 높은 것이 정말로 원하는 출력인가?"라는 물음은 뒤의 Reward model·LLM-as-a-Judge 기반 Best-of-N으로 이어진다.

정리하면, 조건부 확률로 다음 단어 후보가 결정되고 모델은 과거 문맥을 바탕으로 다음 단어의 그럴듯함(plausibility)을 출력한다(과거 문맥 반영과 학습 기법은 제3회 강의). 후보에서 어떻게 선택할지가 디코딩 기법의 문제이며 과제마다 적합한 기법이 다르다. 그리고 모델에 대한 입력, 즉 과거 문맥 자체를 공략해 과제를 풀게 하는 것이 다음 절의 프롬프팅이다.

---

## 프롬프팅의 기초: 가중치 재학습 없이 과제를 푼다

"프롬프트"는 원래 인간 입력을 촉구하는 커맨드 표시(`C:\>`, `~$`)를 뜻했지만, 근년에는 AI의 출력을 촉구하는 문자열 — "질문: 일본의 수도는?", "답변:" — 을 의미한다.

전환점은 GPT-3였다. Brown et al. (2020)[5]는 "언어 모델의 규모를 키우면 과제에 무관한(task-agnostic) few-shot 성능이 크게 향상되며 종래의 최고 수준 파인튜닝과 맞먹기도 한다. 1,750억 매개변수의 자기회귀 언어 모델 GPT-3를 학습시키고, 모든 과제에서 기울기 갱신이나 파인튜닝 없이 과제와 few-shot 시연을 순전히 텍스트 상호작용으로만 지정해 적용했다"고 보고했다. 이전까지는 과제마다 전용 모델을 가중치 갱신하며 학습했지만[6], GPT-3는 가중치 재학습 없이 프롬프트만 바꿔 다양한 과제에서 고성능을 달성했다. 전조는 GPT-2(Radford et al., 2019)[7]에서 이미 보였다. "A: "를 붙이면 답하고, "TL;DR:"(Too Long; Didn't Read)을 붙이면 요약하며, "english sentence = french sentence, english sentence =" 형태로 번역했다.

이처럼 가중치를 고정한 언어 모델이 프롬프트에 의한 조건 부여로 과제를 수행하는 것을 **문맥 내 학습**(In-context Learning, ICL)이라 하며, 하나의 모델이 재학습 없이 다양한 과제를 고성능으로 수행한다는 사실이 당시의 충격이었다[5].

프롬프팅이란 특정 기능의 발생을 촉구하도록 언어 모델에 입력하는 컨텍스트 문이다. 과제 설명·지시만 주는 **Zero-shot**, 시연(demonstration) 예를 몇 개 주는 **Few-shot**(예 하나면 one-shot)으로 나뉘며, LLM 이전의 few-shot learning과는 의미가 다르다[5]. 시연 예시 수를 늘리면, 특히 대규모 모델에서, 성능이 크게 오른다[5]. 최근에는 100만 토큰을 받아들이는 long context 모델로 수많은 예시를 주는 many-shot in-context learning[8]까지 등장했다(GPT-3는 2048 토큰). 컨텍스트가 늘면 계산량이 증가하므로 더 향상을 노리려면 파인튜닝으로 효율화해야 한다(제6회 강의).

다단계 추론 과제에서는 **Chain-of-Thought(CoT)** 가 결정적이다. Wei et al. (2022)[9]는 답에 이르는 사고 과정을 예시로 주는 Few-shot CoT를 제안했고, 다양한 수학 데이터셋에서 특히 모델이 클 때 성능 개선이 큼을 보였다. 코지마 등[10]은 CoT 예 없이 "Let's think step by step" 한마디만 붙여 모델 스스로 생각하게 하는 **Zero-shot CoT**를 시도했다. "인간이 파이프라인을 설계하지 않고 모델 스스로 생각시키는 편이 낫지 않을까?"에서 출발한 구절이다. 다만 단일 스텝 상식 추론에서는 오히려 생각이 지나쳐 실패하기도 하며, Zero-shot CoT가 빛을 발하는 것은 본질적으로 다단계 추론 과제에서다[10]. 이론적 근거로 Li et al. (2024)[11]는 CoT·중간 토큰(intermediate token)이 표현력을 향상해 순차적 처리 과제의 성능을 끌어올림을 보였다.

같은 과제라도 프롬프트에 따라 정확도가 크게 달라진다[12][13]. 원하는 출력을 얻도록 프롬프트를 시행착오하는 **프롬프트 엔지니어링**에는 수동과 자동 두 방향이 있다. 수동으로는 few-shot prompting과 CoT prompting이 대표적이며 개발사 가이드라인을 참고할 수 있다. 자동으로는 특수 토큰을 학습하는 prefix tuning·prompt tuning(제6회)과 프롬프트 문 자체를 수정하는 접근이 있다. 후자의 대표적 예로, **Automatic Prompt Engineer**(Zhou et al., 2023)[14]는 입출력 쌍으로 지시문을 LLM 스스로 예측·평가·변형하고, **Demonstrate-Search-Predict**(Khattab et al., 2022)[15]는 질문 분해와 후속 질문 같은 중간 과정을 시행착오로 생성해 결과 일치로 판정하며, **OPRO**(Yang et al., 2024)[16]는 과거 프롬프트와 점수 변천을 주며 점수를 높이는 프롬프트를 생성하고, 최근의 **GEPA**(Agrawal et al., 2025)[17]는 성공·실패 궤적에서 언어 피드백을 작성해 개선하거나 유망 후보와 결합하며 다양성 확보를 돕는다.

정리하면, 프롬프팅은 입력문을 공략해 가중치 재학습 없이 다양한 과제에서 고성능을 달성하는 기술이며, few-shot prompting과 chain-of-thought prompting이 유효하지만 표현·포맷 차이로 성능이 크게 달라져 시행착오가 필요하다.

---

## 메타 생성: 여러 번 추론해 더 나은 출력을 얻는다

Welleck et al. (2024)[18]가 정리한 **메타 생성 알고리즘**은 모델을 여러 번 추론시킨 뒤 출력을 얻는 기법군으로, 추론 시점의 계산을 늘려 품질을 끌어올린다.

가장 단순한 형태는 **Self-Consistency**(Wang et al., 2023)[19]로, 샘플링으로 여러 답을 얻어 다수결로 채택한다. **Best-of-N**[20]은 여러 답에 점수를 매겨 가장 높은 것을 선택한다. 점수는 전용 분류기(Reward Model, Process Reward Model — 제7회 강화학습)를 학습하거나, LLM에게 평가시키는 **LLM-as-a-Judge**(Zheng et al., 2023)[21]로 매긴다. 긴 글을 높게 평가하려는 편향은 있으나 인간 평가와 어느 정도 일치한다. **SELF-REFINE**(Madaan et al., 2023)[22]은 답 생성 → 피드백 → 수정 루프를 같은 모델로 프롬프팅만 바꿔 반복한다. 한 번의 추론이 아니라 여러 번의 시도와 자기 반성으로 품질을 끌어올리는 것이 공통 패턴이다.

---

## 발전적인 프롬프트: 실제 시스템과 새로운 활용

실제 제품의 프롬프트는 단순한 지시문이 아니다. Claude에서 실제로 사용되는 시스템 프롬프트[23]는 2,500단어로, 속성 정보, 장르별 응답 태도, 포맷, knowledge cut-off, 미국 대통령 선거 결과 등을 포함해 모델 행동을 정밀 제어한다.

프롬프트는 공격 대상이 되기도 한다. **적대적 프롬프트**(adversarial prompt)의 대표적인 것이 탈옥(jailbreak)으로, 페르소나 부여로 본래 답하지 않을 것도 답하게 하며("Do Anything Now"), 공격성을 높이는 토큰도 존재한다[24]. 현실 사례로는 투명 색 글자로 숨은 지시를 심어 자료와 다른 보고서를 쓰게 하는 공격[25], 논문 심사를 긍정 유도하는 비밀 명령문(일한미 등 주요 14개 대학 대책)[26]이 보고되었다.

반대로 프롬프팅만으로 복잡한 시스템을 구현하기도 한다. **DeepResearch**는 검색 쿼리 작성, 충분성 점검(회고), 답 생성을 프롬프팅으로 구성한다[27]. 논문에서 포스터를 자동 생성하는 *Paper2Poster*(Pang et al., 2025)[28]는 그림 잘라내기와 파워포인트 조작 라이브러리를 프롬프트와 조합한다(검색·코드 이용은 응용편 제2회).

프롬프팅은 학습 데이터를 만드는 데도 쓰인다. **합성 데이터**(synthetic data)는 LLM 학습용 데이터를 인공적으로, 특히 LLM으로 만드는 것으로, 제어 실험용 TinyStories·Physics of LM, 복잡 데이터셋용 WizardLM·Alpaca[29], 대모델 능력을 소모델로 옮기는 s1K·NaturalThoughts, 고품질 사전학습용 *Textbooks Are All You Need* 등 다양하다. LLM에게 인격·특성을 부여해 인간을 모의하는 **시뮬레이션** 연구도 있다(Park et al., 2024, *Generative Agent Simulations of 1,000 People*[30]).

---

## LLM을 활용한 서비스와 모델의 선택

코드도 언어라는 점에서 코딩은 LLM의 자연스러운 활용처다. GitHub Copilot, Claude Code, Cursor, Cline, Windsurf, Devin 등이 등장했고, Cursor는 2023년 릴리스 이후 2025년 6월 기준 500 million USD ARR에 900 million USD를 조달했다[31][32]. Y Combinator 투자처를 봐도 AI로 개발 속도를 높이고 새 가치를 창출하는 기업이 주류며, "10명 + AI = 10억 달러 기업"이 화제다[33][34].

이 핵심 역량을 Andrej Karpathy(2025)[35]는 **"context engineering"**, 즉 "다음 단계·처리를 위해 컨텍스트 윈도우를 최적의 정보로 채우는 정밀한 예술이자 과학"이라 불렀다. 기본 프롬프팅(이번 회), RAG·tool-use(응용편 제2회), 상태 관리·멀티모달(응용편 제7회)이 모두 이 맥락이며, Gemini_Plays_Pokemon[36]이나 Gemini 2.5[37]의 에이전트 능력이 보여주듯 컨텍스트 설계는 곧 시스템 설계다. 강사는 DeepLearning.ai의 ChatGPT Prompt Engineering for Developers, Building Systems with the ChatGPT API, How Diffusion Models Work, LangChain 강의 두 종을 일본어로 번역했다(deeplearning.ai/courses[38]).

모델 접근은 세 가지다. **API 전용**은 가중치 비공개·사용량 과금으로, 자체 컴퓨터 없이 GPT·Gemini·Claude 등을 쓴다(GPT는 1M 토큰 입력당 $1.25, 출력당 $10). **공개 모델**은 가중치까지 공개되어 분석에도 적합하고 로컬에서 실행 가능하며(Llama·Mistral·DeepSeek·Qwen·gpt-oss), **비공개 모델**은 일부 연구기관만 이용 가능하다(PaLM·Gopher). 공개 모델을 다룰 때는 **Transformers**(HuggingFace의 모델·데이터셋 허브, 연습에서도 사용, 버그 주의)와 **vLLM**(고속 추론)이 핵심이다.

공개 모델의 계산 자원은 세 갈래다. 자체 GPU(H100 80GB 1장 약 600만엔 + 전력·유지보수; 양자화 적용 gpt-oss-120b 이용 가능), 클라우드 GPU(시간당 과금, H100 $1.49/시간도 가능; AWS·GCP·Azure·Lambda·HPC-AI·Hyperbolic), 그리고 **모델 호스팅 서비스**(모델 선택만으로 입출력 과금; Cerebras[40]·Groq·Together.ai·Fireworks, 각 사 독자적 고속화 기술로 성능 차이[39])다.

성능은 lmarena(사용자 투표형)[41]와 HELM(복수 벤치마크 종합)[42]으로 가늠하며 일본어는 Nejumi LLM 리더보드 4[43]를 참고한다. 직접 평가 도구로는 simple-evals/evals(OpenAI), llm-jp-eval(LLM-jp), Lighteval(HuggingFace)가 있다. 단, 프롬프트나 선택지 좁히기 방식 차이로 같은 모델에서도 크게 다른 점수가 나올 수 있어 주의해야 한다[44][45].

선택의 출발점은 가장 성능이 좋은(비싼) 모델을 먼저 쓰는 것이다. 유료 앱이나 API playground로 시작하며[45][39], 여러 모델을 빠르게 비교할 때는 동일 인터페이스의 **OpenRouter**[46]가 유용하다("오루루키 사우나" 정답을 모든 모델이 오답으로 답한 사례도 있어 평가는 신중해야 한다).

---

## 더 읽을거리

- **디코딩/메타 생성**: Generating Text from Language Models(ACL 2023 튜토리얼), Stanford CS324, CMU Advanced NLP Inference I/Advanced Inference Strategies, *From Decoding to Meta-Generation*(arxiv 2406.16838), Beyond Decoding(NeurIPS 2024), HuggingFace Generation strategies, Brown et al. 2024 *Large Language Monkeys*, Wu et al. 2024 *Inference Scaling Laws*, Gu et al. 2024 *A Survey on LLM-as-a-Judge*, Kamoi et al. 2024 *When Can LLMs Actually Correct Their Own Mistakes?*, 2024 가을 LLM 강좌 특별회 "LLM의 자기 수정".
- **프롬프팅/문맥 내 학습**: Stanford CS224U·CS224N Lecture 11, CMU CS11-711, Lilian Weng "Prompt Engineering", Prompt Engineering Guide, *In-context Learning and Induction Heads*(transformer-circuits.pub), Dai et al. 2023, Min et al. 2022, Razeghi et al. 2022, Wei et al. 2023, 대규모 언어 모델 응용 제5회.
- **Chain-of-Thought**: Stanford CS25 LLM Reasoning, Wang et al. 2024, Yao et al. 2023(Tree of Thoughts).
- **발전 프롬프트**: Grok prompts(github.com/xai-org/grok-prompts), Zou et al. 2023, Anthropic "How we built our multi-agent research system", OpenAI Codex CLI 프롬프트.
- **GPT-2/3 뒷이야기**: Ilya Sutskever·Alec Radford 강연, *An Observation on Generalization* 영상.
- **평가/스케일링**: *The Second Half*, Jason Wei "Successful language model evals", *How to Build Good Language Modeling Benchmarks*, *Why You Should Stop Using HotpotQA for AI Agents Evaluation in 2025*, Singh et al. *The Leaderboard Illusion*, MIT TinyLab *TinyML*, *The Ultra-Scale Playbook*, *How to Scale Your Model*, Stanford CS336 Lec. 5~7, 도쿄대 "AI와 반도체" 강좌, Karpathy "Software Is Changing (Again)", Andrew Ng "AI is Accelerating Startups", "Vibe coding MenuGen".

---

## Reference

[1] Chatterji et al., 2025, *How People Use ChatGPT*.
[2] *How to generate text: using different decoding methods for language generation with Transformers*, https://huggingface.co/blog/how-to-generate
[3] Cohere (2024), "Parameters for Controlling Outputs", Cohere LLMU, https://cohere.com/llmu/parameters-for-controlling-outputs
[4] Thinking Machines (2024), "Defeating Nondeterminism in LLM Inference", https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/
[5] Brown et al., 2020, *Language Models are Few-Shot Learners*.
[6] Liu et al., 2021, *Pre-train, Prompt, and Predict: A Systematic Survey of Prompting Methods in Natural Language Processing*.
[7] Radford et al., 2019, *Language Models are Unsupervised Multitask Learners*.
[8] Agarwal et al., 2024, *Many-Shot In-Context Learning*.
[9] Wei et al., 2022, *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*.
[10] Kojima et al., 2022, *Large Language Models are Zero-Shot Reasoners*.
[11] Li et al., 2024, *Chain of Thought Empowers Transformers to Solve Inherently Serial Problems*.
[12] Gonen et al., 2023, *Demystifying Prompts in Language Models via Perplexity Estimation*.
[13] Sclar et al., 2024, *Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design or: How I learned to start worrying about prompt formatting*.
[14] Zhou et al., 2023, *Large Language Models Are Human-Level Prompt Engineers*.
[15] Khattab et al., 2022, *Demonstrate-Search-Predict: Combining Retrieval and Language Models for Knowledge-Intensive NLP Tasks*.
[16] Yang et al., 2024, *Large Language Models as Optimizers*.
[17] Agrawal et al., 2025, *GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning*.
[18] Welleck et al., 2024, *From Decoding to Meta-Generation: Inference-time Algorithms for Large Language Models*.
[19] Wang et al., 2023, *Self-Consistency Improves Chain of Thought Reasoning in Language Models*.
[20] Snell et al., 2024, *Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters*.
[21] Zheng et al., 2023, *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*.
[22] Madaan et al., 2023, *Self-Refine: Iterative Refinement with Self-Feedback*.
[23] Anthropic Release notes, System prompts.
[24] *Adversarial Prompting in LLMs*.
[25] 시마다 타쿠(2025), "AI에 과제를 쓰게 하면 자료에 없는 내용을 출력 ― 게이오대의 AI 대책이 화제, 의도를 들었다", ITmedia AI+, 2025/05/01, https://www.itmedia.co.jp/aiplus/articles/2504/30/news214.html
[26] 니혼게이자이신문(2025), "논문 내에 비밀 명령문, AI에게 '높게 평가하라' 일한미 등 주요 14개 대학에서", 2025/06/29, https://www.nikkei.com/article/DGXZQOUC13BCW0T10C25A6000000/
[27] *Gemini Fullstack LangGraph Quickstart*.
[28] Pang et al., 2025, *Paper2Poster: Towards Multimodal Poster Automation from Scientific Papers*.
[29] Taori et al., 2023, *Alpaca: A Strong, Replicable Instruction-Following Model*.
[30] Park et al., 2024, *Generative Agent Simulations of 1,000 People*.
[31] *Cursor at $100M ARR*, https://sacra.com/research/cursor-at-100m-arr/
[32] Anysphere (2026), "Cursor - The AI-first Code Editor", https://cursor.com/ja
[33] *Startup Directory*, https://www.ycombinator.com/companies
[34] *10 People + AI = Billion Dollar Company?*, https://www.youtube.com/watch?v=CKvo_kQbakU
[35] Andrej Karpathy (2025), "X Post (status/1937902205765607626)", https://x.com/karpathy/status/1937902205765607626
[36] *Gemini_Plays_Pokemon*, https://www.twitch.tv/gemini_plays_pokemon
[37] Google (2025), "Gemini 2.5", https://blog.google/technology/ai/google-gemini-next-generation-december-2025/
[38] DeepLearning.AI, "Courses", https://www.deeplearning.ai/courses/
[39] Artificial Analysis (2026), "GPT-OSS-120B Model Providers and Performance Analysis", https://artificialanalysis.ai/models/gpt-oss-120b/providers
[40] Cerebras Systems (2026), "Cerebras - AI Supercomputing at Unprecedented Speed", https://www.cerebras.ai/
[41] LMSYS Org (2026), "Arena AI Leaderboard (formerly LMSYS Chatbot Arena)", https://lmarena.ai/leaderboard/
[42] Stanford CRFM, "Holistic Evaluation of Language Models (HELM)", https://crfm.stanford.edu/helm/capabilities/latest/
[43] *Nejumi LLM 리더보드 4*, https://wandb.ai/llm-leaderboard/nejumi-leaderboard4/reports/Nejumi-LLM-4--VmlldzoxMzc1OTk1MA
[44] Hugging Face (2024), "What's going on with the Open LLM Leaderboard and MMLU?", https://huggingface.co/blog/open-llm-leaderboard-mmlu
[45] Google DeepMind (2026), "Gemini - Google's Next-Generation AI Models", https://deepmind.google/models/gemini/
[46] OpenRouter (2026), "OpenRouter - A unified API for AI models", https://openrouter.ai/
