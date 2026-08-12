# Day 4: 스케일 법칙

이 장은 도쿄대학교 마츄오·이와사와 연구실이 2025년 10~11월에 개최한 대규모 언어 모델 강좌 기초편 넷째 날 강의를 재구성한 것이다. 이론은 고지마 타케시(小島武), 실습은 여전군(余振軒)이 담당했다. 고지마 타케시는 2023년 도쿄대학교 대학원 공학계 연구과 TMI 박사 과정을 수료한 뒤 같은 연구과의 특임 연구원을 거쳐 2025년부터 특임 조교수를 맡고 있으며, 이전에는 IT 엔지니어로 일했다. Weblab-10B 개발, 기시다 총리·이시바 총리의 LLM 특별 강좌 강사, LLM 개발 콘테스트 2024·2025 운영 측 콘텐츠 리더, AI 백서 2025 Safety 장 집필 등에 참여했고, 연구 분야는 LLM의 작동 원리 이해와 제어(Reasoning Model, 다국어 등), Safety(Unlearning, 지시 추종 능력), Transformer 모델 구조 개선, 그리고 로봇이다. 본 자료는 CC BY-NC-ND 4.0(저작자표시–비영리–변경금지 4.0 국제) 라이선스로 제공된다.

## 강의의 목적과 배경

이 장의 목적은 언어 모델을 스케일, 곧 대규모화하는 의의를 학습하는 데 있다. 이를 위해 스케일 법칙이 무엇인지, 왜 중요한지, 구체적으로 어떻게 구하는지를 다루고, 나아가 학습 시뿐 아니라 추론 시에도 연산량을 스케일시키는 새로운 트렌드를 살펴본다. 실습에서는 PyTorch로 스케일 법칙을 직접 구하는 코드를 구현한다.

현대의 대규모 언어 모델(LLM)은 대부분 2017년에 발명된 Transformer 구조를 기반으로 하는 신경 언어 모델의 한 종류이다. LLM 학습은 일반적으로 세 단계로 이루어진다. 첫째, 사전학습(pretraining)은 대규모 코퍼스를 이용한 자기 지도 학습으로 어휘·문법·기초 지식과 같은 기초적인 언어 이해를 획득하는 단계이다. 둘째, 파인튜닝(fine-tuning)은 레이블이 있는 데이터를 이용한 지도 학습을 통해 사전학습된 모델의 성능을 개선하거나 특정 태스크나 도메인에 적응시키는 단계이다. 셋째, RLHF(인간의 피드백을 이용한 강화학습)는 모델의 출력이 인간의 가치관에 부합하도록 조정하는 단계이다. 이 장에서는 그중 사전학습 단계를 중심으로 스케일 법칙을 다룬다.

2018년 GPT, 2019년 GPT-2, 2020년 GPT-3에 이어 2023년 이후로도 GPT-5, Gemini 2.5, GPT-OSS, DeepSeek-R1, Qwen3 등 많은 LLM이 공개되었다. 이처럼 미국 기업을 중심으로 여러 연구 기관이 독자적인 대규모 언어 모델을 개발하게 된 배경에는 스케일 법칙이라 불리는 경험칙이 자리 잡고 있다.

## 스케일 법칙이란 무엇인가

### 사전학습과 스케일 법칙의 발견

사전학습은 웹에서 수집한 대량의 문장을 이용하여 다음 단어의 예측을 쉬지 않고 수행한다. 예를 들어 "봄은 벚꽃이 아름답다"라는 텍스트를 학습할 때, 모델은 "봄" 다음에 "은"이, "봄은" 다음에 "벚꽃"이 오는 식으로 예측한다. 예측과 정답의 오차, 곧 교차 엔트로피(cross entropy)가 작아지도록 모델을 학습하며, 이 과정에서 읽기·쓰기·셈하기 및 세계의 지식을 습득한다. "봄" "벚꽃" "아름답다"라는 단어 사이에 강한 관계성이 있다는 것(= 세계의 지식)을 학습하는 것이다. GPT 시리즈를 대표로 하는 현대의 LLM은 반드시 이 사전학습을 수행한다.

