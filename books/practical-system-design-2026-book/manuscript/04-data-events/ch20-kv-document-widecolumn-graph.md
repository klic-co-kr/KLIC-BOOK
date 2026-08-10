---
id: ch20
title: Key-Value·Document·Wide-column·Graph
part: data-events
order: 20
status: draft
freshness: current
last_verified: '2026-08-06'
review_due: '2027-02-06'
upstream_lineage:
- source: system-design-primer
  file: README.md
  anchor: nosql
  action: REWRITE
audiences:
- backend-engineer
- platform-engineer
prerequisites:
- ch11
- ch18
learning_objectives:
- 비관계형 데이터 모델을 access pattern과 aggregate 경계로 선택한다.
- denormalization·secondary index·일관성 비용을 설명한다.
- 모델별 hotspot과 schema evolution을 설계한다.
figures:
- fig-ch20-01
- fig-ch20-02
sources:
- dynamo-paper
- bigtable-paper
- mongodb-data-model
- neo4j-graph-modeling
draft_notice: 기술·편집·접근성 검수 전 초고
---

# 20. Key-Value·Document·Wide-column·Graph

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

## 이 장에서 해결할 문제

NoSQL은 하나의 일관된 기술 범주가 아니다. Key-value, document, wide-column, graph는 서로 다른 조회와 분할 문제를 해결한다. “join이 없다”는 단순함은 쓰기 중복, 비동기 index, 애플리케이션 병합 비용으로 이동할 수 있다.

이 절의 기준 출처: [@dynamo-paper; @bigtable-paper].

### 학습 목표

- 비관계형 데이터 모델을 access pattern과 aggregate 경계로 선택한다.
- denormalization·secondary index·일관성 비용을 설명한다.
- 모델별 hotspot과 schema evolution을 설계한다.

## 먼저 결론

- key-value는 key 기반 직접 조회와 단순 partition에 적합하다.
- document는 함께 변경되는 aggregate를 한 단위로 저장하지만 무제한 중첩과 큰 문서는 피한다.
- wide-column은 partition key와 clustering key로 미리 아는 쿼리를 최적화한다.
- graph는 다단계 관계 탐색에 유리하지만 큰 supernode와 분산 traversal을 관리해야 한다.

::: current-note
**2026-08-06 확인:** 이 장은 변화 가능한 표준·프로젝트·AI 구현을 포함한다. 기본 재검토일은 `2027-02-06`이며, 출판 직전 공식 문서를 다시 확인한다.
:::

## 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | Key-Value·Document·Wide-column·Graph에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | key-value는 key 기반 직접 조회와 단순 partition에 적합하다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | query별 materialized view를 추가하되 view 수와 update fan-out을 제한한다. |
| 실패·복구 | “큰 document” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | 크기 상한과 별도 child collection/blob을 둔다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | document의 자유로운 field에 민감 정보가 무단 추가되지 않게 schema validation과 분류를 둔다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | partition/document 크기 분포와 hot key |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

## 핵심 개념

### Key-value model

key로 opaque value를 저장·조회하며 partition과 cache에 적합하다.

### Document model

중첩 field를 가진 문서를 aggregate 단위로 저장한다.

### Wide-column model

partition 안의 정렬된 clustering row를 큰 sparse table처럼 저장한다.

### Property graph

node·edge와 속성으로 관계를 표현하고 traversal을 수행한다.

### Denormalization

읽기 경로를 단순화하기 위해 데이터를 중복 저장하는 설계다.

### Materialized view

원본 변경에서 파생해 특정 query를 위한 형태로 유지하는 데이터다.

### Supernode

edge가 매우 많은 graph node로 traversal과 lock hotspot을 만든다.

핵심 개념의 정의와 범위는 [@dynamo-paper; @bigtable-paper; @mongodb-data-model; @neo4j-graph-modeling]를 기준으로 재검토해야 한다.

