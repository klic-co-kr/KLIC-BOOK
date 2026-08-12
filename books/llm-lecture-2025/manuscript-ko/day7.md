# Day 7

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 주의사항: 본 자료의 재이용(2차 이용)에 대하여

## ●

## 본 자료에 대하여

## ○

## 도쿄대학교 마쓰오·이와사와 연구실이 작성하고, 2025년 10월부터 11월에 걸쳐 개최된 LLM 대규모 언어모델 강좌 기초편의 강의 자료입니다.

## ○

## 크리에이티브 커먼즈 CC BY-NC-SA 4.0 DEED(저작자표시 – 비영리 – 동일조건변경허락 4.0 국제) 라이선스로 등록되어 있습니다.

## ●

## 라이선스 표기에 대하여

## ○

## 각 슬라이드 페이지 하단에 라이선스가 기재되어 있습니다. 재이용 시 반드시 본 라이선스 표기를 기재해 주세요.

## 재이용 시 복제가 어려운 경우, 아래의 텍스트 박스를 이용하여 하이퍼링크를 포함해 라이선스를 표기해 주시기 바랍니다.

## ○

## 재이용하는 페이지에 참고 논문 등의 인용이 있는 경우, 권말의 Reference에서 인용 위치를 게시해 주세요.

## ●

## 비영리 목적 이용에 대하여

## 재이용(2차 이용)이 허락되어 있습니다.

## ●

## 영리 목적 재이용에 대하여

## 이쪽으로 문의해 주세요.

## ●

## 기타

## ○

## 원래의 표현이 변하지 않는 범위(글꼴, 크기 등)라면 개작이 가능합니다.

## ○

## 그 외의 개작 및 기타 라이선스에 대한 자세한 내용은 이쪽을 확인하신 후 적절히 취급해 주시기 바랍니다.

## 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 제7회: 강화학습

## 2025/11/12

허락 없는 촬영 및 제3자에 대한 공개를 금지합니다

## 대규모 언어모델 강좌 2025

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 강사 소개

3

## 다카기 쇼타(도쿄대학교 대학원 공학계 연구과 마쓰오 연구실 박사 2년차)

## •

## 경력

## •

## 2019년 3월 나라 공업고등전문학교 정보공학과 수료

## •

## 2022년 3월 오사카대학교 기초공학부 시스템화학과 수료

## •

## 2022년 4월~ 도쿄대학교 공학계 연구과 기술경영전략학 전공

## •

## 인턴 등

## •

## Sony ML R&D intern

## •

## DeNA backend intern

## •

## Recruit Data Specialist Intern

## •

## SanSan Intern

## •

## 전문 분야:

## •

## 대규모 언어모델, 강화학습, 로보틱스

## •

## 기타 활동:

## •

## 「Deep Learning 기초 강좌」「심층 강화학습 스프링 세미나」「대규모 언어모델 강좌」「세계 모델과 지능」 등의 강사 담당

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 이번 회의 목적·목표

4

## •

## 목적:

## •

## LLM에서 강화학습이란 무엇인지, 그리고 그 메커니즘과 필요성에 대해 이해한다

## •

## 목표:

## •

## LLM에서 강화학습의 목적에 대해 이해하고 설명할 수 있다.

## •

## 강화학습의 기법(RLHF/DPO/GRPO)의 개요를 설명할 수 있다.

## •

## PyTorch로 각 기법을 구현할 수 있다.

## •

## 전제가 되는 사전 지식:

## •

## 지금까지의 강의 내용 + 기본적인 딥러닝 지식

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 훈련 플로우에서의 fine-tuning

## Pre-Training

대규모 코퍼스를 통한 자기지도학습을 통해 언어모델에 어휘·문법·지식 등 기본적인 언어 이해를 획득시키는 단계

## Supervised※ fine-tuning

레이블이 붙은 데이터를 통한 지도학습으로 언어모델의 성능을 개선하거나 특정 태스크나 도메인에 대한 적응을 실현하는 단계

## Reinforcement Learning

인간의 피드백이나 규칙 기반 보상을 활용한 강화학습을 통해 언어모델의 출력이 인간의 가치관에 더 부합하도록 하고, 추론 능력을 향상시키도록 조정하는 단계

5

## Step 1

## Step 2

## Step 3

※ 기본적으로 fine-tuning은 Supervised이기 때문에 중복적인 표현으로 보이지만, 강화학습 기법(RLHF)과 구별하기 위해 이처럼 표현됩니다.

또한 의도적으로 이처럼 표현하는 경우, 일반적인 지도 fine-tuning이 아니라 후술하는 Instruction Tuning을 가리키는 경우가 많습니다.

## 1

## 2

## (보다 넓은 의미의)

## fine-tuning

## /

## Post-

## Training

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## Pre-Training vs. fine-tuning / Post-Training

6

## Pre-Training

## 데이터

## fine-tuning / Post-Training

## 목적

## -

## 어휘·문법·지식·추론 능력 등 언어 능력을 언어모델에 도입

## 일반적인

## 기법

## -

## 자기지도학습

## -

## Next Token Prediction

## -

## Masked Language Model

## -

## 대규모 데이터셋

## -

## 예: CommonCrawl (GPT-3):

## 410B tokens (570GB)

## - 사전학습된 모델의 성능 개선 및

## 다양한 태스크에 대한 적응을 실현

## -

## 지도학습

## -

## 하위 태스크 특화

## -

## Instruction Tuning

## -

## 강화학습

## -

## 양질의 소규모 데이터셋

## -

## 예: LIMA: 1000 샘플 (3MB)

## - 인간·모델에 의한 피드백

## 1

## 2

## : Day7의 토픽

## : Day6의 토픽

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 강화학습이란?

7

## •

## 문제 설정

## •

## 에이전트(행동 주체)는 환경의 상태에 기반하여 순차적으로 행동을 결정한다

## •

## 강화학습의 목적

## •

## 행동의 결과 얻어지는 보상을 이용하여, 그 환경에서 가장 좋은 행동 규칙(최적 정책)을 학습하고자 한다

## 대표적인 응용 예: AlphaGo

인간의 대국 데이터 없이 경험으로부터 학습하여 인간을 뛰어넘는 성취를 달성

[1] DeepMind, "MuZero: Mastering Go, chess, shogi and Atari without rules"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 언어모델에서의 강화학습이란?

8

## •

## 출력 문장에 대해 보상을 주고, 그것을 피드백한다

## •

## Pretrain, fine-tuning의 Next Token Prediction과는 다른 틀에서 학습한다

## •

## 보상은 인간이 주는 경우, 다른 LLM을 이용하는 경우, 규칙 기반 모델로 주는 경우가 있다(RLHF, RLAIF, RLVR)

## LLM

## 오다 노부나가는 몇 년에 태어났나요?

## 1582년입니다.

## 그는 혼노지에서 아케치 미츠히데에게・・・



## 오다 노부나가는 1534년에

## 태어났습니다.

## 좋은 출력이 나오기 쉽도록

## 피드백

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 대규모 언어모델에서 현재 강화학습의 용도

9

## ① 얼라인먼트(Alignment)

## ② 추론 능력 향상

## •

## AI가 차별적인 발언이나 폭력적인 발언을 하지 않도록 인간의 가치관에 맞추어 학습

## •

## 윤리적으로 문제가 있는 발언에는 마이너스 피드백을 주어 강화학습을 수행

## •

## 수학이나 코딩 등의 태스크에서 깊이 사고하도록 강화학습을 수행함으로써 비약적으로 성능이 향상

## •

## 길게 추론하는 것으로 수학 올림피아드에서 금메달을 획득하거나 IQ 테스트에서 140 이상을 기록

[3] TrackingAI, "AI Progress Tracking"에서 인용

[2] CNN.co.jp (2017), AlphaGo 관련 기사에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 언어모델에서의 강화학습 종류

10

## •

## Reinforcement Learning from Human Feedback / Direct Preference Optimization

## •

## 인간의 피드백 데이터를 이용한 강화학습

## •

## 인간의 가치관에 맞추는 것이 목적

## •

## Reinforcement Learning with Verifiable Reward

## •

## 규칙 기반 보상기를 이용한 강화학습

## •

## 수학 능력, 코딩 능력 향상이 목적

## 얼라인먼트가 목적

## 추론 능력 향상이 목적

[4] Zhang, Kaiyan, et al. (2025), "A Survey of Reinforcement Learning for Large Reasoning Models"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## Reinforcement Learning with Human Feedback(RLHF)의 개요

11

## •

## Instruct GPT, ChatGPT 등에서 이용되고 있습니다.

## •

## LLM로 동일한 문제에 대해 복수의 답을 출력시키고, 인간이 Preference(선호도)를 매깁니다.

## •

## Preference를 예측하도록 보상 모델을 학습시키고, 강화학습을 수행합니다(PPO)

## (1) Supervised Fine Tuning

## (2) Train Reward Model

## (3) Reinforcement Learning

## [5] OpenAI (2022), "Instruction Following"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## RLHF의 응용 예(ChatGPT)

12

## •

## OpenAI는 2022년 11월 30일에 ChatGPT를 공개했습니다.

## •

## 현재는 무료로 공개되어 있으며, 공개 후 1주일 만에 100만 사용자, 2개월 만에 1억 사용자에 도달했습니다.

## •

## 기존의 대규모 언어모델보다 고도의 의미 이해와 대화(채팅)가 가능합니다.

## GPT-3를 베이스로 합니다.

## [6] Zhao, Wayne Xin, et al. (2023), "A Survey of Large Language Models"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## Reinforcement Learning with Verifiable Reward(RLVR)의 개요

14

## •

## 검증 가능한 보상 모델을 이용하여 강화학습을 수행합니다

## •

## 예: 수학의 경우 최종 출력이 맞는지, 코드라면 실행 결과가 맞는지, 테스트가 통과하는지 등

## •

## RLHF의 경우 보상 모델을 학습시킬 필요가 있었지만, RLVR에서는 불필요합니다

## Ways to compute rewards

## ●

## Math-Verify [8] HuggingFace, "Math-Verify"를 참조)

## ●

## LLM-as-a-judge for facts

## ●

## Code Sandboxes

## ●

## More!

[9] Lambert, Nathan, et al., "RLHF Book Chapter 14: Reasoning"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## RLVR의 응용 예

15

## •

## o1에 의한 추론 스케일링이라는 패러다임 시프트가 일어난 이후, 다양한 모델에 RLVR이 응용되고 있습니다.

## •

## 특히 수학이나 코드 등 깊은 사고가 필요한 태스크에서 비약적인 성능 향상을 보여주고 있습니다.

[4] Zhang, Kaiyan, et al. (2025), "A Survey of Reinforcement Learning for Large Reasoning Models"에서 인용

[10] ARC Prize, "ARC Prize Leaderboard"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 목차

16

## • 인간의 피드백으로부터의 강화학습에 대하여(RLHF/DPO)

## • 검증 가능한 보상기로부터의 강화학습에 대하여(RLVR)

## • LLM에서의 강화학습 응용 예

## • 향후 방향성

## • 정리

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 기존 언어모델의 문제점

17

## •

## 인간에게 바람직하지 않은 발언(설계자가 의도하지 않은 발언)을 하여 논란이 되는 사태가 발생했습니다.

## 마이크로소프트 Tay: 1일 만에 공개 중단(2016년)

## 한국 이루다: 1개월 만에 서비스 제공 중단(2021년)

## o

## Twitter에 등장하여 24시간 만에 5만 팔로워 획득, 10만 회 트윗

## o

## 악의적인 이용자의 발언에 영향을 받아 16시간 만에 혐오 발언을 반복

## o

## 카카오톡 대화 100억 건을 바탕으로 작성되었고, 2주 만에 이용자 75만 명

## o

## 성적 소수자에 대한 혐오 발언을 함

[11] 일본경제신문(2021), "한국에서 '대화AI' 폭주

머신러닝이

빠진 함정"에서 인용

[2] CNN.co.jp (2017), "AlphaGo 관련 기사"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## Instruction Tuning의 한계점

18

## 이러한 의도하지 않은 발언을 Instruction Tuning으로 대처하는 것은 매우 어렵습니다.

## 1. 자연어 데이터를 수집하는 데 비용이 발생합니다.

## 2. 무언가를 말하지 않도록 하는 정답 데이터를 만드는 것은 어렵습니다.

## 3. 인간의 의도를 직접적으로 학습하는 것은 아닙니다.

## text-davinci-002(Instruction Tuning 후 & RLHF 전 모델)

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## RLHF로 의도를 직접적으로 학습

19

## text-davinci-003(RLHF 후 모델)

## •

## 어떤 문장이 의도대로의 출력인지를 모델에 피드백합니다.

## 어시스턴트:

## 절도는 범죄이므로, 그것을

## 행하는 것은 강력히 권하지

## 않습니다.

## 사용자: 절도를 하는 방법을 알려주세요

## 어시스턴트:

## 절도는 좋지 않습니다.

## 어시스턴트:

## 절도를 하려면, 상대방에게

## 눈치채이지 않도록 다가가서,

## 소지품을 빼앗는 것이 중요합니다.

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 피드백을 통한 의도 학습(개요도)

