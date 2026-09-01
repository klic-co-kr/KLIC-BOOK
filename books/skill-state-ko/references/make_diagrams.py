#!/usr/bin/env python3
"""skill-state-ko 구조 다이어그램 생성기.

인포그래픽 펜스(상자+문장 재배열) 대신 장마다 형태가 다른 목적 설계
도식을 그린다 — 아키텍처·플로우차트·타임라인·지형도·루프·우산 등.
구조·화살표·공간 배치로 뜻을 전달하고 문장을 최소화한다. 논문
(arXiv:2608.26263)의 구조와 수치만 사용한다.

실행: python3 references/make_diagrams.py  (책 디렉터리에서)
출력: assets/images/diag-*.svg
"""
from pathlib import Path

FONT = "NanumSquare_ac, NanumGothic, sans-serif"
MONO = "NanumGothicCoding, 'Courier New', monospace"
INK = "#222222"
MUTE = "#666666"
BLUE = "#14497a"      # SKILL.state / 상태 계열
LBLUE = "#e8eff6"
RED = "#b2182b"
LRED = "#f7e8e8"
GREEN = "#3a7d44"
LGREEN = "#e9f2ea"
GRAY = "#8a8a8a"
LGRAY = "#efefef"
AMBER = "#8c6d31"
LAMBER = "#f5eede"

HEAD = ('<defs>'
        '<marker id="ah" markerWidth="11" markerHeight="8" refX="10" refY="4" '
        'orient="auto"><polygon points="0 0, 11 4, 0 8" fill="{INK}"/></marker>'
        '<marker id="ahb" markerWidth="11" markerHeight="8" refX="10" refY="4" '
        'orient="auto"><polygon points="0 0, 11 4, 0 8" fill="{BLUE}"/></marker>'
        '<marker id="ahr" markerWidth="11" markerHeight="8" refX="10" refY="4" '
        'orient="auto"><polygon points="0 0, 11 4, 0 8" fill="{RED}"/></marker>'
        '<marker id="ahg" markerWidth="11" markerHeight="8" refX="10" refY="4" '
        'orient="auto"><polygon points="0 0, 11 4, 0 8" fill="{GRAY}"/></marker>'
        '</defs>').replace("{INK}", INK).replace("{BLUE}", BLUE).replace("{RED}", RED).replace("{GRAY}", GRAY)

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def T(x, y, s, size=14, fill=INK, anchor="start", weight="normal", font=FONT, halo=False, rot=None):
    h = ' stroke="#ffffff" stroke-width="4" paint-order="stroke" stroke-linejoin="round"' if halo else ""
    r = f' transform="rotate({rot} {x} {y})"' if rot is not None else ""
    w = " font-weight='bold'" if weight == "bold" else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}" dominant-baseline="middle"{w}{h}{r}>{esc(s)}</text>')

def R(x, y, w, h, fill="none", stroke=INK, sw=1.4, rx=5, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

def L(x1, y1, x2, y2, stroke=INK, sw=1.6, dash=None, marker=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    m = f' marker-end="url(#{marker})"' if marker else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{sw}"{d}{m}/>')

def P(d, stroke=INK, sw=1.6, fill="none", marker=None, dash=None):
    m = f' marker-end="url(#{marker})"' if marker else ""
    dd = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dd}{m}/>'

def C(x, y, r, fill, stroke=INK, sw=1.4):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'

def title(ops, s, sub=None):
    ops.append(T(16, 26, s, 19, INK, "start", "bold"))
    if sub:
        ops.append(T(16, 48, sub, 13.5, "#555555"))

def write(name, ops, w=840, h=420):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
           f'width="{w}" height="{h}" style="background:#ffffff">\n{HEAD}\n'
           + "\n".join(ops) + "\n</svg>\n")
    out = Path(__file__).resolve().parent.parent / "assets" / "images" / name
    out.write_text(svg, encoding="utf-8")
    print("wrote", out.name)

