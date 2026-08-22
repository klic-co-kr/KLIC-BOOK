# 인포그래픽 레이어 Phase 4 (topology + approval + layers + emit max_w 파이프라인) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Phase 3에 이어 topology·approval·layers(rings 변형) archetype 3종을 추가하고, Phase 3 최종 리뷰가 이관한 emit max_w 미강제 결함(TextOp 상자 폭이 typst에 도달 안 함)을 골든 전량 재생성 웨이브로 수복한다.

**Architecture:** Phase 1~3과 동일 — parse(스키마)→layout(archetype별 순수 함수)→lint(I1)→emit(ops→typst). 신규 archetype은 `archetypes/` 모듈 + `layout.dispatch` 등록 + `parse` 검증 분기 + lint 필드·render 검수 시트 행. model.py ops 확장(RectOp.rot 회전·CircleOp 신규 — 스펙 §6.3 rings 동심원·게이트 다이아몬드 표현).

**Tech Stack:** Python 3.12 표준 라이브러리, typst 0.15.1, pytest. 신규 의존 0.

**Spec:** `docs/superpowers/specs/2026-08-21-infographic-layer-design.md` (개정 5판 — 본 플랜과 함께 §6.2 ladder 단계 행 추가·개정 이력 기입)

**Phase 1~3 자산 (main 병합 완료, korean-ebook-typst 스위트 207 green):** `scripts/infographic/` 전 모듈(flow·cards·matrix·before_after·ladder·roadmap + base.LayoutError), `templates/infographic/helper.typ`, authoring.md(Phase 3판), 골든 6종(practical). 테스트 관례: `tests/conftest.py`가 스킬 루트 sys.path 추가, `from scripts.infographic.x import y`.

