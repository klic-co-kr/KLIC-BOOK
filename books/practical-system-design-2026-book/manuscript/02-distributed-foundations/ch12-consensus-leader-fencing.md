---
id: ch12
title: Consensus·Leader Election·Fencing
part: distributed-foundations
order: 12
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
- ch09
- ch10
learning_objectives:
- 합의가 필요한 문제와 불필요한 문제를 구분한다.
- term·log replication·majority의 역할을 설명한다.
- lease와 fencing으로 stale leader를 차단한다.
figures:
- fig-ch12-01
- fig-ch12-02
sources:
- raft-paper
- paxos-made-simple
- chubby-paper
draft_notice: 기술·편집·접근성 검수 전 초고
---

# 12. Consensus·Leader Election·Fencing

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

## 이 장에서 해결할 문제

합의는 모든 데이터를 전역 정렬하는 만능 도구가 아니다. 소수의 중요한 메타데이터, leader, membership, lock ownership처럼 단일 결정을 공유해야 할 때 사용하며, 장애 중 안전성과 가용성의 경계를 명확히 한다.

이 절의 기준 출처: [@raft-paper; @paxos-made-simple].

### 학습 목표

- 합의가 필요한 문제와 불필요한 문제를 구분한다.
- term·log replication·majority의 역할을 설명한다.
- lease와 fencing으로 stale leader를 차단한다.

## 먼저 결론

- majority가 없으면 안전한 새 leader를 선출할 수 없으므로 쓰기를 중단하는 편이 낡은 leader 두 개보다 낫다.
- leader election만으로 stale writer가 사라지지 않으므로 저장소가 term·fencing token을 검증해야 한다.
- 합의 그룹 크기와 지리적 배치는 지연·장애 허용·운영 비용을 함께 결정한다.
- 대용량 사용자 데이터보다 작은 제어 메타데이터에 합의를 집중한다.

## 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | Consensus·Leader Election·Fencing에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | majority가 없으면 안전한 새 leader를 선출할 수 없으므로 쓰기를 중단하는 편이 낡은 leader 두 개보다 낫다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | 합의 그룹을 지나치게 크게 만들지 않고 여러 독립 그룹으로 분할한다. |
| 실패·복구 | “Minority island” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | quorum 상실 시 쓰기를 중단하고 fencing을 검증한다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | membership·leader 강제 이전·snapshot 접근 권한을 분리한다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | term 변경·election 시간·leader churn |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

## 핵심 개념

### 합의

비동기 통신과 일부 실패가 있는 노드들이 하나의 값 또는 로그 순서에 동의하는 문제다.

### Term/Epoch

leader 세대를 증가시키는 논리 번호다.

### Majority quorum

구성원 절반 초과가 참여한 겹치는 집합으로 두 개의 독립 leader 결정을 막는다.

### Log replication

leader가 명령 순서를 복제하고 commit된 prefix를 모든 노드가 동일하게 적용하도록 한다.

### Lease

일정 시간 동안 권한이 유효하다는 계약이며 시계 오차와 지연 상한을 고려해야 한다.

### Fencing token

새 소유자가 더 큰 번호를 받아 하위 저장소가 오래된 소유자의 쓰기를 거부하게 하는 값이다.

### Membership change

합의 그룹 구성원을 안전하게 추가·제거하는 절차다.

핵심 개념의 정의와 범위는 [@raft-paper; @paxos-made-simple; @chubby-paper]를 기준으로 재검토해야 한다.

## 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| Consensus members | term, vote, replicated log를 보존한다. |
| Leader | 클라이언트 명령을 log에 순서대로 제안한다. |
| Follower | log를 복제하고 leader 건강을 관찰한다. |
| Client proxy | 현재 leader를 찾고 redirect·retry를 처리한다. |
| State machine | commit된 명령을 결정적으로 적용한다. |
| Fenced resource | DB·파일·작업 실행기가 token을 확인해 stale owner를 막는다. |
| Snapshot/compaction | 오래된 log를 압축하고 신규 노드를 빠르게 합류시킨다. |