스케일 법칙(Scaling Law)은 이런 대규모 학습에서 발견된 경험칙으로, 거듭제곱 법칙(Power-Law)이라고도 불린다. 핵심적인 두 논문이 이 법칙을 정립했다. 하나는 2020년 1월 OpenAI의 Kaplan 등이 발표한 "Scaling Laws for Neural Language Models"이고(GPT-3는 같은 해 6월 발표), 다른 하나는 2022년 DeepMind의 Hoffmann 등이 발표한 "Training Compute-Optimal Large Language Models"(이하 Chinchilla 논문)이다.

### 세 가지 변수와 오차의 관계

스케일 법칙은 컴퓨팅 자원(C), 데이터셋 크기(D), 파라미터 수(N)와 오차(L) 사이에 성립하는 관계를 기술한다. 다른 두 변수가 충분히 크다고 가정할 때, 어느 변수든 오차(Test Loss)와의 사이에 이중 로그 그래프에서 선형 관계가 나타난다.

첫째, 파라미터 수(N)가 커질수록 오차(L)는 일정한 기울기로 감소한다. 둘째, 데이터셋 크기(D)가 커질수록 마찬가지로 오차가 감소한다. 셋째, 컴퓨팅 자원(C)에 대해서도 같은 형태의 관계가 성립한다. 이를 수식으로 나타내면 다음과 같다.

> L(X) = (Xc / X)^α

여기서 X는 C, D, N 중 하나의 변수이고, α는 이중 로그 그래프 상의 기울기, Xc는 절편에 해당하는 값이다. 관계가 거듭제곱 형태로 표현된다는 것이 스케일 법칙이라는 이름의 유래이다.

### 연산량의 단위: FLOPs

컴퓨팅 자원을 나타내는 가로축에 사용되는 단위는 FLOPs(FLoating Points OPerations)이다. 이는 모델 학습에 필요한 총 부동소수점 연산 횟수를 의미한다(파라미터의 덧셈·곱셈 등). 주의할 점은 단위 시간당 처리 능력을 나타내는 HW 성능 지표인 FLOPS(Floating Points Operation Per Second, 대문자 S)와 혼동하기 쉽다는 것이다. 접두사로는 Mega(M, 10^6), Giga(G, 10^9), Tera(T, 10^12), Peta(P, 10^15), Exa(E, 10^18) 등이 사용된다. 스케일 법칙 논문에서는 PF-days(Peta FLOPs days), 즉 1 Peta FLOPS 처리 속도의 서버를 며칠분 학습에 사용했는지를 단위로 쓴다. 참고로 GPT-3의 총 연산량은 약 3.14 × 10^23 FLOPs로 알려져 있으며, 최근 모델들의 FLOPs는 상세가 비공개이므로 정확히 알 수 없다.

LLM 학습에 필요한 연산량은 파라미터 수(N)와 토큰 수(D)를 이용해 다음 근사식으로 구할 수 있다.

> C ≈ 6 × N × D

GPT-3의 경우 175B 파라미터 × 0.3T 토큰 × 6 ≒ 3.14 × 10^23 FLOPs가 된다. 계수가 6인 이유는 파라미터당 MLP 층에서의 행렬 연산 횟수가 순전파(forward) 2회, 역전파(backward) 4회 등 총 6회이기 때문이다. 단, 이 근사는 Attention 기구의 연산량을 무시한 것이다. 시계열 길이가 짧은 경우에는 MLP 연산량이 Attention 연산량보다 압도적으로 크므로 무시해도 무방하지만, 최근 컨텍스트 길이가 길어지는 경향(GPT-3: 2,049 토큰, ChatGPT: 16,385 토큰, GPT-4: 32,768 토큰)을 고려하면 Attention 연산량을 무시할 수 없게 되었을 가능성이 높다. 보다 정확한 계산식은 karpathy/nanoGPT 저장소의 scaling_laws.ipynb 등을 참조할 수 있다.

