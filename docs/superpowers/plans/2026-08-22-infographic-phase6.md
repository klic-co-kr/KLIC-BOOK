# 인포그래픽 Phase 6 — agent-papers-2026-ko 첫 실전 적용 + G1 베이스라인 회복 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 인포그래픽 레이어(Phase 1–5 인프라)의 첫 실전 소비자로 agent-papers-2026-ko 책에 교차검증 통과 펜스 11개를 저작하고, 08-20 폰트 라인업 전환이 유발한 G1 판면 오버플로 회귀를 수복해 qc_gate PASS를 낸다.

**Architecture:** Task 1은 base.typ에 3단 헤딩 강한 간격 규칙을 추가해 페이지 상단 헤딩 글리프 어센더 오버슈트(−3.17pt)를 프레임 안으로 밀어넣는다(메커니즘 실증 완료 — 아래 배경). Task 2–3은 챕터 원고 md에 ` ```infographic ` 펜스 11개를 삽입한다(들어가며 + 제1–10장, layout 5종). Task 4는 전체 빌드·교차검증 경고 0·qc PASS·final 재생성·infographic_pages 리포트·PNG 검증으로 마감한다.

**Tech Stack:** typst 0.15.1(정적 Pretendard만 — VF 금지), pymupdf, pytest, 기존 빌드 파이프라인(`scripts/build.py`·`scripts/qc_gate.py`·`scripts/infographic/`).

**Spec:** `docs/superpowers/specs/2026-08-21-infographic-layer-design.md`

## Global Constraints

- 스펙 §1: 도식은 원고의 **편집적 재배열** — 원문(표 포함) 대체 금지. 표는 그대로 두고 펜스는 인접 위치에 삽입.
- 스펙 §2: 펜스 형식 ` ```infographic ` + JSON. build 파이프라인이 emit·include 치환.
- 스펙 §5(교차검증): 펜스 라벨·텍스트의 모든 숫자 토큰(`NUM_RE = [0-9][0-9.,%]*`)은 evidence 절 `"§N"`이 가리키는 `## ` 슬라이스 원문에 존재해야. 이 책 챕터는 `## `가 장 제목 하나뿐 → 모든 evidence `"§1"` = 챕터 전체(md 표 셀 포함 — 원시 md 슬라이스). thesis·note는 편집자 문구로 검증 제외.
- 강의 팩 요소 상한: flow ≤8, cards ≤6, ladder ≤5단, before_after ≤5(한쪽 기준), topology ≤8노드·층위 ≤4, matrix 2×2 고정.
- 폰트: 정적 Pretendard만. VF 설치 금지(typst 0.15.1 Thin 버그).
- 커밋 규약: `<type>: <한글 설명>`, 빈 본문, attribution 없음.
- 스위트: `python3 -m pytest skills/korean-ebook-typst/tests/ -q` — 병합 전 260+ 전 pass.
- 저자 KLIC, 표지·스타일 자동(`typst-build.yaml` style auto → lecture).

## 배경 — G1 회귀 메커니즘 (2026-08-22 실증 완료)

- 증상: draft 빌드 후 qc_gate G1 판면 오버플로 다수 — 예 `p9 bbox=(65.2,76.2,…) frame=(65.2,79.37,…) text='한계와 남는 의문'` — 전부 3단 헤딩, 전부 y0 76.2 vs 프레임 상단 79.37 = **−3.17pt**.
- 원인: 08-20 저녁 폰트 라인업 전환(`495d49d`·`5cd422d` Noto CJK → Pretendard/SUIT/Wanted Sans/Freesentation). Pretendard-Bold 11pt 어센더 잉크가 라인박스 상단을 초과해 넘침. 3단 헤딩은 팩 테마에 show 규칙이 없어(1·2단만 있음) typst 기본 약한(weak) above 간격이 페이지 상단에서 0으로 붕괴 → 글리프가 프레임 상단에 걸림. G1 측정 코드(qc_gate)는 변경 없음.
- 실증: 최소 재현(base+lecture, `#pagebreak()` 직후 `=== 헤딩`)에서 y0=76.92 vs 프레임 79.37 재현. `#show heading.where(level: 3): it => { v(0.9em, weak: false); it }` 추가 시 페이지 상단 y0=85.92(**+6.55pt 여유**), 중간 페이지 헤딩 above 간격 9.54pt → 18.54pt(1.85em — 한국어 책 절 제목 간격으로 정상권).
- 모든 팩이 동일 폰트군(순서만 다름, 첫 가용 Pretendard 우선)이므로 규칙은 공용 `templates/base.typ`에 둔다(단일 진실, 타 팩 잠재 회귀 동시 예방).

