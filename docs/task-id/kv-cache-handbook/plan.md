# kv-cache-handbook 한국어판 제작 — 구현계획 (L티어)

작성 2026-09-07 · 개정 2026-09-07 (recon-vision 반영 → ②적대검토 3렌즈 34항 반영 v3) ·
전거: `docs/task-id/kv-cache-handbook/recon.md` · `recon-vision.md` · 스킬 `skills/korean-ebook`

## 0. 과업 요약

중문 핸드북 「Understanding KV Cache」(@techNmak, Understanding AI 시리즈 02, 33면)을
한국어 출판형 전자서로 제작한다. 본 과업은 **신규 콘텐츠 생산**(원고 md 39件 + 설정·메타 4件 = 총 43件)이며
엔진·스킬·기존 책은 무변경. 빌드·QC는 기존 korean-ebook 파이프라인이 담당한다.

- 스타일: `practical` (신국판 153×225, G3 밴드 30–40자/줄) — recon 확정
- 제목: 「KV 캐시의 이해」 / 부제 "자기회귀 디코딩에서 최신 대규모 언어모델 추론까지 — Understanding AI 핸드북 02 한국어판"
  (recon 안의 '대언어모델'을 '대규모 언어모델'로 확정 — 일반 독자 정착어. §4 용어 계약 참조)
- 저자 표기: "원문 techNmak · 한국어판 KLIC" · 발행월 2026-09
- 규모: 원문 32 소스(导读 1 + 챕터 30 + 参考文献 1) → 원고 md 39件 (프론트매터 2 + 부 인트로 6 + 챕터 30 + 참고문헌 1)
- 책 두께 추정 48–58면(원문 33면 + 부 인트로 6면분 + 도면 여유 — claim 불요, §0 기록 사항)

## 1. 가정 (불확실 요소 명시)

1. ~~원문 공식 배포 URL 미확보~~ → **사용자가 공개 추적 승인**(2026-09-07). LICENSE-NOTE.md·
   ATTRIBUTION.md는 필수 산물로 승격하며, 원문 전문 스냅샷(`references/source-zh/`) 포함
   공개를 전제로 한다. ATTRIBUTION에는 중문판의 번역 귀속 가능성을 주석한다(영문 원저의
   중문 역본일 수 있음 — 확정된 정보만 표기). 표기 블록의 URL은 확보 시에만 기입한다
   (추측 URL 금지 유지).
2. 부(part) 구성 6부와 부 인트로 2–3문단은 recon 채택 결정사항. 부 인트로는 **원문에 없는
   편역자 프레이밍**이므로 "원문 보존" 범위 밖 부가물임을 각 파일에 명시하지 않는다(실례
   system-design-interview-notes-ko 동일 패턴). 다만 내용은 해당 부 챕터 범위 요약에 한정한다.
3. 번역 제목(§2 대조표)·용어(§4)는 본 계획에서 확정. 라이터 임의 변경 불가. 변경 필요 시
   Phase 4에서 이 표를 먼저 갱신한 뒤 일괄 반영한다.
4. 챕터당 1면 구성(283–586자) 유지 — 챕터 통합·분할 금지. G3 밴드는 조판 결과물이므로
   빌드 루프에서 해소한다.
5. ~~recon-vision.md 미도착~~ → **도착·반영 완료**(2026-09-07, haiku 서브 2건 전수 확인).
   §5 배정은 비전 인벤토리 기준으로 확정했다.

## 2. 수정 대상 — 생성 파일 전체 목록 (43件)

기준 디렉터리: `books/kv-cache-handbook-ko/`. 파일명 규약은 실례
`books/system-design-interview-notes-ko/` 준용(부 디렉터리 + `chNN-slug/index.md`).
**기존 파일 수정 0件 — 전부 신규 생성.** (유일한 예외 편집: 루트 `.gitignore` 1줄 추가 — §6-8)

### 2.1 설정·메타 (4件)

| 파일 | 내용 |
|---|---|
| `typst-build.yaml` | §3 전문 초안 |
| `LICENSE-NOTE.md` | 원문 무료 배포 핸드북의 2차 번역물 · 편집 산출물 KLIC 저작 · 상세 `ATTRIBUTION.md` |
| `ATTRIBUTION.md` | 원문 정보(시리즈·저자·중문 역본 귀속 가능성 주석 — §1-1) · 소스 스냅샷 `references/source-zh/` 전문 공개 · 번역 원칙(요약·삭제·임의 추가 없음) · 도면은 원본 벡터 미사용·`diagram` 펜스 재작성 · **참고문헌 원문 표기(중문 역제 포함)의 보존처** · 이용 범위 |
| `README.md` | 책 디렉터리 간단 소개(제목·원문·빌드 명령 — 수 페이지 분량) |

### 2.2 원고 (39件) — 원문↔번역 챕터 대조표 (권위 표)

부 인트로의 챕터 표는 이 표에서 해당 부 범위를 발췌하되, **원문 열은 소스 숫자 스템**
("1-01" … "30-30")으로 치환해 수록한다(원고 내 한자 금지 §6-9 — 중문 제목 열 폐지,
숫자 스템 재빌드 실험에서 qc PASS 검증). **전체 대조표는 본 표가 단일 전거다.**
원문 제목 열은 실제 면 헤더(각 소스 1행) 기준 — 파일명 스템과 6건 불일치(ch04·14·17·19·27·29).

