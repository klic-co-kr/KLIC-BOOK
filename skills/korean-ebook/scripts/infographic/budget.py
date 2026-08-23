"""budget.py — 텍스트 폭 예산(스펙 §4.3). 폰트 메트릭 없는 근사: KO=1.0, 라틴=0.55, 10% 마진.
팩별 보정 계수: 1순위 폰트가 팩마다 다르므로(§4.1) 단일 전역표를 쓰지 않는다.
골든 교정 1주기(2026-08-22, 스펙 §7·§8-2) 실측값 반영 — 아래 PACK_KO_FACTOR 주석."""
from __future__ import annotations

import math
import unicodedata

KO_UNIT = 1.0
LATIN_UNIT = 0.55
MARGIN = 0.9
DEFAULT_PAD = 8.0

# 팩별 KO 보정 계수 — 골든 교정 1주기 실측(2026-08-22).
# 절차: tests/fixtures/infographic/calib-cards.md를 cli.py preview --style <팩>으로
# 렌더 → PyMuPDF 스팬 폭 실측. 측정 단위 KO 환산 pt, 경계 = 카드 폭(텍스트가
# 카드를 벗어나는 지점). 자당폭(카드 제목 = 본문+1pt bold):
#   practical/b5 Freesentation-Bold 11pt   8.470pt/자(0.770em)
#   essay          SUIT-Bold        11pt   9.614pt/자(0.874em)
#   business       Pretendard-Bold  11.5pt 9.936pt/자(0.864em)
#   lecture        Pretendard-Bold  11pt   9.504pt/자(0.864em)
# ※ business 1순위 Wanted Sans Std(설치본)에 한글 글리프가 없어 스택 폴백
#   Pretendard로 렌더된다 — 실측은 렌더 사실(폴백 포함)을 따른다.
# 판정 계약: 비율 = 예상수용KO자수(max_units 식) ÷ 실측수용KO자수 → 2자리 반올림.
# 전 팩 |비율−1| ≥ 0.30 — 데드밴드(±0.05) 밖, 전 팩 갱신.
PACK_KO_FACTOR = {
    "practical": 0.61,   # 예상 5.52자 / 실측 9자(카드폭 83.5pt) = 0.6136
    "essay": 0.66,       # 예상 6.60자 / 실측 10자(96.7pt) = 0.6605
    "business": 0.70,    # 예상 8.39자 / 실측 12자(123.2pt) = 0.6990
    "lecture": 0.70,     # 예상 9.08자 / 실측 13자(127.0pt) = 0.6983
    "b5": 0.63,          # 예상 6.91자 / 실측 11자(100.5pt) = 0.6285
}


def width_units(text: str, pack: str = "practical") -> float:
    f = PACK_KO_FACTOR.get(pack, 1.0)
    units = 0.0
    for ch in text:
        name = unicodedata.name(ch, "")
        ko = "HANGUL" in name or "CJK" in name or "FULLWIDTH" in name
        units += (KO_UNIT * f) if ko else LATIN_UNIT
    return units


def max_units(box_w: float, size_pt: float, pad: float = DEFAULT_PAD) -> float:
    return (box_w - 2 * pad) * MARGIN / size_pt


def line_count(text: str, box_w: float, size_pt: float, pad: float = DEFAULT_PAD,
               pack: str = "practical") -> int:
    cap = max_units(box_w, size_pt, pad)
    if cap <= 0:
        return 1
    return max(1, math.ceil(width_units(text, pack) / cap))
