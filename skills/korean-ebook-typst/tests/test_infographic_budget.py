"""test_infographic_budget.py — 스펙 §4.3 근사 예산."""
import math

from scripts.infographic.budget import width_units, max_units, line_count


def test_ko_counts_full_latin_discounted():
    assert width_units("접수") == 2.0
    assert abs(width_units("AB") - 1.1) < 1e-9
    assert abs(width_units("eGovFrame") - 9 * 0.55) < 1e-9   # 9자 — 초판 8자 오기 정정
    assert abs(width_units("접수 AB") - (2.0 + 3 * 0.55)) < 1e-9


def test_max_units_formula():
    # box 120pt, size 9pt, pad 8: (120-16)*0.9/9 = 10.4 units
    assert abs(max_units(120.0, 9.0) - 10.4) < 1e-9


def test_line_count_rounds_up_min_one():
    assert line_count("접수등록", 120.0, 9.0) == 1          # 4.0 ≤ 10.4
    assert line_count("접수" * 12, 120.0, 9.0) == 3        # 24.0/10.4 = 2.31 → 3
    assert line_count("한", 15.0, 9.0) == 1                # cap=(15-16)*0.9/9 ≤ 0 → 클램프 1
                                                           # (20pt면 cap=0.4>0이라 3이 된다 — 초판 오기 정정)
