"""layout.py — archetype 라우팅(스펙 §2 원칙 3: 빌드 자동판단 없음, fence.layout 명시만)."""
from __future__ import annotations

from .archetypes import (before_after as _ba, cards as _cards, flow as _flow,
                         ladder as _lad, matrix as _matrix)
from .parse import Fence


def dispatch(fence: Fence, tokens: dict):
    if fence.layout == "flow":
        return _flow.layout(fence, tokens)
    if fence.layout == "cards":
        return _cards.layout(fence, tokens)
    if fence.layout == "matrix":
        return _matrix.layout(fence, tokens)
    if fence.layout == "before_after":
        return _ba.layout(fence, tokens)
    if fence.layout == "ladder":
        return _lad.layout(fence, tokens)
    raise ValueError(f"지원하지 않는 layout: {fence.layout!r}")
