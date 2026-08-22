# tests/test_infographic_layout_topology.py — 스펙 §6.2·§6.3 topology 지오메트리·결정론.
"""test_infographic_layout_topology.py — 스펙 §6.2·§6.3 topology 지오메트리·결정론."""
import json
from pathlib import Path

import pytest

from scripts.infographic.archetypes import topology as topo_arch
from scripts.infographic.archetypes.topology import TopologyLayoutError
from scripts.infographic.model import ArrowOp, RectOp
from scripts.infographic.parse import ParseError, parse_fence

TOKENS = json.loads((Path(__file__).resolve().parents[1] / "styles" / "practical" / "tokens.json").read_text(encoding="utf-8"))
ETOKENS = json.loads((Path(__file__).resolve().parents[1] / "styles" / "essay" / "tokens.json").read_text(encoding="utf-8"))


def _fence(n=6, edges=None, **extra):
    payload = {"layout": "topology", "title": "구성 요소 관계 제목",
               "nodes": [{"id": f"n{i}", "label": f"노드 {i}"} for i in range(n)]}
    if edges is not None:
        payload["edges"] = [{"from": f"n{a}", "to": f"n{b}"} for a, b in edges]
    payload.update(extra)
    return parse_fence(1, 1, json.dumps(payload, ensure_ascii=False))


def test_parse_bounds():
    with pytest.raises(ParseError):
        parse_fence(1, 1, '{"layout":"topology","title":"t","nodes":[]}')                # 하한 3 미만
    with pytest.raises(ParseError):
        _fence(n=9)                                                                    # 절대 상한 8 초과
    with pytest.raises(ParseError):
        _fence(n=3, edges=[(0, 0)])                                                    # 자기 간선
    with pytest.raises(ParseError):
        _fence(n=3, edges=[(0, 3)])                                                    # 미참조 id
    with pytest.raises(ParseError):
        parse_fence(1, 1, '{"layout":"topology","title":"t","nodes":['
                       '{"id":"n0","label":"중복"},{"id":"n0","label":"중복"},'
                       '{"id":"n1","label":"노드"}]}')                                 # id 중복
    with pytest.raises(ParseError):
        parse_fence(1, 1, '{"layout":"topology","title":"t",'
                       '"nodes":[{"id":"a","label":"원"},{"id":"b","label":"변환"},'
                       '{"id":"c","label":"결과"}],'
                       '"edges":[{"from":"a","to":"b"},{"from":"a","to":"b"}]}')       # 간선 중복
    assert parse_fence(1, 1, '{"layout":"network","title":"t","nodes":['  # 별칭 network
        '{"id":"a","label":"클라"},{"id":"b","label":"게이트"},{"id":"c","label":"저장"}]}').layout == "topology"


def test_grid_layout_and_node_geometry():
    fig = topo_arch.layout(_fence(), TOKENS)          # 6노드 무간선 practical — 열수 3
    rects = [o for o in fig.ops if isinstance(o, RectOp) and o.fill_role != "paper"]
    assert len(rects) == 6
    W = TOKENS["body_frame_pt"]["x1"] - TOKENS["body_frame_pt"]["x0"]
    node_w = (W - 28.0 - 2 * 28.0) / 3
    assert abs(rects[0].w - node_w) < 0.01
    assert abs(rects[0].x - 14.0) < 0.01
    assert abs(rects[1].x - (14.0 + node_w + 28.0)) < 0.01   # grid 열 간격
    assert abs(rects[3].y - rects[0].y - (rects[0].h + 24.0)) < 0.01  # 2행째


def test_dag_layers_and_arrows():
    fig = topo_arch.layout(_fence(n=4, edges=[(0, 1), (0, 2), (1, 3), (2, 3)]), TOKENS)
    # 층위: n0=0, n1/n2=1, n3=2 → 열수 3. 화살표 4개 전부 x2 > x1(우향)·샤프트 ≥12pt.
    arrows = [o for o in fig.ops if isinstance(o, ArrowOp)]
    assert len(arrows) == 4
    assert all(a.x2 > a.x1 for a in arrows)
    assert all((a.x2 - a.x1) >= 12.0 - 0.01 for a in arrows)  # G 28 − tip-gap 8×2