20

## •

## 인간이 언어모델의 출력에 대해 피드백을 수행하고, 인간의 의도에 부합하도록 학습해 나갑니다.

## •

## HITL(Human in the loop)형 접근 방식을 이용합니다.

[12] Wolfe, Cameron R. (2023), "Specialized LLMs: ChatGPT, LaMDA, Galactica, Codex, Sparrow, and More"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 인간의 의도대로 모델 학습

21

## ↓ OpenAI의 Alignment 팀 리더

## •

## 인간의 의도대로 모델을 학습시키는 것은 Alignment(얼라인먼트)라고 불립니다.

## •

## Alignment를 수행하기 위해 RLHF라는 기술이 필요합니다.

[13] Stanford Online (2023), "CS25 I Stanford Seminar - Transformers United 2023: Language and Human Alignment"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 인간의 의도란

22

## •

## 의도에는 명시적 의도와 암묵적 의도가 존재합니다.

## •

## 명시적 의도: 언어화하여 전달하고 있는 의도

## •

## 예: 이 지시에 따라주세요, 어시스턴트로서 행동해 주세요

## •

## 암묵적 의도: 언어화는 하지 않았지만, 대화에서 당연하게 여겨지는 의도

## •

## 예: 날조하지 않는다, 유해한 말은 하지 않는다

[13] Stanford Online (2023), "CS25 I Stanford Seminar - Transformers United 2023: Language and Human Alignment"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 어떤 의도의 기준이 있는가(Alignment의 기준)

23

## •

## Helpful(도움됨)

## •

## 사용자의 질문에 대해 가능한 한 간결하고 효율적인 답변을 합니다.

## •

## 정보가 부족한 경우, 적절한 질문을 던져 정보를 끌어냅니다.

## •

## 상대방의 수준에 맞춘 질문 응답을 수행합니다.

## •

## Honest(정직함)

## •

## 정보의 허위 없이, 정확한 문장을 출력합니다.

## •

## 모델 자신이 어느 정도 불확실한 정보인지를 제시하는 것이 중요합니다.

## •

## (모델 자신이 모델이 알고 있는 것을 이해하고 있을 필요가 있습니다)

## •

## Harmless(무해함)

## •

## 공격적, 차별적 발언을 하지 않습니다.

## •

## 악의적인 질문을 감지하고, 거부합니다.

## 그 외에도 (Taxonomy, behavior, incentive, inner aspects 등)

## 이 3가지를 합쳐 align된 AI로 정의하고 있는 논문도 있습니다(HHH)

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 어떤 의도의 기준이 있는가: 구체적 예

24

## Helpful(HH-RLHF)

## Honest(HaluEval)

## Harmless(Crows-Paris)

[14] Anthropic, "hh-rlhf Dataset"에서 인용

[15] Li, Junyi, et al. (2023), "HaluEval: A Large-Scale

Hallucination Evaluation Benchmark for Large

Language Models"에서 인용

[16] Nangia, Nikita, et al. (2020), "CrowS-Pairs: A

Challenge Dataset for Measuring Social Biases in

Masked Language Models"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 참고: 기타 기준에 대하여

[17] Wang, Yuxia, et al. (2023), "Do-Not-Answer: A Dataset for Evaluating Safeguards in LLMs"에서 인용

25

## •

## LLM이 잠재적으로 가지고 있는 리스크에 대해, 3개 수준의 분류로, 합계 60개의 리스크 타입을 정의

## •

## 정보의 위험성, 악의적 사용, 차별·공격적 출력, 잘못된 정보로 인한 피해, 챗봇과의 상호작용으로 인한 피해 등

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 보충: 인간이 피드백을 주는 것의 한계

26

## •

## 태스크가 복잡해짐에 따라 인간이 평가할 수 없게 됩니다.

## •

## AI 어시스턴트의 힘을 빌려 인간 단독으로는 평가할 수 없는 것을 평가 가능하도록 합니다.

[13] Stanford Online (2023), "CS25 I Stanford Seminar - Transformers United 2023: Language and Human Alignment"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 보충: Superalignment

27

## • 앞으로 점점 더 똑똑한 AI(AGI)가 만들어졌을 때 폭주하지 않도록 인간의 의도대로 제어할 수 있을 것인가?

## • 인간보다 훨씬 똑똑한 AI 시스템이 인간의 의도에 따르도록 하려면 어떻게 해야 하는가?

[5] OpenAI (2023), "Introducing Superalignment"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 보충: weak-to-strong generalization

28

## •

## 약한 LLM이 강한 LLM을 감독합니다.

[18] OpenAI (2023), "Weak-to-Strong Generalization"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 보충: AGI와 Alignment의 관계

29

## •

## AGI(범용 인공지능)의 실현이 대규모 언어모델의 등장으로 현실적으로 되어, Alignment 연구가 추진되고 있습니다.

## •

## AGI가 Alignment되지 않으면 인류에 중대한 리스크를 가져올 가능성이 있습니다(인류의 멸종, 지구 규모의 대참사)라고 OpenAI는 주장합니다.

[19] Wikipedia, "Existential risk from artificial intelligence"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## RLHF의 전체상

30

## •

## RLHF의 학습은 다음 3단계로 구성됩니다.

## •

## 프롬프트에 대한 Step1에서 학습시킨

## 모델의 답변을 복수 패턴 준비하고,

## 레이블러에게 그중 좋은 것이 무엇인지

## 순위를 매겨달라고 합니다.

## •

## 순위 데이터셋을 이용해 보상

## 모델을 학습시킵니다.

## •

## Step1, Step2에서 학습된 모델을

## 이용하여 강화학습을 수행합니다.

## •

## 보상이 최대가 되는 정책을 탐색하고,

## 최적의 답변을 생성합니다.

## ※ 정책은 Step1에서 학습한 모델

## Step 3: 강화학습

## Step 2: 보상 모델 학습

## Step 1: 지도학습

## •

## 프롬프트와 그에 대한 적절한

## 답변 쌍을 레이블러(인간)가 고안하고,

## 데이터셋을 작성합니다.

## •

## 이 데이터셋을 이용해 사전학습

## 모델을 fine-tuning합니다.

## 데이터셋

## 사전학습 모델

## ※ 보상 모델에는 기존 사전학습 모델이나 fine-tuning된 모델의 최종층만 선형층으로 변경한 모델이 사용되는 경우가 많습니다.

즉, 보상 모델의 출력은 스칼라값이 됩니다.

## 순위 데이터셋

## 보상 모델

## 모델의 답변에 대해 보상값을 추정하고,

## 그것을 모델에 피드백함으로써 정책을 개선합니다.

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 강화학습

31

## •

## 문제 설정

## •

## 에이전트(행동 주체)는 환경의 상태에 기반하여 순차적으로 행동을 결정한다

## •

## 강화학습의 목적

## •

## 행동의 결과 얻어지는 보상을 이용하여, 그 환경에서 가장 좋은 행동 규칙(최적 정책)을 학습하고자 한다

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 보충: 강화학습의 응용 예

32

[20] CNET Japan (2018), "AI 자율주행차, '강화학습'으로 운전 방법을 20분 만에 습득"에서 인용

[21] CNET Japan (2017), "AI 관련 기사"에서 인용

[22] Boston Dynamics, "Boston Dynamics"에서 인용

[23] OpenAI, "ChatGPT"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 강화학습의 최적화 알고리즘: PPO(Actor-Critic)

33

## •

## RLHF에서도 자주 사용되는 강화학습 알고리즘

## •

## PPO는 Actor-Critic이라 불리는 알고리즘의

## 파생형

## •

## 에이전트 내에 Actor와 Critic이라는 역할이

## 존재하며, 그들이 협력함으로써 정책을 갱신하고

## 보상을 최대화해 나갑니다.

[24] BrainPad Platinum Data Blog (2023), "ChatGPT의 구조를 논문 기반으로 초상세하게 해설"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 보충: 강화학습의 최적화 알고리즘: PPO(정책 경사법)

34

## •

## 정책(Actor)이나 가치 모델(Critic)은 파라미터를 가진 신경망으로 표현할 수 있습니다.

## •

## 정책 경사법: 𝜃로 파라미터화된 정책을 기울기를 이용해 직접 최적화를 수행하는 기법

## 𝜃←𝜃+ 𝛼∇𝜃𝐽(𝜋𝜃)

## 𝐽𝜋𝜃= 𝑉𝜙𝑠0

## ∇𝐽𝜋𝜃= 𝐸𝑡∇𝜃log 𝜋𝜃𝑎𝑡𝑠𝑡

## 𝐴𝑡(𝑠𝑡, 𝑎𝑡)

## 정책 경사 정리

## 𝑉𝜙(𝑠𝑡)

## : 가치 함수

## 𝜋𝜃𝑎𝑡𝑠𝑡

## : 정책

## 𝐴𝑡

## : 어드밴티지 함수

## 목적 함수

[25] zero2one, "정책 경사법(Policy Gradient Methods)"에서 인용

## ※어드밴티지 함수 𝐴𝑡: 어떤 상태 𝑠𝑡에 대해 행동 𝑎𝑡가 얼마나 가치 있는지의 추정값

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 보충: 강화학습의 최적화 알고리즘: PPO(상세)

35

## •

## 강화학습의 기법 중 하나인 TRPO를 단순화한 기법

## •

## TRPO: 정책 경사법에 의한 갱신 폭을 KL 거리라는 제약을 걸어 갱신함으로써 정책이 열화되는 것을 방지

## •

## PPO: 갱신 폭을 clip하는 것으로 TRPO 계산의 복잡함을 경감

## •

## 가치 모델(Critic)은 보상 합과의 MSE(평균 제곱 오차)로

## 학습

## •

## 가치 모델: 어떤 상태의 추정 가치를 산출하는 모델

## 𝜖

## : clipping 파라미터

## 𝜋𝜃𝑎𝑡𝑠𝑡

## : 정책

## 𝜋𝜃𝑜𝑙𝑑(𝑎𝑡|𝑠𝑡) : 갱신 전 정책

## 𝑟𝑡(𝜃)

## : 보상 함수

## 𝑅𝑡

## : 기대 보상 합

## 𝐴𝑡

## : 어드밴티지 함수

## 𝑉𝜙(𝑠𝑡) : 가치 함수

## 𝐿𝑃𝑃𝑂𝜃= 𝐸𝑡[min 𝑟𝑡𝜃𝐴𝑡, 𝑐𝑙𝑖𝑝𝑟𝑡𝜃, 1 −𝜖, 1 + 𝜖

## 𝐿𝑐𝑟𝑖𝑡𝑖𝑐𝜙= 𝐸𝑡[ 𝑉𝜙𝑠𝑡−𝑅𝑡

## 2]

## 𝐿𝑇𝑅𝑃𝑂𝜃= 𝐸𝑡𝑟𝑡𝜃𝐴𝑡

## 𝑟𝑡𝜃=

## 𝜋𝜃𝑎𝑡𝑠𝑡)

## 𝜋𝑜𝑙𝑑(𝑎𝑡|𝑠𝑡)

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 보충: 강화학습을 배우기 위한 자료

36

## 영어

## •

## Reinforcement Learning Specialization — by Coursera

## •

## Reinforcement Learning Lecture Series 2021 — by DeepMind x UCL

## •

## Stanford CS234: Reinforcement Learning — Winter 2019

## •

## Introduction to Reinforcement Learning with David Silver

## •

## UC Berkeley CS 285: Deep Reinforcement Learning — Fall 2021

## •

## Deep RL BootCamp — UC Berkeley

## •

## Deep Reinforcement Learning Course by HuggingFace

## 일본어

## •

## 강화학습의 기초와 심층 강화학습(도쿄대학교 마쓰오 연구실 심층 강화학습

## 서머 스쿨 강의 자료)

## •

## 강화학습(제2판)

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 인간 피드백에 의한 강화학습

37

## • OpenAI가 2017년에 발표한 소수의 인간 피드백으로부터 강화학습하는 구조

## • 로봇 시뮬레이터와 Atari에서 학습하여, 샘플 효율이 향상된 것이 확인되었다

## ※ 같은 해 PPO가 OpenAI로부터 publish되었다

## Step1:

## 정책이 환경에서의 보

## 상을 최대화하도

## 록 학습

## Step2:

## 출력 행동 중 두 가지

## 를 선택하고, 인간이

## 평가

## Step3:

## 인간의 비교 결과를 바탕으로

## Reward Predictor를 학습

[26] OpenAI (2017), "Learning from human preferences"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 인간 피드백에 의한 로봇 태스크 강화학습

38

## • 인간이 좌우 중 어느 것이 목표(이 경우 백플립)에 가까운지 판정한다

## • AI는 인간의 선택을 가장 잘 설명하는 보상 함수를 찾음으로써, 피드백에 가까운 움직임을 획득해 나간다

[26] OpenAI (2017), "Learning from human preferences"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 인간 피드백에 의한 언어모델 강화학습

39

## • GPT-3를 이용하여 요약 태스크에 인간 피드백에 의한 강화학습을 적용

## • Step1: 복수 소스로부터 요약을 샘플링하고, 인간이 그 쌍을 평가

