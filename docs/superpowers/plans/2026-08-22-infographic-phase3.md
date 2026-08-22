# 인포그래픽 레이어 Phase 3 (before_after + ladder + roadmap) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Phase 2(cards·matrix·swimlane)에 이어 before_after·ladder·roadmap archetype 3종을 추가하고, 골든 교정 2주기로 예산 계수를 실측 갱신한다.

**Architecture:** Phase 1·2와 동일 — parse(스키마)→layout(archetype별 순수 함수)→lint(I1)→emit(ops→typst). 신규 archetype은 `archetypes/`에 모듈 추가 + `layout.dispatch` 등록 + `parse` 검증 분기 확장 + lint 필드·render 검수 시트 행 확장. model.py ops 재사용(RectOp/TextOp/ArrowOp 변경 없음).

**Tech Stack:** Python 3.12 표준 라이브러리, typst 0.15.1, pytest. 신규 의존 0.

**Spec:** `docs/superpowers/specs/2026-08-21-infographic-layer-design.md` (개정 4판)

**Phase 1·2 자산 (main 병합 완료, korean-ebook-typst 스위트 181 green):** `scripts/infographic/` 전 모듈(flow·cards·matrix + base.LayoutError), `templates/infographic/helper.typ`, authoring.md(Phase 2판), 골든 3종(flow·cards·matrix practical). 테스트 관례: `tests/conftest.py`가 스킬 루트 sys.path 추가, `from scripts.infographic.x import y`.

**개정 2판 (플랜 적대검토 반영):** C1 패널 폭 상수(CENTER_ZONE 104→56, G 20→14, MIN_PANEL_W 100→65) · C2 ladder 높이 기준점·note 위치 · C3 ladder 화살표 앵커(겹침역 관통) · C4 도달 불가 테스트 2건 교체 · C5 MIN_BAND_W 70→54(스펙 §6.2 상한 표와 양립 — 개정 5판 불필요, essay 3밴드 55.2pt 실측) · I1~I3·m1~m7.

## Global Constraints (Phase 1·2와 동일 + 추가)

- 외부 의존 금지, 펜스 JSON, 결정론(같은 입력=같은 방출 바이트), hex 금지(역할명), leading 1.3em, G3 불변식(본문±0.3pt 밖 — essay 예외 +1.5), I1 메시지 계약(loc/측정값/저자 레버), typst_binary() 재use, timeout=120.
- 모든 archetype 에러는 `archetypes/base.py`의 `LayoutError` 상속(`XLayoutError(LayoutError)`) — render.py·cli.py는 베이스만 catch. 신규 archetype도 즉시 준수.
- lint 필드·검수 시트는 `f.data.get(...)` 접근(KeyError 금지) — 신규 archetype 요소 전부 행으로(§5.4).
- 잉크 bbox 프레임 내 보장(`_ink_ok` 패턴), 높이 85% 한계, TextOp.field 계약(예: `before[2]`, `stages[1].title`, `phases[0].items[2]`).
- **높이·폭 예산은 전부 `budget.line_count` 실측** — 1줄 가정 금지(Phase 2 최종 리뷰 수정 1건의 원칙: card_h/_card_texts 파라미터 일치).
- 판형 상한은 layout이 즉시 에러(스펙 §6.2). 상한 검사는 parse 하한·상한(절대)과 별개 경로 — 양쪽 모두 도달 가능 테스트 유지.
- 판형 상한(§6.2 표): before_after 항목/측 essay 3 / practical 4 / b5 4 / business 5 / lecture 5. roadmap 위상 essay 3 / practical 4 / b5 4 / business 5 / lecture 5. **ladder는 판형 표에 없음 — 절대 3~5만**(하한 3).
- 절대 상한(§3.2): before_after 항목 1~5/측, ladder stages 3~5, roadmap 위상 2~5.
- 별칭 확장: `bridge` → `before_after`(스펙 §3.4). ladder·roadmap 별칭 없음.
- 텍스트 크기: 패널/밴드 제목=본문+1, 항목/본문=본문−1, 제목=H2(essay +1.5), 라벨=label 크기 — Phase 2 cards 관례.
- **archetype별 골든 스냅샷 필수**(스펙 §7·§8) — 3종 각 1개 practical, `IG_REGEN_GOLDEN=1` 절차.
- **골든 교정 2주기**: 신규 3종 calib fixture 실렌더 → 예산표(§4.3) 갱신 — Phase 2 Task 4 절차 반복.
- **병합 게이트**: Task 4(authoring.md 갱신) 완료 전 main 병합 금지.
- 커넥터 상수: 커넥터 복도가 있는 간격(roadmap 밴드 G=28)은 샤프트 가시 ≥12pt 계약 유지(§6.1). before_after의 G=14는 패널-중앙존 순수 여백(복도 아님). 화살표 tip-gap은 8pt(§6.1 밴드 8~12 — flow 선례 +4/−8와 동일 이유로 6pt 미달 금지). ARROW_STROKE_W 1.2·헤드비 3.33(model.py 상수 재use).
- **상수 확정(적대검토 C1·C5)**: before_after `CENTER_ZONE=56.0`·`G=14.0`·`MIN_PANEL_W=65.0` → panel_w practical 111.2 / essay 68.7 / b5 136.8 / business 170.8 / lecture 176.4. roadmap `MIN_BAND_W=54.0`(G=28 유지) → 각 팩 스펙 상한 n에서 essay 55.2 / practical 55.6 / b5 68.4 / business 62.7 / lecture 65.0 — 전팩 상한 도달 가능(밴드 폭 55pt는 항목 초단문 계약, authoring에 명시).
- 텍스트 크기 pad: lint 예산 재검사 pad=8(lint.py 관례)와 일치 — archetype 내부 pad 전부 8.0 고정.

---

### Task 1: before_after archetype + 소비자 확장

**Files:**
- Create: `skills/korean-ebook-typst/scripts/infographic/archetypes/before_after.py`
- Modify: `skills/korean-ebook-typst/scripts/infographic/parse.py` (별칭·VALID_LAYOUTS·검증 분기)
- Modify: `skills/korean-ebook-typst/scripts/infographic/layout.py` (dispatch 등록)
- Modify: `skills/korean-ebook-typst/scripts/infographic/lint.py` (before/after/center 필드)
- Modify: `skills/korean-ebook-typst/scripts/infographic/render.py` (`_sheet_rows` before/after/center 행)
- Test: `skills/korean-ebook-typst/tests/test_infographic_layout_before_after.py`

**Interfaces:**
- Consumes: `base.LayoutError`, `budget.line_count(text, box_w, size_pt, pad, pack)`, `model.RectOp/TextOp/ArrowOp/FigModel`, `parse.Fence/ParseError/DEFAULT_NOTE`
- Produces: `archetypes.before_after.layout(fence, tokens) -> FigModel`, `BeforeAfterLayoutError`, 펜스 데이터 키 `before[]`·`after[]`(문자열 배열)·`center`(선택)·`before_label`/`after_label`(선택, 기본 "이전"/"이후")

**데이터 설계(스펙 §3.2 `before[]`, `after[]`, `center` 라벨):** 항목은 문자열(짧은 문구). 좌우 패널 헤더 라벨은 `before_label`/`after_label` 선택 필드, 기본 "이전"/"이후". `center`는 전환 라벨(선택 — 없으면 화살표만).

**지오메트리(스펙 §6.3 "좌우 패널 + 중앙 전환 화살표"):** 패널 폭 `panel_w = (W − 2P − CENTER_ZONE − 2G) / 2`, `CENTER_ZONE = 56.0`(화살표 + center 라벨), `G = 14.0`. 패널 높이 = 양측 항목 실측 최댓값. 화살표는 패널 수직 중심(tip-gap 양측 8pt), center 라벨은 화살표 위.

