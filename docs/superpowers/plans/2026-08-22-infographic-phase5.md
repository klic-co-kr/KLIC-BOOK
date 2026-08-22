# 인포그래픽 Phase 5 — composite·infographic_pages 리포트·가이드 완성 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 스펙 §3.5 복합 씬(composite) archetype + §5.4 검수 렌더·`infographic_pages` 리포트 + §8.5 가이드 완성으로 인포그래픽 레이어를 완성한다(Phase 4 최종 리뷰 LOW 2건 이관 해소 포함).

**Architecture:** composite는 기존 9 archetype의 `dispatch`를 재사용해 모듈 FigModel을 측정·병합(세로 스택, 배분 초과 시 모듈 단위 분할 에러). 페이지 대응은 각 도식 typ 앞 `#metadata((kind:"ig-fig", name:…, page: here().page()))` 프리픽스 → `typst query`로 수집 → `gate-report.json`의 `infographic_pages` 필드 + 검수 PNG(170 DPI) 렌더.

**Tech Stack:** Python 3.12 표준 라이브러리(재결정론 — 외부 의존 추가 없음), typst 0.15.1(query·compile `--pages`/`--ppi`), pytest. PyMuPDF(qc_gate 기존 사용) 페이지 수 대조.

**Spec:** `docs/superpowers/specs/2026-08-21-infographic-layer-design.md` (§3.4·§3.5·§5.4·§8.5; 본 플랜의 스펙 개정 6판 항 포함)

## Global Constraints

- 결정론: 동일 펜스 JSON + tokens → 바이트 동일 typst. datetime/random 금지.
- 모든 방출 숫자는 `_n()` = `f"{v:.2f}"`.
- 골든은 바이트 정확. 기존 골든 9종 바이트 불변(Task 3 rings 골든 1종 **신규 추가**만 허용).
- 손패치 금지 — 생성 typst/PDF 직수정 없음.
- 테스트 실행은 항상 스코프: `python3 -m pytest skills/korean-ebook-typst/tests/ -q`(루트 pytest는 books/ import SystemExit로 깨짐).
- 테스트 문구·에러 메시지 한국어. 커밋 컨벤션(`feat:`/`fix:`/`docs:`/`test:`), attribution footer 없음.
- 토큰 로드 관례: 테스트는 `json.loads((Path(__file__).resolve().parents[1] / "styles" / "<pack>" / "tokens.json").read_text(encoding="utf-8"))` 인라인(공용 fixture 부재).
- cli preview `--fig`는 **1-기반**(md2typst.py:23 `"index": len(fences) + 1`).
- ladder 4단계 practical 도식 총높이 = H_frame(518.74)·0.85 − P(14) = **426.93pt**(ladder 대수 — 도식 높이가 85% 상한 440.93에서 패딩 14pt를 뺀 값에 도달). composite 배분 에러 테스트의 결정론 근거(검토 G2·G3 수치 재현 합치).
- 이관 과제(Phase 4 최종 리뷰 LOW): ① 별칭 사용 경고(스펙 §3.4 "경고 로그" 미구현 — parse `data["_alias"]` 미소비) ② rings 변형 바이트 골든 부재.

---

### Task 1: composite archetype

**Files:**
- Modify: `skills/korean-ebook-typst/scripts/infographic/parse.py`(composite 분기 + VALID_LAYOUTS 밖 별도 집합)
- Create: `skills/korean-ebook-typst/scripts/infographic/archetypes/composite.py`
- Modify: `skills/korean-ebook-typst/scripts/infographic/layout.py`(dispatch composite)
- Modify: `skills/korean-ebook-typst/scripts/infographic/lint.py`(모듈 필드 전개)
- Modify: `skills/korean-ebook-typst/scripts/infographic/render.py`(`_sheet_rows` 모듈 전개)
- Test: `skills/korean-ebook-typst/tests/test_infographic_layout_composite.py`(신규)
- Spec: `docs/superpowers/specs/2026-08-21-infographic-layer-design.md`(개정 6판 — 아래 Step 0)

**Interfaces:**
- Consumes: `dispatch(Fence, tokens) -> FigModel`(layout.py:10), `Fence(index, line, layout, title, thesis, kicker, note, evidence, data)`(parse.py:38), `sizes(tokens)`(base.py), `LayoutError`(base.py)
- Produces: `composite.layout(fence, tokens) -> FigModel`; `parse` composite 정규화 `data["modules"]`(각 모듈 dict: slot·layout·아키타입 payload 그대로); `lint`/`render` 모듈 필드 경로 `modules[j].<아키타입 경로>`; Task 2·4가 소비

**설계 판정(컨트롤러 — 스펙 해석, 검토 wave 반영):**
1. composite 최상위 `title`/`kicker`는 **선택**(스펙 §3.5 예시에 없음). 모듈이 각자 아키타입 헤더(자기 title)를 렌더한다 — 모듈 title은 각 아키타입 스키마 준수(필수 — 재귀 parse_fence가 검증). 최상위 title 있으면 composite가 kicker+title 블록을 추가(중심좌표·line_count·max_w·field 관례는 기존 archetype과 동일). 최상위 `note`는 **검수 시트 고지로만 소비** — 모듈은 각자 note(미지정 시 DEFAULT_NOTE)를 렌더한다(archetype 단일 진실 불침범, 도식에 고지 2~3회 노출은 의도된 동작). **개정 6판에 명시**.
2. "보조 모듈 축소" 자동 단계는 구현하지 않는다 — 글자·화살표 축소 금지(§3.5)와 모순되는 자동 축소 레버가 없다. 배분 초과 즉시 **모듈 단위 분할 에러**. **스펙 개정 6판**으로 §3.5 문장 교정(Step 0).
3. 모듈 페이로드 검증은 **parse_fence 재귀 재사용** — composite 분기가 각 모듈 payload(슬롯 키 제거)를 `parse_fence`에 다시 통과시켜 개수 상한·스키마 검증을 전수 승계한다(`_module_fence` 직접 생성은 상한 검증 우회 — 검토 G3-M4). 재귀 깊이 1(composite는 모듈 layout에서 제외).
4. 배분: **헤더 선차감** — 최상위 title/kicker 블록 높이 `head_h`를 먼저 계산하고 `H_avail = (y1−y0)·0.85 − head_h`(검토 G1-H1: 미차감 시 총량이 85% 한도를 넘는다). `alloc_primary = min(측정높이, 0.6·H_avail)`, 보조 각 `alloc = (H_avail − alloc_primary − GAP·(n−1)) / n_supporting`(n=모듈 수). 반환 직전 총량 방어 `fig.height > (y1−y0)·0.85` → 에러(산술상 도달 불가지만 §4.1 요건의 명시적 방어선).
5. 에러 스키마는 개정 6판이 2종으로 확정: supporting — 스펙 원문 그대로 "`{slot} {layout} 측정높이 {h}pt > 배분 {H}pt — 보조 모듈 n을 별도 펜스로 분할 권장`"; primary — "`{slot} {layout} 측정높이 {h}pt > 배분 {H}pt — 주 모듈 요소 수 감소 또는 펜스 분할 권장`". 포맷 지정자(`:.2f`)는 구현 세부 — 스펙 문구는 `{h}pt` 표기 유지.
6. 모듈 재귀 금지는 **전 슬롯**(primary 포함) — 메시지 "모듈 재귀 금지". 개정 6판에 명시.