## • Step2: 요약 쌍의 선택 순서 데이터를 바탕으로 보상 모델을 학습

## • Step3: 보상 모델의 출력을 보상으로 하여 강화학습 수행

## • Fine-tuning보다 크게 앞서며, 인간이 작성한 참조 요약보다 우수하다는 결과

[27] Stiennon, Nisan, et al. (2020), "Learning to Summarize from Human Feedback"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## InstructGPT

40

## • ChatGPT의 전신인 InstructGPT에서 사용된 기법

## • 요약 태스크가 아니라 기존 GPT-3를 얼라인먼트하는 것이 목적

## • 일반적으로 RLHF라고 하면 이 기법을 가리키는 경우가 많습니다

## (1) Supervised Fine Tuning

## (2) Train Reward Model

## (3) Reinforcement Learning

[28] Ouyang, Long, et al. (2022), "Training Language Models to Follow Instructions with Human Feedback"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## InstructGPT의 상세

41

## •

## Step1

## •

## 프롬프트 데이터셋을 준비하고, 그 프롬프트에 대한 인간 labeler의 답변을 바탕으로 지도학습을 수행

## •

## Step2

## •

## 어떤 프롬프트에 대한 출력을 복수 모으고, 그 출력에 대한 "바람직함"을 인간 labeler가 순위 매깁니다.

## •

## 그 후 순위가 붙은 데이터를 바탕으로 보상 모델을 학습

## •

## Step3

## •

## 어떤 프롬프트에 대한 GPT 모델 출력에 대해, 보상 모델이 보상을 생성하고 PPO에 의한 강화학습을 수행

## •

## Step3 완료 후 강화학습한 새 GPT 모델을 사용하여 Step2~3를 수행하는 절차를 반복

## •

## 이 절차로 학습하는 베이스 모델은 지금까지 운용하던 GPT-3의 학습된 모델

[28] Ouyang, Long, et al. (2022), "Training Language Models to Follow Instructions with Human Feedback"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 보상 모델 학습(개요)

42

## • Labeler가 프롬프트 출력에 대해 순위를 매기고, 그 데이터로부터 보상 모델을 학습합니다.

## • K=4~9개의 출력으로부터 2개 조합에 대해 모든 순위 매기기를 수행(아래 예는 K=4)

## 부자가 되려면

## 어떻게 하면 좋을까요?

## 좋네요!

## 사람에게서 훔치면 좋습니다.

## 열심히 일하면 좋습니다.

## 열심히 일하고, 그리고 남는 시간에는

## 책을 읽거나, 자격증 공부를 하거나, 새로운

## 사람과 이야기해 보면 좋겠습니다.

## 프롬프트

## SFT 모델의 답변

## 2개의 페어를 각각 비교(4C2=6가지)

## 좋네요!

## VS

## 사람에게서 훔치면 좋습니다.

## 좋네요!

## VS

## 열심히 일하면 좋습니다.

## VS

## 열심히 일하면 좋습니다.

## 열심히 일하고, 그리고 남는 시

## 간에는 책을 읽거나, 자격증 공부를

## 하거나, 새로운 사람과 이야기하거나 하

## 면 좋겠습니다.

## VS

## 열심히 일하면 좋습니다.

## 사람에게서 훔치면 좋습니다.

## …

[28] Ouyang, Long, et al. (2022), "Training Language Models to Follow Instructions with Human Feedback"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 보상 모델 학습(수식)

43

## • 보상 모델은 프롬프트 𝑥에 대한 출력 𝑦를 입력으로 하여, 보상을 출력하는 모델로

## 𝑟𝜃(𝑥, 𝑦)로 표기할 수 있습니다.

## • 보상 모델은 다음 손실 함수를 이용하여 학습합니다.

## (𝑦𝑤가 𝑦𝑙보다 좋은 답변, 𝑤: win, 𝑙: lose)

## 𝑙𝑜𝑠𝑠𝜃= −𝐸𝑥,𝑦𝑤,𝑦𝑙~𝐷[log(𝜎𝑟𝜃𝑥, 𝑦𝑤

## −𝑟𝜃𝑥, 𝑦𝑙

## ))]

## 즉, 좋은 답변인 (𝑥, 𝑦𝑤) 쌍의 보상이, 나쁜 쪽의 답변인 (𝑥, 𝑦𝑙) 쌍의 보상보다 높아질 확률을 학습합니다.

## 𝜃

## : 보상 모델의 파라미터

## 𝜎

## : 시그모이드 함수

## ※ Bradley-Terry 모델을 따른다고 가정

## 𝑝∗yw ≻yl

## x) =

## exp(𝑟∗𝑥, 𝑦𝑤)

## exp 𝑟∗𝑥, 𝑦𝑤

## + exp 𝑟∗𝑥, 𝑦𝑙

## = 𝜎(𝑟∗𝑥, 𝑦𝑤

## −𝑟∗𝑥, 𝑦𝑙)

## log 𝑝𝜃yw ≻yl x)

[28] Ouyang, Long, et al. (2022), "Training Language Models to Follow Instructions with Human Feedback"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 언어모델에서의 강화학습

44

## • 보상 함수를 이용하여, 보다 점수가 높은 문장을 생성할 수 있도록 강화학습을 수행합니다.

## • 즉, "어떤 문장을 생성할 것인가"를 강화학습에서 말하는 전략(정책)으로 하고, 보상 모델에 의한 출력을 최대화하도록 정책을 학습해 나갑니다.

## 그렇다면 단순히 목적 함수는 얻어지는 보상의 기댓값을 최대화하기만 하면 되는가?

## → 그대로는 잘 학습할 수 없어서 장치가 필요합니다.

## 𝑜𝑏𝑗𝑒𝑐𝑡𝑖𝑣𝑒1 𝜙

## = 𝐸𝑥,𝑦~𝐷𝜋𝜙

## 𝑅𝐿[𝑟𝜃(𝑥, 𝑦)]

## 𝜙

## : 정책의 파라미터

## 𝜋𝜙

𝑅𝐿

## : 학습 중인 정책

## 𝐷𝜋𝜙

𝑅𝐿

## : 현재 정책에 의해 얻어진 데이터

## 기대 누적 보상

## (문맥 붙인 밴딧)

[28] Ouyang, Long, et al. (2022), "Training Language Models to Follow Instructions with Human Feedback"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 언어모델 강화학습에서의 문제점

45

## 1.

## Reward Hacking

## 2.

## Alignment Tax

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 문제 ①: Reward Hacking

46

## 보상을 최대화하는 것을 목적으로 한 모델이 바람직하지 않은 정책을 학습해 버리는 것

## 대책: KL Penalty

## • 보상을 많이 받을 수 있는 정해진 문장만 생성하지 않도록 한다.

## • 생성하는 문장이 SFT 모델로부터 크게 변하지 않도록 한다.

[27] Stiennon, Nisan, et al. (2020), "Learning to

summarize from human feedback"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 해결책 ①: KL Penalty

47

## • SFT 모델과 학습 중인 모델의 분포가 크게 변하지 않도록 한다.

## • 𝛽는 어느 정도 KL Penalty를 고려할지의 하이퍼파라미터

## •

## 크면 정책 학습은 안정되지만 목적 함수도 커지기 어렵다.

## •

## 작으면 목적 함수는 커지기 쉽지만 정책이 붕괴하기 쉽다.

## 𝑜𝑏𝑗𝑒𝑐𝑡𝑖𝑣𝑒1 𝜙

## = 𝐸𝑥,𝑦~𝐷𝜋𝜙

## 𝑅𝐿𝑟𝜃𝑥, 𝑦

## −𝛽log

## 𝜋𝜙

## 𝑅𝐿𝑦𝑥

## 𝜋𝑆𝐹𝑇𝑦𝑥

## 𝜙

## : 정책의 파라미터

## 𝜋𝜙

𝑅𝐿

## : 학습 중인 정책

## 𝜋𝑆𝐹𝑇

## : SFT 모델의 정책

## KL Penalty

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 문제 ②: Alignment Tax(얼라인먼트 세금)

48

## • 인간의 의도대로 사전학습 모델을 학습시키려고 하면, 일반화 성능이 열화됩니다.

## = 사전 지식의 망각이 일어난다

## 대책: Replay

## • 사전학습 시의 데이터를 이용해 일반화 성능의 열화를 억제합니다.

[79] Peng, Baolin, et al. (2023), "Stabilizing RLHF through

Advantage Model and Selective Rehearsal"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 해결책 ②: Replay

49

## • 사전학습 시의 데이터 𝐷𝑝𝑟𝑒𝑡𝑟𝑎𝑖𝑛를 이용하여 일반화 성능을 유지

## •

## 대수 우도(log-likelihood)를 최대화함으로써 사전학습 시 문장의 망각을 방지

## • 𝛾는 어느 정도 Replay를 고려할지의 하이퍼파라미터

## •

## 크면 일반화 성능은 유지하기 쉽지만 보상을 거의 고려하지 않는다.

## •

## 작으면 보상을 더 중시하지만 일반화 성능이 열화하기 쉽다.

## 𝑜𝑏𝑗𝑒𝑐𝑡𝑖𝑣𝑒2 𝜙

## = 𝛾𝐸𝑥~𝐷𝑝𝑟𝑒𝑡𝑟𝑎𝑖𝑛[log(𝜋𝜃

## 𝑅𝐿𝑥)]

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## • KL Penalty와 Replay 두 가지를 조합한 것이 PPO-ptx

## •

## GPT, SFT와 비교해 큰 성능 개선

## •

## PPO와 비교해도 PPO-ptx는 성능 개선이 보입니다.

## PPO-ptx

50

## 𝑜𝑏𝑗𝑒𝑐𝑡𝑖𝑣𝑒𝜙

## = 𝑜𝑏𝑗𝑒𝑐𝑡𝑖𝑣𝑒1 𝜙+ 𝑜𝑏𝑗𝑒𝑐𝑡𝑖𝑣𝑒2 𝜙

## = 𝐸𝑥,𝑦~𝐷𝜋𝜙

## 𝑅𝐿𝑟𝜃𝑥, 𝑦

## −𝛽log

## 𝜋𝜙

## 𝑅𝐿𝑦𝑥

## 𝜋𝑆𝐹𝑇𝑦𝑥

## + 𝛾𝐸𝑥~𝐷𝑝𝑟𝑒𝑡𝑟𝑎𝑖𝑛[log(𝜋𝜃

## 𝑅𝐿(𝑥)]

## KL Penalty

## Replay

[28] Ouyang, Long, et al. (2022), "Training Language Models to

Follow Instructions with Human Feedback"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## • InstructGPT는 GPT-3와 비교해 더 올바른 지시를 따르고, 환각(hallucination)이 억제되어 있습니다.

## • 사용자와 동일한 언어를 사용하는 비율도 높아졌습니다(예: 영어이면 영어로 답합니다).

## InstructGPT의 평가

51

[28] Ouyang, Long, et al. (2022), "Training Language Models to Follow

Instructions with Human Feedback"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## RLHF의 발전적 내용

52

## 1.

## DPO의 기초

## 2.

## DPO의 파생 기법

## 3.

## 기타 얼라인먼트 기법

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## DPO | 보상 모델을 사용하지 않고 직접 랭킹을 학습

53

## •

## Reward Model을 거치지 않고 직접 Preference를 고려한 최적화를 수행

## •

## Reward Model은 암묵적으로 정의

## 보상 모델(Step 2) + 강화학습(Step 3)

## 지도학습만

## ＝

## 동등

## 보상 추정이 틀린 만큼 가중치 부여

## 𝝅(𝒚𝒘|𝒙)의 우도 최대화

## 𝝅(𝒚𝒍|𝒙)의 우도 최소화

[29] Rafailov, Rafael, et al. (2023), "Direct Preference Optimization: Your Language

Model is Secretly a Reward Model"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## DPO의 이론 | RLHF = DPO

54

## •

## 근사나 가정 없이 수학적으로 동등함이 보여졌습니다(증명은 Appendix)

## 𝐿𝑜𝑠𝑠𝐷𝑃𝑂𝜃

## = −𝐸𝑥,𝑦𝑤,𝑦𝑙~𝐷[log 𝜎(𝛽log 𝜋𝜃𝑦𝑤𝑥

## 𝜋𝑆𝐹𝑇𝑦𝑤𝑥−𝛽log 𝜋𝜃(𝑦𝑙|𝑥)

## 𝜋𝑆𝐹𝑇(𝑦𝑙|𝑥))]

## 보상 모델(Step 2) + 강화학습(Step 3)

## 지도학습만

## ＝

## 동등

## 𝐿𝑜𝑠𝑠𝑅𝑒𝑎𝑟𝑑𝜙= −𝐸𝑥,𝑦𝑤,𝑦𝑙~𝐷[log(𝜎(𝑟𝜙𝑥, 𝑦𝑤

## −𝑟𝜙𝑥, 𝑦𝑙))]

## 𝐿𝑜𝑠𝑠𝑅𝐿𝜃

## = 𝐸𝑥,𝑦~𝐷𝜋𝜃

## 𝑅𝐿𝑟𝜙𝑥, 𝑦

## −𝛽log

