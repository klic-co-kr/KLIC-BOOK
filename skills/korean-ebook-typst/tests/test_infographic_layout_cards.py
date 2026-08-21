"""test_infographic_layout_cards.py — 스펙 §6.2·§6.3 cards 지오메트리·결정론."""
import json
from pathlib import Path

import pytest

from scripts.infographic.archetypes import cards as cards_arch
from scripts.infographic.model import FigModel, RectOp, TextOp
from scripts.infographic.parse import parse_fence

TOKENS = json.loads((Path(__file__).resolve().parents[1] / "styles" / "practical" / "tokens.json").read_text(encoding="utf-8"))
W = TOKENS["body_frame_pt"]["x1"] - TOKENS["body_frame_pt"]["x0"]
P, G = 14.0, 28.0


def _fence(n: int, value: bool = False, text: str = "근거 문장"):
    cards = []
    for i in range(n):
        c = {"title": f"항목 {i+1}", "text": text}
        if value:
            c["value"] = "3단계"
        cards.append(c)
    body = json.dumps({"layout": "cards", "title": "결론 제목", "cards": cards}, ensure_ascii=False)
    return parse_fence(1, 1, body)


def test_three_cards_one_row_practical():
    fig = cards_arch.layout(_fence(3), TOKENS)
    cards = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
    assert len(cards) == 3
    expect = (W - 2 * P - 2 * G) / 3
    assert abs(cards[0].w - expect) < 0.01
    assert abs(cards[2].x - (P + 2 * (expect + G))) < 0.01


def test_two_cards_widen_to_two_cols():
    fig = cards_arch.layout(_fence(2), TOKENS)
    cards = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
    assert abs(cards[0].w - (W - 2 * P - G) / 2) < 0.01     # cols=min(3,2)=2


def test_five_cards_wrap_two_rows():
    fig = cards_arch.layout(_fence(5), TOKENS)
    cards = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
    assert len(cards) == 5
    assert len({round(r.y, 2) for r in cards}) == 2          # 3+2 랩


def test_five_cards_essay_pack_limit_error():
    # essay 상한 2열×2행=4 — n=5는 layout 판형 상한 경로(parse 2~6 내부)
    ET = json.loads((Path(__file__).resolve().parents[1] / "styles" / "essay" / "tokens.json").read_text(encoding="utf-8"))
    with pytest.raises(cards_arch.CardsLayoutError, match="상한"):
        cards_arch.layout(_fence(5), ET)


def test_cards_lint_and_review_sheet_reach_elements():
    # lint가 cards 요소에 도달하는가(KeyError 아님) — 적대 검토 G1 방어
    from scripts.infographic.lint import check
    from scripts.infographic.render import _review_sheet
    body = json.dumps({"layout": "cards", "title": "t", "cards": [
        {"title": "3단계 확정", "text": "가"},
        {"title": "b", "text": "나"},
        {"title": "c", "text": "다"}]}, ensure_ascii=False)
    fence = parse_fence(1, 1, body)
    figs = {1: cards_arch.layout(fence, TOKENS)}
    found = check([fence], figs, TOKENS, "원문 없음", "ch01.md")
    assert any(f.loc == "ch01.md #1 cards[0].title" for f in found)
    sheet = _review_sheet(fence, [])
    assert "cards[0].title" in sheet


def test_value_renders_large_focus_text():
    fig = cards_arch.layout(_fence(3, value=True), TOKENS)
    values = [t for t in fig.ops if isinstance(t, TextOp) and t.field == "cards[0].value"]
    assert values and values[0].role == "focus" and values[0].weight == "bold"
    assert values[0].size > TOKENS["fonts"]["body"]["size_pt"] + 2


def test_g3_invariant_and_ink_bbox():
    body_size = TOKENS["fonts"]["body"]["size_pt"]
    for n in (2, 3, 4, 6):
        fig = cards_arch.layout(_fence(n), TOKENS)
        assert isinstance(fig, FigModel)
        for o in fig.ops:
            if isinstance(o, RectOp):
                assert o.x - o.stroke_w / 2 >= -0.001 and o.x + o.w + o.stroke_w / 2 <= fig.width + 0.001
            if isinstance(o, TextOp) and o.size != body_size:
                assert abs(o.size - body_size) > 0.3


def test_aliases_principles_dashboard():
    import json as j
    for alias in ("principles", "dashboard"):
        body = j.dumps({"layout": alias, "title": "t", "cards": [
            {"title": "a", "text": "가"}, {"title": "b", "text": "나"}]}, ensure_ascii=False)
        f = parse_fence(1, 1, body)
        assert f.layout == "cards" and f.data["_alias"] == alias


def test_cards_golden_snapshot():
    import os
    from scripts.infographic.emit import render_typ
    GOLDEN = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "infographic" / "golden-cards-practical.typ"
    fig = cards_arch.layout(_fence(3, value=True), TOKENS)
    out = render_typ(fig)
    if not GOLDEN.exists():
        if os.environ.get("IG_REGEN_GOLDEN") != "1":
            pytest.fail("골든 없음 — IG_REGEN_GOLDEN=1 실행 후 눈검·커밋")
        GOLDEN.parent.mkdir(parents=True, exist_ok=True)
        GOLDEN.write_text(out, encoding="utf-8")
    assert out == GOLDEN.read_text(encoding="utf-8")
