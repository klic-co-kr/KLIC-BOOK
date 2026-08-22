# 인포그래픽 Phase 5 — composite·infographic_pages 리포트·가이드 완성 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 스펙 §3.5 복합 씬(composite) archetype + §5.4 검수 렌더·`infographic_pages` 리포트 + §8.5 가이드 완성으로 인포그래픽 레이어를 완성한다(Phase 4 최종 리뷰 LOW 2건 이관 해소 포함).

**Architecture:** composite는 기존 9 archetype의 `dispatch`를 재사용해 모듈 FigModel을 측정·병합(세로 스택, 배분 초과 시 모듈 단위 분할 에러). 페이지 대응은 각 도식 typ 앞 `#metadata((kind:"ig-fig", name:…, page: here().page()))` 프리픽스 → `typst query`로 수집 → `gate-report.json`의 `infographic_pages` 필드 + 검수 PNG(170 DPI) 렌더.

**Tech Stack:** Python 3.12 표준 라이브러리(재결정론 — 외부 의존 추가 없음), typst 0.15.1(query·compile `--pages`/`--ppi`), pytest. PyMuPDF(qc_gate 기존 사용) 페이지 수 대조.

**Spec:** `docs/superpowers/specs/2026-08-21-infographic-layer-design.md` (§3.4·§3.5·§5.4·§8.5; 본 플랜의 스펙 개정 6판 항 포함)

## Global Constraints

- 결정론: 동일 펜스 JSON + tokens → 바이트 동일 typst. datetime/random 금지.
- 모든 방출 숫자는 `_n()` = `f"{v:.2f}"`.
- 골든은 바이트 정확. 기존 골든 9종 바이트 불변(Task 3 rings 골든 1종 **신규 추가**만 허용).
- 손패치 금지 — 생성 typst/PDF 직수정 없음.
- 테스트 실행은 항상 스코프: `python3 -m pytest skills/korean-ebook-typst/tests/ -q`(루트 pytest는 books/ import SystemExit로 깨짐).
- 테스트 문구·에러 메시지 한국어. 커밋 컨벤션(`feat:`/`fix:`/`docs:`/`test:`), attribution footer 없음.
- 토큰 로드 관례: 테스트는 `json.loads((Path(__file__).resolve().parents[1] / "styles" / "<pack>" / "tokens.json").read_text(encoding="utf-8"))` 인라인(공용 fixture 부재).
- cli preview `--fig`는 **1-기반**(md2typst.py:23 `"index": len(fences) + 1`).
- ladder 4단계 practical 레이아웃 높이 = 프레임 85% 상한(426.93pt)을 꽉 채운다 — composite 배분 에러 테스트의 결정론 근거.
- 이관 과제(Phase 4 최종 리뷰 LOW): ① 별칭 사용 경고(스펙 §3.4 "경고 로그" 미구현 — parse `data["_alias"]` 미소비) ② rings 변형 바이트 골든 부재.

---

### Task 1: composite archetype

**Files:**
- Modify: `skills/korean-ebook-typst/scripts/infographic/parse.py`(composite 분기 + VALID_LAYOUTS 밖 별도 집합)
- Create: `skills/korean-ebook-typst/scripts/infographic/archetypes/composite.py`
- Modify: `skills/korean-ebook-typst/scripts/infographic/layout.py`(dispatch composite)
- Modify: `skills/korean-ebook-typst/scripts/infographic/lint.py`(모듈 필드 전개)
- Modify: `skills/korean-ebook-typst/scripts/infographic/render.py`(`_sheet_rows` 모듈 전개)
- Test: `skills/korean-ebook-typst/tests/test_infographic_layout_composite.py`(신규)
- Spec: `docs/superpowers/specs/2026-08-21-infographic-layer-design.md`(개정 6판 — 아래 Step 0)

**Interfaces:**
- Consumes: `dispatch(Fence, tokens) -> FigModel`(layout.py:10), `Fence(index, line, layout, title, thesis, kicker, note, evidence, data)`(parse.py:38), `sizes(tokens)`(base.py), `LayoutError`(base.py)
- Produces: `composite.layout(fence, tokens) -> FigModel`; `parse` composite 정규화 `data["modules"]`(각 모듈 dict: slot·layout·아키타입 payload 그대로); `lint`/`render` 모듈 필드 경로 `modules[j].<아키타입 경로>`; Task 2·4가 소비