- [ ] **Step 1: parse 실패 테스트 작성**

```python
# tests/test_infographic_layout_before_after.py — 초반부
"""test_infographic_layout_before_after.py — 스펙 §6.2·§6.3 before_after 지오메트리·결정론."""
import json
from pathlib import Path

import pytest

from scripts.infographic.archetypes import before_after as ba_arch
from scripts.infographic.model import ArrowOp, FigModel, RectOp, TextOp
from scripts.infographic.parse import ParseError, parse_fence

TOKENS = json.loads((Path(__file__).resolve().parents[1] / "styles" / "practical" / "tokens.json").read_text(encoding="utf-8"))
W = TOKENS["body_frame_pt"]["x1"] - TOKENS["body_frame_pt"]["x0"]
P, G = 14.0, 14.0
CENTER_ZONE = 56.0


def _fence(before, after, center=None, **extra):
    d = {"layout": "before_after", "title": "전환 제목",
         "before": before, "after": after}
    if center:
        d["center"] = center
    d.update(extra)
    return parse_fence(1, 1, json.dumps(d, ensure_ascii=False))


def test_parse_rejects_empty_item():
    # 빈 항목은 after 측에 — 구현 에러문은 f"{side}[{i}]" (I1 정합)
    with pytest.raises(ParseError, match=r"after\[1\] 비어 있음"):
        _fence(["항목"], ["항목", "  "])


def test_parse_rejects_over_absolute_cap():
    with pytest.raises(ParseError, match=r"before 항목 수 6"):
        _fence([f"항목 {i}" for i in range(6)], ["항목"])


def test_alias_bridge_routes_to_before_after():
    body = json.dumps({"layout": "bridge", "title": "t",
                       "before": ["a"], "after": ["b"]}, ensure_ascii=False)
    f = parse_fence(1, 1, body)
    assert f.layout == "before_after"
```

- [ ] **Step 2: 실행 — ParseError으로 실패 확인**

Run: `python3 -m pytest skills/korean-ebook-typst/tests/test_infographic_layout_before_after.py -q` (워크트리 루트에서)
Expected: FAIL — `bridge` unknown layout / 검증 분기 부재

- [ ] **Step 3: parse.py 확장**

```python
# parse.py 상수부 — 기존 행 수정·추가
ALIASES = {"process": "flow", "principles": "cards", "dashboard": "cards",
           "quadrant": "matrix", "bridge": "before_after"}
VALID_LAYOUTS = {"flow", "cards", "matrix", "before_after"}   # Phase 1·2·3
STEP_MIN, STEP_MAX = 2, 8
CARD_MIN, CARD_MAX = 2, 6
LANE_MIN, LANE_MAX = 2, 4
BA_ITEM_MIN, BA_ITEM_MAX = 1, 5          # 스펙 §3.2 before_after 항목/측
```

검증 분기(`if layout == "matrix":` 블록 뒤에 추가):

```python
    if layout == "before_after":
        for side in ("before", "after"):
            items = d.get(side, [])
            if not isinstance(items, list) or not (BA_ITEM_MIN <= len(items) <= BA_ITEM_MAX):
                n = len(items) if isinstance(items, list) else 0
                raise ParseError(index, f"{side} 항목 수 {n} — 하한 {BA_ITEM_MIN}, 상한 {BA_ITEM_MAX}(스펙 §3.2)", line)
            for i, it in enumerate(items):
                if not str(it).strip():
                    raise ParseError(index, f"{side}[{i}] 비어 있음", line)
            data[side] = [str(it).strip() for it in items]
        center = str(d.get("center", "")).strip()
        if center:
            data["center"] = center
        for k in ("before_label", "after_label"):
            v = str(d.get(k, "")).strip()
            if v:
                data[k] = v
```

- [ ] **Step 4: parse 테스트 통과 확인**

Run: 위와 동일. Expected: parse 3건 PASS (layout 테스트는 여전 FAIL)

- [ ] **Step 5: layout 지오메트리 실패 테스트 추가**

```python
def test_two_panels_and_center_arrow_practical():
    fig = ba_arch.layout(_fence(["문장 A", "문장 B"], ["문장 C", "문장 D", "문장 E"],
                                center="AI 도입"), TOKENS)
    panels = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
    assert len(panels) == 2
    panel_w = (W - 2 * P - CENTER_ZONE - 2 * G) / 2
    assert abs(panels[0].w - panel_w) < 0.01
    assert abs(panels[0].x - P) < 0.01
    assert abs(panels[1].x - (W - P - panel_w)) < 0.01
    assert panels[0].h == panels[1].h                      # 양측 동일 높이
    arrows = [o for o in fig.ops if isinstance(o, ArrowOp)]
    assert len(arrows) == 1
    a = arrows[0]
    assert a.x1 < a.x2 and abs(a.y1 - a.y2) < 0.01         # 수평
    assert a.x1 > panels[0].x + panels[0].w                # 좌패널 우변보다 오른쪽
    assert a.x2 < panels[1].x                              # 우패널 좌변보다 왼쪽
    fields = {t.field for t in fig.ops if isinstance(t, TextOp)}
    assert {"before[0]", "before[1]", "after[2]", "center", "before_label", "after_label"} <= fields


def test_panel_height_measured_multi_line_items():
    short = ba_arch.layout(_fence(["짧"], ["짧"]), TOKENS)
    long_ = ba_arch.layout(_fence(["근거 문장이 패널 폭을 넘어 두 줄 이상으로 감싸지는 긴 항목"], ["짧"]), TOKENS)
    p_short = [r for r in short.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"][0]
    p_long = [r for r in long_.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"][0]
    assert p_long.h > p_short.h + 5.0                      # 실측 반영 — 1줄 가정이면 차 0


def test_pack_cap_essay_rejects_four_items():
    essay = json.loads((Path(__file__).resolve().parents[1] / "styles" / "essay" / "tokens.json").read_text(encoding="utf-8"))
    with pytest.raises(ba_arch.BeforeAfterLayoutError, match=r"판형 상한 3개\(essay\)"):
        ba_arch.layout(_fence(["a", "b", "c", "d"], ["a"]), essay)


def test_pack_cap_success_all_packs():
    # I3 — 각 팩 상한 n에서 렌더 성공(상한 도달 가능성 실증, C1 방어)
    packs = {"essay": 3, "practical": 4, "b5": 4, "business": 5, "lecture": 5}
    for name, cap in packs.items():
        toks = json.loads((Path(__file__).resolve().parents[1] / "styles" / name / "tokens.json").read_text(encoding="utf-8"))
        fig = ba_arch.layout(_fence([f"이전 {i}" for i in range(cap)],
                                    [f"이후 {i}" for i in range(cap)], center="전환"), toks)
        panels = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
        assert len(panels) == 2, name
```

- [ ] **Step 6: 실행 — 모듈 부재로 실패 확인**

Run: 위와 동일. Expected: FAIL — `ModuleNotFoundError`/dispatch 미등록

- [ ] **Step 7: before_after.py 구현**

