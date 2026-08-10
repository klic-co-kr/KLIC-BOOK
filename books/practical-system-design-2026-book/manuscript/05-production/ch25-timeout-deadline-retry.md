---
id: ch25
title: Timeout·Deadline·Retry·Backoff·Jitter
part: production
order: 25
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
- ch16
- ch23
learning_objectives:
- timeout과 end-to-end deadline을 구분한다.
- 재시도 가능 조건과 retry budget을 설계한다.
- backoff·jitter·idempotency로 동시 재시도 부하를 제어한다.
figures:
- chart-ch25-01
- fig-ch25-01
- fig-ch25-02
sources:
- aws-timeouts-retries
- google-sre-overload
- stripe-idempotency
draft_notice: 기술·편집·접근성 검수 전 초고
---

# 25. Timeout·Deadline·Retry·Backoff·Jitter

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

## 이 장에서 해결할 문제

timeout은 실패를 해결하지 않고 기다림을 중단할 뿐이다. 재시도는 성공 가능성을 높일 수 있지만 하위 시스템이 느린 원인이 과부하라면 같은 요청을 더 보내 상황을 악화시킨다. 전체 deadline과 한 계층의 retry 소유권이 필요하다.

이 절의 기준 출처: [@aws-timeouts-retries; @google-sre-overload].

### 학습 목표

- timeout과 end-to-end deadline을 구분한다.
- 재시도 가능 조건과 retry budget을 설계한다.
- backoff·jitter·idempotency로 동시 재시도 부하를 제어한다.

## 먼저 결론

- 각 hop이 독립 timeout을 시작하지 말고 상위 요청의 남은 deadline을 전달한다.
- 재시도는 일시적이며 다시 실행해도 안전한 오류에만 사용한다.
- backoff만으로 동시 client가 다시 맞춰지는 문제를 막지 못하므로 jitter를 사용한다.
- 최대 시도 수보다 전체 retry budget·추가 부하 비율을 제한한다.

## 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | Timeout·Deadline·Retry·Backoff·Jitter에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | 각 hop이 독립 timeout을 시작하지 말고 상위 요청의 남은 deadline을 전달한다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | 호출 graph가 깊어질수록 각 hop에 임의 비율로 timeout을 복사하지 않고 critical path 예산을 분배한다. |
| 실패·복구 | “Retry storm” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | 한 계층 소유, budget, exponential backoff, full jitter를 사용한다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | idempotency key가 사용자·operation scope에 묶이고 추측 불가능하거나 인증된 요청에만 유효하게 한다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | attempt별 latency와 최종 사용자 latency |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

<!-- figure-spec
id: chart-ch25-01
chapter: ch25
role: retry-amplification
kind: data-chart
generator: python-matplotlib
output: assets/charts/chart-ch25-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 호출 깊이와 계층별 시도 횟수가 최하위 요청 수를 지수적으로 늘리는 모습을 보여준다.
required_labels_ko:
- 호출 깊이
- 최대 최하위 시도 수
- 계층당 2회
- 계층당 3회
prohibited:
- 출처 없는 실측 수치
- 3D chart
- 잘린 축
- 색상만으로 구분
source_refs:
- aws-timeouts-retries
- google-sre-overload
alt_ko: 호출 깊이와 계층별 시도 횟수가 최하위 요청 수를 지수적으로 늘리는 모습을 보여준다.
caption_ko: 계층별 재시도 증폭
status: specified
spec_file: assets/specs/charts/chart-ch25-01.md
-->

> **시각자료 제작 위치 — 계층별 재시도 증폭**  
> 종류: `data-chart` · 상태: `specified` · 산출 경로: `assets/charts/chart-ch25-01.svg`  
> 제작 명세: `assets/specs/charts/chart-ch25-01.md`  
> 대체 텍스트: 호출 깊이와 계층별 시도 횟수가 최하위 요청 수를 지수적으로 늘리는 모습을 보여준다.


## 핵심 개념

### Timeout

한 작업이나 I/O를 더 기다리지 않기로 정한 한도다.

### Deadline

전체 요청이 완료돼야 하는 절대 시각 또는 남은 시간 예산이다.

### Retry

실패한 작업을 다시 시도하는 행위다.

### Backoff

연속 실패 사이 대기 시간을 늘리는 정책이다.