---

### Task 1: G1 베이스라인 회복 — base.typ 3단 헤딩 강한 간격

**Files:**
- Modify: `skills/korean-ebook-typst/templates/base.typ`
- Test: `skills/korean-ebook-typst/tests/test_g1_heading_page_top.py` (Create)

**Interfaces:**
- Consumes: 기존 `tests/` 컴파일 스모크 패턴(typst 바이너리 `scripts.build.typst_binary`, tmp 디렉터리에 base.typ/theme.typ/tokens.json 복사 후 컴파일).
- Produces: `base.typ` 3단 헤딩 규칙 — Task 4의 qc PASS 전제. 다른 태스크는 의존 없음.

- [ ] **Step 1: 실패 테스트 작성**

```python
"""G1 판면 오버플로 회귀 — 페이지 상단 3단 헤딩 글리프가 프레임 상단 안에 있는지."""
import shutil
import subprocess
import tempfile
from pathlib import Path

import fitz
import pytest

from scripts.build import typst_binary  # noqa: F401  (스키플 마커 — 기존 테스트와 동일 경로)

SKILL = Path(__file__).resolve().parents[1]


def _compile(tmp: Path) -> Path:
    for name, src in (
        ("base.typ", SKILL / "templates" / "base.typ"),
        ("theme.typ", SKILL / "styles" / "lecture" / "theme.typ"),
        ("tokens.json", SKILL / "styles" / "lecture" / "tokens.json"),
    ):
        shutil.copy2(src, tmp / name)
    doc = "\n".join([
        '#import "base.typ": base',
        '#import "theme.typ": theme',
        "#show: base",
        "#show: theme",
        "",
        "#pagebreak()",
        "=== 한계와 남는 의문",
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
    return out


def test_level3_heading_at_page_top_stays_in_frame():
    with tempfile.TemporaryDirectory() as d:
        pdf = _compile(Path(d))
        page = fitz.open(pdf)[1]  # pagebreak 직후 페이지
        # 강의 팩 여백: top 28mm = 79.37pt (a4 595.28 x 841.89)
        import json
        tokens = json.loads((SKILL / "styles" / "lecture" / "tokens.json").read_text())
        top_mm = tokens["margin"]["top_mm"]
        frame_top = top_mm / 25.4 * 72
        spans = [
            s
            for b in page.get_text("dict")["blocks"]
            for l in b.get("lines", [])
            for s in l["spans"]
        ]
        head = next(s for s in spans if "한계" in s["text"])
        assert head["bbox"][1] >= frame_top, (
            f"3단 헤딩 글리프 y0={head['bbox'][1]:.2f} < 프레임 상단 {frame_top:.2f}"
        )
```

주의: tokens.json의 margin 구조가 `{"margin": {"top_mm": 28}}`가 아니면 실제 구조를 읽어 맞춘다(`scripts/build.py`가 읽는 방식과 동일하게). `from scripts.build import typst_binary` 경로는 기존 컴파일 테스트의 임포트 방식을 그대로 따른다(다르면 그 방식으로).

- [ ] **Step 2: 테스트 실패 확인**

Run: `python3 -m pytest skills/korean-ebook-typst/tests/test_g1_heading_page_top.py -q`
Expected: FAIL — `3단 헤딩 글리프 y0=76.92 < 프레임 상단 79.37`

- [ ] **Step 3: base.typ에 규칙 추가**

