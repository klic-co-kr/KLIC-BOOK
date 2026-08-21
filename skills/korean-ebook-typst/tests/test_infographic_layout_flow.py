"""test_infographic_layout_flow.py — 스펙 §6.2·§6.3 flow 지오메트리·결정론·잉크 bbox."""
import json
from pathlib import Path

import pytest

from scripts.infographic.archetypes import flow as flow_arch
from scripts.infographic.model import FigModel, RectOp, TextOp
from scripts.infographic.parse import parse_fence

TOKENS = json.loads((Path(__file__).resolve().parents[1] / "styles" / "practical" / "tokens.json").read_text(encoding="utf-8"))
W = TOKENS["body_frame_pt"]["x1"] - TOKENS["body_frame_pt"]["x0"]   # 334.49
H = TOKENS["body_frame_pt"]["y1"] - TOKENS["body_frame_pt"]["y0"]
P, G, MIN_CARD = 14.0, 28.0, 80.0


def _fence(n_steps: int, title: str = "결론 제목", text: str = "근거 문장"):
    body = json.dumps({
        "layout": "flow", "title": title,
        "steps": [{"title": f"단계 {i+1}", "text": text} for i in range(n_steps)],
    }, ensure_ascii=False)
    return parse_fence(1, 1, body)


def test_two_steps_horizontal():
    fig = flow_arch.layout(_fence(2), TOKENS)
    rects = [o for o in fig.ops if isinstance(o, RectOp)]
    cards = [r for r in rects if r.fill_role == "surface-tint"]
    assert len(cards) == 2
    expect = (W - 2 * P - G) / 2
    assert abs(cards[0].w - expect) < 0.01
    assert abs(cards[1].x - (P + expect + G)) < 0.01


def test_four_steps_wraps_to_2x2():
    fig = flow_arch.layout(_fence(4), TOKENS)
    cards = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
    assert len(cards) == 4
    expect = (W - 2 * P - G) / 2                      # 2열
    assert abs(cards[0].w - expect) < 0.01
    ys = {round(r.y, 2) for r in cards}
    assert len(ys) == 2                               # 2행


def test_eight_steps_pack_limit_error():
    # practical 판형 상한 6 — n=8은 지오메트리 전에 판형 상한 위반 에러
    with pytest.raises(flow_arch.FlowLayoutError, match="판형 상한"):
        flow_arch.layout(_fence(8), TOKENS)


def test_eight_steps_business_wraps_four_cols():
    # business(453.55pt)는 상한 8 — 4열 랩: (453.55-28-84)/4 = 85.4pt ≥ 80
    BTOKENS = json.loads((Path(__file__).resolve().parents[1] / "styles" / "business"
                          / "tokens.json").read_text(encoding="utf-8"))
    fig = flow_arch.layout(_fence(8), BTOKENS)
    cards = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
    assert len(cards) == 8
    expect = (BTOKENS["body_frame_pt"]["x1"] - BTOKENS["body_frame_pt"]["x0"] - 2 * P - 3 * G) / 4
    assert abs(cards[0].w - expect) < 0.01
    assert len({round(r.y, 2) for r in cards}) == 2   # 2행


def test_six_steps_wrap_three_cols():
    # practical n=6: 가로 27.7pt ✗ → 랩 3열 (334.49-28-56)/3 = 83.5pt ≥ 80
    fig = flow_arch.layout(_fence(6), TOKENS)
    cards = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
    assert len(cards) == 6
    assert abs(cards[0].w - (W - 2 * P - 2 * G) / 3) < 0.01


def test_ink_containment_guaranteed():
    for n in (2, 3, 4, 5, 6):
        fig = flow_arch.layout(_fence(n), TOKENS)
        for o in fig.ops:
            if isinstance(o, RectOp):
                assert o.x - o.stroke_w / 2 >= -0.001, f"n={n}"
                assert o.x + o.w + o.stroke_w / 2 <= fig.width + 0.001, f"n={n}"
                assert o.y - o.stroke_w / 2 >= -0.001, f"n={n}"
                assert o.y + o.h + o.stroke_w / 2 <= fig.height + 0.001, f"n={n}"


def test_g3_invariant_sizes_off_body():
    body = TOKENS["fonts"]["body"]["size_pt"]
    fig = flow_arch.layout(_fence(3), TOKENS)
    texts = [o for o in fig.ops if isinstance(o, TextOp) and o.size != body]
    assert texts                                   # 도식 텍스트 존재
    for o in texts:
        assert abs(o.size - body) > 0.3, o.size    # 본문 크기와 0.3pt 이상 차이


def test_height_limit_85pct():
    # n=6(상한 내) + 장문 — 카드 줄수 폭증으로 높이 한계 초과 (n=8은 판형 상한 에러가 먼저)
    # ×8은 교정 전 계수 1.0 기준이었다 — 1주기 실측 계수 0.61(2026-08-22)에서는
    # ×8이 85% 안에 들어와 ×16으로 올린다(줄수 2배 폭증 경로는 동일).
    long_text = "아주 긴 근거 문장이다 " * 16
    with pytest.raises(flow_arch.FlowLayoutError, match="85"):
        flow_arch.layout(_fence(6, text=long_text), TOKENS)


def test_figmodel_is_frozen_deterministic():
    f1 = flow_arch.layout(_fence(5), TOKENS)
    f2 = flow_arch.layout(_fence(5), TOKENS)
    assert f1 == f2                                 # 결정론 — 같은 입력 같은 모델