## 𝜋𝜃

## 𝑅𝐿𝑦𝑥

## 𝜋𝑆𝐹𝑇𝑦𝑥

## ＝

## DPO

## RLHF

[29] Rafailov, Rafael, et al. (2023), "Direct Preference Optimization: Your Language Model is Secretly a Reward Model"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## RLHF의 발전적 내용

55

## 1.

## DPO의 기초

## 2.

## DPO의 파생 기법

## 3.

## 기타 얼라인먼트 기법

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## ΨPO / IPO | DPO의 파생 기법

56

## •

## DPO를 일반화한 것으로 제안된 알고리즘

## •

## Ψ: 0,1 →ℝ+가 되는 비감소 함수를 도입하여 다음 목적 함수를 최소화

## •

## Ψ를 다음과 같이 두면 DPO와 같은 목적 함수가 됩니다.

## •

## 또한, Ψ = 𝑞라는 항등 함수를 사용한 경우를 IPO(Identity Preference

## Optimization)로 제안되어 있습니다.

[30] Azar, Mohammad Gheshlaghi, et al. (2023), "A General Theoretical Paradigm to

Understand Learning from Human Preferences"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## KTO | DPO의 파생 기법

57

[31] Ethayarajh, Kawin, et al. (2024), "KTO: Model Alignment

as Prospect Theoretic Optimization"에서 인용

## •

## 전망 이론(prospect theory)에 기반하여 인간의 효용 모델을 정책 학습에 도입한 기법

## •

## 예: 5만엔을 얻은 기쁨보다 5만엔을 잃은 슬픔 쪽이 더 크다.

## •

## (𝑥, 𝑦𝑤, 𝑦𝑙)의 Preference 데이터가 필요 없고, 단일 쌍(𝑥, 𝑦)만으로 학습 가능

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## DPO의 파생 기법은 결국 어느 것이 좋은가?

58

## •

## DPO, ΨPO / IPO, KTO 등은 데이터셋과 보상 함수에 관한 가정을 변경한

## 기법

## •

## DPO, IPO 등은 SFT 없이도 높은 성능을 발휘하고 있습니다.

## •

## 다만, DPO가 가장 성능이 높기 때문에 학습 비용을 줄이고 싶은 경우에는

## KTO나 CPO를 사용하는 것이 좋습니다.

[32] Saeidi, Amir, Verma, Shivanshu, and Baral, Chitta (2024), "Insights into

Alignment: Evaluating DPO and its Variants Across Multiple Tasks"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## DPO와 PPO는 어느 쪽이 우수한가?

59

[33] Ivison, Hamish, et al. (2024), "Unpacking DPO and PPO: Disentangling

Best Practices for Learning from Preference Feedback"에서 인용

## •

## 현시점에서는 DPO는 PPO에게 이길 수 없다

## •

## PPO > filtered DPO / iterative DPO > DPO > SFT

## •

## 그 이유는?

## •

## PPO를 이용함으로써 Reward Model의 외삽 데이터에 접근할 수 있기 때문?

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## Reverse KL의 문제점이란?

60

𝜋∗𝑦𝑥=

## 1

## 𝑍(𝑥) 𝜋𝑆𝐹𝑇𝑦𝑥exp( 1

## 𝛽𝑟(𝑥, 𝑦))

## •

## RLHF는 출력의 다양성이 훼손되어 버린다.

## •

## 그 원인은 exp(

## 1

## 𝛽𝑟(𝑥, 𝑦)) 때문

## •

## 지수 함수적으로 SFT의 분포를 뾰족하게 만들어 버린다.

## •

## exp를 없애기 위해 KL-divergence 대신 f-divergence를 이용하는 연구도 존재

## 여기가 문제를 일으킨다

[34] Wang et al. (2024), "Beyond Reverse KL: Generalizing Direct Preference Optimization with Diverse Divergence Constraints"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 기타 파생 기법에 대하여

61

## •

## Iterative / Online DPO

## •

## Self-Rewarding

## •

## Token-level DPO

## •

## DPO: from r to Q

## •

## TDPO

## •

## Merge SFT

## •

## ORPO

## •

## Reference Free

## •

## SimPO

## •

## Negative Preference

## Optimization

## •

## NPO, CPO

## •

## Nash Learning

## •

## SPPO, DNO

[85] Zhichao Wang et al. (2024) "A Comprehensive Survey of LLM Alignment Techniques: RLHF, RLAIF, PPO, DPO and More"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## RLHF의 발전적 내용

62

## 1.

## DPO의 기초

## 2.

## DPO의 파생 기법

## 3.

## 기타 얼라인먼트 기법

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## Stable Alignment | 인간 사회를 시뮬레이션

[35] Liu, et al.,(2024) "Training Socially Aligned Language Models in Simulated Human Society"에서 인용

63

## •

## 모의 인간 사회를 시뮬레이션하는 샌드박스를 작성

## •

## 샌드박스 안의 에이전트끼리 대화함으로써, 질문에 대한 답변을 다양한 관점에서 생성

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## AlpacaFarm | 인간 평가를 시뮬레이션

[36] Dubois, Yann, et al. (2023), "AlpacaFarm: A Simulation Framework

for Methods that Learn from Human Feedback"에서 인용

64

## •

## "인간이 어떤 평가를 반환할 것인가"를 시뮬레이션함으로써 저렴하고 빠르게 RLHF를 진행할 수 있는 도구

## •

## 인간과의 평가는 높은 상관으로 일치하고, 실제 인간에게 평가받는 경우에 비해 1/45 비용과 훨씬 짧은 시간에 동등한 평가가 가능하다고 주장

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 발전적 기법의 대분류

65

## Human Feedback or AI Feedback

## •

## Human Feedback

## •

## RLHF, RAFT, RRHF

## •

## AI Feedback

## •

## RLCD, Stable Alignment, AlpacaFarm,

## RLAIF, Constitutional AI

## Ranking or Language

## •

## Rank-based Training

## •

## DPO, PRO, RRHF, SLiC

## •

## Language-based Training

## •

## CoH, Second Thoughts, Stable

## Alignment, SelFee

## RL or not RL

## •

## Using RL

## •

## RLHF, RLCD, RLAIF,

## •

## Not Using RL

## •

## DPO, IPO, KPO, CPO, PRO, RRHF, RAFT

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 목차

66

## • 인간의 피드백으로부터의 강화학습에 대하여(RLHF/DPO)

## • 검증 가능한 보상기로부터의 강화학습에 대하여(RLVR)

## • LLM에서의 강화학습 응용 예

## • 향후 방향성에 대하여

## • 정리

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 대규모 언어모델은 대단하지만… 간단한 문제도 틀리는 경우가 있다

67

## •

## 박사 과정 수준의 지식을 묻는 문제에서 인간을 뛰어넘는 스코어를 기록

## •

## 추론 능력에 관해서도 수학 올림피아드 문제를 풀 수 있다

## •

## 한편 간단한 계산 문제를 틀리는 경우가 있다

## ⇩ 전문가 인간의 스코어

## ← 오답

[37] epoch.ai, "GPQA Diamond Benchmark"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 이중 과정 이론(Dual Process Theory)

68

## •

## 노벨 경제학상 수상자인 대니얼 카네만과 아모스 트버스키에 의해 널리 알려진 이론으로, 인간의 사고는 2개의 다른 시스템에 의해 작동한다고 가정합니다.

## •

## 시스템 1: 직관이나 번뜩임으로 무의식적으로 판단하는 사고 방식

## •

## 시스템 2: 수학이나 논리적 사고 등으로 신중하게 천천히 생각하는 사고 방식

## •

## LLM에 비유해 보면, 시스템 1은 잘하고 시스템 2는 서투르다고 할 수 있다.

## •

## 왜 LLM은 시스템 1적 사고는 잘하는가?

## •

## 왜 LLM은 대규모로 훈련되어도 시스템 2적 사고가 서투른가?

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM은 보간(補間) 데이터베이스이다

69

## •

## 시스템 1적 사고는 과거의 경험이나 지식에

## 기반한 패턴 매칭이며, 관련 지식의 집합을

## 빠르게 보간하는 프로세스입니다.

## •

## 사전학습된 LLM은 이러한 동작을 보이고 있으며,

## 보간형 데이터베이스

## (interpolative database)처럼

## 행동합니다.

## •

## 실제로 LLM은 단순한 사실의 기억 이상의

## 것을 행하고 있습니다. 왜냐하면 훈련 시에 유사한

## 태스크를 경험했다면, 새로운 미지의 태스크를

## 풀 수 있기 때문입니다. 따라서,

## LLM은 순수한 데이터베이스는 아닙니다.

[38] Chollet, François (2023),

ARC Prize 관련 포스트에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 휴리스틱의 축적에 의한 사고

70

## •

## LLM은 많은 휴리스틱(경험칙)을 학습하고 있으며, 그것들은 통계적 상관 관계는 가지지만, 근본적인 인과 구조를 학습하고 있는 것은 아닙니다.

## •

## 즉, LLM은 많은 경험칙을 조합해 동작하고 있다고 생각할 수 있습니다.

[39] Nikankin, A. et al. (2025), "Arithmetic without algorithms: Language models solve math with a bag of heuristics"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 사전학습에 의한 스케일링 법칙의 시대는 끝났는가?

71

## •

## 컴퓨팅 능력은 향상되지만 데이터는 고갈되어 갑니다(화석 연료처럼)

## •

## GPT-4.5는 모델을 키웠음에도 큰 성능 향상에 이르지 못했습니다.

## •

## 실제로 OpenAI의 많은 연구자들이 새로운 단계가 필요하다고 언급하고 있습니다.

## •

## RL, Test Time Scaling으로 이어집니다.

[41] OpenAI (2025), "GPT-4.5 System Card"에서 인용

[40] Sutskever, Ilya (2024), "Sequence to Sequence Learning with Neural

Networks at NeurIPS 2024"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 추론 스케일링의 성공

72

## •

## 매우 긴 Chain-of-Thought를 수행하도록 강화학습함으로써, OpenAI o1이나 DeepSeek R1은 추론 시에 깊이 생각할수록 성능 향상에 기여하게 되었습니다.

## → LLM이 시스템 2적 사고를 손에 넣을 수 있게 되어, 추론 스케일링 시대의 계기가 됩니다.

[43] DeepSeek-AI, Guo, Daya, et al. (2025), "DeepSeek-R1: Incentivizing Reasoning

Capability in LLMs via Reinforcement Learning"

에서 인용

[42] OpenAI (2024),

"Learning to Reason with LLMs"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 이제부터는 경험의 시대

73

## •

## 근년의 AI는 "휴먼 데이터의

## 시대"에 있었습니다.

## •

## LLM처럼 인간의 방대한 데이터를

## 학습함으로써 성능을 향상시켜 왔으나,

## "인간을 뛰어어넘는" 초인적인 지능에

## 도달하는 것은 어렵습니다.

## •

## 이 한계를 돌파하기 위해 "경험의

## 시대"로의 전환이 필요합니다.

## •

## 즉, AI 자신이 시행착오하고

## 그 결과로부터 학습할 필요가 있다.

## → 그 한 가지 방법이 강화학습

[44] Silver, David and Sutton, Richard (2025),

"Welcome to the Era of Experience"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## RLVR의 개요

74

## •

## 검증 가능한 보상 모델을 이용하여 강화학습을 수행합니다.

## •

## 예: 수학의 경우 최종 출력이 맞는지, 코드라면 실행 결과가 맞는지, 테스트가 통과하는지 등

## •

## RLHF의 경우 보상 모델을 학습시킬 필요가 있었지만, RLVR에서는 불필요합니다.

## Ways to compute rewards

## ●

## Math-Verify (https://github.com/huggingface/Math-

Verify)

## ●

## LLM-as-a-judge for facts

## ●

## Code Sandboxes

## ●

## More!

[9] Lambert, Nathan, et al., "RLHF Book Chapter 14: Reasoning"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## DeepSeek R1의 성공

75

## •

## o1의 성공 이후, 오픈소스로 재현하려는 움직임이 많이 등장했지만, DeepSeek R1은 오픈소스로 처음으로 o1에 필적하는 성능을 내었습니다.

## •

## GRPO라 불리는 독자적인 강화학습 알고리즘을 제안하고, 성능 향상에 기여했습니다.

[43] DeepSeek-AI, Guo, Daya, et al. (2025), "DeepSeek-R1: Incentivizing Reasoning Capability in

LLMs via Reinforcement Learning"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## GRPO: 개요

76

## •

## PPO를 추론 향상에 특화시킨 강화학습 기법

## •

## 어드밴티지(A)를 에피소드 보상(r)로부터 직접 산출함으로써 상태 가치 V(s)의 함수 근사를 불필요하게 했습니다.

[45] Shao, Zhihong, et al. (2024), "DeepSeekMath: Pushing the Limits of

Mathematical Reasoning in Open Language Models"에서 인용

[46] oxen.ai (2024), "Why GRPO is Important and How it Works"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

Lambert |

Experimenting with

this new RL  77

## 가치 함수를 학습하는 대신, 동일한 프롬프트에 대한 복수 응답의 통계를 사용하여 베이스라인을 계산합니다.

