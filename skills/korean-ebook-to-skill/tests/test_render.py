# tests/test_render.py
"""Task 6: 지식층 렌더 — extraction-report(루브릭 가시화) + description 포함.

명세 수정 사항(spec-correction) 반영:
- render_skill_md frontmatter에 ``description:`` 필수 (v1 누락 → 스킬 미발견).
- render_extraction_report 루브릭 점수 + genericity 벌점 + rationale 가시화
  (v1은 루브릭을 렌더하지 않아 게이트가 무효했음).
"""
from pathlib import Path
from korean_ebook_to_skill.candidates import load_candidates
from korean_ebook_to_skill.chapters import parse_chapter_file
from korean_ebook_to_skill.appendix_c import compute_recall
from korean_ebook_to_skill.render import (render_skill_md, render_chapter_md,
    render_appendix_c_map, render_extraction_report)
from korean_ebook_to_skill.models import Case

CF = load_candidates(Path("tests/fixtures/candidates.yaml"))


def test_skill_md_groups_and_evidence():
    md = render_skill_md(CF, recall_score=0.1)
    assert md.startswith("---")
    assert "description:" in md            # 발견 가능
    assert "## 방법론" in md
    assert "PSF 3관문 검증" in md
    assert "ch02§2.2" in md


def test_chapter_md_renders_headings():
    cf = parse_chapter_file(Path("tests/fixtures/02-제2장-올바른문제풀기.md"))
    md = render_chapter_md(cf)
    assert "2장 올바른 문제 풀기" in md
    assert "2.1" in md and "2.2" in md


def test_appendix_c_map_recall():
    cases = [Case("1장-1","1장",None,1,"x"), Case("2장-1","2장",None,1,"y")]
    recall = compute_recall([c.model_dump() for c in CF.candidates], cases)
    md = render_appendix_c_map(recall, CF)
    assert "회상율" in md and "2장-1" in md


def test_extraction_report_shows_rubric():
    cases = [Case("2장-1","2장",None,1,"y")]
    recall = compute_recall([c.model_dump() for c in CF.candidates], cases)
    md = render_extraction_report(CF, recall)
    assert "PSF 3관문 검증" in md
    assert "actionable" in md or "실행가능" in md   # 루브릭 가시화
    assert "genericity" in md or "벌점" in md
    assert "approved" in md.lower() or "승인" in md
