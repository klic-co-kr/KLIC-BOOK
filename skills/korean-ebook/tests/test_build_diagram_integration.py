"""build.py — ```diagram 펜스의 조립 통합 (에셋 생성·이미지 치환·임시파일 정리)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import build as bk  # noqa: E402


def _write_config(tmp_path, chapters=("manuscript/ch01.md",), style="practical"):
    (tmp_path / "manuscript").mkdir(parents=True, exist_ok=True)
    (tmp_path / "typst-build.yaml").write_text(
        f'style: "{style}"\ntitle: "테스트 책"\nchapters:\n'
        + "".join(f'  - "{c}"\n' for c in chapters), encoding="utf-8")


DIAGRAM_MD = (
    "## 제1장 · 시험\n\n본문 문단입니다.\n\n"
    "```diagram\n"
    '{"layout": "flow", "title": "검증을 통과해야 남는다", "caption": "그림 1-1 실행 주기",\n'
    '  "nodes": [{"id": "a", "label": "관찰 수신"}, {"id": "b", "label": "상태 병합", "tone": "green"}],\n'
    '  "edges": [{"from": "a", "to": "b"}]}\n'
    "```\n\n뒷문단.\n"
)


def test_expand_diagrams_creates_asset_and_image(tmp_path):
    _write_config(tmp_path)
    src = tmp_path / "manuscript" / "ch01.md"
    src.write_text(DIAGRAM_MD, encoding="utf-8")

    conv, tmp = bk._expand_diagrams(src, 0)
    try:
        assert conv != src
        svg_dir = tmp_path / "assets" / "diagrams"
        svgs = list(svg_dir.glob("000-ch01-dg01.svg"))
        assert len(svgs) == 1
        assert svgs[0].read_text(encoding="utf-8").startswith("<svg")
        body = conv.read_text(encoding="utf-8")
        assert "```diagram" not in body
        assert "![그림 1-1 실행 주기](../assets/diagrams/000-ch01-dg01.svg)" in body
    finally:
        tmp.unlink(missing_ok=True)
    # 원문 불변
    assert "```diagram" in src.read_text(encoding="utf-8")


def test_expand_diagrams_passthrough_without_fence(tmp_path):
    _write_config(tmp_path)
    src = tmp_path / "manuscript" / "ch01.md"
    src.write_text("## 제1장 · 시험\n\n펜스 없음.\n", encoding="utf-8")
    conv, tmp = bk._expand_diagrams(src, 0)
    assert conv == src and tmp is None


def test_assemble_converts_fence_to_figure(tmp_path):
    pytest.importorskip("fitz")
    _write_config(tmp_path)
    (tmp_path / "manuscript" / "ch01.md").write_text(DIAGRAM_MD, encoding="utf-8")
    cfg = bk.load_config(tmp_path / "typst-build.yaml")
    bk.assemble(cfg, tmp_path)
    typ = (tmp_path / "build" / "typ" / "000-ch01.typ").read_text(encoding="utf-8")
    assert "#figure(image(" in typ
    assert "caption: [그림 1-1 실행 주기]" in typ
    # 임시 확장 md는 정리된다
    assert not list((tmp_path / "manuscript").glob(".tmp-diag-*"))