## 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| Request router | key·partition·graph 영역에 요청을 보낸다. |
| Primary data model | aggregate를 선택한 형태로 저장한다. |
| Secondary index/view | 비주요 access pattern을 비동기 또는 동기로 지원한다. |
| Change stream | 중복 데이터와 파생 view를 갱신한다. |
| Reconciliation | 누락·중복·순서 오류를 주기적으로 찾아 수리한다. |
| Schema/version adapter | 오래된 record를 읽고 새 형식으로 변환한다. |

<!-- figure-spec
id: fig-ch20-01
chapter: ch20
role: nosql-models
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch20-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: key-value·document·wide-column·graph의 데이터 형태와 대표 query를 비교한다.
required_labels_ko:
- Key-Value
- Document
- Wide-Column
- Graph
- Partition Key
- Traversal
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- dynamo-paper
- bigtable-paper
- mongodb-data-model
alt_ko: key-value·document·wide-column·graph의 데이터 형태와 대표 query를 비교한다.
caption_ko: key-value·document·wide-column·graph의 데이터 형태와 대표 query를 비교한다
status: specified
spec_file: assets/specs/svg/fig-ch20-01.md
-->

> **시각자료 제작 위치 — key-value·document·wide-column·graph의 데이터 형태와 대표 query를 비교한다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch20-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch20-01.md`  
> 대체 텍스트: key-value·document·wide-column·graph의 데이터 형태와 대표 query를 비교한다.


## 요청·데이터 흐름

1. 업무 query를 key·range·aggregate·relationship traversal로 분류한다.
2. 함께 원자적으로 변경할 범위를 정한다.
3. partition key와 문서/row 크기 상한을 정한다.
4. 중복 field와 secondary view의 source of truth를 지정한다.
5. 변경 이벤트로 파생 모델을 갱신한다.
6. staleness와 repair를 관측한다.
7. schema version을 읽기·쓰기 양쪽에서 점진 전환한다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

## 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| Key-value | 단일 key 조회·분할·확장이 단순하다. | 다양한 query와 관계 검증을 애플리케이션이 맡는다. | 세션·profile·cache·metadata |
| Document | aggregate 읽기와 schema evolution이 유연하다. | 큰 문서·중복·다문서 transaction 비용이 있다. | catalog·content·설정 |
| Wide-column | 높은 write throughput과 시간/범위 query에 적합하다. | query-first schema와 partition size 관리가 필요하다. | 이벤트·시계열·대규모 로그 |
| Graph | 다중 hop 관계와 경로 query가 자연스럽다. | 분산 traversal·supernode·운영 비용이 있다. | 권한 관계·사기 탐지·지식 graph |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@dynamo-paper; @bigtable-paper; @mongodb-data-model]를 참조한다.

## 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| 큰 document | 한 aggregate가 계속 커져 update·복제·전송 비용이 폭증한다. | 크기 상한과 별도 child collection/blob을 둔다. |
| Wide partition | 한 partition key에 수년 데이터가 모여 compaction과 hotspot이 생긴다. | time bucket·hash suffix로 경계를 나눈다. |
| 중복 불일치 | 여러 document의 복사 field가 일부만 갱신된다. | 원장 지정·change stream·reconciliation을 사용한다. |
| Secondary index lag | 색인에서 새 데이터가 누락돼 사용자에게 모순이 보인다. | staleness SLO와 fallback read를 둔다. |
| Graph supernode | 유명 사용자·공통 권한 node에 traversal이 집중된다. | edge type/partition·precomputed view·limit를 적용한다. |

<!-- figure-spec
id: fig-ch20-02
chapter: ch20
role: denormalized-view-flow
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch20-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 원장 변경이 여러 denormalized view와 secondary index로 전파되고 reconciliation되는 흐름을 보여준다.
required_labels_ko:
- 원장
- Change Stream
- Document View
- Wide-column View
- Graph View
- Reconciliation
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- dynamo-paper
- bigtable-paper
- mongodb-data-model
alt_ko: 원장 변경이 여러 denormalized view와 secondary index로 전파되고 reconciliation되는 흐름을 보여준다.
caption_ko: 원장 변경이 여러 denormalized view와 secondary index로 전파되고 reconciliation되는 흐름을 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch20-02.md
-->

> **시각자료 제작 위치 — 원장 변경이 여러 denormalized view와 secondary index로 전파되고 reconciliation되는 흐름을 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch20-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch20-02.md`  
> 대체 텍스트: 원장 변경이 여러 denormalized view와 secondary index로 전파되고 reconciliation되는 흐름을 보여준다.


