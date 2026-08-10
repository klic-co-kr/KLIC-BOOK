---
id: ch17
title: 모듈러 모놀리스·마이크로서비스·Service Mesh
part: network-runtime
order: 17
status: draft
freshness: current
last_verified: '2026-08-06'
review_due: '2027-02-06'
upstream_lineage:
- source: system-design-primer
  file: README.md
  anchor: microservices
  action: REPLACE
audiences:
- backend-engineer
- platform-engineer
prerequisites:
- ch01
- ch14
- ch16
learning_objectives:
- 배포 단위와 모듈 경계를 구분한다.
- 서비스 분리의 비용과 조건을 평가한다.
- service mesh가 해결하는 통신 문제와 해결하지 않는 도메인 문제를 설명한다.
figures:
- fig-ch17-01
- fig-ch17-02
sources:
- kubernetes-concepts
- istio-architecture
- iso-42010
draft_notice: 기술·편집·접근성 검수 전 초고
---

# 17. 모듈러 모놀리스·마이크로서비스·Service Mesh

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

## 이 장에서 해결할 문제

모놀리스와 마이크로서비스는 성숙도 순서가 아니다. 한 프로세스에서도 모듈·데이터 소유권을 엄격히 나눌 수 있고, 여러 서비스여도 같은 DB와 배포를 공유하면 독립성이 없다. 분리는 변경·확장·소유권의 실제 압력이 있을 때 수행한다.

이 절의 기준 출처: [@kubernetes-concepts; @istio-architecture].

### 학습 목표

- 배포 단위와 모듈 경계를 구분한다.
- 서비스 분리의 비용과 조건을 평가한다.
- service mesh가 해결하는 통신 문제와 해결하지 않는 도메인 문제를 설명한다.

## 먼저 결론

- 먼저 모듈 경계와 의존 방향을 만들고 배포 분리는 나중에 선택한다.
- 서비스마다 데이터 쓰기 소유권과 운영 책임이 있어야 한다.
- 분산 호출은 부분 실패·지연·버전·관측 비용을 추가한다.
- service mesh는 mTLS·traffic policy·telemetry를 지원하지만 데이터 소유권과 업무 saga를 설계해주지 않는다.

::: current-note
**2026-08-06 확인:** 이 장은 변화 가능한 표준·프로젝트·AI 구현을 포함한다. 기본 재검토일은 `2027-02-06`이며, 출판 직전 공식 문서를 다시 확인한다.
:::

## 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | 모듈러 모놀리스·마이크로서비스·Service Mesh에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | 먼저 모듈 경계와 의존 방향을 만들고 배포 분리는 나중에 선택한다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | scale profile이 다른 모듈만 독립적으로 분리한다. |
| 실패·복구 | “Chatty calls” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | API coarse-graining, local composition, 비동기 이벤트를 사용한다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | 서비스 identity와 사용자 identity를 구분해 전달한다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | 서비스별 SLO·call graph·dependency latency |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

## 핵심 개념

### 모듈러 모놀리스

하나의 배포 단위 안에서 명시적 모듈 경계와 의존 규칙을 유지하는 구조다.

### 마이크로서비스

독립 배포·소유·데이터 경계를 가진 작은 서비스 집합이다.

### 분산 모놀리스

서비스 수는 많지만 데이터·배포·변경이 강하게 결합된 구조다.

### Bounded context

용어와 모델이 일관된 업무 경계다.

### Service mesh

서비스 간 통신의 proxy와 control plane을 통해 보안·정책·관측을 제공하는 인프라 계층이다.

### Strangler migration

기존 시스템 주변에서 기능을 단계적으로 새 경계로 옮기는 방식이다.

핵심 개념의 정의와 범위는 [@kubernetes-concepts; @istio-architecture; @iso-42010]를 기준으로 재검토해야 한다.

## 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| 도메인 모듈 | 업무 규칙과 자체 데이터 접근을 소유한다. |
| 내부 인터페이스 | 모듈 간 허용된 호출과 이벤트를 정의한다. |
| 서비스 API | 배포 분리 후 네트워크 계약이 된다. |
| Event channel | 비동기 통합과 느슨한 결합을 지원한다. |
| Sidecar/ambient data plane | 서비스 간 mTLS·routing·telemetry를 수행한다. |
| Mesh control plane | identity·policy·route 설정을 배포한다. |
| Platform layer | 배포·관측·secret·template을 표준화한다. |

