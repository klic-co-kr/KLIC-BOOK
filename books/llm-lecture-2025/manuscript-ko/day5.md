# Day 5 — 발전적인 사전학습

대규모 언어 모델 강좌 2025 · 2025/10/29
야마다 이쿠야(山田育矢) — Studio Ousia 최고 과학자, 나고야대학 수리·데이터 과학·인공지능 교육연구센터 객원 교수, 도호쿠대학 언어 AI 연구센터 특임 교수(객원). 다양한 언어 모델의 개발과 국제 콘테스트(NeurIPS EfficientQA 2020 2위, ISWC Challenge 2020 1위, NIPS HCQA 2017 1위 등) 수상 경력이 있으며, 저서로 『대규모 언어 모델 입문』 시리즈와 『딥러닝에 의한 자연어 처리』가 있다.

본 자료는 도쿄대학교 마쓰오·이와사와 연구실이 작성한 강좌 강의 자료이며, 크리에이티브 커먼즈 CC BY-NC-ND 4.0(저작자표시–비영리–변경금지 4.0 국제) 라이선스로 제공된다.

## 이번 장의 목표

본 장은 제3회 「사전학습」의 속편으로, 언어 모델을 스케일(대규모화)하여 사전학습하는 과정에서 등장하는 발전적인 화제를 다룬다. 사전학습은 LLM 개발 파이프라인의 첫 단계에 자리 잡고 있으며, 이후의 사후학습(post-training) 전체의 품질을 좌우하는 토대가 된다.

학습 목표는 세 가지다. 첫째, 모델을 스케일하여 사전학습할 때 발생하는 과제를 설명할 수 있을 것. 둘째, 그 과제에 대응하는 발전적인 방법들을 설명할 수 있을 것. 셋째, 사전학습의 일련의 흐름을 모델 스케일 기술까지 포함하여 코드로 구현할 수 있을 것. 강의에서는 각 요소의 스케일에 따른 문제와 해결 기술을 살피고, 연습에서는 PyTorch로 트랜스포머 모델을 사전학습하는 일련의 흐름(데이터 준비, 전처리, 스케일 기술을 적용한 학습)을 구현한다.

## 사전학습의 중요도와 스케일 법칙

사전학습이 LLM 개발에서 어느 정도의 비중을 차지하는가. 한 가지 참고가 되는 것은 GPT-4의 각 개발 태스크에 투입된 인원 비율이다. 이를 OpenAI가 생각하는 LLM 개발에서의 중요도 비율로 해석해 보면, 사전학습 관련 태스크가 전체에서 상당한 몫을 차지함을 볼 수 있다. 그러면서도 "사전학습을 직접 수행할 필요가 있을까?"라는 질문은 여전히 유효하다. 대부분의 실무에서는 공개된 사전학습 모델을 출발점으로 삼지만, 도메인 특화 모델이나 최첨단 모델을 직접 만들려면 결국 사전학습 단계까지 직접 설계해야 하기 때문이다.

이런 투자가 정당화되는 근거가 스케일 법칙(scaling law)이다. 스케일 법칙은 언어 모델을 대규모화함으로써 성능이 향상되는 관계를 가리키는 경험칙으로, 성능(L)이 컴퓨팅 자원(C), 데이터셋 크기(D), 파라미터 수(N)의 세 요소와 맺는 관계로 정식화된다. 이 법칙은 다양한 도메인에서 대규모 모델을 개발할 장점이 확인되었고, 그 결과 대규모 모델에 대한 투자 리스크가 크게 경감되었다. 성능 예측이 가능해졌기 때문에, 자원을 들이면 그에 상응하는 성능 향상을 기대할 수 있게 된 것이다.

## 스케일화의 세 가지 과제

파라미터, 계산량, 데이터를 스케일하면 스케일 법칙에 따라 성능이 올라가는 것은 사실이지만, 스케일화 과정에는 세 가지 구조적 과제가 뒤따른다.

첫째, 계산량(C)의 확보다. 모델이 스케일됨에 따라 충분한 계산량과 메모리 용량을 갖추고 효율적으로 훈련할 필요가 있다. 모델 크기가 커지면 GPU 자원 요구량이 가파르게 증가하며, 단순히 자원을 늘리는 것만으로는 비용이 감당할 수 없는 수준에 이른다. 효율적으로 대규모 모델을 훈련할 수 있다면 그만큼 비용을 줄일 수 있다.

