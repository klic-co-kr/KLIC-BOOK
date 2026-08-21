"""flow — 순차 단계 배치(스펙 §6.2·§6.3). 결정론: 가로→랩→세로 우선순위 고정."""
from __future__ import annotations

import math

from .. import budget
from ..model import ArrowOp, FigModel, RectOp, TextOp

P = 14.0          # 패널 패딩
G = 28.0          # 카드 간격(가로·랩 공용)
MIN_CARD_W = 80.0
CARD_PAD_IN = 8.0
CARD_PAD_V = 10.0
LEADING = 1.3
HEIGHT_LIMIT = 0.85

# 스펙 §6.2 flow 행 — 판형 조건부 상한. layout이 초과하면 즉시 에러(I1 리포트 합류).
PACK_LIMITS = {"essay": 4, "practical": 6, "b5": 6, "business": 8, "lecture": 8}


class FlowLayoutError(Exception):
    def __init__(self, detail: str):
        super().__init__(detail)
        self.detail = detail


def _ink_ok(ops, width: float, height: float) -> None:
    for o in ops:
        if isinstance(o, RectOp):
            if (o.x - o.stroke_w / 2 < -0.001 or o.x + o.w + o.stroke_w / 2 > width + 0.001
                    or o.y - o.stroke_w / 2 < -0.001 or o.y + o.h + o.stroke_w / 2 > height + 0.001):
                raise FlowLayoutError(f"잉크 bbox 프레임 이탈: rect({o.x:.1f},{o.y:.1f},{o.w:.1f},{o.h:.1f})")


