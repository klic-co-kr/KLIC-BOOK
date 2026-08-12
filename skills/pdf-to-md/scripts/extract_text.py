#!/usr/bin/env python3
"""extract_text.py <pdf> --work <dir> [--ocr paddle|skip] — Step 2 텍스트/OCR 추출.

- text 페이지 → pymupdf get_text("dict") + 헤딩 감지(폰트크기 >= HEADING_SIZE)
- scan/mixed → PaddleOCR(lazy, try/except). --ocr skip 시 이미지 링크 fallback.

산출: work/pages/<NNN>.md (페이지별 원시 MD)
"""
import sys, json, tempfile, os
from pathlib import Path
import fitz  # pymupdf

HEADING_SIZE = 14.0


def extract_text_page(doc, page_num: int) -> str:
    """pymupdf dict → MD (헤딩 감지)."""
    page = doc[page_num - 1]
    d = page.get_text("dict")
    lines = []
    for block in d.get("blocks", []):
        for line in block.get("lines", []):
            spans = line.get("spans", [])
            if not spans:
                continue
            text = "".join(s["text"] for s in spans).strip()
            if not text:
                continue
            max_size = max(s["size"] for s in spans)
            if max_size >= HEADING_SIZE:
                lines.append(f"## {text}")
            else:
                lines.append(text)
    return "\n\n".join(lines)


def ocr_page(doc, page_num: int, ocr_engine: str = "paddle") -> str:
    """scan/mixed 페이지 → MD. paddle 미가용 시 이미지 링크 fallback."""
    img_link = f"![scan-page-{page_num}](assets/images/page-{page_num:03d}.png)"
    if ocr_engine == "skip":
        return img_link
    try:
        from paddleocr import PaddleOCR
        ocr = PaddleOCR(use_angle_cls=True, lang="korean", show_log=False)
        page = doc[page_num - 1]
        pix = page.get_pixmap(dpi=300)
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            pix.save(f.name)
            img_path = f.name
        try:
            result = ocr.ocr(img_path, cls=True)
        finally:
            os.unlink(img_path)
        texts = [r[1][0] for r in (result[0] or []) if r]
        return "\n\n".join(texts) if texts else img_link
    except Exception as e:
        return f"{img_link}\n\n<!-- OCR 실패({type(e).__name__}): {e} -->"


def extract(pdf_path: str, work_dir: str, ocr: str = "paddle") -> None:
    work = Path(work_dir)
    pages = json.loads((work / "pages.json").read_text(encoding="utf-8"))
    (work / "pages").mkdir(exist_ok=True)
    doc = fitz.open(pdf_path)
    for p in pages:
        if p["kind"] == "text":
            md = extract_text_page(doc, p["page"])
        else:
            md = ocr_page(doc, p["page"], ocr)
        (work / "pages" / f"{p['page']:03d}.md").write_text(md, encoding="utf-8")
    doc.close()


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--work", required=True)
    ap.add_argument("--ocr", default="paddle", choices=["paddle", "skip"])
    a = ap.parse_args()
    extract(a.pdf, a.work, a.ocr)
    print(f"extracted → {a.work}/pages/")


if __name__ == "__main__":
    main()
