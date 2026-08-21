"""budget.py — 텍스트 폭 예산(스펙 §4.3). 폰트 메트릭 없는 근사: KO=1.0, 라틴=0.55, 10% 마진.
팩별 보정 계수: 1순위 폰트가 팩마다 다르므로(§4.1) 단일 전역표를 쓰지 않는다.
초기값은 전 팩 1.0 — 골든 교정 절차(Task 11, 스펙 §7)로 팩별 실측값을 갱신한다."""
from __future__ import annotations

import math
import unicodedata

KO_UNIT = 1.0
LATIN_UNIT = 0.55
MARGIN = 0.9
DEFAULT_PAD = 8.0

# 팩별 KO 보정 계수 — 골든 교정(각 팩 1순위 폰트로 fixture 카드 오버플로 한계 실측)으로 갱신.
PACK_KO_FACTOR = {"practical": 1.0, "essay": 1.0, "business": 1.0,
                  "lecture": 1.0, "b5": 1.0}


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
