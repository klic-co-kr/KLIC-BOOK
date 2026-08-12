# Day 6

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 주의사항: 본 자료의 재이용(2차 이용)에 대하여

## ●

본 자료에 대하여

## ○

도쿄대학교 松尾・岩澤 연구실이 작성한 자료로, 2025년 10월부터 11월에 걸쳐 개최된 LLM 대규모 언어 모델 강좌 기초편의 강의 자료입니다.

## ○

크리에이티브 커먼즈 CC BY-NC-SA 4.0 DEED(저작자표시 – 비영리 – 동일조건변경허락 4.0 국제) 라이센스로 등록되어 있습니다.

## ●

라이센스 표기에 대하여

## ○

각 슬라이드 페이지 최하단에 라이센스가 기재되어 있습니다. 재이용 시 반드시 본 라이센스 표기를 기재해 주십시오.

재이용 시 복제가 어려운 경우, 아래의 텍스트 박스를 이용하여 하이퍼링크를 포함해 라이센스를 표기해 주시기 바랍니다.

## ○

재이용하는 페이지에 참조 논문 등의 인용이 있는 경우, 권막의 Reference에서 해당 인용 위치를 게시해 주십시오.

## ●

비영리 목적 이용에 대하여

재이용(2차 이용)이 허락되어 있습니다.

## ●

영리 목적 재이용에 대하여

이쪽으로 문의해 주십시오.

## ●

기타

## ○

원래의 표현이 바뀌지 않는 범위(폰트, 크기 등)라면 개변이 가능합니다.

## ○

그 외의 개변 및 기타 라이센스에 대한 자세한 사항은 이쪽을 확인하신 후 적절하게 취급해 주시기 바랍니다.

도쿄대학교 松尾・岩澤 연구실

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 대규모 언어 모델 fine-tuning

## 강의 파트: 中筋渉太

## 대규모 언어 모델 기초 2025 Autumn Day6

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Day6 강사 자기소개

## 1. Day6 도입

3

먼 과거의 GCI 강좌 해외 연수에서

## -

## 中筋渉太(NAKASUJI, Shota)

## -

## Co-Founder, CIO at SPEQTRA Investment Research Pte. Ltd.

## -

## 싱가포르에서 자산운용계 스타트업을 공동 창업했으며, 데이터 사이언스·AI를 활용한 퀀트 리서치가 전문입니다.

## -

## 이력:

## -

## 2023년 3월 도쿄대학교 공학부 물리공학과 졸업

## -

## 2025년 3월 동 대학원 공학계열 연구과 수료

## -

## 松尾연구실 관련:

## -

## 공동 연구 프로젝트 PM

## -

## 퀀트 운용 프로젝트 PM

## -

## GCI 강좌 TA·강사

## -

## "이미지 인식" 강좌 교재 개발

## -

## "금융시장 거래와 머신러닝" 강좌 감수·강사

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 대규모 언어 모델 fine-tuning

## 대규모 언어 모델 기초 Day6

## 목차

## 01

## 03

## 04

## Parameter Efficient fine-tuning

## Instruction Tuning

## Day6 정리

## 05

## Day6 도입

## 02

## 대규모 언어 모델의 fine-tuning

4

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## LLM fine-tuning에서의 문제 의식

## 1. Day6 도입

## 문제 의식

## 해결의 방향성

5

## -

## 대규모 언어 모델의 성능 개선과 다양한 태스크·도메인에 대한 적응을 실현하고자 한다.

## -

## 막대한 리소스를 요하는 Pre-Training은 많은 주체에게 진입 장벽이 높다.

## -

## fine-tuning을 통해 사전학습된 모델의 성능 개선과 태스크·도메인 적응을 실현한다.

## -

## 특히 Instruction Tuning을 통해 대화 성능과 Zero/Few-shot 성능을 향상시킨다.

## -

## 대규모 언어 모델은 방대한 파라미터를 보유하고 있어, fine-tuning이라 하더라도 모든 파라미터를 다룰 수 없는 경우가 있다.

## -

## Catastrophic Forgetting이나 과적합으로 인해 사전학습 모델의 성능이 훼손될 우려가 있다.

## -

## 추가로 설정한 파라미터나 일부 파라미터만을 학습·갱신 대상으로 삼음으로써 효율적인 fine-tuning을 실현한다.

## -

## 이러한 기법을 특히 Parameter Efficient fine-tuning(PEFT)이라 부른다.

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## LLM fine-tuning 사례 | ChatGPT

## 1. Day6 도입

6

## -

## 사전학습된 LLM은 높은 성능을 보이지만, 반드시 인간의 가치관에 부합하는 출력을 내놓지는 않는다.

## -

## ChatGPT는 InstructGPT 논문※에서 제안된 기법에 따라 위 문제에 대처한다.

## -

## 구체적으로 다음을 조합하여 인간의 가치관으로의 정렬을 실현한다.

## -

## Supervised fine-tuning

## = Instruction Tuning

## -

## RLHF

[2] Ouyang, Long, et al. (2022), "Training language models to follow instructions with human feedback"에서 인용

[1] OpenAI(2023), "Introducing ChatGPT"에서 인용, 일부 변형

Supervised fine-tuning

= Instruction Tuning

Reinforcement Learning from Human Feedback

(RLHF)

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## LLM fine-tuning 사례 | OpenAI API fine-tuning

## 1. Day6 도입

7

[3] OpenAI(2024), "Fine-tuning now available for GPT-4o"에서 인용

## -

## OpenAI API에서는 fine-tuning 기능이 제공된다.

## -

## 자체 데이터셋을 활용한 fine-tuning이 가능하다.

## -

