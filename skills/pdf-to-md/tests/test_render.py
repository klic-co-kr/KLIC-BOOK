"""test_render.py — Step 5 MD 렌더 TDD."""
import json
from pathlib import Path


def _setup_work(tmp_path, chapters, pages_text, approved=True):
    work = tmp_path / "w"
    pdir = work / "pages"
    pdir.mkdir(parents=True)
    for num, body in pages_text.items():
        (pdir / f"{num:03d}.md").write_text(body, encoding="utf-8")
    cf = {
        "source": str(work),
        "n_detected": len(chapters),
        "approval": {"approved_at": "2026-08-12", "by": "test"} if approved else None,
        "chapters": [{**c, "approved": approved} for c in chapters],
    }
    (work / "chapters.json").write_text(json.dumps(cf, ensure_ascii=False), encoding="utf-8")
    return work


def test_render_chapters(tmp_path):
    from scripts.render_md import render
    chapters = [
        {"n": 1, "start_page": 1, "heading": "제1장 시작"},
        {"n": 2, "start_page": 5, "heading": "제2장 계속"},
    ]
    pages = {1: "p1본문", 2: "p2", 3: "p3", 4: "p4", 5: "p5본문", 6: "p6"}
    work = _setup_work(tmp_path, chapters, pages)
    out = tmp_path / "out"
    n = render(str(work), str(out), "test-book", title="테스트책")
    assert n == 2
    assert (out / "01-chapter-제1장-시작.md").exists()
    assert (out / "02-chapter-제2장-계속.md").exists()
    c1 = (out / "01-chapter-제1장-시작.md").read_text(encoding="utf-8")
    assert "# 제1장 시작" in c1
    assert "p1본문" in c1 and "p4" in c1   # p1-4
    assert "p5본문" not in c1              # 다음 챕터
    assert (out / "meta.yaml").exists()
    assert (out / "README.md").exists()


def test_render_blocks_without_approval(tmp_path, capsys):
    from scripts.render_md import render
    chapters = [{"n": 1, "start_page": 1, "heading": "제1장"}]
    work = _setup_work(tmp_path, chapters, {1: "본문"}, approved=False)
    out = tmp_path / "out"
    try:
        render(str(work), str(out), "x")
        assert False, "should have exited"
    except SystemExit:
        pass
