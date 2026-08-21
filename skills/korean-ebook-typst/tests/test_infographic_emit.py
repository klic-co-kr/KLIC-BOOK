"""test_infographic_emit.py — 방출 결정론·래퍼 계약·골든 스냅샷."""
import json
from pathlib import Path

import pytest

from scripts.infographic.archetypes import flow as flow_arch
from scripts.infographic.emit import render_typ
from scripts.infographic.parse import parse_fence

SKILL = Path(__file__).resolve().parents[1]
TOKENS = json.loads((SKILL / "styles" / "practical" / "tokens.json").read_text(encoding="utf-8"))
GOLDEN = SKILL / "tests" / "fixtures" / "infographic" / "golden-flow-practical.typ"

FENCE = parse_fence(1, 1, json.dumps({
    "layout": "flow", "title": "장애 대응은 5단계로 수렴한다",
    "steps": [
        {"title": "접수", "text": "장애 접수 등록"},
        {"title": "분류", "text": "영향도 기반 분류"},
    ],
}, ensure_ascii=False))


def test_emit_calls_helpers_no_hex():
    out = render_typ(flow_arch.layout(FENCE, TOKENS), TOKENS)
    assert '#import "../helper.typ"' in out          # fig는 build/infographic/에 있다(§2)
    assert "#ig-figure(" in out and "#ig-text(" in out
    assert "#EEF3F8" not in out and "#1F4E79" not in out   # hex 금지(§4.2) — 역할명만


def test_helper_has_wrapper_and_leading_contract():
    # 래퍼·leading 계약은 방출물이 아니라 helper.typ에 산다 — 파일 자체를 검사한다
    # (초판은 방출물에서 이 문자열을 찾아 절대 통과 불가였다 — 실증 정정).
    helper = (SKILL / "templates" / "infographic" / "helper.typ").read_text(encoding="utf-8")
    assert "breakable: false" in helper              # §5.1 래퍼
    assert "1.3em" in helper                         # §4.3 leading
    assert "#let pt(n) = n * 1pt" in helper          # pt 셈 — typst 0.15.1에 내장 없음(실증)


def test_emit_deterministic_bytes():
    a = render_typ(flow_arch.layout(FENCE, TOKENS), TOKENS)
    b = render_typ(flow_arch.layout(FENCE, TOKENS), TOKENS)
    assert a == b


def test_golden_snapshot():
    out = render_typ(flow_arch.layout(FENCE, TOKENS), TOKENS)
    if not GOLDEN.exists():
        # 골든은 테스트가 스스로 굳히지 않는다(자기충족 안티패턴 — 적대 검토 지적).
        # 확정 절차: IG_REGEN_GOLDEN=1으로 생성 → 눈검 → 함께 커밋. 그 전엔 실패.
        import os
        if os.environ.get("IG_REGEN_GOLDEN") != "1":
            pytest.fail("골든 없음 — `IG_REGEN_GOLDEN=1 python3 -m pytest …` 실행 후 "
                        "생성 파일을 눈검하고 커밋하라")
        GOLDEN.parent.mkdir(parents=True, exist_ok=True)
        GOLDEN.write_text(out, encoding="utf-8")
    assert out == GOLDEN.read_text(encoding="utf-8")