```python
"""before_after — 좌우 패널 + 중앙 전환(스펙 §6.2·§6.3). 결정론: 판형 상한 초과 시 즉시 에러."""
from __future__ import annotations

from .. import budget
from ..model import ArrowOp, FigModel, RectOp, TextOp
from ..parse import DEFAULT_NOTE, Fence
from .base import LayoutError

P = 14.0
G = 14.0                    # 패널-중앙존 여백(커넥터 복도 아님 — §6.1 대상 외)
CENTER_ZONE = 56.0
BA_ITEM_MIN, BA_ITEM_MAX = 1, 5
PANEL_PAD_H = 8.0           # lint 예산 pad=8과 일치
PANEL_PAD_V = 12.0
ITEM_GAP = 6.0
MIN_PANEL_W = 65.0
LEADING = 1.3
HEIGHT_LIMIT = 0.85

PACK_ITEMS = {"essay": 3, "practical": 4, "b5": 4, "business": 5, "lecture": 5}


class BeforeAfterLayoutError(LayoutError):
    pass


def layout(fence: Fence, tokens: dict) -> FigModel:
    frame = tokens["body_frame_pt"]
    W = frame["x1"] - frame["x0"]
    H_frame = frame["y1"] - frame["y0"]
    pack = tokens.get("style", "practical")
    f = tokens["fonts"]
    body = f["body"]["size_pt"]
    kicker_size = f["label"]["size_pt"]
    title_size = f["heading2"]["size_pt"]
    if abs(title_size - body) <= 0.3:
        title_size = body + 1.5
    item_size = body - 1
    side_size = kicker_size

    n = max(len(fence.data["before"]), len(fence.data["after"]))
    cap = PACK_ITEMS.get(pack)
    if cap is None:
        raise BeforeAfterLayoutError(f"알 수 없는 스타일 팩 {pack!r}")
    if n > cap:
        raise BeforeAfterLayoutError(
            f"항목 {n}개/측 > 판형 상한 {cap}개({pack}) — 항목 축약 또는 펜스 분할")

    panel_w = (W - 2 * P - CENTER_ZONE - 2 * G) / 2
    if panel_w < MIN_PANEL_W:
        raise BeforeAfterLayoutError(
            f"패널 폭 {panel_w:.1f}pt < {MIN_PANEL_W:.0f}pt({pack}) — 항목 문구 축약 또는 center 라벨 축소")

    # 패널 높이 — 항목 전부 line_count 실측(1줄 가정 금지, Phase 2 교훈)
    def items_h(items: list) -> float:
        return sum(budget.line_count(it, panel_w, item_size, PANEL_PAD_H, pack) * item_size * LEADING
                   + ITEM_GAP for it in items) - ITEM_GAP

    panel_head = side_size * LEADING + 10.0
    body_h = max(panel_head + items_h(fence.data["before"]),
                 panel_head + items_h(fence.data["after"]))
    panel_h = body_h + 2 * PANEL_PAD_V

    # 헤더(cards와 동일 구조)
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
        th = budget.line_count(fence.thesis, W - 2 * P, item_size, 0.0, pack)
        texts.append(TextOp(x=W / 2, y=cy + th * item_size * LEADING / 2, size=item_size,
                            text=fence.thesis, role="ink-soft", max_w=W - 2 * P, field="thesis"))
        cy += th * item_size * LEADING
    y = cy + 18.0

    lx, rx = P, W - P - panel_w
    py = y
    rects = [RectOp(x=lx, y=py, w=panel_w, h=panel_h),
             RectOp(x=rx, y=py, w=panel_w, h=panel_h)]

    def panel_texts(items, x0, label, side):
        out = [TextOp(x=x0 + panel_w / 2, y=py + PANEL_PAD_V + side_size * LEADING / 2,
                      size=side_size, text=label, role="ink-mute", weight="bold",
                      max_w=panel_w, field=f"{side}_label")]
        ty = py + PANEL_PAD_V + panel_head
        for i, it in enumerate(items):
            lines = budget.line_count(it, panel_w, item_size, PANEL_PAD_H, pack)
            out.append(TextOp(x=x0 + panel_w / 2, y=ty + lines * item_size * LEADING / 2,
                              size=item_size, text=it, role="ink-soft",
                              max_w=panel_w, field=f"{side}[{i}]"))
            ty += lines * item_size * LEADING + ITEM_GAP
        return out

    texts += panel_texts(fence.data["before"], lx, fence.data.get("before_label", "이전"), "before")
    texts += panel_texts(fence.data["after"], rx, fence.data.get("after_label", "이후"), "after")

    # 중앙 전환 — 수평 화살표(tip-gap 8pt, §6.1) + center 라벨(선택)
    zone_l, zone_r = lx + panel_w, rx
    ay = py + panel_h / 2
    arrows = [ArrowOp(x1=zone_l + 8.0, y1=ay, x2=zone_r - 8.0, y2=ay)]
    if fence.data.get("center"):
        texts.append(TextOp(x=(zone_l + zone_r) / 2, y=ay - kicker_size * LEADING - 4.0,
                            size=kicker_size, text=fence.data["center"], role="focus",
                            weight="bold", max_w=CENTER_ZONE + 2 * G - 16.0, field="center"))

    y = py + panel_h + 12.0
    note = fence.note or DEFAULT_NOTE
    texts.append(TextOp(x=W / 2, y=y + item_size * LEADING / 2, size=item_size,
                        text=note, role="ink-mute", max_w=W - 2 * P, field="note"))
    y += item_size * LEADING

    if y > H_frame * HEIGHT_LIMIT:
        raise BeforeAfterLayoutError(
            f"도식 높이 {y:.0f}pt > 프레임 {H_frame * HEIGHT_LIMIT:.0f}pt(85%) — "
            f"항목 축약 또는 펜스 분할")

    ops = [RectOp(x=0.0, y=0.0, w=W, h=y, rx=0.0, fill_role="paper", stroke_role="rule", stroke_w=0.0),
           *rects, *arrows, *texts]
    _ink_ok(ops, W, y)
    return FigModel(width=W, height=y, ops=tuple(ops), source_index=fence.index)


def _ink_ok(ops, width: float, height: float) -> None:
    for o in ops:
        if isinstance(o, RectOp):
            if (o.x < -0.001 or o.x + o.w > width + 0.001
                    or o.y < -0.001 or o.y + o.h > height + 0.001):
                raise BeforeAfterLayoutError(
                    f"잉크 bbox 프레임 이탈: rect({o.x:.1f},{o.y:.1f},{o.w:.1f},{o.h:.1f})")
        elif isinstance(o, ArrowOp):
            if (min(o.x1, o.x2) < -0.001 or max(o.x1, o.x2) > width + 0.001
                    or min(o.y1, o.y2) < -0.001 or max(o.y1, o.y2) > height + 0.001):
                raise BeforeAfterLayoutError(
                    f"잉크 bbox 프레임 이탈: arrow({o.x1:.1f},{o.y1:.1f}→{o.x2:.1f},{o.y2:.1f})")
        elif isinstance(o, TextOp):
            hw = (o.max_w or 60.0) / 2
            if o.x - hw < -0.001 or o.x + hw > width + 0.001:
                raise BeforeAfterLayoutError(
                    f"잉크 bbox 프레임 이탈: text({o.field}) x={o.x:.1f} max_w={o.max_w:.1f}")
```

layout.py dispatch에 등록:

```python
from .archetypes import before_after as _ba, cards as _cards, flow as _flow, matrix as _matrix
# dispatch 내부에 추가
    if fence.layout == "before_after":
        return _ba.layout(fence, tokens)
```

주의(m2 확정): 위 `_ink_ok` 코드 블록이 기준이다 — Rect+Arrow+Text 전검사. cards.py의 `_ink_ok`(Rect만·stroke_w/2 포함)와 달리 before_after는 ArrowOp·중앙 라벨이 있어 전검사가 필요하다. 임계값 ±0.001은 cards와 동일.

- [ ] **Step 8: lint·render 확장**

lint.py `check()`의 필드 수집부(`cells` 블록 뒤)에 추가:

