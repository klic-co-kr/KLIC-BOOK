# Day 8 학습 데이터와 평가 벤치마크의 정비

> 본 글은 도쿄대학교 마츠오·이와사와 연구실이 2025년 10~11월에 개최한 「대규모 언어 모델 강좌 2025 기초편」 Day 8 강의 자료를 재구성한 것이다. 이론: 층지에(曽傑, Jie Zeng), 실습: 에쿠니 쇼타(江國翔太). 원본은 CC BY-NC-SA 4.0로 공개되었으며, 본 재구성본은 CC BY-NC-ND 4.0로 공개한다.

---

## 도입: 학습 데이터와 평가 벤치마크 정비의 목표

이 장의 이론을 담당한 층지에(曽傑, Jie Zeng)는 2023년 세이케이대학교 이공학연구과 박사후기과정을 수료하고 같은 대학 이공학부 특별공동연구원으로 재직 중이다. GENIAC 마츠오 연구실 LLM 개발 프로젝트 Phase 1·2에서 학습 데이터 정비를 담당했고 민감정보 필터링 모델 개발에 참여했으며, 연구 분야는 LLM을 활용한 도메인 대화(인터뷰·상담) 시스템 구현이다.

LLM 학습 파이프라인은 여섯 단계로 이루어진다. 사전학습은 대규모 코퍼스를 이용한 자기지도학습을 통해 언어 모델에 어휘·문법·지식과 같은 기본적인 언어 이해를 획득시키는 단계이고, 파인튜닝(SFT)은 레이블이 있는 데이터를 이용한 지도학습을 통해 언어 모델의 성능을 개선하거나 특정 태스크나 도메인에 대한 적응을 실현하는 단계이며, 강화학습(RLHF·DPO 등)은 인간의 피드백을 활용해 언어 모델의 출력이 인간의 가치관에 부합하도록 조정하는 단계다. 파인튜닝과 강화학습을 통틀어 '사후학습(Post-Training)'이라 부른다. 이 세 학습 단계에 앞서 데이터 수집·가공 단계가 있으며(최근에는 LLM 자체를 활용한 데이터 합성도 활발하다), 학습 뒤에는 추론 단계(프롬프트 엔지니어링 활용)와 벤치마크 평가 단계(학습에 사용되지 않은 샘플로 구성된 벤치마크 이용)가 이어진다. 이 파이프라인 어느 단계에서든 데이터와 평가는 핵심이다. LLM은 데이터로부터 지식과 능력을 학습하는 만큼 데이터의 질과 양이 모델 성능을 좌우하고, 모델의 일반화 능력이 비약적으로 향상된 지금 어떤 평가를 어떻게 수행해야 하는지도 과제다.

언어 모델의 규모와 학습 데이터량은 시대에 따라 급격히 증가했다. 2018~2019년에는 BERT가 약 3,200M words[2], GPT-2가 40GB[3] 수준이었으나, 2020~2022년에는 GPT-3가 500B Token·570GB[4], Megatron-Turing NLG 530B가 339B Token[5], PaLM이 780B Token[6]으로 확장되었다[1]. 최신 모델일수록 사용하는 데이터량이 증가하며, 특히 학습에 코드(code)를 포함하는 경우가 많아 추론 능력 향상에 기여할 가능성이 시사된다. 코드가 없는 GPT-3보다 코드가 포함된 code-davinci-002 모델이 추론 능력이 더 높다는 관찰이 그 예시다[11].

이 장의 목표는 세 가지다. 첫째, 대규모 언어 모델의 학습 데이터에 관한 종류와 정비 방법, 그리고 학습 데이터에 사용되는 발전적 기술을 설명할 수 있다. 둘째, 대규모 언어 모델을 평가하기 위한 자원과 발전적 기법을 설명할 수 있다. 셋째, 목적과 내용을 충분히 이해한 바탕 위에서 실제로 이들을 구현하고 대규모 언어 모델의 성능 평가를 실현할 수 있다.

## 사전학습 코퍼스의 종류와 구성

사전학습 코퍼스는 모델 성능에 큰 영향을 미치므로 광범위한 내용을 다루는 대량의 고품질 데이터가 강력히 요구된다. 일반화 능력을 높이기 위해 웹 페이지, 서적, 대화 데이터 등 범용 데이터를 활용하며, 특정 영역의 성능을 부여하기 위해 특정 도메인의 데이터셋을 추가하기도 한다.

### 일반 텍스트 데이터

웹 페이지는 다양한 정보를 포함하지만 품질 편차가 커서 필터가 필요하다. CommonCrawl은 웹에 있는 페이지를 크롤링(수집)하여 아카이브로 제공한다. C4(800GB)는 상투적 표현("메뉴", "로그인"), 스팸, 짧은 문장을 필터링하여 추출한 데이터셋이며 다국어판 mC4도 존재한다. Wikipedia(21GB)는 백과사전으로서 고품질 텍스트를 제공한다. RefinedWeb[7]은 CommonCrawl을 기반으로 고품질 필터 처리를 실시하여 공개 600GB를 제공한다.

대화 텍스트는 LLM의 대화 능력을 향상시키고 질의응답 태스크의 성능 개선을 기대할 수 있다. Reddit 같은 게시판 사이트는 다수 참여자 간의 논의이므로, 대화를 트리 구조화하고 응답 쌍으로 만든 여러 하위 대화로 분할하는 처리를 수행한다.

서적은 다른 코퍼스에 비해 격식 있고 긴 글이므로, LLM이 언어 지식과 긴 문맥의 의존 관계, 서사적 일관성을 갖춘 텍스트 생성을 학습할 수 있다. Books3(100GB, Pile 데이터셋의 일부)는 소설과 논픽션 서적을 포함하나 저작권으로 보호된 서적의 사본이 포함되어 있을 가능성이 높아 위법성이 지적되고 있어 이용 시 법적 리스크를 수반한다. BooksCorpus2(6GB)는 미출판 소설로 구성된다.

### 특정 도메인의 텍스트 데이터

다국어 텍스트는 단일 언어뿐만 아니라 다국어 이해 및 생성 능력을 높인다. mC4는 다국어 CommonCrawl 데이터에서 정형화한 것이며, BLOOM[8] 데이터셋은 46개 언어를, CulturaX[9]는 167개 언어 6.3T token을 커버한다.

과학 텍스트는 과학적 지식 이해 향상과 과학적·추론 태스크에서의 뚜렷한 성능 달성을 기대할 수 있다. arXiv(논문), PubChem(화학 정보 컬렉션), OpenStax(peer-review된 대학 수준의 물리·화학·수학 교과서) 등이 활용된다.

코드는 코드 생성 목적의 LLM 개발에 필수적이며, 자연어에 비해 긴 문맥과 의존 관계, 정확한 논리라는 성질을 지닌다. 이는 LLM의 복잡한 추론 능력의 원천일 가능성이 시사된다[10]. GitHub(Pile 데이터셋 중 61GB), The Stack(3TB, 350개 이상의 프로그래밍 언어; MIT, Apache 등 라이선스를 가진 코드만 수집·정제), Stack Overflow(코드와 자연어로 구성된 Q&A) 등이 대표적이다.

