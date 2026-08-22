# 인포그래픽 Phase 6 — agent-papers-2026-ko 첫 실전 적용 + G1 베이스라인 회복 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 인포그래픽 레이어(Phase 1–5 인프라)의 첫 실전 소비자로 agent-papers-2026-ko 책에 교차검증 통과 펜스 11개를 저작하고, 08-20 폰트 라인업 전환이 유발한 G1 판면 오버플로 회귀를 수복해 qc_gate PASS를 낸다.

**Architecture:** Task 1은 5개 팩 theme.typ의 2단 헤딩 규칙(`v(0.8em)` weak)에 강한 간격을 부여해 페이지 상단 헤딩 글리프 어센더 오버슈트(−3.17pt)를 프레임 안으로 밀어넣는다(메커니즘 실증 완료 — 아래 배경). Task 2–3은 챕터 원고 md에 ` ```infographic ` 펜스 11개를 삽입한다(들어가며 + 제1–10장, layout 4종 — before_after는 실재 전환에만). Task 4는 전체 빌드·교차검증 경고 0·qc PASS·final 재생성·infographic_pages 리포트·PNG 검증으로 마감한다.

**Tech Stack:** typst 0.15.1(정적 Pretendard만 — VF 금지), pymupdf, pytest, 기존 빌드 파이프라인(`scripts/build.py`·`scripts/qc_gate.py`·`scripts/infographic/`).

**Spec:** `docs/superpowers/specs/2026-08-21-infographic-layer-design.md`

## Global Constraints

- 스펙 §1: 도식은 원고의 **편집적 재배열** — 원문(표 포함) 대체 금지. 표는 그대로 두고 펜스는 인접 위치에 삽입. 도식 언어로 새로 창작하는 문구는 경계 규약("근거 문구는 원문에서") 위반.
- 스펙 §2: 펜스 형식 ` ```infographic ` + JSON. build 파이프라인이 emit·include 치환.
- 스펙 §5(교차검증): 펜스 title·kicker·항목·축 라벨의 모든 숫자 토큰(`NUM_RE = [0-9][0-9.,%]*`)은 evidence 절 `"§N"`이 가리키는 `## ` 슬라이스 원문에 존재해야. 이 책 챕터는 `## `가 장 제목 하나뿐(12개 md 전수 확인) → 모든 evidence `"§1"` = 챕터 전체(md 표 셀 포함 — 원시 md 슬라이스). thesis·note는 편집자 문구로 검증 제외.
- 레이아웃 라우팅: before_after는 **실재하는 전환**(시간·인과)에만 — 비교·거울 짝은 cards. matrix 2×2는 두 축이 비자명할 때. ladder는 누적 수준·단조 상승.
- 강의 팩 요소 상한: flow ≤8, cards ≤6, ladder ≤5단, before_after ≤5(한쪽 기준), topology ≤8노드·최장경로 층위 ≤4, matrix 2×2 고정. 기하·예산 게이트(커넥터 샤프트 ≥12pt, 축 라벨 ≤3줄)도 치명 I1 — 빌드 중단.
- 폰트: 정적 Pretendard만. VF 설치 금지(typst 0.15.1 Thin 버그).
- 커밋 규약: `<type>: <한글 설명>`, 빈 본문, attribution 없음.
- 스위트: `python3 -m pytest skills/korean-ebook-typst/tests/ -q` — 병합 전 260+ 전 pass.
- 저자 KLIC, 표지·스타일 자동(`typst-build.yaml` style auto → lecture).

## 배경 — G1 회귀 메커니즘 (2026-08-22 실증 완료)

- 증상: draft 빌드 후 qc_gate G1 판면 오버플로 — 예 `p9 bbox=(65.2,76.2,…) frame=(65.2,79.37,…) text='한계와 남는 의문'`. 전부 **md `### ` 절 제목 = typst 2단 헤딩**(md2typst.py `### `→`==`), 13.0pt Pretendard-Bold accent(theme L2 규칙 렌더), 전부 y0 76.2 vs 프레임 상단 79.37 = **−3.17pt**.
- 원인 사슬: 08-20 저녁 폰트 라인업 전환(`495d49d`·`5cd422d` Noto CJK → Pretendard/SUIT/Wanted Sans/Freesentation). Pretendard-Bold 13pt 어센더 잉크가 라인박스 상단을 3.17pt 초과. 5개 팩 theme.typ의 2단 규칙은 `v(0.8em)` **weak** — 페이지 상단에서 0으로 붕괴해 글리프가 프레임 상단에 걸림. G1 측정 코드(qc_gate)는 변경 없음. base.typ의 L2 규칙은 theme가 오버라이드(죽은 경로)라 theme가 수정 대상.
- 실증: 최소 재현(lecture theme, `#pagebreak()` 직후 `== 절제목`)에서 y0=76.92 vs 프레임 79.37 재현. theme L2 규칙의 `v(0.8em)`을 `v(0.8em, weak: false)`로 바꾸면 페이지 상단 y0=95.39(**+16.0pt 여유**), 중간 페이지 간격 불볂(weak는 중간에서 유지되던 값과 동일).
- 3단(md `#### ` → `===`)은 이 책 ch08 3개뿐이고 G1 목록에 없음 — 이번에 고치지 않는다. 타 책(practical-system-design `#### ` 314개·sdi-notes 407개·ai-agent 15개)의 3단 잠재 회귀는 해당 책 재빌드 시점 과제로 이관(재빌드 자체가 폰트 전환 후 미실행 상태).