## 다음과 같은 용도가 예시로 제시된다.

## -

## 출력 포맷 고정

## -

## 이미지 이해 + 텍스트 출력

## -

## 레이아웃 일관성 강화

## -

## Prompting과 비교하여 다음과 같은 장점이 예시로 제시된다.

## -

## 토큰·처리 시간 절약

## -

## 응답의 품질·제어성 향상

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## LLM fine-tuning 사례 | Med-Gemini

## 1. Day6 도입

8

## -

## Med-Gemini※:

## -

## Google이 개발한 대규모 언어 모델 Gemini를 의료용으로 특화시킨 모델이다.

## -

## 의료 분야에서의 멀티모달 능력이 강화되었으며, 각종 벤치마크에서 강력한 결과를 보고했다.

[4] Saab, Khaled, et al.(2024), "Capabilities of gemini models in medicine."에서 인용

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 대규모 언어 모델 기초 Day6의 목표

## 1. Day6 도입

## 대규모 언어 모델의 전형적인 학습 흐름에서 fine-tuning이 Pre-Training이나 RLHF·DPO에 대해 어떻게 위치 짓는지 설명할 수 있다.

## 대규모 언어 모델의 fine-tuning에서 특히 중요한 접근인 Instruction Tuning과 PEFT가 기존 기법과 어떻게 다른지 설명할 수 있다.

## Goal 1

## Goal 2

## Goal 3

9

## Instruction Tuning과 PEFT에 대해, 그 목적과 내용을 충분히 이해한 바탕 위에서 실제로 이들을 구현하고 대규모 언어 모델의 성능 개선을 실현할 수 있다.

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 대규모 언어 모델 fine-tuning

## 대규모 언어 모델 기초 Day6

## 목차

## 01

## 03

## 04

## Parameter Efficient fine-tuning

## Instruction Tuning

## Day6 정리

## 05

## Day6 도입

## 02

## 대규모 언어 모델의 fine-tuning

10

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## LLM 학습 흐름에서의 fine-tuning

## 2. 대규모 언어 모델의 fine-tuning

## Pre-Training

## 대규모 코퍼스를 통한 자기 지도학습으로 언어 모델에 어휘·문법·지식 등 기본적인 언어 이해를 획득시키는 단계

## Supervised fine-tuning

## 레이블이 있는 데이터를 통한 지도학습으로 언어 모델의 성능을 개선하거나, 특정 태스크나 도메인에 대한 적응을 실현하는 단계

## RLHF・DPO etc.

## 인간의 선호에 기반한 후속 최적화를 통해 언어 모델의 출력이 보다 인간의 가치관에 부합하도록 조정하는 단계

11

## Step 1

## Step 2

## Step 3

## 1

## 2

x : 다음 페이지에서 정리

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Pre-Training vs. fine-tuning / Post-Training

## 2. 대규모 언어 모델의 fine-tuning

12

## Pre-Training

## 데이터

## fine-tuning / Post-Training

## 목적

## -

## 어휘·문법·지식·추론 능력 등의 언어 능력을 언어 모델에 도입

## 일반적인

## 기법

## -

## 자기 지도학습

## -

## Next Token Prediction

## -

## Masked Language Model

## -

## 대규모 데이터셋

## -

## 예 CommonCrawl(GPT-3): 410B tokens(570GB)

## -

## 사전학습 모델의 성능 개선 및 다양한 태스크에 대한 적응 실현

## -

## 지도학습

## -

## 하위 태스크로의 특화

## -

## Instruction Tuning

## -

## RLHF・DPO etc.

## -

## 소규모 데이터셋

## -

## 예 LIMA: 1000 샘플(3MB)

## -

## 인간·모델에 의한 피드백

## 1

## 2

: 이번 토픽

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

종래의 fine-tuning

## 태스크

## 설계

## 가중치

## 갱신

대규모 언어 모델의 fine-tuning

13

## 대규모 언어 모델의 fine-tuning

## 2. 대규모 언어 모델의 fine-tuning

## 주목적

## -

## 사전학습 모델을 베이스로 하여, 특정 하위 태스크를 높은 정확도로 풀 수 있는 모델을 효율적으로 획득

## -

## 사전학습 모델의 출력 내용이나 형식을 용도에 맞게 조정·제어

## -

## 사전학습 모델의 미지 태스크에 대한 Zero/Few-shot 성능 개선

## -

## 풀고자 하는 태스크에서 지도학습

## -

## 예: 감정 분석·자연어 추론

## -

## 지시문을 입력, 그에 대한 이상적인 출력문을 정답으로 하는 지도학습(Instruction Tuning)

## -

## 사전학습 모델의 각 층 내 모든 파라미터에 대해 갱신 실시(대조적으로 Full-FT라 부르기도 함)

## -

## 별도 설정한 추가 파라미터나 일부 파라미터만 갱신(Parameter Efficient fine-tuning)

## A

## B

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## fine-tuning의 태스크 설계

## 2. 대규모 언어 모델의 fine-tuning

종래의 fine-tuning

Instruction Tuning

14

## -

## 특정 하위 태스크에서 지도학습을 실시

## -

## 주로 하위 태스크용 특수 토큰을 활용

[5] PyTorch Tutorial, "Dynamic Quantization on BERT"에서 인용

[6] Wei, Jason, et al.(2021) "Finetuned language models are zero-shot learners." arXiv preprint arXiv:2109.01652 (2021).에서 인용, 일부 변형

## -

## 지시문에 대해 이상적인 출력문을 정답으로 하는 지도학습을 실시

## -

## 다양한 태스크가 이 입출력 형식에 내포됨

## A

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## fine-tuning의 가중치 갱신