**설계 판정(컨트롤러 — 스펙 해석):**
1. composite 최상위 `title`/`kicker`는 **선택**(스펙 §3.5 예시에 없음). 모듈이 각자 아키타입 헤더(자기 title)를 렌더한다. 최상위 title 있으면 composite가 kicker+title 블록을 추가.
2. "보조 모듈 축소" 자동 단계는 구현하지 않는다 — 글자·화살표 축소 금지(§3.5)와 모순되는 자동 축소 레버가 없다. 배분 초과 즉시 **모듈 단위 분할 에러**. **스펙 개정 6판**으로 §3.5 문장 교정(Step 0).
3. 모듈 아키타입 필드 검증(요소 수 등)은 `dispatch` 시점 — parse는 구조만(slot·개수·재귀·layout 키). 모듈 LayoutError는 기존 render 변환 경로를 그대로 탄다.
4. 배분: `H_avail = (y1−y0)·0.85`, `alloc_primary = min(측정높이, 0.6·H_avail)`, 보조 각 `alloc = (H_avail − alloc_primary − GAP·(n−1)) / n_supporting`(n=모듈 수). 초과분 에러 메시지는 스펙 스키마 그대로.

- [ ] **Step 0: 스펙 개정 6판 — composite 축소 문구 + 리포트 명칭**

`docs/superpowers/specs/2026-08-21-infographic-layer-design.md` 두 곳:

(a) §3.5 "공간 부족 시" 문단 교체:

```markdown
- 공간 부족 시: **모듈 단위 분할 에러**(자동 축소 없음 — 글자·화살표
  축소 금지와 모순되는 레버가 없다. 개정 6판).
  메시지 스키마: `{모듈 슬롯} {layout} 측정높이 {h:.2f}pt > 배분 {H:.2f}pt
  — 보조 모듈 n을 별도 펜스로 분할 권장`.
```

(b) §5.4 `build_report.json` → `gate-report.json`(구현 실제 명칭 — qc_gate.py:224). 두 occurrence.

커밋: `docs: 스펙 개정 6판 — composite 자동 축소 제거·리포트 명칭 gate-report 정합`

- [ ] **Step 1: 실패 테스트 작성**

`tests/test_infographic_layout_composite.py` 신규:

```python
"""composite — 복합 씬(스펙 §3.5): 모듈 측정·배분·세로 스택·분할 에러."""
import json
import sys
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))

from scripts.infographic import composite as comp_arch
from scripts.infographic.layout import dispatch
from scripts.infographic.parse import ParseError, parse_fence

TOKENS = json.loads((SKILL / "styles" / "practical" / "tokens.json").read_text(encoding="utf-8"))
ETOKENS = json.loads((SKILL / "styles" / "essay" / "tokens.json").read_text(encoding="utf-8"))

CARDS3 = {"layout": "cards",
          "title": "근거 카드 셋",
          "cards": [{"title": f"카드 {i}", "text": f"근거 문장 {i}."} for i in range(1, 4)]}
FLOW2 = {"layout": "flow", "title": "적용 절차",
         "steps": [{"title": "준비", "text": "전제를 확인한다."},
                   {"title": "실행", "text": "절차를 수행한다."}]}
LADDER4 = {"layout": "ladder", "title": "성숙도 계단", "thesis": "단계마다 확신이 쌓인다",
           "stages": [{"title": f"단계 {i}", "text": f"{t} 상태를 넘어선다."}
                      for i, t in enumerate(["사각", "관심", "실행", "정착"], 1)]}


def _fence(modules, title="구성과 절차를 한 장에 담는다", pack_tokens=TOKENS, **kw):
    body = {"layout": "composite", "modules": modules}
    if title is not None:
        body["title"] = title
    body.update(kw)
    f = parse_fence(1, 1, json.dumps(body, ensure_ascii=False))
    return f


def test_parse_bounds():
    with pytest.raises(ParseError):
        _fence([dict(CARDS3, slot="primary")])                     # 보조 0 — 모듈 2~3
    with pytest.raises(ParseError):
        _fence([dict(CARDS3, slot="primary")] +
               [dict(FLOW2, slot="supporting")] * 3)               # 보조 3 — 상한 2
    with pytest.raises(ParseError):
        _fence([dict(CARDS3, slot="main"),                         # slot 오타
                dict(FLOW2, slot="supporting")])
    with pytest.raises(ParseError):
        _fence([dict(CARDS3, slot="primary"), dict(FLOW2, slot="primary")])  # primary 2개
    with pytest.raises(ParseError):
        _fence([dict(CARDS3, slot="primary"),
                dict(LADDER4, slot="supporting", layout="composite")])      # 재귀
    with pytest.raises(ParseError):
        parse_fence(1, 1, json.dumps({"layout": "composite", "modules": [
            {"slot": "primary", "layout": "nope"}]}, ensure_ascii=False))   # unknown


def test_stack_geometry_and_gap():
    # title=None — fig.height = 모듈 높이 합 + GAP 정확히(헤더 블록 없음)
    f = _fence([dict(CARDS3, slot="primary"), dict(FLOW2, slot="supporting")], title=None)
    fig = comp_arch.layout(f, TOKENS)
    c = dispatch(_to_fence(1, 1, CARDS3), TOKENS)
    fl = dispatch(_to_fence(1, 1, FLOW2), TOKENS)
    assert abs(fig.height - (c.height + comp_arch.GAP + fl.height)) < 0.01


def test_title_block_adds_height_and_no_title_omits_it():
    mods = [dict(CARDS3, slot="primary"), dict(FLOW2, slot="supporting")]
    with_t = comp_arch.layout(_fence(mods), TOKENS)
    without = comp_arch.layout(_fence(mods, title=None), TOKENS)
    assert with_t.height > without.height            # 최상위 title 블록만큼 증가
    texts = [op.text for op in with_t.ops if op.__class__.__name__ == "TextOp"]
    assert "구성과 절차를 한 장에 담는다" in texts
    texts_wo = [op.text for op in without.ops if op.__class__.__name__ == "TextOp"]
    assert "구성과 절차를 한 장에 담는다" not in texts_wo


def _to_fence(index, line, d):
    body = dict(d)
    f = parse_fence(index, line, json.dumps(body, ensure_ascii=False))
    return f


def test_primary_over_sixty_percent_error():
    # ladder 4단계 practical = 프레임 85%(426.93) 점유 — 60% 상한 초과 확정
    f = _fence([dict(LADDER4, slot="primary"), dict(FLOW2, slot="supporting")])
    with pytest.raises(comp_arch.CompositeLayoutError, match="primary ladder 측정높이"):
        comp_arch.layout(f, TOKENS)


def test_supporting_over_allocation_error():
    # 보조 ladder 4단계(≈426.93)는 어떤 배분과도 초과 — 확정 에러
    f = _fence([dict(CARDS3, slot="primary"), dict(LADDER4, slot="supporting")])
    with pytest.raises(comp_arch.CompositeLayoutError, match="supporting ladder 측정높이"):
        comp_arch.layout(f, TOKENS)


def test_determinism():
    f = _fence([dict(CARDS3, slot="primary"), dict(FLOW2, slot="supporting")])
    a = comp_arch.layout(f, TOKENS)
    b = comp_arch.layout(_fence([dict(CARDS3, slot="primary"), dict(FLOW2, slot="supporting")]), TOKENS)
    assert [(op.__class__.__name__, getattr(op, "x", None), getattr(op, "y", None))
            for op in a.ops] == [(op.__class__.__name__, getattr(op, "x", None), getattr(op, "y", None))
                                 for op in b.ops]
```

