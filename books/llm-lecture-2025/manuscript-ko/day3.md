# Day 3

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

## 주의사항: 본 자료의 재이용(2차 이용)에 대하여

## ●

## 본 자료에 대하여

## ○

## 도쿄대학교 마츠오·이와사와 연구실이 작성한 자료로, 2025년 10월부터 11월에 걸쳐 개최된 LLM 대규모 언어 모델 강좌 기초편의 강의 자료입니다.

## ○

## 크리에이티브 커먼즈 CC BY-NC-SA 4.0 DEED(저작자표시-비영리-동일조건변경허락 4.0 국제) 라이선스로 등록되어 있습니다.

## ●

## 라이선스 표기에 대하여

## ○

각 슬라이드 페이지 최하단에 라이선스가 명시되어 있습니다. 재이용 시 반드시 본 라이선스 표기를 기재해 주세요.

복제가 곤란한 경우, 아래 텍스트 상자를 활용하여 하이퍼링크를 포함해 라이선스를 표기해 주시기 바랍니다.

## ○

재이용하는 페이지에 참조 논문 등의 인용이 있는 경우, 권망의 Reference에서 해당 인용처를 게재해 주세요.

## ●

## 비영리 목적 이용에 대하여

재이용(2차 이용)이 허락되어 있습니다.

## ●

## 영리 목적 재이용에 대하여

별도 문의해 주시기 바랍니다.

## ●

## 기타

## ○

원래의 표현이 변경되지 않는 범위(글꼴, 크기 등)라면 개작이 가능합니다.

## ○

그 외 개작 및 기타 라이선스에 관한 자세한 내용은 다음 링크를 참고하여 적절히 취급해 주시기 바랍니다.

## 도쿄대학교 마츠오·이와사와 연구실

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

## 3. Pre-training

## 우치야마 후미야(内山史也)

## 대규모 언어 모델 강좌 2025

허가 없는 촬영 및 제3자에 대한 공개를 금지합니다.

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

3

## Pre-training(Day3)

## ● 목적:

## ○ LLM(대규모 언어 모델)의 주류 모델 구조인 Transformer와 그 사전학습 메커니즘을 이해한다.

## ● 목표:

## ○ 언어 모델에서 Transformer의 위치를 설명할 수 있다.

## ○ LLM에서 주류가 된 Transformer의 모델 구조를 설명할 수 있다.

## ○ LLM의 사전학습 파이프라인을 설명할 수 있다.

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

4

## 전체 흐름

## ● 강의:

## ○ 언어 모델이란 무엇인가?

## ○ Transformer

## ○ 사전학습

## ○ 발전 주제

## ● 실습:

## ○ PyTorch를 활용하여 Transformer를 구현하고 학습

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

5

## 목차

## • 언어 모델이란 무엇인가?

## • Transformer

## • 사전학습

## • 발전 주제

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

6

## 목차

## • 언어 모델이란 무엇인가?

## ＊대규모 언어 모델

## • Transformer

## • 사전학습

## • 발전 주제

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

7

## 언어 모델과 Transformer의 관계

최근 대규모 언어 모델에서 일반적으로 사용되는 모델 구조

언어 모델

신경망 언어 모델

Transformer

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

8

## 언어 모델(Language Models)이란

## • 단어 시퀀스(≒문장)의 발생 확률 𝑝(𝑥1, 𝑥2, ⋯, 𝑥𝐿)를 모델화한 것

## • 𝑝(𝑥1, 𝑥2, ⋯, 𝑥𝐿)을 연쇄법칙으로 분해한 형태를 자기회귀 언어 모델(autoregressive language model)이라 한다.

𝑝(𝑥1, 𝑥2, ⋯, 𝑥𝐿) = 𝑃(𝑥1) 𝑝(𝑥2|𝑥1) ⋯ 𝑝(𝑥𝐿|𝑥1, ⋯, 𝑥𝐿−1)

## • 조건부 확률을 알면 생성이 가능하다.

𝑝(東京|日本, の, 首都, は) = 0.2

𝑝(パリ|日本, の, 首都, は) = 0.001

⋮

𝑝(カイロ|日本, の, 首都, は) = 0.0005

## • 𝑥𝐿로 적절한 예측은 arg max 𝑝(𝑥𝐿|𝑥1, ⋯, 𝑥𝐿−1)

## • 이 조건부 확률을 신경망으로 표현한 것이 신경망 언어 모델이다.

## Day1의 복습

## 日本の首都は → 東京

## = arg max 𝑝(𝑥|日本, の, 首都, は)

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

9

## (참고) 딥러닝 이전의 대표적인 언어 모델

## • 조건부 확률을 통계적으로 구하는 방법

## • 대규모 코퍼스 내의 단어열 출현 빈도로부터 산출

## • 단어열 s의 출현 횟수를 #(s)라 하면,

## • 과제

## • 데이터 희소성(data sparseness) 문제

단어열이 길어지면 그 출현 횟수가 급격히 감소하여 조건부 확률 추정이 어려워진다.

## • 유의어 문제

유의어가 개별 사건으로 취급된다. 표현을 미세하게 바꾸는 것만으로도 출현 빈도가 다른 단어로 취급된다(예: "日本の首都は?"과 "日本国の首都は?").

𝑝(東京|日本, の, 首都, は) = #(日本, の, 首都, は, 東京) / #(日本, の, 首都, は)

1000회 / 200회

[1]岡崎直観(2023), 대규모 언어 모델의 경이와 위협 - Speaker Deck를 참고

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

10

## (참고) 딥러닝 이전의 대표적인 언어 모델

## • N-gram 언어 모델

## • 직전 N-1개의 단어를 사용해 다음 단어를 예측

## • 각 단어의 출현 확률은 출현 빈도로 추정

## • (예) 3-gram 언어 모델

## • 데이터 희소성 문제를 어느 정도 회피할 수 있다.

## • 장거리 단어 간의 관계를 파악하기 어렵다는 것이 과제

## Transformer로 해결(후술)

𝑝(東京|日本, の, 首都, は) ≈ 𝑝(東京|首都, は)

직전 2단어 "首都 は"만으로는 "東京"이라고 특정하기 어렵다.

[1]岡崎直観(2023), 대규모 언어 모델의 경이와 위협 - Speaker Deck를 참고

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

11

## 신경망 언어 모델

## • 조건부 확률을 어떤 신경망으로 추정한 모델

## • 다른 기계학습과 마찬가지로 가능도(likelihood)를 최대화하도록 훈련(오차 역전파)

日本 / の / 首都 / は

東京 / 京都 / 東京

오차 / 정답

어떤 네트워크 구조가 최적인가?

신경망

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

12

## 신경망 언어 모델

## • 신경망 언어 모델은 기계 번역 분야에서 크게 발전해 왔다.

## • 여기서부터 기계 번역 태스크를 예로 검토한다.

吾輩 / は / 猫 / である

신경망

I / am / a / cat

I / am / a

[1]岡崎直観(2023), 대규모 언어 모델의 경이와 위협 - Speaker Deck를 참고

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

13

## 신경망 언어 모델

인코더(입력) / 디코더(출력 + 재귀 입력)

吾輩 / は / 猫 / である

I / am / a / cat

I / am / a

## • 인코더: 문장(번역 원 언어) 입력 기구를 가진 신경망

## • 디코더: 문장(번역 대상 언어)의 출력 기구 및 재귀 입력 기구를 가진 신경망(NN)

재귀 입력 / 입력 / 출력

[1]岡崎直観(2023), 대규모 언어 모델의 경이와 위협 - Speaker Deck를 참고

[2] Ilya Sutskever et al. (2014), "sequence to sequence learning with neural networks", NeurIPS2014를 참고

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

14

## 신경망 언어 모델

## • RNN형 언어 모델(대표적 모델: Seq2Seq)

## • RNN: Recurrent Neural Network(순환 신경망)

## • 첫 단어부터 한 단어씩 신경망에 입력하여 뉴런을 순차적으로 갱신

## • 파라미터는 재사용

## • 원리적으로는 임의의 개수의 단어를 입력하고 출력할 수 있다.

吾輩 / は / 猫 / である

I / am / a / cat

I / am / a

[1]岡崎直観(2023), 대규모 언어 모델의 경이와 위협 - Speaker Deck를 참고

[3] Tomáš Mikolov et al. (2010), "recurrent neural network based language model", INTERSPEECH2010

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

15

## 신경망 언어 모델

## • RNN형 언어 모델(대표적 모델: Seq2Seq)

## • 과제①: 뉴런이 고정 길이이므로 장문이 되면 모든 정보를 기억할 수 없다.

결국 단어 간 장거리 의존성 파악이 곤란하다.

## • 과제②: 네트워크가 단어 방향으로 깊어져 학습이 불안정(기울기 소실, 기울기 폭발)하고 학습이 느리다.

吾輩 / は / 猫 / である

I / am / a / cat

I / am / a

여기까지 BackProp 하는 것이 힘들다...

입력 문장이 뭐였더라?(직전 단어는 기억하지만...)

[1]岡崎直観(2023), 대규모 언어 모델의 경이와 위협 - Speaker Deck를 참고

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

16

## 신경망 언어 모델

## • Transformer(모델 구조에 대해서는 후술)

## • 어텐션(attention) 메커니즘을 최대한 활용하여 앞서 언급한 RNN형의 문제를 해결(*)

## • 단어 간 장거리 의존성을 파악할 수 있게 되었다.

## • 오차 역전파(BackProp) 스텝 수가 단어 수에 의존하지 않게(짧아져) 학습의 안정화와 고속화를 실현

吾輩 / は / 猫 / である

I / am / a

어텐션 메커니즘(후술)

어텐션 메커니즘(후술)

I / am / a / cat

(*) RNN에 어텐션 메커니즘을 도입한 선행연구는 존재하지만, 전 단어 간에는 아니었다. Transformer는 전 단어 간에 어텐션 메커니즘을 도입했다. 멀티헤드 어텐션(multi-head attention)도 새롭게 도입되었다.

[4] Dzmitry Bahdanau et al. (2014), "Neural machine translation by jointly learning to align and translate" / 기술적 차이에 대한 해설은 다음이 이해하기 쉽다.

[5] Masaki Hayashi (2022), Transformer와 seq2seq with attention의 차이는? 시열 변환 모델【Q and A 기사】| CVML 전문가 가이드

## 여기까지의 BackProp 스텝 수가 짧아졌다!

## 장문의 중요 부분을 기억하고 있다!

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

17

## 목차

## • 언어 모델이란 무엇인가?

## • Transformer

## • 사전학습

## • 발전 주제

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

18

## LLM의 모델 구조

2024/08/07 Google Scholar에 접속

## • Google을 중심으로 한 연구팀이 발표

