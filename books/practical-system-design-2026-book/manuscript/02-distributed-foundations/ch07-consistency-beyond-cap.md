---
id: ch07
title: CAP를 넘어선 일관성 모델
part: distributed-foundations
order: 7
status: draft
freshness: durable
last_verified: '2026-08-06'
review_due: '2028-08-06'
upstream_lineage:
- source: system-design-primer
  file: README.md
  anchor: cap-theorem
  action: REWRITE
audiences:
- backend-engineer
- platform-engineer
prerequisites:
- ch05
- ch06
learning_objectives:
- CAP가 다루는 조건과 다루지 않는 조건을 설명한다.
- 선형화 가능성·인과·최종 일관성을 사용자 경험과 연결한다.
- 읽기·쓰기 경로별 일관성 요구를 선택한다.
figures:
- fig-ch07-01
- fig-ch07-02
sources:
- gilbert-lynch-cap
- vogels-eventual
- dynamo-paper
draft_notice: 기술·편집·접근성 검수 전 초고
---

# 07. CAP를 넘어선 일관성 모델

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

## 이 장에서 해결할 문제

CAP는 “세 가지 중 두 개를 고르는 제품 분류표”가 아니다. 네트워크 분할 중에도 모든 요청에 응답할지, 하나의 원자적 최신 값처럼 보이게 할지의 충돌을 설명한다. 실제 설계에서는 정상 상태 지연, 세션 보장, 충돌 해결, 격리 수준까지 별도로 선택해야 한다.

이 절의 기준 출처: [@gilbert-lynch-cap; @vogels-eventual].

### 학습 목표

- CAP가 다루는 조건과 다루지 않는 조건을 설명한다.
- 선형화 가능성·인과·최종 일관성을 사용자 경험과 연결한다.
- 읽기·쓰기 경로별 일관성 요구를 선택한다.

## 먼저 결론

- 분할 허용성은 선택 옵션이 아니라 분산 네트워크가 실패할 수 있다는 조건이다.
- 강한 일관성은 모든 데이터와 모든 연산에 동일하게 적용할 필요가 없다.
- 사용자에게 필요한 read-your-writes와 monotonic reads를 먼저 명시한다.
- 충돌을 허용하면 병합 규칙과 의미적 불변조건을 설계해야 한다.

## 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | CAP를 넘어선 일관성 모델에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | 분할 허용성은 선택 옵션이 아니라 분산 네트워크가 실패할 수 있다는 조건이다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | 키·tenant·지역별로 일관성 수준을 다르게 적용하되 API 의미를 명확히 한다. |
| 실패·복구 | “네트워크 분할” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | 쓰기 소유권을 제한하거나 충돌을 의미적으로 병합한다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | 권한·정책 변경이 오래된 복제본에서 허용되지 않도록 강한 읽기 또는 짧은 만료를 사용한다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | 복제 지연 분포와 최대 staleness |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

## 핵심 개념

### CAP의 C

모든 성공한 연산이 하나의 원자적 순서로 보이는 선형화 가능성에 해당하는 강한 조건이다.

### Availability

분할 상황에서도 비실패 노드가 받은 모든 요청에 응답하는 성질을 의미한다.

### Partition

노드 간 메시지가 손실되거나 임의로 지연되는 조건이다.

### 선형화 가능성

각 연산이 호출과 응답 사이 한 시점에 즉시 일어난 것처럼 보이는 모델이다.

### 인과 일관성

원인과 결과 관계가 있는 연산 순서는 모두가 동일하게 관찰하도록 보장한다.

### 세션 보장

read-your-writes, monotonic reads/writes처럼 한 사용자 세션에서 필요한 보장이다.

### 최종 일관성

새 업데이트가 없으면 복제본이 언젠가 같은 값으로 수렴하는 성질이며 수렴 시간과 충돌 의미를 추가로 정의해야 한다.

핵심 개념의 정의와 범위는 [@gilbert-lynch-cap; @vogels-eventual; @dynamo-paper]를 기준으로 재검토해야 한다.

