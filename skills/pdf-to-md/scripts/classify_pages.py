#!/usr/bin/env python3
"""classify_pages.py <pdf> <work_dir> — 페이지별 텍스트/스캔 분류 (Step 1).

페이지별 문자수와 이미지 수로 분류:
- text  : 문자수 >= 100 (텍스트 레이어 풍부)
- scan  : 문자수 < 20   (텍스트 거의 없음 → OCR 대상)
- mixed : 그 사이       (텍스트 + 이미지 혼합)

산출: work/pages.json = [{page, kind, n_chars, n_images}]
"""
import sys, json
from pathlib import Path
import fitz  # pymupdf

TEXT_THRESHOLD = 100   # 문자수 이상 = text
SCAN_THRESHOLD = 20    # 문자수 미만 = scan


def classify(pdf_path: str, work_dir: str) -> list[dict]:
    work = Path(work_dir)
    work.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    pages = []
    for i, page in enumerate(doc):
        n_chars = len(page.get_text("text").strip())
        n_images = len(page.get_images())
        if n_chars >= TEXT_THRESHOLD:
            kind = "text"
        elif n_chars < SCAN_THRESHOLD:
            kind = "scan"
        else:
            kind = "mixed"
        pages.append({
            "page": i + 1,
            "kind": kind,
            "n_chars": n_chars,
            "n_images": n_images,
        })
    doc.close()
    (work / "pages.json").write_text(
        json.dumps(pages, ensure_ascii=False, indent=2), encoding="utf-8")
    return pages


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: classify_pages.py <pdf> <work_dir>")
    pages = classify(sys.argv[1], sys.argv[2])
    dist = {}
    for p in pages:
        dist[p["kind"]] = dist.get(p["kind"], 0) + 1
    print(f"classified {len(pages)} pages → {dist}")


if __name__ == "__main__":
    main()
