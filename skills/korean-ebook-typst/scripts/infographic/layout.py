"""layout.py — archetype 라우팅(스펙 §2 원칙 3: 빌드 자동판단 없음, fence.layout 명시만)."""
from __future__ import annotations

from .archetypes import cards as _cards, flow as _flow
from .parse import Fence


def dispatch(fence: Fence, tokens: dict):
    if fence.layout == "flow":
        return _flow.layout(fence, tokens)
    if fence.layout == "cards":
        return _cards.layout(fence, tokens)
    raise ValueError(f"지원하지 않는 layout: {fence.layout!r}")
