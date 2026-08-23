"""tests/test_build_config.py"""
from pathlib import Path
import textwrap
import pytest
from scripts.build import STYLES, load_config

def _write(tmp_path, content):
    (tmp_path / "typst-build.yaml").write_text(textwrap.dedent(content), encoding="utf-8")
    return tmp_path / "typst-build.yaml"

def test_valid_config(tmp_path):
    p = _write(tmp_path, """\
        style: practical
        title: 테스트 책
        chapters:
          - manuscript/ch01.md
          - manuscript/ch02.md
    """)
    for ch in ("manuscript/ch01.md", "manuscript/ch02.md"):
        (tmp_path / ch).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / ch).write_text("# 챕터\n", encoding="utf-8")
    cfg = load_config(p)
    assert cfg["style"] == "practical"
    assert cfg["title"] == "테스트 책"
    assert cfg["chapters"] == ["manuscript/ch01.md", "manuscript/ch02.md"]
    assert cfg["subtitle"] == "" and cfg["cover"] is None

def test_unknown_style_rejected(tmp_path):
    p = _write(tmp_path, """\
        style: magazine
        title: x
        chapters: [a.md]
    """)
    with pytest.raises(SystemExit):
        load_config(p)

def test_missing_chapters_rejected(tmp_path):
    p = _write(tmp_path, """\
        style: essay
        title: x
    """)
    with pytest.raises(SystemExit):
        load_config(p)

def test_chapter_file_must_exist(tmp_path):
    p = _write(tmp_path, """\
        style: essay
        title: x
        chapters: [nope.md]
    """)
    with pytest.raises(SystemExit):
        load_config(p)
