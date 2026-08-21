# 인포그래픽 레이어 Phase 2 (cards + matrix + flow swimlane) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Phase 1(flow)에 이어 cards·matrix archetype과 flow swimlane 변형을 추가하고, 골든 교정 1주기로 팩별 예산 계수를 실측 갱신한다.

**Architecture:** Phase 1과 동일 — parse(스키마)→layout(archetype별 순수 함수)→lint(I1)→emit(ops→typst). 신규 archetype은 `archetypes/`에 모듈 추가 + `layout.dispatch` 등록 + `parse` 검증 분기 확장. model.py ops 재사용(RectOp/TextOp/ArrowOp 변경 없음).

**Tech Stack:** Python 3.12 표준 라이브러리, typst 0.15.1, pytest. 신규 의존 0.

**Spec:** `docs/superpowers/specs/2026-08-21-infographic-layer-design.md` (개정 3판)

**Phase 1 자산 (main 병합 완료, 155 green):** `scripts/infographic/` 전 모듈, `templates/infographic/helper.typ`, authoring.md, 골든 플로우. 테스트 관례: `tests/conftest.py`가 스킬 루트 sys.path 추가, `from scripts.infographic.x import y`.

## Global Constraints (Phase 1과 동일 + 추가)

- 외부 의존 금지, 펜스 JSON, 결정론(같은 입력=같은 방출 바이트), hex 금지(역할명), leading 1.3em, G3 불변식(본문±0.3pt 밖 — essay 예외 +1.5), I1 메시지 계약(loc/측정값/저작자 레버), typst_binary() 재use, timeout=120.
- **공통 예외 베이스(Task 1 도입)**: `archetypes/base.py`의 `LayoutError(Exception)`(.detail). 모든 archetype 에러가 이것을 상속 — `render.py`·`cli.py`는 베이스만 catch(신규 archetype 에러가 I1 전수 집계·CLI 리포트를 우회해 traceback으로 크래시하는 것을 원천 차단 — 적대 검토 G1).
- **lint·검수 시트는 `f.data.get("steps", [])` 접근**(신규 layout에서 KeyError 금지) — 검수 시트는 archetype별 요소 전부를 행으로 갖는다(§5.4).
- 모든 archetype은 `archetypes/flow.py`의 구조를 따른다: `layout(fence, tokens) -> FigModel`, `XLayoutError(LayoutError)`, 잉크 bbox 보장, 높이 85% 한계, TextOp.field 계약.
- 판형 상한은 layout이 즉시 에러(스펙 §6.2) — Phase 1 PACK_LIMITS 패턴. **상한 검사는 parse 하한·상한과 별개 경로**(parse 2~6 선검증과 판형 상한 n>cols·2 등 layout 에러가 모두 살아있는 테스트 경로 유지 — 도달 불가 테스트 금지, 적대 검토 G1).
- 카드 채움 role "surface-tint"(lint 매립 검사 의존), 화살표 ink-soft 1.2pt open-V. **커넥터 복도 상수는 샤프트 가시 ≥12pt와 양립해야 한다** — `_harrow` 오프셋(+4/−8)에서 샤프트=간격−12이므로 셀 간격 GS ≥ 24(§6.1).
- 텍스트 크기: 카드 제목=본문+1, 카드 본문=본문−1, 제목=H2(essay +1.5), 라벨=label 크기.
- **archetype별 골든 스냅샷 필수**(스펙 §7·§8 종료 조건) — cards·matrix 각 1개, IG_REGEN_GOLDEN 절차.
- **병합 게이트**: Task 4(문서 갱신) 완료 전 main 병합 금지 — 라우팅 표가 코드와 모순되는 중간 상태 방지.
- 프리플라이트 교훈(최종 리뷰): "키가 챕터 단위 유일한가" — 본 Phase 신규 키 없음(펜스 내부). dispatch 키=parse 정규화 layout 문자열 재확인.

---

### Task 1: cards archetype + 공통 예외 베이스 + 소비자 확장

**Files:**
- Create: `skills/korean-ebook-typst/scripts/infographic/archetypes/base.py` (공통 `LayoutError`)
- Create: `skills/korean-ebook-typst/scripts/infographic/archetypes/cards.py`
- Modify: `skills/korean-ebook-typst/scripts/infographic/parse.py` (cards 검증 분기 + unknown-layout 메시지 동적 갱신)
- Modify: `skills/korean-ebook-typst/scripts/infographic/layout.py` (dispatch 등록)
- Modify: `skills/korean-ebook-typst/scripts/infographic/lint.py` (`f.data.get("steps", [])` 전환 + cards 필드)
- Modify: `skills/korean-ebook-typst/scripts/infographic/render.py` (except LayoutError 전환 + `_review_sheet` archetype별 요소 행 확장)
- Modify: `skills/korean-ebook-typst/scripts/infographic/cli.py` (except LayoutError 전환)
- Modify: `skills/korean-ebook-typst/scripts/infographic/archetypes/flow.py` (FlowLayoutError → LayoutError 상속 1줄)
- Test: `skills/korean-ebook-typst/tests/test_infographic_layout_cards.py`
- Test fixture: `skills/korean-ebook-typst/tests/fixtures/infographic/golden-cards-practical.typ` (IG_REGEN_GOLDEN 절차)

**Interfaces:**
- Consumes: Phase 1 전부. `budget.line_count(text, box, size, pad, pack)`, `model.*`, `parse.Fence`.
- Produces:
  - `cards.layout(fence, tokens) -> FigModel`; `cards.CardsLayoutError`(.detail)
  - `cards.PACK_COLS = {"essay": 2, "practical": 3, "b5": 3, "business": 3, "lecture": 3}` (스펙 §6.2 cards 열수)
  - `cards.CARD_MIN_N, CARD_MAX_N = 2, 6` (스펙 §3.2)
  - 배치 결정론: `cols = min(PACK_COLS[pack], n)`; `n > PACK_COLS[pack]*2`면 에러(2행 초과); `cardW = (W − 2P − (cols−1)·G)/cols`; `cardW < 80`이면 에러. 세로 모드 없음(Phase 1과 동일 근거).
  - 카드 내부 스택(위→아래): 선택 `value`(큰 숫자 강조 — 크기 = 카드 제목+2pt, role "focus", 굵게, field "{i}.value") → `title`(굵게) → `text`. value는 문장 숫자 규칙(lint number-evidence) 자동 대상.
  - `parse` 확장: layout "cards" — `cards[]` 2~6, 각 {title 필수, text 필수, value 선택}. 별칭: `principles`→cards, `dashboard`→cards(스펙 §3.4).
  - `lint` 확장: `fields` 수집에 cards 요소 추가: `cards[i].title/.text/.value`.

- [ ] **Step 1: 실패 테스트 작성**