## • 어텐션(attention) 메커니즘 채용으로 단어(토큰)의 장거리 의존 관계를 효율적으로 학습

## • 학습 시 병렬 계산도 효율화되어 대규모화(분산 학습)가 쉬워졌다.

"Attention Is All You Need", 2017

[6] Ashish Vaswani et al. (2017), "Attention Is All You Need", NeurIPS2017에서 인용

## Transformer가 주류("Attention Is All You Need"라는 논문에서 최초 등장)

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

19

## Transformer의 탁월함

## • 2017년 발표 이후 모델 개량과 스케일링을 통해 다수의 벤치마크에서 당시 최고 성능(SOTA)을 지속적으로 달성

## • GPT-1~4, gpt-oss, Gemini 2.5 등은 Transformer를 채택

## • GPT-4는 모델의 상세한 구조는 비공개이지만, Transformer 기반임을 Technical Report에 기재

## • GPT-5의 아키텍처는 불명이지만, system card에는 LLM으로 기술되어 있다.

## • GPT-5의 평가 사례

## • AIME 2025(미국 고교생 대상 수학 경진대회)에서 94.6%(도구 없이) 기록

## • 의료 분야에서 HealthBench Hard 46.2%

## • Gemini 2.5의 평가 사례

## • AIME 2025에서 88.0% 기록

## • 최적화된 프레임워크로 포켓몬스터 블루를 406.5시간에 클리어

## LLM의 모델 구조

[7] OpenAI (2023), "GPT-4 Technical Report"

[8] OpenAI (2025), "GPT-5 System Card"

[9] OpenAI (2025), "GPT-5가 등장"

[10] Google (2025), "Gemini 2.5 tech report"

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

20

## Transformer의 모델 구조

## • "블록(block)": Transformer를 구성하는 최소 단위

## • 좌측 Encoder 블록을 세로로 N층, 우측 Decoder 블록도 세로로 N층 배열하여 구성

[6] Ashish Vaswani et al. (2017), "Attention Is All You Need", NeurIPS2017에서 인용

## Transformer

## Encoder Block

## Decoder Block

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

21

## Transformer의 모델 구조 | 이미지

吾輩 / は / 猫 / である

I / am / a / cat

I / am / a

・  ・

Encoder / Decoder

Encoder/Decoder 블록이 각각 세로로 쌓인다.

토큰 수만큼 블록이 가로로 늘어난다.

어텐션 메커니즘에 의해 가로 블록끼리 연결되어(정보 전달을 수행) <BOS>

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

22

## Transformer의 모델 구조 | 이미지(GPT 시리즈)

桜 / が / 綺麗

は / 桜 / が

・  ・

## ＊실은 Encoder가 없어도 Decoder만으로 텍스트 생성이 가능하다(출력과 재귀 입력이 있으므로).

## ＊GPT 시리즈는 이 형식.

## ＊Transformer가 최초 제안된 분야가 기계 번역이었기 때문에 선행연구의 Encoder-Decoder 형식을 따라 모델 구조가 제안되었다.

春

Decoder

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

23

## • Embedding

## • Multi-Head Attention

## • Feed Forward

## • Others

## Transformer의 구성 요소

각 요소별 해설

[6] Ashish Vaswani et al. (2017), "Attention Is All You Need", NeurIPS2017에서 인용, 일부 개변

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

24

## Transformer의 구성 요소 | Embedding

각 요소별 해설

## • Embedding: 단어의 벡터 변환

## • Multi-Head Attention

## • Feed Forward

## • Others

색을 RGB의 3차원 벡터로 변환하는 것과 비슷하다.

[6] Ashish Vaswani et al. (2017), "Attention Is All You Need", NeurIPS2017에서 인용, 일부 개변

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

25

## Transformer의 구성 요소 | Embedding - 텍스트를 어떻게 Block에 가져오는가?

"春は曙"

"春", "は", "曙"

1050, 80, 24567

[0,0,…,0,1,0,…0]

[0,0,…,0,1,0,…0]

[0,0,…,0,1,0,…0]

[0.2,-0.5,…,…0.4]

[-0.3,1.0,…,…0.8]

[1.7,-0.9,…,…-0.6]

텍스트 / 토큰 / 토큰 ID / One-hot 벡터 / Word Embedding

단어의 분산 표현, 단어 임베딩

MLP에 의한 저차원 변환(학습 대상)

{토큰 ID}번째만 1이고 나머지는 모두 0인 벡터 구성

각 토큰에 일대일로 할당된 토큰 ID로의 변환

토크나이저(*후술)에 의한 분할

1050번째 / 80번째 / 24567번째

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

26

## Transformer의 구성 요소 | Embedding - Word Embedding (WE)

## • 단어(sparse한 정보)를 dense한 표현으로 변환

## • Transformer 등 모델의 입력값으로 취급 가능

## • 학습 완료 후의 Word Embedding에는 단어 간 의미의 유사성이나 관계성이 내장되어 있다(아래 그림은 이미지).

색을 RGB의 3차원 벡터로 변환하는 것과 비슷하다.

[15] Shraddha Anala (2020), "A Guide to Word Embedding. What are they? How are they more useful… | by Shraddha Anala | Towards Data Science"에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

27

## Transformer의 구성 요소 | Embedding - Positional Encoding (PE)

i번째 토큰의 PE

1번째 토큰의 PE

i번째 토큰의 PE

d: 벡터의 차원 수

마지막 토큰의 PE

## • Transformer 블록에 가져오기 전에 Word Embedding에 위치 정보를 추가

## • Transformer 블록의 알고리즘은 토큰의 위치 정보에 의존하지 않는다.

## • 이대로는 단어의 위치 관계가 고려되지 않으므로 사전에 벡터에 내장한다.

## • 구현 예: 토큰의 위치에 따라 다른 PE를 각 WE에 더한다.

## • WE("春") + PE("이것은 1번째 토큰입니다")

## • WE("は") + PE("이것은 2번째 토큰입니다")

## • WE("曙") + PE("이것은 3번째 토큰입니다")

[16] John Hewitt, Natural Language Processing with Deep Learning CS224N/Ling284에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

28

## Transformer의 구성 요소 | Embedding

각 요소별 해설

## • Embedding: 단어의 벡터 변환

## • Multi-Head Attention

## • Feed Forward

## • Others

텍스트를 토큰으로 분할

Word Embedding(벡터)으로 변환

Positional Encoding과 더하여 Transformer에 입력

[6] Ashish Vaswani et al. (2017), "Attention Is All You Need", NeurIPS2017에서 인용, 일부 개변

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

29

## Transformer의 구성 요소 | Multi-Head Attention

각 요소별 해설

## • Embedding

## • Multi-Head Attention

## • Feed Forward

## • Others

[6] Ashish Vaswani et al. (2017), "Attention Is All You Need", NeurIPS2017에서 인용, 일부 개변

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

30

## Transformer의 구성 요소 | Attention

모든 토큰 간의 유사도를 측정함으로써 장거리 토큰 간의 의존 관계를 파악할 수 있게 한 메커니즘.

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

31

## Transformer의 구성 요소 | Attention

수식 정리

다음 페이지부터 이 수식을 애니메이션으로 설명한다.

[6] Ashish Vaswani et al. (2017), "Attention Is All You Need", NeurIPS2017에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

32

## Transformer의 구성 요소 | Attention

春 / は / 曙

어텐션 메커니즘의 입력값: 토큰의 벡터 표현

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium에서 인용, 일부 개변

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

33

## Transformer의 구성 요소 | Attention

선형 변환(MLP)으로 Key 벡터 작성

선형 변환(MLP)으로 Value 벡터 작성

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium에서 인용, 일부 개변

春 / は / 曙

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

34

## Transformer의 구성 요소 | Attention

첫 번째 토큰("春")에 대해 선형 변환(MLP)으로 Query 벡터 작성

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium에서 인용, 일부 개변

春 / は / 曙

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

35

## Transformer의 구성 요소 | Attention

Query 벡터와 Key 벡터의 내적으로 토큰 간 유사도 = Score 측정

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium에서 인용, 일부 개변

春 / は / 曙

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

36

## Transformer의 구성 요소 | Attention

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium에서 인용, 일부 개변

春 / は / 曙

Query 벡터와 Key 벡터의 내적으로 토큰 간 유사도 = Score 측정

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

37

## Transformer의 구성 요소 | Attention

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium에서 인용, 일부 개변

春 / は / 曙

Query 벡터와 Key 벡터의 내적으로 토큰 간 유사도 = Score 측정

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

38

## Transformer의 구성 요소 | Attention

유사도를 Softmax로 정규화(즉, 합계가 1이 됨)

값이 클수록 유사도[=단어 간 의존]가 강하다.

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium에서 인용, 일부 개변

春 / は / 曙

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

39

## Transformer의 구성 요소 | Attention

유사도(실수)와 Value 벡터의 곱셈

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium에서 인용, 일부 개변

春 / は / 曙

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

40

## Transformer의 구성 요소 | Attention

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium에서 인용, 일부 개변

春 / は / 曙

유사도(실수)와 Value 벡터의 곱셈

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

41

## Transformer의 구성 요소 | Attention

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium에서 인용, 일부 개변

春 / は / 曙

유사도(실수)와 Value 벡터의 곱셈

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

42

## Transformer의 구성 요소 | Attention

모든 벡터의 총합 계산

어텐션의 유사도에 따라 Value 벡터의 가중 평균 산출

이를 첫 번째 토큰의 어텐션 메커니즘 출력값으로 한다.

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium에서 인용, 일부 개변

春 / は / 曙

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

43

## Transformer의 구성 요소 | Attention

두 번째 토큰("は")에 대해 선형 변환(MLP)으로 Query 벡터 작성

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium에서 인용, 일부 개변

春 / は / 曙

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

44

## Transformer의 구성 요소 | Attention

같은 흐름으로 두 번째 토큰의 어텐션 메커니즘 출력값 산출

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium에서 인용, 일부 개변

春 / は / 曙

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

45

## Transformer의 구성 요소 | Attention

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium에서 인용, 일부 개변

春 / は / 曙

세 번째 토큰("曙")에 대해 선형 변환(MLP)으로 Query 벡터 작성

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

46

## Transformer의 구성 요소 | Attention

같은 흐름으로 세 번째 토큰의 어텐션 메커니즘 출력값 산출

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium에서 인용, 일부 개변

春 / は / 曙

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

47

## Transformer의 구성 요소 | Attention(빠른 복습)

春 / は / 曙

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium에서 인용, 일부 개변

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

48

## Transformer의 구성 요소 | Attention

春 / は / 曙

입력 / 출력

