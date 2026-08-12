# Day 5

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 주의사항: 본 자료의 재이용(2차 이용)에 대하여

## ●

## 본 자료에 대하여

## ○

## 도쿄대학교 마쓰오·이와사와 연구실이 작성하였으며, 2025년 10월부터 11월에 걸쳐 개최된 LLM 대규모 언어 모델 강좌 기초편

## 의 강의 자료입니다.

## ○

## 크리에이티브 커먼즈 CC BY-NC-SA 4.0 DEED(저작자표시– 비영리– 동일조건변경허락 4.0 국제) 라이선스 등록을

## 하고 있습니다.

## ●

## 라이선스 표기에 대하여

## ○

## 각 슬라이드 페이지 맨 아래에 라이선스 표기가 있습니다. 재이용 시에는 반드시 본 라이선스 표기를 기재해 주세요.

## 재이용 시 복제가 곤란한 경우에는 아래의 텍스트 박스를 이용하여, 하이퍼링크를 포함하여 라이선스 표기를

## 해 주시기 바랍니다.

## ○

## 재이용하는 페이지에 참고 논문 등의 인용이 있는 경우, 권말의 Reference에서 인용 위치를 게재해 주세요.

## ●

## 비영리 목적의 이용에 대하여

## 재이용(2차 이용)이 허락됩니다.

## ●

## 영리 목적의 재이용에 대하여

## 이쪽으로 문의해 주세요.

## ●

## 기타

## ○

## 원래의 표현이 바뀌지 않는 범위(폰트, 크기 등)라면 개변이 가능합니다.

## ○

## 그 이외의 개변이나 라이선스에 대한 자세한 내용은 이쪽을 확인하신 후 적절히 취급해 주시기 바랍니다.

## 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 5. Advanced Pre-training

## 대규모 언어 모델 강좌 2025

## 2025/10/29

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 야마다 이쿠야(山田育矢)

3

## Studio Ousia 최고 과학자(Chief Scientist)

## 나고야대학 수리·데이터 과학·인공지능 교육연구센터 객원 교수

## 도호쿠대학 언어 AI 연구센터 특임 교수(객원)

## 박사(학술)

## 주요 실적:

## •

## 다양한 언어 모델의 개발

## •

## 개발한 빨리누르기 퀴즈 AI가 전미 퀴즈왕 팀에 승리(NIPS Competition 2017)

## •

## 다수의 국제 콘테스트에서 좋은 성적 획득

## NeurIPS EfficientQA 2020 (2위), ISWC Challenge 2020 (1위),

## NIPS HCQA 2017 (1위), WSDM Cup 2017 (2위),

## NAACL HCQA 2016 (1위), ACL W-NUT 2015 (1위) 등

## 주요 저서:

## •

## 대규모 언어 모델 입문·대규모 언어 모델 입문 II

## •

## 딥러닝에 의한 자연어 처리

## https://ikuya.net

## ikuyamada

## ikuya@ikuya.net

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## LLM의 개발 단계

4

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## LLM의 개발 단계

5

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## Pre-training의 위치 설정

6

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## Pre-training의 위치 설정

7

## 제3회와 오늘의 토픽

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 사전학습은 어느 정도 중요할까?

8

[66]  iwiwi, github,

https://gist.github.com/iwiwi/fc174b1f2341c2c0170be87c5b2e1d31,

## GPT-4의 각 개발 태스크에 투입된 인원이 전체에서 차지하는 비율 ≒

## OpenAI가 생각하는 LLM 개발에서의 중요도 비율!?

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 중요한 질문: 사전학습을 직접 수행할 필요가 있을까? (1)

9

[65] weights & biases, 「LLM을 제로부터 트레이닝하기 위한 베스트 프랙티스」에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 중요한 질문: 사전학습을 직접 수행할 필요가 있을까? (2)

10

[65] weights & biases, 「LLM을 제로부터 트레이닝하기 위한 베스트 프랙티스」에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 중요한 질문: 사전학습을 직접 수행할 필요가 있을까? (3)

11

[65] weights & biases, 「LLM을 제로부터 트레이닝하기 위한 베스트 프랙티스」에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 복습 – 스케일 법칙 –

12

## 스케일 법칙: 언어 모델을 스케일(대규모화)시킴으로써 성능이 향상되는 관계

## 이하 3가지 요소와 성능(L) 사이에 성립하는 경험칙

## ■컴퓨팅 자원(C)

## ■데이터셋 크기(D)

## ■파라미터 수(N)

## ●

## 다양한 도메인에서 대규모 모델을 개발하는 장점이 확인되었다.

## ●

## 스케일 법칙에 의해, 대규모 모델에 대한 투자 리스크가 경감되었다.

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## Advanced Pre-training의 목적

13

## (*제3회의 속편)

## 언어 모델을 스케일(=대규모화)하여 사전학습하는 것의 발전적인 화제에 대해 학습한다.

## Goal 1

## 모델을 스케일하여 사전학습하는 데 있어 (발전적인) 과제를 설명할 수 있다.

## 모델을 스케일하여 사전학습하는 (발전적인) 방법을 설명할 수 있다.

## 사전학습의 일련의 흐름을 코드로 구현할 수 있다(모델을 스케일하기 위한 기술도 포함).

## Goal 2

## Goal 3

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 전체 흐름

14

## ●강의:

## ○각 요소의 스케일에 있어서의 문제점

## ○스케일하기 위한 기술

## ●연습:

## ○PyTorch로 트랜스포머 모델을 사전학습하기 위한 일련의 흐름을 구현

## (데이터 준비, 전처리부터 모델을 스케일하는 기술을 사용한 학습까지)

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 목차

15

## •

## 각 요소의 스케일에 있어서의 문제점

## •

## 스케일하기 위한 기술: 파라미터 수(N)에 관련하는 노력

## •

## 스케일하기 위한 기술: 계산량(C)에 관련하는 노력

## •

## 스케일하기 위한 기술: 데이터(D)에 관련하는 노력

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 목차

16

## •

## 각 요소의 스케일에 있어서의 문제점

## •

## 스케일하기 위한 기술: 파라미터 수(N)에 관련하는 노력

## •

## 스케일하기 위한 기술: 계산량(C)에 관련하는 노력

## •

## 스케일하기 위한 기술: 데이터(D)에 관련하는 노력

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 스케일시키는 데 있어서의 과제

17

## 파라미터, 계산량, 데이터를 스케일함으로써,

