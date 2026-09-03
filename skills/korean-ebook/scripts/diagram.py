#!/usr/bin/env python3
"""선언적 SVG 다이어그램 엔진 (korean-ebook).

인포그래픽(상자+문장 재배열)과 정량 차트(금지) 사이의 빈 자리 —
구조를 전달하는 벡터 도식을 챕터 md의 ```diagram 펜스(JSON)로 선언적으로
그린다. 좌표는 엔진이 계산하고, 저자는 노드·간선·레인만 쓴다.

레이아웃:
  flow     세로 플로우차트 — 상자·게이트(다이아)·측면 루프
  cycle    원형 순환 — 중앙 라벨 + 3~8 노드
  timeline 가로 타임라인 — 2~3개 레인, 사건·구간
  scene    자유 배치 — 노드 좌표 직접 지정(탈출구)
  stack    성장 스택 — 열마다 층이 쌓이는 누적 비교

빌드 통합: build.py가 펜스를 감지해 SVG를 에셋으로 내고 이미지
마크다운으로 치환한다(기존 이미지 파이프라인·resvg 재사용).

단독 검사: python3 scripts/diagram.py lint <chapter.md>
         python3 scripts/diagram.py render <chapter.md> --out /tmp
"""
import json
import re
import sys
from pathlib import Path

FONT = "NanumSquare_ac, NanumGothic, sans-serif"
INK = "#222222"
MUTE = "#666666"
BLUE = "#14497a"
LBLUE = "#e8eff6"
RED = "#b2182b"
LRED = "#f7e8e8"
GREEN = "#3a7d44"
LGREEN = "#e9f2ea"
GRAY = "#8a8a8a"
LGRAY = "#efefef"
AMBER = "#8c6d31"
LAMBER = "#f5eede"

FENCE_RE = re.compile(r'^```diagram[ \t]*\n(.*?)^```[ \t]*$', re.S | re.M)

# ── SVG 프리미티브 ───────────────────────────────────────────────────
def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def T(x, y, s, size=14, fill=INK, anchor="start", weight="normal", halo=False):
    h = ' stroke="#ffffff" stroke-width="4" paint-order="stroke" stroke-linejoin="round"' if halo else ""
    w = " font-weight='bold'" if weight == "bold" else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}" dominant-baseline="middle"{w}{h}>{_esc(s)}</text>')

def R(x, y, w, h, fill="none", stroke=INK, sw=1.5, rx=6, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

def L(x1, y1, x2, y2, stroke=INK, sw=1.7, dash=None, marker="ah"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    m = f' marker-end="url(#{marker})"' if marker else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{sw}"{d}{m}/>')

def P(d, stroke=INK, sw=1.7, fill="none", marker=None, dash=None):
    m = f' marker-end="url(#{marker})"' if marker else ""
    dd = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dd}{m}/>'

def C(x, y, r, fill, stroke=INK, sw=1.5):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'

_HEAD = ('<defs>'
         '<marker id="ah" markerWidth="11" markerHeight="8" refX="10" refY="4" '
         'orient="auto"><polygon points="0 0, 11 4, 0 8" fill="#222222"/></marker>'
         '<marker id="ah-blue" markerWidth="11" markerHeight="8" refX="10" refY="4" '
         'orient="auto"><polygon points="0 0, 11 4, 0 8" fill="#14497a"/></marker>'
         '<marker id="ah-red" markerWidth="11" markerHeight="8" refX="10" refY="4" '
         'orient="auto"><polygon points="0 0, 11 4, 0 8" fill="#b2182b"/></marker>'
         '<marker id="ah-gray" markerWidth="11" markerHeight="8" refX="10" refY="4" '
         'orient="auto"><polygon points="0 0, 11 4, 0 8" fill="#8a8a8a"/></marker>'
         '</defs>')

# 인쇄 축척 — 판면 대비 설계폭 840px이면 12px 라벨이 약 6.6pt로 인쇄돼
# 하우스 최소(8.5pt)를 깬다. width 속성만 600으로(축척 0.775, 11px→8.5pt,
# 선굵기 비례). viewBox·좌표 불변 — 책별 생성기와 동일 계약.
_PRINT_W = 600

def _svg(ops, w, h):
    ph = round(h * _PRINT_W / w)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{_PRINT_W}" height="{ph}" style="background:#ffffff">\n{_HEAD}\n'
            + "\n".join(ops) + "\n</svg>\n")

