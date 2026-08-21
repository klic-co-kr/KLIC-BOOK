"""lint.py — I1 게이트(스펙 §5.2). 전수 검사 후 전건 반환: 빌드가 치명(fatal) 것만 모아 중단.
fatal=False(미검증류)은 빌드를 막지 않고 검수 시트로 이관한다(스펙 §3.3)."""
from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass

from . import budget, roles
from .model import (ARROW_HEAD_W, ARROW_STROKE_W, ArrowOp, FigModel,
                    RectOp, TextOp)
from .parse import Fence

NUM_RE = re.compile(r"[0-9][0-9.,%]*")
ORDINAL_RE = re.compile(r"제\d+[장절]")
CIRCLED = set("①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳")
ANY_FENCE_RE = re.compile(r"^```(\w[\w-]*)[ \t]*\n(.*?)^```[ \t]*$", re.S | re.M)

LEV_SHORTEN = "글자 축약"
LEV_FEWER = "요소 수 감소"
LEV_LAYOUT = "layout 변형(예: cards, 2행 랩)"
LEV_SPLIT = "펜스 분할"
MAX_LINES = 3              # 박스당 밀도 상한(스펙 §5.2-2 — "28자>22자"급 실측 보고)


@dataclass(frozen=True)
class LintFinding:
    kind: str
    loc: str
    measured: str
    levers: tuple
    fatal: bool = True


def _numbers_in(text: str) -> list[str]:
    text = ORDINAL_RE.sub("", text)
    text = "".join(ch for ch in text if ch not in CIRCLED)
    return NUM_RE.findall(text)


def _section_text(md: str, n: int) -> str | None:
    # N번째 ^## 헤딩부터 다음 ^## 전까지(스펙 §3.3 교차검증 범위)
    idx = [m.start() for m in re.finditer(r"^## ", md, flags=re.M)]
    if n < 1 or n > len(idx):
        return None
    end = idx[n] if n < len(idx) else len(md)
    return md[idx[n - 1]:end]


