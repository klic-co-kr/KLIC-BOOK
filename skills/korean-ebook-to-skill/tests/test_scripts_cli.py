# tests/test_scripts_cli.py
import subprocess, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]          # 스킬 루트
# NOTE: brief v1 had parents[2] → /mnt/d/DEV/acc0mplish (books/ 없음, 빈 glob).
# ROOT=스킬루트이므로 저장소 루트(KLIC-BOOK)는 parents[1]. off-by-one 수정.
BOOK = str((ROOT.parents[1] / "books" / "forward-deployed-engineer").resolve())
CANDS = str(ROOT / "tests" / "fixtures" / "candidates.yaml")  # CandidateFile 준거

def run(*args):
    # timeout=120: a hung script fails the test loudly instead of hanging the suite (Q2 fix).
    return subprocess.run(["python3", *args], capture_output=True, text=True, cwd=str(ROOT), timeout=120)

def test_extract_writes_outputs(tmp_path):
    r = run(str(ROOT/"scripts/extract.py"), BOOK, str(tmp_path))
    assert r.returncode == 0, r.stderr
    import json
    data = json.loads((tmp_path/"chapters.json").read_text(encoding="utf-8"))
    assert any(c["kind"] == "chapter" for c in data)
    assert (tmp_path/"full_text.txt").stat().st_size > 0
    assert (tmp_path/"candidates.template.yaml").exists()
    assert any(c["content_type"] == "anthology" for c in data), "ch8 should classify ANTHOLOGY on real FDE"

def test_gen_with_approved_candidates(tmp_path):
    work = tmp_path/"work"; out = tmp_path/"skill"
    run(str(ROOT/"scripts/extract.py"), BOOK, str(work))
    r = run(str(ROOT/"scripts/gen_knowledge.py"), BOOK, "--candidates", CANDS,
            "--work", str(work), "--out", str(out))
    assert r.returncode == 0, r.stderr
    assert (out/"SKILL.md").exists()
    assert (out/"extraction-report.md").exists()

def test_gen_rejects_without_approval_log(tmp_path):
    import yaml
    work = tmp_path/"work"; out = tmp_path/"skill"
    run(str(ROOT/"scripts/extract.py"), BOOK, str(work))
    bad = tmp_path/"no_log.yaml"
    d = yaml.safe_load((ROOT/"tests"/"fixtures"/"candidates.yaml").read_text(encoding="utf-8"))
    d["approval_log"] = []
    bad.write_text(yaml.safe_dump(d, allow_unicode=True), encoding="utf-8")
    r = run(str(ROOT/"scripts/gen_knowledge.py"), BOOK, "--candidates", str(bad),
            "--work", str(work), "--out", str(out))
    assert r.returncode != 0 and "approval_log" in (r.stdout+r.stderr)


def test_gen_writes_appendix_c_map_note_when_no_index(tmp_path):
    """회귀: 부록C(INDEX) 챕터가 없는 책도 appendix-c-map.md 가
    '회상 기준 부재' 노트로 작성된다 (spec §8 위험완화).

    이 분기는 recall=None 경로를 실제로 실행한다 — Fix 1 의 RecallResult(0.0,[],[])
    전달 + Fix 2 의 else-노트 작성. 기존 테스트는 FDE(항상 INDEX 보유)만
    커버하여 이 경로가 검증된 적 없었다.
    """
    import yaml
    # 1. 부록C 없는 임시 book_dir 합성 (prose 챕터 1개만)
    book = tmp_path / "noindex-book"
    book.mkdir()
    (book / "01-prose.md").write_text(
        "# 제1장 서론\n\n본문 단락. 부록C 사례 색인 없음.\n",
        encoding="utf-8",
    )
    # 2. approval_log 포함 candidates.yaml (book_title 은 노트에 찍히는지 확인용)
    cands = tmp_path / "cands.yaml"
    d = {
        "book_slug": "noindex-book",
        "book_title": "부록C 없는 책",
        "generated_date": "2026-08-10",
        "version": "1.0",
        "approval_log": [
            {"approved_at": "2026-08-10", "approved_by": "test", "n_approved": 1}
        ],
        "candidates": [
            {
                "id": "principle-1",
                "category": "principle",
                "title": "테스트 원칙",
                "summary": "no-index 회귀용",
                "support_chain": ["요약 근거"],
                "appendix_c_refs": [],
                "source_refs": ["ch01§1.1"],
                "rubric": {
                    "actionable": 3, "generalizable": 4,
                    "non_obvious": 3, "evidenced": 3,
                    "genericity_penalty": 0,
                    "rationale": "no-index 회귀",
                },
                "approved": True,
            }
        ],
    }
    cands.write_text(yaml.safe_dump(d, allow_unicode=True), encoding="utf-8")
    # 3. extract → gen
    work = tmp_path / "work"; out = tmp_path / "skill"
    r = run(str(ROOT/"scripts/extract.py"), str(book), str(work))
    assert r.returncode == 0, r.stderr
    r = run(str(ROOT/"scripts/gen_knowledge.py"), str(book),
            "--candidates", str(cands), "--work", str(work), "--out", str(out))
    assert r.returncode == 0, r.stderr
    # 4. appendix-c-map.md 작성 + 노트 포함 (Fix 2)
    am = out / "appendix-c-map.md"
    assert am.exists(), "appendix-c-map.md should be written even when no INDEX chapter"
    body = am.read_text(encoding="utf-8")
    assert "회상 기준 부재" in body, f"missing note; got:\n{body}"
    # extraction-report.md 도 정상 작성 (Fix 1 — RecallResult 경로, AttributeError 없음)
    assert (out / "extraction-report.md").exists()
