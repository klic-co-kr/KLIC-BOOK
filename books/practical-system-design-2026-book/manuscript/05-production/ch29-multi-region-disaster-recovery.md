---
id: ch29
title: Multi-region·Backup·재해 복구
part: production
order: 29
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
- ch06
- ch10
- ch13
learning_objectives:
- RTO·RPO를 사용자 여정과 데이터별로 정의한다.
- multi-region active/standby·active/active를 비교한다.
- backup·restore·failover·failback을 반복 검증한다.
figures:
- chart-ch29-01
- fig-ch29-01
- fig-ch29-02
sources:
- nist-contingency
- google-sre-book
draft_notice: 기술·편집·접근성 검수 전 초고
---

## 29. Multi-region·Backup·재해 복구

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

### 이 장에서 해결할 문제

다중 리전은 backup을 대체하지 않고 backup도 즉시 failover를 제공하지 않는다. 인프라 장애, 리전 장애, 운영 실수, 논리적 데이터 손상, 자격증명 침해는 서로 다른 복구 수단과 증거를 요구한다.

이 절의 기준 출처: [@nist-contingency; @google-sre-book].

#### 학습 목표

- RTO·RPO를 사용자 여정과 데이터별로 정의한다.
- multi-region active/standby·active/active를 비교한다.
- backup·restore·failover·failback을 반복 검증한다.

### 먼저 결론

- RTO는 서비스 복구 시간, RPO는 허용 가능한 데이터 손실 시점이다.
- 복제는 최신 상태를 빠르게 전달하지만 잘못된 삭제와 오염도 복제한다.
- backup은 운영 계정·region·자격증명과 독립돼야 한다.
- DR 계획은 트래픽 전환 후 데이터 검증·외부 의존성·failback까지 포함한다.

### 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | Multi-region·Backup·재해 복구에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | RTO는 서비스 복구 시간, RPO는 허용 가능한 데이터 손실 시점이다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | DR 용량은 정상 평균이 아니라 장애 시 합류 트래픽과 복구 작업을 합쳐 계산한다. |
| 실패·복구 | “Backup unusable” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | 주기적 격리 restore와 application validation을 실행한다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | backup vault의 삭제·retention 변경 권한을 운영 admin과 분리한다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | backup age·success·immutability·restore test |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

<!-- figure-spec
id: chart-ch29-01
chapter: ch29
role: dr-rto-cost
kind: data-chart
generator: python-matplotlib
output: assets/charts/chart-ch29-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: backup/restore, pilot light, warm standby, active-active를 상대 RTO와 정상 비용으로 비교한다.
required_labels_ko:
- 상대 정상 운영 비용
- 상대 RTO
- 전략별 점
prohibited:
- 출처 없는 실측 수치
- 3D chart
- 잘린 축
- 색상만으로 구분
source_refs:
- nist-contingency
- google-sre-book
alt_ko: backup/restore, pilot light, warm standby, active-active를 상대 RTO와 정상 비용으로 비교한다.
caption_ko: DR 전략의 RTO·비용 비교
status: specified
spec_file: assets/specs/charts/chart-ch29-01.md
-->

> **시각자료 제작 위치 — DR 전략의 RTO·비용 비교**  
> 종류: `data-chart` · 상태: `specified` · 산출 경로: `assets/charts/chart-ch29-01.svg`  
> 제작 명세: `assets/specs/charts/chart-ch29-01.md`  
> 대체 텍스트: backup/restore, pilot light, warm standby, active-active를 상대 RTO와 정상 비용으로 비교한다.


### 핵심 개념

#### RTO

중단 후 허용 가능한 서비스 복구 시간 목표다.

#### RPO

복구 시 허용 가능한 데이터 손실 시점 목표다.

#### Backup

운영 상태와 분리된 복구용 데이터 사본이다.

#### PITR

log와 base snapshot을 이용해 특정 시점으로 복구하는 방식이다.

#### Active/Standby

한 region이 주 처리하고 다른 region이 대기한다.

#### Active/Active

둘 이상의 region이 동시에 사용자 요청을 처리한다.

#### Failback