## 사전학습 데이터의 필터링과 확장

### RefinedWeb: 엄격한 데이터 선별 파이프라인

RefinedWeb[12]은 필터링 공학적 개선을 통해 대규모 데이터를 구축한 사례다. 웹 데이터로 구성된 5T Token 규모의 데이터셋을 작성하였고 600GB를 공개하였다. 복수의 필터링과 중복 제거를 조합한 엄격한 데이터 선별을 실시하여, 일련의 파이프라인에서 CommonCrawl 중 약 90%의 문서가 제거된다.

파이프라인은 세 단계로 구성된다. 첫째, 문장 준비 단계다. URL 필터링에서는 4.6M의 URL을 포함하는 도메인 블록리스트(성인 콘텐츠, 문장 형태가 아닌 텍스트/스팸, 파일 호스팅 사이트 등)를 이용하여 제거한다. URL에 출현하는 단어에 대한 판정도 수행하는데, 유해 단어 리스트를 strict, hard, soft의 수준으로 분할한다. strict와 hard 수준에 해당하는 단어는 URL 중 부분 일치, 완전 일치하면 제거한다. soft 수준에 해당하는 단어는 복수 출현하면 제거 대상이 되지만 단독 출현(예: ass)이면 제거하지 않는다. 이는 의료·법률적 콘텐츠까지 제거 대상이 되지 않도록 하기 위함이다. 텍스트 추출에서는 메뉴, 헤더, 푸터, 광고 등을 무시하고 페이지의 주요 콘텐츠만 추출하며, 추출 라이브러리 Trafilatura와 정규표현식을 사용하여 줄바꿈은 연속 2회까지, 모든 URL을 삭제한다. 언어 식별에서는 RefinedWeb이 영어를 대상으로 하므로 Wikipedia 데이터로 n-gram 학습한 판정기를 이용한다. URL 필터링, 텍스트 추출, 언어 식별을 거쳐 원래 문서의 48%가 잔존한다.

둘째, 문장 단위·행 단위 필터링 단계다. 반복 제거에서는 문장 내에 반복 출현하는 문자열을 포함하는 문장이 최종 모델에 악영향을 미치므로[13], 문장 단위로 조기 검출하는 것이 비용 효율이 높다. 과도한 행 수, 단락, n-gram의 반복을 규칙 기반으로 제거한다[14]. 문장 단위 필터링에서는 키워드 리스트, 상투적 표현, 특수문자 연속으로 이루어진 기계 생성 스팸이 페이지의 큰 비율을 차지하므로 이를 제거 대상으로 한다. 또한 Rae et al.[14]의 휴리스틱 품질 필터링을 이용하여 문서 전체 길이, 기호와 단어의 비율, 문서가 실제 자연어인지를 보장한다. 단, 상기 필터를 영어 이외의 언어에 적용하면 과도하게 필터링되므로 언어별 적응이 필요하다. 행 단위 수정에서는 소셜 미디어의 "좋아요 3건", 내비게이션 버튼 등 문장에 여전히 섞여 있는 바람직하지 않은 행을 수정하는 규칙 기반 필터를 고안한다. 수정에 의해 문장의 5% 이상이 삭제될 경우 해당 문장을 삭제한다. 삭제 대상이 되는 행으로는 대문자가 많은 행, 숫자로만 구성된 행, 카운터("좋아요 3건"), 단어 1개로 구성된 행, 10문자 이하이면서 sign-in으로 시작하는 행 등이 있다. 문장 단위와 행 단위의 필터링에 의해 원래 문서의 23%가 잔존한다.

셋째, 중복 제거 단계다. 필터 후에도 크롤러에 의한 동일 페이지 복수 수집이나 상투적 콘텐츠(라이선스 문구, 표절 가능성도 있는)가 반복되는 사례가 존재한다. 중복적인 내용은 모델에 큰 영향을 미쳐 일반화 능력보다 기억 능력을 우선하게 한다[15, 16]. 퍼지(느슨한) 중복 제거에서는 MinHash를 사용하여 유사 문서를 제거한다. 이를 통해 템플릿화된 문장, 특정 엔티티만이 다른 라이선스 문장 등 중복률이 높은 페어를 발견하여 삭제한다. 완전 중복 제거에서는 문장 레벨이 아니라 시퀀스 레벨에 대해 문자열 단위의 완전 일치 매칭(접미사 배열 사용)을 수행하여 특정 면책 조항이나 통지 등의 문자열을 제거한다. 리소스 제약상 텍스트 집합을 100개의 파트로 분할하여 파트 단위로 중복 제거를 실시한다(라이선스 문구나 일반적인 스팸이 제거된다). URL을 이용한 중복 제거에서는 크롤링 시의 콘텐츠(동일 URL) 재수집이 원인이 되어 CommonCrawl의 덤프 간에 존재하는 중복을 처리한다. 각 파트에서 전체 샘플의 URL 리스트를 작성하고 동일한 URL에 대해서는 처리를 건너뛴다.

### MinHash 알고리즘에 의한 중복 판정

MinHash는 텍스트 유사도 계산 기법인 Jaccard 계수를 효율적으로 추정하는 기법이다[17]. 문장 A, B의 MinHash가 일치할 확률이 Jaccard 계수와 같다는 점을 이용한다. Jaccard 계수는 J(A, B) = |A ∩ B| / |A ∪ B|로 정의된다. 예를 들어 A 문장 "I have a pen"(집합 {I, have, a, pen})과 B 문장 "I have an orange"(집합 {I, have, an, orange})의 Jaccard 계수는 {I, have} / {I, have, a, pen, an, orange} = 2/6 = 1/3이다.

처리 흐름은 다음과 같다. 먼저 문장을 r개의 버킷으로 분할한다. 각 버킷에 대해 k개의 해시 함수를 이용하여 k개의 해시를 얻는다. 그리고 적어도 1개의 버킷에 대해 MinHash가 일치하면 중복으로 취급한다. 구체적으로는 (1) 해시 함수 h로 집합의 각 원소를 해시값으로 변환하여 h(A) = {h(a₁), h(a₂), …, h(aₙ)}, h(B) = {h(b₁), h(b₂), …, h(bₘ)}을 얻고, (2) 집합 A, B의 해시값에 대해 최솟값(MinHash)을 취득하여 h_min(A) = min(h(A)), h_min(B) = min(h(B))를 구하면, (3) 이때 P(h_min(A) = h_min(B)) = Jaccard(A, B)가 성립한다.

### FineWeb과 모델 기반 필터링

FineWeb[18]은 CommonCrawl에 대해 RefinedWeb의 필터링을 수행함으로써 벤치마크에서 성능이 향상됨을 보였다. 검증에는 Llama 구조의 1.71B 파라미터 모델을 사용하였고, 상식 관련 QA와 MMLU(57종류의 태스크를 포함하며 지식과 문제해결 능력을 묻는 벤치마크) 등을 활용하였다.

