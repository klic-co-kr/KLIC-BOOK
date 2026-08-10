---
id: ch06
title: 가용성·신뢰성·내구성과 장애 도메인
part: distributed-foundations
order: 6
status: draft
freshness: durable
last_verified: '2026-08-06'
review_due: '2028-08-06'
upstream_lineage:
- source: system-design-primer
  file: README.md
  anchor: availability-in-nines
  action: REWRITE
audiences:
- backend-engineer
- platform-engineer
prerequisites:
- ch04
- ch05
learning_objectives:
- 가용성·신뢰성·내구성을 구분한다.
- 장애 도메인과 공통 원인 실패를 식별한다.
- 중복 구성의 실제 독립성과 복구 능력을 검증한다.
figures:
- chart-ch06-01
- fig-ch06-01
- fig-ch06-02
sources:
- google-sre-book
- nist-contingency
draft_notice: 기술·편집·접근성 검수 전 초고
---

# 06. 가용성·신뢰성·내구성과 장애 도메인

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

## 이 장에서 해결할 문제

서버를 두 대 배치했다고 고가용성이 되는 것은 아니다. 두 복제본이 같은 전원, 제어면, 자격증명, 배포 파이프라인, 데이터 손상 경로를 공유하면 하나의 장애가 동시에 둘을 무너뜨릴 수 있다.

이 절의 기준 출처: [@google-sre-book; @nist-contingency].

### 학습 목표

- 가용성·신뢰성·내구성을 구분한다.
- 장애 도메인과 공통 원인 실패를 식별한다.
- 중복 구성의 실제 독립성과 복구 능력을 검증한다.

## 먼저 결론

- 가용성은 요청 시 서비스가 유용한 결과를 제공하는 비율이다.
- 신뢰성은 일정 기간 올바르게 동작할 가능성과 실패 특성을 포함한다.
- 내구성은 이미 승인된 데이터가 장기간 보존될 가능성이다.
- 중복은 독립된 장애 도메인과 검증된 failover가 있을 때만 효과가 있다.

## 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | 가용성·신뢰성·내구성과 장애 도메인에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | 가용성은 요청 시 서비스가 유용한 결과를 제공하는 비율이다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | 장애 도메인별로 최소 필요 복제본과 quorum을 계산한다. |
| 실패·복구 | “영역 장애” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | 복제본과 quorum을 독립 zone에 배치한다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | 비상 계정과 복구 키는 평상시 계정과 독립적으로 보호하고 사용을 감사한다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | 사용자 여정 가용성과 오류 예산 |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

<!-- figure-spec
id: chart-ch06-01
chapter: ch06
role: availability-composition
kind: data-chart
generator: python-matplotlib
output: assets/charts/chart-ch06-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 독립 가정을 전제로 구성 요소 가용성이 직렬·병렬 연결에서 어떻게 합성되는지 비교한다.
required_labels_ko:
- 구성
- 계산된 가용성(%)
- 직렬 2개
- 병렬 2개
- 병렬 3개
prohibited:
- 출처 없는 실측 수치
- 3D chart
- 잘린 축
- 색상만으로 구분
source_refs:
- google-sre-book
- nist-contingency
alt_ko: 독립 가정을 전제로 구성 요소 가용성이 직렬·병렬 연결에서 어떻게 합성되는지 비교한다.
caption_ko: 직렬·병렬 구성의 단순 가용성
status: specified
spec_file: assets/specs/charts/chart-ch06-01.md
-->

> **시각자료 제작 위치 — 직렬·병렬 구성의 단순 가용성**  
> 종류: `data-chart` · 상태: `specified` · 산출 경로: `assets/charts/chart-ch06-01.svg`  
> 제작 명세: `assets/specs/charts/chart-ch06-01.md`  
> 대체 텍스트: 독립 가정을 전제로 구성 요소 가용성이 직렬·병렬 연결에서 어떻게 합성되는지 비교한다.

## 핵심 개념

### 가용성

필요한 시점에 서비스를 사용할 수 있는 정도다.

### 신뢰성

요구된 조건에서 올바르게 동작하는 성질이다.

### 내구성

기록된 데이터가 손실되지 않고 보존되는 성질이다.

