# tests/test_infographic_layout_layers.py — 스펙 §6.2·§6.3 layers 지오메트리·결정론.
"""test_infographic_layout_layers.py — 스펙 §6.2·§6.3 layers 지오메트리·결정론."""
import json
from pathlib import Path

import pytest

from scripts.infographic.archetypes import layers as layers_arch
from scripts.infographic.model import CircleOp, RectOp, TextOp
from scripts.infographic.parse import ParseError, parse_fence

TOKENS = json.loads((Path(__file__).resolve().parents[1] / "styles" / "practical" / "tokens.json").read_text(encoding="utf-8"))
ETOKENS = json.loads((Path(__file__).resolve().parents[1] / "styles" / "essay" / "tokens.json").read_text(encoding="utf-8"))


def _stack_fence(n=4, **extra):
    payload = {"layout": "layers", "title": "계층 구조 점검 제목",
               "stack": [{"label": f"계층 {i}"} for i in range(n)]}
    payload.update(extra)
    return parse_fence(1, 1, json.dumps(payload, ensure_ascii=False))


def _rings_fence(n=4):
    return parse_fence(1, 1, json.dumps({"layout": "layers", "title": "계층 구조 점검 제목",
                                      "rings": [{"label": f"링 {i}"} for i in range(n)]},
                                     ensure_ascii=False))


def test_parse_bounds():
    with pytest.raises(ParseError):                        # stack·rings 동시
        parse_fence(1, 1, '{"layout":"layers","title":"t","stack":[{"label":"외부"},{"label":"내부"}],'
                       '"rings":[{"label":"외부"},{"label":"내부"}]}')
    with pytest.raises(ParseError):                        # 둘 다 없음
        parse_fence(1, 1, '{"layout":"layers","title":"t"}')
    with pytest.raises(ParseError):
        _stack_fence(n=7)                                  # 상한 6 초과
    with pytest.raises(ParseError):
        _stack_fence(n=1)                                  # 하한 2 미만
    with pytest.raises(ParseError):
        parse_fence(1, 1, '{"layout":"layers","title":"t","stack":[{"label":"외부"},{"label":""}]}')


def test_stack_rows_full_width():
    fig = layers_arch.layout(_stack_fence(n=4), TOKENS)
    rects = [o for o in fig.ops if isinstance(o, RectOp) and o.fill_role != "paper"]
    W = TOKENS["body_frame_pt"]["x1"] - TOKENS["body_frame_pt"]["x0"]
    assert len(rects) == 4
    assert all(abs(r.x - 14.0) < 0.01 and abs(r.w - (W - 28.0)) < 0.01 for r in rects)
    assert abs(rects[1].y - rects[0].y - rects[0].h - 10.0) < 0.01


def test_rings_radii_equidistant():
    fig = layers_arch.layout(_rings_fence(), TOKENS)          # rings 4개 practical
    cs = [o for o in fig.ops if isinstance(o, CircleOp)]
    assert len(cs) == 4
    r_max = (TOKENS["body_frame_pt"]["x1"] - TOKENS["body_frame_pt"]["x0"] - 28.0) / 2
    step = (r_max - 0.25 * r_max) / 3
    assert abs(cs[0].r - r_max) < 0.01
    assert abs(cs[3].r - (r_max - 3 * step)) < 0.01


def test_rings_label_max_w_within_chord():
    # 링 라벨 상자 폭 = 라벨 중심선(원 중심에서 r−d 위)의 현(chord) − pad — 최내곽 링이 가장 좁다.
    import math
    fig = layers_arch.layout(_rings_fence(), TOKENS)
    labels = sorted((o for o in fig.ops if isinstance(o, TextOp)
                     and o.field.startswith("rings[")), key=lambda o: o.max_w)
    r_max = (TOKENS["body_frame_pt"]["x1"] - TOKENS["body_frame_pt"]["x0"] - 28.0) / 2
    step = (r_max - 0.25 * r_max) / 3
    item = TOKENS["fonts"]["body"]["size_pt"] - 1
    d = 6.0 + item * 1.3 / 2
    r_inner = r_max - 3 * step
    expect = 2 * math.sqrt(r_inner * r_inner - (r_inner - d) ** 2) - 16.0
    assert labels[0].field == "rings[3].label"
    assert abs(labels[0].max_w - expect) < 0.01


def test_layers_determinism():
    f = _stack_fence(n=4)
    assert layers_arch.layout(f, TOKENS).ops == layers_arch.layout(f, TOKENS).ops


def test_rings_essay_fits_frame():
    # rings 분기 결정론 + 가장 좁은 essay 팩에서도 4링 동심원이 85% 프레임 안.
    f = _rings_fence()
    fig1 = layers_arch.layout(f, ETOKENS)
    assert fig1.ops == layers_arch.layout(f, ETOKENS).ops
    H = ETOKENS["body_frame_pt"]["y1"] - ETOKENS["body_frame_pt"]["y0"]
    assert fig1.height <= H * 0.85


def test_layers_elements_reach_lint_and_sheet():
    from scripts.infographic.lint import check
    from scripts.infographic.render import _review_sheet, _sheet_rows
    f = _stack_fence(n=4)
    f.data["stack"][0]["label"] = "표현 계층은 3종 뷰를 가진다"
    figs = {1: layers_arch.layout(f, TOKENS)}
    found = check([f], figs, TOKENS, "원문 없음", "ch01.md")
    assert any(x.kind == "number-evidence" and x.loc == "ch01.md #1 stack[0].label" for x in found)
    rows = dict(_sheet_rows(f))
    assert {"stack[0].label", "stack[3].label"} <= set(rows)
    sheet = _review_sheet(f, [])
    assert "stack[0].label" in sheet


def test_layers_golden_snapshot():
    import os
    from scripts.infographic.emit import render_typ
    GOLDEN = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "infographic" / "golden-layers-practical.typ"
    payload = {"layout": "layers", "title": "계층은 표현에서 자료로 내려간다",
               "kicker": "구조",
               "stack": [{"label": "표현 계층"}, {"label": "응용 계층"},
                         {"label": "논리 계층"}, {"label": "자료 계층"}]}
    # stack 기본 변형 — 전폭 4행, 순서 = 위→아래(표현이 가장 위).
    f = parse_fence(1, 1, json.dumps(payload, ensure_ascii=False))
    code = render_typ(layers_arch.layout(f, TOKENS))
    if os.environ.get("IG_REGEN_GOLDEN") != "1":
        if not GOLDEN.exists():
            pytest.fail("골든 없음 — `IG_REGEN_GOLDEN=1 python3 -m pytest …` 실행 후 눈검·커밋")
        assert code == GOLDEN.read_text(encoding="utf-8")
    else:
        GOLDEN.parent.mkdir(parents=True, exist_ok=True)
        GOLDEN.write_text(code, encoding="utf-8")
        pytest.fail("골든 재생성 — 눈검 후 커밋")