## 스케일 법칙에 따라 성능이 올라가는 것은 알겠으나,

## 스케일시키는 데 있어 다양한 과제가 있다.

## 계산량(C)

## 충분한 계산량/

## 메모리 용량을 확보하여

## 효율적으로 훈련할 필요

## 파라미터 수(N)

## 모델이 스케일됨에

## 따라 증가하는

## 비용을 억제할 필요

## 데이터(D)

## 성능을 발휘하기 위한

## 학습용 데이터를 준비할

## 필요

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## N, C: 모델 크기 증가에 수반하여 필요한 비용이 증가

18

## "Mosaic LLMs (Part 1): Billion-Parameter GPT Training Made Easy" [14] 에서 발췌

## →효율적으로 대규모 모델을 훈련할 수 있다면, 비용을 줄일 수 있다

[14] Abhinav Venigalla, Linden Li, Billion-Parameter GPT Training Made Easy, MosaicML에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## N, C: 트랜스포머는 시퀀스 길이에 대해 필요한 계산량/메모리가 증가

19

## Self-Attention에서는, 시퀀스 길이 n의 제곱에 비례하는 계산량과 메모리가 필요하다.

## [15] Vaswani+. Attention Is All You Need. 2017에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## ■복습 | 왜 시퀀스 길이의 제곱에 비례하는 계산량/메모리가 필요한가?

20

## "Understanding Attention Mechanism in Transformer Neural Networks" [16]에서 발췌

## 각 토큰이 다른 모든 토큰과의 연관성을 계산하기 때문에,

## 모든 토큰의 조합에 대해 계산을 수행하고, 그 값을 기억할 필요가 있다.

[16] Jaiyam Sharma, Understanding Attention Mechanism in Transformer Neural Networks, LearnOpenCV에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## D: 데이터 고갈 문제 | 데이터는 어디까지 늘릴 수 있는가?

21

## 과거 웹 데이터의 증가 추세, 학습 데이터의 증가 추세로부터의 예측

## 양질의 언어 데이터는 2024년경에 고갈될 것으로 예측된다.

[17] Villalobos+. Will we run out of data? An analysis of the limits of scaling datasets in Machine Learning. 2022에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 목차

22

## •

## 각 요소의 스케일에 있어서의 문제점

## •

## 스케일하기 위한 기술: 파라미터 수(N)에 관련하는 노력

## •

## 스케일하기 위한 기술: 계산량(C)에 관련하는 노력

## •

## 스케일하기 위한 기술: 데이터(D)에 관련하는 노력

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 목차

23

## •

## 각 요소의 스케일에 있어서의 문제점

## •

## 스케일하기 위한 기술: 파라미터 수(N)에 관련하는 노력

## •

## 스케일하기 위한 기술: 계산량(C)에 관련하는 노력

## •

## 스케일하기 위한 기술: 데이터(D)에 관련하는 노력

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 파라미터(N)에 관련하는 노력의 전체상

24

## 모델이 스케일됨에

## 따라

## 비용이 증가한다

## Self-Attention 자체의

## 계산/메모리 효율을 개선한다

## 과제

## 방향성

## 해결책

## Efficient Attention

## 계산 비용을 팽창시키지 않고

## 모델의 파라미터를 늘린다

## 혼합 전문가(Mixture of Experts)

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 파라미터(N)에 관련하는 노력의 전체상

25

## 모델이 스케일됨에

## 따라

## 비용이 증가한다

## 과제

## 방향성

## 해결책

## Self-Attention 자체의

## 계산/메모리 효율을 개선한다

## Efficient Attention

## 계산 비용을 팽창시키지 않고

## 모델의 파라미터를 늘린다

## 혼합 전문가(Mixture of Experts)

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## Sparse Transformer: Sparse(희소)한 Attention의 제안

26

## ・Attention을 계산하는 위치를 한정(계산하지 않는 위치는 마스크)함으로써 계산량을 삭감

## ・매우 긴 시퀀스 길이의 입력(예: 이미지나 음성)에 대해서도 효율적으로 트랜스포머를 이용 가능하게 한다.

## [19] Child+. Generating Long Sequences with Sparse Transformers. 2019에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## Sparse Transformer: Sparse(희소)한 Attention의 제안

27

## 어텐션 기구를

## 2회 통과시키면

## 모든 토큰에

## 어텐션이 도달한다.

## [19] Child+. Generating Long Sequences with Sparse Transformers. 2019에서 인용

## [64] sunbluesome. Sparse Transformer를 이해하고 싶다에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## Big Bird: Sparse(희소)한 Attention의 제안

28

## 방법

## 다수의 Sparse한

## Attention을

## 조합하여,

## Attention을 근사하고,

## 긴 시퀀스에 대응한다

## 결과

## 긴 시퀀스를 다루는 질의응답

## 및 요약 등의 태스크

## 에서 좋은 성능을 획득

## 유사 아이디어: "Longformer: The Long-Document Transformer", 2020

## [20] Zahher+. Big Bird: Transformers for Longer Sequences. 2020에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## FlashAttention: 메모리 액세스를 고려하여 고속화를 실현

29

## Attention의 계산은, 연산이 아니라 메모리 I/O에 병목이 있다는 점을 지적

## 입력 행렬을 잘게 분할하여 계산함으로써, 시퀀스 길이 × 시퀀스 길이의 Attention 행렬

## 전체의 메모리 읽기/쓰기를 회피한다. GPU SRAM에서 가능한 한 처리를 완결시키도록

## (저속인 GPU HBM 메모리로의 액세스 횟수를 삭감) 하여, 대폭적인 고속화(예: GPT-2에서

## 최대 7.6배)에 성공

## 구현의 최적화

## (fused kernel)

## 에 의한 대폭적인 속도

## 향상

[21] Dao+. FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness. 2022에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## FlashAttention2: FlashAttention을 더욱 고속화

30

## "FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning" [22]

## 방법: 구현 상의 3가지 공법을 쌓음으로써 고속화

## •

## 알고리즘을 공략함으로써 행렬 연산 이외의 연산을 될 수 있는 한 삭감한다

## (GPU는 행렬 연산에 전용 연산 유닛이 있기 때문에 고속히 처리할 수 있다)

## •

## 배치나 Attention의 헤드뿐만 아니라 시퀀스 방향으로도 병렬 연산을 실시함으로써 배치나

## 헤드 수가 적은 경우에도 고속화할 수 있도록 한다

## •