### 장애 도메인

한 원인으로 함께 실패할 수 있는 자원의 묶음이다.

### 공통 원인 실패

중복된 구성 요소가 공유 의존성이나 같은 결함으로 동시에 실패하는 현상이다.

### MTTR

장애 후 정상 서비스로 복구하는 데 걸리는 평균 시간이며 분포와 단계별 시간도 함께 봐야 한다.

핵심 개념의 정의와 범위는 [@google-sre-book; @nist-contingency]를 기준으로 재검토해야 한다.

## 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| 서비스 복제본 | 요청 처리를 여러 인스턴스로 분산한다. |
| 상태 저장 계층 | 데이터 복제와 복구 가능한 원장을 제공한다. |
| 트래픽 전환기 | 건강 상태와 정책에 따라 우회한다. |
| 제어면 | 배포·구성·인증·DNS를 관리한다. |
| 백업 저장소 | 운영 복제와 독립된 복구 지점을 보존한다. |
| 복구 오케스트레이션 | failover, restore, 검증, failback 절차를 자동화한다. |

<!-- figure-spec
id: fig-ch06-01
chapter: ch06
role: failure-domain-map
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch06-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 인스턴스·zone·리전·제어면·자격증명·배포 경로의 공유 장애 도메인을 보여준다.
required_labels_ko:
- 인스턴스
- Zone
- 리전
- 제어면
- KMS
- 배포 파이프라인
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- google-sre-book
- nist-contingency
alt_ko: 인스턴스·zone·리전·제어면·자격증명·배포 경로의 공유 장애 도메인을 보여준다.
caption_ko: 인스턴스·zone·리전·제어면·자격증명·배포 경로의 공유 장애 도메인을 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch06-01.md
-->

> **시각자료 제작 위치 — 인스턴스·zone·리전·제어면·자격증명·배포 경로의 공유 장애 도메인을 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch06-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch06-01.md`  
> 대체 텍스트: 인스턴스·zone·리전·제어면·자격증명·배포 경로의 공유 장애 도메인을 보여준다.

## 요청·데이터 흐름

1. 각 사용자 여정의 의존성 그래프를 그린다.
2. 노드마다 공유 장애 도메인을 태깅한다.
3. 단일 장애가 여정에 미치는 영향을 평가한다.
4. failover가 필요한 상태와 데이터 손실 범위를 정한다.
5. 백업 복구로만 해결되는 손상 시나리오를 분리한다.
6. 게임데이에서 탐지·의사결정·복구 시간을 측정한다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

## 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| Active/Standby | 상태와 쓰기 경로가 단순하고 충돌이 적다. | 대기 자원 비용과 승격 시간이 필요하다. | 강한 쓰기 소유권이 필요한 시스템 |
| Active/Active | 지역별 지연과 일부 장애 격리가 좋다. | 충돌·순서·데이터 정책이 복잡하다. | 독립 분할 가능한 워크로드 |
| 복구 중심 단일 운영 | 평상시 비용이 낮다. | RTO 동안 서비스를 제공하지 못한다. | 낮은 중요도 또는 긴 RTO 허용 |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@google-sre-book; @nist-contingency]를 참조한다.

## 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| 영역 장애 | 같은 zone의 앱·DB·캐시가 동시에 중단된다. | 복제본과 quorum을 독립 zone에 배치한다. |
| 잘못된 배포 | 모든 복제본에 같은 결함이 동시에 배포된다. | 점진 배포, 이전 버전 유지, 자동 rollback을 사용한다. |
| 자격증명 만료 | 여러 리전에 복제했지만 공통 인증서·KMS가 실패한다. | 만료 감시, 다중 경로, 비상 접근 절차를 검증한다. |
| 논리적 데이터 손상 | 복제가 삭제·오염을 빠르게 전파한다. | 불변 백업, point-in-time recovery, 복구 리허설을 둔다. |
| 제어면 장애 | 데이터면은 살아 있지만 설정 변경이나 신규 배포가 불가능하다. | 데이터면의 마지막 정상 설정 유지와 수동 절차를 설계한다. |

<!-- figure-spec
id: fig-ch06-02
chapter: ch06
role: redundancy-vs-recovery
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch06-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 복제·failover·백업·restore가 서로 다른 실패를 담당하는 관계를 보여준다.
required_labels_ko:
- 복제
- Failover
- 백업
- Restore
- 논리 손상
- 물리 장애
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- google-sre-book
- nist-contingency
alt_ko: 복제·failover·백업·restore가 서로 다른 실패를 담당하는 관계를 보여준다.
caption_ko: 복제·failover·백업·restore가 서로 다른 실패를 담당하는 관계를 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch06-02.md
-->

> **시각자료 제작 위치 — 복제·failover·백업·restore가 서로 다른 실패를 담당하는 관계를 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch06-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch06-02.md`  
> 대체 텍스트: 복제·failover·백업·restore가 서로 다른 실패를 담당하는 관계를 보여준다.

