import pytest
from pathlib import Path
from korean_ebook_to_skill.candidates import load_candidates, dump_candidates, CandidateFile

def test_load():
    cf = load_candidates(Path("tests/fixtures/candidates.yaml"))
    assert cf.book_slug == "forward-deployed-engineer"
    assert cf.candidates[0].rubric.actionable == 5
    assert cf.candidates[0].appendix_c_refs == ["2장-1"]
    assert cf.approval_log and cf.approval_log[0]["approved_by"] == "human"

def test_invalid_category_rejected():
    bad = {"book_slug":"x","book_title":"x","generated_date":"2026-08-10","version":"1.0",
           "approval_log":[], "candidates":[{"id":"x","category":"bogus","title":"t","summary":"s",
           "support_chain":[],"appendix_c_refs":[],"source_refs":[],
           "rubric":{"actionable":1,"generalizable":1,"non_obvious":1,"evidenced":1,
           "genericity_penalty":0,"rationale":"r"},"approved":True}]}
    with pytest.raises(Exception): CandidateFile.model_validate(bad)

def test_dump_roundtrip(tmp_path):
    cf = load_candidates(Path("tests/fixtures/candidates.yaml"))
    p = tmp_path / "out.yaml"; dump_candidates(cf, p)
    cf2 = load_candidates(p)
    assert cf2.candidates[0].id == "psf-3gate"