## 워프(동시에 실행되는 스레드 그룹을 가리키는 GPU 용어)를 query 행렬에서

## 분할함으로써, 워프 간 동기 및 통신을 삭감하고, 병렬성을 향상

## FlashAttention의 약 2배 고속화(PyTorch의 표준 Attention의 최대 9배 고속화)

[22] Tri Dao. FlashAttention-2: Faster Attention with Better

Parallelism and Work Partitioning. 2023에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 파라미터(N)에 관련하는 노력: 혼합 전문가(Mixture of Experts)

31

## 모델이 스케일됨에

## 따라

## 비용이 증가한다

## 과제

## 방향성

## 해결책

## Self-Attention 자체의

## 계산/메모리 효율을 개선한다

## Efficient Attention

## 계산 비용을 팽창시키지 않고

## 모델의 파라미터를 늘린다

## 혼합 전문가(Mixture of Experts)

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 계산 비용을 팽창시키지 않고 모델의 파라미터를 늘린다?

32

## 준비하는

## 파라미터 수

## 필요한 계산량

## 준비하는

## 파라미터 수

## 필요한 계산량

## 준비하는

## 파라미터 수

## 필요한 계산량

## 통상

## 하고 싶은 일

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 혼합 전문가(MoE)

33

## 다수의 전문가(신경망)를 준비해 두고, 입력 값에

## 따라, 일부 전문가에만 포워드한다. → 모든 파라미터를

## 사용하는 것은 아니므로, 계산량을 억제할 수 있다.

## 전문가 A

## (라는 신경망)

## 전문가 B

## (라는 신경망)

## 전문가 C

## (라는 신경망)

## 입력

## 출력

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 혼합 전문가(MoE)

34

## 다수의 전문가(신경망)를 준비해 두고, 입력 값에

## 따라, 일부 전문가에만 포워드한다. → 모든 파라미터를

## 사용하는 것은 아니므로, 계산량을 억제할 수 있다.

## 전문가 A

## (라는 신경망)

## 전문가 B

## (라는 신경망)

## 전문가 C

## (라는 신경망)

## 입력

## 출력

## *엄밀히 말하면, 어느 전문가에게 할당할지를

## 결정하기 위한 작은 신경망(라우터 신경망)이

## 추가로 필요하므로, 그 만큼

## 약간의 계산량은 증가한다.

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 혼합 전문가(MoE)

35

## ■

## 계산량을 억제하면서, 퍼포먼스를 개선할 수 있음이 실험으로 확인되었다.

## →동일한 계산량으로 학습한다는 제약 하에서, MoE를 사용한 모델이 사용하지 않은 모델

## (통상의 모델)보다 퍼포먼스가 높다.

## ■

## 유출 정보에 따르면, GPT-4는 MoE 모델 구조를 채택하고 있다고 한다.

## ■

## 최근 다수의 오픈 모델(DeepSeek, Qwen 등)도 MoE 모델을 채택

## 라우터 신경망이

## 데이터의 클러스터 중심점을

## 기준으로 각 전문가에 대해

## 사례를 할당하고,

## 각 전문가는 그

## 클러스터 내에서의 분류에 특화하는

## 학습이 수행되었다

## 복잡한 분류 문제에 MoE를 적용한 경우의 각 사례에 대한 라우터 신경망에 의한

## 전문가 할당의 시각화

## (t-SNE로 데이터셋의 사례를 2차원으로 시각화. 색은 전문가 할당을 나타낸다)

## [23] Chen+. Towards Understanding Mixture of Experts in Deep Learning. 2022에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## Switch Transformer: 1조 6000억 파라미터의 MoE 모델

36

## 방법

## T5 모델의 피드포워드 층에

## MoE를 적용하여, 대규모화

## 다수의 MoE에서는 각 토큰마다

## 복수의 전문가가 사용되지만

## 이를 하나의 전문가만을

## 사용하도록 함으로써, 통신·

## 계산 비용의 삭감을 실현

## 결과

## 1.6조 파라미터 모델의 학습에서

## T5-XXL 모델에 대해 4배의

## 사전학습 스피드업

## [25] Fedus+. Switch Transformers: Scaling to Trillion Parameter Models with

Simple and Efficient Sparsity. 2021에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## DeepSpeed-MoE: MoE 모델의 학습 효율 개선

37

## DeepSpeed MoE라는 최적화된 구

## 현에 의해, 자기회귀 모델에서의

## 품질이 동등한 Dense 모델과 비교하여

## 5배 정도 학습 비용을 삭감한 MoE의

## 학습을 실현

[26] Rajbhandari+. DeepSpeed-MoE: Advancing Mixture-of-Experts Inference and Training to Power Next-Generation AI Scale. 2022에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## PR-MoE: MoE 모델의 성능을 유지한 모델 크기 삭감

38

## 방법

## PR-MoE라는 아키텍처를 제안

## •

## 각 토큰이 1개의 고정된 MLP와

## 1개의 전문가의 양쪽을 이용

## •

## 트랜스포머의 후반 층에서

## 보다 많은 전문가를 활용

## 결과

## 표준적인 MoE보다 적은 파라미터 수로

## 동등한 성능을 달성

## •

## 350M: 1/3 이하의 파라미터로 동등 성능

## •

## 1.3B: Standard-MoE의 약 60% 파라미터로

## 동등 성능

[26] Rajbhandari+. DeepSpeed-MoE: Advancing Mixture-of-Experts Inference and Training to Power Next-Generation AI Scale. 2022에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## ■MoE를 포함하는 언어 모델에 있어서의 스케일 법칙

39

## (왼쪽 그림) 전문가 수를 늘리면 로그 손실이 내려가지만, 특히 큰 모델 크기에서는

## 너무 많이 늘리면 효과가 약해진다 (회색 선이 선형으로 피팅시킨 것)

## (오른쪽 그림) MoE 모델의 파라미터 수를 여러 요소를 가미하여 통상 모델의 파라미터 수로

## 환산하면, 스케일 법칙이 성립

## 아래 선일수록

## 손실이 작다 =

## 모델 크기가

## 크다

[27] Clark+. Unified Scaling Laws for Routed Language Models. 2022에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 통상 모델을 MoE화했을 때

## 효과가 있는 최대 파라미터 수

## ■MoE를 포함하는 언어 모델에 있어서의 스케일 법칙

40

## 통상 모델의 파라미터 수가 커지면

## MoE화의 효과는 비례하여 낮아진다

