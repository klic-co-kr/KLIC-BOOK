"""cover_compositions — 표지 변조 프로파일 엔진.

골격(V1~V5)은 구조를 정하고, 프로파일은 변조축(타이틀 앵커·모티프 유형·
밀도·액센트 회귀)을 정한다. 프로파일 선택은 제목 해시로 결정적 — 같은 책은
같은 표지, 책마다 달라진다. opt-in(cover_composition: true)일 때만 개입하고
꺼져 있으면 기존 변형 문법을 그대로 둔다.
"""
from __future__ import annotations

import hashlib
import random

# 변조축
#   anchor  — 타이틀 세로 앵커: top | mid | bottom
#   motif   — 모티프 유형: dots | circles | lines | squares | none
#   density — 모티프 채움 밀도 0.0~1.0
#   accent  — 액센트색 회귀 지점 수 2~5 (모티프 내 brand 점 비율로 구현)
#   pitch   — 모티프 격자 피치 계수 0.8(촘촘)~1.6(여유)
Profile = tuple  # (name, anchor, motif, density, accent, pitch)

PROFILES: list[Profile] = [
    # 구도 논리 — 배치의 원리
    ("삼분법 구도",      "bottom", "dots",    0.30, 3, 1.2),
    ("황금비 구도",      "bottom", "lines",   0.25, 2, 1.3),
    ("대각선 구도",      "bottom", "squares", 0.35, 3, 1.1),
    ("방사 구도",        "mid",    "circles", 0.40, 4, 1.0),
    ("원형 구도",        "mid",    "circles", 0.30, 3, 1.2),
    ("프레임 내 프레임", "bottom", "none",    0.0,  2, 1.0),
    ("부감 구도",        "top",    "squares", 0.45, 3, 1.0),
    ("조감 구도",        "top",    "dots",    0.35, 3, 1.2),
    ("수평 강조",        "mid",    "lines",   0.40, 2, 1.0),
    ("수직 강조",        "bottom", "lines",   0.20, 2, 1.4),
    ("역대각 구도",      "top",    "squares", 0.30, 3, 1.2),
    ("중앙 밀집",        "mid",    "squares", 0.55, 4, 0.9),
    # 시각 원칙 — 위계와 리듬
    ("대비 강조",        "bottom", "dots",    0.50, 5, 0.9),
    ("반복 리듬",        "bottom", "squares", 0.60, 3, 0.8),
    ("점진 위계",        "bottom", "dots",    0.25, 2, 1.5),
    ("군집",             "mid",    "dots",    0.45, 3, 0.9),
    ("여백 우위",        "mid",    "none",    0.0,  2, 1.6),
    ("밀도 우위",        "bottom", "squares", 0.75, 4, 0.8),
    ("번갈아 강조",      "mid",    "lines",   0.50, 4, 1.0),
    ("단일 초점",        "bottom", "circles", 0.25, 2, 1.3),
    # 출판 판면 — 표지의 표현형
    ("대제목 판면",      "bottom", "none",    0.0,  2, 1.0),
    ("테두리 판면",      "bottom", "none",    0.0,  3, 1.0),
    ("이미지 창 판면",   "mid",    "squares", 0.40, 2, 1.1),
    ("몬드리안 판면",    "mid",    "squares", 0.65, 4, 1.0),
    ("서커스 판면",      "top",    "circles", 0.55, 5, 0.9),
    ("실루엣 판면",      "bottom", "lines",   0.30, 2, 1.2),
    ("글자 조형 판면",   "bottom", "none",    0.0,  2, 1.2),
    ("콜라주 판면",      "mid",    "dots",    0.60, 5, 0.8),
    ("다중 패널",        "top",    "squares", 0.50, 3, 1.0),
    ("미니멀 판면",      "bottom", "none",    0.0,  2, 1.6),
    # 격자 — 질서의 체계
    ("단일 격자",        "bottom", "dots",    0.35, 3, 1.0),
    ("모듈 격자",        "bottom", "squares", 0.50, 3, 1.0),
    ("위계 격자",        "bottom", "dots",    0.30, 3, 1.1),
    ("비대칭 격자",      "bottom", "squares", 0.40, 3, 1.2),
    ("기준선 격자",      "bottom", "lines",   0.25, 2, 1.3),
    ("등간격 격자",      "mid",    "dots",    0.55, 2, 0.9),
    ("중첩 격자",        "mid",    "circles", 0.45, 4, 1.0),
    ("방사 격자",        "mid",    "circles", 0.40, 4, 1.1),
    ("확장 격자",        "top",    "squares", 0.45, 3, 1.1),
    ("축 체계",          "bottom", "lines",   0.20, 2, 1.4),
    # 전통 구도 — 한국적 질서
    ("여백",             "mid",    "none",    0.0,  2, 1.6),
    ("허실",             "bottom", "dots",    0.20, 2, 1.4),
    ("주빈 위계",        "bottom", "dots",    0.25, 2, 1.3),
    ("개합",             "top",    "lines",   0.30, 3, 1.2),
    ("책가도 진열",      "top",    "squares", 0.70, 3, 0.8),
    ("병풍 연폭",        "mid",    "squares", 0.55, 3, 1.0),
    ("문자도",           "mid",    "squares", 0.65, 4, 0.9),
    ("단청 머리초",      "top",    "circles", 0.50, 5, 0.9),
    ("십장생",           "bottom", "circles", 0.35, 3, 1.1),
    ("일수이석",         "bottom", "lines",   0.35, 2, 1.2),
]