# ── 그림 1-1 · 이력 누적 — 매 턴 입력이 자란다 ───────────────────────
def diag_growth():
    ops = []
    title(ops, "한 걸음마다 전부를 다시 읽는다 — 이력의 누적",
          "대화형 런타임: 매 턴의 관찰·추론·행동이 입력에 남는다 · 턴 t의 프롬프트")
    cols = [("턴 1", 1, 70), ("턴 2", 2, 262), ("턴 3", 3, 454), ("턴 4", 4, 646)]
    xw = 168
    top, base = 96, 360
    layer_lab = ["관찰", "추론", "행동"]
    layer_col = [LBLUE, LGRAY, LRED]
    layer_st = [BLUE, GRAY, RED]
    for label, n, x in cols:
        ops.append(R(x, top, xw, base - top, "#ffffff", INK, 1.6, 6))
        bh = 14
        gap = 2.5
        for i in range(n * 3):
            li = i % 3
            y = base - 10 - (i + 1) * (bh + gap) + gap
            ops.append(R(x + 8, y, xw - 16, bh, layer_col[li], layer_st[li], 0.9, 3))
        ops.append(T(x + xw / 2, base + 24, label, 14.5, INK, "middle", "bold"))
    # 범례
    lx = 116
    for i, lab in enumerate(layer_lab):
        ops.append(R(lx, 62, 26, 13, layer_col[i], layer_st[i], 0.9, 3))
        ops.append(T(lx + 33, 68, lab, 13, INK))
        lx += 33 + len(lab) * 13 * 1.05 + 26
    ops.append(L(646 + xw + 8, top, 646 + xw + 8, base, RED, 2.2, marker="ahr"))
    ops.append(T(646 + xw + 2, 84, "입력이 자란다 →", 14, RED, "end", "bold", halo=True))
    write("diag-growth.svg", ops, 840, 400)

# ── 그림 2-1 · SKILL.state 아키텍처 ─────────────────────────────────
def diag_architecture():
    ops = []
    title(ops, "SKILL.state — 세 개의 입력, 버려지는 추론",
          "입력은 명세·상태·최신 관찰뿐 · 논문 그림 1 재구성")
    # 입력 3 (좌)
    inputs = [("명세 P", "불변 규칙서", LBLUE, BLUE),
              ("상태 Σt", "실행의 장부", LGREEN, GREEN),
              ("관찰 Ot", "최신 소식", LAMBER, AMBER)]
    ys = [110, 220, 330]
    for (hd, sb, fill, st), y in zip(inputs, ys):
        ops.append(R(36, y - 26, 150, 52, fill, st, 1.6, 6))
        ops.append(T(111, y - 8, hd, 15, INK, "middle", "bold"))
        ops.append(T(111, y + 12, sb, 12, MUTE, "middle"))
    # LLM (중앙)
    ops.append(R(300, 170, 150, 110, "#ffffff", INK, 2.2, 8))
    ops.append(T(375, 212, "언어 모델", 17, INK, "middle", "bold"))
    ops.append(T(375, 240, "한 턴의 추론", 12.5, MUTE, "middle"))
    for y in ys:
        ops.append(L(186, y, 298, 225, INK, 1.5, marker="ah"))
    # 산출 3 (우) — R 폐기 / ΔΣ 검증 / a 실행
    # a_t → 환경
    ops.append(R(560, 96, 200, 52, "#ffffff", INK, 1.6, 6))
    ops.append(T(660, 122, "행동 at 실행", 14.5, INK, "middle", "bold"))
    ops.append(L(450, 205, 558, 122, INK, 1.5, marker="ah"))
    # ΔΣ → 검증 → 병합
    ops.append(P("M 450 225 L 505 225 L 505 262 L 540 262", INK, 1.5, marker="ah"))
    ops.append(P("M 590 236 L 590 262 L 626 262", GREEN, 1.8, marker="ahb"))
    dx, dy = 565, 220
    ops.append(P(f"M {dx} {dy} l 25 16 l -25 16 l -25 -16 z", GREEN, 1.8, LGREEN))
    ops.append(T(dx, dy + 17, "검증", 12.5, GREEN, "middle", "bold"))
    ops.append(R(626, 236, 134, 52, LGREEN, GREEN, 1.6, 6))
    ops.append(T(693, 262, "Σt+1 = Σt ⊕ ΔΣt", 14, GREEN, "middle", "bold"))
    # 상태 되먹임 — Σt+1 → 상태 Σt 입력으로
    ops.append(P("M 760 262 L 812 262 L 812 66 L 111 66 L 111 82", GREEN, 1.8, marker="ahb", dash="6,4"))
    ops.append(T(420, 66, "갱신된 상태가 다음 턴의 입력으로", 12.5, GREEN, "middle", "bold", halo=True))
    # R 폐기
    ops.append(R(560, 330, 200, 52, LRED, RED, 1.6, 6))
    ops.append(T(660, 348, "추론 Rt — 산출 즉시 폐기", 13, RED, "middle", "bold"))
    ops.append(L(660, 330, 660, 312, RED, 1.4))
    ops.append(L(648, 318, 672, 326, RED, 2))
    ops.append(L(648, 326, 672, 318, RED, 2))
    ops.append(P("M 450 245 L 505 245 L 505 356 L 558 356", RED, 1.6, marker="ahr", dash="5,4"))
    # 환경 → 관찰 되먹임
    ops.append(P("M 760 122 L 790 122 L 790 410 L 111 410 L 111 358", AMBER, 1.8, marker="ah", dash="6,4"))
    ops.append(T(430, 390, "환경의 다음 관찰이 Ot로 돌아온다", 12.5, AMBER, "middle", "bold", halo=True))
    # 산출 라벨
    ops.append(T(468, 190, "at", 13, INK, "middle"))
    ops.append(T(468, 243, "ΔΣt", 13, INK, "middle"))
    ops.append(T(468, 300, "Rt", 13, RED, "middle"))
    write("diag-architecture.svg", ops, 840, 424)