이해를 돕기 위한 미니 퀴즈를 하나 생각해보자. GPU A100 1기의 연산 능력을 약 10^14 FLOPS(대문자 S이므로 단위 시간당 연산량)라고 가정하자. 그렇다면 A100을 1000기 사용할 때, GPT-3 학습에는 어느 정도의 학습 시간이 필요한가? 이 문제에 답하려면 FLOPs(총 연산량)를 FLOPS(단위 시간당 연산량)로 나누어 시간을 구하면 된다.

### 모델 크기와 학습 곡선

컴퓨팅 자원(C)과 오차(L)의 관계를 더 자세히 보면, 서로 다른 모델 크기로 학습했을 때의 학습 곡선이 의미 있는 패턴을 보여준다. 모델 크기가 작으면 적은 컴퓨팅 자원으로도 빠른 속도로 Loss가 내려가지만, 일정 시점 이후로는 학습을 계속해도 Loss가 내려가기 어려워진다(포화, saturate). 반면 모델 크기가 크면 적은 컴퓨팅 자원으로는 Loss가 좀처럼 내려가지 않지만, 학습을 계속하면 Loss가 계속 내려가 포화되지 않고 최종적으로 더 좋은 성능에 도달한다.

이로부터 두 가지 통찰을 얻는다. 어떤 수준의 Loss(성능)를 달성하는 데 최적인 모델 크기는 정해져 있으며, 제한된 컴퓨팅 자원으로 최고의 성능을 발휘하는 모델 크기도 역시 정해져 있다. 즉, 주어진 컴퓨팅 자원량에 대해 최적의 성능을 발휘하는 모델 크기가 존재하고, 그 최적점들의 집합을 연결한 선이 바로 스케일 법칙이 기술하는 관계이다.

### 스케일 법칙의 역사와 다양한 도메인에서의 검증

스케일링은 새로운 현상이 아니다. 적어도 2017년 Baidu Research의 Hestness 등이 검증했으며, 이 연구에서는 기계 번역, 언어 모델링, 이미지 분류, 음성 인식 등 다수의 도메인에서 스케일 법칙의 발생을 확인했다. 특히 데이터에 관한 스케일 법칙을 중심으로 검증했다(모델에 대해서도 일부). 당시 연구와 Kaplan 등 이후의 연구를 비교하면 공통점은 데이터에 관한 스케일 법칙이 검증되었다는 점이고, 차이점은 대상 모델(Transformer 이전의 LSTM 등 RNN형 언어 모델)과 규모(특히 모델 규모)가 다르다는 점이다.

GPT-3에서도 스케일 법칙이 이용되었으며, 선행 연구(Kaplan 등 2020)보다 2 자릿수 오더 더 큰 연산량에서 스케일 법칙을 확인했다. 모델 구조 탐색 측면에서도 깊이(depth) 등 다양한 구조 요소에 대해 스케일 법칙이 검토되었다. 이후 Mixture of Experts(MoE) 모델에서도 일반 Transformer(점선)와 비교해(실선) 스케일 법칙이 검증되었고(MoE의 상세는 Day 5에서 다룬다), 이미지 생성, 멀티모달, 동영상, 수리 등 언어 이외의 도메인에서도 연산량에 관한 스케일 법칙이 성립함이 확인되었다. 어떤 연산량이 주어졌을 때 최적인 모델 크기는 도메인 간에 대체로 비슷한 경향을 보인다.

## 스케일 법칙의 활용 방법

### 투자 판단과 모델 구조 탐색

스케일 법칙의 가장 큰 가치는 성능을 예측 가능하게 만든다는 데 있다. GPT-4 기술 보고서에 따르면, GPT-4를 1.0으로 한 연산량(X축)과 성능(Y축)의 관계에서 1/1000 정도의 작은 모델까지로도 성능을 정확하게 예측할 수 있었다. GPT-4의 파라미터 수는 공개되지 않았지만, 아무리 작아도 10^10(10B)보다는 크고, 그래프의 최소가 10^3이라고 하면 약 10^13(1T)까지 스케일 예측이 유효하다는 의미이다. 이는 대규모 모델에 대한 투자 위험을 줄여 준다("Scaling laws de-risk investments in large models"). 실제로 모델 구조 탐색이나 하이퍼파라미터 탐색 단계에서 작은 모델로 어느 구조가 우수한지(예: Transformer vs LSTM), 어느 쪽이 더 스케일에 유리한지(예: 파라미터가 작을 때는 층이 적은 쪽이, 클 때는 층이 많은 쪽이 유리)를 판단할 수 있다.

