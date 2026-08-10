---
id: ch04
title: SLI·SLO·SLA와 Error Budget
part: design-method
order: 4
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
- ch01
- ch02
learning_objectives:
- 사용자 경험을 나타내는 SLI를 정의한다.
- SLO와 error budget을 계산한다.
- 신뢰성 목표를 배포·투자·장애 대응 결정에 연결한다.
figures:
- chart-ch04-01
- fig-ch04-01
- fig-ch04-02
sources:
- google-sre-slo
- google-sre-error-budget
- google-sre-book
draft_notice: 기술·편집·접근성 검수 전 초고
---

# 04. SLI·SLO·SLA와 Error Budget

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

## 이 장에서 해결할 문제

“항상 안정적”이라는 요구는 설계 입력이 아니다. 사용자 관점의 신호를 SLI로 측정하고, 관측 창과 목표 비율을 SLO로 정하며, 허용 실패량인 error budget을 변경 속도와 신뢰성 투자에 사용해야 한다.

이 절의 기준 출처: [@google-sre-slo; @google-sre-error-budget].

### 학습 목표

- 사용자 경험을 나타내는 SLI를 정의한다.
- SLO와 error budget을 계산한다.
- 신뢰성 목표를 배포·투자·장애 대응 결정에 연결한다.

## 먼저 결론

- SLI는 시스템 내부 CPU보다 사용자가 완료한 결과를 우선한다.
- 분모와 좋은 이벤트의 조건을 명시한다.
- 모든 기능에 같은 SLO를 주지 말고 사용자 여정과 중요도에 따라 분리한다.
- SLA는 외부 약속이고 SLO는 내부 운영 목표이므로 동일시하지 않는다.

::: current-note
**2026-08-06 확인:** 이 장은 변화 가능한 표준·프로젝트·AI 구현을 포함한다. 기본 재검토일은 `2027-02-06`이며, 출판 직전 공식 문서를 다시 확인한다.
:::

## 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | SLI·SLO·SLA와 Error Budget에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | SLI는 시스템 내부 CPU보다 사용자가 완료한 결과를 우선한다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | 서비스 계층을 나눌 때 의존성 SLO가 사용자 여정 SLO에 어떻게 합성되는지 계산한다. |
| 실패·복구 | “계측 공백” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | 분모 소스와 독립적인 합성 검사, missing-data 정책을 둔다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | 보안 차단과 정상 오류를 SLI에서 구분하되 공격 트래픽을 무조건 삭제하지 않는다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | 좋은 이벤트/전체 유효 이벤트 비율 |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

<!-- figure-spec
id: chart-ch04-01
chapter: ch04
role: error-budget-burn
kind: data-chart
generator: python-matplotlib
output: assets/charts/chart-ch04-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 28일 SLO 예산이 정상·느린 소진·빠른 소진 시나리오에서 시간에 따라 감소하는 모습을 보여준다.
required_labels_ko:
- 관측 창 경과 시간
- 남은 Error Budget (%)
- 정상 소진
- 3배 Burn
- 20배 Burn
prohibited:
- 출처 없는 실측 수치
- 3D chart
- 잘린 축
- 색상만으로 구분
source_refs:
- google-sre-slo
- google-sre-error-budget
alt_ko: 28일 SLO 예산이 정상·느린 소진·빠른 소진 시나리오에서 시간에 따라 감소하는 모습을 보여준다.
caption_ko: Error budget과 burn rate
status: specified
spec_file: assets/specs/charts/chart-ch04-01.md
-->

> **시각자료 제작 위치 — Error budget과 burn rate**  
> 종류: `data-chart` · 상태: `specified` · 산출 경로: `assets/charts/chart-ch04-01.svg`  
> 제작 명세: `assets/specs/charts/chart-ch04-01.md`  
> 대체 텍스트: 28일 SLO 예산이 정상·느린 소진·빠른 소진 시나리오에서 시간에 따라 감소하는 모습을 보여준다.


## 핵심 개념

### SLI

좋은 이벤트의 비율이나 지연 분포처럼 서비스 수준을 측정하는 지표다.

### SLO

정해진 관측 창에서 SLI가 달성해야 하는 목표다.

### SLA

서비스 제공자와 고객 사이의 약속이며 위반 시 조치가 포함될 수 있다.

### Error budget

`1 - SLO`에 해당하는 허용 실패량이다.

### Burn rate

