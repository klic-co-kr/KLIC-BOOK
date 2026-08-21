"""model.py — 도식 draw ops(스펙 §2). emit은 이 ops만 소비한다."""
from __future__ import annotations

from dataclasses import dataclass

ARROW_STROKE_W = 1.2
ARROW_HEAD_W = 4.0          # /1.2 = 3.33 — §5.2-4 허용 2.5~3.5


@dataclass(frozen=True)
class RectOp:
    x: float; y: float; w: float; h: float
    rx: float = 8.0
    fill_role: str = "surface-tint"
    stroke_role: str = "rule"
    stroke_w: float = 0.5


@dataclass(frozen=True)
class TextOp:
    x: float; y: float          # 텍스트 블록 중심점(절대좌표)
    size: float
    text: str
    role: str = "ink"
    weight: str = "regular"
    max_w: float = 0.0          # 예산 검사용 상자 폭(0=검사 생략)
    field: str = ""             # I1 위치 계약용 필드 경로(예: steps[1].title)


@dataclass(frozen=True)
class ArrowOp:
    x1: float; y1: float; x2: float; y2: float
    style: str = "solid"        # solid=순차, dashed=참조(§6.1)


@dataclass(frozen=True)
class FigModel:
    width: float
    height: float
    ops: tuple
    source_index: int           # 펜스 순번 — lint 위치 표기용