둘째, 파라미터 수(N)의 비용이다. 모델이 스케일됨에 따라 증가하는 비용을 억제해야 한다. 여기서 특히 치명적인 것이 트랜스포머의 self-attention 구조다. self-attention에서는 시퀀스 길이 n의 제곱에 비례하는 계산량과 메모리가 필요하다. 각 토큰이 다른 모든 토큰과의 연관성을 계산하기 때문에, 모든 토큰의 조합에 대해 계산을 수행하고 그 값을 기억해야 한다. 시퀀스가 길어질수록 이 비용은 제곱으로 불어난다.

셋째, 데이터(D)의 한계다. 성능을 발휘하기 위한 학습용 데이터를 준비해야 하는데, 양질의 언어 데이터는 사실상 2024년경에 고갈될 것으로 예측된다. 과거 웹 데이터의 증가 추세와 학습 데이터의 증가 추세를 외삽한 연구(Villalobos et al., 2022)가 이 예측의 근거가 되며, 이는 스케일 법칙에 기대어 모델을 키우는 전략 자체에 장기적 제약이 있음을 의미한다.

이 세 가지 과제에 대응하기 위해 본 장에서는 파라미터(N), 계산량(C), 데이터(D) 각각에 대한 접근을 차례로 살핀다.

## 파라미터(N) 효율화: Efficient Attention과 혼합 전문가

파라미터 수와 관련된 과제에 대응하는 방향은 두 갈래다. 하나는 self-attention 자체의 계산·메모리 효율을 개선하는 것이고, 다른 하나는 계산 비용을 팽창시키지 않으면서 모델의 파라미터를 늘리는 것이다. 전자를 Efficient Attention, 후자를 혼합 전문가(Mixture of Experts, MoE)라 부른다.

### Efficient Attention의 계보

Sparse Transformer(Child et al., 2019)는 attention을 계산하는 위치를 한정함으로써 계산량을 삭감한다. 계산하지 않는 위치는 마스크 처리하여 희소(sparsely)하게 attention을 수행하는데, 어텐션 기구를 두 번 통과시키면 모든 토큰에 어텐션이 도달하도록 설계되어 있다. 이를 통해 이미지나 음성처럼 매우 긴 시퀀스 길이의 입력에 대해서도 트랜스포머를 효율적으로 이용할 수 있게 된다.

Big Bird(Zaheer et al., 2020)는 다수의 희소한 attention을 조합하여 attention을 근사함으로써 긴 시퀀스에 대응한다. 긴 시퀀스를 다루는 질의응답 및 요약 등의 태스크에서 좋은 성능을 획득했으며, 유사한 아이디어로 Longformer(The Long-Document Transformer, 2020)가 있다.

FlashAttention(Dao et al., 2022)은 방향을 달리한다. attention의 계산은 연산 자체가 아니라 메모리 I/O에 병목이 있다는 점을 지적한 것이다. 입력 행렬을 잘게 분할하여 계산함으로써, 시퀀스 길이 × 시퀀스 길이의 attention 행렬 전체에 대한 메모리 읽기/쓰기를 회피한다. 처리를 가능한 한 GPU SRAM 안에서 완결시켜 저속인 GPU HBM 메모리로의 액세스 횟수를 줄이고, fused kernel 구현의 최적화를 통해 대폭적인 속도 향상을 달성했다. 예컨대 GPT-2에서는 최대 7.6배의 가속을 보고한다.

FlashAttention-2(Tri Dao, 2023)는 여기에 세 가지 구현 공법을 더해 고속화한다. 첫째, 알고리즘을 공략하여 행렬 연산 이외의 연산을 될 수 있는 대로 삭감한다. GPU는 행렬 연산에 전용 연산 유닛이 있어 고속히 처리할 수 있기 때문이다. 둘째, 배치나 attention의 헤드뿐만 아니라 시퀀스 방향으로도 병렬 연산을 수행하여, 배치나 헤드 수가 적은 경우에도 고속화할 수 있도록 한다. 셋째, 워프(동시에 실행되는 스레드 그룹을 가리키는 GPU 용어)를 query 행렬에서 분할함으로써 워프 간 동기 및 통신을 줄이고 병렬성을 향상시킨다. 그 결과, FlashAttention 대비 약 2배, PyTorch 표준 attention 대비 최대 9배의 고속화를 달성했다.

### 혼합 전문가(Mixture of Experts)

