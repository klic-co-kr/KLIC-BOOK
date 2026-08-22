"""cards — 헤드라인 카드 그리드(스펙 §6.2·§6.3). 결정론: cols=min(팩열수,n), 2행 랩, 세로 없음."""
from __future__ import annotations

from .. import budget
from ..model import FigModel, RectOp, TextOp
from ..parse import DEFAULT_NOTE, Fence
from .base import LayoutError

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


class CardsLayoutError(LayoutError):
    pass


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
        # value도 실측 줄 수 반영 — _card_texts(렌더)와 동일 파라미터(cardW·CARD_PAD_IN·pack)
        h = 2 * CARD_PAD_V
        if "value" in c:
            h += budget.line_count(c["value"], cardW, value_size, CARD_PAD_IN, pack) * value_size * LEADING + 4.0
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
    # pad를 CARD_PAD_IN으로 명시 — card_h(높이 예산)와 같은 파라미터로 줄 수 일치 보장
    t_lines = budget.line_count(c["title"], cw, t_size, CARD_PAD_IN, pack)
    x_lines = budget.line_count(c["text"], cw, x_size, CARD_PAD_IN, pack)
    v_lines = budget.line_count(c.get("value", ""), cw, v_size, CARD_PAD_IN, pack) if "value" in c else 0
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
