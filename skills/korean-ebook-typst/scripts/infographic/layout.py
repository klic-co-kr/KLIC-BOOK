"""layout.py — archetype 라우팅(스펙 §2 원칙 3: 빌드 자동판단 없음, fence.layout 명시만)."""
from __future__ import annotations

from .archetypes import (approval as _appr, before_after as _ba, cards as _cards,
                         flow as _flow, ladder as _lad, layers as _layers,
                         matrix as _matrix, roadmap as _rm, topology as _topo)
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
    if fence.layout == "roadmap":
        return _rm.layout(fence, tokens)
    if fence.layout == "topology":
        return _topo.layout(fence, tokens)
    if fence.layout == "approval":
        return _appr.layout(fence, tokens)
    if fence.layout == "layers":
        return _layers.layout(fence, tokens)
    raise ValueError(f"지원하지 않는 layout: {fence.layout!r}")