`templates/base.typ`의 2단 헤딩 show 규칙 뒤에 추가(주석 포함, 주변 주석 밀도에 맞춤):

```typst
// 3단 헤딩: 기본 above 간격은 weak라 페이지 상단에서 붕괴하는데,
// Pretendard 계열 어센더 잉크가 라인박스를 3.2pt 넘어 G1 프레임 오버플로.
// 강한 간격으로 프레임 상단 안에 여유를 확보한다(중간 페이지 above ≈ 1.85em).
#show heading.where(level: 3): it => { v(0.9em, weak: false); it }
```

- [ ] **Step 4: 테스트 통과 확인**

Run: `python3 -m pytest skills/korean-ebook-typst/tests/test_g1_heading_page_top.py -q`
Expected: PASS

- [ ] **Step 5: 전체 스위트 + 실책 G1 확인**

Run: `python3 -m pytest skills/korean-ebook-typst/tests/ -q`
Expected: 기존 전부 pass + 신규 1 pass (골든 바이트 불변 — 골든 문서는 헤딩 없음).

Run: `python3 skills/korean-ebook-typst/scripts/build.py books/agent-papers-2026-ko && python3 skills/korean-ebook-typst/scripts/qc_gate.py books/agent-papers-2026-ko; python3 -c "import json;d=json.load(open('books/agent-papers-2026-ko/gate-report.json'));print('g1:',d.get('g1_overflow'))"`
Expected: build 성공, qc g1_overflow `[]` (G4 스타일 경고·기타 게이트는 Task 4에서 최종 확인).

- [ ] **Step 6: 커밋**

```bash
git add skills/korean-ebook-typst/templates/base.typ skills/korean-ebook-typst/tests/test_g1_heading_page_top.py
git commit -m "fix: 3단 헤딩 페이지 상단 G1 오버플로 — 강한 간격 규칙"
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
- Consumes: 스펙 §2 펜스 계약, §5 교차검증(evidence `"§1"`), 강의 팩 상한.
- Produces: 6개 펜스 삽입된 md — Task 4 빌드의 입력. 모든 숫자 토큰은 아래 예시에 **정확히** 담긴 대로 사용(원문 존재 2026-08-22 전수 검증 완료).

**공통 규칙(각 펜스에 적용):**
- 펜스는 지정된 `### ` 절의 **끝**(다음 `### ` 헤딩 직전)에 빈 줄 1개를 두고 삽입. 표는 절대 지우지 않는다.
- 모든 펜스에 `"evidence": "§1"` (책 챕터는 `## ` 슬라이스가 장 전체).
- `note`는 편집자 문구(교차검증 제외)로 "편집 요약: …" 형식.
- 아래 JSON을 그대로 복사(라벨의 모든 숫자는 원문 표 셀·본문에 존재 확인됨).

- [ ] **Step 1: 들어가며 — cards (묶음 A–D)**

`00-들어가며.md`의 `### 네 가지 질문, 열 장` 절 끝(`### 이 책을 읽는 방법` 직전)에 삽입:

````markdown
```infographic
{
  "layout": "cards",
  "title": "네 묶음 — 설계 두 개, 운영 두 개",
  "kicker": "BOOK MAP",
  "thesis": "왼쪽(A·B)은 만들기 전에 정하는 설계 결정, 오른쪽(C·D)은 만든 뒤에 관리하는 운영 결정이다.",
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

`02-*.md`의 `### 무엇이 밝혀졌나` 절, 결과 표와 "차이는 3단계에서 벌어집니다" 문단 **사이**에 삽입:

````markdown
```infographic
{
  "layout": "cards",
  "title": "다섯 인수인계 전략, 통과는 하나뿐",
  "kicker": "HANDOFF A–E",
  "thesis": "차이는 단일 단계가 아니라 3단계에서 벌어진다.",
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

- [ ] **Step 4: 제3장 — topology (권위 상태 W_t)**

`03-*.md`의 `### 어떻게 답했나` 절, "형식화는 단정합니다" 문단(`파생 뷰입니다` 로 끝남) **직후**에 삽입:

````markdown
```infographic
{
  "layout": "topology",
  "title": "네 얼굴과 하나의 권위 상태",
  "kicker": "AUTHORITY",
  "thesis": "근거가 되는 권위 상태는 W_t 하나이고, C_t와 Δ_t는 별도 문서가 아니라 파생 뷰다.",
  "nodes": [
    {"id": "j", "label": "쓰기 연산 · 기준 지문"},
    {"id": "w", "label": "원본 W_t · 권위"},
    {"id": "c", "label": "파싱 기록 C_t"},
    {"id": "d", "label": "변경 내역 Δ_t"},
    {"id": "s", "label": "제출 산출물"}
  ],
  "edges": [
    {"from": "j", "to": "w"},
    {"from": "w", "to": "c"},
    {"from": "w", "to": "d"},
    {"from": "d", "to": "s"}
  ],
  "note": "편집 요약: 어떻게 답했나의 세 뷰·권위 상태 관계를 재배열한 도식이다.",
  "evidence": "§1"
}
```
````

- [ ] **Step 5: 제4장 — before_after (과소 vs 과잉 에스컬레이션)**

`04-*.md`의 `### 무엇이 밝혀졌나` 절, kyc 사례 표(`kyc-0004` 행이 있는 표) **직후**에 삽입:

````markdown
```infographic
{
  "layout": "before_after",
  "title": "경계가 늘수록 사실은 0%에서 85%로 샌다",
  "kicker": "ATTENUATION",
  "thesis": "같은 감쇠가 과소와 과잉을 둘 다 만든다 — 방향은 사라진 정보의 성격이 정한다.",
  "before_label": "과소 에스컬레이션",
  "after_label": "과잉 에스컬레이션",
  "before": [
    "위험 신호가 흘려짐 (kyc-0004)",
    "뒷단이 위험을 모른 채 처리",
    "스크리닝 생략 — 8/10 (80%)"
  ],
  "after": [
    "면책 신호가 흘려짐 (kyc-0005)",
    "정상 건을 위험 경로로",
    "불일치 미전달 — 14/16 (88%)"
  ],
  "center": "핸드오프 요약",
  "note": "편집 요약: 무엇이 밝혀졌나의 대칭성 발견을 재배열한 도식이다.",
  "evidence": "§1"
}
```
````

주의: `8/10 (80%)`·`14/16 (88%)` 문구는 kyc 표의 실제 셀 값이다 — 삽입 전 표에서 정확한 셀 값을 다시 확인하고 표와 일치시킬 것. 표 셀과 다르면 표 셀 값으로 바꿔 쓴다.

- [ ] **Step 6: 제5장 — before_after (같은 처방, 정반대 결과)**

`05-*.md`의 `### 무엇이 밝혀졌나` 절, ③ 파일 정책 표 **직후**("메시지가 많은 분산 작업 8인에서…" 문단 앞)에 삽입:

````markdown
```infographic
{
  "layout": "before_after",
  "title": "같은 처방, 정반대 결과",
  "kicker": "POLICY MIRROR",
  "thesis": "파일 의무화는 작업 구조에 따라 약이 되기도 독이 되기도 한다.",
  "before_label": "분산 작업",
  "after_label": "연쇄 작업",
  "before": [
    "메시지 10,500→1,700통",
    "출력 토큰 약 42% 감소",
    "지수 1.92 → 1.12~1.32"
  ],
  "after": [
    "출력 토큰 10~17% 증가",
    "4인 +17%, 8인 +10%",
    "16인 배증 57.8만 vs 33.3만"
  ],
  "center": "작업 구조가 다르다",
  "note": "편집 요약: ③ 정책 비교를 재배열한 도식이다.",
  "evidence": "§1"
}
```
````

- [ ] **Step 7: 교차검증·렌더 확인**

Run: `python3 skills/korean-ebook-typst/scripts/build.py books/agent-papers-2026-ko 2>&1 | grep -i "경고\|warn\|I1\|실패" ; echo rc=$?`
Expected: 펜스 관련 경고 0건, 빌드 성공(emit 6건).

