# 제7회: 강화학습

*도쿄대학교 마쓰오·이와사와 연구실이 작성하고, 2025년 10월부터 11월에 걸쳐 개최된 「대규모 언어모델 강좌 2025」 기초편 강의 자료입니다. 크리에이티브 커먼즈 CC BY-NC-ND 4.0(저작자표시–비영리–변경금지 4.0 국제) 라이선스로 등록되어 있습니다. 재이용(2차 이용)이 허락되어 있으며, 재이용 시에는 반드시 라이선스 표기를 기재해 주세요. 재이용하는 곳에 참고 논문 등의 인용이 있는 경우, 권말의 References에서 인용 위치를 게시해 주세요. 원래의 표현이 변하지 않는 범위(글꼴·크기 등)라면 개작이 가능하며, 영리 목적 재이용에 대해서는 별도 문의가 필요합니다. 허락 없는 촬영 및 제3자에 대한 공개를 금지합니다.*

*강사: 다카기 쇼타(도쿄대학교 대학원 공학계 연구과 마쓰오 연구실 박사 2년차). 2019년 나라 공업고등전문학교 정보공학과, 2022년 오사카대학교 기초공학부 시스템화학과를 거쳐 2022년 4월부터 도쿄대학교 공학계 연구과 기술경영전략학 전공. Sony ML R&D intern, DeNA backend intern, Recruit Data Specialist Intern, SanSan Intern 등을 경험했습니다. 전문 분야는 대규모 언어모델, 강화학습, 로보틱스이며, 「Deep Learning 기초 강좌」「심층 강화학습 스프링 세미나」「대규모 언어모델 강좌」「세계 모델과 지능」 등의 강사를 담당했습니다.*

## 이번 회의 목적과 목표

이번 회의의 목적은 LLM에서 강화학습이란 무엇인지, 그 메커니즘과 필요성을 이해하는 데 있습니다. 구체적 목표는 셋입니다. 첫째, LLM에서 강화학습의 목적을 이해하고 설명할 수 있다. 둘째, 강화학습의 대표적 기법인 RLHF, DPO, GRPO의 개요를 설명할 수 있다. 셋째, PyTorch로 각 기법을 구현할 수 있다. 지금까지의 강의 내용과 기본적인 딥러닝 지식을 전제로 합니다.

## LLM 훈련 플로우에서 강화학습의 위치

LLM의 훈련은 세 단계로 구성됩니다. 첫 번째 **사전학습(Pre-Training)** 단계는 대규모 코퍼스를 통한 자기지도학습으로 어휘·문법·지식·추론 능력 등 기본 언어 이해를 획득시키는 단계입니다. Next Token Prediction, Masked Language Model 등이 사용되며, GPT-3의 사례에서는 CommonCrawl 기반 410B 토큰(약 570GB) 같은 대규모 데이터셋이 활용됩니다. 두 번째 **지도 fine-tuning(Supervised Fine-Tuning)** 단계는 레이블이 붙은 데이터로 언어모델의 성능을 개선하거나 특정 태스크·도메인에 적응합니다. 하위 태스크 특화와 Instruction Tuning이 여기에 해당하며, LIMA(1,000샘플, 약 3MB)처럼 양질의 소규모 데이터셋이 자주 사용됩니다. 세 번째 **강화학습(Reinforcement Learning)** 단계가 이번 강의의 주제로, 인간의 피드백이나 규칙 기반 보상을 활용해 언어모델의 출력이 인간의 가치관에 더 부합하도록 조정하고 추론 능력을 향상시킵니다.

"Supervised fine-tuning"이라는 표현은 강화학습 기법인 RLHF와 구별하기 위해 사용됩니다. 의도적으로 이 표현을 쓰는 경우 일반적인 지도 fine-tuning이 아니라 Instruction Tuning을 가리키는 경우가 많습니다. 사전학습과 fine-tuning/Post-Training의 차이는 목적과 데이터 규모에 있습니다. 사전학습이 대규모 데이터로 일반 언어 능력을 도입하는 데 반해, fine-tuning은 소규모 양질의 데이터로 특정 태스크에 적응하거나 인간·모델의 피드백을 반영합니다.

강화학습에서 에이전트(행동 주체)는 환경의 상태에 기반하여 순차적으로 행동을 결정하며, 행동의 결과 얻어지는 보상을 이용해 최적 정책을 학습합니다. 대표적 응용으로 AlphaGo를 들 수 있으며, 자율주행차, 로봇 공학(Boston Dynamics 등), 게임 등 널리 응용되어 왔습니다.

언어모델에서의 강화학습은 출력 문장에 대해 보상을 주고 그것을 피드백하는 구조로, Next Token Prediction과는 다른 틀에서 학습합니다. 보상의 주체는 세 유형입니다. 인간이 주는 경우(RLHF), 다른 LLM을 이용하는 경우(RLAIF), 규칙 기반 모델로 주는 경우(RLVR). 대규모 언어모델에서 강화학습은 주로 두 가지 용도로 쓰입니다. 첫째는 **얼라인먼트(Alignment)**로, 차별적·폭력적 발언을 억제하고 인간의 가치관에 맞추는 것입니다. 둘째는 **추론 능력 향상**으로, 수학·코딩 등에서 깊이 사고하도록 강화학습을 수행해 비약적 성능 향상을 달성합니다(수학 올림피아드 금메달, IQ 140 이상 기록 등). 이에 따라 언어모델 강화학습은 두 갈래로 나뉩니다. 인간의 가치관에 맞추는 RLHF/DPO 계열과, 수학·코딩 능력 향상이 목적인 RLVR 계열입니다.

## RLHF: 인간의 피드백으로부터의 강화학습

### 기존 언어모델의 문제점과 얼라인먼트의 필요성

