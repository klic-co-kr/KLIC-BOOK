# Day 3: 사전학습 (Pre-training)

> 본 자료는 도쿄대학교 마츠오·이와사와 연구실이 작성한 2025년 LLM 대규모 언어 모델 강좌 기초편(10~11월 개최) 강의 자료를 재구성한 것이다. 강사는 우치야마 후미야(内山史也). 원자료는 크리에이티브 커먼즈 CC BY-NC-ND 4.0(저작자표시-비영리-변경금지 4.0 국제) 라이선스로 제공된다. 재이용 시 라이선스 표기를 반드시 기재하고, 참조 논문은 본 말미의 참고문헌에서 인용처를 게재할 것. 영리 목적 재이용은 별도 문의가 필요하다.

## 1. 사전학습과 언어 모델

### 강의의 목적과 구성

이 장에서는 대규모 언어 모델(LLM)의 주류 모델 구조인 Transformer와 그 사전학습 메커니즘을 이해하는 것을 목적으로 한다. 구체적 목표는 세 가지다. (1) 언어 모델에서 Transformer의 위치를 설명할 수 있다. (2) LLM에서 주류가 된 Transformer의 모델 구조를 설명할 수 있다. (3) LLM의 사전학습 파이프라인을 설명할 수 있다. 실습에서는 PyTorch를 활용해 Transformer를 직접 구현하고 학습한다.

LLM의 학습은 세 단계로 구성된다. Step 1 사전학습은 대규모 코퍼스를 통한 자기 지도 학습으로 모델에 어휘·문법·기본 지식 등 기초적인 언어 이해를 획득시키는 단계이며, 본 장(Day 3)의 주제다. Step 2 파인튜닝은 레이블이 있는 데이터를 통한 지도 학습으로 사전학습된 모델의 성능을 개선하거나 특정 태스크나 도메인에 적응시킨다(Day 6). Step 3 강화 학습은 인간 피드백을 활용해 모델의 출력이 인간의 가치관에 부합하도록 조정한다(Day 7).

### 언어 모델이란

언어 모델(Language Model)이란 단어 시퀀스(≈문장)의 발생 확률 $p(x_1, x_2, \cdots, x_L)$를 모델화한 것이다. 이 확률을 연쇄법칙으로 분해한 형태를 자기회귀 언어 모델(autoregressive language model)이라 한다.

$$p(x_1, x_2, \cdots, x_L) = P(x_1)\, p(x_2|x_1)\, \cdots\, p(x_L|x_1, \cdots, x_{L-1})$$

조건부 확률을 알면 텍스트 생성이 가능해진다. 예컨대 "日本 の 首都 は"라는 문맥이 주어졌을 때 $p(東京|\text{日本, の, 首都, は}) = 0.2$, $p(パリ|\cdots) = 0.001$, $p(カイロ|\cdots) = 0.0005$와 같이 단어별 확률을 계산할 수 있으며, 다음 단어 $x_L$의 적절한 예측은 $\arg\max\, p(x_L|x_1, \cdots, x_{L-1})$로 얻는다. Day 1에서 복습한 "日本の首都は → 東京"도 $\arg\max\, p(x|\text{日本, の, 首都, は})$에 해당한다. 이 조건부 확률을 신경망으로 표현한 것이 신경망 언어 모델이다.

### 딥러닝 이전의 언어 모델

딥러닝 이전에는 조건부 확률을 통계적으로 구했다. 대규모 코퍼스 내 단어열 출현 빈도로부터 확률을 산정하며, 단어열 $s$의 출현 횟수를 $\#(s)$라 하면 $p(東京|\text{日本, の, 首都, は}) = \#(\text{日本, の, 首都, は, 東京}) / \#(\text{日本, の, 首都, は})$로 추정한다 [1]. 이 접근에는 두 가지 과제가 있다. 첫째, 데이터 희소성(data sparseness) 문제로 단어열이 길어지면 출현 횟수가 급격히 감소해 조건부 확률 추정이 어려워진다. 둘째, 유의어가 개별 사건으로 취급되어 "日本の首都は?"과 "日本国の首都は?"처럼 미세한 표현 차이만으로 출현 빈도가 다른 단어로 취급된다.

이를 보완하기 위해 직전 $N-1$개의 단어만으로 다음 단어를 예측하는 N-gram 언어 모델이 사용되었다. 3-gram 예로 $p(東京|\text{日本, の, 首都, は}) \approx p(東京|\text{首都, は})$이며, 데이터 희소성 문제를 어느 정도 회피할 수 있다. 그러나 직전 2단어 "首都 は"만으로는 "東京"을 특정하기 어렵듯 장거리 단어 간 관계를 파악하기 어렵다는 과제가 남으며, 이는 후술하는 Transformer로 해결된다 [1].

### 신경망 언어 모델과 RNN의 과제

신경망 언어 모델은 조건부 확률을 어떤 신경망으로 추정한 모델이며, 다른 기계학습과 마찬가지로 가능도(likelihood)를 최대화하도록 오차 역전파로 훈련한다. 신경망 언어 모델은 특히 기계 번역 분야에서 크게 발전했으며, 입력 문장(번역 원 언어)을 받는 인코더와 출력 문장(번역 대상 언어)을 출력·재귀 입력하는 디코더로 구성된다 [2].

대표적인 RNN형 언어 모델인 Seq2Seq [3]는 순환 신경망(RNN: Recurrent Neural Network)으로, 첫 단어부터 한 단어씩 입력해 뉴런을 순차적으로 갱신하며 파라미터를 재사용한다. 원리적으로는 임의 개수의 단어를 입력·출력할 수 있으나 두 가지 과제가 있었다. 첫째, 뉴런이 고정 길이이므로 장문이 되면 모든 정보를 기억할 수 없어 단어 간 장거리 의존성 파악이 곤란하다. 둘째, 네트워크가 단어 방향으로 깊어져 학습이 불안정(기울기 소실·기울기 폭발)하고 속도가 느리다.