```python
"""test_infographic_layout_cards.py — 스펙 §6.2·§6.3 cards 지오메트리·결정론."""
import json
from pathlib import Path

import pytest

from scripts.infographic.archetypes import cards as cards_arch
from scripts.infographic.model import FigModel, RectOp, TextOp
from scripts.infographic.parse import parse_fence

TOKENS = json.loads((Path(__file__).resolve().parents[1] / "styles" / "practical" / "tokens.json").read_text(encoding="utf-8"))
W = TOKENS["body_frame_pt"]["x1"] - TOKENS["body_frame_pt"]["x0"]
P, G = 14.0, 28.0


def _fence(n: int, value: bool = False, text: str = "근거 문장"):
    cards = []
    for i in range(n):
        c = {"title": f"항목 {i+1}", "text": text}
        if value:
            c["value"] = "3단계"
        cards.append(c)
    body = json.dumps({"layout": "cards", "title": "결론 제목", "cards": cards}, ensure_ascii=False)
    return parse_fence(1, 1, body)


def test_three_cards_one_row_practical():
    fig = cards_arch.layout(_fence(3), TOKENS)
    cards = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
    assert len(cards) == 3
    expect = (W - 2 * P - 2 * G) / 3
    assert abs(cards[0].w - expect) < 0.01
    assert abs(cards[2].x - (P + 2 * (expect + G))) < 0.01


def test_two_cards_widen_to_two_cols():
    fig = cards_arch.layout(_fence(2), TOKENS)
    cards = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
    assert abs(cards[0].w - (W - 2 * P - G) / 2) < 0.01     # cols=min(3,2)=2


def test_five_cards_wrap_two_rows():
    fig = cards_arch.layout(_fence(5), TOKENS)
    cards = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
    assert len(cards) == 5
    assert len({round(r.y, 2) for r in cards}) == 2          # 3+2 랩


def test_five_cards_essay_pack_limit_error():
    # essay 상한 2열×2행=4 — n=5는 layout 판형 상한 경로(parse 2~6 내부)
    ET = json.loads((Path(__file__).resolve().parents[1] / "styles" / "essay" / "tokens.json").read_text(encoding="utf-8"))
    with pytest.raises(cards_arch.CardsLayoutError, match="상한"):
        cards_arch.layout(_fence(5), ET)


def test_cards_lint_and_review_sheet_reach_elements():
    # lint가 cards 요소에 도달하는가(KeyError 아님) — 적대 검토 G1 방어
    from scripts.infographic.lint import check
    from scripts.infographic.render import _review_sheet
    body = json.dumps({"layout": "cards", "title": "t", "cards": [
        {"title": "3단계 확정", "text": "가"},
        {"title": "b", "text": "나"},
        {"title": "c", "text": "다"}]}, ensure_ascii=False)
    fence = parse_fence(1, 1, body)
    figs = {1: cards_arch.layout(fence, TOKENS)}
    found = check([fence], figs, TOKENS, "원문 없음", "ch01.md")
    assert any(f.loc == "ch01.md #1 cards[0].title" for f in found)
    sheet = _review_sheet(fence, [])
    assert "cards[0].title" in sheet


def test_value_renders_large_focus_text():
    fig = cards_arch.layout(_fence(3, value=True), TOKENS)
    values = [t for t in fig.ops if isinstance(t, TextOp) and t.field == "cards[0].value"]
    assert values and values[0].role == "focus" and values[0].weight == "bold"
    assert values[0].size > TOKENS["fonts"]["body"]["size_pt"] + 2


def test_g3_invariant_and_ink_bbox():
    body_size = TOKENS["fonts"]["body"]["size_pt"]
    for n in (2, 3, 4, 6):
        fig = cards_arch.layout(_fence(n), TOKENS)
        assert isinstance(fig, FigModel)
        for o in fig.ops:
            if isinstance(o, RectOp):
                assert o.x - o.stroke_w / 2 >= -0.001 and o.x + o.w + o.stroke_w / 2 <= fig.width + 0.001
            if isinstance(o, TextOp) and o.size != body_size:
                assert abs(o.size - body_size) > 0.3


def test_aliases_principles_dashboard():
    import json as j
    for alias in ("principles", "dashboard"):
        body = j.dumps({"layout": alias, "title": "t", "cards": [
            {"title": "a", "text": "가"}, {"title": "b", "text": "나"}]}, ensure_ascii=False)
        f = parse_fence(1, 1, body)
        assert f.layout == "cards" and f.data["_alias"] == alias
```

- [ ] **Step 2: 실패 확인**

Run: `cd /mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook-typst && python3 -m pytest tests/test_infographic_layout_cards.py -v`
Expected: FAIL — `ModuleNotFoundError: ... cards`

- [ ] **Step 3: 최소 구현**

`archetypes/cards.py`:

```python
"""cards — 헤드라인 카드 그리드(스펙 §6.2·§6.3). 결정론: cols=min(팩열수,n), 2행 랩, 세로 없음."""
from __future__ import annotations

from .. import budget
from ..model import FigModel, RectOp, TextOp
from ..parse import DEFAULT_NOTE, Fence

P = 14.0
G = 28.0
CARD_MIN_N, CARD_MAX_N = 2, 6
MIN_CARD_W = 80.0
CARD_PAD_IN = 8.0
CARD_PAD_V = 10.0
LEADING = 1.3
HEIGHT_LIMIT = 0.85
VALUE_BONUS_PT = 2.0                       # value 강조 — 카드 제목+2pt

PACK_COLS = {"essay": 2, "practical": 3, "b5": 3, "business": 3, "lecture": 3}


class CardsLayoutError(Exception):
    def __init__(self, detail: str):
        super().__init__(detail)
        self.detail = detail


def layout(fence: Fence, tokens: dict) -> FigModel:
    frame = tokens["body_frame_pt"]
    W = frame["x1"] - frame["x0"]
    H_frame = frame["y1"] - frame["y0"]
    pack = tokens.get("style", "practical")
    f = tokens["fonts"]
    body = f["body"]["size_pt"]
    title_size = f["heading2"]["size_pt"]
    if abs(title_size - body) <= 0.3:
        title_size = body + 1.5
    kicker_size = f["label"]["size_pt"]
    card_title_size = body + 1
    card_text_size = body - 1
    value_size = card_title_size + VALUE_BONUS_PT

    cols_n = PACK_COLS.get(pack)
    if cols_n is None:
        raise CardsLayoutError(f"알 수 없는 스타일 팩 {pack!r}")
    items = fence.data["cards"]
    n = len(items)
    if n < CARD_MIN_N or n > CARD_MAX_N:
        raise CardsLayoutError(f"cards {n}개 — 하한 {CARD_MIN_N}, 상한 {CARD_MAX_N}")
    if n > cols_n * 2:
        raise CardsLayoutError(
            f"cards {n}개 > 판형 상한 {cols_n * 2}({pack} {cols_n}열×2행) — 요소 수 감소 또는 펜스 분할")
    cols = min(cols_n, n)
    cardW = (W - 2 * P - (cols - 1) * G) / cols
    if cardW < MIN_CARD_W:
        raise CardsLayoutError(
            f"카드폭 {cardW:.1f}pt < {MIN_CARD_W:.0f}pt({pack}) — 글자 축약, 요소 수 감소 또는 펜스 분할")

    def card_h(c: dict) -> float:
        h = 2 * CARD_PAD_V
        if "value" in c:
            h += value_size * LEADING + 4.0
        h += budget.line_count(c["title"], cardW, card_title_size, CARD_PAD_IN, pack) * card_title_size * LEADING + 4.0
        h += budget.line_count(c["text"], cardW, card_text_size, CARD_PAD_IN, pack) * card_text_size * LEADING
        return h

    # 헤더(Phase 1 flow와 동일 구조)
    texts: list[TextOp] = []
    cy = 0.0
    if fence.kicker:
        texts.append(TextOp(x=W / 2, y=cy + kicker_size * LEADING / 2, size=kicker_size,
                            text=fence.kicker, role="ink-mute", field="kicker"))
        cy += kicker_size * LEADING
    t_lines = budget.line_count(fence.title, W - 2 * P, title_size, 0.0, pack)
    texts.append(TextOp(x=W / 2, y=cy + t_lines * title_size * LEADING / 2, size=title_size,
                        text=fence.title, role="ink", weight="bold", max_w=W - 2 * P, field="title"))
    cy += t_lines * title_size * LEADING
    if fence.thesis:
        th = budget.line_count(fence.thesis, W - 2 * P, card_text_size, 0.0, pack)
        texts.append(TextOp(x=W / 2, y=cy + th * card_text_size * LEADING / 2, size=card_text_size,
                            text=fence.thesis, role="ink-soft", max_w=W - 2 * P, field="thesis"))
        cy += th * card_text_size * LEADING
    y = cy + 18.0

    rows = [items[i:i + cols] for i in range(0, n, cols)]
    row_h = [max(card_h(c) for c in row) for row in rows]
    cards: list[RectOp] = []
    for r, row in enumerate(rows):
        ry = y + sum(row_h[:r]) + G * r
        for j, c in enumerate(row):
            idx = r * cols + j
            cx = P + j * (cardW + G)
            cards.append(RectOp(x=cx, y=ry, w=cardW, h=row_h[r]))
            _card_texts(texts, c, cx, ry, cardW, row_h[r],
                        card_title_size, card_text_size, value_size, idx, pack)
    y = y + sum(row_h) + G * (len(rows) - 1)

    y += 12.0
    note = fence.note or DEFAULT_NOTE
    texts.append(TextOp(x=W / 2, y=y + card_text_size * LEADING / 2, size=card_text_size,
                        text=note, role="ink-mute", max_w=W - 2 * P, field="note"))
    y += card_text_size * LEADING

    if y > H_frame * HEIGHT_LIMIT:
        raise CardsLayoutError(
            f"도식 높이 {y:.0f}pt > 프레임 {H_frame * HEIGHT_LIMIT:.0f}pt(85%) — "
            f"문구 축약, 요소 수 감소 또는 펜스 분할")

    ops = [RectOp(x=0.0, y=0.0, w=W, h=y, rx=0.0, fill_role="paper", stroke_role="rule", stroke_w=0.0),
           *cards, *texts]
    _ink_ok(ops, W, y)
    return FigModel(width=W, height=y, ops=tuple(ops), source_index=fence.index)


def _card_texts(out: list, c: dict, cx: float, cy: float, cw: float, ch: float,
                t_size: float, x_size: float, v_size: float, idx: int, pack: str) -> None:
    t_lines = budget.line_count(c["title"], cw, t_size, pack=pack)
    x_lines = budget.line_count(c["text"], cw, x_size, pack=pack)
    v_lines = budget.line_count(c.get("value", ""), cw, v_size, pack=pack) if "value" in c else 0
    block = (v_lines * v_size * LEADING + 4.0 if "value" in c else 0.0) \
        + t_lines * t_size * LEADING + 4.0 + x_lines * x_size * LEADING
    top = cy + (ch - block) / 2
    cur = top
    if "value" in c:
        out.append(TextOp(x=cx + cw / 2, y=cur + v_lines * v_size * LEADING / 2, size=v_size,
                          text=c["value"], role="focus", weight="bold", max_w=cw,
                          field=f"cards[{idx}].value"))
        cur += v_lines * v_size * LEADING + 4.0
    out.append(TextOp(x=cx + cw / 2, y=cur + t_lines * t_size * LEADING / 2, size=t_size,
                      text=c["title"], role="ink", weight="bold", max_w=cw,
                      field=f"cards[{idx}].title"))
    cur += t_lines * t_size * LEADING + 4.0
    out.append(TextOp(x=cx + cw / 2, y=cur + x_lines * x_size * LEADING / 2, size=x_size,
                      text=c["text"], role="ink-soft", max_w=cw, field=f"cards[{idx}].text"))


def _ink_ok(ops, width: float, height: float) -> None:
    for o in ops:
        if isinstance(o, RectOp):
            if (o.x - o.stroke_w / 2 < -0.001 or o.x + o.w + o.stroke_w / 2 > width + 0.001
                    or o.y - o.stroke_w / 2 < -0.001 or o.y + o.h + o.stroke_w / 2 > height + 0.001):
                raise CardsLayoutError(
                    f"잉크 bbox 프레임 이탈: rect({o.x:.1f},{o.y:.1f},{o.w:.1f},{o.h:.1f})")
```