MoE는 계산 비용을 팽창시키지 않고 모델 파라미터를 늘리는 접근이다. 다수의 전문가(각각이 신경망)를 준비해 두고, 입력 값에 따라 일부 전문가에만 포워드한다. 모든 파라미터를 사용하는 것은 아니므로 계산량을 억제할 수 있다. 엄밀히 말하면 어느 전문가에게 할당할지를 결정하기 위한 작은 신경망(라우터 신경망)이 추가로 필요하므로 그 만큼 약간의 계산량은 증가하지만, 전체적으로는 파라미터 대비 계산량을 크게 줄일 수 있다.

실험적으로 계산량을 억제하면서 퍼포먼스를 개선할 수 있음이 확인되었다. 동일한 계산량으로 학습한다는 제약 하에서, MoE를 사용한 모델이 사용하지 않은 통상 모델보다 퍼포먼스가 높다. 유출 정보에 따르면 GPT-4는 MoE 모델 구조를 채택하고 있다고 하며, 최근 DeepSeek, Qwen 등 다수의 오픈 모델도 MoE를 채택하고 있다. 복잡한 분류 문제에 MoE를 적용하면, 라우터 신경망이 데이터의 클러스터 중심점을 기준으로 각 사례를 전문가에 할당하고, 각 전문가는 그 클러스터 내에서의 분류에 특화하는 학습이 수행됨이 시각화(t-SNE)를 통해 확인되었다.

Switch Transformer(Fedus et al., 2021)는 T5 모델의 피드포워드 층에 MoE를 적용하여 대규모화한 1조 6000억 파라미터 모델이다. 다수의 MoE에서는 각 토큰마다 복수의 전문가가 사용되지만, 이를 하나의 전문가만 사용하도록 단순화하여 통신·계산 비용의 삭감을 실현했다. 그 결과 1.6조 파라미터 모델의 학습에서 T5-XXL 모델에 대해 4배의 사전학습 스피드업을 달성했다.

DeepSpeed-MoE(Rajbhandari et al., 2022)는 최적화된 구현을 통해 MoE 모델의 학습 효율을 개선한다. 자기회귀 모델에서 품질이 동등한 Dense 모델과 비교하여 약 5배의 학습 비용 삭감을 실현했다. 같은 연구에서 제안된 PR-MoE는 모델 크기를 줄이면서 성능을 유지하는 아키텍처다. 각 토큰이 1개의 고정된 MLP와 1개의 전문가 양쪽을 이용하고, 트랜스포머의 후반 층에서 보다 많은 전문가를 활용하도록 설계되었다. 그 결과 표준적인 MoE보다 적은 파라미터 수로 동등한 성능을 달성했다(350M 모델에서는 1/3 이하의 파라미터로, 1.3B 모델에서는 표준 MoE의 약 60% 파라미터로 동등 성능).

MoE 모델에도 스케일 법칙은 성립한다(Clark et al., 2022). 전문가 수를 늘리면 로그 손실이 내려가지만, 특히 큰 모델 크기에서는 너무 많이 늘리면 효과가 약해진다. MoE 모델의 파라미터 수을 여러 요소를 가미하여 통상 모델의 파라미터 수로 환산하면 스케일 법칙이 성립한다. 다만 통상 모델의 파라미터 수가 커지면 MoE화의 효과는 비례하여 낮아지므로, 모델 크기에 적합한 전문가 수를 선택하는 것이 바람직하다.

## 계산량(C) 효율화: 병렬화와 양자화

계산량의 과제에는 두 방향이 있다. 훈련 시에는 복수의 GPU를 효율적으로 활용하는 병렬 계산이 필요하고, 추론 시(주로)에는 모델의 경량화를 통해 소규모 GPU 환경에서의 운용을 가능하게 하는 양자화가 필요하다.

### 병렬 계산

딥러닝의 병렬화는 여러 축으로 전개된다. 데이터 병렬, 파이프라인 병렬, 텐서 병렬이 그 축들이며, 전문가 병렬은 MoE 모델에 특화된 추가 축이다.

ZeRO(ZeRO: Memory Optimizations Toward Training Trillion Parameter Models, Rajbhandari et al., 2019)는 데이터 병렬 시의 메모리 효율화 기법이다. 어느 요소를 메모리에서 병렬화하는가에 따라 세 단계의 동작 모드를 갖는다. Stage 1, Stage 2, Stage 3로 단계가 진행될수록 메모리를 삭감할 수 있지만, 통신 오버헤드가 증가한다. 대표적인 라이브러리인 DeepSpeed를 통해 환경 설정(config)을 기술하는 것만으로 이용할 수 있다.