초기 대규모 언어모델은 인간에게 바람직하지 않은 발언, 즉 설계자가 의도하지 않은 발언을 하여 논란이 되었습니다. 마이크로소프트 Tay는 Twitter에 등장하여 24시간 만에 5만 팔로워를 획득하고 10만 회 트윗했지만, 악의적 이용자의 발언에 영향을 받아 16시간 만에 혐오 발언을 반복하였고 결국 공개 하루 만에 중단되었습니다(2016년). 한국의 이루다는 카카오톡 대화 100억 건을 바탕으로 작성되어 2주 만에 이용자 75만 명을 기록했지만, 성적 소수자에 대한 혐오 발언으로 약 1개월 만에 서비스가 중단되었습니다(2021년).

이러한 의도하지 않은 발언을 Instruction Tuning만으로 대처하는 것은 어렵습니다. 자연어 데이터 수집에 비용이 들고, "말하지 않도록" 하는 정답 데이터를 만들기 어려우며, Instruction Tuning은 인간의 의도를 직접적으로 학습하는 것이 아니기 때문입니다. 그래서 어떤 문장이 의도대로의 출력인지를 모델에 피드백하여 인간의 의도에 직접 부합하도록 학습하는 HITL(Human in the loop) 접근이 필요해졌습니다.

인간의 의도대로 모델을 학습시키는 것을 **얼라인먼트(Alignment)**라 하며, 이를 위해 RLHF가 필요합니다. 인간의 의도에는 명시적 의도("이 지시에 따라주세요", "어시스턴트로서 행동해 주세요")와 암묵적 의도("날조하지 않는다", "유해한 말은 하지 않는다")가 존재합니다.

### 얼라인먼트의 기준: HHH

얼라인먼트의 기준은 보통 세 가지로 정리됩니다. **Helpful(도움됨)**은 사용자 질문에 간결·효율적으로 답하고, 정보가 부족하면 적절한 질문을 던지며, 상대방의 수준에 맞춘 응답을 합니다. **Honest(정직함)**는 허위 없이 정확한 문장을 출력하며, 자신이 어느 정도 불확실한 정보인지 제시합니다(이를 위해 모델은 자신이 무엇을 아는지 이해해야 합니다). **Harmless(무해함)**는 공격적·차별적 발언을 하지 않고 악의적 질문을 감지해 거부합니다. 이 세 가지를 합쳐 **HHH**라 부르며, Helpful은 HH-RLHF, Honest는 HaluEval, Harmless는 CrowS-Pairs·WinoGender 등으로 평가합니다. 그 밖에 LLM 잠재적 리스크를 3개 수준·합계 60개 타입으로 정의한 Do-Not-Answer 같은 평가 데이터셋도 존재합니다.

인간이 피드백을 주는 것에도 한계가 있습니다. 태스크가 복잡해지면 인간이 평가할 수 없게 되기 때문입니다. 이를 보완하기 위해 AI 어시스턴트의 힘을 빌리는 연구가 진행되고 있습니다. 더 나아가 AGI가 폭주하지 않도록 제어하는 **Superalignment** 연구, 약한 LLM이 강한 LLM을 감독하는 weak-to-strong generalization 등이 추진되고 있습니다. AGI가 Alignment되지 않으면 인류에 중대한 리스크를 가져올 가능성이 있다고 OpenAI는 주장합니다.

### RLHF의 전체상과 역사

RLHF는 InstructGPT, ChatGPT 등에서 이용됩니다. ChatGPT는 2022년 11월 30일 공개되어 1주일 만에 100만 사용자, 2개월 만에 1억 사용자에 도달했습니다.

RLHF의 학습은 세 단계로 구성됩니다. **Step 1(지도학습)**에서는 프롬프트와 그에 대한 적절한 답변 쌍을 레이블러(인간)가 고안해 데이터셋을 작성하고, 사전학습 모델을 fine-tuning합니다. **Step 2(보상 모델 학습)**에서는 어떤 프롬프트에 대한 Step 1 모델의 답변을 복수 패턴 준비해 레이블러에게 순위를 매겨 달라고 하고, 이 순위 데이터셋으로 보상 모델을 학습합니다. **Step 3(강화학습)**에서는 보상이 최대가 되는 정책(Step 1 모델)을 탐색해 최적의 답변을 생성합니다. 모델 답변에 대해 보상값을 추정하고 그것을 피드백하여 정책을 개선합니다. 보상 모델에는 사전학습 모델이나 fine-tuning 모델의 최종층만 선형층으로 변경한 모델이 자주 사용되어 출력은 스칼라값이 됩니다.

RLHF의 역사는 2017년 OpenAI의 "소수의 인간 피드백으로부터 강화학습" 연구로 거슬러 올라갑니다(같은 해 PPO가 발표됨). 로봇 시뮬레이터와 Atari에서 샘플 효율 향상을 확인했으며, 정책이 보상을 최대화하도록 학습하고, 출력 행동 중 두 가지를 인간이 평가하며, 비교 결과로 Reward Predictor를 학습하는 세 단계로 이루어졌습니다. 2020년에는 GPT-3로 요약 태스크에 적용되어 fine-tuning이나 인간 작성 참조 요약보다 우수한 결과를 보였습니다.

**InstructGPT**에서 이 기법이 본격 정립되었습니다. Step 1에서는 프롬프트 데이터셋에 대한 인간 labeler의 답변으로 지도학습을 수행하고, Step 2에서는 출력에 대한 "바람직함"을 순위 매긴 데이터로 보상 모델을 학습하며, Step 3에서는 보상 모델이 보상을 생성하고 PPO로 강화학습을 수행합니다. Step 3 완료 후 새 모델로 Step 2~3를 반복합니다.

### 강화학습의 최적화 알고리즘: PPO

RLHF에서 자주 사용되는 강화학습 알고리즘은 **PPO**입니다. PPO는 Actor-Critic 알고리즘의 파생형으로, Actor와 Critic이 협력해 정책을 갱신하고 보상을 최대화합니다.

정책(Actor)과 가치 모델(Critic)은 파라미터를 가진 신경망으로 표현됩니다. **정책 경사법**은 𝜃로 파라미터화된 정책을 기울기로 직접 최적화하는 기법입니다.



