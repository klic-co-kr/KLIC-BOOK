#!/usr/bin/env python3
"""SKILL.state 책 차트 생성기 (개정2 — 범례 하단 이동·후광·여백 보정).

arXiv:2608.26263 표 1·2·4·5·7·8·9·11의 실측치만 사용해 SVG 차트를 만든다.
임의 값은 하나도 없다 — 아래 DATA 상수가 논문 표의 전사이고, 스크립트는
좌표 계산만 한다. 빌드 파이프라인이 resvg로 4배 래스터화해 책에 넣는다.

실행: python3 references/make_charts.py  (책 디렉터리에서)
출력: assets/images/fig-*.svg
"""
import math
from pathlib import Path

# ── 논문 표 전사 (arXiv:2608.26263) ──────────────────────────────────
# 표 1 · 창고 장기 지평 (Gemini-3-Flash): T → 런타임 → (정확도, 평균프롬프트, 총토큰)
T1 = {
    10:  {"react": (0.90, 3249, 9438),    "memory": (1.00, 3300, 9972),
          "stateful": (1.00, 3430, 10337), "skill": (1.00, 1775, 5870)},
    25:  {"react": (0.92, 6052, 42689),   "memory": (0.99, 6357, 43067),
          "stateful": (1.00, 5858, 41238), "skill": (1.00, 1736, 14714)},
    50:  {"react": (0.88, 11931, 171658), "memory": (0.93, 7582, 131455),
          "stateful": (0.94, 11594, 170992), "skill": (0.96, 1773, 30151)},
    100: {"react": (0.84, 36362, 1245413), "memory": (0.87, 29607, 1082154),
          "stateful": (0.91, 31354, 1062387), "skill": (0.94, 1905, 65408)},
    200: {"react": (0.74, 48007, 2608755), "memory": (0.84, 84364, 6175509),
          "stateful": (0.88, 72305, 5041164), "skill": (0.94, 1811, 122384)},
}
# 표 2 · 창고 노이즈 강건성 (T=50): 노이즈 → 런타임 → 점수
T2 = {
    5:  {"react": 0.68, "memory": 1.00, "stateful": 1.00, "skill": 1.00},
    20: {"react": 0.61, "memory": 1.00, "stateful": 0.98, "skill": 0.97},
    50: {"react": 0.53, "memory": 0.96, "stateful": 0.98, "skill": 0.98},
}
# 표 9 · 저장소 노이즈 강건성 (T=50)
T9 = {
    0:  {"react": 0.76, "memory": 0.85, "stateful": 0.88, "skill": 0.90},
    5:  {"react": 0.62, "memory": 0.85, "stateful": 0.86, "skill": 0.88},
    20: {"react": 0.48, "memory": 0.83, "stateful": 0.85, "skill": 0.86},
    50: {"react": 0.11, "memory": 0.74, "stateful": 0.78, "skill": 0.80},
}
# 표 5 · 예산 매칭 대조 (창고 T=100): 구성 → (점수, 평균프롬프트, 총토큰)
T5 = [
    ("ReAct 전체",  0.84, 36362, 1245413),
    ("슬라이딩 윈도", 0.18,  1800,   62100),
    ("요약 상한",   0.52,  1840,   63400),
    ("LLMLingua",   0.22,  1810,   62350),
    ("SKILL.state", 0.94,  1905,   65408),
]
# 표 11 · 예산 매칭 다중 지평: T → [ReAct전체, 요약상한, 슬라이딩, LLMLingua, SKILL.state]
T11 = {
    10:  [1.00, 0.92, 0.90, 0.88, 0.90],
    25:  [1.00, 0.76, 0.62, 0.60, 0.92],
    50:  [0.96, 0.64, 0.35, 0.38, 0.88],
    100: [0.94, 0.52, 0.18, 0.22, 0.84],
}
# 표 4 · 공개 벤치마크 (Gemini-3-Flash): 패스율%
T4 = {
    "CTF (100과제)":  {"react": 43.2, "memory": 46.4, "stateful": 41.8, "skill": 54.2},
    "τ-Bench 리테일": {"react": 48.2, "memory": 29.9, "stateful": 51.7, "skill": 58.3},
    "τ-Bench 항공":   {"react": 21.8, "memory": 23.6, "stateful": 28.1, "skill": 32.4},
}
# 표 7·8 · 소형 모델 창고 스케일링 점수
T7 = {  # Gemma-4-31B
    10:  {"react": 0.90, "memory": 0.85, "stateful": 0.90, "skill": 0.98},
    25:  {"react": 0.64, "memory": 0.72, "stateful": 0.76, "skill": 0.84},
    50:  {"react": 0.31, "memory": 0.41, "stateful": 0.55, "skill": 0.68},
    100: {"react": 0.21, "memory": 0.24, "stateful": 0.42, "skill": 0.42},
}
T8 = {  # Qwen-3-8B
    10:  {"react": 0.84, "memory": 0.80, "stateful": 0.84, "skill": 0.94},
    25:  {"react": 0.54, "memory": 0.62, "stateful": 0.66, "skill": 0.76},
    50:  {"react": 0.24, "memory": 0.33, "stateful": 0.44, "skill": 0.58},
    100: {"react": 0.15, "memory": 0.18, "stateful": 0.31, "skill": 0.34},
}