3D 병렬화는 병렬화 전략마다 통신 오버헤드가 다르다는 점을 적극 활용한다. 통신 오버헤드는 텐서 병렬이 파이프라인 병렬보다 훨씬 크다(텐서 병렬 ≫ 파이프라인 병렬). 이 특성을 이용해 GPU·노드의 배치에 따라 통신 비용을 억제하며 병렬화를 구성한다. 예를 들어 4개의 GPU를 가진 8노드로 3D 병렬화를 구성할 때, 고 오버헤드의 텐서 병렬은 노드 내에 배치하고, 저 오버헤드의 파이프라인 병렬은 노드를 가로질러 배치하며, 데이터 병렬과 ZeRO Stage 1의 조합으로 GPU 메모리 효율을 높인다.

전문가 병렬화(expert parallelism)는 MoE 모델 전용의 병렬화 기법이다. MoE의 각 전문가를 다른 GPU에 배치한다. 행렬을 분할하여 복수의 GPU가 보유하는 텐서 병렬과 유사하지만, 모든 층에 적용되는 텐서 병렬화와 달리 전문가 층에만 적용된다는 차이가 있다.

### 양자화

양자화(quantization)는 모델 파라미터의 데이터 타입을 부동소수점(Float 형)에서 정수(Int 형)로 변환하여 연산 처리를 수행하는 기법이다. 추론 시 필요 메모리량을 삭감할 수 있지만, 단순히 이를 수행하면 성능 저하가 발생한다. 그래서 정밀도 저하를 억제하는 다양한 공법이 연구되었다.

LLM.int8()(Dettmers et al., 2022)는 성능 저하 없이 가능한 양자화 방법이다. 16비트 행렬 곱셈에서 이상치의 특징을 분리하는 혼합 정밀도 분해(mixed-precision decomposition)를 수행하여, 대부분의 값을 8비트로, 이상치만을 16비트로 표현한다. 구체적으로는 세 단계를 거친다. 첫째, 입력된 은닉 상태로부터 열 단위로 이상치(임계값보다 큰 값)를 추출한다. 둘째, 이상치 행렬에 대해서는 FP16인 채로 행렬 연산을 수행하고, 이상치가 아닌 행렬에 대해서는 INT8로 변환(양자화)하여 행렬 연산을 수행한다. 셋째, INT8의 출력 값을 FP16으로 되돌려 두 개의 출력 값을 가산하여 FP16으로 출력 값을 반환한다. 그 결과 16비트 대비 약 50%의 메모리 삭감이 가능하며, 175B까지의 파라미터를 가지는 LLM에서 성능 저하 없이 추론을 수행할 수 있음을 경험적으로 보였다.

k-bit 스케일 법칙(Dettmers et al., 2023)은 모델의 메모리 용량(비트 수)을 고정했을 때 모델의 크기와 양자화를 어떻게 설정해야 하는가를 묻는다. 예를 들어 30B의 8-bit 모델과 60B의 4-bit 모델은 동일한 메모리 용량이 된다. 메모리 용량을 고정한 경우 4-bit 양자화가 가장 제로샷 성능이 높았고, 3-bit에서는 모델 크기가 커지면 성능이 불안정해진다. 즉 post-hoc 양자화에서는 4-bit가 사실상의 최소 필요 조건으로 보인다.

양자화가 LLM의 중요한 특성인 Emergent Ability를 상실시키지 않는가 하는 우려도 검증되었다(Liu et al., 2023). in-context learning, chain-of-thought reasoning, instruction-following의 세 가지 능력을 계측한 결과, 4비트까지의 양자화 모델에서는 Emergent Ability의 유지가 확인되었다.

BitNet(Wang et al., 2023; Ma et al., 2025)는 훈련 시부터 1bit/1.58bit 양자화를 수행하는 접근이다. 양자화를 적용한 모델을 사전학습하여 구축하며, attention과 MLP에 포함되는 선형 층을 모두 1bit용으로 확장된 선형 층(BitLinear)로 치환한다. 파라미터를 2치({-1, +1}; 1bit) 또는 3치({-1, 0, +1}; 1.58bit)로 나타내며, 동일한 비트 수(메모리 용량)로 비교했을 때 기존 LLM의 성능을 크게 능가했음을 보고했다.

