#!/usr/bin/env python3
"""extract_assets.py <pdf> --out <dir> [--ocr-math] — Step 3 이미지·표·수식 추출.

이미지 → out/assets/images/fig-<page>-<idx>.png (pymupdf xref 추출)
표 → out/assets/tables/ (예약)
수식 → out/assets/formulas/formula-<page>-<idx>.md (--ocr-math 시 pix2tex LaTeX-OCR)

산출 디렉토리:
  out/assets/images/fig-NNN-MM.png
  out/assets/tables/
  out/assets/formulas/formula-NNN-MM.md  (--ocr-math)
"""
import sys
from pathlib import Path
import fitz

# 수식 이미지 휴리스틱: 페이지 면적 대비 작은 비율(그림·사진 아닌 수식 후보)
FORMULA_MAX_AREA_RATIO = 0.05


def _is_formula_candidate(pix, page_area):
    img_area = pix.width * pix.height
    return img_area / page_area <= FORMULA_MAX_AREA_RATIO and pix.width > pix.height * 0.3


def ocr_math_latex(img_path: str) -> str | None:
    """pix2tex(LaTeX-OCR)로 이미지 → LaTeX. 실패/비수식 시 None."""
    try:
        from pix2tex.cli import LatexOCR
        from PIL import Image
        model = LatexOCR()
        return model(Image.open(img_path))
    except Exception as e:
        print(f"WARN pix2tex {img_path}: {e}", file=sys.stderr)
        return None


def extract(pdf_path: str, out_dir: str, ocr_math: bool = False) -> int:
    out = Path(out_dir)
    img_dir = out / "assets" / "images"
    tbl_dir = out / "assets" / "tables"
    fml_dir = out / "assets" / "formulas"
    img_dir.mkdir(parents=True, exist_ok=True)
    tbl_dir.mkdir(parents=True, exist_ok=True)
    if ocr_math:
        fml_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    n_images = 0
    n_formulas = 0
    for i, page in enumerate(doc):
        page_area = page.rect.width * page.rect.height
        for j, img in enumerate(page.get_images()):
            xref = img[0]
            try:
                pix = fitz.Pixmap(doc, xref)
                if pix.n >= 5:
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                fname = f"fig-{i + 1:03d}-{j:02d}.png"
                pix.save(str(img_dir / fname))
                n_images += 1
                # 수식 OCR (작은 이미지 후보만)
                if ocr_math and _is_formula_candidate(pix, page_area):
                    latex = ocr_math_latex(str(img_dir / fname))
                    if latex and len(latex) > 3:
                        (fml_dir / f"formula-{i + 1:03d}-{j:02d}.md").write_text(
                            f"$${latex}$$\n", encoding="utf-8")
                        n_formulas += 1
            except Exception as e:
                print(f"WARN page {i+1} img {j}: {e}", file=sys.stderr)
    doc.close()
    if ocr_math:
        print(f"formulas OCR: {n_formulas}", file=sys.stderr)
    return n_images


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--out", required=True)
    ap.add_argument("--ocr-math", action="store_true", help="수식 이미지 → LaTeX (pix2tex)")
    a = ap.parse_args()
    n = extract(a.pdf, a.out, a.ocr_math)
    print(f"extracted {n} images → {a.out}/assets/images/")


if __name__ == "__main__":
    main()