`parse.py` 수정 — `VALID_LAYOUTS`에 "cards" 추가, `ALIASES`에 `"principles": "cards", "dashboard": "cards"` 추가, 검증 분기:

```python
    if layout == "cards":
        cards_l = d.get("cards", [])
        if not isinstance(cards_l, list) or not (2 <= len(cards_l) <= 6):
            raise ParseError(index, f"cards 개수 {len(cards_l) if isinstance(cards_l, list) else 0} — 하한 2, 상한 6", line)
        for i, c in enumerate(cards_l):
            if not isinstance(c, dict):
                raise ParseError(index, f"cards[{i}] 객체 아님", line)
            if not str(c.get("title", "")).strip() or not str(c.get("text", "")).strip():
                raise ParseError(index, f"cards[{i}].title/.text 비어 있음", line)
            data["cards"] = [{"title": str(c["title"]).strip(), "text": str(c["text"]).strip(),
                              **({"value": str(c["value"]).strip()} if str(c.get("value", "")).strip() else {})}
                             for c in cards_l]
```

(steps 검증은 기존 flow 분기 유지 — layout별 검사 후 공통 data 채움 구조로 리팩터 최소화: 기존 `data["steps"]` 블록을 `if layout == "flow":`로 감싼다.)

`layout.py` dispatch 확장:

```python
from .archetypes import cards as _cards, flow as _flow

def dispatch(fence, tokens):
    if fence.layout == "flow":
        return _flow.layout(fence, tokens)
    if fence.layout == "cards":
        return _cards.layout(fence, tokens)
    raise ValueError(f"지원하지 않는 layout: {fence.layout!r}")
```

`lint.py` `fields` 수집 확장(fences 루프 안) + **steps 접근 전환**:

```python
# 기존: for i, s in enumerate(f.data["steps"]):  → 아래로 교체(KeyError 방어)
        for i, s in enumerate(f.data.get("steps", [])):
            ...
# cards 필드 추가:
        for i, c in enumerate(f.data.get("cards", [])):
            fields.append((f"cards[{i}].title", c["title"]))
            fields.append((f"cards[{i}].text", c["text"]))
            if "value" in c:
                fields.append((f"cards[{i}].value", c["value"]))
```

`archetypes/base.py` 신규:

```python
"""base.py — archetype 공통 예외(스펙 §5.2 전수 집계·§5.5 CLI 리포트가 베이스로 catch)."""


class LayoutError(Exception):
    def __init__(self, detail: str):
        super().__init__(detail)
        self.detail = detail
```

소비자 전환 (render.py·cli.py·flow.py):

```python
# archetypes/flow.py — FlowLayoutError를 베이스 상속으로(본문 로직 불변):
from .base import LayoutError
class FlowLayoutError(LayoutError):
    pass    # __init__은 베이스가 detail 처리 — 기존 .detail 계약 유지

# cards.py:
from .base import LayoutError
class CardsLayoutError(LayoutError):
    pass

# render.py: from .archetypes.flow import FlowLayoutError →
from .archetypes.base import LayoutError
# except FlowLayoutError as e:  →  except LayoutError as e:  (I1 "layout" finding 변환은 동일)

# cli.py: from scripts...flow import FlowLayoutError → base.LayoutError, except 절 교체
```

`render.py _review_sheet` — `f.data["steps"]` 순회를 archetype별 전 요소로 교체:

```python
def _sheet_rows(f) -> list[tuple[str, str]]:
    rows = [("title", f.title), ("kicker", f.kicker or "—"), ("thesis", f.thesis or "—")]
    for i, s in enumerate(f.data.get("steps", [])):
        rows.append((f"steps[{i}].title", s["title"]))
        rows.append((f"steps[{i}].text", s["text"]))
    for i, c in enumerate(f.data.get("cards", [])):
        rows.append((f"cards[{i}].title", c["title"]))
        rows.append((f"cards[{i}].text", c["text"]))
        if "value" in c:
            rows.append((f"cards[{i}].value", c["value"]))
    # matrix·lanes 행은 Task 2·3에서 같은 패턴으로 추가
    return rows
```

골든 테스트(test_infographic_layout_cards.py 말미):

```python
def test_cards_golden_snapshot():
    import os
    from scripts.infographic.emit import render_typ
    GOLDEN = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "infographic" / "golden-cards-practical.typ"
    fig = cards_arch.layout(_fence(3, value=True), TOKENS)
    out = render_typ(fig)
    if not GOLDEN.exists():
        if os.environ.get("IG_REGEN_GOLDEN") != "1":
            pytest.fail("골든 없음 — IG_REGEN_GOLDEN=1 실행 후 눈검·커밋")
        GOLDEN.parent.mkdir(parents=True, exist_ok=True)
        GOLDEN.write_text(out, encoding="utf-8")
    assert out == GOLDEN.read_text(encoding="utf-8")
```

(골든 확정 후 Step 4 눈검: 3카드 1행·value 강조·note 포함.)

- [ ] **Step 4: 통과 확인**

Run: `cd /mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook-typst && python3 -m pytest tests/test_infographic_layout_cards.py tests/ -q`
Expected: 신규 9(골든 최초는 실패 → `IG_REGEN_GOLDEN=1` 재실행 9 passed) + 전체 164

- [ ] **Step 5: 커밋**

```bash
git add skills/korean-ebook-typst/scripts/infographic/ skills/korean-ebook-typst/tests/test_infographic_layout_cards.py skills/korean-ebook-typst/tests/fixtures/infographic/golden-cards-practical.typ
git commit -m "feat: cards archetype + 공통 LayoutError 베이스 — 판형 열수 그리드·value 강조·소비자 확장"
```