# ── 스타일 ───────────────────────────────────────────────────────────
FONT = "NanumSquare_ac, NanumGothic, sans-serif"
INK = "#222222"
GRID = "#dddddd"
TICK = "#888888"
C = {"react": "#b2182b", "memory": "#ef8a62", "stateful": "#7fb3d5", "skill": "#14497a"}
LABEL = {"react": "프롬프트(ReAct)", "memory": "메모리(요약)",
         "stateful": "스테이트풀(LangGraph형)", "skill": "SKILL.state"}
W_SKILL = 3.4
W_BASE = 2.0

# 패널 기하
XF0, XF1, YF0, YF1 = 90, 824, 78, 368

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def text(x, y, s, size=15, fill=INK, anchor="start", weight="normal", halo=False):
    fam = FONT
    halo_attr = (' stroke="#ffffff" stroke-width="4" paint-order="stroke"'
                 ' stroke-linejoin="round"') if halo else ""
    bold = " font-weight='bold'" if weight == "bold" else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}" dominant-baseline="middle"'
            f'{bold}{halo_attr}>{esc(s)}</text>')

def frame(title, sub=None):
    """머리글 — 제목 y26, 부제 y48. 플롯 상단 YF0=78과 여유 확보."""
    ops = [text(16, 26, title, 19, INK, "start", "bold")]
    if sub:
        ops.append(text(16, 48, sub, 13.5, "#555555"))
    return ops

def legend_row(items, y, center_x=None):
    """차트 하단 공용 범례. items: [(색, 라벨, 두께, 파선)]"""
    gap = 34
    widths = [gap + len(lab) * 13.5 * 0.92 + 26 for _, lab, _, _ in items]
    total = sum(widths)
    x = (center_x - total / 2) if center_x else (XF0 + XF1) / 2 - total / 2
    ops = []
    for (col, lab, w, dash), _w in zip(items, widths):
        d = " stroke-dasharray='7,5'" if dash else ""
        ops.append(f'<line x1="{x:.1f}" y1="{y}" x2="{x + 28:.1f}" y2="{y}" '
                   f'stroke="{col}" stroke-width="{w}"{d}/>')
        ops.append(text(x + 34, y, lab, 13.5, INK))
        x += _w
    return ops

def fmt_tok(v):
    if v >= 1_000_000:
        s = f"{v/1_000_000:.2f}".rstrip("0").rstrip(".")
        return f"{s}M"
    if v >= 1000:
        s = f"{v/1000:.1f}".rstrip("0").rstrip(".")
        return f"{s}k"
    return str(v)

def write(name, ops, w=840, h=470):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
           f'width="{w}" height="{h}" style="background:#ffffff">\n'
           + "\n".join(ops) + "\n</svg>\n")
    out = Path(__file__).resolve().parent.parent / "assets" / "images" / name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg, encoding="utf-8")
    print("wrote", out.name)

TS = sorted(T1)
XLOG_T = lambda t: XF0 + (math.log10(t) - 1) / (math.log10(200) - 1) * (XF1 - XF0)