비상 region에서 정상 배치로 돌아가며 데이터·트래픽을 다시 정렬하는 과정이다.

#### Recovery dependency

DNS, IdP, KMS, CI, 연락망처럼 복구에 필요한 외부·제어 구성 요소다.

핵심 개념의 정의와 범위는 [@nist-contingency; @google-sre-book]를 기준으로 재검토해야 한다.

### 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| 주 region | 정상 쓰기와 사용자 트래픽을 처리한다. |
| 대기/보조 region | 복제본·용량·구성을 준비한다. |
| Global traffic manager | 건강과 정책에 따라 전환한다. |
| Backup vault | 불변·교차 계정 사본과 catalog를 보존한다. |
| Recovery orchestrator | restore·config·secret·validation 순서를 실행한다. |
| Data validator | record count·checksum·업무 불변조건을 확인한다. |
| DR command | 권한 있는 의사결정·커뮤니케이션·audit를 담당한다. |

<!-- figure-spec
id: fig-ch29-01
chapter: ch29
role: dr-strategy-matrix
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch29-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: pilot light·warm standby·active-active를 RTO·RPO·비용·복잡도로 비교한다.
required_labels_ko:
- Pilot Light
- Warm Standby
- Active/Active
- RTO
- RPO
- 비용
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- nist-contingency
- google-sre-book
alt_ko: pilot light·warm standby·active-active를 RTO·RPO·비용·복잡도로 비교한다.
caption_ko: pilot light·warm standby·active-active를 RTO·RPO·비용·복잡도로 비교한다
status: specified
spec_file: assets/specs/svg/fig-ch29-01.md
-->

> **시각자료 제작 위치 — pilot light·warm standby·active-active를 RTO·RPO·비용·복잡도로 비교한다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch29-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch29-01.md`  
> 대체 텍스트: pilot light·warm standby·active-active를 RTO·RPO·비용·복잡도로 비교한다.


### 요청·데이터 흐름

1. 여정·데이터별 RTO/RPO tier를 정한다.
2. 각 실패 유형에 failover·restore·rebuild 중 수단을 매핑한다.
3. backup을 암호화·불변·교차 계정/region에 보존한다.
4. 복구 환경의 network·identity·secret·quota를 준비한다.
5. 게임데이에서 실제 traffic 없이 restore와 검증을 수행한다.
6. failover 시 쓰기 소유권과 DNS/route를 전환한다.
7. 안정화 후 delta sync·검증·점진 traffic으로 failback한다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

### 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| Pilot light | 핵심 데이터와 최소 인프라만 대기해 비용이 낮다. | scale-up·deploy 때문에 RTO가 길다. | 수시간 RTO |
| Warm standby | 축소된 전체 stack이 대기해 복구가 빠르다. | 지속 비용과 config drift 관리가 필요하다. | 수십 분 RTO |
| Multi-site active/active | 가장 빠른 지역 장애 우회와 낮은 지연을 제공한다. | 일관성·충돌·용량·운영 복잡도가 가장 크다. | 매우 짧은 RTO와 지역별 처리 |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@nist-contingency; @google-sre-book]를 참조한다.

### 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| Backup unusable | 백업 job은 성공했지만 key·schema·권한이 없어 restore가 실패한다. | 주기적 격리 restore와 application validation을 실행한다. |
| Corruption replication | 잘못된 삭제가 모든 active replica로 전파된다. | PITR·불변 backup·deletion delay를 둔다. |
| Standby drift | 대기 region의 image·config·quota가 달라 전환 후 오류가 난다. | IaC drift 검사와 정기 warm-up을 한다. |
| Traffic before data | DNS를 먼저 전환해 새 region이 읽기/쓰기 준비 전 요청을 받는다. | data readiness gate와 점진 traffic을 사용한다. |
| Failback loss | 두 region의 delta를 정리하지 않고 원래 region으로 돌아가 쓰기가 덮인다. | single writer epoch·reconciliation·read-only 전환 단계를 둔다. |

<!-- figure-spec
id: fig-ch29-02
chapter: ch29
role: recovery-runbook
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch29-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 장애 선언·쓰기 차단·restore/승격·검증·traffic 전환·failback 순서를 보여준다.
required_labels_ko:
- 장애 선언
- 쓰기 Fencing
- Restore/승격
- 데이터 검증
- Traffic 전환
- Failback
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- nist-contingency
- google-sre-book
alt_ko: 장애 선언·쓰기 차단·restore/승격·검증·traffic 전환·failback 순서를 보여준다.
caption_ko: 장애 선언·쓰기 차단·restore/승격·검증·traffic 전환·failback 순서를 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch29-02.md
-->

> **시각자료 제작 위치 — 장애 선언·쓰기 차단·restore/승격·검증·traffic 전환·failback 순서를 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch29-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch29-02.md`  
> 대체 텍스트: 장애 선언·쓰기 차단·restore/승격·검증·traffic 전환·failback 순서를 보여준다.