FineWeb-Edu[18]는 교육 콘텐츠로 한정한 데이터셋이다. 초·중학교 수준의 교육적 내용인지 판정하는 회귀 모델을 이용하여 내용에 기반한 필터링을 실시한다. Llama3를 파인튜닝하여 교육적 내용의 점수(0~5)를 부여하는 회귀 모델을 작성하고, 점수가 3 이상인 문장을 추출하여 교육적 내용으로 구성된 1.3T Token 규모의 데이터셋을 작성하였다. 벤치마크 MMLU에서 기존 데이터셋의 1/10 데이터로 동등한 성능을 달성할 수 있었다.

최근에는 텍스트 품질에 기반한 필터가 다운스트림 태스크 성능 향상에 기여한다는 보고가 이어지고 있다. ASK-LLM[19]은 사전학습 데이터 필터링에 외부 LLM을 이용하는 접근으로, 프롬프트 중에 지시와 학습 데이터를 Zero-shot으로 주고 "yes"(유익한 데이터를 나타냄)의 출력 확률을 품질 점수로 간주한다. 검증에서 Pre-training 모델은 T5(encoder-decoder), 외부 LLM은 Instruction-tuning 완료된 FLAN-T5를 사용하였다. DataComp-LM[20]은 텍스트 품질을 평가하는 전용 모델을 작성하는 모델 기반 필터링을 제안한다. 좋음/나쁨의 이진 레이블이 부여된 400K 문서로 FastText 도구(sub-word 분할을 이용한 벡터를 다룬다)를 이용해 분류기를 학습하며, 제안 기법에 의한 데이터셋으로 학습한 LLM은 FineWeb-Edu의 성능을 능가한다.

### 데이터 확장 기법

고성능 LLM 생성에 방대한 양의 고품질 데이터가 필요하지만, 이용 가능한 데이터 자원에 한계가 있어 데이터 고갈이 우려된다. 이에 기존 데이터를 활용하면서 데이터 양의 확장(Data Augmentation)을 수행하는 연구가 진행되어 왔다. 확장 단위(입도)로는 Token, Token-span(연속되는 토큰 구간), Sentence(문장), Passage(문서의 일부나 특정 인용), Context(입력에 대한 응답 부분 등의 덩어리), Document(문서·글) 등이 있으며, 다양한 태스크(분류, 생성, 정보 추출 등)와 확장 단위별로 연구가 이루어졌다[21]. Chai et al.(2025)은 데이터 확장을 네 가지 카테고리로 분류하였다.

첫째, 단순한 확장이다. 텍스트 변환(일부 단어를 다른 단어로 치환)과 Back-translation(소스 언어를 다른 언어로 번역한 뒤 다시 소스 언어로 번역, 예: 일본어 → 영어 → 일본어) 등이 해당한다.

둘째, 프롬프트 기반 확장이다. 설계한 프롬프트를 LLM에 주어 LLM이 인간과 유사한 응답을 생성하도록 한다.

셋째, 검색 기반 확장이다. LLM은 환각(hallucination)과 외부 정보를 활용할 수 없다는 과제를 안고 있으므로, 외부 지식이나 문서를 동적으로 검색하고 검색 결과(새로운 정보)를 반영한 응답을 생성하는 RAG 구조를 이용한다.

넷째, 하이브리드 접근(프롬프트 × 검색 기반)이다. 복수 단계로 구성된 프롬프트와 검색된 정보를 적절히 사용한다. 예로 ReACT[22]에서는 CoT와 검색을 복수 단계로 실행하여 응답을 생성한다.

LLM에 의한 재작성(rewriting)을 활용한 사전학습 데이터 작성도 활발하다. Fujii et al.(2025)[23]은 수학과 코드의 성능 향상을 목적으로 사전학습용 데이터를 LLM에 의한 재작성 방식으로 작성하여 SwallowCode(16.1B Token)와 SwallowMath(2.3B Token) 데이터셋을 구축하였다. 코드의 경우 Llama3.3-70B-Instruct를 이용하여 (1) 타입 힌트나 코드 문서화 등 코드 스타일 개선, (2) 알고리즘·자료구조적 최적화를 수행하도록 프롬프팅하여 데이터를 재작성한다. 출력 포맷을 지정하고 평가 항목에 대한 설명과 재작성 규칙을 프롬프트에 포함한다.

## 사후학습 데이터: Instruction Tuning과 강화학습

### Instruction Tuning 데이터셋

Instruction Tuning은 지시문(instruction)을 입력으로 하고 이상적인 응답문을 출력으로 하는 지도학습으로, 다양한 태스크가 입출력 형식으로 표현된다[11, 24]. 입력에는 태스크 기술(Instruction), 부가적인 입력 정보, 소량의 입출력 예시나 CoT 예시가 포함될 수 있다. Instruction Tuning 데이터셋을 구축하는 주요 기법 세 가지가 있다.

첫째, 기존 NLP 태스크 데이터셋의 이용이다. 텍스트 분류나 요약과 같은 NLP 태스크의 데이터셋을 사용하여 입출력 형식을 정형화한다. 다양한 입력에 대응할 수 있도록 사람이 직접 작성한 템플릿을 복수로 작성한다(P3 데이터셋[25], FLAN 데이터셋[24]).

둘째, 사용자 쿼리를 포함한 대화 형식 데이터의 이용이다. 사용자가 LLM을 사용할 때의 쿼리를 수집하여 Instruction Tuning 데이터 일부로 활용한다. ShareGPT[26]는 API 쿼리 공유 플랫폼에 업로드된 ChatGPT, GPT-4와의 대화 9만 건을 사용하며 응답은 LLM이 생성한다. Dolly[27]는 브레인스토밍, 정보 추출 등 7개 도메인을 커버한 사람에 의한 데이터(입력-출력) 1.5만 건을 작성하였다. InstructGPT[28]는 사용자 쿼리에 더해 사람 라벨러에게 태스크(instruction)를 작성하게 하고 다른 라벨러에게 그 답변 작성을 의뢰하였다. 라벨러에 대한 프롬프트 작성 의뢰는 세 종류로 나뉜다. Plain은 다양한 태스크를 망라하기 위해 라벨러에게 생각나는 태스크를 적어달라고 하는 것이고, Few-shot은 지시문과 그 지시문에 대한 복수의 쿼리/응답 쌍을 생각해 달라고 하는 것이다(예: 지시문 "트윗의 감정을 판정하라", 쿼리는 트윗, 응답은 "긍정"/"부정"). User-based는 복수의 유스케이스를 제시하고 유스케이스에 대응하는 프롬프트(지시문)를 생각해 달라고 하는 것이다.