1스텝으로 모든 단어와 연결되어 멀리 있는 토큰의 정보를 효율적으로 가져올 수 있게 되었다!

각 토큰이 필요한 토큰의 정보만 유연하게 취사선택(이것은 시계열 순서대로 토큰을 가져오는 RNN형에서는 실현 불가능했던 것)

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium에서 인용, 일부 개변

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

49

## Transformer의 구성 요소 | Attention

春 / は / 曙

입력 / 출력

예①: 다음 토큰을 예측할 때 직전 토큰만 도움이 되는 경우, 멀리 볼 필요가 없다.

예②: 다음 토큰을 예측할 때 멀리 있는 토큰 정보가 중요한 경우, 가까이 볼 필요가 없다.

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium에서 인용, 일부 개변

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

50

## Transformer의 구성 요소 | Attention

春 / は / 曙

입력 / 출력

1스텝으로 모든 단어와 연결됨으로써 RNN의 과제였던 ① 단어 간 장거리 의존 관계를 파악할 수 있게 되었다!

② 오차 역전파가 안정적이고 고속화되었다!(*)

## (*)

안정: 기울기 소실이나 기울기 폭발이 발생하지 않음

고속: GPU 등에서 병렬 연산 처리하기 쉬움

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium에서 인용, 일부 개변

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

51

## Transformer의 구성 요소 | Attention

春 / は / 曙

입력 / 출력

즉, 어텐션 메커니즘을 통해 각 토큰의 벡터가 다른 토큰과의 관계성을 흡수하여 더 나은 표현으로 Transform = 변환되었다!

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium에서 인용, 일부 개변

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

52

## Transformer의 구성 요소 | Attention 시각화 예

"it"은 "The" "animal"에 강한 어텐션이 걸려 있음을 알 수 있다.

## ＊항상 이 정도로 명확한 관계가 얻어지는 것은 아니다.

모든 단어 간 Attention Map(히트맵)을 만들 수 있다.

The / The / animal / didn / ' / cross / animal / didn / ' / t / cross / t

[18] Jay Alammar (2018) The Illustrated Transformer – Jay Alammar – Visualizing machine learning one concept at a time.에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

53

## Transformer의 구성 요소 | Attention

수식 정리(복습)

벡터의 차원 수가 증가하면 Q와 K의 내적 값(분산)이 증대. 이를 억제하기 위해 벡터의 차원 수(의 제곱근)로 나눈다.

[6] Ashish Vaswani et al. (2017), "Attention Is All You Need", NeurIPS2017에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

54

## Transformer의 구성 요소 | Attention

Encoder 측 어텐션 메커니즘

## • 입력 텍스트 내 어텐션(Self-Attention)

Decoder 측 어텐션 메커니즘

## • 입력 텍스트와 출력 텍스트를 가로지르는 어텐션(Cross-Attention)

## • 출력 텍스트 내 어텐션(Self-Attention)

## • 출력 텍스트: 자신보다 미래의 토큰에는 어텐션을 못 하도록 마스크(Causal Attention Mask) 적용

Decoder는 미래 텍스트를 예측하는 메커니즘이므로 부정행위를 방지할 필요가 있다.

I / am / a / cat

I / am / a / cat

검은 칸 부분은 Query 측 토큰 기준으로 미래 토큰이므로 Causal Attention Mask를 적용해 어텐션을 걸지 못하게 한다.

## ＊프로그램 구현 상으로는 AttentionMap의 Softmax 직전에 해당 요소에 큰 음수 값(예: -1.0e+10)을 더한다.

## Query / Key

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

55

## Transformer의 구성 요소 | Multi-Head Attention

## • 어텐션 처리를 여러 개 병렬로 수행. 그 후 출력을 하나의 벡터로 통합.

## • 하나의 토큰이 다양한 토큰에 서로 다른 형태의 어텐션을 적용 가능.

i번째 어텐션 메커니즘의 출력

h개의 어텐션 메커니즘 출력(벡터)을 Concatenate

[6] Ashish Vaswani et al. (2017), "Attention Is All You Need", NeurIPS2017에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

56

## Transformer의 구성 요소 | Multi-Head Attention

각 요소별 해설

## • Embedding

## • Multi-Head Attention

## • Feed Forward

## • Others

각 토큰의 벡터를 다른 토큰과의 관계성을 흡수하여 더 나은 표현으로 변환

[6] Ashish Vaswani et al. (2017), "Attention Is All You Need", NeurIPS2017에서 인용, 일부 개변

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

57

## Transformer의 구성 요소 | Feed Forward

각 요소별 해설

## • Embedding

## • Multi-Head Attention

## • Feed Forward

## • Others

[6] Ashish Vaswani et al. (2017), "Attention Is All You Need", NeurIPS2017에서 인용, 일부 개변

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

58

## Feed Forward

## Transformer의 구성 요소 | Feed Forward

거대한 2계층 MLP

활성화 함수(ReLU)

학습 파라미터

입력 / 출력

입력층 / 출력층 / 중간층

중간층의 차원 수는 입력/출력층 차원 수의 수 배

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

59

## Transformer의 구성 요소 | Feed Forward

거대한 2계층 MLP

활성화 함수(ReLU)

학습 파라미터

입력 / 출력

예를 들어 GPT-3의 경우,

## • 입력층/출력층 차원 수: 12,288

## • 중간층 차원 수: 12,288×4=49,152

## • 총 블록 수: 96

즉,

Feed Forward의 파라미터 수: (12,288×49,152)[파라미터/층] × 2[층/블록] × 96[블록] ≒ 116B[파라미터]

GPT-3의 총 파라미터 수: 175B[파라미터]

Feed Forward가 전체에서 차지하는 파라미터 비율: 약 66%

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

60

## Transformer의 구성 요소 | Feed Forward

거대한 2계층 MLP

활성화 함수(ReLU)

학습 파라미터

입력 / 출력

gpt-oss120B / Llama3.1 / DeepSeek-v3 / Qwen3

FF 파라미터 수(Billions): 3.6 (115) / 329 / 23 (657) / 14 (227)

전체 파라미터 수(Billions): 5.1 (117) / 405 / 37 (671) / 22 (235)

파라미터 수에서 FF 비율(%): 71 (98.3) / 81.4 / 62 (97.8) / 64 (96.7)

최근 각 모델 시리즈의 최대 모델 파라미터 구성*

## *

괄호 안은 MoE 모델의 총 파라미터 수. MoE 모델은 입력에 따라 사용하는 파라미터가 달라져 실제 예측 시에는 괄호 왼쪽의 수의 파라미터만 사용된다.

최근 모델은 위 수식과 약간 다른 알고리즘 채택(SwiGLU 등)

huggingface의 config에 등록된 mlp 층의 파라미터 수를 기반으로 계산

gpt-oss는 Model Card의 Table1, DeepSeek-v3는 Technical Report의 Section 4.2도 참고

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

61

## Transformer의 구성 요소 | Feed Forward는 무엇을 하는가?

Feed Forward는 파라미터 수가 큰 만큼 중요할까?

## • 제1층의 파라미터를 Key(K)로 간주

## • 입력 패턴 추출

## • 제2층의 파라미터를 Value(V)로 간주

## • 패턴이 무엇을 의미하는지 표현

## • 신경망 메모리(↓)를 모방

## 로 해석 가능

## ⇒ 지식을 축적하는 장소로 생각할 수 있다.

[19] Mor Geva et al. (2021), "Transformer Feed-Forward Layers Are Key-Value Memories", ACL2021에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

62

## Transformer의 구성 요소 | Feed Forward

각 요소별 해설

## • Embedding

## • Multi-Head Attention

## • Feed Forward

## • Others

거대한 2계층 MLP

Key-Value로 축적한 지식을 추출하는 메커니즘으로 간주되고 있다.

[6] Ashish Vaswani et al. (2017), "Attention Is All You Need", NeurIPS2017에서 인용, 일부 개변

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

63

## Transformer의 구성 요소 | Others

각 요소별 해설

## • Embedding

## • Multi-Head Attention

## • Feed Forward

## • Others

[6] Ashish Vaswani et al. (2017), "Attention Is All You Need", NeurIPS2017에서 인용, 일부 개변

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

64

## Transformer의 구성 요소 | Add & Norm

Add: 잔차 연결(residual connection)

깊은 층의 학습 시 사용하는 기법

Feed Forward / Attention 이후에 적용

Norm: 층 정규화(Layer Normalization)

학습을 안정화하는 기법

은닉층의 차원 축으로 평균과 분산을 취해 정규화

[6] Ashish Vaswani et al. (2017), "Attention Is All You Need", NeurIPS2017에서 인용, 일부 개변

[20] Kaiming He et al. (2016), "Deep Residual Learning for Image Recognition", IEEE2016를 참고

[21] Jimmy Lei Ba et al. (2016), "Layer Normalization"을 참고

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

65

## Transformer의 구성 요소 | 출력층

## • 선형 변환 후 Softmax 함수 적용

## • 다음 단어의 발생 확률 출력

東京 / 京都

[6] Ashish Vaswani et al. (2017), "Attention Is All You Need", NeurIPS2017에서 인용, 일부 개변

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

66

## Transformer의 구성 요소(복습)

## • Embedding

## • Multi-Head Attention

## • Feed Forward

## • Others

잔차 연결 / 층 정규화 / 출력층

텍스트를 토큰으로 분할

Word Embedding(벡터)으로 변환

Positional Encoding과 더하여 Transformer에 입력

각 토큰의 벡터를 다른 토큰과의 관계성을 흡수하여 더 나은 표현으로 변환

거대한 2계층 MLP

Key-Value로 축적한 지식을 추출하는 메커니즘으로 간주됨

[6] Ashish Vaswani et al. (2017), "Attention Is All You Need", NeurIPS2017에서 인용, 일부 개변

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

67

## 목차

## • 언어 모델이란 무엇인가?

## • Transformer

## • 사전학습

## • 발전 주제

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

68

## LLM 학습 흐름

사전학습

대규모 코퍼스를 통한 자기 지도 학습을 통해 대규모 언어 모델에 어휘·문법·기본 지식 등 기초적인 언어 이해를 획득시키는 단계

파인튜닝

레이블이 있는 데이터를 통한 지도 학습을 통해 사전학습된 모델의 성능을 개선하거나 특정 태스크나 도메인에 적응시키는 단계

강화 학습

인간 피드백을 활용하여 대규모 언어 모델의 출력이 인간의 가치관에 보다 부합하도록 조정하는 단계

## Step 1

## Step 2

## Step 3

## Day3(오늘)

## Day6

## Day7

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

69

## 사전학습이란

LLM 이전

・・・

번역 모델 / 요약 모델 / 독해 모델 / ・・・

학습

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

70

## 사전학습이란

LLM 이전 / LLM