def layout(fence, tokens: dict) -> FigModel:
    frame = tokens["body_frame_pt"]
    W = frame["x1"] - frame["x0"]
    H_frame = frame["y1"] - frame["y0"]
    f = tokens["fonts"]
    body = f["body"]["size_pt"]
    # G3 불변식(§5.2-9): 본문±0.3pt 밖. essay처럼 heading2==body인 팩은 +1.5로 밀어낸다.
    title_size = f["heading2"]["size_pt"]
    if abs(title_size - body) <= 0.3:
        title_size = body + 1.5
    kicker_size = f["label"]["size_pt"]
    card_title_size = body + 1
    card_text_size = body - 1

    steps = fence.data["steps"]
    n = len(steps)

    # 배치 결정론(§6.2 개정) — 판형 상한 → 가로 → 2행 랩 → 에러. 세로 모드 없음.
    pack = tokens.get("style", "practical")
    limit = PACK_LIMITS.get(pack)
    if limit is None:
        raise FlowLayoutError(f"알 수 없는 스타일 팩 {pack!r} — tokens.style 확인")
    if n > limit:
        raise FlowLayoutError(
            f"steps {n}개 > 판형 상한 {limit}({pack}) — 요소 수 감소 또는 펜스 분할")
    mode = None
    cardW = 0.0
    cols = n
    cardW_h = (W - 2 * P - (n - 1) * G) / n
    if cardW_h >= MIN_CARD_W:
        mode, cardW = "h", cardW_h
    else:
        cols = math.ceil(n / 2)
        cardW_w = (W - 2 * P - (cols - 1) * G) / cols
        if cardW_w >= MIN_CARD_W:
            mode, cardW = "wrap", cardW_w
        else:
            raise FlowLayoutError(
                f"steps {n}개를 {pack} 판형에 배치 불가(랩 후 카드폭 {cardW_w:.1f}pt < "
                f"{MIN_CARD_W:.0f}pt) — 글자 축약, 요소 수 감소 또는 펜스 분할")

    def card_h(step: dict) -> float:
        t_lines = budget.line_count(step["title"], cardW, card_title_size, CARD_PAD_IN, pack)
        x_lines = budget.line_count(step["text"], cardW, card_text_size, CARD_PAD_IN, pack)
        return 2 * CARD_PAD_V + t_lines * card_title_size * LEADING + 4.0 + x_lines * card_text_size * LEADING

    # 헤더 블록
    header_h = 0.0
    texts: list[TextOp] = []
    if fence.kicker:
        header_h += kicker_size * LEADING
    t_lines = budget.line_count(fence.title, W - 2 * P, title_size, 0.0, pack)
    header_h += t_lines * title_size * LEADING
    if fence.thesis:
        header_h += budget.line_count(fence.thesis, W - 2 * P, card_text_size, 0.0, pack) * card_text_size * LEADING
    header_h += 18.0                                # 제목→카드 간

    ops: list = []
    y = 0.0
    cy = 0.0
    if fence.kicker:
        texts.append(TextOp(x=W / 2, y=cy + kicker_size * LEADING / 2, size=kicker_size,
                            text=fence.kicker, role="ink-mute", field="kicker"))
        cy += kicker_size * LEADING
    texts.append(TextOp(x=W / 2, y=cy + t_lines * title_size * LEADING / 2, size=title_size,
                        text=fence.title, role="ink", weight="bold", max_w=W - 2 * P,
                        field="title"))
    cy += t_lines * title_size * LEADING
    if fence.thesis:
        th_lines = budget.line_count(fence.thesis, W - 2 * P, card_text_size, 0.0, pack)
        texts.append(TextOp(x=W / 2, y=cy + th_lines * card_text_size * LEADING / 2,
                            size=card_text_size, text=fence.thesis, role="ink-soft",
                            max_w=W - 2 * P, field="thesis"))
        cy += th_lines * card_text_size * LEADING
    y = cy + 18.0

    cards: list[RectOp] = []
    arrows: list[ArrowOp] = []
    if mode == "h":
        ch = max(card_h(s) for s in steps)
        for i, s in enumerate(steps):
            cx = P + i * (cardW + G)
            cards.append(RectOp(x=cx, y=y, w=cardW, h=ch))
            _card_texts(texts, s, cx, y, cardW, ch, card_title_size, card_text_size, i, pack)
            if i:
                prev_x = P + (i - 1) * (cardW + G)
                arrows.append(_harrow(prev_x + cardW, y + ch / 2, cx))
        y += ch
    elif mode == "wrap":
        rows = [steps[i:i + cols] for i in range(0, n, cols)]
        row_h = [max(card_h(s) for s in row) for row in rows]
        for r, row in enumerate(rows):
            ry = y + sum(row_h[:r]) + G * r
            for j, s in enumerate(row):
                cx = P + j * (cardW + G)
                cards.append(RectOp(x=cx, y=ry, w=cardW, h=row_h[r]))
                _card_texts(texts, s, cx, ry, cardW, row_h[r], card_title_size,
                            card_text_size, r * cols + j, pack)
                if j:
                    prev_x = P + (j - 1) * (cardW + G)
                    arrows.append(_harrow(prev_x + cardW, ry + row_h[r] / 2, cx))
        y = y + sum(row_h) + G * (len(rows) - 1)

    y += 12.0
    from ..parse import DEFAULT_NOTE
    note = fence.note or DEFAULT_NOTE
    texts.append(TextOp(x=W / 2, y=y + card_text_size * LEADING / 2, size=card_text_size,
                        text=note, role="ink-mute", max_w=W - 2 * P, field="note"))
    y += card_text_size * LEADING

    if y > H_frame * HEIGHT_LIMIT:
        raise FlowLayoutError(
            f"도식 높이 {y:.0f}pt > 프레임 {H_frame * HEIGHT_LIMIT:.0f}pt(85%) — "
            f"steps {n}개를 줄이거나(현재 {n}), 문구를 축약하거나, 도식을 2개 펜스로 분할")

    ops = [RectOp(x=0.0, y=0.0, w=W, h=y, rx=0.0, fill_role="paper", stroke_role="rule", stroke_w=0.0),
           *cards, *arrows, *texts]
    _ink_ok(ops, W, y)
    return FigModel(width=W, height=y, ops=tuple(ops), source_index=fence.index)


def _card_texts(out: list, s: dict, cx: float, cy: float, cw: float, ch: float,
                t_size: float, x_size: float, idx: int, pack: str) -> None:
    t_lines = budget.line_count(s["title"], cw, t_size, pack=pack)
    x_lines = budget.line_count(s["text"], cw, x_size, pack=pack)
    block = t_lines * t_size * LEADING + 4.0 + x_lines * x_size * LEADING
    top = cy + (ch - block) / 2
    out.append(TextOp(x=cx + cw / 2, y=top + t_lines * t_size * LEADING / 2, size=t_size,
                      text=s["title"], role="ink", weight="bold", max_w=cw,
                      field=f"steps[{idx}].title"))
    mid = top + t_lines * t_size * LEADING + 4.0
    out.append(TextOp(x=cx + cw / 2, y=mid + x_lines * x_size * LEADING / 2, size=x_size,
                      text=s["text"], role="ink-soft", max_w=cw, field=f"steps[{idx}].text"))


def _harrow(right_edge: float, ymid: float, next_left: float) -> ArrowOp:
    # 복도 G=28: shaft 길이 16(≥12), tip이 목표 박스 8pt 전에 착지(§6.1)
    return ArrowOp(x1=right_edge + 4.0, y1=ymid, x2=next_left - 8.0, y2=ymid)