## 2. 대규모 언어 모델의 fine-tuning

## 종래의 fine-tuning(Full-FT)

## Parameter Efficient fine-tuning(PEFT)

15

Output

Input

## -

## 사전학습 모델이 지닌 각 층 내 모든 파라미터에 대해 갱신 실시

## -

## 보다 확실한 성능 개선이 기대되는 한편, 더 많은 컴퓨팅 리소스를 필요로 한다.

Input

Output

## -

## 추가로 설정한 파라미터나 일부 파라미터만 학습·갱신

## -

## 적절히 활용할 수 있다면 적은 리소스로 성능 개선을 달성할 수 있다.

추가 설정 분이나

파라미터의

일부를 갱신

층 안의 모든

파라미터가

갱신 대상

## B

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 대규모 언어 모델 fine-tuning

## 대규모 언어 모델 기초 Day6

## 목차

## 01

## 03

## 04

## Parameter Efficient fine-tuning

## Instruction Tuning

## Day6 정리

## 05

## Day6 도입

## 02

## 대규모 언어 모델의 fine-tuning

16

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## fine-tuning의 태스크 설계(재게시)

## 종래의 fine-tuning

## Instruction Tuning

17

## -

## 특정 하위 태스크에서 지도학습 실시

## -

## 주로 하위 태스크용 특수 토큰 활용

[5] PyTorch Tutorial "Dynamic Quantization on BERT"에서 인용

[6] Wei, Jason, et al. "Finetuned language models are zero-shot learners."(2021).에서 인용, 일부 변형

## -

## 지시문에 대해 이상적인 출력문을 정답으로 하는 지도학습을 실시

## -

## 다양한 태스크가 이 입출력 형식에 내포됨

## A

## 3. Instruction Tuning

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Instruction Tuning 개요 | FLAN 논문에 의한 제안

## 3. Instruction Tuning

18

[7] Google Research(2021), "Introducing FLAN: More generalizable Language Models with Instruction fine-tuning"에서 인용

## -

## Wei, Jason, et al. "Finetuned language models are zero-shot learners." arXiv preprint arXiv:2109.01652 (2021).

## -

## 다양한 태스크를 지시·답변이라는 입출력 형식으로 통일한 데이터셋으로 언어 모델을 fine-tuning하는 기법을 제안(Instruction Tuning).

## -

## 이렇게 fine-tuning된 모델은 평가에 사용된 25개 태스크 중,

## -

## 21개 태스크에서 Zero-shot 성능이 향상

## -

## 20개 태스크에서 더 많은 파라미터 수를 가진 GPT-3보다 더 높은 Zero-shot 성능을 보임

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Instruction Tuning 개요 | 태스크 구성과 입출력 예

## 3. Instruction Tuning

## 입력(Instruction)

## 출력(Instance)

## 구성

## 구체 예

## (FLAN※)

## -

## 태스크를 지정하는 지시문

## -

## (Optional) 부수적인 보충 정보

## -

## "Víte, rozhodl jsem se, že si pořídím psa. Translate to English"

## -

## 주어진 지시문에 대한 이상적인 답변 예

19

## -

## "You know, I decided to get a dog."

## -

## "i'm 10x cooler than all of you! What is the sentiment of this tweet?"

## -

## "positive"

xx : 원 데이터에서의 기술

xx : 템플릿에 의해

부가된 지시 부분

[8] HuggingFace, "flan2021_submix_original"에서 인용

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Instruction Tuning의 유효성

## 3. Instruction Tuning

## Zero-shot 성능 향상

## 지시 응답 성능 향상

20

## -

## FLAN※1

## -

## 137B 모델에 Instruction Tuning을 적용하고 GPT-3와 비교

## -

## 파라미터 수에서 크게 앞서는 GPT-3의 Zero-shot 및 Few-shot 성능을 뛰어넘는 Zero-shot 성능을 보였다.

[6] Wei, Jason, et al. (2021), "Finetuned language models are zero-shot learners"에서 인용

[9] Taori, Rohan, et al. (2023), "Alpaca"에서 인용

## -

## Alpaca※2

## -

## Meta사가 개발한 LLaMA 7B 모델에 Instruction Tuning을 적용

## -

## 파라미터 수에서 크게 앞서는 GPT-3.5와 동등 수준의 지시 응답 거동으로 개선

-

입력 예: What is an alpaca? How is it different from a llama?

-

출력 예: An alpaca is domesticated species of South American camelid, related to the llama and the vicuna. It is smaller than a llama, and has finer and softer fleece. ...

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Instruction Tuning의 어려움

## 3. Instruction Tuning

## 데이터셋 작성상의 곤란

## 지식은 도입 가능한가

21

## -

## Instruction Tuning으로 바람직한 거동을 실현하기 위해서는 고품질이고 무해한 데이터셋의 마련이 필요하다.

➢사람이 직접 작성하는 것이 좋은가?

## -

## 한편, 지시에 포함된 개별 태스크나 형식의 다양성의 중요성도 지적되고 있다.

➢기존 데이터셋을 활용?

## -

## 이러한 다양한 관점을 고려하여 데이터셋을 구축하기 위해서는 많은 인적·기술적 리소스가 필요하다.

➢데이터셋도 LLM으로 생성?

[9] Taori, Rohan, et al. (2023), "Alpaca"에서 인용

[10] Zhou, Chunting, et al. (2023), "Lima: Less is more for alignment"에서 인용

## -

## LIMA(2023)[10]

## -

## fine-tuning은 사전학습에서 획득된 지식·능력을 "끌어냄"으로써 성능 개선을 실현한다는 Superficial Alignment Hypothesis를 제창

## -

## Kung and Peng(2023)[9]

