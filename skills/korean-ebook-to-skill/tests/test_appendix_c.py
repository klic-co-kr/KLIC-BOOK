# tests/test_appendix_c.py
from pathlib import Path
from korean_ebook_to_skill.chapters import parse_chapter_file
from korean_ebook_to_skill.appendix_c import parse_cases, compute_recall

CF = parse_chapter_file(Path("tests/fixtures/12-부록C-사례색인및출처.md"))


def test_parse_cases_case_level_not_chapter_buckets():
    cases = parse_cases(CF)
    ids = {c.case_id for c in cases}
    assert "1장-1" in ids and "1장-2" in ids
    assert all(c.chapter.endswith("장") for c in cases)
    assert len(cases) >= 4  # 적어도 번호 항목 수


def test_parse_cases_ignores_part2_sources():
    cases = parse_cases(CF)
    # 제2부 자료출처의 '서문/1장' 항목은 사례 아님 → case_id에 "서문" 없음
    assert not any("서문" in c.case_id for c in cases)


def test_compute_recall_case_granularity():
    cases = [c for c in parse_cases(CF)]  # 1장-1,1장-2,...
    # 한 후보가 1장-1만 커버
    res = compute_recall([{"appendix_c_refs": ["1장-1"]}], cases)
    assert res.coverage < 0.5
    assert "1장-1" in res.covered
    assert "1장-2" in res.uncovered


def test_recall_real_ref_matches_parsed_doc():
    """비순환 통합테스트: 실제 fixture를 파싱한 뒤 candidate ref "2장-1"과 매칭.

    예전 코드는 markdown 전역 번호를 그대로 써서 2장 첫 사례가 "2장-4"가 되었고,
    candidate convention "2장-1"(장별 로컬 순번)과 불일치하여 회상률 0.
    장별 로컬 카운터 수정 후 "2장-1"이 파싱 결과에 존재해야 한다.
    """
    cases = parse_cases(CF)  # 실제 fixture 파싱 (fabrication 없음)
    res = compute_recall([{"appendix_c_refs": ["2장-1"]}], cases)
    assert "2장-1" in res.covered
    assert res.coverage > 0.0