## 확장 전략

- query별 materialized view를 추가하되 view 수와 update fan-out을 제한한다.
- tenant·time bucket으로 partition을 나누고 skew를 모니터링한다.
- large value는 object storage로 분리하고 metadata만 모델에 둔다.
- graph traversal depth·result·CPU budget을 명시한다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

## 보안과 개인정보

- document의 자유로운 field에 민감 정보가 무단 추가되지 않게 schema validation과 분류를 둔다.
- graph 관계가 권한 정보를 노출할 수 있으므로 traversal 결과에 정책을 적용한다.
- tenant key와 partition key를 일치시키거나 모든 query에서 격리 조건을 강제한다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

## 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- partition/document 크기 분포와 hot key
- secondary index lag·view update failure
- read/write amplification과 compaction
- schema version 분포와 lazy migration 실패
- graph traversal depth·visited node·supernode

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

## 비용과 운영 복잡도

- denormalization은 저장량과 write fan-out을 늘린다.
- 특수 DB는 query 개발을 줄여도 별도 backup·upgrade·운영 인력을 요구한다.
- graph·secondary index의 무제한 query를 허용하면 비용 예측이 어렵다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

## 흔한 오해와 안티패턴

- NoSQL은 transaction이 없다고 일반화한다.
- document를 크기 제한 없는 객체 dump로 사용한다.
- wide-column에서 ad-hoc query를 나중에 해결하려 한다.
- graph DB가 모든 join을 더 빠르게 한다고 생각한다.

## 설계 리뷰

- [ ] 모델이 핵심 query와 aggregate 경계를 직접 반영하는가?
- [ ] partition/document/supernode 크기 상한이 있는가?
- [ ] 중복 데이터의 원장과 repair 경로가 명확한가?
- [ ] schema evolution이 오래된 record를 안전하게 처리하는가?
- [ ] query 비용과 tenant 격리가 제한되는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

## 연습문제

1. 사용자 profile을 document로 설계하고 무한히 커지는 활동 기록을 분리하라.
2. IoT 이벤트를 wide-column에 저장할 partition/clustering key를 설계하라.
3. 권한 graph에서 supernode가 되는 조직 전체 그룹을 다루는 방법을 제안하라.

## 핵심 요약

- 비관계형 모델은 서로 다른 access pattern을 해결한다.
- aggregate와 partition 경계가 모델의 핵심이다.
- denormalization은 읽기 이득과 동기화 비용을 교환한다.
- secondary view에는 staleness와 repair가 필요하다.
- 크기·fan-out·query 비용 상한을 명시한다.

## 출처

- [@dynamo-paper] Giuseppe DeCandia et al.. **Dynamo: Amazon's Highly Available Key-value Store** (2007). https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf
- [@bigtable-paper] Fay Chang et al.. **Bigtable: A Distributed Storage System for Structured Data** (2006). https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/
- [@mongodb-data-model] MongoDB. **MongoDB Data Modeling Introduction** (2026). https://www.mongodb.com/docs/manual/data-modeling/
- [@neo4j-graph-modeling] Neo4j. **Graph Data Modeling Guidelines** (2026). https://neo4j.com/docs/getting-started/data-modeling/

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