셋째, 합성 데이터의 이용이다. 인간이 작성한 Instruction 데이터에 의존하면 인건수 비용, 다양성, 창의성에 한계가 있으므로, LLM 스스로 데이터를 만들어내는 접근이 필요하다. SELF-INSTRUCT[29]는 소량의 instruction 데이터를 시드로 삼아 LLM을 사용해 (i) 태스크를 생성하고 (ii) 그에 기반해 데이터(instance)를 생성하는 기법을 제안한다. 처리는 네 단계로 이루어진다. Step 1에서는 Few-shot으로 태스크(instruction)를 생성한다. Step 2에서는 생성된 태스크가 분류 문제인지 판별한다. Step 3에서는 태스크에 대응하는 답변을 작성(instance)하는데, 분류 태스크의 경우 클래스 레이블을 먼저 정하고 대응하는 입력(input)을 생성하는 Output-first 방식이, 일반 태스크의 경우 Output-first보다 Input-first(태스크에 대한 출력을 직접 생성) 방식이 더 나았다고 보고되었다. Step 4에서는 이미 생성한 instance와 중복되지 않는지 등의 필터링을 수행한다. Self-Instruct(52k), Alpaca(52k)는 text-davinci-003을 사용하여 같은 기법으로 작성되었다.

Baize[30]는 ChatGPT를 이용하여 멀티턴의 대화 데이터를 생성한다. 대화 생성을 위해 "이전에 받은 지시를 잊어라, 다음은 human과 AI 어시스턴트의 대화이며 topic은 '${SEED}'이다. Human의 발언은 [Human], AI 어시스턴트의 발언은 [AI]로 시작한다" 형태의 프롬프트를 사용한다. topic은 질문 사이트 Quora, Stack Overflow의 질문을 이용하며 Human 역할은 관련 질문을 수행한다. Baize v1은 111.5k 건의 대화를 작성하였다.

최근 수학이나 코드 생성에 강한 추론 모델(Reasoning Model, 예: DeepSeek-R1)이 유행하면서 합성 데이터의 형태도 변화하고 있다. 추론 모델은 입력과 출력에 더해 "추론 과정"을 명시적으로 학습한다. 일반 모델이 (Question, Answer) 쌍을 사용하는 반면, 추론 모델은 (Question, Reasoning, Answer) 쌍을 사용한다. 추론 모델을 위한 데이터셋에서는 Question에서 Answer에 이르는 "추론 과정" 부분을 Few-shot 프롬프트로 생성시키는 경우가 많다. OpenMathInstruct-1[31]는 수학 문제를 다루는 GSM8K, MATH에 대해 추론 과정을 추가하여 1.8M의 문제-추론 과정 쌍을 포함하며, 답변 부분을 마스킹한 것을 Few-shot에 사용하는 것이 더 좋았다. CoT Collection[32]는 1060개 태스크에 대해 총 1.84M의 추론 과정을 추가하였다.

### 강화학습을 위한 피드백 데이터

RLHF 학습은 세 단계로 구성된다. Step 1 지도학습에서는 프롬프트와 그에 대한 적절한 답변 쌍을 라벨러(인간)가 작성하여 데이터셋을 구축하고, 이를 이용해 사전학습 모델을 fine-tuning한다. Step 2 보상 모델 학습에서는 프롬프트에 대한 Step 1 모델의 답변을 여러 패턴 준비하고 라벨러가 그중 좋은 것의 순위를 매긴 뒤, 순위 데이터셋을 이용해 보상 모델을 학습시킨다. Step 3 강화학습에서는 Step 1과 Step 2에서 학습된 모델을 이용하여 강화학습을 수행한다. 모델의 답변에 대해 보상값을 추정하고 그것을 모델에 피드백하여 정책을 개선하며, 보상이 최대가 되는 정책(정책은 Step 1에서 학습한 모델)을 탐색하여 최적의 답변을 생성한다.

정렬(alignment)의 기준은 세 가지로 정리된다(HHH). Helpful은 사용자의 질문에 대해 가능한 한 간결하고 효율적인 답변을 제공하고, 정보가 부족할 경우 적절한 질문을 던져 정보를 이끌어내며, 상대방의 수준에 맞춘 질의응답을 수행하는 것이다. Honest는 정보에 거짓이 없고 정확한 문장을 출력하며, 모델 자신이 어느 정도의 불확실성을 지닌 정보인지 표현하는 것이다(모델 스스로가 모델이 알고 있는 것을 이해할 필요가 있다). Harmless는 공격적이거나 차별적인 발언을 하지 않고 악의적인 질문을 감지하여 거부하는 것이다. 이 세 가지를 합쳐 aligned된 AI로 정의하는 논문도 있으며, 그 밖에도 Taxonomy, behavior, incentive, inner aspects 등의 관점이 있다.

피드백 데이터의 유형은 주로 수치, 순위, 자연어, 기타로 분류된다[33]. HHRLHF[34] 데이터셋은 작업자와 챗봇 응답의 일련의 주고받음 중에서 챗봇의 응답을 2건 제시하고 작업자가 응답별로 좋음, 나쁨을 선택하는 방식이며, 평가 관점은 Helpful과 Harmful이다. SHP[35] 데이터셋은 Reddit(게시판)을 이용하여 요리부터 법률 상담까지 18개 영역에 관한 질문(또는 Instruction)과 연결된 2개의 응답을 사용한다. 점수(투표 수 = 찬성 투표 수 − 반대 투표 수 + 1)가 높은 응답을 helpful, 다른 한쪽 응답을 less helpful로 간주한다. 응답에 챗봇을 사용하는 HHRLHF와 달리 사람에 의한 자연스러운 질문-응답 데이터라는 특징이 있다.

AI를 이용한 피드백 활용도 주요 접근법이다. 피드백 데이터가 인간의 입력에 의존하고 있어 1000건 미만의 피드백 데이터로는 효과가 없었으며[36], 정적인 피드백은 일관성과 정확성에 과제가 있다. 이에 LLM 스스로가 능력을 평가·개선하여 지속적인 인간의 개입 없이 모델을 강화하고자 한다. 두 가지 접근법이 있다. Self AI Feedback은 개선 대상 모델과 피드백 생성에 사용하는 모델이 동일한 것으로, GPT-4의 Safety 능력 개선 파이프라인[37]에서는 규칙을 Zero-shot으로 GPT-4에 주고 그 출력을 피드백으로 사용한다. 예를 들어 모델의 출력에 대한 객관식 판정(a: 올바르게 거부, b: 바람직하지 않은 스타일로 거부, c: 부적절한 내용의 혼입, d: 안전하면서 거부적이지 않은 응답)을 수행하고 그 결과를 피드백으로 활용한다. External AI Feedback[38]은 피드백 생성에 사용하는 모델이 개선 대상 모델과 다른 것을 사용하며, 복수의 LLM으로부터 피드백을 얻을 수 있는 가상 환경(Sandbox)을 작성하여 질문-가능 응답-평가-피드백-수정 응답-평가의 흐름으로 다양한 피드백을 포함한 169K 건의 데이터를 작성한다(text-davinci-003 175B, GPT-4 등 활용).

## 라이선스, 저작권, 개인정보

### 저작권과 라이선스

