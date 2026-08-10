# tests/test_chapters.py
from pathlib import Path
from korean_ebook_to_skill.chapters import detect_chapters, parse_chapter_file, slugify

def test_detect_chapters_korean_headings():
    text = "# 2장 올바른 문제 풀기\n본문\n## 2.1 개념 증명 무덤\n내용\n## 2.2 PSF\n내용\n"
    segs = detect_chapters(text)
    titles = [s.title for s in segs]
    assert "2장 올바른 문제 풀기" in titles
    assert "2.1 개념 증명 무덤" in titles
    assert all(s.start < s.end for s in segs)

def test_parse_chapter_kind_number():
    cf = parse_chapter_file(Path("tests/fixtures/02-제2장-올바른문제풀기.md"))
    assert cf.kind == "chapter" and cf.number == "02"

def test_parse_appendix_kind():
    cf = parse_chapter_file(Path("tests/fixtures/11-부록B-인물및팀명단.md"))
    assert cf.kind == "appendix" and cf.number == "B"

def test_slugify_parens_and_special():
    assert slugify("PSF (3관문)") == "psf-(3관문)"
    assert slugify("2.2 PSF: 문제와 해결책") == "22-psf-문제와-해결책"