| 소스 숫자 스템 | 원문 면 헤더(실측) | 번역 제목(확정) | 생성 파일(manuscript/) |
|---|---|---|---|
| 0-00 | 导读 | 들어가며 | `00-frontmatter/01-preface.md` |
| 1-01 | 自回归生成 | 자기회귀 생성 | `01-principles/ch01-autoregressive/index.md` |
| 2-02 | 重复计算 | 반복되는 계산 | `01-principles/ch02-recompute/index.md` |
| 3-03 | 工作机制 | 작동 메커니즘 | `01-principles/ch03-mechanism/index.md` |
| 4-04 | 每个注意力层都有自己的缓存 | 층마다의 캐시 | `01-principles/ch04-per-layer/index.md` |
| 5-05 | 预填充与解码 | 사전채움과 디코딩 | `01-principles/ch05-prefill-decode/index.md` |
| 6-06 | 逐步解码 | 한 단계씩 디코딩 | `01-principles/ch06-stepwise-decode/index.md` |
| 7-07 | 内存公式 | 메모리 공식 | `02-cost/ch07-memory-formula/index.md` |
| 8-08 | 内存计算实例 | 메모리 계산 실례 | `02-cost/ch08-memory-worked-example/index.md` |
| 9-09 | 上下文长度 | 문맥 길이 | `02-cost/ch09-context-length/index.md` |
| 10-10 | KV 缓存节省了什么 | KV 캐시가 절약하는 것 | `02-cost/ch10-what-it-saves/index.md` |
| 11-11 | 多头注意力 | 멀티 헤드 어텐션 | `03-architecture/ch11-mha/index.md` |
| 12-12 | 多查询注意力 | 멀티 쿼리 어텐션 | `03-architecture/ch12-mqa/index.md` |
| 13-13 | 分组查询注意力 | 그룹 쿼리 어텐션 | `03-architecture/ch13-gqa/index.md` |
| 14-14 | 一个公式，三种架构 | 하나의 공식, 세 가지 아키텍처 | `03-architecture/ch14-one-formula/index.md` |
| 15-15 | 多头潜在注意力 | 멀티 잠재 어텐션 | `03-architecture/ch15-mla/index.md` |
| 16-16 | 位置信息 | 위치 정보 | `03-architecture/ch16-rope/index.md` |
| 17-17 | 从单个请求到整台服务器 | 요청에서 서버까지 | `04-block-management/ch17-requests/index.md` |
| 18-18 | 碎片化 | 단편화 | `04-block-management/ch18-fragmentation/index.md` |
| 19-19 | PAGEDATTENTION(면 헤더 전체 대문자 — G5 라틴 ALL-CAPS 회피 위해 번역 제목은 PagedAttention) | PagedAttention | `04-block-management/ch19-paged-attention/index.md` |
| 20-20 | 块大小 | 블록 크기 | `04-block-management/ch20-block-size/index.md` |
| 21-21 | 前缀缓存 | 접두사 캐시 | `05-reuse-tiering-precision/ch21-prefix-cache/index.md` |
| 22-22 | 前缀缓存的局限 | 접두사 캐시의 한계 | `05-reuse-tiering-precision/ch22-prefix-limits/index.md` |
| 23-23 | 前缀缓存安全 | 접두사 캐시 보안 | `05-reuse-tiering-precision/ch23-prefix-security/index.md` |
| 24-24 | 淘汰 | 축출 | `05-reuse-tiering-precision/ch24-eviction/index.md` |
| 25-25 | 卸载 | 오프로딩 | `05-reuse-tiering-precision/ch25-offload/index.md` |
| 26-26 | KV 缓存量化 | KV 캐시 양자화 | `05-reuse-tiering-precision/ch26-quantization/index.md` |
| 27-27 | 量化并非没有代价 | 양자화의 대가 | `05-reuse-tiering-precision/ch27-quant-cost/index.md` |
| 28-28 | 常见误解 | 흔한 오해 | `06-synthesis/ch28-misconceptions/index.md` |
| 29-29 | 面向生产环境的理解框架 | 운영 환경 이해의 틀 | `06-synthesis/ch29-production-frame/index.md` |
| 30-30 | 完整的理解框架 | 완전한 이해의 틀 | `06-synthesis/ch30-full-frame/index.md` |
| 31-31 | 参考文献 | 참고문헌 | `07-backmatter/00-references.md` |

**참고문헌 장 번호 결정(명문화)** — 참고문헌은 장 번호 **31을 수용**한다(`## 제31장 — 참고문헌`,
TOC 연속). 검토된 대안 4종은 기각: 무번호 수용(TOC 점검 규칙과 배치 단순성 저해) ·
'맺음말' 라벨(evoharness 맺음말 07번 선례는 있으나 원문 성격은 문헌 목록 — 라벨 불일치) ·
'부록' 라벨(원문이 부록이 아닌 본책 말미 구성) · nonum 백매터(번호 붙임이 실측 관례).

