#!/usr/bin/env python3
"""evals/judgment_comparator.py — 골든 비교 (결정론층만).

실제 판단(후보가 골든을 얼마나 질적으로 충족하는가)은 에이전트가 수행하며
SKILL.md Task 9에서 수동/반자동 채점한다. 이 스크립트는 그 아래 **결정론 회그**만
담당한다: extract.py의 세그먼트 감지 결과(=원문 챕터 markdown)가 골든이 지정한
소스절(source_ref)을 커버하는지 검사한다.

채용 의미:
- 원문에 해당 절 헤더(또는 title_keyword)가 아예 없으면 extract.py가 세그먼트를
  만들 수 없으므로 → 확정 누락(missing).
- 원문에 절/키워드가 있으면 세그먼트는 만들어졌을 것 → 결정론층 통과.
  (후보의 질적 충족 여부는 이 스크립트 범위 밖 — 수동 평가로 간다.)

CLI:
    python3 evals/judgment_comparator.py <golden.json> <chapter.md>
    exit 0 = 전부 커버됨 / exit 1 = 누락 존재
"""
import json
import sys
from pathlib import Path


def _section_token(source_ref: str) -> str:
    """source_ref에서 절 식별자 추출. ``ch02§2.2`` → ``2.2``.

    ``§`` 가 없거나 뒤가 비면 빈 문자열(이 경우 title_keyword로만 판정).
    v1 브리프 pseudocode는 ``split(".")[0]`` 로 ``2.2`` → ``2`` 로 축소해
    거의 항상 통과해버리는 느슨함이 있었다. 여기서는 **전체 절 토큰**(2.2)을
    써서 헤더 마커를 정확히 검사한다.
    """
    if "§" in source_ref:
        tail = source_ref.split("§", 1)[1].strip()
        return tail
    return ""


def check_segments_cover_golden(chapter_md_text, golden):
    """결정론 회그: 골든 source_ref 절이 챕터 원문에 커버되는지.

    Args:
        chapter_md_text: 챕터 markdown 원문 (extract.py 입력 소스).
        golden: ``[{id, category, title_keyword, source_ref}, ...]`` 골든 목록.

    Returns:
        list[str]: 커버되지 않은 골든 id 들 (빈 리스트 = 전부 커버).
    """
    missed = []
    for g in golden:
        section = _section_token(g.get("source_ref", ""))
        keyword = g.get("title_keyword", "")
        section_present = bool(section) and section in chapter_md_text
        keyword_present = bool(keyword) and keyword in chapter_md_text
        if not (section_present or keyword_present):
            missed.append(g["id"])
    return missed


def main(argv):
    golden_path = Path(argv[1])
    chapter_path = Path(argv[2])
    golden = json.loads(golden_path.read_text(encoding="utf-8"))["golden_must_extract"]
    ch_text = chapter_path.read_text(encoding="utf-8")
    missed = check_segments_cover_golden(ch_text, golden)
    print("MISSING:", missed if missed else "none")
    return 1 if missed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
