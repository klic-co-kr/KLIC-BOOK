"""flow — 순차 단계 배치(스펙 §6.2·§6.3). 결정론: 가로→랩 우선순위 고정.
swimlane 변형(§6.3)은 lanes 키로 분기 — steps와 배타(parse 보장)."""
from __future__ import annotations

import math

from .. import budget
from ..model import ArrowOp, FigModel, RectOp, TextOp
from ..parse import DEFAULT_NOTE
from .base import LayoutError, sizes as _base_sizes

P = 14.0          # 패널 패딩
G = 28.0          # 카드 간격(가로·랩 공용)
MIN_CARD_W = 80.0
CARD_PAD_IN = 8.0
CARD_PAD_V = 10.0
LEADING = 1.3
HEIGHT_LIMIT = 0.85

# 스펙 §6.2 flow 행 — 판형 조건부 상한. layout이 초과하면 즉시 에러(I1 리포트 합류).
PACK_LIMITS = {"essay": 4, "practical": 6, "b5": 6, "business": 8, "lecture": 8}

# swimlane 레인 셀 상한(스펙 §6.2 표 swimlane 행, 개정 4판). 셀 간 GS=24:
# _harrow 오프셋(+4/−8)에서 샤프트 가시 = GS−12 = 12pt로 §6.1 하한과 정확히
# 만난다(GS=16이면 4pt — 적대 검토 G1 폐기안).
PACK_LANE_CELLS = {"essay": 2, "practical": 3, "b5": 4, "business": 4, "lecture": 4}
ACTOR_W = 60.0    # 레인 actor 라벨 열 폭
GS = 24.0         # 레인 셀 간 복도 — 샤프트 가시 = GS−12 ≥ 12(§6.1)
MIN_CELL_W = 45.0


class FlowLayoutError(LayoutError):
    pass    # __init__은 베이스가 detail 처리 — 기존 .detail 계약 유지


def _ink_ok(ops, width: float, height: float) -> None:
    for o in ops:
        if isinstance(o, RectOp):
            if (o.x - o.stroke_w / 2 < -0.001 or o.x + o.w + o.stroke_w / 2 > width + 0.001
                    or o.y - o.stroke_w / 2 < -0.001 or o.y + o.h + o.stroke_w / 2 > height + 0.001):
                raise FlowLayoutError(f"잉크 bbox 프레임 이탈: rect({o.x:.1f},{o.y:.1f},{o.w:.1f},{o.h:.1f})")


def _sizes(tokens: dict) -> tuple[float, float, float, float]:
    # G3 불변식(§5.2-9): 본문±0.3pt 밖. essay처럼 heading2==body인 팩은 +1.5로 밀어낸다.
    s = _base_sizes(tokens)
    return (s["kicker"], s["title"], s["ph_title"], s["item"])


def layout(fence, tokens: dict) -> FigModel:
    frame = tokens["body_frame_pt"]
    W = frame["x1"] - frame["x0"]
    H_frame = frame["y1"] - frame["y0"]
    pack = tokens.get("style", "practical")
    sizes = _sizes(tokens)
    # lanes 펜스는 steps가 비어 있어 cardW 산술이 ZeroDivision — 분기가
    # fence.data["steps"] 접근보다 앞이어야 한다.
    if fence.data.get("lanes"):
        return _lanes(fence, W, H_frame, pack, sizes)
    return _steps(fence, W, H_frame, pack, sizes)


