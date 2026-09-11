# guardrails-book ①계획 번들 (plan)

- 과제: arXiv 2604.01483v1 (Type-Checked Compliance / Lean-Agent Protocol) 정독 + 한국 IT 각색 논문 8편 수록 A4 전자책
- 저장소: `/mnt/d/DEV/acc0mplish/KLIC-BOOK` · 엔진: korean-ebook 스킬(typst, style=lecture)
- 계획 작성: plan-high · 작성일 2026-09-11
- 실행 계약: `docs/task-id/guardrails-book/briefs/batch-a.md` ~ `batch-e.md`(재작성 금지 — 본 계획은 검증·보완만)
- 산출물 총괄: 책 15원고 + `typst-build.yaml` + QC PASS PDF

---

## 1. 구조 검증

### 1.1 커버리지 맵 — 원문 §1–§7 ↔ 15장

| 원문 절 | 내용 | 담당 장 | 비고 |
|---|---|---|---|
| §1 서론 | 확률적 에이전트 vs 결정론적 규제 | 01 | 도입 훅(Knight Capital) 포함 |
| §1 + §5.1 | 가드레일 3계보 | 02 | 비교표 1개 |
| §2.1 (배경) | 형식 검증·Lean 4·CIC·Mathlib·sorry·Lean4Lean | 03 | 각색 확장 장(각색 명시 의무) |
| §2.1–2.2 | Aristotle 구조·IMO 2025·자동 형식화·자기수리 | 04 | 수열 혼동 사례·환각 컴플라이언스 중화 |
| §2.3 | 승인 루프(비동기 구성/동기 5단계·State A/B) | 05 | diagram(approval) |
| §2.4 | 지연 논증 — Cedar 5μs/Rust 7μs·grind·SMT | 05 | 05에 병합(적절) |
| §3.1 | SEC 15c3-5·전속 통제·hard guardrail | 06 | 한국 각색 절 포함 |
| §3.2 | OCC 2011-12(MRM)·FINRA 3110·24-09 | 06 | 06에 병합(적절) |
| §3.3 | 설명할 권리·역방향 형식화·Herald·NL2Lean | 07 | |
| §4.1 | 치명적 삼각·형식 기법·침해 가정 | 08 | |
| §4.2.1–4.2.3 | 논리적 탈옥·형식화 드리프트·MenTaL 완화 | 08 | |
| §4.3 | Docker 결함·WASM 3대 보장·WASI | 08 | diagram(layers) |
| §5.1 | NeMo·Guardrails AI 상세 비교 | 09 | 02와 역할 분리 — 아래 1.3 참조 |
| §5.2 | Cedar forbid>permit·AMM 형식화·해머 사건 | 09 | diagram(matrix) |
| §6.1–6.3 | 3단계 로드맵(그림자→Beta→Production) | 14 | diagram(roadmap) |
| §7 결론 | 근본 비양립 해소·규제 매핑 회수 | 14 | |
| 각색(원문 외) | 전자정부·CMS/PMS/Slack·UI·언어 계층 | 10–13 | 논문집 장머리 출처 표기 |
| References | 인용 목록 | (전 장) | 스킬 규약상 출처는 인쇄물 본문에 내장 — 별도 장 불필요 |

### 1.2 판정 — **구조 결함 없음**

- 원문 §1–§7 전 절이 15장 중 하나 이상에 배정됐고, 누락 § 없음(§2.4가 05에, §3.2가 06에 병합된 것은 같은 주제 선상 병합으로 적절).
- 각색 장(10–13)이 원문 파트(01–09)와 결론(14) 사이에 끼는 배치는 결론 장 14의 마지막 절 '한국 독자를 위한 총정리'(브리프 batch-c — 10~13장 회수)와 정합. 재배치 사유 성립.
- 분량 배분: 배치당 파일 수 A=3·B=3·C=4·D=2·E=2 — 스폰 균형 양호(C가 최대 4로 5파일 이내).

### 1.3 구조 노트 2건 (결함 아님 — 관리 항목)

1. **§5.1 이중 커버(02·09)** — 브리프가 역할 분리함(02=계보·비교표 중심 / 09=NeMo·Guardrails AI 상세·Cedar·DeFi·사건 사회학). 집필 시 이 경계를 지키는지 ③조립 단계에서 메인이 스폿 체크.
2. **책 순서 가정(중요)** — 구조 목록의 나열 순서는 배치(A~E) grouping이며 책 순서가 아니다. **책 순서 = 파일번호 오름차순 00→14**로 판단한다. 근거: (a) 14장 '총정리'가 10~13장을 회수하므로 14가 마지막이어야 함 (b) 09(§5)가 08(§4) 뒤에 오는 것이 원문 순서 (c) 나열 순서 해석 시 §2→§5→§3으로 원문 순서가 붕괴하고 결론이 각색 앞에 놓이는 모순. → `typst-build.yaml`의 `chapters:`는 `manuscript/00-...`부터 `manuscript/14-...`까지 오름차순 나열(스킬 규약: 목록 순서가 책 순서). 메인 세션이 yaml 작성 시 이 가정을 확정한다. 만약 다른 의도라면 원고 파일 변경 없이 yaml 순서만 고치면 된다(저비용 수정).

