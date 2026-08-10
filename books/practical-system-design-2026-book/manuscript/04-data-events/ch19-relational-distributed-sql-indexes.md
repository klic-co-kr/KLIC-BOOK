---
id: ch19
title: 관계형 DB·분산 SQL·인덱스
part: data-events
order: 19
status: draft
freshness: current
last_verified: '2026-08-06'
review_due: '2027-02-06'
upstream_lineage:
- source: system-design-primer
  file: README.md
  anchor: relational-database-management-system
  action: REWRITE
audiences:
- backend-engineer
- platform-engineer
prerequisites:
- ch08
- ch10
- ch11
- ch18
learning_objectives:
- 관계형 모델과 인덱스의 비용을 쿼리 계획으로 설명한다.
- 수직 확장·읽기 복제·샤딩·분산 SQL의 경계를 비교한다.
- 온라인 schema·index 변경을 안전하게 수행한다.
figures:
- fig-ch19-01
- fig-ch19-02
sources:
- postgres-indexes
- postgres-transaction-iso
- spanner-paper
draft_notice: 기술·편집·접근성 검수 전 초고
---

# 19. 관계형 DB·분산 SQL·인덱스

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

## 이 장에서 해결할 문제

관계형 데이터베이스의 강점은 단순히 SQL 문법이 아니라 제약, transaction, optimizer, 성숙한 복구 도구가 결합된 데 있다. 분산 SQL은 이 모델을 여러 노드로 확장하지만 원격 transaction과 데이터 배치 비용을 없애지는 않는다.

이 절의 기준 출처: [@postgres-indexes; @postgres-transaction-iso].

### 학습 목표

- 관계형 모델과 인덱스의 비용을 쿼리 계획으로 설명한다.
- 수직 확장·읽기 복제·샤딩·분산 SQL의 경계를 비교한다.
- 온라인 schema·index 변경을 안전하게 수행한다.

## 먼저 결론

- 정규화와 denormalization은 읽기·쓰기·불변조건 비용의 선택이다.
- 인덱스는 읽기를 줄이는 대신 쓰기·저장·vacuum 비용을 늘린다.
- query plan과 실제 cardinality가 성능 판단의 근거다.
- 분산 SQL에서도 locality와 transaction 범위를 데이터 모델에 반영한다.

::: current-note
**2026-08-06 확인:** 이 장은 변화 가능한 표준·프로젝트·AI 구현을 포함한다. 기본 재검토일은 `2027-02-06`이며, 출판 직전 공식 문서를 다시 확인한다.
:::

## 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | 관계형 DB·분산 SQL·인덱스에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | 정규화와 denormalization은 읽기·쓰기·불변조건 비용의 선택이다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | connection pool을 DB 처리량과 transaction 길이에 맞추고 무제한 연결을 막는다. |
| 실패·복구 | “통계 부정확” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | analyze, extended statistics, plan regression 감시를 사용한다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | DB role을 애플리케이션 기능별 최소 권한으로 나눈다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | query fingerprint별 latency·rows·buffer I/O |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

## 핵심 개념

### 관계형 제약

PK, FK, UNIQUE, CHECK로 데이터 규칙을 DB가 검증한다.

### B-tree index

정렬된 키 구조로 equality·range·order query를 지원한다.

### Covering index

쿼리에 필요한 열을 index에서 충족해 table lookup을 줄인다.

### Query optimizer

통계와 비용 모델로 join 순서와 access path를 선택한다.

### Read replica

원장 변경을 복제해 읽기 부하를 분산한다.

### Distributed SQL

여러 노드에 partition·replication하면서 SQL transaction을 제공하는 계열이다.

### Online schema change

오래 잠그지 않고 expand·backfill·switch·contract로 구조를 변경하는 방식이다.

핵심 개념의 정의와 범위는 [@postgres-indexes; @postgres-transaction-iso; @spanner-paper]를 기준으로 재검토해야 한다.

## 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| SQL gateway | connection·parse·auth·route를 처리한다. |
| Transaction coordinator | 분산된 read/write의 commit을 조정한다. |
| Range/Shard replica | 키 범위를 저장하고 consensus로 복제한다. |
| Optimizer/statistics | 분산 비용과 cardinality를 추정한다. |
| Index set | 주요 access path와 제약을 지원한다. |
| Change pipeline | schema migration·backfill·validation을 수행한다. |
| Backup/PITR | WAL·snapshot으로 복구 지점을 제공한다. |

<!-- figure-spec
id: fig-ch19-01
chapter: ch19
role: relational-query-path
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch19-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: SQL이 parse·optimize·index/join·transaction·WAL로 처리되는 경로를 보여준다.
required_labels_ko:
- SQL Gateway
- Optimizer
- Index Scan
- Join
- Transaction
- WAL
- Replica
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- postgres-indexes
- postgres-transaction-iso
- spanner-paper
alt_ko: SQL이 parse·optimize·index/join·transaction·WAL로 처리되는 경로를 보여준다.
caption_ko: SQL이 parse·optimize·index/join·transaction·WAL로 처리되는 경로를 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch19-01.md
-->