- [ ] **Step 0: 스펙 개정 6판**

`docs/superpowers/specs/2026-08-21-infographic-layer-design.md` 다섯 곳:

(a) §3.5 "공간 부족 시" 문단 교체:

```markdown
- 공간 부족 시: **모듈 단위 분할 에러**(자동 축소 없음 — 글자·화살표
  축소 금지와 모순되는 레버가 없다. 개정 6판).
  메시지 스키마: `{모듈 슬롯} {layout} 측정높이 {h}pt > 배분 {H}pt
  — 보조 모듈 n을 별도 펜스로 분할 권장`(보조) /
  `… — 주 모듈 요소 수 감소 또는 펜스 분할 권장`(주).
```

(b) §5.4 `build_report.json` → `gate-report.json`(구현 실제 명칭 — qc_gate.py:224). §5.4 1회뿐이다(다른 occurrence 없음 — grep 확인).

(c) §3.5에 2줄 추가: "최상위 title/kicker는 선택(모듈이 각자 아키타입 헤더를 렌더한다 — 모듈 title은 각 아키타입 스키마 준수). 모듈 layout에 composite는 전 슬롯(primary 포함) 금지."

(d) 문서 제목 판수 갱신 "(개정 5판)" → "(개정 6판)" + §10 개정 이력에 항목 추가: "개정 6판(2026-08-22): composite 자동 축소 제거·에러 스키마 2종 확정, 최상위 title 선택·모듈 재귀 전 슬롯 금지 명시, 리포트 명칭 gate-report 정합, 치트시트 practical 기준 명시."

(e) §8 치트시트 항목에 "(practical 기준)" 명시 — 전 팩형 수치 확장은 본 플랜 범위 밖.

커밋(스펙 단독 — Task 1 코드 커밋은 스펙 미포함): `docs: 스펙 개정 6판 — composite 축소 제거·title 선택·명칭 정합`

- [ ] **Step 1: 실패 테스트 작성**

`tests/test_infographic_layout_composite.py` 신규:

```python
"""composite — 복합 씬(스펙 §3.5): 모듈 측정·배분·세로 스택·분할 에러."""
import json
import sys
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))

from scripts.infographic.archetypes import composite as comp_arch
from scripts.infographic.layout import dispatch
from scripts.infographic.parse import ParseError, parse_fence

TOKENS = json.loads((SKILL / "styles" / "practical" / "tokens.json").read_text(encoding="utf-8"))

CARDS3 = {"layout": "cards",
          "title": "근거 카드 셋",
          "cards": [{"title": f"카드 {i}", "text": f"근거 문장 {i}."} for i in range(1, 4)]}
FLOW2 = {"layout": "flow", "title": "적용 절차",
         "steps": [{"title": "준비", "text": "전제를 확인한다."},
                   {"title": "실행", "text": "절차를 수행한다."}]}
LADDER4 = {"layout": "ladder", "title": "성숙도 계단", "thesis": "단계마다 확신이 쌓인다",
           "stages": [{"title": f"단계 {i}", "text": f"{t} 상태를 넘어선다."}
                      for i, t in enumerate(["사각", "관심", "실행", "정착"], 1)]}


def _fence(modules, title="구성과 절차를 한 장에 담는다", pack_tokens=TOKENS, **kw):
    body = {"layout": "composite", "modules": modules}
    if title is not None:
        body["title"] = title
    body.update(kw)
    f = parse_fence(1, 1, json.dumps(body, ensure_ascii=False))
    return f


def test_parse_bounds():
    with pytest.raises(ParseError):
        _fence([dict(CARDS3, slot="primary")])                     # 보조 0 — 모듈 2~3
    with pytest.raises(ParseError):
        _fence([dict(CARDS3, slot="primary")] +
               [dict(FLOW2, slot="supporting")] * 3)               # 보조 3 — 상한 2
    with pytest.raises(ParseError):
        _fence([dict(CARDS3, slot="main"),                         # slot 오타
                dict(FLOW2, slot="supporting")])
    with pytest.raises(ParseError):
        _fence([dict(CARDS3, slot="primary"), dict(FLOW2, slot="primary")])  # primary 2개
    with pytest.raises(ParseError):
        _fence([dict(CARDS3, slot="primary"),
                dict(LADDER4, slot="supporting", layout="composite")])      # 재귀
    with pytest.raises(ParseError):
        parse_fence(1, 1, json.dumps({"layout": "composite", "modules": [
            {"slot": "primary", "layout": "nope"}]}, ensure_ascii=False))   # unknown


def test_stack_geometry_and_gap():
    # title=None — fig.height = 모듈 높이 합 + GAP 정확히(헤더 블록 없음)
    f = _fence([dict(CARDS3, slot="primary"), dict(FLOW2, slot="supporting")], title=None)
    fig = comp_arch.layout(f, TOKENS)
    c = dispatch(_to_fence(1, 1, CARDS3), TOKENS)
    fl = dispatch(_to_fence(1, 1, FLOW2), TOKENS)
    assert abs(fig.height - (c.height + comp_arch.GAP + fl.height)) < 0.01


def test_title_block_adds_height_and_no_title_omits_it():
    mods = [dict(CARDS3, slot="primary"), dict(FLOW2, slot="supporting")]
    with_t = comp_arch.layout(_fence(mods), TOKENS)
    without = comp_arch.layout(_fence(mods, title=None), TOKENS)
    assert with_t.height > without.height            # 최상위 title 블록만큼 증가
    texts = [op.text for op in with_t.ops if op.__class__.__name__ == "TextOp"]
    assert "구성과 절차를 한 장에 담는다" in texts
    texts_wo = [op.text for op in without.ops if op.__class__.__name__ == "TextOp"]
    assert "구성과 절차를 한 장에 담는다" not in texts_wo


def test_total_height_within_85_percent_even_with_title():
    # G1-H1 방어: 헤더 포함 총량도 85% 한도 내 — H_avail이 헤더를 선차감한다
    frame = TOKENS["body_frame_pt"]
    cap = (frame["y1"] - frame["y0"]) * 0.85
    f = _fence([dict(CARDS3, slot="primary"), dict(FLOW2, slot="supporting")])
    assert comp_arch.layout(f, TOKENS).height <= cap + 0.01


def _to_fence(index, line, d):
    body = dict(d)
    f = parse_fence(index, line, json.dumps(body, ensure_ascii=False))
    return f


def test_primary_over_sixty_percent_error():
    # ladder 4단계 practical = 프레임 85%(426.93) 점유 — 60% 상한 초과 확정
    f = _fence([dict(LADDER4, slot="primary"), dict(FLOW2, slot="supporting")])
    with pytest.raises(comp_arch.CompositeLayoutError, match="primary ladder 측정높이"):
        comp_arch.layout(f, TOKENS)


def test_supporting_over_allocation_error():
    # 보조 ladder 4단계(≈426.93)는 어떤 배분과도 초과 — 확정 에러
    f = _fence([dict(CARDS3, slot="primary"), dict(LADDER4, slot="supporting")])
    with pytest.raises(comp_arch.CompositeLayoutError, match="supporting ladder 측정높이"):
        comp_arch.layout(f, TOKENS)


def test_determinism():
    f = _fence([dict(CARDS3, slot="primary"), dict(FLOW2, slot="supporting")])
    a = comp_arch.layout(f, TOKENS)
    b = comp_arch.layout(_fence([dict(CARDS3, slot="primary"), dict(FLOW2, slot="supporting")]), TOKENS)
    assert [(op.__class__.__name__, getattr(op, "x", None), getattr(op, "y", None))
            for op in a.ops] == [(op.__class__.__name__, getattr(op, "x", None), getattr(op, "y", None))
                                 for op in b.ops]
```