![수식](eq-svg/eq-078cca7b5a.svg)




![수식](eq-svg/eq-539fb934c6.svg)




![수식](eq-svg/eq-f8ca1199e9.svg)





![수식](eq-svg/eq-f4d527d906.svg)



PPO는 TRPO를 단순화한 기법입니다. TRPO는 정책 경사법의 갱신 폭에 KL 거리 제약을 걸어 정책 열화를 방지하고, PPO는 갱신 폭을 clip해 계산 복잡함을 경감합니다. 가치 모델은 보상 합과의 MSE로 학습됩니다.



![수식](eq-svg/eq-a0d22e1c20.svg)




![수식](eq-svg/eq-539565c1ff.svg)




![수식](eq-svg/eq-532bde36de.svg)





![수식](eq-svg/eq-a94fb46f03.svg)



강화학습 학습 자료로는 영어권의 Coursera RL Specialization, Reinforcement Learning Lecture Series 2021(DeepMind x UCL), Stanford CS234: Reinforcement Learning, David Silver의 Introduction to Reinforcement Learning, UC Berkeley CS 285: Deep Reinforcement Learning, Deep RL BootCamp, HuggingFace의 Deep Reinforcement Learning Course가 있으며, 일본어 자료로는 도쿄대학교 마쓰오 연구실 심층 강화학습 서머 스쿨 강의 자료와 『강화학습(제2판)』 등이 있습니다.

### 보상 모델 학습



![수식](eq-svg/eq-c3b37719b3.svg)





![수식](eq-svg/eq-ebe7409ea8.svg)





![수식](eq-svg/eq-fb28edcccc.svg)



### 언어모델 강화학습의 문제와 해결책

언어모델 강화학습은 "어떤 문장을 생성할 것인가"를 정책으로 하고 보상 모델 출력을 최대화하도록 학습합니다. 단순히 보상 기댓값을 최대화하면 학습이 잘 되지 않아 별도 장치가 필요합니다.



![수식](eq-svg/eq-250657986b.svg)



두 가지 문제가 있습니다. 첫째, **Reward Hacking**입니다. 보상을 최대화하려는 모델이 바람직하지 않은 정책을 학습해 버리는 현상으로, 대책으로 **KL Penalty**를 사용합니다. 생성 문장이 SFT 모델로부터 크게 변하지 않도록 하며, 𝛽 하이퍼파라미터로 균형을 조정합니다(크면 안정적이지만 목적 함수가 커지기 어렵고, 작으면 목적 함수는 커지지만 정책이 붕괴하기 쉽습니다).



![수식](eq-svg/eq-bf48f4e6a5.svg)



둘째, **Alignment Tax(얼라인먼트 세금)**입니다. 인간의 의도대로 학습시키면 일반화 성능이 열화(사전 지식 망각)하는 현상으로, 대책으로 **Replay**를 사용합니다. 사전학습 데이터 𝐷_pretrain로 대수 우도(log-likelihood)를 최대화해 망각을 방지하며, 𝛾로 균형을 조정합니다.



![수식](eq-svg/eq-28dc484d2a.svg)



둘을 조합한 것이 **PPO-ptx**입니다.



![수식](eq-svg/eq-67a9f05461.svg)



PPO-ptx는 GPT, SFT와 비교해 큰 성능 개선을 보였으며 PPO 대비로도 개선이 확인되었습니다. InstructGPT는 GPT-3보다 지시를 잘 따르고 환각이 억제되며, 사용자와 동일 언어를 사용하는 비율도 높아졌습니다.

참고로 Reverse KL(𝐷_KL[𝜋^RL || 𝜋^SFT])은 특정 모드를 커버하도록 학습하여 RLHF에서 채택되며, Forward KL(𝐷_KL[𝜋^SFT || 𝜋^RL])은 원래 분포 전체를 커버하도록 학습합니다.

### PPO-max와 강화학습의 안정화

PPO-ptx만으로 충분한 학습이 되는 것은 아닙니다. RL은 기본적으로 학습이 불안정하여 세밀한 구현 테크닉과 하이퍼파라미터 조정이 필요합니다. **PPO-max**는 Clipping, Initialization, GAE 등 학습 안정화 테크닉을 추가한 방법으로, 장기적 안정 학습을 실현합니다.

### RLHF의 평가

평가 기준은 Honesty, Helpfulness, Harmlessness입니다. **Honesty** 평가에는 TruthfulQA와 HaluEval이 사용됩니다. TruthfulQA는 진실성을 평가하는 벤치마크로 건강, 법률, 금융, 정치 등 38개 카테고리에 걸친 817개 질문과 답변으로 구성되며, fine-tuning된 GPT-3를 이용해 평가를 자동화합니다. HaluEval은 환각을 인식할 수 있는지 평가하는 벤치마크로 ChatGPT가 환각을 일으키기 쉬운 데이터로 구성됩니다. **Helpfulness** 평가에는 Anthropic이 개발한 HH-RLHF가 자주 사용되는데, 크라우드 워커에 의해 수집되었으며 학습과 평가 모두에 활용됩니다. **Harmlessness** 평가에는 인종/피부색, 성별/성 정체성, 성적 지향, 종교, 연령, 국적, 장애, 외모, 사회경제적 지위의 9가지 편견에 관한 CrowS-Pairs와 젠더 바이어스에 관한 WinoGender가 사용됩니다. 포괄적 평가 도구 **FLASK**는 4가지 관점(Logical Thinking, Background Knowledge, Problem Handling, User Alignment)에서 12개 스킬을 GPT-4로 5단계 평가하며 FLASK dataset과 FLASK-HARD dataset이 준비되어 있고, 인간 평가와 GPT-4 평가가 유사한 경향을 보입니다. 또한 보상 모델이 올바르게 학습되었는지 포괄적으로 평가하는 **RewardBench** 벤치마크와 리더보드도 공개되어 있습니다.

