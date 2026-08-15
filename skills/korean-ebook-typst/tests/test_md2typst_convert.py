"""tests/test_md2typst_convert.py — 헤딩·인용 변환 회귀"""
from scripts.md2typst import convert

def test_h2_converts():
    out = convert("## 절 제목\n")
    assert out.strip().startswith("= 절 제목")

def test_h3_converts():
    out = convert("### 소절\n")
    assert out.strip().startswith("== 소절")

def test_h4_converts():
    out = convert("#### 깊은 제목\n")
    assert out.strip().startswith("=== 깊은 제목")

def test_h1_still_converts():
    out = convert("# 장 제목\n")
    assert out.strip().startswith("= 장 제목")

def test_blockquote_converts():
    out = convert("> 인용문입니다\n")
    assert out.strip() == "#quote[인용문입니다]"

def test_body_hash_still_escaped():
    out = convert("C# 언어 이야기\n")
    assert "\\#" in out and "= " not in out

def test_heading_with_specials():
    # 한글 시작 인라인 수식은 step 5 범위 밖(미변환, 원래 동작) — 라틴 수식으로 검증
    # (컨트롤러 승인: brief fixture $수식$ → $x$ 교체)
    out = convert("## 절 $x$ 과 [괄호]\n")
    assert out.strip().startswith("= 절 ")
    assert "#mitex" in out