주: `LADDER4`·`CARDS3`·`FLOW2` 페이로드는 각 archetype의 확정 스키마를 따른다(`stages[i].title/text`, `cards[i].title/text`, `steps[i].title/text` — `_sheet_rows` 경로와 일치). 실행 시 실제 필수 필드(예: ladder thesis)가 더 있으면 `test_infographic_layout_ladder.py` 등 기존 테스트의 펜스 형태를 복제해 채운다 — 배분 에러 테스트의 결정론(426.93pt 점유)은 stages 4개(practical PACK_STAGES=5 이하)가 유지하는 한 불변.

- [ ] **Step 2: RED 확인**

Run: `python3 -m pytest skills/korean-ebook-typst/tests/test_infographic_layout_composite.py -q`
Expected: FAIL — `ModuleNotFoundError: scripts.infographic.composite`

- [ ] **Step 3: parse composite 분기 + composite.py + dispatch + lint/render 전개**

`parse.py` — VALID_LAYOUTS 뒤 composite 구조 검색 분기(accumulator 관례, 다른 분기 뒤):

```python
if layout == "composite":
    mods = d.get("modules")
    if not isinstance(mods, list) or not (2 <= len(mods) <= 3):
        raise ParseError(index, "composite modules — 주 1 + 보조 1~2(2~3개 배열)", line)
    seen_slots = []
    norm = []
    for j, m in enumerate(mods):
        if not isinstance(m, dict):
            raise ParseError(index, f"modules[{j}] — 객체여야 한다", line)
        slot = m.get("slot")
        if slot not in ("primary", "supporting"):
            raise ParseError(index, f"modules[{j}].slot {slot!r} — primary|supporting", line)
        mlayout = m.get("layout")
        if mlayout == "composite":
            raise ParseError(index, f"modules[{j}].layout composite — 보조 모듈 재귀 금지", line)
        if mlayout not in VALID_LAYOUTS:
            raise ParseError(index, f"modules[{j}].layout {mlayout!r} — 알 수 없는 layout", line)
        mod = {k: (v.strip() if isinstance(v, str) else v) for k, v in m.items()}
        seen_slots.append(slot)
        norm.append(mod)
    if seen_slots.count("primary") != 1:
        raise ParseError(index, f"primary 정확히 1개 필요(현재 {seen_slots.count('primary')})", line)
    data["modules"] = norm
```

`Fence` title/kicker/thesis/note는 공통 추출부가 그대로 통과시킨다(composite는 title 선택 — 공통부의 title 누락 거부를 composite에서 완화하려면 공통 추출 **전**에 `if layout == "composite":` 분기로 `d.get("title")` 기본 `""` 삽입 후 공통부 진입. 구현 위치는 기존 공통 추출부 코드를 읽고 최소 변경점 선택).

