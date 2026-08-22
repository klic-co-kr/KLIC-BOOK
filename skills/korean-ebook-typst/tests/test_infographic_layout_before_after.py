"""test_infographic_layout_before_after.py — 스펙 §6.2·§6.3 before_after 지오메트리·결정론."""
import json
from pathlib import Path

import pytest

from scripts.infographic.archetypes import before_after as ba_arch
from scripts.infographic.model import ArrowOp, RectOp, TextOp
from scripts.infographic.parse import ParseError, parse_fence

TOKENS = json.loads((Path(__file__).resolve().parents[1] / "styles" / "practical" / "tokens.json").read_text(encoding="utf-8"))
W = TOKENS["body_frame_pt"]["x1"] - TOKENS["body_frame_pt"]["x0"]
P, G = 14.0, 14.0
CENTER_ZONE = 56.0


def _fence(before, after, center=None, **extra):
    d = {"layout": "before_after", "title": "전환 제목",
         "before": before, "after": after}
    if center:
        d["center"] = center
    d.update(extra)
    return parse_fence(1, 1, json.dumps(d, ensure_ascii=False))


def test_parse_rejects_empty_item():
    # 빈 항목은 after 측에 — 구현 에러문은 f"{side}[{i}]" (I1 정합)
    with pytest.raises(ParseError, match=r"after\[1\] 비어 있음"):
        _fence(["항목"], ["항목", "  "])


def test_parse_rejects_over_absolute_cap():
    with pytest.raises(ParseError, match=r"before 항목 수 6"):
        _fence([f"항목 {i}" for i in range(6)], ["항목"])


def test_alias_bridge_routes_to_before_after():
    body = json.dumps({"layout": "bridge", "title": "t",
                       "before": ["a"], "after": ["b"]}, ensure_ascii=False)
    f = parse_fence(1, 1, body)
    assert f.layout == "before_after"


def test_two_panels_and_center_arrow_practical():
    fig = ba_arch.layout(_fence(["문장 A", "문장 B"], ["문장 C", "문장 D", "문장 E"],
                                center="AI 도입"), TOKENS)
    panels = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
    assert len(panels) == 2
    panel_w = (W - 2 * P - CENTER_ZONE - 2 * G) / 2
    assert abs(panels[0].w - panel_w) < 0.01
    assert abs(panels[0].x - P) < 0.01
    assert abs(panels[1].x - (W - P - panel_w)) < 0.01
    assert panels[0].h == panels[1].h                      # 양측 동일 높이
    arrows = [o for o in fig.ops if isinstance(o, ArrowOp)]
    assert len(arrows) == 1
    a = arrows[0]
    assert a.x1 < a.x2 and abs(a.y1 - a.y2) < 0.01         # 수평
    assert a.x1 > panels[0].x + panels[0].w                # 좌패널 우변보다 오른쪽
    assert a.x2 < panels[1].x                              # 우패널 좌변보다 왼쪽
    fields = {t.field for t in fig.ops if isinstance(t, TextOp)}
    assert {"before[0]", "before[1]", "after[2]", "center", "before_label", "after_label"} <= fields


def test_panel_height_measured_multi_line_items():
    short = ba_arch.layout(_fence(["짧"], ["짧"]), TOKENS)
    long_ = ba_arch.layout(_fence(["근거 문장이 패널 폭을 넘어 두 줄 이상으로 감싸지는 긴 항목"], ["짧"]), TOKENS)
    p_short = [r for r in short.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"][0]
    p_long = [r for r in long_.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"][0]
    assert p_long.h > p_short.h + 5.0                      # 실측 반영 — 1줄 가정이면 차 0


def test_pack_cap_essay_rejects_four_items():
    essay = json.loads((Path(__file__).resolve().parents[1] / "styles" / "essay" / "tokens.json").read_text(encoding="utf-8"))
    with pytest.raises(ba_arch.BeforeAfterLayoutError, match=r"판형 상한 3개\(essay\)"):
        ba_arch.layout(_fence(["a", "b", "c", "d"], ["a"]), essay)


def test_pack_cap_success_all_packs():
    # I3 — 각 팩 상한 n에서 렌더 성공(상한 도달 가능성 실증, C1 방어)
    packs = {"essay": 3, "practical": 4, "b5": 4, "business": 5, "lecture": 5}
    for name, cap in packs.items():
        toks = json.loads((Path(__file__).resolve().parents[1] / "styles" / name / "tokens.json").read_text(encoding="utf-8"))
        fig = ba_arch.layout(_fence([f"이전 {i}" for i in range(cap)],
                                    [f"이후 {i}" for i in range(cap)], center="전환"), toks)
        panels = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
        assert len(panels) == 2, name


def test_height_limit_85pct():
    # 최종 리뷰 3 — 85% 높이 게이트: 4장문 항목/측(판형 상한 내) → 줄수 폭증
    # (n=5는 practical 판형 상한 에러가 먼저)
    long_text = "아주 긴 근거 문장이다 " * 8
    with pytest.raises(ba_arch.BeforeAfterLayoutError, match="85"):
        ba_arch.layout(_fence([long_text] * 4, [long_text] * 4), TOKENS)


def test_before_after_elements_reach_lint_and_sheet():
    # cards의 test_cards_lint_and_review_sheet_reach_elements 패턴을 그대로 따른다 —
    # 1) 숫자 포함 항목(before/after/center)이 I1 숫자-evidence 검사 대상에 들어가는지
    # 2) render._sheet_rows가 before[i]·after[i]·center·라벨 행을 반환하는지
    from scripts.infographic.lint import check
    from scripts.infographic.render import _review_sheet, _sheet_rows
    f = _fence(["예산 3배 증가", "리드타임 2주"], ["CAPEX 12% 절감"], center="전환",
               before_label="AS-IS", after_label="TO-BE")
    figs = {1: ba_arch.layout(f, TOKENS)}
    found = check([f], figs, TOKENS, "원문 없음", "ch01.md")
    assert any(x.kind == "number-evidence" and x.loc == "ch01.md #1 before[0]" for x in found)
    assert any(x.kind == "number-evidence" and x.loc == "ch01.md #1 after[0]" for x in found)
    rows = dict(_sheet_rows(f))
    assert {"before[0]", "before[1]", "after[0]", "center",
            "before_label", "after_label"} <= set(rows)
    sheet = _review_sheet(f, [])
    for path in ("before[0]", "after[0]", "center", "before_label", "after_label"):
        assert path in sheet


def test_before_after_golden_snapshot():
    # cards 골든 패턴(test_infographic_layout_cards.py:124-135) 복제 — I2:
    # emit 심볼은 render_typ(fig)뿐(emit.py:21), os는 파일 상단 임포트
    import os
    GOLDEN = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "infographic" / "golden-before-after-practical.typ"
    fig = ba_arch.layout(_fence(["리드타임 2주", "수작업 5단계"], ["리드타임 3일", "자동화 1단계"], center="AI 도입"), TOKENS)
    from scripts.infographic.emit import render_typ
    code = render_typ(fig)
    if os.environ.get("IG_REGEN_GOLDEN") != "1":
        if not GOLDEN.exists():
            pytest.fail("골든 없음 — `IG_REGEN_GOLDEN=1 python3 -m pytest …` 실행 후 눈검·커밋")
        assert code == GOLDEN.read_text(encoding="utf-8")
    else:
        GOLDEN.write_text(code, encoding="utf-8")
        pytest.fail("골든 재생성 — 눈검 후 커밋")
