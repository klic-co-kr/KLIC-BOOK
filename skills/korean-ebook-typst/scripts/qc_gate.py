#!/usr/bin/env python3
"""korean-ebook-typst QC 게이트 — PASS 시에만 final/ 생성."""
import json
import re
import shutil
import sys
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


MATH_FONT_ALLOWLIST = {
    "newcomputermodern", "newcomputermodernmath", "newcmmath",
    "libertinusserif", "libertinussans", "libertinusmath",
    "lmroman", "lmmono",
}


def norm_font(name: str) -> str:
    """basefont → 정규화된 폰트 패밀리명.

    PDF basefont 실측 형태: "KVHFRP+NotoSansCJKkr-Regular-Identity-H".
    서브셋 접두(ABCDE+)와 스타일·인코딩 접미사(-Regular-Identity-H)를
    잘라야 tokens.json 스택 이름("Noto Sans CJK KR")과 매칭된다.
    """
    if "+" in name:
        name = name.split("+", 1)[1]
    name = name.split("-", 1)[0]
    return "".join(ch for ch in name.lower() if ch.isalnum())


def check_fonts(pdf: Path, allowed: set) -> list:
    violations, seen = [], set()
    with fitz.open(pdf) as doc:
        for page in doc:
            for f in page.get_fonts():
                basefont = f[3]
                n = norm_font(basefont)
                if n in seen:
                    continue
                seen.add(n)
                if n in allowed or n in MATH_FONT_ALLOWLIST or not n:
                    continue
                violations.append(f"계약 외 폰트: {basefont}")
    return violations


def check_chars_band(pdf: Path, band: dict, body_size_pt: float,
                     frame_width_pt: float) -> list:
    warns = []
    with fitz.open(pdf) as doc:
        for pno in range(2, len(doc)):  # 표지(1쪽)·목차(2쪽) 제외
            for block in doc[pno].get_text("dict")["blocks"]:
                if block["type"] != 0:
                    continue
                for line in block["lines"]:
                    spans = [s for s in line["spans"]
                             if abs(s["size"] - body_size_pt) <= 0.3]
                    if not spans:
                        continue
                    w = line["bbox"][2] - line["bbox"][0]
                    if w < frame_width_pt * 0.80:
                        continue  # 문단 마지막 줄 등 정렬 줄 아님
                    text = "".join(s["text"] for s in spans).strip()
                    n = len(text.replace(" ", ""))
                    if n < band["min"] or n > band["max"]:
                        warns.append(f"p{pno + 1} {n}자/줄: {text[:20]!r}")
    return warns


def allowed_fonts(tokens: dict) -> set:
    """tokens fonts → 정규화 허용 집합(stack + 선택 ps 별칭).

    KoPubWorld바탕처럼 임베드 PostScript명(KoPubWorldBatang)이 스택
    표기와 달라 정규화 결과가 어긋나는 폰트는 스택 항목의 "ps" 배열로
    임베드명을 추가 등록한다.
    """
    allowed = {norm_font(f) for fs in tokens["fonts"].values() for f in fs["stack"]}
    allowed |= {norm_font(p) for fs in tokens["fonts"].values() for p in fs.get("ps", [])}
    return allowed


def run(book_dir: Path) -> int:
    build = book_dir / "build"
    draft = book_dir / "draft"
    tokens_path = build / "tokens.json"
    if not tokens_path.exists():
        print("[qc] build/ 없음 — 먼저 build.py 실행", file=sys.stderr)
        return 1
    tokens = json.loads(tokens_path.read_text(encoding="utf-8"))
    pdfs = sorted(draft.glob("*.pdf"))
    if not pdfs:
        print("[qc] draft/*.pdf 없음", file=sys.stderr)
        return 1
    pdf = pdfs[0]
    if len(pdfs) > 1:
        # build.py는 항상 pdf 1개만 남기므로 2개 이상은 이전 빌드 잔여 —
        # 어떤 pdf가 검사됐는지 알려야 낡은 결과를 잘못 읽지 않는다.
        print(f"[qc] 경고: draft/*.pdf {len(pdfs)}개 — {pdf.name}만 검사"
              f"(무시: {', '.join(p.name for p in pdfs[1:])})", file=sys.stderr)
    frame = load_frame(tokens_path)
    overflow = check_overflow(pdf, frame)
    allowed = allowed_fonts(tokens)
    fonts = check_fonts(pdf, allowed)
    band = tokens.get("chars_per_line")
    frame_w = frame[2] - frame[0]
    warns = check_chars_band(pdf, band, tokens["fonts"]["body"]["size_pt"],
                             frame_w) if band else []
    report = {"g1_overflow": overflow, "g2_fonts": fonts, "g3_band_warns": warns,
              "pass": not overflow and not fonts}
    (book_dir / "gate-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if not report["pass"]:
        # FAIL 시 낡은 final/<책>.pdf가 남으면 직전 PASS 결과로 오탐된다 —
        # 폐기한다(2026-08-15 종단 검증 발견, 컨트롤러 판정).
        final = book_dir / "final"
        if final.is_dir():
            for old in final.glob("*.pdf"):
                old.unlink()
        print(f"[qc] FAIL — gate-report.json 참조: {overflow[:3]} {fonts[:3]}",
              file=sys.stderr)
        return 1
    final = book_dir / "final"
    final.mkdir(exist_ok=True)
    shutil.copy2(pdf, final / pdf.name)
    print(f"[qc] PASS → {final / pdf.name} (WARN {len(warns)}건)")
    return 0


def main() -> None:
    if len(sys.argv) != 2:
        print("사용법: qc_gate.py <책디렉터리>", file=sys.stderr)
        raise SystemExit(1)
    raise SystemExit(run(Path(sys.argv[1]).resolve()))


if __name__ == "__main__":
    main()