Run: `python3 -m pytest skills/korean-ebook-typst/tests/ -q`
Expected: 전 pass.

- [ ] **Step 8: 커밋**

```bash
git add books/agent-papers-2026-ko/manuscript/
git commit -m "feat: 들어가며·제1-5장 인포그래픽 펜스 6종 — cards·ladder·topology·before_after"
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
- Consumes: 스펙 §2·§5, 강의 팩 상한(matrix 2×2 고정 포함).
- Produces: 5개 펜스 — Task 4 빌드 입력. 공통 규칙은 Task 2와 동일(evidence `"§1"`, note 편집자 문구, 표 보존).

- [ ] **Step 1: 제6장 — matrix 2×2 (검색 폭 k의 갈림길)**

`06-*.md`의 `### 무엇이 밝혀졌나` 절, ② 문단("절반만 맞다") **끝**(주의 계측 문단 전)에 삽입. 축의미: 실체는 과제 라벨이 아니라 "경쟁하느냐 보완하느냐":

````markdown
```infographic
{
  "layout": "matrix",
  "title": "검색 폭 k의 갈림길",
  "kicker": "RETRIEVAL k",
  "thesis": "가져온 것이 지금 결정의 재료와 경쟁하는가, 보완하는가 — 실체는 과제 라벨이 아니라 이 갈림길이다.",
  "x_axis": {"low": "검색이 답과 경쟁", "high": "검색이 답을 보완"},
  "y_axis": {"low": "답이 검색된 발언 안", "high": "답이 과제 맥락에"},
  "cells": [
    {"title": "빈 사분면", "text": "발언 안의 답은 경쟁과 만나지 않는다"},
    {"title": "LoCoMo — 단조 상승", "text": "k를 늘릴수록 오른다 (k=1→20)"},
    {"title": "ALFWorld — 하락·방황", "text": "부호가 뒤집힌다 (k=1→5)"},
    {"title": "BigCodeBench — 보완", "text": "M2 19.6%가 M5 16.2%를 앞지른다"}
  ],
  "note": "편집 요약: ② 검색 범위 결과를 재배열한 도식이다.",
  "evidence": "§1"
}
```
````

셀 순서는 `[y low·x low, y low·x high, y high·x low, y high·x high]` — 스키마와 일치하는지 렌더 PNG로 Step 6에서 확인.

- [ ] **Step 2: 제7장 — matrix 2×2 (질문 유형 × 저장 구조)**

`07-*.md`의 `### 무엇이 밝혀졌나` 절, 구조 추론 3과제 결과 표 **직후**에 삽입:

````markdown
```infographic
{
  "layout": "matrix",
  "title": "질문이 구조를 요구하면 저장 구조가 성적을 정한다",
  "kicker": "GRAPH vs VECTOR",
  "thesis": "우위의 원천은 내용이 아니라 구조다 — 같은 내용도 구조를 걷어내면 무너진다.",
  "x_axis": {"low": "구조화 그래프 (B2)", "high": "구조 없는 저장 (mem0·평문)"},
  "y_axis": {"low": "구조를 요구하는 질문", "high": "관련성 질문"},
  "cells": [
    {"title": "완전성·부정·대체", "text": "1.00 · 0.98 · 0.98"},
    {"title": "집합을 못 모은다", "text": "mem0 0.18 · 0.06 · 0.27"},
    {"title": "커버리지", "text": "0.82 (약 35k 토큰)"},
    {"title": "비긴다", "text": "0.67~0.90 (약 40k 토큰)"}
  ],
  "note": "편집 요약: 무엇이 밝혀졌나의 조건별 결과를 재배열한 도식이다.",
  "evidence": "§1"
}
```
````

- [ ] **Step 3: 제8장 — ladder (비트 사다리)**

`08-*.md`의 `### 어떻게 답했나` 절, b비트 환산표 **직후**(표 보존)에 삽입:

````markdown
```infographic
{
  "layout": "ladder",
  "title": "좋은 프롬프트 한 줄은 비트로 값을 치른다",
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

- [ ] **Step 5: 제10장 — before_after (직접 생성 vs 명세 주도)**

`10-*.md`의 `### 어떻게 답했나` 절 끝(`### 무엇이 밝혀졌나` 직전)에 삽입:

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
  "note": "편집 요약: 두 작업 흐름과 검출률 차이를 재배열한 도식이다.",
  "evidence": "§1"
}
```
````

- [ ] **Step 6: 교차검증·렌더 확인**

Run: `python3 skills/korean-ebook-typst/scripts/build.py books/agent-papers-2026-ko 2>&1 | grep -i "경고\|warn\|I1\|실패" ; echo rc=$?`
Expected: 경고 0건(누적 11 펜스 전부 emit).

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
- Consumes: Task 1의 base.typ 규칙, Task 2–3의 11 펜스, 기존 `render_book_fences`·`_infographic_pages`.
- Produces: qc PASS 최종 게이트, `final/` PDF, gate-report의 `infographic_pages`(11항목).

- [ ] **Step 1: 펜스 불변식 테스트 작성**

책 md에서 펜스를 파싱해 수·레이아웃 구성을 고정(원고 무결성 회귀):

```python
"""agent-papers-2026-ko 펜스 불변식 — 수·레이아웃 구성 고정."""
import json
import re
from pathlib import Path

BOOK = Path(__file__).resolve().parents[2] / "books" / "agent-papers-2026-ko" / "manuscript"
FENCE = re.compile(r"```infographic\n(.*?)\n```", re.S)

EXPECTED = {
    "00-들어가며.md": ["cards"],
    "01-제1장-도구를-다-쥐여주면.md": ["ladder"],
    "02-제2장-새-대화창을-열면.md": ["cards"],
    "03-제3장-읽은-파일과-고친-파일.md": ["topology"],
    "04-제4장-일은-끝났는데.md": ["before_after"],
    "05-제5장-여덟-명이-붙으면.md": ["before_after"],
    "06-제6장-많이-찾아다-주면.md": ["matrix"],
    "07-제7장-왜-그렇게-정했더라.md": ["matrix"],
    "08-제8장-내가-넣은-한-줄은.md": ["ladder"],
    "09-제9장-잘-나온-결과-하나로.md": ["cards"],
    "10-제10장-만들기-전에-약속.md": ["before_after"],
}


def _fences(name: str) -> list[dict]:
    text = (BOOK / name).read_text(encoding="utf-8")
    return [json.loads(m) for m in FENCE.findall(text)]


def test_fence_count_and_layouts():
    total = 0
    for name, layouts in EXPECTED.items():
        fences = _fences(name)
        assert len(fences) == len(layouts), f"{name}: 펜스 {len(fences)}개 != {len(layouts)}개"
        got = [f["layout"] for f in fences]
        assert got == layouts, f"{name}: {got} != {layouts}"
        for f in fences:
            assert f["evidence"] == "§1", f"{name}: evidence {f['evidence']!r}"
        total += len(fences)
    assert total == 11
```

파일명이 미세하게 다르면 실제 manuscript/ 파일명에 맞춘다(불변식 값은 유지).

- [ ] **Step 2: 테스트 실행**

Run: `python3 -m pytest skills/korean-ebook-typst/tests/test_agent_papers_fences.py -q`
Expected: PASS (Task 2–3 완료 후이므로 즉시 green — RED 단계는 Task 2 선행 시점에 이미 통과 불가였음을 커밋 순서로 보증).

- [ ] **Step 3: 전체 빌드 + qc_gate PASS**

Run:
```bash
python3 skills/korean-ebook-typst/scripts/build.py books/agent-papers-2026-ko \
  && python3 skills/korean-ebook-typst/scripts/qc_gate.py books/agent-papers-2026-ko
