---
id: ch26
title: Circuit Breaker·Bulkhead·Backpressure·Load Shedding
part: production
order: 26
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
- ch25
learning_objectives:
- 장애 격리와 과부하 제어 패턴의 역할을 구분한다.
- backpressure를 생산자까지 전달한다.
- load shedding과 graceful degradation 우선순위를 설계한다.
figures:
- fig-ch26-01
- fig-ch26-02
sources:
- google-sre-overload
- aws-timeouts-retries
draft_notice: 기술·편집·접근성 검수 전 초고
---

## 26. Circuit Breaker·Bulkhead·Backpressure·Load Shedding

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

### 이 장에서 해결할 문제

복원력 패턴은 실패한 하위를 숨기는 장식이 아니다. circuit breaker는 반복 실패 호출을 줄이고, bulkhead는 자원 풀을 격리하며, backpressure는 생산 속도를 늦추고, load shedding은 감당할 수 없는 요청을 명시적으로 버린다.

이 절의 기준 출처: [@google-sre-overload; @aws-timeouts-retries].

#### 학습 목표

- 장애 격리와 과부하 제어 패턴의 역할을 구분한다.
- backpressure를 생산자까지 전달한다.
- load shedding과 graceful degradation 우선순위를 설계한다.

### 먼저 결론

- 과부하를 queue 증가로 숨기지 말고 admission 단계에서 제한한다.
- circuit breaker는 health oracle이 아니라 최근 실패를 바탕으로 한 로컬 보호 장치다.
- bulkhead는 중요한 workload가 비핵심 workload에 자원을 빼앗기지 않게 한다.
- shed 정책은 우선순위·공정성·사용자에게 보이는 오류 의미를 가져야 한다.

### 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | Circuit Breaker·Bulkhead·Backpressure·Load Shedding에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | 과부하를 queue 증가로 숨기지 말고 admission 단계에서 제한한다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | global limit와 instance limit를 조합해 scale-out 중 double admission을 막는다. |
| 실패·복구 | “Breaker herd” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | randomized probe와 global load signal을 사용한다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | quota·priority를 client가 임의 조작하지 못하게 서버 정책에서 결정한다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | admitted/rejected/shed 요청과 이유 |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

### 핵심 개념

#### Circuit breaker

실패율·지연이 임계치를 넘으면 일정 기간 호출을 빠르게 실패시키고 probe로 회복을 확인한다.

#### Bulkhead

thread·connection·queue·tenant capacity를 분리해 실패 전파를 줄인다.

#### Backpressure

consumer가 감당할 수 있는 속도를 producer에게 전달하거나 수신을 늦추는 메커니즘이다.

#### Load shedding

처리 능력을 넘은 요청을 의도적으로 거부·축소하는 전략이다.

#### Admission control

요청을 작업 큐에 넣기 전에 현재 자원과 정책으로 허용 여부를 결정한다.

#### Graceful degradation

전체 실패 대신 비핵심 기능·정확도·신선도를 낮춰 핵심 여정을 유지한다.

#### Adaptive concurrency

관측된 지연·queue로 허용 동시성을 동적으로 조절한다.

핵심 개념의 정의와 범위는 [@google-sre-overload; @aws-timeouts-retries]를 기준으로 재검토해야 한다.

### 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| Ingress limiter | tenant·priority·global quota를 적용한다. |
| Admission controller | queue·CPU·downstream 건강으로 수락 여부를 정한다. |
| Bulkhead pools | 핵심/비핵심 또는 tenant별 자원을 격리한다. |
| Circuit breaker | dependency별 closed/open/half-open 상태를 관리한다. |
| Backpressure channel | credit·window·lag·429/503로 생산 속도를 제어한다. |
| Degradation policy | cache·partial result·read-only·feature off를 선택한다. |
| Recovery controller | probe와 점진 트래픽으로 정상 상태를 복원한다. |

<!-- figure-spec
id: fig-ch26-01
chapter: ch26
role: resilience-patterns
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch26-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: ingress에서 admission·bulkhead·circuit·backpressure·degradation이 적용되는 위치를 보여준다.
required_labels_ko:
- Ingress
- Admission
- Bulkhead
- Circuit Breaker
- Downstream
- Backpressure
- Degradation
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- google-sre-overload
- aws-timeouts-retries
alt_ko: ingress에서 admission·bulkhead·circuit·backpressure·degradation이 적용되는 위치를 보여준다.
caption_ko: ingress에서 admission·bulkhead·circuit·backpressure·degradation이 적용되는 위치를 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch26-01.md
-->