### Jitter

재시도 시점을 무작위화해 동기화된 폭주를 줄인다.

### Retry budget

정상 요청 대비 추가 시도량 또는 전체 시간·횟수를 제한하는 예산이다.

### Idempotency

같은 요청을 여러 번 수행해도 의도한 최종 효과가 한 번과 같도록 하는 성질이다.

핵심 개념의 정의와 범위는 [@aws-timeouts-retries; @google-sre-overload; @stripe-idempotency]를 기준으로 재검토해야 한다.

## 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| Client deadline | 사용자 경험과 전체 작업 한도를 정한다. |
| Ingress | deadline·request ID·idempotency key를 검증한다. |
| Retry owner | 한 계층에서 retry classification과 budget을 관리한다. |
| Downstream client | 남은 deadline보다 짧은 connect/read/write timeout을 적용한다. |
| Idempotency store | 요청 key와 진행·결과 상태를 보존한다. |
| Circuit/load signal | 과부하·Retry-After·queue 상태를 재시도 판단에 제공한다. |

<!-- figure-spec
id: fig-ch25-01
chapter: ch25
role: deadline-propagation
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch25-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 클라이언트 전체 deadline이 gateway·service·DB 호출의 남은 예산으로 줄어드는 흐름을 보여준다.
required_labels_ko:
- 클라이언트
- Gateway
- Service A
- Service B
- DB
- 남은 Deadline
- 취소
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- aws-timeouts-retries
- google-sre-overload
- stripe-idempotency
alt_ko: 클라이언트 전체 deadline이 gateway·service·DB 호출의 남은 예산으로 줄어드는 흐름을 보여준다.
caption_ko: 클라이언트 전체 deadline이 gateway·service·DB 호출의 남은 예산으로 줄어드는 흐름을 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch25-01.md
-->

> **시각자료 제작 위치 — 클라이언트 전체 deadline이 gateway·service·DB 호출의 남은 예산으로 줄어드는 흐름을 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch25-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch25-01.md`  
> 대체 텍스트: 클라이언트 전체 deadline이 gateway·service·DB 호출의 남은 예산으로 줄어드는 흐름을 보여준다.


## 요청·데이터 흐름

1. 클라이언트가 전체 deadline과 요청 식별자를 보낸다.
2. ingress가 남은 예산을 계산하고 이미 만료된 요청을 거부한다.
3. 하위 호출 전에 connect·request timeout을 예산 안에서 배분한다.
4. 오류를 retryable·permanent·unknown으로 분류한다.
5. retryable이고 예산이 남으면 jittered backoff 후 다시 시도한다.
6. 서버는 idempotency key로 중복 진행·완료 결과를 반환한다.
7. deadline 만료 시 하위 취소를 전파하고 늦은 결과 처리를 중단한다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

## 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| 고정 timeout, 무재시도 | 부하와 중복 효과가 예측 가능하다. | 짧은 일시 실패도 사용자 오류가 된다. | 비멱등·빠른 실패 선호 |
| 제한 재시도 | 일시 네트워크 오류를 흡수한다. | 부하 증폭과 tail 증가가 생긴다. | 멱등 읽기·작은 쓰기 |
| 비동기 job 전환 | 긴 작업을 durable queue와 상태 조회로 분리한다. | UX·상태 기계·취소가 복잡해진다. | 수초 이상 작업·외부 의존성 |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@aws-timeouts-retries; @google-sre-overload; @stripe-idempotency]를 참조한다.

## 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| Retry storm | 하위 장애 중 모든 client가 즉시 여러 번 재시도한다. | 한 계층 소유, budget, exponential backoff, full jitter를 사용한다. |
| Timeout mismatch | gateway는 2초인데 하위 작업은 30초 계속돼 자원이 누적된다. | deadline propagation과 cancellation을 적용한다. |
| Unknown outcome | client timeout 후 서버 commit 여부를 알 수 없다. | idempotency key와 결과 조회 endpoint를 둔다. |
| Too-short timeout | 정상 p99·DNS·TLS handshake를 포함하지 못해 가짜 오류를 만든다. | 단계별 분포와 cold path를 측정해 설정한다. |
| Too-long timeout | 실패한 요청이 thread·connection·memory를 오래 점유한다. | queue budget과 사용자 SLO에 맞춰 제한한다. |

<!-- figure-spec
id: fig-ch25-02
chapter: ch25
role: retry-backoff-jitter
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch25-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 여러 client의 동기 재시도와 jitter 적용 후 분산된 재시도를 비교한다.
required_labels_ko:
- Client 1
- Client 2
- Client 3
- 실패
- Backoff
- Jitter
- Retry Budget
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- aws-timeouts-retries
- google-sre-overload
- stripe-idempotency
alt_ko: 여러 client의 동기 재시도와 jitter 적용 후 분산된 재시도를 비교한다.
caption_ko: 여러 client의 동기 재시도와 jitter 적용 후 분산된 재시도를 비교한다
status: specified
spec_file: assets/specs/svg/fig-ch25-02.md
-->

> **시각자료 제작 위치 — 여러 client의 동기 재시도와 jitter 적용 후 분산된 재시도를 비교한다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch25-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch25-02.md`  
> 대체 텍스트: 여러 client의 동기 재시도와 jitter 적용 후 분산된 재시도를 비교한다.