・・・

번역 모델 / 요약 모델 / 독해 모델 / ・・・

사전학습 / 범용 / LLM

학습 / 대규모 코퍼스

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

71

## 사전학습이란

LLM 이전 / LLM

・・・

번역 모델 / 요약 모델 / 독해 모델 / ・・・

번역 모델 / 요약 모델 / 독해 모델

사후 학습

## • 파인튜닝

## • 강화 학습

사전학습 / 범용 / LLM

학습 / 대규모 코퍼스

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

72

## 사전학습이란

## • 사전학습의 목적

## • 후속 태스크에 공통으로 필요한 범용 지식(예: 읽기·쓰기·셈하기)을 학습하고 그 지식을 후속 태스크로 전이(c.f. Transfer Learning)

## • 후속 태스크를 위한 좋은 파라미터 초기값을 얻을 수 있다고도 해석 가능

## ＊후속 태스크: 최종적으로 풀고자 하는 태스크(요약, 번역, 독해…)

[22] Rishi Bommasani et al. (2021), "On the Opportunities and Risks of Foundation Models"에서 인용, 일부 개변

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

73

## 사전학습 파이프라인

데이터 수집

데이터 전처리

훈련

평가

상세한 해설은 본 자료 "발전 주제" 섹션에서

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

74

## 데이터 수집 | 데이터 구성 요소

## • 예로 작년에 릴리스되고 데이터 소스 비율이 공개된 OLMo2 사례가 아래 그림.

## • 사전학습용 데이터는 일반적으로 웹 대규모 크롤 데이터

코드 / 백과사전 / 논문 / 일반적인 웹사이트(뉴스, 블로그, 홈페이지)

[12] Allen Institute for AI, Univ. of Washington, NYU (2025), "2 OLMo 2 Furious"에서 인용, 일부 개변

## 수학 특화 데이터

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

75

[13] OpenAI (2025), "gpt-oss-120b & gpt-oss-20b Model Card"

[14] Qwen (2025), "Qwen3 Technical Report"

[12] Allen Institute for AI, Univ. of Washington, NYU (2025), "2 OLMo 2 Furious"

[24] Tom Brown et al. (2020), "Language Models are Few-Shot Learners", NeurIPS2020에서 인용

Llama3.1, DeepSeek-v3는 Huggingface 레포지토리 기재를 인용

## 데이터 수집 | 데이터 양

최근 모델의 사전학습 토큰 수

## • 1~40조 토큰*의 텍스트 사용

## *토큰: 언어 AI가 처리하는 언어의 단위. 일본어는 대략 1문자 1토큰

## • 서적으로 환산(1권 10만 토큰으로 가정)하면

## 1조 토큰은 약 1,000만 권에 상당

## 참고: 도쿄대 도서관이 1,000만 권 이상

## 국회도서관이 약 4,800만 권

토큰 수[조]

gpt-oss120B / 수조

Llama3.1 / 15~

DeepSeek-v3 / 14.8

Qwen3 / 36

GPT-3 / 0.5

OLMo 2 / 3.9

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

76

## •

Quality Filtering(품질 필터링)

분류기나 휴리스틱으로 질이 낮은 데이터를 제거

## •

De-dup(중복 제거)

가까운 위치에 중복이 있으면 학습에 악영향이 크므로 문장, 문서, 데이터셋 등 다양한 단위로 중복을 제거

## •

Privacy Reduction(프라이버시 저감)

개인을 식별할 수 있는 정보를 제거(＊)

## •

Tokenization(토큰화)

(다음 페이지에서 설명)

## LLM 사전학습의 전형적인 전처리 파이프라인

## ＊데이터셋마다 전처리 방식은 다릅니다. 본 자료 "발전 주제"도 참조.

（＊）Our approach relies on a combination of logistic classifiers (content tagging) and regular expressions (PII detection). In practice: We detect and mask email addresses, phone numbers, and IP addresses.

[25] Luca Soldaini (2023), AI2 Dolma: 3 Trillion Token Open Corpus for LLMs | AI2 Blog

[26] Wayne Xin Zhao et al. (2023), "A Survey of Large Language Models"에서 인용

## 데이터 전처리

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

77

## 데이터 전처리 | Tokenization: 텍스트 토큰화

## • 토큰화: 텍스트를 "토큰"이라 불리는 최소 단위로 분할하는 것

## • 토크나이저: 토큰화를 수행하는 프로그램

## • 예: Byte Pair Encoding(BPE), SentencePiece

## • 효율적으로 토큰화하고 싶다 → 일반적으로 어휘 출현 빈도에 기반한 알고리즘으로 실현

## • 코퍼스에서 정의한 알고리즘에 따라 토크나이저가 어휘 사전을 작성한 후 토큰화 수행(상세는 본 자료 "발전 주제"에서 해설)

"吾輩は猫である。"

↓

"吾輩", "は", "猫", "で", "ある", "。"

토큰화 이미지

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

78

## 훈련(사전학습) | Next Token Prediction

## • 학습용 텍스트 데이터를 사용해 다음 토큰의 생성 확률을 계속 예측

## • 자기 지도 학습의 일종

吾輩

吾輩 / は

吾輩 / は / 猫

吾輩 / は / 猫 / で

吾輩 / は / 猫 / で / ある

LLM / LLM / LLM / LLM / LLM

P(は|吾輩)

P(猫|吾輩,は)

P(で|吾輩,は,猫)

P(ある|吾輩,は,猫,で)

P(。|吾輩,は,猫,で,ある)

입력 / 예측

は / 猫 / で / ある / 。

정답

예측과 정답의 오차(교차 엔트로피)가 작아지도록 학습

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

79

## 훈련(사전학습) | Next Token Prediction

## • 학습용 텍스트 데이터를 사용해 다음 토큰의 발생 확률을 계속 예측

## • 예측과 정답의 오차(교차 엔트로피)가 작아지도록 학습

## • 즉 사전학습의 목적 함수로 minimize(교차 엔트로피)를 사용

## ＊위 샘플 문장 단위의 교차 엔트로피를 미니배치 내 각 샘플 문장마다 계산하여 평균한 것을 Loss로 함

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

80

## 훈련(사전학습) | Next Token Prediction

## • 일반적으로 1 epoch만 학습(1~3 범위)

[28] Hugo Touvron et al. (2023), "Llama 2: Open Foundation and Fine-Tuned Chat Models"에서 인용

[23] Hugo Touvron et al. (2023), "LLaMA: Open and Efficient Foundation Language Models"에서 인용

[27] Guilherme Penedo et al.(2023), "The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Data, and Web Data Only"에서 인용

## [23]

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

81

## 훈련(사전학습) | Next Token Prediction

## • 일반적으로 1 epoch만 학습(1~3 범위)

## • 여러 epoch 학습하면 과적합되어 degradation(성능 저하)되거나 차이가 없음

## • 모델 크기가 커질수록 degradation 경향이 강해짐

81

[29] Fuzhao Xue et al. (2023), "To Repeat or Not To Repeat: Insights from Scaling LLM under Token-Crisis"에서 인용(좌도)

[30] Niklas Muennighoff et al. (2023), "Scaling Data-Constrained Language Models"에서 인용(우도)

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

82

## 훈련(사전학습) | Next Token Prediction

## • 원리적으로는 간단하지만 실제로 해보면 어렵다.

## • 소규모 모델 학습에서는 발생하지 않지만, 대규모 모델 학습(+다중 노드 분산 학습)에서 발생하는 현상

## •

교차 엔트로피 발산(Loss 스파이크)

## •

하드웨어, 네트워크 등 저수준 에러

82

계산하는 수치 포맷에 따라서도 안정성이 달라짐(최근은 bfloat16이 주류)

82

[31] Stas Bekman (2022) The Technology Behind BLOOM Training에서 인용(좌도)

[32] suchenxang (2023), metaseq/projects/OPT/chronicles/OPT175B_Logbook.pdf at main · facebookresearch/metaseq · GitHub에서 인용(우도)

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

83

## 훈련(사전학습) | 하이퍼파라미터 예

## • Optimizer: Adam[33], AdamW[34]

## • Scheduler: Learning Rate Warmup + Decay

## • 부동소수점 정밀도: 최근 BF16이 주류

## • Batch Size: 수백만 토큰이 일반적

83

83

83

## 미니배치 내 토큰 수 = 샘플 수 × 최대 토큰 길이

샘플 수 / 샘플당 최대 토큰 길이

[33] Diederik P. Kingma & Jimmy Ba, (2014), "Adam: A Method for Stochastic Optimization"를 참고

[34] Ilya Loshchilov & Frank Hutter, (2017), "Decoupled Weight Decay Regularization"을 참고

[23] Hugo Touvron et al. (2023), "LLaMA: Open and Efficient Foundation Language Models"에서 인용, 일부 개변(좌하표)

[35] Shikoan's ML Blog (2021), Cosine Decay와 Warmup을 동시에 수행하는 스케줄러(timm) | Shikoan's ML Blog에서 인용, 일부 개변(우상도)

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

84

## 평가 | 정량 평가(Upstream)

## • 교차 엔트로피 Validation Loss:

## •

Loss가 떨어지고 있는지(사전학습 자체가 붕괴하지 않았는지) 모니터링

## •

모델 간 성능 차이 확인

## •

Test Loss는 논문에서 (거의) 보이지 않음*사전학습은 1 epoch 학습이 일반적이므로 Overfit하지 않다는 전제 때문인가?

## •

경우에 따라 Training Loss만으로 끝나는 경우도 많음.

84

[23] Hugo Touvron et al. (2023), "LLaMA: Open and Efficient Foundation Language Models"에서 인용, 일부 개변(좌도)

[24] Tom Brown et al. (2020), "Language Models are Few-Shot Learners"의 arXiv판에서 인용(우도)

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

85

## 평가 | 정량 평가(Upstream)

## • 교차 엔트로피의 다양한 명칭

## •

교차 엔트로피

## •

Cross Entropy Loss

## •

CELoss

## • 식 변형 시 교차 엔트로피와 실질 동일한 지표.

## •

Perplexity(PPL)

## •

Bits-Per-Character(BPC)

## •

Bits-Per-Word(BPW)

85

[7] OpenAI (2023) "GPT-4 Technical Report"에서 인용, 일부 개변(우상도)

[28] Hugo Touvron et al. (2023), "Llama 2: Open Foundation and Fine-Tuned Chat Models"에서 인용, 일부 개변(우하도)

참고: [36] Chip Huyen (2019), Evaluation Metrics for Language Modeling

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

86

[24] Tom Brown et al. (2020), "Language Models are Few-Shot Learners"의 arXiv판에서 일부 발췌, 개변

## 평가 | 정량 평가(Downstream)