def check(fences: list[Fence], figs: dict[int, FigModel], tokens: dict,
          chapter_md: str, chapter_name: str) -> list[LintFinding]:
    # 펜스 마커의 순번 숫자(⟦IG:2⟧)가 원문에 없는 숫자를 우연 통과시킬 수
    # 있다 — 단일 지점 방어(strip). 호출자(render·cli)가 치환본을 넘겨도
    # 마커는 여기서 끊긴다(컨트롤러 판정).
    chapter_md = re.sub(r"⟦IG:\d+⟧", "", chapter_md)
    out: list[LintFinding] = []

    # 1. 토큰 존재(§5.2-7)
    info = tokens.get("infographic", {})
    for role in roles.REQUIRED_INFO_ROLES:
        if not isinstance(info.get(role), str):
            out.append(LintFinding("tokens", f"{chapter_name} tokens.infographic.{role}",
                                   "값 없음", ("스타일 팩에 5역할 정의",)))

    # 2. 펜스 위장 감지(§5.2-8) — 미등록 펜스 언어에 layout 키가 있으면 오타 의심
    for m in ANY_FENCE_RE.finditer(chapter_md):
        lang, body = m.group(1), m.group(2)
        if lang == "infographic":
            continue
        try:
            d = json.loads(body)
        except ValueError:
            continue
        if isinstance(d, dict) and "layout" in d:
            out.append(LintFinding(
                "fence-impostor", f"{chapter_name} 펜스언어:{lang}",
                f"```{lang} 내용이 layout 키 포함 JSON — infographic 오타 의심"
                "(그대로 두면 YAML이 코드블록으로 인쇄됨)",
                ("펜스 언어를 infographic으로 수정",)))

    # 3. 커넥터 상수(§5.2-4) — 헤드/샤프트 비 2.5~3.5 (1회 검증)
    ratio = ARROW_HEAD_W / ARROW_STROKE_W
    if not 2.5 <= ratio <= 3.5:
        out.append(LintFinding(
            "connector", f"{chapter_name} model.ARROW_HEAD_W",
            f"헤드/샤프트 비 {ratio:.2f} — 허용 2.5~3.5",
            ("ARROW_HEAD_W/ARROW_STROKE_W 상수 수정",)))

    body_size = tokens["fonts"]["body"]["size_pt"]
    # 예산 측정도 flow 배치와 같은 팩 계수로 — PACK_KO_FACTOR 교정(§7)이
    # 게이트에도 활성화된다(최종 리뷰 Important: 누락 시 잠재 위반).
    pack = tokens.get("style", "practical")
    section_cache: dict[str, str | None] = {}

    for f in fences:
        prefix = f"{chapter_name} #{f.index}"

        # 4. 숫자-evidence 교차검증(§3.3) — 미검증은 비치명
        fields: list[tuple[str, str]] = [("title", f.title)]
        if f.kicker:
            fields.append(("kicker", f.kicker))
        for i, s in enumerate(f.data.get("steps", [])):
            fields.append((f"steps[{i}].title", s["title"]))
            fields.append((f"steps[{i}].text", s["text"]))
        for i, c in enumerate(f.data.get("cards", [])):
            fields.append((f"cards[{i}].title", c["title"]))
            fields.append((f"cards[{i}].text", c["text"]))
            if "value" in c:
                fields.append((f"cards[{i}].value", c["value"]))
        for c, h in enumerate(f.data.get("headers", [])):
            fields.append((f"headers[{c}]", h))
        for r, row in enumerate(f.data.get("rows", [])):
            for c, cell in enumerate(row):
                fields.append((f"cell[{r}][{c}]", cell))
        for i, cell in enumerate(f.data.get("cells", [])):
            fields.append((f"cells[{i}].title", cell["title"]))
            fields.append((f"cells[{i}].text", cell["text"]))
        if "x_axis" in f.data:
            fields.append(("axis.x0", f.data["x_axis"]["low"]))
            fields.append(("axis.x1", f.data["x_axis"]["high"]))
        if "y_axis" in f.data:
            fields.append(("axis.y0", f.data["y_axis"]["low"]))
            fields.append(("axis.y1", f.data["y_axis"]["high"]))
        sec = None
        if f.evidence:
            if f.evidence not in section_cache:
                m = re.fullmatch(r"§(\d+)", f.evidence.strip())
                section_cache[f.evidence] = (
                    _section_text(chapter_md, int(m.group(1))) if m else None)
            sec = section_cache[f.evidence]
        for path, text in fields:
            nums = _numbers_in(text)
            if not nums:
                continue
            if not f.evidence:
                out.append(LintFinding(
                    "number-evidence", f"{prefix} {path}",
                    f"숫자 {nums} 존재, evidence 필드 없음",
                    ("원문 절 앵커 evidence 추가(예: \"§1\")",)))
            elif sec is None:
                out.append(LintFinding(
                    "number-unverified", f"{prefix} {path}",
                    f"숫자 {nums} — 미검증(evidence {f.evidence!r} 해석 불가·범위 밖) "
                    "→ 검수 시트 사람 대조 필수",
                    ("evidence를 §N 형식으로 바꾸거나 검수 시트에서 사람 대조",),
                    fatal=False))
            else:
                for num in nums:
                    if num not in sec:
                        out.append(LintFinding(
                            "number-evidence", f"{prefix} {path}",
                            f"숫자 {num!r} 원문(evidence {f.evidence})에 없음",
                            (LEV_SHORTEN, "원문에 있는 숫자로 교체")))

        # 5. FigModel ops — 예산(§5.2-2)·G3(§5.2-9)·커넥터(§5.2-4)
        fig = figs.get(f.index)
        if fig is None:
            continue
        cards = [o for o in fig.ops if isinstance(o, RectOp)
                 and o.fill_role == "surface-tint"]
        for op in fig.ops:
            if isinstance(op, TextOp):
                if op.max_w > 0 and op.field:
                    lines = budget.line_count(op.text, op.max_w, op.size, pack=pack)
                    if lines > MAX_LINES:
                        out.append(LintFinding(
                            "budget", f"{prefix} {op.field}",
                            f"예상 {lines}줄 > 밀도 상한 {MAX_LINES}줄 "
                            f"({budget.width_units(op.text):.0f}단위, 상자 {op.max_w:.0f}pt)",
                            (LEV_SHORTEN, LEV_FEWER, LEV_SPLIT)))
                if abs(op.size - body_size) <= 0.3:
                    out.append(LintFinding(
                        "g3-invariant", f"{prefix} {op.field or 'text'}",
                        f"크기 {op.size}pt — 본문 {body_size}pt±0.3 밖이어야 함",
                        ("크기 사다리 재검토(layout 버그)",)))
            elif isinstance(op, ArrowOp):
                length = math.hypot(op.x2 - op.x1, op.y2 - op.y1)
                if length < 12.0:
                    out.append(LintFinding(
                        "connector", f"{prefix} arrow({op.x1:.0f},{op.y1:.0f}→{op.x2:.0f},{op.y2:.0f})",
                        f"샤프트 가시 {length:.1f}pt < 12pt(§6.1)",
                        (LEV_LAYOUT, LEV_SPLIT)))
                for ex, ey in ((op.x1, op.y1), (op.x2, op.y2)):
                    for c in cards:
                        if c.x < ex < c.x + c.w and c.y < ey < c.y + c.h:
                            out.append(LintFinding(
                                "connector", f"{prefix} arrow→({ex:.0f},{ey:.0f})",
                                f"끝점이 카드({c.x:.0f},{c.y:.0f},{c.w:.0f}×{c.h:.0f}) "
                                "내부에 묻힘 — tip-gap 8~12pt 유지(§6.1)",
                                (LEV_LAYOUT,)))
    return out