### 효율적인 모델 선택과 샘플 효율

파라미터 수가 많을수록 샘플 효율(sample efficiency)은 좋다. 작은 모델에서는 학습 도중부터 Loss가 내려가기 어려워지므로, 어떤 Loss를 달성하는 데 작은 모델로 연산을 계속하는 것은 비효율적이다.

### Chinchilla: 주어진 연산량 하의 최적 배분

주어진 연산량 하에서 최적인 파라미터 수와 토큰 수를 찾는 연구가 DeepMind의 Chinchilla 논문이다. 연산량을 고정하고 파라미터 수와 토큰 수를 변동시키면(Chinchilla와 PaLM 2 모두에서 확인), 어느 연산량에서든 U 커브가 나타나며 최적인 값이 존재한다. U 커브가 되는 이유는 더 큰 파라미터 크기의 모델일수록 학습 초기의 Loss가 내려가기 어렵기 때문이다. 각 곡선마다 Training Loss가 최소가 되는 포인트를 찾고, 여러 연산량에 대해 같은 방법으로 최적인 파라미터 크기를 도출하면 FLOPs와 Parameter 사이의 최적 관계를 얻을 수 있으며, 이는 거의 직선 관계이다. 토큰 수에 대해서도 같은 방식으로 최적값을 구할 수 있다.

Chinchilla는 이 최적 연산 배분에 기반해 모델 크기는 70B(Gopher의 약 1/4배)로, 토큰 수는 1.4T(Gopher의 약 4.6배)로 설정했다. 그 결과 더 거대한 모델(Gopher 280B)을 제치고 많은 케이스에서 승리했으며, 이는 발견한 관계식의 타당성을 시사한다. 핵심 결론은 "최적 토큰 수 = 20 × 파라미터 수"이다. PaLM 2에서도 같은 실험이 수행되어 Chinchilla와 마찬가지의 스케일 법칙이 확인되었다.

### Chinchilla 법칙을 넘어서: 추론 비용 고려

하지만 Chinchilla 법칙이 정말 최적인지에 대한 반론도 있다. Chinchilla의 모델 크기(70B)는 여전히 추론 비용이 높다. 학습만 보면 큰 모델이 같은 FLOPs로 더 높은 성능을 내지만, 추론 시에는 큰 모델이 더 많은 FLOPs를 필요로 한다. 따라서 학습과 추론 양쪽의 FLOPs를 모두 고려한 최적해를 도출하는 편이 낫다는 주장이 나왔다("Chinchilla Trap").

Harm de Vries는 최적 모델 크기의 40~60% 이내의 모델 크기를 선택하여 10~42%의 연산량 추가로 동일 성능의 모델을 학습할 수 있다고 지적했다. Sardana 등의 연구에서는 추론 시 토큰 수와 달성하고자 하는 학습 Loss를 가정했을 때, 라이프타임 전체의 총 FLOPs를 최소로 하는 최적의 파라미터 수 및 학습 토큰 수를 도출했는데, 추론 횟수가 많아질수록 라이프타임 전체로는 학습 토큰 수를 늘리는 쪽이 유리함을 보였다.

실제 모델들의 토큰 대 파라미터 비율(D/N)을 보면 이 경향이 반영되어 있다. Gopher(N=280B, D=0.3T)은 D/N이 1.07이었으나, Chinchilla(70B, 1.4T)는 20.0, Llama 2 7B(1.8T)는 285, Llama 3 70B(15T)는 214.2, Qwen 3 32B(36T)는 1125에 이른다. 최근 모델일수록 Chinchilla가 제시한 20을 크게 웃도는 토큰 수로 학습하는 추세이다.

### 예측 가능한 개선과 예측 불가능한 개선