```python
        for side in ("before", "after"):
            for i, it in enumerate(f.data.get(side, [])):
                fields.append((f"{side}[{i}]", it))
        if f.data.get("center"):
            fields.append(("center", f.data["center"]))
        for k in ("before_label", "after_label"):
            if f.data.get(k):
                fields.append((k, f.data[k]))
```

render.py `_sheet_rows()`에 동일 구조 행 추가(값은 `(field, text)` 튜플, cards 블록 뒤):

```python
    for side in ("before", "after"):
        for i, it in enumerate(f.data.get(side, [])):
            rows.append((f"{side}[{i}]", it))
    if f.data.get("center"):
        rows.append(("center", f.data["center"]))
    for k in ("before_label", "after_label"):
        if f.data.get(k):
            rows.append((k, f.data[k]))
```

- [ ] **Step 9: lint·render 테스트 추가 후 전체 통과 확인**

```python
def test_before_after_elements_reach_lint_and_sheet():
    # cards의 test_cards_lint_and_review_sheet_reach_elements 패턴을 그대로 따른다 —
    # 기존 테스트(tests/test_infographic_layout_cards.py)를 읽고 동일 구조로 작성:
    # 1) 숫자 포함 항목(before/after/center)이 I1 숫자-evidence 검사 대상에 들어가는지
    # 2) render._sheet_rows가 before[i]·after[i]·center·라벨 행을 반환하는지
    f = _fence(["예산 3배 증가", "리드타임 2주"], ["CAPEX 12% 절감"], center="전환")
    fig = ba_arch.layout(f, TOKENS)
    # 이하 기존 cards lint 테스트의 check() 호출·단언 구조를 복제(시그니처는 lint.py:51 실효 따름)
```

주의(m4): `lint.check`의 실효 시그니처는 `lint.py:51`을 직접 확인 — `check(fences, figs, tokens, chapter_md, chapter_name)`. 플랜에 시그니처를 하드코딩하지 않는다(구현자가 기존 테스트에서 복사). 검증 포인트: 숫자 포함 before/after 항목 → I1 경고 집계, 검수 시트에 전 요소 행.

Run: `python3 -m pytest skills/korean-ebook-typst/tests/ -q`
Expected: 181 + 신규 전부 PASS

- [ ] **Step 10: Commit**

```bash
git add skills/korean-ebook-typst/scripts/infographic/ skills/korean-ebook-typst/tests/test_infographic_layout_before_after.py
git commit -m "feat: before_after archetype — 좌우 패널·중앙 전환 화살표·판형 상한 + 소비자 확장"
```

---

### Task 2: ladder archetype

**Files:**
- Create: `skills/korean-ebook-typst/scripts/infographic/archetypes/ladder.py`
- Modify: `skills/korean-ebook-typst/scripts/infographic/parse.py` (검증 분기·VALID_LAYOUTS)
- Modify: `skills/korean-ebook-typst/scripts/infographic/layout.py` (dispatch)
- Modify: `skills/korean-ebook-typst/scripts/infographic/lint.py`·`render.py` (stages 필드)
- Test: `skills/korean-ebook-typst/tests/test_infographic_layout_ladder.py`

**Interfaces:**
- Consumes: Task 1과 동일 + `parse.STAGE_MIN/STAGE_MAX`
- Produces: `archetypes.ladder.layout(fence, tokens) -> FigModel`, `LadderLayoutError`, 데이터 `stages[]`({title, text} — steps 관례)

**데이터:** `stages[]` {title, text}, 하한 3·상한 5(절대 — 판형 상한 없음, §6.2 표에 ladder 부재).

**지오메트리(§6.3 "계단식 — x·y 동시 증가 오프셋"):** 단계 상자 폭 `box_w = 0.56 × (W − 2P)` 고정, 오프셋 `dx = (W − 2P − box_w)/(n−1)`, `dy = (H_avail − n×box_h)/(n−1)`. 하→상: stages[0] 좌하단, stages[n−1] 우상단. 연결은 대각 ArrowOp(상자 i 우상변 → 상자 i+1 좌하변).

- [ ] **Step 1: parse 실패 테스트**

```python
"""test_infographic_layout_ladder.py — 스펙 §6.2·§6.3 ladder 계단 지오메트리."""
import json
from pathlib import Path

import pytest

from scripts.infographic.archetypes import ladder as ladder_arch
from scripts.infographic.model import ArrowOp, RectOp, TextOp
from scripts.infographic.parse import ParseError, parse_fence

TOKENS = json.loads((Path(__file__).resolve().parents[1] / "styles" / "practical" / "tokens.json").read_text(encoding="utf-8"))
W = TOKENS["body_frame_pt"]["x1"] - TOKENS["body_frame_pt"]["x0"]
P = 14.0


def _fence(n):
    stages = [{"title": f"단계 {i+1}", "text": "근거 문장"} for i in range(n)]
    return parse_fence(1, 1, json.dumps(
        {"layout": "ladder", "title": "성숙도 사다리", "stages": stages}, ensure_ascii=False))


def test_parse_bounds():
    with pytest.raises(ParseError, match="stages 개수 2"):
        _fence(2)
    with pytest.raises(ParseError, match="stages 개수 6"):
        _fence(6)


def test_no_pack_cap_only_absolute():
    # ladder는 판형 상한 없음 — practical 5단계(절대 상한)가 레이아웃 에러 없이 통과
    # (C4a: essay 5단계는 폭 249pt에서 dy<16 에러 — 도달 불가 조합이므로 practical 사용)
    fig = ladder_arch.layout(_fence(5), TOKENS)    # 예외 없음 자체가 검증
    assert fig.height > 0
```

- [ ] **Step 2: 실행 — 실패 확인**

Run: `python3 -m pytest skills/korean-ebook-typst/tests/test_infographic_layout_ladder.py -q`
Expected: FAIL — unknown layout `ladder`

- [ ] **Step 3: parse.py 확장**

```python
STAGE_MIN, STAGE_MAX = 3, 5              # 스펙 §3.2 ladder — 절대 상한만(판형 표 부재)
VALID_LAYOUTS = {"flow", "cards", "matrix", "before_after", "ladder"}
```

분기(Task 1 before_after 블록 뒤):

```python
    if layout == "ladder":
        stages = d.get("stages", [])
        if not isinstance(stages, list) or not (STAGE_MIN <= len(stages) <= STAGE_MAX):
            n = len(stages) if isinstance(stages, list) else 0
            raise ParseError(index, f"stages 개수 {n} — 하한 {STAGE_MIN}, 상한 {STAGE_MAX}(스펙 §3.2)", line)
        for i, s in enumerate(stages):
            if not isinstance(s, dict):
                raise ParseError(index, f"stages[{i}] 객체 아님", line)
            if not str(s.get("title", "")).strip() or not str(s.get("text", "")).strip():
                raise ParseError(index, f"stages[{i}].title/.text 비어 있음", line)
        data["stages"] = [{"title": str(s["title"]).strip(), "text": str(s["text"]).strip()}
                          for s in stages]
```

- [ ] **Step 4: 지오메트리 실패 테스트 추가**

