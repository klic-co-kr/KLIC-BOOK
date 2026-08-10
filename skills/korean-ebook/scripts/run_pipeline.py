#!/usr/bin/env python3
"""Run build -> verify -> render -> contact sheet -> package in one command."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Iterable


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
DEFAULT_CONFIG = SKILL_ROOT / "assets" / "book-config.example.yaml"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(cmd: list[str], allow_nonzero: bool = False) -> int:
    print("+", " ".join(f'"{x}"' if " " in x else x for x in cmd), flush=True)
    proc = subprocess.run(cmd, check=False)
    if proc.returncode != 0 and not allow_nonzero:
        raise RuntimeError(f"Command failed with exit code {proc.returncode}: {cmd[1] if len(cmd) > 1 else cmd[0]}")
    return proc.returncode


def zip_paths(base: Path, paths: Iterable[Path], target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(set(p.resolve() for p in paths)):
            if not path.exists() or not path.is_file():
                continue
            zf.write(path, arcname=path.relative_to(base).as_posix())


def completion_markdown(
    status: str,
    build: dict,
    verification: dict | None,
    outputs: list[Path],
    unchecked: list[str],
) -> str:
    pdf = Path(build["output"]["pdf"])
    lines = [
        "# 완료 보고",
        "",
        "## Goal — 원고 편집 PDF 제작",
        "",
        f"- 상태: **{status}**",
        f"- PDF: `{pdf.name}`",
        f"- 페이지 수: {build['output'].get('pages', 'unknown')}",
        f"- 목차 레이아웃: {build['output'].get('toc_layout', 'unknown')}",
        f"- 시각 요약 페이지: {build['output'].get('visual_summary_pages', 0)}",
        f"- 북마크 상위 항목: {build['output'].get('outline_top_level_count', 'unknown')}",
        f"- 전체 북마크: {build['output'].get('outline_item_count', 'unknown')}",
        f"- 링크·주석: {build['output'].get('annotations', 'unknown')}",
        f"- PDF SHA-256: `{build['output'].get('pdf_sha256', '')}`",
        "",
        "## 입력 경계",
        "",
        f"- CONTENT 파일: {build['input'].get('content_file_count', 0)}개",
        f"- REFERENCE 파일: {build['input'].get('reference_file_count', 0)}개",
        "- 참고자료 본문 유입: 없음(빌드 스크립트 정책)",
        "",
    ]
    if verification:
        lines.extend(
            [
                "## 무결성 검수",
                "",
                f"- 자동 검수 상태: {verification['summary']['status']}",
                f"- 고위험 오류: {verification['summary']['high_issues']}건",
                f"- 중간 위험 경고: {verification['summary']['medium_issues']}건",
                f"- 누락 문단 표본: {verification['integrity']['missing_probe_count']}건 / {verification['integrity']['probe_count']}건",
                f"- 누락 제목: {verification['integrity']['missing_heading_count']}건",
                f"- 참고자료 오염 후보: {verification['reference_isolation']['match_count']}건",
                f"- 비-A4 페이지: {len(verification['structure']['non_a4_pages'])}건",
                f"- 빈 페이지 후보: {len(verification['structure']['blank_page_candidates'])}건",
                "",
            ]
        )
    lines.extend(["## 산출물", ""])
    for output in outputs:
        lines.append(f"- `{output.name}` — SHA-256 `{sha256_file(output)}`")
    if unchecked:
        lines.extend(["", "## 확인하지 못한 범위", ""])
        lines.extend(f"- {item}" for item in unchecked)
    else:
        lines.extend(
            [
                "",
                "## 수동 확인 필요",
                "",
                "- 접촉표와 개별 렌더 페이지를 열어 잘림·겹침·표 오류를 최종 확인해야 합니다. 자동 검사는 이를 대체하지 않습니다.",
            ]
        )
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--reference", type=Path, action="append", default=[])
    parser.add_argument("--dpi", type=int, default=160)
    parser.add_argument("--skip-render", action="store_true")
    parser.add_argument("--include-renders", action="store_true")
    parser.add_argument("--keep-workdir", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    python = sys.executable

    publish_cmd = [
        python,
        str(SCRIPT_DIR / "publish_book.py"),
        "--input",
        str(args.input.resolve()),
        "--output-dir",
        str(out),
        "--config",
        str(args.config.resolve()),
    ]
    for ref in args.reference:
        publish_cmd.extend(["--reference", str(ref.resolve())])
    if args.keep_workdir:
        publish_cmd.append("--keep-workdir")
    try:
        run(publish_cmd)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    build_path = out / "build_report.json"
    manifest_path = out / "source_manifest.json"
    build = json.loads(build_path.read_text(encoding="utf-8"))
    pdf = Path(build["output"]["pdf"])

    verification_dir = out / "verification"
    verify_cmd = [
        python,
        str(SCRIPT_DIR / "verify_pdf.py"),
        "--pdf",
        str(pdf),
        "--source-manifest",
        str(manifest_path),
        "--report-dir",
        str(verification_dir),
    ]
    for ref in args.reference:
        verify_cmd.extend(["--reference", str(ref.resolve())])
    verify_code = run(verify_cmd, allow_nonzero=True)
    verification_path = verification_dir / "verification.json"
    verification = json.loads(verification_path.read_text(encoding="utf-8")) if verification_path.exists() else None

    contact_outputs: list[Path] = []
    unchecked: list[str] = []
    if not args.skip_render:
        rendered = out / "rendered"
        render_code = run(
            [
                python,
                str(SCRIPT_DIR / "render_pdf.py"),
                "--pdf",
                str(pdf),
                "--out-dir",
                str(rendered),
                "--dpi",
                str(args.dpi),
            ],
            allow_nonzero=True,
        )
        if render_code == 0:
            contact_base = out / "contact-sheet.jpg"
            contact_code = run(
                [
                    python,
                    str(SCRIPT_DIR / "make_contact_sheet.py"),
                    "--input-dir",
                    str(rendered),
                    "--output",
                    str(contact_base),
                ],
                allow_nonzero=True,
            )
            if contact_code == 0:
                contact_outputs = sorted(out.glob("contact-sheet*.jpg"))
            else:
                unchecked.append("접촉표 생성에 실패했습니다.")
        else:
            unchecked.append("PDF 전 페이지 렌더링에 실패했습니다.")
    else:
        unchecked.append("--skip-render 옵션으로 시각 렌더링을 생략했습니다.")

    if verification and verification["summary"]["status"] == "pass" and not unchecked:
        status = "자동 검수 통과 — 수동 시각 확인 필요"
    elif verification and verification["summary"]["status"] == "fail":
        status = "실패"
    else:
        status = "조건부 완료"

    report_outputs = [pdf, build_path, manifest_path]
    if verification_path.exists():
        report_outputs.extend([verification_path, verification_dir / "verification.md"])
    report_outputs.extend(contact_outputs)

    completion_path = out / "completion_report.md"
    completion_path.write_text(
        completion_markdown(status, build, verification, [p for p in report_outputs if p.exists()], unchecked),
        encoding="utf-8",
    )
    report_outputs.append(completion_path)

    sha_path = out / f"{pdf.name}.sha256"
    sha_path.write_text(f"{sha256_file(pdf)}  {pdf.name}\n", encoding="utf-8")
    report_outputs.append(sha_path)

    package_path = out / f"{pdf.stem}_패키지.zip"
    package_files = list(report_outputs) + [out / "book.html"]
    if args.include_renders:
        package_files.extend((out / "rendered").glob("page-*.png"))
    zip_paths(out, package_files, package_path)
    package_sha = out / f"{package_path.name}.sha256"
    package_sha.write_text(f"{sha256_file(package_path)}  {package_path.name}\n", encoding="utf-8")

    print(f"Completion report: {completion_path}")
    print(f"Package: {package_path}")
    print(f"Package SHA-256: {sha256_file(package_path)}")
    if verify_code == 2:
        return 2
    return 0 if verify_code == 0 and not unchecked else 1


if __name__ == "__main__":
    raise SystemExit(main())