### RLHF의 과제

RLHF는 Human Feedback, Reward Model, Policy 각 부분에 과제를 안고 있으며, Reward Model과 Policy 양쪽에 공통되는 과제도 있습니다.

**Human Feedback의 과제**: (1) Misaligned Evaluators — 질 높은 labeler 선택이 어렵고, 유해한 편견을 가진 평가자나 데이터 오염 시도가 있을 수 있으며, RLHF가 "누구의 의견을 반영하는가"의 문제도 있습니다(RLHF 전에는 저소득·저학력과 일치하던 의견이 RLHF 후 역전되기도 함). (2) Difficulty of Oversight — 인간은 단순 실수를 저지르고 어려운 태스크를 평가할 수 없으며, 크라우드 워커의 33~46%가 LLM을 사용하는 것으로 추정됩니다(스스로 생각하는 것보다 LLM에게 생각하게 하면 API 대금을 지불하더라도 경제적 플러스가 되기 때문). (3) Data Quality — 데이터 수집 바이어스, 비용·품질 트레이드오프. 모델의 지식과 능력은 대부분 사전학습 시에 학습된다는 가정하에, 양질의 데이터를 소량이라도 모을 필요가 있습니다. (4) Feedback Type Limitations — 2개 쌍 ranking은 쉽지만 효율이 나쁘고, 언어 피드백은 품질 보장이 어렵습니다.

**Reward Model의 과제**: (1) Problem Misspecification — 개별 인간의 가치관을 보상 함수로 표현하기 어렵고 복수 의견 문제에 단일 스코어 매기기가 어렵습니다. (2) Misgeneralization/Hacking — 올바른 레이블에서라도 보상 해킹이 일어날 수 있으며, 과적합 시 특히 쉽습니다(스케일링 법칙 연구 있음). (3) Evaluation Difficulty — 보상 모델 평가 자체가 어렵습니다.

**Policy의 과제**: (1) RL Difficulties — 정책 최적화가 어렵고 적대적 악용(Jailbreak, 예: GPT-4 DAN attack)이 가능합니다. (2) Policy Misgeneralization — 최적 RL 에이전트는 권력을 추구하는 경향이 있습니다. (3) Distributional Challenges — 모드 붕괴(다양성 상실)나 사전 모델 바이어스 강화가 일어날 수 있습니다(GPT-4는 RLHF 후 자신 있게 틀리는 경우가 늘어났습니다).

Reward Model과 Policy를 동시에 학습하면 데이터 분포 변화가 유발됩니다. 온라인 학습에서는 보상 모델-정책 간 순환 영향이, 오프라인 학습에서는 보상 모델 바이어스로 잘못된 일반화 가능성이 있습니다.

### RLHF 과제에 대한 대책

Human Feedback 대책으로는 문장별 보상 추정이나 3개 보상 모델(사실 부정확, 관련성 없음, 정보 불완전) 학습 등 상세 피드백 설계가 있습니다. Reward Model 대책으로는 복수 관점에서 학습된 보상 모델 파라미터를 섞는 Model Soup 방식(파레토 최적 alignment 지향)이 있습니다. Policy 대책으로는 복수 모델 출력으로 순위를 매겨 SFT하는 **RRHF**(PPO 간소화 기법), 보상 모델 상위 100/k%를 필터링해 PPO 없이 동등 이상 성능을 내는 **RAFT**, 유해·무해 프롬프트로 자동 보상 할당하는 **RLCD**, 랭킹에 이유를 추가해 fine-tuning하는 **Chain of Hindsight**(CoHF) 등이 제안되었습니다.

RLHF 구현 라이브러리로는 trl(HuggingFace, PPO 기반), trlx(CarperAI, PPO·ILQL), RL4ML(다양한 RL 알고리즘), DeepSpeed Chat(GPU 1대로 100억 파라미터, 복수 GPU로 1000억 파라미터, SoTA 15배 빠른 학습)이 있습니다. 자주 사용되는 데이터셋은 HH-RLHF(chosen/rejected 랭킹), OpenAssistant(oasst1, oasst2), HelpSteer, Uni-RLHF, UltraFeedback 등이며 기본적으로 영어가 대부분입니다.

## DPO: 보상 모델 없이 직접 선호도를 학습하는 얼라인먼트 기법

### DPO의 기초와 이론

$$**DPO**(Direct Preference Optimization)는 Reward Model을 거치지 않고 직접 Preference를 고려한 최적화를 수행합니다. Reward Model은 암묵적으로 정의되며, 결과적으로 "보상 모델 학습 + 강화학습"이 "지도학습만"과 동등해집니다. 보상 추정이 틀린 만큼 가중치를 부여하며 𝜋(yw|x) 우도를 최대화하고 𝜋(yl|x) 우도를 최소화합니다$$

DPO와 RLHF는 근사나 가정 없이 수학적으로 동등함이 보여졌습니다(증명은 Appendix).



![수식](eq-svg/eq-fcd00346ee.svg)



증명은 RLHF 목적 함수로부터 출발합니다.



![수식](eq-svg/eq-0f090d09b0.svg)



이 문제의 최적해는 해석적으로 풀 수 있습니다.



![수식](eq-svg/eq-dd44aa60cb.svg)




![수식](eq-svg/eq-2c4b1f83f4.svg)





![수식](eq-svg/eq-8da1d289ba.svg)





![수식](eq-svg/eq-4729e354c4.svg)





![수식](eq-svg/eq-3a0fb79996.svg)





![수식](eq-svg/eq-ebe7409ea8.svg)




![수식](eq-svg/eq-f9ccabb991.svg)



$$보상 모델 r𝜃(x, y)을 𝛽·log(𝜋𝜃(y|x) / 𝜋^SFT(y|x))로 간주하고 있다고 해석할 수 있습니다. 논문 제목 "Your Language Model is Secretly a Reward Model"이 이를 가리킵니다$$

### DPO의 파생 기법



![수식](eq-svg/eq-5327cb8f78.svg)