`archetypes/composite.py`:

```python
"""composite — 복합 씬(스펙 §3.5): 모듈 측정·배분 검증·세로 스택. 자동 축소 없음(개정 6판)."""
from __future__ import annotations

from .. import layout as _layout
from ..model import FigModel, TextOp
from ..parse import Fence
from .base import LayoutError, sizes

GAP = 24.0
PRIMARY_FRAC = 0.6
HEIGHT_LIMIT = 0.85
LEADING = 1.3


class CompositeLayoutError(LayoutError):
    pass


def _module_fence(parent: Fence, m: dict) -> Fence:
    return Fence(index=parent.index, line=parent.line, layout=m["layout"],
                 title=m.get("title", ""), thesis=m.get("thesis"), kicker=m.get("kicker"),
                 note=m.get("note"), evidence=m.get("evidence"),
                 data={k: v for k, v in m.items()
                       if k not in ("slot", "layout", "title", "thesis", "kicker", "note", "evidence")})


def layout(fence: Fence, tokens: dict) -> FigModel:
    frame = tokens["body_frame_pt"]
    H_avail = (frame["y1"] - frame["y0"]) * HEIGHT_LIMIT
    s = sizes(tokens)
    mods = fence.data["modules"]
    figs = [(m, _layout.dispatch(_module_fence(fence, m), tokens)) for m in mods]

    prim = [(m, g) for m, g in figs if m["slot"] == "primary"][0]
    if prim[1].height > H_avail * PRIMARY_FRAC:
        raise CompositeLayoutError(
            f"primary {prim[0]['layout']} 측정높이 {prim[1].height:.2f}pt "
            f"> 배분 {H_avail * PRIMARY_FRAC:.2f}pt — 주 모듈 요소 수 감소 또는 펜스 분할 권장")

    alloc_supp = (H_avail - min(prim[1].height, H_avail * PRIMARY_FRAC)
                  - GAP * (len(figs) - 1)) / max(1, len(figs) - 1)
    for m, g in figs:
        if m["slot"] == "supporting" and g.height > alloc_supp:
            raise CompositeLayoutError(
                f"supporting {m['layout']} 측정높이 {g.height:.2f}pt > 배분 {alloc_supp:.2f}pt"
                f" — 보조 모듈 {len(figs) - 1}을(를) 별도 펜스로 분할 권장")

    head = []
    y = 0.0
    if fence.title:
        if fence.kicker:
            head.append(TextOp(x=frame["x0"], y=y, size=s["kicker"], text=fence.kicker,
                               role="label"))
            y += s["kicker"] * LEADING + 2.0
        head.append(TextOp(x=frame["x0"], y=y, size=s["title"], text=fence.title,
                           role="title", weight="bold"))
        y += s["title"] * LEADING + 10.0
    ops = list(head)
    for i, (m, g) in enumerate(figs):
        for op in g.ops:
            cloned = type(op)(**{k: (v if k != "y" else v + y) for k, v in vars(op).items()})
            ops.append(cloned)
        y += g.height
        if i < len(figs) - 1:
            y += GAP
    return FigModel(width=figs[0][1].width, height=y, ops=ops, source_index=fence.index)
```

주: `vars(op)` 얕은 복사 — dataclass 필드 전부 치환 재구성(불변 패턴). 최상위 title 블록 진행은 위 `head` 로직이 유일 진실(별도 상수 노출 없음 — 테스트는 유무 높이 차·텍스트 유무로 검증).

`layout.py` dispatch에:

```python
    if fence.layout == "composite":
        return _comp.layout(fence, tokens)
```

(import행에 `composite as _comp` 추가.)

`lint.py` 필드 평탄 수집부·`render.py` `_sheet_rows` — 기존 9종 루프를 그대로 두고 composite만 추가하면 9루프 3중 복제(lint·render·모듈)가 된다. 대신 **헬퍼 추출**: 양 파일의 필드 수집 루프를 동일 인자 `(title, kicker, thesis, data, prefix) -> list[tuple[str, str]]` 함수로 묶는다(`render.py`는 `_sheet_rows` 내부에서 이미 2-튜플 반환 — 그 본체를 `rows_from(title, kicker, thesis, data, prefix)`로 추출, 기존 경로는 `rows_from(f.title, f.kicker, f.thesis, f.data, "")` 호출. `lint.py`의 필드 수집부도 동일 구조로 추출해 동일 함수를 쓰려면 순환 임포트 주의 — lint가 render에서 임포트하지 않고 **각자 자기 파일에 유지**하되 동일 prefix 관계). composite 분기:

```python
    for j, m in enumerate(f.data.get("modules", [])):
        rows.extend(rows_from(m.get("title", ""), m.get("kicker"), m.get("thesis"),
                              m, f"modules[{j}]."))
```

경로 예: `ch01.md #1 modules[0].cards[0].title`.

- [ ] **Step 4: GREEN 확인**

