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
    assert "ch01.md #1" in (r.stdout + r.stderr)          # 위치 계약


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
