"""diagram 엔진 — 스키마 검증·렌더·빌드 통합."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import diagram as dg  # noqa: E402


FLOW = {
    "layout": "flow",
    "title": "검증을 통과해야 상태에 남는다",
    "sub": "테스트 플로우",
    "nodes": [
        {"id": "a", "label": "관찰 수신"},
        {"id": "b", "label": "프롬프트 구성"},
        {"id": "v", "label": "검증", "kind": "gate", "tone": "blue"},
        {"id": "c", "label": "상태 병합", "tone": "green"},
        {"id": "r", "label": "롤백 · 재시도", "tone": "red"},
    ],
    "edges": [
        {"from": "a", "to": "b"},
        {"from": "b", "to": "v"},
        {"from": "v", "to": "c", "kind": "ok", "label": "통과"},
        {"from": "v", "to": "r", "kind": "fail", "label": "실패"},
        {"from": "r", "to": "b", "kind": "back", "side": "left"},
    ],
}

CYCLE = {
    "layout": "cycle",
    "title": "매 턴 장부만 고친다",
    "center": "슬롯 장부",
    "nodes": [{"label": "청취"}, {"label": "해석"}, {"label": "갱신"}, {"label": "행동"}],
}

TIMELINE = {
    "layout": "timeline",
    "title": "환각의 길이가 회복력이다",
    "axis": "턴",
    "lanes": [
        {"name": "이력 기반", "tone": "red",
         "events": [{"label": "알림"}, {"label": "환각"}, {"label": "환각"},
                    {"label": "환각"}, {"label": "회복", "major": True}]},
        {"name": "상태 기반", "tone": "green",
         "events": [{"label": "알림"}, {"label": "정답", "major": True}]},
    ],
}

STACK = {
    "layout": "stack",
    "title": "이력은 걸음마다 쌓인다",
    "legend": ["관찰", "추론", "행동"],
    "cols": [{"label": "턴 1", "layers": 3}, {"label": "턴 2", "layers": 6},
             {"label": "턴 3", "layers": 9}],
}

SCENE = {
    "layout": "scene",
    "title": "두 계층",
    "nodes": [
        {"id": "x", "label": "장기 기억", "x": 60, "y": 100, "w": 160, "h": 50, "tone": "gray"},
        {"id": "y", "label": "실행 상태", "x": 560, "y": 100, "w": 160, "h": 50, "tone": "blue"},
    ],
    "edges": [{"from": "x", "to": "y", "label": "투영"}],
}


def test_lint_accepts_all_layouts():
    for f in (FLOW, CYCLE, TIMELINE, STACK, SCENE):
        dg.lint_fence(f)


def test_lint_rejects_unknown_layout():
    with pytest.raises(ValueError):
        dg.lint_fence({"layout": "bogus", "title": "x"})


def test_lint_rejects_dangling_edge():
    bad = {"layout": "flow", "title": "x",
           "nodes": [{"id": "a", "label": "A"}],
           "edges": [{"from": "a", "to": "zz"}]}
    with pytest.raises(ValueError):
        dg.lint_fence(bad)


def test_lint_rejects_long_title_and_labels():
    with pytest.raises(ValueError):
        dg.lint_fence({"layout": "cycle", "title": "길다" * 30,
                       "nodes": [{"label": "a"}, {"label": "b"}, {"label": "c"}]})
    with pytest.raises(ValueError):
        dg.lint_fence({"layout": "flow", "title": "x",
                       "nodes": [{"id": "a", "label": "이것은매우긴라벨입니다" * 4}]})


def test_lint_cycle_node_bounds():
    with pytest.raises(ValueError):
        dg.lint_fence({"layout": "cycle", "title": "x",
                       "nodes": [{"label": "a"}, {"label": "b"}]})


def test_render_flow_produces_svg():
    svg = dg.render_fence(FLOW)
    assert svg.startswith("<svg")
    assert "게이트" not in svg or "검증" in svg
    assert svg.count("marker-end") >= 5
    assert "롤백" in svg


def test_render_cycle_arc_count():
    svg = dg.render_fence(CYCLE)
    assert svg.count("<path") >= 4  # 호 4 + 없음(상자는 rect)


def test_render_timeline_lanes():
    svg = dg.render_fence(TIMELINE)
    assert "이력 기반" in svg and "상태 기반" in svg and "턴" in svg


def test_render_stack_blocks():
    svg = dg.render_fence(STACK)
    # 3+6+9=18개 층 블록
    assert svg.count("<rect") >= 18 + 3  # 블록 + 패널 3


def test_render_scene_nodes_and_edge():
    svg = dg.render_fence(SCENE)
    assert "장기 기억" in svg and "실행 상태" in svg and "투영" in svg


def test_extract_finds_fences():
    md = "# 챕터\n\n텍스트\n\n```diagram\n" + \
         '{"layout": "cycle", "title": "t", "nodes": [{"label": "a"}, {"label": "b"}, {"label": "c"}]}' + \
         "\n```\n"
    _, fences = dg.extract(md)
    assert len(fences) == 1 and fences[0][0]["layout"] == "cycle"


def test_render_invalid_fence_raises():
    with pytest.raises(ValueError):
        dg.render_fence({"layout": "flow", "title": "x", "nodes": []})
