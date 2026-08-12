#!/usr/bin/env python3
"""Verify a korean-ebook static manual package independently from its builder."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup

from manual_common import Issue, load_manual, resolve_local_path, validate_source_contract


REQUIRED_LESSON_HEADINGS = {
    "이 작업의 목적",
    "언제 사용하는가",
    "시작 전 준비",
    "안전 경계",
    "실행 단계",
    "주의할 점",
    "흔한 실수",
    "완료 확인",
    "근거",
    "다음 분기",
}
PLACEHOLDER_RE = re.compile(r"\b(?:TODO|TBD|UI_CAPTURE_REQUIRED)\b", re.IGNORECASE)
RAW_MARKDOWN_LINK_RE = re.compile(r"\[[^\]\n]+\]\([^)\n]+\)")
RAW_HTML_RE = re.compile(r"</?(?:a|div|span|section|article|img|video)\b[^>]*>", re.IGNORECASE)
TEMPLATE_TOKEN_RE = re.compile(r"\{\{[^{}\n]+\}\}")
EXTERNAL_SCHEMES = {"http", "https", "mailto", "tel"}
ACTIVE_TAGS = {"script", "iframe", "object", "embed"}
ACTIVE_MARKDOWN_HTML_RE = re.compile(
    r"</?(?:script|iframe|object|embed)\b[^>]*>", re.IGNORECASE
)
UNSAFE_MARKDOWN_LINK_RE = re.compile(
    r"\[[^\]\n]+\]\(\s*(?:javascript|data):", re.IGNORECASE
)
EXTERNAL_CSS_RE = re.compile(
    r"@import\b|url\(\s*['\"]?\s*(?:https?:|data:|javascript:)", re.IGNORECASE
)


def _issue(
    issues: list[Issue],
    severity: str,
    code: str,
    message: str,
    location: str,
) -> None:
    issues.append(Issue(severity, code, message, location))


def _required_paths(data: dict[str, Any]) -> set[str]:
    paths = {
        "index.html",
        "overview.html",
        "assets/manual.css",
        "sources/evidence-map.md",
        "qa/build-report.json",
        "manual-manifest.json",
        "STATUS.md",
        "HANDOFF.md",
    }
    paths.update(f"lessons/{lesson['id']}.html" for lesson in data.get("lessons", []))
    return paths


def _safe_package_target(package_dir: Path, page: Path, raw_target: str) -> Path | None:
    split = urlsplit(raw_target)
    scheme = split.scheme.casefold()
    if scheme and scheme not in EXTERNAL_SCHEMES:
        raise ValueError(f"unsafe link scheme: {scheme}")
    if scheme in EXTERNAL_SCHEMES or split.netloc:
        return None
    path_text = unquote(split.path)
    if not path_text:
        return None
    target = (page.parent / path_text).resolve()
    try:
        target.relative_to(package_dir.resolve())
    except ValueError as exc:
        raise ValueError(f"link escapes package root: {raw_target}") from exc
    return target


def _scan_html(package_dir: Path, path: Path, issues: list[Issue]) -> BeautifulSoup:
    rel = path.relative_to(package_dir).as_posix()
    try:
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    except (OSError, UnicodeError) as exc:
        _issue(issues, "high", "html-read", f"HTML을 읽을 수 없습니다: {exc}", rel)
        return BeautifulSoup("", "html.parser")

    if soup.find("html") is None or soup.find("body") is None or soup.find("main") is None:
        _issue(issues, "high", "html-structure", "html/body/main 구조가 필요합니다", rel)
    if soup.find("title") is None or not soup.title.get_text(strip=True):
        _issue(issues, "high", "html-title", "비어 있지 않은 title이 필요합니다", rel)
    if soup.find("h1") is None:
        _issue(issues, "high", "html-h1", "페이지마다 H1이 필요합니다", rel)

    for tag in soup.find_all(ACTIVE_TAGS):
        _issue(
            issues,
            "high",
            "active-content",
            f"실행 가능한 HTML 요소를 허용하지 않습니다: {tag.name}",
            rel,
        )
    for tag in soup.find_all(True):
        for attribute in tag.attrs:
            if str(attribute).casefold().startswith("on"):
                _issue(
                    issues,
                    "high",
                    "active-content",
                    f"이벤트 핸들러 속성을 허용하지 않습니다: {attribute}",
                    rel,
                )

    visible = soup.get_text("\n", strip=True)
    for match in PLACEHOLDER_RE.finditer(visible):
        _issue(
            issues,
            "high",
            "placeholder-leak",
            f"최종 사용자 화면에 placeholder가 노출됩니다: {match.group(0)}",
            rel,
        )
    if RAW_MARKDOWN_LINK_RE.search(visible):
        _issue(
            issues,
            "high",
            "raw-markdown-link",
            "원시 Markdown 링크 문법이 사용자 화면에 노출됩니다",
            rel,
        )
    if RAW_HTML_RE.search(visible):
        _issue(
            issues,
            "high",
            "raw-html-leak",
            "원시 HTML 태그가 사용자 화면에 노출됩니다",
            rel,
        )
    if TEMPLATE_TOKEN_RE.search(visible):
        _issue(
            issues,
            "high",
            "template-token-leak",
            "치환되지 않은 템플릿 변수가 사용자 화면에 노출됩니다",
            rel,
        )

    for element, attribute in [(tag, attr) for tag in soup.find_all(True) for attr in ("href", "src") if tag.has_attr(attr)]:
        raw_target = str(element.get(attribute) or "")
        if not raw_target or raw_target.startswith("#"):
            continue
        try:
            split = urlsplit(raw_target)
            if attribute == "href" and (split.scheme or split.netloc):
                _issue(
                    issues,
                    "high",
                    "external-link",
                    f"패키지 밖 링크를 허용하지 않습니다: {raw_target}",
                    rel,
                )
                continue
            if attribute == "src" and (split.scheme or split.netloc):
                raise ValueError(f"external asset is not allowed: {raw_target}")
            target = _safe_package_target(package_dir, path, raw_target)
        except ValueError as exc:
            _issue(issues, "high", "unsafe-link", str(exc), rel)
            continue
        if target is not None and not target.exists():
            _issue(
                issues,
                "high",
                "broken-link",
                f"깨진 내부 링크 또는 매체 경로: {raw_target}",
                rel,
            )
    for image in soup.find_all("img"):
        if not str(image.get("alt") or "").strip():
            _issue(issues, "medium", "missing-alt", "이미지 alt 설명이 없습니다", rel)
    return soup


def _check_lesson_depth(
    package_dir: Path,
    data: dict[str, Any],
    issues: list[Issue],
) -> None:
    for lesson in data.get("lessons", []):
        rel = f"lessons/{lesson['id']}.html"
        path = package_dir / rel
        if not path.is_file():
            continue
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        headings = {heading.get_text(" ", strip=True) for heading in soup.find_all("h2")}
        for missing in sorted(REQUIRED_LESSON_HEADINGS - headings):
            _issue(
                issues,
                "high",
                "lesson-depth",
                f"독립 lesson 필수 구획이 없습니다: {missing}",
                rel,
            )
        step_count = len(soup.select(".step-list .step"))
        if step_count != len(lesson.get("steps", [])):
            _issue(
                issues,
                "high",
                "step-count",
                f"manifest 단계 {len(lesson.get('steps', []))}개와 HTML 단계 {step_count}개가 다릅니다",
                rel,
            )
        for index, step in enumerate(soup.select(".step-list .step"), start=1):
            if index > len(lesson.get("steps", [])):
                _issue(
                    issues,
                    "high",
                    "step-content-drift",
                    f"manifest에 없는 {index}번 단계가 삽입되었습니다",
                    rel,
                )
                continue
            manifest_step = lesson.get("steps", [])[index - 1]
            expected_fields = {
                "h3": str(manifest_step["title"]),
                ".operation": f"작업 유형: {manifest_step['operation']}",
                ".action": f"실행: {manifest_step['action']}",
                ".evidence": f"화면·문서 증거: {manifest_step['evidence']}",
                ".success": f"성공 판정: {manifest_step['success']}",
            }
            if manifest_step["operation"] == "write":
                expected_fields[".readback"] = f"변경 후 재확인: {manifest_step['readback']}"
            for selector, expected in expected_fields.items():
                element = step.select_one(selector)
                actual = element.get_text(" ", strip=True) if element else ""
                if actual != expected:
                    _issue(
                        issues,
                        "high",
                        "step-content-drift",
                        f"{index}번 단계의 {selector} 내용이 manifest와 다릅니다",
                        rel,
                    )
            if step.select_one(".evidence") is None or step.select_one(".success") is None:
                _issue(
                    issues,
                    "high",
                    "step-evidence",
                    f"{index}번 단계에 증거 또는 성공 판정이 없습니다",
                    rel,
                )


def _check_status_truthfulness(
    package_dir: Path,
    data: dict[str, Any],
    issues: list[Issue],
) -> None:
    status = str(data.get("manual", {}).get("status") or "")
    index_path = package_dir / "index.html"
    if not index_path.is_file():
        return
    soup = BeautifulSoup(index_path.read_text(encoding="utf-8"), "html.parser")
    banner = soup.select_one(".status-banner")
    if status in {"draft", "provisional"} and banner is None:
        _issue(
            issues,
            "high",
            "missing-status-banner",
            "임시 매뉴얼에 독자용 상태 고지가 없습니다",
            "index.html",
        )
    if status == "final" and banner is not None:
        _issue(
            issues,
            "medium",
            "stale-status-banner",
            "final 매뉴얼에 임시 상태 배너가 남아 있습니다",
            "index.html",
        )


def _check_visual_evidence(
    package_dir: Path,
    data: dict[str, Any],
    visual_evidence: Path | None,
    visual_reviewed_claim: bool,
    issues: list[Issue],
) -> str:
    status = str(data.get("manual", {}).get("status") or "")
    if visual_evidence is None:
        if visual_reviewed_claim or status == "final":
            _issue(
                issues,
                "high",
                "visual-evidence-required",
                "시각 검수 PASS에는 구조화된 visual-review.json 증거가 필요합니다",
                "qa/visual-review.json",
            )
            return "fail"
        return "not_run"

    evidence_path = visual_evidence.resolve()
    try:
        evidence_path.relative_to(package_dir.resolve())
    except ValueError:
        _issue(
            issues,
            "high",
            "visual-evidence-location",
            "visual-review.json은 검증 대상 패키지 안에 있어야 합니다",
            str(evidence_path),
        )
        return "fail"
    try:
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        _issue(
            issues,
            "high",
            "visual-evidence-read",
            f"시각 검수 증거를 읽을 수 없습니다: {exc}",
            str(evidence_path),
        )
        return "fail"
    if not isinstance(evidence, dict):
        _issue(
            issues,
            "high",
            "visual-evidence-object",
            "visual-review.json은 JSON object여야 합니다",
            str(evidence_path),
        )
        return "fail"

    def require_text(field: str, expected: str | None = None) -> str:
        value = evidence.get(field)
        if not isinstance(value, str) or not value.strip():
            _issue(
                issues,
                "high",
                "visual-evidence-field",
                f"visual-review.json의 {field}가 필요합니다",
                str(evidence_path),
            )
            return ""
        if expected is not None and value != expected:
            _issue(
                issues,
                "high",
                "visual-evidence-verdict",
                f"visual-review.json의 {field}는 {expected}여야 합니다",
                str(evidence_path),
            )
        return value

    if evidence.get("schema_version") != 1:
        _issue(
            issues,
            "high",
            "visual-evidence-schema",
            "visual-review.json schema_version은 1이어야 합니다",
            str(evidence_path),
        )
    require_text("status", "pass")
    require_text("reviewed_at")
    require_text("reviewer")
    require_text("keyboard_navigation", "pass")
    require_text("internal_navigation", "pass")

    viewports = evidence.get("viewports")
    if not isinstance(viewports, list) or len(viewports) < 2 or not all(
        isinstance(value, str) and re.fullmatch(r"\d+x\d+", value) for value in viewports
    ):
        _issue(
            issues,
            "high",
            "visual-evidence-viewports",
            "desktop과 mobile을 포함한 viewport 두 개 이상이 필요합니다",
            str(evidence_path),
        )

    reviewed_pages = evidence.get("pages")
    required_pages = {
        "index.html",
        "overview.html",
        *(f"lessons/{lesson['id']}.html" for lesson in data.get("lessons", [])),
    }
    if not isinstance(reviewed_pages, list):
        _issue(
            issues,
            "high",
            "visual-evidence-pages",
            "검수한 pages 목록이 필요합니다",
            str(evidence_path),
        )
    else:
        missing_pages = required_pages - {str(value) for value in reviewed_pages}
        for rel in sorted(missing_pages):
            _issue(
                issues,
                "high",
                "visual-page-missing",
                f"시각 검수에서 빠진 필수 페이지: {rel}",
                str(evidence_path),
            )

    console_errors = evidence.get("console_errors")
    if not isinstance(console_errors, int) or isinstance(console_errors, bool) or console_errors != 0:
        _issue(
            issues,
            "high",
            "visual-console-errors",
            "시각 검수 PASS에는 console_errors: 0이 필요합니다",
            str(evidence_path),
        )
    findings = evidence.get("findings")
    if not isinstance(findings, list):
        _issue(
            issues,
            "high",
            "visual-findings",
            "visual-review.json의 findings는 배열이어야 합니다",
            str(evidence_path),
        )
    else:
        for index, finding in enumerate(findings):
            if not isinstance(finding, dict):
                _issue(
                    issues,
                    "high",
                    "visual-finding-schema",
                    f"findings[{index}]는 object여야 합니다",
                    str(evidence_path),
                )
                continue
            severity = str(finding.get("severity") or "")
            finding_status = str(finding.get("status") or "")
            if severity not in {"low", "medium", "high", "critical"} or finding_status not in {
                "open",
                "resolved",
                "accepted",
            }:
                _issue(
                    issues,
                    "high",
                    "visual-finding-schema",
                    f"findings[{index}]의 severity/status가 유효하지 않습니다",
                    str(evidence_path),
                )
            if severity in {"high", "critical"} and finding_status != "resolved":
                _issue(
                    issues,
                    "high",
                    "visual-unresolved-finding",
                    f"미해결 {severity} 시각 finding이 있습니다: {finding.get('message', '')}",
                    str(evidence_path),
                )
    return "fail" if any(issue.code.startswith("visual-") and issue.severity == "high" for issue in issues) else "pass"


def _check_manifest_parity(
    package_dir: Path,
    data: dict[str, Any],
    issues: list[Issue],
) -> None:
    normalized_path = package_dir / "manual-manifest.json"
    if not normalized_path.is_file():
        return
    try:
        packaged = json.loads(normalized_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeError) as exc:
        _issue(
            issues,
            "high",
            "packaged-manifest",
            f"manual-manifest.json을 읽을 수 없습니다: {exc}",
            "manual-manifest.json",
        )
        return
    if packaged != data:
        _issue(
            issues,
            "high",
            "manifest-drift",
            "빌드 패키지 매니페스트가 입력 manual.yaml과 다릅니다",
            "manual-manifest.json",
        )


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _check_evidence_integrity(
    manifest_path: Path,
    package_dir: Path,
    data: dict[str, Any],
    issues: list[Issue],
) -> None:
    report_path = package_dir / "qa" / "build-report.json"
    if not report_path.is_file():
        return
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        _issue(issues, "high", "build-report-read", f"build report를 읽을 수 없습니다: {exc}", "qa/build-report.json")
        return
    if report.get("source_manifest_sha256") != _sha256_file(manifest_path):
        _issue(issues, "high", "source-manifest-drift", "manual.yaml이 빌드 후 변경되었습니다", str(manifest_path))
    recorded = report.get("evidence_files")
    if not isinstance(recorded, dict):
        _issue(issues, "high", "evidence-manifest", "build report에 evidence_files가 없습니다", "qa/build-report.json")
        return
    for source in data.get("sources", []):
        source_id = str(source.get("id") or "")
        item = recorded.get(source_id)
        if not isinstance(item, dict):
            _issue(issues, "high", "evidence-manifest", f"기록되지 않은 근거입니다: {source_id}", "qa/build-report.json")
            continue
        path = resolve_local_path(manifest_path.parent, str(source.get("path") or ""))
        if item.get("sha256") != _sha256_file(path) or item.get("bytes") != path.stat().st_size:
            _issue(issues, "high", "evidence-drift", f"빌드 후 근거 파일이 변경되었습니다: {source_id}", str(path))
    packaged_media = report.get("packaged_media")
    if not isinstance(packaged_media, dict):
        _issue(issues, "high", "media-manifest", "build report에 packaged_media가 없습니다", "qa/build-report.json")
        return
    declared_media = {
        str(media.get("path") or ""): str(media.get("sha256") or "")
        for lesson in data.get("lessons", [])
        for media in lesson.get("media", [])
        if isinstance(media, dict)
    }
    for source_path, item in packaged_media.items():
        if not isinstance(item, dict) or not isinstance(item.get("package_path"), str):
            _issue(issues, "high", "media-manifest", f"잘못된 packaged media 기록입니다: {source_path}", "qa/build-report.json")
            continue
        try:
            path = _resolved_package_file(package_dir, item["package_path"])
        except ValueError as exc:
            _issue(issues, "high", "package-symlink", str(exc), item["package_path"])
            continue
        actual_sha256 = _sha256_file(path) if path.is_file() else ""
        if (
            not path.is_file()
            or item.get("sha256") != actual_sha256
            or item.get("bytes") != path.stat().st_size
            or declared_media.get(source_path) != actual_sha256
        ):
            _issue(issues, "high", "media-drift", f"패키지 매체가 빌드 후 변경되었습니다: {source_path}", item["package_path"])


def _resolved_package_file(package_dir: Path, relative: str) -> Path:
    raw = package_dir / relative
    if raw.is_symlink():
        raise ValueError(f"package file must not be a symbolic link: {relative}")
    resolved = raw.resolve()
    try:
        resolved.relative_to(package_dir.resolve())
    except ValueError as exc:
        raise ValueError(f"package file escapes package root: {relative}") from exc
    return resolved


def _check_required_file_safety(
    package_dir: Path,
    data: dict[str, Any],
    issues: list[Issue],
) -> None:
    for rel in sorted(_required_paths(data)):
        try:
            path = _resolved_package_file(package_dir, rel)
        except ValueError as exc:
            _issue(issues, "high", "package-symlink", str(exc), rel)
            continue
        if not path.is_file():
            _issue(issues, "high", "missing-output", f"필수 산출물이 없습니다: {rel}", rel)


def _check_static_content(package_dir: Path, issues: list[Issue]) -> None:
    css_path = package_dir / "assets" / "manual.css"
    if css_path.is_file() and not css_path.is_symlink():
        try:
            css = css_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            _issue(issues, "high", "css-read", f"CSS를 읽을 수 없습니다: {exc}", "assets/manual.css")
        else:
            if EXTERNAL_CSS_RE.search(css):
                _issue(
                    issues,
                    "high",
                    "external-css",
                    "외부 CSS import 또는 실행 가능한 URL을 허용하지 않습니다",
                    "assets/manual.css",
                )

    for rel in ("STATUS.md", "HANDOFF.md", "sources/evidence-map.md"):
        path = package_dir / rel
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            _issue(issues, "high", "markdown-read", f"Markdown을 읽을 수 없습니다: {exc}", rel)
            continue
        if ACTIVE_MARKDOWN_HTML_RE.search(text) or UNSAFE_MARKDOWN_LINK_RE.search(text):
            _issue(
                issues,
                "high",
                "markdown-active-content",
                "보조 Markdown에 실행 가능한 HTML 또는 링크가 있습니다",
                rel,
            )
        for match in PLACEHOLDER_RE.finditer(text):
            _issue(
                issues,
                "high",
                "placeholder-leak",
                f"보조 Markdown에 placeholder가 노출됩니다: {match.group(0)}",
                rel,
            )
        if TEMPLATE_TOKEN_RE.search(text):
            _issue(
                issues,
                "high",
                "template-token-leak",
                "보조 Markdown에 치환되지 않은 템플릿 변수가 있습니다",
                rel,
            )


def _safe_report_directory(package_dir: Path) -> Path:
    qa_dir = package_dir / "qa"
    if qa_dir.is_symlink():
        raise ValueError("qa report directory must not be a symbolic link")
    if qa_dir.exists() and not qa_dir.is_dir():
        raise ValueError("qa report path must be a directory")
    for name in ("verification.json", "verification.md"):
        path = qa_dir / name
        if path.is_symlink():
            raise ValueError(f"verification report must not be a symbolic link: {name}")
    qa_dir.mkdir(parents=True, exist_ok=True)
    try:
        qa_dir.resolve().relative_to(package_dir.resolve())
    except ValueError as exc:
        raise ValueError("qa report directory escapes package root") from exc
    return qa_dir


def _verification_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# 매뉴얼 검증 보고서",
        "",
        f"- 상태: **{report['summary']['status']}**",
        f"- 매뉴얼 상태: `{report['manual_status']}`",
        f"- 고위험 오류: {report['summary']['high_issues']}건",
        f"- 중간 위험 경고: {report['summary']['medium_issues']}건",
        f"- 기술 검증: `{report['checks']['technical']}`",
        f"- 내용·근거 검증: `{report['checks']['content']}`",
        f"- 시각·사용성 검증: `{report['checks']['visual']}`",
        "",
        "## 발견 사항",
        "",
    ]
    if report["issues"]:
        lines.extend(
            f"- [{item['severity']}] `{item['code']}` {item['message']} ({item['location']})"
            for item in report["issues"]
        )
    else:
        lines.append("- 없음")
    return "\n".join(lines) + "\n"


def verify(
    manifest_path: Path,
    package_dir: Path,
    visual_evidence: Path | None = None,
    visual_reviewed_claim: bool = False,
) -> dict[str, Any]:
    manifest_path = manifest_path.resolve()
    raw_package_dir = package_dir.absolute()
    if raw_package_dir.is_symlink():
        raise ValueError(f"manual package directory must not be a symbolic link: {raw_package_dir}")
    package_dir = package_dir.resolve()
    data = load_manual(manifest_path)
    issues = list(validate_source_contract(data, manifest_path.parent))

    if not package_dir.is_dir():
        raise ValueError(f"manual package directory not found: {package_dir}")
    _check_required_file_safety(package_dir, data, issues)
    _check_static_content(package_dir, issues)
    html_paths = sorted(
        path
        for path in package_dir.rglob("*.html")
        if path.is_file() and not path.is_symlink()
    )
    for path in html_paths:
        _scan_html(package_dir, path, issues)
    _check_lesson_depth(package_dir, data, issues)
    _check_status_truthfulness(package_dir, data, issues)
    _check_manifest_parity(package_dir, data, issues)
    _check_evidence_integrity(manifest_path, package_dir, data, issues)
    visual_status = _check_visual_evidence(
        package_dir,
        data,
        visual_evidence,
        visual_reviewed_claim,
        issues,
    )

    technical_codes = {
        "package-dir",
        "missing-output",
        "html-read",
        "html-structure",
        "html-title",
        "html-h1",
        "unsafe-link",
        "broken-link",
        "missing-alt",
        "packaged-manifest",
        "manifest-drift",
        "build-report-read",
        "source-manifest-drift",
        "evidence-manifest",
        "evidence-drift",
        "active-content",
        "external-link",
        "package-symlink",
        "media-manifest",
        "media-drift",
        "css-read",
        "external-css",
        "markdown-read",
        "markdown-active-content",
    }
    content_codes = {
        issue.code
        for issue in issues
        if issue.code not in technical_codes and not issue.code.startswith("visual-")
    }
    technical_failures = [
        issue for issue in issues if issue.code in technical_codes and issue.severity == "high"
    ]
    content_failures = [
        issue for issue in issues if issue.code in content_codes and issue.severity == "high"
    ]
    high_count = sum(issue.severity == "high" for issue in issues)
    medium_count = sum(issue.severity == "medium" for issue in issues)
    report = {
        "schema_version": 1,
        "manual_id": str(data.get("manual", {}).get("id") or ""),
        "manual_status": str(data.get("manual", {}).get("status") or ""),
        "summary": {
            "status": "pass" if high_count == 0 else "fail",
            "high_issues": high_count,
            "medium_issues": medium_count,
        },
        "checks": {
            "technical": "pass" if not technical_failures else "fail",
            "content": "pass" if not content_failures else "fail",
            "visual": visual_status,
        },
        "issues": [issue.to_dict() for issue in issues],
    }
    qa_dir = _safe_report_directory(package_dir)
    (qa_dir / "verification.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (qa_dir / "verification.md").write_text(
        _verification_markdown(report), encoding="utf-8"
    )
    return report


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--package-dir", type=Path, required=True)
    parser.add_argument(
        "--visual-evidence",
        type=Path,
        help="package-local visual-review.json with browser QA evidence",
    )
    parser.add_argument(
        "--visual-reviewed",
        action="store_true",
        help="deprecated claim flag; fails unless --visual-evidence is also provided",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        report = verify(
            args.manifest,
            args.package_dir,
            args.visual_evidence,
            args.visual_reviewed,
        )
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2
    print(
        "VERIFIED: "
        f"status={report['summary']['status']} "
        f"high={report['summary']['high_issues']} "
        f"medium={report['summary']['medium_issues']} "
        f"visual={report['checks']['visual']}"
    )
    return 0 if report["summary"]["status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
