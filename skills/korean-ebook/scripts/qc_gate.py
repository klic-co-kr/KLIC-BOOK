#!/usr/bin/env python3
"""korean-ebook QC 게이트 — PASS 시에만 final/ 생성."""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
import fitz  # PyMuPDF

try:
    from build import typst_binary  # CLI 컨텍스트 — scripts/가 sys.path에 있다
except ImportError:  # scripts.* 패키지로 임포트되는 테스트 환경(korean_lint 관례)
    from scripts.build import typst_binary


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
    with fitz.open(pdf) as doc:
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
                        if by1 < y0:
                            continue  # 헤더 러닝헤드 — 상단 여백 전용 영역
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


def family_raw(basefont: str) -> str:
    """basefont → 가족명 원문(서브셋·스타일 접미사만 제거).

    NanumSquare_ac처럼 가족명 자체에 밑줄이 붙은 폰트는 임베드 PS명이
    NanumSquare_acR로 끝나 norm 정규화(alnum만) 후 매칭이 어긋난다.
    원문 비교로 변형 접미사를 판정하기 위해 쓴다.
    """
    if "+" in basefont:
        basefont = basefont.split("+", 1)[1]
    return basefont.split("-", 1)[0]


VARIANT_SUFFIX = re.compile(r"^[A-Za-z_]{0,4}$")

def _font_allowed(basefont: str, allowed_norm: set,
                  allowed_raw: set) -> bool:
    n = norm_font(basefont)
    if n in allowed_norm or n in MATH_FONT_ALLOWLIST or not n:
        return True
    # 변형 접미사 매칭: 임베드 PS명(NanumSquare_acR)이 스택 가족명
    # (NanumSquare_ac) + 짧은 스타일 접미사(R·AC 등 4자 이하)면 같은
    # 가족으로 본다. NanumGothic↔NanumGothicCoding 같은 타 가족은
    # 접미사가 4자를 넘어 기각된다.
    fam = family_raw(basefont)
    return any(fam == a or fam.startswith(a) and VARIANT_SUFFIX.match(fam[len(a):])
               for a in allowed_raw if a)

def check_fonts(pdf: Path, allowed_norm: set, allowed_raw: set) -> list:
    violations, seen = [], set()
    with fitz.open(pdf) as doc:
        for page in doc:
            for f in page.get_fonts():
                basefont = f[3]
                n = norm_font(basefont)
                if n in seen:
                    continue
                seen.add(n)
                if _font_allowed(basefont, allowed_norm, allowed_raw):
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


def allowed_fonts(tokens: dict) -> tuple:
    """tokens fonts → (정규화 허용집합, 원문 가족명 집합).

    정규화 집합은 기존대로 stack + 선택 ps 별칭. 원문 집합은 G2 변형
    접미사 매칭(NanumSquare_ac ↔ NanumSquare_acR)에 쓰인다.
    """
    allowed_norm = {norm_font(f) for fs in tokens["fonts"].values() for f in fs["stack"]}
    allowed_norm |= {norm_font(p) for fs in tokens["fonts"].values() for p in fs.get("ps", [])}
    allowed_raw = {f for fs in tokens["fonts"].values() for f in fs["stack"]}
    allowed_raw |= {p for fs in tokens["fonts"].values() for p in fs.get("ps", [])}
    return allowed_norm, allowed_raw


def check_review_sheets(build: Path) -> list[str]:
    """미완료 검수 시트 파일명 반환(스펙 §5.4 — 확인란 미완료 시 WARN, 에러 아님)."""
    igdir = build / "infographic"
    if not igdir.exists():
        return []
    incomplete = []
    for sheet in sorted(igdir.glob("*.review.md")):
        if "- [ ] 원문 대조 완료" in sheet.read_text(encoding="utf-8"):
            incomplete.append(sheet.name)
    return incomplete