## ↓

## 모델 크기에 적합한 전문가 수를 선택하는 것이 좋다

## 통상 모델의 파라미터 수

[27] Clark+. Unified Scaling Laws for Routed Language Models. 2022에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 목차

41

## •

## 각 요소의 스케일에 있어서의 문제점

## •

## 스케일하기 위한 기술: 파라미터 수(N)에 관련하는 노력

## •

## 스케일하기 위한 기술: 계산량(C)에 관련하는 노력

## •

## 스케일하기 위한 기술: 데이터(D)에 관련하는 노력

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 목차

42

## •

## 각 요소의 스케일에 있어서의 문제점

## •

## 스케일하기 위한 기술: 파라미터 수(N)에 관련하는 노력

## •

## 스케일하기 위한 기술: 계산량(C)에 관련하는 노력

## •

## 스케일하기 위한 기술: 데이터(D)에 관련하는 노력

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 계산량(C)에 관련하는 노력의 전체상

43

## 충분한 계산량/

## 메모리 용량을 확보하고

## 효율적으로

## 훈련할 필요

## (주로 추론 시) 모델의 경량화를

## 통해, 소규모 GPU 환경에서의

## 운용을 가능하게 한다

## 훈련에 있어 복수의 GPU를

## 효율적으로 활용한다

## 과제

## 방향성

## 해결책

## 양자화

## 병렬 계산

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 계산량(C)에 관련하는 노력: 병렬 계산

44

## 충분한 계산량/

## 메모리 용량을 확보하고

## 효율적으로

## 훈련할 필요

## 과제

## 방향성

## 해결책

## (주로 추론 시) 모델의 경량화를

## 통해, 소규모 GPU 환경에서의

## 운용을 가능하게 한다

## 훈련에 있어 복수의 GPU를

## 효율적으로 활용한다

## 양자화

## 병렬 계산

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 딥러닝에 있어서의 병렬화

45

## "DeepSpeed: 딥러닝의 훈련과 추론을 획기적으로 고속화하는 프레임워크" [32]에서 발췌,

## [32] Microsoft DeepSpeed Team, DeepSpeed: Extreme-scale model training for everyone, Microsoft에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## ZeRO: 데이터 병렬 시의 메모리 효율화

46

## "DeepSpeed: 딥러닝의 훈련과 추론을 획기적으로 고속화하는 프레임워크" [32]에서 발췌,

[32] Microsoft DeepSpeed Team, DeepSpeed: Extreme-scale model training for everyone, Microsoft에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## ZeRO: 데이터 병렬 시의 메모리 효율화

47

## Stage 1

## Stage 2

## Stage 3

## • 어느 요소를 메모리에서 병렬화하는가에 따라, 3단계의 동작 모드가 존재

## • 단계가 진행될수록 메모리를 삭감할 수 있지만, 통신 오버헤드가 증가한다

[33] Rajbhandari+. ZeRO: Memory Optimizations Toward Training Trillion Parameter Models. 2019에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 3D 병렬화

48

## "DeepSpeed: 딥러닝의 훈련과 추론을 획기적으로 고속화하는 프레임워크" [32]에서 발췌,

## • 병렬화 전략마다 통신 오버헤드가 다르다

## 텐서 병렬 >> 파이프라인 병렬

## • 3D 병렬화: GPU·노드의 배치에 따라 통신 비용을 억제하며 병렬화

## 파이프라인 병렬

## 데이터 병렬 + ZeRO

## 4개의 GPU를 가진 8노드로

## 3D parallelism을 구성한 예

## 같은 색의 GPU는 동일 노드에 배치되어

## 있음을 나타낸다

## •

## 고 오버헤드의 텐서 병렬을

## 노드 내에 배치

## •

## 저 오버헤드의 파이프라인 병렬을

## 노드를 가로질러 배치

## •

## 데이터 병렬과 ZeRO stage 1의 조합에

## 의해, GPU 메모리 효율을 높인다

[32] Microsoft DeepSpeed Team, DeepSpeed: Extreme-scale model training for everyone, Microsoft에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## ■보충 | ZeRO는 환경 설정을 기술하는 것만으로 이용 가능

49

## *대표적인 라이브러리: deepspeed

## [34] Microsoft, https://github.com/microsoft/DeepSpeed에서 인용

## [35] DeepSpeed, https://www.deepspeed.ai/docs/config-json/에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 전문가 병렬화

50

## "NVIDIA NeMo Framework User Guide - Parallelisms" [55]에서 발췌,

## • MoE 모델 전용의 병렬화 기법

## • MoE의 각 전문가를 다른 GPU에 배치한다

## • 행렬을 분할하여 복수의 GPU가 보유하는 텐서 병렬과 유사하다

## • 모든 층에 적용되는 텐서 병렬화와 달리, 전문가 병렬화는

## 전문가 층에만 적용된다

## [55] NVIDIA NeMo Framework User Guide - Parallelisms, NVIDIA에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 계산량(C)에 관련하는 노력: 양자화

51

## 충분한 계산량/

## 메모리 용량을 확보하고

## 효율적으로

## 훈련할 필요

## 과제

## 방향성

## 해결책

## (주로 추론 시) 모델의 경량화를

## 통해, 소규모 GPU 환경에서의

## 운용을 가능하게 한다

## 훈련에 있어 복수의 GPU를

## 효율적으로 활용한다

## 양자화

## 병렬 계산

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 양자화란

52

## •

## 모델 파라미터의 데이터 타입을

## 부동소수점(Float 형)에서 정수(Int 형)로 변환하여 연산 처리를 수행한다

## •

## 추론 시에, 필요 메모리량을 삭감할 수 있다.

## •

## 단순히 이를 수행하면 성능 저하가 발생한다.

[63] Younes Belkada, Tim Dettmers, A Gentle Introduction to 8-bit Matrix Multiplication for transformers at scale using Hugging Face Transformers, Accelerate and bitsandbytes,

Hugging Face, https://huggingface.co/blog/hf-bitsandbytes-integration#a-gentle-summary-of-llmint8-zero-degradation-matrix-multiplication-for-large-language-models에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## LLM.int8(): 성능 저하 없이 가능한 양자화 방법

53

## 방법

## 16비트 행렬 곱셈에서 이상치의 특징을

## 분리하는 혼합 정밀도 분해를 수행하여,

## 대부분의 값을 8비트로,

## 이상치만을 16비트로 표현한다

## 결과

