"""tests/test_qc_gate.py — G2 폰트 계약·G3 밴드 (typst 필요 테스트는 SKIP)

브리프 대비 테스트 수정(실증 근거, .smoke/cli-book PDF 실측):
- "Noto Serif KR" 미설치 → 설치된 "Noto Sans CJK KR"로 대체.
- `#set text(..)[본문]`은 set 규칙에 content를 못 붙이는 구문 오류 → 본문 분리.
- mitex 0.2.7은 LaTeX 문자열 인자만 지원(`#mitex[${..}$]` panic) → 백틱 호출.
- norm_font("Noto Sans CJK KR") == "notosanscjkkr" (브리프 "notosanscjkr"는
  오타 — 실제 임베드 basefont "NotoSansCJKkr-Regular-…"도 같은 값으로
  정규화되어 계약 매칭이 성립. 한 글자 적은 기대값이면 실책 전부 오탐).
"""
import shutil, subprocess, json
from pathlib import Path
import pytest
import fitz
from scripts.qc_gate import check_fonts, check_chars_band, norm_font, run, _font_allowed

SKIP = pytest.mark.skipif(not shutil.which("typst"), reason="typst 미설치")


def _make_book(tmp_path: Path, texts: list) -> None:
    """게이트용 책 스캐폴드 — texts별 draft pdf 1개씩 생성.

    texts가 비어 있으면 빈 페이지(오버플로 0 → PASS), 텍스트가 있으면
    프레임 밖 잉크(오버플로 → FAIL).
    """
    build = tmp_path / "build"
    build.mkdir(parents=True, exist_ok=True)
    draft = tmp_path / "draft"
    draft.mkdir(parents=True, exist_ok=True)
    (build / "tokens.json").write_text(json.dumps({
        "body_frame_pt": {"x0": 10, "y0": 10, "x1": 90, "y1": 90},
        "fonts": {"body": {"stack": ["Noto Sans CJK KR"], "size_pt": 10}},
    }), encoding="utf-8")
    for i, page_texts in enumerate(texts):
        doc = fitz.open()
        for t in page_texts or [None]:
            page = doc.new_page(width=100, height=100)
            if t:
                page.insert_text((5, 50), t)  # x0=5 < 10 → 프레임 밖
        doc.save(draft / f"book-{i}.pdf")
        doc.close()


def test_run_fail_deletes_stale_final(tmp_path):
    # FAIL 시 기존 final/<책>.pdf가 남으면 낡은 PASS 결과로 오탐된다 —
    # 삭제해야 한다(2026-08-15 컨트롤러 판정).
    _make_book(tmp_path, [["프레임 밖 텍스트"]])
    final = tmp_path / "final"
    final.mkdir()
    stale = final / "실전 시스템 설계 2026.pdf"
    stale.write_bytes(b"%PDF-stale")
    rc = run(tmp_path)
    assert rc == 1
    assert not stale.exists()


def test_run_multiple_draft_pdfs_warns(tmp_path, capsys):
    # draft에 pdf 2개 이상이면 첫 번째만 조용히 검사하지 않고 경고한다.
    _make_book(tmp_path, [[], []])
    run(tmp_path)
    err = capsys.readouterr().err
    assert "2개" in err and "book-1.pdf" in err

def test_norm_font_strips_subset_prefix():
    assert norm_font("SIFNZL+NanumSquareB") == "nanumsquareb"
    # 실측 basefont는 스타일·인코딩 접미사까지 포함 — 이걸 잘라야 계약 매칭
    assert norm_font("KVHFRP+NotoSansCJKkr-Regular-Identity-H") == "notosanscjkkr"

def test_norm_font_normalizes():
    assert norm_font("Noto Sans CJK KR") == "notosanscjkkr"

@SKIP
def test_fonts_in_contract(tmp_path):
    src = tmp_path / "t.typ"
    src.write_text('#set text(font: "Noto Sans CJK KR", lang: "ko")\n본문',
                   encoding="utf-8")
    pdf = tmp_path / "t.pdf"
    subprocess.run(["typst", "compile", str(src), str(pdf)],
                   check=True, capture_output=True)
    assert check_fonts(pdf, {"notosanscjkkr"}, {"Noto Sans CJK KR"}) == []

@SKIP
def test_fonts_out_of_contract(tmp_path):
    src = tmp_path / "t.typ"
    src.write_text('#set text(font: "Noto Sans CJK KR", lang: "ko")\n'
                   '본문 #text(font: "DejaVu Sans Mono")[x]',
                   encoding="utf-8")
    pdf = tmp_path / "t.pdf"
    subprocess.run(["typst", "compile", str(src), str(pdf)],
                   check=True, capture_output=True)
    bad = check_fonts(pdf, {"notosanscjkkr"}, {"Noto Sans CJK KR"})
    # 위반 메시지는 원본 basefont 표기("DejaVuSansMono")를 보존 — 소문자 비교
    assert any("dejavusansmono" in b.lower() for b in bad)

@SKIP
def test_math_fonts_allowlisted(tmp_path):
    """mitex 수식 폰트(NewCMMath)는 계약 외 허용 목록으로 통과"""
    src = tmp_path / "t.typ"
    src.write_text('#import "@preview/mitex:0.2.7": mitex\n'
                   '#set text(font: "Noto Sans CJK KR", lang: "ko")\n'
                   '본문 #mitex[`E=m c^2`]',
                   encoding="utf-8")
    pdf = tmp_path / "t.pdf"
    subprocess.run(["typst", "compile", str(src), str(pdf)],
                   check=True, capture_output=True)
    assert check_fonts(pdf, {"notosanscjkkr"}, {"Noto Sans CJK KR"}) == []

def test_font_variant_suffix_match():
    """임베드 PS명 변형 접미사(NanumSquare_acR)는 같은 가족으로 통과."""
    assert _font_allowed("HXBYGS+NanumSquare_acR-Regular",
                         {"nanumsquareac"}, {"NanumSquare_ac"})
    # 타 가족(NanumGothicCoding)은 접미사 4자 초과 — 기각
    assert not _font_allowed("XX+NanumGothicCoding-Regular",
                             {"nanumgothic"}, {"NanumGothic"})
