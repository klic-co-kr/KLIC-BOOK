---
id: ch31
title: RAG 데이터 파이프라인과 Retrieval 품질
part: ai-native
order: 31
status: draft
freshness: current
last_verified: '2026-08-06'
review_due: '2027-02-06'
upstream_lineage:
- source: new-2026-edition
  file: null
  anchor: null
  action: ADD
audiences:
- backend-engineer
- platform-engineer
prerequisites:
- ch21
- ch24
- ch27
- ch28
learning_objectives:
- RAG를 수집·정제·검색·생성·근거 검증 파이프라인으로 분해한다.
- chunk·embedding·index·reranking의 version과 품질을 관리한다.
- tenant 권한·freshness·provenance를 retrieval 경로에 적용한다.
figures:
- fig-ch31-01
- fig-ch31-02
sources:
- rag-paper
- dpr-paper
- beir-paper
- hnsw-paper
- owasp-llm
draft_notice: 기술·편집·접근성 검수 전 초고
---

## 31. RAG 데이터 파이프라인과 Retrieval 품질

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

### 이 장에서 해결할 문제

RAG 품질 문제를 모델 prompt 하나로 해결할 수는 없다. 답변 품질은 원문 수집, parsing, chunk 경계, metadata, embedding, candidate retrieval, reranking, context 구성, 생성, citation 검증의 연쇄 결과다. 각 단계를 독립적으로 평가해야 한다.

이 절의 기준 출처: [@rag-paper; @dpr-paper].

#### 학습 목표

- RAG를 수집·정제·검색·생성·근거 검증 파이프라인으로 분해한다.
- chunk·embedding·index·reranking의 version과 품질을 관리한다.
- tenant 권한·freshness·provenance를 retrieval 경로에 적용한다.

### 먼저 결론

- 원문과 metadata를 진실의 원천으로 보존하고 vector/text index는 재구축 가능한 파생 상태로 둔다.
- retrieval 품질은 answer quality와 분리해 recall·ranking·coverage를 먼저 측정한다.
- chunk와 embedding model을 versioning하고 dual-index로 안전하게 전환한다.
- tenant·ACL filter는 후보 검색 전후에 적용하고 citation이 실제 원문 범위와 일치하는지 검증한다.

::: current-note
**2026-08-06 확인:** 이 장은 변화 가능한 표준·프로젝트·AI 구현을 포함한다. 기본 재검토일은 `2027-02-06`이며, 출판 직전 공식 문서를 다시 확인한다.
:::

### 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | RAG 데이터 파이프라인과 Retrieval 품질에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | 원문과 metadata를 진실의 원천으로 보존하고 vector/text index는 재구축 가능한 파생 상태로 둔다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | tenant·source·language별 index 분리와 shared index filter 비용을 비교한다. |
| 실패·복구 | “Parser corruption” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | 문서 형식별 품질 검사와 원문 span preview를 둔다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | connector credential은 source별 최소 read 권한과 짧은 수명을 사용한다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | ingestion freshness·parser failure·chunk count 변화 |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

### 핵심 개념

#### RAG

외부 지식을 검색해 생성 모델의 입력 context에 결합하는 구조다.

#### Chunking

문서를 검색·context 단위로 나누는 과정이며 구조·중첩·overlap이 품질과 비용에 영향을 준다.

#### Embedding

query와 문서 조각을 vector 공간에 표현한다.

#### Candidate retrieval

lexical·dense·hybrid 방식으로 상위 후보를 빠르게 찾는다.

#### Reranking

더 비싼 모델이나 규칙으로 후보 순서를 다시 평가한다.

#### Grounding

답변이 제공된 근거에 기반하도록 만드는 설계와 검증이다.

#### Provenance

원문·version·위치·수집 시각·변환 이력을 추적하는 metadata다.

#### Freshness

원문 변경이 검색·답변에 반영되기까지의 시간이다.

핵심 개념의 정의와 범위는 [@rag-paper; @dpr-paper; @beir-paper; @hnsw-paper; @owasp-llm]를 기준으로 재검토해야 한다.