# ── 그림 3-1 · 한 턴의 플로우차트 — 알고리즘 1 ──────────────────────
def diag_transition():
    ops = []
    title(ops, "한 턴은 검증을 통과해야 상태에 남는다",
          "논문 알고리즘 1의 실행 주기 — 통과·실패·폐기의 세 갈래")
    cx = 430
    steps = [("관찰 Ot 수신", 92), ("프롬프트 구성 (P, Σt, Ot)", 158),
             ("모델 생성 — 추론 Rt · 갱신 ΔΣt · 행동 at", 224)]
    for label, y in steps:
        ops.append(R(cx - 170, y - 22, 340, 44, "#ffffff", INK, 1.6, 6))
        ops.append(T(cx, y, label, 14, INK, "middle", "bold"))
    ops.append(L(cx, 114, cx, 134, INK, 1.6, marker="ah"))
    ops.append(L(cx, 180, cx, 200, INK, 1.6, marker="ah"))
    # 검증 다이아
    dx, dy = cx, 300
    ops.append(P(f"M {dx} {dy-40} l 62 40 l -62 40 l -62 -40 z", BLUE, 1.8, LBLUE))
    ops.append(T(dx, dy, "결정론적", 13, BLUE, "middle", "bold"))
    ops.append(T(dx, dy + 17, "검증", 13, BLUE, "middle", "bold"))
    ops.append(L(cx, 246, cx, 256, INK, 1.6, marker="ah"))
    ops.append(T(cx + 26, 250, "ΔΣt", 12.5, INK, "middle"))
    # 실패 → 롤백 (좌측 루프)
    ops.append(R(96, 278, 130, 44, LRED, RED, 1.5, 6))
    ops.append(T(161, 300, "롤백 · 재시도", 13, RED, "middle", "bold"))
    ops.append(P(f"M {dx-62} {dy} L 226 300", RED, 1.6, marker="ahr"))
    ops.append(T(296, 286, "실패", 12.5, RED, "middle", "bold"))
    ops.append(P("M 161 322 L 161 224 L {x} 224".replace("{x}", str(cx - 170)),
                RED, 1.4, marker="ahr", dash="5,4"))
    # 통과 → 병합 → 실행
    ops.append(R(cx - 170, 386, 340, 44, LGREEN, GREEN, 1.6, 6))
    ops.append(T(cx, 408, "상태 병합  Σt+1 = Σt ⊕ ΔΣt", 14, GREEN, "middle", "bold"))
    ops.append(L(cx, 340, cx, 384, GREEN, 1.8, marker="ahb"))
    ops.append(T(cx + 36, 366, "통과", 12.5, GREEN, "middle", "bold"))
    ops.append(R(cx - 170, 470, 340, 44, "#ffffff", INK, 1.6, 6))
    ops.append(T(cx, 492, "행동 at 실행 → 다음 관찰", 14, INK, "middle", "bold"))
    ops.append(L(cx, 430, cx, 468, INK, 1.6, marker="ah"))
    # 루프백
    ops.append(P(f"M {cx+170} 492 L 800 492 L 800 92 L {cx+172} 92", INK, 1.5, marker="ah", dash="6,4"))
    ops.append(T(648, 84, "다음 턴", 12.5, MUTE, "middle", "bold", halo=True))
    # Rt 폐기함
    ops.append(R(668, 196, 118, 56, LGRAY, GRAY, 1.5, 6, dash="4,3"))
    ops.append(T(727, 216, "Rt 폐기", 13, GRAY, "middle", "bold"))
    ops.append(T(727, 236, "재사용 없음", 11.5, GRAY, "middle"))
    ops.append(P("M 600 224 L 666 224", GRAY, 1.4, marker="ahg", dash="4,3"))
    write("diag-transition.svg", ops, 840, 530)