def _title(ops, title, sub=None):
    ops.append(T(16, 26, title, 19, INK, "start", "bold"))
    if sub:
        ops.append(T(16, 48, sub, 13.5, "#555555"))

# ── 검증 ─────────────────────────────────────────────────────────────
def _need(d, keys):
    for k in keys:
        if k not in d:
            raise ValueError(f"필수 키 없음: {k}")

def lint_fence(fence: dict):
    """펜스 스키마 검증 — 위반 시 ValueError."""
    _need(fence, ["layout", "title"])
    lay = fence["layout"]
    if lay not in ("flow", "cycle", "timeline", "scene", "stack"):
        raise ValueError(f"알 수 없는 layout: {lay}")
    if len(fence["title"]) > 40:
        raise ValueError("title 40자 초과 — 도식 제목은 결론형 명제로 짧게")
    if lay == "flow":
        nodes = fence.get("nodes", [])
        if not 2 <= len(nodes) <= 8:
            raise ValueError("flow 노드 2~8개")
        ids = set()
        for n in nodes:
            _need(n, ["id", "label"])
            if n["id"] in ids:
                raise ValueError(f"노드 id 중복: {n['id']}")
            ids.add(n["id"])
            if n.get("kind") not in (None, "box", "gate", "note"):
                raise ValueError(f"노드 kind 오류: {n.get('kind')}")
            if len(n["label"]) > 34:
                raise ValueError(f"노드 라벨 34자 초과: {n['id']}")
        for e in fence.get("edges", []):
            _need(e, ["from", "to"])
            if e["from"] not in ids or e["to"] not in ids:
                raise ValueError(f"간선이 없는 노드 참조: {e['from']}->{e['to']}")
    elif lay == "cycle":
        nodes = fence.get("nodes", [])
        if not 3 <= len(nodes) <= 8:
            raise ValueError("cycle 노드 3~8개")
        for n in nodes:
            _need(n, ["label"])
            if len(n["label"]) > 12:
                raise ValueError(f"cycle 라벨 12자 초과: {n['label']}")
    elif lay == "timeline":
        lanes = fence.get("lanes", [])
        if not 2 <= len(lanes) <= 3:
            raise ValueError("timeline 레인 2~3개")
        for ln in lanes:
            _need(ln, ["name", "events"])
            if len(ln["name"]) > 12:
                raise ValueError(f"레인 이름 12자 초과: {ln['name']}")
            if not 1 <= len(ln["events"]) <= 8:
                raise ValueError("레인 사건 1~8개")
    elif lay == "scene":
        nodes = fence.get("nodes", [])
        if not 2 <= len(nodes) <= 12:
            raise ValueError("scene 노드 2~12개")
        ids = set()
        for n in nodes:
            _need(n, ["id", "label", "x", "y", "w", "h"])
            for k in ("x", "y", "w", "h"):
                if not isinstance(n[k], (int, float)) or n[k] < 0:
                    raise ValueError(f"scene 좌표는 0 이상 숫자: {n['id']}.{k}")
            if n["id"] in ids:
                raise ValueError(f"노드 id 중복: {n['id']}")
            ids.add(n["id"])
            if len(n["label"]) > 24:
                raise ValueError(f"scene 라벨 24자 초과: {n['id']}")
        for e in fence.get("edges", []):
            _need(e, ["from", "to"])
            if e["from"] not in ids or e["to"] not in ids:
                raise ValueError(f"간선이 없는 노드 참조: {e['from']}->{e['to']}")
    elif lay == "stack":
        cols = fence.get("cols", [])
        if not 2 <= len(cols) <= 6:
            raise ValueError("stack 열 2~6개")
        for c in cols:
            _need(c, ["label", "layers"])
            if not 1 <= c["layers"] <= 12:
                raise ValueError(f"stack layers 1~12: {c['label']}")

