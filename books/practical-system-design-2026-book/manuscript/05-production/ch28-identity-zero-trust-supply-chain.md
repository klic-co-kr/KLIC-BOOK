---
id: ch28
title: 인증·인가·Zero Trust·Secrets·공급망 보안
part: production
order: 28
status: draft
freshness: current
last_verified: '2026-08-06'
review_due: '2027-02-06'
upstream_lineage:
- source: system-design-primer
  file: README.md
  anchor: not-applicable
  action: REPLACE
audiences:
- backend-engineer
- platform-engineer
prerequisites:
- ch01
- ch14
- ch27
learning_objectives:
- 인증·인가·세션·서비스 identity를 구분한다.
- zero trust 원칙을 자원 접근 흐름에 적용한다.
- secret·artifact·배포 공급망을 검증 가능하게 만든다.
figures:
- fig-ch28-01
- fig-ch28-02
sources:
- nist-zero-trust
- rfc9700
- webauthn3
- slsa12
draft_notice: 기술·편집·접근성 검수 전 초고
---

## 28. 인증·인가·Zero Trust·Secrets·공급망 보안

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

### 이 장에서 해결할 문제

보안은 외곽 방화벽 한 겹이 아니라 모든 자원 접근에서 주체, 장치, workload, 요청 맥락, 정책을 검증하는 연속된 결정이다. 네트워크 위치는 신뢰의 근거 중 하나일 뿐이며, 인증 성공과 업무 권한 승인은 분리해야 한다.

이 절의 기준 출처: [@nist-zero-trust; @rfc9700].

#### 학습 목표

- 인증·인가·세션·서비스 identity를 구분한다.
- zero trust 원칙을 자원 접근 흐름에 적용한다.
- secret·artifact·배포 공급망을 검증 가능하게 만든다.

### 먼저 결론

- 인증은 누구인지, 인가는 무엇을 할 수 있는지 결정한다.
- zero trust는 내부망이라는 이유만으로 암묵적 신뢰를 부여하지 않는다.
- 장기 secret를 코드·이미지·환경에 복사하지 않고 짧은 수명 credential과 workload identity를 선호한다.
- 배포 artifact는 출처·build 과정·서명을 검증하고 생산자에서 runtime까지 계보를 보존한다.

::: current-note
**2026-08-06 확인:** 이 장은 변화 가능한 표준·프로젝트·AI 구현을 포함한다. 기본 재검토일은 `2027-02-06`이며, 출판 직전 공식 문서를 다시 확인한다.
:::

### 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | 인증·인가·Zero Trust·Secrets·공급망 보안에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | 인증은 누구인지, 인가는 무엇을 할 수 있는지 결정한다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | 정책 평가를 중앙 논리와 지역 cache로 분리하되 revoke·version 정책을 둔다. |
| 실패·복구 | “Token theft” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | 짧은 수명, sender constraint, audience 제한, revoke·risk signal을 사용한다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | 개인정보 최소 수집·목적 제한·보존·삭제를 데이터 설계에 포함한다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | 인증 성공/실패·MFA/WebAuthn 사용률·위험 신호 |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

### 핵심 개념

#### 인증

사용자·서비스·장치가 주장한 identity를 검증한다.

#### 인가

검증된 주체가 특정 자원에 특정 action을 수행할 수 있는지 결정한다.

#### 세션

인증 상태를 일정 기간 유지하는 server/client 계약이다.

#### Zero trust

위치나 소유만으로 신뢰하지 않고 접근마다 명시적 검증과 최소 권한을 적용하는 접근법이다.

#### Workload identity

서비스 instance가 장기 공유 secret 없이 자신을 증명하는 identity다.

#### Secret

password, API key, private key처럼 노출되면 권한을 행사할 수 있는 값이다.

#### Attestation/Provenance

artifact가 어떤 source·builder·dependency로 생성됐는지 검증하는 증거다.

#### FIDO/WebAuthn

공개키 credential로 phishing-resistant 인증을 제공하는 웹 표준 계열이다.

핵심 개념의 정의와 범위는 [@nist-zero-trust; @rfc9700; @webauthn3; @slsa12]를 기준으로 재검토해야 한다.