```python
def test_stair_offsets_both_axes():
    fig = ladder_arch.layout(_fence(4), TOKENS)
    boxes = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
    assert len(boxes) == 4
    box_w = boxes[0].w
    avail = W - 2 * P
    dx = (avail - box_w) / 3
    for i in range(4):
        assert abs(boxes[i].x - (P + i * dx)) < 0.01          # x 단조 증가
        assert abs(boxes[i].w - box_w) < 0.01
    for i in range(3):
        assert boxes[i + 1].y + boxes[i + 1].h < boxes[i].y   # y 단조 상승(하→상)
    arrows = [o for o in fig.ops if isinstance(o, ArrowOp)]
    assert len(arrows) == 3                                    # 계단 연결선
    a = arrows[0]
    assert a.x2 > a.x1 and a.y2 < a.y1                         # 우상향 대각


def test_box_height_measured():
    fig = ladder_arch.layout(_fence(3), TOKENS)
    boxes = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
    assert boxes[0].h == boxes[1].h == boxes[2].h              # 최대 단계 높이 통일


def test_step_gap_error_on_tall_stages():
    # C4b: ladder의 공간 부족 에러는 dy<STEP_GAP_MIN 경로 — 85% 분기는
    # H_avail 산식상 도달 불가(구조적 불변식 검사로만 존재)
    long_text = "근거 문장이 상자 폭을 넘어 여러 줄로 감싸지는 매우 긴 문장입니다 " * 6
    stages = [{"title": f"단계 {i+1}", "text": long_text} for i in range(5)]
    f = parse_fence(1, 1, json.dumps(
        {"layout": "ladder", "title": "성숙도", "stages": stages}, ensure_ascii=False))
    with pytest.raises(ladder_arch.LadderLayoutError, match="단 간격"):
        ladder_arch.layout(f, TOKENS)
```

- [ ] **Step 5: 실행 — 실패 확인**

Expected: FAIL — `ladder` 모듈 부재

- [ ] **Step 6: ladder.py 구현**

```python
"""ladder — 계단식 성숙도(스펙 §6.3). x·y 동시 증가 오프셋, 하→상. 판형 상한 없음(절대 3~5만)."""
from __future__ import annotations

from .. import budget
from ..model import ArrowOp, FigModel, RectOp, TextOp
from ..parse import DEFAULT_NOTE, Fence
from .base import LayoutError

P = 14.0
BOX_W_FRAC = 0.56
STAGE_PAD_IN = 8.0
STAGE_PAD_V = 10.0
STEP_GAP_MIN = 16.0            # 계단 단 사이 최소 시각 간격
LEADING = 1.3
HEIGHT_LIMIT = 0.85


class LadderLayoutError(LayoutError):
    pass


def layout(fence: Fence, tokens: dict) -> FigModel:
    frame = tokens["body_frame_pt"]
    W = frame["x1"] - frame["x0"]
    H_frame = frame["y1"] - frame["y0"]
    pack = tokens.get("style", "practical")
    f = tokens["fonts"]
    body = f["body"]["size_pt"]
    kicker_size = f["label"]["size_pt"]
    title_size = f["heading2"]["size_pt"]
    if abs(title_size - body) <= 0.3:
        title_size = body + 1.5
    st_title_size = body + 1
    st_text_size = body - 1

    stages = fence.data["stages"]
    n = len(stages)
    avail_w = W - 2 * P
    box_w = BOX_W_FRAC * avail_w
    box_pad_h = 8.0

    # 상자 높이 — 최대 단계 기준 통일, 전부 실측
    def stage_h(s: dict) -> float:
        h = 2 * STAGE_PAD_V
        h += budget.line_count(s["title"], box_w, st_title_size, box_pad_h, pack) * st_title_size * LEADING + 4.0
        h += budget.line_count(s["text"], box_w, st_text_size, box_pad_h, pack) * st_text_size * LEADING
        return h

    box_h = max(stage_h(s) for s in stages)

    # 헤더(cards·before_after와 동일 구조)
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
        th = budget.line_count(fence.thesis, W - 2 * P, st_text_size, 0.0, pack)
        texts.append(TextOp(x=W / 2, y=cy + th * st_text_size * LEADING / 2, size=st_text_size,
                            text=fence.thesis, role="ink-soft", max_w=W - 2 * P, field="thesis"))
        cy += th * st_text_size * LEADING
    y = cy + 18.0

    note = fence.note or DEFAULT_NOTE
    note_h = st_text_size * LEADING
    H_avail = H_frame * HEIGHT_LIMIT - y - note_h - 12.0 - P
    dy = (H_avail - n * box_h) / (n - 1)
    if dy < STEP_GAP_MIN:
        raise LadderLayoutError(
            f"계단 단 간격 {dy:.1f}pt < {STEP_GAP_MIN:.0f}pt — 단계 축약(문구·수) 또는 펜스 분할")

    dx = (avail_w - box_w) / (n - 1)
    rects: list[RectOp] = []
    arrows: list[ArrowOp] = []
    stage_top = [y + (n - 1 - i) * (box_h + dy) for i in range(n)]   # stages[0]=최하단
    for i, s in enumerate(stages):
        sx, sy = P + i * dx, stage_top[i]
        rects.append(RectOp(x=sx, y=sy, w=box_w, h=box_h))
        ty = sy + STAGE_PAD_V
        tl = budget.line_count(s["title"], box_w, st_title_size, box_pad_h, pack)
        texts.append(TextOp(x=sx + box_w / 2, y=ty + tl * st_title_size * LEADING / 2,
                            size=st_title_size, text=s["title"], role="ink", weight="bold",
                            max_w=box_w, field=f"stages[{i}].title"))
        ty += tl * st_title_size * LEADING + 4.0
        xl = budget.line_count(s["text"], box_w, st_text_size, box_pad_h, pack)
        texts.append(TextOp(x=sx + box_w / 2, y=ty + xl * st_text_size * LEADING / 2,
                            size=st_text_size, text=s["text"], role="ink-soft",
                            max_w=box_w, field=f"stages[{i}].text"))
        if i:
            # C3: dx < box_w 항상(상자 수평 겹침) — 모서리→모서리는 좌상향이 되므로
            # 겹침역 중심 ±4pt 관통로로 우상향 보장(x 증가 8pt·y 상승 dy)
            ov_mid = (sx + rects[i - 1].x + box_w) / 2
            arrows.append(ArrowOp(x1=ov_mid - 4.0, y1=rects[i - 1].y,
                                  x2=ov_mid + 4.0, y2=sy + box_h))

    # C2: 잉크 최심부 = 최하단 상자(stage_top[0]) 하변 — note는 그 아래
    y = stage_top[0] + box_h + 12.0
    texts.append(TextOp(x=W / 2, y=y + note_h / 2, size=st_text_size,
                        text=note, role="ink-mute", max_w=W - 2 * P, field="note"))
    y += note_h

    ops = [RectOp(x=0.0, y=0.0, w=W, h=y, rx=0.0, fill_role="paper", stroke_role="rule", stroke_w=0.0),
           *rects, *arrows, *texts]
    _ink_ok(ops, W, y)
    return FigModel(width=W, height=y, ops=tuple(ops), source_index=fence.index)


def _ink_ok(ops, width: float, height: float) -> None:
    # before_after와 동일 논리 — RectOp/ArrowOp/TextOp bbox 프레임 검사
    ...
```

주의: `_ink_ok`는 Task 1에서 작성한 것과 동일 논리를 ladder용으로 복제(모듈 로컬 함수 관례 — cards·flow도 각자 보유).

**높이 불변식(C2)**: 총높이 = `y + H_avail + 12 + note_h = 0.85·H_frame − P` 로 수렴 — 85% 초과 분기는 존재하지 않는다(도달 불가 dead code 제거, C4b). ladder의 공간 부족 에러 경로는 dy<STEP_GAP_MIN 단 하나: 헤더가 길거나 단계 문구가 길면 box_h·H_avail이 압박해 dy가 16pt 미만으로 떨어진다(가로/세로 랩 개념 없음).

layout.py dispatch 등록(`_lad` 임포트 포함), lint 필드(`steps`와 동일 — `stages[i].title`·`stages[i].text`), render `_sheet_rows` 동일 추가:

