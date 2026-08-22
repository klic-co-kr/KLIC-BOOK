"""test_infographic_layout_ladder.py — 스펙 §6.2·§6.3 ladder 계단 지오메트리."""
import json
from pathlib import Path

import pytest

from scripts.infographic.archetypes import ladder as ladder_arch
from scripts.infographic.model import ArrowOp, RectOp, TextOp
from scripts.infographic.parse import ParseError, parse_fence

TOKENS = json.loads((Path(__file__).resolve().parents[1] / "styles" / "practical" / "tokens.json").read_text(encoding="utf-8"))
W = TOKENS["body_frame_pt"]["x1"] - TOKENS["body_frame_pt"]["x0"]
P = 14.0


def _fence(n):
    stages = [{"title": f"단계 {i+1}", "text": "근거 문장"} for i in range(n)]
    return parse_fence(1, 1, json.dumps(
        {"layout": "ladder", "title": "성숙도 사다리", "stages": stages}, ensure_ascii=False))


def test_parse_bounds():
    with pytest.raises(ParseError, match="stages 개수 2"):
        _fence(2)
    with pytest.raises(ParseError, match="stages 개수 6"):
        _fence(6)


def test_no_pack_cap_only_absolute():
    # ladder는 판형 상한 없음 — practical 5단계(절대 상한)가 레이아웃 에러 없이 통과
    # (C4a: essay 5단계는 폭 249pt에서 dy<16 에러 — 도달 불가 조합이므로 practical 사용)
    fig = ladder_arch.layout(_fence(5), TOKENS)    # 예외 없음 자체가 검증
    assert fig.height > 0


def test_stair_offsets_both_axes():
    fig = ladder_arch.layout(_fence(4), TOKENS)
    boxes = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
    assert len(boxes) == 4
    box_w = boxes[0].w
    avail = W - 2 * P
    assert abs(box_w - 0.56 * avail) < 0.01                    # BOX_W_FRAC 0.56 고정
    dx = (avail - box_w) / 3
    for i in range(4):
        assert abs(boxes[i].x - (P + i * dx)) < 0.01          # x 단조 증가
        assert abs(boxes[i].w - box_w) < 0.01
    for i in range(3):
        assert boxes[i + 1].y + boxes[i + 1].h < boxes[i].y   # y 단조 상승(하→상)
    arrows = [o for o in fig.ops if isinstance(o, ArrowOp)]
    assert len(arrows) == 3                                    # 계단 연결선
    a = arrows[0]
    assert a.x2 > a.x1 and a.y2 < a.y1                         # 우상향 대각


def test_box_height_measured():
    fig = ladder_arch.layout(_fence(3), TOKENS)
    boxes = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
    assert boxes[0].h == boxes[1].h == boxes[2].h              # 최대 단계 높이 통일


def test_step_gap_error_on_tall_stages():
    # C4b: ladder의 공간 부족 에러는 dy<STEP_GAP_MIN 경로 — 85% 분기는
    # H_avail 산식상 도달 불가(구조적 불변식 검사로만 존재)
    long_text = "근거 문장이 상자 폭을 넘어 여러 줄로 감싸지는 매우 긴 문장입니다 " * 6
    stages = [{"title": f"단계 {i+1}", "text": long_text} for i in range(5)]
    f = parse_fence(1, 1, json.dumps(
        {"layout": "ladder", "title": "성숙도", "stages": stages}, ensure_ascii=False))
    with pytest.raises(ladder_arch.LadderLayoutError, match="단 간격"):
        ladder_arch.layout(f, TOKENS)


def test_ladder_golden_snapshot():
    # cards 골든 패턴(test_infographic_layout_cards.py:124-135) 복제 — I2:
    # emit 심볼은 render_typ(fig)뿐(emit.py:21), os는 파일 상단 임포트
    import os
    GOLDEN = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "infographic" / "golden-ladder-practical.typ"
    fig = ladder_arch.layout(_fence(4), TOKENS)
    from scripts.infographic.emit import render_typ
    code = render_typ(fig)
    if os.environ.get("IG_REGEN_GOLDEN") != "1":
        if not GOLDEN.exists():
            pytest.fail("골든 없음 — `IG_REGEN_GOLDEN=1 python3 -m pytest …` 실행 후 눈검·커밋")
        assert code == GOLDEN.read_text(encoding="utf-8")
    else:
        GOLDEN.write_text(code, encoding="utf-8")
        pytest.fail("골든 재생성 — 눈검 후 커밋")
