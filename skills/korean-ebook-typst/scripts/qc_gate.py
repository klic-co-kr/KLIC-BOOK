#!/usr/bin/env python3
"""korean-ebook-typst QC 게이트 — PASS 시에만 final/ 생성."""
import json
import re
from pathlib import Path
import fitz  # PyMuPDF


def load_frame(tokens_path: Path) -> tuple:
    t = json.loads(tokens_path.read_text(encoding="utf-8"))
    f = t["body_frame_pt"]
    return (f["x0"], f["y0"], f["x1"], f["y1"])


def _ink_bbox(line: dict) -> tuple:
    """행의 잉크 bbox와 텍스트 반환 — 선행/후행 공백 문자 bbox는 제외.

    fitz 행 bbox는 줄바꿈 뒤 남은 후행 공백 폭까지 포함해 양쪽정렬
    행을 실제보다 넓게 잰다(lecture 실측 +5.03pt). 공백은 잉크가 아니므로
    rawdict 글자 단위 bbox로 다시 계산한다. 전부 공백이면 (None, "").
    """
    chars = [c for s in line["spans"] for c in s["chars"]]
    text = "".join(c["c"] for c in chars).strip()
    i, j = 0, len(chars)
    while i < j and chars[i]["c"].isspace():
        i += 1
    while j > i and chars[j - 1]["c"].isspace():
        j -= 1
    if i >= j:
        return None, ""
    sel = chars[i:j]
    x0 = min(c["bbox"][0] for c in sel)
    y0 = min(c["bbox"][1] for c in sel)
    x1 = max(c["bbox"][2] for c in sel)
    y1 = max(c["bbox"][3] for c in sel)
    return (x0, y0, x1, y1), text


def check_overflow(pdf: Path, frame: tuple, skip_pages: int = 1) -> list:
    x0, y0, x1, y1 = frame
    tol = 3.0  # pt 허용 오차 — 글리프 어센트가 행 bbox를 프레임 위로
    # 끌어올린다(lecture 실측: 20pt 헤딩 +2.94pt). 1pt면 정상 콘텐츠 오탐.
    violations = []
    doc = fitz.open(pdf)
    for pno in range(skip_pages, len(doc)):
        for block in doc[pno].get_text("rawdict")["blocks"]:
            if block["type"] != 0:
                continue
            for line in block["lines"]:
                ink, text = _ink_bbox(line)
                if ink is None:
                    continue
                bx0, by0, bx1, by1 = ink
                outside = bx0 < x0 - tol or bx1 > x1 + tol or \
                    by0 < y0 - tol or by1 > y1 + tol
                if outside:
                    if by0 > y1 and re.fullmatch(r"\d{1,3}", text):
                        continue  # 푸터 쪽번호
                    violations.append(
                        f"p{pno + 1} bbox=({bx0:.1f},{by0:.1f},{bx1:.1f},{by1:.1f}) "
                        f"frame=({x0},{y0},{x1},{y1}) text={text[:30]!r}")
    return violations
