from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from validate_book import validate_project  # noqa: E402


def make_project(tmp_path: Path) -> Path:
    root = tmp_path / "book"
    manuscript = root / "manuscript"
    figures = root / "assets" / "figures"
    charts = root / "assets" / "charts"
    research = root / "research"
    build = root / "build"
    for path in (manuscript, figures, charts, research, build):
        path.mkdir(parents=True, exist_ok=True)

    for number in range(1, 13):
        (manuscript / f"{number:02d}-chapter.md").write_text(
            f"# {number}장 테스트\n\n[원자료] 검증 문장 (SRC-001)\n",
            encoding="utf-8",
        )
    for number in range(1, 13):
        (figures / f"FIG-{number:03d}.svg").write_text("<svg/>", encoding="utf-8")
    for number in range(1, 9):
        (charts / f"CHT-{number:03d}.svg").write_text("<svg/>", encoding="utf-8")

    (research / "source-register.yaml").write_text(
        yaml.safe_dump(
            {"sources": [{"id": "SRC-001", "url": "https://example.com"}]},
            allow_unicode=True,
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    (research / "claim-register.yaml").write_text(
        yaml.safe_dump({"claims": []}, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    (build / "build_report.json").write_text(
        json.dumps({"output": {"pages": 100}}, ensure_ascii=False),
        encoding="utf-8",
    )
    return root


def test_requires_twelve_chapters(tmp_path: Path) -> None:
    root = make_project(tmp_path)
    (root / "manuscript" / "12-chapter.md").unlink()

    errors = validate_project(root)

    assert "장 본문은 12개여야 합니다: 11개" in errors


def test_requires_source_ids_to_exist(tmp_path: Path) -> None:
    root = make_project(tmp_path)
    chapter = root / "manuscript" / "01-chapter.md"
    chapter.write_text(chapter.read_text(encoding="utf-8") + "미등록 근거 SRC-999\n", encoding="utf-8")

    errors = validate_project(root)

    assert "등록되지 않은 출처 ID: SRC-999" in errors


def test_rejects_factoryx_internal_implementation_claims(tmp_path: Path) -> None:
    root = make_project(tmp_path)
    chapter = root / "manuscript" / "07-chapter.md"
    chapter.write_text("# 7장\n\nFactoryX는 DRA를 사용한다.\n", encoding="utf-8")

    errors = validate_project(root)

    assert any(error.startswith("FactoryX 내부 구현으로 단정한 금지 문장:") for error in errors)


def test_requires_twelve_figures_and_eight_charts(tmp_path: Path) -> None:
    root = make_project(tmp_path)
    (root / "assets" / "figures" / "FIG-012.svg").unlink()
    (root / "assets" / "charts" / "CHT-008.svg").unlink()

    errors = validate_project(root)

    assert "기술 도형은 12개 이상이어야 합니다: 11개" in errors
    assert "데이터 차트는 8개 이상이어야 합니다: 7개" in errors


def test_rejects_pending_figure_markers(tmp_path: Path) -> None:
    root = make_project(tmp_path)
    chapter = root / "manuscript" / "03-chapter.md"
    chapter.write_text("# 3장\n\n> 제작 예정: 냉각 도형\n", encoding="utf-8")

    errors = validate_project(root)

    assert "제작 대기 자리표시자가 남아 있습니다: 03-chapter.md" in errors


def test_requires_exactly_one_hundred_pages_when_build_exists(tmp_path: Path) -> None:
    root = make_project(tmp_path)
    report = root / "build" / "build_report.json"
    report.write_text(json.dumps({"output": {"pages": 99}}), encoding="utf-8")

    errors = validate_project(root, require_build=True)

    assert "최종 PDF 페이지 수는 100이어야 합니다: 99쪽" in errors