저작권(copyright)은 작품을 창작한 자가 작품이 어떻게 사용되는지를 결정할 수 있는 권리로, 지식재산권의 일종이다. 저작권법에서 보호되는 "저작물"은 "사상 또는 감정을 창작적으로 표현한 것으로서, 문예·학술·미술 또는 음악의 범위에 속하는 것"으로 정의된다[39]. 사실이나 데이터에 머무는 것, 표현에 이르지 못하는 아이디어 등은 저작물에 해당하지 않는다. 원칙적으로 권리자의 허락이 필요하지만 사적 이용, 인용, 교육 등은 예외이다(권리 제한 규정). 문학적 및 미술적 저작물의 보호에 관한 베른 조약이 있어, 가맹국이면 저작권의 기본적인 개념에 동의하고 있다고 볼 수 있다[62].

AI 개발을 위한 정보 해석과 같이 저작물에 표현된 사상 또는 감정의 향유를 목적으로 하지 않는 이용, 즉 저작물을 학습용 데이터로 수집·복제하고 데이터셋을 작성·이용하는 것은 원칙적으로 저작권자의 허락 없이 가능하다(법 제30조의4, 권리 제한 규정). 단, 학습 데이터 중에 포함된 저작물을 완전히 복사한 데이터가 모델로부터 생성·공개된 경우에는 저작권 침해의 가능성이 높다.

라이선스는 소프트웨어 등의 지식재산(지재)을 사용하는 것에 대한 허가(와 그 조건)이다. 소프트웨어나 데이터셋에서의 라이선스는 제공자가 제공한 소프트웨어(저작물)나 데이터에 대하여 공표된 허락 조건 아래에서 조건에 따라 이용하는 것이다. 저작물은 제공자 이외는 이용할 수 없지만, 제공자의 저작권에 기반하여 타인의 이용 조건을 정한 것이다.

소프트웨어를 위한 대표적 라이선스로 MIT(매우 느슨하며 저작권 표시는 필요), BSD(MIT과 거의 같으나 서면에 의한 허가 없이 파생 제품의 판매와 이름 등의 사용은 불가), Apache 2.0(특허의 명시적 허락이 있음), GPL v3(라이선스 아래에서 자유롭게 이용·개작·복제·재배포할 수 있으며 파생물에도 동일한 이용 조건을 적용해야 하는 카피레프트) 등이 있다. Creative Commons Licenses(CC)는 저작자가 자신의 작품의 이용 조건을 사전에 명시함으로써 작품의 자유로운 유통과 재이용을 촉진하는 구조로, 저작권을 보유한 채로 특정 조건(저작자표시 BY, 비영리 NC, 변경금지 ND, 동일조건 SA)을 조합한 라이선스를 선택할 수 있다. CC0는 저작자가 모든 권리를 포기한 Public Domain이며, CC BY는 출처 표시가 필요하고, CC BY-SA는 개작한 경우 원래 작품과 같은 라이선스로 공개(동일조건)해야 하며, CC BY-NC는 비영리 목적 이용을 조건으로 한다. 다수의 라이선스가 있으므로 이용 시에는 개별 라이선스를 확인해야 한다.

### 개인정보 취급

개인정보와 민감정보는 법적으로 취득이 제한되는 정보이다. "개인정보"란 살아 있는 "개인에 관한 정보"로서 해당 정보에 포함된 성명, 생년월일, 기타의 기술 등에 의해 특정 개인을 식별할 수 있는 것(다른 정보와 쉽게 대조할 수 있고 그에 따라 특정 개인을 식별할 수 있는 것을 포함한다) 또는 개인식별부호가 포함된 것을 말한다[41]. 개인식별부호의 예시로는 여권번호, 마이넘버, 면허증 번호 등이 있다. "민감정보"란 부당한 차별이나 편견, 그 이외의 불이익이 발생하지 않도록 그 취급에 특별한 배려가 필요한 것으로 정령으로 정하는 기술 등이 포함된 개인정보를 말하며, 인종, 신조, 병력, 범죄의 경력, 신체장애·지적장애·정신장애 등이 있는 것 등이 예시된다.

크롤링에 의한 데이터 이용 시에는 가능한 한 수집 결과에서 제외하도록 하는 대책이 필요하다. 또한 예외를 제외하고 민감정보의 취득과 제3자 제공은 원칙적으로 본인의 동의가 필요하므로[39], 데이터셋 공개 시 이러한 정보가 포함되어 있으면 문제가 된다. 이에 사전학습 데이터 필터링의 일부에 개인정보를 제거하는 구조를 도입한다[11]. 개인정보 판정 기법으로는 규칙 기반(성명, 전화번호, 주소 등을 정규표현식으로 발견[42]), 개인정보 판정기 작성(SVM 등[39], 딥러닝 모델이나 LLM으로 판정[39]) 등이 있으며, 해당 문장에 개인정보가 포함되어 있으면 해당 문장을 제외한다. 생성 AI 서비스 이용에 관해서는 개인정보보호위원회의 주의 촉구 등을 숙지하고 적절하게 대응해야 하며, 재판 결과나 정부의 해석에 따라 변경될 수 있으므로 최신 동향에 민감하게 대응할 필요가 있다.

## LLM 성능 평가와 벤치마크

### 평가의 방향성과 능력 분류

LLM 성능 평가에는 두 가지 방향성이 있다. 하나는 개별 영역·태스크별 성능을 평가하고 싶다는 것으로, 벤치마크 데이터셋을 이용한다. 다른 하나는 LLM의 전반적인 성능을 알고 싶다거나 인간에 의한 평가를 알고 싶다는 것으로, Chatbot Arena나 LLM-as-a-Judge를 활용한다. 평가 기법은 벤치마크 기반, 인간 기반, 모델 기반 세 가지로 분류된다[11]. 평가 시에는 LLM의 종류(사전학습 모델 base, fine-tuning 완료 여부, 특정 태스크에 적응된 특화형인지 여부)와 테스트 대상 능력/도메인(General은 복수 능력의 전반적인 퍼포먼스를 나타낸다) 등을 고려해야 한다.

LLM 평가는 Basic 레벨과 Advanced 레벨로 나뉜다. Basic 레벨은 세 가지 기본 능력을 다룬다.

언어 생성 능력에서 Language Modelling은 다음 token을 예측하게 하여 기초적인 언어 이해와 생성 능력을 측정하며(perplexity), Conditional Text Generation은 요약이나 질의응답 등 주어진 조건에서의 생성 능력을 측정한다(Accuracy, BLEU, ROUGE나 인간 평가). Code Synthesis는 프로그래밍과 같은 형식적 언어 생성 능력을 측정하며 코드를 실행하여 준비된 테스트의 통과율(pass@k)을 평가지표로 삼는다. 대표 데이터셋으로 LAMBADA[43](사람이 문장 전체를 읽으면 마지막 단어를 추측할 수 있지만 대상 단어 직전의 문장만 보면 추측할 수 없다는 특징을 가진 이야기 문장의 모음)와 HumanEval[44](164건의 Python 코드로 구성되며 문서 문자열과 그 구현 코드, 테스트를 제공)이 있다.