Transformer [4][5]는 어텐션(attention) 메커니즘을 최대한 활용해 이 두 과제를 해결한다. 단어 간 장거리 의존성을 파악할 수 있게 되었고, 오차 역전파 스텝 수가 단어 수에 의존하지 않게 짧아져 학습의 안정화와 고속화를 실현했다. 어텐션을 RNN에 도입한 선행연구 [4]는 있었으나 전 단어 간에는 아니었으며, Transformer가 전 단어 간에 어텐션을 도입하고 멀티헤드 어텐션(multi-head attention)을 새롭게 채택한 점이 차별적이다.

## 2. Transformer의 모델 구조

### Transformer가 주류가 된 배경

Transformer는 2017년 "Attention Is All You Need" [6]에서 최초로 발표된 이래, 어텐션 메커니즘 채용으로 단어(토큰)의 장거리 의존 관계를 효율적으로 학습하며, 학습 시 병렬 계산도 효율화되어 분산 학습을 통한 대규모화가 쉬워졌다. 발표 이후 모델 개량과 스케일링을 통해 다수의 벤치마크에서 당시 최고 성능(SOTA)을 지속적으로 달성했다.

GPT-1~4, gpt-oss, Gemini 2.5 등은 모두 Transformer를 채택한다. GPT-4는 상세 구조가 비공개이나 Technical Report에서 Transformer 기반임을 명시하고 있으며 [7], GPT-5의 아키텍처는 불명이지만 system card에 LLM으로 기재되어 있다 [8][9]. 평가 사례로 GPT-5는 AIME 2025(미국 고교생 수학 경진대회)에서 도구 없이 94.6%, 의료 분야 HealthBench Hard 46.2%를 기록했고, Gemini 2.5는 AIME 2025에서 88.0%, 최적화된 프레임워크로 포켓몬스터 블루를 406.5시간에 클리어했다 [10].

### 블록 구조와 Encoder/Decoder

Transformer의 최소 단위는 "블록(block)"이며, 좌측 Encoder 블록을 세로로 N층, 우측 Decoder 블록도 세로로 N층 배열하여 구성된다 [6]. 토큰 수만큼 블록이 가로로 늘어나고 어텐션 메커니즘에 의해 가로 블록끼리 정보가 전달된다. 다만 실제로는 Encoder가 없어도 Decoder만으로 텍스트 생성이 가능하며(출력과 재귀 입력이 있으므로), GPT 시리즈가 이 형식을 취한다. Transformer가 최초 제안된 분야가 기계 번역이었기에 선행연구의 Encoder-Decoder 형식을 따라 제안되었을 뿐이다.

Transformer의 구성 요소는 크게 Embedding, Multi-Head Attention, Feed Forward, Others(Add & Norm, 출력층)로 나뉜다.

### Embedding: 단어의 벡터 변환

텍스트를 Transformer 블록에 가져오는 첫 단계는 Embedding이다. "春は曙"라는 텍스트는 토크나이저(후술)에 의해 "春", "は", "曙"와 같은 토큰으로 분할되고, 각 토큰은 일대일로 할당된 토큰 ID(예: 1050, 80, 24567)로 변환된다. 이를 다시 {토큰 ID}번째만 1이고 나머지는 0인 one-hot 벡터로 구성한 뒤, MLP에 의한 저차원 변환(학습 대상)을 거쳐 Word Embedding이라는 단어의 분산 표현을 얻는다. 이는 색을 RGB의 3차원 벡터로 변환하는 것과 비슷하다 [15].

Word Embedding(WE)은 단어라는 sparse한 정보를 dense한 표현으로 변환하여 Transformer 등 모델의 입력값으로 취급 가능하게 한다. 학습 완료 후의 Word Embedding에는 단어 간 의미의 유사성이나 관계성이 내장된다.

Transformer 블록의 알고리즘은 토큰의 위치 정보에 의존하지 않으므로, 블록에 가져오기 전에 Positional Encoding(PE)으로 위치 정보를 추가해야 한다. 토큰 위치에 따라 다른 PE를 각 WE에 더하며, 예컨대 WE("春") + PE("이것은 1번째 토큰입니다"), WE("は") + PE("이것은 2번째 토큰입니다"), WE("曙") + PE("이것은 3번째 토큰입니다")와 같다 [16].

### Multi-Head Attention

Attention은 모든 토큰 간의 유사도를 측정함으로써 장거리 토큰 간의 의존 관계를 파악할 수 있게 한 메커니즘이다. 핵심 수식은 다음과 같다 [6].

$$\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right) V$$

"春 は 曙" 세 토큰의 예로 단계를 보면 [17]. 우선 각 토큰의 벡터 표현을 어텐션 메커니즘의 입력값으로 받는다. 각 토큰에 대해 선형 변환(MLP)으로 Key 벡터와 Value 벡터를 작성하고, 대상 토큰(예: 첫 번째 "春")에 대해서는 Query 벡터를 작성한다. Query 벡터와 Key 벡터의 내적으로 토큰 간 유사도(Score)를 측정한 뒤, 이를 Softmax로 정규화(합계 1)한다. 값이 클수록 단어 간 의존이 강하다. 정규화된 유사도(실수)와 Value 벡터를 곱하고 모든 벡터의 총합을 계산하면 어텐션의 유사도에 따른 Value 벡터의 가중 평균이 산출되며, 이것이 해당 토큰의 어텐션 출력값이 된다. 같은 흐름을 두 번째 "は", 세 번째 "曙" 토큰에도 적용한다.

벡터 차원 수가 증가하면 $Q$와 $K$의 내적 값(분산)이 커지므로, 이를 억제하기 위해 차원 수의 제곱근 $\sqrt{d_k}$로 나눈다. 어텐션을 통해 각 토큰의 벡터는 다른 토큰과의 관계성을 흡수하여 더 나은 표현으로 변환된다. 1스텝으로 모든 단어와 연결됨으로써 각 토큰이 필요한 토큰의 정보만 유연하게 취사선택할 수 있으며, 이는 시계열 순서대로 토큰을 가져오는 RNN형에서는 실현 불가능했다. 직전 토큰만 보면 충분한 경우는 가까이 보고, 멀리 있는 토큰이 중요한 경우는 멀리 보는 식이다. 결과적으로 (1) 단어 간 장거리 의존 관계를 파악할 수 있고, (2) 기울기 소실/폭발 없이 안정적이며 GPU 등에서 병렬 연산 처리하기 쉬워 학습이 고속화된다.

