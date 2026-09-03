"""test_e2e.py — 전 파이프라인 회귀 (text-only 모드, paddle skip).

PDF(챕터 헤딩) → classify → extract(skip) → assets → split → (승인) → render.
산출 디렉토리 구조 + 챕터 수 검증.
"""
import json
import fitz


def _make_book_pdf(path, n_chapters=3):
    doc = fitz.open()
    for ch in range(1, n_chapters + 1):
        p = doc.new_page()
        p.insert_text((72, 72), f"Chapter {ch} Title", fontsize=18)        # 헤딩
        p.insert_text((72, 120), "body content here. " * 20, fontsize=11)  # 본문 text 분류
        p2 = doc.new_page()
        p2.insert_text((72, 72), "continued body text. " * 30, fontsize=11)
    doc.save(str(path))
    doc.close()


def test_pipeline_text_only(tmp_path):
    from scripts.classify_pages import classify
    from scripts.extract_text import extract as extract_text
    from scripts.extract_assets import extract as extract_assets
    from scripts.split_chapters import split
    from scripts.render_md import render

    pdf = tmp_path / "book.pdf"
    _make_book_pdf(pdf, n_chapters=3)
    work = tmp_path / "work"
    out = tmp_path / "out"

    # Step 1
    classify(str(pdf), str(work))
    # Step 2 (skip OCR)
    extract_text(str(pdf), str(work), ocr="skip")
    # Step 3
    extract_assets(str(pdf), str(out))
    # Step 4
    chapters = split(str(work))
    assert len(chapters) == 3
    # 게이트 승인 시뮬레이션 (사람이 chapters.json 확정했다고 가정)
    cf = json.loads((work / "chapters.json").read_text(encoding="utf-8"))
    cf["approval"] = {"approved_at": "2026-08-12", "by": "e2e-test"}
    cf["chapters"] = [{**c, "approved": True} for c in cf["chapters"]]
    (work / "chapters.json").write_text(json.dumps(cf, ensure_ascii=False), encoding="utf-8")
    # Step 5
    n = render(str(work), str(out), "e2e-book", title="E2E 테스트책")
    assert n == 3
    # 산출 구조
    assert (out / "README.md").exists()
    assert (out / "meta.yaml").exists()
    assert len(list(out.glob("0*-chapter-*.md"))) == 3
    assert (out / "assets" / "images").is_dir()