주: `LADDER4`·`CARDS3`·`FLOW2` 페이로드는 각 archetype의 확정 스키마를 따른다(`stages[i].title/text`, `cards[i].title/text`, `steps[i].title/text` — `_sheet_rows` 경로와 일치). 실행 시 실제 필수 필드(예: ladder thesis)가 더 있으면 `test_infographic_layout_ladder.py` 등 기존 테스트의 펜스 형태를 복제해 채운다 — 배분 에러 테스트의 결정론(426.93pt 점유)은 stages 4개(practical PACK_STAGES=5 이하)가 유지하는 한 불변.

- [ ] **Step 2: RED 확인**

Run: `python3 -m pytest skills/korean-ebook-typst/tests/test_infographic_layout_composite.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'scripts.infographic.archetypes.composite'`

- [ ] **Step 3: parse composite 분기 + composite.py + dispatch + lint/render 전개**

`parse.py` — 두 곳:

(1) 최상위 게이트 완화(공통 추출부 앞쪽 — 실제 줄 위치는 코드에서 확인):
`layout not in VALID_LAYOUTS` 검사 → `layout not in VALID_LAYOUTS and layout != "composite"`; title 필수 검사 → `if not title and layout != "composite":`.

(2) composite 구조 분기(다른 layout 분기와 동급 — accumulator 관례):

```python
if layout == "composite":
    mods = d.get("modules")
    if not isinstance(mods, list) or not (2 <= len(mods) <= 3):
        raise ParseError(index, "composite modules — 주 1 + 보조 1~2(2~3개 배열)", line)
    seen_slots = []
    mod_fences = []
    for j, m in enumerate(mods):
        if not isinstance(m, dict):
            raise ParseError(index, f"modules[{j}] — 객체여야 한다", line)
        slot = m.get("slot")
        if slot not in ("primary", "supporting"):
            raise ParseError(index, f"modules[{j}].slot {slot!r} — primary|supporting", line)
        mlayout = m.get("layout")
        if mlayout == "composite":
            raise ParseError(index, f"modules[{j}].layout composite — 모듈 재귀 금지(전 슬롯)", line)
        if mlayout not in VALID_LAYOUTS:
            raise ParseError(index, f"modules[{j}].layout {mlayout!r} — 알 수 없는 layout", line)
        # 모듈 페이로드를 parse_fence에 재통과 — 개수 상한·스키마 검증 전수 승계(판정 3)
        payload = {k: v for k, v in m.items() if k != "slot"}
        mf = parse_fence(index, line, payload if isinstance(payload, dict)
                         else payload)   # body 인자형(str이면 json.dumps(payload, ensure_ascii=False))
        mf.data["_slot"] = slot          # data 여분 키 — "_alias"와 동일 관례(archetype은 무시)
        seen_slots.append(slot)
        mod_fences.append(mf)
    if seen_slots.count("primary") != 1:
        raise ParseError(index, f"primary 정확히 1개 필요(현재 {seen_slots.count('primary')})", line)
    data["modules"] = mod_fences
```

(모듈 payload에 포함된 title은 각 아키타입 스키마대로 필수 — 재귀 parse_fence가 검증한다.)

`archetypes/composite.py`:

```python
"""composite — 복합 씬(스펙 §3.5): 모듈 측정·배분 검증·세로 스택. 자동 축소 없음(개정 6판)."""
from __future__ import annotations

import dataclasses

from .. import budget, layout as _layout
from ..model import FigModel, TextOp
from ..parse import Fence
from .base import LayoutError, sizes

GAP = 24.0
PRIMARY_FRAC = 0.6
HEIGHT_LIMIT = 0.85
LEADING = 1.3
PAD = 14.0
_OFFY = ("y", "y1", "y2")   # 세로 이동 대상 필드 — ArrowOp(x1,y1,x2,y2) 등 전 커버


class CompositeLayoutError(LayoutError):
    pass


def _head_h(fence: Fence, tokens: dict) -> float:
    """최상위 헤더 블록 높이 — kicker 1줄 + title 실측 줄 수 + 하단 여백 10pt."""
    frame = tokens["body_frame_pt"]
    W = frame["x1"] - frame["x0"]
    s = sizes(tokens)
    pack = tokens.get("style", "practical")
    h = 0.0
    if fence.kicker:
        h += s["kicker"] * LEADING
    if fence.title:
        h += budget.line_count(fence.title, W - 2 * PAD, s["title"], 0.0, pack) \
            * s["title"] * LEADING + 10.0
    return h


def layout(fence: Fence, tokens: dict) -> FigModel:
    frame = tokens["body_frame_pt"]
    H_frame = frame["y1"] - frame["y0"]
    s = sizes(tokens)
    head_h = _head_h(fence, tokens)
    H_avail = H_frame * HEIGHT_LIMIT - head_h      # 헤더 선차감(판정 4 — G1-H1)
    mods = fence.data["modules"]                   # parse가 Fence 리스트로 정규화(판정 3)
    figs = [(m, _layout.dispatch(m, tokens)) for m in mods]

    prim = [(m, g) for m, g in figs if m.data["_slot"] == "primary"][0]
    if prim[1].height > H_avail * PRIMARY_FRAC:
        raise CompositeLayoutError(
            f"primary {prim[0].layout} 측정높이 {prim[1].height:.2f}pt "
            f"> 배분 {H_avail * PRIMARY_FRAC:.2f}pt — 주 모듈 요소 수 감소 또는 펜스 분할 권장")

    alloc_supp = (H_avail - min(prim[1].height, H_avail * PRIMARY_FRAC)
                  - GAP * (len(figs) - 1)) / max(1, len(figs) - 1)
    for m, g in figs:
        if m.data["_slot"] == "supporting" and g.height > alloc_supp:
            raise CompositeLayoutError(
                f"supporting {m.layout} 측정높이 {g.height:.2f}pt > 배분 {alloc_supp:.2f}pt"
                f" — 보조 모듈 {len(figs) - 1}을(를) 별도 펜스로 분할 권장")

    W = frame["x1"] - frame["x0"]
    head: list[TextOp] = []
    y = 0.0
    if fence.kicker:
        head.append(TextOp(x=W / 2, y=y + s["kicker"] * LEADING / 2, size=s["kicker"],
                           text=fence.kicker, role="ink-mute", field="kicker"))
        y += s["kicker"] * LEADING
    if fence.title:
        t_lines = budget.line_count(fence.title, W - 2 * PAD, s["title"], 0.0,
                                    tokens.get("style", "practical"))
        head.append(TextOp(x=W / 2, y=y + t_lines * s["title"] * LEADING / 2, size=s["title"],
                           text=fence.title, role="ink", weight="bold", max_w=W - 2 * PAD,
                           field="title"))
        y += t_lines * s["title"] * LEADING + 10.0
    ops: list = list(head)
    for i, (m, g) in enumerate(figs):
        for op in g.ops:
            # 세로 이동은 y·y1·y2 전부 — RectOp.y만 옮기면 ArrowOp이 원 위치에 남는다(G3-H2)
            ops.append(dataclasses.replace(
                op, **{k: getattr(op, k) + y for k in _OFFY if hasattr(op, k)}))
        y += g.height
        if i < len(figs) - 1:
            y += GAP
    if y > H_frame * HEIGHT_LIMIT + 0.01:          # §4.1 총량 방어(판정 4)
        raise CompositeLayoutError(
            f"도식 높이 {y:.2f}pt > 프레임 {H_frame * HEIGHT_LIMIT:.2f}pt(85%) — 펜스 분할 권장")
    return FigModel(width=W, height=y, ops=tuple(ops), source_index=fence.index)
```

주: 임포트 순환(layout ↔ composite)은 함수 본문에서만 `_layout.dispatch`에 접근하므로 안전(모듈 로드 시점 참조 아님) — 기존 archetypes가 `.. budget`을 임포트하는 것과 같은 위상. `dataclasses.replace`는 dataclass 오퍼이션 전 필드 치환 재구성(불변).

`layout.py` dispatch에:

```python
    if fence.layout == "composite":
        return _comp.layout(fence, tokens)
```

(import행에 `composite as _comp` 추가.)

`lint.py` 필드 평탄 수집부·`render.py` `_sheet_rows` — 기존 9종 루프를 그대로 두고 composite만 추가하면 9루프 3중 복제(lint·render·모듈)가 된다. 대신 **헬퍼 추출**: 양 파일의 필드 수집 루프를 동일 인자 `(title, kicker, thesis, data, prefix) -> list[tuple[str, str]]` 함수로 묶는다(`render.py`는 `_sheet_rows` 내부에서 이미 2-튜플 반환 — 그 본체를 `rows_from(title, kicker, thesis, data, prefix)`로 추출, 기존 경로는 `rows_from(f.title, f.kicker, f.thesis, f.data, "")` 호출. `lint.py`의 필드 수집부도 동일 구조로 추출해 동일 함수를 쓰려면 순환 임포트 주의 — lint가 render에서 임포트하지 않고 **각자 자기 파일에 유지**하되 동일 prefix 관계). composite 분기(모듈은 parse가 Fence로 정규화 — `m.title`·`m.kicker`·`m.thesis`·`m.data` 속성):

```python
    for j, m in enumerate(f.data.get("modules", [])):
        rows.extend(rows_from(m.title, m.kicker, m.thesis, m.data, f"modules[{j}]."))
```

경로 예: `ch01.md #1 modules[0].cards[0].title`. (rows_from 본체가 모듈 data의 `_slot`·`_alias` 여분 키는 건너뛰도록 — 기존 루프가 특정 키만 읽으므로 자동 만족.)

- [ ] **Step 4: GREEN 확인**

Run: `python3 -m pytest skills/korean-ebook-typst/tests/test_infographic_layout_composite.py -q`
Expected: PASS 전 건(함수 7). 이후 전체: `python3 -m pytest skills/korean-ebook-typst/tests/ -q` — 기존 239 + 신규 7 = **246 passed**(골든·기존 무변경).

- [ ] **Step 5: 검수 시트 모듈 전개 + composite 바이트 골든**

같은 파일에 추가:

```python
def test_sheet_rows_reach_module_fields():
    from scripts.infographic import render as ig_render
    f = _fence([dict(CARDS3, slot="primary"), dict(FLOW2, slot="supporting")])
    rows = dict(ig_render._sheet_rows(f))
    assert rows["modules[0].cards[0].title"] == "카드 1"
    assert rows["modules[1].steps[0].title"] == "준비"


GOLDEN = Path(__file__).parent / "fixtures" / "infographic" / "golden-composite-practical.typ"


def test_composite_golden():
    import os
    from scripts.infographic import emit
    fig = comp_arch.layout(_fence([dict(CARDS3, slot="primary"),
                                   dict(FLOW2, slot="supporting")]), TOKENS)
    typ = emit.render_typ(fig)
    if not GOLDEN.exists():
        if not os.environ.get("IG_REGEN_GOLDEN"):
            pytest.fail("골든 부재 — IG_REGEN_GOLDEN=1로 재생성")
        GOLDEN.write_text(typ, encoding="utf-8")
        pytest.fail("골든 재생성 — 눈검(모듈 헤더 2개·24pt 간격·노트 2개) 후 커밋")
    assert GOLDEN.read_text(encoding="utf-8") == typ
```

Run: `IG_REGEN_GOLDEN=1 python3 -m pytest ...composite.py -q` → 골든 재생성 fail → **눈검**(`typst compile` 스크린 또는 emit 출력 육안 — 카드+플로우 스택·간격·헤더·**flow 화살표가 플로우 모듈 영역에 위치**·노트 2개) → 재실행 PASS. 전체: **248 passed**. 커밋(골든 fixture 포함 — 스펙은 제외, Step 0에서 단독 커밋됨):

```bash
git add skills/korean-ebook-typst/scripts/infographic skills/korean-ebook-typst/tests/test_infographic_layout_composite.py skills/korean-ebook-typst/tests/fixtures/infographic/golden-composite-practical.typ
git commit -m "feat: composite archetype — 모듈 측정·배분 검증·세로 스택"
```

---

### Task 2: infographic_pages 리포트 + 검수 렌더 PNG

**Files:**
- Modify: `skills/korean-ebook-typst/scripts/infographic/render.py`(metadata 프리픽스 + manifest.json)
- Modify: `skills/korean-ebook-typst/scripts/qc_gate.py`(query 수집·gate-report `infographic_pages`·PNG 170 DPI)
- Test: `skills/korean-ebook-typst/tests/test_infographic_pages_report.py`(신규)

**Interfaces:**
- Consumes: `render_book_fences(book_dir, build, cfg) -> dict[int, dict[int, str]]`(render.py:31), `typst_binary()`(build.py), gate-report.json 라이터(qc_gate.py:224), PyMuPDF(qc_gate 기존)
- Produces: `build/infographic/manifest.json`(이름·챕터·펜스 인덱스 배열); `gate-report.json` 필드 `"infographic_pages": {"count": N, "expected": M, "match": bool, "figs": [{"name","chapter","index","page"}]}`; `build/infographic/review-pNNN.png`(도식 페이지 170 DPI). Task 4 통합이 소비.

**설계 판정:** 페이지 대응 = 각 도식 typ 첫 줄 `#context metadata((kind: "ig-fig", name: "<name>", page: here().page()))` — `#context` 없으면 typst 0.15.1이 "can only be used when context is known" 컴파일 에러로 전 도식 붕괴(검토 G3-C1 실증). 수집은 `typst query <main.typ> metadata --field value --root <build>` — **stdout은 JSON 배열 하나**(줄 단위 아님 → `json.loads(r.stdout or "[]")`; deprecation 경고는 stderr). PNG는 도식이 실린 **unique 페이지**별 1장(`typst compile main.typ review-pNNN.png --pages N --ppi 170 --root build`). 페이지 대응 일치 검사는 수집 count+**page가 실제 PDF 페이지 범위 내** 두 축(§5.4 "실제 페이지 수와의 일치 검사").

**호출 계약:** 테스트의 `assemble`·`compile_pdf`·`qc_gate.run` 호출 시그니처·인자는 기존 `tests/test_build_compile.py`(assemble+compile_pdf in-process)와 `tests/test_qc_gate.py`(qc_gate.run)가 쓰는 호출을 **그대로 복제**한다(아래 코드의 `b.assemble(cfg, book)` 등은 의사 코드 — 실제 인자 순서·cfg 키·리턴값은 해당 파일에서 확인해 대체).

- [ ] **Step 1: 실패 테스트 작성**

```python
"""infographic_pages 리포트(스펙 §5.4 개정 6판) — metadata 페이지 매핑·일치 검사·PNG 렌더."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))

from scripts.infographic import emit, render as ig_render

try:
    from scripts.build import typst_binary  # noqa: E402
    TYPST = typst_binary()   # typst 부재 시 build._fail이 SystemExit(1) — 수용해 skip
except SystemExit:
    TYPST = None

BOOK = """# 검증용 장

```infographic
{"layout": "flow", "title": "절차는 두 단계로 끝난다",
 "steps": [{"title": "준비", "text": "전제를 확인한다."},
           {"title": "실행", "text": "절차를 수행한다."}]}
