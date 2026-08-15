---
id: ch09
title: 시간·순서·논리 시계·분산 ID
part: distributed-foundations
order: 9
status: draft
freshness: durable
last_verified: '2026-08-06'
review_due: '2028-08-06'
upstream_lineage:
- source: new-2026-edition
  file: null
  anchor: null
  action: ADD
audiences:
- backend-engineer
- platform-engineer
prerequisites:
- ch05
- ch07
learning_objectives:
- 물리 시계와 논리적 순서를 구분한다.
- 인과 관계를 표현하는 시계와 버전 메타데이터를 선택한다.
- 분산 ID의 정렬성·고유성·정보 노출을 비교한다.
figures:
- fig-ch09-01
- fig-ch09-02
sources:
- lamport-time
- rfc9562
- dynamo-paper
draft_notice: 기술·편집·접근성 검수 전 초고
---

## 09. 시간·순서·논리 시계·분산 ID

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

### 이 장에서 해결할 문제

분산 시스템에는 모든 노드가 공유하는 완벽한 현재 시각이 없다. 벽시계는 만료·사용자 표시·운영 분석에 필요하지만, 사건의 인과 순서와 단일 승자를 정하는 근거로 사용하려면 오차·점프·동률을 다뤄야 한다.

이 절의 기준 출처: [@lamport-time; @rfc9562].

#### 학습 목표

- 물리 시계와 논리적 순서를 구분한다.
- 인과 관계를 표현하는 시계와 버전 메타데이터를 선택한다.
- 분산 ID의 정렬성·고유성·정보 노출을 비교한다.

### 먼저 결론

- 벽시계 타임스탬프와 논리적 버전을 분리한다.
- “먼저”가 업무적으로 필요한 곳만 순서를 강제한다.
- 시간 기반 ID는 정렬과 locality를 얻지만 생성 시간·트래픽 패턴을 노출할 수 있다.
- 시계 오차 한계와 동기화 실패를 관측하고 안전 여유에 포함한다.

### 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | 시간·순서·논리 시계·분산 ID에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | 벽시계 타임스탬프와 논리적 버전을 분리한다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | 전역 순서 대신 aggregate·partition 단위 순서를 사용해 조정을 줄인다. |
| 실패·복구 | “시계 역행” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | 마지막 발급 값 보존, 논리 카운터, 역행 시 차단을 사용한다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | ID에서 tenant·시간·region 정보를 불필요하게 노출하지 않는다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | 노드별 clock offset·동기화 상태 |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

### 핵심 개념

#### 벽시계

달력상의 시각을 나타내며 NTP 조정, leap second 처리, VM 일시정지 등으로 단조 증가하지 않을 수 있다.

#### 단조 시계

한 프로세스 안에서 경과 시간을 측정하는 데 적합하며 절대 시각과는 다르다.

#### Lamport clock

인과 관계가 있으면 논리 시계 값도 증가하도록 만드는 단순한 순서 메타데이터다.

#### Vector clock

여러 노드의 진행 상태를 벡터로 기록해 인과와 동시성을 구분한다.

#### Hybrid logical clock

물리 시간에 가까운 정렬성과 논리적 단조성을 결합한다.

#### 분산 ID

중앙 병목 없이 고유 식별자를 만들기 위한 UUID, 시간 정렬 ID, 구간 할당 등이다.

핵심 개념의 정의와 범위는 [@lamport-time; @rfc9562; @dynamo-paper]를 기준으로 재검토해야 한다.

### 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| 시간 동기화 계층 | 노드 시계 오차와 동기 상태를 관리한다. |
| ID 생성기 | 고유성·정렬성·가용성 정책에 따라 ID를 발급한다. |
| 버전 메타데이터 | 업데이트의 인과 관계와 동시성을 표현한다. |
| 순서 결정기 | 필요한 도메인 범위에서 단일 순서를 부여한다. |
| 저장·색인 계층 | ID와 버전의 정렬 특성을 활용하거나 hot partition을 방지한다. |
| 감사 계층 | 사용자 표시 시간과 처리 순서를 구분해 기록한다. |