$$**KTO**(Kahneman-Tversky Optimization)는 전망 이론(prospect theory)에 기반해 인간의 효용 모델을 도입합니다(예: "5만엔을 얻은 기쁨보다 잃은 슬픔이 더 크다"). (x, yw, yl) Preference 데이터가 필요 없고 단일 쌍 (x, y)만으로 학습 가능합니다$$

DPO, ΨPO/IPO, KTO 등은 데이터셋과 보상 함수 가정을 변경한 기법들입니다. DPO가 가장 성능이 높지만, 학습 비용을 줄이려면 KTO나 CPO가 권장됩니다. 한편 "현 시점에서 DPO는 PPO에게 이길 수 없다"는 평가도 있으며, PPO > filtered DPO / iterative DPO > DPO > SFT의 순위로 알려져 있습니다. 그 이유는 PPO를 이용함으로써 Reward Model의 외삽 데이터에 접근할 수 있기 때문으로 추정됩니다.



![수식](eq-svg/eq-33ce0cfbcb.svg)



### 기타 얼라인먼트 기법

**Stable Alignment**는 모의 인간 사회 샌드박스에서 에이전트끼리 대화하며 다양한 관점의 답변을 생성합니다. **AlpacaFarm**은 "인간이 어떤 평가를 반환할 것인가"를 시뮬레이션해 저렴하고 빠르게 RLHF를 진행하는 도구로, 실제 인간 평가 대비 1/45 비용으로 동등한 평가가 가능하다고 주장합니다.

발전 기법은 여러 축으로 분류됩니다. Feedback 원천별: Human Feedback(RLHF, RAFT, RRHF) vs AI Feedback(RLCD, Stable Alignment, AlpacaFarm, RLAIF, Constitutional AI). 학습 방식별: Rank-based(DPO, PRO, RRHF, SLiC) vs Language-based(CoH, Second Thoughts, Stable Alignment, SelFee). RL 사용 여부별: Using RL(RLHF, RLCD, RLAIF) vs Not Using RL(DPO, IPO, KPO, CPO, PRO, RRHF, RAFT).

### 발전적 의제

RLHF를 둘러싼 근본 질문들이 남아 있습니다. (1) 왜 RLHF로 성능이 올라가는가 — 실제로는 사전학습에서 얻은 분포를 의도에 맞는 출력으로 변화시키고 있을 뿐일 수 있습니다. (2) RL은 정말 필요한가 — DPO, PRO, RLCD 등 RL 미사용 방법이 동등 이상의 성능을 내고 있어, 아마도 RL은 필요하지 않을 수 있습니다. (3) SFT vs RLHF — 어느 정도는 SFT로 충분하지만 나머지 1% 제어에는 필요합니다. (4) RLHF vs RLAIF — AI Feedback에서는 Feedback 원천 모델 성능을 넘어서기 어렵지만, RLAIF(Constitutional AI 등)나 외부 도구 활용 RLCF(reinforcement learning from computational feedback) 방향으로 발전할 것으로 보입니다.

## RLVR: 검증 가능한 보상으로 추론 능력을 향상시키는 강화학습

### LLM 추론의 한계와 경험의 시대

대규모 언어모델은 박사 과정 수준 지식 문제에서 인간을 뛰어넘고 수학 올림피아드 문제도 풀 수 있지만, 한편으로는 간단한 계산 문제를 틀리기도 합니다. **이중 과정 이론(Dual Process Theory)**은 카네만과 트버스키가 널리 알린 이론으로, 인간 사고가 두 시스템으로 작동한다고 가정합니다. 시스템 1은 직관·번뜩임으로 무의식적 판단하는 사고, 시스템 2는 수학·논리적 사고로 신중하게 천천히 생각하는 사고입니다. LLM은 시스템 1은 잘하지만 시스템 2는 서투릅니다.

시스템 1적 사고는 과거 경험·지식에 기반한 패턴 매칭이며 빠르게 보간하는 프로세스입니다. 사전학습된 LLM은 **보간형 데이터베이스(interpolative database)**처럼 행동하며, 많은 휴리스틱(경험칙)을 학습하고 조합해 동작하지만 근본적 인과 구조를 학습하고 있는 것은 아닙니다.

사전학습 스케일링 법칙의 시대는 끝났는가 하는 질문이 제기됩니다. 컴퓨팅은 향상되지만 데이터는 고갈되어 가며, GPT-4.5는 모델을 키웠음에도 큰 성능 향상에 이르지 못했습니다. 근년 AI는 "휴먼 데이터의 시대"에 있었으나, 인간의 방대한 데이터를 학습하는 것만으로는 "인간을 뛰어넘는" 초인적 지능에 도달하기 어렵습니다. 이 한계 돌파를 위해 "경험의 시대"로의 전환이 필요하며, AI 자신이 시행착오하고 그 결과로부터 학습하도록 하는 방법이 강화학습입니다.

추론 스케일링은 성공적으로 입증되었습니다. 매우 긴 Chain-of-Thought를 수행하도록 강화학습함으로써 OpenAI o1이나 DeepSeek R1은 추론 시 깊이 생각할수록 성능 향상에 기여했으며, LLM이 시스템 2적 사고를 손에 넣어 추론 스케일링 시대의 계기가 되었습니다.

### RLVR의 개요와 DeepSeek R1의 성공

**RLVR**(Reinforcement Learning with Verifiable Reward)은 검증 가능한 보상 모델로 강화학습을 수행합니다. 수학은 최종 출력이 맞는지, 코드는 실행 결과가 맞는지·테스트가 통과하는지로 보상을 계산합니다. RLHF와 달리 보상 모델 학습이 불필요합니다. 보상 계산 방법으로 Math-Verify, LLM-as-a-judge for facts, Code Sandboxes 등이 사용됩니다. o1 이후 다양한 모델에 RLVR이 응용되고 있으며 수학·코드 등 깊은 사고가 필요한 태스크에서 비약적 성능 향상을 보여주고 있습니다.

