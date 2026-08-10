#!/usr/bin/env python3
"""Build a Korean editorial book PDF from Markdown content.

The script deliberately keeps content and references separate. Reference files are
recorded in the manifest but never parsed into the book body.
"""

from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import hashlib
import html
import json
import os
import re
import shutil
import sys
import tempfile
import unicodedata
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote, urlparse

try:
    import mistune
    import yaml
    from bs4 import BeautifulSoup
    from pypdf import PdfReader
    from weasyprint import HTML
except ImportError as exc:  # pragma: no cover - dependency preflight
    print(f"Missing dependency: {exc}", file=sys.stderr)
    print("Run: python -m pip install -r scripts/requirements.txt", file=sys.stderr)
    raise SystemExit(2) from exc


SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = SKILL_ROOT / "assets" / "book-config.example.yaml"


@dataclass
class SourceDoc:
    path: Path
    rel_path: str
    raw_text: str
    processed_markdown: str
    title: str
    headings: list[tuple[int, str]] = field(default_factory=list)
    section_titles: list[str] = field(default_factory=list)
    html_body: str = ""
    anchor: str = ""
    sha256: str = ""
    counts: dict[str, int] = field(default_factory=dict)
    probes: list[dict[str, Any]] = field(default_factory=list)


class BuildError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).strip().lower()
    normalized = re.sub(r"[^0-9a-z가-힣]+", "-", normalized)
    normalized = re.sub(r"-+", "-", normalized).strip("-")
    return normalized or "section"


def safe_filename(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).strip()
    value = re.sub(r"[\\/:*?\"<>|]+", "_", value)
    value = re.sub(r"\s+", "_", value)
    value = re.sub(r"_+", "_", value).strip("._")
    return value or "book"


def natural_sort_key(value: str) -> list[Any]:
    parts = re.split(r"(\d+)", value.casefold())
    return [int(part) if part.isdigit() else part for part in parts]


def repair_zip_name(name: str) -> str:
    """Repair UTF-8 filenames stored without the ZIP UTF-8 flag.

    Python follows the ZIP specification and decodes such names as CP437. Some
    archivers nevertheless write raw UTF-8 bytes while leaving the flag unset.
    Re-encoding the decoded string as CP437 and decoding as UTF-8 recovers the
    original name. Already-correct Unicode names are left untouched.
    """

    try:
        candidate = name.encode("cp437").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return name

    def quality(value: str) -> tuple[int, int, int]:
        korean = sum(1 for ch in value if "가" <= ch <= "힣")
        suspicious = sum(1 for ch in value if ch in "∞δφΩ╢╕╣╔╠╬╩╦╪╫╧╨╤╥╙╘╓╒")
        replacements = value.count("�")
        return korean, -suspicious, -replacements

    return candidate if quality(candidate) > quality(name) else name


def safe_extract_zip(zip_path: Path, dest: Path) -> None:
    """Extract a ZIP safely while repairing common Korean filename mojibake."""

    dest_resolved = dest.resolve()
    with zipfile.ZipFile(zip_path) as zf:
        for member in zf.infolist():
            repaired = repair_zip_name(member.filename).replace("\\", "/")
            if not repaired or repaired.startswith("__MACOSX/"):
                continue

            target = (dest / repaired).resolve()
            if not str(target).startswith(str(dest_resolved) + os.sep) and target != dest_resolved:
                raise BuildError(f"Unsafe ZIP path: {member.filename}")

            # Reject symbolic links. They can escape the extraction root later.
            unix_mode = (member.external_attr >> 16) & 0o170000
            if unix_mode == 0o120000:
                raise BuildError(f"ZIP symbolic links are not supported: {member.filename}")

            if member.is_dir() or repaired.endswith("/"):
                target.mkdir(parents=True, exist_ok=True)
                continue

            target.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(member, "r") as source, target.open("wb") as output:
                shutil.copyfileobj(source, output)


