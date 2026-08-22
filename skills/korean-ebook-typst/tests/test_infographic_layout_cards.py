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


def test_value_wrapped_lines_measured_in_card_height():
    # 최종 리뷰 — value 2줄 감싸짐: card_h(높이 예산)이 실측 줄 수를 반영해
    # _card_texts(렌더 블록)와 일치. 1줄 가정이면 높이 차 0 → 잉크 bbox 이탈.
    from scripts.infographic import budget
    body_size = TOKENS["fonts"]["body"]["size_pt"]
    value_size = body_size + 1 + cards_arch.VALUE_BONUS_PT
    cardW = (W - 2 * P - 2 * G) / 3
    long_value = "열 번 다시 확인하는 긴 값"
    assert budget.line_count(long_value, cardW, value_size,
                            cards_arch.CARD_PAD_IN, "practical") == 2       # 사전 조건

    def card_h_of(value: str) -> float:
        body = json.dumps({"layout": "cards", "title": "t", "cards": [
            {"title": "a", "value": value, "text": "근거"},
            {"title": "b", "value": value, "text": "근거"},
            {"title": "c", "value": value, "text": "근거"}]}, ensure_ascii=False)
        fig = cards_arch.layout(parse_fence(1, 1, body), TOKENS)
        card = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"][0]
        return card.h

    assert abs(card_h_of(long_value) - card_h_of("3단계")
               - (cards_arch.block_h(2, value_size) - cards_arch.block_h(1, value_size))) < 0.01


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


def test_card_text_max_w_excludes_padding():
    # 실측(2026-08-22, PyMuPDF): max_w=카드 전폭이면 잉크가 테두리에 닿는다/넘는다
    # (ch00 −2.01pt, ch04 −1.59pt 관측). line_count 예산(pad=8)이 감안하는 좌우
    # CARD_PAD_IN을 렌더에도 반영 — 예산과 렌더가 같은 폭을 본다.
    fig = cards_arch.layout(_fence(3), TOKENS)
    card = next(r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint")
    fields = [o for o in fig.ops if isinstance(o, TextOp) and o.field and o.field.startswith("cards[0].")]
    assert fields
    for o in fields:
        assert o.max_w == pytest.approx(card.w - 2 * cards_arch.CARD_PAD_IN)


def test_block_h_matches_typst_line_advance():
    # typst 실측(2026-08-22, Pretendard 11pt·leading 1.3em): 줄 진행 2.008em
    # = leading 1.3em + cap 0.71em. 1줄 박스 높이 1.19em(ascent 1.06 +
    # descent 0.13, 스팬 bbox 실측). 구형 LINE_FIRST_EM=0.75는 박스를 0.44em
    # 과소 — 중심 앵커 블록끼리 밀려 헤더 잉크 겹침(4.89pt 스팬 실측).
    assert cards_arch.block_h(1, 10.0) == pytest.approx(11.9)
    assert cards_arch.block_h(2, 10.0) == pytest.approx(32.4)
    assert cards_arch.block_h(3, 10.0) == pytest.approx(52.9)


def test_header_blocks_have_ink_gap():
    # 중심 앵커 TextOp는 size·1.19em 박스가 중심에서 뻗는다 — 인접 헤더 블록
    # 중심 거리가 (박스1+박스2)/2 + 여유보다 작으면 잉크 겹침(agent-papers
    # 5개 cards 펜스 실측 4.89/4.85pt). gap 3pt 이상을 보증한다.
    body = json.dumps({"layout": "cards", "title": "결론 제목", "kicker": "KICKER",
                       "thesis": "단일 문장 논지", "cards": [
                         {"title": "a", "value": "3단계", "text": "근거"},
                         {"title": "b", "value": "3단계", "text": "근거"},
                         {"title": "c", "value": "3단계", "text": "근거"}]}, ensure_ascii=False)
    fig = cards_arch.layout(parse_fence(1, 1, body), TOKENS)
    heads = sorted((t for t in fig.ops if isinstance(t, TextOp)
                    and t.field in ("kicker", "title", "thesis")),
                   key=lambda t: t.y)
    assert len(heads) == 3
    for a, b in zip(heads, heads[1:]):
        need = (a.size + b.size) * 1.19 / 2
        assert b.y - a.y >= need + 3.0


def test_card_height_grows_with_measured_advance():
    # value 2줄 vs 1줄 카드 높이 차 = block_h(2)−block_h(1) = 2.05em
    # (구형 기대치 value_size*1.3은 2줄 블록을 0.75em 과소).
    body_size = TOKENS["fonts"]["body"]["size_pt"]
    value_size = body_size + 1 + cards_arch.VALUE_BONUS_PT
    long_value = "열 번 다시 확인하는 긴 값"
    from scripts.infographic import budget
    cardW = (W - 2 * P - 2 * G) / 3
    assert budget.line_count(long_value, cardW, value_size,
                            cards_arch.CARD_PAD_IN, "practical") == 2       # 사전 조건

    def card_h_of(value: str) -> float:
        body = json.dumps({"layout": "cards", "title": "t", "cards": [
            {"title": "a", "value": value, "text": "근거"},
            {"title": "b", "value": value, "text": "근거"},
            {"title": "c", "value": value, "text": "근거"}]}, ensure_ascii=False)
        fig = cards_arch.layout(parse_fence(1, 1, body), TOKENS)
        card = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"][0]
        return card.h

    assert abs(card_h_of(long_value) - card_h_of("3단계")
               - (cards_arch.block_h(2, value_size) - cards_arch.block_h(1, value_size))) < 0.01