def _header(fence, W: float, texts: list, pack: str, sizes: tuple) -> float:
    """kicker→title→thesis 수직 스택. 반환값은 콘텐츠 영역 시작 y."""
    kicker_size, title_size, _, cx_size = sizes
    t_lines = budget.line_count(fence.title, W - 2 * P, title_size, 0.0, pack)
    cy = 0.0
    if fence.kicker:
        # kicker: 저작 계약 초단문(1줄)
        texts.append(TextOp(x=W / 2, y=cy + kicker_size * LEADING / 2, size=kicker_size,
                            text=fence.kicker, role="ink-mute", field="kicker"))
        cy += kicker_size * LEADING
    texts.append(TextOp(x=W / 2, y=cy + t_lines * title_size * LEADING / 2, size=title_size,
                        text=fence.title, role="ink", weight="bold", max_w=W - 2 * P,
                        field="title"))
    cy += t_lines * title_size * LEADING
    if fence.thesis:
        th_lines = budget.line_count(fence.thesis, W - 2 * P, cx_size, 0.0, pack)
        texts.append(TextOp(x=W / 2, y=cy + th_lines * cx_size * LEADING / 2,
                            size=cx_size, text=fence.thesis, role="ink-soft",
                            max_w=W - 2 * P, field="thesis"))
        cy += th_lines * cx_size * LEADING
    return cy + 18.0


def _finish(fence, cards: list, arrows: list, texts: list, y: float,
            W: float, H_frame: float, cx_size: float, pack: str, remedy: str) -> FigModel:
    """note 부착 → 85% 높이 검사 → 잉크 bbox → FigModel. steps/lanes 공통 마무리."""
    y += 12.0
    note = fence.note or DEFAULT_NOTE
    nl = budget.line_count(note, W - 2 * P, cx_size, 8.0, pack)
    texts.append(TextOp(x=W / 2, y=y + nl * cx_size * LEADING / 2, size=cx_size,
                        text=note, role="ink-mute", max_w=W - 2 * P, field="note"))
    y += nl * cx_size * LEADING
    if y > H_frame * HEIGHT_LIMIT:
        raise FlowLayoutError(
            f"도식 높이 {y:.0f}pt > 프레임 {H_frame * HEIGHT_LIMIT:.0f}pt(85%) — {remedy}")
    ops = [RectOp(x=0.0, y=0.0, w=W, h=y, rx=0.0, fill_role="paper", stroke_role="rule", stroke_w=0.0),
           *cards, *arrows, *texts]
    _ink_ok(ops, W, y)
    return FigModel(width=W, height=y, ops=tuple(ops), source_index=fence.index)


def _steps(fence, W: float, H_frame: float, pack: str, sizes: tuple) -> FigModel:
    _, _, ct_size, cx_size = sizes
    steps = fence.data["steps"]
    n = len(steps)

    # 배치 결정론(§6.2 개정) — 판형 상한 → 가로 → 2행 랩 → 에러. 세로 모드 없음.
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
        t_lines = budget.line_count(step["title"], cardW, ct_size, CARD_PAD_IN, pack)
        x_lines = budget.line_count(step["text"], cardW, cx_size, CARD_PAD_IN, pack)
        return 2 * CARD_PAD_V + t_lines * ct_size * LEADING + 4.0 + x_lines * cx_size * LEADING

    texts: list[TextOp] = []
    y = _header(fence, W, texts, pack, sizes)

    cards: list[RectOp] = []
    arrows: list[ArrowOp] = []
    if mode == "h":
        ch = max(card_h(s) for s in steps)
        for i, s in enumerate(steps):
            cx = P + i * (cardW + G)
            cards.append(RectOp(x=cx, y=y, w=cardW, h=ch))
            _cell_texts(texts, s, cx, y, cardW, ch, ct_size, cx_size, f"steps[{i}]", pack)
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
                _cell_texts(texts, s, cx, ry, cardW, row_h[r], ct_size, cx_size,
                            f"steps[{r * cols + j}]", pack)
                if j:
                    prev_x = P + (j - 1) * (cardW + G)
                    arrows.append(_harrow(prev_x + cardW, ry + row_h[r] / 2, cx))
        y = y + sum(row_h) + G * (len(rows) - 1)

    return _finish(fence, cards, arrows, texts, y, W, H_frame, cx_size, pack,
                   f"steps {n}개를 줄이거나(현재 {n}), 문구를 축약하거나, 도식을 2개 펜스로 분할")