스케일 법칙으로 예측 가능한 성질에는 성능의 개략 산정, 일반적인 문장의 다음 단어 예측 정확도, 번역이나 QA 태스크에서의 평균적인 점수 개선 등이 있다. 반면 예측 불가능한 성질도 존재한다.

대표적인 예가 창발 능력(Emergent Ability)이다. 모델 크기를 거대하게 하면 특정 태스크에서 성능이 "갑자기" 대폭 올라가는 현상이 관찰된다. 하지만 이것이 정말 "창발"이나 "상전이"인지에 대해서는 반론도 있다. 성능의 측정 방법에 의존할 수 있고(이것은 본 논문에서도 지적됨), 가로축이 로그인 것도 이상하며, 애초에 무엇을 창발이라 할 것인지도 논쟁거리이다. 다만 거대 모델과 거대 연산으로 생각보다 잘하게 되는 것은 사실이다.

또 다른 예로 Grokking이 있다. 이는 학습을 계속하면 갑자기 검증 데이터에서의 정답률이 높아지는 현상으로, 학습 데이터에서의 정답률은 그 이전에 이미 높은, 즉 과적합 후에도 학습을 계속하면 발생하는 현상이다. 연구에 따르면 과학습 중에는 단순히 기억만 하던 것이, 일반화 단계에 이르면 내부 표현이 깔끔하게 정렬되는 식으로 기억을 일반화하고 있다.

### 다운스트림 태스크와 스케일 법칙

Loss(사전학습의 교차 엔트로피)가 낮다는 것이 반드시 다운스트림 태스크의 성능이 높은 것으로 직결되는가? 기본적으로는 YES이지만 예외도 자주 있다. 성능은 깔끔하게 상승하는 경우도 있고, 갑자기 상승하는 경우(Emergent Ability), 오르지 않는 경우, 내려갔다가 오르는 경우(Inverse scaling prize) 등 태스크의 종류와 난이도에 따라 다양한 패턴이 나타난다.

다운스트림 태스크 데이터가 학습 데이터와 분포가 정렬되어 있는 경우에는 사전학습 데이터량과 다운스트림 태스크 평가값 사이에 스케일 법칙이 성립한다. 기계 번역 태스크로 검증한 결과, MC4(Multilingual C4) 같은 사전학습 데이터와 다운스트림 태스크 데이터의 임베딩 공간에서의 분포 거리가 가까울수록 스케일 법칙이 잘 들어맞는다. 분포 외 데이터(WebText2 이외)에서는 성능 열화가 보이지만 오프셋의 차이 정도이며 기울기는 거의 같다.

### 스케일 법칙 활용의 정리

예측 가능한 성능 개선에 의해 다음과 같은 물음에 답할 수 있다. 투자의 판단(더 많이 컴퓨터에 투자할 것인가), 효율적인 모델 선택(파라미터를 늘렸을 때 어느 쪽이 좋은 모델인가), 효율적인 컴퓨팅 자원 이용(토큰과 파라미터 중 어느 쪽을 늘려야 하는가; Chinchilla Optimal에서는 최적 토큰 수 = 20 × 파라미터 수이며, 추론 비용을 고려하면 계수가 변화한다). 단, 다운스트림 태스크에 스케일 법칙이 반드시 성립한다고는 한정하지 않는다.

## 스케일 법칙의 구하는 방법

### 기본 접근: 작은 실험에서 피팅하기

스케일 법칙을 구하는 기본 방법은 비교적 작은 몇 가지 조건으로 실험을 수행하고 결과를 피팅(fitting)하는 것이다. GPT-4 기술 보고서와 Hoffmann 등의 연구가 이 방식을 따랐다. 이때 두 가지 핵심적인 질문이 생긴다. 모델 크기를 어떻게 변화시킬 것인가? 학습률 등의 하이퍼파라미터는 어떻게 설정할 것인가?

### 모델 크기를 변화시키는 방법

