#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml


SOURCE_ID_RE = re.compile(r"\bSRC-\d{3}\b")
CHAPTER_RE = re.compile(r"^(0[1-9]|1[0-2])[-_].*\.md$")
PROHIBITED_IMPLEMENTATION_RE = re.compile(
    r"FactoryX는\s+(?:내부적으로\s+)?(?:Kubernetes\s+)?"
    r"(DRA|Kueue|MIG|Slurm)(?:을|를)\s*(사용|채택|구현)(?:한다|했다|하고)",
    re.IGNORECASE,
)
PENDING_MARKERS = ("제작 예정", "figure-pending")


def _yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def collect_project(root: Path) -> dict[str, object]:
    manuscript_dir = root / "manuscript"
    figure_dir = root / "assets" / "figures"
    chart_dir = root / "assets" / "charts"
    chapter_paths = sorted(
        path for path in manuscript_dir.glob("*.md") if CHAPTER_RE.match(path.name)
    ) if manuscript_dir.exists() else []
    manuscript_paths = sorted(manuscript_dir.glob("*.md")) if manuscript_dir.exists() else []
    source_data = _yaml(root / "research" / "source-register.yaml")
    source_ids = {
        str(item.get("id"))
        for item in source_data.get("sources", [])
        if isinstance(item, dict) and item.get("id")
    }
    build_report_path = root / "build" / "build_report.json"
    page_count = None
    if build_report_path.exists():
        try:
            report = json.loads(build_report_path.read_text(encoding="utf-8"))
            page_count = report.get("output", {}).get("pages")
        except (json.JSONDecodeError, AttributeError):
            page_count = "invalid"
    return {
        "chapter_paths": chapter_paths,
        "manuscript_paths": manuscript_paths,
        "figure_paths": sorted(figure_dir.glob("*.svg")) if figure_dir.exists() else [],
        "chart_paths": sorted(chart_dir.glob("*.svg")) if chart_dir.exists() else [],
        "source_ids": source_ids,
        "page_count": page_count,
        "build_report_exists": build_report_path.exists(),
    }


def validate_project(root: Path, require_build: bool = False) -> list[str]:
    project = collect_project(root)
    errors: list[str] = []

    chapter_paths = project["chapter_paths"]
    if len(chapter_paths) != 12:
        errors.append(f"장 본문은 12개여야 합니다: {len(chapter_paths)}개")

    source_ids = project["source_ids"]
    used_source_ids: set[str] = set()
    for path in project["manuscript_paths"]:
        text = path.read_text(encoding="utf-8")
        used_source_ids.update(SOURCE_ID_RE.findall(text))
        match = PROHIBITED_IMPLEMENTATION_RE.search(text)
        if match:
            sentence = text[match.start():].splitlines()[0].strip()
            errors.append(f"FactoryX 내부 구현으로 단정한 금지 문장: {path.name}: {sentence}")
        if any(marker in text for marker in PENDING_MARKERS):
            errors.append(f"제작 대기 자리표시자가 남아 있습니다: {path.name}")
    for source_id in sorted(used_source_ids - source_ids):
        errors.append(f"등록되지 않은 출처 ID: {source_id}")

    figure_paths = project["figure_paths"]
    chart_paths = project["chart_paths"]
    if len(figure_paths) < 12:
        errors.append(f"기술 도형은 12개 이상이어야 합니다: {len(figure_paths)}개")
    if len(chart_paths) < 8:
        errors.append(f"데이터 차트는 8개 이상이어야 합니다: {len(chart_paths)}개")

    if require_build:
        if not project["build_report_exists"]:
            errors.append("build/build_report.json이 없습니다.")
        elif project["page_count"] != 100:
            errors.append(f"최종 PDF 페이지 수는 100이어야 합니다: {project['page_count']}쪽")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="FactoryX 책의 출판 계약을 검증합니다.")
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--require-build", action="store_true")
    args = parser.parse_args(argv)

    errors = validate_project(args.root.resolve(), require_build=args.require_build)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    project = collect_project(args.root.resolve())
    print(
        "VALID: "
        f"chapters={len(project['chapter_paths'])} "
        f"figures={len(project['figure_paths'])} "
        f"charts={len(project['chart_paths'])} "
        f"sources={len(project['source_ids'])} "
        f"pages={project['page_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
