#!/usr/bin/env python3
"""Build a deterministic, evidence-grounded static operator manual package."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
import shutil
import sys
from typing import Any

from manual_common import Issue, as_list, load_manual, resolve_local_path, validate_source_contract


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
TEMPLATE_PATH = SKILL_ROOT / "assets" / "manual-template.html"
CSS_PATH = SKILL_ROOT / "assets" / "manual.css"


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ul(items: list[Any], class_name: str = "") -> str:
    class_attr = f' class="{esc(class_name)}"' if class_name else ""
    return f"<ul{class_attr}>" + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ul>"


def section(title: str, body: str, section_id: str = "") -> str:
    id_attr = f' id="{esc(section_id)}"' if section_id else ""
    return f"<section{id_attr}><h2>{esc(title)}</h2>{body}</section>"


def render_shell(
    *,
    manual: dict[str, Any],
    page_title: str,
    description: str,
    content: str,
    depth: int,
) -> str:
    prefix = "../" * depth
    status = str(manual["status"])
    status_banner = ""
    if status != "final":
        status_banner = (
            '<div class="status-banner" role="status">'
            "검증 범위가 제한된 임시 매뉴얼입니다. STATUS와 HANDOFF의 미확인 범위를 확인하세요."
            "</div>"
        )
    replacements = {
        "{{LANG}}": esc(manual["language"]),
        "{{DESCRIPTION}}": esc(description),
        "{{PAGE_TITLE}}": esc(page_title),
        "{{CSS_PATH}}": prefix + "assets/manual.css",
        "{{STATUS}}": esc(status),
        "{{STATUS_BANNER}}": status_banner,
        "{{HOME_PATH}}": prefix + "index.html",
        "{{OVERVIEW_PATH}}": prefix + "overview.html",
        "{{MANUAL_TITLE}}": esc(manual["title"]),
        "{{CONTENT}}": content,
        "{{VERSION_BASIS}}": esc(
            f"판본 {manual['version']} · 기준 {manual['version_basis']}"
        ),
    }
    page = TEMPLATE_PATH.read_text(encoding="utf-8")
    for token, value in replacements.items():
        page = page.replace(token, value)
    return page


def render_index(data: dict[str, Any]) -> str:
    manual = data["manual"]
    lessons = {lesson["id"]: lesson for lesson in data["lessons"]}
    workflow_cards: list[str] = []
    for workflow in data["workflows"]:
        lesson_links = "".join(
            f'<li><a href="lessons/{esc(lesson_id)}.html">{esc(lessons[lesson_id]["title"])}</a></li>'
            for lesson_id in workflow["lessons"]
            if lesson_id in lessons
        )
        workflow_cards.append(
            '<article class="card workflow">'
            f'<p class="eyebrow">{esc(workflow["trigger"])}</p>'
            f'<h3>{esc(workflow["title"])}</h3>'
            f'<p>{esc(workflow["goal"])}</p>'
            f'<p><strong>완료 상태:</strong> {esc(workflow["outcome"])}</p>'
            f'<ol>{lesson_links}</ol>'
            "</article>"
        )
    content = (
        '<section class="hero">'
        '<p class="eyebrow">KLIC OPERATOR MANUAL</p>'
        f'<h1>{esc(manual["title"])}</h1>'
        f'<p class="lede">{esc(manual.get("subtitle") or manual["purpose"])}</p>'
        f'{ul(as_list(manual["audience"]), "meta-list")}'
        '<p><a class="lesson-link" href="overview.html">시스템 개요부터 읽기 →</a></p>'
        "</section>"
        + section("업무 흐름", '<div class="grid">' + "".join(workflow_cards) + "</div>")
        + section(
            "이 매뉴얼의 근거",
            f'<p>총 {len(data["sources"])}개 근거와 {len(data["lessons"])}개 lesson을 사용합니다. '
            '<a href="sources/evidence-map.md">근거 맵 보기</a></p>',
        )
    )
    return render_shell(
        manual=manual,
        page_title=manual["title"],
        description=manual["purpose"],
        content=content,
        depth=0,
    )


def render_overview(data: dict[str, Any]) -> str:
    manual = data["manual"]
    overview = data["overview"]
    role_cards = "".join(
        f'<article class="card"><h3>{esc(item["name"])}</h3><p>{esc(item["responsibility"])}</p></article>'
        for item in overview["roles"]
    )
    component_cards = "".join(
        f'<article class="card"><h3>{esc(item["name"])}</h3><p>{esc(item["purpose"])}</p></article>'
        for item in overview["components"]
    )
    confusion_cards = "".join(
        '<article class="card">'
        f'<h3>{esc(item["confusion"])}</h3>'
        f'<p><strong>바르게 이해하기:</strong> {esc(item["correction"])}</p>'
        "</article>"
        for item in overview["beginner_confusions"]
    )
    content = (
        '<section class="hero">'
        '<p class="eyebrow">SYSTEM OVERVIEW</p>'
        '<h1>시스템 개요</h1>'
        f'<p class="lede">{esc(overview["summary"])}</p>'
        f'<p><strong>한 줄 정신 모형:</strong> {esc(overview["mental_model"])}</p>'
        "</section>"
        + section("누가 무엇을 하는가", f'<div class="grid">{role_cards}</div>')
        + section("주요 구성요소", f'<div class="grid">{component_cards}</div>')
        + section("작업의 생명주기", ul(overview["lifecycle"], "lifecycle"))
        + section("처음에 자주 헷갈리는 점", f'<div class="grid">{confusion_cards}</div>')
        + '<p><a class="lesson-link" href="index.html">업무 흐름으로 이동 →</a></p>'
    )
    return render_shell(
        manual=manual,
        page_title=f"시스템 개요 · {manual['title']}",
        description=overview["summary"],
        content=content,
        depth=0,
    )


def render_media(
    lesson: dict[str, Any],
    media_map: dict[str, str],
) -> str:
    blocks: list[str] = []
    for item in as_list(lesson.get("media")):
        target = media_map[str(item["path"])]
        if item["type"] == "image":
            media_tag = f'<img src="../{esc(target)}" alt="{esc(item["alt"])}">'
        else:
            media_tag = (
                f'<video controls preload="metadata" aria-label="{esc(item["alt"])}">'
                f'<source src="../{esc(target)}"></video>'
            )
        blocks.append(
            f'<figure>{media_tag}<figcaption>{esc(item["alt"])}</figcaption></figure>'
        )
    return "".join(blocks)


def render_lesson(
    data: dict[str, Any],
    lesson: dict[str, Any],
    source_titles: dict[str, str],
    media_map: dict[str, str],
) -> str:
    manual = data["manual"]
    risk_class = " danger" if lesson["risk"] in {"high", "critical"} else ""
    steps: list[str] = []
    for step in lesson["steps"]:
        refs = ", ".join(str(ref) for ref in step["source_refs"])
        readback = ""
        if step["operation"] == "write":
            readback = (
                f'<p class="readback"><strong>변경 후 재확인:</strong> {esc(step["readback"])}</p>'
            )
        steps.append(
            '<li class="step">'
            f'<h3>{esc(step["title"])}</h3>'
            f'<p class="operation"><strong>작업 유형:</strong> {esc(step["operation"])}</p>'
            f'<p class="action"><strong>실행:</strong> {esc(step["action"])}</p>'
            f'<p class="evidence"><strong>화면·문서 증거:</strong> {esc(step["evidence"])}</p>'
            f'<p class="success"><strong>성공 판정:</strong> {esc(step["success"])}</p>'
            f'{readback}'
            f'<p><small>근거: {esc(refs)}</small></p>'
            "</li>"
        )
    source_items = "".join(
        f'<li><code>{esc(ref)}</code> — {esc(source_titles.get(str(ref), "알 수 없는 근거"))}</li>'
        for ref in lesson["source_refs"]
    )
    content = (
        '<section class="hero">'
        f'<p class="eyebrow">LESSON · {esc(lesson["id"])}</p>'
        f'<h1>{esc(lesson["title"])}</h1>'
        f'<p class="lede">{esc(lesson["purpose"])}</p>'
        f'{ul(as_list(lesson["audience"]), "meta-list")}'
        "</section>"
        + section("이 작업의 목적", f'<p>{esc(lesson["purpose"])}</p>')
        + section("언제 사용하는가", f'<p>{esc(lesson["when_to_use"])}</p>')
        + section("시작 전 준비", ul(lesson["prerequisites"]))
        + section(
            "안전 경계",
            f'<div class="warning{risk_class}"><p><strong>위험도:</strong> {esc(lesson["risk"])}</p>'
            f'<p><strong>승인 필요:</strong> {"예" if lesson["approval_required"] else "아니오"}</p>'
            f'<p><strong>실행 환경:</strong> {esc(lesson["fixture"])}</p></div>',
        )
        + section("실행 단계", f'<ol class="step-list">{"".join(steps)}</ol>')
        + section("화면·매체 증거", render_media(lesson, media_map))
        + section("주의할 점", ul(lesson["cautions"]))
        + section("흔한 실수", ul(lesson["common_mistakes"]))
        + section("완료 확인", ul(lesson["completion_checks"]))
        + section("근거", f'<ul class="source-list">{source_items}</ul>')
        + section("다음 분기", f'<p>{esc(lesson["next"])}</p>')
        + '<p><a class="lesson-link" href="../index.html">전체 업무 흐름으로 돌아가기 →</a></p>'
    )
    return render_shell(
        manual=manual,
        page_title=f"{lesson['title']} · {manual['title']}",
        description=lesson["purpose"],
        content=content,
        depth=1,
    )


def evidence_map(data: dict[str, Any]) -> str:
    lines = [
        "# 근거 맵",
        "",
        "| ID | 등급 | 제목 | 경로 | 확인일 | 사용 lesson |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    source_to_lessons: dict[str, list[str]] = {source["id"]: [] for source in data["sources"]}
    for lesson in data["lessons"]:
        refs = set(str(ref) for ref in lesson["source_refs"])
        for step in lesson["steps"]:
            refs.update(str(ref) for ref in step["source_refs"])
        for ref in refs:
            if ref in source_to_lessons:
                source_to_lessons[ref].append(lesson["id"])
    def md_cell(value: Any) -> str:
        text = html.escape(str(value), quote=False)
        for raw, escaped in (
            ("\\", "\\\\"),
            ("|", "\\|"),
            ("[", "\\["),
            ("]", "\\]"),
            ("(", "\\("),
            (")", "\\)"),
        ):
            text = text.replace(raw, escaped)
        return text.replace("\r", " ").replace("\n", " ")

    for source in data["sources"]:
        lessons = ", ".join(sorted(source_to_lessons[source["id"]])) or "미사용"
        lines.append(
            f"| {md_cell(source['id'])} | {md_cell(source['evidence_type'])} | "
            f"{md_cell(source['title'])} | `{md_cell(source['path'])}` | "
            f"{md_cell(source['checked_at'])} | {md_cell(lessons)} |"
        )
    return "\n".join(lines) + "\n"


def status_markdown(data: dict[str, Any]) -> str:
    manual = data["manual"]
    unchecked = []
    if manual["status"] != "final":
        unchecked.append("브라우저 시각·사용성 검수를 완료하기 전까지 임시 배포 상태로 유지한다.")
    lines = [
        "# STATUS",
        "",
        f"- manual: `{manual['id']}`",
        f"- status: `{manual['status']}`",
        f"- version: `{manual['version']}`",
        f"- version basis: {manual['version_basis']}",
        f"- workflows: {len(data['workflows'])}",
        f"- lessons: {len(data['lessons'])}",
        f"- sources: {len(data['sources'])}",
        "",
        "## 자동 검증과 별도인 항목",
        "",
    ]
    lines.extend(f"- {item}" for item in (unchecked or ["브라우저 시각 검수 결과를 HANDOFF에 기록한다."]))
    return "\n".join(lines) + "\n"


def handoff_markdown(data: dict[str, Any]) -> str:
    manual = data["manual"]
    return "\n".join(
        [
            "# HANDOFF",
            "",
            f"## {manual['title']}",
            "",
            f"- 판본: `{manual['version']}`",
            f"- 기준: {manual['version_basis']}",
            f"- 상태: `{manual['status']}`",
            "- 시작 페이지: `index.html`",
            "- 시스템 개요: `overview.html`",
            "- 근거 맵: `sources/evidence-map.md`",
            "- 자동 검증: `qa/verification.json` 생성 후 확인",
            "",
            "## 완료 주장 경계",
            "",
            "- 자동 링크·스키마 검증과 브라우저 시각·사용성 검증을 분리해 보고한다.",
            "- 실제 화면 또는 런타임을 확인하지 않은 절차는 최종 동작으로 단정하지 않는다.",
            "- 고위험 절차는 승인된 안전 환경과 식별 가능한 테스트 데이터에서만 실행한다.",
            "",
        ]
    )


def copy_media(data: dict[str, Any], root: Path, out: Path) -> dict[str, str]:
    mapping: dict[str, str] = {}
    used_names: dict[str, str] = {}
    for lesson in data["lessons"]:
        for item in as_list(lesson.get("media")):
            rel = str(item["path"])
            source = resolve_local_path(root, rel)
            name = source.name
            if name in used_names and used_names[name] != sha256_file(source):
                name = f"{hashlib.sha256(rel.encode('utf-8')).hexdigest()[:10]}-{name}"
            used_names[name] = sha256_file(source)
            target = out / "media" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
            mapping[rel] = f"media/{name}"
    return mapping


def validate_output_directory(manifest_path: Path, output_dir: Path) -> None:
    """Reject broad or non-empty output paths; the builder never deletes user data."""
    current = output_dir
    while current.parent != current:
        if current.is_symlink():
            raise ValueError(f"output path contains a symbolic link component: {current}")
        current = current.parent
    if output_dir.parent == output_dir:
        raise ValueError("output directory cannot be a filesystem root")
    protected = {
        manifest_path: "contains the manifest",
        Path(__file__).resolve(): "contains the manual builder",
        TEMPLATE_PATH.resolve(): "contains the manual template",
        CSS_PATH.resolve(): "contains the manual stylesheet",
    }
    for path, reason in protected.items():
        try:
            path.relative_to(output_dir)
        except ValueError:
            continue
        raise ValueError(f"unsafe output directory: {reason}: {output_dir}")
    if output_dir.exists():
        if not output_dir.is_dir():
            raise ValueError(f"output path is not a directory: {output_dir}")
        if any(output_dir.iterdir()):
            raise ValueError(f"output directory must be empty: {output_dir}")


def build(manifest_path: Path, output_dir: Path) -> dict[str, Any]:
    manifest_path = manifest_path.resolve()
    raw_output_dir = output_dir.absolute()
    validate_output_directory(manifest_path, raw_output_dir)
    output_dir = raw_output_dir.resolve()
    root = manifest_path.parent
    data = load_manual(manifest_path)
    issues = validate_source_contract(data, root)
    high = [issue for issue in issues if issue.severity == "high"]
    if high:
        raise ManualBuildError(issues)

    for directory in ["assets", "lessons", "media", "sources", "qa"]:
        (output_dir / directory).mkdir(parents=True, exist_ok=True)

    shutil.copyfile(CSS_PATH, output_dir / "assets" / "manual.css")
    media_map = copy_media(data, root, output_dir)
    packaged_media = {
        source_rel: {
            "package_path": package_rel,
            "sha256": sha256_file(output_dir / package_rel),
            "bytes": (output_dir / package_rel).stat().st_size,
        }
        for source_rel, package_rel in sorted(media_map.items())
    }
    source_titles = {source["id"]: source["title"] for source in data["sources"]}
    (output_dir / "index.html").write_text(render_index(data), encoding="utf-8")
    (output_dir / "overview.html").write_text(render_overview(data), encoding="utf-8")
    for lesson in data["lessons"]:
        (output_dir / "lessons" / f"{lesson['id']}.html").write_text(
            render_lesson(data, lesson, source_titles, media_map),
            encoding="utf-8",
        )
    (output_dir / "sources" / "evidence-map.md").write_text(
        evidence_map(data), encoding="utf-8"
    )
    normalized = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    (output_dir / "manual-manifest.json").write_text(normalized, encoding="utf-8")
    (output_dir / "STATUS.md").write_text(status_markdown(data), encoding="utf-8")
    (output_dir / "HANDOFF.md").write_text(handoff_markdown(data), encoding="utf-8")

    evidence_files = {
        str(source["id"]): {
            "path": str(source["path"]),
            "sha256": sha256_file(resolve_local_path(root, str(source["path"]))),
            "bytes": resolve_local_path(root, str(source["path"])).stat().st_size,
            "evidence_type": str(source["evidence_type"]),
        }
        for source in data["sources"]
    }
    report = {
        "schema_version": 1,
        "manual_id": data["manual"]["id"],
        "manual_status": data["manual"]["status"],
        "counts": {
            "workflows": len(data["workflows"]),
            "lessons": len(data["lessons"]),
            "sources": len(data["sources"]),
            "media": len(media_map),
        },
        "source_manifest_sha256": sha256_file(manifest_path),
        "evidence_files": evidence_files,
        "packaged_media": packaged_media,
        "issues": [issue.to_dict() for issue in issues],
    }
    (output_dir / "qa" / "build-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return report


class ManualBuildError(RuntimeError):
    def __init__(self, issues: list[Issue]):
        super().__init__("manual source contract failed")
        self.issues = issues


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        report = build(args.manifest, args.output_dir)
    except (ManualBuildError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        for issue in getattr(exc, "issues", []):
            print(f"- [{issue.severity}] {issue.message}", file=sys.stderr)
        return 2
    print(
        "BUILT: "
        f"workflows={report['counts']['workflows']} "
        f"lessons={report['counts']['lessons']} "
        f"sources={report['counts']['sources']} "
        f"status={report['manual_status']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
