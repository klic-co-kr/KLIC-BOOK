"""Tests for generate_summary.py — deterministic summary scaffold generator.

Discipline: the script must emit EMPTY scaffolds only (no LLM, no injected
claims). These tests pin that contract: chapter files contain the required
section headers + auto-extracted H2 sections + source citation, the glossary
lists H2/bold-term candidates as commented entries, and re-runs are idempotent.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import generate_summary

SCRIPT = Path(generate_summary.__file__)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _make_manuscript(tmp_path: Path) -> Path:
    """Build a tiny manuscript: 2 numbered chapters + a README to be skipped."""
    md = tmp_path / "manuscript"
    md.mkdir()
    (md / "01-제1장-서론.md").write_text(
        "# 제1장 서론\n"
        "\n"
        "**핵심용어**와 **배포모델**을 정의한다.\n"
        "\n"
        "## 배경\n"
        "\n"
        "왜 이 장이 필요한지 원문이 설명한다.\n"
        "\n"
        "## 목표\n"
        "\n"
        "검증 가능한 산출물을 정의한다.\n",
        encoding="utf-8",
    )
    (md / "02-부록A-용어.md").write_text(
        "# 부록 A 용어 정리\n"
        "\n"
        "## 기본 개념\n"
        "\n"
        "**배포모델**에 대한 설명. 본문에 없는 의미를 덧붙이지 않는다.\n",
        encoding="utf-8",
    )
    # README must be skipped (does not match ^NN[-_] pattern, but assert anyway)
    (md / "README.md").write_text("# readme — not a chapter\n", encoding="utf-8")
    return md


def _run(manuscript: Path, out: Path, *extra: str):
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(manuscript), str(out), *extra],
        capture_output=True, text=True,
    )


# ---------------------------------------------------------------------------
# Unit tests — pure helpers
# ---------------------------------------------------------------------------

def test_classify_kind_detects_appendix_afterword_chapter():
    assert generate_summary.classify_kind("부록 A 용어 정리") == "appendix"
    assert generate_summary.classify_kind("후기") == "afterword"
    assert generate_summary.classify_kind("맺음말을 열며") == "afterword"
    assert generate_summary.classify_kind("제1장 서론") == "chapter"
    assert generate_summary.classify_kind("1장 진단") == "chapter"


def test_classify_kind_empty_and_unknown_defaults_chapter():
    assert generate_summary.classify_kind("") == "chapter"
    assert generate_summary.classify_kind("이름 없는 장") == "chapter"


def test_slugify_strips_leading_prefix_preserves_korean():
    assert generate_summary.slugify("01-제1장-서론") == "제1장-서론"
    assert generate_summary.slugify("02_부록A-용어") == "부록a-용어"
    # prefix stripped, then internal spaces collapse to hyphens
    assert generate_summary.slugify("03-some title here") == "some-title-here"


def test_extract_bold_terms_finds_spans():
    terms = generate_summary.extract_bold_terms("a **용어** and **배포모델** here.")
    assert terms == ["용어", "배포모델"]


# ---------------------------------------------------------------------------
# Integration tests — CLI contract
# ---------------------------------------------------------------------------

def test_generates_chapter_scaffolds(tmp_path):
    md = _make_manuscript(tmp_path)
    out = tmp_path / "out"
    res = _run(md, out)
    assert res.returncode == 0, res.stderr

    chap_dir = out / "summary" / "chapters"
    ch01 = list(chap_dir.glob("ch01-*.md"))
    ch02 = list(chap_dir.glob("ch02-*.md"))
    assert len(ch01) == 1, f"expected 1 ch01 file, got {ch01}"
    assert len(ch02) == 1, f"expected 1 ch02 file, got {ch02}"

    text01 = ch01[0].read_text(encoding="utf-8")
    # required scaffold sections
    assert "## 핵심 아이디어" in text01
    assert "## 절 구성" in text01
    assert "## 주요 개념" in text01
    assert "## 핵심 요약" in text01
    # auto-extracted H2 sections (절 구성 is populated from the source)
    assert "- 배경" in text01
    assert "- 목표" in text01
    # 원문 근거 citation (filename) present
    assert "01-제1장-서론.md" in text01
    # title is the H1
    assert "# 제1장 서론" in text01
    # README must not have produced a scaffold
    assert not list(chap_dir.glob("*README*"))


def test_appendix_kind_detected_in_metadata(tmp_path):
    md = _make_manuscript(tmp_path)
    out = tmp_path / "out"
    _run(md, out)
    ch02 = list((out / "summary" / "chapters").glob("ch02-*.md"))[0]
    text = ch02.read_text(encoding="utf-8")
    assert "kind: appendix" in text


def test_glossary_exists_with_candidates(tmp_path):
    md = _make_manuscript(tmp_path)
    out = tmp_path / "out"
    _run(md, out)
    glossary = out / "summary" / "glossary.md"
    assert glossary.exists()
    g = glossary.read_text(encoding="utf-8")
    assert "용어집" in g
    assert "원문에 없는 의미 부여 금지" in g
    # bold-term candidates
    assert "핵심용어" in g
    assert "배포모델" in g
    # H2-heading candidate
    assert "배경" in g
    assert "기본 개념" in g


def test_summary_message_counts_chapters(tmp_path):
    md = _make_manuscript(tmp_path)
    out = tmp_path / "out"
    res = _run(md, out)
    assert "generated summary scaffold" in res.stdout
    assert "2 chapters" in res.stdout


def test_idempotent_rerun(tmp_path):
    md = _make_manuscript(tmp_path)
    out = tmp_path / "out"
    _run(md, out)
    chap_dir = out / "summary" / "chapters"
    first_files = sorted(p.name for p in chap_dir.glob("ch*.md"))
    first_contents = {p.name: p.read_text(encoding="utf-8") for p in chap_dir.glob("ch*.md")}
    glossary_first = (out / "summary" / "glossary.md").read_text(encoding="utf-8")

    # second run over same out_dir
    res = _run(md, out)
    assert res.returncode == 0, res.stderr

    second_files = sorted(p.name for p in chap_dir.glob("ch*.md"))
    assert second_files == first_files, "file set changed on re-run"
    for name, content in first_contents.items():
        assert (chap_dir / name).read_text(encoding="utf-8") == content, (
            f"{name} content drifted on re-run"
        )
    assert (out / "summary" / "glossary.md").read_text(encoding="utf-8") == glossary_first


def test_stale_chapter_file_removed_on_rerun(tmp_path):
    """Idempotency must also clean up a chapter that no longer exists in source."""
    md = _make_manuscript(tmp_path)
    out = tmp_path / "out"
    _run(md, out)
    chap_dir = out / "summary" / "chapters"
    # seed a stale scaffold file that has no source counterpart
    stale = chap_dir / "ch99-ghost.md"
    stale.write_text("# ghost\n", encoding="utf-8")
    assert stale.exists()
    _run(md, out)
    assert not stale.exists(), "stale chapter scaffold should be removed on re-run"


# ---------------------------------------------------------------------------
# Config-contract tests — summary.auto_terms / summary.default_note wiring
# ---------------------------------------------------------------------------

def test_no_auto_terms_flag_omits_glossary_candidates(tmp_path):
    """--no-auto-terms (summary.auto_terms: false) → glossary must emit NO
    auto-extracted H2/bold candidates; an empty agent-fill section instead."""
    md = _make_manuscript(tmp_path)
    out = tmp_path / "out"
    res = _run(md, out, "--no-auto-terms")
    assert res.returncode == 0, res.stderr

    glossary = out / "summary" / "glossary.md"
    assert glossary.exists()
    g = glossary.read_text(encoding="utf-8")
    # glossary header + discipline still present
    assert "용어집" in g
    # auto-extracted candidate terms must NOT appear as candidate entries
    assert "- **핵심용어**" not in g
    assert "- **배포모델**" not in g
    # H2-heading candidates must NOT appear either
    assert "- **배경**" not in g
    assert "- **기본 개념**" not in g
    # the disablement marker + empty fill-manually placeholder are present
    assert "auto_terms=false" in g or "auto_terms 비활성화" in g
    assert "직접 용어 추가" in g or "직접 조사" in g


def test_note_flag_overrides_default_note_in_both_scaffolds(tmp_path):
    """--note <text> (summary.default_note) → both chapter + glossary scaffolds
    contain the caller-supplied note text instead of the hardcoded default."""
    md = _make_manuscript(tmp_path)
    out = tmp_path / "out"
    custom = "커스텀 편집 노트 — 원문을 대체하지 않는다."
    res = _run(md, out, "--note", custom)
    assert res.returncode == 0, res.stderr

    # chapter scaffold carries the custom note (and still cites the filename)
    ch01 = list((out / "summary" / "chapters").glob("ch01-*.md"))[0]
    chap_text = ch01.read_text(encoding="utf-8")
    assert custom in chap_text
    assert "01-제1장-서론.md" in chap_text  # filename citation preserved
    # the old hardcoded chapter tail is no longer the note line
    assert "에이전트가 핵심 아이디어·개념·요약 작성." not in chap_text

    # glossary scaffold carries the custom note too
    glossary = out / "summary" / "glossary.md"
    g = glossary.read_text(encoding="utf-8")
    assert custom in g
    # default glossary note is replaced
    assert "원문 근거 용어 후보(에이전트가 선별·정의)." not in g
    # candidate extraction still works by default (auto_terms untouched)
    assert "- **핵심용어**" in g