def test_dag_cycle_rejected():
    with pytest.raises(TopologyLayoutError, match="순환"):
        topo_arch.layout(_fence(n=3, edges=[(0, 1), (1, 2), (2, 0)]), TOKENS)


def test_pack_cap_essay():
    topo_arch.layout(_fence(n=5), ETOKENS)                     # essay 상한 5 — 통과
    with pytest.raises(TopologyLayoutError, match="판형 상한"):
        topo_arch.layout(_fence(n=6), ETOKENS)


def test_node_width_floor():
    # essay 5노드 DAG로 열수 5를 만들면 노드 폭이 하상수에 걸린다(n0→n1→n2→n3→n4).
    with pytest.raises(TopologyLayoutError, match="노드 폭"):
        topo_arch.layout(_fence(n=5, edges=[(0, 1), (1, 2), (2, 3), (3, 4)]), ETOKENS)


def test_determinism():
    f = _fence(n=5, edges=[(0, 1), (1, 2)])
    assert topo_arch.layout(f, TOKENS).ops == topo_arch.layout(f, TOKENS).ops


def test_dashed_edge_style():
    f2 = _fence(n=3, edges=[(0, 1)])
    f2.data["edges"][0]["dashed"] = True        # 검증 통과 후 속성 주입 — style 방출만 검사
    fig2 = topo_arch.layout(f2, TOKENS)
    assert any(isinstance(o, ArrowOp) and o.style == "dashed" for o in fig2.ops)


def test_topology_elements_reach_lint_and_sheet():
    # test_before_after_elements_reach_lint_and_sheet 패턴 복제 —
    # lint.check는 5인자(fences, figs, tokens, chapter_md, chapter_name)·반환은 LintFinding 리스트,
    # loc는 "{chapter} #{index} {필드}"형. _sheet_rows는 2-튜플 (필드경로, 문구).
    from scripts.infographic.lint import check
    from scripts.infographic.render import _review_sheet, _sheet_rows
    f = _fence(n=3)
    f.data["nodes"][0]["label"] = "관문 3개를 지난다"
    figs = {1: topo_arch.layout(f, TOKENS)}
    found = check([f], figs, TOKENS, "원문 없음", "ch01.md")
    assert any(x.kind == "number-evidence" and x.loc == "ch01.md #1 nodes[0].label" for x in found)
    rows = dict(_sheet_rows(f))
    assert {"nodes[0].label", "nodes[1].label", "nodes[2].label"} <= set(rows)
    sheet = _review_sheet(f, [])
    for i in range(3):
        assert f"nodes[{i}].label" in sheet


def test_topology_golden_snapshot():
    import os
    from scripts.infographic.emit import render_typ
    GOLDEN = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "infographic" / "golden-topology-practical.typ"
    payload = {"layout": "topology", "title": "구성 요소는 흐름을 따라 연결된다",
               "kicker": "구성",
               "nodes": [{"id": "a", "label": "수집"}, {"id": "b", "label": "정제"},
                         {"id": "c", "label": "변환"}, {"id": "d", "label": "저장"},
                         {"id": "e", "label": "질의"}],
               "edges": [{"from": "a", "to": "b"}, {"from": "a", "to": "c"},
                         {"from": "c", "to": "d"}, {"from": "c", "to": "e", "dashed": True}]}
    # 층위: a=0, b/c=1, d/e=2 → 3열 — practical node_w 83.5pt(MIN 54 통과).
    # 연쇄 a→b→c→d→e는 5층 5열 → 38.9pt로 하상수 에러가 나므로 금지(5노드 체인 불가).
    f = parse_fence(1, 1, json.dumps(payload, ensure_ascii=False))
    code = render_typ(topo_arch.layout(f, TOKENS))
    if os.environ.get("IG_REGEN_GOLDEN") != "1":
        if not GOLDEN.exists():
            pytest.fail("골든 없음 — `IG_REGEN_GOLDEN=1 python3 -m pytest …` 실행 후 눈검·커밋")
        assert code == GOLDEN.read_text(encoding="utf-8")
    else:
        GOLDEN.parent.mkdir(parents=True, exist_ok=True)
        GOLDEN.write_text(code, encoding="utf-8")
        pytest.fail("골든 재생성 — 눈검 후 커밋")