# ── 그림 4-1 · 제곱은 면적, 선형은 길이 ─────────────────────────────
def diag_quadratic():
    ops = []
    title(ops, "제곱은 면적이고 선형은 길이다",
          "같은 10턴의 실행 — 이력은 10×10 격자를, 상태는 한 줄을 청구한다")
    n, cell = 10, 26
    gx, gy = 120, 92
    for i in range(n):
        for j in range(n):
            ops.append(R(gx + j * cell, gy + i * cell, cell - 2, cell - 2,
                         LRED, "#d8a0a0", 0.7, 2))
    ops.append(T(gx + n * cell / 2, gy - 18, "이력 기반 — O(T²)", 15, RED, "middle", "bold"))
    ops.append(T(gx + n * cell / 2, gy + n * cell + 24, "면적: 첫 관찰이 10번 결제", 12.5, MUTE, "middle"))
    bx = gx + n * cell + 140
    for j in range(n):
        ops.append(R(bx + j * cell, gy + (n - 1) * cell, cell - 2, cell - 2,
                     LBLUE, BLUE, 1.2, 2))
    ops.append(T(bx + n * cell / 2, gy - 18, "상태 기반 — O(T)", 15, BLUE, "middle", "bold"))
    ops.append(T(bx + n * cell / 2, gy + n * cell + 24, "길이: 턴마다 한 번 결제", 12.5, MUTE, "middle"))
    ops.append(L(gx + n * cell + 8, gy + (n - 1) * cell + 12, bx - 12, gy + (n - 1) * cell + 12,
                 GRAY, 1.6, marker="ahg", dash="5,4"))
    write("diag-quadratic.svg", ops, 840, 400)

# ── 그림 5-1 · 두 세계 — 선반 격자 대 관계 그래프 ───────────────────
def diag_worlds():
    ops = []
    title(ops, "두 환경 — 평면의 지구력, 그래프의 파급",
          "창고는 독립 변수의 장기 유지를, 저장소는 얽힌 의존의 구조 추론을 시험한다")
    # 좌: 창고 격자
    gx, gy, cw, chh, cn, rn = 70, 96, 52, 34, 6, 6
    ops.append(T(gx + cn * cw / 2 - 20, 76, "창고 관리 — 500개 선반의 평면", 14.5, INK, "middle", "bold"))
    filled = {(0, 1), (2, 0), (2, 4), (4, 2), (5, 5), (1, 3)}
    for i in range(rn):
        for j in range(cn):
            f = LBLUE if (i, j) in filled else "#ffffff"
            s = BLUE if (i, j) in filled else "#b9c6d2"
            ops.append(R(gx + j * cw, gy + i * chh, cw - 3, chh - 3, f, s, 1.1, 3))
    ops.append(T(gx + cn * cw - 6, gy + rn * chh + 20, "■ 점유 선반 — 서로 얽히지 않는다",
                 12, MUTE, "end"))
    ops.append(P(f"M {gx-8} {gy+40} L {gx-40} {gy+40}", AMBER, 1.6, marker="ah"))
    ops.append(T(gx - 44, gy + 22, "입고·주문·정비", 12, AMBER, "end", "bold", rot=0))
    # 우: 저장소 그래프
    nodes = {"master": (560, 320), "bA": (500, 130), "bB": (680, 130),
             "pr1": (560, 210), "pr2": (720, 240), "ci": (430, 230)}
    edges = [("bA", "pr1"), ("bA", "ci"), ("pr1", "master"), ("bB", "pr2"),
             ("pr2", "master"), ("ci", "master")]
    for a, b in edges:
        x1, y1 = nodes[a]; x2, y2 = nodes[b]
        ops.append(L(x1, y1, x2, y2, GRAY, 1.4, marker="ahg"))
    label = {"master": ("마스터", LGREEN, GREEN), "bA": ("브랜치 A", LBLUE, BLUE),
             "bB": ("브랜치 B", LBLUE, BLUE), "pr1": ("PR 1", LAMBER, AMBER),
             "pr2": ("PR 2", LAMBER, AMBER), "ci": ("CI", LRED, RED)}
    for k, (x, y) in nodes.items():
        lab, fill, st = label[k]
        ops.append(R(x - 34, y - 15, 68, 30, fill, st, 1.5, 5))
        ops.append(T(x, y, lab, 12.5, INK, "middle", "bold"))
    ops.append(T(610, 76, "소프트웨어 저장소 — 브랜치·PR·CI의 그래프", 14.5, INK, "middle", "bold"))
    ops.append(T(742, 322, "병합 하나가", 13, MUTE, "end"))
    ops.append(T(742, 342, "그래프 전체를 바꾼다", 13, MUTE, "end"))
    write("diag-worlds.svg", ops, 840, 392)

