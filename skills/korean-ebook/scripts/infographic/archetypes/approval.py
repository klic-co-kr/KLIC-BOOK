"""approval — 가로 결재 경로 + 게이트 다이아몬드(스펙 §6.3). 폭 하상수로 즉시 에러."""
from __future__ import annotations

from .. import budget
from ..model import ArrowOp, FigModel, RectOp, TextOp
from ..parse import DEFAULT_NOTE, Fence
from .base import LayoutError, sizes

P = 14.0
G = 28.0                     # 커넥터 복도 — tip-gap 8 양측 후 샤프트 12pt(§6.1)
STEP_PAD_IN = 8.0
STEP_PAD_V = 10.0
STEP_GAP_V = 6.0             # 제목·본문 사이
MIN_STEP_W = 48.0            # 도달 한계 실측 — essay 3·55.15 / practical 4·55.62 / b5 5·49.10 / business 5(n=6=47.59<48) / lecture 6·49.48pt
MARK_SIDE = 12.0             # 게이트 다이아몬드 한 변 — 회전 bbox 16.97pt
LEADING = 1.3
HEIGHT_LIMIT = 0.85


class ApprovalLayoutError(LayoutError):
    pass


def layout(fence: Fence, tokens: dict) -> FigModel:
    frame = tokens["body_frame_pt"]
    W = frame["x1"] - frame["x0"]
    H_frame = frame["y1"] - frame["y0"]
    pack = tokens.get("style", "practical")
    s = sizes(tokens)
    kicker_size, title_size = s["kicker"], s["title"]
    ph_title_size, item_size = s["ph_title"], s["item"]

    steps = fence.data["path"]
    n = len(steps)

    step_w = (W - 2 * P - (n - 1) * G) / n
    if step_w < MIN_STEP_W:
        raise ApprovalLayoutError(
            f"스텝 폭 {step_w:.1f}pt < {MIN_STEP_W:.0f}pt({pack}) — 경로 축약 또는 펜스 분할")

    def step_h(st: dict) -> float:
        h = 2 * STEP_PAD_V
        h += budget.line_count(st["title"], step_w, ph_title_size, STEP_PAD_IN, pack) * ph_title_size * LEADING
        if st.get("text"):
            h += STEP_GAP_V + budget.line_count(st["text"], step_w, item_size, STEP_PAD_IN, pack) * item_size * LEADING
        return h

    step_h_max = max(step_h(st) for st in steps)

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
    y0 = cy + 18.0 + MARK_SIDE * 0.8            # 마커 상단 돌출 여유

    rects: list[RectOp] = []
    arrows: list[ArrowOp] = []
    for i, st in enumerate(steps):
        sx = P + i * (step_w + G)
        rects.append(RectOp(x=sx, y=y0, w=step_w, h=step_h_max))
        if st.get("gate"):
            rects.append(RectOp(x=sx + step_w / 2 - MARK_SIDE / 2, y=y0 - MARK_SIDE / 2,
                                w=MARK_SIDE, h=MARK_SIDE, rx=0.0, rot=45.0))
        ty = y0 + STEP_PAD_V
        tl = budget.line_count(st["title"], step_w, ph_title_size, STEP_PAD_IN, pack)
        texts.append(TextOp(x=sx + step_w / 2, y=ty + tl * ph_title_size * LEADING / 2,
                            size=ph_title_size, text=st["title"], role="ink", weight="bold",
                            max_w=step_w, field=f"path[{i}].title"))
        ty += tl * ph_title_size * LEADING
        if st.get("text"):
            gl = budget.line_count(st["text"], step_w, item_size, STEP_PAD_IN, pack)
            ty += STEP_GAP_V
            texts.append(TextOp(x=sx + step_w / 2, y=ty + gl * item_size * LEADING / 2,
                                size=item_size, text=st["text"], role="ink-soft",
                                max_w=step_w, field=f"path[{i}].text"))
            ty += gl * item_size * LEADING
        if i < n - 1:
            arrows.append(ArrowOp(x1=sx + step_w + 8.0, y1=y0 + step_h_max / 2,
                                  x2=sx + step_w + G - 8.0, y2=y0 + step_h_max / 2))

    y = y0 + step_h_max + 12.0
    note = fence.note or DEFAULT_NOTE
    nl = budget.line_count(note, W - 2 * P, item_size, 8.0, pack)
    texts.append(TextOp(x=W / 2, y=y + nl * item_size * LEADING / 2, size=item_size,
                        text=note, role="ink-mute", max_w=W - 2 * P, field="note"))
    y += nl * item_size * LEADING

    if y > H_frame * HEIGHT_LIMIT:
        raise ApprovalLayoutError(
            f"도식 높이 {y:.0f}pt > 프레임 {H_frame * HEIGHT_LIMIT:.0f}pt(85%) — 스텝 축약 또는 펜스 분할")

    ops = [RectOp(x=0.0, y=0.0, w=W, h=y, rx=0.0, fill_role="paper", stroke_role="rule", stroke_w=0.0),
           *rects, *arrows, *texts]
    _ink_ok(ops, W, y)
    return FigModel(width=W, height=y, ops=tuple(ops), source_index=fence.index)


def _ink_ok(ops, width: float, height: float) -> None:
    # _ink_ok 표준형(Task 1과 동일 — Rect stroke_w/2 포함). 회전 rect는 중심 대칭
    # 확장이므로 등가 반폭 w/2·h/2의 대각 반경을 더해 검사한다(보수적).
    import math as _m
    for o in ops:
        if isinstance(o, RectOp):
            if o.rot != 0.0:
                rad = _m.sqrt(o.w * o.w + o.h * o.h) / 2
                cx, cy2 = o.x + o.w / 2, o.y + o.h / 2
                if (cx - rad < -0.001 or cx + rad > width + 0.001
                        or cy2 - rad < -0.001 or cy2 + rad > height + 0.001):
                    raise ApprovalLayoutError(
                        f"잉크 bbox 프레임 이탈: rect(rot {o.rot:.0f}°) 중심({cx:.1f},{cy2:.1f})")
            else:
                s = o.stroke_w / 2
                if (o.x - s < -0.001 or o.x + o.w + s > width + 0.001
                        or o.y - s < -0.001 or o.y + o.h + s > height + 0.001):
                    raise ApprovalLayoutError(
                        f"잉크 bbox 프레임 이탈: rect({o.x:.1f},{o.y:.1f},{o.w:.1f},{o.h:.1f})")
        elif isinstance(o, ArrowOp):
            if (min(o.x1, o.x2) < -0.001 or max(o.x1, o.x2) > width + 0.001
                    or min(o.y1, o.y2) < -0.001 or max(o.y1, o.y2) > height + 0.001):
                raise ApprovalLayoutError(
                    f"잉크 bbox 프레임 이탈: arrow({o.x1:.1f},{o.y1:.1f}→{o.x2:.1f},{o.y2:.1f})")
        elif isinstance(o, TextOp):
            hw = (o.max_w or 60.0) / 2
            if o.x - hw < -0.001 or o.x + hw > width + 0.001:
                raise ApprovalLayoutError(
                    f"잉크 bbox 프레임 이탈: text({o.field}) x={o.x:.1f} max_w={o.max_w:.1f}")
