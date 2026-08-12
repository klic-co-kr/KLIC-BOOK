from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from generate_visuals import generate_all, generate_chart  # noqa: E402


ASSET_IDS = [*(f"FIG-{n:03d}" for n in range(1, 13)), *(f"CHT-{n:03d}" for n in range(1, 9))]
FORBIDDEN = ("<script", "<image", "data:", "linearGradient", "radialGradient", "var(")
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF]")


def asset_path(asset_id: str) -> Path:
    folder = "figures" if asset_id.startswith("FIG") else "charts"
    return ROOT / "assets" / folder / f"{asset_id}.svg"


def test_all_twenty_assets_are_referenced_and_generated() -> None:
    manuscript = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "manuscript").glob("*.md"))
    referenced = set(re.findall(r"^id: ((?:FIG|CHT)-\d{3})$", manuscript, re.MULTILINE))

    assert set(ASSET_IDS) <= referenced
    assert all(asset_path(asset_id).exists() for asset_id in ASSET_IDS)


def test_svg_contract() -> None:
    for asset_id in ASSET_IDS:
        path = asset_path(asset_id)
        text = path.read_text(encoding="utf-8")
        root = ET.fromstring(text)

        assert root.attrib.get("viewBox") == "0 0 1600 900", asset_id
        assert any(child.tag.endswith("title") and (child.text or "").strip() for child in root), asset_id
        assert any(child.tag.endswith("desc") and (child.text or "").strip() for child in root), asset_id
        assert not any(token in text for token in FORBIDDEN), asset_id
        assert not EMOJI_RE.search(text), asset_id
        assert "font-family" in text, asset_id


def test_charts_show_evidence_label_source_and_unit() -> None:
    for asset_id in (f"CHT-{n:03d}" for n in range(1, 9)):
        text = asset_path(asset_id).read_text(encoding="utf-8")
        assert any(label in text for label in ("공식 발표", "원자료", "가정 계산")), asset_id
        assert re.search(r"SRC-\d{3}|출처 없음", text), asset_id
        assert "단위:" in text, asset_id


def test_independent_metrics_render_as_separate_panels() -> None:
    text = asset_path("CHT-004").read_text(encoding="utf-8")

    assert 'data-panel="annual-failure"' in text
    assert 'data-panel="mean-time-between-failure"' in text


def test_generation_is_deterministic() -> None:
    generate_all(ROOT)
    first = {asset_id: asset_path(asset_id).read_bytes() for asset_id in ASSET_IDS}
    generate_all(ROOT)
    second = {asset_id: asset_path(asset_id).read_bytes() for asset_id in ASSET_IDS}

    assert first == second


def test_chart_rejects_missing_claim(tmp_path: Path) -> None:
    spec = {"title": "test", "claim_ids": ["CLM-999"], "series": []}

    try:
        generate_chart("CHT-999", spec, {}, tmp_path / "missing.svg")
    except KeyError as exc:
        assert "CLM-999" in str(exc)
    else:
        raise AssertionError("missing claim must fail")
