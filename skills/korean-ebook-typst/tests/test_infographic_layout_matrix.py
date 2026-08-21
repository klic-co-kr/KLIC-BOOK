"""test_infographic_layout_matrix.py — 스펙 §6.2·§6.3 matrix 격자·정성."""
import json
from pathlib import Path

import pytest

from scripts.infographic.archetypes import matrix as matrix_arch
from scripts.infographic.model import RectOp, TextOp
from scripts.infographic.parse import parse_fence

TOKENS = json.loads((Path(__file__).resolve().parents[1] / "styles" / "practical" / "tokens.json").read_text(encoding="utf-8"))
W = TOKENS["body_frame_pt"]["x1"] - TOKENS["body_frame_pt"]["x0"]
P = 14.0


def _grid_fence(ncols=4, nrows=3):
    headers = [f"열 {i+1}" for i in range(ncols)]
    rows = [[f"행 {r+1}-{c+1}" for c in range(ncols)] for r in range(nrows)]
    return parse_fence(1, 1, json.dumps(
        {"layout": "matrix", "title": "판단표", "headers": headers, "rows": rows}, ensure_ascii=False))


def _qual_fence():
    return parse_fence(1, 1, json.dumps({
        "layout": "matrix", "title": "정성 매트릭스",
        "x_axis": {"low": "소규모", "high": "대규모"},
        "y_axis": {"low": "단기", "high": "장기"},
        "cells": [
            {"title": "신속 검증", "text": "가설 확인"},
            {"title": "확장 투자", "text": "규모 대응"},
            {"title": "부채 정리", "text": "구조 조정"},
            {"title": "전략 전환", "text": "사업 재편"}],
    }, ensure_ascii=False))


def test_grid_geometry():
    fig = matrix_arch.layout(_grid_fence(), TOKENS)
    cells = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
    assert len(cells) == 4 * 3
    expect = (W - 2 * P) / 4
    assert abs(cells[0].w - expect) < 0.01
    assert abs(cells[1].x - (P + expect)) < 0.01          # 간격 0 — 인접 격자


def test_grid_first_column_bold():
    fig = matrix_arch.layout(_grid_fence(), TOKENS)
    first = [t for t in fig.ops if isinstance(t, TextOp) and t.field == "cell[0][0]"]
    assert first and first[0].weight == "bold"


def test_grid_five_cols_practical_rejected():
    with pytest.raises(matrix_arch.MatrixLayoutError, match="열"):
        matrix_arch.layout(_grid_fence(ncols=5), TOKENS)  # practical 상한 4


def test_grid_six_cols_business_ok():
    BT = json.loads((Path(__file__).resolve().parents[1] / "styles" / "business" / "tokens.json").read_text(encoding="utf-8"))
    fig = matrix_arch.layout(_grid_fence(ncols=5), BT)     # business 상한 5
    assert fig.width > 0


def test_qualitative_four_cells_with_axis_labels():
    fig = matrix_arch.layout(_qual_fence(), TOKENS)
    cells = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
    assert len(cells) == 4
    labels = [t.text for t in fig.ops if isinstance(t, TextOp) and t.field.startswith("axis.")]
    assert "소규모" in labels and "장기" in labels
    AXIS_W = 40.0                                          # 구현 상수 — y축 라벨 열
    expect = (W - 2 * P - AXIS_W - 28.0) / 2               # 119.2pt(적대 검토 20pt 오차 정정)
    assert abs(cells[0].w - expect) < 0.01


def test_quadrant_alias_routes_to_qualitative():
    body = json.dumps({
        "layout": "quadrant", "title": "t",
        "x_axis": {"low": "a", "high": "b"}, "y_axis": {"low": "c", "high": "d"},
        "cells": [{"title": "1", "text": "x"}, {"title": "2", "text": "x"},
                  {"title": "3", "text": "x"}, {"title": "4", "text": "x"}]}, ensure_ascii=False)
    f = parse_fence(1, 1, body)
    assert f.layout == "matrix" and "x_axis" in f.data    # 정성 형태로 라우팅


def test_matrix_golden_snapshot():
    import os
    from scripts.infographic.emit import render_typ
    GOLDEN = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "infographic" / "golden-matrix-practical.typ"
    out = render_typ(matrix_arch.layout(_grid_fence(), TOKENS))
    if not GOLDEN.exists():
        if os.environ.get("IG_REGEN_GOLDEN") != "1":
            pytest.fail("골든 없음 — IG_REGEN_GOLDEN=1 실행 후 눈검·커밋")
        GOLDEN.parent.mkdir(parents=True, exist_ok=True)
        GOLDEN.write_text(out, encoding="utf-8")
    assert out == GOLDEN.read_text(encoding="utf-8")


def test_qualitative_requires_four_cells():
    body = json.dumps({
        "layout": "matrix", "title": "t",
        "x_axis": {"low": "a", "high": "b"}, "y_axis": {"low": "c", "high": "d"},
        "cells": [{"title": "1", "text": "x"}]}, ensure_ascii=False)
    from scripts.infographic.parse import ParseError
    with pytest.raises(ParseError, match="cells"):
        parse_fence(1, 1, body)


def test_height_limit():
    long = "아주 긴 셀 텍스트이다 " * 6
    body = json.dumps({"layout": "matrix", "title": "t",
                       "headers": ["a", "b", "c", "d"],
                       "rows": [[long] * 4 for _ in range(6)]}, ensure_ascii=False)
    with pytest.raises(matrix_arch.MatrixLayoutError, match="85"):
        matrix_arch.layout(parse_fence(1, 1, body), TOKENS)