---

### Task 1: G1 베이스라인 회복 — 5팩 theme 2단 헤딩 강한 간격

**Files:**
- Modify: `skills/korean-ebook-typst/styles/lecture/theme.typ:17`
- Modify: `skills/korean-ebook-typst/styles/b5/theme.typ`
- Modify: `skills/korean-ebook-typst/styles/business/theme.typ`
- Modify: `skills/korean-ebook-typst/styles/essay/theme.typ`
- Modify: `skills/korean-ebook-typst/styles/practical/theme.typ`
- Test: `skills/korean-ebook-typst/tests/test_g1_heading_page_top.py` (Create)

**Interfaces:**
- Consumes: 기존 컴파일 테스트 관례(`test_build_compile.py` — conftest가 스킬 루트를 sys.path에 추가, `pytestmark = skipif(shutil.which("typst") is None)`).
- Produces: 5팩 전부의 L2 강한 간격 — Task 4 qc PASS의 전제.

- [ ] **Step 1: 실패 테스트 작성**

```python
"""G1 판면 오버플로 회귀 — 페이지 상단 2단 헤딩 글리프가 프레임 상단 안에 있는지.

md '### ' 절 제목 → typst 2단. theme L2 규칙의 v(0.8em) weak가 페이지 상단에서
붕괴해 Pretendard-Bold 어센더 잉크가 프레임을 3.2pt 넘는다(2026-08-22 회귀).
"""
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest

from scripts.build import typst_binary

pytestmark = pytest.mark.skipif(shutil.which("typst") is None, reason="typst 미설치")

SKILL = Path(__file__).resolve().parents[1]


def _compile(tmp: Path, style: str) -> tuple[float, float]:
    for name, src in (
        ("base.typ", SKILL / "templates" / "base.typ"),
        ("theme.typ", SKILL / "styles" / style / "theme.typ"),
        ("tokens.json", SKILL / "styles" / style / "tokens.json"),
    ):
        shutil.copy2(src, tmp / name)
    doc = "\n".join([
        '#import "base.typ": base',
        '#import "theme.typ": theme',
        "#show: base",
        "#show: theme",
        "",
        "#pagebreak()",
        "== 한계와 남는 의문",
        "본문 한 줄.",
        "",
    ])
    (tmp / "main.typ").write_text(doc, encoding="utf-8")
    out = tmp / "probe.pdf"
    r = subprocess.run(
        [typst_binary(), "compile", str(tmp / "main.typ"), str(out), "--root", str(tmp)],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr
    page = fitz.open(out)[1]
    tokens = json.loads((SKILL / "styles" / style / "tokens.json").read_text())
    frame_top = tokens["margin"]["top_mm"] / 25.4 * 72
    spans = [
        s
        for b in page.get_text("dict")["blocks"]
        for l in b.get("lines", [])
        for s in l["spans"]
    ]
    head = next(s for s in spans if "한계" in s["text"])
    return head["bbox"][1], frame_top


@pytest.mark.parametrize("style", ["b5", "business", "essay", "lecture", "practical"])
def test_level2_heading_at_page_top_stays_in_frame(style):
    import fitz  # 로컬 임포트 — 미설치 환경 skip은 conftest/기존 관례에 맡김

    with tempfile.TemporaryDirectory() as d:
        y0, frame_top = _compile(Path(d), style)
        assert y0 >= frame_top, (
            f"{style}: 2단 헤딩 글리프 y0={y0:.2f} < 프레임 상단 {frame_top:.2f}"
        )
```

주의: `import fitz`를 파일 상단으로 올려도 무방(기존 qc 테스트가 이미 pymupdf 의존). tokens.json margin 구조 `{"margin": {"top_mm": N}}` 실측 확인됨.

- [ ] **Step 2: 테스트 실패 확인**

Run: `python3 -m pytest skills/korean-ebook-typst/tests/test_g1_heading_page_top.py -q`
Expected: 5개 전부 FAIL — `2단 헤딩 글리프 y0=76.xx < 프레임 상단 79.37` (팩별 여백 차이로 frame_top은 상이할 수 있음 — 위반 자체로 판정)