**DeepSeek R1**은 오픈소스로 처음으로 o1에 필적하는 성능을 내었으며, 독자적 강화학습 알고리즘인 GRPO를 제안해 성능 향상에 기여했습니다.

### GRPO와 그 발전판



![수식](eq-svg/eq-75d60389ae.svg)



RLVR에 의해 흥미로운 **"아하 체험"**이 관찰됩니다. 자신의 시행착오 결과가 틀렸을 때 "Wait, wait. That's an aha moment"라며 올바른 풀이를 깨닫는 현상입니다. 또한 강화학습으로 Verification, Backtrack 행동이 증가하며 스코어도 향상됩니다. RL 전 모델에서 이 두 행동이 보이지 않으면 RL을 해도 성능이 향상되지 않습니다.

GRPO의 두 문제점: (1) **Length normalization bias** — 토큰 길이로 정규화되어 길이를 길게 하는 쪽이 페널티를 받기 어려워 학습이 진행되면 생성 길이가 길어집니다. (2) **Question-level difficulty bias** — 어드밴티지를 표준 편차로 나누어 극단적 난이도 문제에서 더 높은 가중치가 부여됩니다.

발전판 **Dr. GRPO**는 길이 정규화 없이 토큰 손실을 합산한 뒤 그룹 수로만 평균을 내어 길이 바이어스를 줄이며, 더 짧은 길이로 높은 스코어를 달성합니다. **DAPO**는 동적 샘플링과 확장 클리핑으로 탐색성·안정성을 높였습니다. 길이 정규화 방법에 따라 Default GRPO(시퀀스 길이 정규화, 안정적이나 편향 큼), Dr. GRPO(정규화 없음, 편향 없으나 불안정), DAPO(전체 토큰 수 정규화, 질문별 편향)로 차이가 납니다.

### SFT는 기억하고 RL은 일반화를 촉진한다

토이 태스크에서 SFT와 RL을 비교한 결과, 분포 내 데이터에서는 SFT가 강하고 분포 외에서는 RL이 우수합니다. 즉 **SFT는 기억, RL은 일반화를 촉진**한다는 것이 시사됩니다. RLVR에 의해 새로운 사고가 획득되는가에 대해서는, 사전학습 모델에 존재하는 사고 패턴을 강화하고 있을 가능성이 제기되었습니다(pass@k가 사전학습 모델에 가까워짐). 반면 **ProRL**(Prolonged RL)은 엔트로피 붕괴(출력 분포가 다양성을 잃고 엔트로피가 급격히 저하되는 현상)를 방지해 베이스 모델에서 도달 불가능한 새 추론 전략을 학습할 수 있다고 주장합니다.

다양성을 유지한 채 강화학습하는 **Pass@K Training**(SimKO 등)은 학습 중 탐색을 촉진해 베이스 모델에 없던 추론 전략을 획득하고, 엔트로피 붕괴를 방지하며 Pass@1 성능도 향상시킵니다. 단 1개 훈련 샘플로도 데이터셋 전체 사용과 동등한 성능을 달성했다는 연구도 있습니다.

### RLVR의 향후 과제

(1) 일반화에 SFT가 좋은가, RL이 좋은가, 양쪽인가 — SFT로 새 사고 패턴을 학습시키고 RL로 강화하는 방식, 지속적 학습 기법이 이상적입니다. (2) 사전학습 모델은 무엇을 사용해야 하는가 — Qwen Family는 RL로 비약적 향상을 보이지만 Llama Family는 상대적으로 낮으며, 사전학습 분포에 따라 RL 효과가 다릅니다. (3) 보상은 결과에만 주는가, 중간 결과에도 주는가 — 도중 과정 보상이 효율적이겠지만 현재는 최종 결과 보상이 더 나은 성능을 보입니다. (4) 검증 불가능한 태스크에서의 추론 — 수학·코드 외의 영역으로의 확장이 과제입니다.

## 강화학습의 응용과 향후 방향

강화학습은 언어 영역을 넘어 확장되고 있습니다. **멀티모달 태스크**: 이미지·동영상 입력 추론 모델, 3D 씬 이해 향상(3D-R1 등). **에이전트 태스크**: WebAgent, GUI-Agent, OS 조작 강화학습(GUI-R1 등)으로 태스크 성공률 향상. **로봇 태스크**: VLA(Vision-Language-Action Model) 강화학습으로 장기 태스크 성능 비약적 향상, SFT Model에 없던 새 행동 학습(SimpleVLA-RL 등).

향후 방향: (1) **효율적 추론** — 강화학습으로 생성 길이가 길어져 간단한 문제에서도 길게 생각하거나 overthink 하는 문제를, 태스크 난이도에 따른 길이 제어로 해결해야 합니다. (2) **잠재 공간 추론** — 사고 과정을 토큰화하는 것은 비효율적이며(인간이 매번 말하면서 생각하는 것과 같음), 잠재 공간에서 추론해 추상적 사건을 효율적으로 계산해야 합니다. (3) **사전학습부터 강화학습** — 기존 사전학습은 대규모 데이터와 Next Token Prediction에 의존하여 교사 데이터 이상의 성능을 낼 수 없으나, 사전학습부터 RL을 수행하면 데이터 이상의 성능이 가능할 것으로 기대됩니다(Reinforcement Pre-Training).

## 정리

**RLHF**는 Alignment(인간의 의도대로 모델 학습)를 적용하는 한 방법으로, 인간의 피드백 데이터로 언어모델을 강화학습합니다. **DPO**는 지도학습으로 Alignment를 적용하는 기법으로 RLHF와 수학적으로 동등합니다. **RLVR**은 검증 가능한 보상으로 추론 능력을 향상시키며, GRPO, DAPO, Dr. GRPO 등의 종류가 있습니다. 강화학습은 언어를 넘어 멀티모달, 에이전트, 로봇 등으로 응용 범위를 넓혀가며, 효율적 추론, 잠재 공간 추론, 사전학습 단계부터의 강화학습 등 새로운 방향으로 연구가 진행되고 있습니다.

