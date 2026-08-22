"""composite — 복합 씬(스펙 §3.5): 모듈 측정·배분·세로 스택·분할 에러."""
import json
import sys
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))

from scripts.infographic.archetypes import composite as comp_arch
from scripts.infographic.layout import dispatch
from scripts.infographic.parse import ParseError, parse_fence

TOKENS = json.loads((SKILL / "styles" / "practical" / "tokens.json").read_text(encoding="utf-8"))

CARDS3 = {"layout": "cards",
          "title": "근거 카드 셋",
          "cards": [{"title": f"카드 {i}", "text": f"근거 문장 {i}."} for i in range(1, 4)]}
FLOW2 = {"layout": "flow", "title": "적용 절차",
         "steps": [{"title": "준비", "text": "전제를 확인한다."},
                   {"title": "실행", "text": "절차를 수행한다."}]}
LADDER4 = {"layout": "ladder", "title": "성숙도 계단", "thesis": "단계마다 확신이 쌓인다",
           "stages": [{"title": f"단계 {i}", "text": f"{t} 상태를 넘어선다."}
                      for i, t in enumerate(["사각", "관심", "실행", "정착"], 1)]}


def _fence(modules, title="구성과 절차를 한 장에 담는다", **kw):
    body = {"layout": "composite", "modules": modules}
    if title is not None:
        body["title"] = title
    body.update(kw)
    f = parse_fence(1, 1, json.dumps(body, ensure_ascii=False))
    return f


def test_parse_bounds():
    with pytest.raises(ParseError):
        _fence([dict(CARDS3, slot="primary")])                     # 보조 0 — 모듈 2~3
    with pytest.raises(ParseError):
        _fence([dict(CARDS3, slot="primary")] +
               [dict(FLOW2, slot="supporting")] * 3)               # 보조 3 — 상한 2
    with pytest.raises(ParseError):
        _fence([dict(CARDS3, slot="main"),                         # slot 오타
                dict(FLOW2, slot="supporting")])
    with pytest.raises(ParseError):
        _fence([dict(CARDS3, slot="primary"), dict(FLOW2, slot="primary")])  # primary 2개
    with pytest.raises(ParseError):
        _fence([dict(CARDS3, slot="primary"),
                dict(LADDER4, slot="supporting", layout="composite")])      # 재귀
    with pytest.raises(ParseError):
        parse_fence(1, 1, json.dumps({"layout": "composite", "modules": [
            {"slot": "primary", "layout": "nope"}]}, ensure_ascii=False))   # unknown


def test_stack_geometry_and_gap():
    # title=None — fig.height = 모듈 높이 합 + GAP 정확히(헤더 블록 없음)
    f = _fence([dict(CARDS3, slot="primary"), dict(FLOW2, slot="supporting")], title=None)
    fig = comp_arch.layout(f, TOKENS)
    c = dispatch(_to_fence(1, 1, CARDS3), TOKENS)
    fl = dispatch(_to_fence(1, 1, FLOW2), TOKENS)
    assert abs(fig.height - (c.height + comp_arch.GAP + fl.height)) < 0.01


def test_title_block_adds_height_and_no_title_omits_it():
    mods = [dict(CARDS3, slot="primary"), dict(FLOW2, slot="supporting")]
    with_t = comp_arch.layout(_fence(mods), TOKENS)
    without = comp_arch.layout(_fence(mods, title=None), TOKENS)
    assert with_t.height > without.height            # 최상위 title 블록만큼 증가
    texts = [op.text for op in with_t.ops if op.__class__.__name__ == "TextOp"]
    assert "구성과 절차를 한 장에 담는다" in texts
    texts_wo = [op.text for op in without.ops if op.__class__.__name__ == "TextOp"]
    assert "구성과 절차를 한 장에 담는다" not in texts_wo


def test_total_height_within_85_percent_even_with_title():
    # G1-H1 방어: 헤더 포함 총량도 85% 한도 내 — H_avail이 헤더를 선차감한다
    frame = TOKENS["body_frame_pt"]
    cap = (frame["y1"] - frame["y0"]) * 0.85
    f = _fence([dict(CARDS3, slot="primary"), dict(FLOW2, slot="supporting")])
    assert comp_arch.layout(f, TOKENS).height <= cap + 0.01


def _to_fence(index, line, d):
    body = dict(d)
    f = parse_fence(index, line, json.dumps(body, ensure_ascii=False))
    return f


def test_primary_over_sixty_percent_error():
    # ladder 4단계 practical = 프레임 85%(426.93) 점유 — 60% 상한 초과 확정
    f = _fence([dict(LADDER4, slot="primary"), dict(FLOW2, slot="supporting")])
    with pytest.raises(comp_arch.CompositeLayoutError, match="primary ladder 측정높이"):
        comp_arch.layout(f, TOKENS)


def test_supporting_over_allocation_error():
    # 보조 ladder 4단계(≈426.93)는 어떤 배분과도 초과 — 확정 에러
    f = _fence([dict(CARDS3, slot="primary"), dict(LADDER4, slot="supporting")])
    with pytest.raises(comp_arch.CompositeLayoutError, match="supporting ladder 측정높이"):
        comp_arch.layout(f, TOKENS)


def test_determinism():
    f = _fence([dict(CARDS3, slot="primary"), dict(FLOW2, slot="supporting")])
    a = comp_arch.layout(f, TOKENS)
    b = comp_arch.layout(_fence([dict(CARDS3, slot="primary"), dict(FLOW2, slot="supporting")]), TOKENS)
    assert [(op.__class__.__name__, getattr(op, "x", None), getattr(op, "y", None))
            for op in a.ops] == [(op.__class__.__name__, getattr(op, "x", None), getattr(op, "y", None))
                                 for op in b.ops]


def test_sheet_rows_reach_module_fields():
    from scripts.infographic import render as ig_render
    f = _fence([dict(CARDS3, slot="primary"), dict(FLOW2, slot="supporting")])
    rows = dict(ig_render._sheet_rows(f))
    assert rows["modules[0].cards[0].title"] == "카드 1"
    assert rows["modules[1].steps[0].title"] == "준비"


GOLDEN = Path(__file__).parent / "fixtures" / "infographic" / "golden-composite-practical.typ"


def test_composite_golden():
    import os
    from scripts.infographic import emit
    fig = comp_arch.layout(_fence([dict(CARDS3, slot="primary"),
                                   dict(FLOW2, slot="supporting")]), TOKENS)
    typ = emit.render_typ(fig)
    if not GOLDEN.exists():
        if not os.environ.get("IG_REGEN_GOLDEN"):
            pytest.fail("골든 부재 — IG_REGEN_GOLDEN=1로 재생성")
        GOLDEN.write_text(typ, encoding="utf-8")
        pytest.fail("골든 재생성 — 눈검(모듈 헤더 2개·24pt 간격·노트 2개) 후 커밋")
    assert GOLDEN.read_text(encoding="utf-8") == typ
