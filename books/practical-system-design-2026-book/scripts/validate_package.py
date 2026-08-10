from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []

def fail(message: str) -> None:
    errors.append(message)

def load_yaml(rel: str):
    try:
        return yaml.safe_load((ROOT / rel).read_text(encoding='utf-8'))
    except Exception as exc:
        fail(f"YAML parse failure {rel}: {exc}")
        return {}

book = load_yaml('book.manifest.yaml')
chapters_doc = load_yaml('manifests/chapters.yaml')
assets_doc = load_yaml('manifests/assets.yaml')
sources_doc = load_yaml('manifests/sources.yaml')
chapters = chapters_doc.get('chapters', [])
assets = assets_doc.get('assets', [])
sources = {s['id'] for s in sources_doc.get('sources', [])}

expected_chapters = [f'ch{i:02d}' for i in range(1,39)]
ids = [c.get('id') for c in chapters]
if ids != expected_chapters:
    fail(f'chapter ids/order mismatch: {ids}')
if len(chapters) != 38:
    fail(f'chapter count: expected 38, got {len(chapters)}')

required_headings = [
    '## 이 장에서 해결할 문제','## 먼저 결론','## 요구사항과 실패 모델',
    '## 핵심 개념','## 기준 아키텍처','## 요청·데이터 흐름',
    '## 대안과 트레이드오프','## 장애 시나리오','## 확장 전략',
    '## 보안과 개인정보','## 관측 가능성','## 비용과 운영 복잡도',
    '## 흔한 오해와 안티패턴','## 설계 리뷰','## 연습문제','## 핵심 요약','## 출처'
]
figure_ids_seen: list[str] = []
source_refs_seen: set[str] = set()
for c in chapters:
    path = ROOT / c['file']
    if not path.exists():
        fail(f'missing chapter file: {c["file"]}')
        continue
    text = path.read_text(encoding='utf-8')
    if len(text) < 5500:
        fail(f'chapter too short ({len(text)} chars): {c["id"]}')
    for h in required_headings:
        if h not in text:
            fail(f'missing heading {h} in {c["id"]}')
    if re.search(r'\b(TODO|TBD|FIXME)\b', text, re.I):
        fail(f'placeholder token in {c["id"]}')
    blocks = re.findall(r'<!-- figure-spec\n(.*?)\n-->', text, re.S)
    parsed_ids = []
    for b in blocks:
        try:
            spec = yaml.safe_load(b)
            parsed_ids.append(spec['id'])
        except Exception as exc:
            fail(f'figure-spec parse failure in {c["id"]}: {exc}')
    if parsed_ids != c['figures']:
        fail(f'figure list mismatch {c["id"]}: manifest={c["figures"]} body={parsed_ids}')
    figure_ids_seen.extend(parsed_ids)
    for ref in c.get('source_refs', []):
        source_refs_seen.add(ref)
        if ref not in sources:
            fail(f'unknown source {ref} in {c["id"]}')

asset_ids = [a.get('id') for a in assets]
if len(asset_ids) != len(set(asset_ids)):
    fail('duplicate asset ids')
if len(assets) != 119:
    fail(f'asset count: expected 119, got {len(assets)}')
kind_counts = {}
for a in assets:
    kind_counts[a['kind']] = kind_counts.get(a['kind'], 0) + 1
    spec_rel = a.get('spec_file') or a.get('prompt_file')
    if not spec_rel or not (ROOT / spec_rel).exists():
        fail(f'missing asset specification for {a["id"]}: {spec_rel}')
    if a.get('status') != 'specified':
        fail(f'asset not specified: {a["id"]}')
if kind_counts != {'conceptual-illustration': 19, 'technical-diagram': 88, 'data-chart': 12}:
    fail(f'asset kinds mismatch: {kind_counts}')

chapter_asset_ids = {a['id'] for a in assets if a.get('chapter')}
if set(figure_ids_seen) != chapter_asset_ids:
    fail(f'chapter figure coverage mismatch: body={len(set(figure_ids_seen))}, manifest={len(chapter_asset_ids)}')

book_text = (ROOT / 'BOOK.md').read_text(encoding='utf-8')
for i in range(1,39):
    if not re.search(rf'^# {i:02d}\.', book_text, re.M):
        fail(f'BOOK.md missing chapter {i:02d}')
if len(book_text) < 250000:
    fail(f'BOOK.md unexpectedly short: {len(book_text)} chars')

if book.get('visual_budget',{}).get('total') != 119:
    fail('root manifest visual budget mismatch')
if book.get('draft_boundaries',{}).get('actual_visual_binaries_generated') is not False:
    fail('draft boundary must state visual binaries are not generated')

if errors:
    print('VALIDATION FAILED')
    for e in errors:
        print('-', e)
    sys.exit(1)

print('VALIDATION OK')
print(f'chapters={len(chapters)}')
print(f'assets={len(assets)} technical={kind_counts.get("technical-diagram")} image2={kind_counts.get("conceptual-illustration")} charts={kind_counts.get("data-chart")}')
print(f'sources={len(sources)}')
print(f'book_chars={len(book_text)}')
print(f'chapter_chars={sum(len((ROOT / c["file"]).read_text(encoding="utf-8")) for c in chapters)}')