```python
    for i, s in enumerate(f.data.get("stages", [])):
        rows.append((f"stages[{i}].title", s["title"]))
        rows.append((f"stages[{i}].text", s["text"]))
```

- [ ] **Step 7: 실행 — 전체 통과 확인**

Run: `python3 -m pytest skills/korean-ebook-typst/tests/ -q`
Expected: 전부 PASS

- [ ] **Step 8: Commit**

```bash
git add skills/korean-ebook-typst/scripts/infographic/ skills/korean-ebook-typst/tests/test_infographic_layout_ladder.py
git commit -m "feat: ladder archetype — 계단식 x·y 오프셋·단 간격 하한 + stages 소비자 확장"
```

---

### Task 3: roadmap archetype + 골든 3종 + 골든 교정 2주기

**Files:**
- Create: `skills/korean-ebook-typst/scripts/infographic/archetypes/roadmap.py`
- Modify: `parse.py`·`layout.py`·`lint.py`·`render.py` (Task 1·2와 동일 지점)
- Create: `skills/korean-ebook-typst/tests/test_infographic_layout_roadmap.py`
- Create: `skills/korean-ebook-typst/tests/fixtures/infographic/calib-before-after.md`·`calib-ladder.md`·`calib-roadmap.md`
- Create(재생성 절차): `golden-before-after-practical.typ`·`golden-ladder-practical.typ`·`golden-roadmap-practical.typ`

**Interfaces:**
- Consumes: Task 1·2와 동일
- Produces: `archetypes.roadmap.layout(fence, tokens) -> FigModel`, `RoadmapLayoutError`, 데이터 `phases[]`({period, title, items[]} — items 문자열 배열)

**데이터:** `phases[]` {period, title, items[]}. 위상 하한 2·절대 상한 5(§3.2), 판형 상한 essay 3 / practical 4 / b5 4 / business 5 / lecture 5(§6.2). items 하한 1·상한 4(플랜 결정 — 높이 예산 보호, 스펙 무규정).

**지오메트리(§6.3 "가로 타임라인 + 위상 밴드"):** 상단 가로 타임라인(ArrowOp, P→W−P) + 밴드 n개 가로 배치, `band_w = (W−2P−(n−1)G)/n`. 밴드 내부: period(kicker 스타일)→title(본문+1)→items(본문−1, 실측). 밴드 높이는 최대 위상 기준 통일.

- [ ] **Step 1: parse 실패 테스트**

```python
"""test_infographic_layout_roadmap.py — 스펙 §6.2·§6.3 roadmap 타임라인·위상 밴드."""
import json
from pathlib import Path

import pytest

from scripts.infographic.archetypes import roadmap as rm_arch
from scripts.infographic.model import ArrowOp, RectOp, TextOp
from scripts.infographic.parse import ParseError, parse_fence

TOKENS = json.loads((Path(__file__).resolve().parents[1] / "styles" / "practical" / "tokens.json").read_text(encoding="utf-8"))
W = TOKENS["body_frame_pt"]["x1"] - TOKENS["body_frame_pt"]["x0"]
P, G = 14.0, 28.0


def _fence(n, items=2):
    phases = [{"period": f"20{25+i}년", "title": f"위상 {i+1}",
               "items": [f"항목 {j}" for j in range(items)]} for i in range(n)]
    return parse_fence(1, 1, json.dumps(
        {"layout": "roadmap", "title": "도입 로드맵", "phases": phases}, ensure_ascii=False))


def test_parse_bounds():
    with pytest.raises(ParseError, match="phases 개수 1"):
        _fence(1)
    with pytest.raises(ParseError, match="items 개수 5"):
        _fence(2, items=5)


def test_timeline_arrow_and_bands():
    fig = rm_arch.layout(_fence(3), TOKENS)
    bands = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
    assert len(bands) == 3
    band_w = (W - 2 * P - 2 * G) / 3
    assert abs(bands[0].w - band_w) < 0.01
    assert abs(bands[2].x - (P + 2 * (band_w + G))) < 0.01
    arrows = [o for o in fig.ops if isinstance(o, ArrowOp)]
    assert len(arrows) == 1 and arrows[0].x1 < arrows[0].x2
    assert arrows[0].y1 < bands[0].y                    # 타임라인은 밴드 위
    fields = {t.field for t in fig.ops if isinstance(t, TextOp)}
    assert {"phases[0].period", "phases[1].title", "phases[2].items[1]"} <= fields


def test_band_height_measured_max():
    fig = rm_arch.layout(_fence(2, items=3), TOKENS)
    bands = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
    assert bands[0].h == bands[1].h


def test_pack_cap_essay():
    essay = json.loads((Path(__file__).resolve().parents[1] / "styles" / "essay" / "tokens.json").read_text(encoding="utf-8"))
    with pytest.raises(rm_arch.RoadmapLayoutError, match=r"판형 상한 3위상\(essay\)"):
        rm_arch.layout(_fence(4), essay)


def test_pack_cap_success_all_packs():
    # I3 — 각 팩 스펙 상한 n에서 렌더 성공(C5 방어: 밴드폭 ≥ MIN_BAND_W 실증)
    packs = {"essay": 3, "practical": 4, "b5": 4, "business": 5, "lecture": 5}
    for name, cap in packs.items():
        toks = json.loads((Path(__file__).resolve().parents[1] / "styles" / name / "tokens.json").read_text(encoding="utf-8"))
        fig = rm_arch.layout(_fence(cap), toks)
        bands = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
        assert len(bands) == cap, name
        assert bands[0].w >= rm_arch.MIN_BAND_W - 0.01, name
```

- [ ] **Step 2: 실행 — 실패 확인**

Expected: FAIL — unknown layout `roadmap`

- [ ] **Step 3: parse.py 확장**

```python
PHASE_MIN, PHASE_MAX = 2, 5              # 스펙 §3.2 roadmap 위상
PHASE_ITEMS_MIN, PHASE_ITEMS_MAX = 1, 4  # 플랜 결정 — 높이 예산 보호
VALID_LAYOUTS = {"flow", "cards", "matrix", "before_after", "ladder", "roadmap"}
```

분기(Task 2 ladder 뒤):

```python
    if layout == "roadmap":
        phases = d.get("phases", [])
        if not isinstance(phases, list) or not (PHASE_MIN <= len(phases) <= PHASE_MAX):
            n = len(phases) if isinstance(phases, list) else 0
            raise ParseError(index, f"phases 개수 {n} — 하한 {PHASE_MIN}, 상한 {PHASE_MAX}(스펙 §3.2)", line)
        for i, p in enumerate(phases):
            if not isinstance(p, dict):
                raise ParseError(index, f"phases[{i}] 객체 아님", line)
            if not str(p.get("period", "")).strip() or not str(p.get("title", "")).strip():
                raise ParseError(index, f"phases[{i}].period/.title 비어 있음", line)
            items = p.get("items", [])
            if not isinstance(items, list) or not (PHASE_ITEMS_MIN <= len(items) <= PHASE_ITEMS_MAX):
                m = len(items) if isinstance(items, list) else 0
                raise ParseError(index, f"phases[{i}].items 개수 {m} — 하한 {PHASE_ITEMS_MIN}, 상한 {PHASE_ITEMS_MAX}", line)
            for j, it in enumerate(items):
                if not str(it).strip():
                    raise ParseError(index, f"phases[{i}].items[{j}] 비어 있음", line)
        data["phases"] = [{"period": str(p["period"]).strip(), "title": str(p["title"]).strip(),
                           "items": [str(it).strip() for it in p["items"]]} for p in phases]
```

- [ ] **Step 4: roadmap.py 구현**