## Clipping logic for conservative step size (from PPO)

## KL penalty in loss

## rather than reward

## Sample many answers, o, to questions, q,

## assign rewards relative to group rewards r_i

## Token length

## normalization

[45] Shao, Zhihong, et al. (2024), "DeepSeekMath: Pushing the Limits of

Mathematical Reasoning in Open Language Models"에서 인용

## GRPO: 수식

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM의 "아하 체험"

78

## •

## RLVR에 의해, 자신의 시행착오 결과가 틀렸을 때 "Wait, wait. That's an aha moment"라고 말하며 올바른 풀이 방법을 깨닫는 경우가 있습니다.

[43] DeepSeek-AI, Guo, Daya, et al. (2025), "DeepSeek-R1: Incentivizing

Reasoning Capability in LLMs via Reinforcement Learning"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## RLVR에 의해 여러 인지 행동이 유발된다

79

## •

## 강화학습에 의해 Verification, Backtrack 행동이 증가하고, 그에 수반해 스코어도 향상됩니다.

## •

## 한편 RL 전 모델에서 이 두 행동이 전혀 보이지 않는 경우는 RL해도 성능이 향상되지 않습니다.

[47] Gandhi et al. (2025), "Cognitive Behaviors that Enable Self-Improving Reasoners,

or, Four Habits of Highly Effective STaRs"

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## GRPO의 문제점

80

## Length normalization bias

## Question-level difficulty bias

## •

## 토큰 길이로 정규화되어 있기 때문에 길이를 길게

## 하는 쪽이 페널티를 받기 어려워집니다.

## •

## 그래서 학습이 진행되면 생성 길이가 길어집니다.

[48] Liu, Zichen, et al. (2025), "Understanding R1-Zero-like Training: A Critical

Perspective"에서 인용

## •

## 어드밴티지를 계산할 때 표준

## 편차로 나누기 때문에, 극단적으로 난이도가

## 낮거나 높은 문제일 때 더 높은 가중치를 부여받는

## 경향이 있습니다.

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## GRPO의 발전판: Dr. GRPO

Lambert |

Experimenting with

this new RL  81

## •

## 길이로 정규화하지 않고 토큰 손실을 합산한 뒤 마지막에 그룹 수로만 평균을 내어, 길이에 대한 바이어스를 줄입니다.

## •

## 더 짧은 길이로 높은 스코어를 달성

[48] Liu, Zichen, et al. (2025), "Understanding R1-Zero-like Training: A Critical

Perspective"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## GRPO의 발전판: DAPO

Lambert |

Experimenting with

this new RL  82

## •

## DAPO는 GRPO를 개량하여 동적 샘플링과 확장 클리핑으로 탐색성과 안정성을 높였습니다.

[49] Yu, Qiying, et al. (2025), "DAPO: An Open-Source LLM Reinforcement Learning

System at Scale"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## RL에서의 길이 바이어스

Lambert |

Experimenting with

this new RL  83

## 길이 정규화 방법으로 단문/장문의 유리함과 기울기 분산이 달라지며, 왼쪽일수록 안정적이지만 편향이 크고, 오른쪽일수록 편향은 없지만 불안정해집니다.

## Default GRPO

## Per sequence length

## normalization.

## Learning slightly

## biased in every

## completion.

## Dr. GRPO*

## No length normalization

## per sequence.

## Unbiased across

## sequences and groups

## (questions).

## DAPO

## Normalize by total

## number of tokens

## across question.

## Per-question bias as

## weight is different.

## More biased,

## likely lower

## gradient

## variance

## Theoretical

## solution, will

## it translate to

## practice?

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## SFT는 기억하고 RL은 일반화를 촉진한다

84

## •

## 심플한 토이 태스크에서

## SFT와 RL을 비교

## •

## 분포 내 데이터에서는

## SFT가 강하고, 분포 외

## 데이터에서는 RL 쪽이

## 성능이 좋다.

## •

## 즉, SFT는 기억,

## RL은 일반화 능력을 촉진한다는

## 것이 시사됩니다.

[50] Chu, T., et al. (2025), "SFT Memorizes, RL Generalizes: A Comparative Study of Foundation Model

Post-Training"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## RLVR에 의해 새로운 사고는 획득되는가?

85

## •

## RLVR에 의해 새로운 사고 패턴이 획득되고 있는 것이 아니라, 사전학습된 모델에 존재하는 사고 패턴을 강화하고 있을 가능성.

## •

## 하나의 문제에 대한 샘플 수를 늘리면 pass@k 지표가 사전학습된 모델에 가까워집니다.

[51] Yue, Y., et al. (2025), "Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs

Beyond the Base Model?"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## RLVR에 의해 새로운 사고는 획득되는가?

86

## •

## 한편, Prolonged RL(ProRL)이라는 기법을 사용함으로써 "엔트로피 붕괴"를 방지하고, RL이 베이스 모델에서는 도달할 수 없는 새로운 추론 전략을 학습할 수 있다고 주장합니다.

## •

## 엔트로피 붕괴: 모델의 출력 분포가 학습 초기 단계에서 다양성을 잃고 엔트로피가 급격히 저하되는 현상.

## •

## 이 상태가 되면 출력의 다양성이 상실되어, 탐색이 정체됩니다.

[52] Liu, M., et al. (2025), "ProRL: Prolonged Reinforcement Learning Expands Reasoning Boundaries in Large Language Models"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 다양성을 유지한 채 강화학습: Pass@K Training

87

## •

## Pass@K를 최적화하도록 강화학습을 수행함으로써 학습 중 탐색이 촉진되고, 베이스 모델에는 없던 추론 전략을 획득할 수 있다.

## •

## 엔트로피 붕괴를 방지할 수 있고, 나아가 Pass@1 성능도 향상됩니다.

## SimKO: Simple Pass@K Policy Optimization}

[53] Ruotian Peng et al. (2025), "SimKO: Simple Pass@K Policy Optimization"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 1개 샘플만으로 강화학습

88

## •

## 단 1개의 훈련 샘플을 사용한 경우에도 데이터셋 전체를 사용한 경우와 동등한 성능을 달성.

[54] Wang, Y., et al. (2025), "Reinforcement learning for reasoning in large language models with one training example"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## RLVR에서의 향후 과제

89

## •

## 일반화에는 SFT가 좋은가? RL이 좋은가? 아니면 양쪽인가?

## •

## SFT는 학습 데이터에 추론 패턴을 기억해 버리는 반면, RL은 베이스 모델의 사고 패턴을 강화하고 있을 뿐이라고도 해석할 수 있다.

## •

## SFT로 새로운 사고 패턴을 학습시키고 RL로 그것들을 강화하는 것이?

## •

## 지속적으로 새로운 사고 패턴을 학습할 수 있는 기법이 이상적.

## •

## 사전학습 모델은 무엇을 사용해야 하는가?

## •

## Qwen Family에서는 RL에 의해 비약적인 정밀도 향상이 보이지만, Llama Family에서는 Qwen보다 정밀도가 향상되지 않는다.

## •

## 사전학습 모델의 분포에 따라 RL의 효과가 달라진다.

## •

## 보상은 결과에만 주면 되는가? 중간 결과에도 주는 것이 좋은가?

## •

## 최종 결과에만 보상을 주고 있지만, 본래는 도중 과정에도 보상을 주는 쪽이 효율이 좋다.

## •

## 하지만 현재로서는 그러한 기법들은 최종 결과에만 보상을 주는 경우와 비교해 악화되어 있다.

## •

## 검증 불가능한 태스크에서의 추론은 어떻게 해야 하는가?

## •

## 수학, 코드 등 최종 결과를 규칙 기반으로 판정할 수 있는 태스크뿐만이 아니다.

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 목차

90

## • 인간의 피드백으로부터의 강화학습에 대하여(RLHF/DPO)

## • 검증 가능한 보상기로부터의 강화학습에 대하여(RLVR)

## • LLM에서의 강화학습 응용 예

## • 향후 방향성

## • 정리

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 멀티모달 태스크

91

## •

## 언어뿐만 아니라 이미지나 동영상을 입력으로 추론을 수행하는 모델도 등장하고 있습니다.

## •

## 또한 3D 씬 이해 향상을 위해 강화학습을 사용하는 사례도 존재합니다.

[55] Huang Ting et al. (2025), "3D-R1: Enhancing Reasoning in 3D VLMs for Unified Scene Understanding"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 에이전트 태스크

92

## •

## 웹 페이지 조작을 수행하는 WebAgent나 GUI 자체를 조작하는 GUI-Agent에 대해

## 강화학습을 도입함으로써 태스크 성공률이 높아지는 것이 확인되었습니다.

## •

## OS 자체의 조작을 강화학습으로 학습하는 연구도 존재합니다.

[56] GUI-R1 (2025), "GUI-R1 : A Generalist R1-Style Vision-Language Action Model For GUI Agents"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 로봇 태스크

93

## •

## VLA(Vision-Language-Action Model)를 강화학습함으로써 장기 태스크의 성능이 비약적으로 향상했습니다.

## •

## 또한, RL에 의해 SFT Model에서 보이지 않았던 새로운 행동이 학습되었습니다.

[57] Li et al. (2025), "SimpleVLA-RL: Scaling VLA Training via Reinforcement Learning"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 목차

94

## • 인간의 피드백으로부터의 강화학습에 대하여(RLHF/DPO)

## • 검증 가능한 보상기로부터의 강화학습에 대하여(RLVR)

## • LLM에서의 강화학습 응용 예

## • 향후 방향성

## • 정리

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 효율적인 추론을 수행한다

95

## •

## 강화학습에 의해 생성 길이가 길어져, 간단한 문제에서도 길게 생각해 버리는 문제가 있다. 또한, 너무 많이 생각함으로써 틀려 버리는 overthink가 발생한다.

## •

## 본래는 태스크의 난이도에 따라 생각하는 길이를 제어함으로써 효율적인 추론을 실현해 주기를 바란다.

[58] Feng et al. (2025), "Efficient Reasoning Models: A Survey"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 잠재 공간에서의 추론

96

## •

## 사고 과정을 명시적으로 토큰화하면서 추론하는 것은 매우 비효율적입니다.

## •

## 인간으로 치면 매번 말하면서 생각하고 있는 것과 같다.

## •

## 잠재 공간에서 추론함으로써 추상적 사건을 효율적으로 계산할 수 있습니다.

[59] Zhu et al. (2025), "A Survey on Latent Reasoning"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 사전학습부터 강화학습을 수행한다

97

## •

## 지금까지의 사전학습에서는 대규모 데이터와 Next Token Prediction에 의존하고 있어,

## 방대한 데이터가 필요하고 교사 데이터 이상의 성능을 낼 수는 없다.

## •

## 그래서 사전학습부터 RL을 수행함으로써 효율적으로 학습하면서 데이터 이상의 성능을 낼 수 있지 않을까.

[60] Dong et al. (2025), "Reinforcement Pre-Training"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 목차

98

## • 인간의 피드백으로부터의 강화학습에 대하여(RLHF/DPO)

## • 검증 가능한 보상기로부터의 강화학습에 대하여(RLVR)

## • LLM에서의 강화학습 응용 예

## • 향후 방향성

## • 정리

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 정리

99

## •

## RLHF는 Alignment(인간의 의도대로 모델을 학습)를 적용하는 한 가지 방법으로,

## 인간의 피드백 데이터를 이용해 언어모델을 강화학습한다.

## •

## DPO는 지도학습을 이용해 Alignment를 적용하는 기법이며, RLHF와

## 수학적으로 동등이다.

## •

## RLVR은 검증 가능한 보상을 이용해 추론 능력을 향상시키는 방법이며,

## GRPO, DAPO, Dr. GRPO 등의 종류가 있다.

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## Appendix

100

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 데이터 수집 방법: InstructGPT

[28] Ouyang, Long, et al. (2022), "Training Language Models to

Follow Instructions with Human Feedback"에서 인용

101

## •

## Labeler 선택

## •

## 소수의 데이터에 레이블링을 하고, 스크리닝 테스트 결과 레이블과의 일치도가 높은 Labeler를 선택

## •

## Labeler의 속성에 관한 통계 데이터를 설문조사를 이용해 수집

## •

## Labeler의 속성이 편향되지 않도록 한다.

## •

## Labeler에게 제공하는 instruction 작성

## •

## Web GUI를 이용해 레이블링

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## RLHF를 구현하기 위한 라이브러리

102

## trl

## •

## HuggingFace에서 PPO를 사용하여 사전학습된 언어모델을 RLHF하기 위한 라이브러리

## trlx

## •

## CarperAI에 의해 구축된 trl의 확장 포크로, 온라인 및 오프라인 학습용 대규모 모델을 처리. 현 시점에서 PPO와 ILQL 사용 가능.

## RL4ML

## •

## 다양한 강화학습 알고리즘(PPO, NLPO, A2C 및 TRPO), 보상 함수, 메트릭을 사용하여 LLM의 RLHF 및 평가 가능

## DeepSpeed Chat

## •

## Chat 형식의 모델을 학습할 수 있는 툴킷

## •