# ── 렌더 ─────────────────────────────────────────────────────────────
FILLS = {"blue": (LBLUE, BLUE), "green": (LGREEN, GREEN), "red": (LRED, RED),
         "gray": (LGRAY, GRAY), "amber": (LAMBER, AMBER)}

def _fill_pair(tonne):
    return FILLS.get(tonne, ("#ffffff", INK))

def _render_flow(f):
    nodes = f["nodes"]
    edges = f.get("edges", [])
    w = 840
    cx = 400
    top = 84
    row_h = 76
    h = top + len(nodes) * row_h + 46
    ops = []
    _title(ops, f["title"], f.get("sub"))
    pos = {}
    for i, n in enumerate(nodes):
        y = top + i * row_h
        pos[n["id"]] = (cx, y)
        fill, st = _fill_pair(n.get("tone", ""))
        kind = n.get("kind", "box")
        if kind == "gate":
            ops.append(P(f"M {cx} {y-34} l 78 22 l -78 22 l -78 -22 z", fill, st, 1.8))
            ops.append(T(cx, y, n["label"], 13, st, "middle", "bold"))
        elif kind == "note":
            ops.append(R(cx - 170, y - 18, 340, 36, fill, st, 1.3, 6, dash="5,3"))
            ops.append(T(cx, y, n["label"], 12.5, MUTE, "middle"))
        else:
            ops.append(R(cx - 170, y - 22, 340, 44, fill, st, 1.7, 6))
            ops.append(T(cx, y, n["label"], 14, INK, "middle", "bold"))
    for e in edges:
        a, b = pos[e["from"]], pos[e["to"]]
        col = {"ok": GREEN, "fail": RED, "back": GRAY}.get(e.get("kind", ""), INK)
        mk = {"ok": "ah-blue", "fail": "ah-red", "back": "ah-gray"}.get(e.get("kind", ""), "ah")
        dash = "5,4" if e.get("kind") in ("fail", "back") else None
        if e.get("side") == "left":
            ops.append(P(f"M {a[0]-170} {a[1]} L 90 {a[1]} L 90 {b[1]} L {b[0]-176} {b[1]}",
                         col, 1.6, marker=mk, dash=dash))
        elif e.get("side") == "right":
            ops.append(P(f"M {a[0]+170} {a[1]} L 750 {a[1]} L 750 {b[1]} L {b[0]+176} {b[1]}",
                         col, 1.6, marker=mk, dash=dash))
        else:
            ops.append(L(a[0], a[1] + 24, b[0], b[1] - 26, col, 1.7, dash, mk))
        if e.get("label"):
            lx = cx + 200 if e.get("side") != "left" else cx - 200
            ops.append(T(lx, (a[1] + b[1]) / 2, e["label"], 12, col, "middle", "bold", halo=True))
    return _svg(ops, w, h)

