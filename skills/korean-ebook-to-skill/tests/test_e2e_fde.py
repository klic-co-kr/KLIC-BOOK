# tests/test_e2e_fde.py
"""E2E 통합테스트 — 전체 FDE 책에 대한 extract → gen → validate 파이프라인 회그 보호.

Task 10 캡스톤. 결정론 전 구간을 subprocess 로 구동하여:
1. extract.py 가 전체 FDE(12 파일)를 산출
2. gen_knowledge.py 가 fixture candidates(1 approved: psf-3gate)로 지식층 렌더
3. validate.py --strict 가 exit 0

그리고 품질 불변량을 검증한다:
- 콘텐츠타입 분포: 7 prose / 1 anthology / 1 afterword / 1 glossary / 1 roster / 1 index
- ch8(ANTHOLOGY) → 5 서브청크
- judgment_comparator 가 ch02 골든(2.1/2.2절) 누락 없음(MISSING: none)

주의: 본 테스트가 회상률이 낮은 것(1/129 ≈ 0.8%)은 정상이다. fixture candidate
1개만 승인했기 때문이며, 이는 파이프라인 자체를 증명할 뿐 사람+에이전트의
전체 판단 실행(SKILL.md Step 2, runtime)이 아니다. runtime 실행은 본 테스트
범위 밖(operational)이다.
"""
import json
import subprocess
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]            # 스킬 루트
# 저장소 루트(KLIC-BOOK) = ROOT.parents[1]. brief v1 의 parents[2] 는 off-by-one.
BOOK = str((ROOT.parents[1] / "books" / "forward-deployed-engineer").resolve())
FIXTURE_CANDIDATES = ROOT / "tests" / "fixtures" / "candidates.yaml"
GOLDEN = ROOT / "evals" / "judgment_cases.json"


def _run(*args, cwd=None):
    # timeout=120: hung script cannot hang the suite (Q2 fix). subprocess
    # returns CompletedProcess on success; raises TimeoutExpired → test fails loud.
    return subprocess.run(
        ["python3", *args], capture_output=True, text=True, cwd=cwd or str(ROOT),
        timeout=120,
    )


def test_pipeline_extract_gen_validate(tmp_path):
    """Step 1: 결정론 E2E — extract → gen → validate, 산출 3종 + exit 0."""
    work, out = tmp_path / "work", tmp_path / "skill"

    # 1. extract.py (전체 FDE)
    r = _run(str(ROOT / "scripts" / "extract.py"), BOOK, str(work))
    assert r.returncode == 0, r.stderr
    assert (work / "chapters.json").exists()
    assert (work / "full_text.txt").exists()
    assert (work / "candidates.template.yaml").exists()

    # 2. gen_knowledge.py — fixture candidates 복사 + approval_log 보강
    import yaml
    cands = tmp_path / "c.yaml"
    d = yaml.safe_load(FIXTURE_CANDIDATES.read_text(encoding="utf-8"))
    # fixture 는 이미 approval_log 1건을 가지지만 E2E 주체를 명시적으로 남긴다.
    d["approval_log"] = [
        {"approved_at": "2026-08-10", "approved_by": "e2e", "n_approved": 1}
    ]
    cands.write_text(yaml.safe_dump(d, allow_unicode=True), encoding="utf-8")
    r = _run(
        str(ROOT / "scripts" / "gen_knowledge.py"), BOOK,
        "--candidates", str(cands), "--work", str(work), "--out", str(out),
    )
    assert r.returncode == 0, r.stderr

    # 산출 3종 + 챕터 디렉토리
    for f in ("SKILL.md", "extraction-report.md", "appendix-c-map.md"):
        assert (out / f).exists(), f"missing output: {f}"
    assert out.joinpath("chapters").is_dir() and any(out.joinpath("chapters").iterdir())

    # 3. validate.py --strict → exit 0
    r = _run(str(ROOT / "scripts" / "validate.py"), str(out), "--strict")
    assert r.returncode == 0, "validate --strict failed:\n" + r.stdout + r.stderr


def test_full_fde_content_type_distribution(tmp_path):
    """전체 FDE 의 콘텐츠타입 분포 불변량.

    7 prose(ch1-7) / 1 anthology(ch8) / 1 afterword(후기) /
    1 glossary(부록A) / 1 roster(부록B) / 1 index(부록C) = 12 파일.
    """
    work = tmp_path / "work"
    r = _run(str(ROOT / "scripts" / "extract.py"), BOOK, str(work))
    assert r.returncode == 0, r.stderr
    chapters = json.loads((work / "chapters.json").read_text(encoding="utf-8"))

    assert len(chapters) == 12, f"expected 12 files, got {len(chapters)}"
    import collections
    dist = collections.Counter(c["content_type"] for c in chapters)
    assert dict(dist) == {
        "prose": 7,
        "anthology": 1,
        "afterword": 1,
        "glossary": 1,
        "roster": 1,
        "index": 1,
    }, f"content-type distribution mismatch: {dict(dist)}"

    # ch8 이 ANTHOLOGY 인지 확인
    ch8 = next(c for c in chapters if c["number"] == "08")
    assert ch8["content_type"] == "anthology"


def test_ch8_anthology_produces_5_chunks(tmp_path):
    """ch8 완결사례집(ANTHOLOGY) → ## N.M 절 단위 5 서브청크."""
    work = tmp_path / "work"
    _run(str(ROOT / "scripts" / "extract.py"), BOOK, str(work))
    chunks_dir = work / "chunks"
    chunks = sorted(p.name for p in chunks_dir.glob("08-*.md"))
    assert chunks == [
        "08-8.1.md", "08-8.2.md", "08-8.3.md", "08-8.4.md", "08-8.5.md",
    ], f"ch8 chunks mismatch: {chunks}"


def test_judgment_comparator_ch02_no_missing(tmp_path):
    """judgment_comparator 가 생성된 ch02 마크다운 대비 골든 누락 없음.

    골든(psf-3gate ch02§2.2, poc-purgatory ch02§2.1)의 절 토큰(2.1/2.2)이
    extract 의 세그먼트 감지 결과에 모두 존재함을 증명 → 결정론 회그 통과.
    """
    work, out = tmp_path / "work", tmp_path / "skill"
    _run(str(ROOT / "scripts" / "extract.py"), BOOK, str(work))
    _run(
        str(ROOT / "scripts" / "gen_knowledge.py"), BOOK,
        "--candidates", str(FIXTURE_CANDIDATES),
        "--work", str(work), "--out", str(out),
    )
    ch02 = next(out.joinpath("chapters").glob("ch02-*.md"))
    r = _run(
        str(ROOT / "evals" / "judgment_comparator.py"),
        str(GOLDEN), str(ch02),
    )
    assert r.returncode == 0, "comparator reported missing golden: " + r.stdout
    assert "MISSING: none" in r.stdout