- [ ] **Step 3: 5개 theme.typ L2 규칙 수정**

각 팩 theme.typ의 2단 헤딩 show 규칙에서 첫 줄 `v(0.8em)`을 강한 간격으로:

```typst
  show heading.where(level: 2): it => {
    v(0.8em, weak: false)
    ...
```

5개 팩 전부 동일 변경(lecture 기준 `styles/lecture/theme.typ:17`). 주석 한 줄 추가(각 파일 규칙 위):

```typst
    // weak 간격은 페이지 상단에서 붕괴 — Pretendard 계열 어센더 잉크가
    // 프레임 상단을 3.2pt 넘어 G1 오버플로가 된다. 강한 간격으로 보호.
```

- [ ] **Step 4: 테스트 통과 확인**

Run: `python3 -m pytest skills/korean-ebook-typst/tests/test_g1_heading_page_top.py -q`
Expected: 5 passed (lecture 기준 y0=95.39 ≥ 79.37)

- [ ] **Step 5: 전체 스위트 + 실책 G1 확인**

Run: `python3 -m pytest skills/korean-ebook-typst/tests/ -q`
Expected: 기존 전부 pass + 신규 5 pass. 골든은 emit .typ 텍스트 스냅샷(컴파일 산물 아님)이라 불변.

Run: `python3 skills/korean-ebook-typst/scripts/build.py books/agent-papers-2026-ko && python3 skills/korean-ebook-typst/scripts/qc_gate.py books/agent-papers-2026-ko; python3 -c "import json;d=json.load(open('books/agent-papers-2026-ko/gate-report.json'));print('g1:',d.get('g1_overflow'))"`
Expected: build 성공, qc g1_overflow `[]` (G4 문체 경고·검수시트 WARN은 비차단 — `pass: not overflow and not fonts`).

- [ ] **Step 6: 커밋**

```bash
git add skills/korean-ebook-typst/styles/*/theme.typ skills/korean-ebook-typst/tests/test_g1_heading_page_top.py
git commit -m "fix: 2단 헤딩 페이지 상단 G1 오버플로 — 5팩 theme 강한 간격"
```

---

### Task 2: 펜스 저작 — 들어가며 + 제1–5장 (6개)

**Files:**
- Modify: `books/agent-papers-2026-ko/manuscript/00-들어가며.md`
- Modify: `books/agent-papers-2026-ko/manuscript/01-제1장-도구를-다-쥐여주면.md`
- Modify: `books/agent-papers-2026-ko/manuscript/02-제2장-새-대화창을-열면.md`
- Modify: `books/agent-papers-2026-ko/manuscript/03-제3장-읽은-파일과-고친-파일.md`
- Modify: `books/agent-papers-2026-ko/manuscript/04-제4장-일은-끝났는데.md`
- Modify: `books/agent-papers-2026-ko/manuscript/05-제5장-여덟-명이-붙으면.md`

**Interfaces:**
- Consumes: 스펙 §2 펜스 계약, §5 교차검증(evidence `"§1"`), 강의 팩 상한·기하·예산 게이트.
- Produces: 6개 펜스 삽입된 md — Task 4 빌드의 입력. 모든 숫자 토큰은 아래 예시에 **정확히** 담긴 대로 사용(원문 존재 2026-08-22 전수 검증 + lint 파이프라인 기계 검증 완료).

**공통 규칙(각 펜스에 적용):**
- 삽입 위치는 각 스텝의 지시가 우선한다(기본값 "절 끝·다음 `### ` 직전"은 스텝이位置를 지정하지 않을 때만). 표는 절대 지우지 않는다. 펜스 블록 앞뒤 빈 줄 1개.
- 모든 펜스에 `"evidence": "§1"`. `note`는 "편집 요약: …" 형식(편집자 문구, 검증 제외).
- 아래 JSON을 그대로 복사(문구·숫자는 원문 대조 + geometry/budget lint 통과 버전).

- [ ] **Step 1: 들어가며 — cards (묶음 A–D)**

`00-들어가며.md`의 `### 네 가지 질문, 열 장` 절 끝(`### 이 책을 읽는 방법` 직전)에 삽입:

````markdown
```infographic
{
  "layout": "cards",
  "title": "네 묶음 — 설계 두 개, 운영 두 개",
  "kicker": "BOOK MAP",
  "thesis": "A·B는 만들기 전에 정하는 설계 결정, C·D는 만든 뒤에 관리하는 운영 결정이다.",
  "cards": [
    {"title": "A · 무엇을 얼마나 줄 것인가", "text": "1·2·3장 — 넉넉하게 주는 것은 공짜가 아니다"},
    {"title": "B · 얼마나 쪼갤 것인가", "text": "4·5장 — 쪼개는 것은 이득이 아니라 거래다"},
    {"title": "C · 무엇을 기억할 것인가", "text": "6·7장 — 돕는 일과 해로운 일이 갈린다"},
    {"title": "D · 어떻게 잴 것인가", "text": "8·9·10장 — 점수만 보면 비용이 안 보인다"}
  ],
  "note": "편집 요약: 들어가며의 네 묶음 구성을 재배열한 도식이다.",
  "evidence": "§1"
}
```
````