def ygrid(ops, ticks, yf, fmt):
    for xv in ticks:
        y = yf(xv)
        ops.append(f'<line x1="{XF0}" y1="{y:.1f}" x2="{XF1}" y2="{y:.1f}" '
                   f'stroke="{GRID}" stroke-width="1"/>')
        ops.append(text(XF0 - 10, y, fmt(xv), 13.5, TICK, "end"))

def axes(ops):
    ops.append(f'<line x1="{XF0}" y1="{YF0}" x2="{XF0}" y2="{YF1}" stroke="{INK}" stroke-width="1.4"/>')
    ops.append(f'<line x1="{XF0}" y1="{YF1}" x2="{XF1}" y2="{YF1}" stroke="{INK}" stroke-width="1.4"/>')

def xticks_log(ops, xs):
    for t in xs:
        x = XLOG_T(t)
        ops.append(f'<line x1="{x:.1f}" y1="{YF1}" x2="{x:.1f}" y2="{YF1 + 4}" '
                   f'stroke="{GRID}" stroke-width="1" stroke-dasharray="2,3"/>')
        ops.append(text(x, YF1 + 22, str(t), 14, INK, "middle"))

def xticks_lin(ops, xs, xf):
    for t in xs:
        x = xf(t)
        ops.append(f'<line x1="{x:.1f}" y1="{YF1}" x2="{x:.1f}" y2="{YF1 + 4}" '
                   f'stroke="{GRID}" stroke-width="1" stroke-dasharray="2,3"/>')
        ops.append(text(x, YF1 + 22, str(t), 14, INK, "middle"))

def series_lines(ops, xs, xf, yf, key, vals):
    w = W_SKILL if key == "skill" else W_BASE
    pts = " ".join(f"{xf(t):.1f},{yf(v):.1f}" for t, v in zip(xs, vals))
    ops.append(f'<polyline points="{pts}" fill="none" stroke="{C[key]}" '
               f'stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"/>')
    for t, v in zip(xs, vals):
        r = 4.4 if key == "skill" else 3.4
        fill = C[key] if key == "skill" else "#ffffff"
        ops.append(f'<circle cx="{xf(t):.1f}" cy="{yf(v):.1f}" r="{r}" '
                   f'fill="{fill}" stroke="{C[key]}" stroke-width="{w}"/>')

STD_LEGEND = [(C[k], LABEL[k], W_SKILL if k == "skill" else W_BASE, False)
              for k in ("react", "memory", "stateful", "skill")]

# ── 그림 1 · 누적 토큰 (log y) ───────────────────────────────────────
def fig_token_scaling():
    lo, hi = math.log10(5000), math.log10(9_000_000)
    yf = lambda v: YF1 - (math.log10(v) - lo) / (hi - lo) * (YF1 - YF0)
    ops = frame("누적 토큰 소비 — 이차 팽창 대 선형 성장 (로그 축)",
                "창고 환경 · Gemini-3-Flash · 논문 표 1 · 가로축은 실행 지평 T (로그)")
    ygrid(ops, [10_000, 100_000, 1_000_000], yf, fmt_tok)
    xticks_log(ops, TS)
    axes(ops)
    for k in ("react", "memory", "stateful", "skill"):
        series_lines(ops, TS, XLOG_T, yf, k, [T1[t][k][2] for t in TS])
    ops.append(text(XLOG_T(60), yf(20_000), "약 16.2배 차이", 14, "#333333", "middle", "bold", halo=True))
    ops += legend_row(STD_LEGEND, YF1 + 66)
    write("fig-token-scaling.svg", ops)

# ── 그림 2 · 평균 프롬프트 크기 ──────────────────────────────────────
def fig_prompt_flat():
    ymax = 90_000
    yf = lambda v: YF1 - v / ymax * (YF1 - YF0)
    xf = lambda t: XF0 + (t - 10) / 190 * (XF1 - XF0)
    ops = frame("평균 프롬프트 크기 — SKILL.state는 평평하다",
                "턴당 입력 토큰 · 논문 표 1 · SKILL.state는 지평과 무관하게 약 1,700~1,900 토큰")
    ygrid(ops, [0, 20_000, 40_000, 60_000, 80_000], yf, fmt_tok)
    xticks_lin(ops, TS, xf)
    axes(ops)
    for k in ("react", "memory", "stateful", "skill"):
        series_lines(ops, TS, xf, yf, k, [T1[t][k][1] for t in TS])
    ops.append(text(xf(110), yf(62_000), "이력이 입력을 밀어 올린다", 14, "#333333", "middle", "bold", halo=True))
    ops += legend_row(STD_LEGEND, YF1 + 66)
    write("fig-prompt-flat.svg", ops)

