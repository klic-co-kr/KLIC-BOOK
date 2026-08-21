"""parse.py — 펜스 JSON → Fence 모델 + 상태 기계(스펙 §3.1·§3.4). 표준 라이브러리만."""
from __future__ import annotations

import json
from dataclasses import dataclass

DEFAULT_NOTE = ("편집 요약: 본문의 장·절 구조와 핵심 문장을 재배열한 도식이며, "
                "원문을 대체하지 않습니다.")

# 스펙 §3.4 — 구시스템 별칭 → 규범 키워드
ALIASES = {"process": "flow"}
VALID_LAYOUTS = {"flow"}          # Phase 1. 이후 Task에서 확장
STEP_MIN, STEP_MAX = 2, 8


class ParseError(Exception):
    def __init__(self, fence_index: int, detail: str, line: int = 0):
        # 라인은 펜스 시작 라인 — 메시지에 포함해 저작자가 펜스를 바로 찾게 한다(§3.4).
        super().__init__(f"#{fence_index}(ch 라인 {line}): {detail}")
        self.fence_index = fence_index
        self.detail = detail
        self.line = line


@dataclass(frozen=True)
class Fence:
    index: int
    line: int
    layout: str
    title: str
    thesis: str | None
    kicker: str | None
    note: str | None
    evidence: str | None
    data: dict


def normalize(text: str) -> str:
    return text.replace("﻿", "").replace("\r\n", "\n").replace("\r", "\n")


def parse_fence(index: int, line: int, body: str) -> Fence:
    if not body.strip():
        raise ParseError(index, "빈 펜스 — layout·title·steps를 넣어라", line)
    try:
        d = json.loads(body)
        if not isinstance(d, dict):
            raise ValueError("펜스 내용이 JSON 객체가 아님")
    except ValueError as exc:
        raise ParseError(index, f"JSON 파싱 실패: {exc}", line) from exc

    raw_layout = str(d.get("layout", "")).strip()
    alias = raw_layout in ALIASES
    layout = ALIASES.get(raw_layout, raw_layout)
    if layout not in VALID_LAYOUTS:
        raise ParseError(index, f"unknown layout {raw_layout!r} (가능: flow)", line)

    title = str(d.get("title", "")).strip()
    if not title:
        raise ParseError(index, "title 필수 — 결론형 제목을 넣어라", line)

    def opt(key: str) -> str | None:
        v = d.get(key)
        return str(v).strip() if isinstance(v, str) and v.strip() else None

    data: dict = dict(steps=[])
    steps = d.get("steps", [])
    if not isinstance(steps, list) or not (STEP_MIN <= len(steps) <= STEP_MAX):
        raise ParseError(index, f"steps 개수 {len(steps) if isinstance(steps, list) else 0} — 하한 {STEP_MIN}, 상한 {STEP_MAX}", line)
    for i, s in enumerate(steps):
        if not isinstance(s, dict):
            raise ParseError(index, f"steps[{i}] 객체 아님", line)
        t = str(s.get("title", "")).strip()
        x = str(s.get("text", "")).strip()
        if not t or not x:
            raise ParseError(index, f"steps[{i}].title/.text 비어 있음 — 근거 문구를 넣어라", line)
        data["steps"].append({"title": t, "text": x})
    if alias:
        data["_alias"] = raw_layout

    return Fence(
        index=index, line=line, layout=layout, title=title,
        thesis=opt("thesis"), kicker=opt("kicker"),
        note=opt("note"), evidence=opt("evidence"), data=data,
    )