카드 제목이 3열 예산(~11.7자/줄) 경계라 2줄 랩 가능 — 허용됨(높이 자동 조정).

- [ ] **Step 2: 제1장 — ladder (K1–K5)**

`01-*.md`의 `### 어떻게 답했나` 절 끝(`### 무엇이 밝혀졌나` 직전, K-표 문단 뒤)에 삽입:

````markdown
```infographic
{
  "layout": "ladder",
  "title": "하네스 제공 등급은 누적 사다리다",
  "kicker": "K-LADDER",
  "thesis": "위 등급은 아래 등급의 모든 것을 포함하며, 최대 제공이 성능 최적은 아니다.",
  "stages": [
    {"title": "K1 모델 단독", "text": "과제 문구와 모델의 매개지식뿐"},
    {"title": "K2 정적 지식", "text": "매뉴얼·SOP·사양서·규칙 기반"},
    {"title": "K3 시계열 관측", "text": "텔레메트리·로그·알람·계측"},
    {"title": "K4 구조와 물리", "text": "위상·지배 방정식·물리 제약"},
    {"title": "K5 순방향 시뮬레이션", "text": "디지털트윈 롤아웃·반사실 평가"}
  ],
  "note": "편집 요약: 어떻게 답했나의 다섯 단계 사다리 표를 재배열한 도식이다.",
  "evidence": "§1"
}
```
````

- [ ] **Step 3: 제2장 — cards (전략 A–E)**

`02-*.md`의 `### 무엇이 밝혀졌나` 절, 결과 표(전체 30회 열이 있는 표) **직후**, "(D·E는 1차 배치…" 괄호 문단 앞에 삽입:

````markdown
```infographic
{
  "layout": "cards",
  "title": "다섯 인수인계 전략, 3단계를 넘기는 하나뿔",
  "kicker": "HANDOFF A–E",
  "thesis": "단일 단계에서는 다섯이 비슷하고, 차이는 3단계에서 벌어진다.",
  "cards": [
    {"title": "A · 원자료 재독", "text": "이번 단계 자료만 다시 읽는다 — 0/15"},
    {"title": "B · 전체 히스토리 재생", "text": "이전 것 전부를 원문 순서로 — 2/15"},
    {"title": "C · 런타임 매개 핸드오프", "text": "수락된 상태와 꾸러미를 넘긴다 — 14/15", "value": "통과"},
    {"title": "D · 롤링 요약", "text": "수락된 결정의 산문 사영 — 0/15"},
    {"title": "E · 경량 JSON", "text": "수락된 결정의 고정필드 사영 — 0/15"}
  ],
  "note": "편집 요약: 3단계 계열 통과 결과를 재배열한 도식이다.",
  "evidence": "§1"
}
```
````

- [ ] **Step 4: 제3장 — topology (네 가지 얼굴·권위 상태)**

`03-*.md`의 `### 어떻게 답했나` 절, "형식화는 단정합니다" 문단(세 뷰 소개, "…비동기 재파싱이 끝나야 최신으로 돌아옵니다"로 끝남) **직후**에 삽입:

````markdown
```infographic
{
  "layout": "topology",
  "title": "네 가지 얼굴, 권위는 하나",
  "kicker": "AUTHORITY",
  "thesis": "실행과 제출의 근거가 되는 권위 상태는 W_t 하나이고, C_t와 Δ_t는 별도 문서가 아니라 파생 뷰다.",
  "nodes": [
    {"id": "w", "label": "네이티브 파일 W_t · 권위"},
    {"id": "c", "label": "파싱된 뷰 C_t"},
    {"id": "d", "label": "변경 내역 Δ_t"},
    {"id": "s", "label": "제출 산출물"}
  ],
  "edges": [
    {"from": "w", "to": "c"},
    {"from": "w", "to": "d"},
    {"from": "d", "to": "s"}
  ],
  "note": "편집 요약: 어떻게 답했나의 세 뷰·권위 상태 관계를 재배열한 도식이다.",
  "evidence": "§1"
}
```
````

4노드·최장경로 3층위 — 5노드(j 쓰기 연산 포함) 버전은 커넥터 샤프트 11.96pt < 12pt로 치명 I1이므로 **이 형태를 유지**한다.

- [ ] **Step 5: 제4장 — cards 2장 (과소·과잉 거울)**

`04-*.md`의 `### 무엇이 밝혀졌나` 절, kyc 사례 표(`kyc-0004` 행 포함) **직후**에 삽입. 원문의 과소·과잉은 동시적 거울 짝(전환이 아님)이라 before_after 대신 cards:

````markdown
```infographic
{
  "layout": "cards",
  "title": "같은 감쇠가 과소와 과잉을 둘 다 만든다",
  "kicker": "ATTENUATION",
  "thesis": "감쇠는 안전한 방향으로만 기울지 않는다 — 방향은 사라진 정보의 성격이 정하고, 그건 미리 알 수 없다.",
  "cards": [
    {"title": "과소 에스컬레이션", "text": "위험 신호가 흘려짐 (kyc-0004) — 스크리닝 생략, 8/10 (80%)"},
    {"title": "과잉 에스컬레이션", "text": "면책 신호가 흘려짐 (kyc-0005) — 불일치 미전달, 14/16 (88%)"}
  ],
  "note": "편집 요약: 무엇이 밝혀졌나의 대칭성 발견을 재배열한 도식이다.",
  "evidence": "§1"
}
```
````

`8/10 (80%)`·`14/16 (88%)`은 kyc 표 셀 값 — 삽입 전 표에서 재확인, 다르면 표 값으로.

- [ ] **Step 6: 제5장 — cards 2장 (같은 처방, 정반대 결과)**

`05-*.md`의 `### 무엇이 밝혀졌나` 절, ③ 파일 정책 표 **직후**("메시지가 많은 분산 작업 8인에서…" 문단 앞)에 삽입. 분산/연쇄는 비교지 전환이 아니라 cards:

````markdown
```infographic
{
  "layout": "cards",
  "title": "같은 처방, 정반대 결과",
  "kicker": "POLICY MIRROR",
  "thesis": "파일 의무화는 작업 구조에 따라 약이 되기도 독이 되기도 한다.",
  "cards": [
    {"title": "분산 작업 — 약", "text": "메시지 10,500→1,700통 · 출력 토큰 약 42% 감소 · 지수 1.92 → 1.12~1.32", "value": "−42%"},
    {"title": "연쇄 작업 — 독", "text": "출력 토큰 10~17% 증가 · 4인 +17%, 8인 +10% · 16인 배증 57.8만 vs 33.3만", "value": "+10~17%"}
  ],
  "note": "편집 요약: ③ 파일 정책 비교를 재배열한 도식이다.",
  "evidence": "§1"
}
```
````

- [ ] **Step 7: 교차검증·렌더 확인**

Run: `python3 skills/korean-ebook-typst/scripts/build.py books/agent-papers-2026-ko > /tmp/p6b.log 2>&1; echo "build_rc=$?"; grep -iE "경고|warn|I1|실패" /tmp/p6b.log; echo "grep_rc=$? (경고 0건이면 grep_rc=1이 정상)"`
Expected: `build_rc=0`, grep 출력 없음(누적 6 펜스 emit, 치명 I1 0건).

Run: `python3 -m pytest skills/korean-ebook-typst/tests/ -q`
Expected: 전 pass.

- [ ] **Step 8: 커밋**

```bash
git add books/agent-papers-2026-ko/manuscript/
git commit -m "feat: 들어가며·제1-5장 인포그래픽 펜스 6종 — cards·ladder·topology"
```

---

### Task 3: 펜스 저작 — 제6–10장 (5개)

**Files:**
- Modify: `books/agent-papers-2026-ko/manuscript/06-제6장-많이-찾아다-주면.md`
- Modify: `books/agent-papers-2026-ko/manuscript/07-제7장-왜-그렇게-정했더라.md`
- Modify: `books/agent-papers-2026-ko/manuscript/08-제8장-내가-넣은-한-줄은.md`
- Modify: `books/agent-papers-2026-ko/manuscript/09-제9장-잘-나온-결과-하나로.md`
- Modify: `books/agent-papers-2026-ko/manuscript/10-제10장-만들기-전에-약속.md`

**Interfaces:**
- Consumes: 스펙 §2·§5, 강의 팩 상한, 기하·예산 게이트.
- Produces: 5개 펜스 — Task 4 빌드 입력. 공통 규칙은 Task 2와 동일.

- [ ] **Step 1: 제6장 — matrix 2×2 (검색 폭 k의 갈림길)**

`06-*.md`의 `### 무엇이 밝혀졌나` 절, "…갈림길의 실체는 '조회 대 실행'이라는 과제 라벨이 아니라, **가져온 것이 지금 결정의 재료와 경쟁하는가, 보완하는가**입니다." 문단 **직후**(③ 항목 앞)에 삽입 — 축 개념·BigCodeBench 숫자가 이 문단과 요약 표에 처음 나오므로 근거보다 앞서지 않게:

````markdown
```infographic
{
  "layout": "matrix",
  "title": "검색 폭 k의 갈림길",
  "kicker": "RETRIEVAL k",
  "thesis": "실체는 과제 라벨이 아니라 — 가져온 것이 지금 결정의 재료와 경쟁하는가, 보완하는가.",
  "x_axis": {"low": "검색이 답과 경쟁", "high": "검색이 답을 보완"},
  "y_axis": {"low": "발언 안의 답", "high": "답이 과제 맥락에"},
  "cells": [
    {"title": "빈 사분면", "text": "이 사분면에 든 벤치마크는 없음"},
    {"title": "LoCoMo — 단조 상승", "text": "k를 늘릴수록 오른다 (k=1→20)"},
    {"title": "ALFWorld — 하락·방황", "text": "부호가 뒤집힌다 (k=1→5)"},
    {"title": "BigCodeBench — 보완", "text": "M2 19.6%가 M5 16.2%를 앞지른다"}
  ],
  "note": "편집 요약: ② 검색 범위 결과를 재배열한 도식이다.",
  "evidence": "§1"
}
```
````

셀 순서 `[y low·x low, y low·x high, y high·x low, y high·x high]`(authoring.md与 일치). y0 라벨은 예산(≤3줄) 때문에 "발언 안의 답"로 축약된 버전 — 변경 금지.

- [ ] **Step 2: 제7장 — matrix 2×2 (질문 유형 × 저장 구조)**

`07-*.md`의 `### 무엇이 밝혀졌나` 절, "구조적 추론이 필요한 세 과제의 결과는 아래와 같다" 문장 아래 결과 표 **직후**에 삽입:

````markdown
```infographic
{
  "layout": "matrix",
  "title": "질문이 구조를 요구하면 저장 구조가 성적을 정한다",
  "kicker": "GRAPH vs VECTOR",
  "thesis": "우위의 원천은 내용이 아니라 구조다 — 같은 내용도 구조를 걷어내면 무너진다.",
  "x_axis": {"low": "구조화 그래프 (B2)", "high": "구조 없는 저장 (mem0·평문)"},
  "y_axis": {"low": "구조 질문", "high": "관련성 질문"},
  "cells": [
    {"title": "완전성·부정·대체", "text": "1.00 · 0.98 · 0.98"},
    {"title": "집합을 못 모은다", "text": "mem0 0.18 · 0.06 · 0.27"},
    {"title": "커버리지", "text": "0.82 (약 35k 토큰)"},
    {"title": "비긴다", "text": "0.67~0.90 (약 40k 토큰)"}
  ],
  "note": "편집 요약: 결과 표와 관련성 검색 비교를 2×2로 재배열한 도식이다.",
  "evidence": "§1"
}
```
````

y0 라벨 "구조 질문"은 예산(≤3줄) 축약 버전 — 변경 금지.

- [ ] **Step 3: 제8장 — ladder (비트 사다리)**

`08-*.md`의 `### 어떻게 답했나` 절, b비트 환산표 **직후**(표 보존)에 삽입:

````markdown
```infographic
{
  "layout": "ladder",
  "title": "좋은 프롬프트 한 줄은 비트로 값을 매긴다",
  "kicker": "BITS",
  "thesis": "규칙은 하나 — b비트는 2의 b승배.",
  "stages": [
    {"title": "1비트 — 2배", "text": "시도 두 번이 한 번으로"},
    {"title": "3비트 — 8배", "text": "여덟 번 넣을 일이 한 번으로"},
    {"title": "5비트 — 32배", "text": "재현 기대 비용이 서른두 배 차이"},
    {"title": "10비트 — 1,024배", "text": "백 번과 십만 번의 차이"},
    {"title": "20비트 — 약 100만 배", "text": "사실상 없으면 못 얻는다"}
  ],
  "note": "편집 요약: 어떻게 답했나의 비트 환산표를 재배열한 도식이다.",
  "evidence": "§1"
}
```
````

- [ ] **Step 4: 제9장 — cards (과정 지표 C1·C2·C3)**

`09-*.md`의 `### 무엇이 밝혀졌나` 절, "과정 지표는 점수가 같아도 이유가 다름을 보여준다" 문단 **직후**에 삽입:

````markdown
```infographic
{
  "layout": "cards",
  "title": "과정 지표 세 축이 모델을 가른다",
  "kicker": "C1 · C2 · C3",
  "thesis": "경쟁적인 해법에 도달하는 능력은 널려 있고, 재현하는 능력이 모델을 가른다.",
  "cards": [
    {"title": "C1 · 해결책", "text": "방향을 일찍 잡았나 — 0.473~0.612 넓게 갈림"},
    {"title": "C2 · 실행", "text": "실제로 도는가 — 0.880~0.967 전 모델 몰림"},
    {"title": "C3 · 피드백 제어", "text": "최고점 유지·회복 — 0.772~0.928 갈림"}
  ],
  "note": "편집 요약: 무엇이 밝혀졌나의 과정 지표 산포를 재배열한 도식이다.",
  "evidence": "§1"
}
```
````