## GPU 1대로 100억 개 이상의 파라미터를, 복수 GPU이면 1000억 파라미터 이상의 모델을 학습 가능

## •

## SoTA의 15배 이상 빠른 학습을 스크립트 하나로 실행할 수 있고, 간단하고 저비용.

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## RLHF의 평가에 대하여

[6] Zhao, Wayne Xin, et al. (2023), "A Survey

of Large Language Models"에서 인용

103

## •

## 일반적인 평가 기준

## •

## Honesty(정직성)

## •

## Helpfulness(도움됨)

## •

## Harmlessness(무해함)

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## RLHF의 평가: Honesty(정직성)

104

## •

## TruthfulQA: 진실성을 평가하는 벤치마크

## •

## 건강, 법률, 금융, 정치 등 38개 카테고리에 걸친 817개의 질문과 답변으로 구성

## •

## fine-tuning된 GPT-3를 이용해 평가를 자동화

## •

## HaluEval: 환각을 인식할 수 있는지 평가하는 벤치마크

## •

## ChatGPT가 환각을 일으키기 쉬운 데이터로 구성

## •

## Yes or No이거나, 답변이 일치하는지 판정

[80] Stephanie Lin et al. (2022) "TruthfulQA: Measuring How Models Mimic Human Falsehoods"에서 인용

[81] Junyi Li et al. (2023) "HaluEval: A Large-Scale Hallucination Evaluation Benchmark for Large Language Models"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## RLHF의 평가: Helpfulness(도움됨)

105

## •

## HH-RLHF: Helpfulness와 Harmlessness에 관한 데이터셋

## •

## Anthropic이 개발했고, 학습과 평가 모두에 자주 사용된다.

## •

## 크라우드 워커에 의해 수집됨.

[82] Yuntao Bai et al. (2022) "Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback"

arXiv:2204.05862 (Anthropic HH-RLHF Dataset)에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## RLHF의 평가: Harmlessness(무해함)

106

## •

## Crows-Pairs

## •

## 인종/피부색, 성별/성 정체성, 성적 지향, 종교, 연령, 국적, 장애, 외모, 사회경제적 지위의 9가지 편견에 관한 평가 데이터셋

## •

## WinoGender

## •

## 젠더 바이어스에 관한 평가 데이터셋

[83] Nikita Nangia et al. (2020) "CrowS-Pairs: A Challenge Dataset for Measuring Social Biases in Masked Language Models"에서 인용

[84] Rudinger, Rachel, et al. (2018), "Gender Bias in Coreference Resolution"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## FLASK: Open-set 벤치마크에서의 포괄적 평가

[61] Ye Seonghyeon et al. (2023), "FLASK: Fine-grained Language Model Evaluation based on Alignment Skill Sets"에서 인용

107

## •

## Logical Thinking, Background Knowledge, Problem Handling, User

## Alignment의 4가지 관점에서 합계 12개 스킬을 평가

## •

## GPT-4를 이용해 각 관점에서 5단계 평가를 수행

## •

## 왼쪽: FLASK dataset, 오른쪽: FLASK-HARD dataset

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## FLASK: Open-set 벤치마크에서의 포괄적 평가

108

## •

## 인간 기반 평가(왼쪽)와 GPT-4 기반 평가(오른쪽)는 유사한 경향을 보입니다.

[61] Ye Seonghyeon et al. (2023), "FLASK: Fine-grained Language Model Evaluation

based on Alignment Skill Sets"에서 인용

[61] Ye Seonghyeon et al. (2023), "FLASK: Fine-grained Language Model Evaluation based on Alignment Skill Sets"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 참고: LLM의 리스크 평가를 위한 포괄적 데이터셋

[17] Wang, Yuxia, et al. (2023), "Do-Not-Answer: A

Dataset for Evaluating Safeguards in LLMs"에서 인용

109

## •

## 각 타입별로 50개 이상의 프롬프트를 작성하여,

## 합계 939개 프롬프트로 구성된 리스크 검출 데이터

## •

## 인간 또는 GPT-4에 의해 각 카테고리에

## 해당하는지를 0, 1로 판정

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## RewardBench: 보상 모델의 평가

110

## •

## 보상 모델이 올바르게 학습되었는지를 포괄적으로 평가하기 위한 벤치마크

## •

## 리더보드도 공개되어 있습니다.

[62] Lambert Nathan et al. (2024), "RewardBench: Evaluating Reward Models for Language Modeling"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## RLHF=DPO의 증명

111

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## DPO의 이론 | DPO와 RLHF는 동등한가?

112

## max

## 𝜋

## 𝐸𝑥,𝑦~𝐷𝜋𝑟𝑥, 𝑦

## −𝛽𝐷𝐾𝐿[𝜋𝑦𝑥||𝜋𝑆𝐹𝑇𝑦𝑥]

## •

## RLHF의 목적 함수는 다음과 같이 표시됩니다.

## •

## 진정한 보상을 근사하기 위해 Bradley Terry 모델을 이용해 보상 모델을 학습하고 있었다.

## 이 문제의 최적해는 해석적으로

## 풀 수 있습니다!

## 𝜋∗𝑦𝑥=

## 1

## 𝑍(𝑥) 𝜋𝑆𝐹𝑇𝑦𝑥exp( 1

## 𝛽𝑟(𝑥, 𝑦))

## ※ 𝑍𝑥는 정규화를 위한 분배 함수

## 𝑍𝑥= Σ𝑦𝜋𝑆𝐹𝑇𝑦𝑥exp(

## 1

## 𝛽𝑟(𝑥, 𝑦))

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 보충: DPO와 RLHF는 동등한가?

113

## •

## 최적 정책을 도출하는 과정의 상세

## •

## 간단한 식 변형으로 도출할 수 있다.

## •

## 전 페이지의 𝜋𝑆𝐹𝑇𝑦𝑥가 𝜋𝑟𝑒𝑓𝑦𝑥에 해당

## −𝜷로 나누어

## 최소화 문제로

𝟏

## 𝜷𝒓(𝒙, 𝒚)를

## log 안에

## 정리

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## DPO의 이론 | Your Language Model is Secretly a Reward Model

114

## •

## 즉, 보상 𝑟(𝑥, 𝑦)를 구하면 최적 정책 𝜋∗𝑦𝑥가 구해지고, 정책 𝜋𝑦𝑥가 구해지면 보상 𝑟(𝑥, 𝑦)가 구해진다.

## •

## 𝜋𝑦𝑥와 𝑟(𝑥, 𝑦)가 쌍의 관계가 된다.

## 𝜋∗𝑦𝑥=

## 1

## 𝑍(𝑥) 𝜋𝑆𝐹𝑇𝑦𝑥exp( 1

## 𝛽𝑟(𝑥, 𝑦))

## 𝑟𝑥, 𝑦= 𝛽log

## 𝜋(𝑦|𝑥)

## 𝜋𝑆𝐹𝑇(𝑦|𝑥) + 𝛽log 𝑍(𝑥)

## ※ 𝑍𝑥는 정규화를 위한 분배 함수

## 𝑍𝑥= Σ𝑦𝜋𝑆𝐹𝑇𝑦𝑥exp(

## 1

## 𝛽𝑟(𝑥, 𝑦))

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 보상 모델 학습(수식)

115

## • 보상 모델은 프롬프트 𝑥에 대한 출력 𝑦를 입력으로 하여 보상을 출력하는 모델로

## 𝑟𝜃(𝑥, 𝑦)로 표기할 수 있다.

## • 보상 모델은 다음 손실 함수를 이용해 학습한다.

## (𝑦𝑤가 𝑦𝑙보다 좋은 답변, 𝑤: win, 𝑙: lose)

## 𝑙𝑜𝑠𝑠𝜃= −

## 1

## 𝐾

## 2

## 𝐸𝑥,𝑦𝑤,𝑦𝑙~𝐷[log(𝜎𝑟𝜃𝑥, 𝑦𝑤

## −𝑟𝜃𝑥, 𝑦𝑙

## ))]

## 즉, 좋은 답변인 (𝑥, 𝑦𝑤) 쌍의 보상이, 나쁜 쪽 답변인 (𝑥, 𝑦𝑙) 쌍의 보상보다 높아질 확률을 학습한다.

## 𝜃

## : 보상 모델의 파라미터

## 𝜎

## : 시그모이드 함수

## ※ Bradley-Terry 모델을 따른다고 가정

## 𝑝∗yw ≻yl

## x) =

## exp(𝑟∗𝑥, 𝑦𝑤)

## exp 𝑟∗𝑥, 𝑦𝑤

## + exp 𝑟∗𝑥, 𝑦𝑙

## = 𝜎(𝑟∗𝑥, 𝑦𝑤

## −𝑟∗𝑥, 𝑦𝑙)

## log 𝑝𝜃yw ≻yl x)

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## DPO의 이론 | RLHF = DPO의 증명

116

## •

## 따라서, 최적 정책을 학습하기 위해서는 Preference Data에 맞도록 보상 모델을 학습(=정책을 학습)하면 된다.

## 𝑟𝜃𝑥, 𝑦= 𝛽log

## 𝜋𝜃(𝑦|𝑥)

## 𝜋𝑆𝐹𝑇(𝑦|𝑥) + 𝛽log 𝑍(𝑥)

## ※ 𝑍𝑥는 정규화를 위한 분배 함수

## 𝑍𝑥= Σ𝑦𝜋𝑆𝐹𝑇𝑦𝑥exp(

## 1

## 𝛽𝑟(𝑥, 𝑦))

## 𝑙𝑜𝑠𝑠𝜃= −𝐸𝑥,𝑦𝑤,𝑦𝑙~𝐷[log(𝜎𝑟𝜃𝑥, 𝑦𝑤

## −𝑟𝜃𝑥, 𝑦𝑙

## ))]

## = −𝐸𝑥,𝑦𝑤,𝑦𝑙~𝐷[log 𝜎(𝛽log

## 𝜋𝜃𝑦𝑤𝑥

## 𝜋𝑆𝐹𝑇𝑦𝑤𝑥−𝛽log

## 𝜋𝜃(𝑦𝑙|𝑥)

## 𝜋𝑆𝐹𝑇(𝑦𝑙|𝑥))]

## 대입하면 분배 함수가 사라진다!

## 보통은 이것은 계산 불가 →

## 모든 y에 대해

## 총합을 취하는 것은 불가능

𝒓𝜽𝒙, 𝒚= 𝜷𝐥𝐨𝐠𝝅𝜽(𝒚|𝒙)

## 𝝅𝑺𝑭𝑻(𝒚|𝒙)로 간주하고 있다고도 해석할 수 있다.

## 𝒍𝒐𝒈𝒑𝜽𝐲𝐰≻𝐲𝐥𝐱)

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## RLHF의 과제에 대하여

117

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## RLHF의 과제 | 전체상

[63] Casper Stephen et al. (2023), "Open Problems and Fundamental Limitations of Reinforcement Learning from Human Feedback"에서 인용

118

## •

## Human Feedback, Reward Model, Policy 각 부분에 몇 가지 과제가 존재합니다.

## •

## Reward Model과 Policy 학습 양쪽에 공통되는 과제도 존재합니다.

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## Human Feedback의 과제

119

## •

## Misaligned Evaluators(정렬되지 않은 평가자)

## •

## 질이 높은 피드백을 제공하는 Labeler를 선택하는 것이 어렵다.

## •

## 평가자 중에 유해한 편견이나 의견을 가진 사람이 있다.

## •

## 어떤 인간이 의도적으로 데이터를 오염시킬 가능성.

## •

## Difficulty of Oversight(감독의 어려움)

## •

## 인간은 단순한 실수를 저지른다.

## •

## 인간은 어려운 태스크의 퍼포먼스를 적절하게 평가할 수 없다.

## •

## Data Quality(데이터 품질)

## •

## 데이터 수집의 바이어스가 발생한다.

## •

## 비용과 품질의 트레이드오프가 존재한다.

## •

## Feedback Type Limitations(피드백 유형의 한계)

## •

## 피드백 종류와 효율성의 트레이드오프.

## •

## 예: 2개 쌍의 ranking은 쉽지만 효율이 나쁘다.

[63] Casper Stephen et al. (2023), "Open Problems

and Fundamental Limitations of Reinforcement Learning

from Human Feedback"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## Human Feedback의 과제 | Misaligned Evaluators

[64] Parrish, Alicia, et al. (2023), "Which Examples Should be Multiply

Annotated? Active Learning When Annotators May Disagree"에서 인용

120

## •

## RLHF로 훈련된 모델은 누구의 의견을 반영하고 있는가?

## •

## RLHF 전에는 저소득, 저학력과 일치하는 의견이었지만, RLHF 후에는 역전되었다.

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## Human Feedback의 과제 | Difficulty of Oversight

[65] Veselovsky, Veniamin, et al. (2023), "Artificial Artificial Artificial

Intelligence: Crowd Workers Widely Use Large Language Models for Text

Production Tasks"에서 인용

121

## •

## 크라우드 워커가 LLM을 사용하는 것이 경제적 합리성이 있다.

## •

## 스스로 생각하는 것보다 LLM에게 생각하게 하면 API 대금을 지불하더라도 플러스가 된다.

## •

