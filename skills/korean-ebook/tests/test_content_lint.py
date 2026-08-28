"""tests/test_content_lint.py — G5 콘텐츠 정합성 검사 회귀.

설득의 구조(OCR 정제 원고) 파생 — 라틴 잔존·판독불능·교차참조·보강 마커를
게이트 리포트로 남겨 downstream 보고서가 인용하게 한다.
"""
import pytest
from pathlib import Path

from scripts.content_lint import (
    scan_latin, scan_markers, scan_xref, scan_comments, lint,
)


# ── 라틴 잔존 ──────────────────────────────────────────────────────

def test_latin_catches_ocr_junk():
    hits = scan_latin("소름이 돋았습니다. OAHU. 그리고 DRM FASS] 뼈대")
    seqs = {h.split("'")[1] for h in hits}
    assert "OAHU" in seqs and "FASS" in seqs


def test_latin_allows_real_acronyms():
    text = "RAS를 통과하고 CTA를 늘린다. CEO가 TED에서 말했다. ROI·CPC·DNA·WHO·QSC"
    assert scan_latin(text) == []


def test_latin_ignores_capitalized_words_and_code():
    # Capitalized-case 일반 영단어·인라인 코드·Step 라벨은 오탐 아님
    assert scan_latin("Influence와 Giver, `npm RUN` 아님 — Step 3에서") == []


def test_latin_reports_line_number():
    hits = scan_latin("정상 문장\n\n여기 OAHU 남음")
    assert hits and "L3" in hits[0]


# ── 판독불능 마커 ──────────────────────────────────────────────────

def test_marker_catches_placeholder():
    hits = scan_markers("후기 중 〈○○ 님〉과 ______ 부분")
    assert len(hits) >= 2


def test_marker_clean_text():
    assert scan_markers("김철수 님의 후기입니다") == []


# ── 교차참조 ────────────────────────────────────────────────────────

def test_xref_flags_missing_chapter():
    chapters = {"2", "5"}
    hits = scan_xref("3장에서 배운 것과 14장에서 만납니다", chapters)
    joined = " ".join(hits)
    assert "3장 참조" in joined and "14장 참조" in joined
    assert "5장" not in joined


def test_xref_passes_valid_refs():
    assert scan_xref("2장과 5장에서", {"2", "5"}) == []


# ── HTML 주석 잔여 ──────────────────────────────────────────────────

def test_comments_detected():
    assert scan_comments("본문\n<!-- 주의: 이동 필요 -->\n끝") != []


def test_comments_clean():
    assert scan_comments("본문만 있다") == []


# ── 통합 lint ───────────────────────────────────────────────────────

def test_lint_returns_file_map_and_rescan_inventory(tmp_path: Path):
    md = tmp_path / "01-가.md"
    md.write_text("## 가\n\n2장에서 배웠습니다. 여기 OAHU.\n\n> ⚠️ 인쇄 p.26 미스캔 — 재스캔 후 보강 필요\n", encoding="utf-8")
    warns, rescan = lint([str(md)], tmp_path)
    key = str(md)
    assert key in warns and warns[key]
    assert rescan and "p.26" in rescan[0]


def test_lint_clean_manuscript(tmp_path: Path):
    md = tmp_path / "01-가.md"
    md.write_text("## 가\n\n깨끗한 문장입니다. RAS와 Step 1.\n", encoding="utf-8")
    warns, rescan = lint([str(md)], tmp_path)
    assert warns == {} and rescan == []
