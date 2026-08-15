---
id: ch05
title: 지연시간·처리량·동시성과 Tail Latency
part: distributed-foundations
order: 5
status: draft
freshness: durable
last_verified: '2026-08-06'
review_due: '2028-08-06'
upstream_lineage:
- source: system-design-primer
  file: README.md
  anchor: latency-numbers-every-programmer-should-know
  action: REWRITE
audiences:
- backend-engineer
- platform-engineer
prerequisites:
- ch02
learning_objectives:
- 지연시간 분포와 처리량을 함께 해석한다.
- 큐잉과 fan-out이 tail latency를 증폭하는 이유를 설명한다.
- timeout·용량·복제 전략을 백분위 지표로 설계한다.
figures:
- chart-ch05-01
- fig-ch05-01
- fig-ch05-02
sources:
- dean-tail-at-scale
- google-sre-overload
- google-sre-book
draft_notice: 기술·편집·접근성 검수 전 초고
---

## 05. 지연시간·처리량·동시성과 Tail Latency

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

### 이 장에서 해결할 문제

평균 지연시간은 사용자의 나쁜 경험을 숨길 수 있다. 여러 하위 호출을 병렬로 수행하는 서비스에서는 각 호출의 작은 꼬리가 전체 요청의 꼬리로 증폭되므로 p95·p99와 큐잉 상태를 설계 입력으로 사용해야 한다.

이 절의 기준 출처: [@dean-tail-at-scale; @google-sre-overload].

#### 학습 목표

- 지연시간 분포와 처리량을 함께 해석한다.
- 큐잉과 fan-out이 tail latency를 증폭하는 이유를 설명한다.
- timeout·용량·복제 전략을 백분위 지표로 설계한다.

### 먼저 결론

- 지연시간과 처리량은 같은 숫자가 아니며 부하가 포화점에 가까워지면 함께 악화될 수 있다.
- 평균뿐 아니라 p50·p95·p99와 timeout 비율을 본다.
- fan-out 수가 커질수록 하나 이상의 느린 하위 호출을 만날 확률이 증가한다.
- 여유 용량, 요청 축소, hedging은 비용과 중복 부작용을 함께 평가한다.

### 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | 지연시간·처리량·동시성과 Tail Latency에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | 지연시간과 처리량은 같은 숫자가 아니며 부하가 포화점에 가까워지면 함께 악화될 수 있다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | 포화점보다 낮은 목표 사용률을 유지해 burst와 장애 전환 여유를 둔다. |
| 실패·복구 | “큐 폭증” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | 유한 큐, admission control, backpressure를 적용한다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | 고객 우선순위가 권한 우회로 악용되지 않게 서버가 정책을 결정한다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | 단계별 p50·p95·p99·p99.9 지연 |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

<!-- figure-spec
id: chart-ch05-01
chapter: ch05
role: latency-percentiles
kind: data-chart
generator: python-matplotlib
output: assets/charts/chart-ch05-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 같은 평균을 가져도 p99가 다른 두 latency 분포를 histogram/ECDF로 비교한다.
required_labels_ko:
- 응답 지연(ms)
- 누적 요청 비율
- 분포 A
- 분포 B
prohibited:
- 출처 없는 실측 수치
- 3D chart
- 잘린 축
- 색상만으로 구분
source_refs:
- dean-tail-at-scale
- google-sre-overload
alt_ko: 같은 평균을 가져도 p99가 다른 두 latency 분포를 histogram/ECDF로 비교한다.
caption_ko: 평균과 꼬리 지연 분포
status: specified
spec_file: assets/specs/charts/chart-ch05-01.md
-->

> **시각자료 제작 위치 — 평균과 꼬리 지연 분포**  
> 종류: `data-chart` · 상태: `specified` · 산출 경로: `assets/charts/chart-ch05-01.svg`  
> 제작 명세: `assets/specs/charts/chart-ch05-01.md`  
> 대체 텍스트: 같은 평균을 가져도 p99가 다른 두 latency 분포를 histogram/ECDF로 비교한다.

### 핵심 개념

#### 지연시간

작업 하나가 시작부터 완료까지 걸린 시간이다.

#### 처리량

단위 시간에 완료한 작업 수다.

#### 동시성

같은 시점에 진행 중인 작업 수다.

#### Tail latency

분포의 상위 백분위에서 나타나는 느린 응답이다.

#### 큐잉 지연

자원이 바빠 실제 처리를 시작하기 전 기다리는 시간이다.

#### Fan-out 증폭