<!-- figure-spec
id: fig-ch09-01
chapter: ch09
role: clock-models
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch09-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 벽시계·단조 시계·Lamport·vector·hybrid logical clock의 목적을 비교한다.
required_labels_ko:
- 벽시계
- 단조 시계
- Lamport Clock
- Vector Clock
- Hybrid Logical Clock
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- lamport-time
- rfc9562
- dynamo-paper
alt_ko: 벽시계·단조 시계·Lamport·vector·hybrid logical clock의 목적을 비교한다.
caption_ko: 벽시계·단조 시계·Lamport·vector·hybrid logical clock의 목적을 비교한다
status: specified
spec_file: assets/specs/svg/fig-ch09-01.md
-->

> **시각자료 제작 위치 — 벽시계·단조 시계·Lamport·vector·hybrid logical clock의 목적을 비교한다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch09-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch09-01.md`  
> 대체 텍스트: 벽시계·단조 시계·Lamport·vector·hybrid logical clock의 목적을 비교한다.


### 요청·데이터 흐름

1. 요구되는 순서의 범위를 전역·tenant·aggregate·partition으로 정한다.
2. 표시 시간, timeout 경과, 인과 버전에 서로 다른 시계를 선택한다.
3. ID에 필요한 고유성·정렬성·예측 불가능성을 정한다.
4. 노드 재시작·시계 역행·동일 밀리초 burst를 처리한다.
5. 수신 측에서 버전 비교와 중복 검사를 수행한다.
6. 감사 로그에는 발생 시각·수신 시각·처리 순서를 구분해 저장한다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

### 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| UUID v4 | 중앙 조정 없이 예측하기 어렵고 단순하다. | 무작위 인덱스 locality가 낮고 시간 정렬이 없다. | 공개 식별자·일반 객체 |
| 시간 정렬 UUID/ID | B-tree locality와 시간순 조회가 좋다. | 생성 시간 노출·동일 시각 충돌·노드 식별 관리가 필요하다. | 고속 쓰기·로그·이벤트 |
| 중앙 sequence | 작고 완전한 증가 순서를 제공한다. | 중앙 의존성과 다중 리전 지연이 생긴다. | 단일 DB 범위의 업무 번호 |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@lamport-time; @rfc9562; @dynamo-paper]를 참조한다.

### 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| 시계 역행 | VM 이동이나 동기화로 시간이 뒤로 가며 ID 중복·만료 오류가 난다. | 마지막 발급 값 보존, 논리 카운터, 역행 시 차단을 사용한다. |
| 노드 ID 충돌 | 두 생성기가 같은 worker ID로 같은 시각에 같은 값을 만든다. | lease 기반 할당과 fencing, 시작 전 충돌 검사를 둔다. |
| 전역 순서 착각 | 시간 정렬 ID를 모든 사건의 정확한 발생 순서로 해석한다. | 인과 관계와 수신·커밋 순서를 별도 기록한다. |
| hot partition | 시간 접두사가 같은 새 ID가 한 shard에 집중된다. | hash prefix, bucket, range split 전략을 적용한다. |
| 정보 노출 | 공개 ID로 생성 시각이나 대략적 거래량을 추정할 수 있다. | 외부 식별자와 내부 정렬 키를 분리한다. |

<!-- figure-spec
id: fig-ch09-02
chapter: ch09
role: distributed-id-layout
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch09-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 시간·노드·카운터·무작위 비트로 구성된 분산 ID와 인덱스 분포를 보여준다.
required_labels_ko:
- 시간 비트
- 노드 ID
- 순번
- 무작위
- 정렬
- Hot Partition
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- lamport-time
- rfc9562
- dynamo-paper
alt_ko: 시간·노드·카운터·무작위 비트로 구성된 분산 ID와 인덱스 분포를 보여준다.
caption_ko: 시간·노드·카운터·무작위 비트로 구성된 분산 ID와 인덱스 분포를 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch09-02.md
-->

> **시각자료 제작 위치 — 시간·노드·카운터·무작위 비트로 구성된 분산 ID와 인덱스 분포를 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch09-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch09-02.md`  
> 대체 텍스트: 시간·노드·카운터·무작위 비트로 구성된 분산 ID와 인덱스 분포를 보여준다.