Run: `python3 -m pytest skills/korean-ebook-typst/tests/test_infographic_layout_composite.py -q`
Expected: PASS 전 건(함수 6). 이후 전체: `python3 -m pytest skills/korean-ebook-typst/tests/ -q` — 기존 239 + 신규 6 = **245 passed**(골든·기존 무변경).

- [ ] **Step 5: 검수 시트 모듈 전개 + composite 바이트 골든**

같은 파일에 추가:

```python
def test_sheet_rows_reach_module_fields():
    from scripts.infographic import render as ig_render
    f = _fence([dict(CARDS3, slot="primary"), dict(FLOW2, slot="supporting")])
    rows = dict(ig_render._sheet_rows(f))
    assert rows["modules[0].cards[0].title"] == "카드 1"
    assert rows["modules[1].steps[0].title"] == "준비"


GOLDEN = Path(__file__).parent / "fixtures" / "infographic" / "golden-composite-practical.typ"


def test_composite_golden():
    import os
    from scripts.infographic import emit
    fig = comp_arch.layout(_fence([dict(CARDS3, slot="primary"),
                                   dict(FLOW2, slot="supporting")]), TOKENS)
    typ = emit.render_typ(fig)
    if not GOLDEN.exists():
        if not os.environ.get("IG_REGEN_GOLDEN"):
            pytest.fail("골든 부재 — IG_REGEN_GOLDEN=1로 재생성")
        GOLDEN.write_text(typ, encoding="utf-8")
        pytest.fail("골든 재생성 — 눈검(모듈 헤더 2개·24pt 간격·노트 2개) 후 커밋")
    assert GOLDEN.read_text(encoding="utf-8") == typ
```

Run: `IG_REGEN_GOLDEN=1 python3 -m pytest ...composite.py -q` → 골든 재생성 fail → **눈검**(`typst compile` 스크린 또는 emit 출력 육안 — 카드+플로우 스택·간격·헤더) → 재실행 PASS. 전체: **247 passed**. 커밋:

```bash
git add -A skills/korean-ebook-typst/scripts/infographic skills/korean-ebook-typst/tests/test_infographic_layout_composite.py docs/superpowers/specs/2026-08-21-infographic-layer-design.md
git commit -m "feat: composite archetype — 모듈 측정·배분 검증·세로 스택 + 스펙 개정 6판"
```

---

### Task 2: infographic_pages 리포트 + 검수 렌더 PNG

**Files:**
- Modify: `skills/korean-ebook-typst/scripts/infographic/render.py`(metadata 프리픽스 + manifest.json)
- Modify: `skills/korean-ebook-typst/scripts/qc_gate.py`(query 수집·gate-report `infographic_pages`·PNG 170 DPI)
- Test: `skills/korean-ebook-typst/tests/test_infographic_pages_report.py`(신규)

**Interfaces:**
- Consumes: `render_book_fences(book_dir, build, cfg) -> dict[int, dict[int, str]]`(render.py:31), `typst_binary()`(build.py), gate-report.json 라이터(qc_gate.py:224), PyMuPDF(qc_gate 기존)
- Produces: `build/infographic/manifest.json`(이름·챕터·펜스 인덱스 배열); `gate-report.json` 필드 `"infographic_pages": {"count": N, "expected": M, "match": bool, "figs": [{"name","chapter","index","page"}]}`; `build/infographic/review-pNNN.png`(도식 페이지 170 DPI). Task 4 통합이 소비.

**설계 판정:** 페이지 대응 = 각 도식 typ 첫 줄 `#metadata((kind: "ig-fig", name: "<name>", page: here().page()))` — `here()` 값 평가로 페이지 번호가 value 안에 직렬화된다. 수집은 `typst query <main.typ> metadata --field value --root <build>` — **stdout은 JSON 배열 하나**(줄 단위 아님 → `json.loads(r.stdout or "[]")`). PNG는 도식이 실린 **unique 페이지**별 1장(`typst compile main.typ review-pNNN.png --pages N --ppi 170 --root build`).

**호출 계약:** 테스트의 `assemble`·`compile_pdf`·`qc_gate.run` 호출 시그니처·인자는 기존 `tests/test_infographic_build_integration.py`가 이미 쓰는 호출을 **그대로 복제**한다(아래 코드의 `b.assemble(cfg, book)` 등은 의사 코드 — 실제 인자 순서·cfg 키·리턴값은 해당 파일에서 확인해 대체).

- [ ] **Step 1: 실패 테스트 작성**

