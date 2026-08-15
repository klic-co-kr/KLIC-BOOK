---
id: ch18
title: 워크로드에서 저장소 선택하기
part: data-events
order: 18
status: draft
freshness: durable
last_verified: '2026-08-06'
review_due: '2028-08-06'
upstream_lineage:
- source: system-design-primer
  file: README.md
  anchor: database
  action: REWRITE
audiences:
- backend-engineer
- platform-engineer
prerequisites:
- ch01
- ch02
- ch07
- ch08
learning_objectives:
- 접근 패턴과 불변조건으로 저장소 요구를 도출한다.
- 하나의 저장소와 다중 저장소 전략의 비용을 비교한다.
- 벤치마크를 실제 데이터·쿼리·장애 조건으로 설계한다.
figures:
- fig-ch18-01
- fig-ch18-02
sources:
- postgres-transaction-iso
- dynamo-paper
- bigtable-paper
draft_notice: 기술·편집·접근성 검수 전 초고
---

## 18. 워크로드에서 저장소 선택하기

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

### 이 장에서 해결할 문제

저장소 선택은 “SQL 대 NoSQL” 투표가 아니다. 쓰기 단위, 조회 형태, 일관성, 데이터 수명, 재구축 가능성, 운영 역량을 먼저 적고 그 요구를 가장 단순하게 만족하는 저장소를 선택해야 한다.

이 절의 기준 출처: [@postgres-transaction-iso; @dynamo-paper].

#### 학습 목표

- 접근 패턴과 불변조건으로 저장소 요구를 도출한다.
- 하나의 저장소와 다중 저장소 전략의 비용을 비교한다.
- 벤치마크를 실제 데이터·쿼리·장애 조건으로 설계한다.

### 먼저 결론

- 데이터 모델보다 먼저 읽기·쓰기·삭제·분석·복구 패턴을 표로 만든다.
- 핵심 원장은 가장 강한 불변조건을 지키는 저장소에 둔다.
- 파생 색인·캐시는 재구축 경로와 허용 staleness를 명시한다.
- polyglot persistence는 기능 이점보다 데이터 동기화·백업·운영 비용을 함께 계산한다.

### 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | 워크로드에서 저장소 선택하기에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | 데이터 모델보다 먼저 읽기·쓰기·삭제·분석·복구 패턴을 표로 만든다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | 한계에 도달한 축이 저장량인지 QPS인지 쿼리 복잡도인지 먼저 측정한다. |
| 실패·복구 | “벤치마크 왜곡” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | 운영 분포·payload·concurrency·장애를 재현한다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | 민감 데이터의 저장 위치·암호화 키·접근 감사를 후보 평가에 포함한다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | 쿼리 패턴별 p95/p99·rows scanned·cache hit |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

### 핵심 개념

#### System of record

업무상 진실의 원천과 승인된 상태를 소유하는 저장소다.

#### Access pattern

키 조회, 범위, join, graph traversal, full-text, vector search 같은 실제 읽기·쓰기 형태다.

#### Working set

짧은 시간에 반복 접근되는 데이터 집합이다.

#### Write amplification

하나의 논리 쓰기가 복제·색인·compaction으로 여러 물리 쓰기를 만드는 정도다.

#### Derived store

원본에서 다시 만들 수 있는 cache·search index·warehouse·feature store다.

#### Operational envelope

데이터 크기, latency, throughput, failure, 복구, 인력 범위에서 검증된 운영 영역이다.

핵심 개념의 정의와 범위는 [@postgres-transaction-iso; @dynamo-paper; @bigtable-paper]를 기준으로 재검토해야 한다.

### 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| 요구 매트릭스 | 불변조건·쿼리·규모·수명·SLO를 정리한다. |
| 원장 저장소 | 승인된 상태와 transaction을 보존한다. |
| 파생 파이프라인 | CDC·batch로 색인·cache·분석 저장소를 갱신한다. |
| Read model | 사용자 화면과 검색에 맞춘 조회 모델을 제공한다. |
| 복구 경로 | 원장 backup과 파생 저장소 재구축을 분리한다. |
| 벤치마크 하네스 | 실제 분포·쿼리·failure를 재현한다. |

