# tests/test_infographic_emit_max_w.py — emit max_w 방출 + note 다중 줄 예산.
"""test_infographic_emit_max_w.py — 스펙 §5.1 emit max_w 방출 + note 다중 줄 예산화."""
from scripts.infographic.emit import render_typ
from scripts.infographic.model import FigModel, TextOp


def test_emit_max_w_unit_synthetic():
    # 합성 FigModel — TextOp 2개(폭 0·폭 100)로 방출 문자열 직접 단언(펜스 의존 없음).
    fig = FigModel(width=300.0, height=100.0, source_index=0, ops=(
        TextOp(x=150.0, y=20.0, size=9.0, text="폭 없음", max_w=0.0),
        TextOp(x=150.0, y=50.0, size=9.0, text="폭 있음", max_w=100.0),
    ))
    lines = [l for l in render_typ(fig).splitlines() if "ig-text(" in l]
    assert len(lines) == 2
    assert "max-w" not in lines[0] and "폭 없음" in lines[0]
    assert "max-w: 100.00pt" in lines[1]        # _n()은 2자리 반올림(f"{v:.2f}") 방출