# ── 그림 3 · 정확도 ──────────────────────────────────────────────────
def fig_accuracy_scaling():
    yf = lambda v: YF1 - (v - 0.6) / 0.42 * (YF1 - YF0)
    xf = lambda t: XF0 + (t - 10) / 190 * (XF1 - XF0)
    ops = frame("정확도 — 길어져도 무너지지 않는다",
                "창고 환경 · 논문 표 1 · 이력 기반 런타임은 T가 늘수록 하락")
    ygrid(ops, [0.6, 0.7, 0.8, 0.9, 1.0], yf, lambda v: f"{v:.1f}")
    xticks_lin(ops, TS, xf)
    axes(ops)
    for k in ("react", "memory", "stateful", "skill"):
        series_lines(ops, TS, xf, yf, k, [T1[t][k][0] for t in TS])
    ops += legend_row(STD_LEGEND, YF1 + 66)
    write("fig-accuracy-scaling.svg", ops)

# ── 2패널 공용 ───────────────────────────────────────────────────────
def two_panel(data_list, title, sub, fname, ymax=1.0, ylabel_fmt=None):
    """data_list: [(dict, 패널제목)]. 범례는 차트 밑 공용 1줄."""
    ops = frame(title, sub)
    for pi, (data, ptitle) in enumerate(data_list):
        x0 = 90 + pi * 380
        x1 = x0 + 344
        xs = sorted(data)
        # 우측 18pt 안쪽 여백 — 끝점 마커가 패널 가장자리/이웃 눈금 라벨에 닿지 않게
        xf = lambda v, x0=x0, x1=x1, xs=xs: x0 + 8 + (v - xs[0]) / (xs[-1] - xs[0]) * (x1 - x0 - 26)
        yf = lambda v: YF1 - v / ymax * (YF1 - YF0)
        fmt = ylabel_fmt or (lambda v: f"{v:.2f}")
        for gv in (0.0, 0.25, 0.5, 0.75, 1.0):
            if gv > ymax:
                continue
            y = yf(gv)
            ops.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>')
            ops.append(text(x0 - 10, y, fmt(gv), 13, TICK, "end"))
        for v in xs:
            x = xf(v)
            ops.append(f'<line x1="{x:.1f}" y1="{YF1}" x2="{x:.1f}" y2="{YF1 + 4}" '
                       f'stroke="{GRID}" stroke-width="1" stroke-dasharray="2,3"/>')
            ops.append(text(x, YF1 + 20, str(v), 13.5, INK, "middle"))
        ops.append(f'<line x1="{x0}" y1="{YF0}" x2="{x0}" y2="{YF1}" stroke="{INK}" stroke-width="1.4"/>')
        ops.append(f'<line x1="{x0}" y1="{YF1}" x2="{x1}" y2="{YF1}" stroke="{INK}" stroke-width="1.4"/>')
        # 패널 제목 — 축 아래 좌측, x축 라벨과 겹치지 않게 별도 줄
        ops.append(text(x0, YF1 + 44, ptitle, 14.5, INK, "start", "bold"))
        ops.append(text((x0 + x1) / 2, YF1 + 64, "턴당 노이즈 사건 수", 12.5, "#555555", "middle"))
        for k in ("react", "memory", "stateful", "skill"):
            w = W_SKILL if k == "skill" else W_BASE
            pts = " ".join(f"{xf(v):.1f},{yf(data[v][k]):.1f}" for v in xs)
            ops.append(f'<polyline points="{pts}" fill="none" stroke="{C[k]}" '
                       f'stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"/>')
            for v in xs:
                r = 4.2 if k == "skill" else 3.2
                fill = C[k] if k == "skill" else "#ffffff"
                ops.append(f'<circle cx="{xf(v):.1f}" cy="{yf(data[v][k]):.1f}" r="{r}" '
                           f'fill="{fill}" stroke="{C[k]}" stroke-width="{w}"/>')
    ops += legend_row(STD_LEGEND, YF1 + 102, center_x=430)
    write(fname, ops, 860, 520)