## 확장 전략

- 호출 graph가 깊어질수록 각 hop에 임의 비율로 timeout을 복사하지 않고 critical path 예산을 분배한다.
- batch 요청은 항목별 실패와 전체 deadline을 분리한다.
- Retry-After와 서버 load signal을 존중한다.
- 재시도보다 fallback·cache·queue·degradation이 더 싼 경로인지 비교한다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

## 보안과 개인정보

- idempotency key가 사용자·operation scope에 묶이고 추측 불가능하거나 인증된 요청에만 유효하게 한다.
- 재시도 로그에 민감 payload를 반복 저장하지 않는다.
- timeout 오류가 내부 topology와 공급자 정보를 과도하게 노출하지 않게 한다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

## 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- attempt별 latency와 최종 사용자 latency
- timeout 단계(connect/read/write/queue)별 비율
- retry attempts·success-after-retry·amplification
- idempotency hit·conflict·in-progress
- deadline exceeded 후 계속 실행된 작업 수

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

## 비용과 운영 복잡도

- 재시도는 추가 compute·DB·egress를 소비한다.
- 너무 짧은 timeout은 오류·지원 비용을, 너무 긴 timeout은 자원·사용자 대기 비용을 만든다.
- idempotency 결과 보존 기간은 storage와 업무 재시도 창 사이의 선택이다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

## 흔한 오해와 안티패턴

- 모든 5xx를 같은 방식으로 재시도한다.
- 각 계층이 3회 재시도하면 총 3회라고 생각한다.
- timeout 값을 평균 latency의 두 배로 정한다.
- POST는 무조건 재시도 불가능하다고 단정하거나 반대로 key 없이 재시도한다.

## 설계 리뷰

- [ ] 전체 deadline과 hop별 timeout 관계가 명확한가?
- [ ] 오류별 retryability가 계약에 정의됐는가?
- [ ] 한 계층이 retry budget을 소유하는가?
- [ ] unknown outcome을 idempotency와 조회로 해결하는가?
- [ ] 재시도 증폭과 늦은 작업을 관측하는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

## 연습문제

1. 5단계 호출이 각자 3회 시도할 때 최악의 하위 호출 수를 계산하고 retry owner를 하나로 줄여라.
2. 결제 승인 timeout 후 결과를 모르는 상태를 idempotency key로 설계하라.
3. p99 400ms인 API의 1초 deadline 안에서 두 하위 호출 예산을 배분하라.

## 핵심 요약

- timeout은 기다림 중단, deadline은 전체 시간 계약이다.
- 재시도는 안전한 일시 오류와 멱등성에만 사용한다.
- retry budget과 jitter로 부하 증폭을 제한한다.
- unknown outcome에는 결과 조회가 필요하다.
- 취소와 남은 deadline을 하위까지 전달한다.

## 출처

- [@aws-timeouts-retries] Amazon Web Services. **Timeouts, retries, and backoff with jitter** (2026). https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
- [@google-sre-overload] Google. **Site Reliability Engineering — Handling Overload** (2016). https://sre.google/sre-book/handling-overload/
- [@stripe-idempotency] Stripe. **Stripe API — Idempotent requests** (2026). https://docs.stripe.com/api/idempotent_requests

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