- [ ] **Step 5: 제10장 — before_after (직접 생성 → 명세 주도)**

`10-*.md`의 `### 어떻게 답했나` 절 끝(`### 무엇이 밝혀졌나` 직전)에 삽입. 실재 전환(흐름 교체)이라 before_after 적합:

````markdown
```infographic
{
  "layout": "before_after",
  "title": "명세 문서 한 장이 검출률을 바꾼다",
  "kicker": "SPEC-FIRST",
  "thesis": "실행 예산이 늘수록 격차가 벌어진다 — 다섯 번에 +9.8%포인트.",
  "before_label": "직접 생성",
  "after_label": "명세 주도",
  "before": [
    "코드 → 에이전트 → 테스트 직행",
    "정상 경로 중심",
    "반복해도 53%대 정체"
  ],
  "after": [
    "코드 → 계약 문서 → 테스트",
    "경계·면책 목록이 근거",
    "detect@5 63.2% (+9.8%p)"
  ],
  "center": "계약 문서",
  "note": "편집 요약: 두 흐름의 전환 구조와 검출률 차이를 재배열한 도식이다.",
  "evidence": "§1"
}
```
````

- [ ] **Step 6: 교차검증·렌더 확인**

Run: `python3 skills/korean-ebook-typst/scripts/build.py books/agent-papers-2026-ko > /tmp/p6c.log 2>&1; echo "build_rc=$?"; grep -iE "경고|warn|I1|실패" /tmp/p6c.log; echo "grep_rc=$? (경고 0건이면 grep_rc=1이 정상)"`
Expected: `build_rc=0`, grep 출력 없음(누적 11 펜스 emit).

Run: `python3 -m pytest skills/korean-ebook-typst/tests/ -q`
Expected: 전 pass.

- [ ] **Step 7: 커밋**

```bash
git add books/agent-papers-2026-ko/manuscript/
git commit -m "feat: 제6-10장 인포그래픽 펜스 5종 — matrix 2×2·ladder·cards·before_after"
```

---

### Task 4: 통합 — qc PASS·final 재생성·infographic_pages·PNG 검증

**Files:**
- Test: `skills/korean-ebook-typst/tests/test_agent_papers_fences.py` (Create — 펜스 수·레이아웃 불변식)

**Interfaces:**
- Consumes: Task 1의 theme 수정, Task 2–3의 11 펜스, 기존 `render_book_fences`·`_infographic_pages`.
- Produces: qc PASS 최종 게이트, `final/` PDF, gate-report의 `infographic_pages`.

- [ ] **Step 1: 펜스 불변식 테스트 작성**

책 md에서 펜스를 파싱해 수·레이아웃 구성을 고정(원고 무결성 회귀). tests/ 위치상 repo 루트는 `parents[3]`:

```python
"""agent-papers-2026-ko 펜스 불변식 — 수·레이아웃 구성 고정."""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
BOOK = REPO / "books" / "agent-papers-2026-ko" / "manuscript"
FENCE = re.compile(r"```infographic\n(.*?)\n```", re.S)

EXPECTED = {
    "00-들어가며.md": ["cards"],
    "01-제1장-도구를-다-쥐여주면.md": ["ladder"],
    "02-제2장-새-대화창을-열면.md": ["cards"],
    "03-제3장-읽은-파일과-고친-파일.md": ["topology"],
    "04-제4장-일은-끝났는데.md": ["cards"],
    "05-제5장-여덟-명이-붙으면.md": ["cards"],
    "06-제6장-많이-찾아다-주면.md": ["matrix"],
    "07-제7장-왜-그렇게-정했더라.md": ["matrix"],
    "08-제8장-내가-넣은-한-줄은.md": ["ladder"],
    "09-제9장-잘-나온-결과-하나로.md": ["cards"],
    "10-제10장-만들기-전에-약속.md": ["before_after"],
}


def _fences(text: str) -> list[dict]:
    return [json.loads(m) for m in FENCE.findall(text)]


def test_fence_count_and_layouts():
    total = 0
    for name, layouts in EXPECTED.items():
        fences = _fences((BOOK / name).read_text(encoding="utf-8"))
        assert len(fences) == len(layouts), f"{name}: 펜스 {len(fences)}개 != {len(layouts)}개"
        got = [f["layout"] for f in fences]
        assert got == layouts, f"{name}: {got} != {layouts}"
        for f in fences:
            assert f["evidence"] == "§1", f"{name}: evidence {f['evidence']!r}"
        total += len(fences)
    assert total == 11


def test_no_stray_fences_outside_expected_files():
    for p in sorted(BOOK.glob("*.md")):
        if p.name in EXPECTED:
            continue
        assert not FENCE.search(p.read_text(encoding="utf-8")), f"{p.name}: 예상 밖 펜스"
```