```

본문 산문 한 줄.
"""


def _book(tmp_path: Path) -> Path:
    (tmp_path / "typst-build.yaml").write_text(
        "title: 검증책\nsubtitle: 부제\nauthor: 저자\nstyle: practical\ncover: auto\n"
        "chapters: [ch01.md]\n", encoding="utf-8")
    (tmp_path / "ch01.md").write_text(BOOK, encoding="utf-8")
    return tmp_path


pytestmark = pytest.mark.skipif(not TYPST or not Path(TYPST).exists(), reason="typst 없음")


def test_manifest_and_metadata_prefix(tmp_path):
    import scripts.build as b
    book = _book(tmp_path)
    cfg = {"title": "검증책", "subtitle": "부제", "author": "저자", "style": "practical",
           "cover": "auto", "chapters": ["ch01.md"]}
    main_typ = b.assemble(cfg, book)
    build = book / "build"
    manifest = json.loads((build / "infographic" / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["count"] == 1
    fig = manifest["figs"][0]
    assert fig["name"] == "000-fig01.typ" and fig["index"] == 1
    body = (build / "infographic" / fig["name"]).read_text(encoding="utf-8")
    assert body.splitlines()[0] == ('#context metadata((kind: "ig-fig", name: "000-fig01.typ", '
                                    'page: here().page()))')


def test_query_reports_page_and_gate_field(tmp_path):
    import scripts.build as b
    from scripts import qc_gate
    book = _book(tmp_path)
    cfg = {"title": "검증책", "subtitle": "부제", "author": "저자", "style": "practical",
           "cover": "auto", "chapters": ["ch01.md"]}
    main_typ = b.assemble(cfg, book)
    b.compile_pdf(main_typ, "검증책")
    rc = qc_gate.run(book)
    assert rc == 0
    report = json.loads((book / "gate-report.json").read_text(encoding="utf-8"))
    igp = report["infographic_pages"]
    assert igp["count"] == 1 and igp["expected"] == 1 and igp["match"] is True
    page = igp["figs"][0]["page"]
    assert isinstance(page, int) and page >= 1
    import fitz
    doc = fitz.open(book / "draft" / "검증책.pdf")
    assert page <= doc.page_count
    pngs = sorted((book / "build" / "infographic").glob("review-p*.png"))
    assert len(pngs) == len({f["page"] for f in igp["figs"]})
    assert pngs and pngs[0].stat().st_size > 10_000
```

- [ ] **Step 2: RED 확인**

Run: `python3 -m pytest skills/korean-ebook-typst/tests/test_infographic_pages_report.py -q`
Expected: FAIL — manifest.json 부재(KeyError/FileNotFoundError).

- [ ] **Step 3: 구현**

`render.py` `render_book_fences` emit 루프 — typ 작성 시 프리픽스(`#context` 필수) + 루프 끝에서 manifest:

```python
        for f in fences:
            fig = figs[f.index]
            name = f"{idx:03d}-fig{f.index:02d}.typ"
            (out_dir / name).write_text(
                f'#context metadata((kind: "ig-fig", name: "{name}", '
                f'page: here().page()))\n' + emit.render_typ(fig), encoding="utf-8")
            ...
        # (메서드 말미, result 반환 직전)
    manifest = {"count": sum(len(e) for e in result.values()),
                "figs": [{"name": nm, "chapter": idx, "index": fi}
                         for idx, emits in result.items() for fi, nm in emits.items()]}
    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    return result
```

`qc_gate.py` `run()` — report 라이터 앞에 삽입(빌드 main.typ·manifest 존재 시; 모듈 헤더에 `import subprocess` 추가 — 현재 없음):

```python
    igp = _infographic_pages(book, pdf)   # pdf: run()이 이미 파악한 최종 PDF 경로
    report = {..., "infographic_pages": igp, ...}


def _infographic_pages(book: Path, pdf: Path | None) -> dict:
    """§5.4 개정 6판 — typst query metadata로 도식-페이지 대응·일치 검사·검수 PNG."""
    build = book / "build"
    main = build / "main.typ"
    mf = build / "infographic" / "manifest.json"
    if not (main.exists() and mf.exists()):
        return {"count": 0, "expected": 0, "match": True, "figs": []}
    manifest = json.loads(mf.read_text(encoding="utf-8"))
    r = subprocess.run([typst_binary(), "query", str(main), "metadata",
                        "--field", "value", "--root", str(build)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return {"count": 0, "expected": manifest["count"], "match": False, "figs": []}
    queried = json.loads(r.stdout or "[]")   # stdout = JSON 배열 하나
    figs = [{"name": f["name"], "chapter": f["chapter"], "index": f["index"],
             "page": q["page"]}
            for q in queried if isinstance(q, dict) and q.get("kind") == "ig-fig"
            for f in manifest["figs"] if f["name"] == q.get("name")]
    # §5.4 "실제 페이지 수와의 일치 검사" — page가 PDF 범위 내인가(G1-M6)
    pages_ok = True
    if pdf is not None and pdf.exists():
        import fitz
        with fitz.open(pdf) as doc:
            pages_ok = doc.page_count > 0 and all(
                1 <= f["page"] <= doc.page_count for f in figs)
    out = {"count": len(figs), "expected": manifest["count"],
           "match": len(figs) == manifest["count"] and pages_ok, "figs": figs}
    for pno in sorted({f["page"] for f in figs} if pages_ok else set()):
        png = build / "infographic" / f"review-p{pno:03d}.png"
        subprocess.run([typst_binary(), "compile", str(main), str(png),
                        "--pages", str(pno), "--ppi", "170", "--root", str(build)],
                       capture_output=True, text=True, check=False)
    return out
```

주: qc_gate의 typst 바이너리 임포트는 **이중 try/except 관례**(qc_gate.py:211-214 korean_lint·render.py:13-16 md2typst와 동일) — `try: from build import typst_binary / except ImportError: from scripts.build import typst_binary`. 단순 relative import는 `python3 scripts/qc_gate.py <책dir>` CLI 경로(SKILL.md 공식)를 즉시 깬다(G2-M5). `match=False`는 에러가 아니라 WARN 채널 — `run()` 출력문에 `도식 {count}/{expected}` 한 줄 추가. PNG 렌더 실패는 무시(check=False) — 검수 렌더는 best-effort, 검수자 안내물. `match=False` 시 `pass`에는 영향 없음(WARN) — 다만 `count==0 and expected>0`은 build 붕괴 신호이므로 콘솔에 경고 문구 출력. `typst query`의 deprecation 경고(stderr)는 0.15.1 고정 상태 무해.

- [ ] **Step 4: GREEN 확인**

Run: `python3 -m pytest skills/korean-ebook-typst/tests/test_infographic_pages_report.py -q` → PASS(2). 전체: **250 passed**(기존 골든 바이트 불변 — metadata 프리픽스는 standalone 골든 emit 대상 아님: 골든 테스트는 `emit.render_typ` 출력을 비교하고 프리픽스는 render.py가 파일에만 붙인다).

- [ ] **Step 5: 커밋**

```bash
git add skills/korean-ebook-typst/scripts/infographic/render.py skills/korean-ebook-typst/scripts/qc_gate.py skills/korean-ebook-typst/tests/test_infographic_pages_report.py
git commit -m "feat: infographic_pages 리포트 — metadata 페이지 매핑·gate-report 필드·검수 PNG 170DPI"
```

---

### Task 3: 가이드 완성 + 이관 LOW 해소