<!-- figure-spec
id: fig-ch18-01
chapter: ch18
role: storage-decision-matrix
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch18-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 불변조건·쿼리·규모·수명·일관성·운영성을 후보 저장소에 매핑한다.
required_labels_ko:
- 불변조건
- 조회 패턴
- 쓰기 패턴
- 규모
- 보존
- 복구
- 후보 저장소
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- postgres-transaction-iso
- dynamo-paper
- bigtable-paper
alt_ko: 불변조건·쿼리·규모·수명·일관성·운영성을 후보 저장소에 매핑한다.
caption_ko: 불변조건·쿼리·규모·수명·일관성·운영성을 후보 저장소에 매핑한다
status: specified
spec_file: assets/specs/svg/fig-ch18-01.md
-->

> **시각자료 제작 위치 — 불변조건·쿼리·규모·수명·일관성·운영성을 후보 저장소에 매핑한다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch18-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch18-01.md`  
> 대체 텍스트: 불변조건·쿼리·규모·수명·일관성·운영성을 후보 저장소에 매핑한다.


### 요청·데이터 흐름

1. 업무 불변조건과 단일 쓰기 소유자를 정한다.
2. 읽기·쓰기 패턴을 빈도·key·범위·payload로 정리한다.
3. 데이터 규모·성장·보존·삭제 요구를 계산한다.
4. 후보 저장소를 필수 조건으로 먼저 거른다.
5. 실제 데이터 분포와 쿼리로 작은 proof를 수행한다.
6. 장애·복구·schema evolution을 함께 시험한다.
7. 선택과 탈출 경로를 ADR에 기록한다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

### 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| 단일 범용 DB | transaction·backup·운영이 단순하다. | 검색·graph·대규모 blob 같은 특수 패턴 효율이 낮을 수 있다. | 대부분의 초기·중간 시스템 |
| 원장+파생 저장소 | 핵심 불변조건과 특수 조회를 각각 최적화한다. | 동기화·staleness·rebuild 운영이 필요하다. | 검색·분석·추천이 있는 시스템 |
| 다중 독립 원장 | 도메인별 독립 확장과 소유가 가능하다. | cross-domain transaction과 데이터 거버넌스가 복잡하다. | 명확한 bounded context와 운영 역량 |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@postgres-transaction-iso; @dynamo-paper; @bigtable-paper]를 참조한다.

### 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| 벤치마크 왜곡 | 균등 random key로만 시험해 실제 hot tenant와 범위 조회를 놓친다. | 운영 분포·payload·concurrency·장애를 재현한다. |
| 기능 체크리스트 선택 | 제품 기능 수는 많지만 핵심 쿼리와 복구가 불안정하다. | 필수 여정과 운영 증거에 가중한다. |
| 파생 저장소 원장화 | 검색 index가 직접 수정돼 원본과 수렴 경로가 사라진다. | 쓰기 소유자를 원장으로 제한하고 재구축을 정기 시험한다. |
| Schema lock-in | 데이터 변환과 export가 검증되지 않아 탈퇴가 어렵다. | 정기 export·restore·dual-read proof를 수행한다. |
| 운영 역량 부족 | 기술은 맞지만 on-call과 backup·upgrade가 감당되지 않는다. | 관리형 서비스 또는 더 단순한 저장소를 선택한다. |

<!-- figure-spec
id: fig-ch18-02
chapter: ch18
role: system-of-record-and-derived
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch18-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 원장 DB에서 CDC로 cache·search·analytics를 만드는 흐름과 rebuild 경계를 보여준다.
required_labels_ko:
- 원장 DB
- CDC
- Cache
- Search Index
- Analytics
- 재구축
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- postgres-transaction-iso
- dynamo-paper
- bigtable-paper
alt_ko: 원장 DB에서 CDC로 cache·search·analytics를 만드는 흐름과 rebuild 경계를 보여준다.
caption_ko: 원장 DB에서 CDC로 cache·search·analytics를 만드는 흐름과 rebuild 경계를 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch18-02.md
-->

> **시각자료 제작 위치 — 원장 DB에서 CDC로 cache·search·analytics를 만드는 흐름과 rebuild 경계를 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch18-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch18-02.md`  
> 대체 텍스트: 원장 DB에서 CDC로 cache·search·analytics를 만드는 흐름과 rebuild 경계를 보여준다.


