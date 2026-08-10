"""tests/test_evals.py — eval suite 계약 테스트 (Task 8).

검증 대상:
- judgment_cases.json 스키마 (eval 전용 — CandidateFile과 별 스키마)
- judgment_comparator.py 의 check_segments_cover_golden 결정론 회그
- skill_utility.md / stability.md / recall_cases.md 문서 계약
"""
import json
import pathlib

EVALS = pathlib.Path(__file__).resolve().parents[1] / "evals"
FIXTURES = pathlib.Path(__file__).resolve().parent / "fixtures"


# --- judgment_cases.json (eval 전용 골든) ------------------------------------

def test_judgment_cases_schema():
    d = json.loads((EVALS / "judgment_cases.json").read_text(encoding="utf-8"))
    assert "golden_must_extract" in d and len(d["golden_must_extract"]) >= 2
    for g in d["golden_must_extract"]:
        assert all(k in g for k in ("id", "category", "title_keyword", "source_ref"))


def test_judgment_cases_separate_from_candidate_schema():
    """BLOCKER 방어: eval 골든은 CandidateFile 필드(title/source_refs/rubric)를
    사용하지 않는다. 스키마 분리 계약."""
    d = json.loads((EVALS / "judgment_cases.json").read_text(encoding="utf-8"))
    for g in d["golden_must_extract"]:
        # eval-only 필드
        assert "title_keyword" in g and "source_ref" in g
        # CandidateFile 필드가 뒤섞이지 않았는지 확인 (분리 계약)
        assert "title" not in g, "eval 골든에 CandidateFile의 title 필드가 섞임"
        assert "rubric" not in g, "eval 골든에 CandidateFile의 rubric 필드가 섞임"
        assert "approved" not in g, "eval 골든에 CandidateFile의 approved 필드가 섞임"


# --- judgment_comparator.py (결정론 회그) ------------------------------------

def test_comparator_importable():
    from evals.judgment_comparator import check_segments_cover_golden  # noqa: F401


def test_comparator_covers_ch02_golden():
    """ch02 fixture는 골든 source절을 모두 포함해야 → missed == []."""
    from evals.judgment_comparator import check_segments_cover_golden

    golden = json.loads((EVALS / "judgment_cases.json").read_text(encoding="utf-8"))[
        "golden_must_extract"
    ]
    ch_text = (FIXTURES / "02-제2장-올바른문제풀기.md").read_text(encoding="utf-8")
    missed = check_segments_cover_golden(ch_text, golden)
    assert missed == [], f"골든 source절이 ch02에서 누락: {missed}"


def test_comparator_detects_missing_section():
    from evals.judgment_comparator import check_segments_cover_golden

    # 존재하지 않는 절 + 존재하지 않는 키워드 → 누락 보고
    golden = [
        {"id": "ghost-1", "category": "x", "title_keyword": "절대없는키워드XYZ",
         "source_ref": "ch99§9.9"}
    ]
    missed = check_segments_cover_golden("# 가짜 챕터\n본문 없음", golden)
    assert missed == ["ghost-1"]


def test_comparator_section_token_is_discriminating():
    # 브리프 v1 buggy 형태 split(".")[0] 은 "2.2" → "2" 로 축소해 거의 항상 통과해
    # 버린다(느슨함). 전체 절 토큰("2.2")을 요구하는지 판별하는 회귀 방어.
    #
    # 이 텍스트는 bare "2"(예: "2.1"·"02")는 포함하지만 "2.2" 헤더는 없다.
    # 키워드도 없다. 따라서:
    #   - fixed (전체 토큰 "2.2"): "2.2" not in text + keyword 없음 → missed == ["x"]
    #   - buggy  (split(".")[0] → "2"): "2" in text → 통과 → missed == []  (이 테스트 실패)
    from evals.judgment_comparator import check_segments_cover_golden

    text = "## 2.1 다른 절\nchapter 02 내용"  # "2.2" 헤더 없음, bare "2" 는 있음
    golden = [
        {"id": "x", "category": "x", "title_keyword": "절대없는키워드XYZ",
         "source_ref": "ch02§2.2"}
    ]
    missed = check_segments_cover_golden(text, golden)
    assert missed == ["x"], (
        "전체 절 토큰(2.2)이 아닌 split('.')[0](2) 축소가 도입되면 "
        "이 어서션이 깨져야 한다 — 느슨한 매칭 회귀 방어"
    )


# --- skill_utility.md (정성 루브릭) ------------------------------------------

def test_skill_utility_exists():
    assert (EVALS / "skill_utility.md").exists()
    txt = (EVALS / "skill_utility.md").read_text(encoding="utf-8")
    assert "held-out" in txt and "루브릭" in txt


# --- stability.md (Jaccard 3×2 게이트) ---------------------------------------

def test_stability_contract():
    txt = (EVALS / "stability.md").read_text(encoding="utf-8")
    assert "0.5" in txt and "Jaccard" in txt


# --- recall_cases.md (사례 단위 회상) ----------------------------------------

def test_recall_cases_exists():
    assert (EVALS / "recall_cases.md").exists()
    txt = (EVALS / "recall_cases.md").read_text(encoding="utf-8")
    assert "사례 단위" in txt or "사례단위" in txt
