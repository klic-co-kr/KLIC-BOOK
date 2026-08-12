#!/usr/bin/env python3
"""extract_assets.py <pdf> --out <dir> — Step 3 이미지·표 추출.

이미지 → out/assets/images/fig-<page>-<idx>.png (pymupdf xref 추출)
표 → out/assets/tables/ (PP-Structure 가용 시 MD, 아니면 생략 — 본 v1은 이미지 중심)

산출 디렉토리 구조:
  out/assets/images/fig-NNN-MM.png
  out/assets/tables/  (예약)
"""
import sys
from pathlib import Path
import fitz


def extract(pdf_path: str, out_dir: str) -> int:
    out = Path(out_dir)
    img_dir = out / "assets" / "images"
    tbl_dir = out / "assets" / "tables"
    img_dir.mkdir(parents=True, exist_ok=True)
    tbl_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    n_images = 0
    for i, page in enumerate(doc):
        for j, img in enumerate(page.get_images()):
            xref = img[0]
            try:
                pix = fitz.Pixmap(doc, xref)
                if pix.n >= 5:  # CMYK → RGB
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                pix.save(str(img_dir / f"fig-{i + 1:03d}-{j:02d}.png"))
                n_images += 1
            except Exception as e:
                print(f"WARN page {i+1} img {j}: {e}", file=sys.stderr)
    doc.close()
    return n_images


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    n = extract(a.pdf, a.out)
    print(f"extracted {n} images → {a.out}/assets/images/")


if __name__ == "__main__":
    main()
