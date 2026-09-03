"""tests/test_raw_block_style.py — 코드 블록(raw) 시각 서식 회귀.

github-guide 실측(2026-08): raw에 mono 폰트 규칙만 있고 배경·패딩이
없어 코드가 산문에 묻힌다고 지적받았다. base.typ이 블록 raw에 채움
상자를 입히는지를 렌더 픽셀로 검증한다 — 글자 스팬 왼쪽 패딩 영역
(x0 − 4pt)이 흰 종지가 아니면 배경이 있는 것이다. 인라인 raw는
산문 행 높이를 침범하지 않는 선에서 같은 계열 칩을 입힌다(여기선
블록만 계약 — 인라인 칩은 타이포그래피 선택지라 픽셀 고정 대상 아님).
"""
import shutil
from pathlib import Path

import fitz
import pytest

from scripts.build import load_config, assemble, compile_pdf

SKIP = pytest.mark.skipif(not shutil.which("typst"), reason="typst 미설치")

MD = """## 1장 코드

본문 산문이 있다.

```bash
git clone https://example.com/repo.git
cd repo && make all
```

뒷산문도 있다.
"""


@SKIP
def test_raw_block_has_background(tmp_path):
    book = tmp_path / "b"
    book.mkdir()
    (book / "typst-build.yaml").write_text(
        "style: b5\ntitle: 코드블록 샘플\nchapters:\n  - ch01.md\n",
        encoding="utf-8")
    (book / "ch01.md").write_text(MD, encoding="utf-8")
    cfg = load_config(book / "typst-build.yaml")
    pdf = compile_pdf(assemble(cfg, book), cfg["title"])

    doc = fitz.open(pdf)
    found = False
    for page in doc:
        for b in page.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                for s in l["spans"]:
                    if "Mono" not in s["font"] or "git" not in s["text"]:
                        continue
                    found = True
                    x0, y0, x1, y1 = s["bbox"]
                    ymid = (y0 + y1) / 2
                    # 스팬 시작점 왼쪽 4pt — 블록 x-패딩(inset) 안쪽이라
                    # 글시가 없다. 배경 없으면 종지 흰색 255가 나온다.
                    clip = fitz.Rect(x0 - 4.5, ymid - 0.5, x0 - 3.5, ymid + 0.5)
                    pix = page.get_pixmap(clip=clip)
                    r, g, bl = pix.pixel(pix.width // 2, pix.height // 2)
                    assert (r, g, bl) != (255, 255, 255), \
                        f"배경 없음(흰 종지): {s['text'][:20]!r} 앞 패딩 픽셀 {r},{g},{bl}"
    assert found, "mono 스팬 자체가 없다 — 빌드·폰트 환경 확인"


@SKIP
def test_inline_raw_long_in_quotes_no_overflow(tmp_path):
    """긴 인라인 코드 + 연속 인용 병합 문단이 프레임을 뚫지 않는지.

    ai-agent-book ch9·ch10 실측(2026-08): 한국어 문장을 백틱에 통째로
    싼 인라인 코드가 box 칩 안에서 줄바꿀이 금지되고, 연속 #quote가
    한 문단으로 병합되는 typst 기본 동작과 만나 60pt+ 돌출했다.
    칩 소재가 highlight(개행 추종)인지를 프레임 밖 라인 부재로 검증.
    """
    book = tmp_path / "b"
    book.mkdir()
    long_inline = "`" + "[EMO:happy][SPEED:fast]너무 좋네요! 주문이 확인되었습니다." \
        "[THINKING]음, 배송 시간을 확인해 볼게요...[EMO:neutral][SPEED:normal]" \
        "내일 오후 배송 예정입니다.`"
    (book / "typst-build.yaml").write_text(
        "style: lecture\ntitle: 인라인 재현\nchapters:\n  - ch01.md\n",
        encoding="utf-8")
    (book / "ch01.md").write_text(
        "## 1장 인용\n\n> Fish Audio S1의 음성 복제 능력을 사용한다. "
        "24개의 참조 음성 라이브러리를 구축한다. 각각 약 5초.\n"
        f"> LLM 출력 예: {long_inline}\n"
        "> 실행 계층은 표식을 해석해 해당 참조 음성에 매핑한다.\n",
        encoding="utf-8")
    cfg = load_config(book / "typst-build.yaml")
    pdf = compile_pdf(assemble(cfg, book), cfg["title"])

    doc = fitz.open(pdf)
    # frame 우측 = 페이지 폭 − 바깥여백(lecture 20mm≈56.7pt). 정상
    # justify 라인은 frame+4pt 안에서 끝난다. 라인이 페이지 우측
    # 20pt 이내(=어느 스타일 마진 안쪽)까지 뻗으면 돌출로 본다.
    over = []
    for pno, page in enumerate(doc):
        pw = page.rect.width
        for b in page.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                x1 = l["bbox"][2]
                txt = "".join(s["text"] for s in l["spans"]).strip()
                if txt and x1 > pw - 20:
                    over.append((pno + 1, round(x1, 1), txt[:40]))
    assert not over, f"프레임 밖 라인: {over}"
