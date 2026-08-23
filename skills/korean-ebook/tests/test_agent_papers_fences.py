"""agent-papers-2026-ko 펜스 불변식 — 수·레이아웃 구성 고정."""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
BOOK = REPO / "books" / "agent-papers-2026-ko" / "manuscript"
# md2typst.IG_RE와 동일 패턴 — 검증 대상과 파서가 같은 펜스를 보게(후행 공백·들여쓰기 경계 포함)
FENCE = re.compile(r"^```infographic[ \t]*\n(.*?)^```[ \t]*$", re.S | re.M)

EXPECTED = {
    "00-들어가며.md": ["cards"],
    "01-제1장-도구를-다-쥐여주면.md": ["ladder"],
    "02-제2장-새-대화창을-열면.md": ["cards"],
    "03-제3장-읽은-파일과-고친-파일.md": ["topology"],
    "04-제4장-일은-끝났는데.md": ["cards"],
    "05-제5장-여덟-명이-붙으면.md": ["cards"],
    "06-제6장-많이-찾아다-주면.md": ["matrix"],
    "07-제7장-왜-그렇게-정했더라.md": ["matrix"],
    "08-제8장-내가-넣은-한-줄은.md": ["ladder"],
    "09-제9장-잘-나온-결과-하나로.md": ["cards"],
    "10-제10장-만들기-전에-약속.md": ["before_after"],
}


def _fences(text: str) -> list[dict]:
    return [json.loads(m) for m in FENCE.findall(text)]


def test_fence_count_and_layouts():
    total = 0
    for name, layouts in EXPECTED.items():
        fences = _fences((BOOK / name).read_text(encoding="utf-8"))
        assert len(fences) == len(layouts), f"{name}: 펜스 {len(fences)}개 != {len(layouts)}개"
        got = [f["layout"] for f in fences]
        assert got == layouts, f"{name}: {got} != {layouts}"
        for f in fences:
            assert f["evidence"] == "§1", f"{name}: evidence {f['evidence']!r}"
        total += len(fences)
    assert total == 11


def test_no_stray_fences_outside_expected_files():
    for p in sorted(BOOK.glob("*.md")):
        if p.name in EXPECTED:
            continue
        assert not FENCE.search(p.read_text(encoding="utf-8")), f"{p.name}: 예상 밖 펜스"