## References

[1] DeepMind, "MuZero: Mastering Go, chess, shogi and Atari without rules", https://deepmind.google/blog/muzero-mastering-go-chess-shogi-and-atari-without-rules/

[2] CNN.co.jp (2017), "AlphaGo 관련 기사", https://www.cnn.co.jp/tech/35080140.html

[3] TrackingAI, "AI Progress Tracking", https://www.trackingai.org/home

[4] Zhang, Kaiyan, et al. (2025), "A Survey of Reinforcement Learning for Large Reasoning Models", arXiv:2509.08827

[5] OpenAI (2022), "Instruction Following", https://openai.com/research/instruction-following

[6] Zhao, Wayne Xin, et al. (2023), "A Survey of Large Language Models", arXiv:2303.18223

[7] Touvron, Hugo, et al. (2023), "Llama 2: Open foundation and fine-tuned chat models", arXiv:2307.09288

[8] HuggingFace, "Math-Verify", https://github.com/huggingface/Math-Verify

[9] Lambert, Nathan, et al., "RLHF Book Chapter 14: Reasoning", https://rlhfbook.com/c/07-reasoning

[10] ARC Prize, "ARC Prize Leaderboard", https://arcprize.org/leaderboard

[11] 일본경제신문(2021), "한국에서 '대화AI' 폭주 — 머신러닝이 빠진 함정", https://www.nikkei.com/article/DGXZQOGM21B9V0R20C21A1000000/

[12] Wolfe, Cameron R. (2023), "Specialized LLMs: ChatGPT, LaMDA, Galactica, Codex, Sparrow, and More", https://cameronrwolfe.substack.com/p/specialized-llms-chatgpt-lamda-galactica

[13] Stanford Online (2023), "CS25 I Stanford Seminar - Transformers United 2023: Language and Human Alignment", https://www.youtube.com/watch?v=DJ1Yy6Aquug

[14] Anthropic, "hh-rlhf Dataset", https://huggingface.co/datasets/Anthropic/hh-rlhf

[15] Li, Junyi, et al. (2023), "HaluEval", arXiv:2305.11747

[16] Nangia, Nikita, et al. (2020), "CrowS-Pairs", arXiv:2010.00133

[17] Wang, Yuxia, et al. (2023), "Do-Not-Answer: A Dataset for Evaluating Safeguards in LLMs", arXiv:2308.13387

[18] OpenAI (2023), "Weak-to-Strong Generalization", https://openai.com/index/weak-to-strong-generalization/

[19] Wikipedia, "Existential risk from artificial intelligence", https://en.wikipedia.org/wiki/Existential_risk_from_artificial_intelligence

[20] CNET Japan (2018), "AI 자율주행차, '강화학습'으로 운전 방법을 20분 만에 습득", https://japan.cnet.com/article/35122203/

[21] CNET Japan (2017), "AI 관련 기사", https://japan.cnet.com/article/35094593/

[22] Boston Dynamics, https://bostondynamics.com/

[23] OpenAI, "ChatGPT", https://chatgpt.com/

[24] BrainPad (2023), "ChatGPT의 구조를 논문 기반으로 초상세하게 해설", https://blog.brainpad.co.jp/entry/2023/05/31/160719

[25] zero2one, "정책 경사법(Policy Gradient Methods)", https://zero2one.jp/ai-word/policy-gradient-methods/

[26] OpenAI (2017), "Learning from human preferences", https://openai.com/index/learning-from-human-preferences/

[27] Stiennon, Nisan, et al. (2020), "Learning to Summarize from Human Feedback", arXiv:2009.01325

[28] Ouyang, Long, et al. (2022), "Training Language Models to Follow Instructions with Human Feedback", arXiv:2203.02155

[29] Rafailov, Rafael, et al. (2023), "Direct Preference Optimization: Your Language Model is Secretly a Reward Model", arXiv:2305.18290

[30] Azar, Mohammad Gheshlaghi, et al. (2023), "A General Theoretical Paradigm to Understand Learning from Human Preferences", arXiv:2310.12036

[31] Ethayarajh, Kawin, et al. (2024), "KTO: Model Alignment as Prospect Theoretic Optimization", arXiv:2402.01306

[32] Saeidi, Amir, et al. (2024), "Insights into Alignment: Evaluating DPO and its Variants Across Multiple Tasks", arXiv:2404.14723

[33] Ivison, Hamish, et al. (2024), "Unpacking DPO and PPO: Disentangling Best Practices for Learning from Preference Feedback", arXiv:2406.09279

[34] Wang, et al. (2024), "Beyond Reverse KL: Generalizing Direct Preference Optimization with Diverse Divergence Constraints", ICLR 2024, arXiv:2309.16240

[35] Liu, et al. (2024), "Training Socially Aligned Language Models in Simulated Human Society"

[36] Dubois, Yann, et al. (2023), "AlpacaFarm: A Simulation Framework for Methods that Learn from Human Feedback", arXiv:2305.14387

[37] epoch.ai, "GPQA Diamond Benchmark", https://epoch.ai/benchmarks/gpqa-diamond

[38] Chollet, François (2023), ARC Prize 관련 포스트, https://x.com/fchollet

[39] Nikankin, A., et al. (2025), "Arithmetic without algorithms: Language models solve math with a bag of heuristics", arXiv:2410.21272

[40] Sutskever, Ilya (2024), "Sequence to Sequence Learning with Neural Networks", NeurIPS 2024

[41] OpenAI (2025), "GPT-4.5 System Card", https://cdn.openai.com/gpt-4-5-system-card-2272025.pdf

[42] OpenAI (2024), "Learning to Reason with LLMs", https://openai.com/index/learning-to-reason-with-llms/

[43] DeepSeek-AI, Guo, Daya, et al. (2025), "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning", arXiv:2501.12948

[44] Silver, David and Sutton, Richard (2025), "Welcome to the Era of Experience"