<!-- figure-spec
id: fig-ch12-01
chapter: ch12
role: raft-log-consensus
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch12-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: leader가 term·index를 가진 log를 복제하고 majority commit하는 과정을 보여준다.
required_labels_ko:
- Leader
- Follower A
- Follower B
- Term
- Log Index
- Majority
- Commit
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- raft-paper
- paxos-made-simple
- chubby-paper
alt_ko: leader가 term·index를 가진 log를 복제하고 majority commit하는 과정을 보여준다.
caption_ko: leader가 term·index를 가진 log를 복제하고 majority commit하는 과정을 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch12-01.md
-->

> **시각자료 제작 위치 — leader가 term·index를 가진 log를 복제하고 majority commit하는 과정을 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch12-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch12-01.md`  
> 대체 텍스트: leader가 term·index를 가진 log를 복제하고 majority commit하는 과정을 보여준다.

## 요청·데이터 흐름

1. 클라이언트가 요청 ID와 명령을 leader에 보낸다.
2. leader가 현재 term과 log index를 붙여 replica에 전송한다.
3. majority가 내구성 있게 저장하면 commit index를 전진시킨다.
4. 모든 노드는 같은 순서로 상태 기계에 적용한다.
5. leader 응답이 유실되면 클라이언트는 요청 ID로 결과를 재조회한다.
6. leader 상실 시 더 최신 log를 가진 후보가 새 term에서 선출된다.
7. 외부 자원은 새 fencing token보다 작은 쓰기를 거부한다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

## 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| Raft형 replicated log | 역할과 log 규칙을 설명하기 쉽고 구현이 널리 검증됐다. | membership·snapshot·운영 구현은 여전히 복잡하다. | 제어 메타데이터·구성 저장소 |
| 외부 합의 서비스 사용 | 애플리케이션이 직접 알고리즘을 구현하지 않아도 된다. | 외부 서비스의 SLO·세션·watch 의미를 이해해야 한다. | leader lease·service discovery |
| DB row lock/lease | 작은 범위에서 단순하고 기존 트랜잭션을 활용한다. | 시계·연결 끊김·긴 작업에 stale owner 위험이 있다. | 단일 DB 범위 작업 잠금 |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@raft-paper; @paxos-made-simple; @chubby-paper]를 참조한다.

## 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| Minority island | 분할된 소수 노드가 이전 leader를 계속 신뢰한다. | quorum 상실 시 쓰기를 중단하고 fencing을 검증한다. |
| 장기 GC pause | leader가 멈춘 동안 새 leader가 선출되고, 이전 leader가 깨어나 다시 쓴다. | term/token을 모든 외부 쓰기에 전달한다. |
| Disk full | 일부 노드가 log를 저장하지 못해 quorum과 snapshot이 정체된다. | 디스크 여유·compaction·read-only 보호 모드를 둔다. |
| 잘못된 membership 변경 | 동시에 여러 구성을 바꿔 겹치지 않는 quorum이 생긴다. | joint consensus 또는 검증된 순차 절차를 사용한다. |
| 결정적 적용 위반 | 노드별 시간·무작위·외부 호출로 상태 기계 결과가 달라진다. | 명령에 필요한 결과를 포함하고 적용 함수를 결정적으로 만든다. |

<!-- figure-spec
id: fig-ch12-02
chapter: ch12
role: lease-fencing
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch12-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 오래된 worker와 새 worker가 같은 자원에 접근할 때 fencing token이 stale write를 막는 모습을 보여준다.
required_labels_ko:
- Worker A
- Worker B
- Lease
- Fencing Token
- 공유 자원
- 거부
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- raft-paper
- paxos-made-simple
- chubby-paper
alt_ko: 오래된 worker와 새 worker가 같은 자원에 접근할 때 fencing token이 stale write를 막는 모습을 보여준다.
caption_ko: 오래된 worker와 새 worker가 같은 자원에 접근할 때 fencing token이 stale write를 막는 모습을 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch12-02.md
-->

> **시각자료 제작 위치 — 오래된 worker와 새 worker가 같은 자원에 접근할 때 fencing token이 stale write를 막는 모습을 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch12-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch12-02.md`  
> 대체 텍스트: 오래된 worker와 새 worker가 같은 자원에 접근할 때 fencing token이 stale write를 막는 모습을 보여준다.

