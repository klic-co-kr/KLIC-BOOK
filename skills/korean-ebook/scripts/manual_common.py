#!/usr/bin/env python3
"""Shared schema and evidence checks for the korean-ebook manual pipeline."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
from pathlib import Path
import re
from typing import Any, Iterable

import yaml


ALLOWED_MANUAL_STATUSES = {"draft", "provisional", "final"}
ALLOWED_EVIDENCE_TYPES = {
    "source",
    "ui",
    "runtime",
    "operator-confirmed",
    "inference",
}
ALLOWED_RISKS = {"none", "low", "medium", "high", "critical"}
ALLOWED_MEDIA_TYPES = {"image", "video"}
ALLOWED_OPERATIONS = {"read", "write"}
STATE_CHANGING_RISKS = {"high", "critical"}
SAFE_FIXTURES = {"demo", "staging", "local", "sandbox", "dedicated-test-data"}
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SOURCE_ID_RE = re.compile(r"^[A-Za-z0-9]+(?:[-_.][A-Za-z0-9]+)*$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
STATE_CHANGE_ACTION_RE = re.compile(
    r"(?:삭제|변경|저장|승인|제출|결제|청구|지급|송금|취소|생성|추가|수정|발행)(?:한다|합니다|하세요|했다|합니다)|"
    r"\b(?:delete|remove|update|create|submit|approve|publish|pay|charge|grant|revoke|write)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Issue:
    severity: str
    code: str
    message: str
    location: str = ""

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def load_manual(path: Path) -> dict[str, Any]:
    """Load a UTF-8 YAML manual manifest and require a mapping root."""
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"manifest not found: {path}") from exc
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("manual manifest must be a YAML object")
    return data


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def resolve_local_path(root: Path, value: str) -> Path:
    """Resolve a manifest path and reject absolute or root-escaping values."""
    rel = Path(value)
    if rel.is_absolute():
        raise ValueError(f"absolute path is not allowed: {value}")
    resolved = (root / rel).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError(f"path escapes manifest root: {value}") from exc
    return resolved


def _required_text(
    obj: dict[str, Any],
    fields: Iterable[str],
    location: str,
    issues: list[Issue],
) -> None:
    for field in fields:
        value = obj.get(field)
        if not isinstance(value, str) or not value.strip():
            issues.append(
                Issue("high", "required-field", f"{location}.{field} is required", location)
            )


def _required_list(
    obj: dict[str, Any],
    field: str,
    location: str,
    issues: list[Issue],
) -> list[Any]:
    value = obj.get(field)
    if not isinstance(value, list) or not value:
        issues.append(
            Issue("high", "required-list", f"{location}.{field} must be a non-empty list", location)
        )
        return []
    return value


def _validate_id(value: Any, location: str, issues: list[Issue]) -> str:
    text = str(value or "")
    if not ID_RE.fullmatch(text):
        issues.append(
            Issue(
                "high",
                "invalid-id",
                f"{location} must use lowercase ASCII letters, digits, and hyphens",
                location,
            )
        )
    return text


def _validate_source_id(value: Any, location: str, issues: list[Issue]) -> str:
    text = str(value or "")
    if not SOURCE_ID_RE.fullmatch(text):
        issues.append(
            Issue(
                "high",
                "invalid-source-id",
                f"{location} must use letters, digits, hyphens, underscores, or dots",
                location,
            )
        )
    return text


def _validate_source_path(
    root: Path,
    rel: Any,
    expected_sha256: Any,
    location: str,
    issues: list[Issue],
) -> None:
    if not isinstance(rel, str) or not rel.strip():
        issues.append(Issue("high", "required-path", f"{location} is required", location))
        return
    try:
        path = resolve_local_path(root, rel)
    except ValueError as exc:
        issues.append(Issue("high", "unsafe-path", str(exc), location))
        return
    if not isinstance(expected_sha256, str) or not SHA256_RE.fullmatch(expected_sha256):
        issues.append(
            Issue(
                "high",
                "evidence-sha256",
                f"{location.rsplit('.', 1)[0]}.sha256 must be 64 lowercase hex characters",
                location,
            )
        )
    if not path.is_file():
        issues.append(Issue("high", "missing-file", f"missing local evidence: {rel}", location))
    elif path.stat().st_size == 0:
        issues.append(Issue("high", "empty-file", f"local evidence is empty: {rel}", location))
    elif isinstance(expected_sha256, str) and SHA256_RE.fullmatch(expected_sha256):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != expected_sha256:
            issues.append(
                Issue(
                    "high",
                    "evidence-sha256-mismatch",
                    f"local evidence does not match declared SHA-256: {rel}",
                    location,
                )
            )


def validate_source_contract(data: dict[str, Any], root: Path) -> list[Issue]:
    """Validate content depth, evidence links, and risky-action boundaries."""
    issues: list[Issue] = []
    if data.get("schema_version") != 1:
        issues.append(
            Issue("high", "schema-version", "schema_version must be 1", "schema_version")
        )

    manual = data.get("manual")
    if not isinstance(manual, dict):
        issues.append(Issue("high", "manual-object", "manual must be an object", "manual"))
        manual = {}
    _required_text(
        manual,
        ["id", "title", "language", "status", "version", "version_basis", "purpose"],
        "manual",
        issues,
    )
    manual_id = _validate_id(manual.get("id"), "manual.id", issues)
    del manual_id
    _required_list(manual, "audience", "manual", issues)
    status = str(manual.get("status") or "")
    if status and status not in ALLOWED_MANUAL_STATUSES:
        issues.append(
            Issue(
                "high",
                "manual-status",
                f"manual.status must be one of {sorted(ALLOWED_MANUAL_STATUSES)}",
                "manual.status",
            )
        )

    overview = data.get("overview")
    if not isinstance(overview, dict):
        issues.append(Issue("high", "overview-object", "overview must be an object", "overview"))
        overview = {}
    _required_text(overview, ["summary", "mental_model"], "overview", issues)
    for field in ["roles", "components", "lifecycle", "beginner_confusions"]:
        _required_list(overview, field, "overview", issues)
    for index, role in enumerate(as_list(overview.get("roles"))):
        location = f"overview.roles[{index}]"
        if not isinstance(role, dict):
            issues.append(Issue("high", "role-object", f"{location} must be an object", location))
        else:
            _required_text(role, ["name", "responsibility"], location, issues)
    for index, component in enumerate(as_list(overview.get("components"))):
        location = f"overview.components[{index}]"
        if not isinstance(component, dict):
            issues.append(
                Issue("high", "component-object", f"{location} must be an object", location)
            )
        else:
            _required_text(component, ["name", "purpose"], location, issues)
    for index, item in enumerate(as_list(overview.get("beginner_confusions"))):
        location = f"overview.beginner_confusions[{index}]"
        if not isinstance(item, dict):
            issues.append(
                Issue("high", "confusion-object", f"{location} must be an object", location)
            )
        else:
            _required_text(item, ["confusion", "correction"], location, issues)

    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        issues.append(
            Issue("high", "sources-list", "sources must be a non-empty list", "sources")
        )
        sources = []
    source_ids: set[str] = set()
    source_types: dict[str, str] = {}
    for index, source in enumerate(sources):
        location = f"sources[{index}]"
        if not isinstance(source, dict):
            issues.append(Issue("high", "source-object", f"{location} must be an object", location))
            continue
        _required_text(source, ["id", "title", "evidence_type", "path", "checked_at", "sha256"], location, issues)
        source_id = _validate_source_id(source.get("id"), f"{location}.id", issues)
        if source_id in source_ids:
            issues.append(
                Issue("high", "duplicate-source", f"duplicate source id: {source_id}", location)
            )
        source_ids.add(source_id)
        evidence_type = str(source.get("evidence_type") or "")
        source_types[source_id] = evidence_type
        if evidence_type and evidence_type not in ALLOWED_EVIDENCE_TYPES:
            issues.append(
                Issue(
                    "high",
                    "evidence-type",
                    f"{location}.evidence_type must be one of {sorted(ALLOWED_EVIDENCE_TYPES)}",
                    location,
                )
            )
        _validate_source_path(
            root,
            source.get("path"),
            source.get("sha256"),
            f"{location}.path",
            issues,
        )

    lessons = data.get("lessons")
    if not isinstance(lessons, list) or not lessons:
        issues.append(
            Issue("high", "lessons-list", "lessons must be a non-empty list", "lessons")
        )
        lessons = []
    lesson_ids: set[str] = set()
    for index, lesson in enumerate(lessons):
        location = f"lessons[{index}]"
        if not isinstance(lesson, dict):
            issues.append(Issue("high", "lesson-object", f"{location} must be an object", location))
            continue
        _required_text(
            lesson,
            ["id", "title", "purpose", "when_to_use", "risk", "fixture", "next"],
            location,
            issues,
        )
        for field in [
            "audience",
            "prerequisites",
            "source_refs",
            "steps",
            "cautions",
            "common_mistakes",
            "completion_checks",
        ]:
            _required_list(lesson, field, location, issues)
        lesson_id = _validate_id(lesson.get("id"), f"{location}.id", issues)
        if lesson_id in lesson_ids:
            issues.append(
                Issue("high", "duplicate-lesson", f"duplicate lesson id: {lesson_id}", location)
            )
        lesson_ids.add(lesson_id)
        risk = str(lesson.get("risk") or "")
        if risk and risk not in ALLOWED_RISKS:
            issues.append(
                Issue(
                    "high",
                    "risk-value",
                    f"{location}.risk must be one of {sorted(ALLOWED_RISKS)}",
                    location,
                )
            )
        if not isinstance(lesson.get("approval_required"), bool):
            issues.append(
                Issue(
                    "high",
                    "approval-required",
                    f"{location}.approval_required must be boolean",
                    location,
                )
            )
        fixture = str(lesson.get("fixture") or "")
        if risk in STATE_CHANGING_RISKS:
            if lesson.get("approval_required") is not True:
                issues.append(
                    Issue(
                        "high",
                        "unsafe-action",
                        f"{location}: high-risk action requires approval_required: true",
                        location,
                    )
                )
            if fixture not in SAFE_FIXTURES:
                issues.append(
                    Issue(
                        "high",
                        "unsafe-fixture",
                        f"{location}: high-risk action requires a safe fixture {sorted(SAFE_FIXTURES)}",
                        location,
                    )
                )

        lesson_refs = [str(value) for value in as_list(lesson.get("source_refs"))]
        for ref in lesson_refs:
            if ref not in source_ids:
                issues.append(
                    Issue("high", "unknown-source", f"{location}: unknown source ref {ref}", location)
                )
        if status == "final" and lesson_refs and all(
            source_types.get(ref) == "inference" for ref in lesson_refs
        ):
            issues.append(
                Issue(
                    "high",
                    "inference-only-final",
                    f"{location}: a final lesson cannot rely only on inference",
                    location,
                )
            )

        for step_index, step in enumerate(as_list(lesson.get("steps"))):
            step_location = f"{location}.steps[{step_index}]"
            if not isinstance(step, dict):
                issues.append(
                    Issue("high", "step-object", f"{step_location} must be an object", step_location)
                )
                continue
            _required_text(
                step,
                ["title", "operation", "action", "evidence", "success"],
                step_location,
                issues,
            )
            operation = str(step.get("operation") or "")
            if operation and operation not in ALLOWED_OPERATIONS:
                issues.append(
                    Issue(
                        "high",
                        "operation-value",
                        f"{step_location}.operation must be one of {sorted(ALLOWED_OPERATIONS)}",
                        step_location,
                    )
                )
            action = str(step.get("action") or "")
            if operation == "read" and STATE_CHANGE_ACTION_RE.search(action):
                issues.append(
                    Issue(
                        "high",
                        "misclassified-operation",
                        f"{step_location}: action appears state-changing but operation is read",
                        step_location,
                    )
                )
            if operation == "write":
                if risk not in STATE_CHANGING_RISKS:
                    issues.append(
                        Issue(
                            "high",
                            "state-changing-risk",
                            f"{step_location}: state-changing step requires lesson risk high or critical",
                            step_location,
                        )
                    )
                if lesson.get("approval_required") is not True:
                    issues.append(
                        Issue(
                            "high",
                            "state-changing-approval",
                            f"{step_location}: state-changing step requires approval_required: true",
                            step_location,
                        )
                    )
                if fixture not in SAFE_FIXTURES:
                    issues.append(
                        Issue(
                            "high",
                            "state-changing-fixture",
                            f"{step_location}: state-changing step requires a safe fixture",
                            step_location,
                        )
                    )
                if not isinstance(step.get("readback"), str) or not step["readback"].strip():
                    issues.append(
                        Issue(
                            "high",
                            "state-changing-readback",
                            f"{step_location}: state-changing step requires a readback assertion",
                            step_location,
                        )
                    )
            refs = _required_list(step, "source_refs", step_location, issues)
            normalized_refs = [str(value) for value in refs]
            for ref in normalized_refs:
                if ref not in source_ids:
                    issues.append(
                        Issue(
                            "high",
                            "unknown-source",
                            f"{step_location}: unknown source ref {ref}",
                            step_location,
                        )
                    )
            if status == "final" and normalized_refs and all(
                source_types.get(ref) == "inference" for ref in normalized_refs
            ):
                issues.append(
                    Issue(
                        "high",
                        "inference-only-step",
                        f"{step_location}: final step cannot rely only on inference",
                        step_location,
                    )
                )

        media_items = as_list(lesson.get("media"))
        for media_index, media in enumerate(media_items):
            media_location = f"{location}.media[{media_index}]"
            if not isinstance(media, dict):
                issues.append(
                    Issue("high", "media-object", f"{media_location} must be an object", media_location)
                )
                continue
            _required_text(media, ["type", "path", "alt", "sha256"], media_location, issues)
            media_refs = _required_list(media, "source_refs", media_location, issues)
            media_type = str(media.get("type") or "")
            if media_type and media_type not in ALLOWED_MEDIA_TYPES:
                issues.append(
                    Issue(
                        "high",
                        "media-type",
                        f"{media_location}.type must be image or video",
                        media_location,
                    )
                )
            _validate_source_path(
                root,
                media.get("path"),
                media.get("sha256"),
                f"{media_location}.path",
                issues,
            )
            for ref in [str(value) for value in media_refs]:
                if ref not in source_ids:
                    issues.append(
                        Issue(
                            "high",
                            "unknown-source",
                            f"{media_location}: unknown source ref {ref}",
                            media_location,
                        )
                    )

    workflows = data.get("workflows")
    if not isinstance(workflows, list) or not workflows:
        issues.append(
            Issue("high", "workflows-list", "workflows must be a non-empty list", "workflows")
        )
        workflows = []
    workflow_ids: set[str] = set()
    referenced_lessons: set[str] = set()
    for index, workflow in enumerate(workflows):
        location = f"workflows[{index}]"
        if not isinstance(workflow, dict):
            issues.append(
                Issue("high", "workflow-object", f"{location} must be an object", location)
            )
            continue
        _required_text(workflow, ["id", "title", "goal", "trigger", "outcome"], location, issues)
        lesson_refs = _required_list(workflow, "lessons", location, issues)
        workflow_id = _validate_id(workflow.get("id"), f"{location}.id", issues)
        if workflow_id in workflow_ids:
            issues.append(
                Issue("high", "duplicate-workflow", f"duplicate workflow id: {workflow_id}", location)
            )
        workflow_ids.add(workflow_id)
        for lesson_ref in [str(value) for value in lesson_refs]:
            referenced_lessons.add(lesson_ref)
            if lesson_ref not in lesson_ids:
                issues.append(
                    Issue(
                        "high",
                        "unknown-lesson",
                        f"{location}: unknown lesson ref {lesson_ref}",
                        location,
                    )
                )
    for lesson_id in lesson_ids - referenced_lessons:
        issues.append(
            Issue(
                "medium",
                "orphan-lesson",
                f"lesson is not assigned to any workflow: {lesson_id}",
                "workflows",
            )
        )
    return issues


def highest_issue_count(issues: Iterable[Issue], severity: str) -> int:
    return sum(1 for issue in issues if issue.severity == severity)