## -

## Instruction Tuning에 의한 성능 개선이 태스크의 이해를 통한 것이 아니라 출력 형식 같은 표면적 사항의 학습에 기인할 가능성을 지적

: 다음 페이지 이후에서 상해

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

22

## Instruction 데이터셋 작성상의 요점

## 3. Instruction Tuning

## -

## LIMA[10]: Instruction Tuning에서는 데이터의 양보다 질이 중요하다고 주장

## -

## 1000건이라는 소량의 고품질 데이터를 이용한 Instruction Tuning만으로 RLHF로 학습된 모델보다 고품질의 답변을 생성할 수 있었음을 보고

## -

## 사전학습 모델에 대해 우려되는 유해한 출력을 억제하기 위해, Instruction Tuning에서는 유해한 데이터를 피해 학습을 실시하고자 한다.

## -

## Llama 2[11]: 무해한 데이터셋 구축의 실례를 제시(다음 페이지에서 상세)

## -

## 태스크별 지시 형식의 다양화로 미지 태스크에 대한 성능이 향상[12]

## 데이터의 질

## 데이터의

## 무해성

## 지시 형식의

## 다양성

[10] Zhou, Chunting, et al. (2023), "Lima: Less is more for alignment"에서 인용

[11] Touvron, Hugo, et al. (2023), "Llama 2: Open foundation and fine-tuned chat models"에서 인용

[12] Sanh, Victor, et al. (2021), "Multitask prompted training enables zero-shot task generalization"에서 인용

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Instruction 데이터셋 구축 사례 | Llama2

## 3. Instruction Tuning

23

## Llama2란[11]

## 어노테이터의 선정·지시

## -

## Meta사가 개발·공개하는 대규모 언어 모델로, 7B, 13B, 70B의 변형을 포함

## -

## 사전학습 모델에 더해 Instruction Tuning 및 RLHF 적용 모델도 제공

## -

## 안전성 향상을 목적으로 인간에 의한 어노테이션과 평가를 적극적으로 채용

## -

## 어노테이터가 다양한 데이터 작성 태스크에 임하는 위해서의 자질과 적성을 평가하기 위해 복수의 테스트를 실시

## -

## 선정된 어노테이터에게 다음을 만족하는 지시문·답변의 작성을 의뢰

## -

## Informative

## -

## Relevant

## -

## Harmless

## -

## 예: 지시문 작성에서 피해야 할 항목

## -

## 범죄 행위의 조장

## -

## 공격적인 언행의 조장

## -

## Truthful

## -

## Clear

[11] Touvron, Hugo, et al. (2023), "Llama 2: Open foundation and fine-tuned chat models"에서 인용

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Instruction 데이터셋의 구축 기법

## 3. Instruction Tuning

## -

## 기존의 레이블이 있는 데이터셋을 템플릿을 이용해 변환

## -

## FLAN[6]: 62개의 데이터셋을 통합

## -

## 지시문에 대한 답변을 인간이 작성

## -

## InstructGPT[2]: 인간이 작성한 지시문에 대해 인간이 답변을 작성

## -

## 지시문에 대한 답변을 LLM이 생성

## -

## Self-Instruct[13]: LLM에 의한 지시문과 답변 생성 프레임워크를 제안

## 레이블이 있는

## 데이터셋의

## 통합

## 인간에 의한

## 데이터 작성

## LLM에 의한

## 데이터 생성

24

[2] Ouyang, Long, et al. (2022), "Training language models to follow instructions with human feedback"에서 인용

[6] Wei, Jason, et al. (2021), "Finetuned language models are zero-shot learners"에서 인용

[13] Wang, Yizhong, et al. (2022), arXiv:2212.10560에서 인용

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 대규모 언어 모델 fine-tuning

## 대규모 언어 모델 기초 Day6

## 목차

## 01

## 03

## 04

## Parameter Efficient fine-tuning

## Instruction Tuning

## Day6 정리

## 05

## Day6 도입

## 02

## LLM fine-tuning

25

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## fine-tuning의 가중치 갱신(재게시)

## 종래의 fine-tuning(Full-FT)

## Parameter Efficient fine-tuning(PEFT)

26

Output

Input

## -

## 사전학습 모델이 지닌 각 층 내 모든 파라미터에 대해 갱신 실시

## -

## 보다 확실한 성능 개선이 기대되는 한편, 더 많은 컴퓨팅 리소스를 필요로 한다.

Input

Output

## -

## 추가로 설정한 파라미터나 일부 파라미터만 학습·갱신

## -

## 적절히 활용할 수 있다면 적은 리소스로 성능 개선을 달성할 수 있다.

추가 설정 분이나

파라미터의

일부를 갱신

층 안의 모든

파라미터가

갱신 대상

## B

## 4. Parameter Efficient fine-tuning

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Full-FT vs. Parameter Efficient fine-tuning

## 4. Parameter Efficient fine-tuning

27

## Full-FT

## 보존

## 영역

## Parameter Efficient fine-tuning(PEFT)

## 개요

## -

## 사전학습 모델의 모든 파라미터에 대해, 다른 태스크에서 갱신 실시

## 컴퓨팅

## 리소스

## -

## 대규모 모델에서는 막대한 컴퓨팅 리소스가 필요

## -

## 예 GPT-3: 1.2TB의 GPU 메모리

## -

## 원 모델과 동일 크기의 파라미터를 보존해야 하므로 큰 영역이 필요

## -

## 예 GPT-3: 350GB의 보존 영역

## -

## 추가로 설정한 파라미터나 일부 파라미터만으로 갱신 실시

## -

## 대규모 모델에 대해서도 제한된 컴퓨팅 리소스로 성능 개선을 실현