def fig_noise():
    two_panel([(T2, "창고 환경"), (T9, "저장소 환경")],
              "노이즈 강건성 — 오염된 관찰을 흘려보내지 않는다",
              "T=50 고정 · 노이즈는 턴당 무관계 사건 수 · 논문 표 2(창고)·표 9(저장소)",
              "fig-noise.svg")

def fig_openweight():
    two_panel([(T7, "Gemma-4-31B"), (T8, "Qwen-3-8B")],
              "소형 모델에서도 방향은 같다 — 폭은 크게",
              "창고 환경 점수 · 논문 표 7(Gemma-4-31B)·표 8(Qwen-3-8B) · 가로축은 실행 지평 T",
              "fig-openweight.svg",
              ylabel_fmt=lambda v: f"{v:.1f}")

# ── 그림 5 · 예산 매칭 막대 ──────────────────────────────────────────
def fig_budget_bars():
    ops = frame("같은 예산, 다른 결말 — 예산 매칭 대조 (창고 T=100)",
                "모든 압축 구성을 SKILL.state 예산(약 1,800 토큰)에 맞춰도 점수는 갈린다 · 논문 표 5")
    n = len(T5)
    x0, x1 = 90, 824
    slot = (x1 - x0 - 40) / n
    bw = slot * 0.58
    yf = lambda v: YF1 - v / 1.0 * (YF1 - YF0)
    for gv in (0.0, 0.25, 0.5, 0.75, 1.0):
        y = yf(gv)
        ops.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>')
        ops.append(text(x0 - 10, y, f"{gv:.2f}", 13.5, TICK, "end"))
    ops.append(f'<line x1="{x0}" y1="{YF0}" x2="{x0}" y2="{YF1}" stroke="{INK}" stroke-width="1.4"/>')
    ops.append(f'<line x1="{x0}" y1="{YF1}" x2="{x1}" y2="{YF1}" stroke="{INK}" stroke-width="1.4"/>')
    for i, (name, score, prompt, tokens) in enumerate(T5):
        cx = x0 + 20 + slot * i + slot / 2
        bx = cx - bw / 2
        col = C["skill"] if "SKILL" in name else "#c9c9c9"
        ops.append(f'<rect x="{bx:.1f}" y="{yf(score):.1f}" width="{bw:.1f}" '
                   f'height="{YF1 - yf(score):.1f}" fill="{col}" stroke="{INK}" stroke-width="0.8" rx="2"/>')
        ops.append(text(cx, yf(score) - 15, f"{score:.2f}", 16, INK, "middle", "bold", halo=True))
        lines = name.split()
        for j, ln in enumerate(lines):
            ops.append(text(cx, YF1 + 22 + j * 18, ln, 13.5, INK, "middle"))
        # 캡션은 이름 줄 수와 무관하게 공통 베이스라인(2줄 기준)에 둔다
        ops.append(text(cx, YF1 + 22 + 2 * 18 + 8,
                        f"평균 {fmt_tok(prompt)} · 총 {fmt_tok(tokens)}", 12.5, "#666666", "middle"))
    write("fig-budget-bars.svg", ops, 840, 470)