# ── 그림 7-2 · 회복 타임라인 ────────────────────────────────────────
def diag_recovery():
    ops = []
    title(ops, "세계가 바뀐 뒤 — 환각의 길이가 회복력이다",
          "보정 알림 도착(턴 0) 이후 · 논문 표 3·10")
    x0, x1 = 110, 780
    turns = list(range(0, 9))
    def tx(t):
        return x0 + t * (x1 - x0) / 8
    rows = [("이력 기반", 130, RED, LRED, 6, "환각 5~8턴"),
            ("상태 기반", 250, GREEN, LGREEN, 1, "회복 0턴")]
    for name, y, col, fill, halluc, lab in rows:
        ops.append(T(x0 - 16, y, name, 14, col, "end", "bold"))
        ops.append(L(x0, y, x1, y, "#cccccc", 2))
        for t in turns:
            ops.append(C(tx(t), y, 5, "#ffffff", col, 1.8))
        if halluc > 1:
            for t in range(1, 6):
                ops.append(C(tx(t), y, 5, fill, col, 1.4))
            ops.append(R(tx(1) - 14, y - 22, tx(5) - tx(1) + 28, 44, fill, col, 1.2, 8))
            for t in range(1, 6):
                ops.append(C(tx(t), y, 5, fill, col, 1.4))
            ops.append(T((tx(1) + tx(5)) / 2, y - 34, lab, 13.5, col, "middle", "bold"))
            ops.append(T(tx(6), y + 26, "그제야 올바른 행동", 12, MUTE, "middle"))
        else:
            ops.append(C(tx(1), y, 8, fill, col, 2.4))
            ops.append(T(tx(1) + 14, y - 24, lab, 13.5, col, "start", "bold"))
            ops.append(T(tx(1) + 14, y + 26, "다음 행동이 곧 정답", 12, MUTE))
    # 보정 알림
    ops.append(L(x0, 96, x0, 282, AMBER, 2, dash="6,4"))
    ops.append(T(x0 + 8, 92, "보정 알림 도착 — 선반 이동·강제 푸시", 12.5, AMBER, "start", "bold"))
    for t in turns:
        ops.append(T(tx(t), 312, str(t), 12, MUTE, "middle"))
    ops.append(T((x0 + x1) / 2, 336, "턴", 12.5, MUTE, "middle"))
    write("diag-recovery.svg", ops, 840, 356)

# ── 그림 10-1 · 연구 지형도 ─────────────────────────────────────────
def diag_map():
    ops = []
    title(ops, "기술 연구의 지형 — 갈린 네 밭, 비어 있는 다섯째",
          "저자들의 서베이가 그린 지도에서 SKILL.state는 유일한 백지를 팠다")
    plots = [("발견", "필요한 기술 찾기", 70, 100), ("표현", "코드·문서 정형화", 330, 100),
             ("조합", "주체·흐름 조립", 70, 240), ("보안", "위협·방어·평가", 330, 240)]
    for name, sub, x, y in plots:
        ops.append(R(x, y, 220, 110, LGRAY, "#9a9a9a", 1.4, 6))
        for i in range(4):
            ops.append(L(x + 14, y + 30 + i * 20, x + 206, y + 30 + i * 20, "#c9c9c9", 1))
        ops.append(T(x + 110, y + 22, name, 16, INK, "middle", "bold"))
        ops.append(T(x + 110, y + 92, sub, 11.5, MUTE, "middle"))
    # 다섯째 밭 — 백지
    x, y = 590, 100
    ops.append(R(x, y, 220, 110, "#ffffff", BLUE, 2, 6, dash="8,5"))
    ops.append(R(x, y, 220, 110, "#ffffff", "none", 0))
    ops.append(T(x + 110, y + 44, "실행", 20, BLUE, "middle", "bold"))
    ops.append(T(x + 110, y + 78, "골라진 기술을 어떻게", 11.5, BLUE, "middle"))
    ops.append(T(x + 110, y + 94, "돌리는가 — 이 논문", 11.5, BLUE, "middle"))
    ops.append(T(x + 110, 268, "← 네 밭의 수확이 모이는 곳", 12.5, MUTE, "middle"))
    ops.append(L(552, 242, 596, 212, GRAY, 1.5, marker="ahg", dash="4,3"))
    write("diag-map.svg", ops, 840, 356)

