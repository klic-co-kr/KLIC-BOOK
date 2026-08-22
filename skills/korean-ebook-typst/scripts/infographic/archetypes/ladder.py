"""ladder — 계단식 성숙도(스펙 §6.3). x·y 동시 증가 오프셋, 하→상. 판형 상한 없음(절대 3~5만)."""
from __future__ import annotations

from .. import budget
from ..model import ArrowOp, FigModel, RectOp, TextOp
from ..parse import DEFAULT_NOTE, Fence
from .base import LayoutError

P = 14.0
BOX_W_FRAC = 0.56
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
    for o in ops:
        if isinstance(o, RectOp):
            if (o.x < -0.001 or o.x + o.w > width + 0.001
                    or o.y < -0.001 or o.y + o.h > height + 0.001):
                raise LadderLayoutError(
                    f"잉크 bbox 프레임 이탈: rect({o.x:.1f},{o.y:.1f},{o.w:.1f},{o.h:.1f})")
        elif isinstance(o, ArrowOp):
            if (min(o.x1, o.x2) < -0.001 or max(o.x1, o.x2) > width + 0.001
                    or min(o.y1, o.y2) < -0.001 or max(o.y1, o.y2) > height + 0.001):
                raise LadderLayoutError(
                    f"잉크 bbox 프레임 이탈: arrow({o.x1:.1f},{o.y1:.1f}→{o.x2:.1f},{o.y2:.1f})")
        elif isinstance(o, TextOp):
            hw = (o.max_w or 60.0) / 2
            if o.x - hw < -0.001 or o.x + hw > width + 0.001:
                raise LadderLayoutError(
                    f"잉크 bbox 프레임 이탈: text({o.field}) x={o.x:.1f} max_w={o.max_w:.1f}")