---

### Task 2: matrix archetype (격자 + 정성 2×2)

**Files:**
- Create: `skills/korean-ebook-typst/scripts/infographic/archetypes/matrix.py`
- Modify: `parse.py` (matrix 두 형태 검증 + VALID_LAYOUTS에 "matrix" 추가 + ALIASES에 `"quadrant": "matrix"`), `layout.py` (dispatch), `lint.py` (필드 수집 — 축 라벨 포함), `render.py` `_sheet_rows` (headers/rows/cells 행)
- Test: `skills/korean-ebook-typst/tests/test_infographic_layout_matrix.py`
- Test fixture: `tests/fixtures/infographic/golden-matrix-practical.typ`

**Interfaces:**
- `matrix.layout(fence, tokens) -> FigModel`; `matrix.MatrixLayoutError`(.detail)
- `matrix.PACK_MAX_COLS = {"essay": 3, "practical": 4, "b5": 4, "business": 5, "lecture": 5}` (스펙 §6.2 matrix 열수)
- 데이터 두 형태(스펙 §3.2):
  - 격자: `headers[]`(2~판열수), `rows[][]`(각 행 len==len(headers), 행 1~6). 첫 열은 행 라벨(굵게 렌더).
  - 정성: `x_axis: {low, high}`, `y_axis: {low, high}`, `cells[]` 정확히 4({title, text}, 순서 = [yl·xl, yl·xh, yh·xl, yh·xh]… 아니오 — 행 우선: [low-low, low-high, high-low, high-high], y 우선 행). 셀 TextOp.field = `cells[i].title/.text`.
- 격자 지오메트리: `colW = (W − 2P) / ncols`(셀 간격 0 — 표 형태, 인접 rect가 격자선을 이룬다). 행 높이 = 해당 행 셀 텍스트 최대 줄수 기반. 셀 rect role "surface"… 아니오 — lint 매립 검사가 surface-tint 카드만 보므로 격자 셀은 `fill_role="surface-tint"` 유지(매립 검사 일관성), 첫 열은 `stroke_role="rule"`·굵은 텍스트.
- 정성 지오메트리: 축 라벨 행/열(kicker 크기, 좌상단 축명 생략 — low/high 라벨만), 셀 `cellW=(W−2P−G)/2`, 셀 간 G.
- 상한 에러는 모두 MatrixLayoutError(저작자 레버 포함).

- [ ] **Step 1: 실패 테스트 작성**

```python
"""test_infographic_layout_matrix.py — 스펙 §6.2·§6.3 matrix 격자·정성."""
import json
from pathlib import Path

import pytest

from scripts.infographic.archetypes import matrix as matrix_arch
from scripts.infographic.model import RectOp, TextOp
from scripts.infographic.parse import parse_fence

TOKENS = json.loads((Path(__file__).resolve().parents[1] / "styles" / "practical" / "tokens.json").read_text(encoding="utf-8"))
W = TOKENS["body_frame_pt"]["x1"] - TOKENS["body_frame_pt"]["x0"]
P = 14.0


def _grid_fence(ncols=4, nrows=3):
    headers = [f"열 {i+1}" for i in range(ncols)]
    rows = [[f"행 {r+1}-{c+1}" for c in range(ncols)] for r in range(nrows)]
    return parse_fence(1, 1, json.dumps(
        {"layout": "matrix", "title": "판단표", "headers": headers, "rows": rows}, ensure_ascii=False))


def _qual_fence():
    return parse_fence(1, 1, json.dumps({
        "layout": "matrix", "title": "정성 매트릭스",
        "x_axis": {"low": "소규모", "high": "대규모"},
        "y_axis": {"low": "단기", "high": "장기"},
        "cells": [
            {"title": "신속 검증", "text": "가설 확인"},
            {"title": "확장 투자", "text": "규모 대응"},
            {"title": "부채 정리", "text": "구조 조정"},
            {"title": "전략 전환", "text": "사업 재편"}]},
    }, ensure_ascii=False))


def test_grid_geometry():
    fig = matrix_arch.layout(_grid_fence(), TOKENS)
    cells = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
    assert len(cells) == 4 * 3
    expect = (W - 2 * P) / 4
    assert abs(cells[0].w - expect) < 0.01
    assert abs(cells[1].x - (P + expect)) < 0.01          # 간격 0 — 인접 격자


def test_grid_first_column_bold():
    fig = matrix_arch.layout(_grid_fence(), TOKENS)
    first = [t for t in fig.ops if isinstance(t, TextOp) and t.field == "cell[0][0]"]
    assert first and first[0].weight == "bold"


def test_grid_five_cols_practical_rejected():
    with pytest.raises(matrix_arch.MatrixLayoutError, match="열"):
        matrix_arch.layout(_grid_fence(ncols=5), TOKENS)  # practical 상한 4


def test_grid_six_cols_business_ok():
    BT = json.loads((Path(__file__).resolve().parents[1] / "styles" / "business" / "tokens.json").read_text(encoding="utf-8"))
    fig = matrix_arch.layout(_grid_fence(ncols=5), BT)     # business 상한 5
    assert fig.width > 0


def test_qualitative_four_cells_with_axis_labels():
    fig = matrix_arch.layout(_qual_fence(), TOKENS)
    cells = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
    assert len(cells) == 4
    labels = [t.text for t in fig.ops if isinstance(t, TextOp) and t.field.startswith("axis.")]
    assert "소규모" in labels and "장기" in labels
    AXIS_W = 40.0                                          # 구현 상수 — y축 라벨 열
    expect = (W - 2 * P - AXIS_W - 28.0) / 2               # 119.2pt(적대 검토 20pt 오차 정정)
    assert abs(cells[0].w - expect) < 0.01


def test_quadrant_alias_routes_to_qualitative():
    body = json.dumps({
        "layout": "quadrant", "title": "t",
        "x_axis": {"low": "a", "high": "b"}, "y_axis": {"low": "c", "high": "d"},
        "cells": [{"title": "1", "text": "x"}, {"title": "2", "text": "x"},
                  {"title": "3", "text": "x"}, {"title": "4", "text": "x"}]}, ensure_ascii=False)
    f = parse_fence(1, 1, body)
    assert f.layout == "matrix" and "x_axis" in f.data    # 정성 형태로 라우팅


def test_matrix_golden_snapshot():
    import os
    from scripts.infographic.emit import render_typ
    GOLDEN = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "infographic" / "golden-matrix-practical.typ"
    out = render_typ(matrix_arch.layout(_grid_fence(), TOKENS))
    if not GOLDEN.exists():
        if os.environ.get("IG_REGEN_GOLDEN") != "1":
            pytest.fail("골든 없음 — IG_REGEN_GOLDEN=1 실행 후 눈검·커밋")
        GOLDEN.parent.mkdir(parents=True, exist_ok=True)
        GOLDEN.write_text(out, encoding="utf-8")
    assert out == GOLDEN.read_text(encoding="utf-8")


def test_qualitative_requires_four_cells():
    body = json.dumps({
        "layout": "matrix", "title": "t",
        "x_axis": {"low": "a", "high": "b"}, "y_axis": {"low": "c", "high": "d"},
        "cells": [{"title": "1", "text": "x"}]}, ensure_ascii=False)
    from scripts.infographic.parse import ParseError
    with pytest.raises(ParseError, match="cells"):
        parse_fence(1, 1, body)


def test_height_limit():
    long = "아주 긴 셀 텍스트이다 " * 6
    body = json.dumps({"layout": "matrix", "title": "t",
                       "headers": ["a", "b", "c", "d"],
                       "rows": [[long] * 4 for _ in range(6)]}, ensure_ascii=False)
    with pytest.raises(matrix_arch.MatrixLayoutError, match="85"):
        matrix_arch.layout(parse_fence(1, 1, body), TOKENS)
```

- [ ] **Step 2: 실패 확인**

Run: `cd /mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook-typst && python3 -m pytest tests/test_infographic_layout_matrix.py -v`
Expected: FAIL — ModuleNotFoundError

- [ ] **Step 3: 최소 구현**

`archetypes/matrix.py`:

```python
"""matrix — 비교 격자 + 정성 2×2(스펙 §6.2·§6.3). 셀 간격 0(격자), 정성 셀 간 G."""
from __future__ import annotations

from .base import LayoutError
from .. import budget
from ..model import FigModel, RectOp, TextOp
from ..parse import DEFAULT_NOTE, Fence

P = 14.0
G = 28.0
MIN_COL_W = 40.0                 # 격자 셀 최소폭 — 이 이하면 텍스트 불가
MIN_QUAL_W = 60.0                # 정성 셀 최소폭(카드 문지방 완화 — essay 격자 3열 73.8pt와 정합)
CELL_PAD = 6.0
LEADING = 1.3
HEIGHT_LIMIT = 0.85
GRID_MAX_ROWS = 6

PACK_MAX_COLS = {"essay": 3, "practical": 4, "b5": 4, "business": 5, "lecture": 5}


class MatrixLayoutError(LayoutError):
    pass


def layout(fence: Fence, tokens: dict) -> FigModel:
    if "headers" in fence.data:
        return _grid(fence, tokens)
    return _qualitative(fence, tokens)


def _sizes(tokens: dict):
    f = tokens["fonts"]
    body = f["body"]["size_pt"]
    title_size = f["heading2"]["size_pt"]
    if abs(title_size - body) <= 0.3:
        title_size = body + 1.5
    return (f["label"]["size_pt"], title_size, body + 1, body - 1, body)


def _header_block(fence, tokens, W, texts):
    kicker_size, title_size, ct_size, cx_size, body = _sizes(tokens)
    cy = 0.0
    if fence.kicker:
        texts.append(TextOp(x=W / 2, y=cy + kicker_size * LEADING / 2, size=kicker_size,
                            text=fence.kicker, role="ink-mute", field="kicker"))
        cy += kicker_size * LEADING
    t_lines = budget.line_count(fence.title, W - 2 * P, title_size, 0.0, tokens.get("style", "practical"))
    texts.append(TextOp(x=W / 2, y=cy + t_lines * title_size * LEADING / 2, size=title_size,
                        text=fence.title, role="ink", weight="bold", max_w=W - 2 * P, field="title"))
    cy += t_lines * title_size * LEADING
    return cy + 18.0


def _footer(fence, texts, y, cx_size, W):
    texts.append(TextOp(x=W / 2, y=y + cx_size * LEADING / 2, size=cx_size,
                        text=fence.note or DEFAULT_NOTE, role="ink-mute",
                        max_w=W - 2 * P, field="note"))
    return y + cx_size * LEADING


def _finish(ops, texts, W, y, H_frame, source_index: int):
    """ops+texts를 합산해 잉크 검사 후 FigModel 반환 — texts를 버리면 안 된다(적대 검토 G1)."""
    all_ops = [*ops, *texts]
    if y > H_frame * HEIGHT_LIMIT:
        raise MatrixLayoutError(
            f"도식 높이 {y:.0f}pt > 프레임 {H_frame * HEIGHT_LIMIT:.0f}pt(85%) — "
            f"행 감소, 문구 축약 또는 펜스 분할")
    for o in all_ops:
        if isinstance(o, RectOp):
            if (o.x - o.stroke_w / 2 < -0.001 or o.x + o.w + o.stroke_w / 2 > W + 0.001
                    or o.y - o.stroke_w / 2 < -0.001 or o.y + o.h + o.stroke_w / 2 > y + 0.001):
                raise MatrixLayoutError(f"잉크 bbox 프레임 이탈: rect({o.x:.1f},{o.y:.1f})")
    return FigModel(width=W, height=y, ops=tuple(all_ops), source_index=source_index)


def _grid(fence: Fence, tokens: dict) -> FigModel:
    frame = tokens["body_frame_pt"]
    W, H_frame = frame["x1"] - frame["x0"], frame["y1"] - frame["y0"]
    pack = tokens.get("style", "practical")
    kicker_size, title_size, ct_size, cx_size, body = _sizes(tokens)
    headers = fence.data["headers"]
    rows = fence.data["rows"]
    ncols = len(headers)
    max_cols = PACK_MAX_COLS.get(pack)
    if max_cols is None:
        raise MatrixLayoutError(f"알 수 없는 스타일 팩 {pack!r}")
    if ncols > max_cols:
        raise MatrixLayoutError(
            f"열 {ncols}개 > 판형 상한 {max_cols}({pack}) — 열 감소 또는 펜스 분할")

    texts: list[TextOp] = []
    y = _header_block(fence, tokens, W, texts)

    colW = (W - 2 * P) / ncols
    if colW < MIN_COL_W:
        raise MatrixLayoutError(
            f"셀폭 {colW:.1f}pt < {MIN_COL_W:.0f}pt — 열 감소 또는 문구 축약")

    # 헤더 행
    hh = max(budget.line_count(h, colW, kicker_size, CELL_PAD, pack) for h in headers) * kicker_size * LEADING + 8.0
    for c, h in enumerate(headers):
        texts.append(TextOp(x=P + c * colW + colW / 2, y=y + hh / 2, size=kicker_size,
                            text=h, role="ink-mute", weight="bold", max_w=colW, field=f"headers[{c}]"))
    y += hh

    ops: list = [RectOp(x=0.0, y=0.0, w=W, h=0.1, rx=0.0, fill_role="paper",
                        stroke_role="rule", stroke_w=0.0)]
    for r, row in enumerate(rows):
        lines = max(budget.line_count(cell, colW, cx_size, CELL_PAD, pack) for cell in row)
        rh = lines * cx_size * LEADING + 8.0
        for c, cell in enumerate(row):
            first = c == 0
            ops.append(RectOp(x=P + c * colW, y=y, w=colW, h=rh, fill_role="surface-tint"))
            texts.append(TextOp(x=P + c * colW + colW / 2, y=y + rh / 2, size=cx_size,
                                text=cell, role="ink" if first else "ink-soft",
                                weight="bold" if first else "regular", max_w=colW,
                                field=f"cell[{r}][{c}]"))
        y += rh
    y += 12.0
    y = _footer(fence, texts, y, cx_size, W)
    return _finish(ops, texts, W, y, H_frame, fence.index)


def _qualitative(fence: Fence, tokens: dict) -> FigModel:
    frame = tokens["body_frame_pt"]
    W, H_frame = frame["x1"] - frame["x0"], frame["y1"] - frame["y0"]
    pack = tokens.get("style", "practical")
    kicker_size, title_size, ct_size, cx_size, body = _sizes(tokens)
    xa, ya, cells = fence.data["x_axis"], fence.data["y_axis"], fence.data["cells"]

    texts: list[TextOp] = []
    y = _header_block(fence, tokens, W, texts)

    # x축 라벨 행(하단 축 위) + y축 라벨(좌측 열) — 축 라벨 폭 40pt
    AXIS_W = 40.0
    cellW = (W - 2 * P - AXIS_W - G) / 2

    # y축 라벨(low 위, high 아래) — 각 셀 행 중심
    def cell_h(cell: dict) -> float:
        return 2 * 10.0 + budget.line_count(cell["title"], cellW, ct_size, 8.0, pack) * ct_size * LEADING \
            + 4.0 + budget.line_count(cell["text"], cellW, cx_size, 8.0, pack) * cx_size * LEADING

    if cellW < MIN_QUAL_W:
        raise MatrixLayoutError(
            f"정성 셀폭 {cellW:.1f}pt < {MIN_QUAL_W:.0f}pt — 문구 축약 또는 축 라벨 축소")

    h0 = max(cell_h(cells[0]), cell_h(cells[1]))
    h1 = max(cell_h(cells[2]), cell_h(cells[3]))
    # x 라벨(2칸: low/high) 위 행
    xl_h = kicker_size * LEADING + 6.0
    for j, lab in enumerate((xa["low"], xa["high"])):
        texts.append(TextOp(x=P + AXIS_W + j * (cellW + G) + cellW / 2, y=y + xl_h / 2,
                            size=kicker_size, text=lab, role="ink-mute", field=f"axis.x{j}"))
    y += xl_h
    ops: list = [RectOp(x=0.0, y=0.0, w=W, h=0.1, rx=0.0, fill_role="paper",
                        stroke_role="rule", stroke_w=0.0)]
    for r, (ylab, pair, hh) in enumerate(((ya["low"], (cells[0], cells[1]), h0),
                                          (ya["high"], (cells[2], cells[3]), h1))):
        ry = y + sum((h0, h1)[:r]) + G * r
        texts.append(TextOp(x=P + AXIS_W / 2, y=ry + hh / 2, size=kicker_size,
                            text=ylab, role="ink-mute", weight="bold", max_w=AXIS_W,
                            field=f"axis.y{r}"))
        for j, cell in enumerate(pair):
            cx = P + AXIS_W + j * (cellW + G)
            idx = r * 2 + j
            ops.append(RectOp(x=cx, y=ry, w=cellW, h=hh))
            texts.append(TextOp(x=cx + cellW / 2, y=ry + 10.0 + budget.line_count(
                cell["title"], cellW, ct_size, 8.0, pack) * ct_size * LEADING / 2,
                size=ct_size, text=cell["title"], role="ink", weight="bold",
                max_w=cellW, field=f"cells[{idx}].title"))
            texts.append(TextOp(x=cx + cellW / 2, y=ry + hh - 10.0 - budget.line_count(
                cell["text"], cellW, cx_size, 8.0, pack) * cx_size * LEADING / 2,
                size=cx_size, text=cell["text"], role="ink-soft", max_w=cellW,
                field=f"cells[{idx}].text"))
    y = y + h0 + h1 + G
    y += 12.0
    y = _footer(fence, texts, y, cx_size, W)
    return _finish(ops, texts, W, y, H_frame, fence.index)
```

