"""test_split.py — Step 4 챕터 분할 TDD."""
from pathlib import Path


def _write_pages(work, pages: dict):
    pdir = Path(work) / "pages"
    pdir.mkdir(parents=True, exist_ok=True)
    for num, body in pages.items():
        (pdir / f"{num:03d}.md").write_text(body, encoding="utf-8")


def test_detect_korean_chapter(tmp_path):
    from scripts.split_chapters import split
    work = tmp_path / "w"
    _write_pages(work, {
        1: "## 제1장 시작\n\n본문",
        5: "## 제2장 계속\n\n본문",
    })
    chapters = split(str(work))
    assert len(chapters) == 2
    assert "제1장" in chapters[0]["heading"]
    assert chapters[0]["start_page"] == 1
    assert chapters[1]["start_page"] == 5
    assert all(c["approved"] is False for c in chapters)  # 게이트 전


def test_detect_english_and_appendix(tmp_path):
    from scripts.split_chapters import split
    work = tmp_path / "w"
    _write_pages(work, {
        1: "## Chapter 1 Intro\nbody",
        10: "## Chapter 2 Body\nbody",
        20: "## 부록 A 자료\nbody",
    })
    chapters = split(str(work))
    assert len(chapters) == 3
    assert "Chapter 1" in chapters[0]["heading"]
    assert "부록" in chapters[2]["heading"]


def test_no_chapter(tmp_path):
    from scripts.split_chapters import split
    work = tmp_path / "w"
    _write_pages(work, {1: "본문만\n없다"})
    chapters = split(str(work))
    assert len(chapters) == 0
    # 게이트 보고서·chapters.json 산출
    assert (work / "chapters.json").exists()
    assert (work / "chapter-gate.md").exists()


def test_false_positive_filtered(tmp_path):
    from scripts.split_chapters import split
    work = tmp_path / "w"
    _write_pages(work, {1: "본문\n\nTable 1 결과\n그림 2 구조\n2026년"})
    chapters = split(str(work))
    assert len(chapters) == 0  # 표/그림/날짜는 챕터 아님