## 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| 쓰기 조정자 | 쓰기 순서·버전·quorum을 결정한다. |
| 복제본 집합 | 독립 장애 도메인에 상태를 저장한다. |
| 읽기 라우터 | 필요한 일관성 수준에 따라 leader·quorum·로컬 복제본을 선택한다. |
| 버전 메타데이터 | 논리 시계·버전 벡터·타임스탬프로 충돌을 감지한다. |
| 충돌 해석기 | 업무 규칙에 따라 병합·거부·사용자 확인을 수행한다. |
| 세션 토큰 | 클라이언트가 본 최소 버전이나 region affinity를 전달한다. |

<!-- figure-spec
id: fig-ch07-01
chapter: ch07
role: cap-partition-timeline
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch07-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 두 복제본 사이 분할 중 쓰기·읽기 선택과 응답 결과를 시간축으로 보여준다.
required_labels_ko:
- 클라이언트 A
- 복제본 A
- 네트워크 분할
- 복제본 B
- 클라이언트 B
- 성공
- 거부
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- gilbert-lynch-cap
- vogels-eventual
- dynamo-paper
alt_ko: 두 복제본 사이 분할 중 쓰기·읽기 선택과 응답 결과를 시간축으로 보여준다.
caption_ko: 두 복제본 사이 분할 중 쓰기·읽기 선택과 응답 결과를 시간축으로 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch07-01.md
-->

> **시각자료 제작 위치 — 두 복제본 사이 분할 중 쓰기·읽기 선택과 응답 결과를 시간축으로 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch07-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch07-01.md`  
> 대체 텍스트: 두 복제본 사이 분할 중 쓰기·읽기 선택과 응답 결과를 시간축으로 보여준다.

## 요청·데이터 흐름

1. 연산별 불변조건과 사용자 기대를 분류한다.
2. 분할·리더 상실 시 허용할 응답을 결정한다.
3. 쓰기 acknowledgement 조건과 읽기 소스를 정한다.
4. 세션 토큰 또는 버전 조건을 전달한다.
5. 동시 쓰기 충돌을 감지한다.
6. 자동 병합 불가능한 충돌은 명시적 워크플로로 보낸다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

## 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| Leader 기반 강한 읽기 | 순서와 불변조건을 이해하기 쉽다. | 원격 leader 지연과 분할 중 쓰기 중단이 발생한다. | 결제 잔액·유일성·권한 변경 |
| Quorum 읽기/쓰기 | 일부 노드 실패를 견디며 조정 가능하다. | 지연·repair·sloppy quorum 의미가 복잡하다. | 복제 KV·메타데이터 |
| 로컬 eventual 읽기 | 지역 지연과 가용성이 좋다. | 오래된 값·역전·충돌을 사용자 흐름에서 처리해야 한다. | 피드·통계·검색 색인 |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@gilbert-lynch-cap; @vogels-eventual; @dynamo-paper]를 참조한다.

## 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| 네트워크 분할 | 각 지역이 독립 쓰기를 받아 동일 키가 갈라진다. | 쓰기 소유권을 제한하거나 충돌을 의미적으로 병합한다. |
| 복제 지연 | 사용자가 방금 쓴 값을 다른 복제본에서 읽지 못한다. | 세션 affinity, version token, leader read를 적용한다. |
| 시계 오차 | last-write-wins가 실제 인과관계를 뒤집는다. | 물리 시간만으로 충돌을 해결하지 않고 논리 버전을 사용한다. |
| read repair 폭증 | 오래된 복제본 수리가 사용자 읽기 경로를 느리게 한다. | background repair와 repair budget을 둔다. |
| 유령 성공 | client timeout 후 쓰기는 성공했지만 재시도로 중복 상태가 생긴다. | idempotency key와 결과 조회 계약을 둔다. |

<!-- figure-spec
id: fig-ch07-02
chapter: ch07
role: consistency-spectrum
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch07-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 선형화·순차·인과·세션·최종 일관성을 보장과 비용 관점에서 비교한다.
required_labels_ko:
- 선형화 가능성
- 순차 일관성
- 인과 일관성
- 세션 보장
- 최종 일관성
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- gilbert-lynch-cap
- vogels-eventual
- dynamo-paper
alt_ko: 선형화·순차·인과·세션·최종 일관성을 보장과 비용 관점에서 비교한다.
caption_ko: 선형화·순차·인과·세션·최종 일관성을 보장과 비용 관점에서 비교한다
status: specified
spec_file: assets/specs/svg/fig-ch07-02.md
-->

> **시각자료 제작 위치 — 선형화·순차·인과·세션·최종 일관성을 보장과 비용 관점에서 비교한다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch07-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch07-02.md`  
> 대체 텍스트: 선형화·순차·인과·세션·최종 일관성을 보장과 비용 관점에서 비교한다.

