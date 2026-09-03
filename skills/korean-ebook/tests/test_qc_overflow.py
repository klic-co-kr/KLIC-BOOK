"""tests/test_qc_overflow.py — typst 필요

모든 테스트 문서는 2쪽 이상: check_overflow 기본 skip_pages=1이
1쪽(표지)을 검사하지 않으므로, 단쪽 문서는 아무 것도 검사하지 않고
통과해 버린다.
"""
import shutil
import subprocess
from pathlib import Path
import pytest
from scripts.qc_gate import _ink_bbox, check_overflow, load_frame

SKIP = pytest.mark.skipif(not shutil.which("typst"), reason="typst 미설치")

FRAME = (56.7, 62.4, 391.2, 581.1)  # practical 근사값

def _compile(tmp_path, body):
    src = tmp_path / "t.typ"
    src.write_text(f"""#set page(width: 153mm, height: 225mm,
  margin: (top: 22mm, bottom: 20mm, left: 20mm, right: 15mm))
#set text(lang: "ko", font: "Noto Serif KR", size: 10pt)
{body}
""", encoding="utf-8")
    pdf = tmp_path / "t.pdf"
    subprocess.run(["typst", "compile", str(src), str(pdf)], check=True,
                   capture_output=True)
    return pdf

@SKIP
def test_no_overflow_clean_page(tmp_path):
    pdf = _compile(tmp_path, "정상 본문입니다. 판면 안에 있습니다.\n#pagebreak()\n둘째 쪽 정상 본문입니다.")
    assert check_overflow(pdf, FRAME) == []

@SKIP
def test_overflow_detected(tmp_path):
    pdf = _compile(tmp_path,
        '표지 아닌 첫 쪽.\n#pagebreak()\n#place(top + left, dx: -15mm, dy: 100mm)[바깥 텍스트]')
    assert len(check_overflow(pdf, FRAME)) >= 1

@SKIP
def test_page_number_footer_allowed(tmp_path):
    pdf = _compile(tmp_path,
        '#set page(footer: context align(center)[#counter(page).display("1")])\n정상 본문.\n#pagebreak()\n둘째 쪽 정상 본문.')
    assert check_overflow(pdf, FRAME) == []

@SKIP
def test_cover_page_skipped(tmp_path):
    pdf = _compile(tmp_path, '#page(margin: 0pt)[#place(top + left, dx: -30mm)[표지]]\n본문.')
    assert check_overflow(pdf, FRAME) == []


def test_ink_bbox_ignores_trailing_space():
    """후행 공백 폭은 잉크가 아니므로 bbox에서 제외해야 한다."""
    line = {"spans": [{"text": "샘플. ", "chars": [
        {"c": "샘", "bbox": (65.2, 197.9, 75.2, 207.9)},
        {"c": "플", "bbox": (75.2, 197.9, 85.2, 207.9)},
        {"c": ".", "bbox": (85.2, 197.9, 88.2, 207.9)},
        {"c": " ", "bbox": (88.2, 197.9, 93.2, 207.9)},
    ]}]}
    ink, text = _ink_bbox(line)
    assert ink == (65.2, 197.9, 88.2, 207.9)
    assert text == "샘플."


def test_ink_bbox_all_whitespace():
    line = {"spans": [{"text": "  ", "chars": [
        {"c": " ", "bbox": (1, 1, 2, 2)},
        {"c": " ", "bbox": (2, 1, 3, 2)},
    ]}]}
    assert _ink_bbox(line) == (None, "")

@SKIP
def test_running_header_top_margin_allowed(tmp_path):
    # 러닝헤드(상단 여백 장 제목)는 쪽번호와 동일하게 판면 밖 여백 요소다.
    # 미면제 시 practical 러닝헤드가 G1 위반으로 오탐된다.
    pdf = _compile(tmp_path,
        '#set page(header: align(right)[CHAPTER 01 · 확장])\n'
        '정상 본문.\n#pagebreak()\n둘째 쪽 정상 본문.')
    assert check_overflow(pdf, FRAME) == []
