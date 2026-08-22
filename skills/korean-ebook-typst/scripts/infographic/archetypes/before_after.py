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
