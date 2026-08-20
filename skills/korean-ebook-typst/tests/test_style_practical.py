"""tests/test_style_practical.py — practical 스타일 팩 스모크 + G2 ps 허용 별칭

스모크: assemble→compile→G1 bbox. 실측 환경 폰트 참고:
- "Noto Serif KR"·"KoPubWorld바탕" 미설치 → 임베드 폰트는 폴백이다.
  G2 전체 실행(run)은 이 머신에서 별도 폴백 폰트를 ps에 등록해야 통과한다
  (등록은 스타일 팩 소비 머신 폰트 환경에 맞춰 조정 — 여기선 G1만 게이트).
"""
import shutil
from pathlib import Path
import pytest
from scripts.build import load_config, assemble, compile_pdf
from scripts.qc_gate import allowed_fonts, check_overflow, load_frame, \
    norm_font, run as qc_run

FIXTURE = Path(__file__).parent / "fixtures" / "sample-manuscript"
SKIP = pytest.mark.skipif(not shutil.which("typst"), reason="typst 미설치")


def test_allowed_fonts_includes_ps_aliases():
    """ps 필드의 PostScript 별칭이 허용 집합에 들어가야 한다.

    KoPubWorld바탕(스택 표기)의 임베드 basefont는 "KoPubWorldBatang" —
    정규화 결과가 서로 달라("kopubworld바탕" vs "kopubworldbatang")
    ps 명시 없이는 G2가 정상 폰트를 계약 위반으로 오탐한다.
    """
    tokens = {"fonts": {
        "body": {"stack": ["Noto Serif KR", "KoPubWorld바탕"],
                 "ps": ["KoPubWorldBatang"]},
        "heading1": {"stack": ["Noto Sans KR"]},
    }}
    a = allowed_fonts(tokens)[0]
    assert "kopubworldbatang" in a          # ps 별칭 경로
    assert "kopubworld바탕" in a            # 스택 표기도 유지
    assert "notoserifkr" in a
    assert "notosanskr" in a


def test_allowed_fonts_without_ps_unchanged():
    tokens = {"fonts": {"body": {"stack": ["Noto Sans KR"]}}}
    assert allowed_fonts(tokens)[0] == {"notosanskr"}


@SKIP
def test_practical_smoke(tmp_path):
    book = tmp_path / "b"
    book.mkdir()
    (book / "typst-build.yaml").write_text(
        "style: practical\ntitle: 실용서 샘플\nchapters:\n  - ch01.md\n  - ch02.md\n",
        encoding="utf-8")
    for f in FIXTURE.glob("*.md"):
        (book / f.name).write_text(f.read_text(encoding="utf-8"), encoding="utf-8")
    cfg = load_config(book / "typst-build.yaml")
    pdf = compile_pdf(assemble(cfg, book), cfg["title"])
    assert pdf.exists()
    frame = load_frame(book / "build" / "tokens.json")
    assert check_overflow(pdf, frame) == []


@SKIP
def test_practical_qc_gate_full_pass(tmp_path):
    """G1+G2+G3 전체 게이트가 practical 스모크북에서 PASS(final/ 생성)해야 한다.

    빌드 머신 설치 폰트가 스택 1순위(Noto Serif CJK KR)이므로 폴백 임베드
    없이 G2가 성립한다. 스택 전체가 없는 머신에서는 이 테스트가 폴백 폰트
    계약 위반으로 실패한다 — 설치 폰트에 맞춰 ps를 보정할 것.
    """
    book = tmp_path / "b"
    book.mkdir()
    (book / "typst-build.yaml").write_text(
        "style: practical\ntitle: 실용서 샘플\nchapters:\n  - ch01.md\n  - ch02.md\n",
        encoding="utf-8")
    for f in FIXTURE.glob("*.md"):
        (book / f.name).write_text(f.read_text(encoding="utf-8"), encoding="utf-8")
    cfg = load_config(book / "typst-build.yaml")
    compile_pdf(assemble(cfg, book), cfg["title"])
    assert qc_run(book) == 0
    assert (book / "final").is_dir()

@SKIP
def test_raw_code_font_stays_in_contract(tmp_path):
    """코드(한글 포함)가 mono+body 계약 폰트로만 렌더링되어야 한다.

    base.typ이 raw 폰트를 지정하지 않으면 typst 기본 DejaVu Sans Mono로
    렌더링되고 코드 내 한글이 Unifont 마지막 폴백으로 떨어져 G2 위반
    (실전시스템설계 코드 블록 실측). mono 스택이 허용 집합에 들어가야 한다.
    """
    import fitz
    book = tmp_path / "b"
    book.mkdir()
    (book / "ch01.md").write_text(
        "# 1장\n\n```\nQPS = 25,000 events/s · 보존 기간 30일\n```\n",
        encoding="utf-8")
    (book / "typst-build.yaml").write_text(
        "style: practical\ntitle: 코드 샘플\nchapters:\n  - ch01.md\n",
        encoding="utf-8")
    cfg = load_config(book / "typst-build.yaml")
    pdf = compile_pdf(assemble(cfg, book), cfg["title"])
    basefonts = {norm_font(f[3]) for p in fitz.open(pdf) for f in p.get_fonts()}
    assert "dejavusansmono" in basefonts          # mono 스택이 실제로 적용
    assert not any("unifont" in f for f in basefonts)  # 한글이 Unifont 폴백 아님

@SKIP
def test_long_middledot_heading_stays_in_frame(tmp_path):
    """·연쇄+하이픈 장 제목이 양쪽정렬 늘어남으로 프레임을 넘치지 않아야 한다.

    헤딩이 par(justify: true)를 상속하면 ZWSP/공백이 늘어나며 안쪽여백을
    침범한다(실전시스템설계 ch20 실측 +3.2pt). 헤딩은 양쪽정렬 대상이
    아니다 — show heading에서 justify를 끈다.
    """
    book = tmp_path / "b"
    book.mkdir()
    (book / "ch01.md").write_text(
        "# 20. Key-Value·Document·Wide-column·Graph\n\n"
        "본문 문단이다. 제목이 길어도 본문 정렬은 그대로다.\n",
        encoding="utf-8")
    (book / "typst-build.yaml").write_text(
        "style: practical\ntitle: 제목 샘플\nchapters:\n  - ch01.md\n",
        encoding="utf-8")
    cfg = load_config(book / "typst-build.yaml")
    pdf = compile_pdf(assemble(cfg, book), cfg["title"])
    frame = load_frame(book / "build" / "tokens.json")
    assert check_overflow(pdf, frame) == []

def test_practical_body_stack_sans_first():
    # IT 실용서 본문은 산세리프 우선 — 5폰트 라인업(Pretendard·SUIT·
    # Wanted Sans Std·Freesentation·Montserrat) 중 Pretendard 선행.
    # 정적 웨이트만 쓴다(typst VF Thin 버그 — memory 참조).
    import json
    from pathlib import Path
    tokens = json.loads((Path(__file__).parent.parent / "styles/practical/tokens.json").read_text(encoding="utf-8"))
    assert tokens["fonts"]["body"]["stack"][0] == "Pretendard"

def test_practical_toc_depth_is_two():
    # 467면 책의 인쇄 차례는 장급만으론 부족하다 — 절급(depth 2)까지.
    import json
    from pathlib import Path
    tokens = json.loads((Path(__file__).parent.parent / "styles/practical/tokens.json").read_text(encoding="utf-8"))
    assert tokens.get("toc_depth") == 2
