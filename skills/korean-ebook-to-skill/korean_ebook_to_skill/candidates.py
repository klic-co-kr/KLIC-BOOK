# korean_ebook_to_skill/candidates.py
"""candidates YAML 스키마 + load/dump + approval_log.

Candidate.appendix_c_refs 형식 pin: ``"N장-M"`` (예: ``"2장-1"``).
이는 부록C 사례의 case_id(``korean_ebook_to_skill.appendix_c.parse_cases``)와
정확히 매칭되어 회상률 산정(``compute_recall``)의 기준이 된다.
"""
from pathlib import Path
from pydantic import BaseModel, Field, field_validator
import yaml

CATEGORIES = {"methodology", "research", "solution", "principle", "anti-pattern"}


class Rubric(BaseModel):
    actionable: int = Field(ge=1, le=5)
    generalizable: int = Field(ge=1, le=5)
    non_obvious: int = Field(ge=1, le=5)
    evidenced: int = Field(ge=1, le=5)
    genericity_penalty: int = Field(ge=-5, le=0)
    rationale: str


class Candidate(BaseModel):
    id: str
    category: str
    title: str
    summary: str
    support_chain: list[str]
    appendix_c_refs: list[str] = []   # 형식 "N장-M" (예 "2장-1") — 부록C 사례 case_id와 매칭
    source_refs: list[str]            # 형식 "chNN§N.M"
    rubric: Rubric
    approved: bool = False

    @field_validator("category")
    @classmethod
    def _cat(cls, v):
        if v not in CATEGORIES:
            raise ValueError(f"category must be in {sorted(CATEGORIES)}")
        return v


class CandidateFile(BaseModel):
    book_slug: str
    book_title: str
    generated_date: str
    version: str
    approval_log: list[dict] = []
    candidates: list[Candidate]


def load_candidates(path) -> CandidateFile:
    return CandidateFile.model_validate(
        yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    )


def dump_candidates(cf: CandidateFile, path) -> None:
    Path(path).write_text(
        yaml.safe_dump(cf.model_dump(mode="json"), allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
