"""test_infographic_compile.py — emit 산출물 컴파일 스모크(스펙 §7 통합 전 단계).

배치 주의(적대 검토 실증): fig.typ의 import는 "../helper.typ"이므로 fig를
하위 디렉터리에 두고 helper를 루트에 둬야 한다 — build/와 동일 구조.
같은 디렉터리에 두면 `path "../helper.typ" would escape the project root`.
"""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

from scripts.build import typst_binary
from scripts.infographic.archetypes import approval as approval_arch
from scripts.infographic.archetypes import flow as flow_arch
from scripts.infographic.archetypes import layers as layers_arch
from scripts.infographic.emit import render_typ
from scripts.infographic.parse import parse_fence

SKILL = Path(__file__).resolve().parents[1]
# typst 부재 시 typst_binary()는 falsy가 아니라 SystemExit(1)(build.py _fail)을
# 던진다 — 잡아서 빈 문자열로 돌려야 skipif가 도달한다(세션 전체 INTERNALERROR 방지).
try:
    TYPST = typst_binary()      # PATH → ~/.local/bin/typst 폴백 단일화(Global Constraints)
except SystemExit:
    TYPST = ""
pytestmark = pytest.mark.skipif(not TYPST, reason="typst 바이너리 없음")


def test_flow_fig_compiles(tmp_path):
    tokens = json.loads((SKILL / "styles" / "practical" / "tokens.json").read_text(encoding="utf-8"))
    fence = parse_fence(1, 1, json.dumps({
        "layout": "flow", "title": "컴파일 스모크",
        "steps": [{"title": "A", "text": "가"}, {"title": "B", "text": "나"}],
    }, ensure_ascii=False))
    out = render_typ(flow_arch.layout(fence, tokens))
    # build/와 동일 배치: 루트에 tokens·helper, 하위 infographic/에 fig
    (tmp_path / "tokens.json").write_text(json.dumps(tokens, ensure_ascii=False), encoding="utf-8")
    shutil.copy2(SKILL / "templates" / "infographic" / "helper.typ", tmp_path / "helper.typ")
    igdir = tmp_path / "infographic"; igdir.mkdir()
    (igdir / "fig.typ").write_text(out, encoding="utf-8")
    r = subprocess.run([TYPST, "compile", str(igdir / "fig.typ"),
                        str(igdir / "fig.pdf"), "--root", str(tmp_path)],
                       capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stderr
    assert (igdir / "fig.pdf").stat().st_size > 1000


def _smoke_compile(arch, payload: dict, tmp_path):
    """아키타입 산출 typst를 build/와 동일 배치(루트 tokens·helper, 하위 infographic/)로 컴파일."""
    tokens = json.loads((SKILL / "styles" / "practical" / "tokens.json").read_text(encoding="utf-8"))
    fence = parse_fence(1, 1, json.dumps(payload, ensure_ascii=False))
    out = render_typ(arch.layout(fence, tokens))
    (tmp_path / "tokens.json").write_text(json.dumps(tokens, ensure_ascii=False), encoding="utf-8")
    shutil.copy2(SKILL / "templates" / "infographic" / "helper.typ", tmp_path / "helper.typ")
    igdir = tmp_path / "infographic"; igdir.mkdir()
    (igdir / "fig.typ").write_text(out, encoding="utf-8")
    return subprocess.run([TYPST, "compile", str(igdir / "fig.typ"),
                           str(igdir / "fig.pdf"), "--root", str(tmp_path)],
                          capture_output=True, text=True, timeout=120), igdir


def test_approval_fig_compiles(tmp_path):
    # rot: 45deg 게이트 다이아몬드 마커를 포함한 방출물의 컴파일 스모크.
    r, igdir = _smoke_compile(approval_arch, {
        "layout": "approval", "title": "승인 경로 스모크",
        "path": [{"title": "기획"}, {"title": "검토", "gate": True}, {"title": "집행"}],
    }, tmp_path)
    assert r.returncode == 0, r.stderr
    assert (igdir / "fig.pdf").stat().st_size > 1000


def test_layers_rings_fig_compiles(tmp_path):
    # CircleOp → 조건부 ig-circle 헤더 임포트 + ig-circle 호출의 컴파일 스모크.
    r, igdir = _smoke_compile(layers_arch, {
        "layout": "layers", "title": "계층 스모크",
        "rings": [{"label": "표현"}, {"label": "논리"}, {"label": "자료"}],
    }, tmp_path)
    assert r.returncode == 0, r.stderr
    assert (igdir / "fig.pdf").stat().st_size > 1000