## • 다양한 하위 태스크(최종적으로 풀고자 하는 태스크)(*1)로 평가

## • In-Context Learning(Zero-shot, Few-shot)(*2)으로 평가하는 경우가 많음

## • 사후 학습(파인튜닝이나 RLHF)(*3)으로 하위 태스크 성능은 더 향상

## (*1) 본 강의 "발전 주제"에 평가 벤치마크 설명 있음.

## (*2) Day2를 복습하세요.

## (*3) Day5, Day7에서 설명 예정.

하위 태스크

86

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

87

## 평가 | 정성 평가(샘플 평가)

## • 사전학습된 LLM을 사용하여 텍스트를 출력(디코딩)해 본다.

## • 디코딩에는 다양한 방식이 존재

## •

Greedy Decoding

## •

Beam Search

## •

Random Sampling

87

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

88

## 평가 | 사전학습 모델에 의한 텍스트 생성(디코딩) 방법

## • 디코딩 방식 ①: Greedy Decoding

## •

발생 확률이 가장 높은 다음 토큰을 순차적으로 선택

88

[37] Kaito Sugimoto (2021) 텍스트 생성에서의 decoding 테크닉: Greedy search, Beam search, Top-K, Top-p에서 인용, 일부 개변

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

89

## • 디코딩 방식 ②: Beam Search

## •

높은 발생 확률이 되는 토큰 시퀀스를 탐색하여 발견

직전뿐 아니라 그 이후까지 보고 결정

## •

단, 전 시퀀스 탐색(Exhaustive Search)하면 계산량 폭발

미리 정해둔 빔 크기 내에서 탐색

## 평가 | 사전학습 모델에 의한 텍스트 생성(디코딩) 방법

89

## 빔 크기=3인 경우

[37] Kaito Sugimoto (2021) 텍스트 생성에서의 decoding 테크닉: Greedy search, Beam search, Top-K, Top-p에서 인용, 일부 개변

[38] mm_0824 (2020) 빔서치(Beam Search) 이해하기 | 즐기며 이해하는 AI·머신러닝 입문에서 인용(우도)

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

90

## 평가 | 사전학습 모델에 의한 텍스트 생성(디코딩) 방법

## • 디코딩 방식 ③: Random Sampling

## •

다음 토큰의 발생 확률 분포를 따라 무작위로 선택.

## •

Top_p: 상위 p% 토큰에서 선택. (예) 0.9

## •

Top_k: 상위 k개 토큰에서 선택. (예) 10

## •

Temperature: 0 이상의 실수(스칼라 값). Softmax 직전 Logit의 분모에 곱함.

## Temperature = 1이면 일반 Softmax와 동일.

90

[39] cohere, Temperature에서 인용

[68] Harshit Sharma (2022), "Softmax Temperature"에서 인용, 일부 개변

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

91

## 평가 | 사전학습 모델에 의한 텍스트 생성(디코딩) 방법

## • 상황에 따라 바람직한 디코딩 방식은 달라짐

## •

분류 문제를 푸는 경우, 결정론적 답을 내는 Greedy Decoding이 선호됨

## •

Beam Search는 기계 번역 태스크에서 자주 볼 수 있음

## •

장문 생성의 경우 Random Sampling을 수행하는 경우가 많음

91

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

92

## 목차

## • 언어 모델이란 무엇인가?

## • Transformer

## • 사전학습

## • 발전 주제

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

93

## 발전 주제

데이터 / 모델 / 학습 / 평가·분석

## •

주요 데이터셋

## •

데이터 처리(클렌징, 토큰화)

## •

주요 모델

## •

아키텍처 구성 요소

## •

Attention

## •

목적 함수

## •

평가

## •

분석

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

94

## 발전 주제

데이터 / 모델 / 학습 / 평가·분석

## •

주요 데이터셋

## •

데이터 처리(클렌징, 토큰화)

## •

주요 모델

## •

아키텍처 구성 요소

## •

Attention

## •

목적 함수

## •

평가

## •

분석

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

95

## 학습에 사용하는 데이터셋의 변천

"A Survey of Large Language Models", 2023

## ■주요 모델의 학습 데이터 구성

## • GPT-2에서는 웹페이지 코퍼스(약 40GB)만으로 학습을 수행

## • 최근에는 Code나 대화 데이터 등 다양한 데이터로 학습하는 모델이 증가

95

[26] Wayne Xin Zhao et al. (2023), "A Survey of Large Language Models"에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

96

## C4 | 필터링된 거대한 웹페이지 영어 코퍼스

"Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer", 2019

## • Common Crawl… 공개된 웹 아카이브를 스크래핑하여 수집한 데이터셋. 월당 약 20TB의 데이터량 존재.

## • C4… 2019년 4월 웹 추출 데이터 중 언어 판정 결과가 영어이고, 다수의 데이터 필터링, 클렌징을 거쳐 수집된 데이터셋

## ■C4 유래 데이터셋과 기존 데이터셋으로 학습한 경우 성능 비교

C4 유래 데이터셋 / 기존 데이터셋

[41] Colin Raffel et al. (2020), "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer"에서 인용, 일부 개변

96

[41] Colin Raffel et al. (2020), "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer"에서 인용, 일부 개변

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

97

## 다국어에 걸쳐 수집된 텍스트 코퍼스

"Unsupervised Cross-lingual Representation Learning at Scale", ACL2020

"mT5: A Massively Multilingual Pre-trained Text-to-Text Transformer", NAACL2021

## • 100개 언어에 걸쳐 수집된 텍스트 코퍼스

## • 각 언어로 학습한 모델과 fastText를 사용하여 필터링 수행

## CC-100

## • 앞서 언급한 C4와 마찬가지로 언어 판정 후 필터링한 101개 언어를 포함한 텍스트 코퍼스

## mC4

97

[42] Alexis Conneau et al. (2020), "Unsupervised Cross-lingual Representation Learning at Scale", ACL2020에서 인용

[43] Linting Xue et al. (2021), "mT5: A massively multilingual pre-trained text-to-text transformer", ACL2021에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

98

## The Pile | 다양한 소스를 포함한 영어 코퍼스

"The Pile: An 800GB Dataset of Diverse Text for Language Modeling", 2020

## • the Pile… 22개의 다양한 소스를 조합한 언어 모델링용 825.18GB 데이터셋

## 학습 데이터셋의 다양성을 높여 크로스 도메인 성능 기대

## • the Pile로 학습한 모델이 CC-100이나 Common Crawl로 학습한 모델 성능 상회

98

[44] Leo Gao et al. (2020), "The Pile: An 800GB Dataset of Diverse Text for Language Modeling"에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

99

[25] Luca Soldaini et al. (2023) "Dolma: An Open Corpus of 3 Trillion Tokens for Language Model Pretraining Research"에서 인용

## Dolma: 최대급 혼합 사전학습용 공개 데이터셋

"Dolma: An Open Corpus of 3 Trillion Tokens for Language Model Pretraining Research", 2023

## • Dolma…

웹 콘텐츠, 학술 출판물, 코드, 서적, 백과사전의 다양한 조합으로 구성된 5334GB(3T tokens) 공개 데이터셋

## • 과거 연구도 반영하여 데이터 처리 베스트 프랙티스(후술)를 따랐다고 언급

99

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

100

## Dolma의 텍스트 데이터 처리 프로세스(1)

"Dolma: An Open Corpus of 3 Trillion Tokens for Language Model Pretraining Research", 2023

1. fastText 언어 식별 모델을 사용해 영어일 가능성이 50% 이상인 문서 보존

2. 출처 URL 기반으로 중복 제거

3. 구두점으로 끝나지 않는 모든 단락 필터링

100

[25] Luca Soldaini et al. (2023) "Dolma: An Open Corpus of 3 Trillion Tokens for Language Model Pretraining Research"에서 인용, 일부 개변

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

101

## Dolma의 텍스트 데이터 처리 프로세스(2)

"Dolma: An Open Corpus of 3 Trillion Tokens for Language Model Pretraining Research", 2023

4. 유해하거나 음란할 가능성이 60% 이상으로 판정된 것 삭제

개인정보도 정규표현식으로 검출하여 마스크

5. 문서 내 중복 단락 삭제

6. 평가 셋에 포함된 13토큰 이상 단락을 학습 셋에서 제거

101

[25] Luca Soldaini et al. (2023) "Dolma: An Open Corpus of 3 Trillion Tokens for Language Model Pretraining Research"에서 인용, 일부 개변

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

102

## ■보충 | 사전학습용 데이터셋 전처리의 차이

"AI2 Dolma: 3 Trillion Token Open Corpus for Language Model Pretraining", 2023

102

[25] Luca Soldaini et al. (2023) "Dolma: An Open Corpus of 3 Trillion Tokens for Language Model Pretraining Research"에서 인용, 일부 개변

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

103

## FineWeb | 웹 데이터 특화의 더 큰 데이터셋

"The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale"

## • Llama 아키텍처의 소규모 모델 70개 이상 학습하여 진행한 어블레이션(ablation) 실험을 통한 경험적 베스트 프랙티스 발견

## • CommonCrawl에서 정제한 18.5T tokens로 구성된 데이터셋

## •

웹 정제에 특화함으로써 더 큰 데이터셋 구축 가능

（c.f. RefinedWeb(5T), RedPajama-v2(영불서독이 합계 30T)）

103

[40] Hugging Face (2024) The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale의 블로그에서 인용

[27] Guilherme Penedo et al.(2023), The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Data, and Web Data Only

[45] Weber, et. Al. (2024), RedPajama: an Open Dataset for Training Large Language Models

## 소규모 모델 실험에서 다른 공개 데이터셋보다 높은 학습 효율 실현

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

104

## FineWeb | 웹 데이터 특화의 더 큰 데이터셋

"The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale"

## •

파생 데이터셋

## •

FineWeb-edu

분류기를 사용한 FineWeb의 "교육적" 서브셋 1.3T tokens

## •

FineWeb 2

"FineWeb2: One Pipeline to Scale Them All — Adapting Pre-Training Data Processing to Every Language"

다국어판 FineWeb

일본어는 331Billion words 포함, 비교적 풍부

104

[40] Hugging Face (2024) The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale

[69] Hugging Face, EPFL (2025) FineWeb2: One Pipeline to Scale Them All — Adapting Pre-Training Data Processing to Every Language

그림은 FineWeb-edu의 HF 레포지토리에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

105

## 텍스트 토큰화

대표 기법: Byte Pair Encoding(BPE)

## •

텍스트를 서브워드(단어보다 세밀한 단위)로 분할

## •

토크나이저의 어휘 작성 방법은 우측 그림 참조.

## •

어휘 크기(기본 어휘 수 + 병합 수)는 하이퍼파라미터

## •