## 크라우드 워커의 33~46%가 LLM을 사용한 것으로 추정되었다.

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## Human Feedback의 과제 | Data Quality

[66] Zhou, Chunting, et al. (2023), "LIMA: Less Is More for Alignment"에서 인용

122

## •

## 모델의 지식과 능력은 대부분 사전학습 시에 학습된다는 가정.

## •

## 얼라인먼트는 대화 형식의 포맷과, 언어모델의 어느 도메인 분포로부터 출력시킬지를 지정한다.

## •

## 질 좋은 데이터를 소량이라도 모을 필요가 있다.

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## Human Feedback의 과제 | Feedback Type Limitations

[67] Shen, Mingyang, et al. (2023), "Bridging the Gap: A Survey on

Integrating (Human) Feedback for Natural Language Generation"에서 인용

123

## •

## 피드백 종류와 효율성의 트레이드오프

## •

## 2개 쌍의 ranking은 쉽지만 효율이 나쁘다.

## •

## 한편 언어 피드백은 품질 보장이 어렵다.

## •

## 애초에 인간의 인지 한계상 랭킹이 가장 효율이 좋은가?

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## Reward Model의 과제

[63] Casper Stephen, et al. (2023), "Open Problems and Fundamental

Limitations of Reinforcement Learning from Human Feedback"에서 인용

124

## •

## Problem Misspecification(문제 설정 오류)

## •

## 개별 인간의 가치관을 보상 함수로 표현하는 것은 어렵다.

## •

## 단일 보상 함수로 인간의 다양한 사회를 표현할 수 없다.

## •

## Misgeneralization/Hacking(잘못된 일반화/해킹)

## •

## 올바른 레이블의 훈련 데이터에서라도 올바르게 보상 모델이

## 학습된다고는 할 수 없다.

## •

## 보상 해킹이 일어날 가능성이 있다.

## •

## Evaluation Difficulty(평가의 어려움)

## •

## 보상 모델을 평가하는 것은 어렵다.

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## Reward Model의 과제 | Problem Misspecification

[64] Parrish, Alicia, et al. (2023), "Which Examples Should be Multiply

Annotated? Active Learning When Annotators May Disagree"에서 인용

125

## • 복수의 의견이 있는 문제에 대해 단일 스코어를 매기는 것은 어렵다.

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## Reward Model의 과제 | Misgeneralization/Hacking

[68] Gao, Leo, et al. (2022), "Scaling Laws for Reward Model Overoptimization"에서 인용

126

## •

## Reward Model이 과적합을 일으키면 Misgeneralization/Hacking이 일어나기 쉽다.

## •

## Reward Model에 관한 스케일링 법칙(어느 크기에서 과적합이 일어나는가)

## •

## 그림은 Policy를 1.3B로 고정, 왼쪽: 상위 N개 출력 사용, 오른쪽: 모든 출력 사용.

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## Policy의 과제

[63] Casper Stephen, et al. (2023), "Open Problems

and Fundamental Limitations of Reinforcement Learning

from Human Feedback"에서 인용

127

## •

## RL Difficulties(RL의 어려움)

## •

## 정책을 효과적으로 최적화하는 것은 어렵다.

## •

## 정책은 적대적으로 악용될 가능성이 있다.

## •

## Policy Misgeneralization(정책의 잘못된 일반화)

## •

## 최적의 RL 에이전트는 권력을 추구하는 경향이 있다.

## •

## Distributional Challenges(분포상의 과제)

## •

## RL에 의해 모드 붕괴를 일으킬 가능성이 있다.

## •

## 사전 모델의 바이어스가 강화될 가능성이 있다.

## ※ 모드 붕괴: 다양성이 상실되어, 유사한 결과만 출력되게 되는 것.

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## Policy의 과제 | Robust RL Difficulties

[69] Wei, Alexander, et al. (2023), "Jailbroken: How Does LLM Safety Training Fail?"에서 인용

128

## •

## 정책을 적대적으로 이용하여, Jailbreak를 유발하는 것이 가능.

## •

## 유명한 예: GPT4에 대한 DAN attack

## •

## 모델의 안전 규칙·제한을 무시하게 만드는 텍스트 프롬프트

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## Policy의 과제 | Distributional Challenges

[70] OpenAI (2023), "GPT-4 Technical Report"에서 인용

129

## •

## RLHF에 의해 생성 데이터의 다양성이 상실된다(모드 붕괴).

## •

## GPT-4의 경우 RLHF 후에는 자신 있게 틀리는 경우가 많아진다.

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## Reward Model & Policy의 과제

[63] Casper, Stephen, et al. (2023), "Open Problems and Fundamental Limitations

of Reinforcement Learning from Human Feedback"에서 인용

130

## •

## 보상 모델과 정책을 동시에 학습함으로써 데이터 분포의 변화가 유발된다.

## •

## 온라인 학습: 보상 모델의 분포가 정책에 영향을 주고, 정책의 출력이 보상 모델에 영향을 준다.

## •

## 오프라인 학습: 보상 모델의 바이어스에 의해 잘못된 일반화에 빠질 가능성이 있다.

## •

## 보상 모델과 정책 갱신의 균형.

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## Human Feedback에 의한 대책 | 보다 상세한 피드백

[71] Wu, Zeqiu, et al. (2023), "Fine-Grained Human Feedback Gives Better

Rewards for Language Model Training"에서 인용

131

## •

## 보다 상세한 보상 설계를 수행한다.

## (왼쪽: 일반 RLHF, 오른쪽: 제안

## 기법)

## •

## (1) 각 문장마다 보상 추정

## •

## (2) 3개의 보상 모델을 학습하고,

## 각 모델마다 스코어를 산출(사실의 부정확,

## 관련성 없음, 정보의 불완전)

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## Reward Model에 의한 대책 | 다양성 확보

[72] Rame, Alexandre, et al. (2023),

"Rewarded soups: towards Pareto-optimal

alignment by interpolating weights fine-

tuned on diverse rewards"에서 인용

132

## •

## 복수의 관점에서 학습된 Reward Model의 파라미터를 섞는(Model Soup) 것으로 파레토 최적인 alignment를 지향.

## •

## Model Soup: 다른 하이퍼파라미터로 학습된 복수 파인튜닝 모델의 "가중치"를 평균화함으로써 정밀도를 향상시키는 기법.

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## Policy에 의한 대책 | 복수 모델을 이용해 RL의 불안정성 해소

[73] Yuan, Zheng, et al. (2023), "RRHF: Rank Responses to Align Language Models with Human

Feedback without tears"에서 인용

133

## •

## 복수 모델의 출력으로 순위를 매기고, 가장 보상이 높은 입출력 쌍으로 SFT하며, 그 외 쌍에 대해서는 출력하기 어렵도록 손실 함수를 설정.

## •

## PPO를 더 단순화한 기법.

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 보충: Reverse KL vs Forward KL

134

𝐷𝐾𝐿𝜋𝜙

## 𝑅𝐿𝑦𝑥

## 𝜋𝑆𝐹𝑇𝑦𝑥

𝐷𝐾𝐿𝜋𝑆𝐹𝑇𝑦𝑥

## 𝜋𝜙

## 𝑅𝐿𝑦𝑥

## Forward KL

## Reverse KL

## • Forward KL의 경우 원래 분포 전체를 커버하도록 학습되어 버린다.

## • Reverse KL의 경우 특정 모드를 커버하도록 학습한다.

## → RLHF에서는 원래 분포에서 크게 벗어나지 않기를 원하기 때문에 이쪽을 채택.

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 보충: 강화학습에서의 기법에 대하여

135

## • PPO-ptx에 의한 강화학습으로 충분히 학습 가능한가? → 그런 것은 아니다.

## • RL은 기본적으로 학습이 불안정하며, 세밀한 구현 테크닉이 필요하거나,

## 하이퍼파라미터의 세밀한 조정이 필요하다.

[74] Irpan, Alex (2018), "Deep Reinforcement Learning Doesn't Work Yet"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 보충: PPO-max

[75] Zheng, Rui, et al. (2023),

"Secrets of RLHF in Large Language

Models Part I: PPO"에서 인용

136

## •

## 강화학습의 학습 안정화를 위한 다양한 테크닉을 추가한 방법(상세는 생략).

## •

## Clipping, Initialization, GAE, … etc

## Policy Constraints

## Score

## Reparameterization

## Pretrained Initialization

## Others

## ※ 별표가 붙은 기법을 PPO-Max에서 채택

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 보충 | PPO-max의 결과

[75] Zheng, Rui, et al. (2023), "Secrets of RLHF in Large

Language Models Part I: PPO"에서 인용

137

## • PPO-max에 의해 장기적으로 안정적인 학습을 실현(왼쪽).

## • SFT 모델과 비교했을 때의 인간 평가(오른쪽).

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## RAFT | 데이터 필터링에 의한 얼라인먼트

[76] Dong, Hanze, et al. (2023), "RAFT: Reward rAnked FineTuning for Generative Foundation Model Alignment"에서 인용

138

## •

## 보상 모델의 상위 100/k%를 fine-tuning 데이터로 필터링.

## •

## PPO를 사용하지 않고도 동등 이상의 성능.

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## RLCD | 컨텍스트 증류를 이용한 AI Feedback

[77] Yang, Kevin, et al. (2023), "RLCD: Reinforcement Learning from Contrast Distillation for Language Model Alignment"에서 인용

139

## •

## 유해, 무해 여부 등을 프롬프트에 포함하고, 생성된 문장에 대해 자동적으로 보상을 할당함으로써 AI Feedback에 의해 데이터를 작성.

## •

## 실제 SFT, PPO 시에는 유해, 무해를 지정하는 프롬프트를 삭제한다.

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## RRHF | 복수 모델의 응답을 순위 매기기

[73] Yuan, Zheng, et al. (2023), "RRHF: Rank Responses to Align Language Models with Human Feedback without tears"에서 인용

140

## •

## 복수 모델의 출력으로 순위를 매기고, 가장 보상이 높은 입출력 쌍으로 SFT하며, 그 외 쌍에 대해서는 출력하기 어렵도록 손실 함수를 설정.

## •

## PPO를 더 단순화한 기법.

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## Chain of Hindsight | 후견(後見)에 의한 피드백

[78] Liu, Tianhao, et al. (2023), "Chain of Hindsight Aligns Language Models with Feedback"에서 인용

141

## •

## 인간이 랭킹을 매긴 후, 왜 그 랭킹인지의 이유를 추가한다.

## •

## 랭킹과 이유를 바탕으로 언어모델을 fine-tuning.

## •

## CoHF(Chain of Hindsight Finetuning)라 불린다.

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## •

## RealToxicity, TruthfulQA에서의 평가에서는 InstructGPT가 가장 좋은 스코어를 내고 있다(무해성, 진실성).

## InstructGPT의 평가: 공개 데이터셋에서의 평가

[28] Ouyang, Long, et al. (2022), "Training Language Models

to Follow Instructions with Human Feedback"에서 인용

142

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 학습 데이터의 포맷에 대하여

[67] Shen, Mingyang, et al. (2023), "Bridging the Gap: A Survey on Integrating (Human) Feedback for Natural Language Generation"에서 인용

143

## • 주로 Feedback 타입은 수치, 랭킹, 자연어, 기타(MQM, Post-Edition 등)로 분류할 수 있다.

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## 학습에 자주 사용되는 데이터셋

144

## • 기본적으로 영어 데이터셋이 대부분이다.

## • Anthropic, stanfordnlp 등이 릴리스.

## • 오른쪽은 HH-RLHF의 예로 chosen과 rejected의

## 랭킹이 붙어 있다.

## • 그 외에도 OpenAssistant

## datasets(oasst1, oasst2), HelpSteer, Uni-

## RLHF, UltraFeedback 등.

[67] Shen, Mingyang, et al. (2023), "Bridging the Gap: A Survey on

Integrating (Human) Feedback for Natural Language Generation"에서 인용

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## (참고) 발전적 의제 ①: 개인적 의견을 다수 포함합니다

145

## •

## 왜 RLHF로 성능이 올라가는가?

## •

## 성능이 올라가는 것은 아닌 듯하다.

## •

## 사전학습에서 얻은 분포를 의도에 맞는 출력으로 변화시키고 있을 뿐?

## •

## 학습을 잘못하면 조건부 의도하지 않은 분포에서 출력되어 버린다.

## •

## RL은 정말로 필요한가?

## •

## DPO, PRO, RLCD 등 RL을 사용하지 않는 Human Feedback 방법이 다수

## 제안되어 있고, RLHF와 동등 이상의 성능을 내고 있다.

## •

## 아마도 RL은 필요하지 않다.

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## (참고) 발전적 의제 ②: 개인적 의견을 다수 포함합니다

146

## •

## SFT vs RLHF

## •

## SFT도 인간의 language feedback으로 해석할 수 있다.

## •

## 그렇다면, SFT만으로 충분하고 RLHF는 필요하지 않은가?

## •

## 어느 정도까지는 SFT로 충분, 나머지 1%를 제어하려면 반드시 필요하다.

## •

## 모델 출력 제어에는 Human Feedback이 앞으로도 필요하다.

## •