하나의 요청이 여러 하위 요청 중 가장 느린 결과를 기다리며 꼬리가 커지는 현상이다.

핵심 개념의 정의와 범위는 [@dean-tail-at-scale; @google-sre-overload; @google-sre-book]를 기준으로 재검토해야 한다.

#### 간단한 fan-out 계산

하위 호출 하나가 목표 지연 안에 끝날 확률이 `0.99`이고, 서로 독립이라고 단순 가정하자. 20개 호출이 모두 목표 안에 끝날 확률은 다음과 같다.

```text
0.99^20 ≈ 0.8179
```

즉 약 18.2%의 상위 요청은 적어도 하나의 느린 하위 호출을 만난다. 실제 호출은 독립이 아닐 수 있고 공유 자원 때문에 함께 느려질 수 있으므로 이 계산은 하한·상한이 아니라 현상을 이해하기 위한 단순 모델이다.

### 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| Ingress | 요청을 받아 admission control과 deadline을 적용한다. |
| 작업 큐 | 대기 작업과 우선순위를 관리한다. |
| Worker pool | 제한된 동시성으로 실제 처리를 수행한다. |
| 하위 의존성 | DB·캐시·외부 API 호출을 제공한다. |
| 분포 집계기 | 구간별 latency histogram과 timeout을 기록한다. |
| 과부하 제어 | 큐 제한, load shedding, degradation을 수행한다. |

<!-- figure-spec
id: fig-ch05-01
chapter: ch05
role: latency-decomposition
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch05-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 전체 지연을 네트워크·큐 대기·처리·하위 호출·직렬화로 분해한다.
required_labels_ko:
- 전체 지연
- 네트워크
- 큐 대기
- 처리
- 하위 호출
- 직렬화
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- dean-tail-at-scale
- google-sre-overload
- google-sre-book
alt_ko: 전체 지연을 네트워크·큐 대기·처리·하위 호출·직렬화로 분해한다.
caption_ko: 전체 지연을 네트워크·큐 대기·처리·하위 호출·직렬화로 분해한다
status: specified
spec_file: assets/specs/svg/fig-ch05-01.md
-->

> **시각자료 제작 위치 — 전체 지연을 네트워크·큐 대기·처리·하위 호출·직렬화로 분해한다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch05-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch05-01.md`  
> 대체 텍스트: 전체 지연을 네트워크·큐 대기·처리·하위 호출·직렬화로 분해한다.

### 요청·데이터 흐름

1. 클라이언트가 전체 deadline을 포함해 요청한다.
2. 입구에서 요청 크기·우선순위·현재 부하를 검사한다.
3. 큐에서 기다린 시간을 별도 기록한다.
4. 남은 deadline을 하위 호출에 분배한다.
5. 병렬 호출 중 필수·선택 결과를 구분한다.
6. 응답 후 전체 및 단계별 지연 분포를 기록한다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

### 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| 대기열 확장 | 짧은 burst를 흡수하고 손실을 줄인다. | 오래된 요청이 쌓여 지연과 메모리가 폭증한다. | burst가 짧고 작업 가치가 유지될 때 |
| 동시성 확대 | 처리량을 늘릴 수 있다. | DB 연결·CPU 경쟁으로 오히려 tail이 악화될 수 있다. | 하위 자원에 여유가 있을 때 |
| 요청 축소/거부 | 핵심 요청의 지연을 보호한다. | 일부 기능 품질이나 성공률을 포기한다. | 포화 상태와 우선순위가 명확할 때 |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@dean-tail-at-scale; @google-sre-overload; @google-sre-book]를 참조한다.

### 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| 큐 폭증 | 도착률이 처리율을 넘으며 대기 시간이 deadline을 초과한다. | 유한 큐, admission control, backpressure를 적용한다. |
| 느린 하위 의존성 | 한 DB shard나 외부 API가 p99를 지배한다. | 단계별 deadline, 격리 pool, fallback을 둔다. |
| 재시도 폭풍 | timeout이 재시도를 만들고 추가 부하가 더 많은 timeout을 만든다. | 재시도 예산, jitter, 멱등성, 서버 힌트를 사용한다. |
| GC·스케줄링 정지 | 짧은 정지가 일부 요청에 긴 꼬리로 나타난다. | 런타임 pause와 CPU throttling을 요청 trace와 상관 분석한다. |
| Coordinated omission | 부하 생성기가 느린 동안 새 요청을 보내지 않아 지연을 낮게 측정한다. | 고정 도착률을 보존하는 부하 모델과 원시 분포를 사용한다. |

<!-- figure-spec
id: fig-ch05-02
chapter: ch05
role: fanout-tail
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch05-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: fan-out 개수가 증가할수록 하나 이상의 느린 하위 호출을 만날 확률이 커지는 모습을 보여준다.
required_labels_ko:
- 요청
- 병렬 호출
- 빠른 응답
- 느린 응답
- 전체 완료
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- dean-tail-at-scale
- google-sre-overload
- google-sre-book
alt_ko: fan-out 개수가 증가할수록 하나 이상의 느린 하위 호출을 만날 확률이 커지는 모습을 보여준다.
caption_ko: fan-out 개수가 증가할수록 하나 이상의 느린 하위 호출을 만날 확률이 커지는 모습을 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch05-02.md
-->

> **시각자료 제작 위치 — fan-out 개수가 증가할수록 하나 이상의 느린 하위 호출을 만날 확률이 커지는 모습을 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch05-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch05-02.md`  
> 대체 텍스트: fan-out 개수가 증가할수록 하나 이상의 느린 하위 호출을 만날 확률이 커지는 모습을 보여준다.

