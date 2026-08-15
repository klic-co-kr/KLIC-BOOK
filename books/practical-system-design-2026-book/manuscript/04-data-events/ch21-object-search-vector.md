---
id: ch21
title: Object Storage·Search·Vector Store
part: data-events
order: 21
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
- ch18
- ch20
learning_objectives:
- blob·full-text·vector 검색의 서로 다른 저장·조회 모델을 설명한다.
- 원장 metadata와 파생 index의 경계를 설계한다.
- ingestion·version·삭제·재색인을 운영한다.
figures:
- fig-ch21-01
- fig-ch21-02
sources:
- s3-consistency
- lucene-docs
- hnsw-paper
draft_notice: 기술·편집·접근성 검수 전 초고
---

## 21. Object Storage·Search·Vector Store

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

### 이 장에서 해결할 문제

객체 저장소, 검색 엔진, vector store는 범용 원장의 대체물이 아니라 큰 불변 blob과 파생 검색 구조를 제공하는 계층이다. 원본 문서와 metadata를 보존하고 검색 index는 언제든 재구축할 수 있어야 한다.

이 절의 기준 출처: [@s3-consistency; @lucene-docs].

#### 학습 목표

- blob·full-text·vector 검색의 서로 다른 저장·조회 모델을 설명한다.
- 원장 metadata와 파생 index의 경계를 설계한다.
- ingestion·version·삭제·재색인을 운영한다.

### 먼저 결론

- object key와 metadata DB의 일관성 경계를 명시한다.
- 검색 index는 tokenization·mapping·ranking 버전에 따라 결과가 바뀐다.
- vector 검색은 embedding model·distance metric·filter·index parameter를 함께 버전 관리한다.
- 삭제는 object, text index, vector, cache, backup에 비동기로 전파되므로 완료 상태를 추적한다.

::: current-note
**2026-08-06 확인:** 이 장은 변화 가능한 표준·프로젝트·AI 구현을 포함한다. 기본 재검토일은 `2027-02-06`이며, 출판 직전 공식 문서를 다시 확인한다.
:::

### 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | Object Storage·Search·Vector Store에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | object key와 metadata DB의 일관성 경계를 명시한다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | object는 content-addressed key·multipart·lifecycle tiering으로 운영한다. |
| 실패·복구 | “Orphan object” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | pending state·idempotent finalize·garbage collector를 둔다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | signed URL을 짧은 만료·정확한 method/object로 제한한다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | object upload/finalize/orphan·checksum failure |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

### 핵심 개념

#### Object storage

큰 immutable 또는 versioned blob을 key로 저장하는 계층이다.

#### Inverted index

term에서 포함 document 목록으로 연결해 full-text 검색을 지원한다.

#### Analyzer

텍스트를 token으로 분해·정규화하는 규칙이다.

#### Embedding

문서나 query를 수치 vector로 표현한 값이다.

#### ANN index

정확한 전체 비교 대신 근사 최근접 탐색으로 latency와 recall을 교환한다.

#### Metadata filter

tenant·권한·날짜 같은 구조적 조건으로 검색 후보를 제한한다.

#### Reindex

새 mapping·analyzer·model로 파생 index를 다시 만드는 작업이다.

핵심 개념의 정의와 범위는 [@s3-consistency; @lucene-docs; @hnsw-paper]를 기준으로 재검토해야 한다.

### 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| Metadata DB | object ownership·version·상태·권한을 원장으로 저장한다. |
| Object store | 원문·이미지·chunk 원본을 보존한다. |
| Ingestion worker | scan·parse·normalize·chunk·hash를 수행한다. |
| Text index | lexical search와 filter를 제공한다. |
| Vector index | embedding ANN search를 제공한다. |
| Search coordinator | query rewrite·hybrid retrieval·reranking을 조합한다. |
| Reindex controller | 새 index를 병렬 구축·검증·alias 전환한다. |

<!-- figure-spec
id: fig-ch21-01
chapter: ch21
role: content-index-pipeline
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch21-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 원문 object와 metadata에서 parser·chunk·text/vector index가 생성되는 흐름을 보여준다.
required_labels_ko:
- Metadata DB
- Object Store
- Parser
- Chunk
- Text Index
- Vector Index
- Search Coordinator
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- s3-consistency
- lucene-docs
- hnsw-paper
alt_ko: 원문 object와 metadata에서 parser·chunk·text/vector index가 생성되는 흐름을 보여준다.
caption_ko: 원문 object와 metadata에서 parser·chunk·text/vector index가 생성되는 흐름을 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch21-01.md
-->

