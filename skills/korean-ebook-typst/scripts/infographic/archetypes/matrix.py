"""matrix — 비교 격자 + 정성 2×2(스펙 §6.2·§6.3). 셀 간격 0(격자), 정성 셀 간 G."""
from __future__ import annotations

from .base import LayoutError
from .. import budget
from ..model import FigModel, RectOp, TextOp
from ..parse import DEFAULT_NOTE, Fence

P = 14.0
G = 28.0
MIN_COL_W = 40.0                 # 격자 셀 최소폭 — 이 이하면 텍스트 불가
MIN_QUAL_W = 60.0                # 정성 셀 최소폭(카드 문지방 완화 — essay 격자 3열 73.8pt와 정합)
CELL_PAD = 6.0
LEADING = 1.3
HEIGHT_LIMIT = 0.85
GRID_MAX_ROWS = 6

PACK_MAX_COLS = {"essay": 3, "practical": 4, "b5": 4, "business": 5, "lecture": 5}


class MatrixLayoutError(LayoutError):
    pass


def layout(fence: Fence, tokens: dict) -> FigModel:
    if "headers" in fence.data:
        return _grid(fence, tokens)
    return _qualitative(fence, tokens)


def _sizes(tokens: dict):
    f = tokens["fonts"]
    body = f["body"]["size_pt"]
    title_size = f["heading2"]["size_pt"]
    if abs(title_size - body) <= 0.3:
        title_size = body + 1.5
    return (f["label"]["size_pt"], title_size, body + 1, body - 1, body)


def _header_block(fence, tokens, W, texts):
    kicker_size, title_size, ct_size, cx_size, body = _sizes(tokens)
    cy = 0.0
    if fence.kicker:
        texts.append(TextOp(x=W / 2, y=cy + kicker_size * LEADING / 2, size=kicker_size,
                            text=fence.kicker, role="ink-mute", field="kicker"))
        cy += kicker_size * LEADING
    t_lines = budget.line_count(fence.title, W - 2 * P, title_size, 0.0, tokens.get("style", "practical"))
    texts.append(TextOp(x=W / 2, y=cy + t_lines * title_size * LEADING / 2, size=title_size,
                        text=fence.title, role="ink", weight="bold", max_w=W - 2 * P, field="title"))
    cy += t_lines * title_size * LEADING
    return cy + 18.0


def _footer(fence, texts, y, cx_size, W):
    texts.append(TextOp(x=W / 2, y=y + cx_size * LEADING / 2, size=cx_size,
                        text=fence.note or DEFAULT_NOTE, role="ink-mute",
                        max_w=W - 2 * P, field="note"))
    return y + cx_size * LEADING


def _finish(ops, texts, W, y, H_frame, source_index: int):
    """ops+texts를 합산해 잉크 검사 후 FigModel 반환 — texts를 버리면 안 된다(적대 검토 G1)."""
    all_ops = [*ops, *texts]
    if y > H_frame * HEIGHT_LIMIT:
        raise MatrixLayoutError(
            f"도식 높이 {y:.0f}pt > 프레임 {H_frame * HEIGHT_LIMIT:.0f}pt(85%) — "
            f"행 감소, 문구 축약 또는 펜스 분할")
    for o in all_ops:
        if isinstance(o, RectOp):
            if (o.x - o.stroke_w / 2 < -0.001 or o.x + o.w + o.stroke_w / 2 > W + 0.001
                    or o.y - o.stroke_w / 2 < -0.001 or o.y + o.h + o.stroke_w / 2 > y + 0.001):
                raise MatrixLayoutError(f"잉크 bbox 프레임 이탈: rect({o.x:.1f},{o.y:.1f})")
    return FigModel(width=W, height=y, ops=tuple(all_ops), source_index=source_index)