어텐션은 시각화도 가능하다. 모든 단어 간 Attention Map(히트맵)을 만들면 "it"이 "The animal"에 강한 어텐션이 걸리는 식의 관계가 드러난다 [18]. 단, 항상 이 정도로 명확한 관계가 얻어지는 것은 아니다.

Encoder 측에서는 입력 텍스트 내의 Self-Attention을 수행한다. Decoder 측에서는 (1) 입력 텍스트와 출력 텍스트를 가로지르는 Cross-Attention, (2) 출력 텍스트 내 Self-Attention을 수행하되, 출력은 미래 토큰을 예측하는 메커니즘이므로 자신보다 미래 토큰에는 어텐션을 못 하도록 Causal Attention Mask를 적용한다. 구현 상으로는 Attention Map의 Softmax 직전에 해당 요소에 큰 음수 값(예: -1.0e+10)을 더하는 방식이다.

Multi-Head Attention은 어텐션 처리를 여러 개 병렬로 수행한 뒤 출력을 하나의 벡터로 통합한다. h개의 어텐션 메커니즘 출력(벡터)을 Concatenate하며, 하나의 토큰이 다양한 토큰에 서로 다른 형태의 어텐션을 적용할 수 있다 [6].

### Feed Forward

Feed Forward는 거대한 2계층 MLP로, 활성화 함수(ReLU)를 사이에 두고 학습 파라미터를 가진다. 중간층의 차원 수는 입력/출력층 차원 수의 수 배이다.

GPT-3 예시로 입력층/출력층 차원 수 12,288, 중간층 12,288×4=49,152, 총 블록 수 96이며, Feed Forward 파라미터 수는 (12,288×49,152)[파라미터/층] × 2[층/블록] × 96[블록] ≈ 116B로, GPT-3 전체 175B 파라미터의 약 66%를 차지한다. 최근 모델의 Feed Forward 파라미터 비율도 gpt-oss120B 71%, Llama3.1-405B 81.4%, DeepSeek-v3 62%, Qwen3 64%에 달한다(괄호 안은 MoE 모델 총 파라미터 수로, 입력에 따라 사용하는 파라미터가 달라져 실제 예측 시에는 괄호 왼쪽 수만 사용된다). 최근 모델은 SwiGLU 등 약간 다른 알고리즘을 채택한다 [13][14].

Feed Forward는 파라미터 수가 큰 만큼 중요한 역할을 한다. 제1층의 파라미터를 Key(K)로, 제2층의 파라미터를 Value(V)로 간주하면 입력 패턴 추출과 패턴 의미 표현을 수행하는 신경망 메모리를 모방한 것으로 해석 가능하며, 곧 "지식을 축적하는 장소"로 간주할 수 있다 [19].

### Add & Norm과 출력층

Add는 잔차 연결(residual connection)로 깊은 층 학습에 사용하는 기법으로 Feed Forward/Attention 이후에 적용되며 [20], Norm은 층 정규화(Layer Normalization)로 은닉층 차원 축으로 평균과 분산을 취해 학습을 안정화한다 [21]. 출력층에서는 선형 변환 후 Softmax 함수를 적용하여 다음 단어의 발생 확률을 출력한다.

## 3. 사전학습 파이프라인

### 사전학습의 의의

LLM 이전에는 번역·요약·독해 등 각 태스크마다 개별 모델을 학습했다. LLM은 대규모 코퍼스로 사전학습하여 범용 모델을 만들고, 그 위에 파인튜닝과 강화 학습 등 사후 학습으로 태스크별 성능을 끌어올린다. 사전학습의 목적은 후속 태스크에 공통으로 필요한 범용 지식(읽기·쓰기·셈하기)을 학습하고 이를 전이(Transfer Learning)하는 데 있다. 동시에 후속 태스크를 위한 좋은 파라미터 초기값을 얻는 것으로도 해석된다 [22]. 사전학습 파이프라인은 데이터 수집, 데이터 전처리, 훈련, 평가의 네 단계로 구성된다.

### 데이터 수집

사전학습용 데이터는 일반적으로 웹 대규모 크롤 데이터이며, 코드·백과사전·논문·일반 웹사이트(뉴스·블로그·홈페이지)·수학 특화 데이터 등으로 구성된다. 작년에 릴리스된 OLMo2의 데이터 소스 비율이 공개 사례로 참고된다 [12].

데이터 양은 최근 모델 기준 1~40조 토큰의 텍스트를 사용한다(토큰은 언어 AI가 처리하는 언어의 단위로, 일본어는 대략 1문자 1토큰). 1조 토큰을 서적으로 환산(1권 10만 토큰 가정)하면 약 1,000만 권에 상당하며, 이는 도쿄대 도서관(1,000만 권 이상) 규모에 맞먹는다(국회도서관은 약 4,800만 권). 구체적 토큰 수는 GPT-3 0.5조, OLMo 2 3.9조, Llama3.1 15조, DeepSeek-v3 14.8조, Qwen3 36조 등이며, gpt-oss120B는 수조 토큰을 사용한다 [13][14][24].

### 데이터 전처리

LLM 사전학습의 전형적인 전처리 파이프라인은 네 단계로 이루어진다 [25][26]. 첫째, Quality Filtering(품질 필터링)은 분류기나 휴리스틱으로 질이 낮은 데이터를 제거한다. 둘째, De-dup(중복 제거)는 가까운 위치에 중복이 있으면 학습에 악영향이 크므로 문장·문서·데이터셋 등 다양한 단위로 중복을 제거한다. 셋째, Privacy Reduction(프라이버시 저감)은 개인 식별 정보를 제거하며, AI2 Dolma에서는 logistic classifiers(content tagging)와 정규표현식(PII detection)을 조합해 이메일 주소·전화번호·IP 주소를 검출·마스크한다 [25]. 넷째, Tokenization(토큰화)은 텍스트를 토큰이라는 최소 단위로 분할하는 것으로, 다음 절에서 다룬다. 데이터셋마다 전처리 방식은 다르다.

### Tokenization