### 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| Identity provider | 사용자 인증과 token 발급을 담당한다. |
| Policy decision point | subject·resource·action·context를 평가한다. |
| Policy enforcement point | gateway·service·DB에서 결정을 강제한다. |
| Workload identity issuer | runtime attestation을 바탕으로 짧은 credential을 발급한다. |
| Secret manager/KMS | secret과 key의 생성·보관·회전·감사를 제공한다. |
| Artifact registry | 서명된 image/package와 provenance를 보존한다. |
| Admission controller | 검증되지 않은 artifact·권한·구성을 배포 전에 차단한다. |
| Audit pipeline | 인증·정책 결정·관리 작업을 tamper-evident하게 기록한다. |

<!-- figure-spec
id: fig-ch28-01
chapter: ch28
role: zero-trust-access
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch28-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 사용자·장치·workload identity와 정책 결정·강제·resource 접근 경계를 보여준다.
required_labels_ko:
- 사용자
- 장치
- Identity Provider
- Policy Engine
- Enforcement Point
- Resource
- Audit
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- nist-zero-trust
- rfc9700
- webauthn3
alt_ko: 사용자·장치·workload identity와 정책 결정·강제·resource 접근 경계를 보여준다.
caption_ko: 사용자·장치·workload identity와 정책 결정·강제·resource 접근 경계를 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch28-01.md
-->

> **시각자료 제작 위치 — 사용자·장치·workload identity와 정책 결정·강제·resource 접근 경계를 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch28-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch28-01.md`  
> 대체 텍스트: 사용자·장치·workload identity와 정책 결정·강제·resource 접근 경계를 보여준다.

### 요청·데이터 흐름

1. 사용자 또는 workload가 강한 인증으로 identity를 얻는다.
2. 요청이 audience·scope·expiry가 제한된 token을 제시한다.
3. enforcement point가 token 서명·발급자·replay·binding을 검증한다.
4. policy engine이 resource·tenant·action·context로 권한을 결정한다.
5. 민감 action은 step-up 또는 별도 승인·transaction 정책을 요구한다.
6. 배포 시 artifact signature와 provenance를 검증한다.
7. secret·권한·artifact 변경을 감사하고 자동 만료·회전한다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

### 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| 중앙 RBAC | 역할 기반 관리가 단순하고 감사하기 쉽다. | 역할 폭증과 context 부족이 생길 수 있다. | 안정된 조직 권한 |
| ABAC/정책 엔진 | resource·tenant·시간·위험 등 세밀한 결정을 제공한다. | 정책 디버깅·성능·일관성 운영이 필요하다. | 복잡한 멀티테넌트·규제 |
| 네트워크 격리 중심 | 침해 표면과 경로를 줄인다. | identity·업무 권한을 대체할 수 없다. | 방어 계층 |
| 짧은 workload credential | 장기 secret 노출 위험을 줄인다. | identity control plane 가용성과 clock이 필요하다. | 동적 cloud workload |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@nist-zero-trust; @rfc9700; @webauthn3]를 참조한다.

### 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| Token theft | bearer token이 탈취돼 다른 장치에서 사용된다. | 짧은 수명, sender constraint, audience 제한, revoke·risk signal을 사용한다. |
| 권한 cache stale | role 회수 후 오래된 정책 cache가 계속 허용한다. | versioned policy와 민감 action의 강한 recheck를 둔다. |
| Secret sprawl | 키가 repo·image·log·CI 변수에 복제된다. | 동적 발급, secret scanning, 중앙 rotation, 사용 inventory를 둔다. |
| Supply-chain compromise | 악성 dependency 또는 builder가 정상 이름 artifact를 만든다. | pinning, isolated build, provenance, signature, admission verification을 사용한다. |
| Break-glass abuse | 비상 계정이 평상시 우회 경로가 된다. | 시간 제한·다중 승인·강한 감사·사후 검토를 적용한다. |
| IdP outage | 인증·token 검증 제어면 장애가 모든 서비스로 전파된다. | local signature validation, key cache, 제한된 기존 session 정책을 둔다. |

<!-- figure-spec
id: fig-ch28-02
chapter: ch28
role: software-supply-chain
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch28-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: source·dependency·builder·artifact·registry·admission·runtime의 서명과 provenance 검증을 보여준다.
required_labels_ko:
- Source
- Dependency
- Builder
- Provenance
- Artifact Registry
- Admission
- Runtime
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- nist-zero-trust
- rfc9700
- webauthn3
alt_ko: source·dependency·builder·artifact·registry·admission·runtime의 서명과 provenance 검증을 보여준다.
caption_ko: source·dependency·builder·artifact·registry·admission·runtime의 서명과 provenance 검증을 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch28-02.md
-->

> **시각자료 제작 위치 — source·dependency·builder·artifact·registry·admission·runtime의 서명과 provenance 검증을 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch28-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch28-02.md`  
> 대체 텍스트: source·dependency·builder·artifact·registry·admission·runtime의 서명과 provenance 검증을 보여준다.