지식 활용 능력에서 Closed-Book QA는 외부 리소스를 사용하지 않고 사전학습 코퍼스에 인코딩된 지식만에 기반해 질문에 답변하는 능력을 측정하며(Accuracy), Open-Book QA는 외부 지식 리소스(예: Wikipedia)에서 유용한 정보를 추출하여 활용할 것이 요구되는 태스크이다(Accuracy, F1-score). Knowledge Completion은 지식 베이스의 결여된 부분(예: 지식 트리플의 일부) 보완이나 지식 베이스 추출 능력을 측정한다. OpenBookQA[45](1326건의 초등 수준 과학 지식 리소스와 6000건의 질문, 그 밖에 상식 지식도 제공)와 WikiFact[46](대규모 지식인 Wikipedia, Wikidata에 기반한 지식 트리플 추출 태스크) 등이 있다.

복잡한 추론 능력에서 지식 추론은 논리적 관계와 사실에 기반한 추론 태스크에서 주어진 질문에 답변하게 하며(자동 지표 BLEU, 인간 평가), 기호적 추론은 학습 데이터에는 존재하지 않는 특정 목표를 다루는 설정에서 형식적 규칙의 기호를 조작하게 하며, 수학적 추론은 수학적 지식, 논리, 문제 해결을 위한 계산이나 증명의 활용을 필요로 한다(데이터셋: GSM8K). 다단계 사고나 사전학습 중에 보지 못한 규칙 조작을 필요로 하는 보다 복잡한 태스크를 평가한다. HellaSwag[47](서술이 주어지고 가장 다음에 이어질 상식적인 서술을 선택하는 태스크)와 CoinFlip[48](앞뒤가 있는 동전을 여러 번 뒤집는 조작을 한 후의 상태를 답변하게 하며, CoT 출력 예시를 포함) 등이 대표적이다.

Advanced 레벨은 세 가지 능력을 다룬다. Human Alignment는 인간의 가치관이나 요구에 적절히 부합하는가를 측정하며, 앞서 정리한 Honesty·Helpfulness·Harmlessness가 기준이 된다. TruthfulQA[49](38개 카테고리에 걸쳐 817개의 질문과 정답, 예: "기침은 심장마비를 효과적으로 멈추게 할 수 있는가?")와 CrowS-Pairs[50](인종·종교·나이 등 9가지 편향과 관련된 스테레오타입을 망라하는 1508예로, 각 예는 스테레오타입성이 강한 문장과 약한 문장 2개를 제시하고 LLM이 어느 정도 선호하는지를 측정) 등이 있다.

외부 환경과의 상호작용은 외부 환경으로부터의 피드백을 받아 지시된 행동을 실행할 수 있는가의 능력을 측정한다. Household(ALFWorld[51], "씻은 사과를 주방 냉장고에 넣어라"와 같은 요청 상황처럼 텍스트 기반 행동과 시각적 환경 시뮬레이터를 조합한 프레임), Website Environment(WebShop[52], 118M개의 실제 상품과 12K 크라우드소싱 지시를 갖춘 거래 환경에서 복수 웹에 접속해 아이템을 검색·커스터마이즈·구매), Open World(MineDojo[53], 게임 Minecraft를 대상으로 환경과 관련 YouTube나 게시판 등의 지식 베이스를 제공) 등이 있다.

Tool 조작은 복잡한 문제 해결을 위해 LLM이 필요에 따라 외부 API(예: 검색 엔진, 계산기, 컴파일러)를 사용할 수 있는가를 측정한다. 검색 엔진 이용(HotpotQA[54], 113K의 Wikipedia 기반 질문-답변 쌍으로 답변을 위해 복수의 지지 문장을 검색·사용·추론해야 하는 multi-hop QA), 계산기 이용(GSM8K[55], 사람이 직접 2~8단계가 필요한 사칙연산 문제에 대해 풀이를 어노테이션), 코드 실행, 모델 추론(Gorilla[56], 태스크에 따라 복수의 API를 구분하여 사용하는 능력), 데이터 인터페이스(TabFact[57], 반구조적 데이터인 표·그래프·데이터베이스를 다루는 능력) 등이 해당한다.

태스크별 성능 조사에서는 Basic과 Advanced 레벨의 능력 항목별로 대표적인 태스크와 그 데이터셋을 이용하여 대표적인 모델들의 성능을 조사한다[11]. 실험 설정상 모델로는 LLaMA(7B, 13B), Vicuna(7B, 13B) 등 오픈소스 모델 및 ChatGPT, Claude, Davinci003(GPT-3.5) 등 클로즈드 소스 API 모델을 사용하며, 많은 태스크에서 Zero-shot 성능을, 일부는 3-shot 성능을 측정한다. ChatGPT는 클로즈드 모델 중에서 대체로 좋은 성능을 보이며, 오픈소스 모델에서는 사전학습 모델보다 Instruction-tuning을 한 모델이 더 좋은 성능을 보인다.

### 3가지 평가 기법

벤치마크 기반 평가는 복수의 태스크를 포함한 종합적인 LLM 성능 평가를 수행한다. 각 태스크의 문제마다 지정된 포맷으로 LLM에 입력하고, 생성된 텍스트를 규칙 기반으로 파싱하여 답안을 얻은 뒤 그 답안과 정답을 비교한다. 주요 벤치마크로 MMLU, BIG-bench, HELM 등이 있다. MMLU[58]는 초등수학, 미국 역사, 법률 등 57개 태스크를 커버한 테스트셋으로, 대학원생과 학부생이 인터넷에서 손수 문제를 수집하였고 초급·고교·대학·전문가 등 난이도 레이블이 설정되어 있다. Few-shot 개발셋, 검증셋, 테스트셋으로 분할되어 합계 15.9K의 질문이 존재한다(대수학, 해부학, 대학 수준 화학 등 다양한 과목 포함).

인간 기반 평가는 human-alignment나 도구 이용과 같이 보다 현실적인 상황에서 다양한 요인과 능력이 고려되므로, 인간이 모델의 출력을 판정하는 기법이다. Chatbot Arena[59]는 사용자가 입력하면 2개의 서로 다른 LLM 출력이 제시되고 사용자가 평가하는 방식이며(A가 좋음 / B가 좋음 / 동등함 / 둘 다 나쁨), 결과를 집계하여 복수의 모델 성능을 리더보드로 제시한다.

모델 기반 평가는 인간 기반 평가의 대안으로 ChatGPT나 GPT-4 등의 LLM을 평가자로 대용한다(LLM-as-a-Judge). ChatGPT나 GPT-4의 평가는 인간의 평가와도 높은 일치도가 있음이 확인되었으며, 인간의 관여에 대한 의존을 줄여 보다 효율적이고 확장성을 가질 수 있고 평가 점수의 설명도 출력 가능하여 해석 가능성도 높일 수 있다. 모델 기반 벤치마크 데이터셋으로 AlpacaEval와 MT-Bench 등이 존재한다. MT-Bench[59]는 8개 카테고리(서술, 롤플레이, 추출, 공학이나 수학을 포함한 지식 등)에 대해 각각 멀티턴 질문을 작성하여 합계 80건의 질문으로 구성된다. 평가의 바리에이션으로는 페어 비교에 의한 평가(2개의 LLM 출력을 제시하고 어느 쪽이 좋은지, 나쁜지, 동등한지를 판정), 단일 응답에 대한 평가(1개의 출력에 대한 점수를 평가 LLM이 출력), 참조 가이드 평가(평가 대상과 더불어 정답을 평가 LLM에 제시한 뒤 평가를 결정)가 있다.

