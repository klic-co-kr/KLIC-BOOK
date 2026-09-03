"""test_infographic_layout_flow_lanes.py — 스펙 §6.3 flow(swimlane) + T5 보강."""
import json
from pathlib import Path

import pytest

from scripts.infographic.archetypes import flow as flow_arch
from scripts.infographic.model import RectOp, TextOp
from scripts.infographic.parse import ParseError, parse_fence

TOKENS = json.loads((Path(__file__).resolve().parents[1] / "styles" / "practical" / "tokens.json").read_text(encoding="utf-8"))
W = TOKENS["body_frame_pt"]["x1"] - TOKENS["body_frame_pt"]["x0"]
P, GS, ACTOR_W = 14.0, 24.0, 60.0


def _lane_fence(nlanes=2, nsteps=3):
    lanes = [{"actor": f"주체 {i+1}",
              "steps": [{"title": f"단계 {j+1}", "text": "근거"} for j in range(nsteps)]}
             for i in range(nlanes)]
    return parse_fence(1, 1, json.dumps(
        {"layout": "flow", "title": "레인 흐름", "lanes": lanes}, ensure_ascii=False))


def test_two_lanes_three_steps_geometry():
    fig = flow_arch.layout(_lane_fence(2, 3), TOKENS)
    cells = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
    assert len(cells) == 6                                   # 2레인 × 3셀
    expect = (W - 2 * P - ACTOR_W - 2 * GS) / 3              # 66.2pt
    assert abs(cells[0].w - expect) < 0.01
    assert cells[0].x == P + ACTOR_W
    assert len({round(c.y, 2) for c in cells}) == 2          # 레인 2행


def test_lane_actors_bold_labels():
    fig = flow_arch.layout(_lane_fence(2, 3), TOKENS)
    actors = [t for t in fig.ops if isinstance(t, TextOp) and t.field == "lanes[0].actor"]
    assert actors and actors[0].weight == "bold"


def test_lane_arrows_meet_shaft_minimum():
    # §6.1 샤프트 ≥12pt — GS=24에서 12pt(적대 검토 G1 회귀 방어)
    from scripts.infographic.lint import check
    figs = {1: flow_arch.layout(_lane_fence(2, 3), TOKENS)}
    fence = _lane_fence(2, 3)
    found = check([fence], figs, TOKENS, "원문", "ch01.md")
    assert not [f for f in found if f.kind == "connector"]


def test_three_cells_essay_rejected():
    # essay 상한 2 — parse는 레인당 steps 2~4를 통과시키므로 m=3이 layout 판형
    # 상한 경로에 도달한다(레인 수 하한 2로 _lane_fence(1,3)은 parse에서 걸림).
    ET = json.loads((Path(__file__).resolve().parents[1] / "styles" / "essay" / "tokens.json").read_text(encoding="utf-8"))
    with pytest.raises(flow_arch.FlowLayoutError, match="셀"):
        flow_arch.layout(_lane_fence(2, 3), ET)


def test_both_steps_and_lanes_rejected():
    body = json.dumps({"layout": "flow", "title": "t",
                       "steps": [{"title": "a", "text": "b"}],
                       "lanes": [{"actor": "x", "steps": [{"title": "c", "text": "d"}]}]},
                      ensure_ascii=False)
    with pytest.raises(ParseError, match="steps|lanes"):
        parse_fence(1, 1, body)


def test_kicker_thesis_geometry_now_tested():
    """Phase 1 T5 deferred — kicker/thesis 분기 첫 지오메트리 단언."""
    fence = parse_fence(1, 1, json.dumps({
        "layout": "flow", "title": "제목", "kicker": "CHAPTER MAP", "thesis": "한 문장 설명",
        "steps": [{"title": "a", "text": "가"}, {"title": "b", "text": "나"}]}, ensure_ascii=False))
    fig = flow_arch.layout(fence, TOKENS)
    kick = [t for t in fig.ops if isinstance(t, TextOp) and t.field == "kicker"]
    th = [t for t in fig.ops if isinstance(t, TextOp) and t.field == "thesis"]
    assert kick and kick[0].y < th[0].y                      # kicker가 thesis 위
    assert kick[0].size == TOKENS["fonts"]["label"]["size_pt"]