[45] Shao, Zhihong, et al. (2024), "DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models", arXiv:2402.03300

[46] oxen.ai (2024), "Why GRPO is Important and How it Works", https://www.oxen.ai/blog/why-grpo-is-important-and-how-it-works

[47] Gandhi, et al. (2025), "Cognitive Behaviors that Enable Self-Improving Reasoners, or, Four Habits of Highly Effective STaRs", arXiv:2503.01307

[48] Liu, Zichen, et al. (2025), "Understanding R1-Zero-like Training: A Critical Perspective", arXiv:2503.20783

[49] Yu, Qiying, et al. (2025), "DAPO: An Open-Source LLM Reinforcement Learning System at Scale", arXiv:2503.14476

[50] Chu, T., et al. (2025), "SFT Memorizes, RL Generalizes: A Comparative Study of Foundation Model Post-Training", arXiv:2501.17161

[51] Yue, Y., et al. (2025), "Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model?", https://openreview.net/pdf?id=4OsgYD7em5

[52] Liu, M., et al. (2025), "ProRL: Prolonged Reinforcement Learning Expands Reasoning Boundaries in Large Language Models", arXiv:2505.24864

[53] Peng, Ruotian, et al. (2025), "SimKO: Simple Pass@K Policy Optimization", arXiv:2510.14807

[54] Wang, Y., et al. (2025), "Reinforcement Learning for Reasoning in Large Language Models with One Training Example", arXiv 2025

[55] Huang, Ting, et al. (2025), "3D-R1: Enhancing Reasoning in 3D VLMs for Unified Scene Understanding", arXiv:2507.23478

[56] GUI-R1 (2025), "GUI-R1: A Generalist R1-Style Vision-Language Action Model For GUI Agents", arXiv:2504.10458

[57] Li, et al. (2025), "SimpleVLA-RL: Scaling VLA Training via Reinforcement Learning", arXiv:2509.09674

[58] Feng, et al. (2025), "Efficient Reasoning Models: A Survey", arXiv:2504.10903

[59] Zhu, et al. (2025), "A Survey on Latent Reasoning", arXiv:2507.06203

[60] Dong, et al. (2025), "Reinforcement Pre-Training", arXiv:2506.08007

[61] Ye, Seonghyeon, et al. (2023), "FLASK: Fine-grained Language Model Evaluation based on Alignment Skill Sets", arXiv:2307.10928

[62] Lambert, Nathan, et al. (2024), "RewardBench: Evaluating Reward Models for Language Modeling", arXiv:2403.13787

[63] Casper, Stephen, et al. (2023), "Open Problems and Fundamental Limitations of Reinforcement Learning from Human Feedback", arXiv:2307.15217

[64] Parrish, Alicia, et al. (2023), "Which Examples Should be Multiply Annotated? Active Learning When Annotators May Disagree", ACL Findings 2023

[65] Veselovsky, Veniamin, et al. (2023), "Artificial Artificial Artificial Intelligence: Crowd Workers Widely Use Large Language Models for Text Production Tasks", arXiv:2306.07899

[66] Zhou, Chunting, et al. (2023), "LIMA: Less Is More for Alignment", arXiv:2305.11206

[67] Shen, Mingyang, et al. (2023), "Bridging the Gap: A Survey on Integrating (Human) Feedback for Natural Language Generation", arXiv:2305.00955

[68] Gao, Leo, et al. (2022), "Scaling Laws for Reward Model Overoptimization", arXiv:2210.10760

[69] Wei, Alexander, et al. (2023), "Jailbroken: How Does LLM Safety Training Fail?", arXiv:2307.02483

[70] OpenAI (2023), "GPT-4 Technical Report", arXiv:2303.08774

[71] Wu, Zeqiu, et al. (2023), "Fine-Grained Human Feedback Gives Better Rewards for Language Model Training", arXiv:2306.01693

[72] Rame, Alexandre, et al. (2023), "Rewarded soups: towards Pareto-optimal alignment by interpolating weights fine-tuned on diverse rewards", arXiv:2306.04488

[73] Yuan, Zheng, et al. (2023), "RRHF: Rank Responses to Align Language Models with Human Feedback without tears", arXiv:2304.05302

[74] Irpan, Alex (2018), "Deep Reinforcement Learning Doesn't Work Yet", https://www.alexirpan.com/2018/02/14/rl-hard.html

[75] Zheng, Rui, et al. (2023), "Secrets of RLHF in Large Language Models Part I: PPO", arXiv:2307.04964

[76] Dong, Hanze, et al. (2023), "RAFT: Reward rAnked FineTuning for Generative Foundation Model Alignment", arXiv:2304.06767

[77] Yang, Kevin, et al. (2023), "RLCD: Reinforcement Learning from Contrast Distillation for Language Model Alignment", https://github.com/facebookresearch/RLCD

[78] Liu, Tianhao, et al. (2023), "Chain of Hindsight Aligns Language Models with Feedback", arXiv:2302.02676

[79] Peng, Baolin, et al. (2023), "Stabilizing RLHF through Advantage Model and Selective Rehearsal", arXiv:2309.10202

[80] Lin, Stephanie, et al. (2022), "TruthfulQA: Measuring How Models Mimic Human Falsehoods", ACL 2022

[81] Li, Junyi, et al. (2023), "HaluEval", EMNLP 2023

[82] Bai, Yuntao, et al. (2022), "Training a Helpful and Harmless Assistant with RLHF", arXiv:2204.05862 (Anthropic HH-RLHF Dataset)

[83] Nangia, Nikita, et al. (2020), "CrowS-Pairs", EMNLP 2020

[84] Rudinger, Rachel, et al. (2018), "Gender Bias in Coreference Resolution", https://github.com/rudinger/winogender-schemas

[85] Wang, Zhichao, et al. (2024), "A Comprehensive Survey of LLM Alignment Techniques: RLHF, RLAIF, PPO, DPO and More", arXiv:2407.16216