---

## 2. 변경 파일 목록 (전체 과업 기준)

| 경로 | 구분 | 변경 요약 | 담당 |
|---|---|---|---|
| `docs/task-id/guardrails-book/plan.md` | 신규 | 본 계획 번들 | ①계획(완료) |
| `books/lean-guardrails-ko/manuscript/00-들어가며.md` | 신규 | 원문 인용 블록(단일 논문 규약) + 책 읽는 법·파트 안내 | 메인 |
| `books/lean-guardrails-ko/manuscript/01-위기의-정체.md` ~ `03-Lean-4의-문법.md` | 신규 | 배치 A(3파일) | implement-med A |
| `books/lean-guardrails-ko/manuscript/04-Aristotle와-자동-형식화.md`·`05-결정론적-승인-루프.md`·`09-시장과-선례.md` | 신규 | 배치 B(3파일, 05·09 diagram) | implement-med B |
| `books/lean-guardrails-ko/manuscript/06-규제-매핑-한국-금융으로.md`·`07-설명할-권리와-역방향-형식화.md`·`08-공격-표면과-WASM-샌드박스.md`·`14-로드맵과-결론.md` | 신규 | 배치 C(4파일, 08·14 diagram) | implement-med C |
| `books/lean-guardrails-ko/manuscript/10-전자정부프레임워크의-가드레일.md`·`11-CMS-PMS-Slack의-가드레일.md` | 신규 | 배치 D(2파일, 11 diagram 권장, 장머리 출처 표기) | implement-med D |
| `books/lean-guardrails-ko/manuscript/12-Flutter-React-Native-TypeScript.md`·`13-Rust-Go-Python.md` | 신규 | 배치 E(2파일, 장머리 출처 표기) | implement-med E |
| `books/lean-guardrails-ko/typst-build.yaml` | 신규 | style=lecture·chapters 00→14 오름차순·cover 옵션 | 메인 |
| `docs/task-id/guardrails-book/state.json` | 갱신 | claims evidence·phase·round (메인 단일 writer) | 메인 |
| `build/`·`draft/`·`final/`·`gate-report.json` | 생성 | 빌드 산물(gitignore — 추적 대상 아님) | Phase 2 |

`docs/task-id/guardrails-book/briefs/*`·`sources/*`는 읽기 전용(계약·소스 — 변경 금지).

---

## 3. Phase 분해 (의존관계 포함)

### Phase 1 — 원고 집필 (병렬)

- **1A 선행(메인, 즉시)**: `books/lean-guardrails-ko/typst-build.yaml` 작성(style=lecture, chapters 00→14 오름차순 — 가정 1.3-2 확정 지점). 원고 유무와 무관하므로 병렬 스폰과 독립.
- **1B 메인 직접**: `00-들어가며.md` — 장 제목 `##`, 첫 머리 단일 논문 인용 블록(원문·링크·코드 행 — arXiv 2604.01483v1·github.com/arkanemystic/lean-agent-protocol), 책 읽는 법(파트 1 원문 정독 01–09 / 파트 2 한국 각색 10–13 / 결론 14), 3,000~4,200자.
- **1C 병렬 스폰 ×5 (implement-med)**: 배치 A~E — 브리프 파일이 각 스폰의 유일 계약. 파일 집합이 서로소(경합 0).
- 각 스폰 지시에 공통 첨부: (1) 브리프 경로 (2) 원문 소스 경로 (3) `skills/korean-ebook/SKILL.md` 헤딩 규약 (4) diagram 장 스폰은 `skills/korean-ebook/references/diagram-authoring.md` 선독 (5) 아래 §4 보존 제약 verbatim (6) 완료 보고 형식(브리프 각 꼬리 절).
- **완료 판정**: 15개 원고 파일 존재 + 각 배치 완료 보고 접수(grep `^## `=1·`^# `=0·wc -m·diagram 펜스·논문 실물 확인 내역). 빌드는 아직 아님.

### Phase 2 — 조립·빌드·QC 게이트 (메인, Phase 1 전체 완료 후)

