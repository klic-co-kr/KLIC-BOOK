"""render.py — 책 단위 펜스 렌더 오케스트레이션(스펙 §2 [2]).
I1 치명 위반은 전건 모아 중단. ParseError·LayoutError(archetype 공통 베이스)도
finding으로 변환해 전수 집계한다(초판은 첫 위반 traceback 크래시였다 — 적대 검토 정정)."""
from __future__ import annotations

import json
from pathlib import Path

from . import emit, layout, lint
from .archetypes.base import LayoutError
from .parse import DEFAULT_NOTE, ParseError, parse_fence

try:
    import md2typst  # 빌드 서브프로세스 컨텍스트 — scripts/가 sys.path에 있다
except ImportError:  # scripts.* 패키지로 임포트되는 테스트 환경(qc_gate 관례)
    from scripts import md2typst


class I1Error(Exception):
    def __init__(self, findings):
        self.findings = findings      # super()보다 먼저 — report()가 self.findings를 참조한다
        super().__init__(self.report())

    def report(self) -> str:
        lines = ["[I1] 인포그래픽 린트 위반 — 전건:"]
        for f in self.findings:
            lines.append(f"  [{f.kind}] {f.loc} — {f.measured} → 제안: {', '.join(f.levers)}")
        return "\n".join(lines)


def render_book_fences(book_dir: Path, build: Path, cfg: dict) -> dict[int, dict[int, str]]:
    out_dir = build / "infographic"
    out_dir.mkdir(parents=True, exist_ok=True)
    tokens = json.loads((build / "tokens.json").read_text(encoding="utf-8"))
    all_findings: list[lint.LintFinding] = []
    parsed_by_chapter: dict[int, tuple] = {}

    for idx, ch in enumerate(cfg["chapters"]):
        # 펜스 소스는 원고 md 단일 진실 — build/fences/<stem>.fences.json 사이드카를
        # 다시 읽으면 동명 스템 챕터(part1/ch01.md vs part2/ch01.md)가 마지막
        # 작성자로 서로를 덮어써 한쪽 도식이 조용히 뒤바뀐다(최종 리뷰 Critical 1).
        # 사이드카는 md2typst가 계속 쓰되 저작 디버그 용도로만 쓰인다.
        # §3.3 교차검증은 본문 산문 기준 — 펜스 자기 JSON이 자기 숫자의
        # 근거로 승격되면 검증이 무치화된다(자기참조, 컨트롤러 판정).
        # 펜스를 ⟦IG:N⟧ 마커로 치환한 본을 넘긴다(마커는 lint.check 내부 strip).
        chapter_md, fences_raw = md2typst.extract_fences(
            (book_dir / ch).read_text(encoding="utf-8"))
        if not fences_raw:
            continue
        # 챕터 위치 라벨도 인덱스 prefix로 — 동명 파일(ch01.md 2개)의 loc 모호성 제거.
        chapter_name = f"{idx:03d}-{Path(ch).name}"
        fences = []
        for raw in fences_raw:
            try:
                fences.append(parse_fence(raw["index"], raw["line"], raw["body"]))
            except ParseError as e:
                all_findings.append(lint.LintFinding(
                    "schema", f"{chapter_name} #{e.fence_index}", e.detail,
                    ("펜스 JSON 스키마 수정",)))
        figs = {}
        for f in fences:
            try:
                figs[f.index] = layout.dispatch(f, tokens)
            except LayoutError as e:
                all_findings.append(lint.LintFinding(
                    "layout", f"{chapter_name} #{f.index}", e.detail,
                    ("글자 축약", "요소 수 감소", "펜스 분할")))
        all_findings.extend(lint.check(fences, figs, tokens, chapter_md, chapter_name))
        parsed_by_chapter[idx] = (fences, figs, chapter_name)

    fatal = [f for f in all_findings if f.fatal]
    if fatal:
        raise I1Error(fatal)

    result: dict[int, dict[int, str]] = {}
    for idx, (fences, figs, chapter_name) in parsed_by_chapter.items():
        emits: dict[int, str] = {}
        for f in fences:
            fig = figs[f.index]
            name = f"{idx:03d}-fig{f.index:02d}.typ"
            # #context 필수 — typst 0.15.1은 context 없는 metadata가
            # "can only be used when context is known" 컴파일 에러로 전 도식을
            # 깨뜨린다(검토 G3-C1 실증). 프리픽스는 파일에만 붙는다 — standalone
            # 골든(emit.render_typ 출력) 바이트는 불변.
            (out_dir / name).write_text(
                f'#context metadata((kind: "ig-fig", name: "{name}", '
                f'page: here().page()))\n' + emit.render_typ(fig), encoding="utf-8")
            unverified = [x for x in all_findings
                          if x.kind == "number-unverified"
                          and x.loc.startswith(f"{chapter_name} #{f.index} ")]
            (out_dir / name.replace(".typ", ".review.md")).write_text(
                _review_sheet(f, unverified), encoding="utf-8")
            emits[f.index] = name
        result[idx] = emits
    # §5.4 개정 6판 — qc_gate의 typst query 페이지 대응이 짝지을 이름·챕터·인덱스.
    manifest = {"count": sum(len(e) for e in result.values()),
                "figs": [{"name": nm, "chapter": idx, "index": fi}
                         for idx, emits in result.items() for fi, nm in emits.items()]}
    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    return result