모델 크기를 바꾸는 수단으로는 층 수를 늘리거나, 임베딩 차원을 올리거나, FFN의 중간층 차원을 크게 하거나, 어텐션 헤드 수를 늘리는 등 여러 가지가 있다. Kaplan 등의 원 논문에서는 파라미터 수를 고정했을 때 신경망의 여러 요소를 조정하여 검토한 결과, 큰 영향은 없다는 결론을 내렸다. 예컨대 종횡비(aspect ratio, 임베딩 크기 / 층 수)는 큰 영향을 미치지 않았다.

실제 사례를 보면, Llama 3는 종횡비가 128, 102.4, 130 등으로 모델 차원 대 FFN 차원 비율은 3.5로 일정하며, 헤드 수도 모델 차원에 대해 비례해서 스케일한다. Cerebras GPT 역시 종횡비가 76.8, 77.7, 85.3 등으로 모델 차원 대 FFN 차원 비율을 4.0으로 유지한다(헤드 수는 다소 불규칙하게 변화). 즉, 대체로 고정된 계수를 유지하면서 스케일하는 것이 일반적이다.

### 하이퍼파라미터 변화와 μTransfer

모델 크기를 스케일시킬 때 학습률과 스케줄링을 어떻게 설정할 것인가도 중요한 문제이다. 통상적인 초기화의 경우, 폭(width)을 변화시키면 최적인 학습률이 달라진다(다만 어느 정도 경향은 있다). 경험칙으로는 모델 크기를 크게 했을 때 학습률은 점차 작게, 배치 크기는 크게 하는 것이 좋은 경향이 있다. Cerebras GPT 등 실제 모델들도 모델 파라미터가 클수록 학습률을 작게, 배치 크기를 크게 설정하는 경향을 보인다.

Yang 등이 제안한 μTransfer(μP 전이)는 이 문제를 우아하게 해결하는 방법이다. 가중치 초기화 방법과 weight별 학습률 설정 방법을 변경함으로써, 작은 모델에서 찾은 최적의 학습률을 큰 모델에 제로샷으로 전이할 수 있다. μTransfer를 사용하면 모델 크기가 달라도 거의 같은 정도의 학습률 값으로 최적의 Loss를 달성할 수 있다. Cerebras GPT는 μTransfer를 실제로 적용한 사례이다.

스케일 법칙의 상세에 더 관심 있는 독자는 Hashimoto와 Liang의 Stanford CS336 강의("Language Modeling from Scratch", 2024)를 참조하기를 권한다.

## 추론 시의 스케일링

### 동기: 추론 부하의 차이

"바나나의 색은 무엇입니까?"와 "스케일 법칙의 문제는 무엇이라고 생각합니까?"는 필요한 사고의 과정이 분명히 다르다. 후자는 추론 시에 더 큰 부하가 걸린다. 이러한 구조를 LLM에서 어떻게 실현할 수 있는가, 또 효과적인가라는 질문이 추론 시 스케일링의 출발점이다. OpenAI가 발표한 o1 모델도 테스트 시의 추론을 스케일링시킴으로써 성능 향상을 보고했다.

추론 시에 연산량을 스케일시키는 방법은 크게 프롬프팅(prompting), 디코딩(decoding), 메타 제너레이션(meta-generation) 세 가지 수준으로 나눌 수 있다.

### 프롬프팅과 디코딩

프롬프팅 수준에서는 Chain-of-Thought Prompting과 Many-Shot In-Context Learning(ICL)이 대표적이다. 프롬프팅을 통해 추론 시의 토큰 수를 늘림으로써 추론 시의 연산량을 스케일시키는 시도이다.

디코딩 수준에서는 사전학습된 LLM이 텍스트를 출력(디코드)하는 방식을 다양화한다. 사전학습된 LLM을 사용하여 텍스트를 출력(디코드)하는 데는 다양한 방식이 존재하며, 기본적인 방식으로 Greedy Decoding, Beam Search, Random Sampling, Top-K / Top-P Sampling 등이 있고, 그 외에도 다수의 방식이 제안되어 있다. 발전적인 예로 Contrastive Decoding이 있는데, 이는 전문가 모델과 아마추어 모델(통상 더 적은 파라미터 수)을 이용해 확률밀도비를 취하고 거기서부터 샘플링을 수행하여, 전문가 모델의 출력을 강조하고 아마추어 모델의 출력을 감소시키도록 생성하는 방식이다. 외부 모델을 사용하는 이 방식은 생성 품질을 높이는 효과적인 수단이다.

