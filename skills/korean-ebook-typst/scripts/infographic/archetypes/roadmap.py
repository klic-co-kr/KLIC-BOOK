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
    for o in ops:
        if isinstance(o, RectOp):
            if (o.x < -0.001 or o.x + o.w > width + 0.001
                    or o.y < -0.001 or o.y + o.h > height + 0.001):
                raise RoadmapLayoutError(
                    f"잉크 bbox 프레임 이탈: rect({o.x:.1f},{o.y:.1f},{o.w:.1f},{o.h:.1f})")
        elif isinstance(o, ArrowOp):
            if (min(o.x1, o.x2) < -0.001 or max(o.x1, o.x2) > width + 0.001
                    or min(o.y1, o.y2) < -0.001 or max(o.y1, o.y2) > height + 0.001):
                raise RoadmapLayoutError(
                    f"잉크 bbox 프레임 이탈: arrow({o.x1:.1f},{o.y1:.1f}→{o.x2:.1f},{o.y2:.1f})")
        elif isinstance(o, TextOp):
            hw = (o.max_w or 60.0) / 2
            if o.x - hw < -0.001 or o.x + hw > width + 0.001:
                raise RoadmapLayoutError(
                    f"잉크 bbox 프레임 이탈: text({o.field}) x={o.x:.1f} max_w={o.max_w:.1f}")
