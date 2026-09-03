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
