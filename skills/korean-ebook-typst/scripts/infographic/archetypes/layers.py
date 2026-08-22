"""layers — 수평 스택 기본·rings 동심원 변형(스펙 §6.3). 계층 수 절대 상한은 parse가 검사."""
from __future__ import annotations

import math

from .. import budget
from ..model import CircleOp, FigModel, RectOp, TextOp
from ..parse import DEFAULT_NOTE, Fence
from .base import LayoutError, sizes

P = 14.0
ROW_PAD_IN = 8.0
ROW_PAD_V = 10.0
ROW_GAP = 10.0
RING_MIN_FRAC = 0.25          # 최내곽 반경 = R_max의 25%
RING_LABEL_IN = 6.0           # 링 상단부터 라벨 중심까지
LEADING = 1.3
HEIGHT_LIMIT = 0.85


class LayersLayoutError(LayoutError):
    pass


def layout(fence: Fence, tokens: dict) -> FigModel:
    frame = tokens["body_frame_pt"]
    W = frame["x1"] - frame["x0"]
    H_frame = frame["y1"] - frame["y0"]
    pack = tokens.get("style", "practical")
    s = sizes(tokens)
    kicker_size, title_size, item_size = s["kicker"], s["title"], s["item"]

    stack = fence.data.get("stack")
    rings = fence.data.get("rings")

    # 헤더(공통 구조) — kicker는 저작 계약 초단문(1줄)
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
    y0 = cy + 18.0

    rects: list[RectOp] = []
    circles: list[CircleOp] = []
    if stack is not None:
        # 수평 스택 — 주어진 순서 = 위→아래. 전폭 행, 높이 실측.
        y = y0
        for i, row in enumerate(stack):
            row_w = W - 2 * P
            rl = budget.line_count(row["label"], row_w, item_size, ROW_PAD_IN, pack)
            row_h = 2 * ROW_PAD_V + rl * item_size * LEADING
            rects.append(RectOp(x=P, y=y, w=row_w, h=row_h))
            texts.append(TextOp(x=W / 2, y=y + ROW_PAD_V + rl * item_size * LEADING / 2,
                                size=item_size, text=row["label"], role="ink",
                                max_w=row_w, field=f"stack[{i}].label"))
            y += row_h + ROW_GAP
        y -= ROW_GAP
    else:
        # 동심원 — rings[0] = 최외곽. 등간격 반경, 라벨은 12시 방향 현(chord) 폭 안 실측.
        n = len(rings)
        r_max = (W - 2 * P) / 2
        r_min = RING_MIN_FRAC * r_max
        step = (r_max - r_min) / (n - 1) if n > 1 else 0.0
        cc_y = y0 + r_max
        for i, ring in enumerate(rings):
            r = r_max - i * step
            circles.append(CircleOp(x=W / 2, y=cc_y, r=r))
        for i, ring in enumerate(rings):
            r = r_max - i * step
            d = RING_LABEL_IN + item_size * LEADING / 2
            chord = 2 * math.sqrt(max(r * r - d * d, 0.0)) - 2 * ROW_PAD_IN
            rl = budget.line_count(ring["label"], chord, item_size, ROW_PAD_IN, pack)
            texts.append(TextOp(x=W / 2, y=cc_y - r + d, size=item_size,
                                text=ring["label"], role="ink", max_w=chord,
                                field=f"rings[{i}].label"))
        y = y0 + 2 * r_max

    y += 12.0
    note = fence.note or DEFAULT_NOTE
    nl = budget.line_count(note, W - 2 * P, item_size, 8.0, pack)
    texts.append(TextOp(x=W / 2, y=y + nl * item_size * LEADING / 2, size=item_size,
                        text=note, role="ink-mute", max_w=W - 2 * P, field="note"))
    y += nl * item_size * LEADING

    if y > H_frame * HEIGHT_LIMIT:
        raise LayersLayoutError(
            f"도식 높이 {y:.0f}pt > 프레임 {H_frame * HEIGHT_LIMIT:.0f}pt(85%) — 계층 축약 또는 펜스 분할")

    ops = [RectOp(x=0.0, y=0.0, w=W, h=y, rx=0.0, fill_role="paper", stroke_role="rule", stroke_w=0.0),
           *circles, *rects, *texts]
    _ink_ok(ops, W, y)
    return FigModel(width=W, height=y, ops=tuple(ops), source_index=fence.index)


def _ink_ok(ops, width: float, height: float) -> None:
    # _ink_ok 표준형(Task 1과 동일 — Rect stroke_w/2 포함) + Circle 분기(반경+반 스트로크).
    for o in ops:
        if isinstance(o, CircleOp):
            s = o.stroke_w / 2
            if (o.x - o.r - s < -0.001 or o.x + o.r + s > width + 0.001
                    or o.y - o.r - s < -0.001 or o.y + o.r + s > height + 0.001):
                raise LayersLayoutError(
                    f"잉크 bbox 프레임 이탈: circle({o.x:.1f},{o.y:.1f},r={o.r:.1f})")
        elif isinstance(o, RectOp):
            s = o.stroke_w / 2
            if (o.x - s < -0.001 or o.x + o.w + s > width + 0.001
                    or o.y - s < -0.001 or o.y + o.h + s > height + 0.001):
                raise LayersLayoutError(
                    f"잉크 bbox 프레임 이탈: rect({o.x:.1f},{o.y:.1f},{o.w:.1f},{o.h:.1f})")
        elif isinstance(o, TextOp):
            hw = (o.max_w or 60.0) / 2
            if o.x - hw < -0.001 or o.x + hw > width + 0.001:
                raise LayersLayoutError(
                    f"잉크 bbox 프레임 이탈: text({o.field}) x={o.x:.1f} max_w={o.max_w:.1f}")