토큰화는 텍스트를 토큰이라 불리는 최소 단위로 분할하는 것이며, 이를 수행하는 프로그램이 토크나이저다. 대표 예로 Byte Pair Encoding(BPE)과 SentencePiece가 있으며, 어휘 출현 빈도에 기반한 알고리즘으로 효율적 토큰화를 실현한다. 코퍼스에서 정의한 알고리즘에 따라 토크나이저가 어휘 사전을 작성한 뒤 토큰화를 수행한다. 예컨대 "吾輩は猫である。"는 "吾輩", "は", "猫", "で", "ある", "。"로 분할될 수 있다.

대표 기법인 BPE는 텍스트를 서브워드(단어보다 세밀한 단위)로 분할하며, 어휘 크기(기본 어휘 수 + 병합 수)는 하이퍼파라미터다. GPT, GPT-2, RoBERTa, BART, DeBERTa 등 다수 Transformer에서 사용된다. 학습 과정의 예를 보면, 코퍼스가 'hug'(10), 'pug'(5), 'pun'(12), 'bun'(4), 'hugs'(5)의 5개 단어로 이루어졌다고 가정할 때, (1) 각 단어를 문자로 분할하여 ('h','u','g', 10), ('p','u','g', 5), … 형태로 만들고, (2) 가장 빈도가 높은 인접 쌍 ('u','g')을 ('ug')로 병합하며, (3) 원하는 어휘 수에 도달할 때까지 빈도가 높은 쌍의 병합을 반복한다 [46].