## -

## 예 GPT-3 LoRA: 350GB의 GPU 메모리※

## -

## 갱신 부분의 파라미터만 보존하면 되므로 작은 보존 영역으로 충분

## -

## 예 GPT-3 LoRA: 35MB의 보존 영역[14]

: 다음 페이지에서 상세

[14] Hu, Edward J., et al. (2021), "LoRA: Low-rank adaptation of large language models"에서 인용

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## PEFT에 의한 GPU 메모리 사용량 절감

## 4. Parameter Efficient fine-tuning

28

## Model Loading

## Backward

## (Gradients)

## Optimizer

## (Adam)

## Full-FT (Ntrain :

## 7B)

## PEFT (Ntrain: 1M)

## Total

## ~ 13GB

## ~ 13GB

## Estimation

## size(float) * Nall

## 2 * size(float) *

## Ntrain

## size(float) * Ntrain

## ~ 26GB

## ~ 13GB

## ~ 2MB

## ~ 52GB + α

## ~ 13GB + α

## ~ 4MB

## VRAM by Steps

(※ 상기 외에 batch size에

비례하여 증가하는 Forward 분이나

라이브러리 확보 영역이 있다)

## -

## 7B 모델의 16-bit fine-tuning을 상정하여 Full-FT와 PEFT의 GPU 메모리 사용량을 개략 비교

## -

## 아래에서는 전체 파라미터 수 Nall = 7B, 부동소수점 크기 size(float) = 2byte 상황에 대응

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## PEFT 기법을 평가할 때의 주요 관점

## 4. Parameter Efficient fine-tuning

29

## 성능 개선

## 운용성

## 추론 효율

## -

## Full-FT를 실시한 경우와 비교하여 성능 개선에 큰 열화가 없는가

## -

## 사전학습 모델의 크기에 의존하지 않고 성능 개선이 실현되는가

## -

## 갱신하는※ 파라미터가 적고, 작은 스토리지로 운용이 가능한가

## -

## 그것이 가능하면 복수 모델의 병렬 운용이나 버저닝이 용이

## -

## 추가하는 파라미터가 많아 추론 비용을 증대시키지 않는가

## -

## 입력문의 계열 길이가 길어져 추론 비용을 증대시키지 않는가

## 학습 효율

## -

## 학습하는※ 파라미터가 적고, 작은 GPU 메모리로도 실현 가능한가

## -

## GPU의 효율적 활용에 의해 고속화가 가능한 기법인가

※"학습하는 파라미터는 적지만, 그에 기반하여 많은 파라미터가 갱신된다"는 경우가 있기 때문에,

"갱신하는 파라미터"와 "학습하는 파라미터"라는 비슷한 표현도 여기서는 구별하여 사용하고 있다.

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 다양한 PEFT 기법

## 4. Parameter Efficient fine-tuning

30

[15] Lialin, Vladislav, et al. (2023), "Scaling down to scale up: A guide to parameter-efficient fine-tuning"에서 인용

운용성

학습 효율

추론 효율

Extra FFN :

FFN 층의 추가에 의해

추론에 오버헤드

No overhead :

추론에 오버헤드를

수반하지 않는 기법

Extra input :

입력 계열에의 추가로,

추론에 오버헤드

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## PEFT 기법의 카테고리 분류

## 4. Parameter Efficient fine-tuning

31

[15] Lialin, Vladislav, et al. (2023), "Scaling down to scale up: A guide to parameter-efficient fine-tuning"에서 인용

## 1

## 2

## 3

## 4

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## PEFT 기법의 대표적인 카테고리

## 4. Parameter Efficient fine-tuning

32

## Adapter형

## Soft Prompt형

## Reparametrization형

## Selective형

## 개요

## 대표 예

## 2

## 1

## 3

## 4

## Transformer 내부에 MLP 층(Adapter)을 추가하고, 그것만 학습 실시

## 입력 계열에 태스크별 벡터(Soft Prompt)를 부가하고 학습 실시

## 사전학습 모델이 지닌 파라미터 중 일부만으로 학습 실시

## 행렬 분해에 기반해, 재파라미터화된 가중치에 대해 학습 실시

## Adapter(2019)

## Prompt Tuning

## (2021)

## BitFit(2021)

## LoRA(2021)

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Adapter형 | Adapter(2019)

## 4. Parameter Efficient fine-tuning

33

## 1

[16] Houlsby, Neil, et al. (2019), "Parameter-efficient transfer learning for NLP"에서 인용, 일부 변형

Transformer 내부에

학습 가능한 Adapter

모듈을 추가

Adapter는 단순한

MLP 구조를 가짐

## -

## Transformer 내부에 학습 가능한 Adapter 모듈을 추가·학습

## -

## 추가 위치가 다른 아종이 존재

## (예: Parallel Adapter※는 좌측 그림과 달리 병렬적으로 Adapter를 추가)

## -

## Adapter는 단순한 MLP 구조를 가짐

[17] He, Junxian, et al. (2021), "Towards a unified view of parameter-efficient transfer learning"에서 인용

## -

## Transformer 내부에 학습 가능한 Adapter 모듈을 추가·학습

## -

## 추가 위치가 다른 아종이 존재

## (예: Parallel Adapter※는 좌측 그림과 달리 병렬적으로 Adapter를 추가)

## -

## Adapter는 단순한 MLP 구조를 가짐

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Adapter형 | Adapter(2019)

## 4. Parameter Efficient fine-tuning

34

## 1

[16] Houlsby, Neil, et al. (2019), "Parameter-efficient transfer learning for NLP"에서 인용

횡축(로그):

학습 파라미터 수

