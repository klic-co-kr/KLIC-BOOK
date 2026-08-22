"""test_infographic_build_integration.py — 스펙 §2 [2]: 조립 통합·경로·검수 시트."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[1]


def _make_book(tmp_path: Path) -> Path:
    book = tmp_path / "book"
    (book / "manuscript").mkdir(parents=True)
    (book / "manuscript" / "ch01.md").write_text("""## 첫째 장

대응은 5단계로 수렴한다.

```infographic
{"layout": "flow", "title": "5단계로 수렴한다", "evidence": "§1", "steps": [
  {"title": "접수", "text": "등록"},
  {"title": "폐쇄", "text": "확정"}
]}
```

뒤 본문.
""", encoding="utf-8")
    (book / "typst-build.yaml").write_text(
        'style: practical\n' 'title: "테스트책"\n' 'subtitle: "부"\n'
        'author: "KLIC"\n' 'date: "2026-08"\n'
        "chapters:\n  - manuscript/ch01.md\n", encoding="utf-8")
    return book


def test_assemble_emits_fig_include_and_review_sheet(tmp_path):
    book = _make_book(tmp_path)
    build = book / "build"
    r = subprocess.run([sys.executable, str(SKILL / "scripts" / "build.py"), str(book)],
                       capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stderr
    fig = build / "infographic" / "000-fig01.typ"
    assert fig.exists(), "emit 파일 없음"
    typ = (build / "typ" / "000-ch01.typ").read_text(encoding="utf-8")
    assert '#include "../infographic/000-fig01.typ"' in typ
    assert "⟦IG:1⟧" not in typ
    assert (build / "helper.typ").exists()
    review = build / "infographic" / "000-fig01.review.md"
    body = review.read_text(encoding="utf-8")
    assert "확인란" in body and "steps[0].title" in body
    assert "교차검증" in body and "I1 통과" in body        # 5열 계약(§5.4)
    pdf = book / "draft" / "테스트책.pdf"                  # sanitize_filename은 공백 유지(실증)
    assert pdf.exists() and pdf.stat().st_size > 10_000, "최종 PDF 없음"


PHASE3_MD = """## 첫째 장

리드타임은 2주에서 3일로, 수작업은 5단계에서 1단계로 줄어든다.
성숙도는 4단계로 올라간다. 도입은 2025년 준비, 2026년 확산, 2027년 정착의
세 위상으로 전개된다.

```infographic
{"layout": "before_after", "title": "AI 도입은 리드타임을 2주에서 3일로 줄인다", "evidence": "§1",
 "before": ["리드타임 2주", "수작업 5단계"], "after": ["리드타임 3일", "자동화 1단계"],
 "center": "AI 도입"}
```

```infographic
{"layout": "ladder", "title": "성숙도는 4단계로 올라간다", "evidence": "§1", "stages": [
  {"title": "단계 1", "text": "근거 문장"},
  {"title": "단계 2", "text": "근거 문장"},
  {"title": "단계 3", "text": "근거 문장"},
  {"title": "단계 4", "text": "근거 문장"}
]}
```

```infographic
{"layout": "roadmap", "title": "도입은 세 위상으로 전개된다", "evidence": "§1", "phases": [
  {"period": "2025년", "title": "위상 1", "items": ["항목 0", "항목 1"]},
  {"period": "2026년", "title": "위상 2", "items": ["항목 0", "항목 1"]},
  {"period": "2027년", "title": "위상 3", "items": ["항목 0", "항목 1"]}
]}
```