BPE 이외의 서브워드 단위 토큰화도 있다. WordPiece는 인접 쌍 2요소의 출현 빈도가 낮은 쌍(그 조합 이외에서는 거의 없는 쌍)을 우선 병합하며 $\text{Score} = \text{인접 쌍 }(a,b)\text{의 출현 횟수} / (a\text{의 출현 횟수} \times b\text{의 출현 횟수})$로 정의한다. (un, ##able)처럼 각 요소가 다른 단어에서도 빈출할 가능성이 큰 쌍은 그대로 두고, (hug, ##ging)처럼 각 요소가 다른 곳에서 빈출하지 않는 쌍은 병합한다. BERT, ELECTRA 등에서 사용된다. SentencePiece는 사전 단어 분할 없이 그대로 텍스트를 분할하며, 어휘 집합에 공백을 추가하고 BPE나 Unigram 등 알고리즘으로 어휘를 병합한다. 일본어 등 영어 이외의 다양한 언어에서도 쉽게 토크나이저 작성이 가능하고 서브워드 분할 알고리즘도 선택할 수 있어 T5, ALBERT 등에서 사용된다 [46].

이모지 등 처리에 관해서는, 코퍼스에 없는 문자는 <unk>로 변환되므로 많은 NLP 모델이 이모지로 콘텐츠를 분석하는 것을 서투름한다. GPT-2와 RoBERTa의 토크나이저는 이에 대응하기 위해 byte 레벨에서 BPE를 수행한다. 참고로 ByT5 [47]는 텍스트열을 토큰이 아닌 UTF-8 바이트열로 표현하는 token-free 접근으로, 서브워드로 토크나이즈한 mT5에 필적하는 성능을 보였다.

### 훈련: Next Token Prediction

사전학습의 훈련은 Next Token Prediction이라는 자기 지도 학습의 일종으로, 학습용 텍스트 데이터를 사용해 다음 토큰의 생성 확률을 계속 예측한다. "吾輩は猫である。" 예시에서 $P(\text{は}|\text{吾輩})$, $P(\text{猫}|\text{吾輩,は})$, $P(\text{で}|\text{吾輩,は,猫})$, $P(\text{ある}|\text{吾輩,は,猫,で})$, $P(\text{。}|\text{吾輩,は,猫,で,ある})$를 차례로 계산하며, 예측과 정답의 오차(교차 엔트로피)가 작아지도록, 즉 사전학습의 목적 함수로 $\min(\text{교차 엔트로피})$를 사용해 학습한다. 미니배치 내 각 샘플 문장마다 교차 엔트로피를 계산하여 평균한 것을 Loss로 사용한다.

일반적으로 1 epoch만 학습하며(1~3 범위), 여러 epoch 학습하면 과적합으로 degradation(성능 저하)되거나 차이가 없고, 모델 크기가 커질수록 degradation 경향이 강해진다 [23][27][28][29][30]. 원리적으로는 간단하지만 대규모 모델 학습(다중 노드 분산 학습)에서는 교차 엔트로피 발산(Loss 스파이크)이나 하드웨어·네트워크 저수준 에러가 발생하며 [31][32], 계산하는 수치 포맷에 따라 안정성이 달라진다(최근은 bfloat16이 주류).

하이퍼파라미터 예로 Optimizer는 Adam [33], AdamW [34], Scheduler는 Learning Rate Warmup + Decay, 부동소수점 정밀도는 BF16, Batch Size는 수백만 토큰이 일반적이다. 미니배치 내 토큰 수는 (샘플 수 × 최대 토큰 길이)로 계산된다 [23][35].

### 평가

평가는 크게 정량 평가(Upstream)·정량 평가(Downstream)·정성 평가(샘플 평가)로 나뉜다.

정량 평가(Upstream)의 대표 지표는 교차 엔트로피 Validation Loss로, Loss가 떨어지고 있는지(사전학습 자체가 붕괴하지 않았는지) 모니터링하고 모델 간 성능 차이를 확인한다. Test Loss는 논문에서 거의 보이지 않는데, 사전학습이 1 epoch 학습이 일반적이므로 overfit하지 않다는 전제 때문인 것으로 보이며, Training Loss만으로 끝나는 경우도 많다 [23][24]. 교차 엔트로피는 Cross Entropy Loss, CELoss 등 다양한 명칭으로 불리며, 식 변형 시 실질 동일한 지표로 Perplexity(PPL), Bits-Per-Character(BPC), Bits-Per-Word(BPW) 등이 있다 [7][28][36].

정량 평가(Downstream)는 다양한 하위 태스크(최종적으로 풀고자 하는 태스크)로 평가하며, In-Context Learning(Zero-shot, Few-shot, Day 2 복습)으로 평가하는 경우가 많다. 사후 학습(파인튜닝이나 RLHF, Day 5·Day 7 예정)으로 하위 태스크 성능은 더 향상된다. 평가 벤치마크 상세는 본 장 "발전 주제" 절을 참조.

정성 평가(샘플 평가)는 사전학습된 LLM을 사용해 텍스트를 출력(디코딩)해 보는 것이다. 디코딩 방식에는 Greedy Decoding, Beam Search, Random Sampling이 있다 [37][38][39][68]. Greedy Decoding은 발생 확률이 가장 높은 다음 토큰을 순차적으로 선택한다. Beam Search는 높은 발생 확률이 되는 토큰 시퀀스를 탐색하여 발견하는데, 직전뿐 아니라 그 이후까지 보고 결정하되 전 시퀀스 탐색(Exhaustive Search)하면 계산량이 폭발하므로 미리 정해둔 빔 크기 내에서 탐색한다. Random Sampling은 다음 토큰의 발생 확률 분포를 따라 무작위로 선택하며, 상위 p% 토큰에서 선택하는 Top_p(예: 0.9), 상위 k개 토큰에서 선택하는 Top_k(예: 10), 그리고 Softmax 직전 Logit의 분모에 곱하는 Temperature(0 이상의 실수, 1이면 일반 Softmax와 동일) 등의 파라미터로 조정한다. 상황에 따라 바람직한 방식이 달라 분류 문제에는 Greedy Decoding, 기계 번역에는 Beam Search, 장문 생성에는 Random Sampling이 자주 쓰인다.

## 4. 발전 주제: 데이터셋의 변천

### 학습 데이터셋의 흐름

GPT-2 시절에는 웹페이지 코퍼스(약 40GB)만으로 학습했으나, 최근에는 Code나 대화 데이터 등 다양한 데이터로 학습하는 모델이 증가했다 [26]. 대표적인 공개 코퍼스들을 정리한다.

C4 [41]는 Common Crawl(공개된 웹 아카이브를 스크래핑하여 수집, 월당 약 20TB)의 2019년 4월 웹 추출 데이터 중 영어 판정 결과와 다수의 필터링·클렌징을 거쳐 수집된 필터링된 거대 웹페이지 영어 코퍼스다. 다국어 확장으로 CC-100 [42]은 100개 언어에 걸쳐 수집된 텍스트 코퍼스로 각 언어 모델과 fastText로 필터링을 수행하며, mC4 [43]는 C4와 마찬가지로 언어 판정 후 필터링한 101개 언어를 포함한다.

The Pile [44]은 22개의 다양한 소스를 조합한 825.18GB의 언어 모델링용 데이터셋으로, 학습 데이터셋의 다양성을 높여 크로스 도메인 성능을 기대할 수 있으며 CC-100이나 Common Crawl로 학습한 모델 성능을 상회한다. Dolma [25]는 웹 콘텐츠·학술 출판물·코드·서적·백과사전의 다양한 조합으로 구성된 5334GB(3T tokens)로 최대급 혼합 사전학습용 공개 데이터셋이며, 과거 연구도 반영해 데이터 처리 베스트 프랙티스를 따랐다고 언급한다.

### Dolma의 전처리 프로세스

Dolma의 텍스트 데이터 처리는 6단계로 진행된다 [25]. (1) fastText 언어 식별 모델로 영어일 가능성이 50% 이상인 문서를 보존하고, (2) 출처 URL 기반으로 중복을 제거하며, (3) 구두점으로 끝나지 않는 모든 단락을 필터링한다. 이어 (4) 유해하거나 음란할 가능성이 60% 이상으로 판정된 것을 삭제하며 개인정보도 정규표현식으로 검출해 마스크하고, (5) 문서 내 중복 단락을 삭제하며, (6) 평가 셋에 포함된 13토큰 이상 단락을 학습 셋에서 제거한다. 데이터셋마다 전처리 방식은 다르다.

### FineWeb

FineWeb [40]은 Llama 아키텍처 소규모 모델 70개 이상을 학습하여 진행한 어블레이션(ablation) 실험을 통한 경험적 베스트 프랙티스를 반영한 데이터셋으로, CommonCrawl에서 정제한 18.5T tokens로 구성된다. 웹 정제에 특화함으로써 RefinedWeb(5T), RedPajama-v2(영·불·서·독 합계 30T) 대비 더 큰 데이터셋 구축을 가능하게 했고, 소규모 모델 실험에서 다른 공개 데이터셋보다 높은 학습 효율을 실현했다 [27][45].

파생 데이터셋으로 분류기를 사용한 FineWeb의 "교육적" 서브셋 1.3T tokens인 FineWeb-edu, 그리고 다국어판 FineWeb2("FineWeb2: One Pipeline to Scale Them All — Adapting Pre-Training Data Processing to Every Language" [69])가 있다. 일본어는 FineWeb2에 331Billion words로 비교적 풍부하게 포함되어 있다.

## 5. 발전 주제: 모델 아키텍처의 발전

### Transformer의 세 분류

Transformer는 구조에 따라 세 가지로 분류된다 [6]. Encoder-only(BERT, RoBERTa 등)는 인식계(분류)에, Encoder-Decoder(BART, T5 등)는 텍스트 생성계에, Decoder-only(GPT, Llama 등) 역시 텍스트 생성계에 해당한다. 최근 공개되는 모델은 Decoder-only가 많다 [26].

### Encoder-only 계열: BERT, RoBERTa, ALBERT

BERT [48]는 Transformer의 Encoder를 24층 쌓은 양방향 언어 모델로, 사전학습에서 빈칸 채우기(MLM) 태스크와 다음 문장 예측(NSP) 태스크를 학습하고 목적 태스크의 데이터셋으로 파인튜닝하여 11개 NLP 태스크에서 SoTA를 달성했다. 예시로 "[CLS] my dog is cute [SEP] he likes [MASK] ##ng [SEP]"에서 빈칸을 채우고 IsNext 여부를 판정한다.

RoBERTa [49]는 BERT와 동일한 아키텍처에서 일부 요소를 변경해 성능을 높였다. 데이터셋 크기 13GB→160GB, 배치 크기 256→8K, NSP 미사용, 마스크를 동적으로 적용하는 변경으로 GLUE와 SQuAD에서 BERT를 상회했다.

ALBERT [50]는 층 간 파라미터 공유로 BERT-large와 동일한 아키텍처 대비 파라미터를 18배 감소시키고 1.7배 빠른 학습을 가능하게 했다. ALBERT-xxlarge는 BERT-large보다 적은 파라미터 수임에도 GLUE, SQuAD에서 SoTA를 달성했다.

### Encoder-Decoder 계열: BART, T5

BART [51]는 BERT 같은 양방향 인코더와 GPT 같은 자기회귀형 디코더를 결합한 모델로, 무작위로 입력 문서 일부를 훼손시키고 그 재구성을 수행하는 복수 태스크 조합으로 사전학습하여 CNN/DailyMail, XSum 등에서 SoTA를 달성했다.

T5 [41]는 다수의 자연어 처리 태스크를 Text-to-Text 형태로 변환하여 통일된 프레임워크로 학습한다. 사전학습에서는 입력 문서 일부를 무작위로 특수 토큰으로 치환하고 치환 전 토큰을 예측하는 태스크로 학습해 GLUE, SuperGLUE 등에서 SoTA를 기록했다.

### Decoder-only 계열: GPT-3

GPT-3 [24]는 GPT-2의 약 120배 파라미터 수를 가진 모델을 약 14배 데이터로 학습했다. 태스크 관련 설명이나 소수 샷 예시를 입력에 추가해 태스크를 풀 수 있는 문맥 내 학습(In-context Learning)이 가능해져 소수 샷 설정에서 기존 SoTA에 필적 혹은 상회하는 성능을 확인했다. 성능이 너무 뛰어나 모델 공개 없이 API 공개에 그쳤다.

### 정규화 위치와 위치 표현

정규화 위치에 대해 세 가지 변형이 있다 [26]. Post Norm은 원래 Transformer와 마찬가지로 잔차 연결 후 정규화를 배치하나 출력층 부근에서 기울기가 커져 학습이 불안정해지는 경향이 있다. Pre Norm은 각 서브층 앞과 최종 예측 앞에 정규화를 배치하며 성능은 낮아지지만 학습 안정성으로 인해 자주 채택된다. Sandwich Norm은 잔차 연결 전에 추가 정규화를 배치하나 학습이 붕괴하는 경우도 존재한다.

위치 표현에는 절대 위치 표현과 상대 위치 표현이 있다 [52]. 절대 위치 표현은 각 토큰의 절대적 위치를 나타내는 어떤 표현(예: sin파/cos파)을 입력 표현에 더하는 방식으로, 입력 내용과 독립적이므로 계산 속도가 빠르나 알려지지 않은 길이의 시열 입력에 취약하다. 상대 위치 표현은 토큰 간 상대적 거리를 Attention 계산 시 활용하며 미지의 시열 길이에도 견고성이 높지만 입력에 고유한 값을 취해 추가 계산이 필요하다.

ALiBi [53]는 Attention 스코어 계산 시 Key와 Query의 상대적 거리에 대해 선형인 패널티를 가산하는 상대 위치 임베딩으로, 가까운 토큰 간보다 먼 토큰 간의 Attention 스코어를 더 낮춘다. 절대 위치 표현보다 성능이 좋고 외삽(extrapolation) 성능도 우수하다.

### 최근 LLM 모델 구조와 Attention 변형

최근 모델은 Attention/Feed Forward/Normalization이 개량되고 있다 [70]. Positional Embedding으로 RoPE, Attention으로 Grouped Query Attention·Sliding Window Attention·Multi-head Latent Attention, Feed Forward로 SwiGLU·Mixture of Experts, 그리고 Others로 RMSNorm이 채택되고 있다. 최신 모델 아키텍처 해설은 Sebastian Raschka의 "The Big LLM Architecture Comparison" [70]가 참고된다.

Sparse Attention은 종래 Attention의 시열 길이에 대한 제곱 계산 복잡성 문제의식에서 출발해, 모든 토큰에 대해 Attention을 계산하는 대신 국부적으로 설정한 토큰으로 학습하여 계산량을 절감한다(Big Bird [54], Longformer [55] 등의 유사 아이디어). Grouped-Query Attention(GQA) [56]은 Multi-head Attention이 디코딩 시 모든 Key와 Value를 읽어와야 해 추론 속도 병목이 되는 문제의식에서, Key와 Value를 일부(Group-query) 또는 하나(Multi-query)의 헤드에서 공유하여 메모리 부하를 줄이고 추론 속도를 향상시키며 Llama3 등에서 채택된다.

## 6. 발전 주제: 목적 함수, 평가, 분석

### 목적 함수의 발전

UniLM [57]은 Attention 마스크 영역을 변화시켜 양방향 언어 모델링, 단방향 언어 모델링, 배열 간 언어 모델링을 결합한 복합적 목적 함수로 사전학습해, GLUE 같은 식별 태스크에서 BERT에 필적하면서도 CNN/DM 같은 언어 생성 태스크에서 SoTA를 달성했다.

UL2 [58]는 T5 같은 결손 토큰 예측(R-Denoising, X-Denoising)과 GPT 같은 연속 토큰 예측을 결합한 MoD(Mixture-of-Denoisers)라는 통일적 목적 함수로 학습한다. MoD를 지속적 사전학습에 사용하는 UL2R(UL2 Repair) 훈련 방법도 후에 제안되었으며, EncDec과 Dec 양쪽 아키텍처에서 균형 있게 성능 향상을 확인했다.

### 평가의 확장과 FLASK

평가 대상은 자연어 이해(GLUE, SuperGLUE, SQuAD)에서 도메인 지식(MMLU, MATH, MultiMedQA, APPS, CUAD), 윤리성·신뢰성(FLASK, TrustGPT, TruthfulQA), 도구 활용(ToolBench)까지 확장되었다 [26]. FLASK [60]은 LLM에 필요한 스킬을 정의하고 모델의 행동에 대해 인간 또는 모델이 스코어링을 수행하는 벤치마크로, 주로 4가지 능력(논리적 사고, 배경 지식, 문제 해결 능력, 지시 추종성)으로 구성된 평가 프레임워크를 구축하고 이를 12개의 상세한 스킬 항목으로 세분화한다.

### Attention 분석과 모델 해석

Attention의 대소는 자주 가시화되며 이를 Attention map이라 부른다 [61]. Attention이 단어 중요도를 나타내는 것처럼 보이지만 Attention에는 설명 능력이 없다는 입장의 논문도 복수 존재한다. 종래 Attention에서는 복수 층을 경유해 정보가 오가므로 Attention map 자체를 입력에 대한 기여로 해석하기에는 신뢰성이 부족하다. Attention Rollout [62]은 자신보다 앞에 있는 층의 Attention map을 순차적으로 곱하고, Attention Flow는 각 층의 Attention을 플로우 네트워크로 해석해 입력 토큰에 대한 어텐션을 근사한다.

참고로, 현재 사전학습과 Transformer는 스탠다드가 되었지만 이 둘이 세트로 의미가 있는 것은 아니다 [63]. CNN에서도 사전학습 효과가 있으며 일부 태스크에서 CNN 모델이 T5를 상회하는 성능을 발휘하기도 한다. CNN이 항상 Transformer의 대체가 되는 것은 아니지만, 사전학습이라는 패러다임 전환과 아키텍처의 변천은 분리해 생각해야 한다는 주장이 있다. 이론적으로 상대 위치 표현을 사용하면 Multi-Head Self-Attention은 Convolution을 내포한다 [64].

### 적대적 공격과 프로빙

적대적 공격(adversarial attack) 분석은 인간에게는 사소한 영향만 주는 섭동(perturbation)이라도 신경망이 크게 영향을 받는 경우가 존재한다는 문제의식에서 출발한다 [65]. 입력 일부를 편집해 모델 성능을 열화시키는 공격을 검증함과 함께 그 공격에 의한 실패를 막는 방어 방법을 검토한다.

프로빙(probing) [66]은 언어 모델이 내부적으로 획득한 능력을 분석하는 방법이다. 언어 모델의 태스크 성능은 출력으로 평가할 수 있지만 내부적으로 획득한 능력은 출력만으로는 쉽게 평가할 수 없다. 어떤 입력을 주었을 때 언어 모델에서 얻어지는 임베딩 표현에서 특정 태스크(예: 품사 분류)를 수행하는 분류기(프로브)를 훈련했을 때의 성공률로부터, 임베딩 표현에 그 태스크를 나타내는 표현이 인코딩되어 있는지 검증한다. 최근에는 모델의 임베딩 표현에 개입을 수행해 출력으로의 인과관계를 조사하는 경우도 많다.

## 7. 정리

본 장에서는 대규모 언어 모델(LLM)의 사전학습을 네 관점에서 소개했다.

첫째, 언어 모델에서 Transformer의 위치다. Transformer는 신경망 언어 모델의 하나로 취급되며, RNN형 언어 모델이 안고 있던 장거리 의존성 파악·학습 불안정성 과제를 해결했다.

둘째, LLM에서 주류가 된 Transformer 모델 구조다. Self-Attention 메커니즘을 가진 모델 구조이며 1스텝으로 전 단어 정보와 연결 가능하다. 이로써 과제①(단어 간 장거리 의존성 파악)과 과제②(오차 역전파 계산 스텝이 문장 길이에 비의존하게 되어 학습 안정·고속화)가 해결되었다.

셋째, LLM의 사전학습이다. 대규모 코퍼스로 학습을 수행함으로써 모델의 범용성을 높이고 있으며, Next Token Prediction이라는 자기 지도 학습으로 최적화한다.

넷째, 발전 주제다. 데이터·모델·학습·평가 분석에 대한 발전적 주제를 해설했다.

모델별 학습 방법과 세부 요소의 차이, 그리고 모델의 접근성(API 전용·공개 & 거대·비공개)에 관해서는 보충 자료와 "A Survey of Large Language Models" [26], "Holistic Evaluation of Language Models" [67]을 참조할 것.

## 참고문헌

[1] 岡崎直観 (2023), "대규모 언어 모델의 경이와 위협", Speaker Deck.
[2] Ilya Sutskever et al. (2014), "Sequence to Sequence Learning with Neural Networks", NeurIPS2014.
[3] Tomáš Mikolov et al. (2010), "Recurrent Neural Network Based Language Model", Proc. Interspeech 2010, 1045-1048.
[4] Dzmitry Bahdanau et al. (2014), "Neural Machine Translation by Jointly Learning to Align and Translate", arXiv:1409.0473.
[5] Masaki Hayashi (2022), "Transformer와 seq2seq with attention의 차이는? 시열 변환 모델【Q and A 기사】", CVML 전문가 가이드.
[6] Ashish Vaswani et al. (2017), "Attention Is All You Need", NeurIPS2017.
[7] OpenAI (2023), "GPT-4 Technical Report", arXiv:2303.08774.
[8] OpenAI (2025), "GPT-5 System Card".
[9] OpenAI (2025), "GPT-5가 등장".
[10] Google (2025), "Gemini 2.5 tech report".
[11] OpenAI (2024), "Learning to Reason with LLMs".
[12] Allen Institute for AI, Univ. of Washington, NYU (2025), "2 OLMo 2 Furious", arXiv:2501.00656.
[13] OpenAI (2025), "gpt-oss-120b & gpt-oss-20b Model Card", arXiv:2508.10925.
[14] Qwen (2025), "Qwen3 Technical Report", arXiv:2505.09388.
[15] Shraddha Anala (2020), "A Guide to Word Embedding", Towards Data Science.
[16] John Hewitt, "Natural Language Processing with Deep Learning CS224N/Ling284".
[17] Raimi Karim (2019), "Illustrated: Self-Attention", Medium.
[18] Jay Alammar (2018), "The Illustrated Transformer", jalammar.github.io.
[19] Mor Geva et al. (2021), "Transformer Feed-Forward Layers Are Key-Value Memories", EMNLP2021, 5484-5495.
[20] Kaiming He et al. (2016), "Deep Residual Learning for Image Recognition", CVPR2016, 770-778.
[21] Jimmy Lei Ba et al. (2016), "Layer Normalization", arXiv:1607.06450.
[22] Rishi Bommasani et al. (2021), "On the Opportunities and Risks of Foundation Models", arXiv:2108.07258.
[23] Hugo Touvron et al. (2023), "LLaMA: Open and Efficient Foundation Language Models", arXiv:2302.13971.
[24] Tom Brown et al. (2020), "Language Models are Few-Shot Learners", NeurIPS2020.
[25] Luca Soldaini et al. (2023), "Dolma: An Open Corpus of 3 Trillion Tokens for Language Model Pretraining Research", AI2 Blog.
[26] Wayne Xin Zhao et al. (2023), "A Survey of Large Language Models", arXiv:2303.18223.
[27] Guilherme Penedo et al. (2023), "The RefinedWeb Dataset for Falcon LLM", arXiv:2306.01116.
[28] Hugo Touvron et al. (2023), "Llama 2: Open Foundation and Fine-Tuned Chat Models", arXiv:2307.09288.
[29] Fuzhao Xue et al. (2023), "To Repeat or Not To Repeat: Insights from Scaling LLM under Token-Crisis", arXiv:2305.13230.
[30] Niklas Muennighoff et al. (2023), "Scaling Data-Constrained Language Models", arXiv:2305.16264.
[31] Stas Bekman (2022), "The Technology Behind BLOOM Training", huggingface.co.
[32] facebookresearch (2023), "OPT175B Logbook", GitHub metaseq.
[33] Diederik P. Kingma & Jimmy Ba (2014), "Adam: A Method for Stochastic Optimization", arXiv:1412.6980.
[34] Ilya Loshchilov & Frank Hutter (2017), "Decoupled Weight Decay Regularization", arXiv:1711.05101.
[35] Shikoan's ML Blog (2021), "Cosine Decay와 Warmup을 동시에 수행하는 스케줄러(timm)".
[36] Chip Huyen (2019), "Evaluation Metrics for Language Modeling", thegradient.pub.
[37] Kaito Sugimoto (2021), "텍스트 생성에서의 decoding 테크닉: Greedy search, Beam search, Top-K, Top-p", zenn.dev.
[38] mm_0824 (2020), "빔서치(Beam Search) 이해하기", data-analytics.fun.
[39] cohere, "Temperature", docs.cohere.com.
[40] Hugging Face (2024), "The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale", arXiv:2406.17557.
[41] Colin Raffel et al. (2020), "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer", JMLR 21(1):140, 5485-5551.
[42] Alexis Conneau et al. (2020), "Unsupervised Cross-lingual Representation Learning at Scale", ACL2020, 8440-8451.
[43] Linting Xue et al. (2021), "mT5: A Massively Multilingual Pre-trained Text-to-Text Transformer", NAACL2021, 483-498.
[44] Leo Gao et al. (2020), "The Pile: An 800GB Dataset of Diverse Text for Language Modeling", arXiv:2101.00027.
[45] Weber et al. (2024), "RedPajama: an Open Dataset for Training Large Language Models", NeurIPS2024.
[46] Hugging Face (2025), "Hugging Face LLM Course", Chapter 6.5-6.6.
[47] Linting Xue et al. (2022), "ByT5: Towards a Token-Free Future with Pre-trained Byte-to-Byte Models", TACL 10:291-306.
[48] Jacob Devlin et al. (2019), "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding", NAACL-HLT 2019, 4171-4186.
[49] Yinhan Liu et al. (2019), "RoBERTa: A Robustly Optimized BERT Pretraining Approach", arXiv:1907.11692.
[50] Zhenzhong Lan et al. (2020), "ALBERT: A Lite BERT for Self-supervised Learning of Language Representations", ICLR2020.
[51] Mike Lewis et al. (2020), "BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension", ACL2020, 7871-7880.
[52] 清野舜 (2022), "보다 나은 Transformer 만들기", Speaker Deck.
[53] Ofir Press et al. (2021), "Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation", arXiv:2108.12409.
[54] Manzil Zaheer et al. (2020), "Big Bird: Transformers for Longer Sequences", NeurIPS2020.
[55] Iz Beltagy et al. (2020), "Longformer: The Long-Document Transformer", arXiv:2004.05150.
[56] Joshua Ainslie et al. (2023), "GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints", arXiv:2305.13245.
[57] Li Dong et al. (2019), "Unified Language Model Pre-training for Natural Language Understanding and Generation", NeurIPS2019.
[58] Yi Tay et al. (2022), "UL2: Unifying Language Learning Paradigms", arXiv:2205.05131.
[59] Yupeng Chang et al. (2023), "A Survey on Evaluation of Large Language Models", arXiv:2307.03109.
[60] Seonghyeon Ye et al. (2023), "FLASK: Fine-grained Language Model Evaluation based on Alignment Skill Sets", arXiv:2307.10928.
[61] Andrea Galassi et al. (2019), "Attention in Natural Language Processing", arXiv:1902.02181.
[62] Samira Abnar & Willem Zuidema (2020), "Quantifying Attention Flow in Transformers", ACL2020, 4190-4197.
[63] Yi Tay et al. (2021), "Are Pre-trained Convolutions Better than Pre-trained Transformers?", ACL2021, 4349-4359.
[64] Jean-Baptiste et al. (2020), "On the Relationship between Self-Attention and Convolutional Layers", ICLR2020.
[65] Jack Morris (2020), "What are adversarial examples in NLP?", towardsdatascience.com.
[66] Yonatan Belinkov (2022), "Probing Classifiers: Promises, Shortcomings, and Advances", Computational Linguistics 48(1):207-119.
[67] Percy Liang (2022), "Holistic Evaluation of Language Models", arXiv:2211.09110.
[68] Harshit Sharma (2022), "Softmax Temperature".
[69] Hugging Face, EPFL (2025), "FineWeb2: One Pipeline to Scale Them All — Adapting Pre-Training Data Processing to Every Language", COLM2025.
[70] Sebastian Raschka, "The Big LLM Architecture Comparison", magazine.sebastianraschka.com.
