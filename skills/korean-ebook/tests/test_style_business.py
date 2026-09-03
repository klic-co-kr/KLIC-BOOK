"""tests/test_style_business.py — business 스타일 팩 스모크 + 토큰 계약 유닛

스모크: assemble→compile→G1 bbox. 이어 G1+G2+G3 전체 게이트 통과(final/).
빌드 머신 실측 폰트: "Noto Sans KR" 설치(VF) — body 스택 1순위이므로 폴백
임베드 없이 G2가 성립한다. "Pretendard"는 미설치 후순위 폴백(스택 전체가
없는 환경용).
"""
import json
import shutil
from pathlib import Path
import pytest
from scripts.build import load_config, assemble, compile_pdf
from scripts.qc_gate import allowed_fonts, check_overflow, load_frame, run as qc_run

FIXTURE = Path(__file__).parent / "fixtures" / "sample-manuscript"
TOKENS = Path(__file__).parent.parent / "styles" / "business" / "tokens.json"
SKIP = pytest.mark.skipif(not shutil.which("typst"), reason="typst 미설치")
MM = 72 / 25.4  # mm → pt


def _tokens() -> dict:
    return json.loads(TOKENS.read_text(encoding="utf-8"))


def _book(tmp_path: Path) -> Path:
    book = tmp_path / "b"
    book.mkdir()
    (book / "typst-build.yaml").write_text(
        "style: business\ntitle: 백서 샘플\nchapters:\n  - ch01.md\n  - ch02.md\n",
        encoding="utf-8")
    for f in FIXTURE.glob("*.md"):
        (book / f.name).write_text(f.read_text(encoding="utf-8"), encoding="utf-8")
    return book


def test_business_frame_matches_trim_margins():
    """body_frame_pt는 trim/margin 유도값과 일치해야 한다(G1 프레임 정합성).

    대형판 200×280, inner 22, top 24, outer 18, bottom 22mm:
    x0=inner, y0=top, x1=width-outer, y1=height-bottom(pt 환산).
    """
    t = _tokens()
    f = t["body_frame_pt"]
    assert f["x0"] == pytest.approx(t["margin"]["inner_mm"] * MM, abs=0.05)
    assert f["y0"] == pytest.approx(t["margin"]["top_mm"] * MM, abs=0.05)
    assert f["x1"] == pytest.approx(
        (t["trim"]["width_mm"] - t["margin"]["outer_mm"]) * MM, abs=0.05)
    assert f["y1"] == pytest.approx(
        (t["trim"]["height_mm"] - t["margin"]["bottom_mm"]) * MM, abs=0.05)


def test_business_body_font_five_lineup():
    """business 본문은 5폰트 라인업에서 Wanted Sans Std 선행(2026-08-20).

    G2 허용 집합은 스택 정규화로 성립 — ps 별칭 의존 제거.
    """
    a = allowed_fonts(_tokens())[0]
    assert "wantedsansstd" in a            # 스택 표기 정규화
    assert "pretendard" in a               # 후순위 폴백
    assert _tokens()["fonts"]["body"]["stack"][0] == "Wanted Sans Std"


def test_business_label_top_uppercase():
    """label-top은 이미 대문자 SECTION — theme에서 upper() 없이 직접 렌더."""
    assert _tokens()["label-top"] == "SECTION"
    assert _tokens()["label-top"].isupper()


@SKIP
def test_business_smoke(tmp_path):
    book = _book(tmp_path)
    cfg = load_config(book / "typst-build.yaml")
    pdf = compile_pdf(assemble(cfg, book), cfg["title"])
    assert pdf.exists()
    frame = load_frame(book / "build" / "tokens.json")
    assert check_overflow(pdf, frame) == []


@SKIP
def test_business_qc_gate_full_pass(tmp_path):
    """G1+G2+G3 전체 게이트가 business 스모크북에서 PASS(final/ 생성)해야 한다.

    body·heading 전 스택이 빌드 머신 설치 폰트(Noto Sans KR) 기반이므로
    폴백 임베드 없이 G2가 성립한다. 스택 전체가 없는 머신에서는 이 테스트가
    폴백 폰트 계약 위반으로 실패한다.
    """
    book = _book(tmp_path)
    cfg = load_config(book / "typst-build.yaml")
    compile_pdf(assemble(cfg, book), cfg["title"])
    assert qc_run(book) == 0
    assert (book / "final").is_dir()
