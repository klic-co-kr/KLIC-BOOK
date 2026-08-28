"""b5 스타일 팩 계약 테스트 — 176×250 B5판 실용서."""

import json
from pathlib import Path

import pytest

MM = 72 / 25.4


def _tokens():
    return json.loads(
        (Path(__file__).parent.parent / "styles/b5/tokens.json").read_text(
            encoding="utf-8"))


def test_b5_trim_is_iso_b5():
    t = _tokens()
    assert (t["trim"]["width_mm"], t["trim"]["height_mm"]) == (176, 250)


def test_b5_frame_matches_trim_margins():
    """body_frame_pt는 trim/margin 유도값과 일치해야 한다(G1 프레임 정합성).

    B5 176×250, inner 22, top 24, outer 18, bottom 22mm:
    x0=inner, y0=top, x1=width-outer, y1=height-bottom(pt 환산).
    """
    t = _tokens()
    f = t["body_frame_pt"]
    assert f["x0"] == pytest.approx(t["margin"]["inner_mm"] * MM, abs=0.05)
    assert f["y0"] == pytest.approx(t["margin"]["top_mm"] * MM, abs=0.05)
    assert f["x1"] == pytest.approx(
        (t["trim"]["width_mm"] - t["margin"]["outer_mm"]) * MM, abs=0.05)
    assert f["y1"] == pytest.approx(
        (t["trim"]["height_mm"] - t["margin"]["bottom_mm"]) * MM, abs=0.05)


def test_b5_body_font_matches_practical_lineup():
    """b5는 practical과 같은 5폰트 라인업 — G2 허용 집합 정규화 매칭."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
    from qc_gate import allowed_fonts
    a = allowed_fonts(_tokens())[0]
    assert "freesentation" in a
    assert "pretendard" in a


def test_b5_band_derives_from_frame_width():
    """G3 밴드 35–45는 판면 폭 × 본문 pt에서 유도. 실측 평균 glyph advance는
    전각 em의 ~0.78(공백·라틴·문장부호 혼합 — 설득의 구조 10pt판 실측 0.771).
    26.08.28 재보정: 본문 10→11.5pt·마진 22/18→24/20으로 48–52자 만선 해소."""
    t = _tokens()
    frame_mm = (t["trim"]["width_mm"] - t["margin"]["inner_mm"]
                - t["margin"]["outer_mm"])
    cpl = frame_mm / (t["fonts"]["body"]["size_pt"] * 25.4 / 72 * 0.78)
    assert t["chars_per_line"]["min"] <= cpl <= t["chars_per_line"]["max"]


def test_b5_stack_freesentation_first():
    t = _tokens()
    assert t["fonts"]["body"]["stack"][0] == "Freesentation"
    assert t["fonts"]["label"]["stack"][0] == "Montserrat"
