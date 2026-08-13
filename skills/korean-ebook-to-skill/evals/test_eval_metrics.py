"""test_eval_metrics.py — 책→스킼 판단 품질 메트릭 TDD (논문 시사점).

메트릭:
- precision: AI 후보 중 골든(인간 정답) 매칭 비율
- recall:    골든 중 AI 후보 커버 비율
- adoption:  승인(approved) 후보 / 전체 후보 (게이트 통과율)
- rounds:    approval_log 라운드 수 (인간 개입)
매칭: id 일치 OR source_ref 겹침 OR title_keyword 포함.
"""
import json, textwrap
from pathlib import Path


def _write(tmp, cands, golden, approval_log):
    cf = tmp / "candidates.yaml"
    cf.write_text(textwrap.dedent(cands), encoding="utf-8")
    g = tmp / "golden.json"
    g.write_text(json.dumps(golden, ensure_ascii=False), encoding="utf-8")
    return cf, g


def test_perfect(tmp_path):
    from evals.eval_metrics import compute_metrics
    cands = """
approval_log: [{approved_at: x}]
candidates:
  - id: psf-3gate
    category: methodology
    title: PSF 3관문
    source_refs: ["ch02§2.2"]
    approved: true
  - id: poc-purgatory
    category: research
    title: POC 연옥
    source_refs: ["ch02§2.1"]
    approved: true
"""
    golden = {"golden_must_extract": [
        {"id": "psf-3gate", "source_ref": "ch02§2.2", "title_keyword": "PSF"},
        {"id": "poc-purgatory", "source_ref": "ch02§2.1", "title_keyword": "POC"}]}
    cf, g = _write(tmp_path, cands, golden, 1)
    m = compute_metrics(str(cf), str(g))
    assert m["precision"] == 1.0
    assert m["recall"] == 1.0
    assert m["adoption"] == 1.0
    assert m["f1"] == 1.0
    assert m["rounds"] == 1
    assert m["n_golden"] == 2 and m["n_candidates"] == 2


def test_partial_with_noise(tmp_path):
    """1 골든 매칭 + 1 비정답 후보 + 1 미승인."""
    from evals.eval_metrics import compute_metrics
    cands = """
approval_log: [{approved_at: x}, {approved_at: y}]
candidates:
  - id: psf-3gate
    category: methodology
    title: PSF 3관문
    source_refs: ["ch02§2.2"]
    approved: true
  - id: noise-1
    category: principle
    title: 의미없는 통찰
    source_refs: ["ch02§9.9"]
    approved: false
"""
    golden = {"golden_must_extract": [
        {"id": "psf-3gate", "source_ref": "ch02§2.2", "title_keyword": "PSF"},
        {"id": "poc-purgatory", "source_ref": "ch02§2.1", "title_keyword": "POC"}]}
    cf, g = _write(tmp_path, cands, golden, 2)
    m = compute_metrics(str(cf), str(g))
    assert m["precision"] == 0.5    # 1 매칭 / 2 후보
    assert m["recall"] == 0.5       # 1 골든 / 2
    assert m["adoption"] == 0.5     # 1 승인 / 2
    assert m["rounds"] == 2


def test_no_false_partial_match(tmp_path):
    """source_ref 부분문자열 오탐 방지: ch02§2.2 ≠ ch02§2.22."""
    from evals.eval_metrics import compute_metrics
    cands = """
approval_log: []
candidates:
  - id: x
    category: methodology
    title: 다른 것
    source_refs: ["ch02§2.22"]
    approved: false
"""
    golden = {"golden_must_extract": [
        {"id": "psf-3gate", "source_ref": "ch02§2.2", "title_keyword": "PSF"}]}
    cf, g = _write(tmp_path, cands, golden, 0)
    m = compute_metrics(str(cf), str(g))
    assert m["precision"] == 0.0    # ch02§2.22 ≠ ch02§2.2 (부분 매칭 X)
    assert m["recall"] == 0.0
