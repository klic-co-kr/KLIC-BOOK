# tests/test_filename_normalization.py
"""한글 파일명이 NFD(자모 분리)로 들어와도 kind/content_type 분류가 동작해야 한다.

macOS(APFS/HFS+)는 경로에 따라 파일명을 NFD로 돌려준다. 대표적으로 GitHub
"Download ZIP" 으로 받은 사본을 압축 해제하면 NFD 가 된다. git clone 사본은
core.precomposeunicode 덕분에 NFC 라서, 기존 e2e 테스트는 이 경로를 잡지 못한다.
따라서 여기서는 NFD 파일명을 명시적으로 만들어 회귀를 고정한다.
"""
import unicodedata

import pytest

from korean_ebook_to_skill.chapters import parse_chapter_file
from korean_ebook_to_skill.content_type import classify_content_type
from korean_ebook_to_skill.models import ContentType

# (파일명, 기대 kind, 기대 content_type, 본문)
CASES = [
    ("09-후기-FDE의직업윤리.md", "afterword", ContentType.AFTERWORD, "# 후기\n본문\n"),
    (
        "11-부록B-인물및팀명단.md",
        "appendix",
        ContentType.ROSTER,
        "# 부록B 인물 및 팀 명단\n- 아무개\n",
    ),
]


def _write_nfd(tmp_path, name: str, text: str):
    """파일명을 NFD 로 강제해 기록한다."""
    nfd_name = unicodedata.normalize("NFD", name)
    p = tmp_path / nfd_name
    p.write_text(text, encoding="utf-8")
    # 파일시스템이 이름을 되돌려주는 방식과 무관하게, 우리가 만든 NFD 경로로 읽는다.
    return p


@pytest.mark.parametrize("name,expected_kind,expected_type,text", CASES)
def test_nfd_filename_classifies_same_as_nfc(
    tmp_path, name, expected_kind, expected_type, text
):
    p = _write_nfd(tmp_path, name, text)
    cf = parse_chapter_file(p)
    assert cf.kind == expected_kind, f"NFD 파일명에서 kind 오분류: {cf.kind}"
    assert classify_content_type(cf) == expected_type


@pytest.mark.parametrize("name,expected_kind,expected_type,text", CASES)
def test_nfc_filename_still_classifies(
    tmp_path, name, expected_kind, expected_type, text
):
    p = tmp_path / unicodedata.normalize("NFC", name)
    p.write_text(text, encoding="utf-8")
    cf = parse_chapter_file(p)
    assert cf.kind == expected_kind
    assert classify_content_type(cf) == expected_type


def test_appendix_number_extracted_from_nfd_name(tmp_path):
    p = _write_nfd(tmp_path, "10-부록A-핵심지표.md", "# 부록A 핵심지표\n**MTTR:** 값\n")
    cf = parse_chapter_file(p)
    assert cf.kind == "appendix"
    assert cf.number == "A"