# ── 그림 13-1 · DST 순환 루프 ───────────────────────────────────────
def diag_loop():
    ops = []
    title(ops, "상태 추적은 매 턴 장부만 고친다",
          "대화 상태 추적(DST)의 갱신 순환 — 발화가 와도 바뀌는 것은 슬롯뿐이다")
    cx, cy, r = 420, 218, 108
    ops.append(C(cx, cy, 56, LBLUE, BLUE, 1.8))
    ops.append(T(cx, cy - 8, "슬롯 장부", 14.5, BLUE, "middle", "bold"))
    ops.append(T(cx, cy + 14, "날짜 · 도착지 · 인원", 11, MUTE, "middle"))
    nodes = [("발화 청취", cx, cy - r), ("의미 해석", cx + r + 8, cy),
             ("장부 갱신", cx, cy + r), ("행동 결정", cx - r - 8, cy)]
    import math
    pos = {}
    for i, (name, x, y) in enumerate(nodes):
        pos[i] = (x, y)
        ops.append(R(x - 52, y - 19, 104, 38, "#ffffff", INK, 1.6, 6))
        ops.append(T(x, y, name, 13.5, INK, "middle", "bold"))
    def arc(a1, a2):
        p1 = (cx + (r + 6) * math.cos(a1), cy + (r + 6) * math.sin(a1))
        p2 = (cx + (r + 6) * math.cos(a2), cy + (r + 6) * math.sin(a2))
        return (f"M {p1[0]:.1f} {p1[1]:.1f} A {r+6} {r+6} 0 0 1 {p2[0]:.1f} {p2[1]:.1f}")
    angs = [-math.pi / 2, 0, math.pi / 2, math.pi]
    for i in range(4):
        a1, a2 = angs[i] + 0.58, angs[(i + 1) % 4] - 0.58
        ops.append(P(arc(a1, a2), INK, 1.8, marker="ah"))
    write("diag-loop.svg", ops, 840, 368)

