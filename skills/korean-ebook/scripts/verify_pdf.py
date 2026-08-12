#!/usr/bin/env python3
"""Verify structure, source integrity, fonts, and reference isolation of a PDF."""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
import unicodedata
import zipfile
from pathlib import Path
from typing import Any, Iterable

try:
    from pypdf import PdfReader
except ImportError as exc:  # pragma: no cover
    print("Missing pypdf. Install scripts/requirements.txt", file=sys.stderr)
    raise SystemExit(2) from exc


A4_WIDTH_PT = 595.276
A4_HEIGHT_PT = 841.890


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", value)
    value = value.replace("–", "-").replace("—", "-")
    return re.sub(r"[\s-]+", "", value)


def extract_pdf_text(path: Path) -> tuple[str, str]:
    pdftotext = shutil.which("pdftotext")
    if pdftotext:
        proc = subprocess.run(
            [pdftotext, "-enc", "UTF-8", str(path), "-"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if proc.returncode == 0:
            return proc.stdout.decode("utf-8", errors="replace"), "pdftotext"
    reader = PdfReader(str(path))
    return "\n\f\n".join(page.extract_text() or "" for page in reader.pages), "pypdf"


def extract_docx_or_pptx_text(path: Path) -> str:
    text_parts: list[str] = []
    with zipfile.ZipFile(path) as zf:
        candidates = []
        if path.suffix.casefold() == ".docx":
            candidates = [name for name in zf.namelist() if name.startswith("word/") and name.endswith(".xml")]
        elif path.suffix.casefold() == ".pptx":
            candidates = [name for name in zf.namelist() if name.startswith("ppt/slides/") and name.endswith(".xml")]
        for name in candidates:
            raw = zf.read(name).decode("utf-8", errors="ignore")
            raw = re.sub(r"</w:p>|</a:p>", "\n", raw)
            for left, right in re.findall(r"<w:t[^>]*>(.*?)</w:t>|<a:t[^>]*>(.*?)</a:t>", raw):
                text_parts.append(html.unescape(left or right))
    return " ".join(text_parts)


def extract_reference_text(path: Path) -> tuple[str, str]:
    suffix = path.suffix.casefold()
    if suffix in {".md", ".markdown", ".txt", ".html", ".htm", ".csv", ".json", ".yaml", ".yml"}:
        return path.read_text(encoding="utf-8", errors="replace"), "plain-text"
    if suffix == ".pdf":
        return extract_pdf_text(path)
    if suffix in {".docx", ".pptx"}:
        try:
            return extract_docx_or_pptx_text(path), "office-xml"
        except Exception as exc:
            return "", f"unverified: {exc}"
    return "", "unsupported"


def words(value: str) -> list[str]:
    value = unicodedata.normalize("NFKC", value).casefold()
    return re.findall(r"[0-9a-z가-힣]+", value)


def ngrams(word_list: list[str], n: int, min_chars: int, limit: int = 250_000) -> set[str]:
    result: set[str] = set()
    if n <= 0 or len(word_list) < n:
        return result
    for idx in range(len(word_list) - n + 1):
        gram = " ".join(word_list[idx : idx + n])
        if len(gram.replace(" ", "")) >= min_chars:
            result.add(gram)
        if len(result) >= limit:
            break
    return result


def count_outline(items: Any) -> int:
    if not isinstance(items, list):
        return 0
    count = 0
    for item in items:
        if isinstance(item, list):
            count += count_outline(item)
        else:
            count += 1
    return count


def parse_pdffonts(pdf: Path) -> dict[str, Any]:
    exe = shutil.which("pdffonts")
    if not exe:
        return {"status": "unverified", "reason": "pdffonts not found", "fonts": []}
    proc = subprocess.run([exe, str(pdf)], check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        return {"status": "unverified", "reason": proc.stderr.strip(), "fonts": []}
    fonts: list[dict[str, str]] = []
    lines = proc.stdout.splitlines()
    for line in lines[2:]:
        parts = line.split()
        if len(parts) < 6:
            continue
        # The last five fields are emb, sub, uni, object id, generation id.
        emb, sub, uni = parts[-5], parts[-4], parts[-3]
        fonts.append({"name": parts[0], "embedded": emb, "subset": sub, "unicode": uni, "raw": line})
    status = "pass" if fonts and all(f["embedded"] == "yes" and f["unicode"] == "yes" for f in fonts) else "fail"
    return {"status": status, "fonts": fonts, "raw": proc.stdout}


def repair_zip_name(name: str) -> str:
    """Recover raw UTF-8 ZIP names that were decoded as CP437."""

    try:
        candidate = name.encode("cp437").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return name

    def quality(value: str) -> tuple[int, int, int]:
        korean = sum(1 for ch in value if "가" <= ch <= "힣")
        suspicious = sum(1 for ch in value if ch in "∞δφΩ╢╕╣╔╠╬╩╦╪╫╧╨╤╥╙╘╓╒")
        return korean, -suspicious, -value.count("�")

    return candidate if quality(candidate) > quality(name) else name


def markdown_to_plain(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"~~~.*?~~~", " ", text, flags=re.S)
    text = re.sub(r"!\[([^]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.M)
    text = re.sub(r"[*_`>|~-]", " ", text)
    return text


def source_text_from_manifest(manifest: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    chunks: list[str] = []
    status: list[dict[str, Any]] = []
    origin = manifest.get("input_origin") or {}
    origin_type = origin.get("type")
    origin_path = Path(origin.get("path", "")) if origin.get("path") else None
    zip_handle: zipfile.ZipFile | None = None
    zip_entries: list[tuple[zipfile.ZipInfo, str]] = []
    if origin_type == "zip" and origin_path and origin_path.exists():
        try:
            zip_handle = zipfile.ZipFile(origin_path)
            zip_entries = [(info, repair_zip_name(info.filename).replace("\\", "/")) for info in zip_handle.infolist()]
        except Exception:
            zip_handle = None

    try:
        for item in manifest.get("content_files", []):
            recorded_path = Path(item.get("path", ""))
            rel = str(item.get("relative_path", "")).replace("\\", "/")
            record: dict[str, Any] = {
                "path": str(recorded_path),
                "relative_path": rel,
                "exists": False,
                "hash_matches": False,
                "source_location": None,
            }
            data: bytes | None = None

            if recorded_path.exists():
                data = recorded_path.read_bytes()
                record["source_location"] = "build-path"
            elif origin_type == "directory" and origin_path:
                candidate = (origin_path / rel).resolve()
                if candidate.exists() and candidate.is_file():
                    data = candidate.read_bytes()
                    record["source_location"] = "origin-directory"
                    record["path"] = str(candidate)
            elif zip_handle is not None and rel:
                candidates = [(info, repaired) for info, repaired in zip_entries if repaired == rel or repaired.endswith("/" + rel)]
                if candidates:
                    chosen_info, chosen_name = sorted(
                        candidates, key=lambda value: (value[1].count("/"), len(value[1]))
                    )[0]
                    data = zip_handle.read(chosen_info)
                    record["source_location"] = f"origin-zip:{chosen_name}"

            if data is not None:
                record["exists"] = True
                actual_hash = hashlib.sha256(data).hexdigest()
                record["actual_sha256"] = actual_hash
                record["expected_sha256"] = item.get("sha256")
                record["hash_matches"] = actual_hash == item.get("sha256")
                try:
                    chunks.append(markdown_to_plain(data.decode("utf-8-sig", errors="replace")))
                except Exception as exc:
                    record["read_error"] = str(exc)
            status.append(record)
    finally:
        if zip_handle is not None:
            zip_handle.close()
    return "\n".join(chunks), status


def page_size_checks(reader: PdfReader, tolerance: float = 3.0) -> tuple[list[dict[str, Any]], list[int]]:
    sizes: list[dict[str, Any]] = []
    non_a4: list[int] = []
    for idx, page in enumerate(reader.pages, start=1):
        box = page.mediabox
        width = float(box.width)
        height = float(box.height)
        is_a4 = (abs(width - A4_WIDTH_PT) <= tolerance and abs(height - A4_HEIGHT_PT) <= tolerance) or (
            abs(height - A4_WIDTH_PT) <= tolerance and abs(width - A4_HEIGHT_PT) <= tolerance
        )
        sizes.append({"page": idx, "width_pt": round(width, 3), "height_pt": round(height, 3), "a4": is_a4})
        if not is_a4:
            non_a4.append(idx)
    return sizes, non_a4


def write_markdown_report(path: Path, report: dict[str, Any]) -> None:
    summary = report["summary"]
    lines = [
        "# PDF 검수 보고서",
        "",
        f"- 상태: **{summary['status']}**",
        f"- PDF: `{report['pdf']['path']}`",
        f"- 페이지: {report['pdf']['pages']}",
        f"- SHA-256: `{report['pdf']['sha256']}`",
        f"- 텍스트 추출기: {report['pdf']['text_extractor']}",
        "",
        "## 핵심 결과",
        "",
        f"- 비-A4 페이지: {len(report['structure']['non_a4_pages'])}개",
        f"- 북마크: {report['structure']['outline_items']}개",
        f"- 링크 주석: {report['structure']['link_annotations']}개",
        f"- 글꼴: {report['fonts']['status']}",
        f"- 누락 문단 표본: {report['integrity']['missing_probe_count']}개 / {report['integrity']['probe_count']}개",
        f"- 누락 제목: {report['integrity']['missing_heading_count']}개",
        f"- 참고자료 오염 후보: {report['reference_isolation']['match_count']}개",
        f"- 빈 페이지 후보: {len(report['structure']['blank_page_candidates'])}개",
        "",
    ]
    if report["issues"]:
        lines.extend(["## 발견 사항", ""])
        for issue in report["issues"]:
            lines.append(f"- **{issue['severity']}** — {issue['message']}")
        lines.append("")
    if report["integrity"]["missing_probes"]:
        lines.extend(["## 누락 문단 표본", ""])
        for item in report["integrity"]["missing_probes"][:30]:
            lines.append(f"- `{item['source']}` — {item['probe']}")
        lines.append("")
    if report["reference_isolation"]["matches"]:
        lines.extend(["## 참고자료 오염 후보", ""])
        for item in report["reference_isolation"]["matches"][:30]:
            lines.append(f"- `{item['reference']}` — {item['ngram']}")
        lines.append("")
    lines.extend(
        [
            "## 판정 기준",
            "",
            "자동 검사는 시각 검수를 대체하지 않습니다. 최종 완료 전 전 페이지 렌더 또는 접촉표를 확인해야 합니다.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--source-manifest", type=Path, required=True)
    parser.add_argument("--reference", type=Path, action="append", default=[])
    parser.add_argument("--report-dir", type=Path, required=True)
    parser.add_argument("--ngram-words", type=int, default=8)
    parser.add_argument("--ngram-min-chars", type=int, default=44)
    parser.add_argument("--allow-blank-pages", type=int, default=0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    pdf = args.pdf.resolve()
    manifest_path = args.source_manifest.resolve()
    report_dir = args.report_dir.resolve()
    report_dir.mkdir(parents=True, exist_ok=True)
    issues: list[dict[str, str]] = []

    if not pdf.exists():
        print(f"PDF not found: {pdf}", file=sys.stderr)
        return 2
    if not manifest_path.exists():
        print(f"Source manifest not found: {manifest_path}", file=sys.stderr)
        return 2

    try:
        reader = PdfReader(str(pdf))
    except Exception as exc:
        print(f"Cannot open PDF: {exc}", file=sys.stderr)
        return 2
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    text, extractor = extract_pdf_text(pdf)
    normalized_pdf = normalize_text(text)
    pages_text = text.split("\f")[: len(reader.pages)]
    blank_candidates = [idx for idx, value in enumerate(pages_text, start=1) if len(normalize_text(value)) < 12]

    sizes, non_a4 = page_size_checks(reader)
    if non_a4:
        issues.append({"severity": "high", "message": f"A4가 아닌 페이지가 {len(non_a4)}개 있습니다: {non_a4[:20]}"})

    metadata = {str(k): str(v) for k, v in (reader.metadata or {}).items()}
    expected_meta = manifest.get("book_metadata") or {}
    expected_title = str(expected_meta.get("title", "")).strip()
    expected_author = str(expected_meta.get("author", "")).strip()
    if not metadata.get("/Title"):
        issues.append({"severity": "medium", "message": "PDF 제목 메타데이터가 없습니다."})
    elif expected_title and normalize_text(metadata.get("/Title", "")) != normalize_text(expected_title):
        issues.append({"severity": "medium", "message": "PDF 제목 메타데이터가 설정값과 다릅니다."})
    if expected_author and not metadata.get("/Author"):
        issues.append({"severity": "medium", "message": "설정에 저자가 있으나 PDF 저자 메타데이터가 없습니다."})
    elif expected_author and normalize_text(metadata.get("/Author", "")) != normalize_text(expected_author):
        issues.append({"severity": "medium", "message": "PDF 저자 메타데이터가 설정값과 다릅니다."})

    try:
        outline_items = count_outline(reader.outline)
    except Exception:
        outline_items = 0
    if outline_items == 0:
        issues.append({"severity": "high", "message": "PDF 북마크/아웃라인이 없습니다."})

    annotations = 0
    link_annotations = 0
    for page in reader.pages:
        annots = page.get("/Annots") or []
        annotations += len(annots)
        for ref in annots:
            try:
                obj = ref.get_object()
                if obj.get("/Subtype") == "/Link":
                    link_annotations += 1
            except Exception:
                continue

    fonts = parse_pdffonts(pdf)
    if fonts["status"] == "fail":
        bad = [f["name"] for f in fonts["fonts"] if f["embedded"] != "yes" or f["unicode"] != "yes"]
        issues.append({"severity": "high", "message": f"임베딩 또는 유니코드 매핑이 불완전한 글꼴: {', '.join(bad)}"})
    elif fonts["status"] == "unverified":
        issues.append({"severity": "medium", "message": f"글꼴 검사를 완료하지 못했습니다: {fonts.get('reason', '')}"})

    if "�" in text:
        issues.append({"severity": "high", "message": "텍스트 추출 결과에서 대체문자 �가 발견되었습니다."})

    source_text, source_file_status = source_text_from_manifest(manifest)
    for item in source_file_status:
        if not item["exists"]:
            issues.append({"severity": "medium", "message": f"소스 파일을 다시 열 수 없어 해시 재검증을 생략했습니다: {item['relative_path']}"})
        elif not item["hash_matches"]:
            issues.append({"severity": "high", "message": f"소스 파일 해시가 빌드 시점과 다릅니다: {item['path']}"})

    probes: list[dict[str, Any]] = []
    headings: list[dict[str, str]] = []
    for doc in manifest.get("content_files", []):
        source = doc.get("relative_path") or doc.get("path")
        for probe in doc.get("probes", []):
            probes.append({"source": source, **probe})
        rendered_title = doc.get("rendered_title") or doc.get("title")
        if rendered_title:
            headings.append({"source": source, "text": str(rendered_title)})
        for heading in doc.get("headings", []):
            headings.append({"source": source, "text": str(heading.get("text", ""))})

    missing_probes: list[dict[str, Any]] = []
    for probe in probes:
        prefix = normalize_text(str(probe.get("prefix", "")))
        suffix = normalize_text(str(probe.get("suffix", "")))
        if not prefix or not suffix or prefix not in normalized_pdf or suffix not in normalized_pdf:
            missing_probes.append({"source": probe["source"], "probe": probe.get("probe", "")})
    missing_ratio = (len(missing_probes) / len(probes)) if probes else 0.0
    if missing_probes and missing_ratio > 0.02:
        issues.append({"severity": "high", "message": f"원문 문단 표본 {len(missing_probes)}개가 PDF에서 확인되지 않았습니다 ({missing_ratio:.1%})."})
    elif missing_probes:
        issues.append({"severity": "medium", "message": f"원문 문단 표본 {len(missing_probes)}개가 PDF에서 확인되지 않았습니다 ({missing_ratio:.1%})."})

    missing_headings: list[dict[str, str]] = []
    for heading in headings:
        norm = normalize_text(heading["text"])
        if len(norm) >= 2 and norm not in normalized_pdf:
            missing_headings.append(heading)
    if missing_headings:
        issues.append({"severity": "high", "message": f"원문 제목 {len(missing_headings)}개가 PDF에서 확인되지 않았습니다."})

    if len(blank_candidates) > args.allow_blank_pages:
        issues.append({"severity": "medium", "message": f"빈 페이지 후보가 {len(blank_candidates)}개 있습니다: {blank_candidates[:30]}"})

    source_grams = ngrams(words(source_text), args.ngram_words, args.ngram_min_chars)
    output_grams = ngrams(words(text), args.ngram_words, args.ngram_min_chars)
    reference_records: list[dict[str, Any]] = []
    contamination: list[dict[str, str]] = []
    references = [p.resolve() for p in args.reference]
    if not references:
        references = [Path(item["path"]) for item in manifest.get("reference_files", []) if item.get("path")]
    for reference in references:
        record: dict[str, Any] = {"path": str(reference), "exists": reference.exists()}
        if not reference.exists():
            record["status"] = "missing"
            reference_records.append(record)
            issues.append({"severity": "medium", "message": f"참고자료를 찾을 수 없어 오염 검사를 생략했습니다: {reference}"})
            continue
        ref_text, method = extract_reference_text(reference)
        record["extractor"] = method
        record["characters"] = len(ref_text)
        if not ref_text:
            record["status"] = "unverified"
            reference_records.append(record)
            issues.append({"severity": "medium", "message": f"참고자료 텍스트를 추출하지 못했습니다: {reference.name} ({method})"})
            continue
        ref_grams = ngrams(words(ref_text), args.ngram_words, args.ngram_min_chars)
        unique_ref = ref_grams - source_grams
        matches = sorted(unique_ref & output_grams)
        record["status"] = "checked"
        record["unique_ngrams"] = len(unique_ref)
        record["matches"] = len(matches)
        reference_records.append(record)
        for gram in matches[:50]:
            contamination.append({"reference": reference.name, "ngram": gram})
    if contamination:
        issues.append({"severity": "high", "message": f"참고자료 고유 문구가 최종 PDF에 들어간 후보가 {len(contamination)}개 있습니다."})

    high_count = sum(1 for issue in issues if issue["severity"] == "high")
    medium_count = sum(1 for issue in issues if issue["severity"] == "medium")
    status = "fail" if high_count else ("conditional" if medium_count else "pass")

    report = {
        "schema_version": 1,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "summary": {"status": status, "high_issues": high_count, "medium_issues": medium_count},
        "pdf": {
            "path": str(pdf),
            "sha256": sha256_file(pdf),
            "size_bytes": pdf.stat().st_size,
            "pages": len(reader.pages),
            "metadata": metadata,
            "text_extractor": extractor,
        },
        "structure": {
            "page_sizes": sizes,
            "non_a4_pages": non_a4,
            "outline_items": outline_items,
            "annotations": annotations,
            "link_annotations": link_annotations,
            "blank_page_candidates": blank_candidates,
        },
        "fonts": fonts,
        "integrity": {
            "source_file_status": source_file_status,
            "probe_count": len(probes),
            "missing_probe_count": len(missing_probes),
            "missing_probe_ratio": missing_ratio,
            "missing_probes": missing_probes[:100],
            "heading_count": len(headings),
            "missing_heading_count": len(missing_headings),
            "missing_headings": missing_headings[:100],
        },
        "reference_isolation": {
            "references": reference_records,
            "match_count": len(contamination),
            "matches": contamination[:100],
            "ngram_words": args.ngram_words,
            "ngram_min_chars": args.ngram_min_chars,
        },
        "issues": issues,
        "manual_review_required": True,
    }

    json_path = report_dir / "verification.json"
    md_path = report_dir / "verification.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown_report(md_path, report)
    print(f"Status: {status}")
    print(f"Report: {md_path}")
    print(f"High issues: {high_count}; medium issues: {medium_count}")
    return 2 if status == "fail" else (1 if status == "conditional" else 0)


if __name__ == "__main__":
    raise SystemExit(main())