```python
"""roadmap — 가로 타임라인 + 위상 밴드(스펙 §6.2·§6.3). 판형 상한 위상 수로 즉시 에러."""
from __future__ import annotations

from .. import budget
from ..model import ArrowOp, FigModel, RectOp, TextOp
from ..parse import DEFAULT_NOTE, Fence
from .base import LayoutError

P = 14.0
G = 28.0
BAND_PAD_IN = 8.0
BAND_PAD_V = 10.0
ITEM_GAP = 5.0
TL_H = 24.0                    # 타임라인 축 높이(축+여백)
MIN_BAND_W = 54.0              # C5 — essay 3밴드 55.2pt·practical 4밴드 55.6pt 실측, 전팩 상한 도달
LEADING = 1.3
HEIGHT_LIMIT = 0.85

PACK_PHASES = {"essay": 3, "practical": 4, "b5": 4, "business": 5, "lecture": 5}


class RoadmapLayoutError(LayoutError):
    pass


def layout(fence: Fence, tokens: dict) -> FigModel:
    frame = tokens["body_frame_pt"]
    W = frame["x1"] - frame["x0"]
    H_frame = frame["y1"] - frame["y0"]
    pack = tokens.get("style", "practical")
    f = tokens["fonts"]
    body = f["body"]["size_pt"]
    kicker_size = f["label"]["size_pt"]
    title_size = f["heading2"]["size_pt"]
    if abs(title_size - body) <= 0.3:
        title_size = body + 1.5
    ph_title_size = body + 1
    item_size = body - 1

    phases = fence.data["phases"]
    n = len(phases)
    cap = PACK_PHASES.get(pack)
    if cap is None:
        raise RoadmapLayoutError(f"알 수 없는 스타일 팩 {pack!r}")
    if n > cap:
        raise RoadmapLayoutError(
            f"위상 {n}개 > 판형 상한 {cap}위상({pack}) — 위상 통합 또는 펜스 분할")

    band_w = (W - 2 * P - (n - 1) * G) / n
    if band_w < MIN_BAND_W:
        raise RoadmapLayoutError(
            f"밴드 폭 {band_w:.1f}pt < {MIN_BAND_W:.0f}pt({pack}) — 위상 통합 또는 펜스 분할")

    # 밴드 높이 — 최대 위상 기준, 전부 실측
    def phase_h(p: dict) -> float:
        h = 2 * BAND_PAD_V
        h += kicker_size * LEADING + 6.0                      # period
        h += budget.line_count(p["title"], band_w, ph_title_size, BAND_PAD_IN, pack) * ph_title_size * LEADING + 4.0
        for it in p["items"]:
            h += budget.line_count(it, band_w, item_size, BAND_PAD_IN, pack) * item_size * LEADING + ITEM_GAP
        return h

    band_h = max(phase_h(p) for p in phases)

    # 헤더(공통 구조) — kicker/title/thesis 후 y 시작
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
        th = budget.line_count(fence.thesis, W - 2 * P, item_size, 0.0, pack)
        texts.append(TextOp(x=W / 2, y=cy + th * item_size * LEADING / 2, size=item_size,
                            text=fence.thesis, role="ink-soft", max_w=W - 2 * P, field="thesis"))
        cy += th * item_size * LEADING
    y = cy + 18.0

    # 가로 타임라인 — 밴드 위 축
    arrows = [ArrowOp(x1=P, y1=y + TL_H / 2, x2=W - P, y2=y + TL_H / 2)]
    y += TL_H

    rects: list[RectOp] = []
    for i, p in enumerate(phases):
        bx = P + i * (band_w + G)
        rects.append(RectOp(x=bx, y=y, w=band_w, h=band_h))
        ty = y + BAND_PAD_V
        texts.append(TextOp(x=bx + band_w / 2, y=ty + kicker_size * LEADING / 2, size=kicker_size,
                            text=p["period"], role="ink-mute", weight="bold",
                            max_w=band_w, field=f"phases[{i}].period"))
        ty += kicker_size * LEADING + 6.0
        tl = budget.line_count(p["title"], band_w, ph_title_size, BAND_PAD_IN, pack)
        texts.append(TextOp(x=bx + band_w / 2, y=ty + tl * ph_title_size * LEADING / 2,
                            size=ph_title_size, text=p["title"], role="ink", weight="bold",
                            max_w=band_w, field=f"phases[{i}].title"))
        ty += tl * ph_title_size * LEADING + 4.0
        for j, it in enumerate(p["items"]):
            il = budget.line_count(it, band_w, item_size, BAND_PAD_IN, pack)
            texts.append(TextOp(x=bx + band_w / 2, y=ty + il * item_size * LEADING / 2,
                                size=item_size, text=it, role="ink-soft",
                                max_w=band_w, field=f"phases[{i}].items[{j}]"))
            ty += il * item_size * LEADING + ITEM_GAP

    y = y + band_h + 12.0
    note = fence.note or DEFAULT_NOTE
    texts.append(TextOp(x=W / 2, y=y + item_size * LEADING / 2, size=item_size,
                        text=note, role="ink-mute", max_w=W - 2 * P, field="note"))
    y += item_size * LEADING

    if y > H_frame * HEIGHT_LIMIT:
        raise RoadmapLayoutError(
            f"도식 높이 {y:.0f}pt > 프레임 {H_frame * HEIGHT_LIMIT:.0f}pt(85%) — 항목 축약 또는 펜스 분할")

    ops = [RectOp(x=0.0, y=0.0, w=W, h=y, rx=0.0, fill_role="paper", stroke_role="rule", stroke_w=0.0),
           *rects, *arrows, *texts]
    _ink_ok(ops, W, y)
    return FigModel(width=W, height=y, ops=tuple(ops), source_index=fence.index)


def _ink_ok(ops, width: float, height: float) -> None:
    # Task 1·2와 동일 논리
    ...
```

dispatch 등록, lint 필드(`phases[i].period`·`.title`·`.items[j]`), render `_sheet_rows` 동일 추가.

- [ ] **Step 5: 전체 테스트 통과 확인**

Run: `python3 -m pytest skills/korean-ebook-typst/tests/ -q`
Expected: 전부 PASS

- [ ] **Step 6: 골든 스냅샷 3종 — 실패 테스트 → 재생성 → 통과**

골든 테스트는 cards 패턴(`test_infographic_layout_cards.py:124` `test_cards_golden_snapshot`)을 그대로 복제 — archetype·골든 경로만 교체. 3개 테스트:

```python
def test_before_after_golden_snapshot():
    # cards 골든 패턴(test_infographic_layout_cards.py:124-135) 복제 — I2:
    # emit 심볼은 render_typ(fig)뿐(emit.py:21), os는 파일 상단 임포트
    import os
    GOLDEN = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "infographic" / "golden-before-after-practical.typ"
    fig = ba_arch.layout(_fence(["리드타임 2주", "수작업 5단계"], ["리드타임 3일", "자동화 1단계"], center="AI 도입"), TOKENS)
    from scripts.infographic.emit import render_typ
    code = render_typ(fig)
    if os.environ.get("IG_REGEN_GOLDEN") != "1":
        if not GOLDEN.exists():
            pytest.fail("골든 없음 — `IG_REGEN_GOLDEN=1 python3 -m pytest …` 실행 후 눈검·커밋")
        assert code == GOLDEN.read_text(encoding="utf-8")
    else:
        GOLDEN.write_text(code, encoding="utf-8")
        pytest.fail("골든 재생성 — 눈검 후 커밋")
```

ladder·roadmap 동일 구조(`_lad`·`_rm` arch 모듈과 각 `_fence` 사용, 골든 경로만 교체).

