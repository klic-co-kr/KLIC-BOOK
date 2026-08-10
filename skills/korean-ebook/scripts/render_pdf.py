#!/usr/bin/env python3
"""Render PDF pages to PNG for visual inspection."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:  # pragma: no cover
    fitz = None


def parse_pages(spec: str | None, total: int) -> list[int]:
    if not spec:
        return list(range(1, total + 1))
    result: set[int] = set()
    for token in spec.split(","):
        token = token.strip()
        if not token:
            continue
        if "-" in token:
            start_s, end_s = token.split("-", 1)
            start, end = int(start_s), int(end_s)
            if start > end:
                start, end = end, start
            result.update(range(start, end + 1))
        else:
            result.add(int(token))
    invalid = sorted(p for p in result if p < 1 or p > total)
    if invalid:
        raise ValueError(f"Page numbers out of range: {invalid}")
    return sorted(result)


def render_with_fitz(pdf: Path, out_dir: Path, dpi: int, pages: list[int]) -> None:
    if fitz is None:
        raise RuntimeError("PyMuPDF is not installed")
    doc = fitz.open(pdf)
    matrix = fitz.Matrix(dpi / 72.0, dpi / 72.0)
    width = max(3, len(str(len(doc))))
    for page_no in pages:
        page = doc.load_page(page_no - 1)
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        pix.save(out_dir / f"page-{page_no:0{width}d}.png")


def render_with_pdftoppm(pdf: Path, out_dir: Path, dpi: int, total: int) -> None:
    exe = shutil.which("pdftoppm")
    if not exe:
        raise RuntimeError("pdftoppm not found")
    prefix = out_dir / "_raw"
    proc = subprocess.run(
        [exe, "-png", "-r", str(dpi), str(pdf), str(prefix)],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "pdftoppm failed")
    width = max(3, len(str(total)))
    raw_files = sorted(out_dir.glob("_raw-*.png"), key=lambda p: int(re.search(r"(\d+)$", p.stem).group(1)))
    for idx, raw in enumerate(raw_files, start=1):
        raw.rename(out_dir / f"page-{idx:0{width}d}.png")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--dpi", type=int, default=160)
    parser.add_argument("--pages", help="1-based page list, e.g. 1,3-5,10")
    parser.add_argument("--renderer", choices=["auto", "pdftoppm", "pymupdf"], default="auto")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    pdf = args.pdf.resolve()
    out_dir = args.out_dir.resolve()
    if not pdf.exists():
        print(f"PDF not found: {pdf}", file=sys.stderr)
        return 2
    if fitz is None:
        print("PyMuPDF is required to inspect page count. Install requirements.txt", file=sys.stderr)
        return 2
    doc = fitz.open(pdf)
    total = len(doc)
    doc.close()
    pages = parse_pages(args.pages, total)
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("page-*.png"):
        old.unlink()

    renderer = args.renderer
    try:
        if renderer == "pdftoppm" or (renderer == "auto" and not args.pages and shutil.which("pdftoppm")):
            render_with_pdftoppm(pdf, out_dir, args.dpi, total)
            used = "pdftoppm"
        else:
            render_with_fitz(pdf, out_dir, args.dpi, pages)
            used = "PyMuPDF"
    except Exception as exc:
        if renderer == "auto":
            try:
                render_with_fitz(pdf, out_dir, args.dpi, pages)
                used = "PyMuPDF fallback"
            except Exception as fallback_exc:
                print(f"Render failed: {fallback_exc}", file=sys.stderr)
                return 2
        else:
            print(f"Render failed: {exc}", file=sys.stderr)
            return 2

    count = len(list(out_dir.glob("page-*.png")))
    print(f"Rendered {count} page(s) with {used}: {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