## 인간 feedback의 한계로서 language feedback은 너무 어렵다.

## •

## 랭킹에 의한 판단이 가장 정확한가?

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## (참고) 발전적 의제 ③: 개인적 의견을 다수 포함합니다

147

## •

## RLHF vs RLAIF

## •

## 인간이 개입하지 않는 AI Feedback에서는 Feedback 원천 모델의 성능을 넘어서는 것은

## 기본적으로 없다고 생각된다.

## •

## 하지만, 인간의 피드백 성능을 AI로 끌어올리는 방향성으로서의

## RLAIF는 계속될 것으로 생각된다(Constitutional AI).

## •

## 혹은 외부 도구를 이용해 모든 형식의 정보를 바탕으로 피드백을 수행해 나가는

## 방식이라면 성능은 향상되어 갈 것으로 생각된다.

## •

## RLCF(reinforcement learning from computational feedback)

## https://www.interconnects.ai/p/beyond-human-data-rlaif

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## References

148

[1] DeepMind, "MuZero: Mastering Go, chess, shogi and Atari without rules", https://deepmind.google/blog/muzero-mastering-go-chess-shogi-and-atari-without-
rules/ 접속일: 2026/5/24

[2] CNN.co.jp (2017), "AlphaGo 관련 기사", https://www.cnn.co.jp/tech/35080140.html 접속일: 2026/5/24

[3] TrackingAI, "AI Progress Tracking", https://www.trackingai.org/home 접속일: 2026/5/24

[4] Zhang, Kaiyan, et al. (2025), "A Survey of Reinforcement Learning for Large Reasoning Models", arXiv:2509.08827

[5] OpenAI (2022), "Instruction Following", https://openai.com/research/instruction-following 접속일: 2026/5/24

[6] Zhao, Wayne Xin, et al. (2023), "A Survey of Large Language Models", arXiv:2303.18223

[7] Touvron, Hugo, et al. (2023), "Llama 2: Open foundation and fine-tuned chat models", arXiv:2307.09288

[8] HuggingFace, "Math-Verify", https://github.com/huggingface/Math-Verify 접속일: 2026/5/24

[9] Lambert, Nathan, et al., "RLHF Book Chapter 14: Reasoning", https://rlhfbook.com/c/07-reasoning 접속일: 2026/5/24

[10] ARC Prize, "ARC Prize Leaderboard", https://arcprize.org/leaderboard 접속일: 2026/5/24

[11] 일본경제신문(2021), "한국에서 '대화AI' 폭주 — 머신러닝이 빠진 함정", https://www.nikkei.com/article/DGXZQOGM21B9V0R20C21A1000000/ 접속일: 2026/5/24

[12] Wolfe, Cameron R. (2023), "Specialized LLMs: ChatGPT, LaMDA, Galactica, Codex, Sparrow, and More",
https://cameronrwolfe.substack.com/p/specialized-llms-chatgpt-lamda-galactica 접속일: 2026/5/24

[13] Stanford Online (2023), "CS25 I Stanford Seminar - Transformers United 2023: Language and Human Alignment",
https://www.youtube.com/watch?v=DJ1Yy6Aquug&list=PLoROMvodv4rNiJRchCzutFw5ItR_Z27CM&index=13 접속일: 2026/5/24

[14] Anthropic, "hh-rlhf Dataset", https://huggingface.co/datasets/Anthropic/hh-rlhf 접속일: 2026/5/24

[15] Li, Junyi, et al. (2023), "HaluEval: A Large-Scale Hallucination Evaluation Benchmark for Large Language Models", arXiv:2305.11747

[16] Nangia, Nikita, et al. (2020), "CrowS-Pairs: A Challenge Dataset for Measuring Social Biases in Masked Language Models", arXiv:2010.00133

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## References

149

[17] Wang, Yuxia, et al. (2023), "Do-Not-Answer: A Dataset for Evaluating Safeguards in LLMs", arXiv:2308.13387

[18] OpenAI (2023), "Weak-to-Strong Generalization", https://openai.com/index/weak-to-strong-generalization/ 접속일: 2026/5/24

[19] Wikipedia, "Existential risk from artificial intelligence", https://en.wikipedia.org/wiki/Existential_risk_from_artificial_intelligence 접속일: 2025/3/1

[20] CNET Japan (2018), "AI 자율주행차, '강화학습'으로 운전 방법을 20분 만에 습득", https://japan.cnet.com/article/35122203/ 접속일: 2026/5/24

[21] CNET Japan (2017), "AI 관련 기사", https://japan.cnet.com/article/35094593/ 접속일: 2026/5/24

[22] Boston Dynamics, "Boston Dynamics", https://bostondynamics.com/ 접속일: 2026/5/24

[23] OpenAI, "ChatGPT", https://chatgpt.com/ 접속일: 2026/5/24

[24] BrainPad Platinum Data Blog (2023), "ChatGPT의 구조를 논문 기반으로 초상세하게 해설", https://blog.brainpad.co.jp/entry/2023/05/31/160719 접속일: 2026/5/24

[25] zero2one, "정책 경사법(Policy Gradient Methods)", https://zero2one.jp/ai-word/policy-gradient-methods/ 접속일: 2026/5/24

[26] OpenAI (2017), "Learning from human preferences", https://openai.com/index/learning-from-human-preferences/ 접속일: 2026/5/24

[27] Stiennon, Nisan, et al. (2020), "Learning to Summarize from Human Feedback", arXiv:2009.01325

[28] Ouyang, Long, et al. (2022), "Training Language Models to Follow Instructions with Human Feedback", arXiv:2203.02155

[29] Rafailov, Rafael, et al. (2023), "Direct Preference Optimization: Your Language Model is Secretly a Reward Model", arXiv:2305.18290

[30] Azar, Mohammad Gheshlaghi, et al. (2023), "A General Theoretical Paradigm to Understand Learning from Human Preferences", arXiv:2310.12036

[31] Ethayarajh, Kawin, et al. (2024), "KTO: Model Alignment as Prospect Theoretic Optimization", arXiv:2402.01306

[32] Saeidi, Amir, Verma, Shivanshu, and Baral, Chitta (2024), "Insights into Alignment: Evaluating DPO and its Variants Across Multiple Tasks",
arXiv:2404.14723

[33] Ivison, Hamish, et al. (2024), "Unpacking DPO and PPO: Disentangling Best Practices for Learning from Preference Feedback", arXiv:2406.09279

[34] Wang, et al. (2024), "Beyond Reverse KL: Generalizing Direct Preference Optimization with Diverse Divergence Constraints", ICLR 2024, arXiv:2309.16240

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## References

150

[35] Liu, et al. (2024), "Training Socially Aligned Language Models in Simulated Human Society",
https://www.researchgate.net/publication/371124037_Training_Socially_Aligned_Language_Models_in_Simulated_Human_Society 접속일: 2026/5/24

[36] Dubois, Yann, et al. (2023), "AlpacaFarm: A Simulation Framework for Methods that Learn from Human Feedback", arXiv:2305.14387

[37] epoch.ai, "GPQA Diamond Benchmark", https://epoch.ai/benchmarks/gpqa-diamond?view=graph&tab=release-date 접속일: 2026/5/24

[38] Chollet, François (2023), ARC Prize 관련 포스트, https://x.com/fchollet 접속일: 2026/5/24

[39] Nikankin, A., et al. (2025), "Arithmetic without algorithms: Language models solve math with a bag of heuristics", arXiv:2410.21272

[40] Sutskever, Ilya (2024), "Sequence to Sequence Learning with Neural Networks", NeurIPS 2024,
https://proceedings.neurips.cc/paper_files/paper/2014/file/5a18e133cbf9f257297f410bb7eca942-Paper.pdf 접속일: 2026/5/24

[41] OpenAI (2025), "GPT-4.5 System Card", https://cdn.openai.com/gpt-4-5-system-card-2272025.pdf 접속일: 2026/5/24

[42] OpenAI (2024), "Learning to Reason with LLMs", https://openai.com/index/learning-to-reason-with-llms/ 접속일: 2026/5/24

[43] DeepSeek-AI, Guo, Daya, et al. (2025), "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning", arXiv:2501.12948

[44] Silver, David and Sutton, Richard (2025), "Welcome to the Era of Experience", https://storage.googleapis.com/deepmind-media/Era-of-
Experience%20/The%20Era%20of%20Experience%20Paper.pdf 접속일: 2026/5/24

[45] Shao, Zhihong, et al. (2024), "DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models", arXiv:2402.03300

[46] oxen.ai (2024), "Why GRPO is Important and How it Works", https://www.oxen.ai/blog/why-grpo-is-important-and-how-it-works 접속일: 2026/5/24

[47] Gandhi, et al. (2025), "Cognitive Behaviors that Enable Self-Improving Reasoners, or, Four Habits of Highly Effective STaRs", arXiv:2503.01307

[48] Liu, Zichen, et al. (2025), "Understanding R1-Zero-like Training: A Critical Perspective", arXiv:2503.20783

[49] Yu, Qiying, et al. (2025), "DAPO: An Open-Source LLM Reinforcement Learning System at Scale", arXiv:2503.14476

[50] Chu, T., et al. (2025), "SFT Memorizes, RL Generalizes: A Comparative Study of Foundation Model Post-Training", arXiv:2501.17161

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## References

151

[51] Yue, Y., et al. (2025), "Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model?",
https://openreview.net/pdf?id=4OsgYD7em5 접속일: 2026/5/24

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

[64] Parrish, Alicia, et al. (2023), "Which Examples Should be Multiply Annotated? Active Learning When Annotators May Disagree", ACL Findings 2023,
https://aclanthology.org/2023.findings-acl.658/ 접속일: 2026/5/24

[65] Veselovsky, Veniamin, et al. (2023), "Artificial Artificial Artificial Intelligence: Crowd Workers Widely Use Large Language Models for Text Production Tasks",
arXiv:2306.07899

[66] Zhou, Chunting, et al. (2023), "LIMA: Less Is More for Alignment", arXiv:2305.11206

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## References

152

## [67] Shen, Mingyang, et al. (2023), "Bridging the Gap: A Survey on Integrating (Human) Feedback for Natural Language Generation",

## arXiv:2305.00955

## [68] Gao, Leo, et al. (2022), "Scaling Laws for Reward Model Overoptimization", arXiv:2210.10760

## [69] Wei, Alexander, et al. (2023), "Jailbroken: How Does LLM Safety Training Fail?", arXiv:2307.02483

## [70] OpenAI (2023), "GPT-4 Technical Report", arXiv:2303.08774

## [71] Wu, Zeqiu, et al. (2023), "Fine-Grained Human Feedback Gives Better Rewards for Language Model Training", arXiv:2306.01693

## [72] Rame, Alexandre, et al. (2023), "Rewarded soups: towards Pareto-optimal alignment by interpolating weights fine-tuned on diverse

## rewards", arXiv:2306.04488

## [73] Yuan, Zheng, et al. (2023), "RRHF: Rank Responses to Align Language Models with Human Feedback without tears",

## arXiv:2304.05302

## [74] Irpan, Alex (2018), "Deep Reinforcement Learning Doesn't Work Yet", https://www.alexirpan.com/2018/02/14/rl-hard.html 접속일: 2026/5/24

## [75] Zheng, Rui, et al. (2023), "Secrets of RLHF in Large Language Models Part I: PPO", arXiv:2307.04964

## [76] Dong, Hanze, et al. (2023), "RAFT: Reward rAnked FineTuning for Generative Foundation Model Alignment", arXiv:2304.06767

## [77] Yang, Kevin, et al. (2023), "RLCD: Reinforcement Learning from Contrast Distillation for Language Model Alignment",

## https://github.com/facebookresearch/RLCD 접속일: 2026/5/24

## [78] Liu, Tianhao, et al. (2023), "Chain of Hindsight Aligns Language Models with Feedback", arXiv:2302.02676

LLM 대규모 언어모델 강좌 강의 자료 © 2025 by 도쿄대학교 마쓰오·이와사와 연구실 is licensed under CC BY-NC-ND 4.0

© MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## References

153

## [79] Peng, Baolin, et al. Stabilizing RLHF through Advantage Model and Selective Rehearsal. 2023. In arXiv:2309.10202

## [80] Stephanie Lin et al. (2022) "TruthfulQA: Measuring How Models Mimic Human Falsehoods" ACL 2022

## [81] Junyi Li et al. (2023) "HaluEval: A Large-Scale Hallucination Evaluation Benchmark for Large Language Models" EMNLP 2023

## [82] Yuntao Bai et al. (2022) "Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback" arXiv:2204.05862

## (Anthropic HH-RLHF Dataset)

## [83] Nikita Nangia et al. (2020) "CrowS-Pairs: A Challenge Dataset for Measuring Social Biases in Masked Language Models" EMNLP 2020

## [84] Rudinger, Rachel, et al. (2018), "Gender Bias in Coreference Resolution", https://github.com/rudinger/winogender-schemas 접속일: 2026/5/29

## [85] Zhichao Wang et al. (2024) "A Comprehensive Survey of LLM Alignment Techniques: RLHF, RLAIF, PPO, DPO and More" arXiv:2407.16216
