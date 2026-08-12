from __future__ import annotations

"""Generate the FactoryX book's source-traceable, pure-SVG visual assets."""

import argparse
import html
from pathlib import Path
from typing import Any

import yaml


WIDTH = 1600
HEIGHT = 900
EXPECTED_IDS = [
    *(f"FIG-{number:03d}" for number in range(1, 13)),
    *(f"CHT-{number:03d}" for number in range(1, 9)),
]


def _escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def _frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"YAML frontmatter가 없습니다: {path}")
    _, raw, _ = text.split("---", 2)
    spec = yaml.safe_load(raw)
    if not isinstance(spec, dict):
        raise ValueError(f"명세가 YAML 객체가 아닙니다: {path}")
    return spec


def _records(path: Path, key: str) -> dict[str, dict[str, Any]]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    rows = data.get(key, []) if isinstance(data, dict) else []
    return {str(row["id"]): row for row in rows}


def _tspans(x: float, y: float, lines: list[str], css_class: str, anchor: str = "start") -> str:
    safe_lines = lines or [""]
    spans = "".join(
        f'<tspan x="{x:.1f}" dy="{0 if index == 0 else 30}">{_escape(line)}</tspan>'
        for index, line in enumerate(safe_lines)
    )
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{css_class}" text-anchor="{anchor}">{spans}</text>'


def _svg(asset_id: str, title: str, desc: str, body: list[str]) -> str:
    css = """
.paper { fill: #f7f5ef; }
.band { fill: #10324a; }
.surface { fill: #dce8e8; stroke: #10324a; stroke-width: 3; }
.surface-teal { fill: #d7eceb; stroke: #087e8b; stroke-width: 3; }
.surface-amber { fill: #f4e5c9; stroke: #d18b24; stroke-width: 3; }
.line { stroke: #7f9ba0; stroke-width: 4; fill: none; marker-end: url(#arrow); }
.rule { stroke: #7f9ba0; stroke-width: 2; }
.title { font-family: 'Noto Serif CJK KR', serif; font-size: 38px; font-weight: 700; fill: #f7f5ef; }
.subtitle { font-family: 'Noto Sans CJK KR', sans-serif; font-size: 22px; fill: #18313f; }
.body { font-family: 'Noto Sans CJK KR', sans-serif; font-size: 21px; fill: #18313f; }
.small { font-family: 'Noto Sans CJK KR', sans-serif; font-size: 17px; fill: #18313f; }
.value { font-family: 'Noto Sans CJK KR', sans-serif; font-size: 24px; font-weight: 700; fill: #10324a; }
.node-label { font-family: 'Noto Sans CJK KR', sans-serif; font-size: 21px; font-weight: 700; fill: #18313f; }
.bar-teal { fill: #087e8b; }
.bar-navy { fill: #10324a; }
.bar-amber { fill: #d18b24; }
""".strip()
    content = "\n  ".join(body)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="{asset_id}-title {asset_id}-desc">
  <title id="{asset_id}-title">{_escape(title)}</title>
  <desc id="{asset_id}-desc">{_escape(desc)}</desc>
  <defs>
    <style>{css}</style>
    <marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><polygon points="0,0 12,6 0,12" fill="#7f9ba0"/></marker>
  </defs>
  <rect class="paper" width="1600" height="900"/>
  <rect class="band" width="1600" height="112"/>
  {_tspans(90, 68, [title], "title")}
  {content}