### 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| Source registry | 문서 소유자·version·권한·수집 정책을 원장으로 관리한다. |
| Ingestion workers | fetch·parse·normalize·malware scan을 수행한다. |
| Chunk store | 원문 위치와 version을 가진 chunk를 보존한다. |
| Text/vector indexes | lexical·semantic candidate를 제공한다. |
| Retriever | filter·query rewrite·hybrid fusion을 수행한다. |
| Reranker | 상위 후보의 relevance를 정밀 평가한다. |
| Context builder | token budget·중복·provenance를 고려해 context를 구성한다. |
| Answer service | 생성과 citation·policy 검증을 수행한다. |
| Evaluation store | golden query·judgment·online feedback을 보존한다. |

<!-- figure-spec
id: fig-ch31-01
chapter: ch31
role: rag-ingestion-serving
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch31-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: source 수집에서 parse·chunk·embedding·index와 query retrieval·rerank·generation까지 전체 파이프라인을 보여준다.
required_labels_ko:
- Source Registry
- Parser
- Chunker
- Embedding
- Text Index
- Vector Index
- Retriever
- Reranker
- Generator
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- rag-paper
- dpr-paper
- beir-paper
alt_ko: source 수집에서 parse·chunk·embedding·index와 query retrieval·rerank·generation까지 전체 파이프라인을 보여준다.
caption_ko: source 수집에서 parse·chunk·embedding·index와 query retrieval·rerank·generation까지 전체 파이프라인을 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch31-01.md
-->

> **시각자료 제작 위치 — source 수집에서 parse·chunk·embedding·index와 query retrieval·rerank·generation까지 전체 파이프라인을 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch31-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch31-01.md`  
> 대체 텍스트: source 수집에서 parse·chunk·embedding·index와 query retrieval·rerank·generation까지 전체 파이프라인을 보여준다.

### 요청·데이터 흐름

1. source connector가 권한과 change cursor를 확인해 문서를 수집한다.
2. parser가 격리 환경에서 구조와 원문 span을 추출한다.
3. chunker가 문서 구조·token 목표·overlap 정책으로 조각을 만든다.
4. embedding과 lexical analyzer version을 붙여 dual index에 저장한다.
5. query에서 tenant·권한·언어·의도를 추출한다.
6. hybrid retrieval과 metadata filter로 후보를 얻는다.
7. reranker가 evidence relevance를 평가한다.
8. context builder가 중복과 token budget을 조정한다.
9. answer가 citation span과 policy를 검증한 뒤 반환된다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

### 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| Lexical retrieval | 정확한 용어·코드·이름에 강하고 설명이 쉽다. | 표현이 다른 의미 검색에 약하다. | 정책 번호·제품명·정확 문구 |
| Dense retrieval | 의미 유사성에 강하다. | 모델 domain·filter·근사 index에 따라 누락될 수 있다. | 자연어 질문·동의 표현 |
| Hybrid+rerank | 정확어와 의미를 결합해 품질이 높을 수 있다. | 지연·비용·평가·운영 경로가 복잡하다. | 고품질 엔터프라이즈 RAG |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@rag-paper; @dpr-paper; @beir-paper]를 참조한다.

### 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| Parser corruption | 표·머리글·OCR 순서가 깨져 의미 없는 chunk가 생성된다. | 문서 형식별 품질 검사와 원문 span preview를 둔다. |
| ACL leak | 공유 index에서 filter가 누락돼 다른 tenant 문서가 후보에 들어온다. | pre-filter·post-filter·answer citation 검증을 중복 적용한다. |
| Stale index | 원문 변경/삭제가 index에 늦게 반영된다. | change cursor·deletion ledger·freshness SLO를 둔다. |
| Embedding mismatch | query는 새 model, 문서는 이전 model vector를 사용한다. | model version별 index와 routing을 분리한다. |
| Context poisoning | 문서 안의 명령문이 system instruction처럼 처리된다. | retrieved content를 untrusted data로 구분하고 tool/policy 권한과 분리한다. |
| Citation drift | 답변 문장이 실제 citation span에서 지지되지 않는다. | claim-evidence 검사와 source snippet 확인을 적용한다. |

<!-- figure-spec
id: fig-ch31-02
chapter: ch31
role: rag-quality-funnel
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch31-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: candidate recall·rerank precision·context coverage·grounded answer로 이어지는 품질 funnel을 보여준다.
required_labels_ko:
- Recall@k
- Reranker
- Context Coverage
- Grounding
- Citation
- Abstention
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- rag-paper
- dpr-paper
- beir-paper
alt_ko: candidate recall·rerank precision·context coverage·grounded answer로 이어지는 품질 funnel을 보여준다.
caption_ko: candidate recall·rerank precision·context coverage·grounded answer로 이어지는 품질 funnel을 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch31-02.md
-->

> **시각자료 제작 위치 — candidate recall·rerank precision·context coverage·grounded answer로 이어지는 품질 funnel을 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch31-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch31-02.md`  
> 대체 텍스트: candidate recall·rerank precision·context coverage·grounded answer로 이어지는 품질 funnel을 보여준다.

