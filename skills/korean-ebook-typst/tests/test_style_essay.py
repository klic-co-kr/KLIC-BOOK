"""tests/test_style_essay.py — essay 스타일 팩 스모크 + 토큰 계약 유닛

스모크: assemble→compile→G1 bbox. 이어 G1+G2+G3 전체 게이트 통과(final/).
빌드 머신 실측 폰트: "Noto Serif CJK KR"·"Noto Sans KR" 설치 —
body 스택 1순위가 설치 폰트이므로 폴백 임베드 없이 G2가 성립한다.
"Noto Serif KR"은 미설치 후순위 폴백(스택 전체가 없는 환경용).
"""
import json
import shutil
from pathlib import Path
import pytest
from scripts.build import load_config, assemble, compile_pdf
from scripts.qc_gate import allowed_fonts, check_overflow, load_frame, run as qc_run

FIXTURE = Path(__file__).parent / "fixtures" / "sample-manuscript"
TOKENS = Path(__file__).parent.parent / "styles" / "essay" / "tokens.json"
SKIP = pytest.mark.skipif(not shutil.which("typst"), reason="typst 미설치")
MM = 72 / 25.4  # mm → pt


def _tokens() -> dict:
    return json.loads(TOKENS.read_text(encoding="utf-8"))


def test_essay_frame_matches_trim_margins():
    """body_frame_pt는 trim/margin 유도값과 일치해야 한다(G1 프레임 정합성).

    사륙판 128×188, inner/outer 20, top 24, bottom 26mm:
    x0=inner, y0=top, x1=width-inner, y1=height-bottom(pt 환산).
    """
    t = _tokens()
    f = t["body_frame_pt"]
    assert f["x0"] == pytest.approx(t["margin"]["inner_mm"] * MM, abs=0.05)
    assert f["y0"] == pytest.approx(t["margin"]["top_mm"] * MM, abs=0.05)
    assert f["x1"] == pytest.approx(
        (t["trim"]["width_mm"] - t["margin"]["outer_mm"]) * MM, abs=0.05)
    assert f["y1"] == pytest.approx(
        (t["trim"]["height_mm"] - t["margin"]["bottom_mm"]) * MM, abs=0.05)


def test_essay_body_font_ps_alias():
    """body 임베드 PostScript명(NotoSerifCJKkr)이 G2 허용 집합에 들어가야 한다.

    ttc 임베드 basefont는 "NotoSerifCJKkr-Regular-..." — 정규화 시 스택 표기
    "Noto Serif CJK KR"과 결과가 같지만, 임베드명 사례를 ps로 명시 등록해
    폰트 환경 변화에도 계약이 깨지지 않게 한다(qc_gate allowed_fonts).
    """
    a = allowed_fonts(_tokens())
    assert "notoserifcjkkr" in a          # 스택 표기 정규화
    assert "notoserifkr" in a             # 후순위 폴백
    assert _tokens()["fonts"]["body"].get("ps") == ["NotoSerifCJKkr"]


@SKIP
def test_essay_smoke(tmp_path):
    book = tmp_path / "b"
    book.mkdir()
    (book / "typst-build.yaml").write_text(
        "style: essay\ntitle: 에세이 샘플\nchapters:\n  - ch01.md\n  - ch02.md\n",
        encoding="utf-8")
    for f in FIXTURE.glob("*.md"):
        (book / f.name).write_text(f.read_text(encoding="utf-8"), encoding="utf-8")
    cfg = load_config(book / "typst-build.yaml")
    pdf = compile_pdf(assemble(cfg, book), cfg["title"])
    assert pdf.exists()
    frame = load_frame(book / "build" / "tokens.json")
    assert check_overflow(pdf, frame) == []


@SKIP
def test_essay_toc_no_dot_leaders(tmp_path):
    """목차 리더 점선 금지(STYLE.md) — TOC 면에 점선 잉크가 없어야 한다.

    base.typ make-toc는 outline() 기본 리더를 쓰므로, theme.typ이
    outline.entry 쇼 규칙으로 무점선 엔트리(제목 + 1fr + 쪽수, 링크 유지)로
    오버라이드한다.
    """
    import fitz
    book = tmp_path / "b"
    book.mkdir()
    (book / "typst-build.yaml").write_text(
        "style: essay\ntitle: 에세이 샘플\nchapters:\n  - ch01.md\n  - ch02.md\n",
        encoding="utf-8")
    for f in FIXTURE.glob("*.md"):
        (book / f.name).write_text(f.read_text(encoding="utf-8"), encoding="utf-8")
    cfg = load_config(book / "typst-build.yaml")
    pdf = compile_pdf(assemble(cfg, book), cfg["title"])
    toc_text = fitz.open(pdf)[1].get_text()
    assert ". ." not in toc_text
    assert "첫째 장" in toc_text  # 엔트리 본문은 유지


@SKIP
def test_essay_qc_gate_full_pass(tmp_path):
    """G1+G2+G3 전체 게이트가 essay 스모크북에서 PASS(final/ 생성)해야 한다.

    body 스택 1순위(Noto Serif CJK KR)·heading 스택(Noto Sans KR) 모두 빌드
    머신 설치 폰트이므로 폴백 임베드 없이 G2가 성립한다. 스택 전체가 없는
    머신에서는 이 테스트가 폴백 폰트 계약 위반으로 실패한다.
    """
    book = tmp_path / "b"
    book.mkdir()
    (book / "typst-build.yaml").write_text(
        "style: essay\ntitle: 에세이 샘플\nchapters:\n  - ch01.md\n  - ch02.md\n",
        encoding="utf-8")
    for f in FIXTURE.glob("*.md"):
        (book / f.name).write_text(f.read_text(encoding="utf-8"), encoding="utf-8")
    cfg = load_config(book / "typst-build.yaml")
    compile_pdf(assemble(cfg, book), cfg["title"])
    assert qc_run(book) == 0
    assert (book / "final").is_dir()