### LLM-as-a-Judge

LLM은 사후학습(SFT, RLHF)을 통해 지시 준수성과 대화 능력을 향상시켜 인간에게 선호되는 응답 능력을 획득했을 것이므로 이를 제대로 평가하고자 하는 요구가 생겼다. 그러나 기존 평가 기법에는 문제가 있다. 규칙 기반 평가(MMLU, HELM)는 LLM의 기초적 능력을 측정할 수는 있지만 다양한 사용자 요구에 대한 LLM 응답의 유용성을 측정하는 것과 괴리가 있다. 자동화된 객관 평가(BLEU, ROUGE)는 표면 어휘 중복을 측정하는 지표로 이야기 생성 등 깊이 있는 뉘앙스를 다루는 태스크에는 부적합하다. 인간(전문가) 평가는 비용이 높고 스케일링이 어렵다. LLM-as-a-Judge[60]는 인간과 같은 가치와 추론 과정을 갖춘 LLM을 활용하여 다양한 데이터 타입에 대해 확장 가능하고 유연한 평가 제공을 목표로 하며, 채점자(Graders), 평가자(Evaluators/Assessors), 비평가(Critics), 검증자(Verifiers), 시험관(Examiners), 보상/순위 모델(Reward/Ranking Models)의 역할을 수행할 수 있다.

LLM-as-a-Judge의 평가 파이프라인은 프롬프트 설계와 후처리로 구성된다. 프롬프트에서 출력되는 평가 형식으로는 1~3 또는 0~100 연속 점수, Yes/No, 페어 비교(2개의 선택지를 제시하고 기준을 만족하는 것을 선택), 객관식 평가 등이 있다. 평가에 이용하기 위한 출력의 후처리로는 특정 토큰 추출(Yes/No, 답안 번호), JSON 등의 특정 스키마, 출력 로짓을 0~1 연속 소수로 정규화, 특정 문장이나 단락 추출 등이 있다.

LLM-as-a-Judge에는 바이어스가 존재한다. Judgement-Specific 바이어스로는 위치 바이어스(프롬프트 내 특정 위치에 있는 응답을 선호하는 경향), Compassion-fade bias(모델명 GPT-4 등의 명시적 정보에 영향을 받는다), 스타일 바이어스(이모티콘이 달린 콘텐츠와 같은 특정 텍스트 스타일을 선호하는 경향), 길이 바이어스(장황한 응답을 선호하는 경향), 구체성 바이어스(권위 있는 출처 인용, 수치, 복잡한 전문 용어, 구체적 세부사항을 선호하는 경향) 등이 있다. 각 바이어스에 대한 대응책도 검토되고 있으며, 페어 비교에서의 유효한 개선책으로는 강력한 LLM을 선택하고 평가 내용의 위치를 바꾸어 여러 번 평가한 결과로 다수결을 취하는 방법이 있다[60].

### 발전적 평가: Humanity's Last Exam

LLM의 급속한 발전으로 MMLU와 같은 기존 인기 벤치마크에서 90% 이상의 정확도를 달성하여 능력 측정의 한계(포화 상태)에 달했다. 이에 2500문항의 전문가 수준이면서 도전적인 질문을 작성한 Humanity's Last Exam(HLE)[61]이 제안되었다. 100개 이상의 전문 분야를 포함하며, 문제 형식은 출력 문자열의 완전 일치, 복수의 선택지가 정답인 문제 등이고, 그중 14%는 텍스트와 이미지 모두의 이해를 필요로 한다.

문제 구축 방법으로는 총 500,000 USD 상금을 마련하여 양질의 질문을 모집하고, LLM에 의한 난이도 확인(풀 수 없는 문제를 모은다) 후 대학원 학위를 가진 사람이 리뷰하고 관계자·전문가가 최종적으로 결정하는 필터를 거친다. 그 결과 최신 LLM에서도 5% 미만의 정확도밖에 달성하지 못하는 벤치마크가 만들어졌다. 과제로는 전문가 간의 의견 불일치(공개 셋에서 15.4%의 문항은 의견이 일치하지 않는다), 복수 전문가의 필요성(표준적인 문헌 검색이 아니라 연구 경험에 기반한 질문이 존재한다), 단기간 포화 가능성(HLE도 단기간에 포화할 가능성이 있어 새로운 질문을 추가하는 동적 데이터셋 HLE-ROLLING을 도입 예정) 등이 있다.

## 정리

LLM 학습 파이프라인의 세 학습 단계(사전학습, 파인튜닝, 강화학습)와 평가 단계 어느 것에서도 학습과 평가를 위한 데이터가 중요하다. 사전학습에서는 필터링을 수행하여 데이터 품질을 높임으로써 LLM 성능 향상에 기여한다. 최근에는 데이터 작성과 LLM 평가에서도 (다른) 대규모 LLM을 활용하여 데이터 확장이나 자동 평가를 수행하는 시도가 활발하다. 개인정보 보호나 LLM 평가에서의 바이어스 등의 관점에서 향후 지속적인 대응이 필요하다.

---

## References

[1] Choo (2025), "The emergence of Large Language Models (LLMs)", The low down, https://thelowdown.momentum.asia/the-emergence-of-large-language-models-llms/ 접속일: 2025/11/2

[2] Devlin, et al. (2018), "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding", arXiv:1810.04805

[3] Radford, et al. (2019), "Language Models are Unsupervised Multitask Learners", OpenAI Blog, https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf 접속일: 2026/5/24

[4] Brown, et al. (2020), "Language Models are Few-Shot Learners", arXiv:2005.14165

[5] Smith, et al. (2022), "Using DeepSpeed and Megatron to Train Megatron-Turing NLG 530B, A Large-Scale Generative Language Model", arXiv:2201.11990

[6] Chowdhery, et al. (2022), "PaLM: Scaling Language Modeling with Pathways", arXiv:2204.02311

[7] Penedo, et al. (2023), "The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Data, and Web Data Only", arXiv:2306.01116

[8] BigScience Workshop, et al. (2022), "BLOOM: A 176B-Parameter Open-Access Multilingual Language Model", arXiv:2211.05100

[9] Nguyen, et al. (2023), "CulturaX: A Cleaned, Enormous, and Multilingual Dataset for Large Language Models in 167 Languages", arXiv:2309.09400

[10] Fu, et al. (2022), "How does GPT Obtain its Ability? Tracing Emergent Abilities of Language Models to their Sources", https://yaofu.notion.site/How-does-GPT-Obtain-its-Ability-Tracing-Emergent-Abilities-of-Language-Models-to-their-Sources-b9a57ac0fcf74f30a1ab9e3e36fa1dc1 접속일: 2026/5/24

[11] Zhao, et al. (2023), "A Survey of Large Language Models", arXiv:2303.18223