error budget이 기준 속도보다 얼마나 빠르게 소진되는지 나타낸다.

### 관측 창

최근 28일 같은 rolling window 또는 달력 월처럼 목표를 평가하는 기간이다.

핵심 개념의 정의와 범위는 [@google-sre-slo; @google-sre-error-budget; @google-sre-book]를 기준으로 재검토해야 한다.

### Error budget 계산

28일 관측 창에서 가용성 SLO가 `99.9%`라면 허용 실패 비율은 `0.1% = 0.001`이다.

```text
28 days × 24 h/day × 60 min/h × 0.001
= 40.32 minutes
```

이 값은 “40분 19.2초 동안 마음대로 장애가 나도 된다”는 뜻이 아니다. 요청 비율 SLI라면 허용 실패 요청 수로 계산해야 하고, 짧은 시간에 예산을 집중 소진하면 사용자의 실제 피해가 더 클 수 있다.

## 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| 이벤트 계측 | 요청·작업·사용자 여정의 성공, 지연, 신선도를 기록한다. |
| SLI 집계 | 좋은 이벤트와 전체 유효 이벤트를 같은 정의로 집계한다. |
| SLO 평가 | 관측 창, 목표, 제외 규칙을 적용한다. |
| Burn-rate 경보 | 빠른 소진과 느린 소진을 서로 다른 창으로 감지한다. |
| 정책 연결 | 배포 중단, 안정화 작업, 용량 투자, 사후 분석을 결정한다. |

<!-- figure-spec
id: fig-ch04-01
chapter: ch04
role: slo-stack
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch04-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 사용자 여정에서 SLI·SLO·SLA·error budget 정책으로 내려가는 관계를 보여준다.
required_labels_ko:
- 사용자 여정
- SLI
- SLO
- SLA
- Error Budget
- 운영 정책
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- google-sre-slo
- google-sre-error-budget
- google-sre-book
alt_ko: 사용자 여정에서 SLI·SLO·SLA·error budget 정책으로 내려가는 관계를 보여준다.
caption_ko: 사용자 여정에서 SLI·SLO·SLA·error budget 정책으로 내려가는 관계를 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch04-01.md
-->

> **시각자료 제작 위치 — 사용자 여정에서 SLI·SLO·SLA·error budget 정책으로 내려가는 관계를 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch04-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch04-01.md`  
> 대체 텍스트: 사용자 여정에서 SLI·SLO·SLA·error budget 정책으로 내려가는 관계를 보여준다.


## 요청·데이터 흐름

1. 사용자가 가치 있는 결과를 얻는 여정을 고른다.
2. 좋은 이벤트와 유효한 전체 이벤트를 정의한다.
3. 계측 누락·봇·의도적 차단 같은 제외 규칙을 명시한다.
4. 달성 가능한 기준선과 사업 기대를 비교해 SLO를 정한다.
5. 빠른/느린 burn-rate 경보를 구성한다.
6. error budget 정책을 배포와 우선순위에 연결한다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

## 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| 요청 기반 SLI | 계산과 설명이 단순하다. | 다단계 비동기 여정의 완료를 놓칠 수 있다. | 동기 API |
| 사용자 여정 SLI | 실제 가치 전달을 잘 반영한다. | 상관관계와 지연된 완료 추적이 어렵다. | 주문·결제·업로드 |
| 창 기반 가용성 | 긴 장애 시간을 직관적으로 보여준다. | 짧은 고빈도 오류의 사용자 영향을 왜곡할 수 있다. | 전통적 인프라 SLA |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@google-sre-slo; @google-sre-error-budget; @google-sre-book]를 참조한다.

## 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| 계측 공백 | 장애 중 telemetry도 사라져 성공처럼 보인다. | 분모 소스와 독립적인 합성 검사, missing-data 정책을 둔다. |
| 잘못된 분모 | 클라이언트 취소나 차단 요청을 임의로 제외해 목표가 부풀려진다. | 제외 규칙을 코드·문서·리뷰로 관리한다. |
| SLO 과다 | 세부 엔드포인트마다 SLO를 만들어 운영자가 신호를 해석하지 못한다. | 핵심 사용자 여정과 대표 서비스 지표로 제한한다. |
| 예산 무시 | error budget을 초과해도 배포 속도가 바뀌지 않는다. | 사전에 합의한 정책으로 안정화와 출시 결정을 연결한다. |

<!-- figure-spec
id: fig-ch04-02
chapter: ch04
role: burn-rate-windows
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch04-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 짧은 창과 긴 창의 burn rate가 빠른 장애와 느린 열화를 포착하는 방식을 보여준다.
required_labels_ko:
- 5분
- 1시간
- 6시간
- 28일 창
- 빠른 소진
- 느린 소진
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- google-sre-slo
- google-sre-error-budget
- google-sre-book
alt_ko: 짧은 창과 긴 창의 burn rate가 빠른 장애와 느린 열화를 포착하는 방식을 보여준다.
caption_ko: 짧은 창과 긴 창의 burn rate가 빠른 장애와 느린 열화를 포착하는 방식을 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch04-02.md
-->

> **시각자료 제작 위치 — 짧은 창과 긴 창의 burn rate가 빠른 장애와 느린 열화를 포착하는 방식을 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch04-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch04-02.md`  
> 대체 텍스트: 짧은 창과 긴 창의 burn rate가 빠른 장애와 느린 열화를 포착하는 방식을 보여준다.