뒤 본문.
"""


def test_phase3_archetypes_build_pdf_and_review_sheets(tmp_path):
    # 종료 조건(스펙 §8 Phase 3): 신규 3종 펜스가 빌드 전 과정을 통과한다 —
    # 펜스↔emit 1:1 · 챕터 typ include 치환 · PDF 생성 · 검수 시트 신규 필드 행
    # (m6: 검수 시트는 빌드 경로 render_book_fences에서만 생성 — cli lint는
    # 만들지 않는다). 펜스 데이터는 Task 1~3 레이아웃 테스트 _fence와 동일.
    book = tmp_path / "book3"
    (book / "manuscript").mkdir(parents=True)
    (book / "manuscript" / "ch01.md").write_text(PHASE3_MD, encoding="utf-8")
    (book / "typst-build.yaml").write_text(
        'style: practical\n' 'title: "페이즈3책"\n' 'subtitle: "부"\n'
        'author: "KLIC"\n' 'date: "2026-08"\n'
        "chapters:\n  - manuscript/ch01.md\n", encoding="utf-8")
    r = subprocess.run([sys.executable, str(SKILL / "scripts" / "build.py"), str(book)],
                       capture_output=True, text=True, timeout=180)
    assert r.returncode == 0, r.stderr
    typ = (book / "build" / "typ" / "000-ch01.typ").read_text(encoding="utf-8")
    for n in (1, 2, 3):
        assert f'#include "../infographic/000-fig0{n}.typ"' in typ
        assert (book / "build" / "infographic" / f"000-fig0{n}.typ").exists()
    assert len(list((book / "build" / "infographic").glob("000-fig*.typ"))) == 3   # 중복 emit 방어
    sheets = {n: (book / "build" / "infographic" / f"000-fig0{n}.review.md").read_text(encoding="utf-8")
              for n in (1, 2, 3)}
    assert "before[0]" in sheets[1] and "after[1]" in sheets[1] and "center" in sheets[1]
    assert "stages[3].title" in sheets[2]                      # ladder 마지막 단계
    assert "phases[0].period" in sheets[3] and "phases[2].items[1]" in sheets[3]
    for s in sheets.values():
        assert "I1 통과" in s                                  # 숫자 전부 교차검증 통과
    pdf = book / "draft" / "페이즈3책.pdf"
    assert pdf.exists() and pdf.stat().st_size > 10_000, "최종 PDF 없음"


def test_i1_blocks_build_with_full_report(tmp_path):
    book = _make_book(tmp_path)
    ch = book / "manuscript" / "ch01.md"
    ch.write_text(ch.read_text(encoding="utf-8").replace(
        '"title": "5단계로 수렴한다"',
        '"title": "777단계로 수렴한다"'), encoding="utf-8")   # 원문에 없는 숫자
    r = subprocess.run([sys.executable, str(SKILL / "scripts" / "build.py"), str(book)],
                       capture_output=True, text=True, timeout=120)
    assert r.returncode != 0
    assert "number-evidence" in (r.stdout + r.stderr)
    assert "000-ch01.md #1" in (r.stdout + r.stderr)      # 위치 계약 — 인덱스 prefix로 동명 스템 모호성 제거


SAME_STEM_MD = """## {part} 장

{mark} 흐름을 정리한다.

```infographic
{{"layout": "flow", "title": "{mark} 절차", "steps": [
  {{"title": "{mark} 접수", "text": "{mark} 등록"}},
  {{"title": "{mark} 확정", "text": "{mark} 마감"}}
]}}
```

뒤 본문.
"""


def test_same_stem_chapters_keep_own_fences(tmp_path):
    # 동일 stem 챕터(part1/ch01.md vs part2/ch01.md) — fences 사이드카가
    # <stem>.json 키로 충돌, 마지막 챕터가 앞 챕터의 도식을 조용히 덮어썼다
    # (최종 리뷰 Critical 1). 원고 md 직독으로 각 챕터가 자기 도식을 낸다.
    book = tmp_path / "book"
    for part, mark in (("part1", "앞부분"), ("part2", "뒷부분")):
        d = book / "manuscript" / part
        d.mkdir(parents=True)
        (d / "ch01.md").write_text(
            SAME_STEM_MD.format(part=part, mark=mark), encoding="utf-8")
    (book / "typst-build.yaml").write_text(
        'style: practical\n' 'title: "동일스템책"\n' 'subtitle: "부"\n'
        'author: "KLIC"\n' 'date: "2026-08"\n'
        "chapters:\n  - manuscript/part1/ch01.md\n"
        "  - manuscript/part2/ch01.md\n", encoding="utf-8")
    r = subprocess.run([sys.executable, str(SKILL / "scripts" / "build.py"), str(book)],
                       capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stderr
    fig_a = book / "build" / "infographic" / "000-fig01.typ"
    fig_b = book / "build" / "infographic" / "001-fig01.typ"
    assert "앞부분" in fig_a.read_text(encoding="utf-8")
    assert "뒷부분" in fig_b.read_text(encoding="utf-8")
    assert "앞부분" not in fig_b.read_text(encoding="utf-8")   # 뒤바뀜 방어
    pdf = book / "draft" / "동일스템책.pdf"
    assert pdf.exists() and pdf.stat().st_size > 10_000       # 두 도식 모두 인쇄됨


def test_qc_gate_warns_on_unreviewed_sheets(tmp_path):
    from scripts.qc_gate import check_review_sheets
    igdir = tmp_path / "build" / "infographic"; igdir.mkdir(parents=True)
    (igdir / "000-fig01.review.md").write_text(
        "| 요소 |\n- [ ] 원문 대조 완료", encoding="utf-8")          # 미완료
    (igdir / "000-fig02.review.md").write_text(
        "| 요소 |\n- [x] 원문 대조 완료", encoding="utf-8")          # 완료
    pending = check_review_sheets(tmp_path / "build")
    assert pending == ["000-fig01.review.md"]


def test_rebuild_resets_infographic_dir(tmp_path):
    book = _make_book(tmp_path)
    subprocess.run([sys.executable, str(SKILL / "scripts" / "build.py"), str(book)],
                   capture_output=True, text=True, timeout=120)
    stale = book / "build" / "infographic" / "zzz-stale.typ"
    stale.write_text("garbage", encoding="utf-8")
    subprocess.run([sys.executable, str(SKILL / "scripts" / "build.py"), str(book)],
                   capture_output=True, text=True, timeout=120)
    assert not stale.exists()