def _render_cycle(f):
    import math
    nodes = f["nodes"]
    n = len(nodes)
    w = 840
    h = 430
    cx, cy, r = 420, 235, 128
    ops = []
    _title(ops, f["title"], f.get("sub"))
    fill, st = _fill_pair(f.get("tone", "blue"))
    ops.append(C(cx, cy, 62, fill, st, 1.8))
    ops.append(T(cx, cy, f.get("center", ""), 14, st, "middle", "bold"))
    poss = []
    for i, nd in enumerate(nodes):
        ang = -math.pi / 2 + 2 * math.pi * i / n
        x, y = cx + (r + 14) * math.cos(ang), cy + (r + 14) * math.sin(ang)
        poss.append((x, y))
        nf, ns = _fill_pair(nd.get("tone", ""))
        ops.append(R(x - 56, y - 19, 112, 38, nf, ns, 1.6, 6))
        ops.append(T(x, y, nd["label"], 13, INK, "middle", "bold"))
    half = math.atan(64 / (r + 14)) + 0.10
    for i in range(n):
        a1 = -math.pi / 2 + 2 * math.pi * i / n + half
        a2 = -math.pi / 2 + 2 * math.pi * (i + 1) / n - half
        p1 = (cx + (r + 6) * math.cos(a1), cy + (r + 6) * math.sin(a1))
        p2 = (cx + (r + 6) * math.cos(a2), cy + (r + 6) * math.sin(a2))
        ops.append(P(f"M {p1[0]:.1f} {p1[1]:.1f} A {r+6} {r+6} 0 0 1 {p2[0]:.1f} {p2[1]:.1f}",
                     INK, 1.8, marker="ah"))
    return _svg(ops, w, h)

def _render_timeline(f):
    lanes = f["lanes"]
    w = 840
    h = 120 + len(lanes) * 110 + 40
    x0, x1 = 150, 780
    ops = []
    _title(ops, f["title"], f.get("sub"))
    tones = {"blue": BLUE, "red": RED, "green": GREEN, "amber": AMBER, "gray": GRAY}
    for li, lane in enumerate(lanes):
        y = 130 + li * 110
        col = tones.get(lane.get("tone", ""), INK)
        lfill, lst = _fill_pair(lane.get("tone", ""))
        ops.append(T(x0 - 20, y, lane["name"], 14, col, "end", "bold"))
        ops.append(L(x0, y, x1, y, "#cccccc", 2))
        evs = lane["events"]
        for i, ev in enumerate(evs):
            x = x0 + i * (x1 - x0) / (len(evs) - 1 if len(evs) > 1 else 1)
            big = ev.get("major", False)
            ops.append(C(x, y, 9 if big else 5.5, lfill if big else "#ffffff", col, 2 if big else 1.8))
            ops.append(T(x, y - 26 if i % 2 == 0 else y + 30, ev["label"],
                         12.5, col if big else MUTE, "middle",
                         "bold" if big else "normal"))
        for sp in lane.get("spans", []):
            i, j = sp["from"], sp["to"]
            xa = x0 + i * (x1 - x0) / (len(evs) - 1 if len(evs) > 1 else 1)
            xb = x0 + j * (x1 - x0) / (len(evs) - 1 if len(evs) > 1 else 1)
            sc = tones.get(sp.get("tone", "red"), RED)
            sf, _ = _fill_pair(sp.get("tone", "red"))
            ops.append(R(xa - 10, y - 20, xb - xa + 20, 40, sf, sc, 1.3, 8))
            if sp.get("label"):
                ops.append(T((xa + xb) / 2, y - 34, sp["label"], 12.5, sc, "middle", "bold"))
    ops.append(T((x0 + x1) / 2, h - 18, f.get("axis", ""), 12.5, MUTE, "middle"))
    return _svg(ops, w, h)

def _render_scene(f):
    nodes = f["nodes"]
    edges = f.get("edges", [])
    w = f.get("width", 840)
    h = f.get("height", 420)
    ops = []
    _title(ops, f["title"], f.get("sub"))
    pos = {}
    for n in nodes:
        x, y, nw, nh = n["x"], n["y"], n["w"], n["h"]
        pos[n["id"]] = (x + nw / 2, y + nh / 2, x, y, nw, nh)
        fill, st = _fill_pair(n.get("tone", ""))
        ops.append(R(x, y, nw, nh, fill, st, 1.7, 6, n.get("dash")))
        ops.append(T(x + nw / 2, y + nh / 2, n["label"], n.get("size", 14),
                     INK, "middle", "bold"))
        if n.get("sub"):
            ops.append(T(x + nw / 2, y + nh / 2 + 20, n["sub"], 11.5, MUTE, "middle"))
    for e in edges:
        ax, ay, _, _, _, _ = pos[e["from"]]
        bx, by, _, _, _, _ = pos[e["to"]]
        col = {"ok": GREEN, "fail": RED, "back": GRAY}.get(e.get("kind", ""), INK)
        mk = {"ok": "ah-blue", "fail": "ah-red", "back": "ah-gray"}.get(e.get("kind", ""), "ah")
        ops.append(P(f"M {ax:.1f} {ay:.1f} L {bx:.1f} {by:.1f}", col, 1.7,
                     marker=mk, dash=e.get("dash")))
        if e.get("label"):
            ops.append(T((ax + bx) / 2, (ay + by) / 2 - 12, e["label"], 11.5, col,
                         "middle", "bold", halo=True))
    return _svg(ops, w, h)