<!-- figure-spec
id: fig-ch17-01
chapter: ch17
role: architecture-evolution
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch17-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 모놀리스→모듈러 모놀리스→선택적 서비스 분리의 단계와 되돌림 지점을 보여준다.
required_labels_ko:
- 모놀리스
- 모듈 경계
- 데이터 소유권
- 서비스 분리
- 독립 배포
- 되돌림
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- kubernetes-concepts
- istio-architecture
- iso-42010
alt_ko: 모놀리스→모듈러 모놀리스→선택적 서비스 분리의 단계와 되돌림 지점을 보여준다.
caption_ko: 모놀리스→모듈러 모놀리스→선택적 서비스 분리의 단계와 되돌림 지점을 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch17-01.md
-->

> **시각자료 제작 위치 — 모놀리스→모듈러 모놀리스→선택적 서비스 분리의 단계와 되돌림 지점을 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch17-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch17-01.md`  
> 대체 텍스트: 모놀리스→모듈러 모놀리스→선택적 서비스 분리의 단계와 되돌림 지점을 보여준다.


## 요청·데이터 흐름

1. 변경 이유와 데이터 소유권으로 모듈을 정의한다.
2. 모듈 내부 DB table 접근을 외부에서 금지한다.
3. 호출 graph와 transaction boundary를 측정한다.
4. 독립 확장·배포·보안 요구가 큰 모듈을 분리 후보로 정한다.
5. API/event 계약과 데이터 migration을 단계적으로 적용한다.
6. mesh는 반복 통신 정책이 충분히 많을 때 도입한다.
7. 분리 후 지연·오류·운영 비용이 목표를 만족하는지 검증한다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

## 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| 모듈러 모놀리스 | 로컬 transaction·디버깅·배포가 단순하다. | 강제 장치가 없으면 경계가 무너질 수 있다. | 초기·중간 규모, 복잡한 도메인 |
| 마이크로서비스 | 독립 배포·확장·팀 소유가 가능하다. | 네트워크·데이터·관측·플랫폼 비용이 크다. | 독립 변화 압력이 검증된 경계 |
| Service mesh | 일관된 mTLS·traffic policy·telemetry를 제공한다. | control/data plane 복잡도와 리소스 비용이 있다. | 많은 서비스의 공통 통신 정책 |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@kubernetes-concepts; @istio-architecture; @iso-42010]를 참조한다.

## 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| Chatty calls | 로컬 함수였던 호출이 수십 개 동기 RPC가 되어 tail이 악화된다. | API coarse-graining, local composition, 비동기 이벤트를 사용한다. |
| 공유 DB | 여러 서비스가 같은 table을 수정해 배포 독립성이 사라진다. | 쓰기 소유자를 정하고 API/CDC로 읽기 모델을 제공한다. |
| Mesh outage | control plane 설정 오류나 인증서 문제로 광범위 통신 장애가 난다. | last-known config, canary, fail-safe 정책, 범위 축소를 둔다. |
| Version lockstep | 서비스가 함께 배포돼야만 호환된다. | additive contract, consumer-driven test, expand-contract migration을 사용한다. |
| 조직 경계 불일치 | 한 팀이 수십 서비스를 맡아 on-call과 변경 속도가 악화된다. | 서비스 수를 팀 인지 부하와 운영 능력에 맞춘다. |

<!-- figure-spec
id: fig-ch17-02
chapter: ch17
role: service-mesh-scope
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch17-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 애플리케이션·data plane·control plane·platform의 책임과 mesh가 다루지 않는 업무 트랜잭션을 보여준다.
required_labels_ko:
- 애플리케이션
- Sidecar/Data Plane
- Control Plane
- Platform
- mTLS
- 업무 트랜잭션
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- kubernetes-concepts
- istio-architecture
- iso-42010
alt_ko: 애플리케이션·data plane·control plane·platform의 책임과 mesh가 다루지 않는 업무 트랜잭션을 보여준다.
caption_ko: 애플리케이션·data plane·control plane·platform의 책임과 mesh가 다루지 않는 업무 트랜잭션을 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch17-02.md
-->

> **시각자료 제작 위치 — 애플리케이션·data plane·control plane·platform의 책임과 mesh가 다루지 않는 업무 트랜잭션을 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch17-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch17-02.md`  
> 대체 텍스트: 애플리케이션·data plane·control plane·platform의 책임과 mesh가 다루지 않는 업무 트랜잭션을 보여준다.


