from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
PUBLISH_BOOK = REPO_ROOT / "skills" / "korean-ebook" / "scripts" / "publish_book.py"
SPEC = importlib.util.spec_from_file_location("korean_ebook_publish_book", PUBLISH_BOOK)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_embedded_figure_preserves_following_markdown_heading(tmp_path: Path) -> None:
    (tmp_path / "figure.svg").write_text("<svg/>", encoding="utf-8")
    source = """<!-- figure-spec
id: FIG-999
output: figure.svg
alt_ko: 테스트 도형
caption_ko: 테스트 캡션
-->

## 다음 절
"""

    processed, _ = MODULE.embed_figure_specs(source, tmp_path)
    rendered = MODULE.markdown_renderer()(processed)

    assert "<h2>다음 절</h2>" in rendered
    assert "## 다음 절" not in rendered