GPT, GPT-2, RoBERTa, BART, DeBERTa 등 다수 Transformer에서 사용

## •

이모지 등 처리

## •

코퍼스에 없는 문자를 사용하는 경우 그 문자는 <unk>로 변환

## •

따라서 많은 NLP 모델이 이모지로 콘텐츠를 분석하는 것을 서투름

## •

GPT-2와 RoBERTa의 토크나이저는 이에 대응하기 위해 byte 레벨에서 BPE 수행

예) 코퍼스가 다음 5개 단어로 이루어져 있다고 가정

'hug', 'pug', 'pun', 'bun', 'hugs'

1. 각 단어의 출현 횟수 카운트

('hug', 10), ('pug', 5), ('pun', 12), ('bun', 4), ('hugs', 5)

2. 단어를 문자로 분할

('h' 'u' 'g', 10), ('p' 'u' 'g', 5), ('p' 'u' 'n', 12), ('b' 'u' 'n', 4), ('h' 'u' 'g' 's', 5)

3. 가장 빈도가 높은 인접 쌍('u', 'g')을 ('ug')로 병합

('h' 'ug', 10), ('p' 'ug', 5), ('p' 'u' 'n', 12), ('b' 'u' 'n', 4), ('h' 'ug' 's', 5)

4. 원하는 어휘 수에 도달할 때까지 빈도가 높은 쌍의 병합 반복

('h' 'ug', 10), ('p' 'ug', 5), ('p' 'un', 12), ('b' 'un', 4), ('h' 'ug' 's', 5) …

[46] Hugging Face (2025), Hugging Face LLM Course의 Chapter6.5에서 예시 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

106

## BPE 이외의 서브워드 단위 토큰화

기타 토크나이저

## •

BPE와 달리 인접 쌍 2요소의 출현 빈도가 낮은 쌍(그 조합 이외에서는 거의 없는 쌍)을 우선적으로 병합

Score = 인접 쌍(a,b)의 출현 횟수 / (a의 출현 횟수 × b의 출현 횟수)

## •

