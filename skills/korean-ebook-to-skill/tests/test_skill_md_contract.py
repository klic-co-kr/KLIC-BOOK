"""tests/test_skill_md_contract.py — SKILL.md 오케스트레이션 계약 테스트 (Task 9).

SKILL.md 는 에이전트가 따르는 "스킬의 영혼"이다. 이 파일이 위험 아티팩트:
- CLI 스크립트 경로/이름이 바뀌면 워크플로우가 끊긴다.
- 5카테고리/5루브릭 키가 코드 스키마(candidates.py)와 불일치하면 게이트가 무효.
- 한국어 섹션 헤더가 사라지면 에이전트가 섹션을 못 찾는다.
- approval_log 언급이 없으면 사람 게이트가 은연중 건너뛰어질 수 있다.

이 테스트는 SKILL.md 의 정체성·구조·키 문자열을 동결하여 조용한 회귀를 잡는다.
"""
import pathlib

SK = pathlib.Path(__file__).resolve().parents[1] / "SKILL.md"


def test_skill_md_exists():
    assert SK.exists(), f"SKILL.md 가 없음: {SK}"


def test_skill_md_contract():
    md = SK.read_text(encoding="utf-8")
    # frontmatter + 정체성
    assert md.startswith("---") and "name: korean-ebook-to-skill" in md
    assert "description:" in md
    # 필수 한국어 섹션 헤더 (에이전트 탐색용)
    for h in ("워크플로우", "판단 루브릭", "근거", "한국어"):
        assert h in md, f"필수 섹션 헤더 누락: {h}"
    # 3 CLI — 워크플로우 단계별 정확 명령
    for cli in ("scripts/extract.py", "scripts/gen_knowledge.py", "scripts/validate.py"):
        assert cli in md, f"CLI 경로 누락: {cli}"
    # 5카테고리 — candidates.py CATEGORIES 와 일치
    for cat in ("methodology", "research", "solution", "principle", "anti-pattern"):
        assert cat in md, f"카테고리 키 누락: {cat}"
    # 5루브릭 키 — candidates.py Rubric 필드와 일치
    for crit in ("actionable", "generalizable", "non_obvious", "evidenced", "genericity"):
        assert crit in md, f"루브릭 키 누락: {crit}"
    # skill-utility 평가 절차 링크
    assert "skill_utility" in md or "skill-utility" in md
    # 사람 게이트 메커니즘
    assert "approval_log" in md