## 확장 전략

- scale profile이 다른 모듈만 독립적으로 분리한다.
- 동기 call depth와 fan-out budget을 제한한다.
- 플랫폼 자동화 없이는 서비스 수 증가를 멈추고 표준 golden path를 먼저 만든다.
- mesh policy는 namespace·tenant 단위로 점진 적용하고 config blast radius를 제한한다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

## 보안과 개인정보

- 서비스 identity와 사용자 identity를 구분해 전달한다.
- mTLS가 애플리케이션 권한을 대체하지 않는다는 점을 명시한다.
- 공유 DB를 분리하는 동안 최소 권한·감사·dual-write 위험을 관리한다.
- mesh admin과 workload deploy 권한을 분리한다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

## 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- 서비스별 SLO·call graph·dependency latency
- 배포 빈도·변경 실패율·MTTR
- 동기 call depth·fan-out·retry amplification
- mesh config reject·certificate expiry·proxy resource
- 공유 DB 접근·contract break 건수

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

## 비용과 운영 복잡도

- 서비스 하나마다 build·deploy·runtime·observability·on-call 비용이 생긴다.
- mesh proxy는 CPU·메모리·지연과 control plane 운영 비용을 추가한다.
- 모듈러 모놀리스는 인프라 비용이 낮지만 경계 테스트와 코드 ownership 투자가 필요하다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

## 흔한 오해와 안티패턴

- 서비스 수를 현대성 지표로 사용한다.
- 테이블을 서비스별로 나누면 도메인 경계가 생겼다고 생각한다.
- service mesh가 retry·transaction·보안을 자동으로 해결한다고 믿는다.
- 공통 라이브러리 업데이트를 위해 모든 서비스를 동시에 배포한다.

## 설계 리뷰

- [ ] 독립 배포가 실제로 필요한 변경 압력이 있는가?
- [ ] 서비스마다 데이터 쓰기 소유자와 on-call이 있는가?
- [ ] 동기 call graph가 사용자 SLO를 만족하는가?
- [ ] mesh 도입 전에 해결할 반복 문제와 성공 지표가 명확한가?
- [ ] 되돌리기 가능한 단계적 분리 계획이 있는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

## 연습문제

1. 공유 DB를 사용하는 5개 서비스가 왜 분산 모놀리스인지 장애 시나리오로 설명하라.
2. 모듈러 모놀리스의 주문 모듈을 서비스로 분리하는 expand-contract 단계를 설계하라.
3. mesh의 자동 재시도가 비멱등 결제 호출을 중복시키는 경로를 막아라.

## 핵심 요약

- 배포 단위와 모듈 경계는 다른 개념이다.
- 마이크로서비스는 독립성의 이익과 분산 비용을 함께 가진다.
- 데이터 소유권이 없는 서비스 분리는 독립적이지 않다.
- service mesh는 통신 인프라 문제를 해결할 뿐 도메인 설계를 대신하지 않는다.
- 팀의 운영 능력이 서비스 수의 현실적 상한을 결정한다.

## 출처

- [@kubernetes-concepts] Kubernetes Authors. **Kubernetes Concepts** (2026). https://kubernetes.io/docs/concepts/
- [@istio-architecture] Istio Authors. **Istio Architecture** (2026). https://istio.io/latest/docs/ops/deployment/architecture/
- [@iso-42010] ISO/IEC/IEEE. **ISO/IEC/IEEE 42010:2022 — Architecture description** (2022). https://www.iso.org/standard/74393.html

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