def rows_from(title: str, kicker: str | None, thesis: str | None, data: dict,
              prefix: str = "") -> list[tuple[str, str]]:
    """펜스 필드 평탄 수집(검수 시트 5열 계약용 2-튜플) — composite 모듈
    전개가 같은 본체를 prefix로 재사용한다(lint.rows_from과 경로 관계 공용)."""
    rows = [(f"{prefix}title", title), (f"{prefix}kicker", kicker or "—"),
            (f"{prefix}thesis", thesis or "—")]
    for i, s in enumerate(data.get("steps", [])):
        rows.append((f"{prefix}steps[{i}].title", s["title"]))
        rows.append((f"{prefix}steps[{i}].text", s["text"]))
    for i, ln in enumerate(data.get("lanes", [])):
        rows.append((f"{prefix}lanes[{i}].actor", ln["actor"]))
        for j, s in enumerate(ln["steps"]):
            rows.append((f"{prefix}lanes[{i}].steps[{j}].title", s["title"]))
            rows.append((f"{prefix}lanes[{i}].steps[{j}].text", s["text"]))
    for i, c in enumerate(data.get("cards", [])):
        rows.append((f"{prefix}cards[{i}].title", c["title"]))
        rows.append((f"{prefix}cards[{i}].text", c["text"]))
        if "value" in c:
            rows.append((f"{prefix}cards[{i}].value", c["value"]))
    for side in ("before", "after"):
        for i, it in enumerate(data.get(side, [])):
            rows.append((f"{prefix}{side}[{i}]", it))
    if data.get("center"):
        rows.append((f"{prefix}center", data["center"]))
    for k in ("before_label", "after_label"):
        if data.get(k):
            rows.append((f"{prefix}{k}", data[k]))
    for i, s in enumerate(data.get("stages", [])):
        rows.append((f"{prefix}stages[{i}].title", s["title"]))
        rows.append((f"{prefix}stages[{i}].text", s["text"]))
    for i, p in enumerate(data.get("phases", [])):
        rows.append((f"{prefix}phases[{i}].period", p["period"]))
        rows.append((f"{prefix}phases[{i}].title", p["title"]))
        for j, it in enumerate(p["items"]):
            rows.append((f"{prefix}phases[{i}].items[{j}]", it))
    for c, h in enumerate(data.get("headers", [])):
        rows.append((f"{prefix}headers[{c}]", h))
    for r, row in enumerate(data.get("rows", [])):
        for c, cell in enumerate(row):
            rows.append((f"{prefix}cell[{r}][{c}]", cell))
    for i, cell in enumerate(data.get("cells", [])):
        rows.append((f"{prefix}cells[{i}].title", cell["title"]))
        rows.append((f"{prefix}cells[{i}].text", cell["text"]))
    for i, nd in enumerate(data.get("nodes", [])):
        rows.append((f"{prefix}nodes[{i}].label", nd["label"]))
    for i, st in enumerate(data.get("path", [])):
        rows.append((f"{prefix}path[{i}].title", st["title"]))
        if "text" in st:
            rows.append((f"{prefix}path[{i}].text", st["text"]))
    for key in ("stack", "rings"):
        for i, row in enumerate(data.get(key, [])):
            rows.append((f"{prefix}{key}[{i}].label", row["label"]))
    for ax in ("x_axis", "y_axis"):
        if ax in data:
            rows.append((f"{prefix}axis.{ax[0]}0", data[ax]["low"]))
            rows.append((f"{prefix}axis.{ax[0]}1", data[ax]["high"]))
    return rows


def _sheet_rows(f) -> list[tuple[str, str]]:
    # composite 모듈은 parse가 Fence로 정규화 — m.title·m.data 속성으로 전개
    rows = rows_from(f.title, f.kicker, f.thesis, f.data, "")
    for j, m in enumerate(f.data.get("modules", [])):
        rows.extend(rows_from(m.title, m.kicker, m.thesis, m.data, f"modules[{j}]."))
    return rows


def _review_sheet(f, unverified: list) -> str:
    # 5열 계약(스펙 §5.4) — 요소|문구|evidence|교차검증|확인란 + 미검증 상단 경고.
    rows = _sheet_rows(f)
    lines = [f"# 검수 시트 — 펜스 #{f.index}", ""]
    if unverified:
        lines.append("**⚠ 미검증 숫자 — 사람 대조 필수:**")
        lines += [f"- {u.loc}: {u.measured}" for u in unverified]
        lines.append("")
    lines += [
        f"> 고지: {f.note or DEFAULT_NOTE}",
        f"> evidence: {f.evidence or '—'}",
        "",
        "| 요소 | 문구 | evidence | 교차검증 | 확인란 |",
        "|---|---|---|---|---|",
    ]
    ev = f.evidence or "—"
    for p, t in rows:
        flag = "미검증" if any(f" {p}" in u.loc for u in unverified) else "I1 통과"
        lines.append(f"| {p} | {t} | {ev} | {flag} |  |")
    lines += ["", "- [ ] 원문 대조 완료"]
    return "\n".join(lines) + "\n"
