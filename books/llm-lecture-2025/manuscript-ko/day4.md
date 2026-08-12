# Day 4

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 주의사항: 본 자료의 재이용(2차 이용)에 대해

## ●

## 본 자료에 대해

## ○

## 도쿄대학교 마츄오·이와사와 연구실이 작성하였으며, 2025년 10월부터 11월에 걸쳐 개최된 LLM 대규모 언어 모델 강좌 기초편

## 의 강의 자료입니다.

## ○

## 크리에이티브 커먼즈 CC BY-NC-SA 4.0 DEED(표시– 비영리– 동일조건변경 4.0 국제) 라이선스로 등록되어

## 있습니다.

## ●

## 라이선스 표기에 대해

## ○

## 각 슬라이드의 페이지 하단에 라이선스가 기재되어 있습니다. 재이용 시에는 반드시 본 라이선스 표기를 기재해 주세요.

## 재이용 시 복제가 어려운 경우에는 아래의 텍스트 박스를 이용하여, 하이퍼링크를 포함하여 라이선스를 표기해

## 주시기 바랍니다.

## ○

## 재이용하는 페이지에 참고 논문 등의 인용이 있는 경우, 권말의 Reference에서 인용 위치를 게재해 주세요.

## ●

## 비영리 목적 이용에 대해

## 재이용(2차 이용)이 허락되어 있습니다.

## ●

## 영리 목적 재이용에 대해

## 이쪽으로 문의해 주세요.

## ●

## 기타

## ○

## 원래의 표현이 바뀌지 않는 범위(글꼴, 크기 등)라면 개작이 가능합니다.

## ○

## 그 이외의 개작 및 라이선스에 대한 자세한 내용은 이쪽을 확인하신 후 적절하게 취급해 주시기 바랍니다.

## 도쿄대학교 마츄오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 스케일 법칙

## 이론: 고지마 타케시(小島武)

## 실습: 여전군(余振軒)

허가 없는 촬영 및 제3자

에 대한 공개를 금지합니다

## 대규모 언어 모델 강좌 2025

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

3

## 고지마 타케시(小島武)

3

## ❏ 약력

## ❏ 2023.3 도쿄대학교 대학원 공학계 연구과 TMI 박사 과정 수료

## ❏ 2023.4~ 동 연구과 특임 연구원

## ❏ 2025.1~ 동 연구과 특임 조교수

## ＊이전에는 IT 엔지니어로 일했습니다.

## ❏ 활동

## Weblab-10B 개발, 기시다 총리·이시바 총리의 LLM 특별 강좌에서 강사 담당, LLM 개발 콘테스트

## 2024·2025 운영 측 콘텐츠 리더, AI 백서 2025에서 Safety 장 집필

## ❏ 연구

## LLM의 작동 원리 이해와 제어(Reasoning Model, 다국어 등), Safety(Unlearning,

## 지시 추종 능력), Transformer 모델 구조 개선 등 등 + 로봇

https://github.com/kojima-

takeshi188/zero_shot_cot

https://arxiv.org/abs/2505.12583

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 스케일 법칙(Day4)

## 4

## ●목적:

## ○언어 모델을 스케일(= 대규모화)하는 의의에 대해 학습한다.

## ●목표:

## ○스케일 법칙이 무엇인지, 그리고 그 중요성을 설명할 수 있다.

## ○스케일 법칙의 구체적인 구하는 방법을 설명하고, 구현할 수 있다.

## ○추론 시의 스케일링이 무엇인지에 대해 설명할 수 있다.

## ●실습:

## ○PyTorch로 스케일 법칙을 실제로 구하는 코드를 구현한다

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

5

## 목차

5

## ○스케일 법칙이란 무엇인가

## ○스케일 법칙의 사용 방법

## ○스케일 법칙의 구체적인 구하는 방법

## ○새로운 트렌드: 추론 시의 스케일링

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

6

## 스케일 = 대규모화

6

## 대규모 언어 모델

## Day3에 설명했습니다.

## ＊최근 LLM에 사용되는

## Transformer 모델은

## 신경 언어 모델의 한 종류.

## Day4에서(지금부터) 설명합니다.

## ＊어떻게 스케일시킬 것인가?

## 왜 스케일시키는가?

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## ■LLM 학습 플로 속의 위치

## 사전학습

## 대규모 코퍼스를 이용한 자기 지도 학습을 통해 대규모 언어 모델에

## 어휘·문법·기초 지식과 같은 기초적인 언어 이해를 획득시키는 단계

## 파인튜닝

## 레이블이 있는 데이터를 이용한 지도 학습을 통해 사전학습된 모델의

## 성능을 개선하거나, 특정 태스크나 도메인에 대한 적응을 실현하는 단계

## RLHF

## 인간의 피드백을 이용한 강화학습을 통해 대규모 언어 모델의

## 출력이 인간의 가치관에 보다 부합하도록 조정하는 단계

## Step 1

## Step 2

## Step 3

## Day3(전회) & Day4(금일) & Day5(차회)

## Day6

## Day7

## 7

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 대규모 언어 모델의 전개

8

## • 2025년 이후에도 GPT-5, Gemini 2.5, GPT-OSS, DeepSeek-R1, Qwen3 등 많은 LLM

## 이 공개되었다(진행 중).

## "A Survey of Large Language Models", 2023 (version 16)