부 인트로 6件 + 타이틀 1件 — **부 인트로는 오케스트레이터가 Phase 1에 작성**(단일 목소리 —
병렬 라이터 목소리 노출 제거, §7):

| 파일 | 제목(헤딩 `## 제N부 …` — 실험 검증: `^제\s*\d+\s*부\b` → 파트 라벨 매핑) | 담당 |
|---|---|---|
| `00-frontmatter/00-title.md` | 판권·판소 페이지 — **H1 금지, `**제목**`/`*부제*` 일반 강조 텍스트로 수록** | Phase 1 |
| `01-principles/00-part-introduction.md` | 제1부 원리 — 캐시는 왜 성립하는가 | Phase 1 |
| `02-cost/00-part-introduction.md` | 제2부 비용 — 메모리 공식과 그 영향 | Phase 1 |
| `03-architecture/00-part-introduction.md` | 제3부 아키텍처 — 헤드 구조로 비용 줄이기 | Phase 1 |
| `04-block-management/00-part-introduction.md` | 제4부 블록 관리 — 시스템 문제로서의 캐시 | Phase 1 |
| `05-reuse-tiering-precision/00-part-introduction.md` | 제5부 재사용·계층화·정밀도 | Phase 1 |
| `06-synthesis/00-part-introduction.md` | 제6부 종합 — 하나로 잇는 이해 | Phase 1 |

**프리페이스 머리 원문 표기 블록(Phase 1 — evoharness 양식, 라틴만으로 한자 금지와 양립)**

```markdown
> 원문: Understanding KV Cache — Understanding AI 시리즈 핸드북 02 · @techNmak (중문판 zh-CN)
```

URL은 확보 시에만 둘째 줄 `> 링크: …`로 추가한다(추측 URL 금지 — §1-1).

### 2.3 챕터 md 공통 스키마

```markdown
---
id: chNN
title: "<번역 제목>"
part: principles|cost|architecture|block-management|reuse-tiering-precision|synthesis|backmatter
order: N
source: "<source-zh 파일명>"
status: translated
---

## 제N장 — <번역 제목>

<원문 첫 줄 리드 질문은 ### 절 제목으로 수용 — 선택 여지 없이 고정>

…본문(### 절 · #### 소절)…

참고자료: [n], [n]
```

- 헤딩 규약: 장 제목 `## 제N장 — 제목` 1회(챕터당 — TOC "N 제N장 — …" 전개, evoharness 관례),
  절 `###`, 소절 `####`. **"CHAPTER NN" 형식 폐지·`#` 사용 금지**(H1 개면 충돌).
- 참고문헌 파일(`07-backmatter/00-references.md`)도 같은 스키마를 쓴다(id: ch31, order: 31,
  part: backmatter) — 리드줄 "주요 논문과 현행 구현 자료" 수록, 말미 @techNmak 크레딧 유지(라틴 — 무해).
