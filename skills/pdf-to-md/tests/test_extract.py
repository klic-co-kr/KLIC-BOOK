"""test_extract.py — Step 2 텍스트/OCR 추출 TDD."""
import fitz


def _make_text_pdf(path):
    doc = fitz.open()
    p = doc.new_page()
    p.insert_text((72, 72), "Chapter 1 Heading", fontsize=18)       # 헤딩 (>=14)
    p.insert_text((72, 120), "body text content. " * 10, fontsize=11)  # 본문
    doc.save(str(path))
    doc.close()


def test_extract_text_heading(tmp_path):
    from scripts.extract_text import extract_text_page
    pdf = tmp_path / "t.pdf"
    _make_text_pdf(pdf)
    doc = fitz.open(str(pdf))
    md = extract_text_page(doc, 1)
    doc.close()
    assert "## Chapter 1 Heading" in md   # 헤딩 감지 (폰트크기)
    assert "body text" in md               # 본문 보존


def test_extract_skip_ocr_fallback(tmp_path):
    from scripts.classify_pages import classify
    from scripts.extract_text import extract
    pdf = tmp_path / "scan.pdf"
    doc = fitz.open()
    doc.new_page().insert_text((72, 72), "짧")  # scan (<20자)
    doc.save(str(pdf))
    doc.close()
    work = tmp_path / "w"
    classify(str(pdf), str(work))
    extract(str(pdf), str(work), ocr="skip")
    md = (work / "pages" / "001.md").read_text(encoding="utf-8")
    assert "scan-page-1" in md         # skip → 이미지 링크 fallback


def test_extract_text_page_output(tmp_path):
    from scripts.classify_pages import classify
    from scripts.extract_text import extract
    pdf = tmp_path / "t.pdf"
    _make_text_pdf(pdf)
    work = tmp_path / "w"
    classify(str(pdf), str(work))
    extract(str(pdf), str(work), ocr="skip")
    md = (work / "pages" / "001.md").read_text(encoding="utf-8")
    assert "## Chapter 1" in md


def test_normalize_math():
    """수식 Unicode 기호 → LaTeX 매핑 + $$ 래핑."""
    from scripts.extract_text import normalize_math
    r = normalize_math("손실 L = ∑ p(x) log p")
    assert r"\sum" in r
    assert r.startswith("$$") and r.endswith("$$")
    # 수식 아닌 일반 텍스트는 그대로
    assert normalize_math("일반 텍스트") == "일반 텍스트"
    # 이탤릭 수학 문자 → 보통
    assert "p" in normalize_math("𝑝(𝑥)")


def test_dedupe_repeated_footer(tmp_path):
    """매 페이지 반복되는 푸터(라이선스·페이지번호) 자동 제거."""
    from scripts.classify_pages import classify
    from scripts.extract_text import extract
    pdf = tmp_path / "f.pdf"
    doc = fitz.open()
    for i in range(3):
        p = doc.new_page()
        p.insert_text((72, 72), f"Chapter {i}", fontsize=18)
        p.insert_text((72, 120), f"unique body {i} text " * 20, fontsize=11)
        p.insert_text((72, 700), "COMMON LICENSE FOOTER", fontsize=9)   # 매 페이지 푸터
    doc.save(str(pdf))
    doc.close()
    work = tmp_path / "w"
    classify(str(pdf), str(work))
    extract(str(pdf), str(work), ocr="skip")
    for pg in ("001", "002", "003"):
        md = (work / "pages" / f"{pg}.md").read_text(encoding="utf-8")
        assert "COMMON LICENSE FOOTER" not in md   # 푸터 제거
        assert "unique body" in md                  # 본문 보존