def _grid(fence: Fence, tokens: dict) -> FigModel:
    frame = tokens["body_frame_pt"]
    W, H_frame = frame["x1"] - frame["x0"], frame["y1"] - frame["y0"]
    pack = tokens.get("style", "practical")
    kicker_size, title_size, ct_size, cx_size, body = _sizes(tokens)
    headers = fence.data["headers"]
    rows = fence.data["rows"]
    ncols = len(headers)
    max_cols = PACK_MAX_COLS.get(pack)
    if max_cols is None:
        raise MatrixLayoutError(f"알 수 없는 스타일 팩 {pack!r}")
    if ncols > max_cols:
        raise MatrixLayoutError(
            f"열 {ncols}개 > 판형 상한 {max_cols}({pack}) — 열 감소 또는 펜스 분할")

    texts: list[TextOp] = []
    y = _header_block(fence, tokens, W, texts)

    colW = (W - 2 * P) / ncols
    if colW < MIN_COL_W:
        raise MatrixLayoutError(
            f"셀폭 {colW:.1f}pt < {MIN_COL_W:.0f}pt — 열 감소 또는 문구 축약")

    # 헤더 행
    hh = max(budget.line_count(h, colW, kicker_size, CELL_PAD, pack) for h in headers) * kicker_size * LEADING + 8.0
    for c, h in enumerate(headers):
        texts.append(TextOp(x=P + c * colW + colW / 2, y=y + hh / 2, size=kicker_size,
                            text=h, role="ink-mute", weight="bold", max_w=colW, field=f"headers[{c}]"))
    y += hh

    ops: list = [RectOp(x=0.0, y=0.0, w=W, h=0.1, rx=0.0, fill_role="paper",
                        stroke_role="rule", stroke_w=0.0)]
    for r, row in enumerate(rows):
        lines = max(budget.line_count(cell, colW, cx_size, CELL_PAD, pack) for cell in row)
        rh = lines * cx_size * LEADING + 8.0
        for c, cell in enumerate(row):
            first = c == 0
            ops.append(RectOp(x=P + c * colW, y=y, w=colW, h=rh, fill_role="surface-tint"))
            texts.append(TextOp(x=P + c * colW + colW / 2, y=y + rh / 2, size=cx_size,
                                text=cell, role="ink" if first else "ink-soft",
                                weight="bold" if first else "regular", max_w=colW,
                                field=f"cell[{r}][{c}]"))
        y += rh
    y += 12.0
    y = _footer(fence, texts, y, cx_size, W)
    return _finish(ops, texts, W, y, H_frame, fence.index)


def _qualitative(fence: Fence, tokens: dict) -> FigModel:
    frame = tokens["body_frame_pt"]
    W, H_frame = frame["x1"] - frame["x0"], frame["y1"] - frame["y0"]
    pack = tokens.get("style", "practical")
    kicker_size, title_size, ct_size, cx_size, body = _sizes(tokens)
    xa, ya, cells = fence.data["x_axis"], fence.data["y_axis"], fence.data["cells"]

    texts: list[TextOp] = []
    y = _header_block(fence, tokens, W, texts)

    # x축 라벨 행(하단 축 위) + y축 라벨(좌측 열) — 축 라벨 폭 40pt
    AXIS_W = 40.0
    cellW = (W - 2 * P - AXIS_W - G) / 2

    # y축 라벨(low 위, high 아래) — 각 셀 행 중심
    def cell_h(cell: dict) -> float:
        return 2 * 10.0 + budget.line_count(cell["title"], cellW, ct_size, 8.0, pack) * ct_size * LEADING \
            + 4.0 + budget.line_count(cell["text"], cellW, cx_size, 8.0, pack) * cx_size * LEADING

    if cellW < MIN_QUAL_W:
        raise MatrixLayoutError(
            f"정성 셀폭 {cellW:.1f}pt < {MIN_QUAL_W:.0f}pt — 문구 축약 또는 축 라벨 축소")

    h0 = max(cell_h(cells[0]), cell_h(cells[1]))
    h1 = max(cell_h(cells[2]), cell_h(cells[3]))
    # x 라벨(2칸: low/high) 위 행
    xl_h = kicker_size * LEADING + 6.0
    for j, lab in enumerate((xa["low"], xa["high"])):
        texts.append(TextOp(x=P + AXIS_W + j * (cellW + G) + cellW / 2, y=y + xl_h / 2,
                            size=kicker_size, text=lab, role="ink-mute", max_w=cellW,
                            field=f"axis.x{j}"))
    y += xl_h
    ops: list = [RectOp(x=0.0, y=0.0, w=W, h=0.1, rx=0.0, fill_role="paper",
                        stroke_role="rule", stroke_w=0.0)]
    for r, (ylab, pair, hh) in enumerate(((ya["low"], (cells[0], cells[1]), h0),
                                          (ya["high"], (cells[2], cells[3]), h1))):
        ry = y + sum((h0, h1)[:r]) + G * r
        texts.append(TextOp(x=P + AXIS_W / 2, y=ry + hh / 2, size=kicker_size,
                            text=ylab, role="ink-mute", weight="bold", max_w=AXIS_W,
                            field=f"axis.y{r}"))
        for j, cell in enumerate(pair):
            cx = P + AXIS_W + j * (cellW + G)
            idx = r * 2 + j
            ops.append(RectOp(x=cx, y=ry, w=cellW, h=hh))
            texts.append(TextOp(x=cx + cellW / 2, y=ry + 10.0 + budget.line_count(
                cell["title"], cellW, ct_size, 8.0, pack) * ct_size * LEADING / 2,
                size=ct_size, text=cell["title"], role="ink", weight="bold",
                max_w=cellW, field=f"cells[{idx}].title"))
            texts.append(TextOp(x=cx + cellW / 2, y=ry + hh - 10.0 - budget.line_count(
                cell["text"], cellW, cx_size, 8.0, pack) * cx_size * LEADING / 2,
                size=cx_size, text=cell["text"], role="ink-soft", max_w=cellW,
                field=f"cells[{idx}].text"))
    y = y + h0 + h1 + G
    y += 12.0
    y = _footer(fence, texts, y, cx_size, W)
    return _finish(ops, texts, W, y, H_frame, fence.index)
