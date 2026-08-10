---
id: ch30
title: Container·Kubernetes·Serverless·IaC·GitOps·FinOps
part: production
order: 30
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
- ch03
- ch17
- ch27
- ch28
learning_objectives:
- workload 실행 모델을 운영 요구로 선택한다.
- 선언적 인프라·GitOps·platform 경계를 설계한다.
- 비용을 기술 지표와 사업 가치에 연결한다.
figures:
- fig-ch30-01
- fig-ch30-02
sources:
- kubernetes-concepts
- opengitops
- finops-framework
- cncf-platforms
- slsa12
draft_notice: 기술·편집·접근성 검수 전 초고
---

# 30. Container·Kubernetes·Serverless·IaC·GitOps·FinOps

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

## 이 장에서 해결할 문제

클라우드 네이티브는 도구 목록이 아니라 선언된 상태, 자동 복구, immutable artifact, 표준 운영 경로, 측정 가능한 비용을 결합하는 운영 모델이다. Kubernetes나 serverless를 채택해도 애플리케이션 상태·SLO·보안·비용 책임은 사라지지 않는다.

이 절의 기준 출처: [@kubernetes-concepts; @opengitops].

### 학습 목표

- workload 실행 모델을 운영 요구로 선택한다.
- 선언적 인프라·GitOps·platform 경계를 설계한다.
- 비용을 기술 지표와 사업 가치에 연결한다.

## 먼저 결론

- container는 packaging 경계이고 Kubernetes는 workload orchestration platform이다.
- serverless는 인프라 관리 일부를 공급자에 맡기지만 실행 제한·cold start·event semantics를 검토한다.
- IaC와 GitOps는 desired state와 변경 이력을 코드로 관리하되 secret와 runtime emergency를 별도 설계한다.
- FinOps는 cost allocation만이 아니라 기술 사용과 사업 가치를 함께 최적화하는 협업 체계다.

::: current-note
**2026-08-06 확인:** 이 장은 변화 가능한 표준·프로젝트·AI 구현을 포함한다. 기본 재검토일은 `2027-02-06`이며, 출판 직전 공식 문서를 다시 확인한다.
:::

## 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | Container·Kubernetes·Serverless·IaC·GitOps·FinOps에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | container는 packaging 경계이고 Kubernetes는 workload orchestration platform이다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | cluster 수와 tenant 격리는 security·blast radius·운영 overhead를 함께 평가한다. |
| 실패·복구 | “Config drift” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | reconciliation·drift detection·break-glass 기록을 둔다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | base image·dependency·artifact provenance를 검증한다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | deployment lead time·change failure·rollback |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

## 핵심 개념

### Container image

애플리케이션과 runtime dependency를 immutable artifact로 묶는다.

### Kubernetes control loop

desired state와 actual state 차이를 반복 조정한다.

### Serverless

요청·event에 따라 공급자가 실행 환경과 scale을 관리하는 모델이다.

### IaC

인프라 resource와 policy를 선언형 코드·state로 관리한다.

### GitOps

version-controlled desired state와 자동 reconciliation을 운영 원칙으로 사용한다.

### Platform engineering

개발자가 안전한 표준 경로로 build·deploy·observe할 수 있는 내부 제품을 만든다.

### FinOps

engineering·finance·business가 기술 사용과 비용·가치를 함께 관리하는 운영 방식이다.

### Unit economics

요청·고객·transaction·token 같은 단위당 비용과 가치다.

핵심 개념의 정의와 범위는 [@kubernetes-concepts; @opengitops; @finops-framework; @cncf-platforms; @slsa12]를 기준으로 재검토해야 한다.

## 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| Source/build | 재현 가능한 artifact와 provenance를 만든다. |
| Artifact registry | 서명된 image·package를 보존한다. |
| IaC control | network·cluster·database·policy desired state를 관리한다. |
| GitOps reconciler | 환경 repo 상태를 runtime에 적용한다. |
| Kubernetes/serverless runtime | workload scheduling·scale·health를 수행한다. |
| Internal platform | template·policy·observability·self-service를 제공한다. |
| Cost pipeline | resource usage를 owner·service·unit metric에 연결한다. |
| Governance | quota·policy·exception·lifecycle을 관리한다. |