### 확장 전략

- 포화점보다 낮은 목표 사용률을 유지해 burst와 장애 전환 여유를 둔다.
- hot key·large request·slow tenant를 별도 차원으로 분해한다.
- fan-out 단계에서 부분 결과와 quorum 완료 조건을 사용한다.
- hedged request는 취소·중복 비용과 함께 제한적으로 적용한다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

### 보안과 개인정보

- 고객 우선순위가 권한 우회로 악용되지 않게 서버가 정책을 결정한다.
- 지연 로그의 URL·쿼리·trace attribute에서 개인정보를 제거한다.
- load shedding이 특정 사용자군을 지속적으로 차별하지 않는지 분석한다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

### 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- 단계별 p50·p95·p99·p99.9 지연
- 큐 대기 시간과 queue depth
- 동시성·CPU throttling·GC pause
- timeout·취소·재시도·shed 비율
- fan-out 개수별 전체 요청 지연

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

### 비용과 운영 복잡도

- tail을 낮추기 위한 여유 용량은 직접 비용을 만든다.
- hedging과 복제 읽기는 지연을 낮추지만 하위 시스템 부하를 증가시킨다.
- 더 긴 timeout은 실패율을 낮춰 보이지만 자원 점유와 사용자 대기 비용을 키운다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

### 흔한 오해와 안티패턴

- 평균 응답 시간이 좋으니 성능 문제가 없다고 결론낸다.
- 큐 크기를 늘리면 처리량도 늘어난다고 생각한다.
- 클라이언트 timeout보다 긴 서버 작업을 계속 수행한다.
- p99를 샘플 몇 개의 최대값처럼 해석한다.

### 설계 리뷰

- [ ] 사용자 SLO에 대응하는 백분위가 선택됐는가?
- [ ] 큐 대기와 실제 처리 시간이 분리됐는가?
- [ ] fan-out과 재시도가 하위 부하에 미치는 영향이 계산됐는가?
- [ ] 과부하 시 버릴 기능과 보호할 기능이 정해졌는가?
- [ ] 부하 테스트가 coordinated omission을 피하는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

### 연습문제

1. 하위 호출 20개 각각이 99% 확률로 빠를 때 전체 요청이 모두 빠를 확률을 계산하라.
2. 큐가 비어 있을 때와 1초치 작업이 쌓였을 때 같은 timeout 정책의 차이를 설명하라.
3. 검색 결과의 정확도 일부를 포기해 p99를 보호하는 degradation 단계를 설계하라.

### 핵심 요약

- 평균은 tail latency를 설명하지 못한다.
- 포화점 근처에서는 큐잉이 지연을 급격히 키운다.
- fan-out은 작은 하위 꼬리를 전체 꼬리로 증폭한다.
- deadline·유한 큐·부하 제어를 함께 설계한다.
- 성능 측정 자체의 편향도 검증해야 한다.

### 출처

- [@dean-tail-at-scale] Jeffrey Dean and Luiz André Barroso. **The Tail at Scale** (2013). https://research.google/pubs/the-tail-at-scale/
- [@google-sre-overload] Google. **Site Reliability Engineering — Handling Overload** (2016). https://sre.google/sre-book/handling-overload/
- [@google-sre-book] Google. **Site Reliability Engineering** (2016). https://sre.google/sre-book/table-of-contents/

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