Full-FT(탑 층만)

Adapter:

Full-FT와

동등한 정확도

## -

## Cons

## -

## Adapter가 추가됨으로써 추론에 오버헤드가 발생

## -

## Pros

## -

## Full-FT 대비 10⁻¹에서 10⁻² 정도로 작은 학습 파라미터 수로 Full-FT와 동등한 정확도(좌측 그림)

## -

## Adapter만 보존하면 되어 유연하게 교체 대응이 가능

SQuAD 태스크

BERT FT 비교

종축:

F1 score

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Soft-Prompt형 | Prompt Tuning(2021)

## 4. Parameter Efficient fine-tuning

35

## 2

[18] Lester, Brian, et al. (2021), "The power of scale for parameter-efficient prompt tuning"에서 인용

종래의 fine-tuning:

태스크마다 FT를 실시

Prompt Tuning:

태스크마다 벡터를

마련하고 입력에 부가·학습

## -

## 각 태스크에 대응한 벡터(Soft Prompt)를 입력 계열에 부가하고, 그 파라미터를 학습

## -

## Soft Prompt는 문장 형태로 설계된 프롬프트(Hard Prompt)에 대한 호칭·개념

## -

## 즉, 각 태스크마다 특화된 프롬프트 엔지니어링을 학습하고 있다고 간주할 수 있다.

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Soft-Prompt형 | Prompt Tuning(2021)

## 4. Parameter Efficient fine-tuning

36

## 2

[18] Lester, Brian, et al. (2021), "The power of scale for parameter-efficient prompt tuning"에서 인용, 일부 변형

횡축(로그):

전체 파라미터 수

GPT-3 Few-shot

T5 Prompt Tuning

T5 Full-FT

빨강: 태스크마다

주황: 멀티태스크

## -

## Pros

## -

## 모델 크기가 큰 경우 Prompt Tuning은 Full-FT와 동등한 정확도(좌측 그림)

## -

## T5-XXL(11B)에서 Soft Prompt 길이를 100으로 하면, 학습 파라미터 수는 4096 * 100

## 이것은 Full-FT의 0.007%에 해당

## -

## Cons

## -

## Soft Prompt가 입력 계열을 압박

## -

## 프롬프트 엔지니어링의 확장으로 간주하면 해석성이 결여된 결과가 됨

SuperGLUE 벤치

마크 비교

종축:

SuperGLUE Score

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Selective형 | BitFit(2021)

## 4. Parameter Efficient fine-tuning

37

## 3

[19] Zaken, Elad Ben, et al. (2021), "BitFit: Simple parameter-efficient fine-tuning for transformer-based masked language-models"에서 인용, 일부 변형

## -

## Transformer의 각 모듈에 포함된 바이어스 항에 대해서만 학습·갱신 실시

## -

## 구체적으로 다음에 포함된 바이어스 항이 해당

## -

## Attention

## -

## Feed-Forward Network

## -

## Layer Normalization

b: 바이어스 항

이것들만 학습·갱신

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Selective형 | BitFit(2021)

## 4. Parameter Efficient fine-tuning

38

## 3

[19] Zaken, Elad Ben, et al. (2021), "BitFit: Simple parameter-efficient fine-tuning for transformer-based masked language-models"에서 인용, 일부 변형

횡축:

학습 데이터 수

종축:

Exact Match

빨간 선: Full-FT

파란 선: BitFit

## -

## Pros

## -

## 학습 데이터 수가 작은 영역에서는 BitFit이 Full-FT보다 높은 정확도를 보였다(좌측 그림).

## -

## BERT(Base) 모델에서 BitFit에 의한 학습 파라미터 수는 Full-FT 대비 0.1% 정도

## -

## Cons

## -

## GPT-3 같은 보다 대규모 모델에서는 Full-FT나 다른 PEFT 기법보다 정확도가 뒤떨어진다[14].

[14] Hu, Edward J., et al. (2021), "LoRA: Low-rank adaptation of large language models"에서 인용

SQuAD 태스크

BERT FT 비교

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Reparametrization형 | LoRA(2021)

## 4. Parameter Efficient fine-tuning

39

## 4

[14] Hu, Edward J., et al. (2021), "LoRA: Low-rank adaptation of large language models"에서 인용, 일부 변형

## -

## fine-tuning으로 갱신된 가중치 W는 일반적으로 원래 가중치 W₀와 증분 가중치 ΔW의 합으로 표현 가능

저랭크 행렬을

2개 도입

-

A: d × r

-

B: r × d

사전학습

모델 선형 층

가중치는 고정

A는 정규 난수로

초기화

B는 영행렬로

초기화

2개 경로의 결과를

합산하여 다음 층으로 전달

## -

## LoRA에서는 이 증분 가중치 ΔW를 두 저랭크 행렬 A, B의 곱으로 삼고, 그것들에 대해 학습 실시

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Reparametrization형 | LoRA(2021)

## 4. Parameter Efficient fine-tuning

40

## 4

[14] Hu, Edward J., et al. (2021), "LoRA: Low-rank adaptation of large language models"에서 인용, 일부 변형

횡축(로그):

학습 파라미터 수

Soft Prompt 계열 기법

(초록·노랑)은 불안정

LoRA(분홍)·

Adapter(주황)은

비교적 안정

종축:

Accuracy

Full-FT

## -

## Pros

## -

## Full-FT 대비 10⁻²에서 10⁻⁴ 정도로 작은 학습 파라미터 수로 Full-FT와 동등한 정확도(좌측 그림)

## -

## 추론 시에는 얻어진 가중치를 원래 가중치에 미리 더해두면 오버헤드가 발생하지 않는다.

## -

## Cons

