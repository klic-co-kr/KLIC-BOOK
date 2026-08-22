"""G1 판면 오버플로 회귀 — 페이지 상단 2단 헤딩 글리프가 프레임 상단 안에 있는지.

md '### ' 절 제목 → typst 2단. 헤딩 블록이 잔여 공간에 못 들어가 다음 면으로
밀릴 때 선행 v는 면 경계에서 소멸한다(weak 불문 — strong로도 실측 불변,
2026-08-22 회귀, agent-papers p9 실측 3.17pt). Pretendard/SUIT 계열 어센더
잉크가 프레임 상단을 넘어 G1 오버플로가 되므로 theme L2는 pad(top: 3.5pt)로
방어한다.

재현은 명시적 pagebreak()가 아니라 잔여 갭 유도여야 한다 — 강제 개행 뒤의
v는 보존되어(lecture 실측 +6.42pt) 회귀가 재현되지 않는다. 프레임을 10pt만
못 채우는 블록을 두면 헤딩이 자연 밀림으로 다음 면 상단에 오고, 그 때의
선행 v만 소멸한다.
"""
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import fitz
import pytest

from scripts.build import typst_binary

pytestmark = pytest.mark.skipif(shutil.which("typst") is None, reason="typst 미설치")

SKILL = Path(__file__).resolve().parents[1]


def _compile(tmp: Path, style: str) -> tuple[float, float]:
    for name, src in (
        ("base.typ", SKILL / "templates" / "base.typ"),
        ("theme.typ", SKILL / "styles" / style / "theme.typ"),
        ("tokens.json", SKILL / "styles" / style / "tokens.json"),
    ):
        shutil.copy2(src, tmp / name)
    frame = json.loads((SKILL / "styles" / style / "tokens.json").read_text())[
        "body_frame_pt"
    ]
    # 잔여 10pt — 어느 팩의 2단 헤딩 블록(v + 행)도 못 들어가는 크기
    filler = frame["y1"] - frame["y0"] - 10.0
    doc = "\n".join([
        '#import "base.typ": base',
        '#import "theme.typ": theme',
        "#show: base",
        "#show: theme",
        "",
        f"#block(height: {filler:.2f}pt)[]",
        "== 한계와 남는 의문",
        "본문 한 줄.",
        "",
    ])
    (tmp / "main.typ").write_text(doc, encoding="utf-8")
    out = tmp / "probe.pdf"
    r = subprocess.run(
        [typst_binary(), "compile", str(tmp / "main.typ"), str(out), "--root", str(tmp)],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr
    page = fitz.open(out)[1]
    spans = [
        s
        for b in page.get_text("dict")["blocks"]
        for l in b.get("lines", [])
        for s in l["spans"]
    ]
    head = next(s for s in spans if "한계" in s["text"])
    return head["bbox"][1], frame["y0"]


@pytest.mark.parametrize("style", ["b5", "business", "essay", "lecture", "practical"])
def test_level2_heading_at_page_top_stays_in_frame(style):
    with tempfile.TemporaryDirectory() as d:
        y0, frame_top = _compile(Path(d), style)
        assert y0 >= frame_top, (
            f"{style}: 2단 헤딩 글리프 y0={y0:.2f} < 프레임 상단 {frame_top:.2f}"
        )