## 16비트와 비교하여 약 50%의 메모리

## 삭감이 가능한 경우를 나타낸다

## 175B까지의 파라미터를 가지는 LLM에

## 있어서, 성능 저하 없이 추론을 수행

## 할 수 있음을 경험적으로 보인다

[37] Dettmers+. LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale. 2022에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## LLM.int8(): 성능 저하 없이 가능한 양자화 방법

54

## Step1. 입력된 은닉 상태로부터,

## 열 단위로 이상치(임계값보다 큰 값)

## 을 추출한다.

## Step2. 이상치 행렬에 대해서는,

## FP16인 채로 행렬 연산. 이상치가 아닌

## 행렬에 대해서는, INT8로 변환하여

## (양자화하여) 행렬 연산.

## Step3. 2개의 출력 값이 존재한다.

## INT8의 출력 값은 FP16으로 되돌려, 2개의

## 출력 값을 가산하여, FP16으로 출력

## 값을 반환한다.

[63] Younes Belkada, Tim Dettmers, A Gentle Introduction to 8-bit Matrix Multiplication for transformers at scale using Hugging Face Transformers, Accelerate and

bitsandbytes, Hugging Face에서 인용

[37] Dettmers+. LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale. 2022에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## k-bit 스케일 법칙

55

## •

## 모델의 메모리 용량(비트 수)을

## 고정했을 때, 모델의 크기와

## 양자화를 어떻게 설정해야 하는가

## 예: 30B의 8-bit 모델과 60B의

## 4-bit 모델은 동일한 메모리 용량이

## 된다

## •

## 메모리 용량을 고정한 경우,

## 4bit 양자화가 가장 제로샷이

## 높았다

## •

## 3bit에 있어서는 모델 크기가

## 커지면 성능이 불안정하게

## →post-hoc 양자화에서는 4-bit가

## 최소 필요?

[56] Dettmers+. The case for 4-bit precision: k-bit Inference Scaling Laws. 2023에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 양자화에 의해 Emergent Ability는 상실되지 않는가

56

## ・Emergent Ability는 LLM의 중요한 특성

## ・in-context learning, chain-of-thought reasoning, instruction-following의 능력을 계측

## ・결과로서 4비트까지의 양자화 모델에서는 Emergent Ability의 유지를 확인

[38] Liu+. Do Emergent Abilities Exist in Quantized Large Language Models: An Empirical Study. 2023에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 훈련 시부터 1bit/1.58bit 양자화를 수행한다: BitNet

57

## •

## 양자화를 적용한 모델을 사전학습하여 구축

## •

## 왼쪽 그림: Attention·MLP에 포함되는 선형 층을 모두 1bit용으로 확장된 선형 층(BitLinear)로 치환하여

## 구축

## •

## 오른쪽 그림: 모델의 비트 수(메모리 용량)로 비교하여 기존 LLM의 성능을 크게

## 능가했음을 보고

## BitNet: 파라미터를 2치({-1, +1}; 1bit)／3치({-1, 0, 1}; 1.58bit)로 나타낸다

[57] Wang+. BitNet: Scaling 1-bit Transformers for Large Language Models. 2023에서 인용

[58] Ma+. BitNet b1.58 2B4T Technical Report. 2025에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 목차

58

## •

## 각 요소의 스케일에 있어서의 문제점

## •

## 스케일하기 위한 기술: 파라미터 수(N)에 관련하는 노력

## •

## 스케일하기 위한 기술: 계산량(C)에 관련하는 노력

## •

## 스케일하기 위한 기술: 데이터(D)에 관련하는 노력

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 목차

59

## •

## 각 요소의 스케일에 있어서의 문제점

## •

## 스케일하기 위한 기술: 파라미터 수(N)에 관련하는 노력

## •

## 스케일하기 위한 기술: 계산량(C)에 관련하는 노력

## •

## 스케일하기 위한 기술: 데이터(D)에 관련하는 노력

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 데이터셋(D)에 관련하는 노력의 전체상

60

## 성능을 발휘하기 위한

## 학습용

## 데이터를 준비할

## 필요

## 과제

## 방향성

## 해결책

## 데이터셋의 품질을

## 개선한다

## 성능을 발휘하기 위한

## 데이터셋을 탐색한다

## 데이터 전처리

## 데이터셋 정비

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 데이터셋(D)에 관련하는 노력: 데이터셋 정비

61

## 성능을 발휘하기 위한

## 학습용

## 데이터를 준비할

## 필요

## 과제

## 방향성

## 해결책

## 데이터셋의 품질을

## 개선한다

## 성능을 발휘하기 위한

## 데이터셋을 탐색한다

## 데이터 전처리

## 데이터셋 정비

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 어떤 학습 데이터로 학습해야 하는가

62

## ■주요 모델의 학습 데이터의 구성

## • 최근 모델은 많은 케이스에서 Code 학습을 수행하고 있다. GPT-3는 없음.

## • Code로 학습한 모델(예: code-davinci-002)은 GPT-3보다 추론 성능이 좋다

## • ChatGPT도 code-davinci-002를 베이스로 학습되어 있다고 간주된다.

## [2] Zhao+. A Survey of Large Language Models. 2023에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 특정 도메인 데이터에 의한 지속적인 사전학습

63

## 사전학습 후에 특정 도메인의 문서(예: arXiv의 논문 요지)를 지속적으로 학습시킨다.

## 지속 학습한 모델의 다운스트림 태스크에서의 성능을 평가

## 사전학습 후에 지속 학습함으로써, 치명적 망각이 일어나기 어려운 데다가,

## 다운스트림 태스크에서의 뛰어난 성능을 발휘할 수 있음을 보인다

[41] Cossu+. Continual Pre-Training Mitigates Forgetting in Language and Vision. 2022에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## Chinchilla: 최적 계산 할당에 기반하여 N과 D를 정한 모델

64

## • LLM의 사전 훈련 예산은 계산량(GPU 수나 시간)에 비례.

## • 계산량을 파라미터 수와 학습 데이터량에 어떻게 할당하는지가

## 중요해진다.

## • OpenAI에 의한 종래의 스케일 법칙[3]은 파라미터에 대해 필요로 하는

## 학습 데이터량의 견적이 너무 적다는 점을 지적.

[42] Hoffmann+. Training Compute-Optimal Large Language Models. 2022에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## Chinchilla: 최적 계산 할당에 기반하여 N과 D를 정한 모델

65

## 데이터 크기 D