### 확장 전략

- tenant·source·language별 index 분리와 shared index filter 비용을 비교한다.
- batch embedding은 throughput을 높이되 freshness tier에 따라 priority를 둔다.
- candidate 수·rerank 수·context token을 단계별 budget으로 제한한다.
- reindex는 shadow query로 quality·latency·cost를 비교한 뒤 alias를 전환한다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

### 보안과 개인정보

- connector credential은 source별 최소 read 권한과 짧은 수명을 사용한다.
- 문서 parser·archive extraction을 sandbox에 격리한다.
- ACL과 tenant filter를 retrieval, rerank, answer 단계에서 검증한다.
- prompt injection을 이유로 retrieved text에 tool 실행 권한을 부여하지 않는다.
- 삭제·보존 요청을 원문·chunk·embedding·cache·evaluation sample에 전파한다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

### 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- ingestion freshness·parser failure·chunk count 변화
- retrieval Recall@k·nDCG/MRR·zero-result
- candidate/rerank/context 단계별 latency와 token
- ACL filter selectivity·denied candidate·leak test
- citation coverage·unsupported claim·answer abstention
- model/index version별 quality·cost

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

### 비용과 운영 복잡도

- embedding·reindex·vector memory·reranker inference·context token이 주요 비용 축이다.
- 문서를 무조건 작은 chunk로 나누면 index와 retrieval 후보·token 비용이 늘어난다.
- 고품질 reranking은 모든 query가 아니라 risk·uncertainty·value tier에 선택 적용할 수 있다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

### 흔한 오해와 안티패턴

- vector DB를 추가하면 RAG가 완성된다고 생각한다.
- 답변 평가만 하고 retrieval 누락 원인을 측정하지 않는다.
- 모든 문서를 같은 chunk 크기와 embedding model로 처리한다.
- citation URL만 붙이면 grounding이 검증됐다고 본다.

### 설계 리뷰

- [ ] 원문·chunk·index·model version의 계보가 추적되는가?
- [ ] retrieval 품질과 generation 품질이 분리 평가되는가?
- [ ] ACL·tenant·삭제가 모든 단계에서 강제되는가?
- [ ] reindex를 dual-run·shadow·rollback할 수 있는가?
- [ ] citation이 실제 claim을 지지하는지 검증하는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

### 연습문제

1. 사내 규정 PDF의 표·부록·개정 이력을 보존하는 chunk 전략을 설계하라.
2. Recall@20은 높지만 answer가 틀린 RAG를 retrieval·rerank·generation 단계로 진단하라.
3. embedding model 교체의 dual-index와 quality gate를 작성하라.

### 핵심 요약

- RAG는 end-to-end 데이터 파이프라인이다.
- 원문은 원장이고 index는 파생 상태다.
- retrieval과 generation을 분리 평가한다.
- version·freshness·provenance를 모든 chunk에 붙인다.
- ACL과 citation 검증은 품질이 아니라 보안 경계이기도 하다.

### 출처

- [@rag-paper] Patrick Lewis et al.. **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks** (2020). https://arxiv.org/abs/2005.11401
- [@dpr-paper] Vladimir Karpukhin et al.. **Dense Passage Retrieval for Open-Domain Question Answering** (2020). https://arxiv.org/abs/2004.04906
- [@beir-paper] Nandan Thakur et al.. **BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models** (2021). https://arxiv.org/abs/2104.08663
- [@hnsw-paper] Yu. A. Malkov and D. A. Yashunin. **Efficient and Robust Approximate Nearest Neighbor Search Using Hierarchical Navigable Small World Graphs** (2018). https://arxiv.org/abs/1603.09320
- [@owasp-llm] OWASP Foundation. **OWASP Top 10 for LLM Applications** (2025). https://genai.owasp.org/llm-top-10/

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