**Phase 3 최종 리뷰 이관 과제 (본 플랜이 흡수):** ① emit max_w 미강제(Important #1 — essay note 2행째 완전 클리핑 실증) ② note 1줄 가정 전 archetype 공통 ③ PACK_STAGES 팩 상한 스펙 §6.2 정식화 ④ `_ink_ok` Rect 분기 stroke_w/2 누락(잠재) ⑤ `_sizes` 중복 base 팩토리 통일.

## Global Constraints (Phase 1~3와 동일 + 추가)

- 외부 의존 금지, 펜스 JSON, 결정론(같은 입력=같은 방출 바이트), hex 금지(역할명), leading 1.3em, G3 불변식(본문±0.3pt 밖 — essay 예외 +1.5), I1 메시지 계약(loc/측정값/저자 레버), typst_binary() 재use, timeout=120.
- 모든 archetype 에러는 `archetypes/base.py`의 `LayoutError` 상속(`XLayoutError(LayoutError)`) — render.py·cli.py는 베이스만 catch.
- lint 필드·검수 시트는 `f.data.get(...)` 접근(KeyError 금지).
- 잉크 bbox 프레임 내 보장(`_ink_ok`), 높이 85% 한계, TextOp.field 계약(예: `nodes[2].label`, `path[1].title`, `stack[3].label`).
- **높이·폭 예산은 전부 `budget.line_count(text, box_w, size_pt, pad, pack)` 실측** — 1줄 가정 금지. 유일 예외: `kicker`·패널/스텝 라벨류는 저작 계약상 초단문(1줄) — authoring.md 규칙으로 통제(코드 주석에 계약 명시).
- 판형 상한은 layout이 즉시 에러(스펙 §6.2). 상한 검사는 parse 하한·상한(절대)과 별개 경로 — 양쪽 모두 도달 가능 테스트 유지.
- 판형 상한(§6.2 표): topology 노드 essay 5 / practical 6 / b5 7 / business 8 / lecture 8. **ladder 단계(개정 5판 신규 행) essay 4 / practical·b5·business·lecture 5.** approval·layers는 판형 표에 없음 — 폭 하상수(MIN_STEP_W 등) 도달 에러로 갈음.
- 절대 상한(§3.2): topology 노드 3~8, approval 경로 3~8·게이트 ≤4, layers(stack 또는 rings) 2~6.
- 별칭 확장: `network` → `topology`(스펙 §3.4). approval·layers 별칭 없음.
- 텍스트 크기: 스텝/노드 제목=본문+1, 항목/본문=본문−1, 제목=H2(essay +1.5), 라벨=label 크기 — Phase 2·3 cards 관례. 공용 산출은 `base.sizes(tokens)` 팩토리(본 플랜 Task 1 도입).
- **archetype별 골든 스냅샷 필수** — 3종 각 1개 practical, `IG_REGEN_GOLDEN=1` 절차. Task 1은 기존 골든 6종 전량 재생성 웨이브(emit max-w 인자 추가로 바이트 변경 — 내용 불변).
- **골든 교정 3주기**(Task 4): 신규 3종 calib fixture × 5팩 실렌더 → 예산표 갱신 — Phase 2·3 절차 반복. 계수 갱신 시에만 m7 재확증(골든 재생성) 발동.
- **병합 게이트**: Task 4(authoring.md 갱신) 완료 전 main 병합 금지.
- 커넥터 상수: 커넥터 복도 G는 샤프트 가시 ≥12pt 계약(tip-gap 8 양측 → G ≥ 28). topology·approval G=28.0. ARROW_STROKE_W 1.2·헤드비 3.33(model.py 상수 재use). dashed = 비동기/참조 간선(§6.1 — topology `dashed:true`).
- archetype 내부 pad 전부 8.0 고정(lint 재검사 pad=8와 일치).
- **`_ink_ok` 표준(개정)**: Rect 분기에 `stroke_w/2` 포함(스펙 §5.2-3 문언 회복) — Task 1이 5개 모듈(flow·matrix·before_after·ladder·roadmap; cards는 기존 포함)에 적용, Task 2·3 신규 모듈은 표준형으로 작성.
- 루트 `pytest` 금지(books/ import-time SystemExit) — 항상 `python3 -m pytest skills/korean-ebook-typst/tests/ -q`.

---

### Task 1: emit max_w 파이프라인 + note 다중 줄 예산화 + 프리미티브 통일 + 골든 6종 재생성

**Files:**
- Modify: `skills/korean-ebook-typst/scripts/infographic/emit.py:36-40` (TextOp max-w 방출)
- Modify: `skills/korean-ebook-typst/templates/infographic/helper.typ:32-37` (ig-text 폭 강제)
- Modify: `skills/korean-ebook-typst/scripts/infographic/archetypes/base.py` (sizes 팩토리 추가)
- Modify: `skills/korean-ebook-typst/scripts/infographic/archetypes/flow.py`·`cards.py`·`matrix.py`·`before_after.py`·`ladder.py`·`roadmap.py` (note 다중 줄·_ink_ok stroke_w/2·sizes 팩토리 전환)
- Test: `skills/korean-ebook-typst/tests/test_infographic_emit_max_w.py` (신규), 기존 archetype 테스트 2파일에 note 다중 줄 테스트 추가
- Regenerate: `tests/fixtures/infographic/golden-{flow,cards,matrix,before-after,ladder,roadmap}-practical.typ` 6종

**Interfaces:**
- Consumes: `model.TextOp.max_w`(0.0=검사 생략 센티넬 — 방출도 생략), `budget.line_count`, `parse.DEFAULT_NOTE`
- Produces: emit 결과의 모든 TextOp( max_w>0 ) 행에 `, max-w: {폭}pt` 인자; helper `ig-text(..., max-w: 0pt)`; `base.sizes(tokens) -> dict[str, float]` 키 `body`/`kicker`/`title`/`ph_title`/`item`; 전 archetype note 높이 = `line_count(note, W-2P, item_size, 8.0, pack)`줄

**결함 근거(Phase 3 최종 리뷰 실측):** emit.py가 TextOp.max_w를 방출하지 않고 helper ig-text가 폭 없는 box를 쓴다 → typst는 그림 전체 폭 W에서만 줄바꿈. (a) essay DEFAULT_NOTE 2행째가 paper rect 밖에서 완전 클리핑(픽셀 샘플링 실증) (b) practical 밴드 항목 87.9pt > 밴드 83.5pt 수평 삐져나옴. note 높이 예산도 전 archetype이 1줄 고정(`item_size*LEADING`)이라 2줄 모델과 배치가 어긋난다.

- [ ] **Step 1: 실패 테스트 작성**

```python
# tests/test_infographic_emit_max_w.py — emit max_w 방출·note 다중 줄 예산.
"""test_infographic_emit_max_w.py — 스펙 §5.1 emit max_w 방출 + note 다중 줄 예산화."""
import pytest

from scripts.infographic.archetypes import flow, roadmap
from scripts.infographic.emit import render_typ
from scripts.infographic.parse import DEFAULT_NOTE

from .test_infographic_layout import TOKENS  # conftest 경로 관례에 따라 기존 테스트 파일의
# TOKENS practical 딕트 임포트(없으면 해당 파일에서 복제해 온 것을 쓴다 — 관례 준수)


def _flow_fence():
    from scripts.infographic.parse import parse_fence
    return parse_fence(0, """{"layout":"flow","title":"흐름 검증 제목",
      "steps":[{"title":"준비","text":"준비 문장"},{"title":"실행","text":"실행 문장"}]}""")
```
```

```python
def test_emit_max_w_unit_synthetic():
    # 합성 FigModel — TextOp 2개(폭 0·폭 100)로 방출 문자열 직접 단언(펜스 의존 없음).
    from scripts.infographic.model import FigModel, RectOp, TextOp
    fig = FigModel(width=300.0, height=100.0, source_index=0, ops=(
        TextOp(x=150.0, y=20.0, size=9.0, text="폭 없음", max_w=0.0),
        TextOp(x=150.0, y=50.0, size=9.0, text="폭 있음", max_w=100.0),
    ))
    lines = [l for l in render_typ(fig).splitlines() if "ig-text(" in l]
    assert len(lines) == 2
    assert "max-w" not in lines[0] and "폭 없음" in lines[0]
    assert "max-w: 100.00pt" in lines[1]
```

노트: `TOKENS`·`_essay_tokens`·`_tokens(pack)`·`_fence(...)` 조달은 기존 `test_infographic_layout_*.py`의 관례(tokens.json 직독 헬퍼·펜스 생성자)를 그대로 재사용한다. essay DEFAULT_NOTE 2줄 회귀(클리핑 결함의 핵심 사례)는 `test_infographic_layout_flow.py`에 추가:

```python
def test_note_measured_two_lines_essay(_tokens):  # _tokens("essay") 관례 헬퍼
    essay = _tokens("essay")
    item = essay["fonts"]["body"]["size_pt"] - 1
    w = essay["body_frame_pt"]["x1"] - essay["body_frame_pt"]["x0"] - 28.0
    nl = budget.line_count(parse_mod.DEFAULT_NOTE, w, item, 8.0, "essay")
    assert nl == 2  # 전제 — Phase 3 최종 리뷰 실측(essay 본문폭에서 기본 노트 2줄)
    h_short = flow_arch.layout(_fence(note="한 줄 노트"), essay).height
    h_default = flow_arch.layout(_fence(note=None), essay).height
    assert abs((h_default - h_short) - (nl - 1) * item * 1.3) < 0.01
```

`test_infographic_layout_roadmap.py`에도 동일 구조 1건(전제 `nl` practical == 1, 델타 0 — 배관 회귀):

```python
def test_note_measured_pushes_fig_height():
    short = rm_arch.layout(_fence(note="한 줄 노트"), TOKENS)
    default = rm_arch.layout(_fence(note=None), TOKENS)
    nl = budget.line_count(parse_mod.DEFAULT_NOTE,
                           TOKENS["body_frame_pt"]["x1"] - TOKENS["body_frame_pt"]["x0"] - 28.0,
                           TOKENS["fonts"]["body"]["size_pt"] - 1, 8.0, "practical")
    assert nl == 1
    assert abs((default.height - short.height) - (nl - 1) * (TOKENS["fonts"]["body"]["size_pt"] - 1) * 1.3) < 0.01
```

- [ ] **Step 2: RED 확인**

Run: `python3 -m pytest skills/korean-ebook-typst/tests/test_infographic_emit_max_w.py -q`
Expected: FAIL — `max-w` 방출 없음(assert "max-w: " in out 실패), note 높이 1줄 고정.

- [ ] **Step 3: emit.py — TextOp max-w 방출**

```python
        elif isinstance(op, TextOp):
            w = f", weight: \"{op.weight}\"" if op.weight != "regular" else ""
            mw = f", max-w: {_n(op.max_w)}pt" if op.max_w > 0 else ""
            # ig-text는 컨테이너 중심 앵커라 절대좌표 환산에 fw·fh가 필요하다(helper 참조).
            lines.append(f"  #ig-text({_n(op.x)}, {_n(op.y)}, {_n(fig.width)}, "
                         f"{_n(fig.height)}, {_n(op.size)}, \"{op.role}\"{w}{mw})[{_esc(op.text)}]")
```

- [ ] **Step 4: helper.typ — ig-text 폭 강제(중앙 정렬 유지)**

```typst
// text — x,y는 텍스트 블록 중심의 절대좌표, fw·fh는 도식 전체 폭·높이.
// max-w>0이면 상자 폭을 강제해 상자 안에서 줄바꿈한다(Phase 4 — emit max_w 미강제 결함 수복).
// 줄은 상자 안에서 중앙 정렬 — 폭 없는 박스(내용 밀착) 시대의 시각과 동일하게.
#let ig-text(x, y, fw, fh, size, role, weight: "regular", max-w: 0pt, body) = place(
  center + horizon, dx: pt(x - fw / 2), dy: pt(y - fh / 2),
  box(inset: 0pt, width: if max-w > 0pt { pt(max-w) })[#set par(leading: 1.3em)
    #align(center)[#text(size: pt(size), fill: ig-color(role),
          weight: if weight == "bold" { "bold" } else { "regular" })[#body]]],
)
```

- [ ] **Step 5: base.py — sizes 팩토리 추가**

```python
def sizes(tokens: dict) -> dict:
    """공용 텍스트 크기 산출(스펙 §4.3·Phase 2 cards 관례) — archetype 공통 단일 진실."""
    f = tokens["fonts"]
    body = f["body"]["size_pt"]
    title = f["heading2"]["size_pt"]
    if abs(title - body) <= 0.3:
        title = body + 1.5
    return {"body": body, "kicker": f["label"]["size_pt"], "title": title,
            "ph_title": body + 1, "item": body - 1}
```

- [ ] **Step 6: 6개 archetype 모듈 — 기계적 전환 3종**

각 모듈(flow·cards·matrix·before_after·ladder·roadmap)에 동일 적용:

(a) 인라인 크기 산출 블록을 팩토리 치환(지역 변수명은 유지 — `s = sizes(tokens)` 후 언팩):

```python
from .base import LayoutError, sizes
# ... 기존 f["body"]["size_pt"] 등 5줄 산출을:
s = sizes(tokens)
kicker_size, title_size = s["kicker"], s["title"]
ph_title_size, item_size = s["ph_title"], s["item"]
```
(모듈이 쓰지 않는 키는 언팩 생략 — 예: roadmap은 전부 사용. cards/matrix의 기존 변수명이 다르면 그 이름으로 언팩. 만약 모듈 기존 산출값이 팩토리 값과 다르면(예: cards의 kicker 계산) **팩토리 값을 따른다** — 값 변화가 생기면 골든 눈검 단계에서 확인하고 보고서에 명기.)

(b) note 블록 다중 줄 예산화(전 모듈 동일 패턴 — 아래는 roadmap.py:108-112 개정):

```python
    y = y + band_h + 12.0
    note = fence.note or DEFAULT_NOTE
    nl = budget.line_count(note, W - 2 * P, item_size, 8.0, pack)
    texts.append(TextOp(x=W / 2, y=y + nl * item_size * LEADING / 2, size=item_size,
                        text=note, role="ink-mute", max_w=W - 2 * P, field="note"))
    y += nl * item_size * LEADING
```

(각 모듈의 note y 기준식이 미세하게 다르면(예: ladder note_h 상수) `nl` 곱만 같은 방식으로 치환 — 배치 y 중심 `+ nl*size*LEADING/2`, 진행 `+= nl*size*LEADING`. kicker는 1줄 계약 유지 — 해당 줄에 `# kicker: 저작 계약 초단문(1줄)` 주석 추가.)

(c) `_ink_ok` Rect 분기에 stroke_w/2 추가(5개 모듈 — cards.py는 이미 포함, 형태만 대조 확인):

```python
        if isinstance(o, RectOp):
            s = o.stroke_w / 2
            if (o.x - s < -0.001 or o.x + o.w + s > width + 0.001
                    or o.y - s < -0.001 or o.y + o.h + s > height + 0.001):
                raise <모듈>Error(
                    f"잉크 bbox 프레임 이탈: rect({o.x:.1f},{o.y:.1f},{o.w:.1f},{o.h:.1f})")
```

- [ ] **Step 7: 스위트 통과 확인(골든 재생성 전 — 골든 6종은 이 시점에서 FAIL 예상)**

Run: `python3 -m pytest skills/korean-ebook-typst/tests/ -q`
Expected: 골든 스냅샷 6종 FAIL(바이트 변경 — max-w 인자), 나머지 전부 PASS. 골든 외 FAIL이 있으면 수정.

- [ ] **Step 8: 골든 6종 재생성 웨이브**

```bash
IG_REGEN_GOLDEN=1 python3 -m pytest skills/korean-ebook-typst/tests/ -q
```
Expected: 6골든 write+FAIL(설계상). 이후 눈검: 기존 하네스 관례(`.scratch/` 임시 typst 컴파일 `--ppi 144` PNG)로 6종 전부 — ① practical 시각적 레이아웃 변화 없음(줄바꿈 변화 0 — practical 텍스트는 전부 예산 내 1줄) ② 텍스트 중앙 정렬 유지. 추가로 `cli.py preview --style essay`로 essay 1종 — DEFAULT_NOTE가 2줄로 **보이게** 렌더되는지(클리핑 소멸 확인 — 본 태스크의 목적).
재실행: `python3 -m pytest skills/korean-ebook-typst/tests/ -q` → 전부 PASS(바이트 안정).

- [ ] **Step 9: 커밋**

```bash
git add skills/korean-ebook-typst/scripts/infographic/emit.py \
        skills/korean-ebook-typst/templates/infographic/helper.typ \
        skills/korean-ebook-typst/scripts/infographic/archetypes/ \
        skills/korean-ebook-typst/tests/test_infographic_emit_max_w.py \
        skills/korean-ebook-typst/tests/test_infographic_layout_flow.py \
        skills/korean-ebook-typst/tests/test_infographic_layout_roadmap.py \
        skills/korean-ebook-typst/tests/fixtures/infographic/
git commit -m "fix: emit max_w 파이프라인 — ig-text 상자 폭 강제·note 다중 줄 예산·_ink_ok stroke_w/2·sizes 팩토리 + 골든 6종 재생성"
```

---

### Task 2: topology archetype + 골든

**Files:**
- Create: `skills/korean-ebook-typst/scripts/infographic/archetypes/topology.py`
- Modify: `skills/korean-ebook-typst/scripts/infographic/parse.py` (별칭 network·VALID_LAYOUTS·검증 분기)
- Modify: `skills/korean-ebook-typst/scripts/infographic/layout.py:20-21` (dispatch)
- Modify: `skills/korean-ebook-typst/scripts/infographic/lint.py` (nodes 필드)
- Modify: `skills/korean-ebook-typst/scripts/infographic/render.py` (`_sheet_rows` nodes 행)
- Test: `skills/korean-ebook-typst/tests/test_infographic_layout_topology.py` + 골든 fixture

**Interfaces:**
- Consumes: `base.LayoutError`·`base.sizes`, `budget.line_count`, `model.RectOp/TextOp/ArrowOp/FigModel`, `parse.Fence/DEFAULT_NOTE`
- Produces: `archetypes.topology.layout(fence, tokens) -> FigModel`, `TopologyLayoutError`, 펜스 데이터 `nodes[]`({id, label})·`edges[]`({from, to, dashed?}) — edges 생략/빈 배열 = grid 배치, 있으면 최장경로 DAG 층위

**데이터 설계(스펙 §3.2 `nodes[]`, `edges[]`):** 노드 label은 초단문. 간선 from→to는 노드 id 참조. `dashed:true` = 참조 간선(§6.1). 순환·자기 간선·중복 간선·미참조 id는 parse 거부.

**지오메트리(스펙 §6.3 "grid 배치 기본. 방향 간선 있으면 계층(DAG 층위) 자동 배치"):** 간선 없음 → 열수 `ceil(sqrt(n))` grid(행 우선 채움). 간선 있음 → Kahn 위상 정렬 + 최장경로 층위(layer[to] ≥ layer[from]+1 보장 — 역방향 화살표 불가). 열수 = 층위 수, 열内 노드는 등장 순서로 수직 스택. 노드 폭 `node_w = (W−2P−(cols−1)G)/cols`(G=28 — 샤프트 ≥12pt), 하상수 MIN_NODE_W 54.0(스펙 §6.2 상한 전팩 도달: essay 5노드 3열 55.15pt 실측). 노드 높이 = 전 노드 최대 실측(균일 그리드). 간선 화살표 = 소스 우변 중심 → 타깃 좌변 중심(tip-gap 8 양측, 대각 허용 — ladder C3 선례).

- [ ] **Step 1: parse 실패 테스트 작성**

```python
# tests/test_infographic_layout_topology.py — 스펙 §6.2·§6.3 topology 지오메트리·결정론.
"""test_infographic_layout_topology.py — 스펙 §6.2·§6.3 topology 지오메트리·결정론."""
import json

import pytest

from scripts.infographic.archetypes import topology as topo_arch
from scripts.infographic.archetypes.topology import TopologyLayoutError
from scripts.infographic.parse import ParseError, parse_fence


def _fence(n=6, edges=None, **extra):
    payload = {"layout": "topology", "title": "구성 요소 관계 제목",
               "nodes": [{"id": f"n{i}", "label": f"노드 {i}"} for i in range(n)]}
    if edges is not None:
        payload["edges"] = [{"from": f"n{a}", "to": f"n{b}"} for a, b in edges]
    payload.update(extra)
    return parse_fence(0, json.dumps(payload, ensure_ascii=False))


def test_parse_bounds():
    with pytest.raises(ParseError):
        parse_fence(0, '{"layout":"topology","title":"t","nodes":[]}')                # 하한 3 미만
    with pytest.raises(ParseError):
        _fence(n=9)                                                                    # 절대 상한 8 초과
    with pytest.raises(ParseError):
        _fence(n=3, edges=[(0, 0)])                                                    # 자기 간선
    with pytest.raises(ParseError):
        _fence(n=3, edges=[(0, 3)])                                                    # 미참조 id
    with pytest.raises(ParseError):
        parse_fence(0, '{"layout":"topology","title":"t","nodes":['
                       '{"id":"n0","label":"중복"},{"id":"n0","label":"중복"},'
                       '{"id":"n1","label":"노드"}]}')                                 # id 중복
    with pytest.raises(ParseError):
        parse_fence(0, '{"layout":"topology","title":"t",'
                       '"nodes":[{"id":"a","label":"원"},{"id":"b","label":"변환"},'
                       '{"id":"c","label":"결과"}],'
                       '"edges":[{"from":"a","to":"b"},{"from":"a","to":"b"}]}')       # 간선 중복
    assert parse_fence(0, '{"layout":"network","title":"t","nodes":['  # 별칭 network
        '{"id":"a","label":"클라"},{"id":"b","label":"게이트"},{"id":"c","label":"저장"}]}').layout == "topology"
```

- [ ] **Step 2: RED 확인** — `python3 -m pytest skills/korean-ebook-typst/tests/test_infographic_layout_topology.py -q` → FAIL(ImportError)

- [ ] **Step 3: parse.py 확장**

상수부에 추가: `NODE_MIN, NODE_MAX = 3, 8`, ALIASES에 `"network": "topology"`, VALID_LAYOUTS에 `"topology"`. 검증 분기(roadmap 뒤) — 기존 분기 스타일 동일:

```python
    elif f.layout == "topology":
        nodes = data.get("nodes")
        if not isinstance(nodes, list) or not (NODE_MIN <= len(nodes) <= NODE_MAX):
            raise ParseError("노드 수는 3~8개 필요")
        seen = set()
        for nd in nodes:
            if (not isinstance(nd, dict) or not isinstance(nd.get("id"), str)
                    or not isinstance(nd.get("label"), str) or not nd["id"] or not nd["label"]):
                raise ParseError("노드는 id·label 비빈 문자열 필요")
            if nd["id"] in seen:
                raise ParseError(f"노드 id 중복: {nd['id']}")
            seen.add(nd["id"])
        edges = data.get("edges", [])
        if not isinstance(edges, list):
            raise ParseError("edges는 배열 필요")
        eset = set()
        for e in edges:
            if (not isinstance(e, dict) or e.get("from") not in seen or e.get("to") not in seen):
                raise ParseError(f"간선 from·to는 노드 id 참조 필요: {e}")
            if e["from"] == e["to"]:
                raise ParseError(f"자기 간선 금지: {e['from']}")
            if (e["from"], e["to"]) in eset:
                raise ParseError(f"간선 중복: {e['from']}→{e['to']}")
            eset.add((e["from"], e["to"]))
            if "dashed" in e and not isinstance(e["dashed"], bool):
                raise ParseError("dashed는 불리언")
```

- [ ] **Step 4: topology.py 구현**

```python
"""topology — 노드 grid/계층 배치 + 간선 화살표(스펙 §6.2·§6.3). 판형 상한 노드 수로 즉시 에러."""
from __future__ import annotations

import math

from .. import budget
from ..model import ArrowOp, FigModel, RectOp, TextOp
from ..parse import DEFAULT_NOTE, Fence
from .base import LayoutError, sizes

P = 14.0
G = 28.0                     # 커넥터 복도 — tip-gap 8 양측 후 샤프트 12pt(§6.1)
G_V = 24.0                   # 같은 열 노드 수직 간격
NODE_PAD_IN = 8.0
NODE_PAD_V = 8.0
MIN_NODE_W = 54.0            # §6.2 상한 전팩 도달 — essay 5노드 3열 55.15pt 실측
LEADING = 1.3
HEIGHT_LIMIT = 0.85

PACK_NODES = {"essay": 5, "practical": 6, "b5": 7, "business": 8, "lecture": 8}


class TopologyLayoutError(LayoutError):
    pass


def layout(fence: Fence, tokens: dict) -> FigModel:
    frame = tokens["body_frame_pt"]
    W = frame["x1"] - frame["x0"]
    H_frame = frame["y1"] - frame["y0"]
    pack = tokens.get("style", "practical")
    s = sizes(tokens)
    kicker_size, title_size, item_size = s["kicker"], s["title"], s["item"]

    nodes = fence.data["nodes"]
    edges = fence.data.get("edges", [])
    n = len(nodes)
    cap = PACK_NODES.get(pack)
    if cap is None:
        raise TopologyLayoutError(f"알 수 없는 스타일 팩 {pack!r}")
    if n > cap:
        raise TopologyLayoutError(
            f"노드 {n}개 > 판형 상한 {cap}개({pack}) — 노드 통합 또는 펜스 분할")

    # 배치 열·행 — 간선 없으면 grid, 있으면 최장경로 DAG 층위
    if edges:
        layer = _longest_path_layers(nodes, edges)
        pos = {}
        per_col: dict[int, int] = {}
        for nd in nodes:
            c = layer[nd["id"]]
            pos[nd["id"]] = (c, per_col.get(c, 0))
            per_col[c] = per_col.get(c, 0) + 1
    else:
        cols = math.ceil(math.sqrt(n))
        pos = {nd["id"]: (i % cols, i // cols) for i, nd in enumerate(nodes)}
    ncols = max(c for c, _ in pos.values()) + 1

    node_w = (W - 2 * P - (ncols - 1) * G) / ncols
    if node_w < MIN_NODE_W:
        raise TopologyLayoutError(
            f"노드 폭 {node_w:.1f}pt < {MIN_NODE_W:.0f}pt({pack}) — 노드 통합 또는 펜스 분할")

    # 노드 높이 — 전 노드 최대 실측(균일 그리드)
    lines = max(budget.line_count(nd["label"], node_w - 2 * NODE_PAD_IN, item_size,
                                 NODE_PAD_IN, pack) for nd in nodes)
    node_h = 2 * NODE_PAD_V + lines * item_size * LEADING

    # 헤더(공통 구조) — kicker/title/thesis 후 y 시작(kicker는 저작 계약 초단문 1줄)
    texts: list[TextOp] = []
    cy = 0.0
    if fence.kicker:
        texts.append(TextOp(x=W / 2, y=cy + kicker_size * LEADING / 2, size=kicker_size,
                            text=fence.kicker, role="ink-mute", field="kicker"))
        cy += kicker_size * LEADING
    t_lines = budget.line_count(fence.title, W - 2 * P, title_size, 0.0, pack)
    texts.append(TextOp(x=W / 2, y=cy + t_lines * title_size * LEADING / 2, size=title_size,
                        text=fence.title, role="ink", weight="bold", max_w=W - 2 * P, field="title"))
    cy += t_lines * title_size * LEADING
    if fence.thesis:
        th = budget.line_count(fence.thesis, W - 2 * P, item_size, 0.0, pack)
        texts.append(TextOp(x=W / 2, y=cy + th * item_size * LEADING / 2, size=item_size,
                            text=fence.thesis, role="ink-soft", max_w=W - 2 * P, field="thesis"))
        cy += th * item_size * LEADING
    y0 = cy + 18.0

    rects: list[RectOp] = []
    center: dict[str, tuple[float, float]] = {}
    for i, nd in enumerate(nodes):
        c, r = pos[nd["id"]]
        nx = P + c * (node_w + G)
        ny = y0 + r * (node_h + G_V)
        rects.append(RectOp(x=nx, y=ny, w=node_w, h=node_h))
        center[nd["id"]] = (nx + node_w / 2, ny + node_h / 2)
        texts.append(TextOp(x=nx + node_w / 2, y=ny + node_h / 2, size=item_size,
                            text=nd["label"], role="ink", max_w=node_w - 2 * NODE_PAD_IN,
                            field=f"nodes[{i}].label"))

    arrows = [ArrowOp(x1=center[e["from"]][0] + node_w / 2 + 8.0, y1=center[e["from"]][1],
                      x2=center[e["to"]][0] - node_w / 2 - 8.0, y2=center[e["to"]][1],
                      style="dashed" if e.get("dashed") else "solid")
              for e in edges]

    bottom = y0 + max(r for _, r in pos.values()) * (node_h + G_V) + node_h
    y = bottom + 12.0
    note = fence.note or DEFAULT_NOTE
    nl = budget.line_count(note, W - 2 * P, item_size, 8.0, pack)
    texts.append(TextOp(x=W / 2, y=y + nl * item_size * LEADING / 2, size=item_size,
                        text=note, role="ink-mute", max_w=W - 2 * P, field="note"))
    y += nl * item_size * LEADING

    if y > H_frame * HEIGHT_LIMIT:
        raise TopologyLayoutError(
            f"도식 높이 {y:.0f}pt > 프레임 {H_frame * HEIGHT_LIMIT:.0f}pt(85%) — 노드 축약 또는 펜스 분할")

    ops = [RectOp(x=0.0, y=0.0, w=W, h=y, rx=0.0, fill_role="paper", stroke_role="rule", stroke_w=0.0),
           *rects, *arrows, *texts]
    _ink_ok(ops, W, y)
    return FigModel(width=W, height=y, ops=tuple(ops), source_index=fence.index)


def _longest_path_layers(nodes: list, edges: list) -> dict:
    ids = [nd["id"] for nd in nodes]
    preds = {i: [] for i in ids}
    succs = {i: [] for i in ids}
    indeg = {i: 0 for i in ids}
    for e in edges:
        succs[e["from"]].append(e["to"])
        preds[e["to"]].append(e["from"])
        indeg[e["to"]] += 1
    order = [i for i in ids if indeg[i] == 0]
    k = 0
    while k < len(order):                  # Kahn — 큐 대신 인덱스 순회(결정론·ids 순서 안정)
        cur = order[k]
        k += 1
        for nxt in succs[cur]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                order.append(nxt)
    if len(order) != len(ids):
        raise TopologyLayoutError("간선 위상 정렬 불가(순환) — 간선 방향 점검")
    layer = {}
    for cur in order:
        layer[cur] = max((layer[p] + 1 for p in preds[cur]), default=0)
    return layer


def _ink_ok(ops, width: float, height: float) -> None:
    for o in ops:
        if isinstance(o, RectOp):
            s = o.stroke_w / 2
            if (o.x - s < -0.001 or o.x + o.w + s > width + 0.001
                    or o.y - s < -0.001 or o.y + o.h + s > height + 0.001):
                raise TopologyLayoutError(
                    f"잉크 bbox 프레임 이탈: rect({o.x:.1f},{o.y:.1f},{o.w:.1f},{o.h:.1f})")
        elif isinstance(o, ArrowOp):
            if (min(o.x1, o.x2) < -0.001 or max(o.x1, o.x2) > width + 0.001
                    or min(o.y1, o.y2) < -0.001 or max(o.y1, o.y2) > height + 0.001):
                raise TopologyLayoutError(
                    f"잉크 bbox 프레임 이탈: arrow({o.x1:.1f},{o.y1:.1f}→{o.x2:.1f},{o.y2:.1f})")
        elif isinstance(o, TextOp):
            hw = (o.max_w or 60.0) / 2
            if o.x - hw < -0.001 or o.x + hw > width + 0.001:
                raise TopologyLayoutError(
                    f"잉크 bbox 프레임 이탈: text({o.field}) x={o.x:.1f} max_w={o.max_w:.1f}")
```

주의: `bottom` 산정의 `max(r for _, r in pos.values())`는 최대 행 인덱스 — `*(node_h+G_V)` 후 `+node_h`로 열 바닥이 된다.

`layout.py` dispatch: `"topology": topology.layout` 등록. `lint.py` 필드 수집(roadmap phases 블록 뒤):

```python
    elif f.layout == "topology":
        for i, nd in enumerate(f.data.get("nodes", [])):
            fields.append((f"nodes[{i}].label", nd.get("label", "")))
```

`render.py` `_sheet_rows`(phases 행 뒤):

```python
    for i, nd in enumerate(f.data.get("nodes", [])):
        rows.append(("노드", f"nodes[{i}].label", str(nd.get("label", ""))))
```

(배치 순서는 cards→before/after→stages→phases→**nodes** — Task 3 path·stack/rings는 nodes 뒤.)

- [ ] **Step 5: 지오메트리·결정론·상한 테스트**

```python
def test_grid_layout_and_node_geometry():
    fig = topo_arch.layout(_fence(), TOKENS)          # 6노드 무간선 practical — 열수 3
    rects = [o for o in fig.ops if isinstance(o, RectOp) and o.fill_role != "paper"]
    assert len(rects) == 6
    W = TOKENS["body_frame_pt"]["x1"] - TOKENS["body_frame_pt"]["x0"]
    node_w = (W - 28.0 - 2 * 28.0) / 3
    assert abs(rects[0].w - node_w) < 0.01
    assert abs(rects[0].x - 14.0) < 0.01
    assert abs(rects[1].x - (14.0 + node_w + 28.0)) < 0.01   # grid 열 간격
    assert abs(rects[3].y - rects[0].y - (rects[0].h + 24.0)) < 0.01  # 2행째


def test_dag_layers_and_arrows():
    fig = topo_arch.layout(_fence(n=4, edges=[(0, 1), (0, 2), (1, 3), (2, 3)]), TOKENS)
    # 층위: n0=0, n1/n2=1, n3=2 → 열수 3. 화살표 4개 전부 x2 > x1(우향)·샤프트 ≥12pt.
    arrows = [o for o in fig.ops if isinstance(o, ArrowOp)]
    assert len(arrows) == 4
    assert all(a.x2 > a.x1 for a in arrows)
    assert all((a.x2 - a.x1) >= 12.0 - 0.01 for a in arrows)  # G 28 − tip-gap 8×2


def test_dag_cycle_rejected():
    with pytest.raises(TopologyLayoutError, match="순환"):
        topo_arch.layout(_fence(n=3, edges=[(0, 1), (1, 2), (2, 0)]), TOKENS)


def test_pack_cap_essay():
    essay = _tokens("essay")
    topo_arch.layout(_fence(n=5), essay)                       # essay 상한 5 — 통과
    with pytest.raises(TopologyLayoutError, match="판형 상한"):
        topo_arch.layout(_fence(n=6), essay)


def test_node_width_floor():
    # essay 5노드 DAG로 열수 5를 만들면 노드 폭이 하상수에 걸린다(n0→n1→n2→n3→n4).
    with pytest.raises(TopologyLayoutError, match="노드 폭"):
        topo_arch.layout(_fence(n=5, edges=[(0, 1), (1, 2), (2, 3), (3, 4)]), _tokens("essay"))


def test_determinism():
    f = _fence(n=5, edges=[(0, 1), (1, 2)])
    assert topo_arch.layout(f, TOKENS).ops == topo_arch.layout(f, TOKENS).ops


def test_dashed_edge_style():
    f2 = _fence(n=3, edges=[(0, 1)])
    f2.data["edges"][0]["dashed"] = True        # 검증 통과 후 속성 주입 — style 방출만 검사
    fig2 = topo_arch.layout(f2, TOKENS)
    assert any(isinstance(o, ArrowOp) and o.style == "dashed" for o in fig2.ops)


def test_topology_elements_reach_lint_and_sheet():
    # 숫자 증거 주입 → I1 검증 단언(loc=nodes[0].label) + 검수 시트 행(nodes[0])
    f = _fence(n=3)
    f.data["nodes"][0]["label"] = "노드 삼개 관문"
    result = lint_mod.check([f], TOKENS)        # 기존 before_after 테스트와 동일 호출 관례
    assert any(getattr(e, "loc", None) == "nodes[0].label" for e in result.verified)
    rows = render_mod._sheet_rows(f)            # 기존 관례 — 실제 함수명은 render.py 참조
    assert ("노드", "nodes[0].label", "노드 삼개 관문") in rows
```

`_tokens`·`TOKENS`·`lint_mod`·`render_mod` 임포트는 기존 archetype 테스트 파일 관례 그대로(`test_infographic_layout_before_after.py` 참조 — lint는 `lint.check(fences, tokens)` 반환 구조, render는 `_sheet_rows(fence)` 시그니처를 해당 파일에서 확인해 관례에 맞춘다).

Run: `python3 -m pytest skills/korean-ebook-typst/tests/test_infographic_layout_topology.py -q` → 전부 PASS.

- [ ] **Step 6: 골든 스냅샷**

cards 패턴 복제 `test_topology_golden_snapshot` — fixture `golden-topology-practical.typ`(5노드 4간선 practical, 숫자·약어 부재). `IG_REGEN_GOLDEN=1` 재생성 → 눈검(grid/층위 정합·화살표 tip-gap·넘침 없음) → 재실행 바이트 동일 PASS.

- [ ] **Step 7: 전체 스위트** — `python3 -m pytest skills/korean-ebook-typst/tests/ -q` → 207 + 신규 전부 PASS

- [ ] **Step 8: 커밋** — `git commit -m "feat: topology archetype — grid·DAG 층위 배치·간선 화살표·판형 상한 + network 별칭"`

---

### Task 3: approval + layers archetype + rot·circle 프리미티브 + 골든 2종

**Files:**
- Modify: `skills/korean-ebook-typst/scripts/infographic/model.py` (RectOp.rot 필드·CircleOp 신규)
- Modify: `skills/korean-ebook-typst/scripts/infographic/emit.py` (rot 인자·ig-circle 방출)
- Modify: `skills/korean-ebook-typst/templates/infographic/helper.typ` (ig-rect rot 파라미터·ig-circle)
- Create: `skills/korean-ebook-typst/scripts/infographic/archetypes/approval.py`·`layers.py`
- Modify: parse.py·layout.py·lint.py·render.py (approval·layers 분기)
- Test: `tests/test_infographic_layout_approval.py`·`tests/test_infographic_layout_layers.py` + 골든 2종

**Interfaces:**
- Consumes: `base.sizes`, `budget.line_count`, 기존 ops
- Produces: `model.RectOp.rot: float = 0.0`(0=방출 생략 — 골든 바이트 불변), `model.CircleOp(x, y, r, fill_role="surface-tint", stroke_role="rule", stroke_w=0.5)`, `archetypes.approval.layout`·`ApprovalLayoutError`, `archetypes.layers.layout`·`LayersLayoutError`
- 펜스 데이터: approval `path[]`({title, text?, gate?}), layers `stack[]` 또는 `rings[]`(각 {label}) — 정확히 하나

**지오메트리:** approval = 가로 경로 스텝 카드(rx 8) + 게이트 스텝에 상단변 중심 45° 회전 마커(한 변 12pt, bbox 16.97pt). G=28(tip-gap 8 양측 → 샤프트 12pt). MIN_STEP_W=48.0(도달 한계 실측: essay 3스텝 55.2 / practical 4·55.6 / b5 5·49.3 / lecture 6·49.5pt). layers stack = 전폭 행 스택(순서 = 상→하), rings = 동심원(외→내, 반경 R_max=(W−2P)/2에서 등간격, R_min=0.25·R_max), 링 라벨은 12시 방향 현(chord) 폭 안 실측.

- [ ] **Step 1: parse 실패 테스트 2종 작성**

```python
# tests/test_infographic_layout_approval.py — 스펙 §6.2·§6.3 approval 지오메트리·결정론.
"""test_infographic_layout_approval.py — 스펙 §6.2·§6.3 approval 지오메트리·결정론."""
import json

import pytest

from scripts.infographic.archetypes import approval as appr_arch
from scripts.infographic.archetypes.approval import ApprovalLayoutError
from scripts.infographic.parse import ParseError, parse_fence


def _fence(n=4, gates=(1, 3), **extra):
    steps = [{"title": f"결재 단계 {i}", "text": "검토 후 진행", **({"gate": True} if i in gates else {})}
             for i in range(n)]
    payload = {"layout": "approval", "title": "결재 흐름 점검 제목", "path": steps}
    payload.update(extra)
    return parse_fence(0, json.dumps(payload, ensure_ascii=False))


def test_parse_bounds():
    with pytest.raises(ParseError):
        _fence(n=2)                                       # 하한 3 미만
    with pytest.raises(ParseError):
        _fence(n=9)                                       # 절대 상한 8 초과
    with pytest.raises(ParseError):
        _fence(n=5, gates=(0, 1, 2, 3, 4))                # 게이트 5개 > 상한 4
    with pytest.raises(ParseError):
        parse_fence(0, '{"layout":"approval","title":"t","path":['
                       '{"title":"기획"},{"text":"제목 누락"},{"title":"승인"}]}')
```

```python
# tests/test_infographic_layout_layers.py — 스펙 §6.2·§6.3 layers 지오메트리·결정론.
"""test_infographic_layout_layers.py — 스펙 §6.2·§6.3 layers 지오메트리·결정론."""
import json

import pytest

from scripts.infographic.archetypes import layers as layers_arch
from scripts.infographic.parse import ParseError, parse_fence


def _stack_fence(n=4, **extra):
    payload = {"layout": "layers", "title": "계층 구조 점검 제목",
               "stack": [{"label": f"계층 {i}"} for i in range(n)]}
    payload.update(extra)
    return parse_fence(0, json.dumps(payload, ensure_ascii=False))


def _rings_fence(n=4):
    return parse_fence(0, json.dumps({"layout": "layers", "title": "계층 구조 점검 제목",
                                      "rings": [{"label": f"링 {i}"} for i in range(n)]},
                                     ensure_ascii=False))


def test_parse_bounds():
    with pytest.raises(ParseError):                        # stack·rings 동시
        parse_fence(0, '{"layout":"layers","title":"t","stack":[{"label":"외부"},{"label":"내부"}],'
                       '"rings":[{"label":"외부"},{"label":"내부"}]}')
    with pytest.raises(ParseError):                        # 둘 다 없음
        parse_fence(0, '{"layout":"layers","title":"t"}')
    with pytest.raises(ParseError):
        _stack_fence(n=7)                                  # 상한 6 초과
    with pytest.raises(ParseError):
        _stack_fence(n=1)                                  # 하한 2 미만
    with pytest.raises(ParseError):
        parse_fence(0, '{"layout":"layers","title":"t","stack":[{"label":"외부"},{"label":""}]}')
```

- [ ] **Step 2: RED 확인** — ImportError

- [ ] **Step 3: parse.py** — 상수 `PATH_MIN, PATH_MAX = 3, 8`, `GATE_MAX = 4`, `LAYER_MIN, LAYER_MAX = 2, 6`, VALID_LAYOUTS + approval·layers, 분기 2개(topology 뒤):

```python
    elif f.layout == "approval":
        path = data.get("path")
        if not isinstance(path, list) or not (PATH_MIN <= len(path) <= PATH_MAX):
            raise ParseError("경로 스텝 수는 3~8개 필요")
        gates = 0
        for st in path:
            if not isinstance(st, dict) or not isinstance(st.get("title"), str) or not st["title"]:
                raise ParseError("경로 스텝은 title 비빈 문자열 필요")
            if "text" in st and not isinstance(st["text"], str):
                raise ParseError("text는 문자열 필요")
            if st.get("gate"):
                gates += 1
        if gates > GATE_MAX:
            raise ParseError(f"게이트 {gates}개 > 상한 {GATE_MAX}개 — 게이트 통합")
    elif f.layout == "layers":
        stack, rings = data.get("stack"), data.get("rings")
        if (stack is None) == (rings is None):
            raise ParseError("stack·rings 중 정확히 하나 필요")
        rows = stack if stack is not None else rings
        if not isinstance(rows, list) or not (LAYER_MIN <= len(rows) <= LAYER_MAX):
            raise ParseError("계층 수는 2~6개 필요")
        for row in rows:
            if not isinstance(row, dict) or not isinstance(row.get("label"), str) or not row["label"]:
                raise ParseError("계층은 label 비빈 문자열 필요")
```

- [ ] **Step 4: model.py·emit.py·helper.typ 프리미티브**

model.py:

```python
@dataclass(frozen=True)
class RectOp:
    x: float; y: float; w: float; h: float
    rx: float = 8.0
    fill_role: str = "surface-tint"
    stroke_role: str = "rule"
    stroke_w: float = 0.5
    rot: float = 0.0            # 도 단위 회전(중심 기준) — 0=방출 생략(게이트 마커 등)


@dataclass(frozen=True)
class CircleOp:
    x: float; y: float; r: float
    fill_role: str = "surface-tint"
    stroke_role: str = "rule"
    stroke_w: float = 0.5
```

emit.py RectOp 행에 `rot` 조건 인자 추가·CircleOp 분기 추가:

```python
        if isinstance(op, RectOp):
            rt = f", rot: {op.rot:g}deg" if op.rot != 0.0 else ""
            lines.append(
                f"  #ig-rect({_n(op.x)}, {_n(op.y)}, {_n(op.w)}, {_n(op.h)}, "
                f"rx: {_n(op.rx)}pt, fill-role: \"{op.fill_role}\", "
                f"stroke-role: \"{op.stroke_role}\", stroke-w: {_n(op.stroke_w)}pt{rt})")
        elif isinstance(op, CircleOp):
            lines.append(
                f"  #ig-circle({_n(op.x)}, {_n(op.y)}, {_n(op.r)}, "
                f"fill-role: \"{op.fill_role}\", stroke-role: \"{op.stroke_role}\", "
                f"stroke-w: {_n(op.stroke_w)}pt)")
```

helper.typ:

```typst
// rect — place(top+left)는 박스 좌상단을 (x,y)에 놓는다(실측 정확).
// rot≠0이면 rect 중심 기준 회전(게이트 다이아몬드 등) — 회전 잉크는 중심 대칭으로 삐져나온다.
#let ig-rect(x, y, w, h, rx: 8pt, fill-role: "surface-tint",
             stroke-role: "rule", stroke-w: 0.5pt, rot: 0deg) = place(
  top + left, dx: pt(x), dy: pt(y),
  rotate(rot, rect(width: pt(w), height: pt(h), radius: rx,
       fill: ig-color(fill-role),
       stroke: if stroke-w == 0pt { none } else {
         (paint: ig-color(stroke-role), thickness: stroke-w) })),
)

// circle — (x,y)는 중심. rings 동심원 변형(스펙 §6.3).
#let ig-circle(x, y, r, fill-role: "surface-tint",
               stroke-role: "rule", stroke-w: 0.5pt) = place(
  top + left, dx: pt(x - r), dy: pt(y - r),
  circle(radius: pt(r), fill: ig-color(fill-role),
         stroke: (paint: ig-color(stroke-role), thickness: stroke-w)),
)
```

(기존 골든은 rot=0 → 방출 바이트 불변 — Task 1 재생성 골든이 그대로 통과해야 한다.)

- [ ] **Step 5: approval.py 구현**

```python
"""approval — 가로 결재 경로 + 게이트 다이아몬드(스펙 §6.3). 폭 하상수로 즉시 에러."""
from __future__ import annotations

from .. import budget
from ..model import ArrowOp, FigModel, RectOp, TextOp
from ..parse import DEFAULT_NOTE, Fence
from .base import LayoutError, sizes

P = 14.0
G = 28.0                     # 커넥터 복도 — tip-gap 8 양측 후 샤프트 12pt(§6.1)
STEP_PAD_IN = 8.0
STEP_PAD_V = 10.0
STEP_GAP_V = 6.0             # 제목·본문 사이
MIN_STEP_W = 48.0            # 도달 한계 실측 — essay 3·55.2 / practical 4·55.6 / b5 5·49.3 / lecture 6·49.5pt
MARK_SIDE = 12.0             # 게이트 다이아몬드 한 변 — 회전 bbox 16.97pt
LEADING = 1.3
HEIGHT_LIMIT = 0.85


class ApprovalLayoutError(LayoutError):
    pass


def layout(fence: Fence, tokens: dict) -> FigModel:
    frame = tokens["body_frame_pt"]
    W = frame["x1"] - frame["x0"]
    H_frame = frame["y1"] - frame["y0"]
    pack = tokens.get("style", "practical")
    s = sizes(tokens)
    kicker_size, title_size = s["kicker"], s["title"]
    ph_title_size, item_size = s["ph_title"], s["item"]

    steps = fence.data["path"]
    n = len(steps)

    step_w = (W - 2 * P - (n - 1) * G) / n
    if step_w < MIN_STEP_W:
        raise ApprovalLayoutError(
            f"스텝 폭 {step_w:.1f}pt < {MIN_STEP_W:.0f}pt({pack}) — 경로 축약 또는 펜스 분할")

    def step_h(st: dict) -> float:
        h = 2 * STEP_PAD_V
        h += budget.line_count(st["title"], step_w, ph_title_size, STEP_PAD_IN, pack) * ph_title_size * LEADING
        if st.get("text"):
            h += STEP_GAP_V + budget.line_count(st["text"], step_w, item_size, STEP_PAD_IN, pack) * item_size * LEADING
        return h

    step_h_max = max(step_h(st) for st in steps)

    # 헤더(공통 구조) — kicker는 저작 계약 초단문(1줄)
    texts: list[TextOp] = []
    cy = 0.0
    if fence.kicker:
        texts.append(TextOp(x=W / 2, y=cy + kicker_size * LEADING / 2, size=kicker_size,
                            text=fence.kicker, role="ink-mute", field="kicker"))
        cy += kicker_size * LEADING
    t_lines = budget.line_count(fence.title, W - 2 * P, title_size, 0.0, pack)
    texts.append(TextOp(x=W / 2, y=cy + t_lines * title_size * LEADING / 2, size=title_size,
                        text=fence.title, role="ink", weight="bold", max_w=W - 2 * P, field="title"))
    cy += t_lines * title_size * LEADING
    if fence.thesis:
        th = budget.line_count(fence.thesis, W - 2 * P, item_size, 0.0, pack)
        texts.append(TextOp(x=W / 2, y=cy + th * item_size * LEADING / 2, size=item_size,
                            text=fence.thesis, role="ink-soft", max_w=W - 2 * P, field="thesis"))
        cy += th * item_size * LEADING
    y0 = cy + 18.0 + MARK_SIDE * 0.8            # 마커 상단 돌출 여유

    rects: list[RectOp] = []
    arrows: list[ArrowOp] = []
    for i, st in enumerate(steps):
        sx = P + i * (step_w + G)
        rects.append(RectOp(x=sx, y=y0, w=step_w, h=step_h_max))
        if st.get("gate"):
            rects.append(RectOp(x=sx + step_w / 2 - MARK_SIDE / 2, y=y0 - MARK_SIDE / 2,
                                w=MARK_SIDE, h=MARK_SIDE, rx=0.0, rot=45.0))
        ty = y0 + STEP_PAD_V
        tl = budget.line_count(st["title"], step_w, ph_title_size, STEP_PAD_IN, pack)
        texts.append(TextOp(x=sx + step_w / 2, y=ty + tl * ph_title_size * LEADING / 2,
                            size=ph_title_size, text=st["title"], role="ink", weight="bold",
                            max_w=step_w, field=f"path[{i}].title"))
        ty += tl * ph_title_size * LEADING
        if st.get("text"):
            gl = budget.line_count(st["text"], step_w, item_size, STEP_PAD_IN, pack)
            ty += STEP_GAP_V
            texts.append(TextOp(x=sx + step_w / 2, y=ty + gl * item_size * LEADING / 2,
                                size=item_size, text=st["text"], role="ink-soft",
                                max_w=step_w, field=f"path[{i}].text"))
            ty += gl * item_size * LEADING
        if i < n - 1:
            arrows.append(ArrowOp(x1=sx + step_w + 8.0, y1=y0 + step_h_max / 2,
                                  x2=sx + step_w + G - 8.0, y2=y0 + step_h_max / 2))

    y = y0 + step_h_max + 12.0
    note = fence.note or DEFAULT_NOTE
    nl = budget.line_count(note, W - 2 * P, item_size, 8.0, pack)
    texts.append(TextOp(x=W / 2, y=y + nl * item_size * LEADING / 2, size=item_size,
                        text=note, role="ink-mute", max_w=W - 2 * P, field="note"))
    y += nl * item_size * LEADING

    if y > H_frame * HEIGHT_LIMIT:
        raise ApprovalLayoutError(
            f"도식 높이 {y:.0f}pt > 프레임 {H_frame * HEIGHT_LIMIT:.0f}pt(85%) — 스텝 축약 또는 펜스 분할")

    ops = [RectOp(x=0.0, y=0.0, w=W, h=y, rx=0.0, fill_role="paper", stroke_role="rule", stroke_w=0.0),
           *rects, *arrows, *texts]
    _ink_ok(ops, W, y)
    return FigModel(width=W, height=y, ops=tuple(ops), source_index=fence.index)


def _ink_ok(ops, width: float, height: float) -> None:
    # _ink_ok 표준형(Task 1과 동일 — Rect stroke_w/2 포함). 회전 rect는 중심 대칭
    # 확장이므로 등가 반폭 w/2·h/2의 대각 반경을 더해 검사한다(보수적).
    import math as _m
    for o in ops:
        if isinstance(o, RectOp):
            if o.rot != 0.0:
                rad = _m.sqrt(o.w * o.w + o.h * o.h) / 2
                cx, cy2 = o.x + o.w / 2, o.y + o.h / 2
                if (cx - rad < -0.001 or cx + rad > width + 0.001
                        or cy2 - rad < -0.001 or cy2 + rad > height + 0.001):
                    raise ApprovalLayoutError(
                        f"잉크 bbox 프레임 이탈: rect(rot {o.rot:.0f}°) 중심({cx:.1f},{cy2:.1f})")
            else:
                s = o.stroke_w / 2
                if (o.x - s < -0.001 or o.x + o.w + s > width + 0.001
                        or o.y - s < -0.001 or o.y + o.h + s > height + 0.001):
                    raise ApprovalLayoutError(
                        f"잉크 bbox 프레임 이탈: rect({o.x:.1f},{o.y:.1f},{o.w:.1f},{o.h:.1f})")
        elif isinstance(o, ArrowOp):
            if (min(o.x1, o.x2) < -0.001 or max(o.x1, o.x2) > width + 0.001
                    or min(o.y1, o.y2) < -0.001 or max(o.y1, o.y2) > height + 0.001):
                raise ApprovalLayoutError(
                    f"잉크 bbox 프레임 이탈: arrow({o.x1:.1f},{o.y1:.1f}→{o.x2:.1f},{o.y2:.1f})")
        elif isinstance(o, TextOp):
            hw = (o.max_w or 60.0) / 2
            if o.x - hw < -0.001 or o.x + hw > width + 0.001:
                raise ApprovalLayoutError(
                    f"잉크 bbox 프레임 이탈: text({o.field}) x={o.x:.1f} max_w={o.max_w:.1f}")
```

- [ ] **Step 6: layers.py 구현**

```python
"""layers — 수평 스택 기본·rings 동심원 변형(스펙 §6.3). 계층 수 절대 상한은 parse가 검사."""
from __future__ import annotations

import math

from .. import budget
from ..model import CircleOp, FigModel, RectOp, TextOp
from ..parse import DEFAULT_NOTE, Fence
from .base import LayoutError, sizes

P = 14.0
ROW_PAD_IN = 8.0
ROW_PAD_V = 10.0
ROW_GAP = 10.0
RING_MIN_FRAC = 0.25          # 최내곽 반경 = R_max의 25%
RING_LABEL_IN = 6.0           # 링 상단부터 라벨 중심까지
LEADING = 1.3
HEIGHT_LIMIT = 0.85


class LayersLayoutError(LayoutError):
    pass


def layout(fence: Fence, tokens: dict) -> FigModel:
    frame = tokens["body_frame_pt"]
    W = frame["x1"] - frame["x0"]
    H_frame = frame["y1"] - frame["y0"]
    pack = tokens.get("style", "practical")
    s = sizes(tokens)
    kicker_size, title_size, item_size = s["kicker"], s["title"], s["item"]

    stack = fence.data.get("stack")
    rings = fence.data.get("rings")

    # 헤더(공통 구조) — kicker는 저작 계약 초단문(1줄)
    texts: list[TextOp] = []
    cy = 0.0
    if fence.kicker:
        texts.append(TextOp(x=W / 2, y=cy + kicker_size * LEADING / 2, size=kicker_size,
                            text=fence.kicker, role="ink-mute", field="kicker"))
        cy += kicker_size * LEADING
    t_lines = budget.line_count(fence.title, W - 2 * P, title_size, 0.0, pack)
    texts.append(TextOp(x=W / 2, y=cy + t_lines * title_size * LEADING / 2, size=title_size,
                        text=fence.title, role="ink", weight="bold", max_w=W - 2 * P, field="title"))
    cy += t_lines * title_size * LEADING
    if fence.thesis:
        th = budget.line_count(fence.thesis, W - 2 * P, item_size, 0.0, pack)
        texts.append(TextOp(x=W / 2, y=cy + th * item_size * LEADING / 2, size=item_size,
                            text=fence.thesis, role="ink-soft", max_w=W - 2 * P, field="thesis"))
        cy += th * item_size * LEADING
    y0 = cy + 18.0

    rects: list[RectOp] = []
    circles: list[CircleOp] = []
    if stack is not None:
        # 수평 스택 — 주어진 순서 = 위→아래. 전폭 행, 높이 실측.
        y = y0
        for i, row in enumerate(stack):
            row_w = W - 2 * P
            rl = budget.line_count(row["label"], row_w, item_size, ROW_PAD_IN, pack)
            row_h = 2 * ROW_PAD_V + rl * item_size * LEADING
            rects.append(RectOp(x=P, y=y, w=row_w, h=row_h))
            texts.append(TextOp(x=W / 2, y=y + ROW_PAD_V + rl * item_size * LEADING / 2,
                                size=item_size, text=row["label"], role="ink",
                                max_w=row_w, field=f"stack[{i}].label"))
            y += row_h + ROW_GAP
        y -= ROW_GAP
    else:
        # 동심원 — rings[0] = 최외곽. 등간격 반경, 라벨은 12시 방향 현(chord) 폭 안 실측.
        n = len(rings)
        r_max = (W - 2 * P) / 2
        r_min = RING_MIN_FRAC * r_max
        step = (r_max - r_min) / (n - 1) if n > 1 else 0.0
        cc_y = y0 + r_max
        for i, ring in enumerate(rings):
            r = r_max - i * step
            circles.append(CircleOp(x=W / 2, y=cc_y, r=r))
        for i, ring in enumerate(rings):
            r = r_max - i * step
            d = RING_LABEL_IN + item_size * LEADING / 2
            chord = 2 * math.sqrt(max(r * r - d * d, 0.0)) - 2 * ROW_PAD_IN
            rl = budget.line_count(ring["label"], chord, item_size, ROW_PAD_IN, pack)
            texts.append(TextOp(x=W / 2, y=cc_y - r + d, size=item_size,
                                text=ring["label"], role="ink", max_w=chord,
                                field=f"rings[{i}].label"))
        y = y0 + 2 * r_max

    y += 12.0
    note = fence.note or DEFAULT_NOTE
    nl = budget.line_count(note, W - 2 * P, item_size, 8.0, pack)
    texts.append(TextOp(x=W / 2, y=y + nl * item_size * LEADING / 2, size=item_size,
                        text=note, role="ink-mute", max_w=W - 2 * P, field="note"))
    y += nl * item_size * LEADING

    if y > H_frame * HEIGHT_LIMIT:
        raise LayersLayoutError(
            f"도식 높이 {y:.0f}pt > 프레임 {H_frame * HEIGHT_LIMIT:.0f}pt(85%) — 계층 축약 또는 펜스 분할")

    ops = [RectOp(x=0.0, y=0.0, w=W, h=y, rx=0.0, fill_role="paper", stroke_role="rule", stroke_w=0.0),
           *circles, *rects, *texts]
    _ink_ok(ops, W, y)
    return FigModel(width=W, height=y, ops=tuple(ops), source_index=fence.index)


def _ink_ok(ops, width: float, height: float) -> None:
    # _ink_ok 표준형(Task 1과 동일 — Rect stroke_w/2 포함) + Circle 분기(반경+반 스트로크).
    for o in ops:
        if isinstance(o, CircleOp):
            s = o.stroke_w / 2
            if (o.x - o.r - s < -0.001 or o.x + o.r + s > width + 0.001
                    or o.y - o.r - s < -0.001 or o.y + o.r + s > height + 0.001):
                raise LayersLayoutError(
                    f"잉크 bbox 프레임 이탈: circle({o.x:.1f},{o.y:.1f},r={o.r:.1f})")
        elif isinstance(o, RectOp):
            s = o.stroke_w / 2
            if (o.x - s < -0.001 or o.x + o.w + s > width + 0.001
                    or o.y - s < -0.001 or o.y + o.h + s > height + 0.001):
                raise LayersLayoutError(
                    f"잉크 bbox 프레임 이탈: rect({o.x:.1f},{o.y:.1f},{o.w:.1f},{o.h:.1f})")
        elif isinstance(o, TextOp):
            hw = (o.max_w or 60.0) / 2
            if o.x - hw < -0.001 or o.x + hw > width + 0.001:
                raise LayersLayoutError(
                    f"잉크 bbox 프레임 이탈: text({o.field}) x={o.x:.1f} max_w={o.max_w:.1f}")
```

`layout.py` dispatch 2행·`lint.py` 필드(path[i].title·path[i].text / stack[i].label·rings[i].label — nodes 뒤)·`render.py` `_sheet_rows`(경로·계층 행) 각 추가.

- [ ] **Step 7: 테스트 수량**

approval: parse 경계 4·스텝 지오메트리(간격·균일 높이)·게이트 마커 rot=45 방출·폭 하상수 에러(practical 5스텝 → `스텝 폭` 매치)·결정론·lint/sheet 도달 = 8종.
layers: parse 경계 5(동시·둘다 없음·상한·하한·빈 라벨)·스택 행 지오메트리(전폭·간격 10)·rings 반경 등간격·rings 라벨 chord 상한·결정론·lint/sheet 도달 = 8종.
핵심 단언 예:

```python
def test_approval_step_geometry_and_gate_marker():
    fig = appr_arch.layout(_fence(n=4, gates=(1,)), TOKENS)
    rects = [o for o in fig.ops if isinstance(o, RectOp) and o.fill_role != "paper"]
    cards = [r for r in rects if r.w > 30.0]              # 마커(12pt)와 카드 분리
    markers = [r for r in rects if abs(r.w - 12.0) < 0.01]
    assert len(cards) == 4 and len(markers) == 1
    W = TOKENS["body_frame_pt"]["x1"] - TOKENS["body_frame_pt"]["x0"]
    step_w = (W - 28.0 - 3 * 28.0) / 4
    assert abs(cards[0].w - step_w) < 0.01
    assert abs(cards[1].x - (14.0 + step_w + 28.0)) < 0.01
    assert markers[0].rot == 45.0 and markers[0].rx == 0.0
    assert abs(markers[0].x + 6.0 - (cards[1].x + step_w / 2)) < 0.01  # 상단변 중심
    arrows = [o for o in fig.ops if isinstance(o, ArrowOp)]
    assert len(arrows) == 3 and all((a.x2 - a.x1) >= 12.0 - 0.01 for a in arrows)


def test_approval_step_width_floor():
    with pytest.raises(ApprovalLayoutError, match="스텝 폭"):
        appr_arch.layout(_fence(n=5), TOKENS)             # practical 5스텝 → 38.9pt < 48pt


def test_stack_rows_full_width():
    fig = layers_arch.layout(_stack_fence(n=4), TOKENS)
    rects = [o for o in fig.ops if isinstance(o, RectOp) and o.fill_role != "paper"]
    W = TOKENS["body_frame_pt"]["x1"] - TOKENS["body_frame_pt"]["x0"]
    assert len(rects) == 4
    assert all(abs(r.x - 14.0) < 0.01 and abs(r.w - (W - 28.0)) < 0.01 for r in rects)
    assert abs(rects[1].y - rects[0].y - rects[0].h - 10.0) < 0.01
```

```python

```python
def test_rings_radii_equidistant():
    fig = layers_arch.layout(_rings_fence(), TOKENS)          # rings 4개 practical
    cs = [o for o in fig.ops if isinstance(o, CircleOp)]
    assert len(cs) == 4
    r_max = (TOKENS["body_frame_pt"]["x1"] - TOKENS["body_frame_pt"]["x0"] - 28.0) / 2
    step = (r_max - 0.25 * r_max) / 3
    assert abs(cs[0].r - r_max) < 0.01
    assert abs(cs[3].r - (r_max - 3 * step)) < 0.01
```

- [ ] **Step 8: 골든 2종** — `golden-approval-practical.typ`(4스텝·게이트 2·rings 아님)·`golden-layers-practical.typ`(stack 4행). 재생성→눈검(다이아몬드 마커 45°·스택 간격·넘침 없음)→바이트 동일 PASS.

- [ ] **Step 9: 전체 스위트 + 커밋** — `feat: approval·layers archetype — 결재 경로 게이트 다이아몬드·스택/동심원 + rot·circle 프리미티브`

---

### Task 4: 골든 교정 3주기 + authoring.md Phase 4판 + PACK_STAGES + SKILL.md + 통합 테스트

**Files:**
- Modify: `skills/korean-ebook-typst/scripts/infographic/archetypes/ladder.py` (PACK_STAGES 판형 상한)
- Create: `skills/korean-ebook-typst/tests/fixtures/infographic/calib-topology.md`·`calib-approval.md`·`calib-layers.md`
- Modify: `skills/korean-ebook-typst/references/infographic/authoring.md` (3 섹션·치트시트·상한 표·라우팅·교정 3주기)
- Modify: `skills/korean-ebook-typst/SKILL.md` (Phase 4판 나열)
- Test: `skills/korean-ebook-typst/tests/test_infographic_build_integration.py` (Phase 4 통합)·ladder 테스트 1건 기대치 갱신

**Interfaces:**
- Consumes: Task 1~3 산출(9종 VALID_LAYOUTS·sizes 팩토리·max_w 강제 emit)
- Produces: ladder 판형 상한 에러(`단계 n개 > 판형 상한 m단계(팩)` — essay 5단계가 기존 "계단 단 간격" 대신 이 에러로 선행), 교정 3주기 판정(계수 갱신 여부), authoring.md Phase 4판

- [ ] **Step 1: ladder PACK_STAGES**

ladder.py 상수부에 추가 후 절대 상한 검사 뒤(스펙 §6.2 — 절대보다 우선 적용이므로 stages 길이 검사 직후):

```python
PACK_STAGES = {"essay": 4, "practical": 5, "b5": 5, "business": 5, "lecture": 5}
```

layout 진입 초반 — stages 파악 직후·계단 지오메트리 앞에 삽입(절대 상한 3~5는 parse가, 판형 상한은 layout이 검사 — essay 5단계가 기존 "계단 단 간격" 에러에 앞서 판형 에러로 선행):

```python
    cap = PACK_STAGES.get(pack)
    if cap is None:
        raise LadderLayoutError(f"알 수 없는 스타일 팩 {pack!r}")
    if len(stages) > cap:
        raise LadderLayoutError(
            f"단계 {len(stages)}개 > 판형 상한 {cap}단계({pack}) — 단계 통합 또는 펜스 분할")
```

기존 essay 5단계 테스트 기대치 갱신(`grep -n "계단" tests/test_infographic_layout_ladder.py` 로 위치 확인 — 메시지 매치를 `간격` → `판형 상한` 으로):

```python
def test_essay_five_stages_pack_cap():     # 기존 essay 5단계 케이스를 이 형태로 교체
    with pytest.raises(LadderLayoutError, match="판형 상한"):
        ladder_arch.layout(_fence(n=5), _tokens("essay"))
```

- [ ] **Step 2: calib fixture 3종** — Phase 3 관례(5팩 전수 렌더 전제·숫자·약어 부재·음절 변주 4/9/13):
  - `calib-topology.md`: 노드 6(무간선 grid — 층위 수 편차로 5팩 폭 실패 방지), 라벨 음절 4·9·13 변주
  - `calib-approval.md`: 경로 4·게이트 2, title 음절 4/9/13 + text 음절 9
  - `calib-layers.md`: stack 4(전팩 렌더 안전 — rings는 chord 실측 편차 큼), 라벨 음절 4·9·13

- [ ] **Step 3: 교정 3주기** — Phase 2·3 절차 동일: 3 fixture × 5팩 15렌더(`cli.py preview --style <팩>`) → PyMuPDF 스팬 bbox 자당폭 + measure() 프로브 2중화 → 실측수용자수 vs `max_units` 비율 → 팩 평균 드리프트 vs Phase 2 계수 → ±0.05 데드밴드 판정. **PACK_KO_FACTOR 갱신 시에만** budget.py 수정 + m7 골든 9종 재확증(IG_REGEN_GOLDEN 웨이브). 무갱신이면 budget.py·골든 불변. 실측치 전부 커밋 body에 기록.

- [ ] **Step 4: authoring.md Phase 4판** — 헤더 "(Phase 4 — +topology·approval·layers)"·`### topology`·`### approval`·`### layers` 3섹션(roadmap 뒤, cards 구조 복제 — 예시 펜스 payload는 Task 2·3 골든/테스트 데이터에서)·치트시트 행(노드 라벨·경로 제목/본문·스택 라벨·링 라벨 — 폭 종류 문단 갱신)·판형 상한 표 topology 행(5/6/7/8/8) + **ladder 단계 행(4/5/5/5/5) 추가** + approval·layers "판형 표 없음 — 폭 하상수 에러" 불릿·라우팅 3행 "Phase 4 사용 가능"·공통 필드 layout 행 9종 + `network` 별칭·emit max_w 강제 노트(Task 1 — "상자 폭 초과 시 상자 안 줄바꿈, 예산표와 렌더가 일치")·교정 3주기 수치 기록·kicker 초단문 1줄 계약 명시.
  수치는 전부 실측 산출(`.scratch/` 스크립트 — tokens.json 실값 + 모듈 공식) 후 기재.

- [ ] **Step 5: SKILL.md** — :25 헤더 "(인포그래픽 — Phase 4)", :28 나열에 `topology`(구성 관계)·`approval`(결재 흐름)·`layers`(계층 구조) 추가(괄호 gloss는 authoring 섹션 제목 그대로).

- [ ] **Step 6: 통합 테스트**

`test_infographic_build_integration.py`에 추가 — Phase 3 통합(`test_phase3_archetypes_build_pdf_and_review_sheets`)과 동일 하니스·관례 복제:

```python
PHASE4_MD = """# 검증 원고

## 검증 챕터

​```infographic
{"layout":"topology","title":"구성 요소 관계","kicker":"구성",
 "nodes":[{"id":"a","label":"입력 수집"},{"id":"b","label":"전처리"},
          {"id":"c","label":"변환"},{"id":"d","label":"저장"},{"id":"e","label":"질의"}],
 "edges":[{"from":"a","to":"b"},{"from":"b","to":"c"},{"from":"c","to":"d"},
          {"from":"d","to":"e","dashed":true}]}
​```

​```infographic
{"layout":"approval","title":"결재 흐름","kicker":"결재",
 "path":[{"title":"기획","text":"방향 확정"},{"title":"부서 검토","gate":true},
         {"title":"예산 승인","gate":true},{"title":"집행","text":"실행"}]}
​```

​```infographic
{"layout":"layers","title":"계층 구조","kicker":"구조",
 "stack":[{"label":"표현 계층"},{"label":"응용 계층"},
          {"label":"도메인 계층"},{"label":"자료 계층"}]}
​```
"""


def test_phase4_archetypes_build_pdf_and_review_sheets(tmp_path):
    # 종료 조건(스펙 §8 Phase 4): 신규 3종 펜스가 빌드 전 과정을 통과한다 —
    # 펜스↔emit 1:1 · 챕터 typ include 치환 · PDF 생성 · 검수 시트 신규 필드 행.
    book = tmp_path / "book4"
    (book / "manuscript").mkdir(parents=True)
    (book / "manuscript" / "ch01.md").write_text(PHASE4_MD, encoding="utf-8")
    (book / "typst-build.yaml").write_text(
        'style: practical\n' 'title: "페이즈4책"\n' 'subtitle: "부"\n'
        'author: "KLIC"\n' 'date: "2026-08"\n'
        "chapters:\n  - manuscript/ch01.md\n", encoding="utf-8")
    r = subprocess.run([sys.executable, str(SKILL / "scripts" / "build.py"), str(book)],
                       capture_output=True, text=True, timeout=180)
    assert r.returncode == 0, r.stderr
    typ = (book / "build" / "typ" / "000-ch01.typ").read_text(encoding="utf-8")
    for n in (1, 2, 3):
        assert f'#include "../infographic/000-fig0{n}.typ"' in typ
        assert (book / "build" / "infographic" / f"000-fig0{n}.typ").exists()
    assert len(list((book / "build" / "infographic").glob("000-fig*.typ"))) == 3   # 중복 emit 방어
    sheets = {n: (book / "build" / "infographic" / f"000-fig0{n}.review.md").read_text(encoding="utf-8")
              for n in (1, 2, 3)}
    assert "nodes[2].label" in sheets[1]                     # topology 변환 노드
    assert "nodes[0].label" in sheets[1]                     # 첫 노드 — 전진 경로
    assert "path[1].title" in sheets[2]                      # approval 게이트 스텝
    assert "path[3].title" in sheets[2]                      # 마지막 스텝
    assert "stack[3].label" in sheets[3]                     # layers 마지막 계층
    assert "stack[0].label" in sheets[3]
    for s in sheets.values():
        assert "I1 통과" in s                                # 숫자 전부 교차검증 통과
    pdf = book / "draft" / "페이즈4책.pdf"
    assert pdf.exists() and pdf.stat().st_size > 10_000, "최종 PDF 없음"
```

(모듈 상단 `subprocess`·`sys`·`SKILL` 임포트는 기존 파일 상단에 이미 존재 — 그대로 사용. PHASE4_MD의 펜스 블록 경계는 원고 안 실제 삼중 백틱.)

- [ ] **Step 7: 종료 조건 확인** — 단위(topology 7+·approval 7+·layers 7+)·골든 9종 전부 존재+PASS·통합 2종(Phase 3+4)·authoring 섹션 3개·검수 시트(빌드 경로)·전체 스위트 green.

- [ ] **Step 8: 커밋** — `docs: 인포그래픽 가이드 Phase 4판 — topology·approval·layers 저작 규칙·치트시트 + 교정 3주기 + ladder 판형 상한` (코드·fixture·문서·테스트 함께 — Phase 3 Task 4 관례)