## 확장 전략

- 키·tenant·지역별로 일관성 수준을 다르게 적용하되 API 의미를 명확히 한다.
- 강한 경로는 범위를 좁혀 quorum 지연과 coordinator 부하를 줄인다.
- eventual 경로는 anti-entropy와 최대 허용 staleness를 운영 지표로 둔다.
- 다중 writer는 충돌률과 병합 실패율이 낮을 때만 이점을 갖는다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

## 보안과 개인정보

- 권한·정책 변경이 오래된 복제본에서 허용되지 않도록 강한 읽기 또는 짧은 만료를 사용한다.
- 삭제 요청이 모든 복제본·색인·백업에 전파되는 시간을 추적한다.
- 충돌 로그에 민감한 본문 대신 버전·해시·식별자를 최소한으로 기록한다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

## 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- 복제 지연 분포와 최대 staleness
- quorum 실패·leader unavailable 비율
- 충돌 감지·자동 병합·수동 해결 건수
- read-your-writes 위반 탐지
- repair backlog와 오래된 replica 수

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

## 비용과 운영 복잡도

- 강한 일관성은 조정과 원격 왕복 비용을 만든다.
- 다중 writer는 평상시 지연을 줄여도 충돌 처리와 운영 복잡도를 늘린다.
- 세션 보장은 전체 선형화보다 저렴하게 사용자 기대를 만족시킬 수 있다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

## 흔한 오해와 안티패턴

- CAP를 데이터베이스 제품에 CP/AP 라벨 하나로 붙인다.
- “eventual”을 언제든 틀린 값을 반환해도 된다는 뜻으로 사용한다.
- 격리 수준과 복제 일관성을 같은 개념으로 혼동한다.
- last-write-wins를 업무 의미와 무관한 안전한 기본값으로 둔다.

## 설계 리뷰

- [ ] 분할 중 각 연산이 성공·실패·대기 중 무엇을 하는가?
- [ ] 사용자에게 필요한 세션 보장이 정의됐는가?
- [ ] 충돌 감지와 병합이 도메인 불변조건을 보존하는가?
- [ ] 최대 staleness와 복제 지연을 관측하는가?
- [ ] 권한·삭제 같은 보안 상태에 더 강한 정책이 적용되는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

## 연습문제

1. 장바구니 수량, 은행 잔액, 좋아요 수 각각에 적절한 일관성 모델을 선택하고 이유를 쓰라.
2. 다중 리전에서 read-your-writes를 제공하는 세 가지 방법을 비교하라.
3. last-write-wins가 할인 쿠폰 사용 횟수 불변조건을 깨뜨리는 시나리오를 구성하라.

## 핵심 요약

- CAP는 분할 중 선형화 가능성과 모든 요청 응답의 충돌을 설명한다.
- 정상 상태의 지연·격리·세션 보장은 별도 설계 문제다.
- 일관성은 데이터가 아니라 연산과 불변조건 단위로 선택한다.
- eventual 시스템도 수렴·staleness·충돌 규칙이 필요하다.
- 사용자 경험에 필요한 최소 보장을 명시하는 것이 출발점이다.

## 출처

- [@gilbert-lynch-cap] Seth Gilbert and Nancy Lynch. **Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services** (2002). https://doi.org/10.1145/564585.564601
- [@vogels-eventual] Werner Vogels. **Eventually Consistent** (2009). https://dl.acm.org/doi/10.1145/1435417.1435432
- [@dynamo-paper] Giuseppe DeCandia et al.. **Dynamo: Amazon's Highly Available Key-value Store** (2007). https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