## 데이터(D) 효율화: 품질, 양, 그리고 한계

데이터의 과제는 다시 두 갈래로 나뉜다. 하나는 성능을 발휘하기 위한 학습용 데이터를 어떻게 준비할 것인가(데이터셋 정비)이고, 다른 하나는 데이터셋의 품질을 어떻게 개선할 것인가(데이터 전처리)이다.

### 학습 데이터의 구성과 도메인 특화

어떤 학습 데이터로 학습해야 하는가라는 물음에 대해, 주요 모델의 학습 데이터 구성이 참고가 된다. 한 가지 뚜렷한 경향은 최근 모델이 많은 케이스에서 코드(code) 학습을 수행하고 있다는 점이다. GPT-3는 코드 학습을 포함하지 않았으나, 코드로 학습한 모델(예: code-davinci-002)은 GPT-3보다 추론 성능이 좋다. ChatGPT도 code-davinci-002를 베이스로 학습되어 있다고 간주된다.

특정 도메인 데이터에 의한 지속적 사전학습(continual pre-training)도 효과적이다(Cossu et al., 2022). 사전학습 후에 특정 도메인의 문서(예: arXiv 논문 요지)를 지속적으로 학습시키는 방식이다. 사전학습 후에 지속 학습함으로써 치명적 망각(catastrophic forgetting)이 일어나기 어려운 데다가, 다운스트림 태스크에서 뛰어난 성능을 발휘할 수 있음이 확인되었다.

### 최적의 자원 할당: Chinchilla와 그 너머

LLM의 사전학습 예산은 계산량(GPU 수나 시간)에 비례한다. 따라서 주어진 계산량을 파라미터 수(N)와 학습 데이터량(D)에 어떻게 할당하는가가 중요해진다. OpenAI의 종래 스케일 법칙(Kaplan et al., 2020)은 파라미터에 대해 필요로 하는 학습 데이터량의 견적이 너무 적다는 점이 지적되었고, 이에 대응한 것이 Chinchilla다(Hoffmann et al., 2022). Chinchilla는 모델 크기를 70B(Gopher의 약 1/4)로 줄이는 대신 데이터 크기를 1.4T 토큰(Gopher의 약 4.6배)까지 늘려, 다수의 케이스에서 Gopher에 승리하며 제안한 관계식의 타당성을 시사했다.

다만 Chinchilla 법칙에도 비판이 있다. "Chinchilla Trap"이라 불리는 지적은 Chinchilla의 최적 모델 크기(70B)가 여전히 커서 추론 비용이 높다는 점을 지적하며, 추론 비용까지 고려하면 더 작은 모델을 대규모 데이터로 훈련해야 한다는 의견이다(de Vries, 2023). 분석에 따르면 Chinchilla 최적인 모델 크기의 40~60% 이내의 모델 크기로, 10~42%의 계산량 추가만으로 동일 성능의 모델을 학습할 수 있다고 한다.

### 언어 데이터 고갈과 지식 습득의 메커니즘

한편 언어 데이터의 고갈 문제는 여전히 현실적 과제다. 앞서 인용한 Villalobos et al.(2022)의 예측에 따르면 양질의 언어 데이터의 고갈이 예측되고 있으며, 이는 스케일 법칙 기반의 성장 전략에 장기적 제약이 될 수 있다.

이 맥락에서 사전학습을 통해 지식이 어떻게 학습되는가를 조사한 연구(Chang et al., 2024)가 시사하는 바가 크다. LLM 사전학습 시에 지식이 어떻게 획듄되어 가는지를 추적한 결과, 지식을 서술한 문장이 출현할 때마다 올바른 지식이 생성되는 확률이 높아지며 지식이 점차 학습되어 간다. 반면 지식이 출현하지 않는 스텝(예: 900스텝 이후)에서는 망각되어 간다. 이는 LLM에게 지식을 가르치기 위해서는 훈련 데이터 중에 반복해서 지식이 출현할 필요가 있음을 의미하며, 중요한 지식이 높은 밀도로 포함되는 고품질 훈련 데이터의 중요성을 시사한다.

### 합성 데이터와 유한 데이터 설정