# 앵커 → V5/V1 계열 타이틀 블록 dy 산출용 기준 높이 비율
ANCHOR_RATIO = {"top": 0.16, "mid": 0.42, "bottom": None}  # None = 기본 하단 앵커


def pick_profile(title: str) -> Profile:
    """제목 해시로 프로파일 1개 선택 — 결정적."""
    h = int(hashlib.sha1(("composition:" + title).encode()).hexdigest(), 16)
    return PROFILES[h % len(PROFILES)]


def motif_block(profile: Profile, *, variant: int, w: float, h: float,
                brand: str, mute: str, pale: str) -> str:
    """프로파일 모티프축을 typst 조각으로 — 골김·책 크기·팔레트에 맞춘다.

    dots/squares: 격자 필드. circles: 겹치는 원. lines: 수평선 필드.
    none: 모티프 없음(빈 문자열). 배치 시드는 (제목 아님) 프로파일 이름+
    변형 — 같은 프로파일이라도 골격마다 놓임이 다를 필요는 없으므로
    이름+variant 시드로 통일해 재현성을 유지한다.
    """
    name, anchor, motif, density, accent, pitch = profile
    rng = random.Random(f"motif:{name}:{variant}")
    if motif == "none":
        return ""
    # 필드 규모 — 밀도가 높으면 넓고 촘촘하게
    cols = max(3, round(6 * (0.7 + density)))
    rows = max(3, round(7 * (0.6 + density * 0.6)))
    step = round(4.2 * pitch, 2)
    fw, fh = cols * step, rows * step
    p_brand = min(0.5, 0.10 + accent * 0.08)
    cells = []
    if motif in ("dots", "squares"):
        for r in range(rows):
            for c in range(cols):
                u = rng.random()
                if u > density:
                    continue
                fill = brand if u < density * p_brand else pale
                if motif == "dots":
                    rad = 0.75 if fill == brand else 0.5
                    cells.append(
                        f"#place(dx: {c * step:.1f}mm, dy: {r * step:.1f}mm, "
                        f'circle(radius: {rad}mm, fill: rgb("{fill}")))')
                else:
                    sz = 1.6 if fill == brand else 1.2
                    cells.append(
                        f"#place(dx: {c * step:.1f}mm, dy: {r * step:.1f}mm, "
                        f'rect(width: {sz}mm, height: {sz}mm, fill: rgb("{fill}")))')
        body = "\n    ".join(cells)
        return (f"#place(top + right, dx: -30mm, dy: 36mm)[\n"
                f"  #box(width: {fw:.1f}mm, height: {fh:.1f}mm)[\n"
                f"    {body}\n  ]\n]")
    if motif == "circles":
        n = 2 + (accent >= 4)
        parts = []
        cr = min(22.0, w * 0.11)
        for i in range(n):
            off = cr * 0.62 * i
            stroke = brand if i % 2 == 0 else pale
            parts.append(
                f"#place(dx: {off:.1f}mm, dy: {cr * 0.62 * (n - 1 - i):.1f}mm, "
                f'circle(radius: {cr:.1f}mm, stroke: 2.2pt + rgb("{stroke}"), fill: none))')
        tint = cr * (1 + 0.62 * (n - 1))
        parts.append(
            f"#place(dx: {tint * 0.4:.1f}mm, dy: {tint * 0.4:.1f}mm, "
            f'circle(radius: {cr:.1f}mm, fill: rgb("{brand}").transparentize(88%)))')
        body = "\n    ".join(parts)
        box = cr * 2 + cr * 0.62 * (n - 1)
        return (f"#place(top + right, dx: -26mm, dy: {h * 0.10:.0f}mm)[\n"
                f"  #box(width: {box:.1f}mm, height: {box:.1f}mm)[\n"
                f"    {body}\n  ]\n]")
    if motif == "lines":
        n = max(3, round(rows * 1.5))
        parts = []
        for i in range(n):
            u = rng.random()
            if u > density + 0.25:
                continue
            lw = fw * (0.35 + 0.6 * rng.random())
            color = brand if u < density * p_brand else pale
            th = 1.2 if color == brand else 0.6
            parts.append(
                f"#place(dx: 0mm, dy: {i * step:.1f}mm, "
                f'rect(width: {lw:.1f}mm, height: {th}pt, fill: rgb("{color}")))')
        body = "\n    ".join(parts)
        return (f"#place(top + right, dx: -30mm, dy: 36mm)[\n"
                f"  #box(width: {fw:.1f}mm, height: {n * step:.1f}mm)[\n"
                f"    {body}\n  ]\n]")
    return ""