> **시각자료 제작 위치 — SQL이 parse·optimize·index/join·transaction·WAL로 처리되는 경로를 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch19-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch19-01.md`  
> 대체 텍스트: SQL이 parse·optimize·index/join·transaction·WAL로 처리되는 경로를 보여준다.

## 요청·데이터 흐름

1. 요청이 transaction과 query를 시작한다.
2. optimizer가 통계로 local/remote plan을 선택한다.
3. route key가 있으면 필요한 shard로 직접 보낸다.
4. index scan·join·filter를 수행한다.
5. 다중 range 쓰기는 coordinator가 commit protocol을 수행한다.
6. WAL/log가 replica와 backup 경로로 전달된다.
7. slow query와 plan change를 관측해 통계를 갱신한다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

## 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| 단일 관계형 DB | 강한 transaction과 운영 단순성이 좋다. | 한 노드 한계와 지역 지연이 있다. | 대부분의 OLTP |
| Primary+read replica | 읽기 확장과 분석 격리에 유리하다. | stale read·lag·승격 복잡도가 있다. | 읽기 비중 높은 시스템 |
| 분산 SQL | 수평 저장·고가용성과 SQL 모델을 결합한다. | 원격 transaction·hot range·운영 비용이 있다. | 큰 데이터·다중 zone 강한 transaction |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@postgres-indexes; @postgres-transaction-iso; @spanner-paper]를 참조한다.

## 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| 통계 부정확 | optimizer가 작은 table로 예상한 결과가 커져 잘못된 join을 선택한다. | analyze, extended statistics, plan regression 감시를 사용한다. |
| 인덱스 폭증 | 모든 쿼리마다 index를 추가해 쓰기와 vacuum이 느려진다. | 사용률·중복·쓰기 비용을 정기 감사한다. |
| 긴 migration lock | DDL이 table을 잠가 요청이 쌓인다. | expand-contract, online build, lock timeout을 사용한다. |
| 분산 hot range | 순차 key가 한 range leader에 쓰기를 집중시킨다. | hash prefix·range split·키 설계를 조정한다. |
| Replica stale read | 방금 쓴 데이터를 follower에서 읽어 사용자 흐름이 깨진다. | session routing·LSN token·leader read를 사용한다. |

<!-- figure-spec
id: fig-ch19-02
chapter: ch19
role: scale-relational-options
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch19-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 단일 DB·read replica·application sharding·distributed SQL의 경계와 비용을 비교한다.
required_labels_ko:
- 단일 DB
- Read Replica
- Sharding
- Distributed SQL
- Coordination
- Locality
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- postgres-indexes
- postgres-transaction-iso
- spanner-paper
alt_ko: 단일 DB·read replica·application sharding·distributed SQL의 경계와 비용을 비교한다.
caption_ko: 단일 DB·read replica·application sharding·distributed SQL의 경계와 비용을 비교한다
status: specified
spec_file: assets/specs/svg/fig-ch19-02.md
-->

> **시각자료 제작 위치 — 단일 DB·read replica·application sharding·distributed SQL의 경계와 비용을 비교한다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch19-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch19-02.md`  
> 대체 텍스트: 단일 DB·read replica·application sharding·distributed SQL의 경계와 비용을 비교한다.

## 확장 전략

- connection pool을 DB 처리량과 transaction 길이에 맞추고 무제한 연결을 막는다.
- partition pruning과 route key로 scatter query를 줄인다.
- index-only scan·batch write·prepared statement를 실제 plan으로 검증한다.
- 분산 전환 전에 vertical scale·query·schema·archive로 한계를 늦춘다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

## 보안과 개인정보

- DB role을 애플리케이션 기능별 최소 권한으로 나눈다.
- row-level security를 사용해도 애플리케이션 tenant 검증과 테스트를 유지한다.
- backup·replica·query log에 동일한 민감 데이터 정책을 적용한다.
- migration 계정과 runtime 계정을 분리한다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

## 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- query fingerprint별 latency·rows·buffer I/O
- index hit·size·write amplification·unused index
- lock wait·deadlock·transaction age
- replication lag·WAL generation·checkpoint
- range hotspot·remote transaction 비율

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

## 비용과 운영 복잡도

- index와 replica는 저장·I/O·backup 비용을 지속적으로 만든다.
- 분산 SQL은 노드 수 외에 cross-region traffic와 operational expertise 비용이 있다.
- 쿼리 최적화와 archive가 더 싼 해결책인지 먼저 비교한다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

## 흔한 오해와 안티패턴

- ORM이 생성한 SQL을 보지 않는다.
- index가 많을수록 항상 빠르다고 생각한다.
- read replica를 강한 read처럼 사용한다.
- 분산 SQL이 data locality 문제를 자동 제거한다고 믿는다.

## 설계 리뷰

- [ ] 핵심 쿼리 plan과 cardinality가 측정됐는가?
- [ ] 제약이 애플리케이션 불변조건을 직접 보호하는가?
- [ ] index의 읽기 이득과 쓰기 비용을 평가했는가?
- [ ] schema 변경이 online·rollback 가능하게 설계됐는가?
- [ ] 분산 transaction과 hot range 비율이 알려져 있는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

## 연습문제

1. 주문 목록 쿼리의 복합 index 열 순서를 access pattern으로 설계하라.
2. 순차 timestamp PK가 분산 SQL hot range를 만드는 이유와 대안을 설명하라.
3. NOT NULL 열 추가를 expand-backfill-validate-contract로 배포하라.

## 핵심 요약

- 관계형 DB는 제약·transaction·optimizer·복구의 결합이다.
- 인덱스는 읽기와 쓰기 비용을 교환한다.
- query plan과 실제 통계로 판단한다.
- 분산 SQL에도 locality와 coordination 비용이 있다.
- schema 변경은 단계적이고 되돌릴 수 있어야 한다.

## 출처

- [@postgres-indexes] PostgreSQL Global Development Group. **PostgreSQL Documentation — Indexes** (2026). https://www.postgresql.org/docs/current/indexes.html
- [@postgres-transaction-iso] PostgreSQL Global Development Group. **PostgreSQL Documentation — Transaction Isolation** (2026). https://www.postgresql.org/docs/current/transaction-iso.html
- [@spanner-paper] James C. Corbett et al.. **Spanner: Google's Globally-Distributed Database** (2012). https://research.google/pubs/spanner-googles-globally-distributed-database/

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