## -

## 특히 난이도가 높은 태스크(예: GSM8k, 수학적 추론)에서 Full-FT 대비 현저한 성능 열위가 발생할 수 있다※

[20] anyscale(2023), "fine-tuning LLMs: LoRA or Full-Parameter? An in-depth Analysis with Llama 2"

WikiSQL 태스크

GPT-3 FT 비교

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Reparametrization형 | LoRA(2021)

## 4. Parameter Efficient fine-tuning

41

## 4

[14] Hu, Edward J., et al. (2021), "LoRA: Low-rank adaptation of large language models"에서 인용, 일부 변형

## -

## Q. 학습 파라미터 수를 일정하게 할 때, LoRA를 적용하는 층의 종류를 더 늘려야 할까, 랭크 r을 더 크게 잡아야 할까?

## -

## A. LoRA를 적용하는 층의 종류를 늘리는 쪽이, 랭크 r이 작아지더라도 더 높은 성능이 된다는 것이 밝혀졌다.

## -

## ※ LoRA 논문에서는 Attention 모듈 내를 적용 대상으로 했으나, 이후 연구에서는 다른 선형 층도 대상으로 함으로써 성능이 개선됨

Weight Type

-

q: Query projection

-

k: Key projection

-

v: Value projection

-

o: Output projection

학습 파라미터 수를 18M로 고정

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Reparametrization형 | LoRA(2021)

## 4. Parameter Efficient fine-tuning

42

## 4

[14] Hu, Edward J., et al. (2021), "LoRA: Low-rank adaptation of large language models"에서 인용, 일부 변형

## -

## Q. LoRA를 적용하는 층의 종류를 고정해 놓고 생각할 때, 랭크 r은 어느 정도의 값을 설정할 필요가 있는가?

## -

## A. LoRA의 랭크 r은 2에서 8 범위에서 높은 성능

## -

## ※ (태스크 의존적이지만) 랭크 1로도 충분한 성능이 나오는 경우도 있음

## 경험적으로는 랭크 8 정도의 설정이 권장되고 있다.

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Reparametrization형 | LoRA의 파생 접근

## 4. Parameter Efficient fine-tuning

43

## QLoRA

## AdaLoRA

## LoRA-Pro

## 목적

## 기법

## 4

## 보다 적은 컴퓨팅 리소스로도 LoRA에 의한 fine-tuning을 실현하고자 한다

## LoRA에 4비트 양자화 등의 기법을 적용해 메모리 사용량을 더욱 절감

## LoRA에서 모든 층의 랭크가 단일 값으로 제한되는 문제 해결

## Full-FT의 기울기를 근사하지 못하는 문제를 완화하고 Full-FT와의 성능 차이를 좁힌다

## 증분 가중치의 특이값 분해에 기반해, 층마다 랭크를 적응적으로 변화시킨다

## LoRA의 두 저랭크 행렬의 기울기가 전체 기울기에 부합하도록 이론적으로 최적 조정

[22] Zhang, Qingru, et al. (2023), "Adaptive budget allocation for parameter-efficient fine-tuning"에서 인용

[21] Dettmers, Tim, et al. (2023), "QLoRA: Efficient finetuning of quantized LLMs"에서 인용

[23] Wang, Zhengbo, et al. (2024), "LoRA-Pro: Are low-rank adapters properly optimized?"에서 인용

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 대표적인 PEFT 기법의 비교

## 4. Parameter Efficient fine-tuning

44

## 성능 개선

## 운용성

## (갱신률※)

## 추론 효율

## 학습 효율

## (학습률※)

## Adapter

## Prompt

## Tuning

## BitFit

## LoRA

불안정한 경향

대규모 모델에서 열화

입력 계열 길이 압박

추론 시간 증가

(태스크에 의존)

(태스크에 의존)

(0.1 - 6 %)

(0.1 - 6 %)

(0.1 %)

(0.1 %)

(0.05 - 0.1 %)

(0.05 - 0.1 %)

(0.01 - 0.5 %)

(~0.5 %)

[15] Lialin, Vladislav, et al. (2023), "Scaling down to scale up: A guide to parameter-efficient fine-tuning"에서 인용

(변화 없음)

(변화 없음)

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 대규모 언어 모델 fine-tuning

## 대규모 언어 모델 기초 Day6

## 목차

## 01

## 03

## 04

## Parameter Efficient fine-tuning

## Instruction Tuning

## Day6 정리

## 05

## Day6 도입

## 02

## LLM fine-tuning

45

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## LLM fine-tuning 사례 되돌아보기 | ChatGPT

46

[1] OpenAI(2023), "Introducing ChatGPT"에서 인용, 일부 변형

Supervised fine-tuning

= Instruction Tuning

Reinforcement Learning from Human Feedback

(RLHF)

## 5. Day6 정리

## -

## ChatGPT는 InstructGPT 논문※에서 제안된 흐름에 따라 다음 기법을 채택

## -

## Supervised fine-tuning

## = Instruction Tuning

## -

## RLHF

## -

## InstructGPT에서는 인간이 Instruction Tuning용으로 약 1만 건의 데이터를 작성

## -

## 이를 통해 인간적 가치관으로의 출력 정렬을 실현

[2] Ouyang, Long, et al. (2022), "Training language models to follow instructions with human feedback"에서 인용

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## LLM fine-tuning 사례 | OpenAI API fine-tuning

## 1. Day6 도입

47

[3] OpenAI(2024), "Fine-tuning now available for GPT-4o"에서 인용

## -

## OpenAI API에서는 fine-tuning 기능이 제공된다.

## -

## 자체 데이터셋을 활용한 fine-tuning이 가능하다.

## -