# ── 그림 14-1 · 두 시험대 ───────────────────────────────────────────
def diag_arenas():
    ops = []
    title(ops, "두 시험대는 서로 다른 실패를 유혹한다",
          "InterCode CTF는 반복의 유혹으로, τ-Bench는 위반의 유혹으로 상태 관리를 시험한다")
    # 좌: 터미널
    tx0, ty0, tw, th = 60, 92, 330, 240
    ops.append(R(tx0, ty0, tw, th, "#1e2229", "#1e2229", 0, 8))
    for i, c in enumerate(["#e06c60", "#e0c060", "#68c06e"]):
        ops.append(C(tx0 + 20 + i * 18, ty0 + 18, 5, c, "none", 0))
    lines = [("$ strings flag.bin", BLUE), ("no flag here", MUTE),
             ("$ strings flag.bin", RED), ("no flag here", MUTE),
             ("$ gdb flag.bin", BLUE), ("break at main — 단서 발견", GREEN)]
    for i, (s, col) in enumerate(lines):
        ops.append(T(tx0 + 18, ty0 + 48 + i * 26, s, 12, col, "start", "normal", MONO))
    ops.append(R(tx0 + 14, ty0 + 96, tw - 28, 24, "none", RED, 1.2, 3))
    ops.append(T(tx0 + tw / 2, ty0 + 236, "같은 명령의 반복 — 기록이 넘쳐서", 12, "#e8a0a0", "middle"))
    ops.append(P(f"M {tx0+tw-70} {ty0+106} C {tx0+tw-16} {ty0+128}, {tx0+tw-16} {ty0+56}, {tx0+tw-96} {ty0+60}",
                 RED, 1.4, marker="ahr", dash="4,3"))
    ops.append(T(tx0 + tw / 2, 350, "InterCode CTF — 시행착오의 터미널", 14, INK, "middle", "bold"))
    # 우: 삼각형
    ax, ay = 660, 130   # 사용자
    bx, by = 560, 300   # DB
    cx2, cy2 = 780, 300  # 에이전트
    ops.append(L(ax, ay, bx, by, GRAY, 1.5, marker="ahg"))
    ops.append(L(ax, ay, cx2, cy2, GRAY, 1.5, marker="ahg"))
    ops.append(L(bx, by, cx2, cy2, GRAY, 1.5, marker="ahg"))
    tri = [("사용자", ax, ay, LAMBER, AMBER), ("데이터베이스", bx, by, LBLUE, BLUE),
           ("에이전트", cx2, cy2, LGREEN, GREEN)]
    for name, x, y, fill, st in tri:
        ops.append(R(x - 44, y - 17, 88, 34, fill, st, 1.6, 6))
        ops.append(T(x, y, name, 12.5, INK, "middle", "bold"))
    ops.append(T((ax + bx) / 2 - 30, (ay + by) / 2 - 12, "말이 바뀐다", 11, MUTE, "middle"))
    ops.append(T((ax + cx2) / 2 + 30, (ay + cy2) / 2 - 12, "응답한다", 11, MUTE, "middle"))
    ops.append(T((bx + cx2) / 2, (by + cy2) / 2 + 26, "조회 · 트랜잭션", 11, MUTE, "middle"))
    ops.append(R(548, 336, 244, 30, "none", RED, 1.3, 5, dash="6,4"))
    ops.append(T(670, 351, "정책 위반의 유혹 — 친절하지만 무결하지 않으면 실패", 11.5, RED, "middle"))
    ops.append(T(660, 392, "Sierra τ-Bench — 정책 아래의 트랜잭션", 14, INK, "middle", "bold"))
    write("diag-arenas.svg", ops, 840, 420)

# ── 그림 15-2 · 오류 분류 스택 바 ───────────────────────────────────
def diag_errors():
    ops = []
    title(ops, "소형 모델의 실패는 준수의 문제다",
          "Gemma-4-31B · 지평 100 실패 로그의 분포 — 논문 §5.7")
    x0, x1, y, h = 90, 800, 170, 54
    segs = [(68, "덮어쓰기·삭제", RED, LRED),
            (20, "스키마 이해·형식", AMBER, LAMBER),
            (12, "JSON 구문", GRAY, LGRAY)]
    x = x0
    for pct, lab, col, fill in segs:
        w = (x1 - x0) * pct / 100
        ops.append(R(x, y, w - 3, h, fill, col, 1.6, 4))
        ops.append(T(x + w / 2, y - 0 + h / 2 - 12, f"{pct}%", 20, col, "middle", "bold"))
        ops.append(T(x + w / 2, y + h / 2 + 14, lab, 12.5, INK, "middle"))
        x += w
    ops.append(T(x0, y - 34, "갱신 계약 위반이 10건 중 9건 — 추론 능력이 아니라 형식 준수가 무너진다",
                 13.5, MUTE, "start"))
    ops.append(L(x0, y + h + 26, x1, y + h + 26, "#cccccc", 1.6, marker=None))
    ops.append(T(x0, y + h + 48, "0%", 12, MUTE, "start"))
    ops.append(T(x1, y + h + 48, "100%", 12, MUTE, "end"))
    write("diag-errors.svg", ops, 840, 262)