### 메타 제너레이션: 추론 시 연산의 대규모 스케일

메타 제너레이션(Meta-Generation)은 토큰 수준의 디코딩을 넘어 문장이나 단락 단위로 생성 과정을 평가하고 생성 프로세스 전체를 최적화하는 개념이다. Snell 등은 이를 세 가지 범주로 정리했다. 어느 쪽이든 추론 시에 연산량이 크게 스케일된다.

첫째, 병렬 탐색(Parallel Search)은 병렬로 여러 후보를 생성하여 스코어링이나 다수결 등으로 생성물을 선택하는 방식이다. Best-of-N은 N개의 답변을 내어 스코어가 가장 높은 것을 선택하며, 스코어 함수는 태스크에 따라 LLM 스코어, 학습한 평가기, BLEU 등 특정 지표 등 임의로 선택할 수 있다. Self-Consistency는 LM에 복수의 추론을 수행시켜 다수결(Majority Voting)로 정답을 고른다. MBR Decoding(Minimum Bayes-Risk Decoding)은 기계 번역에서 쓰이는 방식으로 효용 함수(BLEU, METEOR, BLEURT, COMET 등)를 이용해 출력의 품질을 최대화하도록 디코딩한다. 이 외에도 집계 방식(aggregation type)과 스코어링 기법에 따라 다양한 알고리즘이 존재한다.

둘째, 단계별 탐색(Step Level Search)은 중간 결과를 단계별로 평가하여 생성물을 선택하는 방식이다. 토큰 수준의 Beam Search와 달리 문장이나 단락 단위로 샘플링과 평가를 수행하며, 평가에는 Process Reward Model(PRM)을 이용하고 Top-N Sampling으로 중간 결과를 선택한다. Tree-of-Thought(ToT)는 복수의 사고열을 단번에 출력하여 평가하는 Self-Consistency와 달리 도중에 분기를 시키는 트리 탐색 방식이며, 노드의 평가도 LM으로 수행한다. Game of 24(주어진 4개의 숫자를 사칙연산하여 24를 만들기)와 같이 전략적 사고가 필요한 태스크에서 성능이 대폭 개선되었다. 탐색 방법이나 검증하는 스텝의 차이 등에 의해 다양한 알고리즘이 존재한다.

셋째, 정제(Refinement)는 한 번 생성한 결과나 그 결과에 대한 피드백을 바탕으로 재생성하는 방식이다. Self-Refine은 자기 자신을 사용하여 피드백을 생성하고 출력을 개선하며, 7개의 태스크에서 최대 50% 가까운 정확도 향상을 보였다. 외부나 내부의 피드백 결과를 이용하여 반복적으로 생성 결과를 갱신한다.

### 추론 시 스케일링의 효과

Lightman 등의 연구는 평가 방식의 차이가 성능에 미치는 영향을 보여준다. Outcome-supervised Reward Model(ORM)을 사용하여 출력 전체를 평가하는 Best-of-N(ORM)은 다수결로 선택하는 Majority Voting보다 우수하며, Process-supervised Reward Model(PRM)을 이용해 도중의 가정을 평가하는 Best-of-N(PRM)은 더욱 우수하다.

Snell 등은 같은 컴퓨팅 자원일 때 파라미터를 늘리는 것보다 추론 시 연산을 스케일하는 것이 더 효과적일 수 있음을 보였다. 랜덤 샘플링에 의한 추론 횟수를 늘리고 PRM을 이용해 추론 경로와 최종 답변을 적절히 선택함으로써 성능이 향상된다.

## 정리

이 장에서는 언어 모델의 스케일 법칙을 중심으로 다음을 살펴보았다.

첫째, 스케일 법칙이 무엇인지를 설명했다. 스케일 법칙은 컴퓨팅 자원(C), 데이터셋 크기(D), 파라미터 수(N)와 오차(L) 사이에 성립하는 경험칙으로, 로그 그래프 상에서 거의 직선 관계가 성립한다.

