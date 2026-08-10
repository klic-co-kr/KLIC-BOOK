# tests/test_content_type.py
from pathlib import Path
from korean_ebook_to_skill.chapters import parse_chapter_file
from korean_ebook_to_skill.content_type import classify_content_type
from korean_ebook_to_skill.models import ContentType, ChapterFile

def t(name): return classify_content_type(parse_chapter_file(Path(f"tests/fixtures/{name}")))

def test_prose(): assert t("02-제2장-올바른문제풀기.md") == ContentType.PROSE
def test_index(): assert t("12-부록C-사례색인및출처.md") == ContentType.INDEX
def test_roster(): assert t("11-부록B-인물및팀명단.md") == ContentType.ROSTER
def test_glossary_appendix_a(): assert t("10-부록A-핵심지표.md") == ContentType.GLOSSARY
def test_afterword(): assert t("09-후기-FDE의직업윤리.md") == ContentType.AFTERWORD
def test_anthology_discriminator():
    """ch8 구조판별: '### 방법론 환원' 헤더 존재 시 ANTHOLOGY (char 임계치 버그 회귀가드)."""
    assert t("08-제8장-완결사례집.md") == ContentType.ANTHOLOGY
def test_prose_without_discriminator_stays_prose():
    """방법론 환원 헤더 없는 일반 챕터는 PROSE 유지 (위양성 방지)."""
    assert t("02-제2장-올바른문제풀기.md") == ContentType.PROSE
def test_unknown_kind_falls_through_to_unknown():
    """분류 불가한 kind(방어적 fallback)은 UNKNOWN.

    현재 _kind_number 는 chapter/appendix/afterword 만 생산하므로 이 경로는
    일반 FDE 실행에서는 도달 불가. ChapterFile 을 직접 구성해 방어 라인 회귀가드.
    """
    cf = ChapterFile("x.md", "x", None, "foreword", "본문", [])
    assert classify_content_type(cf) == ContentType.UNKNOWN
