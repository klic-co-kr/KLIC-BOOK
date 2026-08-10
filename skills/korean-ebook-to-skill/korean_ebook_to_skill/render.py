# korean_ebook_to_skill/render.py
"""지식층 렌더 — f-string 기반 (templates/knowledge.md dead code 사용 안 함).

명세 수정 사항(spec-correction) 반영:
- ``render_skill_md`` frontmatter에 ``description:`` 필수 — 스킬 발견 가능성 확보
  (v1은 ``description:`` 누락 → 주제 쿼리에 응답하지 못함, 리뷰어 지적).
- ``render_extraction_report`` 루브릭 4축 점수 + genericity 벌점 + rationale 렌더 —
  게이트(PSF 3관문)의 가시화 표면. v1은 루브릭을 렌더하지 않아 사실상 미사용.
"""
from .candidates import CandidateFile
from .models import ChapterFile
from .appendix_c import RecallResult

# 5개 카테고리 한국어 라벨 + 고정 출력 순서
CAT_KO = {
    "methodology": "방법론",
    "research": "연구",
    "solution": "해결책",
    "principle": "원칙",
    "anti-pattern": "안티패턴",
}
CAT_ORDER = ["methodology", "research", "solution", "principle", "anti-pattern"]


def _item_block(c) -> str:
    """승인된 후보 1개 → 지식층 항목 마크다운 블록 (근거 포함)."""
    return (
        f"### {c.title}\n\n{c.summary}\n\n"
        f"- **지지**: {' / '.join(c.support_chain) or '—'}\n"
        f"- **부록C 사례**: {', '.join(c.appendix_c_refs) or '—'}\n"
        f"- **원문 §**: {', '.join(c.source_refs) or '—'}\n"
    )


def render_skill_md(cf: CandidateFile, chapters=None, recall_score: float = 0.0) -> str:
    """지식층 SKILL.md 본문 렌더.

    ``chapters``는 호환 파라미터(시그니처 안정성). 본 렌더에서는 사용하지 않는다.
    """
    approved = [c for c in cf.candidates if c.approved]
    sections = []
    for cat in CAT_ORDER:
        items = [c for c in approved if c.category == cat]
        if items:
            blocks = "\n".join(_item_block(c) for c in items)
            sections.append(f"## {CAT_KO[cat]}\n\n{blocks}")
    idx = (
        "\n".join(f"- **{c.title}** → {', '.join(c.source_refs)}" for c in approved)
        or "—"
    )
    frontmatter = (
        "---\n"
        f"name: {cf.book_slug}-knowledge\n"
        f"description: \"{cf.book_title} 판단 추출 지식층 — 주제 쿼리 시 항목 + 근거(부록C/원문§) 응답\"\n"
        f"version: \"{cf.version}\"\n"
        f"book_slug: {cf.book_slug}\n"
        f"generated_date: \"{cf.generated_date}\"\n"
        f"recall_score: {recall_score:.2f}\n"
        "---\n"
    )
    body = "\n\n".join(sections)
    return (
        f"{frontmatter}"
        f"# {cf.book_title}\n\n"
        "> AI 판단 추출 가치내용. 주제로 쿼리하면 해당 항목 + 근거 응답.\n\n"
        f"{body}\n\n"
        f"## 색인\n{idx}\n"
    )


def render_chapter_md(cf: ChapterFile) -> str:
    """챕터 파일 → 헤딩 트리 마크다운."""
    lines = [f"# {cf.segments[0].title if cf.segments else cf.slug}"]
    for s in cf.segments[1:]:
        lines.append(f"\n{'#' * (s.level + 1)} {s.title}\n")
    return "\n".join(lines) + "\n"


def render_appendix_c_map(recall: RecallResult, cf: CandidateFile) -> str:
    """부록C 회상 보고 마크다운 (커버/누락 사례)."""
    covered = "\n".join(f"- {c}" for c in recall.covered) or "—"
    uncovered = "\n".join(f"- {c}" for c in recall.uncovered) or "—"
    return (
        f"# 부록C 회상 보고 — {cf.book_title}\n\n"
        f"**사례 회상율**: {recall.coverage:.1%}\n\n"
        f"## 커버된 사례\n{covered}\n\n"
        f"## 누락 사례\n{uncovered}\n"
    )


def render_extraction_report(cf: CandidateFile, recall: RecallResult) -> str:
    """추출 보고서 — 게이트 가시화 표면.

    후보별 테이블: id | 카테고리 | 제목 | 루브릭 4축(act/gen/non-obv/ev) |
    genericity 벌점 | approved | 원문§.  하위에 rationale + 승인 이력.
    """
    rows = []
    for c in cf.candidates:
        r = c.rubric
        rows.append(
            f"| {c.id} | {c.category} | {c.title} | "
            f"{r.actionable}/{r.generalizable}/{r.non_obvious}/{r.evidenced} | "
            f"{r.genericity_penalty} | {'Y' if c.approved else 'N'} | "
            f"{', '.join(c.source_refs)} |"
        )
    table = "\n".join(rows) if rows else "—"
    rationale = "\n".join(f"- **{c.id}**: {c.rubric.rationale}" for c in cf.candidates) or "—"
    log = (
        "\n".join(
            f"- {e.get('approved_at', '?')} by {e.get('approved_by', '?')}"
            for e in cf.approval_log
        )
        or "—"
    )
    return (
        f"# 추출 보고서 — {cf.book_title}\n\n"
        f"**사례 회상율**: {recall.coverage:.1%}\n\n"
        "## 후보\n\n"
        "루브릭 4축: actionable / generalizable / non_obvious / evidenced "
        "(각 1-5), genericity 벌점(0~-5). "
        "표 열: id | 카테고리 | 제목 | 루브릭(act/gen/non-obv/ev) | genericity벌점 | approved | 원문§\n\n"
        "| id | 카테고리 | 제목 | 루브릭(act/gen/non-obv/ev) | genericity벌점 | approved | 원문§ |\n"
        "|---|---|---|---|---|---|---|\n"
        f"{table}\n\n"
        f"## 루브릭 이유\n{rationale}\n\n"
        f"## 승인 이력\n{log}\n"
    )
