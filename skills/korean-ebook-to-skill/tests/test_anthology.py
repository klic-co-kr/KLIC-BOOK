# tests/test_anthology.py
from korean_ebook_to_skill.chapters import parse_chapter_file
from korean_ebook_to_skill.anthology import subchunk_anthology
from pathlib import Path

def test_subchunk_ch8_cases():
    text = ("# 8장 완결 사례집\n\n## 8.1 Palantir: 해자\n\n### 방법론 환원\n내용\n\n"
            "## 8.2 OpenAI: 벽돌\n\n### 방법론 환원\n내용\n\n## 8.5 180일\n\n내용\n")
    from korean_ebook_to_skill.models import ChapterFile
    cf = ChapterFile("x","08",None,"chapter",text,[],None)
    chunks = subchunk_anthology(cf)
    titles = [c.title for c in chunks]
    assert any("Palantir" in t for t in titles)
    assert any("OpenAI" in t for t in titles)
    assert any("방법론 환원" in c.text for c in chunks)  # 환원 블록 보존
