"""topology — 노드 grid/계층 배치 + 간선 화살표(스펙 §6.2·§6.3). 판형 상한 노드 수로 즉시 에러."""
from __future__ import annotations

import math

from .. import budget
from ..model import ArrowOp, FigModel, RectOp, TextOp
from ..parse import DEFAULT_NOTE, Fence
from .base import LayoutError, sizes

P = 14.0
G = 28.0                     # 커넥터 복도 — tip-gap 8 양측 후 샤프트 12pt(§6.1)
G_V = 24.0                   # 같은 열 노드 수직 간격
NODE_PAD_IN = 8.0
NODE_PAD_V = 8.0
MIN_NODE_W = 54.0            # §6.2 상한 전팩 도달 — essay 5노드 3열 55.15pt 실측
LEADING = 1.3
HEIGHT_LIMIT = 0.85

PACK_NODES = {"essay": 5, "practical": 6, "b5": 7, "business": 8, "lecture": 8}


class TopologyLayoutError(LayoutError):
    pass


def layout(fence: Fence, tokens: dict) -> FigModel:
    frame = tokens["body_frame_pt"]
    W = frame["x1"] - frame["x0"]
    H_frame = frame["y1"] - frame["y0"]
    pack = tokens.get("style", "practical")
    s = sizes(tokens)
    kicker_size, title_size, item_size = s["kicker"], s["title"], s["item"]

    nodes = fence.data["nodes"]
    edges = fence.data.get("edges", [])
    n = len(nodes)
    cap = PACK_NODES.get(pack)
    if cap is None:
        raise TopologyLayoutError(f"알 수 없는 스타일 팩 {pack!r}")
    if n > cap:
        raise TopologyLayoutError(
            f"노드 {n}개 > 판형 상한 {cap}개({pack}) — 노드 통합 또는 펜스 분할")

    # 배치 열·행 — 간선 없으면 grid, 있으면 최장경로 DAG 층위
    if edges:
        layer = _longest_path_layers(nodes, edges)
        pos = {}
        per_col: dict[int, int] = {}
        for nd in nodes:
            c = layer[nd["id"]]
            pos[nd["id"]] = (c, per_col.get(c, 0))
            per_col[c] = per_col.get(c, 0) + 1
    else:
        cols = math.ceil(math.sqrt(n))
        pos = {nd["id"]: (i % cols, i // cols) for i, nd in enumerate(nodes)}
    ncols = max(c for c, _ in pos.values()) + 1

    node_w = (W - 2 * P - (ncols - 1) * G) / ncols
    if node_w < MIN_NODE_W:
        raise TopologyLayoutError(
            f"노드 폭 {node_w:.1f}pt < {MIN_NODE_W:.0f}pt({pack}) — 노드 통합 또는 펜스 분할")

    # 노드 높이 — 전 노드 최대 실측(균일 그리드)
    lines = max(budget.line_count(nd["label"], node_w - 2 * NODE_PAD_IN, item_size,
                                 NODE_PAD_IN, pack) for nd in nodes)
    node_h = 2 * NODE_PAD_V + lines * item_size * LEADING

    # 헤더(공통 구조) — kicker/title/thesis 후 y 시작(kicker는 저작 계약 초단문 1줄)
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
    center: dict[str, tuple[float, float]] = {}
    for i, nd in enumerate(nodes):
        c, r = pos[nd["id"]]
        nx = P + c * (node_w + G)
        ny = y0 + r * (node_h + G_V)
        rects.append(RectOp(x=nx, y=ny, w=node_w, h=node_h))
        center[nd["id"]] = (nx + node_w / 2, ny + node_h / 2)
        texts.append(TextOp(x=nx + node_w / 2, y=ny + node_h / 2, size=item_size,
                            text=nd["label"], role="ink", max_w=node_w - 2 * NODE_PAD_IN,
                            field=f"nodes[{i}].label"))

    arrows = [ArrowOp(x1=center[e["from"]][0] + node_w / 2 + 8.0, y1=center[e["from"]][1],
                      x2=center[e["to"]][0] - node_w / 2 - 8.0, y2=center[e["to"]][1],
                      style="dashed" if e.get("dashed") else "solid")
              for e in edges]

    bottom = y0 + max(r for _, r in pos.values()) * (node_h + G_V) + node_h
    y = bottom + 12.0
    note = fence.note or DEFAULT_NOTE
    nl = budget.line_count(note, W - 2 * P, item_size, 8.0, pack)
    texts.append(TextOp(x=W / 2, y=y + nl * item_size * LEADING / 2, size=item_size,
                        text=note, role="ink-mute", max_w=W - 2 * P, field="note"))
    y += nl * item_size * LEADING

    if y > H_frame * HEIGHT_LIMIT:
        raise TopologyLayoutError(
            f"도식 높이 {y:.0f}pt > 프레임 {H_frame * HEIGHT_LIMIT:.0f}pt(85%) — 노드 축약 또는 펜스 분할")

    ops = [RectOp(x=0.0, y=0.0, w=W, h=y, rx=0.0, fill_role="paper", stroke_role="rule", stroke_w=0.0),
           *rects, *arrows, *texts]
    _ink_ok(ops, W, y)
    return FigModel(width=W, height=y, ops=tuple(ops), source_index=fence.index)


def _longest_path_layers(nodes: list, edges: list) -> dict:
    ids = [nd["id"] for nd in nodes]
    preds = {i: [] for i in ids}
    succs = {i: [] for i in ids}
    indeg = {i: 0 for i in ids}
    for e in edges:
        succs[e["from"]].append(e["to"])
        preds[e["to"]].append(e["from"])
        indeg[e["to"]] += 1
    order = [i for i in ids if indeg[i] == 0]
    k = 0
    while k < len(order):                  # Kahn — 큐 대신 인덱스 순회(결정론·ids 순서 안정)
        cur = order[k]
        k += 1
        for nxt in succs[cur]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                order.append(nxt)
    if len(order) != len(ids):
        raise TopologyLayoutError("간선 위상 정렬 불가(순환) — 간선 방향 점검")
    layer = {}
    for cur in order:
        layer[cur] = max((layer[p] + 1 for p in preds[cur]), default=0)
    return layer


def _ink_ok(ops, width: float, height: float) -> None:
    for o in ops:
        if isinstance(o, RectOp):
            s = o.stroke_w / 2
            if (o.x - s < -0.001 or o.x + o.w + s > width + 0.001
                    or o.y - s < -0.001 or o.y + o.h + s > height + 0.001):
                raise TopologyLayoutError(
                    f"잉크 bbox 프레임 이탈: rect({o.x:.1f},{o.y:.1f},{o.w:.1f},{o.h:.1f})")
        elif isinstance(o, ArrowOp):
            if (min(o.x1, o.x2) < -0.001 or max(o.x1, o.x2) > width + 0.001
                    or min(o.y1, o.y2) < -0.001 or max(o.y1, o.y2) > height + 0.001):
                raise TopologyLayoutError(
                    f"잉크 bbox 프레임 이탈: arrow({o.x1:.1f},{o.y1:.1f}→{o.x2:.1f},{o.y2:.1f})")
        elif isinstance(o, TextOp):
            hw = (o.max_w or 60.0) / 2
            if o.x - hw < -0.001 or o.x + hw > width + 0.001:
                raise TopologyLayoutError(
                    f"잉크 bbox 프레임 이탈: text({o.field}) x={o.x:.1f} max_w={o.max_w:.1f}")