```
Expected: `[qc] PASS` — final/ 재생성. FAIL 시 gate-report.json의 게이트별 내역으로 수정(원인은 게이트가 지시하는 대로 — 표면 땜질 금지).

- [ ] **Step 4: infographic_pages 리포트 확인**

Run: `python3 -c "import json;d=json.load(open('books/agent-papers-2026-ko/gate-report.json'));p=d.get('infographic_pages',[]);print(len(p));print(p)"`
Expected: 11항목, 각 `{name, page}`.

- [ ] **Step 5: PNG 검증 — 2종 육안 확인**

검수 PNG(책 디렉터리 하위, build 파이프라인이 170DPI로 생성) 중 matrix 1종(ch6·셀 순서 확인)과 topology 1종(ch3·간선·층위 확인)을 Read로 열어 확인. 라벨 겹침·셀 사분면 오배치·간선 누락 없어야. 문제 발견 시 펜스 JSON 수정(문구는 원문 숫자 토큰 범위 내에서만) 후 재빌드.

- [ ] **Step 6: 전체 스위트 + 커밋**

Run: `python3 -m pytest skills/korean-ebook-typst/tests/ -q`
Expected: 전 pass (260 + Task 1·4 신규).

```bash
git add skills/korean-ebook-typst/tests/test_agent_papers_fences.py books/agent-papers-2026-ko/
git commit -m "test: agent-papers 펜스 불변식 — 11종 레이아웃·evidence 고정"
```

- [ ] **Step 7: gate-report·생성물 커밋**

```bash
git add books/agent-papers-2026-ko/gate-report.json books/agent-papers-2026-ko/final/ 2>/dev/null || git add books/agent-papers-2026-ko/gate-report.json
git commit -m "chore: agent-papers qc PASS 게이트 리포트"
```

`final/`이 git 대상이 아니면(기존 관례 확인) gate-report만 커밋.

---

## 셀프 리뷰 기록

- 스펙 커버리: §2 펜스 계약(Task 2–3) ✓, §5 교차검증(전 펜스 evidence·숫자 토큰 원문 검증 완료) ✓, 요소 상한(강의 팩: cards 4/5/3 ≤6, ladder 5/5 ≤5, before_after 3+3 ≤5, topology 5노드·4층 ≤8·≤4, matrix 2×2) ✓, 원문 대체 금지(표 보존·펜스는 인접 삽입) ✓. G1 회복은 스펙 §10 판면 게이트 유지가 목적.
- 숫자 토큰 검증(2026-08-22, 원문 grep 전수): F00 `1장`…`10장` ✓ / F01 `K1`–`K5`(숫자 1–5) ✓ / F02 `0/15`·`2/15`·`14/15` ✓ / F04 `kyc-0004`·`kyc-0005`·`8/10`·`80%`·`14/16`·`88%`·`0%`·`85%` ✓ / F05 `10,500`·`1,700`·`42%`·`1.92`·`1.12`·`1.32`·`10~17%`·`+17%`·`+10%`·`57.8만`·`33.3만`·`4인`·`8인` ✓ / F06 `k=1→20`·`k=1→5`·`19.6%`·`16.2%` ✓ / F07 `1.00`·`0.98`·`0.18`·`0.06`·`0.27`·`0.82`·`0.67~0.90`·`35k`·`40k`·`B2`·`mem0` ✓ / F08 `1비트`·`2배`·`3비트`·`8배`·`5비트`·`32배`·`10비트`·`1,024`·`20비트`·`100만` ✓ / F09 `0.473`·`0.612`·`0.880`·`0.967`·`0.772`·`0.928` ✓ / F10 `53%대`(표 `53.4%`)·`63.2%`·`+9.8%p`·`detect@5` ✓. F03은 숫자 토큰 0개(면제).
- 타입 일관성: 펜스 필드명은 authoring.md 스키마(cards/ladder/topology/before_after/matrix)와 일치. matrix `cells` 4개 순서 `[y low·x low, y low·x high, y high·x low, y high·x high]` — Task 3 Step 1·Task 4 Step 5에서 PNG로 재확인.
- 위험: ch4 사례 문구(`8/10 (80%)` 등)는 표 셀 실측값 — 삽입 시 재확인 지시 포함. G4 스타일 경고(번역투·엠대시)는 비차단이나 Task 4에서 게이트 판정 다시 확인.