파일명이 미세하게 다르면 실제 manuscript/ 파일명에 맞춘다(불변식 값은 유지).

- [ ] **Step 2: 테스트 실행**

Run: `python3 -m pytest skills/korean-ebook-typst/tests/test_agent_papers_fences.py -q`
Expected: 2 passed (RED 단계는 Task 2 완료 시점에 이미 불가 — 커밋 순서로 보증).

- [ ] **Step 3: 전체 빌드 + qc_gate PASS**

Run:
```bash
python3 skills/korean-ebook-typst/scripts/build.py books/agent-papers-2026-ko \
  && python3 skills/korean-ebook-typst/scripts/qc_gate.py books/agent-papers-2026-ko
```
Expected: `[qc] PASS` — final/ 재생성. FAIL 시 gate-report.json의 게이트별 내역으로 수정(원인은 게이트가 지시하는 대로 — 표면 땜질 금지).

- [ ] **Step 4: infographic_pages 리포트 확인**

Run: `python3 -c "import json;d=json.load(open('books/agent-papers-2026-ko/gate-report.json'));ip=d.get('infographic_pages',{});print(ip.get('count'), ip.get('match'));print(ip.get('figs'))"`
Expected: `11 True` — figs 11항목(각 name·chapter·index·page). `infographic_pages`는 리스트가 아닌 dict `{count, expected, match, figs}`(qc_gate.py:186-219·264-266).

- [ ] **Step 5: PNG 검증 — 2종 육안 확인**

검수 PNG(qc_gate가 170DPI로 생성) 중 matrix 1종(ch6 — 셀 사분면 배치 확인)과 topology 1종(ch3 — 간선·층위 확인)을 Read로 열어 확인. 라벨 겹침·사분면 오배치·간선 누락 없어야. 문제 시 펜스 JSON 수정(원문 숫자 토큰 범위 내에서만) 후 재빌드.

- [ ] **Step 6: 전체 스위트 + 커밋**

Run: `python3 -m pytest skills/korean-ebook-typst/tests/ -q`
Expected: 전 pass (260 + Task 1 5건 + Task 4 2건).

```bash
git add skills/korean-ebook-typst/tests/test_agent_papers_fences.py
git commit -m "test: agent-papers 펜스 불변식 — 11종 레이아웃·evidence 고정"
```

- [ ] **Step 7: 게이트 리포트 커밋**

`final/`·`gate-report.json`은 git 비추적(실측) — 빌드 산출물은 커밋하지 않는다. 대신 최종 게이트 요약을 플랜 체크박스 완료로 기록한다.

---

## 셀프 리뷰 기록 (적대 검토 G1·G2·G3 반영판)

- **검토 반영**: G1 — F03 5노드 커넥터 샤프트 11.96pt 치명 → 4노드(lint PASS) / F06·F07 축 라벨 예산(4줄>3줄) 치명 → 축약(lint PASS) / Task 4 경로 parents[3]·infographic_pages dict·우발 펜스 단언 / ch2 삽입 위치 단일화 / 검증 명령 rc 해석 명시. G2 — F04·F05 before_after 허위 전환 → cards 2장 / F00 thesis 좌우 표현 제거(3열 그리드와 모순) / F02 title 과장 한정 / F08 title 방향 반전 수정("매긴다") / F06 삽입 위치 근거 이후로 이동·빈 사분면 중성화 / F03 로케이터 문구 수정 / F07 note 재배열 범위 명시. G3 — Task 1 전면 수정: 오버플로는 3단이 아니라 **2단**(md `### `→`==`, theme L2 weak v) — 5팩 theme 수정, base.typ 불변 / 3단 잠재 회귀(타 책 `#### ` 736개)는 이관 노트로 기록 / rc·grep 함정 수정.
- 스펙 커버리: §2 ✓ §5(숫자 토큰 11/11 기계 검증 통과 — lint 실행 확인) ✓ 상한(cards 4/5/2/2/3 ≤6, ladder 5/5, before_after 3+3, matrix 2×2, topology 4노드·3층위) ✓ 원문 대체 금지 ✓.
- 배치 다양성: cards×5(00·02·04·05·09)·ladder×2·topology×1·matrix×2·before_after×1 — F04·F05의 before_after→cards 전환으로 대비형 남용 해소(G2 HIGH-1). 06·07 연속 matrix는 축 내용 상이로 수용(G2 판정).
- 잔여 수용 판단(재검토 불필요): F00 카드 제목 2줄 랩 허용 / F01 ladder 상승 어포던스는 thesis가 상쇄 / F08 환산표→ladder는 단조 지수 상승 시각화로 방어 / F10 인접 표와의 항목 일부 중복은 "전환 구조+결과 연결" 재배열 가산으로 정당화.