[[48] Zhao+. A Survey of Large Language Models. 2023 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## Transformer를 이용한 언어 모델의 스케일화[1]

9

## 2019년

## 2020년

## 2018년

## 2023년

## 기본적으로 어느 쪽이든 2017년에 발명된 Transformer라 불리는 구조를 이용.

## GPT-3 등장 이후, 미국 기업을 중심으로 여러 연구 기관이 독자적인 대규모 언어 모델을 개발.

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## What is Scaling? Why Scaling?

10

## 배경에 있는 것은 스케일 법칙이라 불리는 경험칙. 아래를 중심으로 설명.

## 2020년 1월 by OpenAI

## (GPT3는 2020년 6월)

## ■중요 논문 1

## ■중요 논문 2

## 2022년 by DeepMind(당시)

[3] Kaplan+. Scaling Laws for Neural Language Models. 2020 에서 인용

[42] Hoffmann+. Training Compute-Optimal Large Language Models. 2022 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

11

## 사전학습은 웹에서 수집한 대량의 문장을 이용하여 다음 단어의 예측을 쉬지 않고 수행한다

## 사전학습 과정에서 읽기·쓰기·셈하기 및 세계의 모든 지식을 학습한다

## • GPT 시리즈를 대표로 하는 현대의 LLM은 반드시 이 사전학습을 수행한다

## • 예를 들어 아래 그림과 같이 "봄은 벚꽃이 아름답다"라는 텍스트의 사전학습을 통해 "봄"

## "벚꽃" "아름답다"라는 단어 사이에 강한 관계성이 있다는 것(= 세계의 지식)을 학습한다

## 봄

## 봄

## 은

## 봄

## 은

## 벚꽃

## 봄

## 은

## 벚꽃

## 이

## LLM

## LLM

## LLM

## LLM

## P(은|봄)

## P(벚꽃|봄, 은)

## P(이|…)

## 입력

## 예측

## 은

## 벚꽃

## 이

## 아름답다

## 정답

## 예측과 정답의 오차

## (= 교차 엔트로피)

## 가 작아지도록

## 모델을 학습한다

## 입력한 단어의

## 다음에 올 단어는?

## 비교

## P(아름답다|…)

## 사전학습(복습)

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

12

## 컴퓨팅 자원(C), 데이터셋 크기(D), 파라미터 수(N)

## 와 오차(L) 사이에 성립하는 경험칙

## • 각 그림의 데이터 점은 실측값. 단, 다른 2개 변수는 충분히 크다고 가정.

## • 어느 변수든 Test Loss와의 사이에 이중 로그 그래프에서 선형 관계가 보인다

## 스케일 법칙(Scaling Law) *Power-Law(거듭제곱 법칙)이라고도 불린다

## [3] Kaplan+. Scaling Laws for Neural Language Models. 2020 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

13

## ①파라미터 수(N)와 오차(L) 사이에 성립하는 관계성.

## Loss

## = 교차 엔트로피

## 스케일 법칙(Scaling Law)

## [3] Kaplan+. Scaling Laws for Neural Language Models. 2020 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

14

## ②데이터셋 크기(D)와 오차(L) 사이에 성립하는 관계성.

## Loss

## = 교차 엔트로피

## 스케일 법칙(Scaling Law)

## [3] Kaplan+. Scaling Laws for Neural Language Models. 2020 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

15

## ③컴퓨팅 자원(C)과 오차(L) 사이에 성립하는 관계성.

## PF-days:

## Peta FLOPs days(1 Peta FLOPS

## 의 처리 속도를 가진 서버를 며칠분

## 학습에 사용했는가)

## ＊FLOPs: 다음 페이지

## 스케일 법칙(Scaling Law)

## [3] Kaplan+. Scaling Laws for Neural Language Models. 2020 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## ■보충 | 연산량의 단위 FLOPs

16

## • 연산량은 총 몇 회의 부동소수점 연산을 수행하는지로 표현된다

## • 부동소수점 연산의 예: 파라미터의 덧셈, 곱셈

## • 필요한 총 연산량을 나타내는 단위로 헷갈리지만 FLOPs가 사용된다

## • FLoating Points OPerations

## • 스케일 법칙의 가로축은 이것

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## ■보충 | FLOPs와 FLOPS

17

## •

## 이쪽이 FLOPS:

## •

## Floating Points

## Operation Per

## Second

## •

## 단위 시간당

## 얼마나 처리

## 할 수 있는지의 HW 성능

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

18

## ⚫Mega(M): 10^6

## ⚫Giga(G): 10^9

## ⚫Tera(T): 10^12

## ⚫Peta(P): 10^15

## ⚫Exa(E): 10^18

## ····

## 참고로,

## ⚫GPT-3의 총 연산량은 3.14 * 10^23 FLOPs.

## (최근 모델의 FLOPs는 상세가 비공개이므로 불명)

## ■보충 | 큰 숫자의 표현

## [9] Brown+. Language Models are Few-Shot Learners.

## 2020 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 스케일 법칙(Scaling Law)

19

## 각 파란 선은 서로 다른 모델 크기(파라미터)로

## 학습했을 때의 학습 곡선을 나타낸다.

## ③컴퓨팅 자원(C)과 오차(L) 사이에 성립하는 관계성.

## [3] Kaplan+. Scaling Laws for Neural Language Models. 2020 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 스케일 법칙(Scaling Law)

20

## 파라미터 수 N으로 학습했을 때의 학습 곡선

## 파라미터 수 N''으로 학습했을 때의 학습 곡선

## 파라미터 수 N'으로 학습했을 때의 학습 곡선

## *파라미터 수 N < N' < N''

## ③컴퓨팅 자원(C)과 오차(L) 사이에 성립하는 관계성.

## [3] Kaplan+. Scaling Laws for Neural Language Models. 2020 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 스케일 법칙(Scaling Law)

21

## *파라미터 수 N < N' < N''

## N

## N'

## N''

## 모델 크기가 작으면

## 적은 컴퓨팅 자원으로도

## 빠른 속도로 Loss가

## 내려가지만, 그 후

## 학습을 계속해도 Loss가

## 내려가기 어려워진다

## (포화, saturate)

## 모델 크기가 크면

## 적은 컴퓨팅 자원으로는 Loss가

## 좀처럼 내려가지 않지만,

## 학습을 계속하면 Loss가

## 계속 내려가 최종적으로

## 좋은 성능이 된다

## (포화되지 않는다)

## ③컴퓨팅 자원(C)과 오차(L) 사이에 성립하는 관계성.

## [3] Kaplan+. Scaling Laws for Neural Language Models. 2020 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 스케일 법칙(Scaling Law)

22

## *파라미터 수 N < N' < N''

## 이 정도(가로 점선) 수준의 Loss

## (성능)를 달성하는

## 데 최적인 모델 크기는

## "N'". N도 N''도 아니다.

## N

## N'

## N''

## ③컴퓨팅 자원(C)과 오차(L) 사이에 성립하는 관계성.

## [3] Kaplan+. Scaling Laws for Neural Language Models. 2020 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 스케일 법칙(Scaling Law)

23

## *파라미터 수 N < N' < N''

## 제한된 컴퓨팅 자원(세로 점선)으로 최고의 성

## 능(Loss)을 발휘하는 모델 크기는

## "N'". N도 N''도 아니다.

## N

## N'

## N''

## ③컴퓨팅 자원(C)과 오차(L) 사이에 성립하는 관계성.

## [3] Kaplan+. Scaling Laws for Neural Language Models. 2020 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 스케일 법칙(Scaling Law)

24

## *파라미터 수 N < N' < N''

## N

## N'

## N''

## 즉, 이 직선은 "임의의

## 컴퓨팅 자원량이 주어졌을 때,

## 그 컴퓨팅 자원 내에서 최고의

## 성능을 발휘하는

## 파라미터 크기의 모델이

## 도달 가능한 Loss 값(최적점)

## 의 집합"을 의미한다.

## ③컴퓨팅 자원(C)과 오차(L) 사이에 성립하는 관계성.

## [3] Kaplan+. Scaling Laws for Neural Language Models. 2020 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## ■보충 | 스케일 법칙(Scaling Law)이라는 이름의 유래

25

## α: 이중 로그 그래프 상의 기울기

## Xc: 절편(과 같은 것)

## X: 스케일 법칙의 변수(C 또는 D 또는 N)

## 이중 로그 상의 기울기

## 거듭제곱으로 표현 가능

## [3] Kaplan+. Scaling Laws for Neural Language Models. 2020 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## GPT-3에서의 스케일 법칙(OpenAI, 2020)

26

## •

## GPT-3에서도 스케일 법칙

## 이 이용되고 있다

## •

## 선행 연구(*)보다

## 2 자릿수 오더 더 큰

## 연산량의 스케일 법칙

## 을 확인했다.

## (*) "Scaling Laws for Neural Language Models", 2020

## [9] Brown+. Language Models are Few-Shot Learners. 2020 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## ■보충 | 스케일링은 새로운 현상인가?

27

## •

## 적어도 2017년 Baidu Research에서 검증되었다

## •

## 이 연구에서는 스케일 법칙의 발생을 다수의 도메인(기계 번역, 언어 모델링, 이미지

## 분류, 음성 인식 등)에서 검증하고 있다.

[8] Hestness+. Deep Learning Scaling is Predictable, Empirically. 2017 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## ■초기의 스케일 법칙(Baidu, 2017)

28

## 공통점

## 데이터에 관한 스케일 법칙

## 을 검증(모델도 약간)

## 왼쪽은 MT(기계 번역)의 예.

## 차이점

## 1. 대상 모델이 다름

## (Transformer 이전)

## 2. 규모가 다름

## (특히 모델)

## LSTM: RNN형 언어 모델의 한 종류

## [8] Hestness+. Deep Learning Scaling is Predictable, Empirically. 2017 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 다른 모델 구조에서의 검증

29

## 모델 구조의 탐색

## 깊이

## [3] Kaplan+. Scaling Laws for Neural Language Models. 2020 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## Mixture of Expert Model의 스케일 법칙

30

## 그림의 점선이 일반적인 Transformer, 실선이

## Mixture of Expert(MoE)

## Q. MoE란? A. Day 5에서 다룹니다.

[27] Clark+. Unified Scaling Laws for Routed Language Models. 2022 에서 인용

## [64] Ludziejewski+. Scaling Laws for Fine-Grained Mixture

## of Experts. 2024 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 다양한 도메인에서의 스케일 법칙(연산량과 Loss)

31

## 이미지 생성, 멀티모달, 동영상, 수리 등에서도 연산량에 관한 스케일 법칙이 성립

## [11] Henighan+. Scaling Laws for Autoregressive Generative Modeling.

## 2020 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## LLM 학습에 필요한 연산량과 파라미터 수, 토큰 수의 관계

32

## •자주 사용되는 근사식: 6 × N(파라미터 수)× D(토큰 수)

## (예) GPT-3의 경우

## 175B × 0.3T × 6 ≒ 3.14 * E+23 FLOPs

## •왜 6인가? A. 1파라미터당 MLP 층에서의 행렬 연산 횟수가 6회이기 때문.

## Forward

## Backward

## [47] Bahdanau. The FLOPs Calculus of Language Model Training.

## Medium. 2022 에서 인용

## h(i)와 w를 곱한다

## a(j)에 더한다

## a(j)로부터의 기울기를 h(i)에 전한다

## 그 기울기를 집약한다

## w에 대한 기울기를 계산한다

## 그 기울기를 집계한다

## [9] Brown+. Language Models are Few-Shot Learners. 2020 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## ■보충 | Attention은 무시해도 되는가?

33

## •시계열 길이가 짧은 경우,

## MLP의 연산량 >> Attention 기구의 연산량(자세한 내용은 상기 URL을 참조)

## •최근에는 시계열 길이가 길어지는 경향이 있어, 무시할 수 없게 되었을 가능성이 높다.

## •GPT-3: 2,049 토큰(*)

## •ChatGPT: 16,385 토큰(*)

## •GPT-4: 32,768 토큰(*)

## •보다 정확한 계산식 예: https://github.com/karpathy/nanoGPT/blob/master/scaling_laws.ipynb

## [47] Bahdanau. The FLOPs Calculus of Language Model Training. Medium. 2022 에서 인용

## (*) [63] OpenAI. Models overview - OpenAI API Documentation. 2023 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 미니 퀴즈

34

## •전제 | 계산 환경의 연산 능력을 아래와 같이 가정한다

## GPU A100 × 1기: O(E+14 FLOPS)

## ※ 이쪽은 단위 시간당 연산량이므로 대문자

## •퀴즈 | A100을 1000기 사용한다고 할 때, GPT-3 학습에는 어느 정도의 학습 시간이 필요한가?

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## ■여기까지의 정리 | 스케일 법칙이란 무엇인가

35

## •

## 스케일 법칙이란 컴퓨팅 자원(C), 데이터셋 크기(D),

## 파라미터 수(N)와 오차(L) 사이에 성립하는 다음과 같은 경험칙

## •

## 𝐿𝑋 =

## ൗ

## 𝑿𝒄𝑋

## 𝜶

## •

## 거듭제곱 형태를 띤다

## •

## Transformer 이외의 모델, 언어 이외의 태스크에서도 스케일 법칙은 확인되

## 어 있다

## •

## 연산량: FLOPs

## •

## C(연산량) = 6 × N(파라미터 수)× D(토큰 수)

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

36

## 목차

36

## ○스케일 법칙이란 무엇인가

## ○스케일 법칙의 사용 방법

## ○스케일 법칙의 구체적인 구하는 방법

## ○새로운 트렌드: 추론 시의 스케일링

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## (재게시) 스케일 법칙(Scaling Law)

37

## DL에서의 스케일 법칙이란?

## 1. 컴퓨팅 자원(C)

## 2. 데이터셋 크기(D)

## 3. 파라미터 수(N)

## 와 오차(L) 사이에 성립하는 다음 경험칙.

## ※ 다른 2개의 변수가 충분히 큰 경우.

## [3] Kaplan+. Scaling Laws for Neural Language Models. 2020 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

38

## "GPT-4 Technical Report" [13] 에서 발췌

## X축: GPT-4를 1.0으로 한 연산량

## Y축: 성능

## ⇒ 1/1000 정도의 모델까지로

## 성능을 정확하게 예측할 수 있다.

## ※ GPT-4의 파라미터 수는 공개되지 않았지만

## 아무리 작아도 10^10(10B)보다는 크다.

## 왼쪽 그림의 최소가 10^3이라고 하면 10^13(1T)

## "Scaling laws de-risk investments in large models"

## Q. 어떤 모델을 1T까지 스케일해야 하는가?

## [13] OpenAI. GPT-4 Technical Report. 2023 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 보다 정밀한 모델 선택

39

## 모델 구조의 탐색

## 하이퍼파라미터 탐색

## 스케일해도 아마

## Transformer > LSTM

## 파라미터 작다 => 층이 적은 쪽이 좋다

## 파라미터 크다 => 층이 많은 쪽이 좋다

## Q. 모델 A와 모델 B는 어느 쪽이 성능이 좋은가?

[3] Kaplan+. Scaling Laws for Neural Language Models. 2020

## 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 스케일링으로 누릴 수 있는 혜택 | 효율성

40

## 파라미터 수가 많을수록

## 샘플 효율은 좋다

## 작은 모델에서는 학습 도중부터 Loss가 내려가기 어려워진다 -> 어떤

## Loss를 달성하는 데 작은 모델로 연산을 계속하는 것은 비효율적

[3] Kaplan+. Scaling Laws for Neural

## Language Models. 2020 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 주어진 연산량 하에서 최적인 파라미터 수와 토큰 수를 찾는다

41

## •

## 연산량을 고정했을 때, 파라미터 수와 토큰 수를 변동시킨 경우의 플롯

## •

## 왼쪽: Chinchilla, 오른쪽: PaLM2

## •

## 어느 연산량에서든 U 커브가 되어 있으며, 최적인 값이 있어 보인다

## [42] Hoffmann+. Training Compute-Optimal Large Language Models. 2022 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## Chinchilla: 최적 연산 배분에 기반해 N과 D를 결정한 모델

42

## 주어진 연산량(이 곡선의 경우

## 1e19 FLOPs)하에서, 서로 다른 파라미

## 터의 모델(50M, 100M, 300M,

## 1B···)을 각각 학습하고, 각 모델

## 의 최종 Training Loss를 플롯

## 하면 U 커브가 만들어진다.

## Q: 왜 아래가 U 커브가 되는가? ≒ 왜

## 우하향하는 선이 되지 않는가?

## A: 더 큰 파라미터 크기의 모델

## 일수록 학습 초기의 Loss가 내려가

## 기 어렵기 때문(전페이지의 우 그림을 참조).

## [42] Hoffmann+. Training Compute-Optimal Large Language Models. 2022 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## Chinchilla: 최적 연산 배분에 기반해 N과 D를 결정한 모델

43

## 각 곡선마다 Training Loss가 최소가

## 되는 포인트가 존재한다(그림의

## ☆). 이들이 각 연산량(각

## FLOPs)에서의 최적인 파라미

## 터 크기.

## 연산량을 바꾸어, 같은 방법으로 곡선을

## 그려 최적인 파라미터 크기를 도출

## 해 가면, FLOPs와 Parameter

## 사이의 최적 관계를 도출할 수

## 있다. 거의 직선 관계임을 알

## 수 있다.

## [42] Hoffmann+. Training Compute-Optimal Large Language Models. 2022 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## Chinchilla: 최적 연산 배분에 기반해 N과 D를 결정한 모델

44

## • 연산량 고정으로 토큰 수와 파라미터 수를 변동시킨 결과(왼쪽)

## 참고) FLOPs = 6 × N(파라미터 수)× D(토큰 수)

## • 이 결과를 각 FLOPs에서의 최적인 파라미터로 바꾼 것(가운데)

## • 마찬가지로 토큰 수에 대해 최적인 값을 구한 것(오른쪽)

## [42] Hoffmann+. Training Compute-Optimal Large Language Models. 2022 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## Chinchilla: 최적 연산 배분에 기반해 N과 D를 결정한 모델

45

## 데이터 크기 D

## 토큰을 1.4T까지 증가

## (같은 데이터의 다른 서브셋)

## ※ Gopher의 약 4.6배

## 모델 크기 N

## 70B로 설정

## ※ Gopher의 약 1/4배

## 결과

## 많은 케이스에서 더 거대한 모델에 승리

## (발견한 관계식의 타당성을 시사)

## 최적 토큰 수 = 20 * 파라미터 수

## [42] Hoffmann+. Training Compute-Optimal Large Language Models. 2022 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## PaLM2에서의 스케일 법칙(Google, 2023)

46

## PaLM2에서도 같은 실험이 수행되었으며, Chinchilla와 마찬가지의 스케일 법칙이 확인되었다.

## [10] Anil+. PaLM 2 Technical Report. 2023 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## Chinchilla 법칙을 넘는 양의 학습

47

## "Go smol or go home, Why we should train smaller LLMs on more tokens"에서 발췌

## • Chinchilla Trap:

## Chinchilla의 모델 크기(70B)는

## 크기 때문에 추론 비용이 높다*.

## 추론 비용도 고려하여 더

## 작은 모델을 더 오래

## 학습시켜야 한다는 의견

## • 최적 모델 크기의 40-60% 이내의

## 모델 크기를 선택하여,

## 10-42%의 연산량 추가로 동일 성능의

## 모델을 학습할 수 있다는 지적

## 같은 성능을 달성하기 위해

## 필요한 파라미터 크기(가로축)

## 와 연산량(세로축)의 관계

[43] de Vries. Go smol or go home, Why we should train smaller LLMs on more tokens.

## Harm de Vries Blog. 2023 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## Q. Chinchilla 법칙은 정말 *최적*인가?

48

## 학습만 보면, 큰 모델

## 쪽이 작은 모델보다 같은

## FLOPs로 높은 성능을 발휘한다

## 한편, 추론 시에는 큰 모델

## 쪽이 작은 모델보다 더

## 많은 FLOPs를 필요로 한다

## 학습과 추론의 트레이드오프가 발생

## 학습과 추론 양쪽의 FLOPs를 고려

## 한 최적해(토큰 수, 파라미

## 터 수)를 도출하는 편이 좋지

## 않을까?

## [50] Sardana+. Beyond Chinchilla-Optimal: Accounting for Inference in Language Model Scaling Laws. 2024 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 추론 시 비용을 고려한 최적인 토큰 수

49

## •가로축: 추론 시 토큰 수의 가정

## •색: 학습 시 토큰 수를 Chinchilla

## 에 대해 몇 배로 할 것인가(1.01 ~ 40)

## •추론 횟수가 많아질수록 라이프타임

## 전체로는 학습 토큰 수를 늘리는 쪽이

## 유리

## 추론 시 토큰 수와 달성하고자 하는 학습 Loss를 가정했을 때, 라이프

## 타임 전체의 총 FLOPs를 최소로 하는 최적인 파라미터 수 및

## 학습 시 토큰 수

## [50] Sardana+. Beyond Chinchilla-Optimal: Accounting for Inference in Language Model Scaling Laws. 2024 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## ■참고 | 다양한 모델의 Token to Parameter Ratio(D/N)

50

## Params (N)

## Token (D)

## D/N

## Gopher

## 280B

## 0.3T

## 1.07

## Chinchilla

## 70B

## 1.4T

## 20.0

## Llama 2

## 7B

## 1.8T

## 285

## 70B

## 1.8T

## 28.5

## Llama 3

## 70B

## 15T

## 214.2

## 405B

## 15T

## 37.7

## Qwen 3

## 32B

## 36T

## 1125

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## ■보충 | 예측 가능한 개선과 예측 불가능한 개선

51

[12] Ganguli+. Predictability and Surprise in Large Generative Models. 2023 에서 인용

## 예측 가능한 예

## •스케일 법칙에 따른 성능의 개략 산정

## •일반적인 문장의 다음 단어 예측 정확도

## •번역 태스크나 QA 태스크에서의 평균적인 점수 개선

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 예측 불가능한 성질의 예 | Emergent Ability

52

## 모델 크기를 거대하게 하면 성능이 "갑자기" 대폭 올라가는 태스크가 있다

## [4] Wei+. Emergent Abilities of Large Language Models. 2022 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## ■보충 | 정말 창발 능력인가?

53

## •정말 "창발" "상전이" 하고

## 있는지에 대해서는 반론도 있다

## – 성능의 측정 방법에 의존(왼쪽 그림)

## ※ 이것은 본 논문에서도 지적됨

## – 가로축이 로그인 것은 이상하지 않은가

## – 애초에 무엇을 창발이라 할 것인가?

## •거대 모델 | 거대 연산으로 생각보다

## 잘하게 되는 것은 사실

## [5] Schaeffer+. Are Emergent Abilities of Large Language Models a Mirage?. 2023 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 예측 불가능한 성질의 예 | Grokking

54

## "Progress measures for grokking via

## mechanistic interpretability", ICLR2023

## "Grokking: Generalization Beyond Overfitting on

## Small Algorithmic Datasets", 2022

## 학습을 계속하면 갑자기 검증 데이터에서의 정답률이 높아지는 현상

## (학습 데이터에서의 정답률은 그 이전에 이미 높다. 즉 과적합 후에도 학습을 계속하면 발생하는 현상)

## (아래는 a○b = c(예: x+y=?)라는 태스크에서의 성능 조사)

## [6] Power+. Grokking: Generalization Beyond Overfitting on Small Algorithmic Datasets. 2022 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## ■보충 | Grokking 중에 모델 내부에서 무슨 일이 일어나는가?

55

## 유사 연구: "Progress measures for grokking via mechanistic interpretability", ICLR2023

## A. 기억을 일반화하고 있다(위는 학습 과정의 시각화).

## 과학습 중(가운데)은 기억만 하고 있지만, 일반화 후(오른쪽)에는 숫자가 깔끔하게 정렬.

## [7] Liu+. Towards Understanding Grokking: An Effective Theory of Representation Learning. 2022 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 다양한 도메인에서의 스케일 법칙(연산량과 Loss)

56

## 어떤 연산량이 주어졌을 때의 최적인 모델 크기의 도메인 간 비교

## 어느 도메인이든 대체로 비슷한 경향을 보인다

## [11] Henighan+. Scaling Laws for Autoregressive Generative Modeling. 2020 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 다운스트림 태스크의 성능과 스케일 법칙

57

## •

## WebText2: 통상의 테스트 데이터, 그 외: 학습 외의(분포 외) 데이터

## •

## WebText2 이외에서는 성능 열화가 보이지만, 오프셋의 차이 정도이며

## 경향은 같다(기울기도 거의 같다)

## [3] Kaplan+. Scaling Laws for Neural Language Models. 2020 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 스케일 법칙이 가져오는 것

58

## 다운스트림 태스크의 성능과의 관계성

## Q. Loss(사전학습의 교차 엔트로피)가 낮다 = 다운스트림 태스크의 성능이 높은가?

## ①깔끔하게 상승

## ②갑자기 상승

## (Emergent Ability)

## ③오르지 않는다

## ④내려갔다가 오른다

## (Inverse scaling prize)

## •기본적으로는 YES.

## •예외도 자주 있다(예: 아래 그림 ②~③)

## •태스크의 종류나 난이도에 따른다

## "GPT-4 Technical Report", 2023

## "Language Models are Few-Shot Learners", 2020

## ①~③: [9] Brown+. Language Models are Few-Shot Learners. 2020 에서 인용, ④: [13] OpenAI. GPT-4 Technical Report. 2023 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 스케일 법칙이 가져오는 것

59

## 다운스트림 태스크의 성능과의 관계성

## [69] Isik+. Scaling Laws for Downstream Task Performance in Machine Translation. 2024 에서 인용

## 기계 번역 태스크에 의한 검증 결과: 사전학습 데이터(*1)와 다운스트림 태스크 데이터(*2)

## 의 분포 간 거리(*3)가 정렬되어 있는 경우에는 사전학습 데이터량과 다운스트림 태스

## 크의 평가값 사이에 스케일 법칙이 성립한다.

## (*1) MC4(Multilingual C4) (*2) 기계 번역 태스크 (*3) Embedding 공간에서의 분포 거리를 측정

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 여기까지의 정리 | 스케일 법칙의 활용 방법 분류

60

## 예측 가능한 성능 개선에 의해, 다음과 같은 물음에 답할 수 있다.

## •

## 투자의 판단 | 더 많이 컴퓨터에 투자할 것인가?

## •

## 효율적인 모델 선택 | 파라미터를 늘렸을 때 어느 쪽이 좋은 모델인가?

## •

## 효율적인 컴퓨팅 자원 이용 | 토큰과 파라미터 중 어느 쪽을 늘려야 하는가?

## •

## Chinchilla Optimal: 최적 토큰 수 = 20 * 파라미터 수

## •

## 추론 비용을 고려하면 최적 토큰 수의 계수는 변화한다

## •

## 다운스트림 태스크에 스케일 법칙이 반드시 성립한다고는 한정하지 않는다(선형이 된다고는 한정하지 않는

## 다)

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

61

## 목차

61

## ○스케일 법칙이란 무엇인가

## ○스케일 법칙의 사용 방법

## ○스케일 법칙의 구체적인 구하는 방법

## ○새로운 트렌드: 추론 시의 스케일링

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

62

## 스케일 법칙의 측정 방법

62

## 기본적으로는(비교적)작은 몇 가지 조건으로 실험하여 Fitting 한다

## Q. 모델 크기는 어떻게 바꿀 것인가?

## Q. 학습률 등의 하이퍼파라미터는 어떻게 설정할 것인가?

## "GPT-4 Technical Report" [13]

## [42] Hoffmann+. Training Compute-Optimal Large Language Models. 2022 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

63

## Q1. 모델 크기를 어떻게 변화시키는가?

63

## •

## 층 수를 늘린다

## •

## 임베딩 차원을 올린다

## •

## FFN의 중간층 차원을 크게 한다

## •

## 헤드 수를 늘린다

## •

## 기타 등등…

## •

## 어느 것을 어느 정도 할 것인가?

[65] Vaswani+. Attention Is All You Need. 2017 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 모델 크기를 어떻게 변화시키는가?

64

## 원 논문에서는 파라미터 수를 고정했을 때 신경망의 몇 가지 요소를

## 조정하여 검토하고 있다 => 결과적으로 큰 영향은 없다는 결론

## 예: 종횡비(aspect ratio): 임베딩 크기 / 층 수

## ＊가로와 세로의 비율이라는 이미지

## [3] Kaplan+. Scaling Laws for Neural Language Models. 2020 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 사례 1 | Llama 3

65

## 종횡비는 각각 128, 102.4, 130

## Model vs. FFN Dimension은 모두 3.5

## 헤드 수도 Model Dimension에 대해 마찬가지로 스케일

## [66] AI@Meta+. The Llama 3 Herd of Models. 2024 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 사례 2 | Cerebras GPT

66

## 종횡비는 각각 76.8, 77.7, 85.3, 85.3 …

## Model vs. FFN Dimension은 모두 4.0

## 헤드 수는 다소 불규칙하게 변화

## [51] Dey+. Cerebras-GPT: Open Compute-Optimal Language Models Trained on the Cerebras Wafer-Scale Cluster. 2023 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## Q2. 하이퍼파라미터를 어떻게 변화시키는가?

67

## 학습률과 스케줄링이 제각각

## 모델 파라미터 크기가 클수록 학습률은 점차 작게, 배치

## 크기는 크게 하는 경향이 있다.

## !!!!?

## [51] Dey+. Cerebras-GPT: Open Compute-Optimal Language Models Trained on the Cerebras Wafer-Scale Cluster. 2023 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 통상 초기화의 경우, 최적인 하이퍼파라미터는 변동한다

68

## •

## 폭(width)을 변화시켰을 때의 최적인

## 학습률의 플롯

## •

## 폭에 따라 최적인 하이퍼파라미터는 변

## 동한다(다만 어느 정도 경향은

## 있다)

## 경험칙으로서, 모델 크기를 크게

## 했을 때 학습률은 작게,

## 배치 크기는 크게 하는 것이 좋은

## 경향

## [52] Yang+. Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer. 2022 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## μTransfer: 최적인 하이퍼파라미터를 전이 가능한 방법

69

## μTransfer를 사용하면 모델 크기가 달라도 거의 같은

## 정도의 learning rate 값으로 최적인 Loss를 달성할 수 있다

## [52] Yang+. Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer. 2022 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

70

## μTransfer: 최적인 하이퍼파라미터를 전이 가능한 방법

## 가중치 초기화 방법과, weight별 Learning rate 설정 방법을 아래와 같이 변경한다(빨간 글씨)

## [52] Yang+. Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer. 2022 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 사례 | Cerebras GPT + μTransfer

71

## μTransfer를 사용하는 경우

## 일반적인 파라미터 설정

## 즉, 작은 모델에서 최적인 Learning Rate를 찾고, 그 값

## 을 큰 모델에 제로샷으로 전이할 수 있다.

## [51] Dey+. Cerebras-GPT: Open Compute-Optimal Language Models

## Trained on the Cerebras Wafer-Scale Cluster. 2023 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 여기까지의 정리 | 스케일 법칙의 구하는 방법

72

## •

## 스케일 법칙을 구하기 위해서는 기본적으로 몇 가지 설정으로 실험을 수행하고

## 피팅하면 된다.

## •

## 하지만 스케일시킬 때 몇 가지 문제가 발생할 수 있다

## •

## 문제 1. 모델 크기를 어떻게 스케일시킬 것인가?

## • A. 대체로 고정된 계수를 유지하면서 스케일한다

## •

## 문제 2. 모델 크기를 스케일시킬 때 하이퍼파라미터는 어떻게 바꿀 것인가?

## • A. 논문에 따라 다르지만, 대체로 학습률은 점차 작게, 배치 크기는 크게

## 한다. μTransfer라는 방법도 있다.

## •

## 스케일 법칙의 상세에 더 관심 있는 분은 아래를 참조

## •

## [62] Tatsunori Hashimoto, Percy Liang. CS336: Language Modeling from Scratch.

## Stanford University. 2024

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

73

## 목차

73

## ○스케일 법칙이란 무엇인가

## ○스케일 법칙의 사용 방법

## ○스케일 법칙의 구체적인 구하는 방법

## ○새로운 트렌드: 추론 시의 스케일링

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

74

## Motivation

74

## 문제 1: "바나나의 색은 무엇입니까?"

## 문제 2: "스케일 법칙의 문제는 무엇이라고 생각합니까?"

## 두 질문은 필요한 사고의 과정이 분명히 다르다고 여겨진다.

## 후자는 추론 시에 더 부하가 걸린다.

## Q. 이러한 구조를 LLM에서 어떻게 실현할 수 있는가?

## Q. 이러한 구조는 LLM에서 효과적인가?

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## Q. 이러한 구조는 LLM에서 효과적인가? A. Yes

75

## •

## OpenAI가 발표한 o1도 테스트 시의 추론을 스케일링시킴으로써 성능 향상을 보고

## [53] OpenAI. Learning to reason with LLMs. OpenAI Blog. 2024 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## (Day 2 복습) 추론 시에 연산량을 스케일시키는 방법의 예

76

## Chain-of-Thought Prompting

## Many-Shot ICL

## 프롬프팅에 의해 추론 시의 토큰 수를 늘림으로써 추론 시의 연산량을

## 스케일시키는 시도

[67] Wei+. Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. 2022 에서 인용

## [68] Agarwal+. Many-Shot In-Context Learning. 2024 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## •Decoding을 복잡하게 한다

## •사전학습된 LLM을 사용하여 텍스트를 출력(디코드)한다.

## •디코드에는 다양한 방식이 존재한다.

## •Greedy Decoding

## •Beam Search

## •Random Sampling

## •Top K / Top P Sampling

77

## (Day 2, 3 복습) 추론 시에 연산량을 스케일시키는 방법의 예

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 다양한 디코딩 방법

78

## •

## 디코드 방식 일람

## •

## 다양한 방식이 제안되어 있다

## [54] Madaan+. From Decoding to Meta-Generation: Inference-time Algorithms for Large Language Models. 2024 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## 발전적인 디코딩 방법의 예 | Contrastive Decoding

79

## Contrastive Decoding

## •

## 외부 모델을 사용하는 방법의 예

## •

## 전문가 모델과 아마추어

## 모델을 이용하여 확률밀도비를 취하고

## 거기서부터 샘플링을 수행

## •

## 아마추어 모델에는 통상 전문가

## 모델보다 더 적은 파라미

## 터 수의 모델을 사용

## •

## 전문가 모델의 출력을 더

## 강조하고, 아마추어 모델의 출력

## 을 감소시키도록 생성을 수행

## [55] Li+. Contrastive Decoding: Open-ended Text Generation as Optimization. 2023 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

80

## Meta Generation이란? Token Level의 Decoding뿐만 아니라, 문장이나 단락

## 마다 생성 과정을 평가하고, 생성 프로세스 전체를 최적화하는 개념

## From Decoding to Meta-Generation

## [56] Snell+. Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters. 2024 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

81

## ①Parallel search

## 예: Best-of-N, Self-Consistency

## •

## 병렬로 여러 후보를 생성하여 스코어링이나 다수결 등으로 생성물을 선택

## ②Step level search

## 예: Process Reward Model(PRM)

## •

## Step 레벨에 평가를 수행하여 생성물을 선택

## ③Refinement

## 예: Self-Refine

## •

## 외부/내부의 피드백 결과를 이용하여 반복적으로 생성 결과를 갱신

## Meta-Generation의 종류(어느 쪽이든 추론 시에 연산량이 크게 스케일)

## [54] Madaan+. From Decoding to Meta-Generation: Inference-time Algorithms for Large Language Models. 2024 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

82

## Best-of-N

## •

## N개의 답변을 내어 스코어가 가장 높은 것을

## 선택한다

## •

## 스코어 함수는 임의(태스크에 따라 구분하여 사용)

## •

## 예: LLM의 스코어를 사용

## •

## 예: 학습한 평가기를 사용

## •

## 예: BLEU 등 특정 지표를 사용

## ①Parallel Search의 방법 예 | Best-of-N

## [56] Snell+. Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters. 2024 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

83

## Self-Consistency(Day 2 복습)

## •

## LM에 복수의 추론을 수행시켜(아래는 3가지 예) Majority Voting(다수결)

## ①Parallel Search의 방법 예 | Self-Consistency

## [58] Wang+. Self-Consistency Improves Chain of Thought Reasoning in Language Models. 2023 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## ①Parallel Search의 방법 예 | MBR Decoding

84

## MBR Decoding(Minimum Bayes-Risk Decoding)

## •

## 기계 번역 시 사용되는 디코딩 방법

## •

## 효용 함수를 이용하여 출력의 품질을 최대화하도록 디코딩

## •

## 기계 번역에서의 효용 함수: BLEU, METEOR, BLEURT, COMET

## •

## 상세가 알고 싶은 분은 URL

## [57] Eikema+. On the True Distribution Approximation of Minimum Bayes-Risk Decoding. 2020 에서 인용

## •y: 모델의 출력문

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## ①Parallel Search의 다른 방법

85

## Aggregation type이나 Scoring의 기법에 따라 다양한 알고리즘이 존재

## [56] Snell+. Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model

## Parameters. 2024 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## ②Step Level Search의 방법 예 | Beam-Search(Step Level)

86

## Beam-Search(Step Level)

## •

## Token Level의 Beam Search와는 달리,

## 문장이나 단락 단위로 샘플링과 평가를 수행

## •

## 평가에는 PRM(Process Reward Model)을

## 이용하여 중간 결과의 평가와 선택을 수행

## •

## Top-N Sampling으로 중간 결과를 선택

## [56] Snell+. Scaling LLM Test-Time Compute Optimally can be More Effective than

## Scaling Model Parameters. 2024 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## ②Step Level Search의 방법 예 | Tree-of-Thought

87

## Tree-of-Thought

## •

## 복수의 사고열을 단번에 출력하여 평가하는 SC와 달리, ToT는 도중에 분기시

## 킨다(트리 탐색)

## • 노드의 평가도 LM으로 수행

## •

## Game of 24에서의 예와 결과

## • 태스크: 주어진 4개의 숫자를 사칙연산하여 24를 만든다

## •

## 전략적 사고가 필요한 태스크에서 성능이 대폭 개선

## [60] Yao+. Tree of Thoughts: Deliberate Problem Solving with Large Language Models. 2023 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## ②Step Level Search의 다른 방법

88

## 탐색 방법나 검증하는 스텝의 차이 등에 의해 다양한 알고리즘이 존재

## [56] Snell+. Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters. 2024 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

89

## •

## 한 번 생성한 결과나 그 결과에 대한 피드백을 바탕으로 재생성

## [59] Lightman+. Let's Verify Step by Step. 2023 에서 인용

## ③Refinement

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

90

## 자기 자신을 사용하여 피드백을 생성하고 출력을 개선

## [61] Madaan+. Self-Refine: Iterative Refinement with Self-Feedback. 2023 에서 인용

## ③Refinement의 방법 예 | Self-Refine(Day 2 복습)

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

91

## •

## 7개의 태스크에서 최대 50% 가까운 정확도 향상

## [61] Madaan+. Self-Refine: Iterative Refinement with Self-Feedback. 2023 에서 인용

## ③Refinement의 방법 예 | Self-Refine(Day 2 복습)

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## Majority Voting vs. Best-of-N(ORM)

92

## [59] Lightman+. Let's Verify Step by Step. 2023 에서 인용

## Best-of-N(ORM)

## •

## Outcome-supervised Reward Model

## 을 사용하여 출력 전체를 평가

## Majority Voting

## •

## 다수결로 선택

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## Majority Voting vs. Best-of-N(ORM) vs. Best-of-N(PRM)

93

## [59] Lightman+. Let's Verify Step by Step. 2023 에서 인용

## Best-of-N(PRM)

## •

## Process-supervised Reward Model

## 을 이용하여 도중의 가정을 평가

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## Q. 같은 컴퓨팅 자원일 때, 파라미터를 늘리는 것보다 효과적인가?

94

## [56] Snell+. Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters. 2024 에서 인용

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## Q. 같은 컴퓨팅 자원일 때, 파라미터를 늘리는 것보다 효과적인가?

95

## •

## 랜덤 샘플링에 의한 추론 횟수를 늘리고, 프로세스 레벨의 보상 모델

## (PRM)을 이용한 추론 경로/최종 답변의 적절한 선택으로 성능이 향상.

## Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters 에서

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## Q. 같은 컴퓨팅 자원일 때, 파라미터를 늘리는 것보다 효과적인가?

96

## •

## 랜덤 샘플링에 의한 추론 횟수를 늘리고, 프로세스 레벨의 보상 모델

## (PRM)을 이용한 추론 경로/최종 답변의 적절한 선택으로 성능이 향상.

## Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters 에서

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

97

## 오늘의 정리

97

## 언어 모델의 스케일 법칙에 대해 소개했습니다.

## 1.스케일 법칙이 무엇인지에 대해 설명했습니다.

## 스케일 법칙이란 컴퓨팅 자원(C), 데이터셋 크기(D), 파라미터 수(N)와 오

## 차(L) 사이에 성립하는 경험칙; 로그 그래프 상에서 거의 직선 관계가 성립한다.

## 3.추론 시의 스케일링이 무엇인지에 대해 설명했습니다.

## 학습 시뿐만 아니라 추론 시에도 연산량을 스케일시킴으로써 성능을

## 개선할 수 있다. 추론 시의 공부: Prompting, Decoding, Meta-Generation

## 2.스케일 법칙의 구체적인 구하는 방법에 대해 설명했습니다.

## 스케일 법칙을 구하기 위해서는 기본적으로 몇 가지 다른 설정에서 실험을 수행하고

## 피팅한다. 하이퍼파라미터 설정(예: 종횡비, 학습률, 배치 사이

## 즈)에 대해서는 다양한 지견이 논문으로 발표되어 있다.

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## Reference

## 대규모 언어 모델 Day4

98

[1] Bao Hua Choo. The emergence of Large Language Models (LLMs), The low down. 2023. https://thelowdown.momentum.asia/the-emergence-of-large-

language-models-llms/, 접속일: 2023/11/16

[2] Zhao+. A Survey of Large Language Models. 2023. In arXiv:2303.18223v12

[3] Kaplan+. Scaling Laws for Neural Language Models. 2020. In arXiv:2001.08361

[4] Wei+. Emergent Abilities of Large Language Models. 2022. In arXiv:2206.07682v2

[5] Schaeffer+. Are Emergent Abilities of Large Language Models a Mirage?. 2023. In arXiv:2304.15004v2

[6] Power+. Grokking: Generalization Beyond Overfitting on Small Algorithmic Datasets. 2022. In arXiv:2201.02177v1

[7] Liu+. Towards Understanding Grokking: An Effective Theory of Representation Learning. 2022. In NeurIPS2022

[8] Hestness+. Deep Learning Scaling is Predictable, Empirically. 2017. In arXiv:1712.00409v1

[9] Brown+. Language Models are Few-Shot Learners. 2020. In NeurIPS2020

[10] Anil+. PaLM 2 Technical Report. 2023. In arXiv:2305.10403v3

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## Reference

## 대규모 언어 모델 Day4

99

[11] Henighan+. Scaling Laws for Autoregressive Generative Modeling. 2020

[12] Ganguli+. Predictability and Surprise in Large Generative Models. 2023. In arXiv:2202.07785v2

[13] OpenAI. GPT-4 Technical Report. 2023. In arXiv:2303.08774v3

[14] Abhinav Venigalla, Linden Li. Billion-Parameter GPT Training Made Easy. MosaicML. 2022. https://www.mosaicml.com/blog/billion-parameter-gpt-

training-made-easy, 접속일: 2023/11/16

[15] Vaswani+. Attention Is All You Need. 2017. In NeurIPS2017

[16] Jaiyam Sharma. Understanding Attention Mechanism in Transformer Neural Networks. LearnOpenCV. 2022. https://learnopencv.com/attention-

mechanism-in-transformer-neural-networks/, 접속일: 2023/11/16

[17] Villalobos+. Will we run out of data? An analysis of the limits of scaling datasets in Machine Learning. 2022. In arXiv:2211.04325v1

[18] Tay+. Efficient Transformers: A Survey. 2020. In arXiv:2009.06732v3

[19] Child+. Generating Long Sequences with Sparse Transformers. 2019. In arXiv:1904.10509v1

[20] Zahher+. Big Bird: Transformers for Longer Sequences. 2020. In NeurIPS2020

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## Reference

## 대규모 언어 모델 Day4

100

[21] Dao+. FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness. 2022. In NeurIPS2022

[22] Tri Dao. FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning. 2023. In arXiv:2307.08691v1

[23] Chen+. Towards Understanding Mixture of Experts in Deep Learning. 2022. In NeurIPS2022

[24] Shazeer+. Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer. 2017. In ICLR

[25] Fedus+. Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity. 2021. In arXiv:2101.03961v3

[26] Rajbhandari+. DeepSpeed-MoE: Advancing Mixture-of-Experts Inference and Training to Power Next-Generation AI Scale. 2022. In ICML2022

Proceedings of the 39th

International Conference on Machine Learning, PMLR 162:18332-18346

[27] Clark+. Unified Scaling Laws for Routed Language Models. 2022. In arXiv:2202.01169v2

[28] Zhai+. An Attention Free Transformer. 2021. In arXiv:2105.14103v2

[29] Peng+. RWKV: Reinventing RNNs for the Transform. 2023. In arXiv:2305.13048v1

[30] Sun+. Retentive Network: A Successor to Transformer for Large Language Models. 2023. In arXiv:2307.08621v4

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## Reference

## 대규모 언어 모델 Day4

101

[31] Gu+. Efficiently Modeling Long Sequences with Structured State Spaces. 2022. In ICLR2022

[32] Microsoft. DeepSpeed: 심층 학습의 학습과 추론을 극적으로 고속화하는 프레임워크.

https://www.deepspeed.ai/assets/files/DeepSpeed_Overview_Japanese_2023Jun7th.pdf. 접속일: 2023/11/16

[33] Rajbhandari+. ZeRO: Memory Optimizations Toward Training Trillion Parameter Models. 2019. In arXiv:1910.02054

[34] Microsoft. DeepSpeed. https://github.com/microsoft/DeepSpeed. 접속일: 2023/11/16

[35] DeepSpeed Team. Configuration JSON. https://www.deepspeed.ai/docs/config-json/. 접속일: 2023/11/16

[36] Belkada+. A Gentle Introduction to 8-bit Matrix Multiplication for Transformers at Scale using Hugging Face Transformers, Accelerate

and bitsandbytes. Hugging Face Blog. 2022. https://huggingface.co/blog/hf-bitsandbytes-integration#a-gentle-introduction-to-8-bit-

matrix-multiplication-for-transformers-at-scale-using-hugging-face-transformers-accelerate-and-bitsandbytes. 접속일: 2023/11/16

[37] Dettmers+. LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale. 2022. In NeurIPS2022

[38] Liu+. Do Emergent Abilities Exist in Quantized Large Language Models: An Empirical Study. 2023. In arXiv:2307.08072

[39] Penedo+. The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Data, and Web Data Only. 2023. In

arXiv:2306.01116

[40] Okanohara. MinHash에 의한 고속 유사 검색. Preferred Networks Research&Development. 2011.

https://tech.preferred.jp/ja/blog/minhash/. 접속일: 2023/11/16

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## Reference

## 대규모 언어 모델 Day4

102

[41] Cossu+. Continual Pre-Training Mitigates Forgetting in Language and Vision. 2022. In arXiv:2205.09357v1

[42] Hoffmann+. Training Compute-Optimal Large Language Models. 2022. In NeurIPS2022

[43] de Vries. Go smol or go home, Why we should train smaller LLMs on more tokens. Harm de Vries Blog. 2023.

https://www.harmdevries.com/post/model-size-vs-compute-overhead/. 접속일: 2023/11/16

[44] Sorscher+. Beyond neural scaling laws: beating power law scaling via data pruning. 2022. In NeurIPS2022

[45] Tirumala+. D4: Improving LLM Pretraining via Document De-Duplication and Diversification. 2023. In arXiv:2308.12284v1

[46] Zhou+. LIMA: Less Is More for Alignment. 2023. In arXiv:2305.11206v1

[47] Bahdanau. The FLOPs Calculus of Language Model Training. Medium. 2022. https://medium.com/@dzmitrybahdanau/the-flops-calculus-of-

language-model-training-3b19c1f025e4. 접속일: 2023/11/16

[48] Zhao+. A Survey of Large Language Models. 2023. In arXiv:2303.18223

[49] Gu+. Mamba: Linear-Time Sequence Modeling with Selective State Spaces. 2023. In arXiv:2312.00752

[50] Sardana+. Beyond Chinchilla-Optimal: Accounting for Inference in Language Model Scaling Laws. 2024. In ICML2024 (arXiv:2401.00448)

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## Reference

## 대규모 언어 모델 Day4

103

[51] Dey+. Cerebras-GPT: Open Compute-Optimal Language Models Trained on the Cerebras Wafer-Scale Cluster. 2023. In arXiv:2304.03208

[52] Yang+. Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer. 2022. In NeurIPS2022

[53] OpenAI. Learning to reason with LLMs. OpenAI Blog. 2024. https://openai.com/index/learning-to-reason-with-llms/. 접속일: 2026/05/25

[54] Madaan+. From Decoding to Meta-Generation: Inference-time Algorithms for Large Language Models. 2024. In arXiv:2406.16794

[55] Li+. Contrastive Decoding: Open-ended Text Generation as Optimization. 2023. In ACL2023

[56] Snell+. Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters. 2024. In arXiv:2408.03314

[57] Eikema+. On the True Distribution Approximation of Minimum Bayes-Risk Decoding. 2020. In EMNLP2020

[58] Wang+. Self-Consistency Improves Chain of Thought Reasoning in Language Models. 2023. In ICLR2023

[59] Lightman+. Let's Verify Step by Step. 2023. In ICLR2024 (arXiv:2305.20050)

[60] Yao+. Tree of Thoughts: Deliberate Problem Solving with Large Language Models. 2023. In NeurIPS2023

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스

## Reference

## 대규모 언어 모델 Day4

104

[61] Madaan+. Self-Refine: Iterative Refinement with Self-Feedback. 2023

[62] Tatsunori Hashimoto, Percy Liang. CS336: Language Modeling from Scratch. Stanford University. 2024. https://cs336.stanford.edu/

## [63] OpenAI. Models overview - OpenAI API Documentation. 2023. https://platform.openai.com/docs/models/overview. 접속일: 2023/09/14

[64] Ludziejewski+. Scaling Laws for Fine-Grained Mixture of Experts. 2024. 접속일: 2026/05/25

[65] Vaswani+. Attention Is All You Need. 2017

[66] AI@Meta+. The Llama 3 Herd of Models. 2024

[67] Wei+. Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. 2022

[68] Agarwal+. Many-Shot In-Context Learning. 2024

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츄오·이와사와 연구실, CC BY-NC-ND 4.0 라이선스
