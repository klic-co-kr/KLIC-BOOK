---
id: ch32
title: LLM Inference·Batching·KV Cache·Model Routing
part: ai-native
order: 32
status: draft
freshness: volatile
last_verified: '2026-08-06'
review_due: '2026-11-06'
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
- ch21
- ch27
- ch30
learning_objectives:
- LLM 추론을 prefill·decode·KV cache·scheduler로 설명한다.
- continuous batching과 memory pressure의 trade-off를 이해한다.
- model routing·fallback·capacity를 품질·지연·비용으로 설계한다.
figures:
- chart-ch32-01
- fig-ch32-01
- fig-ch32-02
sources:
- vllm-paper
- orca-paper
- nist-genai-profile
draft_notice: 기술·편집·접근성 검수 전 초고
---

# 32. LLM Inference·Batching·KV Cache·Model Routing

> **원고 상태:** 이 장은 실제 내용이 들어 있는 1차 초고다. 출판 전 기술 검수, 문장 편집, 수치 재검증, 시각자료 제작이 필요하다.

## 이 장에서 해결할 문제

LLM 서빙의 병목은 단순히 GPU 연산량 하나가 아니다. 입력 token을 처리하는 prefill과 token을 순차 생성하는 decode는 자원 특성이 다르고, 각 요청의 KV cache가 동적으로 메모리를 점유한다. scheduler와 routing이 품질·지연·처리량·비용을 함께 결정한다.

이 절의 기준 출처: [@vllm-paper; @orca-paper].

### 학습 목표

- LLM 추론을 prefill·decode·KV cache·scheduler로 설명한다.
- continuous batching과 memory pressure의 trade-off를 이해한다.
- model routing·fallback·capacity를 품질·지연·비용으로 설계한다.

## 먼저 결론

- time-to-first-token과 inter-token latency를 전체 latency에서 분리한다.
- batch 크기를 고정하지 않고 도착·sequence 길이·deadline에 따라 연속적으로 관리한다.
- KV cache 부족은 admission·eviction·preemption·offload 정책을 요구한다.
- model routing은 “가장 싼 모델”이 아니라 품질 threshold·risk·latency·capacity를 만족하는 최소 비용 경로를 선택한다.

::: current-note
**2026-08-06 확인:** 이 장은 변화 가능한 표준·프로젝트·AI 구현을 포함한다. 기본 재검토일은 `2026-11-06`이며, 출판 직전 공식 문서를 다시 확인한다.
:::

## 요구사항과 실패 모델

| 차원 | 확인 질문 | 설계 판단 |
|---|---|---|
| 핵심 보장 | LLM Inference·Batching·KV Cache·Model Routing에서 사용자 또는 후속 시스템에 반드시 보장할 결과는 무엇인가? | time-to-first-token과 inter-token latency를 전체 latency에서 분리한다. |
| 규모·분포 | 피크 부하, 데이터량, 지역·tenant 편차가 설계에 어떤 영향을 주는가? | request count보다 input/output token과 sequence length 분포로 capacity를 계획한다. |
| 실패·복구 | “KV cache OOM” 같은 실패에서 결과를 어떻게 판정하고 복구하는가? | token admission, paged allocation, preemption, max length를 둔다. |
| 보안·통제 | 접근 권한, 데이터 보호, 경계 통제를 어디에 적용하는가? | prompt·output·KV·cache에 tenant 민감 데이터가 남는 수명과 격리를 명시한다. |
| 운영 검증 | 어떤 관측 신호로 설계가 실제 요구를 만족하는지 판단하는가? | TTFT·ITL/TPOT·end-to-end p95/p99 |

요구사항은 정상 처리량만으로 끝나지 않는다. 각 항목에 “지연되면?”, “중복되면?”, “일부만 성공하면?”, “운영자가 복구할 수 없으면?”을 추가해 실패 모델로 확장한다.

<!-- figure-spec
id: chart-ch32-01
chapter: ch32
role: llm-sequence-cost
kind: data-chart
generator: python-matplotlib
output: assets/charts/chart-ch32-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: 입력 sequence 길이 증가가 KV cache 점유와 TTFT·unit cost를 어떻게 키우는지 개념적으로 보여준다.
required_labels_ko:
- Input Token 길이
- 정규화된 자원/지연
- KV Cache
- TTFT
- 단위 비용
prohibited:
- 출처 없는 실측 수치
- 3D chart
- 잘린 축
- 색상만으로 구분
source_refs:
- vllm-paper
- orca-paper
alt_ko: 입력 sequence 길이 증가가 KV cache 점유와 TTFT·unit cost를 어떻게 키우는지 개념적으로 보여준다.
caption_ko: Sequence 길이와 KV Cache·TTFT
status: specified
spec_file: assets/specs/charts/chart-ch32-01.md
-->