데이터 고갈에 대한 하나의 대응이 합성 데이터(synthetic data)다. Kang et al.(2025)는 합성 데이터를 사용한 사전학습의 효과를 1,000개 이상의 LLM을 10만 GPU 시간을 사용하여 훈련해 검증했다. 검증한 합성 데이터의 종류는 두 가지다. 하나는 웹 바꾸어말하기(paraphrasing)로, LLM을 사용하여 웹 데이터를 깨끗한 텍스트(HQ) 또는 QA 형식으로 바꾸어말하기하는 것이다. 다른 하나는 합성 교과서(TXBK)로, LLM을 사용하여 교과서 스타일의 데이터를 0부터 작성하는 것이다. 결과는 분명했다. 웹 데이터와 합성 데이터를 섞은 경우에 훈련의 효율이 대폭 개선된 반면, 합성 데이터만으로 훈련하면 성능이 악화되었고 특히 합성 교과서만으로는 현저히 악화되었다. 모든 종류에서 웹 데이터에 33% 비율로 합성 데이터를 섞은 경우에 최선의 성능을 달성했다.

데이터가 유한하고 계산량이 무한한 설정에서의 학습도 검토되었다(Kim et al., 2025). LLM 사전학습에 투입되는 계산량은 해마다 늘어나고 있으나 데이터는 한정되어 있다. 데이터량이 유한하다는 것을 전제로 계산량을 스케일할 때 성능을 개선할 수 있는가? LLM의 표준적인 훈련 설정에서는 스케일할 수 없다. 에포크 수를 늘리면 오버피팅으로 성능이 저하되고, 모델의 크기를 늘리면 충분히 훈련하지 못해 역시 성능이 저하된다. 그러나 훈련 설정을 적절히 조정하면 스케일할 수 있다. 큰 모델일수록 작은 학습률, 적은 에포크 수, 큰 weight decay(강한 정규화)를 적용하는 것이 효과적이다.

### 데이터 전처리: RefinedWeb과 FineWeb-Edu

데이터 전처리 공법의 대표적 사례가 RefinedWeb(Penedo et al., 2023)이다. 웹 데이터만으로 5T 토큰의 데이터셋을 구축했고 그중 600GB를 공개했다. 필터링의 공법 등에 의해 종래보다 대규모 데이터를 구축한 것이다.

핵심은 Macrodata Refinement라는 엄밀한 좁혀내기 파이프라인이다. 복수의 필터링과 중복 제거를 조합하여 데이터를 엄밀하게 좁혀내며, 일련의 파이프라인에서 CommonCrawl 중 약 90%의 문서가 제거된다. 구체적인 단계는 다음과 같다. URL filtering(유해한 URL로부터 취득한 텍스트 배제), Text extraction(헤더나 광고 부분을 제외하고 메인 콘텐츠 텍스트만 추출), Language identification(특정 언어 텍스트만 남김), Repetition removal(텍스트 내 반복문 배제), Document-wise filtering(스팸 텍스트 필터링), Line-wise corrections(행 레벨 필터, 예: SNS의 "좋아요"), Fuzzy deduplication(MinHash 기반 유사 문장 배제), Exact deduplication(지정한 토큰 수 이상의 완전 일치 배제).

FineWeb-Edu(Penedo et al., 2024)는 LLM이 평가한 텍스트의 교육적 가치를 사용해 전처리를 수행한다. 대규모 텍스트에 LLM의 추론을 직접 적용하는 것은 비용이 높기 때문에 경량화가 필요한데, 46만 건의 웹 기사의 "교육적 가치"를 LLM에 평가시켜 훈련 데이터를 작성한 뒤, 작은 모델을 학습시켜 평가기를 만든다. 그 결과 전처리 이전의 데이터(FineWeb)나 기존 데이터(Matrix)와 비교해 지식이나 추론이 필요한 태스크의 성능이 크게 개선되었다.

## 정리

본 장에서는 모델의 스케일을 뒷받침하는 기술 동향을 살폈다. 왜 모델을 스케일시키는가에 대한 답은 스케일 법칙의 성립과 Emergent Ability의 발현에서 찾을 수 있다. 스케일 법칙은 모델의 성능과 {파라미터 수, 데이터량, 계산량}의 관계를 밝혔으며, 이로 인해 성능 예측이 가능해지고 대규모 모델에 대한 투자 리스크가 경감되었다.