def _render_stack(f):
    cols = f["cols"]
    w = 840
    top, base = 96, 360
    h = 400
    ops = []
    _title(ops, f["title"], f.get("sub"))
    xw = (780 - 40 - (len(cols) - 1) * 24) / len(cols)
    palette = [(LBLUE, BLUE), (LGRAY, GRAY), (LRED, RED), (LAMBER, AMBER), (LGREEN, GREEN)]
    legend = f.get("legend", [])
    for i, c in enumerate(cols):
        x = 40 + i * (xw + 24)
        ops.append(R(x, top, xw, base - top, "#ffffff", INK, 1.6, 6))
        bh, gap = 14, 2.5
        for k in range(c["layers"]):
            lf, ls = palette[k % len(palette)]
            y = base - 10 - (k + 1) * (bh + gap) + gap
            ops.append(R(x + 8, y, xw - 16, bh, lf, ls, 0.9, 3))
        ops.append(T(x + xw / 2, base + 24, c["label"], 14, INK, "middle", "bold"))
    lx = 44
    for k, lab in enumerate(legend[:5]):
        lf, ls = palette[k % len(palette)]
        ops.append(R(lx, 62, 26, 13, lf, ls, 0.9, 3))
        ops.append(T(lx + 33, 68, lab, 13, INK))
        lx += 33 + len(lab) * 13 * 1.05 + 26
    return _svg(ops, w, h)

RENDERERS = {"flow": _render_flow, "cycle": _render_cycle,
             "timeline": _render_timeline, "scene": _render_scene,
             "stack": _render_stack}

def render_fence(fence: dict) -> str:
    lint_fence(fence)
    return RENDERERS[fence["layout"]](fence)

def extract(text: str):
    """(치환된 md, [(펜스 dict, 원본 match)]) 반환."""
    out = []
    def repl(m):
        out.append((json.loads(m.group(1)), m.group(0)))
        return m.group(0)
    text2 = FENCE_RE.sub(repl, text)
    return text2, out

# ── CLI ──────────────────────────────────────────────────────────────
def main(argv):
    if len(argv) < 2 or argv[0] not in ("lint", "render"):
        print(__doc__)
        return 2
    md = Path(argv[1]).read_text(encoding="utf-8")
    _, fences = extract(md)
    if not fences:
        print("diagram 펜스 없음")
        return 0
    if argv[0] == "lint":
        for i, (f, raw) in enumerate(fences, 1):
            try:
                lint_fence(f)
                print(f"fig {i}: OK ({f['layout']})")
            except ValueError as e:
                print(f"fig {i}: 위반 — {e}")
                return 1
        return 0
    outdir = Path(argv[3]) if len(argv) > 3 and argv[2] == "--out" else Path("/tmp")
    outdir.mkdir(parents=True, exist_ok=True)
    src = Path(argv[1]).stem
    for i, (f, _) in enumerate(fences, 1):
        (outdir / f"{src}-dg{i:02d}.svg").write_text(render_fence(f), encoding="utf-8")
        print("wrote", (outdir / f"{src}-dg{i:02d}.svg"))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