## 토큰을 1.4T까지 증가

## (같은 데이터의 다른 서브셋)

## ※ Gopher의 약 4.6배

## 모델 크기 N

## 70B로 설정

## ※ Gopher의 약 1/4배

## 결과

## 다수의 케이스에서 Gopher에 승리

## (제안한 관계식의 타당성을 시사)

[42] Hoffmann+. Training Compute-Optimal Large Language Models. 2022에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 실용적인 작은 모델에서는, Chinchilla 법칙보다 많은 데이터가 필요?

66

## • Chinchilla Trap:

## Chinchilla의 모델 크기(70B)는

## 크기 때문에, 추론 비용이 높다*.

## 추론 비용도 고려하여 더

## 작은 모델을 대규모 데이터로

## 훈련해야 한다는 의견

## • Chinchilla 최적인 모델 크기의

## 40-60% 이내의 모델 크기로,

## 10-42%의 계산량 추가로 동성능의

## 모델을 학습할 수 있다

## Chinchilla 최적인 모델과

## 같은 성능을 달성하기 위해

## 필요한 파라미터 비율(횡축)과

## 계산량(종축)의 관계

## 최적 모델 크기

[43] Harm de Vries, Go smol or go home, Why we should train smaller LLMs on

more tokens, 2023에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 언어 데이터 고갈의 문제

67

## "Will we run out of data? An analysis of the limits of scaling datasets in Machine

## Learning" [17]

## 과거 웹 데이터의 증가 추세, 학습 데이터의 증가 추세로부터의 예측

## 양질의 언어 데이터의 고갈이 예측되고 있다.

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 사전학습을 통해 지식은 어떻게 학습되어 가는가

68

## "How Do Large Language Models Acquire Factual Knowledge During Pretraining?" [60]

## 훈련 스텝 수

## 정답 스팬의

## 로그 확률의 변화

## 검은 점선 부분에서 지식을 서술한 문장으로 훈련

## Memorization: 주입한 문장을 그대로 질문으로 이용

## Semantic: 주입한 문장을 바꾸어 말한 질문을 이용

## Composition: 복수의 문장의 지식이 필요한 질문을 이용

## •

## LLM의 사전 훈련 시에 지식이 어떻게 획득되어 가는지를 조사

## •

## 지식을 서술한 문장이 출현하는(점선) 때마다 올바른 지식이 생성되는 확률이 높아지고,

## 지식이 점차 학습되어 간다

## •

## 지식이 출현하지 않는 스텝(900스텝 이후)에서는, 망각되어 간다

## LLM에게 지식을 가르치기 위해서는, 훈련 데이터 중에

## 반복해서 지식이 출현할 필요가 있다

## ↓

## 중요한 지식이 높은 밀도로 포함되는 고품질 훈련 데이터의 중요성을 시사

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 합성 데이터에 의한 사전학습

69

## 방법

## 합성 데이터를 사용한 사전학습의 효과를 1,000개 이상의

## LLM을 10만 GPU 시간을 사용하여 훈련해 검증

## 합성 데이터의 종류:

## •

## 웹 바꾸어말하기: LLM을 사용한 웹 데이터의

## 바꾸어말하기에 의한 합성 데이터 생성

## - HQ: 깨끗한 텍스트로 바꾸어말하기

## - QA: QA로 바꾸어말하기

## •

## TXBK: 합성 교과서: LLM을 사용하여

## 교과서 스타일의 데이터를 0부터 작성

## 결과

## •

## 웹 데이터와 합성 데이터를 섞은 경우에

## 훈련의 효율이 대폭 개선

## •

## 합성 데이터만으로 훈련하면 성능 악화

## →특히 합성 교과서만으로는 현저히 악화

## •

## 모든 종류에서, 웹 데이터에 33% 비율로

## 합성 데이터를 섞은 경우에 최선의 성능을 달성

[59] Kang+. Demystifying Synthetic Data in LLM Pre-training: A Systematic

Study of Scaling Laws, Benefits, and Pitfalls. 2025에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 데이터가 유한하고 계산량이 무한한 설정에서의 학습

70

## •

## LLM의 사전 훈련에 투입되는 계산량은 해마다 늘어나고 있으나,

## 데이터는 한정되어 있다

## •

## 데이터량이 유한하다는 것을 전제로, 계산량을 스케일하는 경우, 성능을 개선할 수 있는가?

## •

## LLM의 표준적인 훈련 설정에서는 스케일할 수 없다(왼쪽 틀)

## 에포크 수를 늘린다 → 오버피팅하여 성능 저하(왼쪽 틀의 왼쪽 그림)

## 모델의 크기를 늘린다 → 충분히 훈련하지 못해 성능 저하(왼쪽 틀의 오른쪽 그림)

## •

## 훈련 설정을 적절히 조정하면 스케일할 수 있다(오른쪽 틀)

## 표준적인 훈련 설정에서의 학습에서는 고정된 데이터량으로 계산량만 늘려도 스케일하지 않는다

## 훈련 설정을 적절히 설정하면 스케일할 수 있다

## 큰 모델일수록

## •

## 작은 학습률

## •

## 적은 에포크 수

## •

## 큰 weight decay

## (강한 정규화)

[61] Kim+. Pre-training under infinite compute. 2025에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 데이터셋(D)에 관련하는 노력의 전체상

71

## 성능을 발휘하기 위한

## 학습용

## 데이터를 준비할

## 필요

## 과제

## 방향성

## 해결책

## 소량의 고품질

## 데이터셋을 준비한다

## 성능을 발휘하기 위한

## 데이터셋을 탐색한다

## 데이터 가지치기 등

## 데이터셋 정비

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## RefinedWeb: 데이터의 전처리(필터링)의 공법

72

## 웹 데이터만으로 5T Token의 데이터셋. 600G가 Public.

## 필터링의 공법(후술) 등에 의해 종래보다 대규모 데이터를 구축.

[39] Penedo+. The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Data, and Web Data Only. 2023에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## Macrodata Refinement: 데이터의 엄밀한 좁혀내기 파이프라인

73

## ・복수의 필터링, 중복 제거를 조합한 엄밀한 데이터의 좁혀내기를 실시

## ・일련의 파이프라인에서 CommonCrawl 중의 약 90%의 문서가 제거된다

[39] Penedo+. The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Data, and Web Data Only. 2023에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## Macrodata Refinement: 데이터의 엄밀한 좁혀내기 파이프라인

74