그러나 스케일화에는 여전히 과제가 존재한다. 스케일에 수반하여 필요로 하는 비용의 증가와 데이터의 부족 등이 그것이다. 이에 대응하여 파라미터 수(N) 측면에서는 보다 메모리·연산 효율이 뛰어난 모델(Efficient Attention, MoE)의 제안이, 계산량(C) 측면에서는 효율적인 학습·추론 방법(병렬화, 양자화)의 정비가, 데이터셋 크기(D) 측면에서는 데이터의 양과 질의 공법(Chinchilla 법칙, 합성 데이터, 정밀 전처리)의 축적이 각각 진행되고 있다. 세 축 모두에서 스케일 법칙이라는 단일한 원리를 실용화하기 위한 다층적 연구·개발이 이어지고 있는 셈이다.

## 참고문헌

[2] Zhao et al. A Survey of Large Language Models. 2023. arXiv:2303.18223.
[3] Kaplan et al. Scaling Laws for Neural Language Models. 2020. arXiv:2001.08361.
[4] Wei et al. Emergent Abilities of Large Language Models. 2022. arXiv:2206.07682.
[14] Abhinav Venigalla, Linden Li. Billion-Parameter GPT Training Made Easy. MosaicML.
[15] Vaswani et al. Attention Is All You Need. 2017. NeurIPS2017.
[17] Villalobos et al. Will we run out of data? An analysis of the limits of scaling datasets in Machine Learning. 2022. arXiv:2211.04325.
[19] Child et al. Generating Long Sequences with Sparse Transformers. 2019. arXiv:1904.10509.
[20] Zaheer et al. Big Bird: Transformers for Longer Sequences. 2020. NeurIPS2020.
[21] Dao et al. FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness. 2022. NeurIPS2022.
[22] Tri Dao. FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning. 2023. arXiv:2307.08691.
[23] Chen et al. Towards Understanding Mixture of Experts in Deep Learning. 2022. NeurIPS2022.
[25] Fedus et al. Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity. 2021. arXiv:2101.03961.
[26] Rajbhandari et al. DeepSpeed-MoE: Advancing Mixture-of-Experts Inference and Training to Power Next-Generation AI Scale. 2022. ICML2022.
[27] Clark et al. Unified Scaling Laws for Routed Language Models. 2022. arXiv:2202.01169.
[32] Microsoft DeepSpeed Team. DeepSpeed: Extreme-scale model training for everyone. Microsoft.
[33] Rajbhandari et al. ZeRO: Memory Optimizations Toward Training Trillion Parameter Models. 2019. arXiv:1910.02054.
[37] Dettmers et al. LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale. 2022. NeurIPS2022.
[38] Liu et al. Do Emergent Abilities Exist in Quantized Large Language Models: An Empirical Study. 2023. arXiv:2307.08072.
[39] Penedo et al. The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Data, and Web Data Only. 2023. arXiv:2306.01116.
[40] Daisuke Okanohara. MinHash에 의한 고속 유사 검색. Preferred Networks R&D, 2011.
[41] Cossu et al. Continual Pre-Training Mitigates Forgetting in Language and Vision. 2022. arXiv:2005.09357.
[42] Hoffmann et al. Training Compute-Optimal Large Language Models. 2022. NeurIPS2022.
[43] Harm de Vries. Go smol or go home, Why we should train smaller LLMs on more tokens. 2023.
[55] NVIDIA. NeMo Framework User Guide — Parallelisms.
[56] Dettmers et al. The case for 4-bit precision: k-bit Inference Scaling Laws. 2023. arXiv:2212.09720.
[57] Wang et al. BitNet: Scaling 1-bit Transformers for Large Language Models. 2023. arXiv:2310.11453.
[58] Ma et al. BitNet b1.58 2B4T Technical Report. 2025. arXiv:2504.12285.
[59] Kang et al. Demystifying Synthetic Data in LLM Pre-training: A Systematic Study of Scaling Laws, Benefits, and Pitfalls. 2025. arXiv:2510.01631.
[60] Chang et al. How Do Large Language Models Acquire Factual Knowledge During Pretraining?. 2024. arXiv:2406.11813.
[61] Kim et al. Pre-training under infinite compute. 2025. arXiv:2509.14786.
[62] Penedo et al. The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale. 2024. arXiv:2406.17557.
[65] weights & biases. LLM을 제로부터 트레이닝하기 위한 베스트 프랙티스.
[66] iwiwi. github gist, https://gist.github.com/iwiwi/fc174b1f2341c2c0170be87c5b2e1d31.