**Files:**
- Modify: `skills/korean-ebook-typst/references/infographic/authoring.md`(composite 섹션·검수 절차 확장)
- Modify: `skills/korean-ebook-typst/SKILL.md`(레이아웃 목록 composite)
- Modify: `skills/korean-ebook-typst/scripts/infographic/render.py`(별칭 경고 finding)
- Test: `skills/korean-ebook-typst/tests/test_infographic_layout_layers.py`(rings 골든 추가)

**Interfaces:**
- Consumes: Task 1 composite 계약(GAP·PRIMARY_FRAC·에러 스키마), Task 2 `infographic_pages`·`review-p*.png` 검수 흐름
- Produces: authoring.md 전체판(§8.5 완성), 별칭 경로 non-fatal finding `kind="schema"` 문구 `"별칭 {raw}→{norm} — 정식 키워드 권장"`, rings 바이트 골든 `golden-layers-rings-practical.typ`

- [ ] **Step 1: 별칭 경고 테스트(RED)** — `test_infographic_pages_report.py`에 추가(`_book`·assemble 호출 계약 재사용):

```python
def test_alias_warning_printed(tmp_path, capsys):
    import scripts.build as b
    book = _book(tmp_path)
    (book / "ch01.md").write_text(
        BOOK.replace('"layout": "flow"', '"layout": "process"'), encoding="utf-8")
    cfg = {"title": "검증책", "subtitle": "부제", "author": "저자", "style": "practical",
           "cover": "auto", "chapters": ["ch01.md"]}
    b.assemble(cfg, book)   # 기존 통합 테스트 호출 계약 — process 별칭이 flow로 정규화돼 빌드 성공
    out = capsys.readouterr().out
    assert "별칭 process→flow — 정식 키워드 권장" in out
    assert "000-ch01.md #1" in out
    # 채널 이원(G1-L10): 콘솔 + 검수 시트 상단 — 로그를 놓쳐도 gate 산출물에 남는다
    sheet = (book / "build" / "infographic" / "000-fig01.review.md").read_text(encoding="utf-8")
    assert "별칭 process→flow — 정식 키워드 권장" in sheet
```

구현 계약(2 채널): ① **render.py parse 루프**(fences.append 직후)가 `f.data.get("_alias")` 있을 때 `print(f"[경고] 별칭 {f.data['_alias']}→{f.layout} — 정식 키워드 권장 ({chapter_name} #{f.index})")` — non-fatal, 빌드 계속. ② `_review_sheet`(또는 그 호출부)이 `f.data.get("_alias")` 있을 때 고지 블록 위에 `**⚠ 별칭 사용:** {alias}→{layout} — 정식 키워드 권장` 한 줄. lint.LintFinding 스키마 위반과 달리 별칭은 정상 빌드 경로라 finding이 아닌 경고이되, stdout만으로는 gate-report를 읽는 downstream이 못 본다는 기존 원칙(qc_gate.py:215-216)에 따라 검수 시트에 병기한다.

- [ ] **Step 2: rings 골든 추가** — `test_infographic_layout_layers.py` 골든 테스트 옆에 always-write 재생성 골든 1종. **골격은 인접 기존 골든 테스트의 형태를 그대로 복제** — 이 파일의 실제 임포트/호출 관례(`layers_arch.layout(parse_fence(...))`, 테스트 내 `from scripts.infographic import emit`)와 재생성 관례(이 파일이 env=1이면 **무조건 재생성**이면 그 관례를 따름)에 맞춘다:

```python
GOLDEN_RINGS = Path(__file__).parent / "fixtures" / "infographic" / "golden-layers-rings-practical.typ"

RINGS_FENCE = {"layout": "layers", "variant": "rings", "title": "계층은 표현에서 자료로 내려간다",
               "rings": [{"label": "표현"}, {"label": "문서"}, {"label": "자료"}, {"label": "부호"}]}
# rings 항목 스키마(_sheet_rows `rings[i].label` 준수)·variant 키·그 외 필수 필드(thesis 등)는
# 이 파일 기존 골든/테스트가 쓰는 확정 형태를 그대로 복제해 조정한다.


def test_layers_rings_golden():
    # 임포트·펜스 생성·render 호출은 인접 골든 테스트 관례 복제 — 아래는 골격
    fig = _layers_dispatch(RINGS_FENCE)
    typ = emit.render_typ(fig)
    regen = os.environ.get("IG_REGEN_GOLDEN")   # 파일 관례에 맞춰 조정
    if regen or not GOLDEN_RINGS.exists():
        GOLDEN_RINGS.write_text(typ, encoding="utf-8")
        pytest.fail("골든 재생성 — 눈검 후 커밋")
    assert GOLDEN_RINGS.read_text(encoding="utf-8") == typ
```

Run: `IG_REGEN_GOLDEN=1 python3 -m pytest ...layers.py -q` → 재생성 fail → 눈검(동심원·라벨 현 내 배치 — rings[0] 102.18pt·rings[3] 39.41pt 폭 계열) → 재실행 PASS.

- [ ] **Step 3: authoring.md 완성**

(a) `### layers — 계층 구조` 뒤에 `### composite — 복합 씬` 섹션: 펜스 예시(주 cards + 보조 flow)·slot 규칙(주 1·보조 1~2·재귀 금지)·배분 규칙(주 60% 상한·측정 우선·슬롯 간 24pt)·**분할 에러 스키마**(개정 6판 — 자동 축소 없음)·"모듈은 각자 결론형 제목을 가진다".
(b) `## 검수` 섹션 확장: `gate-report.json` `infographic_pages`(count/expected/match) 읽는 법·`build/infographic/review-p*.png`(170 DPI) 눈검 항목(카드 줄바꿈·셀 잘림·화살표 충돌·작은 글씨·카드 밖 이탈 — 스펙 §5.4 목록)·확인란 절차 기존 연결.
(c) `## 언제 도식을 넣나` 라우팅 표에 composite 행 추가("한 장에서 대비·절차를 함께 — 주+보조").
(d) `## 예산 치트시트`에 composite 배분 행(주 ≤60%·보조 잔여·GAP 24pt·높이 상한 85%·헤더 선차감). 치트시트는 practical 기준 유지(개정 6판 (e)로 스펙에 명시됨).
(e) 문서 라벨 갱신: authoring.md H1 괄호 라벨 "(Phase 4 — …)" → "(Phase 5 — +composite·검수 렌더·리포트)".

