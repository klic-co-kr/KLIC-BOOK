# Book PDF Downloads Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish the FactoryX book package and expose direct PDF download links for all completed books from the repository README.

**Architecture:** Keep each PDF in its existing book directory and use repository-relative Markdown links with `?raw=1`. A focused pytest contract checks that every catalog entry resolves to a tracked PDF.

**Tech Stack:** Markdown, Git, Python 3.12, pytest, pdfinfo, sha256sum

## Global Constraints

- Base all remote-facing changes on `origin/main`.
- Do not modify existing book PDFs.
- Preserve the user-owned untracked `AGENTS.md` in the original workspaces.
- Do not push the unrelated local `main` history.

---

### Task 1: Record the approved design

**Files:**
- Create: `docs/superpowers/specs/2026-08-12-book-pdf-downloads-design.md`
- Create: `docs/superpowers/plans/2026-08-12-book-pdf-downloads.md`

**Interfaces:**
- Consumes: the approved requirement to upload the built books and link them from README
- Produces: the exact catalog and verification contract used by Task 2

- [ ] **Step 1: Check the documents for placeholders**

Run: `rg -n 'T[B]D|T[O]DO|implement la[t]er|fill [i]n' docs/superpowers`
Expected: no matches.

- [ ] **Step 2: Commit the approved documentation**

Run: `git add docs/superpowers && git commit -m "docs: design book PDF downloads"`
Expected: one documentation commit on `docs/publish-factoryx-downloads`.

### Task 2: Publish the books and download catalog

**Files:**
- Create: `tests/test_readme_downloads.py`
- Modify: `README.md`
- Create: `books/factoryx-ai-infrastructure/**`
- Modify: `books/factoryx-ai-infrastructure/README.md`

**Interfaces:**
- Consumes: five repository-relative PDF paths
- Produces: five `?raw=1` Markdown links whose targets are tracked PDF files

- [ ] **Step 1: Add a failing README download contract**

The test parses the five expected `?raw=1` links from `README.md`, asserts their targets exist, start with `%PDF-`, and are tracked by Git.

- [ ] **Step 2: Verify the contract fails before implementation**

Run: `/mnt/d/DEV/KLIC-BOOK/.venv/bin/python -m pytest -q tests/test_readme_downloads.py`
Expected: failure because the root README has no download links and FactoryX is absent.

- [ ] **Step 3: Restore FactoryX and add the README links**

Run: `git restore --source=24460e5 -- books/factoryx-ai-infrastructure`, then update both README files with the approved links.
Expected: the five links resolve to existing PDFs.

- [ ] **Step 4: Verify downloads and publication integrity**

Run: `/mnt/d/DEV/KLIC-BOOK/.venv/bin/python -m pytest -q tests/test_readme_downloads.py`
Expected: all download-link tests pass.

Run: `/mnt/d/DEV/KLIC-BOOK/.venv/bin/python books/factoryx-ai-infrastructure/scripts/validate_book.py --root books/factoryx-ai-infrastructure --require-build`
Expected: `VALID: chapters=12 figures=12 charts=8 sources=37 pages=100`.

Run: `sha256sum -c books/factoryx-ai-infrastructure/SHA256SUMS`
Expected: all listed artifacts report `OK`.

- [ ] **Step 5: Commit the publication**

Run: `git add README.md books/factoryx-ai-infrastructure tests/test_readme_downloads.py && git commit -m "docs: publish FactoryX book downloads"`
Expected: the publication and link contract are committed together.

### Task 3: Publish through GitHub

**Files:**
- No additional repository files.

**Interfaces:**
- Consumes: verified branch `docs/publish-factoryx-downloads`
- Produces: a GitHub pull request merged into `main`

- [ ] **Step 1: Push the branch and create a PR**

Run: `git push -u origin docs/publish-factoryx-downloads` and create a PR against `main`.
Expected: GitHub returns a PR URL.

- [ ] **Step 2: Verify the remote PR and merge it**

Run the same focused tests on the PR head, confirm the expected head SHA, then merge without force-pushing.
Expected: the PR state is `MERGED` and no open PR remains for this branch.