> **시각자료 제작 위치 — Sequence 길이와 KV Cache·TTFT**  
> 종류: `data-chart` · 상태: `specified` · 산출 경로: `assets/charts/chart-ch32-01.svg`  
> 제작 명세: `assets/specs/charts/chart-ch32-01.md`  
> 대체 텍스트: 입력 sequence 길이 증가가 KV cache 점유와 TTFT·unit cost를 어떻게 키우는지 개념적으로 보여준다.

## 핵심 개념

### Prefill

입력 token 전체를 처리해 첫 KV 상태와 첫 출력 준비를 만드는 단계다.

### Decode

기존 KV cache를 재사용하며 token을 하나씩 생성하는 단계다.

### KV cache

attention의 과거 key/value를 요청·layer별로 보존해 반복 계산을 줄이는 메모리다.

### Continuous batching

완료된 요청을 batch에서 빼고 새 요청을 즉시 넣으며 decode iteration을 공유하는 scheduling이다.

### TTFT

요청부터 첫 token까지의 시간이다.

### ITL/TPOT

출력 token 사이 지연 또는 token당 시간이다.

### Model router

요청 특성·품질·비용·capacity에 따라 model/endpoint를 선택한다.

### Speculative decoding

작은 모델이 제안한 token을 큰 모델이 검증해 decode 속도를 높이는 계열의 방법이다.

### Admission control

예상 token·memory·deadline으로 요청을 수락·queue·거부하는 정책이다.

핵심 개념의 정의와 범위는 [@vllm-paper; @orca-paper; @nist-genai-profile]를 기준으로 재검토해야 한다.

## 기준 아키텍처

아래 구조는 특정 제품 목록이 아니라 책임과 경계를 표현한다. 실제 구현에서는 각 구성 요소의 소유자, 데이터 계약, SLO, 장애 도메인을 추가한다.

| 구성 요소 | 책임 |
|---|---|
| API gateway | auth·quota·request size·streaming 계약을 처리한다. |
| Prompt/context builder | token budget과 policy를 적용한다. |
| Model router | task·risk·language·capacity로 route를 선택한다. |
| Scheduler | prefill/decode queue와 continuous batch를 관리한다. |
| GPU workers | model weights와 KV cache로 inference를 수행한다. |
| KV cache manager | page/block 할당·eviction·prefix reuse를 관리한다. |
| Fallback pool | 다른 model·region·degraded response를 제공한다. |
| Telemetry/eval | quality·TTFT·ITL·token·cost를 기록한다. |

<!-- figure-spec
id: fig-ch32-01
chapter: ch32
role: llm-serving-runtime
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch32-01.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: gateway·router·prefill queue·decode scheduler·GPU worker·KV cache·streaming response를 보여준다.
required_labels_ko:
- Gateway
- Model Router
- Prefill Queue
- Decode Scheduler
- GPU Worker
- KV Cache
- Streaming
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- vllm-paper
- orca-paper
- nist-genai-profile
alt_ko: gateway·router·prefill queue·decode scheduler·GPU worker·KV cache·streaming response를 보여준다.
caption_ko: gateway·router·prefill queue·decode scheduler·GPU worker·KV cache·streaming response를 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch32-01.md
-->