예1: (un, ##able)

각 요소는 다른 단어에서도 빈출할 가능성이 큼(그대로 두고 싶음)

## •

예2: (hug, ##ging)

각 요소는 다른 곳에서 빈출하지 않으므로 병합 OK

## •

BERT, ELECTRA 등에서 사용

## WordPiece

## •

사전 단어 분할 불필요, 그대로 텍스트 분할

## •

어휘 집합에 공백을 추가하고 BPE나 Unigram 등 알고리즘으로 어휘 병합

## •

일본어 등 영어 이외의 다양한 언어에서도 쉽게 토크나이저 작성 가능, 서브워드 분할 알고리즘도 선택 가능

## •

T5, ALBERT 등에서 사용

## SentencePiece

106

[46] Hugging Face (2025), Hugging Face LLM Course의 Chapter6.6에서 예시 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

107

## ■보충 | ByT5: 토큰 프리(token-free) 언어 모델

"ByT5: Towards a token-free future with pre-trained byte-to-byte models", 2021

방법

텍스트열을 토큰으로 표현하지 않고 대신 문자 코드(UTF-8)로 읽은 바이트열로 표현

결과

서브워드로 토크나이즈하여 학습한 모델(mT5)에 필적하는 성능

107

[47] Linting Xue et al. (2022), "ByT5: Towards a token-free future with pre-trained byte-to-byte models" ACL2022에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

108

## 발전 주제

108

데이터 / 모델 / 학습 / 평가·분석

## •

Attention

## •

목적 함수

## •

평가

## •

분석

## •

주요 데이터셋

## •

데이터 처리(클렌징, 토큰화)

## •

주요 모델

## •

아키텍처 구성 요소

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

109

## Transformer 분류

Encoder-only / Encoder-Decoder

BERT, RoBERTa 등 / BART, T5 등

인식계(분류) / 텍스트 생성계

Decoder-only

GPT, Llama 등

텍스트 생성계

[6] Ashish Vaswani et al. (2017), "Attention Is All You Need", NeurIPS2017에서 인용, 일부 개변

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

110

## Transformer 분류

Encoder-only / Encoder-Decoder

BERT, RoBERTa 등 / BART, T5 등

인식계(분류) / 텍스트 생성계

Decoder-only

텍스트 생성계

[6] Ashish Vaswani et al. (2017), "Attention Is All You Need", NeurIPS2017에서 인용, 일부 개변

GPT, Llama 등

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

111

## BERT: 복수 태스크에서 SoTA 달성한 양방향 사전학습 모델

"BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding", NAACL2019

방법

## •

Transformer의 Encoder를 24층 쌓은 양방향 언어 모델

## •

사전학습에서 빈칸 채우기 태스크와 다음 문장 예측 태스크를 학습하고, 목적 태스크의 데이터셋으로 파인튜닝하여 성능 발휘

결과

## •

11개 NLP 태스크에서 SoTA

[CLS] my dog is cute [SEP] he likes [MASK] ##ng [SEP]

IsNext my dog is cute [SEP] he likes play ##ng [SEP]

빈칸 채우기(MLM) / 다음 문장 예측(NSP)

111

[48] Jacob Devlin et al. (2019), "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding", ACL2019에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

112

## RoBERTa: BERT를 개량하여 성능 향상

"RoBERTa: A Robustly Optimized BERT Pretraining Approach", 2019

방법

## •

BERT와 동일한 아키텍처에서 일부 요소 변경

– 데이터셋 크기 13GB→160GB

– 배치 크기 256→8K

– NSP 미사용

– 마스크를 동적으로 적용

결과

## •

GLUE와 SQuAD에서 BERT 상회 성능

112

[49] Yinhan Liu et al. (2019), "RoBERTa: A Robustly Optimized BERT Pretraining Approach"에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

113

## ALBERT: 파라미터 공유로 학습 고속화

"ALBERT: A Lite BERT for Self-supervised Learning of Language Representations", ICLR2020

방법

## •

층 간 파라미터 공유로 BERT-large와 동일한 아키텍처 대비 파라미터가 18배 감소, 1.7배 빠른 학습 가능

결과

## •

ALBERT-xxlarge에서 BERT-large보다 적은 파라미터 수임에도 GLUE, SQuAD에서 SoTA

113

[50] Zhenzhong Lan et al. (2020), "ALBERT: A Lite BERT for Self-supervised Learning of Language Representations" ICLR2020에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

114

## Transformer 분류

Encoder-only / Encoder-Decoder

BERT, RoBERTa 등 / BART, T5 등

인식계(분류) / 텍스트 생성계

Decoder-only

텍스트 생성계

[6] Ashish Vaswani et al. (2017), "Attention Is All You Need", NeurIPS2017에서 인용, 일부 개변

GPT, Llama 등

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

115

## BART: 양방향 인코더와 자기회귀형 디코더의 조합

"BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension", 2019

방법

## •

BERT 같은 양방향 인코더와 GPT 같은 자기회귀형 디코더를 결합한 모델

## •

무작위로 입력 문서 일부를 훼손시키고 그 재구성을 수행하는 복수 태스크 조합으로 사전학습

결과

## •

CNN/DailyMail, XSum 등 태스크에서 SoTA

115

[51] Mike Lewis et al. (2020), "BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension"에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

116

## T5: 모든 태스크를 Text-to-Text로 취급하는 EncDec 모델

"Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer", 2019

방법

## •

다수의 자연어 처리 태스크를 Text-to-Text 형태로 변환하여 통일된 프레임워크로 학습

## •

사전학습에서는 입력 문서 일부를 무작위로 특수 토큰으로 치환하고, 치환 전 토큰을 예측하는 태스크로 학습

결과

## •

GLUE, SuperGLUE 등 태스크에서 SoTA

116

[41] Colin Raffel et al. (2020), "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer"에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

117

## Transformer 분류

Encoder-only / Encoder-Decoder

BERT, RoBERTa 등 / BART, T5 등

인식계(분류) / 텍스트 생성계

Decoder-only

텍스트 생성계

[6] Ashish Vaswani et al. (2017), "Attention Is All You Need", NeurIPS2017에서 인용, 일부 개변

GPT, Llama 등

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

118

## GPT-3: 더 스케일시킨 Dec-only 모델

## • "Language Models are Few-Shot Learners", 2020

방법

## •

GPT-2의 약 120배 파라미터 수를 가진 모델을 약 14배 데이터로 학습

## •

태스크 관련 설명이나 소수 샷 예시를 입력에 추가하여 태스크를 풀 수 있게 되는 문맥 내 학습(In-context Learning) 가능

결과

## •

소수 샷 설정에서 기존 SoTA에 필적, 혹은 상회하는 성능 확인

## •

성능이 너무 뛰어나 모델 공개 없이 API 공개에 그침

118

[24] Tom Brown et al. (2020), "Language Models are Few-Shot Learners", NeurIPS2020에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

119

## ■보충 | 최근 공개되는 모델은 Dec-only 모델이 많다

"A Survey of Large Language Models", 2023

119

[26] Wayne Xin Zhao et al. (2023), "A Survey of Large Language Models"에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

120

## 정규화 위치에 대하여

"A Survey of Large Language Models", 2023

Post Norm / Pre Norm / Sandwich Norm

## •

원래 Transformer와 마찬가지로 잔차 연결 후 정규화 배치

## •

출력층 부근에서 기울기가 커져 학습이 불안정해지는 경향

## •

각 서브층 앞과 최종 예측 앞에 정규화 배치

## •

성능은 낮아지지만 학습 안정성으로 인해 자주 채택

## •

특히 잔차 연결 전에 추가 정규화 배치

## •

학습이 붕괴하는 경우도 존재

수식 표현 / 상세

120

[26] Wayne Xin Zhao et al. (2023), "A Survey of Large Language Models"를 참고

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

121

## 위치 표현에 대하여

"보다 나은 Transformer 만들기", 2022 참고로 작성

절대 위치 표현 / 상대 위치 표현

각 토큰의 절대적 위치를 나타내는 어떤 표현(e.g. sin파/cos파)을 입력 표현에 더함

토큰 간 상대적 거리를 Attention 계산 시 활용

## •

입력 내용과 독립적인 표현이므로 계산 속도가 빠름

## •

알려지지 않은 길이의 시열 입력에 취약

## •

토큰 간 상대적 위치를 사용하여 미지의 시열 길이에도 견고성이 높음

## •

입력에 고유한 값을 취하여 추가 계산 필요

개요 / 상세

121

[52] 清野舜(2022), 보다 나은 Transformer 만들기 - Speaker Deck를 참고

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

122

## ALiBi: 거리에 선형인 바이어스를 통합한 상대 위치 임베딩

"Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation", ICLR2022

방법

## •

Attention 스코어 계산 시 Key와 Query의 상대적 거리에 대해 선형인 패널티를 가산

## •

가까운 토큰 간보다 먼 토큰 간이 Attention 스코어가 더 저하

결과

## •

절대 위치 표현보다 성능이 좋음

## •

외삽(extrapolation) 성능도 우수

122

[53] Ofir Press et al. (2021), "Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation"에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

123

## 최근 LLM 모델 구조

## • 최근 모델은 Attention/Feed Forward/Normalization이 개량되고 있다.

## •

Positional Embedding

## •

RoPE

## •

Attention

## •

Grouped Query Attention

## •

Sliding Window Attention

## •

Multi-head Latent Attention

## •

Feed Forward

## •

SwiGLU

## •

Mixture of Experts

## •

Others

## •

RMSNorm

## • 최신 모델 아키텍처 해설은 다음 참조

## The Big LLM Architecture Comparison [70]

## https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

124

## 발전 주제

데이터 / 모델 / 학습 / 평가·분석

## •

주요 모델

## •

아키텍처 구성 요소

## •

평가

## •

분석

## •

주요 데이터셋

## •

데이터 처리(클렌징, 토큰화)

## •

Attention

## •

목적 함수

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

125

## Sparse Attention: 계산 위치를 한정하여 효율적으로 Attention 계산

"Big Bird: Transformers for Longer Sequences", NeurIPS 2020

문제의식

종래 Attention에서는 시열 길이에 대해 제곱의 계산 복잡성 소요

방법

모든 토큰에 대해 Attention을 계산하는 대신, 국부적으로 설정한 토큰으로 학습하여 계산량 절감

유사 아이디어: [Iz Beltagy et al. 2020] "Longformer: The Long-Document Transformer" [55]

125

[54] Manzil Zaheer et al. (2020), "Big Bird: Transformers for Longer Sequences" NeurIPS2020에서 인용(도)

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

126

## Grouped-Query Attention: Key와 Value를 여러 헤드에서 공유

"GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints", 2023

문제의식

Multi-head Attention에서는 디코딩 시 모든 Key와 Value를 읽어올 필요가 있어 추론 속도의 병목

방법

Key와 Value를 일부(Group-query) 또는 하나(Multi-query)의 헤드에서 공유하여 메모리 부하를 줄이고 추론 속도 향상

Llama3 등에서 채택

126

[56] Joshua Ainslie et al. (2023), "GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints"에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

127

## UniLM: Attention 마스크 위치를 변경하여 복합적 목적 함수 설정

"Unified Language Model Pre-training for Natural Language Understanding and Generation", NeurIPS2019

방법

## •

Attention 마스크 영역을 변화시켜 양방향 언어 모델링, 단방향 언어 모델링, 배열 간 언어 모델링을 결합한 복합적 목적 함수로 사전학습

결과

## •

GLUE 같은 식별 태스크에서 BERT에 필적하는 성능을 보이면서 CNN/DM 같은 언어 생성 태스크에서 SoTA

127

[57] Li Dong et al. (2019), "Unified Language Model Pre-training for Natural Language Understanding and Generation" NeurIPS2019에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

128

## UL2: 복수 태스크를 설정한 통일적 목적 함수로 사전학습

"UL2: Unifying Language Learning Paradigms", 2022

방법

## •

T5 같은 결손 토큰 예측(R-Denoising, X-Denoising)과 GPT 같은 연속 토큰 예측을 결합한 MoD(Mixture-of-Denoisers)라 불리는 통일적 목적 함수로 학습

## •

MoD를 지속적 사전학습에 사용하는 UL2R(UL2 Repair)라는 훈련 방법도 후에 제안

결과

## •

EncDec과 Dec 양쪽 아키텍처에서 균형 있게 성능 향상 확인

128

[58] Yi Tay et al. (2022), "UL2: Unifying Language Learning Paradigms"에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

129

## 발전 주제

데이터 / 모델 / 평가·분석 / 학습

## •

주요 모델

## •

아키텍처 구성 요소

## •

Attention

## •

목적 함수

## •

주요 데이터셋

## •

데이터 처리(클렌징, 토큰화)

## •

평가

## •

분석

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

130

## 평가 대상의 확장

주요 데이터셋

자연어 이해 / 도메인 지식 / 윤리성·신뢰성 / 도구 활용

평가 대상

## •

입력 시열의 이해를 수행하는 태스크

## •

종래 주요 평가 대상

## •

수학이나 과학, 의학 등 답안에 전문 지식이 필요한 태스크

## •

사회적 편향을 포함하지 않는지, 어떤 특성을 가지는지 검증하는 태스크

## •

외부 API 등을 활용해 답안을 작성할 수 있는지 검증하는 태스크

개요

GLUE, SuperGLUE / SQuAD, MMLU / MATH, MultiMedQA, APPS, CUAD / FLASK, TrustGPT, TruthfulQA / ToolBench

130

[26] Wayne Xin Zhao et al. (2023), "A Survey of Large Language Models"에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

131

## FLASK: 언어 모델의 종합적 성능 평가 벤치마크

"FLASK: Fine-grained Language Model Evaluation based on Alignment Skill Sets", 2023

## • LLM에 필요한 스킬을 정의하고, 모델의 행동에 대해 인간 또는 모델이 스코어링을 수행하는 벤치마크

## • 주로 4가지 능력(논리적 사고, 배경 지식, 문제 해결 능력, 지시 추종성)으로 구성된 평가 프레임워크를 구축하고, 이를 12개의 상세한 스킬 항목으로 세분화

131

[60] Seonghyeon Ye et al. (2023), "FLASK: Fine-grained Language Model Evaluation based on Alignment Skill Sets"에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

132

## Attention에 의한 가시화 분석

"Attention in Natural Language Processing", 2019

## •

Attention의 대소는 자주 가시화되며, 이를 Attention map이라 부른다. 위 그림에서 하이라이트된 것은 Attention 스코어가 높은 단어이다.

## •

겉보기에는 Attention이 단어의 중요도를 나타내는 것처럼 보이지만, Attention에는 설명 능력이 없다는 입장의 논문도 복수 존재

132

[61] Andrea Galassi et al. (2019), "Attention in Natural Language Processing"에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

133

## Attention Rollout / Flow: Attention map에서 입력으로의 기여 계산

"Quantifying Attention Flow in Transformers", ACL2020

## • 종래 Attention에서는 복수 층을 경유하여 정보가 오가므로, Attention map 그 자체를 각 상태의 입력에 대한 기여로 해석하기에는 신뢰성 부족

## • Attention Rollout에서는 자신보다 앞에 있는 층의 Attention map을 순차적으로 곱함

## • Attention Flow에서는 각 층의 Attention을 플로우 네트워크로 해석하여 입력 토큰에 대한 어텐션 근사

133

[62] Samira Abnar & Willem Zuidema (2020), "Quantifying Attention Flow in Transformers" ACL2020에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

134

## ■보충 | 임의의 태스크에서 반드시 Attention을 사용해야 하는 것은 아니다

"Are Pre-trained Convolutions Better than Pre-trained Transformers?", ACL2021

## •

현재 사전학습과 Transformer는 스탠다드가 되었지만, 이것은 세트로 의미가 있는 것인가?

## •

CNN에서도 사전학습 효과 있음

## •

일부 태스크에서 CNN 모델이 T5를 상회하는 성능 발휘

## •

CNN이 항상 Transformer의 대체가 되는 것은 아니지만, 사전학습이라는 패러다임 전환과 아키텍처의 변천은 분리해 생각해야 한다고 주장

134

[63] Yi Tay et al. (2021), "Are Pre-trained Convolutions Better than Pre-trained Transformers?" ACL2021에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

135

## ■보충 | Convolution과 Self Attention의 관계

"On the Relationship between Self-Attention and Convolutional Layers", ICLR2020

Filter: 파라미터(정적) / 범위: 국부

Filter: 입력 의존(동적) / 범위: 전역

※단, 상대 위치 표현을 사용하면 Multi-Head Self-Attention은 Conv를 내포

135

[64] Jean-Baptiste et al. (2020), "On the Relationship between Self-Attention and Convolutional Layers" ICLR2020에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

136

## 적대적 공격, 적대적 방어: 언어 모델의 약점에 관한 분석 방법

"What are adversarial examples in NLP?", 2020

문제의식

인간에게는 사소한 영향만 주는 섭동(perturbation)이라도 신경망은 크게 영향을 받는 경우가 존재

방법

입력의 일부를 편집한 결과 모델 성능을 열화시키는 공격을 검증함과 함께, 그 공격에 의한 실패를 막는 방어 방법을 검토

## ■극성 분석에서의 적대적 공격 예

136

[65] Jack Morris (2020), "What are adversarial examples in NLP?"에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

137

## 프로빙(probing): 언어 모델이 내부적으로 획득하는 능력 분석 방법

품사 분류 능력에 대한 프로빙 예

문제의식

언어 모델의 태스크 성능은 출력으로 평가할 수 있지만, 언어 모델이 내부적으로 획득한 능력은 출력만으로는 쉽게 평가 불가

방법

어떤 입력을 주었을 때 언어 모델에서 얻어지는 임베딩 표현에서 특정 태스크(좌도에서는 품사 분류)를 수행하는 분류기(프로브)를 훈련했을 때의 태스크 성공률로부터 임베딩 표현에 그 태스크를 나타내는 표현이 인코딩되어 있는지 검증

최근에는 모델의 임베딩 표현에 개입을 수행해 출력으로의 인과관계를 조사하는 경우도 많음

언어 모델

입력: I am travelling the world

임베딩 표현

분류기(프로브)

품사 태그: NN(명사)

훈련

137

[66] Yonatan Belinkov (2022), "Probing Classifiers: Promises, Shortcomings, and Advances" ACL2022를 참고

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

138

## 오늘의 정리

## 대규모 언어 모델(LLM)의 사전학습을 소개

1. 언어 모델에서 Transformer의 위치

## • Transformer는 신경망 언어 모델의 하나로 취급

## • RNN형 언어 모델이 안고 있던 과제를 해결

3. LLM의 사전학습

## • 대규모 코퍼스로 학습을 수행함으로써 모델의 범용성을 높이고 있다.

## • Next Token Prediction이라는 자기 지도 학습으로 최적화

2. LLM에서 주류가 된 Transformer 모델 구조

## • Self-Attention 메커니즘을 가진 모델 구조이며 1스텝으로 전 단어 정보와 연결 가능

## • 과제① 해결: 단어 간 장거리 의존성을 파악할 수 있게 되었다.

## • 과제② 해결: 오차 역전파 계산 스텝이 문장 길이에 비의존하게 되어 학습 안정·고속화

4. 발전 주제

## • 데이터, 모델, 학습, 평가 분석에 대한 발전적 주제 해설

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

## 보충 자료

139

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

140

## 모델별 학습 방법의 차이

"A Survey of Large Language Models", 2023

140

[26] Wayne Xin Zhao et al. (2023), "A Survey of Large Language Models"에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

141

## 모델별 세부 요소의 차이

"A Survey of Large Language Models", 2023

141

[26] Wayne Xin Zhao et al. (2023), "A Survey of Large Language Models"에서 인용

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

142

## Accessibility of Models

API 전용 / 공개 & 거대 / 비공개

142

[67] Percy Liang (2022), "Holistic Evaluation of Language Models"에서 인용, 일부 개변

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

143

## Reference

[1]

岡崎直観(2023), 대규모 언어 모델의 경이와 위협 - Speaker Deck 접속일: 2025/10/1

[2]

Ilya Sutskever et al. (2014), "sequence to sequence learning with neural networks", NeurIPS2014

[3]

Tomáš Mikolov, et al. (2010), "recurrent neural network based language model", Proc. Interspeech 2010, 1045-1048

[4]

Dzmitry Bahdanau et al. (2014), "Neural machine translation by jointly learning to align and translate", arXiv:1409.0473

[5]

Masaki Hayashi (2022), Transformer와 seq2seq with attention의 차이는? 시열 변환 모델【Q and A 기사】| CVML 전문가 가이드 접속일: 2025/10/1

[6]

Ashish Vaswani et al. (2017), "Attention Is All You Need", NeurIPS2017

[7]

OpenAI (2023) "GPT-4 Technical Report", arXiv:2303.08774

[8]

OpenAI (2025), "GPT-5 System Card" 접속일: 2025/10/1

[9]

OpenAI (2025), "GPT-5가 등장" 접속일: 2025/10/1

[10]

Google (2025), "Gemini 2.5 tech report" 접속일: 2025/10/1

[11]

OpenAI (2024), "Learning to Reason with LLMs"

[12]

Allen Institute for AI, Univ. of Washington, NYU (2025), "2 OLMo 2 Furious", arXiv: 2501.00656

[13]

OpenAI (2025), "gpt-oss-120b & gpt-oss-20b Model Card ", arXiv: 2508.10925

[14]

Qwen (2025), "Qwen3 Technical Report" , arXiv: 2505.09388

[15]

Shraddha Anala (2020), "A Guide to Word Embedding. What are they? How are they more useful… | by Shraddha Anala | Towards Data Science"

접속일: 2025/10/1

[16]

John Hewitt, Natural Language Processing with Deep Learning CS224N/Ling284 접속일: 2025/10/1

[17]

Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium,

https://medium.com/data-science/illustrated-self-attention-2d627e33b20a 접속일: 2025/9/3

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

144

## Reference

[18]

Jay Alammar (2018) The Illustrated Transformer – Jay Alammar – Visualizing machine learning one concept at a time.

https://jalammar.github.io/illustrated-transformer/ 접속일: 2023/11/19

[19]

Mor Geva et al. (2021), "Transformer Feed-Forward Layers Are Key-Value Memories", Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, pages 5484–5495

[20]

Kaiming He et al. (2016), "Deep Residual Learning for Image Recognition", 2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR) pages 770-778

[21]

Jimmy Lei Ba et al. (2016), "Layer Normalization", arXiv:1607.06450

[22]

Rishi Bommasani et al. (2021), "On the Opportunities and Risks of Foundation Models", arXiv:2108.07258

[23]

Hugo Touvron et al. (2023), "LLaMA: Open and Efficient Foundation Language Models", arXiv:2302.13971

[24]

Tom Brown et al. (2020), "Language Models are Few-Shot Learners", NeurIPS2020 (도 중 figure는 arXiv판에서 인용)

[25]

Luca Soldaini (2023), AI2 Dolma: 3 Trillion Token Open Corpus for LLMs | AI2 Blog, https://blog.allenai.org/dolma-3-trillion-tokens-open-llm-corpus-9a0ff4b8da64

접속일: 2023/11/19

[26]

Wayne Xin Zhao et al. (2023), "A Survey of Large Language Models", arXiv:2303.18223

[27]

Guilherme Penedo et al.(2023), "The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Data, and Web Data Only" arXiv: 2306.01116

[28]

Hugo Touvron et al. (2023), "Llama 2: Open Foundation and Fine-Tuned Chat Models" arXiv:2307.09288

[29]

Fuzhao Xue et al. (2023), "To Repeat or Not To Repeat: Insights from Scaling LLM under Token-Crisis", arXiv:2305.13230

[30]

Niklas Muennighoff et al. (2023), "Scaling Data-Constrained Language Models", arXiv:2305.16264

[31]

Stas Bekman (2022) The Technology Behind BLOOM Training https://huggingface.co/blog/bloom-megatron-deepspeed 접속일: 2023/11/19

[32]

suchenxang (2023), metaseq/projects/OPT/chronicles/OPT175B_Logbook.pdf at main · facebookresearch/metaseq · GitHub,

https://github.com/facebookresearch/metaseq/blob/main/projects/OPT/chronicles/OPT175B_Logbook.pdf 접속일: 2023/11/19

[33]

Diederik P. Kingma & Jimmy Ba, (2014), "Adam: A Method for Stochastic Optimization", arXiv:1412.6980

[34]

Ilya Loshchilov & Frank Hutter, (2017), "Decoupled Weight Decay Regularization", arXiv:1711.05101

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

145

## Reference

[35]

Shikoan's ML Blog (2021), Cosine Decay와 Warmup을 동시에 수행하는 스케줄러(timm) | Shikoan's ML Blog, https://blog.shikoan.com/?s=Cosine

접속일: 2023/11/19

[36]

Chip Huyen (2019) Evaluation Metrics for Language Modeling, https://thegradient.pub/understanding-evaluation-metrics-for-language-models/

접속일: 2023/11/19

[37]

Kaito Sugimoto (2021) 텍스트 생성에서의 decoding 테크닉: Greedy search, Beam search, Top-K, Top-p https://zenn.dev/hellorusk/articles/1c0bef15057b1d

접속일: 2023/11/19

[38]

mm_0824 (2020) 빔서치(Beam Search) 이해하기 | 즐기며 이해하는 AI·머신러닝 입문 https://data-analytics.fun/2020/12/16/understanding-beamsearch/

접속일: 2023/11/19

[39]

cohere, Temperature, https://docs.cohere.com/docs/temperature, 접속일: 2023/12/1

[40]

Hugging Face (2024) "The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale", arXiv:2406.17557

[41]

Colin Raffel et al. (2020), "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer",

The Journal of Machine Learning Research, Volume 21, Issue 1, Article No.: 140, pp 5485–5551

[42]

Alexis Conneau et al. (2020), "Unsupervised Cross-lingual Representation Learning at Scale",

Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics, pages 8440–8451

[43]

Linting Xue et al. (2021), "mT5: A massively multilingual pre-trained text-to-text transformer",

Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, pages 483–498

[44]

Leo Gao et al. (2020), "The Pile: An 800GB Dataset of Diverse Text for Language Modeling", arXiv:2101.00027

[45]

Weber, et. Al. (2024), "RedPajama: an Open Dataset for Training Large Language Models", NeurIPS2024

[46]

Hugging Face (2025) Hugging Face LLM Course 접속일: 2025/10/1

[47]

Linting Xue et al. (2022), "ByT5: Towards a token-free future with pre-trained byte-to-byte models"

Transactions of the Association for Computational Linguistics, vol. 10, pp. 291–306

[48]

Jacob Devlin et al. (2019), "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding", Proceedings of NAACL-HLT 2019, pages 4171–4186

[49]

Yinhan Liu et al. (2019), "RoBERTa: A Robustly Optimized BERT Pretraining Approach", arXiv:1907.11692

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

146

## Reference

[50]

Zhenzhong Lan et al. (2020), "ALBERT: A Lite BERT for Self-supervised Learning of Language Representations" ICLR2020

[51]

Mike Lewis et al. (2020), "BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension" Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics, pages 7871–7880

[52]

清野舜(2022), 보다 나은 Transformer 만들기 - Speaker Deck https://speakerdeck.com/butsugiri/yoriliang-itransformerwotukuru 접속일: 2023/11/19

[53]

Ofir Press et al. (2021), "Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation" arXiv:2108.12409

[54]

Manzil Zaheer et al. (2020), "Big Bird: Transformers for Longer Sequences" NeurIPS2020

[55]

Iz Beltagy et al. (2020), "Longformer: The Long-Document Transformer", arXiv:2004.05150

[56]

Joshua Ainslie et al. (2023), "GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints" arXiv:2305.13245

[57]

Li Dong et al. (2019), "Unified Language Model Pre-training for Natural Language Understanding and Generation" NeurIPS2019

[58]

Yi Tay et al. (2022), "UL2: Unifying Language Learning Paradigms" arXiv:2205.05131

[59]

Yupeng Chang et al. (2023), "A Survey on Evaluation of Large Language Models" arXiv:2307.03109

[60]

Seonghyeon Ye et al. (2023), "FLASK: Fine-grained Language Model Evaluation based on Alignment Skill Sets" arXiv:2307.10928

[61]

Andrea Galassi et al. (2019), "Attention in Natural Language Processing" arXiv:1902.02181

[62]

Samira Abnar & Willem Zuidema (2020), "Quantifying Attention Flow in Transformers" Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics, pages 4190–4197

[63]

Yi Tay et al. (2021), "Are Pre-trained Convolutions Better than Pre-trained Transformers?" Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing, pages 4349–4359

[64]

Jean-Baptiste et al. (2020), "On the Relationship between Self-Attention and Convolutional Layers" ICLR2020

[65]

Jack Morris (2020), "What are adversarial examples in NLP?", https://towardsdatascience.com/what-are-adversarial-examples-in-nlp-f928c574478e

접속일: 2023/11/19

[66]

Yonatan Belinkov (2022), "Probing Classifiers: Promises, Shortcomings, and Advances" Computational Linguistics, Volume 48, Issue 1 - March 2022 pages 207-119

[67]

Percy Liang (2022), "Holistic Evaluation of Language Models" arXiv:2211.09110

[68]

Harshit Sharma (2022), "Softmax Temperature"

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

147

## Reference

[69]

Hugging Face, EPFL (2025) FineWeb2: One Pipeline to Scale Them All — Adapting Pre-Training Data Processing to Every Language, COLM2025

[70]

The Big LLM Architecture Comparison https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison

접속일: 2025/10/1

©MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 대규모 언어 모델 강좌 강의 자료 © 2025 by 도쿄대학교 마츠오·이와사와 연구실은 CC BY-NC-ND 4.0 라이선스에 따라 제공됩니다.