def opener_strip(profile: Profile, idx: int, *, brand: str, pale: str) -> str:
    """장 오프너용 우측 에지 세로 진열 스트립.

    표지 모티프와 같은 계열이되 형태를 달리한다 — 표지가 우상단 수평
    필드라면 오프너는 세로 진열. 장 번호(idx)가 시드라 장마다 놓임이
    변한다. none 프로파일도 최소 마커(가는 횡선)를 남긴다.
    """
    name, anchor, motif, density, accent, pitch = profile
    rng = random.Random(f"opener:{name}:{idx}")
    gap = round(7.5 * pitch, 1)
    p_brand = min(0.5, 0.10 + accent * 0.08)
    marks = []
    if motif == "squares":
        n = 5 + round(density * 8)
        for _ in range(n):
            color = brand if rng.random() < p_brand else pale
            sz = 2.4 if color == brand else 1.7
            marks.append(f'rect(width: {sz}mm, height: {sz}mm, '
                         f'fill: rgb("{color}"))')
    elif motif == "dots":
        n = 5 + round(density * 8)
        for _ in range(n):
            color = brand if rng.random() < p_brand else pale
            rad = 1.2 if color == brand else 0.85
            marks.append(f'circle(radius: {rad}mm, fill: rgb("{color}"))')
    elif motif == "circles":
        n = 2 + (accent >= 4)
        for i in range(n):
            color = brand if i % 2 == 0 else pale
            marks.append(f'circle(radius: {2.2 + i * 0.5:.1f}mm, '
                         f'stroke: 1.6pt + rgb("{color}"), fill: none)')
    else:  # lines · none — 가로 틱/횡선의 세로 나열
        n = 4 + round(density * 6) if motif == "lines" else 3
        for _ in range(n):
            color = brand if rng.random() < p_brand else pale
            w = 6 + 10 * rng.random()
            th = 1.4 if color == brand else 0.7
            marks.append(f'rect(width: {w:.1f}mm, height: {th}pt, '
                         f'fill: rgb("{color}"))')
    # openers.typ의 배열(코드 모드) 원소로 쓰인다 — 최외곽 호출은 # 없이.
    return (f'align(right)[#stack(dir: ttb, spacing: {gap}mm, '
            f'{", ".join(marks)})]')