`parse.py` matrix 검증 분기(layout == "matrix"):

```python
    if layout == "matrix":
        if "headers" in d:
            headers = d["headers"]
            rows = d.get("rows", [])
            if not isinstance(headers, list) or not (2 <= len(headers) <= 5):
                raise ParseError(index, f"headers 개수 — 하한 2, 상한 5", line)
            if not isinstance(rows, list) or not (2 <= len(rows) <= 6):
                raise ParseError(index, "rows 개수 — 하한 2(스펙 §3.2), 상한 6", line)
            for r, row in enumerate(rows):
                if not isinstance(row, list) or len(row) != len(headers):
                    raise ParseError(index, f"rows[{r}] 열 수 불일치(headers {len(headers)}열)", line)
                for c, cell in enumerate(row):
                    if not str(cell).strip():
                        raise ParseError(index, f"rows[{r}][{c}] 비어 있음", line)
            data["headers"] = [str(h).strip() for h in headers]
            data["rows"] = [[str(c).strip() for c in row] for row in rows]
        else:
            for k in ("x_axis", "y_axis"):
                ax = d.get(k)
                if not isinstance(ax, dict) or not str(ax.get("low", "")).strip() or not str(ax.get("high", "")).strip():
                    raise ParseError(index, f"{k}.low/.high 필수", line)
            cells = d.get("cells", [])
            if not isinstance(cells, list) or len(cells) != 4:
                raise ParseError(index, "cells 정확히 4개(2×2)", line)
            for i, c in enumerate(cells):
                if not isinstance(c, dict) or not str(c.get("title", "")).strip() or not str(c.get("text", "")).strip():
                    raise ParseError(index, f"cells[{i}].title/.text 비어 있음", line)
            data["x_axis"] = {"low": str(d["x_axis"]["low"]).strip(), "high": str(d["x_axis"]["high"]).strip()}
            data["y_axis"] = {"low": str(d["y_axis"]["low"]).strip(), "high": str(d["y_axis"]["high"]).strip()}
            data["cells"] = [{"title": str(c["title"]).strip(), "text": str(c["text"]).strip()} for c in cells]
```

`layout.py` dispatch에 matrix 등록. `lint.py` fields에 matrix 반영:

`lint.py` fields에 matrix 전 요소(축 라벨 포함 — 적대 검토 G2):

```python
        for c, h in enumerate(f.data.get("headers", [])):
            fields.append((f"headers[{c}]", h))
        for r, row in enumerate(f.data.get("rows", [])):
            for c, cell in enumerate(row):
                fields.append((f"cell[{r}][{c}]", cell))
        for i, cell in enumerate(f.data.get("cells", [])):
            fields.append((f"cells[{i}].title", cell["title"]))
            fields.append((f"cells[{i}].text", cell["text"]))
        if "x_axis" in f.data:
            fields.append(("axis.x0", f.data["x_axis"]["low"]))
            fields.append(("axis.x1", f.data["x_axis"]["high"]))
        if "y_axis" in f.data:
            fields.append(("axis.y0", f.data["y_axis"]["low"]))
            fields.append(("axis.y1", f.data["y_axis"]["high"]))
```

`render.py _sheet_rows`에 matrix 행 추가(Task 1의 `# matrix·lanes 행은 Task 2·3에서` 주석 자리에):

```python
    for c, h in enumerate(f.data.get("headers", [])):
        rows.append((f"headers[{c}]", h))
    for r, row in enumerate(f.data.get("rows", [])):
        for c, cell in enumerate(row):
            rows.append((f"cell[{r}][{c}]", cell))
    for i, cell in enumerate(f.data.get("cells", [])):
        rows.append((f"cells[{i}].title", cell["title"]))
        rows.append((f"cells[{i}].text", cell["text"]))
    for ax in ("x_axis", "y_axis"):
        if ax in f.data:
            rows.append((f"axis.{ax[0]}0", f.data[ax]["low"]))
            rows.append((f"axis.{ax[0]}1", f.data[ax]["high"]))
```

- [ ] **Step 4: 통과 확인**

Run: `cd /mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook-typst && python3 -m pytest tests/test_infographic_layout_matrix.py tests/ -q`
Expected: 신규 9(골든 IG_REGEN_GOLDEN 절차) + 전체 173

- [ ] **Step 5: 커밋**

```bash
git add skills/korean-ebook-typst/scripts/infographic/ skills/korean-ebook-typst/tests/test_infographic_layout_matrix.py skills/korean-ebook-typst/tests/fixtures/infographic/golden-matrix-practical.typ
git commit -m "feat: matrix archetype — 비교 격자·정성 2×2·quadrant 별칭·판형 열수 상한"
```

---

### Task 3: flow swimlane 변형 + kicker/thesis 지오메트리 테스트 보강

**Files:**
- Modify: `archetypes/flow.py` (lanes 배치 + `layout()`을 `_steps`/`_lanes`로 분리), `parse.py` (lanes 검증), `lint.py` (lanes 필드), `render.py` `_sheet_rows` (lanes 행)
- Test: `skills/korean-ebook-typst/tests/test_infographic_layout_flow_lanes.py`

**Interfaces:**
- lanes 데이터(스펙 §3.2): `lanes[]` 2~4({actor 필수, steps[] 2~4 {title, text}}). `steps`와 배타 — 둘 다 있으면 ParseError.
- 지오메트리(개정 — 적대 검토 G1: GS=16은 샤프트 가시 ≥12pt와 양립 불가. `_harrow` 오프셋(+4/−8)에서 샤프트 = GS−12이므로 **GS=24** 고정 — practical m=4 셀폭 43.6pt<45와의 동시 충족이 수학적으로 불가한 원래 설계는 폐기): actor 열 폭 `ACTOR_W=60`, 셀 간 `GS=24`, `cellW = (W − 2P − ACTOR_W − (m−1)·GS)/m`, `MIN_CELL_W=45`.
  - 판형별 셀 상한(수학 검증): essay m=2: (249.45−28−60−24)/2=68.7 ✓, m=3: 43.1 ✗ → **2**. practical m=3: (334.49−28−60−48)/3=66.2 ✓, m=4: 43.6 ✗ → **3**. b5 m=4: (385.51−28−60−72)/4=56.4 ✓ → **4**. business m=4: 73.4 ✓ → **4**. lecture m=4: 76.2 ✓ → **4**.
  - `PACK_LANE_CELLS = {"essay": 2, "practical": 3, "b5": 4, "business": 4, "lecture": 4}` — 스펙 §6.2 표 swimlane 행(개정 4판).
