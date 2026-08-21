#!/usr/bin/env python3
"""cli.py — 인포그래픽 단독 검증(스펙 §5.5). 책 전체 빌드 없이 도식 하나를 검사·렌더."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from md2typst import extract_fences                     # noqa: E402
from build import typst_binary                          # noqa: E402 — 탐지 단일화(Global Constraints)
from infographic import emit, layout, lint              # noqa: E402
from infographic.parse import ParseError, parse_fence   # noqa: E402


def _tokens(style: str) -> dict:
    p = SKILL_DIR / "styles" / style / "tokens.json"
    if not p.exists():
        raise SystemExit(f"스타일 팩 없음: {style}")
    return json.loads(p.read_text(encoding="utf-8"))


def _load(md_path: Path, style: str):
    raw = md_path.read_text(encoding="utf-8")
    # 치환본(펜스 → ⟦IG:N⟧)을 넘긴다 — 펜스 JSON이 자기 숫자의 근거로
    # 승격되는 자기참조 방지. render.py와 동일 계약, 마커는 lint.check가 strip.
    md, fences_raw = extract_fences(raw)
    tokens = _tokens(style)
    fences = [parse_fence(r["index"], r["line"], r["body"]) for r in fences_raw]
    figs = {f.index: layout.dispatch(f, tokens) for f in fences}
    return md, fences, figs, tokens


def cmd_lint(md_path: Path, style: str) -> int:
    md, fences, figs, tokens = _load(md_path, style)
    findings = lint.check(fences, figs, tokens, md, md_path.name)
    if findings:
        print(lint_report(findings), file=sys.stderr)
        return 1
    print(f"OK ({len(fences)} fences)")
    return 0


def lint_report(findings) -> str:
    lines = ["[I1] 위반 — 전건:"]
    lines += [f"  [{f.kind}] {f.loc} — {f.measured} → 제안: {', '.join(f.levers)}"
              for f in findings]
    return "\n".join(lines)


def cmd_preview(md_path: Path, fig_no: int, style: str, out: Path) -> int:
    md, fences, figs, tokens = _load(md_path, style)
    if fig_no not in figs:
        print(f"펜스 #{fig_no} 없음 (존재: {sorted(figs)})", file=sys.stderr)
        return 2
    findings = lint.check(fences, figs, tokens, md, md_path.name)
    keep = [x for x in findings if f" #{fig_no} " in x.loc]
    if keep:
        print(lint_report(keep), file=sys.stderr)
        return 1
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        igdir = tdp / "infographic"; igdir.mkdir()
        (tdp / "tokens.json").write_text(json.dumps(tokens, ensure_ascii=False), encoding="utf-8")
        shutil.copy2(SKILL_DIR / "templates" / "infographic" / "helper.typ", tdp / "helper.typ")
        f = next(x for x in fences if x.index == fig_no)
        (igdir / "fig.typ").write_text(
            emit.render_typ(figs[fig_no], tokens), encoding="utf-8")
        # 1페이지: 판형 크기 페이지에 도식 하나를 상단 배치
        main = (igdir / "fig.typ").read_text(encoding="utf-8")
        # 폰트 스택은 typst 배열 리터럴 (a, b)로 — json 배열 [a, b]는
        # content 블록으로 파싱돼 컴파일이 깨진다(build.py font_stack과 동일).
        font_stack = "(" + ", ".join(f'"{f}"' for f in tokens["fonts"]["body"]["stack"]) + ")"
        page = (f'#set page(width: {tokens["trim"]["width_mm"]}mm, '
                f'height: {tokens["trim"]["height_mm"]}mm, margin: 12mm)\n'
                f'#set text(font: {font_stack}, '
                f'size: {tokens["fonts"]["body"]["size_pt"]}pt, lang: "ko")\n'
                + main)
        (igdir / "fig.typ").write_text(page, encoding="utf-8")
        r = subprocess.run([typst_binary(), "compile",
                            str(igdir / "fig.typ"), str(out), "--root", str(tdp)],
                           capture_output=True, text=True, timeout=120)
        if r.returncode != 0:
            print(r.stderr, file=sys.stderr)
            return 3
    print(f"preview → {out}")
    return 0


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="infographic")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("lint", help="I1 린트만 (렌더 없음)")
    p1.add_argument("md"); p1.add_argument("--style", default="practical")
    p2 = sub.add_parser("preview", help="펜스 1개 standalone PDF")
    p2.add_argument("md"); p2.add_argument("--fig", type=int, required=True)
    p2.add_argument("--style", default="practical"); p2.add_argument("--out", default="fig-preview.pdf")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "lint":
            return cmd_lint(Path(a.md), a.style)
        return cmd_preview(Path(a.md), a.fig, a.style, Path(a.out))
    except ParseError as e:
        print(f"[parse] 펜스 {e.fence_index}: {e.detail}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
