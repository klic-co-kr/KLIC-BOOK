#!/usr/bin/env python3
"""Validate this folder against the Agent Skills packaging rules used by OpenAI."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    print("Missing PyYAML", file=sys.stderr)
    raise SystemExit(2) from exc


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FONT_SUFFIXES = {".ttf", ".otf", ".woff", ".woff2", ".ttc", ".eot"}


def parse_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, flags=re.S)
    if not match:
        raise ValueError("SKILL.md must start with YAML frontmatter")
    return yaml.safe_load(match.group(1)) or {}, match.group(2)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dir", type=Path, nargs="?", default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.skill_dir.resolve()
    issues: list[dict[str, str]] = []

    skill_files = list(root.rglob("SKILL.md")) + list(root.rglob("skill.md"))
    unique = {p.resolve() for p in skill_files}
    if len(unique) != 1:
        issues.append({"severity": "error", "message": f"Exactly one SKILL.md is required; found {len(unique)}"})
    skill_path = root / "SKILL.md"
    if not skill_path.exists():
        issues.append({"severity": "error", "message": "Top-level SKILL.md is missing"})
        frontmatter = {}
        body = ""
    else:
        try:
            frontmatter, body = parse_frontmatter(skill_path)
        except Exception as exc:
            issues.append({"severity": "error", "message": str(exc)})
            frontmatter, body = {}, ""

    name = str(frontmatter.get("name", ""))
    description = str(frontmatter.get("description", ""))
    if not name or len(name) > 64 or not NAME_RE.match(name):
        issues.append({"severity": "error", "message": "name must be 1-64 lowercase ASCII letters/numbers/hyphens"})
    if name and root.name != name:
        issues.append({"severity": "error", "message": f"Directory name '{root.name}' must match skill name '{name}'"})
    if not description or len(description) > 1024:
        issues.append({"severity": "error", "message": "description must be 1-1024 characters"})
    compatibility = frontmatter.get("compatibility")
    if compatibility is not None and (not isinstance(compatibility, str) or not compatibility.strip() or len(compatibility) > 500):
        issues.append({"severity": "error", "message": "compatibility must be a non-empty string of at most 500 characters"})
    metadata = frontmatter.get("metadata")
    if metadata is not None and (not isinstance(metadata, dict) or any(not isinstance(k, str) or not isinstance(v, str) for k, v in metadata.items())):
        issues.append({"severity": "error", "message": "metadata must be a string-to-string mapping"})
    if len(body.splitlines()) > 500:
        issues.append({"severity": "warning", "message": f"SKILL.md body is {len(body.splitlines())} lines; keep it under 500 when possible"})

    files = [p for p in root.rglob("*") if p.is_file()]
    if len(files) > 500:
        issues.append({"severity": "error", "message": f"Skill has {len(files)} files; OpenAI upload limit is 500"})
    total_size = sum(p.stat().st_size for p in files)
    if total_size > 50 * 1024 * 1024:
        issues.append({"severity": "error", "message": f"Uncompressed bundle exceeds 50 MB: {total_size}"})
    for path in files:
        if path.stat().st_size > 25 * 1024 * 1024:
            issues.append({"severity": "error", "message": f"File exceeds 25 MB: {path.relative_to(root)}"})
        if path.suffix.casefold() in FONT_SUFFIXES:
            issues.append({"severity": "error", "message": f"Do not bundle font files: {path.relative_to(root)}"})

    openai_yaml = root / "agents" / "openai.yaml"
    if openai_yaml.exists():
        try:
            agent_meta = yaml.safe_load(openai_yaml.read_text(encoding="utf-8")) or {}
            interface = agent_meta.get("interface")
            if not isinstance(interface, dict):
                issues.append({"severity": "error", "message": "agents/openai.yaml requires an interface mapping"})
            else:
                for field in ("display_name", "short_description"):
                    value = interface.get(field)
                    if not isinstance(value, str) or not value.strip():
                        issues.append({"severity": "error", "message": f"agents/openai.yaml interface.{field} is required"})
                brand = interface.get("brand_color")
                if brand is not None and (not isinstance(brand, str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}", brand)):
                    issues.append({"severity": "error", "message": "interface.brand_color must be a six-digit hex color"})
            policy = agent_meta.get("policy")
            if policy is not None and not isinstance(policy, dict):
                issues.append({"severity": "error", "message": "agents/openai.yaml policy must be a mapping"})
            elif isinstance(policy, dict) and "allow_implicit_invocation" in policy and not isinstance(policy["allow_implicit_invocation"], bool):
                issues.append({"severity": "error", "message": "policy.allow_implicit_invocation must be boolean"})
        except Exception as exc:
            issues.append({"severity": "error", "message": f"agents/openai.yaml is invalid: {exc}"})

    required = [
        openai_yaml,
        root / "scripts" / "publish_book.py",
        root / "scripts" / "verify_pdf.py",
        root / "references" / "content-boundary.md",
        root / "references" / "quality-gates.md",
    ]
    for path in required:
        if not path.exists():
            issues.append({"severity": "error", "message": f"Required package file missing: {path.relative_to(root)}"})

    report = {
        "skill": str(root),
        "name": name,
        "description_chars": len(description),
        "skill_body_lines": len(body.splitlines()),
        "file_count": len(files),
        "uncompressed_bytes": total_size,
        "issues": issues,
        "valid": not any(item["severity"] == "error" for item in issues),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
