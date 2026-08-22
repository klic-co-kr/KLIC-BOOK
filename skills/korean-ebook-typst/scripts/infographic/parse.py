"""parse.py — 펜스 JSON → Fence 모델 + 상태 기계(스펙 §3.1·§3.4). 표준 라이브러리만."""
from __future__ import annotations

import json
from dataclasses import dataclass

DEFAULT_NOTE = ("편집 요약: 본문의 장·절 구조와 핵심 문장을 재배열한 도식이며, "
                "원문을 대체하지 않습니다.")

# 스펙 §3.4 — 구시스템 별칭 → 규범 키워드
ALIASES = {"process": "flow", "principles": "cards", "dashboard": "cards",
           "quadrant": "matrix", "bridge": "before_after"}
VALID_LAYOUTS = {"flow", "cards", "matrix", "before_after"}   # Phase 1·2·3
STEP_MIN, STEP_MAX = 2, 8
CARD_MIN, CARD_MAX = 2, 6
LANE_MIN, LANE_MAX = 2, 4      # lanes 레인 수·레인당 steps 공용(스펙 §3.2)
BA_ITEM_MIN, BA_ITEM_MAX = 1, 5          # 스펙 §3.2 before_after 항목/측


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
        raise ParseError(index,
                         f"unknown layout {raw_layout!r} (가능: {', '.join(sorted(VALID_LAYOUTS))})", line)

    title = str(d.get("title", "")).strip()
    if not title:
        raise ParseError(index, "title 필수 — 결론형 제목을 넣어라", line)

    def opt(key: str) -> str | None:
        v = d.get(key)
        return str(v).strip() if isinstance(v, str) and v.strip() else None

    data: dict = dict(steps=[])
    if layout == "flow":
        has_steps, has_lanes = "steps" in d, "lanes" in d
        if has_steps and has_lanes:
            raise ParseError(index, "steps와 lanes는 배타 — 하나만 넣어라", line)
        if has_lanes:
            lanes = d["lanes"]
            if not isinstance(lanes, list) or not (LANE_MIN <= len(lanes) <= LANE_MAX):
                raise ParseError(index, f"lanes 개수 {len(lanes) if isinstance(lanes, list) else 0} — 하한 {LANE_MIN}, 상한 {LANE_MAX}", line)
            for i, ln in enumerate(lanes):
                if not isinstance(ln, dict) or not str(ln.get("actor", "")).strip():
                    raise ParseError(index, f"lanes[{i}].actor 필수 — 레인 주체를 넣어라", line)
                sts = ln.get("steps", [])
                if not isinstance(sts, list) or not (LANE_MIN <= len(sts) <= LANE_MAX):
                    raise ParseError(index, f"lanes[{i}].steps 개수 {len(sts) if isinstance(sts, list) else 0} — 하한 {LANE_MIN}, 상한 {LANE_MAX}", line)
                for j, s in enumerate(sts):
                    if not isinstance(s, dict) or not str(s.get("title", "")).strip() or not str(s.get("text", "")).strip():
                        raise ParseError(index, f"lanes[{i}].steps[{j}].title/.text 비어 있음", line)
            data["lanes"] = [{"actor": str(ln["actor"]).strip(),
                              "steps": [{"title": str(s["title"]).strip(),
                                         "text": str(s["text"]).strip()} for s in ln["steps"]]}
                             for ln in lanes]
        else:
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
    if layout == "cards":
        cards_l = d.get("cards", [])
        if not isinstance(cards_l, list) or not (CARD_MIN <= len(cards_l) <= CARD_MAX):
            raise ParseError(index, f"cards 개수 {len(cards_l) if isinstance(cards_l, list) else 0} — 하한 {CARD_MIN}, 상한 {CARD_MAX}", line)
        for i, c in enumerate(cards_l):
            if not isinstance(c, dict):
                raise ParseError(index, f"cards[{i}] 객체 아님", line)
            if not str(c.get("title", "")).strip() or not str(c.get("text", "")).strip():
                raise ParseError(index, f"cards[{i}].title/.text 비어 있음", line)
        data["cards"] = [{"title": str(c["title"]).strip(), "text": str(c["text"]).strip(),
                          **({"value": str(c["value"]).strip()} if str(c.get("value", "")).strip() else {})}
                         for c in cards_l]
    if layout == "matrix":
        if "headers" in d:
            headers = d["headers"]
            rows = d.get("rows", [])
            if not isinstance(headers, list) or not (2 <= len(headers) <= 5):
                raise ParseError(index, f"headers 개수 — 하한 2, 상한 5", line)
            if not isinstance(rows, list) or not (2 <= len(rows) <= 6):
                raise ParseError(index, "rows 개수 — 하한 2(스펙 §3.2), 상한 6", line)
            for r, row in enumerate(rows):
                if not isinstance(row, list) or len(row) != len(headers):
                    raise ParseError(index, f"rows[{r}] 열 수 불일치(headers {len(headers)}열)", line)
                for c, cell in enumerate(row):
                    if not str(cell).strip():
                        raise ParseError(index, f"rows[{r}][{c}] 비어 있음", line)
            data["headers"] = [str(h).strip() for h in headers]
            data["rows"] = [[str(c).strip() for c in row] for row in rows]
        else:
            for k in ("x_axis", "y_axis"):
                ax = d.get(k)
                if not isinstance(ax, dict) or not str(ax.get("low", "")).strip() or not str(ax.get("high", "")).strip():
                    raise ParseError(index, f"{k}.low/.high 필수", line)
            cells = d.get("cells", [])
            if not isinstance(cells, list) or len(cells) != 4:
                raise ParseError(index, "cells 정확히 4개(2×2)", line)
            for i, c in enumerate(cells):
                if not isinstance(c, dict) or not str(c.get("title", "")).strip() or not str(c.get("text", "")).strip():
                    raise ParseError(index, f"cells[{i}].title/.text 비어 있음", line)
            data["x_axis"] = {"low": str(d["x_axis"]["low"]).strip(), "high": str(d["x_axis"]["high"]).strip()}
            data["y_axis"] = {"low": str(d["y_axis"]["low"]).strip(), "high": str(d["y_axis"]["high"]).strip()}
            data["cells"] = [{"title": str(c["title"]).strip(), "text": str(c["text"]).strip()} for c in cells]
    if layout == "before_after":
        for side in ("before", "after"):
            items = d.get(side, [])
            if not isinstance(items, list) or not (BA_ITEM_MIN <= len(items) <= BA_ITEM_MAX):
                n = len(items) if isinstance(items, list) else 0
                raise ParseError(index, f"{side} 항목 수 {n} — 하한 {BA_ITEM_MIN}, 상한 {BA_ITEM_MAX}(스펙 §3.2)", line)
            for i, it in enumerate(items):
                if not str(it).strip():
                    raise ParseError(index, f"{side}[{i}] 비어 있음", line)
            data[side] = [str(it).strip() for it in items]
        center = str(d.get("center", "")).strip()
        if center:
            data["center"] = center
        for k in ("before_label", "after_label"):
            v = str(d.get(k, "")).strip()
            if v:
                data[k] = v
    if alias:
        data["_alias"] = raw_layout

    return Fence(
        index=index, line=line, layout=layout, title=title,
        thesis=opt("thesis"), kicker=opt("kicker"),
        note=opt("note"), evidence=opt("evidence"), data=data,
    )
