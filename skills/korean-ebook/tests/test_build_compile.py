"""Task 3 — PDF 컴파일 통합 테스트 (typst 필요, 없으면 스킵)."""
import shutil
from pathlib import Path

import pytest

from scripts.build import load_config, assemble, compile_pdf

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "sample-manuscript"

pytestmark = pytest.mark.skipif(
    shutil.which("typst") is None, reason="typst 미설치"
)


@pytest.fixture(scope="module")
def compiled(tmp_path_factory):
    book = tmp_path_factory.mktemp("book")
    (book / "typst-build.yaml").write_text(
        "style: lecture\n"
        "title: 샘플책\n"
        "chapters:\n"
        "  - ch01.md\n"
        "  - ch02.md\n",
        encoding="utf-8",
    )
    for name in ("ch01.md", "ch02.md"):
        shutil.copy(FIXTURE_DIR / name, book / name)
    cfg = load_config(book / "typst-build.yaml")
    main = assemble(cfg, book)
    return compile_pdf(main, cfg["title"])


def test_compiles_to_pdf(compiled):
    assert compiled.exists()
    assert compiled.stat().st_size > 1000