## ●URL filtering: 유해한 URL로부터 취득한 텍스트를 배제

## ●Text extraction: 텍스트의 메인 콘텐츠 텍스트만 추출(헤더

## 나 광고 부분은 불필요)

## ●Language identification: 특정 언어 텍스트만 남긴다

## ●Repetition removal: 텍스트 내의 반복문을 배제

## ●Document-wise filtering: 스팸 텍스트를 필터링

## ●Line-wise corrections: 텍스트 내의 행 레벨 필터(예: SNS의

## 「좋아요」)

## ●Fuzzy deduplication: 다른 문서에 유사 문장이 존재한 경우는 배제

## (MinHash [40])

## ●Exact deduplication: 다른 문서에 지정한 토큰 수 이상의 완전

## 일치가 존재한 경우는 배제

[39] Penedo+. The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Data, and Web Data Only. 2023에서 인용

[40] Daisuke Okanohara, MinHash에 의한 고속 유사 검색, Preferred Networks Research&Development, 2011에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## FineWeb-Edu: LLM이 평가한 교육적 가치를 사용한 전처리

75

## FineWeb-Edu: LLM이 평가한 텍스트의 교

## 육적 가치를 사용하여 전처리를 수행

## 방법

## 대규모 텍스트에 LLM의 추론을 적용하는 것은

## 비용이 높기 때문에, 경량화가 필요.

## →LLM의 평가 결과를 사용해 경량 분류기를 훈련

## •

## 46만 건의 웹 기사의 「교육적 가치」를

## LLM에 평가시켜 훈련 데이터를 작성

## •

## 작은 모델을 학습하여 평가기를 작성

## 결과

## •

## 전처리를 수행하기 전의 데이터(FineWeb)나 기

## 존 데이터(Matrix)와 비교해, 지식이나

## 추론이 필요한 태스크의 성능이 크게 개선

[62] Penedo+. The FineWeb Datasets: Decanting the Web for the Finest Text

Data at Scale. 2024에서 인용

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## 오늘의 정리

76

## 모델의 스케일을 뒷받침하는 기술 동향에 대해 소개했습니다.

## 1. 왜 모델을 스케일시키는가

## 1) 스케일 법칙의 성립, 2) Emergent Ability

## 3. 모델을 스케일하는 데 있어 문제는 여전히 존재

## •

## 스케일에 수반하여 필요로 하는 비용의 증가, 데이터의 부족, 등등

## 2. 스케일 법칙은 모델의 성능과 {파라미터 수, 데이터량, 계산량}의 관계를 밝혔다

## •

## 스케일 법칙으로 성능 예측이 가능해지며, 대규모 모델에 대한 투자 리스크가 경감.

## 4. 모델의 스케일을 뒷받침하는 다양한 연구·개발이 수행되고 있다

## •

## 파라미터 수(P): 보다 메모리 효율, 연산 효율이 뛰어난 모델의 제안

## •

## 계산량(C): 효율적인 학습, 추론 방법의 정비

## •

## 데이터셋 크기(D): 데이터의 양과 질의 공법

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## References

77

[1] Bao Hua Choo, The emergence of Large Language Models (LLMs), The low down, https://thelowdown.momentum.asia/the-emergence-of-large-language-

models-llms/, 접속일: 2023/11/16

[2] Zhao+. A Survey of Large Language Models. 2023. In arXiv:2303.18223

[3] Kaplan+. Scaling Laws for Neural Language Models. 2020. In arXiv:2001.08361

[4] Wei+. Emergent Abilities of Large Language Models. 2022. In arXiv:2206.07682

[5] Schaeffer+. Are Emergent Abilities of Large Language Models a Mirage?. 2023. In arXiv:2304.15004

[6] Power+. Grokking: Generalization Beyond Overfitting on Small Algorithmic Datasets. 2022. In arXiv:2201.02177

[7] Liu+. Towards Understanding Grokking: An Effective Theory of Representation Learning. 2022. In NeurIPS2022

[8] Hestness+. Deep Learning Scaling is Predictable, Empirically. 2017. In arXiv:1712.00409

[9] Brown+. Language Models are Few-Shot Learners. 2020. In NeurIPS2020

[10] Anil+. PaLM 2 Technical Report. 2023. In arXiv:2305.10403

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## References

78

[11] Henighan+. Scaling Laws for Autoregressive Generative Modeling. 2020. In arXiv:2010.14701

[12] Ganguli+. Predictability and Surprise in Large Generative Models. 2023. In arXiv:2202.07785

[13] OpenAI. GPT-4 Technical Report. 2023. In arXiv:2303.08774

[14] Abhinav Venigalla, Linden Li, Billion-Parameter GPT Training Made Easy, MosaicML, https://www.mosaicml.com/blog/billion-parameter-gpt-

training-made-easy, 접속일: 2023/11/16

[15] Vaswani+. Attention Is All You Need. 2017. In NeurIPS2017

[16] Jaiyam Sharma, Understanding Attention Mechanism in Transformer Neural Networks, LearnOpenCV, https://learnopencv.com/attention-

mechanism-in-transformer-neural-networks/, 접속일: 2023/11/16

[17] Villalobos+. Will we run out of data? An analysis of the limits of scaling datasets in Machine Learning. 2022. In arXiv:2211.04325

[18] Tay+. Efficient Transformers: A Survey. 2020. In arXiv:2009.06732

[19] Child+. Generating Long Sequences with Sparse Transformers. 2019. In arXiv:1904.10509

[20] Zahher+. Big Bird: Transformers for Longer Sequences. 2020. In NeurIPS2020

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## References

79

[21] Dao+. FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness. 2022. In NeurIPS2022

[22] Tri Dao. FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning. 2023. In arXiv:2307.08691

[23] Chen+. Towards Understanding Mixture of Experts in Deep Learning. 2022. In NeurIPS2022

[24] Shazeer+. Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer. 2017. In ICLR

[25] Fedus+. Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity. 2021. In arXiv:2101.03961

[26] Rajbhandari+. DeepSpeed-MoE: Advancing Mixture-of-Experts Inference and Training to Power Next-Generation AI Scale. 2022. In ICML2022

Proceedings of the 39th International Conference on Machine Learning, PMLR 162:18332-18346

[27] Clark+. Unified Scaling Laws for Routed Language Models. 2022. In arXiv:2202.01169

[28] Zhai+. An Attention Free Transformer. 2021. In arXiv:2105.14103

