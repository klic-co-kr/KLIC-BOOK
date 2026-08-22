"""parse.py — 펜스 JSON → Fence 모델 + 상태 기계(스펙 §3.1·§3.4). 표준 라이브러리만."""
from __future__ import annotations

import json
from dataclasses import dataclass

DEFAULT_NOTE = ("편집 요약: 본문의 장·절 구조와 핵심 문장을 재배열한 도식이며, "
                "원문을 대체하지 않습니다.")

# 스펙 §3.4 — 구시스템 별칭 → 규범 키워드
ALIASES = {"process": "flow", "principles": "cards", "dashboard": "cards",
           "quadrant": "matrix", "bridge": "before_after", "network": "topology"}
VALID_LAYOUTS = {"flow", "cards", "matrix", "before_after", "ladder", "roadmap",
                 "topology", "approval", "layers"}   # Phase 1·2·3·4
STEP_MIN, STEP_MAX = 2, 8
CARD_MIN, CARD_MAX = 2, 6
LANE_MIN, LANE_MAX = 2, 4      # lanes 레인 수·레인당 steps 공용(스펙 §3.2)
BA_ITEM_MIN, BA_ITEM_MAX = 1, 5          # 스펙 §3.2 before_after 항목/측
STAGE_MIN, STAGE_MAX = 3, 5              # 스펙 §3.2 ladder — 절대 상한만(판형 표 부재)
PHASE_MIN, PHASE_MAX = 2, 5              # 스펙 §3.2 roadmap 위상
PHASE_ITEMS_MIN, PHASE_ITEMS_MAX = 1, 4  # 플랜 결정 — 높이 예산 보호
NODE_MIN, NODE_MAX = 3, 8                # 스펙 §3.2 topology 절대 상한(판형 상한은 archetype)
PATH_MIN, PATH_MAX = 3, 8                # 스펙 §3.2 approval 경로 스텝
GATE_MAX = 4                             # 스펙 §3.2 approval 게이트 상한
LAYER_MIN, LAYER_MAX = 2, 6              # 스펙 §3.2 layers 계층 수(stack·rings 공용)


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
    if layout == "ladder":
        stages = d.get("stages", [])
        if not isinstance(stages, list) or not (STAGE_MIN <= len(stages) <= STAGE_MAX):
            n = len(stages) if isinstance(stages, list) else 0
            raise ParseError(index, f"stages 개수 {n} — 하한 {STAGE_MIN}, 상한 {STAGE_MAX}(스펙 §3.2)", line)
        for i, s in enumerate(stages):
            if not isinstance(s, dict):
                raise ParseError(index, f"stages[{i}] 객체 아님", line)
            if not str(s.get("title", "")).strip() or not str(s.get("text", "")).strip():
                raise ParseError(index, f"stages[{i}].title/.text 비어 있음", line)
        data["stages"] = [{"title": str(s["title"]).strip(), "text": str(s["text"]).strip()}
                          for s in stages]
    if layout == "roadmap":
        phases = d.get("phases", [])
        if not isinstance(phases, list) or not (PHASE_MIN <= len(phases) <= PHASE_MAX):
            n = len(phases) if isinstance(phases, list) else 0
            raise ParseError(index, f"phases 개수 {n} — 하한 {PHASE_MIN}, 상한 {PHASE_MAX}(스펙 §3.2)", line)
        for i, p in enumerate(phases):
            if not isinstance(p, dict):
                raise ParseError(index, f"phases[{i}] 객체 아님", line)
            if not str(p.get("period", "")).strip() or not str(p.get("title", "")).strip():
                raise ParseError(index, f"phases[{i}].period/.title 비어 있음", line)
            items = p.get("items", [])
            if not isinstance(items, list) or not (PHASE_ITEMS_MIN <= len(items) <= PHASE_ITEMS_MAX):
                m = len(items) if isinstance(items, list) else 0
                raise ParseError(index, f"phases[{i}].items 개수 {m} — 하한 {PHASE_ITEMS_MIN}, 상한 {PHASE_ITEMS_MAX}", line)
            for j, it in enumerate(items):
                if not str(it).strip():
                    raise ParseError(index, f"phases[{i}].items[{j}] 비어 있음", line)
        data["phases"] = [{"period": str(p["period"]).strip(), "title": str(p["title"]).strip(),
                           "items": [str(it).strip() for it in p["items"]]} for p in phases]
    if layout == "topology":
        nodes = d.get("nodes", [])
        if not isinstance(nodes, list) or not (NODE_MIN <= len(nodes) <= NODE_MAX):
            n = len(nodes) if isinstance(nodes, list) else 0
            raise ParseError(index, f"nodes 개수 {n} — 하한 {NODE_MIN}, 상한 {NODE_MAX}", line)
        seen = set()
        for i, nd in enumerate(nodes):
            if (not isinstance(nd, dict) or not isinstance(nd.get("id"), str)
                    or not isinstance(nd.get("label"), str) or not nd["id"].strip() or not nd["label"].strip()):
                raise ParseError(index, f"nodes[{i}] id·label 비빈 문자열 필요", line)
            if nd["id"].strip() in seen:
                raise ParseError(index, f"노드 id 중복: {nd['id'].strip()}", line)
            seen.add(nd["id"].strip())
        edges = d.get("edges", [])
        if not isinstance(edges, list):
            raise ParseError(index, "edges는 배열 필요", line)
        eset = set()
        norm_edges = []
        for i, e in enumerate(edges):
            if (not isinstance(e, dict) or str(e.get("from", "")).strip() not in seen
                    or str(e.get("to", "")).strip() not in seen):
                raise ParseError(index, f"edges[{i}].from/.to는 노드 id 참조 필요", line)
            fr, to = str(e["from"]).strip(), str(e["to"]).strip()
            if fr == to:
                raise ParseError(index, f"자기 간선 금지: {fr}", line)
            if (fr, to) in eset:
                raise ParseError(index, f"간선 중복: {fr}→{to}", line)
            eset.add((fr, to))
            if "dashed" in e and not isinstance(e["dashed"], bool):
                raise ParseError(index, f"edges[{i}].dashed는 불리언", line)
            norm_edges.append({"from": fr, "to": to,
                               **({"dashed": e["dashed"]} if e.get("dashed") else {})})
        data["nodes"] = [{"id": str(nd["id"]).strip(), "label": str(nd["label"]).strip()}
                         for nd in nodes]
        data["edges"] = norm_edges
    if layout == "approval":
        path = d.get("path", [])
        if not isinstance(path, list) or not (PATH_MIN <= len(path) <= PATH_MAX):
            n = len(path) if isinstance(path, list) else 0
            raise ParseError(index, f"path 개수 {n} — 하한 {PATH_MIN}, 상한 {PATH_MAX}", line)
        gates = 0
        norm = []
        for i, st in enumerate(path):
            if not isinstance(st, dict) or not str(st.get("title", "")).strip():
                raise ParseError(index, f"path[{i}].title 필수", line)
            if "gate" in st and not isinstance(st["gate"], bool):
                raise ParseError(index, f"path[{i}].gate는 불리언", line)
            row = {"title": str(st["title"]).strip()}
            if str(st.get("text", "")).strip():
                row["text"] = str(st["text"]).strip()
            if st.get("gate"):
                row["gate"] = True
                gates += 1
            norm.append(row)
        if gates > GATE_MAX:
            raise ParseError(index, f"게이트 {gates}개 > 상한 {GATE_MAX}개 — 게이트 통합", line)
        data["path"] = norm
    if layout == "layers":
        stack, rings = d.get("stack"), d.get("rings")
        if (stack is None) == (rings is None):
            raise ParseError(index, "stack·rings 중 정확히 하나 필요", line)
        rows = stack if stack is not None else rings
        if not isinstance(rows, list) or not (LAYER_MIN <= len(rows) <= LAYER_MAX):
            n = len(rows) if isinstance(rows, list) else 0
            raise ParseError(index, f"계층 수 {n} — 하한 {LAYER_MIN}, 상한 {LAYER_MAX}", line)
        for i, row in enumerate(rows):
            if not isinstance(row, dict) or not str(row.get("label", "")).strip():
                raise ParseError(index, f"계층 label 필수 — rows[{i}]", line)
        key = "stack" if stack is not None else "rings"
        data[key] = [{"label": str(r["label"]).strip()} for r in rows]
    if alias:
        data["_alias"] = raw_layout

    return Fence(
        index=index, line=line, layout=layout, title=title,
        thesis=opt("thesis"), kicker=opt("kicker"),
        note=opt("note"), evidence=opt("evidence"), data=data,
    )
