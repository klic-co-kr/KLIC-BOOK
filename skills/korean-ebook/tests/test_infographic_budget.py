"""test_infographic_budget.py — 스펙 §4.3 근사 예산.
KO 단위는 PACK_KO_FACTOR(골든 교정 1주기 실측, 2026-08-22)에 비례한다 —
절대값이 아니라 계수 대비 비례식으로 검증한다(재교정 시 본 파일 불변)."""
import math

from scripts.infographic.budget import (PACK_KO_FACTOR, line_count,
                                        max_units, width_units)

F = PACK_KO_FACTOR["practical"]          # width_units 기본 팩


def test_ko_counts_full_latin_discounted():
    assert width_units("접수") == 2.0 * F
    assert abs(width_units("AB") - 1.1) < 1e-9              # 라틴은 계수 무관
    assert abs(width_units("eGovFrame") - 9 * 0.55) < 1e-9  # 9자 — 초판 8자 오기 정정
    assert abs(width_units("접수 AB") - (2.0 * F + 3 * 0.55)) < 1e-9
    # 팩별 계수 반영 — 같은 문구라도 팩마다 환산 단위가 다르다(§4.1)
    for pack, f in PACK_KO_FACTOR.items():
        assert abs(width_units("접수", pack) - 2.0 * f) < 1e-9


def test_max_units_formula():
    # box 120pt, size 9pt, pad 8: (120-16)*0.9/9 = 10.4 units
    assert abs(max_units(120.0, 9.0) - 10.4) < 1e-9


def test_line_count_rounds_up_min_one():
    assert line_count("접수등록", 120.0, 9.0) == 1          # 4F ≤ 10.4
    # 3줄 진입: KO 환산 단위가 cap 10.4의 2배 초과 — 계수에서 유도(재교정 내성)
    n3 = math.ceil(2 * 10.4 / (2 * F)) + 1
    assert line_count("접수" * n3, 120.0, 9.0) == 3
    assert line_count("한", 15.0, 9.0) == 1                # cap=(15-16)*0.9/9 ≤ 0 → 클램프 1
                                                           # (20pt면 cap=0.4>0이라 3이 된다 — 초판 오기 정정)