### 확장 전략

- 한계에 도달한 축이 저장량인지 QPS인지 쿼리 복잡도인지 먼저 측정한다.
- 읽기 모델을 추가하기 전에 index·query·connection·batch를 최적화한다.
- 데이터를 수명·온도·tenant로 tiering한다.
- 재구축 가능한 파생 데이터는 원장과 다른 RPO/RTO를 적용한다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

### 보안과 개인정보

- 민감 데이터의 저장 위치·암호화 키·접근 감사를 후보 평가에 포함한다.
- 삭제·보존 정책이 replica·index·backup에 실제 적용되는지 시험한다.
- 관리형 서비스의 운영자 접근·지원 데이터 처리·export 권한을 검토한다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

### 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- 쿼리 패턴별 p95/p99·rows scanned·cache hit
- write amplification·compaction·replication lag
- storage growth·working set·index size
- backup/restore·rebuild 시간
- schema change와 failed migration

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

### 비용과 운영 복잡도

- 저장소 라이선스·인스턴스보다 인덱스·egress·backup·운영 인력 비용을 포함한다.
- 여러 저장소는 각 connector·schema·security·upgrade 비용을 곱한다.
- 과도한 미래 대비는 현재 학습과 장애 표면을 키운다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

### 흔한 오해와 안티패턴

- 유명 기업이 쓰는 저장소를 규모 근거 없이 채택한다.
- “NoSQL은 schema가 없다”고 생각한다.
- 벤치마크에서 평균 latency와 정상 상태만 측정한다.
- 파생 저장소의 rebuild 시간을 모른다.

### 설계 리뷰

- [ ] 핵심 불변조건과 원장이 명확한가?
- [ ] 실제 access pattern과 데이터 분포가 문서화됐는가?
- [ ] 후보의 실패·복구·migration을 시험했는가?
- [ ] 파생 데이터의 staleness와 rebuild 경로가 있는가?
- [ ] 팀이 운영할 수 있는 기술 수를 넘지 않는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

### 연습문제

1. 쇼핑몰의 주문, 상품 검색, 이미지, 추천 embedding에 저장소 역할을 배정하라.
2. 후보 DB 벤치마크에 포함할 데이터 분포·쿼리·장애 항목을 작성하라.
3. 새 검색 저장소를 제거하고 원장으로 되돌아갈 탈출 계획을 설계하라.

### 핵심 요약

- 저장소는 access pattern과 불변조건에서 선택한다.
- 원장과 파생 저장소의 책임을 분리한다.
- 실제 분포와 실패를 포함해 벤치마크한다.
- polyglot은 동기화·보안·복구 비용을 만든다.
- 탈출과 재구축 가능성을 채택 전에 검증한다.

### 출처

- [@postgres-transaction-iso] PostgreSQL Global Development Group. **PostgreSQL Documentation — Transaction Isolation** (2026). https://www.postgresql.org/docs/current/transaction-iso.html
- [@dynamo-paper] Giuseppe DeCandia et al.. **Dynamo: Amazon's Highly Available Key-value Store** (2007). https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf
- [@bigtable-paper] Fay Chang et al.. **Bigtable: A Distributed Storage System for Structured Data** (2006). https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