## 확장 전략

- 합의 그룹을 지나치게 크게 만들지 않고 여러 독립 그룹으로 분할한다.
- read-only 요청은 linearizable read 필요 여부에 따라 lease/read-index/stale replica를 선택한다.
- snapshot 생성·전송이 정상 log 복제와 경쟁하지 않도록 제한한다.
- 장거리 다중 리전 quorum은 쓰기 지연을 직접 증가시키므로 배치와 쓰기 소유권을 재검토한다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

## 보안과 개인정보

- membership·leader 강제 이전·snapshot 접근 권한을 분리한다.
- 합의 로그에 비밀 원문을 넣지 않고 암호화 또는 참조를 사용한다.
- fencing token을 클라이언트 주장만 믿지 않고 신뢰된 저장소가 검증한다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

## 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- term 변경·election 시간·leader churn
- commit latency와 quorum unavailable
- replication match index·snapshot backlog
- stale token 거부 건수
- membership 변경 상태와 disk fsync 오류

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

## 비용과 운영 복잡도

- 합의 노드는 소수라도 상시 다중 장애 도메인 비용이 든다.
- 원격 quorum은 매 쓰기에 네트워크 왕복을 추가한다.
- 자체 구현보다 검증된 시스템 운영이 대개 저렴하지만 그 시스템의 장애 의미를 학습해야 한다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

## 흔한 오해와 안티패턴

- 분산 lock API를 호출했으니 오래 걸리는 작업이 안전하다고 믿는다.
- heartbeats만으로 lease 안전성을 보장한다.
- 합의 그룹에 대용량 blob과 모든 이벤트를 넣는다.
- quorum 수만 맞추고 failure domain과 membership 변경을 무시한다.

## 설계 리뷰

- [ ] 합의가 필요한 단일 결정이 정확히 무엇인가?
- [ ] quorum 상실 시 안전한 동작이 정의됐는가?
- [ ] stale leader의 외부 쓰기를 누가 거부하는가?
- [ ] membership·snapshot·disk full을 운영에서 시험했는가?
- [ ] 합의 데이터 범위가 최소화됐는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

## 연습문제

1. 작업 스케줄러 leader가 GC pause 후 돌아오는 상황을 fencing token으로 해결하라.
2. 5노드 합의 그룹이 두 zone에 3:2로 배치될 때 zone 장애별 가용성을 분석하라.
3. 합의 로그에 비결정적 명령을 넣었을 때 상태가 갈라지는 예를 만들라.

## 핵심 요약

- 합의는 중요한 단일 결정과 로그 순서를 공유하는 도구다.
- majority quorum은 서로 겹쳐 두 leader 결정을 막는다.
- leader election과 stale writer 차단은 별도 문제다.
- fencing token은 하위 자원이 검증해야 한다.
- membership·snapshot·disk도 합의 시스템의 핵심 운영 영역이다.

## 출처

- [@raft-paper] Diego Ongaro and John Ousterhout. **In Search of an Understandable Consensus Algorithm** (2014). https://raft.github.io/raft.pdf
- [@paxos-made-simple] Leslie Lamport. **Paxos Made Simple** (2001). https://lamport.azurewebsites.net/pubs/paxos-simple.pdf
- [@chubby-paper] Mike Burrows. **The Chubby Lock Service for Loosely-Coupled Distributed Systems** (2006). https://research.google/pubs/the-chubby-lock-service-for-loosely-coupled-distributed-systems/

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
