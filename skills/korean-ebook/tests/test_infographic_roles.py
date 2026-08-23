"""test_infographic_roles.py — 스펙 §4.2: 5팩 모두 infographic 5역할 + roles.color 조회."""
import json
from pathlib import Path

import pytest

STYLES = Path(__file__).resolve().parents[1] / "styles"
PACKS = ["practical", "essay", "business", "lecture", "b5"]


def _tokens(pack: str) -> dict:
    return json.loads((STYLES / pack / "tokens.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("pack", PACKS)
def test_every_pack_has_five_info_roles(pack):
    info = _tokens(pack).get("infographic")
    assert isinstance(info, dict), f"{pack}: infographic 섹션 없음"
    for role in ("surface-tint", "focus", "positive", "warning", "on-focus"):
        v = info.get(role)
        assert isinstance(v, str) and v.startswith("#") and len(v) == 7, \
            f"{pack}.{role}: hex 6자리 필요, 값={v!r}"


def test_color_resolves_base_and_info_roles():
    from scripts.infographic import roles
    t = _tokens("practical")
    assert roles.color(t, "accent") == "#1F4E79"
    assert roles.color(t, "surface-tint") == "#EEF3F8"


def test_color_unknown_role_raises():
    from scripts.infographic import roles
    with pytest.raises(KeyError):
        roles.color(_tokens("practical"), "nope")