<!-- figure-spec
id: fig-ch30-01
chapter: ch30
role: cloud-native-delivery
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch30-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: source·build·registry·IaC/GitOps·runtime·telemetry·cost feedback의 폐쇄 루프를 보여준다.
required_labels_ko:
- Source
- Build
- Registry
- IaC
- GitOps
- Runtime
- Telemetry
- Cost Feedback
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- kubernetes-concepts
- opengitops
- finops-framework
alt_ko: source·build·registry·IaC/GitOps·runtime·telemetry·cost feedback의 폐쇄 루프를 보여준다.
caption_ko: source·build·registry·IaC/GitOps·runtime·telemetry·cost feedback의 폐쇄 루프를 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch30-01.md
-->

> **시각자료 제작 위치 — source·build·registry·IaC/GitOps·runtime·telemetry·cost feedback의 폐쇄 루프를 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch30-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch30-01.md`  
> 대체 텍스트: source·build·registry·IaC/GitOps·runtime·telemetry·cost feedback의 폐쇄 루프를 보여준다.


## 요청·데이터 흐름

1. source change가 test와 reproducible build를 통과한다.
2. artifact가 서명·provenance와 함께 registry에 저장된다.
3. 환경 변경이 IaC/Git pull request로 검토된다.
4. reconciler가 canary·policy를 거쳐 desired state를 적용한다.
5. runtime이 health·autoscaling·restart를 수행한다.
6. telemetry와 cost allocation이 service·team·unit에 연결된다.
7. platform 팀이 adoption·lead time·reliability·cost 결과를 제품 지표로 본다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

## 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| VM/managed runtime | 격리와 기존 운영 도구가 익숙하다. | scale·patch·packing 효율이 제한될 수 있다. | stateful·legacy·특수 OS |
| Kubernetes | 다양한 workload와 확장 가능한 platform API를 제공한다. | cluster·network·policy·upgrade 복잡도가 크다. | 다팀·다서비스 platform |
| Serverless | 운영 부담과 scale-to-zero가 좋다. | 실행 제한·lock-in·관측·비용 예측이 필요하다. | event-driven·간헐 workload |
| Managed PaaS | 운영 단순성과 표준 배포를 제공한다. | customization과 탈출 경로가 제한될 수 있다. | 일반 web/API |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@kubernetes-concepts; @opengitops; @finops-framework]를 참조한다.

## 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| Config drift | console 긴급 변경이 IaC/Git desired state와 달라진다. | reconciliation·drift detection·break-glass 기록을 둔다. |
| Autoscaling lag | traffic burst가 pod/function 준비보다 빨라 queue와 timeout이 증가한다. | pre-warm, queue, predictive floor, admission을 사용한다. |
| Control-plane blast | 잘못된 policy/template이 모든 workload 배포를 막는다. | canary scope, policy audit mode, rollback, last-known state를 둔다. |
| Cost runaway | high-cardinality log·egress·idle cluster·unbounded function이 비용을 폭증시킨다. | budget alert, quota, unit cost, anomaly detection을 사용한다. |
| Platform bypass | golden path가 느려 팀이 unmanaged resource를 만든다. | 개발자 경험·escape hatch·feedback으로 platform을 제품처럼 개선한다. |

<!-- figure-spec
id: fig-ch30-02
chapter: ch30
role: runtime-decision
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch30-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: VM·Kubernetes·serverless·managed PaaS를 제어 수준·운영 부담·scale 특성으로 비교한다.
required_labels_ko:
- VM
- Kubernetes
- Serverless
- Managed PaaS
- 제어 수준
- 운영 부담
- Scale
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- kubernetes-concepts
- opengitops
- finops-framework
alt_ko: VM·Kubernetes·serverless·managed PaaS를 제어 수준·운영 부담·scale 특성으로 비교한다.
caption_ko: VM·Kubernetes·serverless·managed PaaS를 제어 수준·운영 부담·scale 특성으로 비교한다
status: specified
spec_file: assets/specs/svg/fig-ch30-02.md
-->

> **시각자료 제작 위치 — VM·Kubernetes·serverless·managed PaaS를 제어 수준·운영 부담·scale 특성으로 비교한다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch30-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch30-02.md`  
> 대체 텍스트: VM·Kubernetes·serverless·managed PaaS를 제어 수준·운영 부담·scale 특성으로 비교한다.