- 레인 행: actor 라벨(굵게, ACTOR_W 열) + 가로 셀 배열. 레인 간 `G`(28). 셀 간 세로 화살표 없음 — 가로 진행만(순서 셀 → 다음 셀 가로 open-V).
- kicker/thesis 테스트 보강(Phase 1 T5 deferred): kicker 있는 flow + thesis 있는 flow의 TextOp field/좌표 단언 추가(이 Task가 flow.py를 다시 만지므로).

- [ ] **Step 1: 실패 테스트 작성**

```python
"""test_infographic_layout_flow_lanes.py — 스펙 §6.3 flow(swimlane) + T5 보강."""
import json
from pathlib import Path

import pytest

from scripts.infographic.archetypes import flow as flow_arch
from scripts.infographic.model import RectOp, TextOp
from scripts.infographic.parse import ParseError, parse_fence

TOKENS = json.loads((Path(__file__).resolve().parents[1] / "styles" / "practical" / "tokens.json").read_text(encoding="utf-8"))
W = TOKENS["body_frame_pt"]["x1"] - TOKENS["body_frame_pt"]["x0"]
P, GS, ACTOR_W = 14.0, 24.0, 60.0


def _lane_fence(nlanes=2, nsteps=3):
    lanes = [{"actor": f"주체 {i+1}",
              "steps": [{"title": f"단계 {j+1}", "text": "근거"} for j in range(nsteps)]}
             for i in range(nlanes)]
    return parse_fence(1, 1, json.dumps(
        {"layout": "flow", "title": "레인 흐름", "lanes": lanes}, ensure_ascii=False))


def test_two_lanes_three_steps_geometry():
    fig = flow_arch.layout(_lane_fence(2, 3), TOKENS)
    cells = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
    assert len(cells) == 6                                   # 2레인 × 3셀
    expect = (W - 2 * P - ACTOR_W - 2 * GS) / 3              # 66.2pt
    assert abs(cells[0].w - expect) < 0.01
    assert cells[0].x == P + ACTOR_W
    assert len({round(c.y, 2) for c in cells}) == 2          # 레인 2행


def test_lane_actors_bold_labels():
    fig = flow_arch.layout(_lane_fence(2, 3), TOKENS)
    actors = [t for t in fig.ops if isinstance(t, TextOp) and t.field == "lanes[0].actor"]
    assert actors and actors[0].weight == "bold"


def test_lane_arrows_meet_shaft_minimum():
    # §6.1 샤프트 ≥12pt — GS=24에서 12pt(적대 검토 G1 회귀 방어)
    from scripts.infographic.lint import check
    figs = {1: flow_arch.layout(_lane_fence(2, 3), TOKENS)}
    fence = _lane_fence(2, 3)
    found = check([fence], figs, TOKENS, "원문", "ch01.md")
    assert not [f for f in found if f.kind == "connector"]


def test_three_cells_essay_rejected():
    # essay 상한 2(parse 2~4 내부) — layout 판형 상한 경로(도달 가능 경로로 정정)
    ET = json.loads((Path(__file__).resolve().parents[1] / "styles" / "essay" / "tokens.json").read_text(encoding="utf-8"))
    with pytest.raises(flow_arch.FlowLayoutError, match="셀"):
        flow_arch.layout(_lane_fence(1, 3), ET)


def test_both_steps_and_lanes_rejected():
    body = json.dumps({"layout": "flow", "title": "t",
                       "steps": [{"title": "a", "text": "b"}],
                       "lanes": [{"actor": "x", "steps": [{"title": "c", "text": "d"}]}]},
                      ensure_ascii=False)
    with pytest.raises(ParseError, match="steps|lanes"):
        parse_fence(1, 1, body)


def test_kicker_thesis_geometry_now_tested():
    """Phase 1 T5 deferred — kicker/thesis 분기 첫 지오메트리 단언."""
    fence = parse_fence(1, 1, json.dumps({
        "layout": "flow", "title": "제목", "kicker": "CHAPTER MAP", "thesis": "한 문장 설명",
        "steps": [{"title": "a", "text": "가"}, {"title": "b", "text": "나"}]}, ensure_ascii=False))
    fig = flow_arch.layout(fence, TOKENS)
    kick = [t for t in fig.ops if isinstance(t, TextOp) and t.field == "kicker"]
    th = [t for t in fig.ops if isinstance(t, TextOp) and t.field == "thesis"]
    assert kick and kick[0].y < th[0].y                      # kicker가 thesis 위
    assert kick[0].size == TOKENS["fonts"]["label"]["size_pt"]
```

- [ ] **Step 2: 실패 확인**

Run: `cd /mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook-typst && python3 -m pytest tests/test_infographic_layout_flow_lanes.py -v`
Expected: FAIL — lanes 미지원(ParseError)

- [ ] **Step 3: 최소 구현**

`parse.py` flow 분기 확장(steps/lanes 배타 + lanes 검증):

```python
    if layout == "flow":
        has_steps, has_lanes = "steps" in d, "lanes" in d
        if has_steps and has_lanes:
            raise ParseError(index, "steps와 lanes는 배타 — 하나만", line)
        if has_lanes:
            lanes = d["lanes"]
            if not isinstance(lanes, list) or not (2 <= len(lanes) <= 4):
                raise ParseError(index, "lanes 개수 — 하한 2, 상한 4", line)
            for i, ln in enumerate(lanes):
                if not isinstance(ln, dict) or not str(ln.get("actor", "")).strip():
                    raise ParseError(index, f"lanes[{i}].actor 필수", line)
                sts = ln.get("steps", [])
                if not isinstance(sts, list) or not (2 <= len(sts) <= 4):
                    raise ParseError(index, f"lanes[{i}].steps 개수 — 하한 2, 상한 4", line)
                for j, s in enumerate(sts):
                    if not str(s.get("title", "")).strip() or not str(s.get("text", "")).strip():
                        raise ParseError(index, f"lanes[{i}].steps[{j}].title/.text 비어 있음", line)
            data["lanes"] = [{"actor": str(ln["actor"]).strip(),
                              "steps": [{"title": str(s["title"]).strip(),
                                         "text": str(s["text"]).strip()} for s in ln["steps"]]}
                             for ln in lanes]
        else:
            # 기존 steps 검증 그대로
            ...
```

`flow.py` lanes 배치 — `layout()` 초반, steps/lanes 분기:

```python
PACK_LANE_CELLS = {"essay": 2, "practical": 3, "b5": 4, "business": 4, "lecture": 4}
ACTOR_W = 60.0
GS = 24.0        # 샤프트 가시 = GS−12 ≥ 12(§6.1) — 16 금지(적대 검토 G1)
MIN_CELL_W = 45.0

def _lanes(fence, tokens, W, H_frame, pack, sizes):
    kicker_size, title_size, ct_size, cx_size = sizes
    lanes = fence.data["lanes"]
    m = max(len(ln["steps"]) for ln in lanes)
    limit = PACK_LANE_CELLS.get(pack)
    if limit is None:
        raise FlowLayoutError(f"알 수 없는 스타일 팩 {pack!r}")
    if m > limit:
        raise FlowLayoutError(f"레인 셀 {m}개 > 판형 상한 {limit}({pack}) — 요소 수 감소 또는 펜스 분할")
    cellW = (W - 2 * P - ACTOR_W - (m - 1) * GS) / m
    if cellW < MIN_CELL_W:
        raise FlowLayoutError(
            f"셀폭 {cellW:.1f}pt < {MIN_CELL_W:.0f}pt — 요소 수 감소 또는 문구 축약")
    texts: list = []
    y = _header(fence, tokens, W, texts, pack)       # 기존 헤더 블록을 함수로 추출(아래 주석)
    def cell_h(s):
        return 2 * 10.0 + budget.line_count(s["title"], cellW, ct_size, 8.0, pack) * ct_size * LEADING \
            + 4.0 + budget.line_count(s["text"], cellW, cx_size, 8.0, pack) * cx_size * LEADING
    ops = [RectOp(x=0.0, y=0.0, w=W, h=0.1, rx=0.0, fill_role="paper", stroke_role="rule", stroke_w=0.0)]
    for i, ln in enumerate(lanes):
        rh = max(cell_h(s) for s in ln["steps"])
        ry = y + sum_row_heights_before + G * i        # 구현: 이전 레인 높이 누적(람다 대신 루프 내 계산)
        texts.append(TextOp(x=P + ACTOR_W / 2, y=ry + rh / 2, size=ct_size,
                            text=ln["actor"], role="ink", weight="bold",
                            max_w=ACTOR_W, field=f"lanes[{i}].actor"))
        for j, s in enumerate(ln["steps"]):
            cx = P + ACTOR_W + j * (cellW + GS)
            ops.append(RectOp(x=cx, y=ry, w=cellW, h=rh))
            _cell_texts(texts, s, cx, ry, cellW, rh, ct_size, cx_size, f"lanes[{i}].steps[{j}]", pack)
            if j:
                arrows.append(_harrow(cx - cellW - GS + cellW, ry + rh / 2, cx))
    ...
```