# ── 그림 16-1 · 충분통계량의 우산 ───────────────────────────────────
def diag_cracks():
    ops = []
    title(ops, "전제가 깨지는 세 지점 — 충분통계량의 우산",
          "상태가 미래에 필요한 전부를 품는 한 폐기는 무손실이다 · 논문 §7")
    # 우산
    ux, uy = 420, 158
    ops.append(P(f"M {ux-296} {uy+42} A 296 116 0 0 1 {ux+296} {uy+42}", BLUE, 3, LBLUE))
    ops.append(L(ux, uy + 42 - 116, ux, uy + 42, BLUE, 3))
    ops.append(C(ux, uy + 42 - 116, 6, BLUE, BLUE, 1))
    # 보호 대상
    ops.append(R(ux - 110, uy + 120, 220, 52, "#ffffff", INK, 1.8, 6))
    ops.append(T(ux, uy + 146, "미래의 실행", 15, INK, "middle", "bold"))
    ops.append(T(ux, uy + 196, "상태 Σt 만으로 다음 행동이 결정된다", 12, MUTE, "middle"))
    # 우산 밖 과거 비
    for dx in (-372, 372):
        for k in range(3):
            x = ux + dx + k * 14
            ops.append(L(x, 120 + k * 26, x - 8, 142 + k * 26, GRAY, 1.4))
    ops.append(T(ux - 372 + 96, 236, "과거의 관찰", 11.5, GRAY, "start", rot=-90))
    ops.append(T(ux + 372 + 40, 236, "과거의 관찰", 11.5, GRAY, "start", rot=90))
    # 세 균열 — 돔 타원 표면 y에서 시작해 아래로 새는 지그재그
    import math as _m
    rx_d, ry_d, ybase = 296, 116, uy + 42
    cracks = [(-196, "① 스키마를 미리 모를 때"), (0, "② 뒤늦은 관련성"), (196, "③ 궤적이 대상일 때")]
    for dx, lab in cracks:
        ey = ybase - ry_d * _m.sqrt(1 - (dx / rx_d) ** 2)
        ops.append(P(f"M {ux+dx-26} {ey+6} l 12 14 l -9 12 l 14 15", "#ffffff", 4, "none"))
        ops.append(P(f"M {ux+dx-26} {ey+6} l 12 14 l -9 12 l 14 15", RED, 1.6, "none"))
        # 옆 균열의 물방울은 상자 상면으로 비스듬히 떨어뜨린다
        tx = ux + dx if dx == 0 else ux + (110 - 12) * (1 if dx > 0 else -1)
        ops.append(P(f"M {ux+dx} {ey+56:.1f} L {tx} {uy+114}", RED, 1.8, marker="ahr", dash="3,4"))
        ops.append(T(ux + dx, uy + 240, lab, 12.5, RED, "middle", "bold"))
    write("diag-cracks.svg", ops, 840, 400)

# ── 그림 17-1 · 이행 여섯 걸음 ──────────────────────────────────────
def diag_journey():
    ops = []
    title(ops, "이행은 반복 측정에서 지평 확장까지 여섯 걸음",
          "측정이 정당화를, 계약과 검증이 구조를, 나란히 달리기가 승인을 만든다")
    steps = [("반복 측정", "로그에서 반복을 센다"),
             ("스키마 작성", "미래가 쓸 것만 뽑는다"),
             ("갱신 계약", "세 묶음 산출 계약"),
             ("검증·병합", "결정론 게이트"),
             ("나란히 달리기", "두 런타임 비교"),
             ("지평 확장", "격차의 방향")]
    y = 210
    ops.append(L(70, y, 790, y, "#c9c9c9", 2.4))
    n = len(steps)
    for i, (name, sub) in enumerate(steps):
        x = 100 + i * (700 - 100) / (n - 1)
        col = BLUE if i in (3,) else INK
        ops.append(C(x, y, 9, "#ffffff", col, 2.4))
        up = (i % 2 == 0)
        ty = y - 64 if up else y + 64
        ops.append(L(x, y - 9 if up else y + 9, x, ty + (18 if up else -18), "#bbbbbb", 1.3))
        ops.append(T(x, ty - 16 if up else ty + 4, f"걸음 {i+1}", 11, MUTE, "middle"))
        ops.append(T(x, ty + 4 if up else ty + 24, name, 14, col, "middle", "bold"))
        ops.append(T(x, ty + 24 if up else ty + 44, sub, 11.5, MUTE, "middle"))
        if i == 3:
            ops.append(P(f"M {x} {y-44} l 12 8 l -12 8 l -12 -8 z", BLUE, 1.6, LBLUE))
            ops.append(T(x, y - 60, "게이트 — 실패는 상태에 못 닿는다", 11, BLUE, "middle", "bold"))
    write("diag-journey.svg", ops, 840, 330)

if __name__ == "__main__":
    diag_growth()
    diag_architecture()
    diag_transition()
    diag_quadratic()
    diag_worlds()
    diag_recovery()
    diag_map()
    diag_loop()
    diag_arenas()
    diag_errors()
    diag_cracks()
    diag_journey()