1. `python3 skills/korean-ebook/scripts/build.py books/lean-guardrails-ko` → draft PDF.
2. `python3 skills/korean-ebook/scripts/qc_gate.py books/lean-guardrails-ko` → G1~G5 판정.
3. `gate-report.json` 기반 지적 면만 수정 → 1~2 재빌드 루프(다이어그램 개별 선검증: `python3 skills/korean-ebook/scripts/infographic/cli.py lint`).
- **완료 판정**: G1·G2 무위반 PASS, `books/lean-guardrails-ko/final/` PDF 생성. G3~G5 WARN은 잔여분을 보고서로 명시(claim 6).

### Phase 3 — ②적대 팬아웃·수정 (원고 완성 후)

- plan-adversary-xhigh 3렌즈 — **GLM 심층 동시 상한 1이므로 직렬 스폰**. 렌즈 제안: (i) 원문 충실도 렌즈(수치·주장 왜곡·누락) (ii) 규약·빌드 렌즈(헤딩·도식·G3/G4 리스크 문장) (iii) 구성·서사 렌즈(02↔09 중복·장 간 연결·각색 명시 누락).
- 판정된 수정은 구현 역할(implement-med 또는 메인)로 복귀해 반영 → 파일이 바뀌면 Phase 2 재실행(재빌드·재게이트).
- **완료 판정**: 렌즈별 판정 보고 접수 + 수정 반영 diff + (변경 시) 재게이트 PASS.

### Phase 4 — ④리뷰·검증 (claims 주입)

- review-pr-xhigh 1스폰 — §5의 claims 목록을 프롬프트에 주입, 각 claim별 검증 가능 증거(파일 존재·grep 결과·gate-report·final PDF) 대조 판정.
- state.json 갱신은 메인만(단일 writer): status/evidence/phase·round 반영.
- **완료 판정**: 전 claims 검증 완료(evidence 기입) + `git status` 무결성 보고(ops-supervisor).

### 단계별 순서 요약 (의존 그래프)

```
typst-build.yaml(메인) ─┐
00-들어가며(메인)      ─┤
배치 A~E 스폰 ×5(병렬) ─┴→ [Phase 1 완료] → build+qc 루프(메인) → [Phase 2 PASS]
 → ②적대 3렌즈(직렬) → 수정(+재게이트) → [Phase 3 완료] → ④review-pr-xhigh → state.json 갱신 → [완료]
```

---

## 4. 보존 제약 (③구현 프롬프트에 verbatim 복사)

```
[보존 제약 — verbatim]
- skills/korean-ebook/ 아래 어떤 파일도 수정·삭제하지 않는다(스크립트·스타일 팩·references·tokens.json 포함). 읽기만 한다.
- books/ 아래 기존 서적 디렉터리(procedural-graphs-ko 등 lean-guardrails-ko 이외 전부)를 만지지 않는다.
- docs/task-id/guardrails-book/briefs/와 sources/ 파일을 수정하지 않는다(계약·원문 소스 불변).
- books/lean-guardrails-ko/manuscript/ 에서 자신의 배치에 배정되지 않은 파일을 생성·수정하지 않는다.
- state.json을 스폰 에이전트가 쓰지 않는다(메인 세션 단일 writer).
- 이미 빌드 가능한 기존 책의 draft/final 산물과 gate-report.json을 지우거나 다시 만들지 않는다.
```

---

## 5. 검증 요구(claims) — 현행 6건 검토 + 제안

`docs/task-id/guardrails-book/state.json` 현행 6건은 모두 검증 가능한 형태로 **유지한다**. 수정·추가 제안:

| # | 현행 | 판정 | 제안 |
|---|---|---|---|
| 1 | yaml lecture·15챕터·순서 일치 | 유지 + 문구 구체화 | "…목록 순서가 책 순서(00→14 오름차순)와 일치한다"로 fix — '책 순서'의 정의를 고정(가정 1.3-2) |
| 2 | build.py exit 0 | 유지 | — |
| 3 | qc_gate PASS(G1·G2)+final/ PDF | 유지 | — |
| 4 | 10~13 장머리 출처 실물 확인 | 유지 + 확장 | 뒤에 "…이며, 미확인 논문은 표기 생략·대체 서술과 사유가 완료 보고에 남아 있다" 추가 — 브리프 D/E의 수용 경로까지 커버. 아울러 "00-들어가며 첫 머리에 단일 논문 인용 블록(원문·링크)이 존재한다"를 본 claim에 합칠 것 |
| 5 | 핵심 수치 보존 | 유지 + 확장 후보 | 기존 목록 유지. 여력 시 "2007 해머 사건·Erdős 문제 1026·728·Debt_to_Income < 0.43" 추가(모두 원문에 실재하는 검증 가능 항목) |
| 6 | G4·G5 경고 0 또는 명시 수용 | 유지 | — |
| 7 | (신규 추가 권고) | 추가 | "15개 원고 파일 각각에서 `^## ` 정확히 1회·`^# ` 0회이고, 다이어그램 필수 장(05·08·09·14)에 ```diagram 펜스가 존재하며, 각 장 본문이 3,000~4,200자(공백 포함)이다" — grep·wc 1줄 검증. 헤딩 위반은 개면 충돌로 G1에 번지므로 1차 방어선 claim으로 선(先)확보 가치가 큼 |

