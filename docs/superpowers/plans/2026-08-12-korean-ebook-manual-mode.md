# Korean Ebook Manual Mode Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild selected manual-production capabilities as a self-contained `manual` mode inside `korean-ebook` without copying the backup skill or changing the existing PDF pipeline.

**Architecture:** Keep one skill with an artifact-format gate and two independent builders. `book` continues to use `publish_book.py` and `verify_pdf.py`; `manual` uses a new schema-driven `build_manual.py` and `verify_manual.py`, sharing only source/evidence boundary rules.

**Tech Stack:** Python 3.11+, PyYAML, BeautifulSoup, HTML5, CSS, pytest

## Global Constraints

- Base remote-facing changes on `origin/main` in `feat/integrate-manual-production`.
- Preserve existing book-mode scripts, configs, and behavior.
- Do not copy `backup/manual-production` wholesale.
- Do not depend on Hermes, peer/oracle tooling, `manual-verification`, `html-for-beginners`, Cloudflare, Driver.js, HyperFrames, OBS, Playwright, or ffmpeg for the core path.
- Keep the skill below the OpenAI 500-file and 50 MB package limits.
- Do not commit `backup/`, `__pycache__`, or user-owned `AGENTS.md`.

---

### Task 1: Define the manual contract with failing tests

**Files:**
- Create: `skills/korean-ebook/tests/test_manual_pipeline.py`
- Create: `skills/korean-ebook/examples/minimal-manual/manual.yaml`

**Interfaces:**
- Consumes: a YAML object with `manual`, `overview`, `workflows`, `lessons`, and `sources`
- Produces: executable expectations for `build_manual.main(argv)` and `verify_manual.main(argv)`

- [ ] **Step 1: Write the failing contract tests**

Test that the current skill metadata routes operator-guide prompts to manual mode, the builder produces the exact package tree, lesson pages contain all teaching-depth sections, unsafe/final manifests fail, provisional manifests keep honest status, and repeated builds are deterministic.

- [ ] **Step 2: Verify RED**

Run: `/mnt/d/DEV/KLIC-BOOK/.venv/bin/python -m pytest -q skills/korean-ebook/tests/test_manual_pipeline.py`

Expected: collection or assertion failures because `build_manual.py`, `verify_manual.py`, the schema, and manual routing do not exist.

### Task 2: Build the self-contained manual pipeline

**Files:**
- Create: `skills/korean-ebook/scripts/manual_common.py`
- Create: `skills/korean-ebook/scripts/build_manual.py`
- Create: `skills/korean-ebook/scripts/verify_manual.py`
- Create: `skills/korean-ebook/assets/manual-template.html`
- Create: `skills/korean-ebook/assets/manual.css`
- Create: `skills/korean-ebook/assets/manual-config.example.yaml`

**Interfaces:**
- `manual_common.load_manual(path: Path) -> dict[str, Any]`
- `manual_common.validate_source_contract(data, root) -> list[Issue]`
- `build_manual.build(manifest_path: Path, output_dir: Path) -> dict[str, Any]`
- `verify_manual.verify(manifest_path: Path, package_dir: Path, visual_reviewed: bool = False) -> dict[str, Any]`

- [ ] **Step 1: Implement schema and path safety**

Require manual identity/status/version, overview mental model, workflows, lessons, sources, step `action/evidence/success`, risk approval fields, unique IDs, and package-root-contained local paths.

- [ ] **Step 2: Implement deterministic package generation**

Generate `index.html`, `overview.html`, standalone lesson pages, shared CSS, evidence map, build report, normalized manifest, `STATUS.md`, and `HANDOFF.md`. Copy only manifest-referenced media.

- [ ] **Step 3: Implement independent verification**

Check required files, HTML parseability, internal links, referenced media, teaching-depth sections, evidence coverage, forbidden placeholders/leaked Markdown, final/provisional truthfulness, and separate technical/content/visual verdicts.

- [ ] **Step 4: Verify GREEN**

Run: `/mnt/d/DEV/KLIC-BOOK/.venv/bin/python -m pytest -q skills/korean-ebook/tests/test_manual_pipeline.py`

Expected: all manual pipeline tests pass.

### Task 3: Reframe the skill around artifact routing

**Files:**
- Modify: `skills/korean-ebook/SKILL.md`
- Create: `skills/korean-ebook/references/manual-production.md`
- Create: `skills/korean-ebook/references/manual-quality-gates.md`
- Create: `skills/korean-ebook/references/manual-media.md`
- Modify: `skills/korean-ebook/references/input-contract.md`
- Modify: `skills/korean-ebook/references/output-contract.md`
- Modify: `skills/korean-ebook/references/quality-gates.md`
- Modify: `skills/korean-ebook/agents/openai.yaml`
- Modify: `skills/korean-ebook/evals/trigger_cases.json`
- Modify: `skills/korean-ebook/evals/quality_cases.md`
- Modify: `skills/korean-ebook/examples/prompt-examples.md`
- Modify: `skills/korean-ebook/README.ko.md`

**Interfaces:**
- Consumes: user intent for a book, manual, or both
- Produces: explicit `book`, `manual`, or `hybrid` routing and progressive disclosure to the correct references/scripts

- [ ] **Step 1: Rewrite the trigger and top-level flow**

Keep `SKILL.md` under 500 body lines. Put only artifact selection, shared boundaries, the two workflows, safety rules, and completion criteria in the body.

- [ ] **Step 2: Add focused manual references**

Document real-work inventory, beginner overview, workflow/lesson depth, risk/approval gates, evidence tiers, media escalation, and three-axis QA without backup-specific names or external skill dependencies.

- [ ] **Step 3: Update examples and UI metadata**

Add positive trigger cases for operator/admin/onboarding/SOP manuals and negative cases for marketing pages, API references, and fictional click paths. Update the default prompt to perform the artifact gate first.

- [ ] **Step 4: Run routing and quality contract tests**

Run: `/mnt/d/DEV/KLIC-BOOK/.venv/bin/python -m pytest -q skills/korean-ebook/tests`

Expected: manual and existing summary tests pass.

### Task 4: Package, validate, and publish

**Files:**
- Modify: `skills/korean-ebook/scripts/validate_skill.py`
- Modify: `skills/korean-ebook/manifest.txt`
- Modify: `skills/korean-ebook/SHA256SUMS`
- Modify: `skills/korean-ebook/VERSION`
- Modify: `skills/korean-ebook/CHANGELOG.md`

**Interfaces:**
- Consumes: the complete skill tree
- Produces: a self-consistent distributable skill with no hidden backup dependency

- [ ] **Step 1: Strengthen package validation**

Require the new manual scripts, template, CSS, and manual references when the skill description claims manual support. Reject backup/Hermes external dependency strings in executable skill instructions.

- [ ] **Step 2: Refresh manifest and checksums**

Generate the sorted tracked-file manifest and SHA-256 entries for every distributable file except `SHA256SUMS`, test cache, and local virtual environments.

- [ ] **Step 3: Run full verification**

Run the skill tests, FactoryX book tests, `validate_skill.py`, all skill checksums, compileall, and a clean minimal-manual build/verify round trip.

- [ ] **Step 4: Commit and publish**

Create focused commits, push `feat/integrate-manual-production`, open a PR to `main`, verify the PR head SHA, and merge only after the same verification passes on the remote-facing branch.
