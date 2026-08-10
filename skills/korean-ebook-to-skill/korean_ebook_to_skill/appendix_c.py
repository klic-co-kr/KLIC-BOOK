# korean_ebook_to_skill/appendix_c.py
"""부록C 사례단위 파싱 + case-level 회상 (BLOCKER 수정).

v1 버그: chapter-bucket 파싱 + split(" ") 매칭 → "2장-1" 회상률 항상 0.
v2 수정: 사례(case) 단위 파싱 + case_id 집합 교집합 매칭.
"""
import re
from dataclasses import dataclass
from .models import ChapterFile, Case

PART1_RE = re.compile(r"## 제1부.*?(?=^## 제2부|\Z)", re.MULTILINE | re.DOTALL)
CHAPTER_HEAD_RE = re.compile(
    r"^###\s*(?P<chapters>\d+(?:[~–-]\d+)?)장(?:\s+(?P<section>\d+\.\d+)절)?\s*\((?P<inside>[^)]*)\)",
    re.MULTILINE,
)
ENTRY_RE = re.compile(r"^(?P<idx>\d+)\.\s+(?P<title>.+)$", re.MULTILINE)


@dataclass
class RecallResult:
    coverage: float
    covered: list
    uncovered: list


def parse_cases(cf: ChapterFile) -> list:
    """부록C 제1부에서 사례(case) 단위로 파싱.

    제2부 자료출처의 '서문 / 1장' 헤더는 사례가 아니므로 제외.
    범위 헤더(4~5장)는 첫 장(4장)으로 귀속.

    case_id는 **장별 로컬 순번**(candidate convention ``"N장-M"``과 일치).
    실제 문서는 전체 제1부에 걸쳐 연속 번호(1~120+)를 사용하므로,
    markdown 항목 번호(``idx``)를 그대로 쓰면 2장 첫 사례가 ``2장-34``가 되어
    candidate의 ``"2장-1"``과 불일치한다. 따라서 장 토큰이 바뀔 때
    로컬 카운터를 리셋하고, 같은 장의 절별 서브블록(예: ``1장 1.3절``)은
    카운터를 이어 받는다(연속 번호이므로 같은 장의 추가 사례).
    """
    m = PART1_RE.search(cf.raw_text)
    block = m.group(0) if m else cf.raw_text
    cases = []
    prev_chapter = None
    local_idx = 0
    for hm in CHAPTER_HEAD_RE.finditer(block):
        chap_token = hm.group("chapters")  # "1" or "4~5"
        section = hm.group("section")
        # 범위 헤더(4~5장)는 첫 장으로 귀속 (단순화)
        primary_chapter = re.split(r"[~–-]", chap_token)[0]
        ch = f"{primary_chapter}장"
        if ch != prev_chapter:
            local_idx = 0
            prev_chapter = ch
        region_start = hm.end()
        next_head = CHAPTER_HEAD_RE.search(block, hm.end())
        region_end = next_head.start() if next_head else len(block)
        for em in ENTRY_RE.finditer(block, region_start, region_end):
            local_idx += 1
            cases.append(
                Case(
                    case_id=f"{ch}-{local_idx}",
                    chapter=ch,
                    section=f"{section}절" if section else None,
                    index=local_idx,
                    title=em.group("title").strip(),
                )
            )
    return cases


def compute_recall(candidates: list, cases: list) -> RecallResult:
    """후보 appendix_c_refs("N장-M")와 case_id 집합 교집합으로 회상률 산출.

    v1 버그 회피: ref를 split/파싱하지 않고 그대로 case_id와 매칭.
    """
    covered_ids = set()
    for cand in candidates:
        for ref in cand.get("appendix_c_refs", []):
            covered_ids.add(ref.strip())  # "2장-1" 그대로
    all_ids = {c.case_id for c in cases}
    covered = sorted(all_ids & covered_ids)
    uncovered = sorted(all_ids - covered_ids)
    return RecallResult(len(covered) / (len(all_ids) or 1), covered, uncovered)