### 확장 전략

- 전역 순서 대신 aggregate·partition 단위 순서를 사용해 조정을 줄인다.
- ID 발급 서비스가 필요하다면 구간 선할당과 지역별 namespace로 병목을 줄인다.
- 벡터 메타데이터 크기는 참여 노드 수와 함께 커지므로 안정된 replica set 또는 압축 전략을 사용한다.
- 감사·분석 파이프라인은 late event와 out-of-order event를 정상 조건으로 처리한다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

### 보안과 개인정보

- ID에서 tenant·시간·region 정보를 불필요하게 노출하지 않는다.
- 인증 토큰 만료 판단은 서버의 신뢰 가능한 시간과 허용 오차를 사용한다.
- 감사 로그 시간 조작을 탐지하고 원본 순서 증거를 보호한다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

### 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- 노드별 clock offset·동기화 상태
- ID 충돌·재발급·시계 역행 차단 건수
- out-of-order·late event 분포
- 버전 충돌과 동시 업데이트 비율
- 순서 결정 서비스의 지연·lease 상태

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

### 비용과 운영 복잡도

- 전역 순서는 조정·가용성·리전 지연 비용을 만든다.
- 긴 ID는 저장·색인·네트워크 비용을 조금 늘리지만 운영 단순성을 줄 수 있다.
- 시간 정렬 키는 쓰기 효율을 높일 수 있으나 shard hotspot 비용을 만든다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

### 흔한 오해와 안티패턴

- created_at을 인과 순서와 동일시한다.
- 밀리초 timestamp만으로 고유 ID를 만든다.
- DB auto-increment를 전 세계 서비스의 전역 순서로 확장한다.
- 시간 기반 공개 ID의 정보 노출을 무시한다.

### 설계 리뷰

- [ ] 업무적으로 필요한 순서 범위가 최소화됐는가?
- [ ] 표시 시간·경과 시간·인과 버전에 올바른 시계를 쓰는가?
- [ ] 시계 역행과 worker ID 충돌을 시험했는가?
- [ ] ID가 shard 분포와 개인정보에 미치는 영향을 평가했는가?
- [ ] late/out-of-order 사건을 운영 지표로 보고 있는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

### 연습문제

1. 채팅 메시지의 전역 순서가 꼭 필요한지 방·사용자·서버 범위로 나누어 논증하라.
2. UUID v4, UUID v7, 중앙 sequence를 주문 ID 요구에 맞춰 비교하라.
3. 서버 시계가 90초 앞으로 갔다가 복구되는 토큰 만료 시나리오를 설계하라.

### 핵심 요약

- 분산 시스템에서 절대 시간과 인과 순서는 다르다.
- 순서 보장은 필요한 범위로 제한한다.
- 논리 시계는 인과 관계와 동시성을 표현한다.
- 분산 ID는 고유성·정렬성·노출·분산 특성을 함께 선택한다.
- 시계와 ID 생성기도 장애·관측 대상이다.

### 출처

- [@lamport-time] Leslie Lamport. **Time, Clocks, and the Ordering of Events in a Distributed System** (1978). https://lamport.azurewebsites.net/pubs/time-clocks.pdf
- [@rfc9562] IETF. **RFC 9562 — Universally Unique IDentifiers (UUIDs)** (2024). https://www.rfc-editor.org/rfc/rfc9562.html
- [@dynamo-paper] Giuseppe DeCandia et al.. **Dynamo: Amazon's Highly Available Key-value Store** (2007). https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
