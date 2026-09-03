"""오프너 변조 활성 경로 컴파일 회귀 — openers.typ enabled 분기.

base.typ의 밝은 오프너(크림 지면·우측 세로 스트립·_occ 인덱싱)은
비활성 stub만으로는 컴파일되지 않는다(적대검토 — 활성 경로 테스트 0건).
여기서는 build가 내놓는 형태의 openers.typ을 직접 만들어 H1 오프너가
에러 없이 렌더되는지와 모듈 계약(enabled·openers 배열)을 검증한다.
"""
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest

from scripts.build import typst_binary
from scripts.cover_compositions import PROFILES, opener_strip, pick_profile

pytestmark = pytest.mark.skipif(shutil.which("typst") is None, reason="typst 미설치")

SKILL = Path(__file__).resolve().parents[1]


def _write_enabled_openers(tmp: Path, n: int = 3) -> None:
    prof = pick_profile("에이전트는 하니스를 배운다")
    acc = "1F4E79"
    frags = [opener_strip(prof, i, brand=acc, pale="CDD8E1") for i in range(n)]
    (tmp / "openers.typ").write_text(
        '#let opener-enabled = true\n'
        '#let opener-paper = rgb("F7F4EE")\n'
        f'#let opener-brand = rgb("{acc}")\n'
        '#let openers = (\n  ' + ',\n  '.join(frags) + ',\n)\n',
        encoding="utf-8")


def test_enabled_opener_compiles_and_renders(tmp_path):
    for name, src in (
        ("base.typ", SKILL / "templates" / "base.typ"),
        ("openers.typ", None),  # 활성 스텁을 직접 생성
        ("klic-flat-dark.tmTheme", SKILL / "templates" / "klic-flat-dark.tmTheme"),
        ("theme.typ", SKILL / "styles" / "lecture" / "theme.typ"),
        ("tokens.json", SKILL / "styles" / "lecture" / "tokens.json"),
    ):
        if src is None:
            _write_enabled_openers(tmp_path)
        else:
            shutil.copy2(src, tmp_path / name)
    # raw 스타일 tokens에는 book.short가 없다 — 실제 조립은 build.py가
    # 주입한다(main.typ 러닝헤드가 H1 이후 면에서 _book-short를 부름).
    import json
    toks = json.loads((tmp_path / "tokens.json").read_text(encoding="utf-8"))
    toks["book"] = {"short": "TEST"}
    (tmp_path / "tokens.json").write_text(
        json.dumps(toks, ensure_ascii=False), encoding="utf-8")
    doc = "\n".join([
        '#import "base.typ": base',
        '#import "theme.typ": theme',
        "#show: base",
        "#show: theme",
        "",
        "= 첫째 장",
        "본문 한 줄.",
        "",
        "= 둘째 장",
        "본문 한 줄.",
        "",
    ])
    (tmp_path / "main.typ").write_text(doc, encoding="utf-8")
    out = tmp_path / "probe.pdf"
    r = subprocess.run(
        [typst_binary(), "compile", str(tmp_path / "main.typ"), str(out),
         "--root", str(tmp_path)],
        capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert out.exists() and out.stat().st_size > 0


def test_opener_strip_every_profile_emits():
    # 50 프로파일 전부 오프너 조각을 만들 수 있어야 한다 —
    # none도 최소 마커(횡선)를 남긴다.
    for prof in PROFILES:
        frag = opener_strip(prof, 0, brand="1F4E79", pale="CDD8E1")
        assert "stack" in frag, prof


def test_opener_strip_varies_by_chapter():
    prof = pick_profile("에이전트는 하니스를 배운다")
    a = opener_strip(prof, 0, brand="1F4E79", pale="CDD8E1")
    b = opener_strip(prof, 1, brand="1F4E79", pale="CDD8E1")
    assert a != b