[29] Peng+. RWKV: Reinventing RNNs for the Transformer Era. 2023. In arXiv:2305.13048

[30] Sun+. Retentive Network: A Successor to Transformer for Large Language Models. 2023. In arXiv:2307.08621

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## References

80

[31] Gu+. Efficiently Modeling Long Sequences with Structured State Spaces. 2022. In ICLR2022

[32] Microsoft DeepSpeed Team, DeepSpeed: Extreme-scale model training for everyone, Microsoft, https://www.microsoft.com/en-

us/research/blog/deepspeed-extreme-scale-model-training-for-everyone/, 접속일: 2025/10/05

[33] Rajbhandari+. ZeRO: Memory Optimizations Toward Training Trillion Parameter Models. 2019. In arXiv:1910.02054

[34] Microsoft, https://github.com/microsoft/DeepSpeed, 접속일: 2023/11/16

[35] DeepSpeed, https://www.deepspeed.ai/docs/config-json/, 접속일: 2023/11/16

[36] Younes Belkada, Tim Dettmers, A Gentle Introduction to 8-bit Matrix Multiplication for transformers at scale using Hugging Face Transformers,

Accelerate and bitsandbytes, Hugging Face, https://huggingface.co/blog/hf-bitsandbytes-integration#a-gentle-introduction-to-8-bit-matrix-

multiplication-for-transformers-at-scale-using-hugging-face-transformers-accelerate-and-bitsandbytes, 접속일: 2023/11/16

[37] Dettmers+. LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale. 2022. In NeurIPS2022

[38] Liu+. Do Emergent Abilities Exist in Quantized Large Language Models: An Empirical Study. 2023. In arXiv:2307.08072

[39] Penedo+. The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Data, and Web Data Only. 2023. In

arXiv:2306.01116

[40] Daisuke Okanohara, MinHash에 의한 고속 유사 검색, Preferred Networks Research&Development, 2011,

https://tech.preferred.jp/ja/blog/minhash/, 접속일: 2023/11/16

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## References

81

[41] Cossu+. Continual Pre-Training Mitigates Forgetting in Language and Vision. 2022. In arXiv:2005.09357

[42] Hoffmann+. Training Compute-Optimal Large Language Models. 2022. In NeurIPS2022

[43] Harm de Vries, Go smol or go home, Why we should train smaller LLMs on more tokens, 2023, https://www.harmdevries.com/post/model-size-

vs-compute-overhead/, 접속일: 2023/11/16

[44] Sorscher+. Beyond neural scaling laws: beating power law scaling via data pruning. 2022. In NeurIPS2022

[45] Tirumala+. D4: Improving LLM Pretraining via Document De-Duplication and Diversification. 2023. In arXiv:2308.12284

[46] Zhou+. LIMA: Less Is More for Alignment. 2023. In arXiv:2305.11206

[47] Dzmitry Bahdanau, The FLOPs Calculus of Language Model Training, Medium, 2022, https://medium.com/@dzmitrybahdanau/the-flops-

calculus-of-language-model-training-3b19c1f025e4, 접속일: 2023/11/16

[48] Wan+. Efficient Large Language Models: A Survey. 2024. In arXiv:2312.03863

[49] Patro and Agneeswaran. Mamba-360: Survey of State Space Models as Transformer Alternative for Long Sequence Modelling: Methods,

Applications, and Challenges. 2024. In arXiv:2404.16112

[50] De+. Griffin: Mixing Gated Linear Recurrences with Local Attention for Efficient Language Models. 2024. In arXiv:2402.19427

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## References

82

[51] Qu+. A Survey of Mamba. 2024. In arXiv:2408.01129

[52] Feng+. Beyond Model Collapse: Scaling Up with Synthesized Data Requires Reinforcement. 2024. In arXiv:2406.07515

[53] Gerstgrasser+. Is Model Collapse Inevitable? Breaking the Curse of Recursion by Accumulating Real and Synthetic Data. 2024. In

arXiv:2404.01413

[54] Munkhdalai+. Leave No Context Behind: Efficient Infinite Context Transformers with Infini-attention. 2024. In arXiv:2404.07143

[55] NVIDIA NeMo Framework User Guide - Parallelisms, NVIDIA, https://docs.nvidia.com/nemo-framework/user-

guide/latest/nemotoolkit/features/parallelisms.html, 접속일: 2025/10/05

[56] Dettmers+. The case for 4-bit precision: k-bit Inference Scaling Laws. 2023. In arXiv:2212.09720

[57] Wang+. BitNet: Scaling 1-bit Transformers for Large Language Models. 2023. In arXiv:2310.11453

[58] Ma+. BitNet b1.58 2B4T Technical Report. 2025. In arXiv:2504.12285

[59] Kang+. Demystifying Synthetic Data in LLM Pre-training: A Systematic Study of Scaling Laws, Benefits, and Pitfalls. 2025. In arXiv:2510.01631

[60] Chang+. How Do Large Language Models Acquire Factual Knowledge During Pretraining?. 2024. In arXiv:2406.11813

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.

## References

83

[61] Kim+. Pre-training under infinite compute. 2025. In arXiv:2509.14786

[62] Penedo+. The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale. 2024. In arXiv:2406.17557

[63] Younes Belkada, Tim Dettmers, A Gentle Introduction to 8-bit Matrix Multiplication for transformers at scale using Hugging Face Transformers,

Accelerate and bitsandbytes, Hugging Face, https://huggingface.co/blog/hf-bitsandbytes-integration#a-gentle-summary-of-llmint8-zero-

degradation-matrix-multiplication-for-large-language-models, 접속일: 2026/05/25

[64] sunbluesome. Sparse Transformer를 이해하고 싶다, Zenn, https://zenn.dev/sunbluesome/articles/5f6a86dfa1e1be, 접속일: 2023/11/16

## [65] weights & biases, 「LLM을 제로부터 트레이닝하기 위한 베스트 프랙티스」, https://wandb.ai/site/resources/whitepapers/llm-

whitepaper-japan/ 접속일: 2026/05/25

[66]  iwiwi, github, https://gist.github.com/iwiwi/fc174b1f2341c2c0170be87c5b2e1d31, 접속일:2026/05/25

대규모 언어 모델 강좌 강의 자료

LLM

도쿄대학교 마쓰오·이와사와 연구실

LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료© 2025 by 도쿄대학교 마쓰오·이와사와 연구실은 CC BY-NC-ND 4.0에 따라 라이선스됩니다.