```python
"""infographic_pages 리포트(스펙 §5.4 개정 6판) — metadata 페이지 매핑·일치 검사·PNG 렌더."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))

from scripts.infographic import emit, render as ig_render

TYPST = None  # typst_binary 재사용
from scripts.build import typst_binary  # noqa: E402
TYPST = typst_binary()

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
    cfg = {"title": "검증책", "subtitle": "부제", "author": "저자", "style": "practical",
           "cover": "auto", "chapters": ["ch01.md"]}
    main_typ = b.assemble(cfg, book)
    build = book / "build"
    manifest = json.loads((build / "infographic" / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["count"] == 1
    fig = manifest["figs"][0]
    assert fig["name"] == "000-fig01.typ" and fig["index"] == 1
    body = (build / "infographic" / fig["name"]).read_text(encoding="utf-8")
    assert body.splitlines()[0] == ('#metadata((kind: "ig-fig", name: "000-fig01.typ", '
                                    'page: here().page()))')


def test_query_reports_page_and_gate_field(tmp_path):
    import scripts.build as b
    from scripts import qc_gate
    book = _book(tmp_path)
    cfg = {"title": "검증책", "subtitle": "부제", "author": "저자", "style": "practical",
           "cover": "auto", "chapters": ["ch01.md"]}
    main_typ = b.assemble(cfg, book)
    b.compile_pdf(main_typ, "검증책")
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
```

- [ ] **Step 2: RED 확인**

Run: `python3 -m pytest skills/korean-ebook-typst/tests/test_infographic_pages_report.py -q`
Expected: FAIL — manifest.json 부재(KeyError/FileNotFoundError).

- [ ] **Step 3: 구현**

`render.py` `render_book_fences` emit 루프 — typ 작성 시 프리픽스 + 루프 끝에서 manifest:

```python
        for f in fences:
            fig = figs[f.index]
            name = f"{idx:03d}-fig{f.index:02d}.typ"
            (out_dir / name).write_text(
                f'#metadata((kind: "ig-fig", name: "{name}", page: here().page()))\n'
                + emit.render_typ(fig), encoding="utf-8")
            ...
        # (메서드 말미, result 반환 직전)
    manifest = {"count": sum(len(e) for e in result.values()),
                "figs": [{"name": nm, "chapter": idx, "index": fi}
                         for idx, emits in result.items() for fi, nm in emits.items()]}
    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    return result
```

`qc_gate.py` `run()` — report 라이터 앞에 삽입(빌드 main.typ·manifest 존재 시):

```python
    igp = _infographic_pages(book)
    report = {..., "infographic_pages": igp, ...}


def _infographic_pages(book: Path) -> dict:
    """§5.4 개정 6판 — typst query metadata로 도식-페이지 대응·일치 검사·검수 PNG."""
    build = book / "build"
    main = build / "main.typ"
    mf = build / "infographic" / "manifest.json"
    if not (main.exists() and mf.exists()):
        return {"count": 0, "expected": 0, "match": True, "figs": []}
    manifest = json.loads(mf.read_text(encoding="utf-8"))
    r = subprocess.run([typst_binary(), "query", str(main), "metadata",
                        "--field", "value", "--root", str(build)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return {"count": 0, "expected": manifest["count"], "match": False, "figs": []}
    queried = json.loads(r.stdout or "[]")   # stdout = JSON 배열 하나
    figs = [{"name": f["name"], "chapter": f["chapter"], "index": f["index"],
             "page": q["page"]}
            for q in queried if q.get("kind") == "ig-fig"
            for f in manifest["figs"] if f["name"] == q.get("name")]
    out = {"count": len(figs), "expected": manifest["count"],
           "match": len(figs) == manifest["count"], "figs": figs}
    for pno in sorted({f["page"] for f in figs}):
        png = build / "infographic" / f"review-p{pno:03d}.png"
        subprocess.run([typst_binary(), "compile", str(main), str(png),
                        "--pages", str(pno), "--ppi", "170", "--root", str(build)],
                       capture_output=True, text=True, check=False)
    return out
```

주: qc_gate의 typst 바이너리 경로는 `build.py:typst_binary()`를 임포트해 재사용(중복 정의 금지 — `from .build import typst_binary` 또는 기존 qc_gate 임포트 관례 따름). `match=False`는 에러가 아니라 WARN 채널 — `run()` 출력문에 `도식 {count}/{expected}` 한 줄 추가. PNG 렌더 실패는 무시(check=False) — 검수 렌더는 best-effort, 검수자 안내물. `match=False` 시 `pass`에는 영향 없음(WARN) — 다만 `count==0 and expected>0`은 build 붕괴 신호이므로 콘솔에 경고 문구 출력.

- [ ] **Step 4: GREEN 확인**

Run: `python3 -m pytest skills/korean-ebook-typst/tests/test_infographic_pages_report.py -q` → PASS(2). 전체: **249 passed**(기존 골든 바이트 불변 — metadata 프리픽스는 standalone 골든 emit 대상 아님: 골든 테스트는 `emit.render_typ` 출력을 비교하고 프리픽스는 render.py가 파일에만 붙인다).

- [ ] **Step 5: 커밋**

```bash
git add skills/korean-ebook-typst/scripts/infographic/render.py skills/korean-ebook-typst/scripts/qc_gate.py skills/korean-ebook-typst/tests/test_infographic_pages_report.py
git commit -m "feat: infographic_pages 리포트 — metadata 페이지 매핑·gate-report 필드·검수 PNG 170DPI"
```

