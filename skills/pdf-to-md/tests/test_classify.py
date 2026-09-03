"""test_classify.py — Step 1 페이지 분류 TDD."""
import json
from pathlib import Path


def _make_pdf(path):
    import fitz
    doc = fitz.open()
    # text 페이지 (200자+)
    doc.new_page().insert_text((72, 72), "제1장 테스트\n" + "한글 텍스트 페이지입니다. " * 30)
    # scan 페이지 (문자 거의 없음)
    doc.new_page().insert_text((72, 72), "짧음")
    # mixed 페이지 (중간)
    doc.new_page().insert_text((72, 72), "혼합 " + "텍스트입니다. " * 8)
    doc.save(str(path))
    doc.close()


def test_classify_three_kinds(tmp_path):
    from scripts.classify_pages import classify
    pdf = tmp_path / "t.pdf"
    _make_pdf(pdf)
    work = tmp_path / "work"
    pages = classify(str(pdf), str(work))
    assert len(pages) == 3
    assert pages[0]["kind"] == "text"      # 200자+
    assert pages[1]["kind"] == "scan"      # <20자
    assert pages[2]["kind"] == "mixed"     # 중간
    # pages.json 산출
    written = json.loads((work / "pages.json").read_text(encoding="utf-8"))
    assert written == pages
    # 필드
    for p in pages:
        assert {"page", "kind", "n_chars", "n_images"} <= set(p)


def test_classify_empty_pdf(tmp_path):
    from scripts.classify_pages import classify
    import fitz
    pdf = tmp_path / "empty.pdf"
    doc = fitz.open(); doc.new_page(); doc.save(str(pdf)); doc.close()
    pages = classify(str(pdf), str(tmp_path / "w"))
    assert len(pages) == 1
    assert pages[0]["kind"] == "scan"      # 빈 페이지