## 다음과 같은 용도가 예시로 제시된다.

## -

## 출력 포맷 고정

## -

## 이미지 이해 + 텍스트 출력

## -

## 레이아웃 일관성 강화

## -

## Prompting과 비교하여 다음과 같은 장점이 예시로 제시된다.

## -

## 토큰·처리 시간 절약

## -

## 응답의 품질·제어성 향상

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## LLM fine-tuning 사례 | Med-Gemini

## 1. Day6 도입

48

## -

## Med-Gemini※:

## -

## Google이 개발한 대규모 언어 모델 Gemini를 의료용으로 특화시킨 모델이다.

## -

## 의료 분야에서의 멀티모달 능력이 강화되었으며, 각종 벤치마크에서 강력한 결과를 보고했다.

[4] Saab, Khaled, et al. (2024), "Capabilities of gemini models in medicine"에서 인용

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 대규모 언어 모델 기초 Day6의 목표

## 대규모 언어 모델의 전형적인 학습 흐름에서 fine-tuning이 Pre-Training이나 RLHF·DPO에 대해 어떻게 위치 짓는지 설명할 수 있다.

## 대규모 언어 모델의 fine-tuning에서 특히 중요한 접근인 Instruction Tuning과 PEFT가 기존 기법과 어떻게 다른지 설명할 수 있다.

## Goal 1

## Goal 2

## Goal 3

49

## Instruction Tuning과 PEFT에 대해, 그 목적과 내용을 충분히 이해한 바탕 위에서 실제로 이들을 구현하고 대규모 언어 모델의 성능 개선을 실현할 수 있다.

## 5. Day6 정리

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 대규모 언어 모델 fine-tuning

## 대규모 언어 모델 기초 Day6

## 목차

## 01

## 03

## 04

## Parameter Efficient fine-tuning

## Instruction Tuning

## Day6 정리

## 05

## Day6 도입

## 02

## 대규모 언어 모델의 fine-tuning

50

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## References

51

[1] OpenAI (2023), "Introducing ChatGPT", https://openai.com/ja-JP/index/chatgpt/ 액세스일: 2026/5/24

[2] Ouyang, Long, et al. (2022), "Training language models to follow instructions with human feedback", Advances in Neural Information Processing Systems 35, pp. 27730-27744

[3] OpenAI (2024), "Fine-tuning now available for GPT-4o", https://openai.com/ja-JP/index/gpt-4o-fine-tuning/ 액세스일: 2026/5/24

[4] Saab, Khaled, et al. (2024), "Capabilities of gemini models in medicine", arXiv:2404.18416

[5] PyTorch Tutorial, "Dynamic Quantization on BERT", https://docs.pytorch.org/tutorials/index.html 액세스일: 2026/5/24

[6] Wei, Jason, et al. (2021), "Finetuned language models are zero-shot learners", arXiv:2109.01652

[7] Google Research (2021), "Introducing FLAN: More generalizable Language Models with Instruction fine-tuning", https://research.google/blog/introducing-flan-more-generalizable-language-models-with-instruction-fine-tuning/ 액세스일: 2026/5/24

[8] HuggingFace, "flan2021_submix_original", https://huggingface.co/datasets/conceptofmind/flan2021_submix_original 액세스일: 2026/5/24

[9] Taori, Rohan, et al. (2023), "Alpaca", Stanford Center for Research on Foundation Models, https://crfm.stanford.edu/2023/03/13/alpaca.html 액세스일: 2026/5/24

[10] Zhou, Chunting, et al. (2023), "Lima: Less is more for alignment", arXiv:2305.11206

[11] Touvron, Hugo, et al. (2023), "Llama 2: Open foundation and fine-tuned chat models", arXiv:2307.09288

[12] Sanh, Victor, et al. (2021), "Multitask prompted training enables zero-shot task generalization", arXiv:2110.08207

[13] Wang, Yizhong, et al. (2022), arXiv:2212.10560

LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by東京大学松尾・岩澤研究室 is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## References

52

[14] Hu, Edward J., et al. (2021), "LoRA: Low-rank adaptation of large language models", arXiv:2106.09685

[15] Lialin, Vladislav, Vijeta Deshpande, and Anna Rumshisky (2023), "Scaling down to scale up: A guide to parameter-efficient fine-tuning", arXiv:2303.15647

[16] Houlsby, Neil, et al. (2019), "Parameter-efficient transfer learning for NLP", International Conference on Machine Learning, PMLR

[17] He, Junxian, et al. (2021), "Towards a unified view of parameter-efficient transfer learning", arXiv:2110.04366

[18] Lester, Brian, Rami Al-Rfou, and Noah Constant (2021), "The power of scale for parameter-efficient prompt tuning", arXiv:2104.08691

[19] Zaken, Elad Ben, Shauli Ravfogel, and Yoav Goldberg (2021), "BitFit: Simple parameter-efficient fine-tuning for transformer-based masked language-models", arXiv:2106.10199

[20] anyscale (2023), "fine-tuning LLMs: LoRA or Full-Parameter? An in-depth Analysis with Llama 2", https://www.anyscale.com/blog/fine-tuning-llms-lora-or-full-parameter-an-in-depth-analysis-with-llama-2 액세스일: 2026/5/24

[21] Dettmers, Tim, et al. (2023), "QLoRA: Efficient finetuning of quantized LLMs", arXiv:2305.14314

[22] Zhang, Qingru, et al. (2023), "Adaptive budget allocation for parameter-efficient fine-tuning", arXiv:2303.10512

[23] Wang, Zhengbo, et al. (2024), "LoRA-Pro: Are low-rank adapters properly optimized?", arXiv:2407.18242
