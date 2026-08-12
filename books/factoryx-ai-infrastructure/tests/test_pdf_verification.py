from __future__ import annotations

import importlib.util
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
VERIFY_PDF = REPO_ROOT / "skills" / "korean-ebook" / "scripts" / "verify_pdf.py"
SPEC = importlib.util.spec_from_file_location("korean_ebook_verify_pdf", VERIFY_PDF)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_normalize_text_tolerates_pdftotext_url_dehyphenation() -> None:
    source = "https://example.com/integrated-design-principles"
    extracted = "https://example.com/integrated-design\nprinciples"

    assert MODULE.normalize_text(source) == MODULE.normalize_text(extracted)
