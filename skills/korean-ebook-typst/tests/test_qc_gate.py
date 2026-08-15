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
from scripts.qc_gate import check_fonts, check_chars_band, norm_font

SKIP = pytest.mark.skipif(not shutil.which("typst"), reason="typst 미설치")

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
    assert check_fonts(pdf, {"notosanscjkkr"}) == []

@SKIP
def test_fonts_out_of_contract(tmp_path):
    src = tmp_path / "t.typ"
    src.write_text('#set text(font: "Noto Sans CJK KR", lang: "ko")\n'
                   '본문 #text(font: "DejaVu Sans Mono")[x]',
                   encoding="utf-8")
    pdf = tmp_path / "t.pdf"
    subprocess.run(["typst", "compile", str(src), str(pdf)],
                   check=True, capture_output=True)
    bad = check_fonts(pdf, {"notosanscjkkr"})
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
    assert check_fonts(pdf, {"notosanscjkkr"}) == []