</svg>
'''


def _source_line(source_ids: list[str], evidence_label: str) -> str:
    sources = " · ".join(source_ids) if source_ids else "출처 없음"
    return f"근거: {evidence_label} | {sources}"


def _edge_endpoints(start: dict[str, Any], end: dict[str, Any]) -> tuple[float, float, float, float]:
    """Return two points on node boundaries, leaving labels and surfaces unobscured."""
    start_w, start_h = float(start.get("w", 250)), float(start.get("h", 112))
    end_w, end_h = float(end.get("w", 250)), float(end.get("h", 112))
    start_x = float(start["x"]) + start_w / 2
    start_y = float(start["y"]) + start_h / 2
    end_x = float(end["x"]) + end_w / 2
    end_y = float(end["y"]) + end_h / 2
    dx, dy = end_x - start_x, end_y - start_y
    if dx == 0 and dy == 0:
        raise ValueError("간선의 시작과 끝이 같습니다")
    start_scale = 1 / max(abs(dx) / (start_w / 2), abs(dy) / (start_h / 2))
    end_scale = 1 / max(abs(dx) / (end_w / 2), abs(dy) / (end_h / 2))
    return (
        start_x + dx * start_scale,
        start_y + dy * start_scale,
        end_x - dx * end_scale,
        end_y - dy * end_scale,
    )


def _validate_sources(spec: dict[str, Any], sources: dict[str, dict[str, Any]]) -> list[str]:
    source_ids = [str(source_id) for source_id in spec.get("source_ids", [])]
    missing = [source_id for source_id in source_ids if source_id not in sources]
    if missing:
        raise KeyError(", ".join(missing))
    return source_ids


def generate_figure(asset_id: str, spec: dict, out_path: Path) -> None:
    """Render a node-and-edge technical diagram from an explicit visual spec."""
    if spec.get("kind") != "figure":
        raise ValueError(f"{asset_id}: figure 명세가 아닙니다")
    nodes = spec.get("nodes")
    edges = spec.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        raise ValueError(f"{asset_id}: nodes와 edges가 필요합니다")

    indexed = {str(node["id"]): node for node in nodes}
    if len(indexed) != len(nodes):
        raise ValueError(f"{asset_id}: node id가 중복됩니다")

    body = [
        _tspans(90, 154, [str(spec["caption"])], "subtitle"),
        '<line class="rule" x1="90" y1="182" x2="1510" y2="182"/>',
    ]
    for edge in edges:
        start = indexed.get(str(edge.get("from")))
        end = indexed.get(str(edge.get("to")))
        if start is None or end is None:
            raise KeyError(f"{asset_id}: edge가 없는 node을 참조합니다")
        x1, y1, x2, y2 = _edge_endpoints(start, end)
        body.append(f'<line class="line" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>')

    classes = ["surface", "surface-teal", "surface-amber"]
    for index, node in enumerate(nodes):
        x, y = float(node["x"]), float(node["y"])
        width, height = float(node.get("w", 250)), float(node.get("h", 112))
        css_class = classes[index % len(classes)]
        body.append(
            f'<rect class="{css_class}" x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" rx="14"/>'
        )
        label = str(node["label"]).split("\n")
        first_y = y + height / 2 - ((len(label) - 1) * 15)
        body.append(_tspans(x + width / 2, first_y, label, "node-label", "middle"))

    body.extend(
        [
            '<line class="rule" x1="90" y1="790" x2="1510" y2="790"/>',
            _tspans(90, 830, [_source_line(list(spec.get("source_ids", [])), str(spec.get("evidence_label", "원자료")))], "small"),
            _tspans(90, 862, [f"{asset_id} | {spec['alt_ko']}"], "small"),
        ]
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(_svg(asset_id, str(spec["title"]), str(spec["alt_ko"]), body), encoding="utf-8")


def _claim_value(claim: dict[str, Any], datum: dict[str, Any]) -> float:
    value = claim.get("value")
    if isinstance(value, list):
        if "index" not in datum:
            raise ValueError(f"{datum['claim_id']}: 배열 claim에는 index가 필요합니다")
        value = value[int(datum["index"])]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{datum['claim_id']}: 숫자 claim이 아닙니다")

    calculation = datum.get("calculation", "raw")
    transform = str(claim.get("transform", ""))
    if calculation == "raw":
        return float(value)
    if calculation == "baseline_100" and "air-100" in transform:
        return 100.0
    if calculation == "inverse_index" and transform.startswith("air-100-liquid"):
        return 100.0 / float(value)
    if calculation == "ratio_index" and transform.startswith("air-100-liquid"):
        return float(value) * 100.0
    raise ValueError(f"{datum['claim_id']}: 허용되지 않은 계산 {calculation}")


def _number(value: float, precision: int | None = None) -> str:
    if precision is not None:
        return f"{value:.{precision}f}"
    if value.is_integer():
        return str(int(value))
    return f"{value:.1f}".rstrip("0").rstrip(".")


def generate_chart(asset_id: str, spec: dict, claims: dict, out_path: Path) -> None:
    """Render a chart whose every plotted datum resolves to a registered claim."""
    claim_ids = [str(claim_id) for claim_id in spec.get("claim_ids", [])]
    if not claim_ids:
        raise ValueError(f"{asset_id}: numeric chart에는 claim_ids가 필요합니다")
    for claim_id in claim_ids:
        if claim_id not in claims:
            raise KeyError(claim_id)
    if spec.get("kind") not in (None, "chart"):
        raise ValueError(f"{asset_id}: chart 명세가 아닙니다")

    points: list[tuple[str, str, float, dict[str, Any], dict[str, Any]]] = []
    for series in spec.get("series", []):
        series_name = str(series.get("name", "series"))
        for datum in series.get("values", []):
            claim_id = str(datum.get("claim_id", ""))
            if claim_id not in claim_ids:
                raise ValueError(f"{asset_id}: datum의 claim_id가 claim_ids에 없습니다: {claim_id}")
            if claim_id not in claims:
                raise KeyError(claim_id)
            points.append(
                (
                    series_name,
                    str(datum["label"]),
                    _claim_value(claims[claim_id], datum),
                    datum,
                    claims[claim_id],
                )
            )
    if not points:
        raise ValueError(f"{asset_id}: numeric chart에는 claim 기반 datum이 필요합니다")

    maximum = max(value for _, _, value, _, _ in points)
    if maximum <= 0:
        raise ValueError(f"{asset_id}: 양수 datum이 필요합니다")
    plot_left, plot_right, plot_top, plot_bottom = 140.0, 1500.0, 300.0, 675.0
    slot = (plot_right - plot_left) / len(points)
    bar_width = min(172.0, slot * 0.56)
    body = [
        _tspans(90, 154, [str(spec["caption"])], "subtitle"),
        '<line class="rule" x1="90" y1="182" x2="1510" y2="182"/>',
        f'<line class="rule" x1="{plot_left:.1f}" y1="{plot_bottom:.1f}" x2="{plot_right:.1f}" y2="{plot_bottom:.1f}"/>',
        _tspans(plot_left, 255, [f"단위: {spec['unit']}"], "body"),
    ]
    independent_panels = bool(spec.get("independent_panels"))
    panel_maxima: dict[str, float] = {}
    if independent_panels:
        panel_order = list(dict.fromkeys(series_name for series_name, _, _, _, _ in points))
        for series_name in panel_order:
            panel_maxima[series_name] = max(
                value for point_series, _, value, _, _ in points if point_series == series_name
            )
        panel_width = (plot_right - plot_left) / len(panel_order)
        for panel_index, series_name in enumerate(panel_order):
            panel_x = plot_left + panel_index * panel_width
            if panel_index:
                body.append(
                    f'<line class="rule" x1="{panel_x:.1f}" y1="286" '
                    f'x2="{panel_x:.1f}" y2="660"/>'
                )
            panel_label = "연간 장애율 지수" if series_name == "annual-failure" else "평균 무고장 시간 지수"
            body.append(
                f'<g data-panel="{_escape(series_name)}">'
                f'{_tspans(panel_x + panel_width / 2, 270, [panel_label], "small", "middle")}'
                f'</g>'
            )
    colors = ["bar-teal", "bar-navy", "bar-amber"]
    for index, (series_name, label, value, datum, _) in enumerate(points):
        scale_maximum = panel_maxima.get(series_name, maximum)
        height = max(4.0, (value / scale_maximum) * (plot_bottom - plot_top))
        x = plot_left + slot * index + (slot - bar_width) / 2
        y = plot_bottom - height
        body.append(
            f'<rect data-panel="{_escape(series_name)}" class="{colors[index % len(colors)]}" '
            f'x="{x:.1f}" y="{y:.1f}" width="{bar_width:.1f}" height="{height:.1f}" rx="8"/>'
        )
        body.append(_tspans(x + bar_width / 2, y - 16, [_number(value, datum.get("precision"))], "value", "middle"))
        body.append(_tspans(x + bar_width / 2, 714, label.split("\n"), "small", "middle"))

    source_ids: list[str] = []
    labels: list[str] = []
    for claim_id in claim_ids:
        claim = claims[claim_id]
        for source_id in claim.get("source_ids", []):
            if source_id not in source_ids:
                source_ids.append(str(source_id))
        label = "가정 계산" if claim.get("label") == "저자 계산" else str(claim.get("label", "원자료"))
        if label not in labels:
            labels.append(label)
    evidence = " · ".join(labels)
    body.extend(
        [
            '<line class="rule" x1="90" y1="770" x2="1510" y2="770"/>',
            _tspans(90, 812, [f"증거 표시: {evidence}"], "small"),
            _tspans(90, 844, [_source_line(source_ids, evidence)], "small"),
            _tspans(90, 876, [f"{asset_id} | {spec['alt_ko']}"], "small"),
        ]
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(_svg(asset_id, str(spec["title"]), str(spec["alt_ko"]), body), encoding="utf-8")


def generate_all(root: Path) -> None:
    """Read both evidence registries and generate every declared FactoryX visual."""
    root = Path(root)
    claims = _records(root / "research" / "claim-register.yaml", "claims")
    sources = _records(root / "research" / "source-register.yaml", "sources")
    spec_dir = root / "assets" / "specs"
    for asset_id in EXPECTED_IDS:
        spec_path = spec_dir / f"{asset_id}.md"
        spec = _frontmatter(spec_path)
        if spec.get("id") != asset_id:
            raise ValueError(f"{spec_path}: id가 {asset_id}와 다릅니다")
        _validate_sources(spec, sources)
        if asset_id.startswith("FIG-"):
            generate_figure(asset_id, spec, root / "assets" / "figures" / f"{asset_id}.svg")
        else:
            generate_chart(asset_id, spec, claims, root / "assets" / "charts" / f"{asset_id}.svg")


def main() -> int:
    parser = argparse.ArgumentParser(description="FactoryX SVG visual generator")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    generate_all(args.root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