---

### Task 3: 가이드 완성 + 이관 LOW 해소

**Files:**
- Modify: `skills/korean-ebook-typst/references/infographic/authoring.md`(composite 섹션·검수 절차 확장)
- Modify: `skills/korean-ebook-typst/SKILL.md`(레이아웃 목록 composite)
- Modify: `skills/korean-ebook-typst/scripts/infographic/render.py`(별칭 경고 finding)
- Test: `skills/korean-ebook-typst/tests/test_infographic_layout_layers.py`(rings 골든 추가)

**Interfaces:**
- Consumes: Task 1 composite 계약(GAP·PRIMARY_FRAC·에러 스키마), Task 2 `infographic_pages`·`review-p*.png` 검수 흐름
- Produces: authoring.md 전체판(§8.5 완성), 별칭 경로 non-fatal finding `kind="schema"` 문구 `"별칭 {raw}→{norm} — 정식 키워드 권장"`, rings 바이트 골든 `golden-layers-rings-practical.typ`

- [ ] **Step 1: 별칭 경고 테스트(RED)** — `test_infographic_pages_report.py`에 추가(`_book`·assemble 호출 계약 재사용):

```python
def test_alias_warning_printed(tmp_path, capsys):
    import scripts.build as b
    book = _book(tmp_path)
    (book / "ch01.md").write_text(
        BOOK.replace('"layout": "flow"', '"layout": "process"'), encoding="utf-8")
    cfg = {"title": "검증책", "subtitle": "부제", "author": "저자", "style": "practical",
           "cover": "auto", "chapters": ["ch01.md"]}
    b.assemble(cfg, book)   # 기존 통합 테스트 호출 계약 — process 별칭이 flow로 정규화돼 빌드 성공
    out = capsys.readouterr().out
    assert "별칭 process→flow — 정식 키워드 권장" in out
    assert "000-ch01.md #1" in out
```

구현 계약: **render.py parse 루프**(fences.append 직후)가 `f.data.get("_alias")` 있을 때 `print(f"[경고] 별칭 {f.data['_alias']}→{f.layout} — 정식 키워드 권장 ({chapter_name} #{f.index})")` — non-fatal, 빌드 계속. lint.LintFinding 스키마 위반과 달리 별칭은 정상 빌드 경로라 finding(invisible)이 아닌 **콘솔 경고**(검수자·작자가 빌드 로그에서 바로 본다).

- [ ] **Step 2: rings 골든 추가** — `test_infographic_layout_layers.py` 골든 테스트 옆에 always-write 재생성 골든 1종:

```python
GOLDEN_RINGS = Path(__file__).parent / "fixtures" / "infographic" / "golden-layers-rings-practical.typ"

RINGS_FENCE = {"layout": "layers", "variant": "rings", "title": "계층은 표현에서 자료로 내려간다",
               "rings": [{"label": "표현"}, {"label": "문서"}, {"label": "자료"}, {"label": "부호"}]}
# rings 항목 스키마(_sheet_rows `rings[i].label` 준수)·variant 키·그 외 필수 필드(thesis 등)는
# test_infographic_layout_layers.py 기존 골든/테스트가 쓰는 확정 형태를 그대로 복제해 조정한다.


def test_layers_rings_golden():
    fig = _layout(json.loads(json.dumps(RINGS_FENCE, ensure_ascii=False)))
    typ = emit.render_typ(fig)
    if not GOLDEN_RINGS.exists():
        if not os.environ.get("IG_REGEN_GOLDEN"):
            pytest.fail("골든 부재 — IG_REGEN_GOLDEN=1로 재생성")
        GOLDEN_RINGS.write_text(typ, encoding="utf-8")
        pytest.fail("골든 재생성 — 눈검 후 커밋")
    assert GOLDEN_RINGS.read_text(encoding="utf-8") == typ
```

Run: `IG_REGEN_GOLDEN=1 python3 -m pytest ...layers.py -q` → 재생성 fail → 눈검(동심원·라벨 현 내 배치) → 재실행 PASS.

- [ ] **Step 3: authoring.md 완성**

(a) `### layers — 계층 구조` 뒤에 `### composite — 복합 씬` 섹션: 펜스 예시(주 cards + 보조 flow)·slot 규칙(주 1·보조 1~2·재귀 금지)·배분 규칙(주 60% 상한·측정 우선·슬롯 간 24pt)·**분할 에러 스키마**(개정 6판 — 자동 축소 없음)·"모듈은 각자 결론형 제목을 가진다".
(b) `## 검수` 섹션 확장: `gate-report.json` `infographic_pages`(count/expected/match) 읽는 법·`build/infographic/review-p*.png`(170 DPI) 눈검 항목(카드 줄바꿈·셀 잘림·화살표 충돌·작은 글씨·카드 밖 이탈 — 스펙 §5.4 목록)·확인란 절차 기존 연결.
(c) `## 언제 도식을 넣나` 라우팅 표에 composite 행 추가("한 장에서 대비·절차를 함께 — 주+보조").
(d) `## 예산 치트시트`에 composite 배분 행(주 ≤60%·보조 잔여·GAP 24pt·높이 상한 85%).