> **시각자료 제작 위치 — 원문 object와 metadata에서 parser·chunk·text/vector index가 생성되는 흐름을 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch21-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch21-01.md`  
> 대체 텍스트: 원문 object와 metadata에서 parser·chunk·text/vector index가 생성되는 흐름을 보여준다.


### 요청·데이터 흐름

1. 업로드 요청이 metadata에 pending record를 만든다.
2. object를 저장하고 checksum·version을 확정한다.
3. worker가 안전하게 문서를 parse하고 chunk를 만든다.
4. text analyzer와 embedding model 버전을 붙여 index한다.
5. query는 tenant·권한 filter 후 lexical/vector 후보를 얻는다.
6. reranker가 상위 결과를 정렬하고 원문 version을 확인한다.
7. 삭제·변경은 tombstone과 job 상태로 모든 파생 index에 전파한다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

### 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| Object+DB | 큰 blob과 transaction metadata를 분리해 비용·내구성이 좋다. | 두 저장소 사이 orphan·pending 상태를 처리해야 한다. | 파일·미디어·문서 원장 |
| Full-text search | 정확한 term·filter·phrase 검색과 설명 가능성이 좋다. | 동의어·의미 변형에 약하고 analyzer 운영이 필요하다. | 검색·로그·catalog |
| Vector ANN | 의미 유사 검색에 유리하다. | 모델 drift·근사 recall·filter 비용·reindex가 필요하다. | RAG·추천·유사도 |
| Hybrid | lexical과 semantic 신호를 결합한다. | 점수 정규화·reranking·운영 경로가 복잡하다. | 정확어와 의미를 함께 요구하는 검색 |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@s3-consistency; @lucene-docs; @hnsw-paper]를 참조한다.

### 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| Orphan object | object 업로드는 성공했지만 metadata commit이 실패한다. | pending state·idempotent finalize·garbage collector를 둔다. |
| Mapping explosion | 동적 field가 무제한 index되어 memory와 cluster state가 커진다. | schema allowlist와 field cardinality limit를 둔다. |
| Model drift | embedding model 변경 후 query와 document vector 공간이 달라진다. | model version을 키에 포함하고 dual index 전환을 한다. |
| 권한 누출 | vector 후보를 얻은 뒤 filter해 다른 tenant 존재가 노출된다. | 가능하면 pre-filter하고 결과 단계에서 다시 검증한다. |
| 삭제 지연 | 원문 삭제 후 search/vector에 결과가 남는다. | deletion ledger와 end-to-end completion SLO를 둔다. |

<!-- figure-spec
id: fig-ch21-02
chapter: ch21
role: hybrid-search
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch21-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: query가 lexical·vector 후보와 metadata filter·reranker를 거쳐 결과가 되는 흐름을 보여준다.
required_labels_ko:
- Query
- Lexical Search
- Vector Search
- ACL Filter
- Fusion
- Reranker
- 결과
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- s3-consistency
- lucene-docs
- hnsw-paper
alt_ko: query가 lexical·vector 후보와 metadata filter·reranker를 거쳐 결과가 되는 흐름을 보여준다.
caption_ko: query가 lexical·vector 후보와 metadata filter·reranker를 거쳐 결과가 되는 흐름을 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch21-02.md
-->

> **시각자료 제작 위치 — query가 lexical·vector 후보와 metadata filter·reranker를 거쳐 결과가 되는 흐름을 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch21-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch21-02.md`  
> 대체 텍스트: query가 lexical·vector 후보와 metadata filter·reranker를 거쳐 결과가 되는 흐름을 보여준다.


### 확장 전략

- object는 content-addressed key·multipart·lifecycle tiering으로 운영한다.
- text/vector index를 tenant·time·size 기준으로 shard하고 hot shard를 감시한다.
- reindex는 정상 query와 resource를 경쟁하므로 rate limit·canary·shadow query를 사용한다.
- hybrid search는 후보 수와 reranker budget을 명시한다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

### 보안과 개인정보

- signed URL을 짧은 만료·정확한 method/object로 제한한다.
- 문서 parser를 격리하고 압축 폭탄·악성 파일·macro를 차단한다.
- search index와 vector에 민감 원문을 불필요하게 중복하지 않는다.
- tenant·ACL filter를 retrieval 전후 두 번 검증한다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

### 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- object upload/finalize/orphan·checksum failure
- indexing lag·failed document·reindex progress
- query latency·candidate count·cache hit
- ANN recall proxy·filter selectivity·model version
- deletion propagation 완료 시간

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

### 비용과 운영 복잡도

- object storage는 저렴한 용량 대신 request·egress·small object 비용을 만든다.
- search replica와 vector memory는 원문 크기보다 크게 비용이 늘 수 있다.
- model 변경마다 전체 embedding 재생성 비용이 발생한다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

### 흔한 오해와 안티패턴

- object store listing을 transaction database처럼 사용한다.
- 검색 index를 유일한 원장으로 수정한다.
- embedding dimension이 높을수록 무조건 품질이 좋다고 생각한다.
- ACL filter를 검색 후 애플리케이션에서만 적용한다.

### 설계 리뷰

- [ ] 원본·metadata·text index·vector의 쓰기 소유자가 명확한가?
- [ ] orphan과 partial indexing 상태를 복구하는가?
- [ ] model/analyzer/mapping 버전과 reindex 절차가 있는가?
- [ ] 권한과 삭제가 모든 파생 저장소에 전파되는가?
- [ ] 검색 품질·latency·비용을 함께 평가하는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

### 연습문제

1. 문서 업로드 중 DB commit이 실패하는 상태 기계를 설계하라.
2. lexical+vector hybrid 검색에서 candidate와 rerank budget을 정하라.
3. embedding model 교체를 dual-index·shadow query·alias switch로 배포하라.

### 핵심 요약

- object storage는 blob, search는 lexical index, vector store는 semantic 후보를 담당한다.
- metadata 원장과 파생 index를 분리한다.
- ingestion과 삭제는 상태가 있는 비동기 workflow다.
- model·analyzer·mapping을 versioning한다.
- 권한 filter는 retrieval의 일부다.

### 출처

- [@s3-consistency] Amazon Web Services. **Amazon S3 Data Consistency Model** (2026). https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html#ConsistencyModel
- [@lucene-docs] Apache Software Foundation. **Apache Lucene Documentation** (2026). https://lucene.apache.org/core/
- [@hnsw-paper] Yu. A. Malkov and D. A. Yashunin. **Efficient and Robust Approximate Nearest Neighbor Search Using Hierarchical Navigable Small World Graphs** (2018). https://arxiv.org/abs/1603.09320

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