- 장 말미 `참고자료: [n], …` 1행 — 원문 식별자 전수·순서 보존(프리페이스 포함 31개 파일).
- 중앙 강조줄(§5.3의 5건)은 blockquote `>` 1줄로 수록(빌드가 `#quote` 렌더) — ch30만 `$$` 블록.
- 챕터 md 내 이미지 없음(도식은 ```diagram 펜스 — 빌드가 SVG 생성).

## 3. 인터페이스 — typst-build.yaml 전문 초안

```yaml
style: practical
title: "KV 캐시의 이해"
short_title: "KV 캐시의 이해"   # 러닝헤드 — 미지정 시 제목 첫 단어 "KV" 2글자 낙점 방지
subtitle: "자기회귀 디코딩에서 최신 대규모 언어모델 추론까지 — Understanding AI 핸드북 02 한국어판"
author: "원문 techNmak · 한국어판 KLIC"
date: "2026-09"
cover: auto                  # 골격 5종(V1–V5) — 변형은 cover_variant로 지정
cover_variant: 5             # 위계 격자형 명시 지정 — composition 프로파일 전축 반영(V1–V4는
                             # 해시 분배 순환이며 V2/V3는 composition 미반영 경고 있음. evoharness 동일 계약)
cover_composition: true
opener_composition: true
cover_series: "KLIC BOOKS"
cover_notes:
  - "· 원리 → 비용 → 아키텍처 → 블록 관리 → 재사용·정밀도 → 종합"
  - "· Understanding AI 핸드북 02 한국어판"
chapters:
  - manuscript/00-frontmatter/00-title.md
  - manuscript/00-frontmatter/01-preface.md
  - manuscript/01-principles/00-part-introduction.md
  - manuscript/01-principles/ch01-autoregressive/index.md
  - manuscript/01-principles/ch02-recompute/index.md
  - manuscript/01-principles/ch03-mechanism/index.md
  - manuscript/01-principles/ch04-per-layer/index.md
  - manuscript/01-principles/ch05-prefill-decode/index.md
  - manuscript/01-principles/ch06-stepwise-decode/index.md
  - manuscript/02-cost/00-part-introduction.md
  - manuscript/02-cost/ch07-memory-formula/index.md
  - manuscript/02-cost/ch08-memory-worked-example/index.md
  - manuscript/02-cost/ch09-context-length/index.md
  - manuscript/02-cost/ch10-what-it-saves/index.md
  - manuscript/03-architecture/00-part-introduction.md
  - manuscript/03-architecture/ch11-mha/index.md
  - manuscript/03-architecture/ch12-mqa/index.md
  - manuscript/03-architecture/ch13-gqa/index.md
  - manuscript/03-architecture/ch14-one-formula/index.md
  - manuscript/03-architecture/ch15-mla/index.md
  - manuscript/03-architecture/ch16-rope/index.md
  - manuscript/04-block-management/00-part-introduction.md
  - manuscript/04-block-management/ch17-requests/index.md
  - manuscript/04-block-management/ch18-fragmentation/index.md
  - manuscript/04-block-management/ch19-paged-attention/index.md
  - manuscript/04-block-management/ch20-block-size/index.md
  - manuscript/05-reuse-tiering-precision/00-part-introduction.md
  - manuscript/05-reuse-tiering-precision/ch21-prefix-cache/index.md
  - manuscript/05-reuse-tiering-precision/ch22-prefix-limits/index.md
  - manuscript/05-reuse-tiering-precision/ch23-prefix-security/index.md
  - manuscript/05-reuse-tiering-precision/ch24-eviction/index.md
  - manuscript/05-reuse-tiering-precision/ch25-offload/index.md
  - manuscript/05-reuse-tiering-precision/ch26-quantization/index.md
  - manuscript/05-reuse-tiering-precision/ch27-quant-cost/index.md
  - manuscript/06-synthesis/00-part-introduction.md
  - manuscript/06-synthesis/ch28-misconceptions/index.md
  - manuscript/06-synthesis/ch29-production-frame/index.md
  - manuscript/06-synthesis/ch30-full-frame/index.md
  - manuscript/07-backmatter/00-references.md
```

(chapters 순서 = 책 순서 39항목. cover: auto + `cover_variant: 5` 명시 — composition 경고 준수.)

## 4. 용어 계약 (병렬 라이터 일관성 — 어긋 시 Phase 4 반려)

| 원문 | 번역(확정) | 비고 |
|---|---|---|
| KV 缓存 | KV 캐시 | |
| 自回归 | 자기회귀 | |
| 预填充 | 사전채움 | 첫 등장 "사전채움(prefill)" 병기 |
| 解码 / 解码器 | 디코딩 / 디코더 | |
| 多头/多查询/分组查询/多头潜在注意力 | 멀티 헤드 어텐션(MHA) / 멀티 쿼리 어텐션(MQA) / 그룹 쿼리 어텐션(GQA) / 멀티 잠재 어텐션(MLA) | 약자 병기 |
| 查询/键/值 | 쿼리/키/값 | Q·K·V 기호는 원문대로 |
| 头 / 头维度 | 헤드 / 헤드 차원 | |
| 层 | 층 | "transformer 층" — 첫 등장 "층(layer)" 병기 |
| 上下文长度 | 문맥 길이 | |
| 大语言模型 | 대규모 언어모델 | 첫 등장 "(LLM)" 병기 |
| 推理 | 추론 | inference |
| 张量 | 텐서 | |
| 序列 | 시퀀스 | |
| 前缀缓存 | 접두사 캐시 | 첫 등장 "(prefix cache)" 병기 |
| 淘汰 | 축출 | eviction |
| 卸载 | 오프로딩 | offloading |
| 量化 | 양자화 | quantization |
| 碎片化 | 단편화 | fragmentation |
| 块 / 块表 | 블록 / 블록 테이블 | PagedAttention 용어 |
| 旋转位置嵌入 | 회전 위치 임베딩(RoPE) | |
| 参考文献 / 参考资料 | 참고문헌 / 참고자료 | |
| 已缓存 / 新增 | 캐시됨 / 신규 | ch06 도면 라벨 |
| 逻辑序列 / 物理缓存 | 논리 시퀀스 / 물리 캐시 | ch19 도면 라벨 |
| 空闲 | 빈 블록 | ch19 물리 캐시 칸 |
| 块表映射 | 블록 테이블 매핑 | ch19 캡션 줄 |
| 稠密注意力 | 밀집 어텐션 | dense attention |
| 因果掩码 | 인과 마스크 | causal mask |
| 分片 | 샤딩 | sharding |

**부속 계약 (표 밖 — 라이터 공통)**

- **번역 등록: 한다체(평서 문어체)** — 전서 실측 관례. "~한다/~이다" 종결, 구어체·존칭 금지.
- **LaTeX 정규형**: 첨자 기호는 `M_{KV}`·`H_{KV}`·`D_h` 표기로 전서 통일(§5.4 수식 12건·§10 C9 기준).
- **도면 글리프 범위**: 상용첨자는 U+00B9(¹)·U+2081–2084(₁₂₃₄) 범위만 — 괄호 상첨(⁽¹⁾)은
  폰트 미지원 실측으로 금지. ⋮(U+22EE) 금지 — 생략 표현은 '…' 라벨 dash 노드(§5.1 ch04).

## 5. 도식·표·강조줄 계획 (recon-vision 반영 확정)

저작 규약 `skills/korean-ebook/references/diagram-authoring.md` 준수. 근거 경계: 본문이 말한
구조만 재배치(라벨·관계 추가 금지). **원본 그래픽은 흑백 박스·무채움·가는 실선 화살표** —
diagram 펜스 `tone` 규약 안에서 절제된 채색만 허용한다(기본 무채색, 의미 구분이 필요한
최소 위치에만 blue/green/red — 장식 채움 금지).

### 5.1 diagram 펜스 — 도면 5개 장·펜스 7건 (v5: scene 엣지 결함 완전 회피)

**엣지는 flow 테두리간 연결에서만 안전(실측)** — scene 배정 도면은 전부 **무엣지**로 설계하고,
flow 2건(ch01·ch06)만 엣지를 쓴다(박스 테두리간 연결 — 라벨 충돌 없음, 코드 검증).

| 챕터 | 원본 구조(p면) | layout | 설계 계약 |
|---|---|---|---|
| ch01 (p3) | 가로 순서도 4박스: 프롬프트→사전채움→디코딩→디코딩 | `flow` 4노드(세로) | 순차 — 엣지 3건, 테두리간 안전 |
| ch04 (p6) | 세로 스택: 제1층 / 제2층 / ⋮ / 제L층 | `scene` **무엣지** | 3박스 + 생략 '…' dash 노드. 라벨 "1층 K¹, V¹" 등 U+00B9 범위(§4 부속 — 괄호 상첨·⋮ 금지) |
| ch06 (p8) | 합류형: 캐시됨 K₁:₃, V₁:₃ + 신규 k₄, v₄ → K₁:₄, V₁:₄ | `flow` 3노드 | 합류의 순차 재해석 — [캐시됨 K₁:₃, V₁:₃] → [신규 k₄, v₄ 추가] → [K₁:₄, V₁:₄]. 본문 절차 목록과 정합 |
| ch14 (p16) | MHA/GQA/MQA 3그룹: Q박스 → KV박스(4/2/1개, 폭 증가) | `scene` **×3 세로 스택, 무엣지 인접성** | 그룹당 노드 8/6/5(단일 scene 상한 12 초과 → 펜스 3개). Q박스를 대응 KV박스 **바로 위** 배치, KV 폭 확장(4/2/1)+tone으로 공유 표현, **화살표 폐지**(부채꼴 적층 결함 회피) |
| ch19 (p21) | 좌우 2그룹: 논리 시퀀스 [B0][B1][B2][B3] vs 물리 캐시 [B2][빈][B0][B3][빈][B1] | `scene` **무엣지** | 10박스. 그룹 라벨은 행 첫 박스 `sub` 또는 gray dash 박스. 매핑 캡션 "블록 테이블 매핑: B0 → 2, B1 → 5, B2 → 0, B3 → 3"은 본문 줄로 유지 |

11장(p13) 헤드 격자(3행×6열 Q/K/V)는 **scene 노드 상한 12 초과 → diagram 펜스 불가,
마크다운 표로 변환**한다(§5.2 표 5건 참조).

**도면 렌더 비전 확인 1회 편성(Phase 3)** — 5개 도면의 렌더 PNG를 비전 서브에이전트가
확인한다. lint는 기하·겹침을 검출하지 못함(실험 실측) — 렌더 결과 육안 확인이 유일한
기하 검증 수단이다.

### 5.2 마크다운 표 — 5건 (booktabs 렌더)

| 챕터 | 내용 | 수치(Never-cut) |
|---|---|---|
| ch05 (p7) | 사전채움 vs 디코딩 비교 | 1열 라벨 × 4행 |
| ch08 (p10) | 아키텍처별 H_KV · KiB/token · 8,192토큰(GiB) | MHA 32/512/4.000 · GQA(예시) 8/128/1.000 · MQA 1/16/0.125 · 검산식 `2·32·8192·8·128·2 = 1,073,741,824 bytes = 1 GiB` |
| ch09 (p11) | 아키텍처 × 문맥길이 8K/32K/128K (GiB) | MHA 4/16/64 · GQA 1/4/16 · MQA 0.125/0.5/2 |
| ch11 (p13) | MHA 헤드 정렬 격자 Q₁..Q₆/K₁..K₆/V₁..V₆ | 3행 × 6열 — 도면의 표 변환분 |
| ch13 (p15) | MHA/GQA/MQA 헤드 구조 비교 | 쿼리 헤드 · KV 헤드 · KV 공유 |

### 5.3 중앙 강조줄 — 5건 (blockquote `>` → #quote 렌더)

| 챕터 | 강조줄 |
|---|---|
| ch20 (p22) | 논리 토큰 이력 ≠ 하나의 연속된 물리 메모리 |
| ch23 (p25) | 캐시 재사용 범위는 신뢰 범위와 일치해야 한다 |
| ch25 (p27) | GPU HBM ↔ CPU 메모리 ↔ 2차 저장/네트워크 계층 (계층 체인) |
| ch27 (p29) | 절감하는 메모리/대역폭과 품질·커널 비용의 균형 |
| ch30 (p32) | 수식 2LTH_KV D_h b — **mitex `$$` 블록**으로 수록(일반 blockquote 아님) |

### 5.4 수식 — 12건

recon 목록(ch01,02,03,04,07,08,09,11,12,13,14,30)은 LaTeX 변환 후 `$$` 블록 사용
(인라인 `$...$` 한국어 \text 혼재 깨짐 회피 — SKILL.md 한계). 검산 수치는 §5.2 표 참조.

나머지 면은 전부 텍스트 전용(recon-vision §텍스트 전용 면 참조) — 원문 표지(p1)는
자동 표지로 대체, 오해 Q&A(p30)는 콜아웃 아닌 본문 반복 구조 유지.

## 6. 보존 제약 (③구현 프롬프트에 verbatim 복사)

1. **엔진·스킬 스크립트·기존 책 무변경** — `skills/`, `books/` 기존 디렉터리, 엔진 파일 일절
   수정 금지. 본 과업의 생성물은 `books/kv-cache-handbook-ko/` 신규 파일과
   `docs/task-id/kv-cache-handbook/` 문서로 한정한다.
2. **원문 전량 수록** — 원문 30챕터 + 导读(들어가며) + 참고문헌 [1]–[11] 전량을 누락 없이
   수록한다. 요약·삭제·임의 추가 금지(마크다운 구조 변환만 허용).
3. **원문의 한정·주의 문장 완화 금지** — "논문이 보고한 특정 결과임", "일반적인 보장이 아님",
   "공식은 이상적 데이터량이며 런타임 전체 소비량이 아님" 류의 한정 표현은 번역 후에도
   동등한 강도로 유지한다.
4. **수치·식별자 Never-cut** — 모든 숫자·단위·arXiv ID·DOI·버전·KiB/GiB·8K/32K/128K·
   블록 크기 등은 글자수 밴드(G3)를 맞추려고 자르지 않는다. 참고문헌 식별자 전수 보존.
5. **장마다 `참고자료: [n], …` 행 보존** — 원문 参考资料 행의 식별자 전수·순서 유지(31개 파일).
6. **korean-style.md 라이터 계약 준수** — 납품 전 자기 리비전 포함, G4 0건 목표.
7. **`references/source-zh/` 원문 무변경** — 대조 교정은 번역문만 수정한다.
8. **빌드 산물 git 커밋 금지** — `build/`, `draft/`, `final/`, `gate-report.json`,
   `manuscript/<part>/assets/diagrams/`(diagram SVG 실제 생성처)은 파이프라인 생성물.
   루트 `.gitignore`에 `books/kv-cache-handbook-ko/manuscript/*/assets/` 1줄을 추가한다
   (Phase 1 오케스트레이터 실행 — 저장소 설정 변경은 엔진 밖, §10 C11 허용 범위).
9. **원고 내 한자·전각문호 전면 금지** — G2 폰트 계약 위반(CRITICAL) 예방.
   `grep -rnP '[\x{4E00}-\x{9FFF}\x{FF01}-\x{FF5E}\x{3001}\x{3002}\x{300A}\x{300B}]' manuscript/`
   → 0건. 부 인트로 대조표 원문 열도 숫자 스템으로 수록(§2.2).
10. **참고문헌 중문 역제(《…》) 제외** — 참고문헌 항목은 원제(영문)·저자·식별자만 수록한다.
    중문 역제를 포함한 원문 표기는 ATTRIBUTION.md가 보존한다(§6-9와 동일 근거).

## 7. 파일 소유권·라이터 분할 (병렬 스폰 3명 — implement-med, R3 문체 일관성)

**5→3 재분배(적대검토 R3)** — 문체 일관성(등록·리듬·접속)을 위해 담당 경계를 넓게 잡는다.
파트 디렉터리 단위 소유권 유지(동일 파일 동시 편집 0건). 부 인트로 6件은 라이터 배정에서
제외 — 오케스트레이터가 Phase 1에 작성한다(§2.2).

| 라이터 | 소유 디렉터리 | 챕터 | 도면·표·강조줄·수식 부하 (v5) |
|---|---|---|---|
| W1 | `01-principles` + `02-cost` | ch01–10 (10件) | 도면 3 펜스(ch01 flow · ch04 scene 무엣지 · ch06 flow) · 표 3(ch05·08·09) · 수식 ch01–04·07–09 |
| W2 | `03-architecture` + `04-block-management` | ch11–20 (10件) | 도면 4 펜스(ch14 scene×3 무엣지 · ch19 scene 무엣지) · 표 2(ch11 격자 변환·ch13) · 강조줄 1(ch20) · 수식 ch11–14 |
| W3 | `05-reuse-tiering-precision` + `06-synthesis` + `07-backmatter` | ch21–31 (11件) | 강조줄 4(ch23·25·27·30 — ch30 `$$` 블록) · 참고문헌 11건(중문 역제 제외 — §6-10) |

### 7.1 라이터 프롬프트 템플릿 (각 스폰에 포함할 요소)

1. **역할**: 한국어판 번역 라이터 — korean-ebook 원고 납품.
2. **소스**: 배정 챕터의 `books/kv-cache-handbook-ko/references/source-zh/<파일명>` 경로 목록
   (§2.2 대조표에서 해당 행만 발췌해 전달 — 원문 면 헤더 열 포함).
3. **문체 계약**: `skills/korean-ebook/docs/korean-style.md` 경로 — 납품 전 자기 리비전 의무,
   G4 텔 자가 점검 후 납입. **등록은 한다체(평서 문어체) 고정(§4 부속).**
4. **산출 경로·스키마**: §2.3 프론트매터+헤딩 규약(`## 제N장 — 제목`, `#` 금지,
   리드 질문 `###` 절 제목 수용 고정).
5. **용어 계약**: §4 표+부속(LaTeX 정규형·도면 글리프 범위) verbatim 전달.
6. **도면**: `references/diagram-authoring.md` 경로 + 배정 layout·펜스 수·설계 계약(§5.1) —
   노드 라벨은 원문 도표 라벨의 번역만, 구조 추가 금지. tone 절제 원칙(기본 무채색,
   의미 구분 최소 채색). lint 명령: `python3 skills/korean-ebook/scripts/diagram.py lint <md>`.
7. **표·강조줄·수식**: 마크다운 표(§5.2 수치 Never-cut) / 강조줄 blockquote 1줄(§5.3) /
   `$$` 블록 LaTeX(인라인 자제, 정규형 준수).
8. **보존 제약**: §6 전항 verbatim(한자·전각 금지 포함).
9. **납품 노트**: 고치지 못한 G4 텔·번역 선택 이유·원문 불명확 부분과 함께 **원문 대조
   셀프체크 결과(소스별 누락·수치·한정문 점검 서술)**를 포함해 보고(파일 아님).

## 8. Phase 분해 (의존관계 순)

| Phase | 내용 | 파일 | 검증 | 의존 |
|---|---|---|---|---|
| 1 | 스캐폴드+프론트매터+부 인트로+설정 | 12件 (yaml·LICENSE·ATTRIBUTION·README·title·preface·부 인트로 6) + `.gitignore` 1줄 편집 | yaml 파싱 통과 · preface 원문 표기 블록(§2.2 양식)·불릿 6·선수지식·참고자료 [1][2][5][6] 대조 · 부 인트로 6건 `## 제N부` 헤딩+스템 대조표(C8 형식) | — |
| 2 | 번역 라이터 3인 병렬 스폰 (W1·W2·W3 — §7) | 30件 (챕터+참고문헌) | 납품 보고(원문 대조 셀프체크 서술 포함 — §7.1-9) + 각 파일 존재 + `## 제N장` 헤딩 1회씩 · **미납 시 10분 워치독 → 동일 역할 1회 재스폰** | Phase 1 — 라이터 상호 무의존 |
| 3 | 도면·표·강조줄·수식 검증 | 0件 (수정만) | `diagram.py lint` 펜스 7건 전 통과 · **도면 렌더 PNG 비전 서브 확인 1회(§5.1)** · 표 5건 형식·수치 원문 대조(§5.2) · 강조줄 5건 blockquote/$$ 수용 확인 · 수식 12건 LaTeX 원문 대조 | Phase 2 |
| 4 | 대조 교정+문체 패스 | 1件 (`docs/task-id/kv-cache-handbook/crosscheck.md`) | 32 소스 ↔ 번역 1:1 대조 — 문장 누락·한정문 완화·식별자·용어 점검 기록 **crosscheck.md 32행** 산출 · 문체 패스(등록·리듬·접속+용어 grep 통일 점검) | Phase 3 |
| 5 | 빌드·QC 루프 | 0件 (수정만) | build.py 성공 → **종료 조건: G1·G2 PASS + G3 0건 + G4 0건**. 우선순위 계약: **수치·식별자·한정문 보존 > 밴드·텔 0건** — 0건화는 문장 재구성으로만 해소하고 절삭·완화 금지 → final/ 생성 | Phase 4 |
| 6 | 리뷰·커밋·푸시 | 0件 | §10 claims 전량 실행·증거 확보 → 커밋 1건 `feat: kv-cache-handbook 한국어판 제작 — 원문 30장 번역·도면 5종·표 5종` → **사용자에게 결과 보고 후 푸시**(§11) | Phase 5 |

Phase 2는 라이터 배치 단위로 독립 검증 가능(W1·W2·W3 각 10~11件 — 각 배치가
스폰→보고→파일 존재 확인으로 닫힌다).

## 9. 위험 지점과 검증 방법

| 위험 | 영향 | 완화·검증 |
|---|---|---|
| 병렬 라이터 용어·제목 불일치 | 전서 일관성 훼손 | §4 용어 계약+§2.2 권위 표 verbatim 전달 · Phase 4 용어 통일 grep 점검 · 3라이터 재구조로 목소리 경계 축소(R3) |
| 중문 직역 번역투 → G4 경고 | QC 지연 | korean-style 자기 리비전 의무 · Phase 5 게이트 루프에서 0건화. 원문 '~ 아니라' 대조 구조는 ≤1회 사용(실측) — 빈도 한도 내 |
| 원고 내 한자·전각 잔입 | G2 폰트 계약 위반(CRITICAL 재발) | §6-9 계약 · C13 grep 검증(라이터 납품 직후 + Phase 5 매 루프) |
| 수식 mitex 변환 실패(인라인 한국어) | 빌드 실패 | `$$` 블록 강제 · Phase 3 LaTeX 대조 · 빌드 성공이 증거 |
| 도면 I1 린트 실패(텍스트 예산)·렌더 기하 결함 | 빌드 실패·품질 저하 | 라이터 lint 개별 실행 · Phase 3 전수 lint + **렌더 PNG 비전 확인 1회**(lint는 기하 미검출 — 실측) |
| 원문 누락·참고자료 누락 | 보존 제약 위반 | claims C4·C7·C12 grep 검증 |
| 한정 문장 완화(번역 매끄럽게 하려다) | 원문 왜곡 | §6-3 명시 + Phase 4 대조 교정 crosscheck.md 전수 점검 |
| G5 — 판독불능 표기·HTML 주석 잔여 | WARN | HTML 주석 금지 · 원문 '第N장' 교차언급 0건(실측) — 검사 항목에서 제외 |
| 라이터 미납·이탈 | Phase 2 지연 | 10분 워치독 → 동일 역할 1회 재스폰(2회째 실패 시 오케스트레이터가 직접 수용) |
| 소스 오염(references/source-zh 수정) | 대조 기준 상실 | §6-7 금지 + C11 diff 검증 |

## 10. 검증 요구 claims (구현 완료 후 리뷰가 실행)

| # | claim | evidence 명령 |
|---|---|---|
| C1 | 빌드 성공 — draft PDF 생성 | `python3 skills/korean-ebook/scripts/build.py books/kv-cache-handbook-ko` 종료 0 + `ls books/kv-cache-handbook-ko/draft/*.pdf` |
| C2 | QC PASS — final 생성(G1·G2 무위반) | `python3 skills/korean-ebook/scripts/qc_gate.py books/kv-cache-handbook-ko` PASS 출력 + `ls books/kv-cache-handbook-ko/final/` |
| C3 | 원고 파일 수 39 | `find books/kv-cache-handbook-ko/manuscript -name '*.md' \| wc -l` → 39 |
| C4 | 참고문헌 [1]–[11] 전량 | `grep -c '^\[' books/kv-cache-handbook-ko/manuscript/07-backmatter/00-references.md` → 11 |
| C5 | G4 경고 0건 | qc_gate 출력(또는 `gate-report.json`)의 G4 count → 0 |
| C6 | 도면 lint 전 통과 + 펜스 수 7건 | 도면 포함 md 5개(ch01·04·06·14·19) 각각 `python3 skills/korean-ebook/scripts/diagram.py lint books/kv-cache-handbook-ko/manuscript/<파일>` 통과 + ``grep -rc '```diagram' <5개 md>`` 합계 → 7 |
| C7 | 참고자료 행 31개 파일 전수 | `grep -rL '참고자료' books/kv-cache-handbook-ko/manuscript/00-frontmatter/01-preface.md books/kv-cache-handbook-ko/manuscript/0[1-6]-*/ch*/index.md` → 출력 없음 |
| C8 | 부 인트로 대조표 6件 존재(스템 열) | `grep -l '^\| 챕터' books/kv-cache-handbook-ko/manuscript/0[1-6]-*/00-part-introduction.md \| wc -l` → 6 |
| C9 | 핵심 수식·수치 Never-cut(정규형 준수) | `grep -c 'M_{KV}' <ch07> <ch30>` 각 ≥1 && `grep -q '1,073,741,824' <ch08>` && `grep -q '128K' <ch09>` → 참. 첨자 표기는 `M_{KV}`·`H_{KV}`·`D_h` 정규형(§4 부속) |
| C10 | 중앙 강조줄 5件 수록 | `grep -c '^> ' <ch20> <ch23> <ch25> <ch27>` 각 ≥1 && `grep -q '\$\$' <ch30>` → 참 |
| C11 | 원문·엔진·기존 책 무변경 | `git diff --name-only <base>..HEAD` — 변경이 `books/kv-cache-handbook-ko/**`, `docs/task-id/kv-cache-handbook/**`, 루트 `.gitignore`(§6-8의 1줄) 범위 내 (스킬·source-zh·타책 제외) |
| C12 | 원문 챕터 1:1 대응 | `grep -h '^source:' books/kv-cache-handbook-ko/manuscript/0[1-6]-*/ch*/index.md \| wc -l` → 30 (§2.2 표와 대조) |
| C13 | 원고 내 한자·전각문호 0건 | `grep -rnP '[\x{4E00}-\x{9FFF}\x{FF01}-\x{FF5E}\x{3001}\x{3002}\x{300A}\x{300B}]' books/kv-cache-handbook-ko/manuscript/` → 출력 없음 |
| C14 | 대조 기록 crosscheck.md 32행 | `wc -l docs/task-id/kv-cache-handbook/crosscheck.md` → 32 (32 소스 각 1행 — Phase 4 산출) |

## 11. 롤백 가능성 판단

**커밋까지 가역 — 신규 파일만 생성하므로** `git clean`/커밋 revert로 무잔여 복원된다
(기존 파일 수정은 `.gitignore` 1줄뿐). 빌드 산물(`build/`·`draft/`·`final/`·
`gate-report.json`·`manuscript/*/assets/diagrams/`)은 파이프라인 재생성분이라 커밋에서
제외하면 롤백 대상도 없다. **푸시 후에는 비가역** — 공개 추적은 사용자 승인(§1-1)으로
진행하되, Phase 6의 커밋·푸시는 사용자에게 결과를 보고한 뒤 실행한다.