> **시각자료 제작 위치 — ingress에서 admission·bulkhead·circuit·backpressure·degradation이 적용되는 위치를 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch26-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch26-01.md`  
> 대체 텍스트: ingress에서 admission·bulkhead·circuit·backpressure·degradation이 적용되는 위치를 보여준다.

### 요청·데이터 흐름

1. 요청에 우선순위·tenant·비용 추정치를 붙인다.
2. ingress quota와 현재 동시성 한도를 검사한다.
3. 허용 요청을 해당 bulkhead queue에 넣는다.
4. 하위 호출 전에 circuit 상태와 남은 deadline을 확인한다.
5. 포화 시 producer에게 backpressure 또는 명시적 거부를 보낸다.
6. degradation 단계에서 비핵심 작업을 생략한다.
7. 회복 시 probe와 작은 트래픽으로 한도를 점진 확대한다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

### 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| 고정 limit | 예측 가능하고 검증이 단순하다. | 트래픽·인스턴스·latency 변화에 과소/과대 제한될 수 있다. | 안정된 workload |
| Adaptive limit | 실제 latency와 queue에 따라 포화 전 보호한다. | 진동·잘못된 신호·튜닝 위험이 있다. | 변동 큰 service |
| Queue buffering | 짧은 burst를 흡수한다. | 작업 가치가 만료되고 memory·tail이 증가한다. | 짧고 복구 가능한 burst |
| Load shedding | 핵심 요청의 SLO를 보호한다. | 거부 정책과 사용자 영향이 필요하다. | 지속 과부하 |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@google-sre-overload; @aws-timeouts-retries]를 참조한다.

### 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| Breaker herd | 모든 instance가 같은 시점에 half-open probe를 보내 하위를 다시 압박한다. | randomized probe와 global load signal을 사용한다. |
| Queue collapse | 무한 queue가 timeout된 요청을 계속 처리한다. | 유한 queue, deadline-aware dequeue, stale work drop을 적용한다. |
| Priority inversion | 비핵심 긴 작업이 핵심 짧은 작업의 pool을 점유한다. | bulkhead와 weighted fair scheduling을 사용한다. |
| Backpressure loss | 중간 broker가 생산자 속도를 늦추지 못해 lag가 무한 증가한다. | credit·quota·producer pause와 retention 경보를 연결한다. |
| Unfair shedding | 같은 고객군이 계속 먼저 거부된다. | tenant별 quota·공정성 지표·sampling을 적용한다. |

<!-- figure-spec
id: fig-ch26-02
chapter: ch26
role: overload-state-machine
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch26-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 정상·압박·shed·복구 상태와 진입·복원 조건을 보여준다.
required_labels_ko:
- 정상
- 압박
- Load Shedding
- Degraded
- Probe
- 복구
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- google-sre-overload
- aws-timeouts-retries
alt_ko: 정상·압박·shed·복구 상태와 진입·복원 조건을 보여준다.
caption_ko: 정상·압박·shed·복구 상태와 진입·복원 조건을 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch26-02.md
-->

> **시각자료 제작 위치 — 정상·압박·shed·복구 상태와 진입·복원 조건을 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch26-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch26-02.md`  
> 대체 텍스트: 정상·압박·shed·복구 상태와 진입·복원 조건을 보여준다.

### 확장 전략

- global limit와 instance limit를 조합해 scale-out 중 double admission을 막는다.
- 비용 추정치가 큰 요청은 별도 pool·async job으로 분리한다.
- degradation은 단계별 feature flag와 자동 복원 조건을 둔다.
- circuit 상태를 모든 장애의 단일 진실로 공유하지 않고 각 호출자의 보호 경계로 사용한다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

### 보안과 개인정보

- quota·priority를 client가 임의 조작하지 못하게 서버 정책에서 결정한다.
- shed 응답이 사용자 존재·권한 여부를 노출하지 않게 일관된 오류를 사용한다.
- 관리자 bypass는 제한된 break-glass와 감사가 필요하다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

### 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- admitted/rejected/shed 요청과 이유
- queue depth·wait·expired work
- bulkhead별 saturation·starvation
- breaker state·open reason·probe success
- backpressure signal·producer rate·consumer lag
- degradation 단계와 사용자 SLI

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

### 비용과 운영 복잡도

- 여유 용량과 격리 pool은 직접 비용이지만 전체 장애 비용을 줄인다.
- 무한 queue는 인프라 비용뿐 아니라 이미 가치 없는 작업 처리 비용을 만든다.
- 세밀한 priority 정책은 운영·제품 합의 비용을 요구한다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

### 흔한 오해와 안티패턴

- circuit breaker를 모든 오류에 복사하면 안정적이라고 생각한다.
- queue를 키워 overload를 해결한다.
- 429/503 없이 연결을 느리게 하는 것만 backpressure라고 부른다.
- load shedding을 무작위 오류로 구현한다.

### 설계 리뷰

- [ ] 포화 신호와 admission 기준이 실제 병목을 반영하는가?
- [ ] 핵심·비핵심 workload가 자원 수준에서 격리되는가?
- [ ] producer까지 backpressure가 전달되는가?
- [ ] shed 우선순위와 공정성이 합의됐는가?
- [ ] 회복 시 probe와 점진 확대가 있는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

### 연습문제

1. 검색 API에서 철자 교정·추천·개인화를 단계적으로 끄는 degradation 정책을 설계하라.
2. 무한 queue가 2초 deadline 작업을 30초 뒤 처리하는 문제를 고쳐라.
3. tenant별 fair shedding과 global overload limit를 함께 설계하라.

### 핵심 요약

- circuit breaker·bulkhead·backpressure·shedding은 서로 다른 문제를 해결한다.
- 무한 queue는 overload를 숨기고 tail을 악화한다.
- admission control은 작업을 시작하기 전에 보호한다.
- degradation은 핵심 사용자 여정을 보존한다.
- 회복도 점진적이고 관측 가능해야 한다.

### 출처

- [@google-sre-overload] Google. **Site Reliability Engineering — Handling Overload** (2016). https://sre.google/sre-book/handling-overload/
- [@aws-timeouts-retries] Amazon Web Services. **Timeouts, retries, and backoff with jitter** (2026). https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