> **시각자료 제작 위치 — gateway·router·prefill queue·decode scheduler·GPU worker·KV cache·streaming response를 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch32-01.svg`  
> 제작 명세: `assets/specs/svg/fig-ch32-01.md`  
> 대체 텍스트: gateway·router·prefill queue·decode scheduler·GPU worker·KV cache·streaming response를 보여준다.

## 요청·데이터 흐름

1. gateway가 auth·quota·max input/output token을 검증한다.
2. router가 task class·quality tier·deadline·capacity를 평가한다.
3. scheduler가 prefill queue와 decode batch에 요청을 배치한다.
4. KV manager가 예상 sequence 길이와 memory block을 할당한다.
5. GPU가 prefill 후 streaming decode를 수행한다.
6. client 취소·deadline 시 decode와 KV를 즉시 회수한다.
7. OOM·overload·quality risk 시 fallback 또는 거부한다.
8. 실제 token·latency·quality 결과를 routing feedback에 사용한다.

흐름을 검토할 때 각 단계의 성공 응답이 무엇을 보장하는지, timeout 이후 결과를 어떻게 확인하는지, 재시도 시 같은 효과가 반복되는지를 함께 기록한다.

## 대안과 트레이드오프

| 대안 | 장점 | 비용·위험 | 적합한 조건 |
|---|---|---|---|
| 단일 대형 model | 품질과 운영 경로가 단순하다. | 비용·latency·capacity 효율이 낮을 수 있다. | 고위험·복잡 task |
| 다중 model routing | 단순 task를 저비용 model로 보내 unit cost를 낮춘다. | 평가·fallback·일관성·debug가 복잡하다. | 다양한 task와 traffic |
| 외부 managed inference | 빠른 도입과 운영 부담 감소가 있다. | quota·data policy·egress·vendor dependency가 있다. | 변동 workload·초기 제품 |
| 자체 GPU serving | 세밀한 최적화와 데이터 통제가 가능하다. | capacity planning·driver·scheduler·on-call 비용이 크다. | 지속 대규모 traffic·특수 요구 |

대안 비교는 제품 선호가 아니라 이 장의 요구사항과 실패 모델을 기준으로 수행한다. 관련 근거는 [@vllm-paper; @orca-paper; @nist-genai-profile]를 참조한다.

## 장애 시나리오

| 시나리오 | 영향 | 대응 원칙 |
|---|---|---|
| KV cache OOM | 긴 prompt와 많은 동시 request가 memory를 소진한다. | token admission, paged allocation, preemption, max length를 둔다. |
| Head-of-line in batch | 긴 prefill 하나가 짧은 decode 요청 TTFT/ITL을 악화시킨다. | prefill chunking, separate queue, priority scheduling을 사용한다. |
| Client disconnect leak | stream 종료 후 decode와 KV가 계속 남는다. | cancellation propagation과 resource reclamation SLO를 둔다. |
| Router feedback loop | 한 endpoint가 느려 우회 트래픽이 다른 endpoint를 포화시키며 계속 진동한다. | hysteresis, capacity reservation, bounded shift를 사용한다. |
| Quality regression | 저비용 model route가 특정 언어·tenant에서 실패한다. | segment별 eval gate, shadow traffic, fallback threshold를 둔다. |
| Quota cliff | 공급자 rate limit이 갑자기 발생해 전체 요청이 재시도된다. | token bucket, queue, multi-provider policy, retry budget을 둔다. |

<!-- figure-spec
id: fig-ch32-02
chapter: ch32
role: model-routing-policy
kind: technical-diagram
generator: direct-svg
output: assets/figures/fig-ch32-02.svg
canvas_preset: chapter-wide
aspect_ratio: '16:9'
brief_ko: task risk·quality threshold·latency·cost·capacity에 따라 model과 fallback을 선택하는 decision flow를 보여준다.
required_labels_ko:
- Task Class
- Risk
- Quality Gate
- Latency Budget
- Cost
- Capacity
- Fallback
prohibited:
- 임의 성능 수치
- 제품 로고
- 래스터 이미지
- base64
- 텍스트 path 변환
source_refs:
- vllm-paper
- orca-paper
- nist-genai-profile
alt_ko: task risk·quality threshold·latency·cost·capacity에 따라 model과 fallback을 선택하는 decision flow를 보여준다.
caption_ko: task risk·quality threshold·latency·cost·capacity에 따라 model과 fallback을 선택하는 decision flow를 보여준다
status: specified
spec_file: assets/specs/svg/fig-ch32-02.md
-->

> **시각자료 제작 위치 — task risk·quality threshold·latency·cost·capacity에 따라 model과 fallback을 선택하는 decision flow를 보여준다**  
> 종류: `technical-diagram` · 상태: `specified` · 산출 경로: `assets/figures/fig-ch32-02.svg`  
> 제작 명세: `assets/specs/svg/fig-ch32-02.md`  
> 대체 텍스트: task risk·quality threshold·latency·cost·capacity에 따라 model과 fallback을 선택하는 decision flow를 보여준다.

## 확장 전략

- request count보다 input/output token과 sequence length 분포로 capacity를 계획한다.
- prefill-heavy와 decode-heavy workload를 분리하거나 scheduler weight를 다르게 둔다.
- prefix cache는 반복 system prompt에 유리하지만 tenant/secret 경계를 보존한다.
- autoscaling은 GPU 준비 시간과 model load 시간을 고려해 floor와 queue를 둔다.
- routing은 품질이 검증된 candidate set 안에서만 비용 최적화를 수행한다.

확장은 구성 요소 수를 늘리는 행위가 아니라 병목 축과 실패 범위를 다시 분리하는 과정이다. 확장 전후의 사용자 SLI와 운영 복잡도를 함께 비교한다.

## 보안과 개인정보

- prompt·output·KV·cache에 tenant 민감 데이터가 남는 수명과 격리를 명시한다.
- model endpoint와 tool access 권한을 분리하고 route 결과가 보안 정책을 낮추지 않게 한다.
- 외부 inference 전송 데이터와 보존 정책을 검토한다.
- prefix cache key에 tenant·policy·model version을 포함한다.

보안 요구는 별도 부록이 아니라 요청·데이터 흐름의 각 경계에 적용한다. 특히 인증된 주체, tenant, 데이터 분류, 보존·삭제, 운영자 권한을 함께 기록한다.

## 관측 가능성

다음 신호를 최소 세그먼트(서비스·지역·tenant 또는 workload class)로 나눠 본다.

- TTFT·ITL/TPOT·end-to-end p95/p99
- input/output token·sequence length·batch occupancy
- GPU utilization·memory·KV block usage·preemption
- queue age·admission reject·client cancel reclaim
- model/route별 quality·fallback·error
- request/token/accepted-answer 단위 비용

경보는 개별 자원 임계값보다 사용자 SLO와 error budget 소진에 연결하고, 조사 시 trace·log·변경 이력으로 내려갈 수 있어야 한다.

## 비용과 운영 복잡도

- GPU cost는 할당 시간과 utilization뿐 아니라 idle floor·model load·replica redundancy로 결정된다.
- 긴 output은 decode 시간과 egress·사용자 대기를 동시에 늘린다.
- routing은 저비용 호출 비율이 아니라 품질 통과 답변당 비용으로 평가한다.
- managed와 self-hosted 비교에 on-call·capacity risk·upgrade를 포함한다.

비용 비교에는 인스턴스 가격뿐 아니라 데이터 전송, 복제·백업, 관측, 보안 통제, 업그레이드, on-call, 장애 복구, 탈출 비용을 포함한다.

## 흔한 오해와 안티패턴

- GPU utilization 하나로 사용자 성능을 판단한다.
- batch를 크게 하면 항상 처리량과 지연이 모두 좋아진다고 생각한다.
- 요청 수만으로 capacity를 계산하고 token 길이를 무시한다.
- router가 평가 없이 가장 싼 model을 선택하게 한다.

## 설계 리뷰

- [ ] TTFT와 ITL SLO가 분리됐는가?
- [ ] token·KV memory 기반 admission이 있는가?
- [ ] client 취소가 compute와 memory를 회수하는가?
- [ ] route별 quality gate와 fallback이 검증됐는가?
- [ ] unit cost가 request가 아니라 token·품질 결과와 연결되는가?

리뷰 결과는 “통과/실패”만 기록하지 않고 남은 가정, 위험 수용자, 실험, 재검토일을 ADR과 backlog에 연결한다.

## 연습문제

1. 동시 요청 100개가 각각 input 8K, output 1K일 때 KV cache와 latency 위험을 정성적으로 분석하라.
2. prefill-heavy 문서 요약과 decode-heavy 채팅을 같은 cluster에서 scheduling하는 정책을 설계하라.
3. 고위험 법률 질문은 큰 model, 일반 FAQ는 작은 model로 route하는 평가 gate를 작성하라.

## 핵심 요약

- LLM inference는 prefill과 decode의 자원 특성이 다르다.
- KV cache가 동시성과 sequence 길이 한계를 결정한다.
- continuous batching은 throughput과 tail을 함께 관리한다.
- model routing은 품질 threshold 안에서 비용을 최적화한다.
- token·memory·취소를 admission과 관측에 포함한다.

## 출처

- [@vllm-paper] Woosuk Kwon et al.. **Efficient Memory Management for Large Language Model Serving with PagedAttention** (2023). https://arxiv.org/abs/2309.06180
- [@orca-paper] Gyeong-In Yu et al.. **Orca: A Distributed Serving System for Transformer-Based Generative Models** (2022). https://www.usenix.org/conference/osdi22/presentation/yu
- [@nist-genai-profile] NIST. **Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile** (2024). https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence

> **검증 기준일:** 2026-08-06. `current`와 `volatile` 내용은 release 전에 공식 원문을 다시 확인한다.