## 확장 전략

- cluster 수와 tenant 격리는 security·blast radius·운영 overhead를 함께 평가한다.
- workload requests/limits와 autoscaling metric을 실제 profile로 조정한다.
- serverless는 concurrency·event source·downstream capacity limit를 함께 설정한다.
- platform API는 공통 80%를 표준화하고 특수 20%는 승인된 extension으로 지원한다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

## 보안과 개인정보

- base image·dependency·artifact provenance를 검증한다.
- cluster/service account·namespace·network policy·secret 권한을 최소화한다.
- IaC state와 plan output에 secret가 노출되지 않게 한다.
- GitOps repo write 권한과 runtime deploy 권한을 분리한다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

## 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- deployment lead time·change failure·rollback
- pod/function cold start·scale lag·throttle
- reconciliation drift·failed apply·policy deny
- platform adoption·golden path completion
- service/team/unit cost·idle·egress·anomaly
- resource request 대비 실제 사용률

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

## 비용과 운영 복잡도

- Kubernetes는 고정 control plane·노드·운영 인력 비용이 있어 작은 workload에 과할 수 있다.
- serverless는 낮은 유휴 비용과 높은 단위 실행 비용 사이의 선택이다.
- FinOps는 단순 절감보다 unit economics·SLO·속도를 함께 본다.
- platform 투자는 서비스마다 반복되는 toil과 사고를 얼마나 줄이는지로 평가한다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

## 흔한 오해와 안티패턴

- container를 쓰면 cloud native라고 생각한다.
- Kubernetes를 조직 문제 해결 도구로 먼저 도입한다.
- Git이 source of truth면 runtime 긴급 변경과 secret가 자동으로 안전하다고 믿는다.
- 비용을 월 합계만 보고 서비스 단위와 사용자 가치에 연결하지 않는다.

## 설계 리뷰

- [ ] workload 요구에 맞는 가장 단순한 runtime을 선택했는가?
- [ ] desired state·artifact·policy·secret 소유권이 분리됐는가?
- [ ] autoscaling이 downstream capacity와 함께 검증됐는가?
- [ ] platform 성공을 개발자·신뢰성·비용 지표로 측정하는가?
- [ ] unit cost와 SLO를 같은 의사결정에 사용하는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

## 연습문제

1. 간헐적 이미지 처리 작업을 VM, Kubernetes Job, serverless로 비교하라.
2. GitOps 긴급 변경 후 desired state와 reconciliate하는 break-glass 절차를 설계하라.
3. API 요청당 비용을 compute·DB·cache·egress·observability로 분해하라.

## 핵심 요약

- 클라우드 네이티브는 선언·자동화·복구·관측의 운영 모델이다.
- runtime 선택은 workload와 팀 역량에 맞춘다.
- IaC와 GitOps에도 drift·secret·긴급 변경 정책이 필요하다.
- platform은 개발자를 위한 내부 제품이다.
- FinOps는 비용을 기술 사용과 사업 가치에 연결한다.

## 출처

- [@kubernetes-concepts] Kubernetes Authors. **Kubernetes Concepts** (2026). https://kubernetes.io/docs/concepts/
- [@opengitops] OpenGitOps. **OpenGitOps Principles** (2026). https://opengitops.dev/
- [@finops-framework] FinOps Foundation. **FinOps Framework** (2026). https://www.finops.org/framework/
- [@cncf-platforms] Cloud Native Computing Foundation. **Platforms White Paper** (2025). https://tag-app-delivery.cncf.io/whitepapers/platforms/
- [@slsa12] OpenSSF. **SLSA Specification v1.2** (2025). https://slsa.dev/spec/v1.2/

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
