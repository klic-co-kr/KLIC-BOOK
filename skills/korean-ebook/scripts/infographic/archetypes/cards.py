"""cards — 헤드라인 카드 그리드(스펙 §6.2·§6.3). 결정론: cols=min(팩열수,n), 2행 랩, 세로 없음."""
from __future__ import annotations

from .. import budget
from ..model import FigModel, RectOp, TextOp
from ..parse import DEFAULT_NOTE, Fence
from .base import LayoutError, sizes

P = 14.0
G = 28.0
CARD_MIN_N, CARD_MAX_N = 2, 6
MIN_CARD_W = 80.0
CARD_PAD_IN = 8.0
CARD_PAD_V = 10.0
LEADING = 1.3
# typst 실측(2026-08-22, Pretendard 11pt·par leading 1.3em): 줄 진행 2.008em
# = leading 1.3em + cap-height 0.71em.
# 1줄 박스 높이는 1.19em(ascent 1.06 + descent 0.13 — 스팬 bbox 실측).
# ig-text는 블록 "중심" 앵커이므로 예산이 박스보다 작으면 인접 블록이
# 중심끼리 밀려 잉크가 겹친다(헤더 kicker↔title 4.89pt, value↔title 1.31pt
# 스팬 실측 — LINE_FIRST_EM=0.75 시대의 값). 예산은 박스 이상을 확보한다.
# 줄 n개 블록 높이 = size·(1.19 + 2.05·(n−1)) — step 2.05는 실측 진행
# 2.008em에 여유를 둔 상한.
LINE_FIRST_EM = 1.19
LINE_STEP_EM = 2.05
HEIGHT_LIMIT = 0.85
VALUE_BONUS_PT = 2.0                       # value 강조 — 카드 제목+2pt


def block_h(n: int, size: float) -> float:
    """줄 n개 텍스트 블록의 typst 레이아웃 높이(pt) — 실측 줄 진행 공식."""
    return size * (LINE_FIRST_EM + LINE_STEP_EM * (n - 1))

PACK_COLS = {"essay": 2, "practical": 3, "b5": 3, "business": 3, "lecture": 3}


class CardsLayoutError(LayoutError):
    pass


def layout(fence: Fence, tokens: dict) -> FigModel:
    frame = tokens["body_frame_pt"]
    W = frame["x1"] - frame["x0"]
    H_frame = frame["y1"] - frame["y0"]
    pack = tokens.get("style", "practical")
    s = sizes(tokens)
    title_size = s["title"]
    kicker_size = s["kicker"]
    card_title_size = s["ph_title"]
    card_text_size = s["item"]
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
            h += block_h(budget.line_count(c["value"], cardW, value_size, CARD_PAD_IN, pack), value_size) + 4.0
        h += block_h(budget.line_count(c["title"], cardW, card_title_size, CARD_PAD_IN, pack), card_title_size) + 4.0
        h += block_h(budget.line_count(c["text"], cardW, card_text_size, CARD_PAD_IN, pack), card_text_size)
        return h

    # 헤더(Phase 1 flow와 동일 구조). 블록 사이 4.0pt 간격 — 중심 앵커 블록이
    # 박스 높이(1.19em)만큼 위아래로 뻗으므로 간격이 없으면 잉크가 맞닿는다
    # (카드 내부 value→title→text의 +4.0과 같은 리듬).
    HEADER_GAP = 4.0
    texts: list[TextOp] = []
    cy = 0.0
    if fence.kicker:
        # kicker: 저작 계약 초단문(1줄)
        texts.append(TextOp(x=W / 2, y=cy + block_h(1, kicker_size) / 2, size=kicker_size,
                            text=fence.kicker, role="ink-mute", field="kicker"))
        cy += block_h(1, kicker_size) + HEADER_GAP
    t_lines = budget.line_count(fence.title, W - 2 * P, title_size, 0.0, pack)
    texts.append(TextOp(x=W / 2, y=cy + block_h(t_lines, title_size) / 2, size=title_size,
                        text=fence.title, role="ink", weight="bold", max_w=W - 2 * P, field="title"))
    cy += block_h(t_lines, title_size) + HEADER_GAP
    if fence.thesis:
        th = budget.line_count(fence.thesis, W - 2 * P, card_text_size, 0.0, pack)
        texts.append(TextOp(x=W / 2, y=cy + block_h(th, card_text_size) / 2, size=card_text_size,
                            text=fence.thesis, role="ink-soft", max_w=W - 2 * P, field="thesis"))
        cy += block_h(th, card_text_size)
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
    nl = budget.line_count(note, W - 2 * P, card_text_size, 8.0, pack)
    texts.append(TextOp(x=W / 2, y=y + block_h(nl, card_text_size) / 2, size=card_text_size,
                        text=note, role="ink-mute", max_w=W - 2 * P, field="note"))
    y += block_h(nl, card_text_size)

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
    # pad를 CARD_PAD_IN으로 명시 — card_h(높이 예산)와 같은 파라미터로 줄 수 일치 보장.
    # max_w도 cw 전폭이 아니라 좌우 CARD_PAD_IN 감소폭 — 잉크가 테두리에 닿지 않는다
    # (실측 2026-08-22: 전폭 기준 최대 −2.01pt 이탈).
    t_lines = budget.line_count(c["title"], cw, t_size, CARD_PAD_IN, pack)
    x_lines = budget.line_count(c["text"], cw, x_size, CARD_PAD_IN, pack)
    v_lines = budget.line_count(c.get("value", ""), cw, v_size, CARD_PAD_IN, pack) if "value" in c else 0
    block = (block_h(v_lines, v_size) + 4.0 if "value" in c else 0.0) \
        + block_h(t_lines, t_size) + 4.0 + block_h(x_lines, x_size)
    top = cy + (ch - block) / 2
    cur = top
    mw = cw - 2 * CARD_PAD_IN
    if "value" in c:
        out.append(TextOp(x=cx + cw / 2, y=cur + block_h(v_lines, v_size) / 2, size=v_size,
                          text=c["value"], role="focus", weight="bold", max_w=mw,
                          field=f"cards[{idx}].value"))
        cur += block_h(v_lines, v_size) + 4.0
    out.append(TextOp(x=cx + cw / 2, y=cur + block_h(t_lines, t_size) / 2, size=t_size,
                      text=c["title"], role="ink", weight="bold", max_w=mw,
                      field=f"cards[{idx}].title"))
    cur += block_h(t_lines, t_size) + 4.0
    out.append(TextOp(x=cx + cw / 2, y=cur + block_h(x_lines, x_size) / 2, size=x_size,
                      text=c["text"], role="ink-soft", max_w=mw, field=f"cards[{idx}].text"))


def _ink_ok(ops, width: float, height: float) -> None:
    for o in ops:
        if isinstance(o, RectOp):
            if (o.x - o.stroke_w / 2 < -0.001 or o.x + o.w + o.stroke_w / 2 > width + 0.001
                    or o.y - o.stroke_w / 2 < -0.001 or o.y + o.h + o.stroke_w / 2 > height + 0.001):
                raise CardsLayoutError(
                    f"잉크 bbox 프레임 이탈: rect({o.x:.1f},{o.y:.1f},{o.w:.1f},{o.h:.1f})")