- 테스트가 없는 창작 과업이므로 대체 확인 수단 = (a) 기계 grep/wc(claim 7) (b) 빌드·QC 게이트(claims 2·3) (c) ②적대 렌즈의 원문 대조(claims 4·5) 3층. claim 7 신설 시 이 조합이 완결됨.
- 11장 diagram은 브리프상 '권장(되도록)'이므로 claim 7의 필수 판정 대상에서 뺀다(실패 오탐 방지).

---

## 6. 위험 노트 (위험 → 완화책 1줄)

| 위험 | 완화책 |
|---|---|
| 다이어그램 I1 린트 실패(05·08·09·14 필수 + 11 권장) | 집필 전 `references/diagram-authoring.md` 선독 + 노드 라벨 12자 내외 보수 저작, 장별 `infographic/cli.py lint` 선검증 후 전체 빌드 |
| 추가 논문 실물 확인 실패(부재·ID 불일치 — 2608.14568·2606.14502·2601.21186·2603.24946 등) | 브리프 D/E 계약대로 webReader/WebFetch 실물 확인 → 미확인분은 표기 생략·대체 서술 후 완료 보고 명시, 한 장에서 2편 이상 실패하면 메인이 대체 소스 재지정 |
| G3 밴드(lecture 40~52자/줄) 이탈 | WARN 게이트라 PASS 지장 없음 — 짧은 조각문·명사 나열 회피가 1차 방어, gate-report.json 잔여는 수용 사유와 함께 보고 |
| G4 문체 경고(번역투·명사형 종결·'의' 연쇄) | 브리프 공통 계약(강의체·능동태·"이 장에서는" 1회 이하) 준수가 1차 방어, WARN 지적 면만 수정 후 재빌드 — 잔여는 claim 6으로 명시 수용 |
| G1 판면 오버플로(표·도식 과다 장 — 02·08·09 등) | 표 컬럼 ≤4·도식 장당 1개 상한 유지, gate-report 기반 지적 면만 수정하는 재빌드 루프 |
| 02↔09 §5.1 내용 중복 | 브리프 역할 분리(02=계보·비교표 / 09=상세·선례) 준수 + ③조립 시 메인이 중복 문단 스폿 체크 |
| typst 특수문자·통화 escape 오류($440M 등) | 브리프 계약대로 통화는 한국어 서술("4억 4천만 달러"), 특수문자는 코드스팬 처리 |
| 병렬 스폰 경합·state 충돌 | 배치 파일 집합이 서로소이며 state.json은 메인 단일 writer — 스폰은 원고 파일만 씀 |
| ②팬아웃 GLM xhigh 상한(동시 1) | 3렌즈를 직렬 스폰으로 운영(Phase 3 명시) — 병렬화 시도 금지 |

---

## 7. 롤백 가능성 — **높음**

- 이번 과업의 모든 쓰기는 `books/lean-guardrails-ko/`(신규 디렉터리 내용) + `docs/task-id/guardrails-book/`(plan.md·state.json) 신규/추가분뿐 — 기존 추적 파일 변형 0.
- 롤백 = `books/lean-guardrails-ko/` 삭제(또는 `git clean/checkout`)로 원점 완전 복귀. 빌드 산물은 gitignore 대상이라 롤백 대상 아님.
- 보존 제약(§4)이 skills·기존 books를 불변으로 묶으므로 회귀 리스크 없음. 배치별 부분 롤백도 파일 단위로 가능(배치 간 결합 없음 — 결합은 Phase 2 빌드에서 처음 발생).

---

## 8. 후속 단계 핸드오프 메모

- ②스폰 프롬프트에는 §1.1 커버리지 맵 + §5 claims 원문 + §6 위험표를 첨부할 것(원문 충실도 렌즈가 claim 5 수치를 1:1 대조).
- ④스폰 프롬프트에는 §5 최종 claims(7건 권고안 확정본)를 verbatim 주입.
- 메인은 Phase 2 진입 전 가정 1.3-2(책 순서 00→14)를 yaml에 반영했는지 확인.