(구현 시 `layout()`의 steps 분기를 `_steps()`로, lanes를 `_lanes()`로 분리 — 공통 헤더/노트/높이검사는 기존 코드 재사용. **lanes 분기는 `fence.data["steps"]` 접근보다 앞에** 둔다 — lanes 펜스에서 steps가 비어 있으면 cardW 산출이 ZeroDivision된다. 화살표는 기존 `_harrow(이전셀우단, y중심, 다음셀좌단)` 그대로 — 이전셀우단 = `이전셀.x + cellW` = `cx − GS`. 의사 루프의 `sum_row_heights_before`는 루프 내 누적 변수로 직접 계산한다.)

`lint.py` fields에 lanes:

```python
        for i, ln in enumerate(f.data.get("lanes", [])):
            fields.append((f"lanes[{i}].actor", ln["actor"]))
            for j, s in enumerate(ln["steps"]):
                fields.append((f"lanes[{i}].steps[{j}].title", s["title"]))
                fields.append((f"lanes[{i}].steps[{j}].text", s["text"]))
```

- [ ] **Step 4: 통과 확인**

`render.py _sheet_rows`에 lanes 행 추가:

```python
    for i, ln in enumerate(f.data.get("lanes", [])):
        rows.append((f"lanes[{i}].actor", ln["actor"]))
        for j, s in enumerate(ln["steps"]):
            rows.append((f"lanes[{i}].steps[{j}].title", s["title"]))
            rows.append((f"lanes[{i}].steps[{j}].text", s["text"]))
```

- [ ] **Step 4: 통과 확인**

Run: `cd /mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook-typst && python3 -m pytest tests/test_infographic_layout_flow_lanes.py tests/ -q`
Expected: 신규 6 + 전체 179 (기존 flow 테스트 무회귀)

- [ ] **Step 5: 커밋**

```bash
git add skills/korean-ebook-typst/scripts/infographic/ skills/korean-ebook-typst/tests/test_infographic_layout_flow_lanes.py
git commit -m "feat: flow swimlane 변형 — 레인 배치(GS=24 샤프트 계약)·판형 셀 상한 + kicker/thesis 지오메트리 테스트"
```

---

### Task 4: authoring.md 갱신 + 골든 교정 1주기 (팩별 계수 실측)

**Files:**
- Modify: `references/infographic/authoring.md` (라우팅 표 cards/matrix/flow-lanes 사용 가능 전환 + 치트시트 3종 반영)
- Modify: `scripts/infographic/budget.py` (PACK_KO_FACTOR 실측값)
- Test: 기존 스위트 회귀 (골든 바이트 불변 확인 — practical 계수가 1.0에서 바뀌면 flow 골든 재확정 필요)

**절차 (골든 교정 1주기 — 스펙 §7·§8-2, 판정 계약 포함):**
1. 각 팩 1순위 폰트로 cards fixture(치트시트 상한 근처 문구)를 `cli.py preview --style <pack>`로 렌더.
2. 오버플로 한계 실측 — **측정 단위: KO 환산 pt**(문구를 KO 글자 수로 조절, budget.max_units 예상 대비 실제 잘림 시작 글자 수).
3. **판정 계약(결정론)**: `비율 = 예상수용KO자수 / 실측수용KO자수`. `|비율 − 1.0| < 0.05`면 데드밴드 — `PACK_KO_FACTOR` 1.0 유지. 벗어나면 비율을 소수 2자리로 반올림해 계수로.
4. **기록 계약**: (a) budget.py `PACK_KO_FACTOR` 각 팩 인라인 주석에 실측치·날짜, (b) authoring.md 치트시트 각주에 근거, (c) 커밋 메시지에 5팩 수치 전부.
5. 전 스위트 — 계수 변화 팩이 practical이면 flow/cards/matrix 골든 `IG_REGEN_GOLDEN=1` 재확정·눈검·커밋(다른 팩은 골든 없음).
6. authoring.md: 라우팅 표 3행(cards·matrix·flow-lanes) "사용 가능" 전환, 각 archetype 펜스 예시·치트시트(카드폭 139.2/83.5·셀폭 76.6·swimlane 셀 66.2) 추가. **lecture cards 열수 3 고정 결정 근거**(스펙 "3~4" 범위 내 고정 — §2 결정론 원칙)도 명시.

**완료 판정**: 5팩 전부 preview 렌더 성공 + 계수 갱신 또는 데드밴드 유지 기록(기록 계약 3곳) + authoring.md 갱신 + 스위트 그린 + 골든 상태 정리. **병합 게이트: 이 Task 완료 전 main 병합 금지.**

- [ ] **Step 1: 교정 실시** (위 절차 1-3)
- [ ] **Step 2: 골든 정리** (절차 4 — 필요시 재확정)
- [ ] **Step 3: authoring.md 갱신**
- [ ] **Step 4: 전체 회귀 + 수동 눈검** (cards 3장·matrix 4×3·swimlane 2레인 각 1회 preview)
- [ ] **Step 5: 커밋**

```bash
git add skills/korean-ebook-typst/references/infographic/authoring.md skills/korean-ebook-typst/scripts/infographic/budget.py skills/korean-ebook-typst/tests/fixtures/
git commit -m "docs: Phase 2 가이드 갱신 + 골든 교정 1주기 — 팩별 계수 실측"
```

---

## Self-Review 결과 (적대 검토 2관점 반영 후)

- **반영된 적대 검토(2026-08-22, 코드 실행 실증 + 계약 검토)**: G1 8건 — ① render/cli가 신규 에러 타입 미캐치 → 공통 `base.LayoutError` 베이스(Task 1) ② lint `f.data["steps"]` KeyError → `.get` 전환 ③ `_review_sheet` steps 순회 → `_sheet_rows` archetype별 전 요소 ④ GS=16 샤프트 4pt 위반 → GS=24·PACK_LANE_CELLS {2,3,4,4,4} 재유도(스펙 §6.2 swimlane 행 추가) ⑤ 정성 cellW 테스트·구현 20pt 불일치 → AXIS_W 반영 ⑥ matrix `_finish` TextOp 누락 → ops+texts 합산 ⑦ test_seven_cards 도달 불가 → essay n=5 경로 ⑧ test_five_cells 도달 불가 → essay 3셀 경로 + 샤프트 최소 회귀 테스트. G2 — quadrant 별칠·VALID_LAYOUTS 명시, rows 하한 2, cards/matrix 골든 추가, essay 정성 floor 60(MIN_QUAL_W), 축 라벨 lint 필드, cli 캐치. G3 — 교정 데드밴드·기록 계약, 병합 게이트, H_frame 감산 정리, unknown-layout 동적 메시지, lecture 3 고정 근거 기록, lanes ZeroDivision 사유 명시, 인터페이스 "첫 열 stroke_rule" 문구 정합화.
- 스펙 커버리지: §6.2 상한 표(PACK_COLS·PACK_MAX_COLS·PACK_LANE_CELLS — swimlane 행은 개정 4판 추가) / §6.3 cards·matrix·flow(swimlane) / §3.2 데이터(value·x_axis·y_axis·cells·lanes) / §3.4 별칭 principles·dashboard·quadrant / §7 archetype 골든 / §8-2 골든 교정 1주기.
- 플레이스홀더: Task 3은 기존 flow.py 재사용 분리 작업 — 신규 산술(cellW·셀높이·레인 누적)은 완전 산식 제공, 레이아웃 뼈대는 구조 지정.
- 타입 일관성: LayoutError 베이스 상속 체계(Task 1 확정) — render/cli는 베이스만 catch. FigModel.source_index 직접 반환(matrix `_finish` 재포장 제거).