def _lanes(fence, W: float, H_frame: float, pack: str, sizes: tuple) -> FigModel:
    """swimlane 배치(§6.3): actor 열(굵게) + 레인 행. 세로 화살표 없음 — 가로 진행만."""
    _, _, ct_size, cx_size = sizes
    lanes = fence.data["lanes"]
    m = max(len(ln["steps"]) for ln in lanes)
    limit = PACK_LANE_CELLS.get(pack)
    if limit is None:
        raise FlowLayoutError(f"알 수 없는 스타일 팩 {pack!r} — tokens.style 확인")
    if m > limit:
        raise FlowLayoutError(
            f"레인 셀 {m}개 > 판형 상한 {limit}({pack}) — 요소 수 감소 또는 펜스 분할")
    cellW = (W - 2 * P - ACTOR_W - (m - 1) * GS) / m
    if cellW < MIN_CELL_W:
        raise FlowLayoutError(
            f"셀폭 {cellW:.1f}pt < {MIN_CELL_W:.0f}pt — 요소 수 감소 또는 문구 축약")
    texts: list[TextOp] = []
    y = _header(fence, W, texts, pack, sizes)

    def cell_h(s: dict) -> float:
        t_lines = budget.line_count(s["title"], cellW, ct_size, CARD_PAD_IN, pack)
        x_lines = budget.line_count(s["text"], cellW, cx_size, CARD_PAD_IN, pack)
        return 2 * CARD_PAD_V + t_lines * ct_size * LEADING + 4.0 + x_lines * cx_size * LEADING

    cards: list[RectOp] = []
    arrows: list[ArrowOp] = []
    below = 0.0                       # 이전 레인 높이 누적 + 레인 간 G — ry 산출용
    for i, ln in enumerate(lanes):
        rh = max(cell_h(s) for s in ln["steps"])
        ry = y + below
        texts.append(TextOp(x=P + ACTOR_W / 2, y=ry + rh / 2, size=ct_size,
                            text=ln["actor"], role="ink", weight="bold",
                            max_w=ACTOR_W, field=f"lanes[{i}].actor"))
        for j, s in enumerate(ln["steps"]):
            cx = P + ACTOR_W + j * (cellW + GS)
            cards.append(RectOp(x=cx, y=ry, w=cellW, h=rh))
            _cell_texts(texts, s, cx, ry, cellW, rh, ct_size, cx_size,
                        f"lanes[{i}].steps[{j}]", pack)
            if j:
                arrows.append(_harrow(cx - GS, ry + rh / 2, cx))
        below += rh + G
    y += below - G                     # 마지막 레인 아래 간격 제거

    return _finish(fence, cards, arrows, texts, y, W, H_frame, cx_size, pack,
                   f"레인 {len(lanes)}개 또는 셀 문구를 줄이거나, 도식을 2개 펜스로 분할")


def _cell_texts(out: list, s: dict, cx: float, cy: float, cw: float, ch: float,
                t_size: float, x_size: float, field: str, pack: str) -> None:
    t_lines = budget.line_count(s["title"], cw, t_size, pack=pack)
    x_lines = budget.line_count(s["text"], cw, x_size, pack=pack)
    block = t_lines * t_size * LEADING + 4.0 + x_lines * x_size * LEADING
    top = cy + (ch - block) / 2
    out.append(TextOp(x=cx + cw / 2, y=top + t_lines * t_size * LEADING / 2, size=t_size,
                      text=s["title"], role="ink", weight="bold", max_w=cw,
                      field=f"{field}.title"))
    mid = top + t_lines * t_size * LEADING + 4.0
    out.append(TextOp(x=cx + cw / 2, y=mid + x_lines * x_size * LEADING / 2, size=x_size,
                      text=s["text"], role="ink-soft", max_w=cw, field=f"{field}.text"))


def _harrow(right_edge: float, ymid: float, next_left: float) -> ArrowOp:
    # 복도 G=28: shaft 길이 16(≥12). 레인 복도 GS=24: shaft 12(하한과 일치).
    # tip이 목표 박스 8pt 전에 착지(§6.1)
    return ArrowOp(x1=right_edge + 4.0, y1=ymid, x2=next_left - 8.0, y2=ymid)