- [ ] **Step 4: SKILL.md** 레이아웃 목록에 composite 추가(기존 9종 나열 형식 준수) + 인포그래픽 섹션 제목의 Phase 라벨 갱신("(인포그래픽 — Phase 4)" → "(인포그래픽 — Phase 5)").

- [ ] **Step 5: 확인 + 커밋**

Run: `python3 -m pytest skills/korean-ebook-typst/tests/ -q` → **252 passed**(250 + 별칭 1 + rings 골든 1).

```bash
git add -A skills/korean-ebook-typst/references/infographic/authoring.md skills/korean-ebook-typst/SKILL.md skills/korean-ebook-typst/scripts/infographic/render.py skills/korean-ebook-typst/tests
git commit -m "docs: 가이드 전체판 완성 — composite·검수 렌더 절차 + 별칭 경고·rings 골든(이관 LOW 해소)"
```

---

### Task 4: 통합 마무리 — 9종+composite fixture 책

**Files:**
- Modify: `skills/korean-ebook-typst/tests/test_infographic_build_integration.py`(composite 펜스 + infographic_pages 단언)
- Test fixture: 기존 통합 fixture 책(Phase 3+4)에 composite 챕터/펜스 추가

**Interfaces:**
- Consumes: Task 1·2 전부, 기존 통합 테스트 구조(subprocess 빌드·검수 시트·I1 단언)
- Produces: 스펙 §7 통합 완료 상태 — "9종+복합 펜스 fixture 책 → build → PDF·infographic_pages 일치 확인"

- [ ] **Step 1: 통합 테스트 확장(RED)** — 기존 통합 fixture는 **코드 내 문자열**(PHASE4_MD 등)이므로, 기존 fixture를 건드리지 않고 **신규 fixture 문자열 PHASE5_MD + 신규 테스트 함수**를 같은 파일에 추가한다(기존 단언·`glob == 3`·`for n in (1,2,3)` 루프는 무변경 유지). PHASE5_MD: PHASE4_MD 챕터에 composite 펜스 1개 추가(주 `cards` 3 + 보조 `flow` 2, 결론형 무숫자 제목 `"구성과 절차를 한 장에 담는다"`) — 펜스 번호는 배치 순서에 따라 확정되므로 실행자가 PHASE5_MD에서 세어 상수로 박는다(아래 `FIG_NO`).

```python
def test_phase5_composite_integration(tmp_path):
    # 빌드·컴파일은 기존 통합 테스트 호출 계약 그대로(PHASE5_MD fixture 사용).
    # 단 gate-report.json은 qc_gate가 쓴다 — 기존 통합 테스트는 qc_gate를 돌리지 않으므로
    # 여기서 명시적으로 호출한다(tests/test_qc_gate.py의 호출 관례 복제 — G2-M4).
    FIG_NO = 4                      # PHASE5_MD에서 composite 펜스의 실제 번호 — 실행자가 확인해 고정
    EXPECTED_FIGS = 4               # 기존 3종 + composite 1
    build = book / "build"
    manifest = json.loads((build / "infographic" / "manifest.json").read_text(encoding="utf-8"))
    assert f"000-fig{FIG_NO:02d}.typ" in [f["name"] for f in manifest["figs"]]
    from scripts import qc_gate
    rc = qc_gate.run(book)
    assert rc == 0
    report = json.loads((book / "gate-report.json").read_text(encoding="utf-8"))
    assert report["infographic_pages"]["match"] is True
    assert report["infographic_pages"]["count"] == manifest["count"] == EXPECTED_FIGS
    sheet = (build / "infographic" / f"000-fig{FIG_NO:02d}.review.md").read_text(encoding="utf-8")
    assert "modules[0].cards[0].title" in sheet and "modules[1].steps[0].title" in sheet
```

- [ ] **Step 2: RED 확인 → 구현(없음 — Task 1~3가 이미 구현; 실패 시 Task 1~3 결함이므로 본태 수정) → GREEN**

Run: `python3 -m pytest skills/korean-ebook-typst/tests/test_infographic_build_integration.py -q` → PASS. 전체: **253 passed** 목표(통합 신규 1).

- [ ] **Step 3: 커밋 + 종료 조건 확인**

```bash
git add skills/korean-ebook-typst/tests
git commit -m "test: 통합 마무리 — composite 포함 fixture 책·infographic_pages 일치"
```

종료 조건: 전체 스위트 green·기존 골든 전종 바이트 불변 + 신규 composite·rings 골든 존재+PASS·`gate-report.json` `infographic_pages.match=true`·authoring.md composite+검수 절차 섹션 존재·SKILL.md 10 layout(9+composite).

---

## Self-Review (기록 — 검토 wave G1·G3 반영 후 갱신)

- 스펙 커버리지: §3.5(Task 1)·§5.4 검수 렌더·리포트(Task 2)·§8.5 가이드·SKILL(Task 3)·§7 통합(Task 4)·§3.4 별칭 경고(Task 3) — 전부 태스크 있음. §3.5 "보조 축소"는 개정 6판으로 명시적 제거(Step 0 — 판수 갱신·§10 이력 포함).
- 플레이스홀더 스캔: `HEAD_H` 제거. assemble/qc_gate 호출은 test_build_compile.py·test_qc_gate.py 복제 계약 + 의사 코드. rings·ladder 페이로드는 `_sheet_rows` 확정 경로 기반 + "인접 테스트 형태 복제" 지시. Task 4는 PHASE5_MD 신규 fixture + FIG_NO/EXPECTED_FIGS 상수로 완결.
- 타입 정합성: 임포트 경로 `archetypes.composite`(파일 위치 정합)·`dataclasses.replace` y/y1/y2 이동(ArrowOp 커버)·모듈 Fence 재귀 parse_fence 승계·`#context metadata`(typst 0.15.1 실증)·query stdout JSON 배열·fitz 페이지 범위 대조 — 전부 반영.
- 테스트 수 산술: 239 → T1 +9(단위 7+시트 1+골든 1)=248 → T2 +2=250 → T3 +2=252 → T4 +1=253.
- 미반영 검토 항목: G1-L9(치트시트 전 팩형 확장) — 개정 6판 (e)로 "practical 기준" 스펙 명시로 봉합(확장은 별도 플랜).