def _infographic_pages(book: Path, pdf: Path | None) -> dict:
    """§5.4 개정 6판 — typst query metadata로 도식-페이지 대응·일치 검사·검수 PNG."""
    build = book / "build"
    main = build / "main.typ"
    mf = build / "infographic" / "manifest.json"
    if not (main.exists() and mf.exists()):
        return {"count": 0, "expected": 0, "match": True, "figs": []}
    manifest = json.loads(mf.read_text(encoding="utf-8"))
    r = subprocess.run([typst_binary(), "query", str(main), "metadata",
                        "--field", "value", "--root", str(build)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return {"count": 0, "expected": manifest["count"], "match": False, "figs": []}
    queried = json.loads(r.stdout or "[]")   # stdout = JSON 배열 하나(줄 단위 아님)
    figs = [{"name": f["name"], "chapter": f["chapter"], "index": f["index"],
             "page": q["page"]}
            for q in queried if isinstance(q, dict) and q.get("kind") == "ig-fig"
            for f in manifest["figs"] if f["name"] == q.get("name")]
    # §5.4 "실제 페이지 수와의 일치 검사" — page가 PDF 범위 내인가(G1-M6)
    pages_ok = True
    if pdf is not None and pdf.exists():
        with fitz.open(pdf) as doc:
            pages_ok = doc.page_count > 0 and all(
                1 <= f["page"] <= doc.page_count for f in figs)
    out = {"count": len(figs), "expected": manifest["count"],
           "match": len(figs) == manifest["count"] and pages_ok, "figs": figs}
    # 검수 렌더 PNG — 도식이 실린 unique 페이지별 1장(170 DPI). best-effort:
    # 실패해도 게이트 판정에 영향 없다(검수자 안내물).
    for pno in sorted({f["page"] for f in figs} if pages_ok else set()):
        png = build / "infographic" / f"review-p{pno:03d}.png"
        subprocess.run([typst_binary(), "compile", str(main), str(png),
                        "--pages", str(pno), "--ppi", "170", "--root", str(build)],
                       capture_output=True, text=True, check=False)
    return out


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
    # 신선도 검사 — build가 실패해도 낡은 draft가 남아 거짓 PASS가 난다
    # (설득의 구조 표지 수정 중 실측: main.typ 15:40 vs draft 14:45).
    main_typ = build / "main.typ"
    if main_typ.exists() and main_typ.stat().st_mtime > pdf.stat().st_mtime:
        print(f"[qc] draft가 main.typ보다 오래 됨 — 빌드 실패 잔여 가능. "
              f"build.py 재실행 필요 ({pdf.name})", file=sys.stderr)
        return 1
    if len(pdfs) > 1:
        # build.py는 항상 pdf 1개만 남기므로 2개 이상은 이전 빌드 잔여 —
        # 어떤 pdf가 검사됐는지 알려야 낡은 결과를 잘못 읽지 않는다.
        print(f"[qc] 경고: draft/*.pdf {len(pdfs)}개 — {pdf.name}만 검사"
              f"(무시: {', '.join(p.name for p in pdfs[1:])})", file=sys.stderr)
    frame = load_frame(tokens_path)
    overflow = check_overflow(pdf, frame)
    allowed_norm, allowed_raw = allowed_fonts(tokens)
    fonts = check_fonts(pdf, allowed_norm, allowed_raw)
    band = tokens.get("chars_per_line")
    frame_w = frame[2] - frame[0]
    warns = check_chars_band(pdf, band, tokens["fonts"]["body"]["size_pt"],
                             frame_w) if band else []
    # G4 한글 문체(fluent-korean 기계화) — WARN. 원고 md에서 검사.
    style_warns = {}
    yml = book_dir / "typst-build.yaml"
    if yml.exists():
        import yaml
        try:
            import korean_lint
        except ImportError:  # scripts.* 패키지로 임포트되는 테스트 환경
            from scripts import korean_lint
        cfg = yaml.safe_load(yml.read_text(encoding="utf-8")) or {}
        style_warns = korean_lint.lint_manuscript(cfg.get("chapters", []),
                                                  book_dir)
    # G5 콘텐츠 정합성 — 라틴 잔존·판독불능·교차참조·주석 잔여(WARN) +
    # ⚠️ 보강 마커 인벤토리(재스캔 자산 — 보고서가 인용). 원고 md에서 검사.
    content_warns, rescan = [], []
    if yml.exists():
        try:
            import content_lint
        except ImportError:
            from scripts import content_lint
        content_warns, rescan = content_lint.lint(cfg.get("chapters", []),
                                                  book_dir)
    # §5.4 미완료 검수 시트 WARN도 리포트 채널로 — stdout 인쇄만으로는
    # gate-report.json을 읽는 downstream이 이 사실을 못 본다(최종 리뷰 Minor).
    unreviewed = check_review_sheets(build)
    igp = _infographic_pages(book_dir, pdf)
    report = {"g1_overflow": overflow, "g2_fonts": fonts, "g3_band_warns": warns,
              "g4_style_warns": style_warns, "ig_review_warns": unreviewed,
              "infographic_pages": igp,
              "g5_content_warns": content_warns, "g5_rescan_inventory": rescan,
              "pass": not overflow and not fonts}
    (book_dir / "gate-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if igp["expected"]:
        print(f"[qc] 도식 페이지 대응 {igp['count']}/{igp['expected']}"
              + ("" if igp["match"] else " — 일치 불량"))
    if igp["count"] == 0 and igp["expected"] > 0:
        # emit은 됐으나 본문 페이지 매핑이 0건 — build 붕괴 신호(WARN 채널).
        print("[WARN] 도식 페이지 대응 0건 — build.py 재실행 필요", file=sys.stderr)
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
    n_style = sum(len(v) for v in style_warns.values())
    n_content = sum(len(v) for v in content_warns.values()) if content_warns else 0
    if unreviewed:
        print(f"[WARN] 미확인 인포그래픽 검수 시트 {len(unreviewed)}건: "
              + ", ".join(unreviewed))
    print(f"[qc] PASS → {final / pdf.name} "
          f"(WARN {len(warns)}건, 문체 {n_style}건, 정합성 {n_content}건, "
          f"검수시트 {len(unreviewed)}건, 보강대상 {len(rescan)}면)")
    return 0


def main() -> None:
    if len(sys.argv) != 2:
        print("사용법: qc_gate.py <책디렉터리>", file=sys.stderr)
        raise SystemExit(1)
    raise SystemExit(run(Path(sys.argv[1]).resolve()))


if __name__ == "__main__":
    main()
