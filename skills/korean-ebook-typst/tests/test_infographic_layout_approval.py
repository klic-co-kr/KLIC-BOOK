# tests/test_infographic_layout_approval.py — 스펙 §6.2·§6.3 approval 지오메트리·결정론.
"""test_infographic_layout_approval.py — 스펙 §6.2·§6.3 approval 지오메트리·결정론."""
import json
from pathlib import Path

import pytest

from scripts.infographic.archetypes import approval as appr_arch
from scripts.infographic.archetypes.approval import ApprovalLayoutError
from scripts.infographic.model import ArrowOp, RectOp
from scripts.infographic.parse import ParseError, parse_fence

TOKENS = json.loads((Path(__file__).resolve().parents[1] / "styles" / "practical" / "tokens.json").read_text(encoding="utf-8"))
ETOKENS = json.loads((Path(__file__).resolve().parents[1] / "styles" / "essay" / "tokens.json").read_text(encoding="utf-8"))


def _fence(n=4, gates=(1, 3), **extra):
    steps = [{"title": f"결재 단계 {i}", "text": "검토 후 진행", **({"gate": True} if i in gates else {})}
             for i in range(n)]
    payload = {"layout": "approval", "title": "결재 흐름 점검 제목", "path": steps}
    payload.update(extra)
    return parse_fence(1, 1, json.dumps(payload, ensure_ascii=False))


def test_parse_bounds():
    with pytest.raises(ParseError):
        _fence(n=2)                                       # 하한 3 미만
    with pytest.raises(ParseError):
        _fence(n=9)                                       # 절대 상한 8 초과
    with pytest.raises(ParseError):
        _fence(n=5, gates=(0, 1, 2, 3, 4))                # 게이트 5개 > 상한 4
    with pytest.raises(ParseError):
        parse_fence(1, 1, '{"layout":"approval","title":"t","path":['
                       '{"title":"기획"},{"text":"제목 누락"},{"title":"승인"}]}')
    with pytest.raises(ParseError):
        parse_fence(1, 1, '{"layout":"approval","title":"t","path":['
                       '{"title":"기획","gate":"예"},{"title":"검토"},{"title":"승인"}]}')  # gate 불리언 아님


def test_approval_step_geometry_and_gate_marker():
    fig = appr_arch.layout(_fence(n=4, gates=(1,)), TOKENS)
    rects = [o for o in fig.ops if isinstance(o, RectOp) and o.fill_role != "paper"]
    cards = [r for r in rects if r.w > 30.0]              # 마커(12pt)와 카드 분리
    markers = [r for r in rects if abs(r.w - 12.0) < 0.01]
    assert len(cards) == 4 and len(markers) == 1
    W = TOKENS["body_frame_pt"]["x1"] - TOKENS["body_frame_pt"]["x0"]
    step_w = (W - 28.0 - 3 * 28.0) / 4
    assert abs(cards[0].w - step_w) < 0.01
    assert abs(cards[1].x - (14.0 + step_w + 28.0)) < 0.01
    assert markers[0].rot == 45.0 and markers[0].rx == 0.0
    assert abs(markers[0].x + 6.0 - (cards[1].x + step_w / 2)) < 0.01  # 상단변 중심
    arrows = [o for o in fig.ops if isinstance(o, ArrowOp)]
    assert len(arrows) == 3 and all((a.x2 - a.x1) >= 12.0 - 0.01 for a in arrows)


def test_approval_step_width_floor():
    with pytest.raises(ApprovalLayoutError, match="스텝 폭"):
        appr_arch.layout(_fence(n=5), TOKENS)             # practical 5스텝 → 38.9pt < 48pt


def test_approval_essay_reach():
    # MIN_STEP_W 주석의 팩별 도달 한계 실측표 — essay는 3스텝(55.15pt)이 한계.
    appr_arch.layout(_fence(n=3), ETOKENS)
    with pytest.raises(ApprovalLayoutError, match="스텝 폭"):
        appr_arch.layout(_fence(n=4), ETOKENS)            # essay 4스텝 → 34.4pt < 48pt


def test_approval_determinism():
    f = _fence(n=4, gates=(1, 3))
    assert appr_arch.layout(f, TOKENS).ops == appr_arch.layout(f, TOKENS).ops


def test_approval_elements_reach_lint_and_sheet():
    # Task 2 topology 패턴과 동일 — lint.check 5인자·loc "{chapter} #{index} {필드}".
    from scripts.infographic.lint import check
    from scripts.infographic.render import _review_sheet, _sheet_rows
    f = _fence(n=4, gates=(1,))
    f.data["path"][0]["title"] = "기획 3일 안에 확정한다"
    figs = {1: appr_arch.layout(f, TOKENS)}
    found = check([f], figs, TOKENS, "원문 없음", "ch01.md")
    assert any(x.kind == "number-evidence" and x.loc == "ch01.md #1 path[0].title" for x in found)
    rows = dict(_sheet_rows(f))
    assert {"path[0].title", "path[1].title", "path[2].text", "path[3].title"} <= set(rows)
    sheet = _review_sheet(f, [])
    assert "path[1].title" in sheet


def test_approval_golden_snapshot():
    import os
    from scripts.infographic.emit import render_typ
    GOLDEN = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "infographic" / "golden-approval-practical.typ"
    payload = {"layout": "approval", "title": "결재는 검토를 거쳐 집행으로 이어진다",
               "kicker": "결재",
               "path": [{"title": "기획", "text": "방향을 정한다"},
                        {"title": "검토", "text": "위험을 점검한다", "gate": True},
                        {"title": "승인", "text": "권한이 확정된다"},
                        {"title": "집행", "text": "업무가 진행된다", "gate": True}]}
    # 4스텝·게이트 2(검토·집행에 45° 다이아몬드) — practical step_w 55.62pt(MIN 48 통과).
    f = parse_fence(1, 1, json.dumps(payload, ensure_ascii=False))
    code = render_typ(appr_arch.layout(f, TOKENS))
    if os.environ.get("IG_REGEN_GOLDEN") != "1":
        if not GOLDEN.exists():
            pytest.fail("골든 없음 — `IG_REGEN_GOLDEN=1 python3 -m pytest …` 실행 후 눈검·커밋")
        assert code == GOLDEN.read_text(encoding="utf-8")
    else:
        GOLDEN.parent.mkdir(parents=True, exist_ok=True)
        GOLDEN.write_text(code, encoding="utf-8")
        pytest.fail("골든 재생성 — 눈검 후 커밋")

