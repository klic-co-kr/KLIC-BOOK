#!/usr/bin/env python3
"""Generate a deterministic structured-summary scaffold from a Korean manuscript.

This script emits EMPTY scaffolds only:

- ``<out_dir>/summary/chapters/ch<NN>-<slug>.md`` per chapter, with the H1
  title, auto-extracted H2 section headings under ``절 구성``, and the four
  agent-fillable sections (핵심 아이디어 / 절 구성 / 주요 개념 / 핵심 요약).
- ``<out_dir>/summary/glossary.md`` with candidate terms (every chapter H2
  heading + every ``**bold**`` span across chapters) listed as commented
  entries for the agent to curate.

It performs NO LLM calls and injects NO content into the original manuscript.
An agent (or human editor) fills the scaffolds afterwards, always citing the
source filename and never asserting beyond the original text.

Usage:
    python3 generate_summary.py <manuscript_dir> <out_dir>
    python3 generate_summary.py <manuscript_dir> <out_dir> --no-auto-terms
    python3 generate_summary.py <manuscript_dir> <out_dir> --note "커스텀 안내문"

Flags:
    --no-auto-terms  Emit NO auto-extracted H2/bold term candidates in the
                     glossary (empty section for the agent to fill manually).
                     Implements ``summary.auto_terms: false`` in book-config.
    --note <text>    Override the hardcoded default editorial note that appears
                     in both the chapter and glossary scaffolds. Implements
                     ``summary.default_note`` in book-config.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Files whose name starts with a two-digit index, e.g. 01-…, 02_…
CHAPTER_FILE_PATTERN = re.compile(r"^[0-9]{2}[-_].*\.md$")
# Leading NN or NN_ / NN- prefix on a filename stem.
_LEADING_INDEX = re.compile(r"^([0-9]{2})[-_]")

# Default editorial notes — the hardcoded values used when ``--note`` is not
# passed. Kept per-scaffold so the default output is byte-identical to the
# pre-flag behaviour; ``--note`` overrides BOTH with the same caller-supplied
# text (the value of ``summary.default_note`` in book-config).
DEFAULT_CHAPTER_NOTE = "편집 요약(원문 대체 아님). 에이전트가 핵심 아이디어·개념·요약 작성."
DEFAULT_GLOSSARY_NOTE = "원문 근거 용어 후보(에이전트가 선별·정의). 원문에 없는 의미 부여 금지."


# ---------------------------------------------------------------------------
# Classification (mirrors publish_book.classify_chapter regex logic, kept
# self-contained so this script has no build-time dependency).
# ---------------------------------------------------------------------------

def classify_kind(title: str) -> str:
    """Return the structural kind of a chapter from its H1 title.

    One of: ``chapter`` | ``appendix`` | ``afterword``.
    Mirrors the regex branches of ``publish_book.classify_chapter`` for the
    부록 / 후기 / N장 families without importing the build module.
    """
    raw = (title or "").strip()
    if not raw:
        return "chapter"
    # 부록 A / 부록 B / 부록1 …
    if re.match(r"^부록\s*[A-Za-z가-힣0-9]+", raw):
        return "appendix"
    # 후기 / 맺음말 / 에필로그
    if raw.startswith(("후기", "맺음말", "에필로그", "에휴로그")):
        return "afterword"
    return "chapter"


# ---------------------------------------------------------------------------
# Pure helpers
# ---------------------------------------------------------------------------

def slugify(stem: str) -> str:
    """Turn a filename stem into a slug. Korean is preserved; the leading
    two-digit index is stripped so ``ch<NN>-<slug>.md`` is not double-numbered;
    whitespace collapses to ``-``.
    """
    s = _LEADING_INDEX.sub("", stem)
    s = s.strip().lower()
    s = re.sub(r"\s+", "-", s)
    return s or stem.lower()


def extract_bold_terms(text: str) -> list[str]:
    """Return ``**term**`` spans in document order (no nested asterisks)."""
    return re.findall(r"\*\*([^*\n]+?)\*\*", text)


def parse_chapter(path: Path) -> dict:
    """Read one chapter file → {path, stem, h1, h2s, kind}."""
    text = path.read_text(encoding="utf-8")
    h1 = ""
    h2s: list[str] = []
    for line in text.splitlines():
        if line.startswith("# ") and not h1:
            h1 = line[2:].strip()
        elif line.startswith("## "):
            h2s.append(line[3:].strip())
    return {
        "path": path,
        "stem": path.stem,
        "h1": h1 or path.stem,
        "h2s": h2s,
        "kind": classify_kind(h1),
    }


def _index_from_name(name: str, fallback: int) -> str:
    m = _LEADING_INDEX.match(name)
    return m.group(1) if m else f"{fallback:02d}"


# ---------------------------------------------------------------------------
# Scaffold builders
# ---------------------------------------------------------------------------

def build_chapter_scaffold(
    ch: dict, book_title: str, note: str = DEFAULT_CHAPTER_NOTE
) -> str:
    title = ch["h1"]
    filename = ch["path"].name
    kind = ch["kind"]
    if ch["h2s"]:
        sections = "\n".join(f"- {h}" for h in ch["h2s"])
    else:
        sections = "- <!-- 원문에 H2 절 제목 없음 -->"
    return (
        f"# {title}\n"
        f"> 원문 근거: {filename} — {note}\n"
        f"<!-- kind: {kind} | book: {book_title} -->\n"
        f"\n"
        f"## 핵심 아이디어\n"
        f"<!-- 에이전트가 1-2문장 작성 (원문 근거 필수) -->\n"
        f"\n"
        f"## 절 구성\n"
        f"{sections}\n"
        f"\n"
        f"## 주요 개념\n"
        f"<!-- 에이전트가 용어 작성 (원문에 없는 의미 부여 금지) -->\n"
        f"\n"
        f"## 핵심 요약\n"
        f"<!-- 에이전트가 3-5 takeaway 작성 -->\n"
    )


def build_glossary(
    book_title: str,
    chapters: list[dict],
    note: str = DEFAULT_GLOSSARY_NOTE,
    auto_terms: bool = True,
) -> str:
    # auto_terms=False (--no-auto-terms) → emit NO auto-extracted H2/bold
    # candidates; leave an empty section for the agent to fill manually.
    if auto_terms:
        candidates: list[str] = []
        for ch in chapters:
            candidates.extend(ch["h2s"])
            candidates.extend(extract_bold_terms(ch["path"].read_text(encoding="utf-8")))
        # de-duplicate, preserve first-seen order
        seen: set[str] = set()
        uniq: list[str] = []
        for c in candidates:
            if c not in seen:
                seen.add(c)
                uniq.append(c)
        if uniq:
            lines = "\n".join(
                f"- **{c}** — <!-- 정의 (원문 근거 필수) -->" for c in uniq
            )
        else:
            lines = "- <!-- 후보 용어 없음 -->"
        extract_comment = (
            "<!-- 후보: chapter H2 headings + bold terms (**term**) 자동 추출 — "
            "에이전트가 선별 -->"
        )
    else:
        lines = "- <!-- auto_terms 비활성화: 에이전트가 직접 용어 추가 (원문 근거 필수) -->"
        extract_comment = (
            "<!-- auto_terms=false: H2/bold 후보 자동 추출 안 함. "
            "에이전트가 원문을 직접 조사해 용어 작성 -->"
        )
    return (
        f"# 용어집 — {book_title}\n"
        f"> {note}\n"
        f"\n"
        f"{extract_comment}\n"
        f"\n"
        f"{lines}\n"
    )


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def generate(
    manuscript_dir: Path,
    out_dir: Path,
    *,
    auto_terms: bool = True,
    note: str | None = None,
) -> int:
    if not manuscript_dir.is_dir():
        print(f"manuscript dir not found: {manuscript_dir}", file=sys.stderr)
        return 2

    files = sorted(
        p for p in manuscript_dir.iterdir()
        if p.is_file() and CHAPTER_FILE_PATTERN.match(p.name)
    )
    if not files:
        print(
            f"no chapter files matching {CHAPTER_FILE_PATTERN.pattern} "
            f"in {manuscript_dir}",
            file=sys.stderr,
        )
        return 1

    chapters = [parse_chapter(p) for p in files]
    book_title = manuscript_dir.name

    # One ``--note`` (== summary.default_note) overrides both per-scaffold
    # defaults; when not supplied, each builder keeps its hardcoded note so
    # default output is unchanged.
    chapter_note = note if note is not None else DEFAULT_CHAPTER_NOTE
    glossary_note = note if note is not None else DEFAULT_GLOSSARY_NOTE

    summary_dir = out_dir / "summary"
    chapters_dir = summary_dir / "chapters"
    chapters_dir.mkdir(parents=True, exist_ok=True)

    # Idempotent: remove stale chapter scaffolds so re-runs converge cleanly
    # even when a source chapter is renamed or deleted.
    for old in chapters_dir.glob("ch*.md"):
        old.unlink()

    for idx, ch in enumerate(chapters, start=1):
        nn = _index_from_name(ch["path"].name, idx)
        slug = slugify(ch["stem"])
        out_path = chapters_dir / f"ch{nn}-{slug}.md"
        out_path.write_text(
            build_chapter_scaffold(ch, book_title, note=chapter_note),
            encoding="utf-8",
        )

    glossary_path = summary_dir / "glossary.md"
    glossary_path.write_text(
        build_glossary(
            book_title, chapters, note=glossary_note, auto_terms=auto_terms
        ),
        encoding="utf-8",
    )

    print(
        f"generated summary scaffold → {summary_dir} "
        f"({len(chapters)} chapters + glossary)"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="generate_summary.py",
        description=(
            "Generate a deterministic summary scaffold (chapter summaries + "
            "glossary) from a Korean manuscript. Emits EMPTY scaffolds only."
        ),
    )
    parser.add_argument("manuscript_dir", help="manuscript directory (NN-*.md files)")
    parser.add_argument("out_dir", help="output directory (summary/ is written here)")
    parser.add_argument(
        "--no-auto-terms",
        action="store_true",
        default=False,
        help=(
            "Emit NO auto-extracted H2/bold term candidates in the glossary "
            "(empty section for the agent to fill manually). Use when "
            "summary.auto_terms is false in book-config."
        ),
    )
    parser.add_argument(
        "--note",
        default=None,
        metavar="<text>",
        help=(
            "Override the hardcoded default editorial note in both the chapter "
            "and glossary scaffolds. Pass summary.default_note from book-config."
        ),
    )
    args = parser.parse_args(argv)
    return generate(
        Path(args.manuscript_dir).resolve(),
        Path(args.out_dir).resolve(),
        auto_terms=not args.no_auto_terms,
        note=args.note,
    )


if __name__ == "__main__":
    raise SystemExit(main())