def load_config(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    for section in ("book", "files", "editorial", "style", "quality", "visuals"):
        data.setdefault(section, {})
    return data


def split_single_markdown(
    input_path: Path, workdir: Path, config: dict[str, Any] | None = None
) -> Path:
    """Split one concatenated Markdown manuscript into per-H1 chapter files.

    A full-book markdown normally leads with a title block (book title H1 +
    subtitle + metadata) and a hand-written table of contents. Both are dropped
    here because the skill regenerates cover, title page and TOC. ``목차`` /
    ``차례`` H1 sections are skipped for the same reason. Everything else becomes
    one ordered file per H1, so the downstream multi-file pipeline (ordering,
    classification, openers) applies unchanged.
    """
    text = strip_yaml_frontmatter(input_path.read_text(encoding="utf-8-sig"))
    lines = text.splitlines(keepends=True)
    chunks: list[tuple[str, str]] = []
    cur_title = ""
    cur: list[str] = []
    for line in lines:
        m = re.match(r"^#\s+(.*?)\s*$", line)
        if m:
            if cur_title or cur:
                chunks.append((cur_title, "".join(cur)))
            cur_title = m.group(1).strip()
            cur = [line]
        else:
            cur.append(line)
    if cur_title or cur:
        chunks.append((cur_title, "".join(cur)))

    skip_exact = {"목차", "차례", "contents", "table of contents", "toc"}
    book_title = ""
    if config:
        book_title = str(config.get("book", {}).get("title", "") or "").strip()

    out_dir = workdir / "content"
    out_dir.mkdir(parents=True, exist_ok=True)
    order = 0
    for title, body in chunks:
        tl = title.strip().strip('"\'"').strip()
        if tl.casefold() in skip_exact:
            continue
        # Drop the leading title block: empty-title pre-H1 fluff (e.g. a cover
        # image line), a chunk whose title equals the configured book title, or
        # any chunk carrying a cover-image marker. The skill regenerates cover,
        # title page and TOC itself.
        is_title_block = (
            not tl
            or (book_title and tl == book_title)
            or "![표지" in body
            or "![cover" in body.casefold()
        )
        if is_title_block:
            continue
        order += 1
        fname = f"{order:02d}-{slugify(tl) or 'section'}.md"
        (out_dir / fname).write_text(body, encoding="utf-8")
    if order == 0:
        raise BuildError("Single-file input yielded no chapters after splitting")
    return out_dir.resolve()


def resolve_input(
    input_path: Path, workdir: Path, config: dict[str, Any] | None = None
) -> Path:
    if input_path.is_dir():
        return input_path.resolve()
    if input_path.is_file() and input_path.suffix.casefold() == ".zip":
        extracted = workdir / "content"
        extracted.mkdir(parents=True, exist_ok=True)
        safe_extract_zip(input_path, extracted)
        children = [p for p in extracted.iterdir() if p.name not in {"__MACOSX"}]
        if len(children) == 1 and children[0].is_dir():
            return children[0].resolve()
        return extracted.resolve()
    if input_path.is_file() and input_path.suffix.casefold() in {".md", ".markdown"}:
        return split_single_markdown(input_path, workdir, config)
    raise BuildError(f"Input must be a directory, ZIP, or single Markdown file: {input_path}")


def is_excluded(rel_path: str, patterns: Iterable[str]) -> bool:
    rel = rel_path.replace(os.sep, "/")
    return any(fnmatch.fnmatch(rel, pattern) for pattern in patterns)


def discover_markdown_files(root: Path, config: dict[str, Any]) -> list[Path]:
    file_cfg = config["files"]
    include_patterns = file_cfg.get("include") or ["*.md", "**/*.md"]
    exclude_patterns = file_cfg.get("exclude") or []
    found: dict[str, Path] = {}
    for pattern in include_patterns:
        for path in root.glob(pattern):
            if not path.is_file() or path.suffix.casefold() not in {".md", ".markdown"}:
                continue
            rel = path.relative_to(root).as_posix()
            if not is_excluded(rel, exclude_patterns):
                found[rel] = path
    if not found:
        raise BuildError(f"No Markdown files found under {root}")

    ordered: list[Path] = []
    explicit_order = file_cfg.get("order") or []
    for item in explicit_order:
        candidate = (root / item).resolve()
        if candidate.exists() and candidate.is_file():
            ordered.append(candidate)
            found.pop(candidate.relative_to(root).as_posix(), None)
        else:
            raise BuildError(f"Configured file not found: {item}")

    front_name = file_cfg.get("front_matter_file")
    if front_name:
        matches = [p for p in found.values() if p.name.casefold() == Path(front_name).name.casefold()]
        if matches:
            chosen = sorted(matches, key=lambda p: len(p.parts))[0]
            ordered.append(chosen)
            found.pop(chosen.relative_to(root).as_posix(), None)

    ordered.extend(sorted(found.values(), key=lambda p: natural_sort_key(p.relative_to(root).as_posix())))
    # de-duplicate while preserving order
    seen: set[Path] = set()
    result: list[Path] = []
    for p in ordered:
        rp = p.resolve()
        if rp not in seen:
            seen.add(rp)
            result.append(rp)
    return result


def strip_yaml_frontmatter(text: str) -> str:
    if text.startswith("---\n") or text.startswith("---\r\n"):
        lines = text.splitlines(keepends=True)
        for idx in range(1, min(len(lines), 200)):
            if lines[idx].strip() == "---":
                return "".join(lines[idx + 1 :])
    return text


def clean_heading(text: str) -> str:
    text = re.sub(r"\s+#+\s*$", "", text.strip())
    text = re.sub(r"\[(.*?)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"~~([^~]+)~~", r"\1", text)
    text = re.sub(r"[*_`]", "", text)
    return html.unescape(text).strip()


def extract_title(text: str, fallback: str) -> str:
    match = re.search(r"(?m)^#\s+(.+?)\s*$", text)
    return clean_heading(match.group(1)) if match else fallback


def extract_headings(text: str) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    in_fence = False
    fence_marker = ""
    for line in text.splitlines():
        stripped = line.lstrip()
        fence = re.match(r"^(```+|~~~+)", stripped)
        if fence:
            marker = fence.group(1)[0]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
            continue
        if in_fence:
            continue
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", stripped)
        if match:
            result.append((len(match.group(1)), clean_heading(match.group(2))))
    return result


def remove_first_h1(text: str) -> str:
    return re.sub(r"(?m)^#\s+.+?\s*\n+", "", text, count=1)


def strip_named_h2_sections(text: str, names: Iterable[str]) -> tuple[str, list[str]]:
    names_norm = {slugify(name) for name in names}
    if not names_norm:
        return text, []
    lines = text.splitlines(keepends=True)
    output: list[str] = []
    removed: list[str] = []
    skipping = False
    current_name = ""
    for line in lines:
        match = re.match(r"^##\s+(.+?)\s*$", line.strip())
        if match:
            heading = clean_heading(match.group(1))
            if slugify(heading) in names_norm:
                skipping = True
                current_name = heading
                removed.append(heading)
                continue
            if skipping:
                skipping = False
                current_name = ""
        if not skipping:
            output.append(line)
    return "".join(output), removed


def sanitize_code_markers(text: str) -> str:
    """비표준 [code]/[/code] 마커를 markdown 코드블록으로 정규화한다.

    일부 변환 도구(html2text mark_code 등)가 <code>를 [code]/[/code]로 감싸는데,
    mistune은 이를 인식하지 못해 마커가 본문에 문자 그대로 남는다. markdown 표준
    펜스(``````)로 바꿔 코드블록으로 렌더링되게 한다.
    """
    text = re.sub(r"(?m)^\[code\]\s*$", "```", text)
    return re.sub(r"(?m)^\[/code\]\s*$", "```", text)


def normalize_markdown_block(value: str) -> str:
    """Normalize a Markdown paragraph for exact editorial transforms.

    This is intentionally conservative. It removes only lightweight Markdown
    punctuation and collapses whitespace so configured boilerplate can be
    moved or omitted without affecting ordinary manuscript prose.
    """

    value = unicodedata.normalize("NFKC", value).strip()
    value = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"[*_`~]", "", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def strip_matching_markdown_paragraphs(text: str, patterns: Iterable[str]) -> tuple[str, list[str]]:
    """Remove only explicitly configured paragraph blocks.

    A pattern is treated as an exact normalized paragraph by default. A value
    wrapped in ``/.../`` is treated as a regular expression. This transform is
    intended for duplicated repository chrome such as a trailing GitHub call
    to action that has been deliberately moved to the editorial note.
    """

    exact: set[str] = set()
    regexes: list[re.Pattern[str]] = []
    for raw_pattern in patterns:
        pattern = str(raw_pattern).strip()
        if len(pattern) >= 2 and pattern.startswith("/") and pattern.endswith("/"):
            regexes.append(re.compile(pattern[1:-1]))
        elif pattern:
            exact.add(normalize_markdown_block(pattern))
    if not exact and not regexes:
        return text, []

    parts = re.split(r"(\n[ \t]*\n+)", text)
    removed: list[str] = []
    output: list[str] = []
    for part in parts:
        if re.fullmatch(r"\n[ \t]*\n+", part or ""):
            output.append(part)
            continue
        normalized = normalize_markdown_block(part)
        matched = normalized in exact or any(regex.search(normalized) for regex in regexes)
        if matched:
            removed.append(normalized)
        else:
            output.append(part)

    result = "".join(output)
    result = re.sub(r"\n[ \t]*\n(?:[ \t]*\n)+", "\n\n", result)
    return result.strip() + ("\n" if result.strip() else ""), removed


def format_build_date(value: str, mode: str) -> str:
    """Format an ISO build date for human-facing book chrome."""

    if mode.casefold() != "korean":
        return value
    try:
        parsed = dt.date.fromisoformat(value)
    except ValueError:
        return value
    return f"{parsed.year}년 {parsed.month}월 {parsed.day}일"


def count_markdown(text: str) -> dict[str, int]:
    headings = extract_headings(text)
    lines = text.splitlines()
    in_fence = False
    paragraphs = 0
    list_items = 0
    table_rows = 0
    links = 0
    images = 0
    footnotes = 0
    buffer: list[str] = []

    def flush() -> None:
        nonlocal paragraphs, buffer
        if buffer:
            paragraphs += 1
            buffer = []

    for line in lines:
        s = line.strip()
        if re.match(r"^(```+|~~~+)", s):
            flush()
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not s:
            flush()
            continue
        if re.match(r"^#{1,6}\s+", s) or s == "---":
            flush()
            continue
        if re.match(r"^(?:[-+*]|\d+[.)])\s+", s):
            flush()
            list_items += 1
        elif s.startswith("|") and s.endswith("|"):
            flush()
            if not re.match(r"^\|?\s*:?-+:?", s):
                table_rows += 1
        else:
            buffer.append(s)
        links += len(re.findall(r"(?<!!)\[[^]]+\]\([^)]+\)", line))
        images += len(re.findall(r"!\[[^]]*\]\([^)]+\)", line))
        footnotes += len(re.findall(r"\[\^[^]]+\]", line))
    flush()
    return {
        "h1": sum(1 for level, _ in headings if level == 1),
        "h2": sum(1 for level, _ in headings if level == 2),
        "h3": sum(1 for level, _ in headings if level == 3),
        "paragraphs": paragraphs,
        "list_items": list_items,
        "table_rows": table_rows,
        "links": links,
        "images": images,
        "footnote_markers": footnotes,
    }


def normalize_probe_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", value)
    value = re.sub(r"\s+", "", value)
    value = value.replace("–", "-").replace("—", "-")
    return value


def make_probes(html_body: str, min_chars: int, limit: int) -> list[dict[str, Any]]:
    soup = BeautifulSoup(html_body, "html.parser")
    probes: list[dict[str, Any]] = []
    for tag in soup.find_all(["p", "li", "td", "th", "blockquote"]):
        text = tag.get_text(" ", strip=True)
        norm = normalize_probe_text(text)
        if len(norm) < min_chars:
            continue
        edge = min(22, max(12, len(norm) // 4))
        probe = norm[:edge] + "…" + norm[-edge:]
        probes.append(
            {
                "probe": probe,
                "prefix": norm[:edge],
                "suffix": norm[-edge:],
                "length": len(norm),
                "sha256": hashlib.sha256(norm.encode("utf-8")).hexdigest(),
            }
        )
        if len(probes) >= limit:
            break
    return probes


def markdown_renderer() -> Any:
    return mistune.create_markdown(
        escape=False,
        plugins=["strikethrough", "footnotes", "table", "task_lists", "url"],
    )


def rewrite_doc_html(
    body_html: str,
    doc: SourceDoc,
    doc_index: int,
    content_root: Path,
    path_to_anchor: dict[str, str],
    used_ids: set[str],
    warnings: list[str],
) -> str:
    soup = BeautifulSoup(body_html, "html.parser")
    heading_counter = 0
    for heading in soup.find_all(re.compile(r"^h[1-6]$")):
        heading_counter += 1
        title = heading.get_text(" ", strip=True)
        base = f"{doc.anchor}-{slugify(title)}"
        candidate = base
        suffix = 2
        while candidate in used_ids:
            candidate = f"{base}-{suffix}"
            suffix += 1
        used_ids.add(candidate)
        heading["id"] = candidate
        heading["data-source"] = doc.rel_path

    for image in soup.find_all("img"):
        src = image.get("src", "")
        parsed = urlparse(src)
        if parsed.scheme in {"http", "https"}:
            warnings.append(f"External image may not render offline: {src}")
            continue
        if parsed.scheme == "data":
            warnings.append(f"Embedded data image found in {doc.rel_path}; keep only when explicitly intended")
            continue
        resolved = (doc.path.parent / unquote(parsed.path)).resolve()
        if not resolved.exists():
            warnings.append(f"Missing image in {doc.rel_path}: {src}")
        else:
            image["src"] = resolved.as_uri()
        if not image.get("alt"):
            image["alt"] = ""

    for link in soup.find_all("a"):
        href = link.get("href", "")
        parsed = urlparse(href)
        if parsed.scheme or href.startswith("#"):
            continue
        target_path = unquote(parsed.path)
        if target_path.lower().endswith((".md", ".markdown")):
            resolved = (doc.path.parent / target_path).resolve()
            try:
                rel = resolved.relative_to(content_root).as_posix()
            except ValueError:
                rel = target_path.replace("\\", "/")
            anchor = path_to_anchor.get(rel)
            if anchor:
                link["href"] = f"#{anchor}"
            else:
                warnings.append(f"Unresolved Markdown link in {doc.rel_path}: {href}")

    wrapper = soup.new_tag("div")
    wrapper["class"] = ["source-document"]
    wrapper["data-source-file"] = doc.rel_path
    for child in list(soup.contents):
        wrapper.append(child.extract())
    return str(wrapper)


FRONT_MATTER_TITLES = {
    "머리말", "서문", "들어가며", "프롤로그", "서", "여는 글",
    "이 책을 사용하는 방법", "이 책을 읽는 법", "읽는 방법", "읽는 법",
    "이 책에 관하여", "책 소개",
}


def classify_chapter(title: str, index: int) -> dict[str, str]:
    """Classify a chapter title into a structural kind.

    kinds: chapter | appendix | afterword | part | frontmatter
    Each result carries: kind, eyebrow, number, display_title, clean_title.
    clean_title is the reader-facing title with any numbering prefix removed,
    so the opener can show "CHAPTER 01" + "요구사항에서 시스템 경계까지"
    without a redundant duplicate number.
    """
    raw = (title or "").strip()
    clean = raw

    # 부록 A / 부록 B ...
    match = re.match(r"^부록\s*([A-Za-z가-힣0-9]+)\s*[-–—:]?\s*(.*)$", raw)
    if match:
        clean = match.group(2).strip() or raw
        return {"kind": "appendix", "eyebrow": "APPENDIX",
                "number": match.group(1).upper(), "display_title": raw, "clean_title": clean}

    # 후기 / 맺음말 / 에필로그
    if raw.startswith(("후기", "맺음말", "에필로그", "에휴로그")):
        return {"kind": "afterword", "eyebrow": "AFTERWORD",
                "number": "후기", "display_title": raw, "clean_title": raw}

    # Part divider: "Part 1. ...", "Part I ...", "제1부 ..."
    match = re.match(r"^Part\s+([0-9IVXLCDM]+)\b[\s.:：—–-]*\s*(.*)$", raw) or \
        re.match(r"^제\s*([0-9]+)\s*부[\s.:：—–-]*\s*(.*)$", raw)
    if match:
        clean = match.group(2).strip() or raw
        return {"kind": "part", "eyebrow": "PART",
                "number": match.group(1), "display_title": raw, "clean_title": clean}

    # chapter "N장 ..." (Korean)
    match = re.match(r"^(\d+)\s*장\s*(.*)$", raw)
    if match:
        clean = match.group(2).strip() or raw
        return {"kind": "chapter", "eyebrow": "CHAPTER",
                "number": f"{int(match.group(1)):02d}", "display_title": raw, "clean_title": clean}

    # chapter "NN. ..." / "NN) ..." / "NN、" / "NN、" (number prefix, common in
    # concatenated single-file manuscripts)
    match = re.match(r"^0*([0-9]{1,3})\s*[.）、]\s*(.*)$", raw)
    if match:
        clean = match.group(2).strip() or raw
        return {"kind": "chapter", "eyebrow": "CHAPTER",
                "number": f"{int(match.group(1)):02d}", "display_title": raw, "clean_title": clean}

    # front matter: preface / how-to-read / about
    if raw in FRONT_MATTER_TITLES or any(raw.startswith(t) for t in
                                         ("머리말", "서문", "들어가며", "프롤로그", "여는 글")):
        return {"kind": "frontmatter", "eyebrow": "FRONT MATTER",
                "number": "", "display_title": raw, "clean_title": raw}

    return {"kind": "chapter", "eyebrow": "CHAPTER",
            "number": f"{index:02d}", "display_title": raw, "clean_title": raw}


def split_title_for_cover(title: str) -> str:
    words = title.split()
    if len(words) <= 3:
        return html.escape(title)
    midpoint = max(1, len(words) // 2)
    return html.escape(" ".join(words[:midpoint])) + "<br>" + html.escape(" ".join(words[midpoint:]))


def extract_title_quote(front_doc: SourceDoc | None) -> str:
    if not front_doc:
        return ""
    soup = BeautifulSoup(front_doc.html_body, "html.parser")
    for p in soup.find_all("p"):
        strong = p.find("strong")
        text = p.get_text(" ", strip=True)
        if strong and 25 <= len(text) <= 220:
            return text
    return ""


COVER_THEMES = {
    "midnight": {"navy": "#081827", "navy_alt": "#102B38", "cyan": "#36C7D0", "cyan_dark": "#0F8790", "amber": "#D39A2C"},
    "burgundy": {"navy": "#2A1219", "navy_alt": "#3A1A22", "cyan": "#D96E5A", "cyan_dark": "#B5523F", "amber": "#E8B86D"},
    "forest":   {"navy": "#0E2A22", "navy_alt": "#143A2E", "cyan": "#C9A24B", "cyan_dark": "#A88636", "amber": "#7FB069"},
    "slate":    {"navy": "#1F232B", "navy_alt": "#272C36", "cyan": "#3FA7A0", "cyan_dark": "#2E8A84", "amber": "#D4A537"},
    "plum":     {"navy": "#241426", "navy_alt": "#2E1A30", "cyan": "#C97A9A", "cyan_dark": "#A85F80", "amber": "#D9B36C"},
    "ink":      {"navy": "#1A1D24", "navy_alt": "#22262F", "cyan": "#D4A537", "cyan_dark": "#B8902A", "amber": "#5AA9C9"},
}


def resolve_cover_theme(config: dict[str, Any]) -> dict[str, str]:
    """cover_theme(명시 또는 책 제목 해시 자동)로 표지·도형 팔레트를 적용한다.

    cover_theme이 없거나 'auto'면 책 제목의 MD5 해시로 테마를 고른다.
    같은 제목은 같은 표지, 다른 제목은 다른 표지가 나온다(재현 가능).
    config.style.colors 의 명시 값은 테마 팔레트로 덮어쓴다.
    """
    import hashlib
    style = config.get("style", {})
    colors = dict(style.get("colors", {}))
    theme = config.get("editorial", {}).get("cover_theme") or style.get("cover_theme")
    if not theme or str(theme).lower() == "auto":
        names = list(COVER_THEMES.keys())
        title = str(config.get("book", {}).get("title", ""))
        h = int(hashlib.md5(title.encode("utf-8")).hexdigest(), 16)
        theme = names[h % len(names)]
    palette = COVER_THEMES.get(str(theme).lower())
    if palette:
        colors.update(palette)
    return colors


def create_css(config: dict[str, Any]) -> str:
    style = config["style"]
    editorial = config["editorial"]
    colors = resolve_cover_theme(config)
    margins = style.get("margins_mm", {})
    c = lambda key, default: colors.get(key, default)
    body_size = float(style.get("body_font_size_pt", 10.6))
    line_height = float(style.get("body_line_height", 1.82))
    book_short_css = str(config.get("book", {}).get("short_title", config.get("book", {}).get("title", "BOOK"))).replace("\\", "\\\\").replace('"', '\\"')
    body_font = style.get("body_font", "NanumMyeongjo, Noto Serif CJK KR, serif")
    heading_font = style.get("heading_font", "NanumSquare, Noto Sans CJK KR, sans-serif")
    mono_font = style.get("mono_font", "NanumGothicCoding, monospace")
    top = float(margins.get("top", 20))
    right = float(margins.get("right", 22))
    bottom = float(margins.get("bottom", 19))
    left = float(margins.get("left", 22))
    front_header = str(editorial.get("front_matter_header", "")).strip()
    front_header_css = front_header.replace("\\", "\\\\").replace('"', '\\"')
    front_header_content = f'"{front_header_css}"' if front_header_css else "none"
    extra_css = str(style.get("extra_css", "")).strip()

    base_css = f"""
@page {{
  size: {style.get('page_size', 'A4')};
  margin: {top}mm {right}mm {bottom}mm {left}mm;
  @top-left {{
    content: string(chapter-title);
    font-family: {heading_font}; font-size: 7.8pt; color: #677783;
    border-bottom: 0.45pt solid {c('line', '#D8E1E2')}; padding-bottom: 4mm;
  }}
  @top-right {{
    content: "{book_short_css}";
    font-family: {heading_font}; font-size: 7.5pt; color: #A0AAB1;
    letter-spacing: .6pt; text-align: right;
    border-bottom: 0.45pt solid {c('line', '#D8E1E2')}; padding-bottom: 4mm;
  }}
  @bottom-center {{
    content: counter(page);
    font-family: {heading_font}; font-size: 7.5pt; color: #98A5AD;
  }}
}}
@page cover {{ size: A4; margin: 0; background: {c('navy', '#081827')};
  @top-left {{ content: none; }} @top-right {{ content: none; }} @bottom-center {{ content: none; }}
}}
@page titlepage {{ size: A4; margin: 0; background: #fff;
  @top-left {{ content: none; }} @top-right {{ content: none; }}
}}
@page editorial {{ size: A4; margin: 28mm 23mm 22mm 23mm;
  @top-left {{ content: none; }} @top-right {{ content: none; }}
}}
@page front {{ size: A4; margin: 24mm 23mm 20mm 23mm;
  @top-left {{ content: {front_header_content}; font-family: {heading_font}; font-size: 7.5pt; letter-spacing: 1.6pt; color: #93A1AA; }} @top-right {{ content: none; }}
}}
@page tocpage {{ size: A4; margin: 18mm 23mm 18mm 23mm;
  @top-left {{ content: "CONTENTS"; font-family: {heading_font}; font-size: 7.5pt; letter-spacing: 1.6pt; color: #93A1AA; }}
  @top-right {{ content: none; }}
}}
@page chapteropen {{ size: A4; margin: 0; background: {c('navy', '#081827')};
  @top-left {{ content: none; }} @top-right {{ content: none; }} @bottom-center {{ content: none; }}
}}
@page visualpage {{ size: A4; margin: 16mm 18mm 16mm 18mm; background: #fff;
  @top-left {{ content: none; }} @top-right {{ content: none; }}
  @bottom-center {{ content: counter(page); font-family: {heading_font}; font-size: 7.5pt; color: #98A5AD; }}
}}

:root {{
  --navy: {c('navy', '#081827')}; --navy-alt: {c('navy_alt', '#102B38')};
  --cyan: {c('cyan', '#36C7D0')}; --cyan-dark: {c('cyan_dark', '#0F8790')};
  --amber: {c('amber', '#D39A2C')}; --ink: {c('ink', '#142131')};
  --text: {c('text', '#283541')}; --muted: {c('muted', '#7A8791')};
  --line: {c('line', '#D8E1E2')}; --wash: {c('wash', '#EFF5F4')};
}}
* {{ box-sizing: border-box; }}
html {{ font-variant-numeric: tabular-nums; }}
body {{ margin: 0; color: var(--text); font-family: {body_font}; font-size: {body_size}pt; line-height: {line_height}; word-break: keep-all; overflow-wrap: break-word; }}
a {{ color: inherit; text-decoration: none; }}
.running-chapter {{ string-set: chapter-title content(); height: 0; overflow: hidden; color: transparent; font-size: 0; }}

.cover {{ page: cover; break-after: page; height: 297mm; position: relative; padding: 29mm 25mm 20mm 25mm; color: white; overflow: hidden; font-family: {heading_font}; }}
.cover::before {{ content: ""; position: absolute; width: 210mm; height: 210mm; right: -94mm; bottom: -93mm; border: 1.2pt solid rgba(54,199,208,.55); border-radius: 50%; }}
.cover::after {{ content: ""; position: absolute; width: 76mm; height: 76mm; right: -8mm; top: 9mm; background: radial-gradient(circle, rgba(54,199,208,.14), rgba(54,199,208,0) 68%); }}
.cover .eyebrow {{ color: var(--cyan); font-size: 8pt; letter-spacing: 2.2pt; margin-bottom: 49mm; }}
.cover h1 {{ color: white; font-size: 31pt; line-height: 1.22; font-weight: 700; margin: 0 0 11mm 0; max-width: 116mm; bookmark-level: none; }}
.cover .subtitle {{ color: #BAC6CD; font-size: 14pt; margin-bottom: 12mm; }}
.accent-bar {{ width: 29mm; height: 1.6mm; background: linear-gradient(90deg, var(--cyan), #75D5C0 42%, var(--amber)); }}
.cover .author-block {{ position: absolute; left: 25mm; bottom: 31mm; }}
.cover .author {{ font-size: 10.5pt; font-weight: 700; margin-bottom: 6mm; }}
.cover .edition {{ color: #8EA0AA; font-size: 7.8pt; }}
.cover .watermark {{ position: absolute; top: 13mm; right: 16mm; font-size: 49pt; font-weight: 700; color: rgba(255,255,255,.055); }}
.network {{ position: absolute; left: 127mm; top: 69mm; width: 62mm; height: 78mm; }}
.network .line {{ position: absolute; height: .55mm; background: rgba(54,199,208,.65); transform-origin: left center; }}
.network .l1 {{ left: 11mm; top: 32mm; width: 49mm; transform: rotate(-43deg); }}
.network .l2 {{ left: 21mm; top: 30mm; width: 50mm; transform: rotate(47deg); }}
.network .node {{ position: absolute; width: 4mm; height: 4mm; border-radius: 50%; background: var(--cyan); }}
.network .n1 {{ left: 9mm; top: 30mm; }} .network .n2 {{ right: 0; top: 0; width: 5mm; height: 5mm; }}
.network .n3 {{ right: -1mm; bottom: 0; background: var(--amber); }}
.process {{ position: absolute; left: 25mm; bottom: 17mm; display: flex; align-items: center; gap: 3.5mm; }}
.process .chip {{ width: 12mm; height: 12mm; border: .6pt solid rgba(54,199,208,.75); border-radius: 3mm; color: #93A7B1; font-size: 6.7pt; display: flex; align-items: center; justify-content: center; text-align: center; padding: 1mm; }}
.process .arrow {{ color: var(--cyan); font-size: 7pt; }}

.title-page {{ page: titlepage; break-after: page; height: 297mm; padding: 76mm 23mm 25mm 23mm; position: relative; }}
.title-page .eyebrow {{ font-family: {heading_font}; color: var(--cyan-dark); font-size: 7.4pt; letter-spacing: 2pt; margin-bottom: 9mm; }}
.title-page h1 {{ font-family: {heading_font}; color: var(--ink); font-size: 27pt; line-height: 1.28; margin: 0 0 13mm; bookmark-level: none; }}
.title-page .subtitle {{ font-family: {heading_font}; color: #75828C; font-size: 12pt; margin-bottom: 26mm; }}
.title-page .quote {{ border-left: 2.2pt solid var(--cyan-dark); padding-left: 9mm; font-size: 13pt; line-height: 1.75; color: #243441; max-width: 145mm; }}
.title-page .author {{ position: absolute; left: 23mm; top: 202mm; font-family: {heading_font}; font-size: 10pt; font-weight: 700; }}
.title-page .edition {{ position: absolute; left: 23mm; top: 216mm; font-family: {heading_font}; font-size: 7.8pt; color: #8D999F; }}

.editorial-note {{ page: editorial; break-after: page; position: relative; min-height: 245mm; }}
.editorial-note h1 {{ font-family: {heading_font}; font-size: 18pt; color: var(--ink); margin: 0 0 9mm; bookmark-level: none; }}
.editorial-note p {{ color: #53616C; margin: 0 0 5mm; }}
.editorial-note .mark {{ position: absolute; right: 0; top: -8mm; font-family: {heading_font}; font-size: 43pt; color: #EDF1F1; font-weight: 700; }}
.notice-box {{ margin-top: 10mm; border-top: 2pt solid var(--cyan-dark); background: var(--wash); padding: 8mm 9mm 7mm; }}
.notice-box p {{ color: #34434D; margin-bottom: 4mm; }}
.notice-box .date {{ color: #9AA6AC; font-family: {heading_font}; font-size: 7.4pt; margin: 0; }}

.front-matter {{ page: front; break-after: page; }}
.front-matter > .source-document > h2:first-child {{ margin-top: 4mm; }}
.front-matter h2 {{ font-family: {heading_font}; font-size: 22pt; line-height: 1.3; color: var(--ink); margin: 12mm 0 7mm; padding-top: 3mm; border-top: .6pt solid var(--line); bookmark-level: 1; }}
.front-matter h2:first-of-type {{ border-top: none; }}
.front-matter h3 {{ font-family: {heading_font}; color: var(--ink); font-size: 14pt; }}
.front-matter p {{ margin: 0 0 5mm; }}
.front-matter ul, .front-matter ol {{ margin: 3mm 0 5mm 7mm; }}

.toc {{ page: tocpage; break-after: page; }}
.toc-head {{ display: flex; align-items: flex-end; justify-content: space-between; gap: 12mm; margin: 5mm 0 11mm; padding-bottom: 7mm; border-bottom: 1.2pt solid var(--ink); }}
.toc h1 {{ font-family: {heading_font}; color: var(--ink); font-size: 27pt; margin: 0; bookmark-level: none; }}
.toc-lead {{ max-width: 74mm; font-family: {heading_font}; font-size: 8pt; line-height: 1.55; color: #76848D; text-align: right; }}
.toc-grid {{ display: block; }}
.toc-item {{ display: grid; grid-template-columns: 17mm 1fr; column-gap: 3mm; break-inside: avoid; margin: 0 0 5.2mm; padding: 3.8mm 0 0; border-top: .65pt solid var(--line); }}
.toc-num {{ color: var(--cyan-dark); font-family: {heading_font}; font-size: 13.5pt; line-height: 1.1; font-weight: 700; }}
.toc-block {{ min-width: 0; }}
.toc-chapter {{ display: block; font-family: {heading_font}; font-size: 10.8pt; line-height: 1.45; font-weight: 700; color: var(--ink); }}
.toc-chapter::after {{ content: leader(".") target-counter(attr(href), page); color: #8B979E; font-weight: 400; font-size: 8pt; white-space: nowrap; }}
.toc-sections {{ margin: 2.2mm 0 0; padding: 0; list-style: none; }}
.toc-sections li {{ margin: 0 0 1.25mm; font-size: 8.25pt; color: #74818A; line-height: 1.48; }}
.toc-sections a {{ display: block; }}
.toc-sections a::after {{ content: leader(".") target-counter(attr(href), page); color: #9AA5AB; font-size: 7.4pt; white-space: nowrap; }}

.chapter-opener {{ page: chapteropen; break-before: page; break-after: page; height: 297mm; padding: 30mm 25mm 25mm; color: white; position: relative; font-family: {heading_font}; overflow: hidden; }}
.chapter-opener::after {{ content: ""; position: absolute; width: 82mm; height: 82mm; right: -8mm; top: 4mm; background: radial-gradient(circle, rgba(54,199,208,.14), rgba(54,199,208,0) 68%); }}
.chapter-opener .eyebrow {{ color: var(--cyan); font-size: 7.7pt; letter-spacing: 2.2pt; margin-bottom: 13mm; }}
.chapter-opener .number {{ font-size: 46pt; color: rgba(255,255,255,.16); line-height: 1; font-weight: 700; margin-bottom: 10mm; }}
.chapter-opener h1 {{ font-size: 27pt; line-height: 1.3; color: white; margin: 0 0 12mm; bookmark-level: 1; }}
.chapter-opener .section-label {{ color: #9BB0BA; font-size: 7.4pt; margin: 20mm 0 6mm; }}
.chapter-opener .sections {{ display: grid; grid-template-columns: 1fr; row-gap: 1.65mm; max-width: 148mm; }}
.chapter-opener .section-item {{ font-size: 7.7pt; line-height: 1.35; color: #B8C4CA; display: grid; grid-template-columns: 10mm 1fr; gap: 2mm; }}
.chapter-opener .section-no {{ color: var(--cyan); }}
.chapter-opener .bottom-line {{ position: absolute; left: 25mm; right: 25mm; bottom: 22mm; height: .5mm; background: linear-gradient(90deg, var(--cyan), rgba(54,199,208,.15)); }}

.chapter-visual {{ page: visualpage; break-after: page; min-height: 263mm; position: relative; font-family: {heading_font}; color: var(--ink); }}
.chapter-visual::before {{ content: ""; position: absolute; left: -18mm; right: -18mm; top: -16mm; height: 8mm; background: linear-gradient(90deg, var(--navy), var(--navy-alt) 70%, var(--cyan-dark)); }}
.visual-head {{ display: grid; grid-template-columns: 1fr 42mm; column-gap: 10mm; align-items: start; padding-top: 4mm; }}
.visual-kicker {{ color: var(--cyan-dark); font-size: 7.3pt; letter-spacing: 1.8pt; font-weight: 700; margin-bottom: 4mm; }}
.visual-title {{ margin: 0; font-size: 22pt; line-height: 1.28; color: var(--ink); bookmark-level: none; }}
.visual-thesis {{ margin: 5mm 0 0; font-family: {body_font}; font-size: 10.2pt; line-height: 1.72; color: #42525E; max-width: 125mm; }}
.visual-badge {{ border: .8pt solid var(--line); background: #F7FAFA; padding: 5mm 4mm; text-align: center; border-radius: 3mm; color: #6D7B84; font-size: 7.2pt; line-height: 1.5; }}
.visual-badge strong {{ display: block; color: var(--cyan-dark); font-size: 16pt; line-height: 1; margin-bottom: 2.2mm; }}
.diagram-shell {{ margin-top: 8mm; border: .7pt solid #D4DFE1; border-radius: 4mm; background: linear-gradient(180deg, #F7FBFB, #FFFFFF); padding: 7mm; min-height: 88mm; break-inside: avoid; position: relative; overflow: hidden; }}
.diagram-shell::after {{ content: ""; position: absolute; width: 50mm; height: 50mm; border: .7pt solid rgba(54,199,208,.16); border-radius: 50%; right: -24mm; bottom: -27mm; }}
.diagram-label {{ font-size: 7.2pt; letter-spacing: 1.4pt; color: #8A979F; margin-bottom: 5mm; }}
.process-diagram {{ display: flex; gap: 3mm; align-items: stretch; }}
.process-step {{ flex: 1 1 0; min-width: 0; padding: 5mm 3mm 4mm; border: .65pt solid #D3DFE0; background: #fff; border-radius: 3mm; text-align: center; position: relative; }}
.process-step:not(:last-child)::after {{ content: "→"; position: absolute; right: -4.2mm; top: 50%; transform: translateY(-50%); color: var(--cyan-dark); font-size: 9pt; font-weight: 700; z-index: 2; }}
.process-no {{ display: inline-flex; align-items: center; justify-content: center; width: 8mm; height: 8mm; border-radius: 50%; background: var(--navy); color: #fff; font-size: 6.8pt; margin-bottom: 3mm; }}
.process-title {{ font-size: 8.2pt; font-weight: 700; line-height: 1.35; color: var(--ink); }}
.process-text {{ margin-top: 2mm; font-family: {body_font}; font-size: 7pt; line-height: 1.45; color: #687680; }}
.bridge-row {{ display: grid; grid-template-columns: 1fr 42mm 1fr; gap: 5mm; align-items: center; min-height: 48mm; }}
.bridge-node {{ padding: 6mm; border-radius: 3mm; border: .7pt solid #D0DCDE; background: #fff; min-height: 36mm; }}
.bridge-node.left {{ border-top: 2pt solid var(--amber); }}
.bridge-node.right {{ border-top: 2pt solid var(--cyan-dark); }}
.bridge-node .node-label {{ font-size: 7pt; letter-spacing: 1.1pt; color: #8A969D; margin-bottom: 2mm; }}
.bridge-node .node-title {{ font-size: 11pt; line-height: 1.35; font-weight: 700; }}
.bridge-node .node-text {{ margin-top: 2mm; font-family: {body_font}; font-size: 7.6pt; line-height: 1.45; color: #66747D; }}
.bridge-core {{ width: 38mm; height: 38mm; margin: auto; border-radius: 50%; border: 1.3pt solid var(--cyan); background: var(--navy); color: #fff; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; position: relative; }}
.bridge-core::before, .bridge-core::after {{ content: ""; position: absolute; top: 50%; width: 12mm; border-top: 1pt solid var(--cyan-dark); }}
.bridge-core::before {{ right: 100%; }}
.bridge-core::after {{ left: 100%; }}
.bridge-core .core-title {{ font-size: 11pt; font-weight: 700; }}
.bridge-core .core-text {{ margin-top: 1.5mm; font-size: 6.8pt; line-height: 1.35; color: #B9C8CF; padding: 0 3mm; }}
.bridge-bands {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 2.4mm; margin-top: 5mm; }}
.bridge-band {{ padding: 3.4mm 2mm; background: #EAF3F3; border-bottom: 1.3pt solid var(--cyan-dark); text-align: center; font-size: 7pt; line-height: 1.35; color: #3D4C56; }}
.quad-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; }}
.quad-card {{ padding: 5mm; min-height: 31mm; background: #fff; border: .7pt solid #D4DFE1; border-radius: 3mm; }}
.quad-card:nth-child(1) {{ border-top: 2pt solid var(--cyan-dark); }}
.quad-card:nth-child(2) {{ border-top: 2pt solid var(--amber); }}
.quad-card:nth-child(3) {{ border-top: 2pt solid #6A9EA4; }}
.quad-card:nth-child(4) {{ border-top: 2pt solid var(--navy-alt); }}
.quad-title {{ font-size: 9.2pt; font-weight: 700; margin-bottom: 2mm; }}
.quad-text {{ font-family: {body_font}; font-size: 7.4pt; line-height: 1.45; color: #65737D; }}
.quad-center {{ margin: 4mm auto 0; width: 92mm; padding: 3.5mm 6mm; border-radius: 10mm; background: var(--navy); color: #fff; text-align: center; font-size: 8.3pt; font-weight: 700; }}
.ladder {{ display: flex; align-items: flex-end; gap: 5mm; min-height: 70mm; padding: 2mm 7mm 0; }}
.ladder-step {{ flex: 1; border-radius: 3mm 3mm 0 0; border: .7pt solid #CDDADB; border-bottom: 0; background: linear-gradient(180deg, #FFFFFF, #EAF3F3); padding: 5mm 4mm; text-align: center; position: relative; }}
.ladder-step:nth-child(1) {{ min-height: 34mm; }}
.ladder-step:nth-child(2) {{ min-height: 49mm; }}
.ladder-step:nth-child(3) {{ min-height: 64mm; background: linear-gradient(180deg, #EFF9F8, #DCEEEF); border-color: #AFCBCD; }}
.ladder-step::before {{ content: attr(data-level); display: inline-flex; align-items: center; justify-content: center; width: 8mm; height: 8mm; border-radius: 50%; background: var(--navy); color: #fff; font-size: 6.6pt; margin-bottom: 3mm; }}
.ladder-title {{ font-size: 9pt; font-weight: 700; line-height: 1.35; }}
.ladder-text {{ margin-top: 2mm; font-family: {body_font}; font-size: 7.2pt; line-height: 1.45; color: #64727C; }}
.ladder-outcome {{ margin-top: 0; padding: 3.5mm; background: var(--navy); color: #fff; text-align: center; font-size: 8.5pt; font-weight: 700; }}
.principle-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 4mm; }}
.principle-card {{ min-height: 34mm; padding: 4.5mm; border: .7pt solid #D2DEDF; border-radius: 4mm; background: #fff; position: relative; }}
.principle-no {{ position: absolute; right: 3mm; top: 2.5mm; font-size: 18pt; line-height: 1; color: #E2ECEC; font-weight: 700; }}
.principle-title {{ position: relative; font-size: 8.8pt; font-weight: 700; color: var(--ink); max-width: 36mm; }}
.principle-text {{ position: relative; margin-top: 2mm; font-family: {body_font}; font-size: 7.1pt; line-height: 1.42; color: #66747D; }}
.dashboard-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; }}
.dashboard-card {{ padding: 5mm; min-height: 35mm; border-radius: 3mm; background: #fff; border: .7pt solid #D2DEDF; }}
.dashboard-card .dash-kicker {{ color: var(--cyan-dark); font-size: 6.8pt; letter-spacing: 1.1pt; }}
.dashboard-card .dash-title {{ margin: 1.5mm 0 2mm; font-size: 9.4pt; font-weight: 700; }}
.dashboard-card .dash-text {{ font-family: {body_font}; font-size: 7.2pt; line-height: 1.45; color: #63717B; }}
.network-hub {{ padding: 4mm 6mm; margin: 0 auto 5mm; width: 92mm; border-radius: 12mm; background: var(--navy); color: #fff; text-align: center; font-size: 9pt; font-weight: 700; }}
.network-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 4mm; }}
.network-card {{ min-height: 30mm; padding: 4mm; border: .7pt solid #D2DEDF; border-radius: 3mm; background: #fff; text-align: center; }}
.network-card .network-title {{ font-size: 8.3pt; font-weight: 700; color: var(--ink); }}
.network-card .network-text {{ margin-top: 2mm; font-family: {body_font}; font-size: 7pt; line-height: 1.4; color: #687680; }}
.visual-matrix {{ width: 100%; border-collapse: collapse; table-layout: fixed; margin: 0; font-size: 7.2pt; line-height: 1.4; }}
.visual-matrix th {{ background: var(--navy); color: #fff; border: 0; border-right: .4pt solid #3C5662; padding: 3mm; font-size: 7.2pt; }}
.visual-matrix td {{ background: #fff; border-bottom: .5pt solid #D7E1E2; border-right: .4pt solid #E0E7E8; padding: 2.7mm; vertical-align: top; }}
.visual-matrix tr:nth-child(even) td {{ background: #F5F9F9; }}
.visual-table-wrap {{ margin-top: 7mm; break-inside: avoid; }}
.visual-table-title {{ font-size: 8pt; letter-spacing: 1.1pt; color: #7C8991; margin-bottom: 3mm; }}
.visual-check-table {{ width: 100%; border-collapse: collapse; table-layout: fixed; margin: 0; font-family: {body_font}; font-size: 7.5pt; line-height: 1.45; }}
.visual-check-table th {{ background: #EAF2F2; color: var(--ink); border-top: 1.2pt solid var(--cyan-dark); border-bottom: .7pt solid #BFCFD0; padding: 2.7mm 3mm; }}
.visual-check-table td {{ padding: 2.6mm 3mm; border-bottom: .5pt solid #D9E2E3; vertical-align: top; }}
.visual-note {{ margin-top: 4mm; font-family: {body_font}; font-size: 6.7pt; color: #8A969D; line-height: 1.45; }}

.chapter-body {{ break-after: page; }}
.chapter-body h2 {{ font-family: {heading_font}; font-size: 19.5pt; line-height: 1.36; color: var(--ink); margin: 10mm 0 5mm; padding-left: 5mm; border-left: 2.3pt solid var(--cyan-dark); break-after: avoid; bookmark-level: 2; }}
.chapter-body h3 {{ font-family: {heading_font}; font-size: 13.8pt; line-height: 1.45; color: var(--ink); margin: 8mm 0 3.5mm; break-after: avoid; bookmark-level: 3; }}
.chapter-body h4 {{ font-family: {heading_font}; font-size: 11.5pt; color: var(--ink); margin: 6mm 0 2.5mm; break-after: avoid; bookmark-level: 4; }}
p {{ margin: 0 0 4.1mm; orphans: 3; widows: 3; }}
strong {{ color: #152534; }}
ul, ol {{ margin: 2mm 0 5mm 7mm; padding-left: 5mm; }}
li {{ margin: 0 0 1.7mm; orphans: 2; widows: 2; }}
li::marker {{ color: var(--cyan-dark); }}
blockquote {{ margin: 5mm 0 8mm; padding: 6mm 9mm 6mm 12mm; background: var(--wash); border-left: 2.4pt solid var(--cyan-dark); color: #2C3C47; position: relative; break-inside: avoid; }}
blockquote::before {{ content: "“"; position: absolute; left: 5mm; top: -1mm; font-family: {heading_font}; font-size: 22pt; color: rgba(15,135,144,.28); }}
blockquote p:last-child {{ margin-bottom: 0; }}
hr {{ border: 0; border-top: .55pt solid var(--line); margin: 9mm 0; }}
code {{ font-family: {mono_font}; font-size: .9em; background: #F2F5F5; padding: .2mm 1mm; border-radius: 1mm; }}
pre {{ font-family: {mono_font}; font-size: 8.3pt; line-height: 1.55; background: #101D28; color: #E8F0F3; padding: 5mm; border-radius: 2mm; white-space: pre-wrap; overflow-wrap: anywhere; break-inside: avoid; }}
pre code {{ background: transparent; color: inherit; padding: 0; }}
table {{ width: 100%; border-collapse: collapse; table-layout: fixed; margin: 5mm 0 7mm; font-size: 8.5pt; line-height: 1.55; break-inside: auto; }}
thead {{ display: table-header-group; }}
tr {{ break-inside: avoid; }}
th {{ font-family: {heading_font}; color: var(--ink); background: #EAF2F2; border-top: 1.2pt solid var(--cyan-dark); border-bottom: .7pt solid #BBCACA; padding: 2.3mm 2.5mm; text-align: left; overflow-wrap: anywhere; }}
td {{ border-bottom: .45pt solid #D9E1E2; padding: 2.1mm 2.5mm; vertical-align: top; overflow-wrap: anywhere; }}
img {{ max-width: 100%; height: auto; display: block; margin: 6mm auto; break-inside: avoid; }}
.footnotes {{ font-size: 8.3pt; color: #66747D; border-top: .6pt solid var(--line); margin-top: 9mm; padding-top: 4mm; }}
.task-list-item {{ list-style: none; }}

@media print {{
  a[href^="http"]::after {{ content: none; }}
}}
"""
    return base_css + ("\n" + extra_css + "\n" if extra_css else "")


def build_cover(config: dict[str, Any], content_root: Path | None = None) -> str:
    book = config["book"]
    editorial = config["editorial"]
    cover_image = str(editorial.get("cover_image", "") or "").strip()
    if cover_image:
        candidates: list[Path] = [Path(cover_image)]
        if content_root is not None:
            candidates.append(content_root / cover_image)
        candidates.append(Path.cwd() / cover_image)
        for candidate in candidates:
            try:
                resolved = candidate.expanduser().resolve()
            except Exception:
                continue
            if resolved.is_file():
                alt = str(book.get("title", "") or "표지")
                return (
                    f'<section class="cover cover-image">'
                    f'<img src="{html.escape(str(resolved))}" alt="{html.escape(alt)}"/>'
                    f"</section>"
                )
    author = str(book.get("author", "")).strip()
    author_html = f'<div class="author">{html.escape(author)} 지음</div>' if author else ""
    chips = editorial.get("cover_process_chips") or []
    chip_html: list[str] = []
    for idx, chip in enumerate(chips):
        if idx:
            chip_html.append('<span class="arrow">→</span>')
        chip_html.append(f'<span class="chip">{html.escape(str(chip))}</span>')
    watermark = str(editorial.get("cover_watermark", "")).strip()
    if not watermark:
        watermark = str(book.get("short_title", "BOOK")).split()[0][:5]
    return f"""
<section class="cover">
  <div class="eyebrow">{html.escape(str(editorial.get('cover_eyebrow', book.get('short_title', 'EDITORIAL BOOK'))))}</div>
  <div class="watermark">{html.escape(watermark)}</div>
  <h1>{split_title_for_cover(str(book.get('title', '제목 없음')))}</h1>
  <div class="subtitle">{html.escape(str(book.get('subtitle', '')))}</div>
  <div class="accent-bar"></div>
  <div class="network"><span class="line l1"></span><span class="line l2"></span><span class="node n1"></span><span class="node n2"></span><span class="node n3"></span></div>
  <div class="author-block">{author_html}<div class="edition">{html.escape(str(book.get('edition_label', '')))}</div></div>
  <div class="process">{''.join(chip_html)}</div>
</section>
"""


def build_title_page(config: dict[str, Any], quote: str) -> str:
    book = config["book"]
    editorial = config["editorial"]
    author = str(book.get("author", "")).strip()
    author_html = f'<div class="author">{html.escape(author)} 지음</div>' if author else ""
    q = f'<div class="quote">{html.escape(quote)}</div>' if quote else ""
    return f"""
<section class="title-page">
  <div class="eyebrow">{html.escape(str(book.get('short_title', 'EDITORIAL BOOK')))}</div>
  <h1>{html.escape(str(book.get('title', '제목 없음')))}</h1>
  <div class="subtitle">{html.escape(str(book.get('subtitle', '')))}</div>
  {q}
  {author_html}
  <div class="edition">{html.escape(str(editorial.get('title_page_edition_label') or book.get('edition_label', '')))}</div>
</section>
"""


def build_editorial_note(config: dict[str, Any], build_date: str) -> str:
    book = config["book"]
    editorial = config["editorial"]
    paragraphs = editorial.get("editorial_note_paragraphs") or []
    body = "".join(f"<p>{html.escape(str(p))}</p>" for p in paragraphs)
    copyright_notice = html.escape(str(book.get("copyright_notice", "")))
    footer_paragraphs = editorial.get("editorial_note_footer_paragraphs") or []
    footer = "".join(f"<p>{html.escape(str(p))}</p>" for p in footer_paragraphs)
    return f"""
<section class="editorial-note">
  <div class="mark">PDF</div>
  <h1>{html.escape(str(editorial.get('editorial_note_title', 'PDF 편집본 안내')))}</h1>
  {body}
  <div class="notice-box">
    {f'<p>{copyright_notice}</p>' if copyright_notice else ''}
    {footer}
    <p class="date">PDF 편집일: {html.escape(build_date)}</p>
  </div>
</section>
"""


def build_toc(chapter_docs: list[SourceDoc], config: dict[str, Any]) -> str:
    editorial = config.get("editorial", {})
    items: list[str] = []
    for index, doc in enumerate(chapter_docs, start=1):
        cls = classify_chapter(doc.title, index)
        num = cls["number"]
        section_links: list[str] = []
        soup = BeautifulSoup(doc.html_body, "html.parser")
        h2s = soup.find_all("h2")
        for h2 in h2s:
            sec_title = h2.get_text(" ", strip=True)
            section_links.append(f'<li><a href="#{html.escape(h2.get("id", doc.anchor))}">{html.escape(sec_title)}</a></li>')
        items.append(
            f'<div class="toc-item"><div class="toc-num">{html.escape(num)}</div><div class="toc-block">'
            f'<a class="toc-chapter" href="#{html.escape(doc.anchor)}">{html.escape(doc.title)}</a>'
            + (f'<ul class="toc-sections">{"".join(section_links)}</ul>' if section_links else "")
            + "</div></div>"
        )
    lead = str(editorial.get("toc_lead", "장과 절을 한 줄 흐름으로 읽을 수 있도록 1단 목차로 구성했습니다.")).strip()
    return (
        '<section class="toc"><div class="toc-head"><h1>목차</h1>'
        f'<div class="toc-lead">{html.escape(lead)}</div></div>'
        f'<div class="toc-grid">{"".join(items)}</div></section>'
    )

def visual_spec_for(doc: SourceDoc, index: int, config: dict[str, Any]) -> dict[str, Any] | None:
    visual_cfg = config.get("visuals", {}) or {}
    if not visual_cfg.get("enabled", False):
        return None
    specs = visual_cfg.get("chapters", {}) or {}
    spec = specs.get(doc.title) or specs.get(str(index))
    if spec:
        return dict(spec)
    if not visual_cfg.get("auto_from_headings", False):
        return None
    titles = [title for level, title in doc.headings if level == 2][:6]
    if not titles:
        return None
    return {
        "kicker": visual_cfg.get("default_kicker", "CHAPTER MAP"),
        "title": visual_cfg.get("default_title", "이 장의 흐름"),
        "thesis": "장 전체의 절 구성을 빠르게 탐색하기 위한 편집 요약입니다.",
        "diagram": {
            "layout": "process",
            "label": "SECTION FLOW",
            "steps": [{"title": title, "text": ""} for title in titles],
        },
    }


def html_text(value: Any) -> str:
    return html.escape(str(value or ""))


def build_process_diagram(diagram: dict[str, Any]) -> str:
    steps = diagram.get("steps") or []
    cards: list[str] = []
    for idx, step in enumerate(steps, start=1):
        cards.append(
            '<div class="process-step">'
            f'<div class="process-no">{idx:02d}</div>'
            f'<div class="process-title">{html_text(step.get("title"))}</div>'
            + (f'<div class="process-text">{html_text(step.get("text"))}</div>' if step.get("text") else "")
            + '</div>'
        )
    return f'<div class="process-diagram">{"".join(cards)}</div>'


def build_bridge_diagram(diagram: dict[str, Any]) -> str:
    left = diagram.get("left") or {}
    center = diagram.get("center") or {}
    right = diagram.get("right") or {}
    bands = diagram.get("bands") or []
    band_html = "".join(f'<div class="bridge-band">{html_text(item)}</div>' for item in bands)
    return f"""
<div class="bridge-row">
  <div class="bridge-node left"><div class="node-label">{html_text(left.get('label'))}</div><div class="node-title">{html_text(left.get('title'))}</div><div class="node-text">{html_text(left.get('text'))}</div></div>
  <div class="bridge-core"><div class="core-title">{html_text(center.get('title'))}</div><div class="core-text">{html_text(center.get('text'))}</div></div>
  <div class="bridge-node right"><div class="node-label">{html_text(right.get('label'))}</div><div class="node-title">{html_text(right.get('title'))}</div><div class="node-text">{html_text(right.get('text'))}</div></div>
</div>
{f'<div class="bridge-bands">{band_html}</div>' if band_html else ''}
"""


def build_quadrant_diagram(diagram: dict[str, Any]) -> str:
    cards = diagram.get("cards") or []
    card_html = "".join(
        f'<div class="quad-card"><div class="quad-title">{html_text(card.get("title"))}</div><div class="quad-text">{html_text(card.get("text"))}</div></div>'
        for card in cards
    )
    center = diagram.get("center")
    return f'<div class="quad-grid">{card_html}</div>' + (f'<div class="quad-center">{html_text(center)}</div>' if center else "")


def build_ladder_diagram(diagram: dict[str, Any]) -> str:
    steps = diagram.get("steps") or []
    cards = "".join(
        f'<div class="ladder-step" data-level="{idx}"><div class="ladder-title">{html_text(step.get("title"))}</div><div class="ladder-text">{html_text(step.get("text"))}</div></div>'
        for idx, step in enumerate(steps, start=1)
    )
    outcome = diagram.get("outcome")
    return f'<div class="ladder">{cards}</div>' + (f'<div class="ladder-outcome">{html_text(outcome)}</div>' if outcome else "")


def build_principle_diagram(diagram: dict[str, Any]) -> str:
    cards = diagram.get("cards") or []
    return '<div class="principle-grid">' + "".join(
        f'<div class="principle-card"><div class="principle-no">{idx:02d}</div><div class="principle-title">{html_text(card.get("title"))}</div><div class="principle-text">{html_text(card.get("text"))}</div></div>'
        for idx, card in enumerate(cards, start=1)
    ) + '</div>'


def build_dashboard_diagram(diagram: dict[str, Any]) -> str:
    cards = diagram.get("cards") or []
    return '<div class="dashboard-grid">' + "".join(
        f'<div class="dashboard-card"><div class="dash-kicker">{html_text(card.get("kicker"))}</div><div class="dash-title">{html_text(card.get("title"))}</div><div class="dash-text">{html_text(card.get("text"))}</div></div>'
        for card in cards
    ) + '</div>'


def build_network_diagram(diagram: dict[str, Any]) -> str:
    cards = diagram.get("cards") or []
    hub = diagram.get("hub") or ""
    return f'<div class="network-hub">{html_text(hub)}</div><div class="network-grid">' + "".join(
        f'<div class="network-card"><div class="network-title">{html_text(card.get("title"))}</div><div class="network-text">{html_text(card.get("text"))}</div></div>'
        for card in cards
    ) + '</div>'


def build_matrix_diagram(diagram: dict[str, Any]) -> str:
    headers = diagram.get("headers") or []
    rows = diagram.get("rows") or []
    head = "".join(f'<th>{html_text(value)}</th>' for value in headers)
    body = "".join('<tr>' + "".join(f'<td>{html_text(value)}</td>' for value in row) + '</tr>' for row in rows)
    return f'<table class="visual-matrix"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'


def build_visual_diagram(diagram: dict[str, Any]) -> str:
    layout = str(diagram.get("layout", "process")).casefold()
    if layout == "bridge":
        return build_bridge_diagram(diagram)
    if layout in {"quadrant", "quadrants"}:
        return build_quadrant_diagram(diagram)
    if layout == "ladder":
        return build_ladder_diagram(diagram)
    if layout in {"principles", "principle"}:
        return build_principle_diagram(diagram)
    if layout == "dashboard":
        return build_dashboard_diagram(diagram)
    if layout == "network":
        return build_network_diagram(diagram)
    if layout == "matrix":
        return build_matrix_diagram(diagram)
    return build_process_diagram(diagram)


def build_check_table(table: dict[str, Any]) -> str:
    headers = table.get("headers") or []
    rows = table.get("rows") or []
    if not headers or not rows:
        return ""
    head = "".join(f'<th>{html_text(value)}</th>' for value in headers)
    body = "".join('<tr>' + "".join(f'<td>{html_text(value)}</td>' for value in row) + '</tr>' for row in rows)
    title = table.get("title") or "판단 프레임"
    return f'<div class="visual-table-wrap"><div class="visual-table-title">{html_text(title)}</div><table class="visual-check-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def build_visual_summary(doc: SourceDoc, index: int, config: dict[str, Any]) -> str:
    spec = visual_spec_for(doc, index, config)
    if not spec:
        return ""
    diagram = spec.get("diagram") or {}
    table = spec.get("table") or {}
    cls = classify_chapter(doc.title, index)
    kicker = spec.get("kicker") or "VISUAL GUIDE"
    title = spec.get("title") or doc.title
    thesis = spec.get("thesis") or ""
    badge_value = spec.get("badge_value") or cls.get("number") or f"{index:02d}"
    badge_label = spec.get("badge_label") or "CHAPTER MAP"
    label = diagram.get("label") or "CONCEPT MAP"
    note = spec.get("note") or config.get("visuals", {}).get(
        "default_note",
        "편집 요약: 본문의 장·절 구조와 핵심 문장을 탐색하기 쉽게 재배열한 도식이며, 원문을 대체하지 않습니다.",
    )
    return f"""
<section class="chapter-visual chapter-{index:02d} kind-{html.escape(cls['kind'])}">
  <div class="visual-head">
    <div>
      <div class="visual-kicker">{html_text(kicker)}</div>
      <h2 class="visual-title">{html_text(title)}</h2>
      {f'<p class="visual-thesis">{html_text(thesis)}</p>' if thesis else ''}
    </div>
    <div class="visual-badge"><strong>{html_text(badge_value)}</strong>{html_text(badge_label)}</div>
  </div>
  <div class="diagram-shell"><div class="diagram-label">{html_text(label)}</div>{build_visual_diagram(diagram)}</div>
  {build_check_table(table)}
  <div class="visual-note">{html_text(note)}</div>
</section>
"""


def build_chapter(doc: SourceDoc, index: int, config: dict[str, Any]) -> str:
    editorial = config["editorial"]
    cls = classify_chapter(doc.title, index)
    kind = cls["kind"]
    clean_title = cls.get("clean_title") or doc.title

    if kind == "frontmatter":
        fm_header = str(editorial.get("front_matter_header", "")).strip()
        eyebrow_html = f'<div class="eyebrow fm-eyebrow">{html.escape(fm_header)}</div>' if fm_header else ""
        return f"""
<section class="front-matter chapter-{index:02d} kind-frontmatter" id="{html.escape(doc.anchor)}">
  <div class="running-chapter"></div>
  {eyebrow_html}
  <h1>{html.escape(clean_title)}</h1>
  <div class="accent-bar"></div>
  {doc.html_body}
</section>
"""

    if kind == "appendix":
        eyebrow = editorial.get("appendix_eyebrow", cls["eyebrow"])
    elif kind == "afterword":
        eyebrow = editorial.get("afterword_eyebrow", cls["eyebrow"])
    elif kind == "part":
        eyebrow = editorial.get("part_eyebrow", cls["eyebrow"])
    else:
        eyebrow = editorial.get("chapter_eyebrow", cls["eyebrow"])

    soup = BeautifulSoup(doc.html_body, "html.parser")
    h2s = soup.find_all("h2")
    section_items: list[str] = []
    for sec_idx, h2 in enumerate(h2s, start=1):
        section_items.append(
            f'<div class="section-item"><span class="section-no">{sec_idx:02d}</span><span>{html.escape(h2.get_text(" ", strip=True))}</span></div>'
        )
    number_html = f'<div class="number">{html.escape(str(cls["number"]))}</div>' if cls.get("number") else ""
    sections_html = ""
    if section_items and kind == "chapter":
        sections_html = '<div class="section-label">이 장의 구성</div><div class="sections">' + ''.join(section_items) + '</div>'
    opener = f"""
<section class="chapter-opener chapter-{index:02d} kind-{html.escape(kind)}" id="{html.escape(doc.anchor)}">
  <div class="eyebrow">{html.escape(str(eyebrow))}</div>
  {number_html}
  <h1>{html.escape(clean_title)}</h1>
  <div class="accent-bar"></div>
  {sections_html}
  <div class="bottom-line"></div>
</section>
"""
    visual = build_visual_summary(doc, index, config) if kind == "chapter" else ""
    body = f"""
<section class="chapter-body chapter-{index:02d} kind-{html.escape(kind)}">
  <div class="running-chapter">{html.escape(doc.title)}</div>
  {doc.html_body}
</section>
"""
    return opener + visual + body


def reference_entries(paths: list[Path]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for path in paths:
        resolved = path.resolve()
        if not resolved.exists() or not resolved.is_file():
            raise BuildError(f"Reference file not found: {path}")
        entries.append(
            {
                "path": str(resolved),
                "name": resolved.name,
                "size_bytes": resolved.stat().st_size,
                "sha256": sha256_file(resolved),
                "usage": "visual-and-process-reference-only",
                "ingested_into_body": False,
            }
        )
    return entries


FIGURE_SPEC_RE = re.compile(
    r"<!--\s*figure-spec\s*(?P<body>.*?)-->\s*"
    r"(?P<bq>(?:^[ \t]*>[^\n]*(?:\r?\n|$))*)",
    re.DOTALL | re.MULTILINE,
)


def _figure_field(body: str, key: str) -> str:
    m = re.search(rf"^[ \t]*{re.escape(key)}:[ \t]*(.+?)[ \t]*$", body, re.MULTILINE)
    if not m:
        return ""
    return m.group(1).strip().strip("'\"")


def embed_figure_specs(
    markdown_text: str, asset_root: Path
) -> tuple[str, list[dict[str, Any]]]:
    """Replace inline figure-spec blocks with the real SVG when it exists, or a
    clean placeholder when it does not.

    A figure-spec is an HTML comment carrying YAML-ish metadata (``output``
    path, ``alt_ko``, ``caption_ko``) immediately followed by a blockquote
    placeholder. When the referenced binary exists under ``asset_root`` we emit a
    ``<figure>`` with the image; otherwise a bordered "제작 예정" placeholder so
    the book never shows the raw spec text.
    """
    figures: list[dict[str, Any]] = []

    def replace(match: re.Match[str]) -> str:
        body = match.group("body")
        output = _figure_field(body, "output")
        alt = _figure_field(body, "alt_ko") or _figure_field(body, "brief_ko")
        caption = _figure_field(body, "caption_ko") or alt
        fig_id = _figure_field(body, "id")
        resolved = ""
        exists = False
        if output:
            cand = (asset_root / output).expanduser()
            try:
                resolved = str(cand.resolve())
                exists = Path(resolved).is_file()
            except Exception:
                exists = False
        figures.append(
            {"id": fig_id, "output": output, "resolved": resolved, "embedded": exists}
        )
        cap_html = html.escape(caption)
        alt_html = html.escape(alt or caption)
        fid = html.escape(fig_id)
        if exists:
            return (
                f'\n<figure class="book-figure" id="{fid}">'
                f'<img src="{html.escape(resolved)}" alt="{alt_html}"/>'
                f"<figcaption>{cap_html}</figcaption>"
                f"</figure>\n"
            )
        return (
            f'\n<figure class="book-figure book-figure-pending" id="{fid}">'
            f'<div class="figure-pending"><span class="figure-pending-mark">시각자료</span>'
            f'<span class="figure-pending-caption">{cap_html}</span></div>'
            f"<figcaption>{cap_html}"
            f'<span class="figure-pending-note"> — 제작 예정</span>'
            f"</figcaption></figure>\n"
        )

    new_text = FIGURE_SPEC_RE.sub(replace, markdown_text)
    return new_text, figures


def build_document(
    content_root: Path,
    files: list[Path],
    config: dict[str, Any],
    references: list[Path],
    output_dir: Path,
    input_origin: dict[str, Any],
    asset_root: Path | None = None,
) -> tuple[Path, Path, dict[str, Any], dict[str, Any]]:
    file_cfg = config["files"]
    quality_cfg = config["quality"]
    front_name = Path(str(file_cfg.get("front_matter_file", "README.md"))).name.casefold()
    strip_sections = file_cfg.get("strip_front_matter_sections") or []
    drop_paragraphs = file_cfg.get("front_matter_drop_paragraphs") or []
    md = markdown_renderer()
    docs: list[SourceDoc] = []
    warnings: list[str] = []
    all_figures: list[dict[str, Any]] = []
    if asset_root is None:
        asset_root = content_root

    for path in files:
        raw = path.read_text(encoding="utf-8-sig")
        text = strip_yaml_frontmatter(raw)
        title = extract_title(text, path.stem)
        processed = remove_first_h1(text)
        removed_sections: list[str] = []
        removed_paragraphs: list[str] = []
        if path.name.casefold() == front_name:
            processed, removed_sections = strip_named_h2_sections(processed, strip_sections)
            processed, removed_paragraphs = strip_matching_markdown_paragraphs(processed, drop_paragraphs)
            if file_cfg.get("strip_front_matter_leading_rules", False):
                processed = re.sub(r"\A(?:[ \t]*\n)*(?:(?:---|\*\*\*|___)[ \t]*\n+)+", "", processed)
        processed, doc_figures = embed_figure_specs(processed, asset_root)
        all_figures.extend(doc_figures)
        headings = extract_headings(processed)
        rel = path.relative_to(content_root).as_posix()
        doc = SourceDoc(
            path=path,
            rel_path=rel,
            raw_text=raw,
            processed_markdown=processed,
            title=title,
            headings=headings,
            section_titles=[name for level, name in headings if level == 2],
            anchor=f"doc-{len(docs)+1:02d}-{slugify(title)}",
            sha256=sha256_file(path),
            counts=count_markdown(processed),
        )
        if removed_sections:
            doc.counts["stripped_editorial_sections"] = len(removed_sections)
        if removed_paragraphs:
            doc.counts["stripped_editorial_paragraphs"] = len(removed_paragraphs)
        docs.append(doc)

    path_to_anchor = {doc.rel_path: doc.anchor for doc in docs}
    used_ids = {doc.anchor for doc in docs}
    for idx, doc in enumerate(docs, start=1):
        rendered = md(sanitize_code_markers(doc.processed_markdown))
        doc.html_body = rewrite_doc_html(rendered, doc, idx, content_root, path_to_anchor, used_ids, warnings)
        doc.probes = make_probes(
            doc.html_body,
            int(quality_cfg.get("paragraph_probe_min_chars", 36)),
            int(quality_cfg.get("paragraph_probe_limit", 1200)),
        )

    front_doc = next((d for d in docs if d.path.name.casefold() == front_name), None)
    chapter_docs = [d for d in docs if d is not front_doc]
    if not chapter_docs:
        chapter_docs = docs
        front_doc = None

    book = config["book"]
    editorial = config["editorial"]

    # Generic configurations may request metadata inference. This changes only
    # book chrome and metadata; it never rewrites manuscript content.
    def auto_value(value: Any) -> bool:
        return value is None or not str(value).strip() or str(value).strip().casefold() == "auto"

    inferred_title = front_doc.title if front_doc is not None else chapter_docs[0].title
    if auto_value(book.get("title")):
        book["title"] = inferred_title
    if auto_value(book.get("short_title")):
        book["short_title"] = str(book["title"])
    if auto_value(book.get("subject")):
        book["subject"] = f"{book['title']} 한국어 출판형 PDF 편집본"
    if str(book.get("author", "")).strip().casefold() == "auto":
        book["author"] = ""
    if str(book.get("subtitle", "")).strip().casefold() == "auto":
        book["subtitle"] = ""

    build_date_value = str(book.get("build_date", "auto"))
    build_date_iso = dt.date.today().isoformat() if build_date_value == "auto" else build_date_value
    build_date = format_build_date(build_date_iso, str(editorial.get("build_date_format", "iso")))
    configured_quote = str(editorial.get("title_page_quote", "auto")).strip()
    quote = extract_title_quote(front_doc) if not configured_quote or configured_quote.casefold() == "auto" else configured_quote

    sections: list[str] = []
    if editorial.get("include_cover", True):
        sections.append(build_cover(config, content_root))
    if editorial.get("include_title_page", True):
        sections.append(build_title_page(config, quote))
    if editorial.get("include_editorial_note", True):
        sections.append(build_editorial_note(config, build_date))
    if front_doc:
        sections.append(f'<section class="front-matter"><div class="running-chapter"></div>{front_doc.html_body}</section>')
    if editorial.get("include_generated_toc", True):
        sections.append(build_toc(chapter_docs, config))
    if editorial.get("include_chapter_openers", True):
        for idx, doc in enumerate(chapter_docs, start=1):
            sections.append(build_chapter(doc, idx, config))
    else:
        for doc in chapter_docs:
            sections.append(f'<section class="chapter-body" id="{doc.anchor}"><div class="running-chapter">{html.escape(doc.title)}</div><h1>{html.escape(doc.title)}</h1>{doc.html_body}</section>')

    css = create_css(config)
    html_doc = f"""<!doctype html>
<html lang="{html.escape(str(book.get('language', 'ko-KR')))}">
<head>
<meta charset="utf-8">
<title>{html.escape(str(book.get('metadata_title') or book.get('title', '제목 없음')))}</title>
<meta name="author" content="{html.escape(str(book.get('author', '')))}">
<meta name="description" content="{html.escape(str(book.get('subject', '')))}">
<meta name="keywords" content="{html.escape(', '.join(str(x) for x in (book.get('keywords') or [])))}">
<style>{css}</style>
</head>
<body>{''.join(sections)}</body>
</html>"""

    output_dir.mkdir(parents=True, exist_ok=True)
    html_path = output_dir / "book.html"
    html_path.write_text(html_doc, encoding="utf-8")
    output_stem = safe_filename(f"{book.get('title', 'book')}_{book.get('output_name', '편집본')}")
    pdf_path = output_dir / f"{output_stem}.pdf"

    HTML(string=html_doc, base_url=str(content_root)).write_pdf(
        target=str(pdf_path),
        presentational_hints=True,
        custom_metadata=True,
    )

    reader = PdfReader(str(pdf_path))
    def outline_counts(items: Any) -> tuple[int, int]:
        if not isinstance(items, list):
            return 0, 0
        top_level = sum(1 for item in items if not isinstance(item, list))

        def recursive_count(values: list[Any]) -> int:
            total = 0
            for value in values:
                total += recursive_count(value) if isinstance(value, list) else 1
            return total

        return top_level, recursive_count(items)

    try:
        outline_top_level_count, outline_item_count = outline_counts(reader.outline)
    except Exception:
        outline_top_level_count, outline_item_count = 0, 0
    annotations = 0
    for page in reader.pages:
        annots = page.get("/Annots")
        if annots:
            annotations += len(annots)

    source_manifest = {
        "schema_version": 1,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "content_root": str(content_root),
        "input_origin": input_origin,
        "content_boundary": "Only files listed in content_files were ingested into the body.",
        "book_metadata": {
            "title": str(book.get("metadata_title") or book.get("title", "")),
            "display_title": str(book.get("title", "")),
            "author": str(book.get("author", "")),
            "subject": str(book.get("subject", "")),
            "language": str(book.get("language", "ko-KR")),
        },
        "content_files": [
            {
                "path": str(doc.path),
                "relative_path": doc.rel_path,
                "title": doc.title,
                "rendered_title": str(book.get("title", doc.title)) if doc is front_doc else doc.title,
                "role": "front_matter" if doc is front_doc else "chapter",
                "sha256": doc.sha256,
                "size_bytes": doc.path.stat().st_size,
                "counts": doc.counts,
                "headings": [{"level": level, "text": text} for level, text in doc.headings],
                "probes": doc.probes,
            }
            for doc in docs
        ],
        "reference_files": reference_entries(references),
    }

    aggregate_counts: dict[str, int] = {}
    for doc in docs:
        for key, value in doc.counts.items():
            if isinstance(value, int):
                aggregate_counts[key] = aggregate_counts.get(key, 0) + value

    build_report = {
        "status": "success",
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "book": book,
        "input": {
            "content_file_count": len(docs),
            "reference_file_count": len(references),
            "aggregate_counts": aggregate_counts,
        },
        "output": {
            "pdf": str(pdf_path),
            "visual_summary_pages": sum(1 for idx, doc in enumerate(chapter_docs, start=1) if visual_spec_for(doc, idx, config)),
            "toc_layout": "one-column",
            "pdf_sha256": sha256_file(pdf_path),
            "pdf_size_bytes": pdf_path.stat().st_size,
            "html": str(html_path),
            "pages": len(reader.pages),
            "outline_top_level_count": outline_top_level_count,
            "outline_item_count": outline_item_count,
            "annotations": annotations,
        },
        "warnings": sorted(set(warnings)),
        "content_policy": {
            "reference_content_ingested": False,
            "front_matter_sections_removed": strip_sections,
            "front_matter_paragraphs_removed": drop_paragraphs,
        },
    }

    manifest_path = output_dir / "source_manifest.json"
    report_path = output_dir / "build_report.json"
    manifest_path.write_text(json.dumps(source_manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    report_path.write_text(json.dumps(build_report, ensure_ascii=False, indent=2), encoding="utf-8")
    return pdf_path, html_path, source_manifest, build_report


def check_dependencies() -> int:
    checks = {
        "python": sys.version.split()[0],
        "mistune": getattr(mistune, "__version__", "unknown"),
        "pyyaml": getattr(yaml, "__version__", "unknown"),
        "beautifulsoup4": "available",
        "pypdf": "available",
        "weasyprint": "available",
        "pdftoppm": shutil.which("pdftoppm") or "not found (PyMuPDF fallback available)",
        "pdftotext": shutil.which("pdftotext") or "not found",
        "pdffonts": shutil.which("pdffonts") or "not found",
    }
    print(json.dumps(checks, ensure_ascii=False, indent=2))
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="CONTENT directory or ZIP")
    parser.add_argument("--output-dir", type=Path, help="Output directory")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="YAML configuration")
    parser.add_argument("--reference", type=Path, action="append", default=[], help="Reference-only file; may be repeated")
    parser.add_argument("--keep-workdir", action="store_true", help="Keep extracted temporary content")
    parser.add_argument("--check-deps", action="store_true", help="Print dependency status and exit")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.check_deps:
        return check_dependencies()
    if not args.input or not args.output_dir:
        raise SystemExit("--input and --output-dir are required unless --check-deps is used")
    config_path = args.config.resolve()
    if not config_path.exists():
        raise SystemExit(f"Config not found: {config_path}")
    config = load_config(config_path)

    temp_obj: tempfile.TemporaryDirectory[str] | None = None
    if args.keep_workdir:
        workdir = args.output_dir.resolve() / "_work"
        workdir.mkdir(parents=True, exist_ok=True)
    else:
        temp_obj = tempfile.TemporaryDirectory(prefix="korean-ebook-")
        workdir = Path(temp_obj.name)

    try:
        input_resolved = args.input.resolve()
        input_origin = {
            "type": "zip" if input_resolved.is_file() and input_resolved.suffix.casefold() == ".zip" else "directory",
            "path": str(input_resolved),
            "sha256": sha256_file(input_resolved) if input_resolved.is_file() else None,
        }
        content_root = resolve_input(input_resolved, workdir, config)
        # asset_root = where figure-spec output paths resolve. For a single-file
        # manuscript this is the file's own directory; for a folder/zip it is the
        # content root itself.
        asset_root = input_resolved.parent if input_resolved.is_file() else content_root
        files = discover_markdown_files(content_root, config)
        pdf_path, html_path, _, report = build_document(
            content_root=content_root,
            files=files,
            config=config,
            references=[p.resolve() for p in args.reference],
            output_dir=args.output_dir.resolve(),
            input_origin=input_origin,
            asset_root=asset_root,
        )
        print(f"PDF: {pdf_path}")
        print(f"HTML: {html_path}")
        print(f"Pages: {report['output']['pages']}")
        print(f"SHA-256: {report['output']['pdf_sha256']}")
        if report["warnings"]:
            print(f"Warnings: {len(report['warnings'])}")
            for warning in report["warnings"][:20]:
                print(f"- {warning}")
        return 0
    except BuildError as exc:
        print(f"Build failed: {exc}", file=sys.stderr)
        return 2
    finally:
        if temp_obj is not None:
            temp_obj.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