둘째, 스케일 법칙의 구체적인 구하는 방법을 설명했다. 스케일 법칙을 구하기 위해서는 기본적으로 몇 가지 다른 설정에서 실험을 수행하고 피팅한다. 하이퍼파라미터 설정(종횡비, 학습률, 배치 크기 등)에 대해서는 다양한 지견이 논문으로 발표되어 있으며, μTransfer 같은 전이 방법도 존재한다.

셋째, 추론 시의 스케일링을 설명했다. 학습 시뿐만 아니라 추론 시에도 연산량을 스케일시킴으로써 성능을 개선할 수 있으며, 추론 시의 방법은 프롬프팅, 디코딩, 메타 제너레이션의 세 수준으로 정리된다.

## 참고문헌

- [3] Kaplan+. Scaling Laws for Neural Language Models. 2020. arXiv:2001.08361
- [4] Wei+. Emergent Abilities of Large Language Models. 2022. arXiv:2206.07682
- [5] Schaeffer+. Are Emergent Abilities of Large Language Models a Mirage?. 2023. arXiv:2304.15004
- [6] Power+. Grokking: Generalization Beyond Overfitting on Small Algorithmic Datasets. 2022. arXiv:2201.02177
- [7] Liu+. Towards Understanding Grokking: An Effective Theory of Representation Learning. 2022. NeurIPS2022
- [8] Hestness+. Deep Learning Scaling is Predictable, Empirically. 2017. arXiv:1712.00409
- [9] Brown+. Language Models are Few-Shot Learners. 2020. NeurIPS2020
- [10] Anil+. PaLM 2 Technical Report. 2023. arXiv:2305.10403
- [11] Henighan+. Scaling Laws for Autoregressive Generative Modeling. 2020
- [12] Ganguli+. Predictability and Surprise in Large Generative Models. 2023. arXiv:2202.07785
- [13] OpenAI. GPT-4 Technical Report. 2023. arXiv:2303.08774
- [42] Hoffmann+. Training Compute-Optimal Large Language Models. 2022. NeurIPS2022
- [43] de Vries. Go smol or go home, Why we should train smaller LLMs on more tokens. 2023
- [47] Bahdanau. The FLOPs Calculus of Language Model Training. Medium. 2022
- [50] Sardana+. Beyond Chinchilla-Optimal: Accounting for Inference in Language Model Scaling Laws. 2024. ICML2024
- [51] Dey+. Cerebras-GPT: Open Compute-Optimal Language Models Trained on the Cerebras Wafer-Scale Cluster. 2023. arXiv:2304.03208
- [52] Yang+. Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer. 2022. NeurIPS2022
- [53] OpenAI. Learning to reason with LLMs. OpenAI Blog. 2024
- [54] Madaan+. From Decoding to Meta-Generation: Inference-time Algorithms for Large Language Models. 2024. arXiv:2406.16794
- [55] Li+. Contrastive Decoding: Open-ended Text Generation as Optimization. 2023. ACL2023
- [56] Snell+. Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters. 2024. arXiv:2408.03314
- [57] Eikema+. On the True Distribution Approximation of Minimum Bayes-Risk Decoding. 2020. EMNLP2020
- [58] Wang+. Self-Consistency Improves Chain of Thought Reasoning in Language Models. 2023. ICLR2023
- [59] Lightman+. Let's Verify Step by Step. 2023. ICLR2024
- [60] Yao+. Tree of Thoughts: Deliberate Problem Solving with Large Language Models. 2023. NeurIPS2023
- [61] Madaan+. Self-Refine: Iterative Refinement with Self-Feedback. 2023
- [62] Tatsunori Hashimoto, Percy Liang. CS336: Language Modeling from Scratch. Stanford University. 2024
- [66] AI@Meta+. The Llama 3 Herd of Models. 2024
- [67] Wei+. Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. 2022
- [68] Agarwal+. Many-Shot In-Context Learning. 2024

---

라이선스: CC BY-NC-ND 4.0 (저작자표시–비영리–변경금지 4.0 국제)
원저작권자: 도쿄대학교 마츄오·이와사와 연구실