Run: `IG_REGEN_GOLDEN=1 python3 -m pytest skills/korean-ebook-typst/tests/test_infographic_layout_before_after.py skills/korean-ebook-typst/tests/test_infographic_layout_ladder.py skills/korean-ebook-typst/tests/test_infographic_layout_roadmap.py -q` → 3골든 생성 → typst 컴파일 눈검(`cli.py preview` 또는 수동) → 재실행으로 PASS.

- [ ] **Step 7: 골든 교정 2주기 — calib fixture 3종 실렌더**

Phase 2 Task 4 절차 반복(작성자는 `.superpowers/sdd/…/task-4-report.md`와 authoring.md "골든 교정 절차" 섹션을 먼저 읽는다):

1. `calib-before-after.md`·`calib-ladder.md`·`calib-roadmap.md` — 항목/단계/위상 수를 상한까지 늘린 극단 fixture. **판형 5팩 전수**(m5 — Phase 2와 동일, 대표/최악 추리기 없음)
2. CLI preview로 실렌더 → 오버플로·공간 부족 에러(단 간격·높이) 발생 지점 실측. 판정 계약: 비율/데드밴드 ±0.05(Phase 2 기준)
3. `budget.py` 계수 드리프트 확인 — 갱신 대상은 `PACK_KO_FACTOR`(팩별 계수; KO_UNIT·LATIN_UNIT·MARGIN은 Phase 1 고정값). Phase 2 실측치 대비 변화 없으면 갱신 생략(기록 계약: 커밋 body에 실측 수치)
4. 계수 갱신 시 **골든 3종 바이트 재확증**(m7 — `IG_REGEN_GOLDEN` 없이 재실행, 바이트 동일 확인. 드리프트 시 재생성·눈검·커밋)
5. 예산표(authoring.md 치트시트) 수치 갱신은 Task 4에서 반영

- [ ] **Step 8: Commit**

```bash
git add skills/korean-ebook-typst/scripts/infographic/ skills/korean-ebook-typst/tests/
git commit -m "feat: roadmap archetype + 골든 3종·교정 2주기 — 타임라인·위상 밴드·판형 상한"
```

---

### Task 4: authoring.md 갱신 + 종료 조건

**Files:**
- Modify: `skills/korean-ebook-typst/references/infographic/authoring.md`
- Modify: `skills/korean-ebook-typst/SKILL.md` (archetype 목록 1줄 있는 경우만)

**Interfaces:**
- Consumes: Task 1~3 전부(스키마·상한·치트시트 수치는 구현된 상수와 일치해야 함)
- Produces: 저작 가이드 Phase 3판 — before_after·ladder·roadmap 섹션 + 치트시트 3행 + 라우팅 갱신

- [ ] **Step 1: authoring.md 섹션 3개 추가**

`### flow`·`### cards`·`### matrix` 섹션 뒤에 각각 추가 — 구조는 cards 섹션 복제(스키마 표·예시 펜스·저작 규칙·I1 주의):

- `### before_after — 전환 대비`: 데이터 키(before[]·after[]·center·before_label/after_label), 항목 수 상한(하한 1·절대 5·판형 표), "항목은 짧은 문구 — 근거 문장은 thesis에" 규칙, "center 라벨은 초단문(중앙존 68pt)" 규칙
- `### ladder — 성숙도 계단`: stages 3~5(판형 상한 없음), "단계 문구 길면 85% 에러" 규칙
- `### roadmap — 시간 전개`: phases 2~5(판형 표)·items 1~4, "위상 수는 판형 상한 우선" 규칙, **"항목은 초단문(밴드 폭 최소 55pt — essay 3위상·practical 4위상에서 4~5자/줄 수준)" 계약**(C5 — MIN_BAND_W 54의 저작측 근거)

각 섹션 예시 펜스는 Task 1~3 테스트의 `_fence` 데이터를 그대로 사용(코드·문서 정합).

- [ ] **Step 2: 치트시트 표 3행 추가**

"예산 치트시트" 표에 before_after 항목/측·ladder 단계·roadmap 위상+항목 행 추가 — 수치는 Task 3 교정 2주기 실측치와 `PACK_ITEMS`·`PACK_PHASES` 상수 대조(불일치 시 문서가 아니라 원인 규명).

- [ ] **Step 3: 라우팅·헤더 갱신**

제목 "(Phase 2 — flow·cards·matrix)" → "(Phase 3 — +before_after·ladder·roadmap)". 라우팅 표·`bridge` 별칭 언급 존재 시 갱신. SKILL.md에 archetype 나열 있으면 3종 추가.

- [ ] **Step 4: 종료 조건 확인(스펙 §8)**

- [ ] 단위 테스트: 3종 지오메트리·결정론·에러 경로 전부 PASS
- [ ] 골든 스냅샷: 3종 존재 + 스냅샷 테스트 PASS
- [ ] 통합: `test_infographic_build_integration.py`에 3종 펜스 fixture 포함(빌드→PDF→infographic_pages 일치) — 기존 통합 테스트 패턴 확인 후 3종 추가
- [ ] authoring.md 해당 섹션 존재
- [ ] 검수 시트 생성 확인(m6 — cli lint는 검수 시트를 만들지 않는다. 빌드 통합 테스트의 `render_book_fences`·`_review_sheet` 경로 또는 실 빌드 1회로 신규 3종 행이 시트에 나오는지 확인)
- [ ] 전체: `python3 -m pytest skills/korean-ebook-typst/tests/ -q` green

- [ ] **Step 5: Commit**

```bash
git add skills/korean-ebook-typst/references/infographic/authoring.md skills/korean-ebook-typst/SKILL.md
git commit -m "docs: 인포그래픽 가이드 Phase 3판 — before_after·ladder·roadmap 저작 규칙·치트시트"
```

---

## Self-Review 결과 (개정 2판 — 적대검토 후)

1. **스펙 커버리지**: §3.2 데이터 3종(Task 1·2·3) ✓ · §6.2 상한 표 before_after·roadmap 행(Task 1·3, **상한 도달 성공 테스트 포함 — I3**), ladder 판형 부재 명시(Task 2) ✓ · §6.3 지오메트리 3종(C3 겹침역 관통로 반영) ✓ · §7 골든·교정 2주기 5팩 전수(Task 3) ✓ · §8 종료 조건(Task 4) ✓ · §3.4 별칭 bridge(Task 1) ✓
2. **플레이스홀더 스캔**: `_ink_ok(...)`의 `...` 2곳(Task 2·3) — "Task 1과 동일 논리" 지시. 브리프가 완전 코드를 요구하면 Task 1의 `_ink_ok`를 문자열 그대로 전달(구현자는 클래스명만 교체).
3. **타입 일치**: `layout(fence, tokens) -> FigModel` 3종 동일 ✓ · 파라미터 `PACK_ITEMS`/`PACK_PHASES`(ladder 무) ✓ · field 경로 `before[i]`/`stages[i].title`/`phases[i].items[j]` 전 모듈 일치 ✓
4. **적대검토 반영(개정 2판)**: C1 패널 상수(전팩 panel_w ≥ 65 실측) · C2 ladder 높이·note(총높이 = 0.85H−P 불변식) · C3 화살표 우상향 산식(x +8pt·y −dy) · C4 도달 가능 테스트만(practical 5단계·"단 간격" match) · C5 MIN_BAND_W 54(전팩 상한 밴드폭 ≥ 54 실측, 스펙 개정 불필요) · I1 after\[1\] match · I2 render_typ·os·골든 부재 fail 분기 · I3 상한 성공 테스트 2종 · m1~m7(181 기준·pad 8·tip-gap 8·lint 패턴 지시·5팩 전수·검수 시트 빌드 경로·골든 바이트 재확증)
