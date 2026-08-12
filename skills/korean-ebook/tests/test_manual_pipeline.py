from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import yaml


SKILL_ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = SKILL_ROOT / "scripts" / "build_manual.py"
VERIFY_SCRIPT = SKILL_ROOT / "scripts" / "verify_manual.py"
VALIDATE_SKILL_SCRIPT = SKILL_ROOT / "scripts" / "validate_skill.py"
SHIPPED_MANUAL = SKILL_ROOT / "examples" / "minimal-manual" / "manual.yaml"
IGNORED_PACKAGE_DIRS = {"__pycache__", ".pytest_cache", ".venv"}


def _write_fixture(tmp_path: Path, *, status: str = "provisional", unsafe: bool = False) -> Path:
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    (source_dir / "operator-guide.md").write_text(
        "# 운영 근거\n\n요청을 검토하고 승인 상태를 확인한다.\n",
        encoding="utf-8",
    )
    media_dir = tmp_path / "evidence"
    media_dir.mkdir()
    (media_dir / "request-list.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="360">'
        '<rect width="640" height="360" fill="#f3efe5"/>'
        '<text x="40" y="80">요청 목록 · 상태: 검토 대기</text></svg>',
        encoding="utf-8",
    )
    source_sha = hashlib.sha256((source_dir / "operator-guide.md").read_bytes()).hexdigest()
    media_sha = hashlib.sha256((media_dir / "request-list.svg").read_bytes()).hexdigest()

    manifest = {
        "schema_version": 1,
        "manual": {
            "id": "sample-operations",
            "title": "샘플 운영 매뉴얼",
            "subtitle": "요청 검토와 완료 확인",
            "language": "ko",
            "audience": ["신규 운영 담당자"],
            "status": status,
            "version": "1.0",
            "version_basis": "operator-guide.md 확인본",
            "purpose": "신규 담당자가 요청을 안전하게 검토하고 완료 상태를 확인하도록 돕는다.",
        },
        "overview": {
            "summary": "요청이 접수되어 검토와 승인 확인을 거쳐 완료되는 운영 흐름이다.",
            "mental_model": "요청 한 건을 바통처럼 다음 담당자에게 넘기는 과정으로 이해한다.",
            "roles": [
                {"name": "요청자", "responsibility": "필요한 정보를 제출한다."},
                {"name": "운영 담당자", "responsibility": "근거와 상태를 검토한다."},
            ],
            "components": [
                {"name": "요청 목록", "purpose": "처리할 작업과 현재 상태를 보여준다."},
                {"name": "상세 화면", "purpose": "입력값과 승인 근거를 확인한다."},
            ],
            "lifecycle": ["접수", "검토", "승인 확인", "완료"],
            "beginner_confusions": [
                {
                    "confusion": "목록에 보이면 처리가 끝난 것으로 생각한다.",
                    "correction": "상세 화면의 완료 상태와 확인 기록까지 읽어야 한다.",
                }
            ],
        },
        "workflows": [
            {
                "id": "request-to-complete",
                "title": "요청 접수부터 완료 확인",
                "goal": "누락 없이 요청을 검토하고 완료 근거를 남긴다.",
                "trigger": "새 요청이 검토 대기 상태로 들어온다.",
                "outcome": "완료 상태와 확인 기록이 함께 남는다.",
                "lessons": ["review-request"],
            }
        ],
        "lessons": [
            {
                "id": "review-request",
                "title": "요청 검토하기",
                "purpose": "요청 내용과 승인 상태를 확인한다.",
                "audience": ["신규 운영 담당자"],
                "when_to_use": "검토 대기 요청을 처음 맡았을 때",
                "prerequisites": ["요청 목록 읽기 권한", "요청 번호"],
                "source_refs": ["SRC-001", "UI-001"],
                "risk": "high" if unsafe else "low",
                "approval_required": False,
                "fixture": "missing" if unsafe else "not_required",
                "steps": [
                    {
                        "title": "검토 대기 요청 찾기",
                        "operation": "read",
                        "action": "요청 목록에서 상태가 ‘검토 대기’인 요청 번호를 연다.",
                        "evidence": "목록과 상세 화면의 요청 번호가 같고 상태가 ‘검토 대기’로 보인다.",
                        "success": "요청자, 요청 내용, 상태를 한 화면에서 확인했다.",
                        "source_refs": ["SRC-001", "UI-001"],
                    },
                    {
                        "title": "완료 근거 읽기",
                        "operation": "read",
                        "action": "필수 입력과 승인 기록을 읽고 누락 여부를 확인한다.",
                        "evidence": "필수 입력이 채워져 있고 승인 기록에 담당자와 상태가 보인다.",
                        "success": "누락 항목이 없고 다음 처리 가능 여부를 설명할 수 있다.",
                        "source_refs": ["SRC-001"],
                    },
                ],
                "cautions": ["상태를 확인하지 않은 채 완료로 간주하지 않는다."],
                "common_mistakes": ["목록의 첫 행을 현재 요청으로 오인한다."],
                "completion_checks": ["요청 번호가 일치한다.", "완료 상태와 확인 기록을 읽었다."],
                "next": "누락이 있으면 요청자에게 보완을 요청하고, 없으면 후속 처리로 이동한다.",
                "media": [
                    {
                        "type": "image",
                        "path": "evidence/request-list.svg",
                        "sha256": media_sha,
                        "alt": "검토 대기 상태가 표시된 요청 목록 예시",
                        "source_refs": ["UI-001"],
                    }
                ],
            }
        ],
        "sources": [
            {
                "id": "SRC-001",
                "title": "운영 가이드",
                "evidence_type": "source",
                "path": "source/operator-guide.md",
                "checked_at": "2026-08-12",
                "sha256": source_sha,
            },
            {
                "id": "UI-001",
                "title": "요청 목록 화면",
                "evidence_type": "ui",
                "path": "evidence/request-list.svg",
                "checked_at": "2026-08-12",
                "sha256": media_sha,
            },
        ],
    }
    path = tmp_path / "manual.yaml"
    path.write_text(yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return path


def _run(script: Path, *args: str) -> subprocess.CompletedProcess[str]:
    assert script.exists(), f"매뉴얼 파이프라인 스크립트가 없습니다: {script.name}"
    return subprocess.run(
        [sys.executable, str(script), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def _tree_digest(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _package_files() -> set[str]:
    return {
        path.relative_to(SKILL_ROOT).as_posix()
        for path in SKILL_ROOT.rglob("*")
        if path.is_file() and not any(part in IGNORED_PACKAGE_DIRS for part in path.parts)
    }


def test_skill_routes_manual_requests_to_a_separate_pipeline():
    text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")

    assert "산출물 형식 게이트" in text
    assert "build_manual.py" in text
    assert "verify_manual.py" in text
    assert "manual.yaml" in text
    assert "manual-verification" not in text
    assert "Hermes" not in text


def test_skill_metadata_and_contracts_expose_manual_mode():
    agent = yaml.safe_load((SKILL_ROOT / "agents/openai.yaml").read_text(encoding="utf-8"))
    trigger_cases = json.loads(
        (SKILL_ROOT / "evals/trigger_cases.json").read_text(encoding="utf-8")
    )
    input_contract = (SKILL_ROOT / "references/input-contract.md").read_text(
        encoding="utf-8"
    )
    output_contract = (SKILL_ROOT / "references/output-contract.md").read_text(
        encoding="utf-8"
    )

    assert "책·매뉴얼" in agent["interface"]["display_name"]
    assert "산출물 형식" in agent["interface"]["default_prompt"]
    assert any("운영 매뉴얼" in prompt for prompt in trigger_cases["positive"])
    assert any("랜딩페이지" in prompt for prompt in trigger_cases["negative"])
    assert "EVIDENCE" in input_contract
    assert "manual.yaml" in input_contract
    assert "index.html" in output_contract
    assert "manual-manifest.json" in output_contract
    assert "book 모드" in output_contract.casefold()
    assert "manual 모드" in output_contract.casefold()


def test_distribution_manifest_and_checksums_cover_the_skill_package():
    packaged = {
        line.strip()
        for line in (SKILL_ROOT / "manifest.txt").read_text(encoding="utf-8").splitlines()
        if line.strip()
    }
    assert packaged == _package_files()

    checksum_lines = [
        line
        for line in (SKILL_ROOT / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    checksums = dict(line.split("  ", 1) for line in checksum_lines)
    assert set(checksums.values()) == packaged - {"SHA256SUMS"}
    for expected, relative in checksums.items():
        assert hashlib.sha256((SKILL_ROOT / relative).read_bytes()).hexdigest() == expected


def test_builds_and_verifies_a_complete_provisional_manual(tmp_path: Path):
    manifest = _write_fixture(tmp_path)
    out = tmp_path / "out"

    built = _run(BUILD_SCRIPT, "--manifest", str(manifest), "--output-dir", str(out))
    assert built.returncode == 0, built.stderr or built.stdout

    expected = {
        "index.html",
        "overview.html",
        "lessons/review-request.html",
        "assets/manual.css",
        "media/request-list.svg",
        "sources/evidence-map.md",
        "qa/build-report.json",
        "manual-manifest.json",
        "STATUS.md",
        "HANDOFF.md",
    }
    assert expected <= {p.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file()}

    lesson = (out / "lessons/review-request.html").read_text(encoding="utf-8")
    for heading in [
        "이 작업의 목적",
        "언제 사용하는가",
        "시작 전 준비",
        "실행 단계",
        "주의할 점",
        "흔한 실수",
        "완료 확인",
        "근거",
        "다음 분기",
    ]:
        assert heading in lesson

    verified = _run(VERIFY_SCRIPT, "--manifest", str(manifest), "--package-dir", str(out))
    assert verified.returncode == 0, verified.stderr or verified.stdout
    report = json.loads((out / "qa/verification.json").read_text(encoding="utf-8"))
    assert report["summary"]["status"] == "pass"
    assert report["manual_status"] == "provisional"
    assert report["checks"]["technical"] == "pass"
    assert report["checks"]["content"] == "pass"
    assert report["checks"]["visual"] == "not_run"


def test_manual_build_is_deterministic(tmp_path: Path):
    manifest = _write_fixture(tmp_path)
    first = tmp_path / "first"
    second = tmp_path / "second"

    assert _run(BUILD_SCRIPT, "--manifest", str(manifest), "--output-dir", str(first)).returncode == 0
    assert _run(BUILD_SCRIPT, "--manifest", str(manifest), "--output-dir", str(second)).returncode == 0
    assert _tree_digest(first) == _tree_digest(second)


def test_builder_rejects_output_directory_that_contains_the_manifest(tmp_path: Path):
    manifest = _write_fixture(tmp_path)
    marker = tmp_path / "must-survive.txt"
    marker.write_text("keep", encoding="utf-8")

    built = _run(BUILD_SCRIPT, "--manifest", str(manifest), "--output-dir", str(tmp_path))

    assert built.returncode == 2
    assert "contains the manifest" in (built.stderr + built.stdout)
    assert marker.read_text(encoding="utf-8") == "keep"
    assert manifest.is_file()


def test_builder_does_not_replace_an_unmarked_nonempty_directory(tmp_path: Path):
    manifest = _write_fixture(tmp_path)
    out = tmp_path / "existing-output"
    out.mkdir()
    marker = out / "user-file.txt"
    marker.write_text("keep", encoding="utf-8")

    built = _run(BUILD_SCRIPT, "--manifest", str(manifest), "--output-dir", str(out))

    assert built.returncode == 2
    assert "must be empty" in (built.stderr + built.stdout)
    assert marker.read_text(encoding="utf-8") == "keep"


def test_builder_does_not_trust_spoofed_package_markers(tmp_path: Path):
    manifest = _write_fixture(tmp_path)
    out = tmp_path / "spoofed-output"
    (out / "qa").mkdir(parents=True)
    (out / "manual-manifest.json").write_text("{}", encoding="utf-8")
    (out / "qa/build-report.json").write_text("{}", encoding="utf-8")
    marker = out / "user-file.txt"
    marker.write_text("keep", encoding="utf-8")

    built = _run(BUILD_SCRIPT, "--manifest", str(manifest), "--output-dir", str(out))

    assert built.returncode == 2
    assert "must be empty" in (built.stderr + built.stdout)
    assert marker.read_text(encoding="utf-8") == "keep"


def test_builder_rejects_a_symlink_output_directory(tmp_path: Path):
    manifest = _write_fixture(tmp_path)
    target = tmp_path / "target"
    target.mkdir()
    output_link = tmp_path / "output-link"
    os.symlink(target, output_link, target_is_directory=True)

    built = _run(BUILD_SCRIPT, "--manifest", str(manifest), "--output-dir", str(output_link))

    assert built.returncode == 2
    assert "symbolic link" in (built.stderr + built.stdout)
    assert list(target.iterdir()) == []


def test_builder_rejects_a_symlink_in_the_output_path(tmp_path: Path):
    manifest = _write_fixture(tmp_path)
    target = tmp_path / "target-parent"
    target.mkdir()
    linked_parent = tmp_path / "linked-parent"
    os.symlink(target, linked_parent, target_is_directory=True)
    nested_output = linked_parent / "manual"

    built = _run(BUILD_SCRIPT, "--manifest", str(manifest), "--output-dir", str(nested_output))

    assert built.returncode == 2
    assert "symbolic link component" in (built.stderr + built.stdout)
    assert not (target / "manual").exists()


def test_unsafe_state_changing_lesson_is_rejected(tmp_path: Path):
    manifest = _write_fixture(tmp_path, status="final", unsafe=True)
    out = tmp_path / "out"

    built = _run(BUILD_SCRIPT, "--manifest", str(manifest), "--output-dir", str(out))

    assert built.returncode == 2
    assert "approval_required" in (built.stderr + built.stdout)
    assert not (out / "index.html").exists()


def test_state_changing_step_requires_explicit_safe_contract(tmp_path: Path):
    manifest = _write_fixture(tmp_path)
    data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    step = data["lessons"][0]["steps"][0]
    step["operation"] = "write"
    step["action"] = "요청을 영구 삭제한다."
    manifest.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")

    built = _run(BUILD_SCRIPT, "--manifest", str(manifest), "--output-dir", str(tmp_path / "out"))

    assert built.returncode == 2
    output = built.stderr + built.stdout
    assert "state-changing" in output
    assert "readback" in output


def test_approved_sandbox_write_with_readback_builds(tmp_path: Path):
    manifest = _write_fixture(tmp_path)
    data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    lesson = data["lessons"][0]
    lesson["risk"] = "high"
    lesson["approval_required"] = True
    lesson["fixture"] = "sandbox"
    step = lesson["steps"][0]
    step["operation"] = "write"
    step["action"] = "샌드박스 요청 상태를 변경한다."
    step["readback"] = "같은 요청 번호를 다시 열어 변경 상태와 감사 기록을 확인한다."
    manifest.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    out = tmp_path / "out"

    built = _run(BUILD_SCRIPT, "--manifest", str(manifest), "--output-dir", str(out))

    assert built.returncode == 0, built.stderr or built.stdout
    lesson_html = (out / "lessons/review-request.html").read_text(encoding="utf-8")
    assert "변경 후 재확인" in lesson_html
    verified = _run(VERIFY_SCRIPT, "--manifest", str(manifest), "--package-dir", str(out))
    assert verified.returncode == 0, verified.stderr or verified.stdout


def test_obvious_state_change_cannot_be_misclassified_as_read(tmp_path: Path):
    manifest = _write_fixture(tmp_path)
    data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    step = data["lessons"][0]["steps"][0]
    step["operation"] = "read"
    step["action"] = "프로덕션 결제 기록을 영구 삭제한다."
    manifest.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")

    built = _run(BUILD_SCRIPT, "--manifest", str(manifest), "--output-dir", str(tmp_path / "out"))

    assert built.returncode == 2
    assert "appears state-changing" in (built.stderr + built.stdout)


def test_final_step_cannot_rely_only_on_inference(tmp_path: Path):
    manifest = _write_fixture(tmp_path, status="final")
    data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    data["sources"].append(
        {
            "id": "INF-001",
            "title": "미확인 추론",
            "evidence_type": "inference",
            "path": "source/operator-guide.md",
            "checked_at": "2026-08-12",
            "sha256": data["sources"][0]["sha256"],
        }
    )
    data["lessons"][0]["source_refs"].append("INF-001")
    for step in data["lessons"][0]["steps"]:
        step["source_refs"] = ["INF-001"]
    manifest.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")

    built = _run(BUILD_SCRIPT, "--manifest", str(manifest), "--output-dir", str(tmp_path / "out"))

    assert built.returncode == 2
    assert "final step cannot rely only on inference" in (built.stderr + built.stdout)


def test_verifier_detects_broken_links_and_leaked_placeholders(tmp_path: Path):
    manifest = _write_fixture(tmp_path)
    out = tmp_path / "out"
    assert _run(BUILD_SCRIPT, "--manifest", str(manifest), "--output-dir", str(out)).returncode == 0
    lesson_path = out / "lessons/review-request.html"
    lesson_path.write_text(
        lesson_path.read_text(encoding="utf-8")
        + '<a href="missing.html">broken</a><a href="javascript:alert(1)">unsafe</a>'
        + '<p>TBD</p><p>[원시 링크](target)</p><p>{{BROKEN}}</p>',
        encoding="utf-8",
    )

    verified = _run(VERIFY_SCRIPT, "--manifest", str(manifest), "--package-dir", str(out))

    assert verified.returncode == 2
    report = json.loads((out / "qa/verification.json").read_text(encoding="utf-8"))
    assert report["summary"]["high_issues"] >= 3
    messages = "\n".join(issue["message"] for issue in report["issues"])
    assert "missing.html" in messages
    assert "TBD" in messages
    assert "원시 Markdown 링크" in messages
    assert "템플릿 변수" in messages
    assert "javascript" in messages


def test_evidence_map_escapes_markdown_and_html_from_source_metadata(tmp_path: Path):
    manifest = _write_fixture(tmp_path)
    data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    data["sources"][0]["title"] = "가이드 | <script>alert(1)</script> [링크](javascript:x)"
    manifest.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    out = tmp_path / "out"

    built = _run(BUILD_SCRIPT, "--manifest", str(manifest), "--output-dir", str(out))

    assert built.returncode == 0, built.stderr or built.stdout
    evidence_map = (out / "sources/evidence-map.md").read_text(encoding="utf-8")
    assert "<script>" not in evidence_map
    assert "[링크](javascript:x)" not in evidence_map
    assert "\\|" in evidence_map


def test_verifier_rejects_active_content_and_step_text_drift(tmp_path: Path):
    manifest = _write_fixture(tmp_path)
    out = tmp_path / "out"
    assert _run(BUILD_SCRIPT, "--manifest", str(manifest), "--output-dir", str(out)).returncode == 0
    lesson_path = out / "lessons/review-request.html"
    changed = lesson_path.read_text(encoding="utf-8").replace(
        "요청 목록에서 상태가 ‘검토 대기’인 요청 번호를 연다.",
        "운영 데이터 전체를 삭제한다.",
    )
    lesson_path.write_text(
        changed
        + '<script src="https://evil.example/payload.js"></script>'
        + '<a href="https://evil.example/phish">공식 문서</a>',
        encoding="utf-8",
    )

    verified = _run(VERIFY_SCRIPT, "--manifest", str(manifest), "--package-dir", str(out))

    assert verified.returncode == 2
    report = json.loads((out / "qa/verification.json").read_text(encoding="utf-8"))
    codes = {issue["code"] for issue in report["issues"]}
    assert "active-content" in codes
    assert "step-content-drift" in codes
    assert "external-link" in codes


def test_verifier_rejects_external_css_and_markdown_active_content(tmp_path: Path):
    manifest = _write_fixture(tmp_path)
    out = tmp_path / "out"
    assert _run(BUILD_SCRIPT, "--manifest", str(manifest), "--output-dir", str(out)).returncode == 0
    (out / "assets/manual.css").write_text(
        '@import url("https://evil.example/x.css");', encoding="utf-8"
    )
    (out / "STATUS.md").write_text(
        "# STATUS\n\n<script>alert(1)</script>\n[x](javascript:alert(1))\n",
        encoding="utf-8",
    )

    verified = _run(VERIFY_SCRIPT, "--manifest", str(manifest), "--package-dir", str(out))

    assert verified.returncode == 2
    report = json.loads((out / "qa/verification.json").read_text(encoding="utf-8"))
    codes = {issue["code"] for issue in report["issues"]}
    assert "external-css" in codes
    assert "markdown-active-content" in codes


def test_verifier_reports_extra_steps_and_package_symlinks_without_crashing(tmp_path: Path):
    manifest = _write_fixture(tmp_path)
    out = tmp_path / "out"
    assert _run(BUILD_SCRIPT, "--manifest", str(manifest), "--output-dir", str(out)).returncode == 0
    lesson_path = out / "lessons/review-request.html"
    lesson_path.write_text(
        lesson_path.read_text(encoding="utf-8").replace(
            "</ol>", '<li class="step"><h3>삽입 단계</h3></li></ol>', 1
        ),
        encoding="utf-8",
    )
    outside = tmp_path / "outside.css"
    outside.write_text("body{}", encoding="utf-8")
    (out / "assets/manual.css").unlink()
    os.symlink(outside, out / "assets/manual.css")

    verified = _run(VERIFY_SCRIPT, "--manifest", str(manifest), "--package-dir", str(out))

    assert verified.returncode == 2, verified.stderr or verified.stdout
    report = json.loads((out / "qa/verification.json").read_text(encoding="utf-8"))
    codes = {issue["code"] for issue in report["issues"]}
    assert "step-count" in codes
    assert "package-symlink" in codes


def test_verifier_detects_evidence_changed_after_build(tmp_path: Path):
    manifest = _write_fixture(tmp_path)
    out = tmp_path / "out"
    assert _run(BUILD_SCRIPT, "--manifest", str(manifest), "--output-dir", str(out)).returncode == 0
    (tmp_path / "source/operator-guide.md").write_text("교체된 근거", encoding="utf-8")

    verified = _run(VERIFY_SCRIPT, "--manifest", str(manifest), "--package-dir", str(out))

    assert verified.returncode == 2
    report = json.loads((out / "qa/verification.json").read_text(encoding="utf-8"))
    assert any(issue["code"] == "evidence-drift" for issue in report["issues"])


def test_builder_rejects_evidence_that_does_not_match_declared_hash(tmp_path: Path):
    manifest = _write_fixture(tmp_path)
    data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    data["sources"][0]["sha256"] = "0" * 64
    manifest.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")

    built = _run(BUILD_SCRIPT, "--manifest", str(manifest), "--output-dir", str(tmp_path / "out"))

    assert built.returncode == 2
    assert "declared SHA-256" in (built.stderr + built.stdout)


def test_verifier_detects_packaged_media_changed_after_build(tmp_path: Path):
    manifest = _write_fixture(tmp_path)
    out = tmp_path / "out"
    assert _run(BUILD_SCRIPT, "--manifest", str(manifest), "--output-dir", str(out)).returncode == 0
    (out / "media/request-list.svg").write_text("<svg/>", encoding="utf-8")

    verified = _run(VERIFY_SCRIPT, "--manifest", str(manifest), "--package-dir", str(out))

    assert verified.returncode == 2
    report = json.loads((out / "qa/verification.json").read_text(encoding="utf-8"))
    assert any(issue["code"] == "media-drift" for issue in report["issues"])


def test_media_hash_is_anchored_to_manual_manifest_not_build_report(tmp_path: Path):
    manifest = _write_fixture(tmp_path)
    out = tmp_path / "out"
    assert _run(BUILD_SCRIPT, "--manifest", str(manifest), "--output-dir", str(out)).returncode == 0
    media = out / "media/request-list.svg"
    media.write_text("<svg><text>tampered</text></svg>", encoding="utf-8")
    report_path = out / "qa/build-report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["packaged_media"]["evidence/request-list.svg"]["sha256"] = hashlib.sha256(
        media.read_bytes()
    ).hexdigest()
    report["packaged_media"]["evidence/request-list.svg"]["bytes"] = media.stat().st_size
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    verified = _run(VERIFY_SCRIPT, "--manifest", str(manifest), "--package-dir", str(out))

    assert verified.returncode == 2
    verification = json.loads((out / "qa/verification.json").read_text(encoding="utf-8"))
    assert any(issue["code"] == "media-drift" for issue in verification["issues"])


def test_verifier_never_writes_through_package_symlink(tmp_path: Path):
    manifest = _write_fixture(tmp_path)
    out = tmp_path / "out"
    external = tmp_path / "external"
    external.mkdir()
    assert _run(BUILD_SCRIPT, "--manifest", str(manifest), "--output-dir", str(out)).returncode == 0
    shutil.rmtree(out / "qa")
    os.symlink(external, out / "qa", target_is_directory=True)

    verified = _run(VERIFY_SCRIPT, "--manifest", str(manifest), "--package-dir", str(out))

    assert verified.returncode == 2
    assert not (external / "verification.json").exists()
    assert not (external / "verification.md").exists()


def test_verifier_rejects_a_symlink_package_directory(tmp_path: Path):
    manifest = _write_fixture(tmp_path)
    real_out = tmp_path / "real-out"
    package_link = tmp_path / "package-link"
    assert _run(BUILD_SCRIPT, "--manifest", str(manifest), "--output-dir", str(real_out)).returncode == 0
    os.symlink(real_out, package_link, target_is_directory=True)

    verified = _run(VERIFY_SCRIPT, "--manifest", str(manifest), "--package-dir", str(package_link))

    assert verified.returncode == 2
    assert "symbolic link" in (verified.stderr + verified.stdout)
    assert not (real_out / "qa/verification.json").exists()


def test_verifier_does_not_create_a_missing_package_directory(tmp_path: Path):
    manifest = _write_fixture(tmp_path)
    missing = tmp_path / "missing-package"

    verified = _run(VERIFY_SCRIPT, "--manifest", str(manifest), "--package-dir", str(missing))

    assert verified.returncode == 2
    assert not missing.exists()


def test_shipped_manual_example_builds_and_verifies(tmp_path: Path):
    assert SHIPPED_MANUAL.is_file()
    out = tmp_path / "example-out"

    built = _run(BUILD_SCRIPT, "--manifest", str(SHIPPED_MANUAL), "--output-dir", str(out))
    assert built.returncode == 0, built.stderr or built.stdout

    verified = _run(
        VERIFY_SCRIPT,
        "--manifest",
        str(SHIPPED_MANUAL),
        "--package-dir",
        str(out),
    )
    assert verified.returncode == 0, verified.stderr or verified.stdout
    report = json.loads((out / "qa/verification.json").read_text(encoding="utf-8"))
    assert report["summary"]["high_issues"] == 0
    assert report["checks"] == {
        "technical": "pass",
        "content": "pass",
        "visual": "not_run",
    }


def test_final_manual_requires_structured_visual_evidence(tmp_path: Path):
    manifest = _write_fixture(tmp_path, status="final")
    out = tmp_path / "out"
    assert _run(BUILD_SCRIPT, "--manifest", str(manifest), "--output-dir", str(out)).returncode == 0

    no_evidence = _run(
        VERIFY_SCRIPT,
        "--manifest",
        str(manifest),
        "--package-dir",
        str(out),
        "--visual-reviewed",
    )
    assert no_evidence.returncode == 2
    failed = json.loads((out / "qa/verification.json").read_text(encoding="utf-8"))
    assert failed["checks"]["content"] == "pass"
    assert failed["checks"]["visual"] == "fail"
    assert any(issue["code"] == "visual-evidence-required" for issue in failed["issues"])

    evidence = out / "qa" / "visual-review.json"
    evidence.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "status": "pass",
                "reviewed_at": "2026-08-12",
                "reviewer": "KLIC QA",
                "viewports": ["1280x800", "390x844"],
                "pages": [
                    "index.html",
                    "overview.html",
                    "lessons/review-request.html",
                ],
                "keyboard_navigation": "pass",
                "internal_navigation": "pass",
                "console_errors": 0,
                "findings": [],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    verified = _run(
        VERIFY_SCRIPT,
        "--manifest",
        str(manifest),
        "--package-dir",
        str(out),
        "--visual-evidence",
        str(evidence),
    )
    assert verified.returncode == 0, verified.stderr or verified.stdout
    report = json.loads((out / "qa/verification.json").read_text(encoding="utf-8"))
    assert report["summary"]["status"] == "pass"
    assert report["checks"]["visual"] == "pass"

    visual_data = json.loads(evidence.read_text(encoding="utf-8"))
    visual_data["findings"] = [
        {
            "severity": "critical",
            "status": "open",
            "page": "index.html",
            "message": "모바일에서 완료 버튼이 보이지 않음",
        }
    ]
    evidence.write_text(json.dumps(visual_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    unresolved = _run(
        VERIFY_SCRIPT,
        "--manifest",
        str(manifest),
        "--package-dir",
        str(out),
        "--visual-evidence",
        str(evidence),
    )
    assert unresolved.returncode == 2
    failed = json.loads((out / "qa/verification.json").read_text(encoding="utf-8"))
    assert any(issue["code"] == "visual-unresolved-finding" for issue in failed["issues"])


def _copy_skill(tmp_path: Path) -> Path:
    copied = tmp_path / "korean-ebook"
    shutil.copytree(
        SKILL_ROOT,
        copied,
        ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.pyc"),
    )
    return copied


def test_skill_validator_requires_claimed_manual_pipeline_files(tmp_path: Path):
    copied = _copy_skill(tmp_path)
    (copied / "scripts/build_manual.py").unlink()

    result = _run(VALIDATE_SKILL_SCRIPT, str(copied))

    assert result.returncode == 2
    report = json.loads(result.stdout)
    assert any("build_manual.py" in issue["message"] for issue in report["issues"])


def test_skill_validator_rejects_removed_external_manual_dependencies(tmp_path: Path):
    copied = _copy_skill(tmp_path)
    skill_path = copied / "SKILL.md"
    skill_path.write_text(
        skill_path.read_text(encoding="utf-8")
        + "\nREQUIRED SUB-SKILL: manual-verification\nHermes peer oracle workflow\n",
        encoding="utf-8",
    )

    result = _run(VALIDATE_SKILL_SCRIPT, str(copied))

    assert result.returncode == 2
    report = json.loads(result.stdout)
    messages = "\n".join(issue["message"] for issue in report["issues"])
    assert "manual-verification" in messages
    assert "Hermes" in messages