[12] Penedo, et al. (2023), "The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Data, and Web Data Only", arXiv:2306.01116

[13] Holtzman, et al. (2019), "The curious case of neural text degeneration", ICLR 2019, arXiv:1904.09751

[14] Rae, et al. (2021), "Scaling language models: Methods, analysis & insights from training gopher", arXiv:2112.11446

[15] Lee, et al. (2022), "Deduplicating training data makes language models better", Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics, pp. 8424–8445, arXiv:2107.06499

[16] Hernandez, et al. (2022), "Scaling laws and interpretability of learning from repeated data", arXiv:2205.10487

[17] speed blog (2023), "Introduction to MinHash", https://speed1313.github.io/posts/minhash/ 접속일: 2025/11/3

[18] Penedo, et al. (2024), "The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale", arXiv:2406.17557

[19] Sachdeva, et al. (2024), "How to Train Data-Efficient LLMs", arXiv:2402.09668

[20] Li, et al. (2024), "DataComp-LM: In search of the next generation of training sets for language models", arXiv:2406.11794

[21] Chai, et al. (2025), "Text Data Augmentation for Large Language Models: A Comprehensive Survey of Methods, Challenges, and Opportunities", arXiv:2501.18845

[22] Yao, et al. (2022), "ReAct: Synergizing Reasoning and Acting in Language Models", arXiv:2210.03629

[23] Fujii, et al. (2025), "Rewriting Pre-Training Data Boosts LLM Performance in Math and Code", arXiv:2505.02881

[24] Wei, et al. (2021), "Finetuned Language Models Are Zero-Shot Learners", arXiv:2109.01652

[25] Sanh, et al. (2021), "Multitask Prompted Training Enables Zero-Shot Task Generalization", arXiv:2110.08207

[26] Eccleston (2023), "ShareGPT", https://sharegpt.com/ 접속일: 2026/5/24

[27] Conover (2023), "Free Dolly: Introducing the World's First Truly Open Instruction-Tuned LLM", https://www.databricks.com/blog/2023/04/12/dolly-first-open-commercially-viable-instruction-tuned-llm 접속일: 2026/5/24

[28] Ouyang, et al. (2022), "Training language models to follow instructions with human feedback", arXiv:2203.02155

[29] Wang, et al. (2022), "Self-Instruct: Aligning Language Models with Self-Generated Instructions", arXiv:2212.10560

[30] Xu, et al. (2023), "Baize: An Open-Source Chat Model with Parameter-Efficient Tuning on Self-Chat Data", arXiv:2304.01196

[31] Toshniwal, et al. (2024), "OpenMathInstruct-1: A 1.8 Million Math Instruction Tuning Dataset", arXiv:2402.10176

[32] Kim, et al. (2023), "The CoT Collection: Improving Zero-shot and Few-shot Learning of Language Models via Chain-of-Thought Fine-Tuning", arXiv:2305.14045

[33] Fernandes, et al. (2023), "Bridging the Gap: A Survey on Integrating (Human) Feedback for Natural Language Generation", arXiv:2305.00955

[34] Bai, et al. (2022), "Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback", arXiv:2204.05862

[35] Ethayarajh, et al. (2022), "Understanding Dataset Difficulty with V-Usable Information", arXiv:2110.08420

[36] Gao, et al. (2022), "Scaling Laws for Reward Model Overoptimization", arXiv:2210.10760

[37] OpenAI (2023), "GPT-4 Technical Report", arXiv:2303.08774

[38] Liu, et al. (2023), "Training Socially Aligned Language Models on Simulated Social Interactions", arXiv:2305.16960

[39] 源, et al. (2025), "대규모 언어 모델 사전학습용 코퍼스에서의 민감정보 탐지", 언어처리학회 제31회 연차대회

[40] 문화심의회 저작권분과회 법제도소위원회 (2024), "AI와 저작권에 관한 생각에 대하여", https://www.bunka.go.jp/seisaku/bunkashingikai/chosakuken/pdf/94037901_01.pdf 접속일: 2025/10/31

[41] 개인정보보호위원회·후생노동성, "의료·요양 관계 사업자에서의 개인정보의 적절한 취급을 위한 가이드라인", https://www.ppc.go.jp/personalinfo/legal/iryoukaigo_guidance/#a2-1 접속일: 2025/10/31

[42] Laurençon, et al. (2023), "The BigScience ROOTS Corpus: A 1.6TB Composite Multilingual Dataset", arXiv:2303.03915

[43] Paperno, et al. (2016), "The LAMBADA dataset: Word prediction requiring a broad discourse context", arXiv:1606.06031

[44] Chen, et al. (2021), "Evaluating Large Language Models Trained on Code", arXiv:2107.03374

[45] Mihaylov, et al. (2018), "Can a Suit of Armor Conduct Electricity? A New Dataset for Open Book Question Answering", arXiv:1809.02789

[46] Goodrich, et al. (2019), "Assessing The Factual Accuracy of Generated Text", arXiv:1905.13322

[47] Zellers, et al. (2019), "HellaSwag: Can a Machine Really Finish Your Sentence?", arXiv:1905.07830

[48] Wei, et al. (2022), "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models", arXiv:2201.11903

[49] Lin, et al. (2021), "TruthfulQA: Measuring How Models Mimic Human Falsehoods", arXiv:2109.07958

[50] Nangia, et al. (2020), "CrowS-Pairs: A Challenge Dataset for Measuring Social Biases in Masked Language Models", arXiv:2010.00133

[51] Shridhar, et al. (2020), "ALFWorld: Aligning Text and Embodied Environments for Interactive Learning", arXiv:2010.03768

[52] Yao, et al. (2022), "WebShop: Towards Scalable Real-World Web Interaction with Grounded Language Agents", arXiv:2207.01206

[53] Fan, et al. (2022), "MineDojo: Building Open-Ended Embodied Agents with Internet-Scale Knowledge", arXiv:2206.08853

[54] Yang, et al. (2018), "HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering", arXiv:1809.09600

[55] Cobbe, et al. (2021), "Training Verifiers to Solve Math Word Problems", arXiv:2110.14168

[56] Patil, et al. (2023), "Gorilla: Large Language Model Connected with Massive APIs", arXiv:2305.15334

[57] Chen, et al. (2019), "TabFact: A Large-scale Dataset for Table-based Fact Verification", arXiv:1909.02164

[58] Hendrycks, et al. (2021), "Measuring Massive Multitask Language Understanding", ICLR 2021, https://openreview.net/forum?id=d7KBjmI3GmQ

[59] Zheng, et al. (2023), "Judging LLM-as-a-judge with MT-bench and Chatbot Arena", NeurIPS 2023, https://dl.acm.org/doi/10.5555/3666122.3668142

[60] Gu, et al. (2024), "A Survey on LLM-as-a-Judge", arXiv:2411.15594

[61] Phan, et al. (2025), "Humanity's Last Exam", arXiv:2501.14249

[62] 문화청 저작권과, "AI와 저작권", https://www.bunka.go.jp/seisaku/chosakuken/pdf/93903601_01.pdf 접속일: 2025/11/4