## 확장 전략

- 장애 도메인별로 최소 필요 복제본과 quorum을 계산한다.
- 읽기 전용·기능 축소 모드를 통해 전체 중단 대신 제한된 서비스를 제공한다.
- 복구 작업도 정상 트래픽과 자원을 경쟁하므로 복구 처리량을 용량 계획에 포함한다.
- failover 후 원래 위치로 돌아가는 failback과 데이터 재동기화까지 설계한다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

## 보안과 개인정보

- 비상 계정과 복구 키는 평상시 계정과 독립적으로 보호하고 사용을 감사한다.
- 백업에는 운영 데이터와 같은 암호화·보존·삭제 정책을 적용한다.
- 장애 대응 중 보안 통제를 무조건 해제하지 않고 제한된 break-glass 절차를 사용한다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

## 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- 사용자 여정 가용성과 오류 예산
- 장애 도메인별 건강·용량·복제 지연
- 탐지·승인·전환·복구·검증 단계 시간
- 백업 성공률보다 실제 restore 성공률
- 공통 의존성 오류와 제어면 가용성

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

## 비용과 운영 복잡도

- 독립 리전·zone·계정은 비용을 늘리지만 공통 원인 위험을 낮춘다.
- 대기 자원은 보험 비용이며 RTO·SLO와 연결해 정한다.
- 복구 자동화와 리허설 비용을 빼면 중복 인프라가 있어도 복구 가능성을 증명할 수 없다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

## 흔한 오해와 안티패턴

- 복제본 수를 가용성과 동일시한다.
- 같은 배포·DNS·KMS를 공유하면서 다중 리전이라고 안심한다.
- 백업 성공 로그만 보고 restore를 시험하지 않는다.
- failover만 설계하고 failback과 재동기화를 생략한다.

## 설계 리뷰

- [ ] 각 중복 구성의 실제 장애 도메인이 다른가?
- [ ] 제어면과 데이터면 실패가 분리돼 있는가?
- [ ] 논리 손상과 물리 손상의 복구 경로가 다른가?
- [ ] RTO·RPO가 기술 구성과 리허설 결과로 입증되는가?
- [ ] 복구 중 보안·감사 통제가 유지되는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

## 연습문제

1. 앱 3대와 DB 3대가 모두 같은 zone에 있을 때 어떤 실패를 견디지 못하는지 나열하라.
2. 99.9% 구성요소 두 개가 직렬·병렬로 연결될 때 단순 독립 가정의 가용성을 계산하라.
3. 잘못된 스키마 마이그레이션이 두 리전에 전파된 상황의 복구 절차를 설계하라.

## 핵심 요약

- 가용성·신뢰성·내구성은 서로 다른 목표다.
- 중복보다 장애 도메인의 독립성이 중요하다.
- 복제는 논리 손상으로부터 보호하지 못한다.
- failover·restore·failback을 모두 검증한다.
- 복구 능력은 리허설 증거로 판단한다.

## 출처

- [@google-sre-book] Google. **Site Reliability Engineering** (2016). https://sre.google/sre-book/table-of-contents/
- [@nist-contingency] NIST. **NIST SP 800-34 Rev. 1 — Contingency Planning Guide for Federal Information Systems** (2010). https://csrc.nist.gov/pubs/sp/800/34/r1/final

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
