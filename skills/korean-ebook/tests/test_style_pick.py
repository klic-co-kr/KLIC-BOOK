"""style_pick — style: auto 판형 자동판단 휴리스틱 테스트."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from style_pick import analyze, pick  # noqa: E402


def _book(tmp_path, chapters: dict) -> Path:
    (tmp_path / "manuscript").mkdir()
    for name, body in chapters.items():
        (tmp_path / "manuscript" / name).write_text(body, encoding="utf-8")
    return tmp_path


def test_table_heavy_manuscript_picks_lecture(tmp_path):
    """논문·도표형(표 다수) → A4 lecture."""
    tbl = "| a | b |\n|---|---|\n| 1 | 2 |\n"
    body = ("## 장\n\n본문 문단입니다. " * 20 + "\n\n" + tbl) * 3
    d = _book(tmp_path, {"ch01.md": body})
    style, why = pick(d, ["manuscript/ch01.md"])
    assert style == "lecture"
    assert "시각 요소" in why


def test_long_prose_picks_essay(tmp_path):
    """표 없는 장문 산문 → B6 essay."""
    para = "아주 긴 문단입니다. " * 40  # ~400자
    body = ("## 장\n\n" + "\n\n".join([para] * 10))
    d = _book(tmp_path, {"ch01.md": body})
    style, _ = pick(d, ["manuscript/ch01.md"])
    assert style == "essay"


def test_mixed_picks_practical(tmp_path):
    """중간 밀도(표 드문드문·짧은 문단) → 신국판 practical."""
    body = "## 장\n\n" + "보통 문단. " * 10 + "\n\n| a |\n|---|\n| 1 |\n"
    d = _book(tmp_path, {"ch01.md": body})
    style, _ = pick(d, ["manuscript/ch01.md"])
    assert style == "practical"


def test_analyze_ignores_fenced_tables(tmp_path):
    """코드펜스 내부 표 구분행은 표로 세지 않는다."""
    md = tmp_path / "x.md"
    md.write_text("```\n|---|\n```\n", encoding="utf-8")
    assert analyze(md)["tables"] == 0
    assert analyze(md)["fences"] == 1  # 펜스 블록 1개(개폐 1회씩 아님)