## 확장 전략

- 서비스 계층을 나눌 때 의존성 SLO가 사용자 여정 SLO에 어떻게 합성되는지 계산한다.
- 고객군·지역·기능별로 분리하되 전체 집계가 심각한 하위 집단을 숨기지 않게 한다.
- 트래픽이 적은 서비스는 이벤트 비율만으로 경보하지 않고 합성 검사와 시간 기반 조건을 함께 쓴다.
- 새 기능은 초기 기준선 관측 후 SLO를 조정하되 목표를 사후에 낮춰 실패를 숨기지 않는다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

## 보안과 개인정보

- 보안 차단과 정상 오류를 SLI에서 구분하되 공격 트래픽을 무조건 삭제하지 않는다.
- 고객별 SLI를 만들 때 개인 식별 가능성을 줄이고 보존 기간을 제한한다.
- SLA 문구와 실제 계측 정의가 모순되지 않도록 법무·제품·운영이 공동 검토한다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

## 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- 좋은 이벤트/전체 유효 이벤트 비율
- 지연 임계값별 성공률
- 28일·1시간·5분 burn rate
- 계측 누락률과 합성 검사 성공률

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

## 비용과 운영 복잡도

- SLO가 높아질수록 중복 인프라·운영 인력·변경 통제 비용이 비선형적으로 증가할 수 있다.
- 낮은 중요도의 기능을 핵심 경로와 분리하면 전체 신뢰성 비용을 줄일 수 있다.
- error budget은 장애 비용과 출시 지연 비용을 같은 언어로 논의하게 한다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

## 흔한 오해와 안티패턴

- 모든 서비스에 99.99%를 복사한다.
- 서버 가동률을 사용자 성공률로 간주한다.
- 평균 지연만 SLI로 사용한다.
- SLO 위반을 평가와 처벌 도구로 사용해 계측 왜곡을 유도한다.

## 설계 리뷰

- [ ] SLI가 사용자 가치와 직접 연결되는가?
- [ ] 좋은 이벤트와 분모·제외 규칙이 명확한가?
- [ ] 관측 창과 목표 선택 근거가 있는가?
- [ ] 빠른 장애와 느린 품질 저하를 모두 감지하는가?
- [ ] error budget 초과 시 실제 행동 정책이 있는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

## 연습문제

1. 99.9% SLO의 30일 error budget을 분과 초로 계산하라.
2. 주문 생성은 성공했지만 배송 지시가 10분 지연되는 시스템의 여정 SLI를 정의하라.
3. 1시간 동안 20배 burn rate와 6시간 동안 3배 burn rate를 어떻게 다르게 대응할지 정책을 작성하라.

## 핵심 요약

- SLI는 사용자 관점의 측정값이다.
- SLO는 목표와 관측 창을 함께 정의한다.
- SLA는 외부 약속이며 SLO와 목적이 다르다.
- error budget은 허용 실패를 변경 정책에 연결한다.
- 계측 공백과 잘못된 분모도 신뢰성 위험이다.

## 출처

- [@google-sre-slo] Google. **SRE Workbook — Implementing SLOs** (2018). https://sre.google/workbook/implementing-slos/
- [@google-sre-error-budget] Google. **SRE Workbook — Error Budget Policy** (2018). https://sre.google/workbook/error-budget-policy/
- [@google-sre-book] Google. **Site Reliability Engineering** (2016). https://sre.google/sre-book/table-of-contents/

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