### 확장 전략

- 정책 평가를 중앙 논리와 지역 cache로 분리하되 revoke·version 정책을 둔다.
- resource별 권한을 token에 모두 넣어 비대해지지 않게 최소 claim과 server lookup을 조합한다.
- 서비스 수가 늘면 workload identity와 mTLS 발급을 자동화한다.
- audit와 detection은 high-volume access와 high-risk admin action을 다른 보존·경보로 관리한다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

### 보안과 개인정보

- 개인정보 최소 수집·목적 제한·보존·삭제를 데이터 설계에 포함한다.
- 인증 로그에도 user agent·IP·device 정보가 민감할 수 있어 접근과 보존을 제한한다.
- key와 secret는 환경별·tenant별 blast radius를 줄이고 회전 가능해야 한다.
- 보안 정책 변경도 코드 리뷰·canary·rollback을 거친다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

### 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- 인증 성공/실패·MFA/WebAuthn 사용률·위험 신호
- 인가 allow/deny·policy version·decision latency
- token expiry·revocation·invalid audience
- secret age·rotation failure·unused credential
- artifact signature/provenance admission failure
- break-glass·privileged action·audit gap

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

### 비용과 운영 복잡도

- 세밀한 정책과 짧은 credential은 control plane·KMS·audit 비용을 만든다.
- 장기 secret는 초기 비용이 낮지만 침해 탐지·회전·사고 비용이 크다.
- 공급망 검증은 build 시간을 늘려도 배포 시 신뢰 근거와 사고 조사 시간을 줄인다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

### 흔한 오해와 안티패턴

- 내부망 요청은 인증을 생략한다.
- JWT 서명만 검증하면 권한 검사가 끝났다고 생각한다.
- secret를 암호화해 repo에 넣으면 안전하다고 본다.
- SBOM이나 서명 파일이 존재하면 실제 배포 artifact가 검증됐다고 가정한다.

### 설계 리뷰

- [ ] 주체·resource·action·context가 권한 결정에 포함되는가?
- [ ] token·policy cache·revocation의 시간 경계가 정의됐는가?
- [ ] 장기 secret를 줄이고 회전·폐기가 자동화됐는가?
- [ ] artifact provenance가 runtime admission에서 실제 검증되는가?
- [ ] break-glass와 관리 action이 독립 감사되는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

### 연습문제

1. 관리자·상담사·학생이 있는 교육 시스템의 RBAC/ABAC 정책을 설계하라.
2. IdP가 20분 중단될 때 신규 로그인과 기존 session의 정책을 구분하라.
3. source commit에서 production container까지 SLSA형 provenance 검증 경로를 그려라.

### 핵심 요약

- 인증과 인가는 별도 결정이다.
- zero trust는 위치 기반 암묵 신뢰를 제거한다.
- 짧은 workload identity가 장기 secret를 줄인다.
- policy cache와 revoke 경계를 설계한다.
- 공급망 증거는 배포 시 검증돼야 가치가 있다.

### 출처

- [@nist-zero-trust] NIST. **NIST SP 800-207 — Zero Trust Architecture** (2020). https://csrc.nist.gov/pubs/sp/800/207/final
- [@rfc9700] IETF. **RFC 9700 — Best Current Practice for OAuth 2.0 Security** (2025). https://www.rfc-editor.org/rfc/rfc9700.html
- [@webauthn3] W3C. **Web Authentication: An API for accessing Public Key Credentials — Level 3 (Candidate Recommendation Snapshot)** (2026). https://www.w3.org/TR/webauthn-3/
- [@slsa12] OpenSSF. **SLSA Specification v1.2** (2025). https://slsa.dev/spec/v1.2/

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