### 확장 전략

- DR 용량은 정상 평균이 아니라 장애 시 합류 트래픽과 복구 작업을 합쳐 계산한다.
- backup restore throughput이 데이터 증가를 따라가는지 정기 측정한다.
- tier별 서비스는 핵심 여정부터 복구하고 비핵심 batch·analytics를 뒤로 미룬다.
- multi-region을 서비스 전체가 아니라 필요한 데이터·기능에 선택적으로 적용한다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

### 보안과 개인정보

- backup vault의 삭제·retention 변경 권한을 운영 admin과 분리한다.
- ransomware·credential compromise 시나리오에서 독립 계정과 offline recovery credential을 검증한다.
- DR 중 개인정보 지역 이전과 규제 통보 절차를 준수한다.
- restore 데이터의 접근과 폐기를 감사한다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

### 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- backup age·success·immutability·restore test
- replication lag·RPO exposure·PITR window
- region readiness·config drift·quota
- failover 단계별 시간과 traffic 오류
- data validation mismatch·failback backlog

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

### 비용과 운영 복잡도

- 다중 region은 compute·storage·replication egress·운영 인력 비용을 크게 늘린다.
- backup 보존 기간과 restore 속도는 storage tier·index·catalog 비용을 교환한다.
- 모든 기능에 같은 RTO를 주지 않고 업무 tiering으로 투자한다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

### 흔한 오해와 안티패턴

- replica가 있으니 backup이 필요 없다고 생각한다.
- RTO/RPO를 모든 데이터에 한 숫자로 적는다.
- DNS 전환만 DR 완료로 본다.
- restore 성공 여부를 파일 존재로만 판단하고 애플리케이션 검증을 하지 않는다.

### 설계 리뷰

- [ ] 실패 유형별 복구 수단이 구분됐는가?
- [ ] RTO/RPO가 실제 restore/failover 결과로 입증되는가?
- [ ] backup이 운영 권한·region·자격증명과 독립적인가?
- [ ] 전환 후 데이터 쓰기 권한과 외부 의존성이 준비됐는가?
- [ ] failback·reconciliation·커뮤니케이션이 계획에 포함됐는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

### 연습문제

1. 주문 DB의 5분 RPO, 검색 index의 24시간 RPO를 각각 복구 설계하라.
2. 잘못된 DELETE가 20분 뒤 발견됐을 때 PITR과 신규 쓰기 보존 절차를 작성하라.
3. warm standby를 분기마다 시험할 게임데이 체크리스트를 만들라.

### 핵심 요약

- 복제·backup·DR은 서로 다른 실패를 담당한다.
- RTO/RPO는 사용자 여정과 데이터별로 정한다.
- 복구에는 identity·KMS·DNS·quota 같은 의존성이 필요하다.
- restore는 업무 불변조건으로 검증한다.
- failover 후 failback까지 하나의 절차다.

### 출처

- [@nist-contingency] NIST. **NIST SP 800-34 Rev. 1 — Contingency Planning Guide for Federal Information Systems** (2010). https://csrc.nist.gov/pubs/sp/800/34/r1/final
- [@google-sre-book] Google. **Site Reliability Engineering** (2016). https://sre.google/sre-book/table-of-contents/

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
