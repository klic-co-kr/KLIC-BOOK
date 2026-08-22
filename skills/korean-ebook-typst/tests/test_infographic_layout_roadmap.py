"""test_infographic_layout_roadmap.py — 스펙 §6.2·§6.3 roadmap 타임라인·위상 밴드."""
import json
from pathlib import Path

import pytest

from scripts.infographic.archetypes import roadmap as rm_arch
from scripts.infographic.model import ArrowOp, RectOp, TextOp
from scripts.infographic.parse import ParseError, parse_fence

TOKENS = json.loads((Path(__file__).resolve().parents[1] / "styles" / "practical" / "tokens.json").read_text(encoding="utf-8"))
W = TOKENS["body_frame_pt"]["x1"] - TOKENS["body_frame_pt"]["x0"]
P, G = 14.0, 28.0


def _fence(n, items=2):
    phases = [{"period": f"20{25+i}년", "title": f"위상 {i+1}",
               "items": [f"항목 {j}" for j in range(items)]} for i in range(n)]
    return parse_fence(1, 1, json.dumps(
        {"layout": "roadmap", "title": "도입 로드맵", "phases": phases}, ensure_ascii=False))


def test_parse_bounds():
    with pytest.raises(ParseError, match="phases 개수 1"):
        _fence(1)
    with pytest.raises(ParseError, match="items 개수 5"):
        _fence(2, items=5)


def test_timeline_arrow_and_bands():
    fig = rm_arch.layout(_fence(3), TOKENS)
    bands = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
    assert len(bands) == 3
    band_w = (W - 2 * P - 2 * G) / 3
    assert abs(bands[0].w - band_w) < 0.01
    assert abs(bands[2].x - (P + 2 * (band_w + G))) < 0.01
    arrows = [o for o in fig.ops if isinstance(o, ArrowOp)]
    assert len(arrows) == 1 and arrows[0].x1 < arrows[0].x2
    assert arrows[0].y1 < bands[0].y                    # 타임라인은 밴드 위
    fields = {t.field for t in fig.ops if isinstance(t, TextOp)}
    assert {"phases[0].period", "phases[1].title", "phases[2].items[1]"} <= fields


def test_band_height_measured_max():
    fig = rm_arch.layout(_fence(2, items=3), TOKENS)
    bands = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
    assert bands[0].h == bands[1].h


def test_period_measured_multi_line_essay():
    # 최종 리뷰 1 — period 1줄 가정 금지: essay 밴드 55.15pt에서 "2026년 하반기"는
    # 모델상 2줄 — 밴드 높이 예산은 실측 줄수를 따른다(1줄 가정이면 차 0)
    essay = json.loads((Path(__file__).resolve().parents[1] / "styles" / "essay" / "tokens.json").read_text(encoding="utf-8"))
    kicker = essay["fonts"]["label"]["size_pt"]

    def band_h(period):
        phases = [{"period": period, "title": "위상 1", "items": ["항목 0"]} for _ in range(3)]
        f = parse_fence(1, 1, json.dumps(
            {"layout": "roadmap", "title": "도입 로드맵", "phases": phases}, ensure_ascii=False))
        fig = rm_arch.layout(f, essay)
        return [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"][0].h

    assert abs(band_h("2026년 하반기") - band_h("2026년") - kicker * 1.3) < 0.01


def test_pack_cap_essay():
    essay = json.loads((Path(__file__).resolve().parents[1] / "styles" / "essay" / "tokens.json").read_text(encoding="utf-8"))
    with pytest.raises(rm_arch.RoadmapLayoutError, match=r"판형 상한 3위상\(essay\)"):
        rm_arch.layout(_fence(4), essay)


def test_pack_cap_success_all_packs():
    # I3 — 각 팩 스펙 상한 n에서 렌더 성공(C5 방어: 밴드폭 ≥ MIN_BAND_W 실증)
    packs = {"essay": 3, "practical": 4, "b5": 4, "business": 5, "lecture": 5}
    for name, cap in packs.items():
        toks = json.loads((Path(__file__).resolve().parents[1] / "styles" / name / "tokens.json").read_text(encoding="utf-8"))
        fig = rm_arch.layout(_fence(cap), toks)
        bands = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
        assert len(bands) == cap, name
        assert bands[0].w >= rm_arch.MIN_BAND_W - 0.01, name


def test_height_limit_85pct():
    # 최종 리뷰 3 — 85% 높이 게이트: 4위상×장문 항목(판형 상한 내) → 밴드 줄수 폭증
    long_text = "아주 긴 항목 문장이다 " * 8
    phases = [{"period": "2025년", "title": "위상", "items": [long_text] * 2} for _ in range(4)]
    f = parse_fence(1, 1, json.dumps(
        {"layout": "roadmap", "title": "도입 로드맵", "phases": phases}, ensure_ascii=False))
    with pytest.raises(rm_arch.RoadmapLayoutError, match="85"):
        rm_arch.layout(f, TOKENS)


def test_roadmap_elements_reach_lint_and_sheet():
    # before_after의 test_before_after_elements_reach_lint_and_sheet 패턴 —
    # 1) 숫자 포함 요소(period/title/items)가 I1 숫자-evidence 검사 대상에 들어가는지
    # 2) render._sheet_rows가 phases[i].* 행을 반환하는지
    from scripts.infographic.lint import check
    from scripts.infographic.render import _review_sheet, _sheet_rows
    f = _fence(2, items=2)
    f.data["phases"][0]["period"] = "2026년 3분기"       # 숫자 주입
    f.data["phases"][0]["items"][0] = "예산 12% 확보"
    figs = {1: rm_arch.layout(f, TOKENS)}
    found = check([f], figs, TOKENS, "원문 없음", "ch01.md")
    assert any(x.kind == "number-evidence" and x.loc == "ch01.md #1 phases[0].period" for x in found)
    assert any(x.kind == "number-evidence" and x.loc == "ch01.md #1 phases[0].items[0]" for x in found)
    rows = dict(_sheet_rows(f))
    assert {"phases[0].period", "phases[0].title", "phases[0].items[0]",
            "phases[1].items[1]"} <= set(rows)
    sheet = _review_sheet(f, [])
    for path in ("phases[0].period", "phases[0].title", "phases[0].items[0]"):
        assert path in sheet


def test_roadmap_golden_snapshot():
    # cards 골든 패턴(test_infographic_layout_cards.py:124-135) 복제 — I2:
    # emit 심볼은 render_typ(fig)뿐(emit.py:21), os는 파일 상단 임포트
    import os
    GOLDEN = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "infographic" / "golden-roadmap-practical.typ"
    fig = rm_arch.layout(_fence(3), TOKENS)
    from scripts.infographic.emit import render_typ
    code = render_typ(fig)
    if os.environ.get("IG_REGEN_GOLDEN") != "1":
        if not GOLDEN.exists():
            pytest.fail("골든 없음 — `IG_REGEN_GOLDEN=1 python3 -m pytest …` 실행 후 눈검·커밋")
        assert code == GOLDEN.read_text(encoding="utf-8")
    else:
        GOLDEN.write_text(code, encoding="utf-8")
        pytest.fail("골든 재생성 — 눈검 후 커밋")
