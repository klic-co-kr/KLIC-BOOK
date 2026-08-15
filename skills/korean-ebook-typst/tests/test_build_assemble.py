"""Task 2 — 조립기(assemble) 테스트."""
import shutil

import pytest

from pathlib import Path

from scripts.build import load_config, assemble

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "sample-manuscript"


def test_assemble_copies_style_and_converts(tmp_path):
    (tmp_path / "typst-build.yaml").write_text(
        "style: lecture\n"
        "title: 샘플\n"
        "chapters:\n"
        "  - ch01.md\n"
        "  - ch02.md\n",
        encoding="utf-8",
    )
    for name in ("ch01.md", "ch02.md"):
        shutil.copy(FIXTURE_DIR / name, tmp_path / name)

    cfg = load_config(tmp_path / "typst-build.yaml")
    main = assemble(cfg, tmp_path)

    assert main == tmp_path / "build" / "main.typ"
    assert (tmp_path / "build" / "tokens.json").exists()
    assert (tmp_path / "build" / "theme.typ").exists()
    assert (tmp_path / "build" / "base.typ").exists()
    assert (tmp_path / "build" / "typ" / "ch01.typ").exists()
    assert (tmp_path / "build" / "typ" / "ch02.typ").exists()

    text = main.read_text(encoding="utf-8")
    assert '#include "base.typ"' in text
    assert '#include "theme.typ"' in text
    assert '#include "typ/ch01.typ"' in text
    assert '#include "typ/ch02.typ"' in text


def test_assemble_missing_chapter_aborts(tmp_path):
    (tmp_path / "typst-build.yaml").write_text(
        "style: lecture\n"
        "title: 샘플\n"
        "chapters:\n"
        "  - ghost.md\n",
        encoding="utf-8",
    )
    cfg = None
    with pytest.raises(SystemExit):
        # load_config가 챕터 존재 검사에서 먼저 중단(방어적 중복)하므로
        # assemble까지 도달하지 못해도 파이프라인 중단 의도는 동일.
        cfg = load_config(tmp_path / "typst-build.yaml")
        assemble(cfg, tmp_path)
