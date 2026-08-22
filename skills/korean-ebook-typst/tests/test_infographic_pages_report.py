"""infographic_pages 리포트(스펙 §5.4 개정 6판) — metadata 페이지 매핑·일치 검사·PNG 렌더."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))

from scripts.infographic import emit, render as ig_render

try:
    from scripts.build import typst_binary  # noqa: E402
    TYPST = typst_binary()   # typst 부재 시 build._fail이 SystemExit(1) — 수용해 skip
except SystemExit:
    TYPST = None

BOOK = """# 검증용 장

```infographic
{"layout": "flow", "title": "절차는 두 단계로 끝난다",
 "steps": [{"title": "준비", "text": "전제를 확인한다."},
           {"title": "실행", "text": "절차를 수행한다."}]}
```

본문 산문 한 줄.
"""


def _book(tmp_path: Path) -> Path:
    (tmp_path / "typst-build.yaml").write_text(
        "title: 검증책\nsubtitle: 부제\nauthor: 저자\nstyle: practical\ncover: auto\n"
        "chapters: [ch01.md]\n", encoding="utf-8")
    (tmp_path / "ch01.md").write_text(BOOK, encoding="utf-8")
    return tmp_path


pytestmark = pytest.mark.skipif(not TYPST or not Path(TYPST).exists(), reason="typst 없음")


def test_manifest_and_metadata_prefix(tmp_path):
    import scripts.build as b
    book = _book(tmp_path)
    # 호출 계약(test_build_compile.py 복제): load_config가 정규화한 cfg를
    # assemble에 넘긴다 — make_auto_cover가 cfg["cover_notes"]를 직접 첨자접근.
    cfg = b.load_config(book / "typst-build.yaml")
    main_typ = b.assemble(cfg, book)
    build = book / "build"
    manifest = json.loads((build / "infographic" / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["count"] == 1
    fig = manifest["figs"][0]
    assert fig["name"] == "000-fig01.typ" and fig["index"] == 1
    body = (build / "infographic" / fig["name"]).read_text(encoding="utf-8")
    assert body.splitlines()[0] == ('#context metadata((kind: "ig-fig", name: "000-fig01.typ", '
                                    'page: here().page()))')


def test_alias_warning_printed(tmp_path, capsys):
    import scripts.build as b
    book = _book(tmp_path)
    (book / "ch01.md").write_text(
        BOOK.replace('"layout": "flow"', '"layout": "process"'), encoding="utf-8")
    # cover_notes 포함 — make_auto_cover가 cfg["cover_notes"]를 직접 첨자접근(위 호출 계약)
    cfg = {"title": "검증책", "subtitle": "부제", "author": "저자", "style": "practical",
           "cover": "auto", "chapters": ["ch01.md"], "cover_notes": None}
    b.assemble(cfg, book)   # 기존 통합 테스트 호출 계약 — process 별칭이 flow로 정규화돼 빌드 성공
    out = capsys.readouterr().out
    assert "별칭 process→flow — 정식 키워드 권장" in out
    assert "000-ch01.md #1" in out
    # 채널 이원(G1-L10): 콘솔 + 검수 시트 상단 — 로그를 놓쳐도 gate 산출물에 남는다
    sheet = (book / "build" / "infographic" / "000-fig01.review.md").read_text(encoding="utf-8")
    assert "별칭 process→flow — 정식 키워드 권장" in sheet


def test_query_reports_page_and_gate_field(tmp_path):
    import scripts.build as b
    from scripts import qc_gate
    book = _book(tmp_path)
    cfg = b.load_config(book / "typst-build.yaml")
    main_typ = b.assemble(cfg, book)
    b.compile_pdf(main_typ, cfg["title"])
    rc = qc_gate.run(book)
    assert rc == 0
    report = json.loads((book / "gate-report.json").read_text(encoding="utf-8"))
    igp = report["infographic_pages"]
    assert igp["count"] == 1 and igp["expected"] == 1 and igp["match"] is True
    page = igp["figs"][0]["page"]
    assert isinstance(page, int) and page >= 1
    import fitz
    doc = fitz.open(book / "draft" / "검증책.pdf")
    assert page <= doc.page_count
    pngs = sorted((book / "build" / "infographic").glob("review-p*.png"))
    assert len(pngs) == len({f["page"] for f in igp["figs"]})
    assert pngs and pngs[0].stat().st_size > 10_000
