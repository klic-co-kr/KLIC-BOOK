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
    rows = {p: t for p, t, _ in ig_render._sheet_rows(f)}
    assert rows["modules[0].cards[0].title"] == "카드 1"
    assert rows["modules[1].steps[0].title"] == "준비"


def test_sheet_rows_carry_resolved_module_evidence():
    # 모듈 행 evidence 열은 해석 규칙 그대로 — 모듈 값 우선·상위 폴백(최종 리뷰).
    # 검수 시트가 모듈 evidence를 보여주지 않으면 대조자가 근거를 확인 못 한다.
    from scripts.infographic import render as ig_render
    f = _fence([dict(CARDS3, slot="primary", evidence="§2"),
                dict(FLOW2, slot="supporting")], evidence="§1")
    rows = {p: ev for p, t, ev in ig_render._sheet_rows(f)}
    assert rows["modules[0].cards[0].title"] == "§2"   # 모듈 자체 우선
    assert rows["modules[1].steps[0].title"] == "§1"   # 상위 폴백
    assert rows["title"] == "§1"


def test_module_alias_normalized_like_top_level():
    # 모듈 별칭도 재귀 파싱이 정규화한다(최종 리뷰) — 사전 VALID_LAYOUTS 검사가
    # 별칭을 "알 수 없는 layout"으로 죽이던 것을 폈다. 재귀 금지(composite) 검사는 잔존.
    f = _fence([dict(CARDS3, slot="primary"),
                dict(FLOW2, slot="supporting", layout="process")])
    m = f.data["modules"][1]
    assert m.layout == "flow" and m.data["_alias"] == "process"
    assert m.data["_slot"] == "supporting"


MODULE_ALIAS_MD = """## 검증 장

```infographic
{"layout": "composite", "title": "구성과 절차를 한 장에 담는다",
 "modules": [
   {"slot": "primary", "layout": "cards", "title": "핵심 구성은 세 축이다",
    "cards": [{"title": "수집", "text": "입력을 모은다."},
              {"title": "정제", "text": "형식을 통일한다."},
              {"title": "배포", "text": "산출물을 전달한다."}]},
   {"slot": "supporting", "layout": "process", "title": "적용 절차는 준비에서 확정으로 이어진다",
    "steps": [{"title": "준비", "text": "전제를 확인한다."},
              {"title": "확정", "text": "결과를 승인한다."}]}]}
```

본문 산문 한 줄.
"""


def test_module_alias_builds_and_warns(tmp_path, capsys):
    # 모듈 별칭(최종 리뷰) — 정규화돼 빌드는 계속되고 최상위와 같은 2채널 경고:
    # 채널 1 콘솔 print + 채널 2 검수 시트 상단 줄.
    from scripts.infographic import render as ig_render
    (tmp_path / "ch01.md").write_text(MODULE_ALIAS_MD, encoding="utf-8")
    build = tmp_path / "build"
    build.mkdir()
    (build / "tokens.json").write_text(
        (SKILL / "styles" / "practical" / "tokens.json").read_text(encoding="utf-8"),
        encoding="utf-8")
    out = ig_render.render_book_fences(tmp_path, build, {"chapters": ["ch01.md"]})
    assert out[0][1] == "000-fig01.typ"            # 별칭 모듈 포함 빌드 성공
    stdout = capsys.readouterr().out
    assert "별칭 process→flow — 정식 키워드 권장" in stdout
    assert "#1 modules[1]" in stdout
    sheet = (build / "infographic" / "000-fig01.review.md").read_text(encoding="utf-8")
    assert "별칭 process→flow — 정식 키워드 권장" in sheet


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
