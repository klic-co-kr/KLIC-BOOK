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

def test_heading_middledot_gets_break_opportunity():
    # typst는 U+00B7을 줄바꿈 기회로 쓰지 않는다 — justify 헤딩에서
    # 긴 라틴 ·연쇄 토큰이 프레임 밖으로 넘친다(실전시스템설계 ch25 실측).
    # 헤딩의 · 뒤에 제로폭 공백을 심어 줄바꿈만 허용한다.
    out = convert("## 25. Timeout·Deadline·Retry\n")
    assert "= 25. Timeout·​Deadline·​Retry" in out

def test_body_middledot_untouched():
    out = convert("본문의 Timeout·Deadline 연쇄\n")
    assert "​" not in out

def test_heading_middledot_skips_math_and_code():
    out = convert("## 절 $x$ 과 `code·x`\n")
    assert "​" not in out

def test_bold_converts_to_typst_strong():
    # md2typst가 강조를 변환하지 않으면 **굵게**가 리터럴 별표로 인쇄된다
    # (실전시스템설계 머리말 실측 — 714건).
    out = convert("요구사항을 **검증 가능한 설계 입력**으로 바꾼다.\n")
    assert "*검증 가능한 설계 입력*" in out
    assert "\\*" not in out

def test_italic_converts_to_typst_emph():
    out = convert("원본 *The System Design Primer*가 제공한 지도\n")
    assert "_The System Design Primer_" in out

def test_stray_asterisk_stays_escaped():
    out = convert("2 * 3 = 6\n")
    assert "\\*" in out

def test_bold_in_code_span_stays_literal():
    out = convert("키워드 `**kwargs**` 인자\n")
    assert "`**kwargs**`" in out

def test_leading_yaml_frontmatter_stripped():
    # 원고 파일은 표준 YAML frontmatter(--- 쌍)로 메타데이터를 싣는다.
    # 미제거 시 id/order/status 덩어리가 본문 산문으로 인쇄된다
    # (실전시스템설계 전 장 실측).
    md = "---\nid: ch01\ntitle: 요구사항\n---\n\n# 1장\n\n본문.\n"
    out = convert(md)
    assert "id: ch01" not in out
    assert "title:" not in out
    assert "= 1장" in out

def test_no_frontmatter_untouched():
    out = convert("본문만 있다\n")
    assert "본문만 있다" in out

def test_midfile_dashes_not_frontmatter():
    # 파일 시작이 아니면 --- 쌍을 frontmatter로 취급하지 않는다
    out = convert("본문\n\n---\n\n뒷문단\n")
    assert "본문" in out and "뒷문단" in out

def test_html_comment_stripped():
    # 원고는 그림 생산 메타데이터를 <!-- figure-spec ... --> HTML 주석으로
    # 싣는다. 미제거 시 메타데이터가 본문 산문으로 인쇄된다(실전시스템설계
    # 전 장 실측).
    md = "<!-- figure-spec\nid: fig-ch01-01\n-->\n\n본문 단락\n"
    out = convert(md)
    assert "figure-spec" not in out
    assert "본문 단락" in out

def test_html_comment_in_code_span_kept():
    out = convert("예시 `<!-- note -->` 코드\n")
    assert "`<!-- note -->`" in out

def test_fenced_code_block_content_not_escaped():
    # 코드펜스 내부는 typst raw block으로 그대로 전달되어야 한다.
    # 미보호 시 # [ ] < 등이 step 6에서 이스케이프되어 \# 형태로 인쇄된다
    # (system-design-notes 번역서 코드블록 57개 실측).
    md = "```\n# comment\narr[0] < 10\n```\n"
    out = convert(md)
    assert "# comment" in out
    assert "\\# comment" not in out
    assert "arr[0] < 10" in out

def test_fenced_code_block_lang_tag_kept():
    md = "```json\n{\"a\": 1}\n```\n"
    out = convert(md)
    assert "```json" in out

def test_fenced_code_block_keeps_inline_dollar():
    # 코드 내 $는 수식도 화폐도 아니다 — raw로 보존
    md = "```\ncost = $5 + $x\n```\n"
    out = convert(md)
    assert "$5 + $x" in out

def test_pipe_table_converts_to_typst_table():
    # md 파이프 표는 typst #table()로 변환되어야 한다.
    # 미변환 시 | A | B | 가 리터럴 파이프 문자로 인쇄된다
    # (system-design-notes 표 148줄 실측).
    md = "| A | B |\n|---|---|\n| 1 | 2 |\n"
    out = convert(md)
    assert "#table(" in out
    assert "[A]" in out and "[B]" in out
    assert "[1]" in out and "[2]" in out
    assert "columns: 2" in out

def test_pipe_table_separator_row_dropped():
    md = "| 항목 | 값 |\n|---|---|\n| QPS | 100 |\n"
    out = convert(md)
    assert "---" not in out.split("#table(")[1]
    assert "[QPS]" in out

def test_pipe_table_cell_bold_converted():
    md = "| 이름 | 설명 |\n|---|---|\n| **캐시** | 빠른 저장 |\n"
    out = convert(md)
    assert "*캐시*" in out
    assert "\\*" not in out

def test_pipe_table_cell_specials_escaped():
    md = "| 키 | 값 |\n|---|---|\n| a#1 | x_y |\n"
    out = convert(md)
    assert "a\\#1" in out
    assert "x\\_y" in out

def test_pipe_table_not_confused_by_body_pipe():
    # 본문 한 줄 짜리 | 는 표로 오인하지 않는다(구분행 필요)
    md = "a | b\n본문\n"
    out = convert(md)
    assert "#table(" not in out

def test_table_and_fence_coexist():
    md = "| A |\n|---|\n| 1 |\n\n```\nx\n```\n"
    out = convert(md)
    assert "#table(" in out and "```" in out