# ── 그림 6 · 예산 매칭 다중 지평 ─────────────────────────────────────
def fig_budget_scaling():
    cols = {"skill": C["skill"], "cap": "#8c6d31", "trunc": C["react"],
            "lingua": "#7f7f7f", "full": "#4a9858"}
    labs = {"skill": "SKILL.state", "cap": "요약 상한", "trunc": "슬라이딩 윈도",
            "lingua": "LLMLingua", "full": "ReAct 전체"}
    idx = {"full": 0, "cap": 1, "trunc": 2, "lingua": 3, "skill": 4}
    ops = frame("지평이 길어질수록 벌어지는 격차 — 예산 매칭 스케일링",
                "창고 · Gemini-3-Flash · 논문 표 11 · 점수")
    xs = sorted(T11)
    xf = lambda t: XF0 + (math.log10(t) - 1) / 2 * (XF1 - XF0)
    yf = lambda v: YF1 - (v - 0.1) / 0.95 * (YF1 - YF0)
    ygrid(ops, [0.2, 0.4, 0.6, 0.8, 1.0], yf, lambda v: f"{v:.1f}")
    xticks_log(ops, xs)
    axes(ops)
    for k in ("full", "cap", "trunc", "lingua", "skill"):
        w = W_SKILL if k == "skill" else W_BASE
        dash = " stroke-dasharray='7,5'" if k == "full" else ""
        pts = " ".join(f"{xf(t):.1f},{yf(T11[t][idx[k]]):.1f}" for t in xs)
        ops.append(f'<polyline points="{pts}" fill="none" stroke="{cols[k]}" '
                   f'stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"' + dash + "/>")
        for t in xs:
            r = 4.4 if k == "skill" else 3.4
            fill = cols[k] if k == "skill" else "#ffffff"
            ops.append(f'<circle cx="{xf(t):.1f}" cy="{yf(T11[t][idx[k]]):.1f}" r="{r}" '
                       f'fill="{fill}" stroke="{cols[k]}" stroke-width="{w}"/>')
    ops += legend_row([(cols[k], labs[k], W_SKILL if k == "skill" else W_BASE, k == "full")
                       for k in ("full", "cap", "trunc", "lingua", "skill")], YF1 + 66)
    write("fig-budget-scaling.svg", ops)

# ── 그림 7 · 공개 벤치마크 ───────────────────────────────────────────
def fig_public_bench():
    ops = frame("실전 벤치마크 패스율 — 세 경기 전판 승리",
                "Gemini-3-Flash · 논문 표 4 · InterCode CTF는 pass@1, τ-Bench는 공식 채점기 기준")
    keys = ["react", "memory", "stateful", "skill"]
    labs = ["프롬프트(ReAct)", "메모리(요약)", "스테이트풀", "SKILL.state"]
    groups = list(T4.keys())
    x0, x1 = 90, 824
    gw = (x1 - x0 - 60) / len(groups)
    bw = gw * 0.19
    ymax = 66.0
    yf = lambda v: YF1 - v / ymax * (YF1 - YF0)
    for gv in (0, 20, 40, 60):
        y = yf(gv)
        ops.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>')
        ops.append(text(x0 - 10, y, f"{gv}%", 13.5, TICK, "end"))
    ops.append(f'<line x1="{x0}" y1="{YF0}" x2="{x0}" y2="{YF1}" stroke="{INK}" stroke-width="1.4"/>')
    ops.append(f'<line x1="{x0}" y1="{YF1}" x2="{x1}" y2="{YF1}" stroke="{INK}" stroke-width="1.4"/>')
    for gi, g in enumerate(groups):
        gcx = x0 + 30 + gw * gi + gw / 2
        for ki, k in enumerate(keys):
            v = T4[g][k]
            bx = gcx - (bw * len(keys) + 6 * (len(keys) - 1)) / 2 + ki * (bw + 6)
            col = C[k] if k == "skill" else "#b8b8b8"
            ops.append(f'<rect x="{bx:.1f}" y="{yf(v):.1f}" width="{bw:.1f}" '
                       f'height="{YF1 - yf(v):.1f}" fill="{col}" stroke="{INK}" stroke-width="0.8" rx="2"/>')
            ops.append(text(bx + bw / 2, yf(v) - 12, f"{v:.1f}", 12.5, INK, "middle",
                            "bold" if k == "skill" else "normal", halo=True))
        ops.append(text(gcx, YF1 + 24, g, 14.5, INK, "middle", "bold"))
    ops += legend_row([("#b8b8b8" if k != "skill" else C[k], lab, 0, False)
                       for k, lab in zip(keys[:3], labs[:3])]
                      + [(C["skill"], "SKILL.state", 0, False)], YF1 + 62)
    # 범례 견본은 막대 모양으로
    ops = [o.replace('stroke-width="0.0"', 'stroke-width="0"') for o in ops]
    write("fig-public-bench.svg", ops, 840, 462)

if __name__ == "__main__":
    fig_token_scaling()
    fig_prompt_flat()
    fig_accuracy_scaling()
    fig_noise()
    fig_budget_bars()
    fig_budget_scaling()
    fig_public_bench()
    fig_openweight()