- [ ] **Step 4: SKILL.md** 레이아웃 목록에 composite 추가(기존 9종 나열 형식 준수).

- [ ] **Step 5: 확인 + 커밋**

Run: `python3 -m pytest skills/korean-ebook-typst/tests/ -q` → **251 passed**(249 + 별칭 1 + rings 골든 1).

```bash
git add -A skills/korean-ebook-typst/references/infographic/authoring.md skills/korean-ebook-typst/SKILL.md skills/korean-ebook-typst/scripts/infographic/render.py skills/korean-ebook-typst/tests
git commit -m "docs: 가이드 전체판 완성 — composite·검수 렌더 절차 + 별칭 경고·rings 골든(이관 LOW 해소)"
```

---

### Task 4: 통합 마무리 — 9종+composite fixture 책

**Files:**
- Modify: `skills/korean-ebook-typst/tests/test_infographic_build_integration.py`(composite 펜스 + infographic_pages 단언)
- Test fixture: 기존 통합 fixture 책(Phase 3+4)에 composite 챕터/펜스 추가

**Interfaces:**
- Consumes: Task 1·2 전부, 기존 통합 테스트 구조(subprocess 빌드·검수 시트·I1 단언)
- Produces: 스펙 §7 통합 완료 상태 — "9종+복합 펜스 fixture 책 → build → PDF·infographic_pages 일치 확인"

- [ ] **Step 1: 통합 테스트 확장(RED)** — 기존 통합 fixture 책 md에 composite 펜스 추가(주 `cards` 3 + 보조 `flow` 2, 결론형 무숫자 제목 `"구성과 절차를 한 장에 담는다"`). 단언 추가:

```python
    # composite 도식 1종 + infographic_pages 일치(§7·§5.4)
    manifest = json.loads((build / "infographic" / "manifest.json").read_text(encoding="utf-8"))
    assert any(f["name"].endswith(f"-fig{N:02d}.typ") for f in manifest["figs"])  # N=composite 펜스 번호
    report = json.loads((book / "gate-report.json").read_text(encoding="utf-8"))
    assert report["infographic_pages"]["match"] is True
    assert report["infographic_pages"]["count"] == manifest["count"] == EXPECTED_FIGS  # 기존 도식 수+1
    # 검수 시트가 composite 모듈 필드를 전개
    sheet = next((build / "infographic").glob("*-figNN.review.md")).read_text(encoding="utf-8")  # composite 것
    assert "modules[0].cards[0].title" in sheet and "modules[1].steps[0].title" in sheet
```

- [ ] **Step 2: RED 확인 → 구현(없음 — Task 1~3가 이미 구현; 실패 시 Task 1~3 결함이므로 본태 수정) → GREEN**

Run: `python3 -m pytest skills/korean-ebook-typst/tests/test_infographic_build_integration.py -q` → PASS. 전체: **252 passed** 목표(통합 신규 1).

- [ ] **Step 3: 커밋 + 종료 조건 확인**

```bash
git add skills/korean-ebook-typst/tests
git commit -m "test: 통합 마무리 — composite 포함 fixture 책·infographic_pages 일치"
```

종료 조건: 전체 스위트 green·기존 골든 전종 바이트 불변 + 신규 composite·rings 골든 존재+PASS·`gate-report.json` `infographic_pages.match=true`·authoring.md composite+검수 절차 섹션 존재·SKILL.md 10 layout(9+composite).

---

## Self-Review (기록)

- 스펙 커버리지: §3.5(Task 1)·§5.4 검수 렌더·리포트(Task 2)·§8.5 가이드·SKILL(Task 3)·§7 통합(Task 4)·§3.4 별칭 경고(Task 3) — 전부 태스크 있음. §3.5 "보조 축소"는 개정 6판으로 명시적 제거(Step 0).
- 플레이스홀더 스캔: `HEAD_H` 상수 제거(유무 높이차 테스트로 대체). assemble/qc_gate 호출은 "기존 통합 테스트 복제" 계약 + 의사 코드 명시(시그니처 드리프트 흡수). RINGS_FENCE·LADDER4 등 펜스 페이로드는 `_sheet_rows` 확정 경로 기반 구체값 + "기존 테스트 형태 복제" 지시.
- 타입 정합성: `Fence` 8필드 생성자·`dispatch` 시그니처·`LintFinding(kind, loc, measured, levers)`·2-튜플 rows·`typst query` stdout=JSON 배열 — 전부 실측·수정 반영.
- 테스트 수 산술: 239 → T1 +8(단위 6+시트 1+골든 1)=247 → T2 +2=249 → T3 +2=251 → T4 +1=252.
