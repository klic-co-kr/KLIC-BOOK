# 인포그래픽 레이어 Phase 1 (인프라 + flow) Implementation Plan — 개정 2판

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

> **개정 2판 (2026-08-22):** 초판 적대 검토 3관점(코드 실행 실증·스펙 충실성·실행가능성) 22건 반영. 주요 수정 — helper.typ 실측 결함 3건 교정(`pt()` 미정의·`place(center+horizon)` 앵커 오류·open-V 퇴화식), 배치 결정론에서 세로 모드 제거(판형 상한 테이블 + 2행 랩으로 전 판형 수학적 합법 — n=8 세로 571pt>한계 441pt 불가 실증), I1 9항목 완전 구현(커넥터 산술·판형 상한·펜스 위장 감지·미검증 비치명 경로), I1Error 생성자 순서·`sys.path` 명시·`_esc @<>` 확장·골든 확정 절차 신설·테스트 7건 정정.

**Goal:** korean-ebook-typst에 ```infographic 펜스 → Python 레이아웃 → typst 벡터 도식 → 책 PDF 삽입까지의 엔드투엔드 파이프라인을 flow archetype 1종으로 관통시킨다.

**Architecture:** md2typst가 펜스를 추출해 사이드 파일로 내보내고(본문에는 플레이스홀더 ⟦IG:N⟧), build.py가 style tokens와 함께 `scripts/infographic/`의 parse→layout→lint→emit을 호출해 `build/infographic/`에 .typ을 방출, 플레이스홀더를 `#include "../infographic/…"`로 치환한다. 좌표는 전부 Python이 계산하고 typst는 칠하기만 한다.

**Tech Stack:** Python 3 표준 라이브러리(re, yaml은 사용 금지 — 아래 Global Constraints), typst 0.15.1, pytest. 신규 외부 의존 0.

**Spec:** `docs/superpowers/specs/2026-08-21-infographic-layer-design.md` (개정 2판) — 실행자는 본 플랜과 스펙을 함께 읽는다. 스펙 §참조를 각 Task에 명시.

## Global Constraints

- 외부 의존 금지: Python 표준 라이브러리만. YAML 파싱에도 PyYAML을 쓰지 않는다 — 펜스 데이터는 **JSON 스키마**로 저작한다(아래 Task 2 근거). typst 패키지(@preview/*) 추가 금지.
- 결정론: 같은 펜스 입력 + 같은 tokens = 같은 방출 바이트(골든 스냅샷이 검증).
- emit은 색을 역할명으로만 참조하고 hex를 하드코딩하지 않는다(스펙 §4.2).
- 도식 텍스트 leading은 1.3em 고정 방출(스펙 §4.3).
- 도식 텍스트 크기는 본문 크기 ±0.3pt 밖이어야 한다(G3 불변식, 스펙 §5.2-9).
- 모든 I1 에러 메시지는 `챕터md #펜스순번 필드경로` 위치 + 측정값 + 저작자 레버 제안을 담는다(스펙 §5.2).
- 빌드 산물 `build/`·`draft/`는 gitignore에 이미 포함 — 커밋 금지.
- 테스트는 `skills/korean-ebook-typst/tests/` 아래. import는 기존 관례를 따른다: `tests/conftest.py`가 스킬 루트를 sys.path에 추가하므로 `from scripts.infographic.x import y` 형식이 그대로 동작한다(기존 `from scripts.build import …`와 동일 패턴, PEP420 네임스페이스).
- 저작 데이터는 JSON: 표준 라이브러리에 YAML 파서가 없어 PyYAML 의존이 강제된다. 의존 금지 원칙이 우선하므로 **펜스 언어는 `infographic`, 내용은 JSON**으로 확정한다(스펙 개정 3판이 §2·§3의 YAML 표기를 JSON으로 확정한다).
- typst 바이너리 탐지는 어디서든 `build.py:typst_binary()` 재사용으로 단일화한다(PATH → `~/.local/bin/typst` 폴백 — 임의 폴백 경로 중복 금지).
- 슬로우 테스트(subprocess 빌드·컴파일 포함)는 `subprocess.run(..., timeout=120)`을 명시한다.

---

### Task 1: tokens.json `infographic` 색 5역할 — 5팩 전부

**Files:**
- Modify: `skills/korean-ebook-typst/styles/{practical,essay,business,lecture,b5}/tokens.json`
- Create: `skills/korean-ebook-typst/scripts/infographic/__init__.py` (빈 패키지 마커)
- Create: `skills/korean-ebook-typst/scripts/infographic/roles.py`
- Test: `skills/korean-ebook-typst/tests/test_infographic_roles.py`

**Interfaces:**
- Produces: `roles.color(tokens: dict, role: str) -> str` — hex 문자열 반환. 역할 11종: `paper, ink, ink-soft, ink-mute, rule, accent, surface-tint, focus, positive, warning, on-focus`. 첫 6종은 `tokens["colors"]`, 후 5종은 `tokens["infographic"]`. 없는 역할이면 `KeyError`.
- Produces: `roles.REQUIRED_INFO_ROLES = ("surface-tint", "focus", "positive", "warning", "on-focus")`

팩별 5역할 값 — 각 팩 accent에서 유도(채도 절제, 스펙 §4.4):

| 팩 | surface-tint | focus | positive | warning | on-focus |
|---|---|---|---|---|---|
| practical | #EEF3F8 | #1F4E79 | #2E6E4E | #8A6D1F | #FFFFFF |
| essay | #F8F1ED | #A2604A | #2E6E4E | #8A6D1F | #FFFFFF |
| business | #EBEEF5 | #1F3864 | #2E6E4E | #8A6D1F | #FFFFFF |
| lecture | #EEF3F8 | #1F4E79 | #2E6E4E | #8A6D1F | #FFFFFF |
| b5 | #EEF3F8 | #1F4E79 | #2E6E4E | #8A6D1F | #FFFFFF |

- [ ] **Step 1: 실패 테스트 작성**

```python
"""test_infographic_roles.py — 스펙 §4.2: 5팩 모두 infographic 5역할 + roles.color 조회."""
import json
from pathlib import Path

import pytest

STYLES = Path(__file__).resolve().parents[1] / "styles"
PACKS = ["practical", "essay", "business", "lecture", "b5"]


def _tokens(pack: str) -> dict:
    return json.loads((STYLES / pack / "tokens.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("pack", PACKS)
def test_every_pack_has_five_info_roles(pack):
    info = _tokens(pack).get("infographic")
    assert isinstance(info, dict), f"{pack}: infographic 섹션 없음"
    for role in ("surface-tint", "focus", "positive", "warning", "on-focus"):
        v = info.get(role)
        assert isinstance(v, str) and v.startswith("#") and len(v) == 7, \
            f"{pack}.{role}: hex 6자리 필요, 값={v!r}"


def test_color_resolves_base_and_info_roles():
    from scripts.infographic import roles
    t = _tokens("practical")
    assert roles.color(t, "accent") == "#1F4E79"
    assert roles.color(t, "surface-tint") == "#EEF3F8"


def test_color_unknown_role_raises():
    from scripts.infographic import roles
    with pytest.raises(KeyError):
        roles.color(_tokens("practical"), "nope")
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `cd /mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook-typst && python3 -m pytest tests/test_infographic_roles.py -v`
Expected: FAIL — `infographic 섹션 없음`, `ModuleNotFoundError: scripts.infographic`

- [ ] **Step 3: 최소 구현**

`scripts/infographic/__init__.py`:

```python
"""인포그래픽 레이어 — 스펙 docs/superpowers/specs/2026-08-21-infographic-layer-design.md."""
```

`scripts/infographic/roles.py`:

```python
"""색 역할 조회(스펙 §4.2). emit·layout은 hex를 직접 다루지 않는다."""
REQUIRED_INFO_ROLES = ("surface-tint", "focus", "positive", "warning", "on-focus")


def color(tokens: dict, role: str) -> str:
    if role in tokens.get("colors", {}):
        return tokens["colors"][role]
    return tokens["infographic"][role]
```

각 팩 tokens.json — 최상위에 섹션 추가(들여쓰기 2칸, 파일 끝 `}` 앞, `colors` 뒤가 자연스러움):

```json
  "infographic": {
    "surface-tint": "#EEF3F8",
    "focus": "#1F4E79",
    "positive": "#2E6E4E",
    "warning": "#8A6D1F",
    "on-focus": "#FFFFFF"
  },
```

(값은 위 표의 팩별 값. essay는 surface-tint #F8F1ED, focus #A2604A / business는 #EBEEF5, #1F3864.)

- [ ] **Step 4: 테스트 통과 확인**

Run: `cd /mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook-typst && python3 -m pytest tests/test_infographic_roles.py -v`
Expected: 7 passed

- [ ] **Step 5: 기존 스모크 회귀**

Run: `cd /mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook-typst && python3 -m pytest tests/ -q`
Expected: 기존 전량 PASS (tokens.json 변경이 기존 빌드에 무영향인지 확인)

- [ ] **Step 6: 커밋**

```bash
git add skills/korean-ebook-typst/styles/*/tokens.json skills/korean-ebook-typst/scripts/infographic/ skills/korean-ebook-typst/tests/test_infographic_roles.py
git commit -m "feat: 인포그래픽 색 5역할 tokens 섹션 5팩 추가 + roles 조회"
```

---

### Task 2: parse.py — 펜스 JSON → 데이터 모델 + 상태 기계

**Files:**
- Create: `skills/korean-ebook-typst/scripts/infographic/parse.py`
- Test: `skills/korean-ebook-typst/tests/test_infographic_parse.py`

**Interfaces:**
- Consumes: 없음 (첫 순수 모듈)
- Produces:
  - `parse.Fence` frozen dataclass — 필드: `index:int`(1부터), `line:int`(펜스 시작 라인), `layout:str`(정규화 후 — Phase 1에선 "flow"), `title:str`, `thesis:str|None`, `kicker:str|None`, `note:str|None`, `evidence:str|None`, `data:dict`(archetype 페이로드)
  - `parse.ParseError(Exception)` — `.fence_index:int`, `.detail:str`
  - `parse.DEFAULT_NOTE = "편집 요약: 본문의 장·절 구조와 핵심 문장을 재배열한 도식이며, 원문을 대체하지 않습니다."` (스펙 §3.1 고정 원문)
  - `parse.parse_fence(index:int, line:int, body:str) -> Fence` — body는 펜스 내부 JSON 문자열. 거부: JSON 파싱 실패, layout 불명(별칭 제외), title 누락, steps 개수 2~8 밖, 빈 title/text. 별칭 수용(경고 아님 — 반환값에 `layout="flow"`로 정규화, `data["_alias"]`에 원래 값 기록): `process`→`flow`
  - `parse.normalize(text:str) -> str` — BOM 제거 + CRLF→LF
- Phase 1 layout은 `flow`만 유효(별칭 `process` 포함). 나머지 8종 키워드는 Task 수행 시점에 유효하지 않으므로 거부.

- [ ] **Step 1: 실패 테스트 작성**

```python
"""test_infographic_parse.py — 스펙 §3.1·§3.4 상태 기계."""
import pytest

from scripts.infographic.parse import (
    Fence, ParseError, parse_fence, normalize, DEFAULT_NOTE,
)

FLOW_BODY = """
{
  "layout": "flow",
  "title": "장애 대응은 접수에서 폐쇄까지 5단계로 수렴한다",
  "thesis": "대응 흐름을 단계화하면 인계 누락이 사라진다",
  "kicker": "CHAPTER MAP",
  "steps": [
    {"title": "접수", "text": "장애 접수 등록"},
    {"title": "분류", "text": "영향도 기반 분류"},
    {"title": "대응", "text": "임시 조치 시행"},
    {"title": "폐쇄", "text": "재발 방지 확정"}
  ]
}
"""


def test_valid_flow_fence():
    f = parse_fence(1, 10, FLOW_BODY)
    assert isinstance(f, Fence)
    assert f.layout == "flow"
    assert f.index == 1 and f.line == 10
    assert len(f.data["steps"]) == 4
    assert f.note is None           # 생략 시 None — emit이 DEFAULT_NOTE 사용
    assert f.evidence is None


def test_alias_process_normalized():
    f = parse_fence(2, 1, FLOW_BODY.replace('"flow"', '"process"'))
    assert f.layout == "flow"
    assert f.data["_alias"] == "process"


def test_note_and_evidence_kept():
    body = FLOW_BODY.replace('"kicker"', '"note": "커스텀 고지",\n  "evidence": "§2",\n  "kicker"')
    f = parse_fence(1, 1, body)
    assert f.note == "커스텀 고지" and f.evidence == "§2"


def test_invalid_json_rejected():
    with pytest.raises(ParseError) as e:
        parse_fence(1, 3, "{ not json")
    assert e.value.fence_index == 1
    assert "JSON" in e.value.detail or "json" in e.value.detail


def test_empty_fence_rejected_with_line():
    with pytest.raises(ParseError, match="빈 펜스") as e:
        parse_fence(2, 41, "   \n")
    assert e.value.line == 41


def test_unknown_layout_rejected():
    with pytest.raises(ParseError, match="(?i)layout"):
        parse_fence(1, 1, FLOW_BODY.replace('"flow"', '"railroad"'))


def test_missing_title_rejected():
    import json
    d = json.loads(FLOW_BODY); del d["title"]
    with pytest.raises(ParseError, match="(?i)title"):
        parse_fence(1, 1, json.dumps(d, ensure_ascii=False))


def test_step_count_bounds():
    import json
    d = json.loads(FLOW_BODY)
    d["steps"] = [{"title": "s", "text": "t"}]           # 1개 — 하한 위반
    with pytest.raises(ParseError, match="steps"):
        parse_fence(1, 1, json.dumps(d, ensure_ascii=False))
    d["steps"] = [{"title": f"s{i}", "text": "t"} for i in range(9)]  # 9개 — 상한
    with pytest.raises(ParseError, match="steps"):
        parse_fence(1, 1, json.dumps(d, ensure_ascii=False))


def test_empty_step_text_rejected():
    import json
    d = json.loads(FLOW_BODY)
    d["steps"][0]["text"] = "   "
    with pytest.raises(ParseError, match="steps\\[0\\]"):
        parse_fence(1, 1, json.dumps(d, ensure_ascii=False))


def test_normalize_strips_bom_and_crlf():
    assert normalize("﻿a\r\nb") == "a\nb"


def test_default_note_text_defined():
    assert "원문을 대체하지 않습니다" in DEFAULT_NOTE
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `cd /mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook-typst && python3 -m pytest tests/test_infographic_parse.py -v`
Expected: FAIL — `ModuleNotFoundError: ... parse`

- [ ] **Step 3: 최소 구현**

```python
"""parse.py — 펜스 JSON → Fence 모델 + 상태 기계(스펙 §3.1·§3.4). 표준 라이브러리만."""
from __future__ import annotations

import json
from dataclasses import dataclass

DEFAULT_NOTE = ("편집 요약: 본문의 장·절 구조와 핵심 문장을 재배열한 도식이며, "
                "원문을 대체하지 않습니다.")

# 스펙 §3.4 — 구시스템 별칭 → 규범 키워드
ALIASES = {"process": "flow"}
VALID_LAYOUTS = {"flow"}          # Phase 1. 이후 Task에서 확장
STEP_MIN, STEP_MAX = 2, 8


class ParseError(Exception):
    def __init__(self, fence_index: int, detail: str, line: int = 0):
        # 라인은 펜스 시작 라인 — 메시지에 포함해 저작자가 펜스를 바로 찾게 한다(§3.4).
        super().__init__(f"#{fence_index}(ch 라인 {line}): {detail}")
        self.fence_index = fence_index
        self.detail = detail
        self.line = line


@dataclass(frozen=True)
class Fence:
    index: int
    line: int
    layout: str
    title: str
    thesis: str | None
    kicker: str | None
    note: str | None
    evidence: str | None
    data: dict


def normalize(text: str) -> str:
    return text.replace("﻿", "").replace("\r\n", "\n").replace("\r", "\n")


def parse_fence(index: int, line: int, body: str) -> Fence:
    if not body.strip():
        raise ParseError(index, "빈 펜스 — layout·title·steps를 넣어라", line)
    try:
        d = json.loads(body)
        if not isinstance(d, dict):
            raise ValueError("펜스 내용이 JSON 객체가 아님")
    except ValueError as exc:
        raise ParseError(index, f"JSON 파싱 실패: {exc}", line) from exc

    raw_layout = str(d.get("layout", "")).strip()
    alias = raw_layout in ALIASES
    layout = ALIASES.get(raw_layout, raw_layout)
    if layout not in VALID_LAYOUTS:
        raise ParseError(index, f"unknown layout {raw_layout!r} (가능: flow)", line)

    title = str(d.get("title", "")).strip()
    if not title:
        raise ParseError(index, "title 필수 — 결론형 제목을 넣어라", line)

    def opt(key: str) -> str | None:
        v = d.get(key)
        return str(v).strip() if isinstance(v, str) and v.strip() else None

    data: dict = dict(steps=[])
    steps = d.get("steps", [])
    if not isinstance(steps, list) or not (STEP_MIN <= len(steps) <= STEP_MAX):
        raise ParseError(index, f"steps 개수 {len(steps) if isinstance(steps, list) else 0} — 하한 {STEP_MIN}, 상한 {STEP_MAX}", line)
    for i, s in enumerate(steps):
        if not isinstance(s, dict):
            raise ParseError(index, f"steps[{i}] 객체 아님", line)
        t = str(s.get("title", "")).strip()
        x = str(s.get("text", "")).strip()
        if not t or not x:
            raise ParseError(index, f"steps[{i}].title/.text 비어 있음 — 근거 문구를 넣어라", line)
        data["steps"].append({"title": t, "text": x})
    if alias:
        data["_alias"] = raw_layout

    return Fence(
        index=index, line=line, layout=layout, title=title,
        thesis=opt("thesis"), kicker=opt("kicker"),
        note=opt("note"), evidence=opt("evidence"), data=data,
    )
```

- [ ] **Step 4: 테스트 통과 확인**

Run: `cd /mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook-typst && python3 -m pytest tests/test_infographic_parse.py -v`
Expected: 10 passed

- [ ] **Step 5: 커밋**

```bash
git add skills/korean-ebook-typst/scripts/infographic/parse.py skills/korean-ebook-typst/tests/test_infographic_parse.py
git commit -m "feat: 인포그래픽 펜스 파서 — Fence 모델·별칭·상태 기계"
```

---

### Task 3: md2typst 펜스 추출 + `--fences-out` 사이드 파일

**Files:**
- Modify: `skills/korean-ebook-typst/scripts/md2typst.py` (convert에 추출 단계 삽입, CLI에 인자 추가)
- Test: `skills/korean-ebook-typst/tests/test_md2typst_fences.py`

**Interfaces:**
- Consumes: 기존 `md2typst.convert(md: str) -> str`, `stash_str` 클로저(15행)
- Produces:
  - `md2typst.extract_fences(md: str) -> tuple[str, list[dict]]` — 반환: (펜스가 마커로 치환된 md, `[{"index": 1, "line": 10, "body": "..."} ...]`). index는 1부터, line은 펜스 시작라인(1부터).
  - CLI: `--fences-out <path>` — 지정 시 챕터별 `<stem>.fences.json` 파일(`[{"index","line","body"} ...]`)로 저장. 미지정 시 기존 동작(펜스는 일반 코드펜스로 stash — 하위 호환).
  - 치환 마커: `⟦IG:N⟧` — convert 내부에서 stash_str()로 보호되어 step 6 이스케이프와 step 0.5 코드펜스 stash를 우회. 최종 .typ에는 `⟦IG:N⟧`만 남는다.
- 근거(스펙 §2 [1]): step 0.5가 모든 ``` 펜스를 원문 통째 stash하므로, infographic 펜스는 **step 0.5보다 먼저** 추출돼야 한다. 마커를 stash_str()에 넣는 이중 보호로 (a) step 6의 `#`→`\#` 이스케이프가 build.py 치환문 `#include`를 깨지 않게 한다(마커 자체엔 # 이 없지만 원문 펜스 재등장을 차단), (b) 펜스 원문이 .typ에 코드블록으로 인쇄되지 않게 한다.

- [ ] **Step 1: 실패 테스트 작성**

```python
"""test_md2typst_fences.py — 스펙 §2 [1]: 펜스 추출·마커 치환·사이드 파일."""
import json
import subprocess
import sys
from pathlib import Path

from scripts.md2typst import convert, extract_fences

MD = """# 서론

본문 문단이다. ```code``` 인라인도 있다.

```infographic
{"layout": "flow", "title": "결론 제목", "steps": [
  {"title": "접수", "text": "등록"},
  {"title": "폐쇄", "text": "확정"}
]}
```

뒤 본문.
"""


def test_extract_fences_returns_marker_and_payload():
    md2, fences = extract_fences(MD)
    assert len(fences) == 1
    assert fences[0]["index"] == 1
    assert fences[0]["line"] == 5                      # 1부터 시작 라인
    assert "flow" in fences[0]["body"]
    assert "⟦IG:1⟧" in md2
    assert '"layout"' not in md2                       # 원문 잔류 없음


def test_convert_leaves_marker_not_yaml():
    out = convert(MD)
    assert "⟦IG:1⟧" in out
    assert '"layout": "flow"' not in out               # YAML이 코드로 인쇄되지 않음
    assert "\\#include" not in out                     # 마커는 이스케이프 대상 아님


def test_code_fence_without_infographic_untouched():
    md2, fences = extract_fences("일반\n\n```\ncode block\n```\n")
    assert fences == []
    assert "```\ncode block\n```" == md2 or "code block" in md2


def test_cli_fences_out_sidecar(tmp_path):
    src = tmp_path / "ch01.md"
    src.write_text(MD, encoding="utf-8")
    out_dir = tmp_path / "typ"
    r = subprocess.run(
        [sys.executable, str(Path(__file__).resolve().parents[1] / "scripts" / "md2typst.py"),
         str(src), "--out", str(out_dir), "--fences-out", str(tmp_path / "fences")],
        capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    side = tmp_path / "fences" / "ch01.fences.json"
    data = json.loads(side.read_text(encoding="utf-8"))
    assert data[0]["index"] == 1 and "flow" in data[0]["body"]
    typ = out_dir / "ch01.typ"
    assert "⟦IG:1⟧" in typ.read_text(encoding="utf-8")
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `cd /mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook-typst && python3 -m pytest tests/test_md2typst_fences.py -v`
Expected: FAIL — `ImportError: cannot import name 'extract_fences'`

- [ ] **Step 3: 최소 구현**

`md2typst.py` — `convert` 함수 위에 신규 함수 추가:

```python
# 0.4 infographic 펜스 추출 — step 0.5(코드펜스 통째 stash)보다 먼저.
# 펜스 원문은 build.py가 render하고, 본문에는 마커 ⟦IG:N⟧만 남는다.
# 마커는 stash_str()에 넣어 이중 보호한다(스펙 §2 [1]).
IG_RE = re.compile(r'^```infographic[ \t]*\n(.*?)^```[ \t]*$', re.S | re.M)


def extract_fences(md: str) -> tuple[str, list[dict]]:
    fences = []
    def _take(m):
        fences.append({
            "index": len(fences) + 1,
            "line": md[:m.start()].count("\n") + 1,
            "body": m.group(1),
        })
        return f"\x01IG{len(fences)}\x01"        # 1차 마커 — 재매치 방지용 비가시 토큰
    md = IG_RE.sub(_take, md)
    return md, fences


def _restore_ig_markers(md: str, stash_str) -> str:
    # 1차 마커(\x01IGn\x01) → stash 보호된 가시 마커 ⟦IG:n⟧.
    return re.sub(r'\x01IG(\d+)\x01',
                  lambda m: stash_str(f"⟦IG:{m.group(1)}⟧"), md)
```

`convert` 내부 수정 — stash_str 정의 직후(현재 14~17행 뒤), frontmatter 제거(23행) **이전에** 삽입:

```python
    # -1. infographic 펜스 — 다른 어떤 변환보다 먼저(스펙 §2 [1]).
    md, _fences = extract_fences(md)
    md = _restore_ig_markers(md, stash_str)
```

(convert에서 펜스 페이로드는 폐기한다 — CLI가 extract_fences를 직접 호출해 사이드 파일을 쓴다. convert는 마커만 남긴다.)

`main()`의 argparse에 추가 후 저장 루프 수정:

```python
    ap.add_argument("--fences-out", default=None,
                    help="펜스 페이로드를 <stem>.fences.json으로 저장")
```

```python
    fences_dir = Path(a.fences_out) if a.fences_out else None
    if fences_dir:
        fences_dir.mkdir(parents=True, exist_ok=True)
    for md in targets:
        raw = md.read_text(encoding='utf-8')
        _, fences = extract_fences(raw)
        if fences_dir:
            (fences_dir / (md.stem + '.fences.json')).write_text(
                json.dumps(fences, ensure_ascii=False, indent=1), encoding='utf-8')
        t = convert(raw)
        (out / (md.stem + '.typ')).write_text(
            '#import "@preview/mitex:0.2.7": mitex\n\n' + t, encoding='utf-8')
        print(f'{md.name} → {md.stem}.typ')
```

`import json`을 상부 import에 추가한다. 위 루프가 기존 저장 루프를 그대로 대체한다(변경분: `raw` 변수·fences 추출·사이드 파일 기록).

- [ ] **Step 4: 테스트 통과 확인**

Run: `cd /mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook-typst && python3 -m pytest tests/test_md2typst_fences.py tests/ -q`
Expected: 전체 PASS (기존 md2typst 테스트 회귀 포함)

- [ ] **Step 5: 커밋**

```bash
git add skills/korean-ebook-typst/scripts/md2typst.py skills/korean-ebook-typst/tests/test_md2typst_fences.py
git commit -m "feat: md2typst infographic 펜스 추출 + --fences-out 사이드 파일"
```

---

### Task 4: budget.py — 텍스트 폭 예산 (근사 계수 + 10% 마진)

**Files:**
- Create: `skills/korean-ebook-typst/scripts/infographic/budget.py`
- Test: `skills/korean-ebook-typst/tests/test_infographic_budget.py`

**Interfaces:**
- Produces:
  - `budget.KO_UNIT = 1.0`, `budget.LATIN_UNIT = 0.55` (스펙 §4.3 — KO 1자 = size_pt, 라틴 = 0.55배)
  - `budget.width_units(text: str) -> float` — KO 문자(유니코드 분류: 한글 음절·자모) 1.0/자, 그 외(라틴·숫자·공백·기호) 0.55/자
  - `budget.MARGIN = 0.9` (10% 여유)
  - `budget.max_units(box_w: float, size_pt: float, pad: float = 8.0) -> float` — `(box_w − 2*pad) * MARGIN / size_pt`. 한 줄에 들어가는 width_units 상한.
  - `budget.line_count(text: str, box_w: float, size_pt: float, pad: float = 8.0) -> int` — 예상 줄 수(올림). 최소 1.

- [ ] **Step 1: 실패 테스트 작성**

```python
"""test_infographic_budget.py — 스펙 §4.3 근사 예산."""
import math

from scripts.infographic.budget import width_units, max_units, line_count


def test_ko_counts_full_latin_discounted():
    assert width_units("접수") == 2.0
    assert abs(width_units("AB") - 1.1) < 1e-9
    assert abs(width_units("eGovFrame") - 9 * 0.55) < 1e-9   # 9자 — 초판 8자 오기 정정
    assert abs(width_units("접수 AB") - (2.0 + 3 * 0.55)) < 1e-9


def test_max_units_formula():
    # box 120pt, size 9pt, pad 8: (120-16)*0.9/9 = 10.4 units
    assert abs(max_units(120.0, 9.0) - 10.4) < 1e-9


def test_line_count_rounds_up_min_one():
    assert line_count("접수등록", 120.0, 9.0) == 1          # 4.0 ≤ 10.4
    assert line_count("접수" * 12, 120.0, 9.0) == 3        # 24.0/10.4 = 2.31 → 3
    assert line_count("한", 15.0, 9.0) == 1                # cap=(15-16)*0.9/9 ≤ 0 → 클램프 1
                                                           # (20pt면 cap=0.4>0이라 3이 된다 — 초판 오기 정정)
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `cd /mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook-typst && python3 -m pytest tests/test_infographic_budget.py -v`
Expected: FAIL — ModuleNotFoundError

- [ ] **Step 3: 최소 구현**

```python
"""budget.py — 텍스트 폭 예산(스펙 §4.3). 폰트 메트릭 없는 근사: KO=1.0, 라틴=0.55, 10% 마진.
팩별 보정 계수: 1순위 폰트가 팩마다 다르므로(§4.1) 단일 전역표를 쓰지 않는다.
초기값은 전 팩 1.0 — 골든 교정 절차(Task 11, 스펙 §7)로 팩별 실측값을 갱신한다."""
from __future__ import annotations

import math
import unicodedata

KO_UNIT = 1.0
LATIN_UNIT = 0.55
MARGIN = 0.9
DEFAULT_PAD = 8.0

# 팩별 KO 보정 계수 — 골든 교정(각 팩 1순위 폰트로 fixture 카드 오버플로 한계 실측)으로 갱신.
PACK_KO_FACTOR = {"practical": 1.0, "essay": 1.0, "business": 1.0,
                  "lecture": 1.0, "b5": 1.0}


def width_units(text: str, pack: str = "practical") -> float:
    f = PACK_KO_FACTOR.get(pack, 1.0)
    units = 0.0
    for ch in text:
        name = unicodedata.name(ch, "")
        ko = "HANGUL" in name or "CJK" in name or "FULLWIDTH" in name
        units += (KO_UNIT * f) if ko else LATIN_UNIT
    return units


def max_units(box_w: float, size_pt: float, pad: float = DEFAULT_PAD) -> float:
    return (box_w - 2 * pad) * MARGIN / size_pt


def line_count(text: str, box_w: float, size_pt: float, pad: float = DEFAULT_PAD,
               pack: str = "practical") -> int:
    cap = max_units(box_w, size_pt, pad)
    if cap <= 0:
        return 1
    return max(1, math.ceil(width_units(text, pack) / cap))
```

- [ ] **Step 4: 테스트 통과 확인**

Run: `cd /mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook-typst && python3 -m pytest tests/test_infographic_budget.py -v`
Expected: 3 passed

- [ ] **Step 5: 커밋**

```bash
git add skills/korean-ebook-typst/scripts/infographic/budget.py skills/korean-ebook-typst/tests/test_infographic_budget.py
git commit -m "feat: 인포그래픽 텍스트 예산 — KO/라틴 계수·10% 마진"
```

---

### Task 5: layout flow — 좌표 모델 + 배치 결정론 + 잉크 bbox

**Files:**
- Create: `skills/korean-ebook-typst/scripts/infographic/model.py` (ops 자료구조)
- Create: `skills/korean-ebook-typst/scripts/infographic/layout.py`
- Create: `skills/korean-ebook-typst/scripts/infographic/archetypes/__init__.py`
- Create: `skills/korean-ebook-typst/scripts/infographic/archetypes/flow.py`
- Test: `skills/korean-ebook-typst/tests/test_infographic_layout_flow.py`

**Interfaces:**
- Consumes: `parse.Fence`, `budget.line_count/width_units`, tokens 구조(`body_frame_pt`, `fonts.*.size_pt`, `style`)
- Produces (model.py — 이후 모든 archetype이 공유):
  - `model.RectOp(x, y, w, h, rx: float, fill_role: str, stroke_role: str, stroke_w: float)` frozen
  - `model.TextOp(x, y, size, text, role: str, weight: str = "regular", max_w: float = 0.0, field: str = "")` frozen — `x,y`는 텍스트 블록 **중심점**(절대좌표), `max_w`는 예산 검증용 상자 폭(0=검사 없음), `field`는 I1 위치 계약용 필드 경로(예: `steps[1].title` — lint loc가 이 값을 쓴다)
  - `model.ArrowOp(x1, y1, x2, y2, style: str)` frozen — style "solid"|"dashed". 헤드는 emit이 x2,y2에 open-V로 그린다.
  - `model.FigModel(width: float, height: float, ops: tuple, source_index: int)` frozen — ops는 RectOp/TextOp/ArrowOp 혼합 튜플. (초판의 `source: Fence` 필드 표기는 오류이다 — 구현·테스트 전부 `source_index: int`.)
  - `model.ARROW_STROKE_W = 1.2`, `model.ARROW_HEAD_W = 4.0` (비율 4.0/1.2 = 3.33 — 스펙 §5.2-4 허용 범위 2.5~3.5 안)
- Produces (archetypes/flow.py):
  - `flow.layout(fence: Fence, tokens: dict) -> FigModel` — 스펙 §6.3 flow 배치. 예외: `flow.FlowLayoutError(Exception)` — `.detail:str` (판형 상한·높이 85% 초과 등 — render가 LintFinding으로 변환해 I1 리포트에 합류)
  - `flow.PACK_LIMITS = {"essay": 4, "practical": 6, "b5": 6, "business": 8, "lecture": 8}` — 스펙 §6.2 flow 행. **layout이 이 표를 초과하면 즉시 FlowLayoutError**(스펙 "이 표를 초과하면 I1 에러"의 구현 지점).
- Produces (layout.py):
  - `layout.dispatch(fence, tokens) -> FigModel` — `fence.layout`으로 archetype 함수 라우팅. Phase 1: flow만.
- 배치 상수(전 팩 공통): 패널 패딩 `P=14`, 카드 간격 `G=28`(가로·랩 공용), 카드 내부 패딩 8, 최소 카드폭 `MIN_CARD_W=80`, 카드 수직 패딩 10, 제목→카드 간 18. (초판의 세로 전용 간격 GV=16·세로 모드는 **삭제** — 근거: n=8 세로 배치 높이 571pt > 한계 441pt로 수학적 불가 실증, GV=16 복도에선 샤프트 가시 8pt < 12pt로 스펙 §6.1 위반.)
- 배치 결정론(스펙 §6.2 개정 — 선택 재량 없음, 세로 없음):
  1. `n = len(steps)`; `pack = tokens["style"]`; `n > PACK_LIMITS[pack]`면 **FlowLayoutError**(`steps {n}개 > 판형 상한 {limit}({pack}) — 요소 수 감소 또는 펜스 분할`)
  2. 가로 1행: `cardW = (W − 2P − (n−1)·G)/n`; `cardW ≥ MIN_CARD_W`면 **가로**
  3. 아니면 2행 랩: `cols = ceil(n/2)`; `cardW = (W − 2P − (cols−1)·G)/cols`; `cardW ≥ MIN_CARD_W`면 **랩**
  4. 아니면 **FlowLayoutError**(공간 부족 — 문구 축약/분할 레버)
  - 수학 검증(MIN_CARD_W=80, 판형 상한 내 모든 n이 ②또는③에 합법): essay n=4 → 랩 2열 96.7pt ✓ · practical n=6 → 랩 3열 83.5pt ✓ · b5 n=6 → 랩 3열 100.5pt ✓ · business n=8 → 랩 4열 85.4pt ✓ · lecture n=8 → 랩 4열 88.2pt ✓. n=3 practical은 가로 83.5pt ✓.
- 세로 산술: 도식 제목 블록(kicker/label 크기 + title/heading2 크기 + thesis/본문−1 크기, 각 줄 `size×1.3` + 블록 여백) → 카드(내부: title `본문+1` ×줄수, gap 4, text `본문−1` ×줄수, 상하 패딩 10) → note(본문−1, 1줄). `height > (body_frame 높이)×0.85`면 FlowLayoutError.
- 잉크 bbox(스펙 §5.2-3): `flow.layout`이 모든 RectOp/ArrowOp에 대해 `x−stroke_w/2 ≥ 0`, `x+w+stroke_w/2 ≤ W`, `y−stroke_w/2 ≥ 0`, `y+h+stroke_w/2 ≤ height`를 산출 시점에 보장 — 위반이면 FlowLayoutError(레이아웃 버그 방어).
- 텍스트 크기(스펙 §4.3, tokens에서 도출): `title = fonts.heading2.size_pt`, `card_title = body+1`, `card_text = body−1`, `kicker/caption = fonts.label.size_pt`. G3 불변식: `card_title`·`card_text`·`title`·`kicker` 모두 `abs(size − body) > 0.3`이어야 함(essay는 heading2가 10pt=body라 **title은 예외 — essay 한정 title 크기를 body+1.5로 대체**하고 나머지는 동일).

- [ ] **Step 1: 실패 테스트 작성**

```python
"""test_infographic_layout_flow.py — 스펙 §6.2·§6.3 flow 지오메트리·결정론·잉크 bbox."""
import json
from pathlib import Path

import pytest

from scripts.infographic.archetypes import flow as flow_arch
from scripts.infographic.model import FigModel, RectOp, TextOp
from scripts.infographic.parse import parse_fence

TOKENS = json.loads((Path(__file__).resolve().parents[1] / "styles" / "practical" / "tokens.json").read_text(encoding="utf-8"))
W = TOKENS["body_frame_pt"]["x1"] - TOKENS["body_frame_pt"]["x0"]   # 334.49
H = TOKENS["body_frame_pt"]["y1"] - TOKENS["body_frame_pt"]["y0"]
P, G, MIN_CARD = 14.0, 28.0, 80.0


def _fence(n_steps: int, title: str = "결론 제목", text: str = "근거 문장"):
    body = json.dumps({
        "layout": "flow", "title": title,
        "steps": [{"title": f"단계 {i+1}", "text": text} for i in range(n_steps)],
    }, ensure_ascii=False)
    return parse_fence(1, 1, body)


def test_two_steps_horizontal():
    fig = flow_arch.layout(_fence(2), TOKENS)
    rects = [o for o in fig.ops if isinstance(o, RectOp)]
    cards = [r for r in rects if r.fill_role == "surface-tint"]
    assert len(cards) == 2
    expect = (W - 2 * P - G) / 2
    assert abs(cards[0].w - expect) < 0.01
    assert abs(cards[1].x - (P + expect + G)) < 0.01


def test_four_steps_wraps_to_2x2():
    fig = flow_arch.layout(_fence(4), TOKENS)
    cards = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
    assert len(cards) == 4
    expect = (W - 2 * P - G) / 2                      # 2열
    assert abs(cards[0].w - expect) < 0.01
    ys = {round(r.y, 2) for r in cards}
    assert len(ys) == 2                               # 2행


def test_eight_steps_pack_limit_error():
    # practical 판형 상한 6 — n=8은 지오메트리 전에 판형 상한 위반 에러
    with pytest.raises(flow_arch.FlowLayoutError, match="판형 상한"):
        flow_arch.layout(_fence(8), TOKENS)


def test_eight_steps_business_wraps_four_cols():
    # business(453.55pt)는 상한 8 — 4열 랩: (453.55-28-84)/4 = 85.4pt ≥ 80
    BTOKENS = json.loads((Path(__file__).resolve().parents[1] / "styles" / "business"
                          / "tokens.json").read_text(encoding="utf-8"))
    fig = flow_arch.layout(_fence(8), BTOKENS)
    cards = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
    assert len(cards) == 8
    expect = (BTOKENS["body_frame_pt"]["x1"] - BTOKENS["body_frame_pt"]["x0"] - 2 * P - 3 * G) / 4
    assert abs(cards[0].w - expect) < 0.01
    assert len({round(r.y, 2) for r in cards}) == 2   # 2행


def test_six_steps_wrap_three_cols():
    # practical n=6: 가로 27.7pt ✗ → 랩 3열 (334.49-28-56)/3 = 83.5pt ≥ 80
    fig = flow_arch.layout(_fence(6), TOKENS)
    cards = [r for r in fig.ops if isinstance(r, RectOp) and r.fill_role == "surface-tint"]
    assert len(cards) == 6
    assert abs(cards[0].w - (W - 2 * P - 2 * G) / 3) < 0.01


def test_ink_containment_guaranteed():
    for n in (2, 3, 4, 5, 6):
        fig = flow_arch.layout(_fence(n), TOKENS)
        for o in fig.ops:
            if isinstance(o, RectOp):
                assert o.x - o.stroke_w / 2 >= -0.001, f"n={n}"
                assert o.x + o.w + o.stroke_w / 2 <= fig.width + 0.001, f"n={n}"
                assert o.y - o.stroke_w / 2 >= -0.001, f"n={n}"
                assert o.y + o.h + o.stroke_w / 2 <= fig.height + 0.001, f"n={n}"


def test_g3_invariant_sizes_off_body():
    body = TOKENS["fonts"]["body"]["size_pt"]
    fig = flow_arch.layout(_fence(3), TOKENS)
    texts = [o for o in fig.ops if isinstance(o, TextOp) and o.size != body]
    assert texts                                   # 도식 텍스트 존재
    for o in texts:
        assert abs(o.size - body) > 0.3, o.size    # 본문 크기와 0.3pt 이상 차이


def test_height_limit_85pct():
    # n=6(상한 내) + 장문 — 카드 줄수 폭증으로 높이 한계 초과 (n=8은 판형 상한 에러가 먼저)
    long_text = "아주 긴 근거 문장이다 " * 8
    with pytest.raises(flow_arch.FlowLayoutError, match="85"):
        flow_arch.layout(_fence(6, text=long_text), TOKENS)


def test_figmodel_is_frozen_deterministic():
    f1 = flow_arch.layout(_fence(5), TOKENS)
    f2 = flow_arch.layout(_fence(5), TOKENS)
    assert f1 == f2                                 # 결정론 — 같은 입력 같은 모델
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `cd /mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook-typst && python3 -m pytest tests/test_infographic_layout_flow.py -v`
Expected: FAIL — ModuleNotFoundError

- [ ] **Step 3: 최소 구현**

`model.py`:

```python
"""model.py — 도식 draw ops(스펙 §2). emit은 이 ops만 소비한다."""
from __future__ import annotations

from dataclasses import dataclass

ARROW_STROKE_W = 1.2
ARROW_HEAD_W = 4.0          # /1.2 = 3.33 — §5.2-4 허용 2.5~3.5


@dataclass(frozen=True)
class RectOp:
    x: float; y: float; w: float; h: float
    rx: float = 8.0
    fill_role: str = "surface-tint"
    stroke_role: str = "rule"
    stroke_w: float = 0.5


@dataclass(frozen=True)
class TextOp:
    x: float; y: float          # 텍스트 블록 중심점(절대좌표)
    size: float
    text: str
    role: str = "ink"
    weight: str = "regular"
    max_w: float = 0.0          # 예산 검사용 상자 폭(0=검사 생략)
    field: str = ""             # I1 위치 계약용 필드 경로(예: steps[1].title)


@dataclass(frozen=True)
class ArrowOp:
    x1: float; y1: float; x2: float; y2: float
    style: str = "solid"        # solid=순차, dashed=참조(§6.1)


@dataclass(frozen=True)
class FigModel:
    width: float
    height: float
    ops: tuple
    source_index: int           # 펜스 순번 — lint 위치 표기용
```

`archetypes/flow.py`:

```python
"""flow — 순차 단계 배치(스펙 §6.2·§6.3). 결정론: 가로→랩→세로 우선순위 고정."""
from __future__ import annotations

import math

from .. import budget
from ..model import ArrowOp, FigModel, RectOp, TextOp

P = 14.0          # 패널 패딩
G = 28.0          # 카드 간격(가로·랩 공용)
MIN_CARD_W = 80.0
CARD_PAD_IN = 8.0
CARD_PAD_V = 10.0
LEADING = 1.3
HEIGHT_LIMIT = 0.85

# 스펙 §6.2 flow 행 — 판형 조건부 상한. layout이 초과하면 즉시 에러(I1 리포트 합류).
PACK_LIMITS = {"essay": 4, "practical": 6, "b5": 6, "business": 8, "lecture": 8}


class FlowLayoutError(Exception):
    def __init__(self, detail: str):
        super().__init__(detail)
        self.detail = detail


def _ink_ok(ops, width: float, height: float) -> None:
    for o in ops:
        if isinstance(o, RectOp):
            if (o.x - o.stroke_w / 2 < -0.001 or o.x + o.w + o.stroke_w / 2 > width + 0.001
                    or o.y - o.stroke_w / 2 < -0.001 or o.y + o.h + o.stroke_w / 2 > height + 0.001):
                raise FlowLayoutError(f"잉크 bbox 프레임 이탈: rect({o.x:.1f},{o.y:.1f},{o.w:.1f},{o.h:.1f})")


def layout(fence, tokens: dict) -> FigModel:
    frame = tokens["body_frame_pt"]
    W = frame["x1"] - frame["x0"]
    H_frame = frame["y1"] - frame["y0"]
    f = tokens["fonts"]
    body = f["body"]["size_pt"]
    # G3 불변식(§5.2-9): 본문±0.3pt 밖. essay처럼 heading2==body인 팩은 +1.5로 밀어낸다.
    title_size = f["heading2"]["size_pt"]
    if abs(title_size - body) <= 0.3:
        title_size = body + 1.5
    kicker_size = f["label"]["size_pt"]
    card_title_size = body + 1
    card_text_size = body - 1

    steps = fence.data["steps"]
    n = len(steps)

    # 배치 결정론(§6.2 개정) — 판형 상한 → 가로 → 2행 랩 → 에러. 세로 모드 없음.
    pack = tokens.get("style", "practical")
    limit = PACK_LIMITS.get(pack)
    if limit is None:
        raise FlowLayoutError(f"알 수 없는 스타일 팩 {pack!r} — tokens.style 확인")
    if n > limit:
        raise FlowLayoutError(
            f"steps {n}개 > 판형 상한 {limit}({pack}) — 요소 수 감소 또는 펜스 분할")
    mode = None
    cardW = 0.0
    cols = n
    cardW_h = (W - 2 * P - (n - 1) * G) / n
    if cardW_h >= MIN_CARD_W:
        mode, cardW = "h", cardW_h
    else:
        cols = math.ceil(n / 2)
        cardW_w = (W - 2 * P - (cols - 1) * G) / cols
        if cardW_w >= MIN_CARD_W:
            mode, cardW = "wrap", cardW_w
        else:
            raise FlowLayoutError(
                f"steps {n}개를 {pack} 판형에 배치 불가(랩 후 카드폭 {cardW_w:.1f}pt < "
                f"{MIN_CARD_W:.0f}pt) — 글자 축약, 요소 수 감소 또는 펜스 분할")

    def card_h(step: dict) -> float:
        t_lines = budget.line_count(step["title"], cardW, card_title_size, CARD_PAD_IN, pack)
        x_lines = budget.line_count(step["text"], cardW, card_text_size, CARD_PAD_IN, pack)
        return 2 * CARD_PAD_V + t_lines * card_title_size * LEADING + 4.0 + x_lines * card_text_size * LEADING

    # 헤더 블록
    header_h = 0.0
    texts: list[TextOp] = []
    if fence.kicker:
        header_h += kicker_size * LEADING
    t_lines = budget.line_count(fence.title, W - 2 * P, title_size, 0.0, pack)
    header_h += t_lines * title_size * LEADING
    if fence.thesis:
        header_h += budget.line_count(fence.thesis, W - 2 * P, card_text_size, 0.0, pack) * card_text_size * LEADING
    header_h += 18.0                                # 제목→카드 간

    ops: list = []
    y = 0.0
    cy = 0.0
    if fence.kicker:
        texts.append(TextOp(x=W / 2, y=cy + kicker_size * LEADING / 2, size=kicker_size,
                            text=fence.kicker, role="ink-mute", field="kicker"))
        cy += kicker_size * LEADING
    texts.append(TextOp(x=W / 2, y=cy + t_lines * title_size * LEADING / 2, size=title_size,
                        text=fence.title, role="ink", weight="bold", max_w=W - 2 * P,
                        field="title"))
    cy += t_lines * title_size * LEADING
    if fence.thesis:
        th_lines = budget.line_count(fence.thesis, W - 2 * P, card_text_size, 0.0, pack)
        texts.append(TextOp(x=W / 2, y=cy + th_lines * card_text_size * LEADING / 2,
                            size=card_text_size, text=fence.thesis, role="ink-soft",
                            max_w=W - 2 * P, field="thesis"))
        cy += th_lines * card_text_size * LEADING
    y = cy + 18.0

    cards: list[RectOp] = []
    arrows: list[ArrowOp] = []
    if mode == "h":
        ch = max(card_h(s) for s in steps)
        for i, s in enumerate(steps):
            cx = P + i * (cardW + G)
            cards.append(RectOp(x=cx, y=y, w=cardW, h=ch))
            _card_texts(texts, s, cx, y, cardW, ch, card_title_size, card_text_size, i, pack)
            if i:
                prev_x = P + (i - 1) * (cardW + G)
                arrows.append(_harrow(prev_x + cardW, y + ch / 2, cx))
        y += ch
    elif mode == "wrap":
        rows = [steps[i:i + cols] for i in range(0, n, cols)]
        row_h = [max(card_h(s) for s in row) for row in rows]
        for r, row in enumerate(rows):
            ry = y + sum(row_h[:r]) + G * r
            for j, s in enumerate(row):
                cx = P + j * (cardW + G)
                cards.append(RectOp(x=cx, y=ry, w=cardW, h=row_h[r]))
                _card_texts(texts, s, cx, ry, cardW, row_h[r], card_title_size,
                            card_text_size, r * cols + j, pack)
                if j:
                    prev_x = P + (j - 1) * (cardW + G)
                    arrows.append(_harrow(prev_x + cardW, ry + row_h[r] / 2, cx))
        y = y + sum(row_h) + G * (len(rows) - 1)

    y += 12.0
    from ..parse import DEFAULT_NOTE
    note = fence.note or DEFAULT_NOTE
    texts.append(TextOp(x=W / 2, y=y + card_text_size * LEADING / 2, size=card_text_size,
                        text=note, role="ink-mute", max_w=W - 2 * P, field="note"))
    y += card_text_size * LEADING

    if y > H_frame * HEIGHT_LIMIT:
        raise FlowLayoutError(
            f"도식 높이 {y:.0f}pt > 프레임 {H_frame * HEIGHT_LIMIT:.0f}pt(85%) — "
            f"steps {n}개를 줄이거나(현재 {n}), 문구를 축약하거나, 도식을 2개 펜스로 분할")

    ops = [RectOp(x=0.0, y=0.0, w=W, h=y, rx=0.0, fill_role="paper", stroke_role="rule", stroke_w=0.0),
           *cards, *arrows, *texts]
    _ink_ok(ops, W, y)
    return FigModel(width=W, height=y, ops=tuple(ops), source_index=fence.index)


def _card_texts(out: list, s: dict, cx: float, cy: float, cw: float, ch: float,
                t_size: float, x_size: float, idx: int, pack: str) -> None:
    t_lines = budget.line_count(s["title"], cw, t_size, pack=pack)
    x_lines = budget.line_count(s["text"], cw, x_size, pack=pack)
    block = t_lines * t_size * LEADING + 4.0 + x_lines * x_size * LEADING
    top = cy + (ch - block) / 2
    out.append(TextOp(x=cx + cw / 2, y=top + t_lines * t_size * LEADING / 2, size=t_size,
                      text=s["title"], role="ink", weight="bold", max_w=cw,
                      field=f"steps[{idx}].title"))
    mid = top + t_lines * t_size * LEADING + 4.0
    out.append(TextOp(x=cx + cw / 2, y=mid + x_lines * x_size * LEADING / 2, size=x_size,
                      text=s["text"], role="ink-soft", max_w=cw, field=f"steps[{idx}].text"))


def _harrow(right_edge: float, ymid: float, next_left: float) -> ArrowOp:
    # 복도 G=28: shaft 길이 16(≥12), tip이 목표 박스 8pt 전에 착지(§6.1)
    return ArrowOp(x1=right_edge + 4.0, y1=ymid, x2=next_left - 8.0, y2=ymid)
```

`layout.py`:

```python
"""layout.py — archetype 라우팅(스펙 §2 원칙 3: 빌드 자동판단 없음, fence.layout 명시만)."""
from __future__ import annotations

from .archetypes import flow as _flow
from .parse import Fence


def dispatch(fence: Fence, tokens: dict):
    if fence.layout == "flow":
        return _flow.layout(fence, tokens)
    raise ValueError(f"지원하지 않는 layout: {fence.layout!r}")
```

`archetypes/__init__.py`는 빈 패키지 마커(`"""archetype별 배치 산술."""` 한 줄).

주의: `_card_texts`의 TextOp y좌표는 텍스트 **블록 중심**이고, title/text 세로 정렬은 위 구현의 블록 중심 배치를 따른다. emit이 이 좌표를 typst `place(dx, dy)` + `align(center + horizon)`로 소비한다(Task 7).

- [ ] **Step 4: 테스트 통과 확인**

Run: `cd /mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook-typst && python3 -m pytest tests/test_infographic_layout_flow.py -v`
Expected: 9 passed

- [ ] **Step 5: 커밋**

```bash
git add skills/korean-ebook-typst/scripts/infographic/ skills/korean-ebook-typst/tests/test_infographic_layout_flow.py
git commit -m "feat: flow archetype 배치 — 결정론(가로→랩→세로)·잉크 bbox·G3 불변식"
```

---

### Task 6: emit.py + helper.typ — FigModel → typst (골든 스냅샷)

**Files:**
- Create: `skills/korean-ebook-typst/scripts/infographic/emit.py`
- Create: `skills/korean-ebook-typst/templates/infographic/helper.typ`
- Test: `skills/korean-ebook-typst/tests/test_infographic_emit.py`
- Create: `skills/korean-ebook-typst/tests/fixtures/infographic/golden-flow-practical.typ` (골든)

**Interfaces:**
- Consumes: `model.FigModel/RectOp/TextOp/ArrowOp`, tokens 구조
- Produces:
  - `emit.render_typ(fig: FigModel, tokens: dict) -> str` — 완전한 .typ 파일 내용(헬퍼 import 포함). 결정론: 입력 같으면 바이트 동일.
  - `helper.typ`의 공개 함수: `ig-color(role)`, `ig-text(size, role, weight, body)`, `ig-rect(x, y, w, h, rx, fill-role, stroke-role, stroke-w)`, `ig-arrow(x1, y1, x2, y2, style)`, `ig-figure(w, h, body)` — 전부 `tokens.json`을 읽는 `#let tokens = json("tokens.json")` 기반.
- emit 방출 계약(스펙 §5.1 래퍼):
  - 최외곽: `#ig-figure(width, height)[…ops…]` — helper의 `ig-figure`가 `block(breakable: false, width, clip: true)` + 내부 `place` 좌표계(좌상단 원점)를 제공.
  - 모든 텍스트: `text(size: …, leading 1.3em)` — helper `ig-text`가 `set par(leading: 1.3em)` 스코프 적용(본문 1.7em 상속 차단, 스펙 §4.3).
  - 화살표: shaft `line(stroke: 1.2pt)` + 목표端 open-V 두 `line`(헤드 폭 4pt, ARROW_HEAD_W) + tip-gap은 layout이 이미 좌표에 반영.
- 숫자 포맷: 좌표·크기는 소수 2자리 반올림(`f"{v:.2f}"`) — 골든 안정성.

- [ ] **Step 1: 실패 테스트 작성**

```python
"""test_infographic_emit.py — 방출 결정론·래퍼 계약·골든 스냅샷."""
import json
from pathlib import Path

import pytest

from scripts.infographic.archetypes import flow as flow_arch
from scripts.infographic.emit import render_typ
from scripts.infographic.parse import parse_fence

SKILL = Path(__file__).resolve().parents[1]
TOKENS = json.loads((SKILL / "styles" / "practical" / "tokens.json").read_text(encoding="utf-8"))
GOLDEN = SKILL / "tests" / "fixtures" / "infographic" / "golden-flow-practical.typ"

FENCE = parse_fence(1, 1, json.dumps({
    "layout": "flow", "title": "장애 대응은 5단계로 수렴한다",
    "steps": [
        {"title": "접수", "text": "장애 접수 등록"},
        {"title": "분류", "text": "영향도 기반 분류"},
    ],
}, ensure_ascii=False))


def test_emit_calls_helpers_no_hex():
    out = render_typ(flow_arch.layout(FENCE, TOKENS), TOKENS)
    assert '#import "../helper.typ"' in out          # fig는 build/infographic/에 있다(§2)
    assert "#ig-figure(" in out and "#ig-text(" in out
    assert "#EEF3F8" not in out and "#1F4E79" not in out   # hex 금지(§4.2) — 역할명만


def test_helper_has_wrapper_and_leading_contract():
    # 래퍼·leading 계약은 방출물이 아니라 helper.typ에 산다 — 파일 자체를 검사한다
    # (초판은 방출물에서 이 문자열을 찾아 절대 통과 불가였다 — 실증 정정).
    helper = (SKILL / "templates" / "infographic" / "helper.typ").read_text(encoding="utf-8")
    assert "breakable: false" in helper              # §5.1 래퍼
    assert "1.3em" in helper                         # §4.3 leading
    assert "#let pt(n) = n * 1pt" in helper          # pt 셈 — typst 0.15.1에 내장 없음(실증)


def test_emit_deterministic_bytes():
    a = render_typ(flow_arch.layout(FENCE, TOKENS), TOKENS)
    b = render_typ(flow_arch.layout(FENCE, TOKENS), TOKENS)
    assert a == b


def test_golden_snapshot():
    out = render_typ(flow_arch.layout(FENCE, TOKENS), TOKENS)
    if not GOLDEN.exists():
        # 골든은 테스트가 스스로 굳히지 않는다(자기충족 안티패턴 — 적대 검토 지적).
        # 확정 절차: IG_REGEN_GOLDEN=1으로 생성 → 눈검 → 함께 커밋. 그 전엔 실패.
        import os
        if os.environ.get("IG_REGEN_GOLDEN") != "1":
            pytest.fail("골든 없음 — `IG_REGEN_GOLDEN=1 python3 -m pytest …` 실행 후 "
                        "생성 파일을 눈검하고 커밋하라")
        GOLDEN.parent.mkdir(parents=True, exist_ok=True)
        GOLDEN.write_text(out, encoding="utf-8")
    assert out == GOLDEN.read_text(encoding="utf-8")
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `cd /mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook-typst && python3 -m pytest tests/test_infographic_emit.py -v`
Expected: FAIL — ModuleNotFoundError emit

- [ ] **Step 3: 최소 구현**

`templates/infographic/helper.typ`:

```typst
// templates/infographic/helper.typ — 인포그래픽 공통 프리미티브(스펙 §4.2·§5.1).
// 색은 역할명만 받는다. hex는 tokens.json이 SSoT.
// 검증 이력(적대 검토 실측): pt() 셤·place 앵커 절대좌표 환산·open-V 절대 대각선 —
// typst 0.15.1 실컴파일 + PyMuPDF 좌표 실측으로 교정된 형태다. 임의 수정 금지.
#let tokens = json("tokens.json")
#let pt(n) = n * 1pt

#let ig-color(role) = {
  if tokens.colors.at(role, default: none) != none { rgb(tokens.colors.at(role)) }
  else { rgb(tokens.infographic.at(role)) }
}

#let ig-figure(w, h, body) = block(
  width: pt(w), height: pt(h), breakable: false, clip: true,
  stroke: none, inset: 0pt,
)[#box(width: 100%, height: 100%)[#body]]

// rect — place(top+left)는 박스 좌상단을 (x,y)에 놓는다(실측 정확).
#let ig-rect(x, y, w, h, rx: 8pt, fill-role: "surface-tint",
             stroke-role: "rule", stroke-w: 0.5pt) = place(
  top + left, dx: pt(x), dy: pt(y),
  rect(width: pt(w), height: pt(h), radius: rx,
       fill: ig-color(fill-role),
       stroke: if stroke-w == 0pt { none } else {
         (paint: ig-color(stroke-role), thickness: stroke-w) }),
)

// text — x,y는 텍스트 블록 중심의 절대좌표, fw·fh는 도식 전체 폭·높이.
// place(center+horizon)는 "컨테이너 중심 + (dx,dy)"에 블록 중심을 놓는다(실측:
// raw dx 전달 시 전 텍스트가 (+W/2, +H/2) 치우침). 절대좌표 (x,y)에 놓으려면
// dx = x − fw/2, dy = y − fh/2 를 전달해야 한다 — emit이 항상 이 환산을 수행한다.
#let ig-text(x, y, fw, fh, size, role, weight: "regular", body) = place(
  center + horizon, dx: pt(x - fw / 2), dy: pt(y - fh / 2),
  box(inset: 0pt)[#set par(leading: 1.3em)
    #text(size: pt(size), fill: ig-color(role),
          weight: if weight == "bold" { "bold" } else { "regular" })[#body]],
)

// arrow — 샤프트(상대 종점) + open-V 헤드(tip에서 뒤꿈치±수직 날개, 절대 대각선).
// 초판의 벡터식은 대수적으로 퇴화해 수평 화살표가 0-길이 선이 됐다(실측) —
// 아래 "tip에서 날개 끝점으로" 상대 벡터 형태가 실측 교정본이다.
#let ig-arrow(x1, y1, x2, y2, style: "solid") = {
  let stroke = (paint: ig-color("ink-soft"), thickness: 1.2pt,
                dash: if style == "dashed" { "dashed" } else { none })
  place(top + left, dx: pt(x1), dy: pt(y1),
        line(end: (pt(x2 - x1), pt(y2 - y1)), stroke: stroke))
  let dx = x2 - x1
  let dy = y2 - y1
  let len = calc.sqrt(dx * dx + dy * dy)
  let ux = dx / len
  let uy = dy / len
  let hw = 4.0                                  // ARROW_HEAD_W — 비율 4.0/1.2 = 3.33
  let bx = x2 - ux * hw                         // 뒤꿈치(shaft 방향 hw 뒤)
  let by = y2 - uy * hw
  let px = -uy                                  // 단위 수직벡터
  let py = ux
  place(top + left, dx: pt(x2), dy: pt(y2),     // 날개 1: tip → heel + perp·hw/2
        line(end: (pt(bx + px * hw / 2 - x2), pt(by + py * hw / 2 - y2)), stroke: stroke))
  place(top + left, dx: pt(x2), dy: pt(y2),     // 날개 2: tip → heel − perp·hw/2
        line(end: (pt(bx - px * hw / 2 - x2), pt(by - py * hw / 2 - y2)), stroke: stroke))
}
```

`emit.py`:

```python
"""emit.py — FigModel → typst 방출(스펙 §5.1). 칠하기만 한다: 조건 분기 금지, 좌표는 2자리 반올림."""
from __future__ import annotations

from .model import ArrowOp, FigModel, RectOp, TextOp


def _n(v: float) -> str:
    return f"{v:.2f}"


def _esc(s: str) -> str:
    # md2typst step 6 기준과 동일하게 @·<·>까지 — "SLA @team"이 label로 해석돼
    # 빌드가 깨지는 것을 막는다(적대 검토 실증).
    for a, b in (("\\", "\\\\"), ("#", "\\#"), ("[", "\\["), ("]", "\\]"),
                 ("$", "\\$"), ("*", "\\*"), ("_", "\\_"),
                 ("@", "\\@"), ("<", "\\<"), (">", "\\>")):
        s = s.replace(a, b)
    return s


def render_typ(fig: FigModel, tokens: dict) -> str:
    lines = [
        "// 자동 생성 — scripts/infographic/emit.py. 수정 금지(원본은 펜스에 있다).",
        '#import "../helper.typ": ig-rect, ig-text, ig-arrow, ig-figure',
        f"#ig-figure({_n(fig.width)}, {_n(fig.height)})[",
    ]
    for op in fig.ops:
        if isinstance(op, RectOp):
            lines.append(
                f"  #ig-rect({_n(op.x)}, {_n(op.y)}, {_n(op.w)}, {_n(op.h)}, "
                f"rx: {_n(op.rx)}pt, fill-role: \"{op.fill_role}\", "
                f"stroke-role: \"{op.stroke_role}\", stroke-w: {_n(op.stroke_w)}pt)")
        elif isinstance(op, ArrowOp):
            lines.append(f"  #ig-arrow({_n(op.x1)}, {_n(op.y1)}, {_n(op.x2)}, {_n(op.y2)}, "
                         f"style: \"{op.style}\")")
        elif isinstance(op, TextOp):
            w = f", weight: \"{op.weight}\"" if op.weight != "regular" else ""
            # ig-text는 컨테이너 중심 앵커라 절대좌표 환산에 fw·fh가 필요하다(helper 참조).
            lines.append(f"  #ig-text({_n(op.x)}, {_n(op.y)}, {_n(fig.width)}, "
                         f"{_n(fig.height)}, {_n(op.size)}, \"{op.role}\"{w})[{_esc(op.text)}]")
    lines.append("]")
    return "\n".join(lines) + "\n"
```

- [ ] **Step 4: 테스트 통과 확인**

Run: `cd /mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook-typst && python3 -m pytest tests/test_infographic_emit.py -v`
Expected: 골든 없음 실패(3 passed, 1 failed — `골든 없음`). 이어 골든 확정 절차:
`IG_REGEN_GOLDEN=1 python3 -m pytest tests/test_infographic_emit.py -v` → 4 passed.
생성된 골든 파일을 반드시 눈으로 확인한다(2단계 카드·제목·note 포함, `#import "../helper.typ"`·`#ig-text` 호출 형태) — 컴파일 검증은 Task 7이, 렌더 눈검은 Task 9 Step 5가 담당하므로 이 단계는 코드 형태 확인으로 족하다. 확인 후 Step 5에서 함께 커밋한다.

- [ ] **Step 5: 커밋**

```bash
git add skills/korean-ebook-typst/scripts/infographic/emit.py skills/korean-ebook-typst/templates/infographic/ skills/korean-ebook-typst/tests/test_infographic_emit.py skills/korean-ebook-typst/tests/fixtures/infographic/
git commit -m "feat: emit + helper.typ — FigModel→typst 방출·래퍼·골든 스냅샷"
```

---

### Task 7: typst 컴파일 스모크 — 방출물이 실제로 컴파일된다

**Files:**
- Test: `skills/korean-ebook-typst/tests/test_infographic_compile.py`

**Interfaces:**
- Consumes: Task 6 `render_typ`, `helper.typ`, `build.py:typst_binary()`(68행 — 경로 해석 재사용)
- Produces: 검증 사실 — 방출 .typ + helper.typ + tokens.json이 typst 0.15.1로 컴파일된다. 화살표 open-V 벡터 계산이 유효한 typst 코드인지 확인(렌더는 사람이 PNG로 눈검 — 본 Task는 컴파일 게이트만).

- [ ] **Step 1: 실패 테스트 작성**

```python
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
from scripts.infographic.archetypes import flow as flow_arch
from scripts.infographic.emit import render_typ
from scripts.infographic.parse import parse_fence

SKILL = Path(__file__).resolve().parents[1]
TYPST = typst_binary()          # PATH → ~/.local/bin/typst 폴백 단일화(Global Constraints)
pytestmark = pytest.mark.skipif(not TYPST, reason="typst 바이너리 없음")


def test_flow_fig_compiles(tmp_path):
    tokens = json.loads((SKILL / "styles" / "practical" / "tokens.json").read_text(encoding="utf-8"))
    fence = parse_fence(1, 1, json.dumps({
        "layout": "flow", "title": "컴파일 스모크",
        "steps": [{"title": "A", "text": "가"}, {"title": "B", "text": "나"}],
    }, ensure_ascii=False))
    out = render_typ(flow_arch.layout(fence, tokens), tokens)
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
```

- [ ] **Step 2: 테스트 실패/에러 확인**

Run: `cd /mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook-typst && python3 -m pytest tests/test_infographic_compile.py -v`
Expected: FAIL 또는 오류 — 모듈 경로/컴파일 에러 중 하나

- [ ] **Step 3: 최소 구현**

테스트 파일 자체가 구현이다(Task 6의 emit·helper가 이미 존재한다 — 이 Task는 검증만 추가). 컴파일이 실패하면 helper.typ(Task 6)의 오탈자를 잡는다. 단 open-V 날개의 **렌더 형태**(날개 2개가 tip에서 V자로 벌어지는지)는 컴파일 게이트가 못 잡는다 — Task 9 Step 5 눈검에서 확인한다.

- [ ] **Step 4: 테스트 통과 확인**

Run: `cd /mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook-typst && python3 -m pytest tests/test_infographic_compile.py -v`
Expected: PASS (typst 없음 환경이면 SKIP — CI가 아닌 로컬 실행 전제)

- [ ] **Step 5: 커밋**

```bash
git add skills/korean-ebook-typst/tests/test_infographic_compile.py skills/korean-ebook-typst/templates/infographic/helper.typ
git commit -m "test: 인포그래픽 방출물 typst 컴파일 스모크"
```

---

### Task 8: lint.py — I1 게이트 (전수 보고·위치 계약·저작자 레버·숫자-evidence 교차검증)

**Files:**
- Create: `skills/korean-ebook-typst/scripts/infographic/lint.py`
- Test: `skills/korean-ebook-typst/tests/test_infographic_lint.py`

**Interfaces:**
- Consumes: `parse.Fence`, `budget.line_count/width_units`, `roles.REQUIRED_INFO_ROLES`, `model.FigModel/ArrowOp/TextOp`(G3·커넥터·예산은 FigModel ops에서 검사)
- Produces:
  - `lint.LintFinding(kind: str, loc: str, measured: str, levers: tuple[str, ...], fatal: bool = True)` frozen — `fatal=False`는 빌드를 막지 않고 검수 시트로 이관(미검증 플래그, 스펙 §3.3·§5.2)
  - `lint.check(fences: list[Fence], figs: dict[int, FigModel], tokens: dict, chapter_md: str, chapter_name: str) -> list[LintFinding]` — **전수 검사 후 전건 반환**(빌드는 치명 것만 모아 중단, 스펙 §5.2). `figs`는 `{fence.index: FigModel}`.
  - 검사 종류(kind) — 스펙 §5.2 9항목 중 Phase 1 해당 전부:
    - `"tokens"`(#7 토큰 존재) — fatal
    - `"number-evidence"`(#5 숫자-evidence·교차검증) — fatal
    - `"number-unverified"`(#5 미검증 — evidence 불해석·타 챕터 인용) — **비치명**: 빌드는 계속, 검수 시트 상단 경고로 이관(스펙 §3.3 "건너뛰고 미검증 플래그"의 구현 — 초판이 이것을 치명 에러로 만들어 타 챕터 인용(스펙 허용)을 영구 빌드 실패로 만들었던 결함 정정)
    - `"budget"`(#2 텍스트 예산) — fatal. 초판의 `cap×10` 문턱(사실상 무검사 — 실증) 폐지. 검사: `budget.line_count(text, op.max_w, op.size) > 3` → "예상 N줄 > 3줄(밀도 상한)" 측정값 보고
    - `"g3-invariant"`(#9 크기 불변식) — fatal
    - `"connector"`(#4 커넥터 산술) — fatal. ArrowOp 전수: ①`len ≥ 12`(샤프트 가시) ②tip이 목표 rect 내부에 착지하지 않는지(끝점이 어떤 RectOp 내부도 침범 않아야) ③`ARROW_HEAD_W/ARROW_STROKE_W` 비율이 2.5~3.5(상수 1회 검증 — 4.0/1.2=3.33)
    - `"fence-impostor"`(#8 펜스 위장 감지) — fatal. chapter_md의 모든 ```펜스 중 언어가 `infographic`이 아닌데 내용이 JSON이고 `layout` 키를 가지면 보고(예: ```infographics 오타 → 무음 코드블록 인쇄 방지)
    - `"layout"`(#1·§6.2) — fatal. `flow.FlowLayoutError`를 render가 이 kind로 변환(판형 상한·공간 부족·높이 85% 초과). `parse.ParseError`도 render가 `"schema"` kind로 변환해 전수 집계(초판은 첫 위반 traceback 크래시였다)
  - loc 형식: `"{chapter_name} #{index} {field_path}"` — 필드 경로는 `TextOp.field`(Task 5)에서 온다. 예: `ch05.md #2 steps[1].title`. 초판처럼 텍스트 스니펫을 loc로 쓰지 않는다.
  - levers는 스펙 §5.2 계약 문구: `("글자 축약", "요소 수 감소", "layout 변형", "펜스 분할")` 중 적합한 것. 폭·간격 확장 제안 금지 준수.
- 숫자 렉시콘(스펙 §3.3): `re.compile(r"[0-9][0-9.,%]*")`. 면제: 매치 직후/직전이 "장"/"절"인 `제N` 형태(`제\d+장`), 원형숫자 `①-⑳`.
- evidence 교차검증: `evidence == "§N"`이면 chapter_md에서 N번째 `^## ` 헤딩 이후 다음 `^## ` 전 텍스트 범위를 추출해, 펜스 내 각 숫자 토큰이 해당 범위에 부분 문자열로 존재하는지 검사. evidence 없음/해석 불가/범위 밖 → finding `"number-evidence"` (미검증 플래그로 loc에 표기 — 검수 시트가 소비).

- [ ] **Step 1: 실패 테스트 작성**

```python
"""test_infographic_lint.py — 스펙 §5.2: 전수 보고·위치·레버·교차검증."""
import json
from pathlib import Path

from scripts.infographic.archetypes import flow as flow_arch
from scripts.infographic.lint import check
from scripts.infographic.parse import parse_fence

SKILL = Path(__file__).resolve().parents[1]
TOKENS = json.loads((SKILL / "styles" / "practical" / "tokens.json").read_text(encoding="utf-8"))

CH = """## 개요

대응은 5단계로 수렴한다. 영향도 기반 분류 후 30분 임시 조치를 시행한다.

## 상세

추가 설명.
"""


def _fences(specs: list[dict]):
    out = []
    for i, s in enumerate(specs, 1):
        out.append(parse_fence(i, 1, json.dumps(s, ensure_ascii=False)))
    return out


def _figs(fences):
    return {f.index: flow_arch.layout(f, TOKENS) for f in fences}


def test_all_findings_collected_not_first_only():
    # 펜스 1: 숫자+evidence 없음 / 펜스 2: 숫자+원문에 없는 값 — 둘 다 보고
    fs = _fences([
        {"layout": "flow", "title": "3단계로 수렴한다", "steps": [
            {"title": "접수", "text": "등록"}, {"title": "폐쇄", "text": "확정"}]},
        {"layout": "flow", "title": "t", "evidence": "§1", "steps": [
            {"title": "분류", "text": "999시간 조치"}, {"title": "폐쇄", "text": "확정"}]},
    ])
    found = check(fs, _figs(fs), TOKENS, CH, "ch01.md")
    kinds = [f.kind for f in found]
    assert "number-evidence" in kinds
    assert sum(1 for f in found if f.kind == "number-evidence") == 2   # 전수
    assert any(f.loc == "ch01.md #1 title" for f in found)             # 위치 계약
    assert any(f.loc == "ch01.md #2 steps[0].text" for f in found)


def test_number_with_valid_evidence_passes():
    fs = _fences([{"layout": "flow", "title": "30분 내 임시 조치", "evidence": "§1", "steps": [
        {"title": "분류", "text": "영향도 분류"}, {"title": "대응", "text": "조치"}]}])
    found = check(fs, _figs(fs), TOKENS, CH, "ch01.md")
    assert not [f for f in found if f.kind == "number-evidence"]


def test_ordinal_exempt():
    fs = _fences([{"layout": "flow", "title": "제2장에서 다루는 흐름", "steps": [
        {"title": "접수", "text": "등록"}, {"title": "폐쇄", "text": "확정"}]}])
    found = check(fs, _figs(fs), TOKENS, CH, "ch01.md")
    assert not [f for f in found if f.kind == "number-evidence"]


def test_unresolvable_evidence_nonfatal():
    fs = _fences([{"layout": "flow", "title": "3단계", "evidence": "§9", "steps": [
        {"title": "접수", "text": "등록"}, {"title": "폐쇄", "text": "확정"}]}])
    found = check(fs, _figs(fs), TOKENS, CH, "ch01.md")
    ev = [f for f in found if f.kind == "number-unverified"]
    assert ev and "미검증" in ev[0].measured
    assert ev[0].fatal is False                    # 빌드 안 막음 — 검수 시트 이관(§3.3)


def test_budget_density_violation_reported_with_field_loc():
    long_title = "아주 긴 단계 제목이라 밀도 상한을 초과하는 텍스트가 이곳에 있다 " * 3
    fs = _fences([{"layout": "flow", "title": "t", "steps": [
        {"title": long_title, "text": "가"}, {"title": "B", "text": "나"}]}])
    found = check(fs, _figs(fs), TOKENS, CH, "ch01.md")
    b = [f for f in found if f.kind == "budget"]
    assert b, "밀도 초과(예상 4줄+)가 보고돼야 한다 — 초판 ×10 문턱은 무검사였다(실증)"
    assert b[0].loc == "ch01.md #1 steps[0].title"   # 필드 경로 loc(§5.2 계약)
    assert "줄" in b[0].measured and b[0].levers     # 측정값 + 레버


def test_fence_impostor_detected():
    md = CH + "\n```infographics\n{\"layout\": \"flow\", \"title\": \"x\"}\n```\n"
    fs = _fences([{"layout": "flow", "title": "t", "steps": [
        {"title": "A", "text": "가"}, {"title": "B", "text": "나"}]}])
    found = check(fs, _figs(fs), TOKENS, md, "ch01.md")
    imp = [f for f in found if f.kind == "fence-impostor"]
    assert imp and imp[0].fatal and "infographics" in imp[0].measured


def test_connector_shaft_visibility_checked():
    from scripts.infographic.model import ArrowOp, FigModel
    fs = _fences([{"layout": "flow", "title": "t", "steps": [
        {"title": "A", "text": "가"}, {"title": "B", "text": "나"}]}])
    figs = _figs(fs)
    f0 = figs[1]
    # 공격: 8pt 샤프트(<12)로 교체 — §6.1 위반 감지
    short = tuple(ArrowOp(x1=o.x1, y1=o.y1, x2=o.x1 + 8.0, y2=o.y1, style=o.style)
                  if isinstance(o, ArrowOp) else o for o in f0.ops)
    figs[1] = FigModel(width=f0.width, height=f0.height, ops=short, source_index=1)
    found = check(fs, figs, TOKENS, CH, "ch01.md")
    assert any(f.kind == "connector" and "12" in f.measured for f in found)


def test_missing_token_roles():
    bad = json.loads(json.dumps(TOKENS)); del bad["infographic"]
    fs = _fences([{"layout": "flow", "title": "t", "steps": [
        {"title": "A", "text": "가"}, {"title": "B", "text": "나"}]}])
    found = check(fs, _figs(fs), bad, CH, "ch01.md")
    assert any(f.kind == "tokens" for f in found)


def test_g3_invariant_checked_from_fig_ops():
    fs = _fences([{"layout": "flow", "title": "t", "steps": [
        {"title": "A", "text": "가"}, {"title": "B", "text": "나"}]}])
    figs = _figs(fs)
    # 공격: 도식 텍스트 하나를 본문 크기로 바꿔치기 — G3 위반 감지 확인
    from scripts.infographic.model import TextOp
    f0 = figs[1]
    tampered = tuple(
        TextOp(x=o.x, y=o.y, size=TOKENS["fonts"]["body"]["size_pt"], text=o.text,
               role=o.role, weight=o.weight, max_w=o.max_w, field=o.field)
        if isinstance(o, TextOp) else o for o in f0.ops)
    figs[1] = type(f0)(width=f0.width, height=f0.height, ops=tampered, source_index=f0.source_index)
    found = check(fs, figs, TOKENS, CH, "ch01.md")
    assert any(f.kind == "g3-invariant" for f in found)
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `cd /mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook-typst && python3 -m pytest tests/test_infographic_lint.py -v`
Expected: FAIL — ModuleNotFoundError lint

- [ ] **Step 3: 최소 구현**

```python
"""lint.py — I1 게이트(스펙 §5.2). 전수 검사 후 전건 반환: 빌드가 치명(fatal) 것만 모아 중단.
fatal=False(미검증류)은 빌드를 막지 않고 검수 시트로 이관한다(스펙 §3.3)."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass

from . import budget, roles
from .model import (ARROW_HEAD_W, ARROW_STROKE_W, ArrowOp, FigModel,
                    RectOp, TextOp)
from .parse import Fence

NUM_RE = re.compile(r"[0-9][0-9.,%]*")
ORDINAL_RE = re.compile(r"제\d+[장절]")
CIRCLED = set("①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳")
ANY_FENCE_RE = re.compile(r"^```(\w[\w-]*)[ \t]*\n(.*?)^```[ \t]*$", re.S | re.M)

LEV_SHORTEN = "글자 축약"
LEV_FEWER = "요소 수 감소"
LEV_LAYOUT = "layout 변형(예: cards, 2행 랩)"
LEV_SPLIT = "펜스 분할"
MAX_LINES = 3              # 박스당 밀도 상한(스펙 §5.2-2 — "28자>22자"급 실측 보고)


@dataclass(frozen=True)
class LintFinding:
    kind: str
    loc: str
    measured: str
    levers: tuple
    fatal: bool = True


def _numbers_in(text: str) -> list[str]:
    text = ORDINAL_RE.sub("", text)
    text = "".join(ch for ch in text if ch not in CIRCLED)
    return NUM_RE.findall(text)


def _section_text(md: str, n: int) -> str | None:
    # N번째 ^## 헤딩부터 다음 ^## 전까지(스펙 §3.3 교차검증 범위)
    idx = [m.start() for m in re.finditer(r"^## ", md, flags=re.M)]
    if n < 1 or n > len(idx):
        return None
    end = idx[n] if n < len(idx) else len(md)
    return md[idx[n - 1]:end]


def check(fences: list[Fence], figs: dict[int, FigModel], tokens: dict,
          chapter_md: str, chapter_name: str) -> list[LintFinding]:
    out: list[LintFinding] = []

    # 1. 토큰 존재(§5.2-7)
    info = tokens.get("infographic", {})
    for role in roles.REQUIRED_INFO_ROLES:
        if not isinstance(info.get(role), str):
            out.append(LintFinding("tokens", f"{chapter_name} tokens.infographic.{role}",
                                   "값 없음", ("스타일 팩에 5역할 정의",)))

    # 2. 펜스 위장 감지(§5.2-8) — 미등록 펜스 언어에 layout 키가 있으면 오타 의심
    for m in ANY_FENCE_RE.finditer(chapter_md):
        lang, body = m.group(1), m.group(2)
        if lang == "infographic":
            continue
        try:
            d = json.loads(body)
        except ValueError:
            continue
        if isinstance(d, dict) and "layout" in d:
            out.append(LintFinding(
                "fence-impostor", f"{chapter_name} 펜스언어:{lang}",
                f"```{lang} 내용이 layout 키 포함 JSON — infographic 오타 의심"
                "(그대로 두면 YAML이 코드블록으로 인쇄됨)",
                ("펜스 언어를 infographic으로 수정",)))

    # 3. 커넥터 상수(§5.2-4) — 헤드/샤프트 비 2.5~3.5 (1회 검증)
    ratio = ARROW_HEAD_W / ARROW_STROKE_W
    if not 2.5 <= ratio <= 3.5:
        out.append(LintFinding(
            "connector", f"{chapter_name} model.ARROW_HEAD_W",
            f"헤드/샤프트 비 {ratio:.2f} — 허용 2.5~3.5",
            ("ARROW_HEAD_W/ARROW_STROKE_W 상수 수정",)))

    body_size = tokens["fonts"]["body"]["size_pt"]
    section_cache: dict[str, str | None] = {}

    for f in fences:
        prefix = f"{chapter_name} #{f.index}"

        # 4. 숫자-evidence 교차검증(§3.3) — 미검증은 비치명
        fields: list[tuple[str, str]] = [("title", f.title)]
        if f.kicker:
            fields.append(("kicker", f.kicker))
        for i, s in enumerate(f.data["steps"]):
            fields.append((f"steps[{i}].title", s["title"]))
            fields.append((f"steps[{i}].text", s["text"]))
        sec = None
        if f.evidence:
            if f.evidence not in section_cache:
                m = re.fullmatch(r"§(\d+)", f.evidence.strip())
                section_cache[f.evidence] = (
                    _section_text(chapter_md, int(m.group(1))) if m else None)
            sec = section_cache[f.evidence]
        for path, text in fields:
            nums = _numbers_in(text)
            if not nums:
                continue
            if not f.evidence:
                out.append(LintFinding(
                    "number-evidence", f"{prefix} {path}",
                    f"숫자 {nums} 존재, evidence 필드 없음",
                    ("원문 절 앵커 evidence 추가(예: \"§1\")",)))
            elif sec is None:
                out.append(LintFinding(
                    "number-unverified", f"{prefix} {path}",
                    f"숫자 {nums} — 미검증(evidence {f.evidence!r} 해석 불가·범위 밖) "
                    "→ 검수 시트 사람 대조 필수",
                    ("evidence를 §N 형식으로 바꾸거나 검수 시트에서 사람 대조",),
                    fatal=False))
            else:
                for num in nums:
                    if num not in sec:
                        out.append(LintFinding(
                            "number-evidence", f"{prefix} {path}",
                            f"숫자 {num!r} 원문(evidence {f.evidence})에 없음",
                            (LEV_SHORTEN, "원문에 있는 숫자로 교체")))

        # 5. FigModel ops — 예산(§5.2-2)·G3(§5.2-9)·커넥터(§5.2-4)
        fig = figs.get(f.index)
        if fig is None:
            continue
        cards = [o for o in fig.ops if isinstance(o, RectOp)
                 and o.fill_role == "surface-tint"]
        for op in fig.ops:
            if isinstance(op, TextOp):
                if op.max_w > 0 and op.field:
                    lines = budget.line_count(op.text, op.max_w, op.size)
                    if lines > MAX_LINES:
                        out.append(LintFinding(
                            "budget", f"{prefix} {op.field}",
                            f"예상 {lines}줄 > 밀도 상한 {MAX_LINES}줄 "
                            f"({budget.width_units(op.text):.0f}단위, 상자 {op.max_w:.0f}pt)",
                            (LEV_SHORTEN, LEV_FEWER, LEV_SPLIT)))
                if abs(op.size - body_size) <= 0.3:
                    out.append(LintFinding(
                        "g3-invariant", f"{prefix} {op.field or 'text'}",
                        f"크기 {op.size}pt — 본문 {body_size}pt±0.3 밖이어야 함",
                        ("크기 사다리 재검토(layout 버그)",)))
            elif isinstance(op, ArrowOp):
                import math as _math
                length = _math.hypot(op.x2 - op.x1, op.y2 - op.y1)
                if length < 12.0:
                    out.append(LintFinding(
                        "connector", f"{prefix} arrow({op.x1:.0f},{op.y1:.0f}→{op.x2:.0f},{op.y2:.0f})",
                        f"샤프트 가시 {length:.1f}pt < 12pt(§6.1)",
                        (LEV_LAYOUT, LEV_SPLIT)))
                for ex, ey in ((op.x1, op.y1), (op.x2, op.y2)):
                    for c in cards:
                        if c.x < ex < c.x + c.w and c.y < ey < c.y + c.h:
                            out.append(LintFinding(
                                "connector", f"{prefix} arrow→({ex:.0f},{ey:.0f})",
                                f"끝점이 카드({c.x:.0f},{c.y:.0f},{c.w:.0f}×{c.h:.0f}) "
                                "내부에 묻힘 — tip-gap 8~12pt 유지(§6.1)",
                                (LEV_LAYOUT,)))
    return out
```

- [ ] **Step 4: 테스트 통과 확인**

Run: `cd /mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook-typst && python3 -m pytest tests/test_infographic_lint.py -v`
Expected: 9 passed

- [ ] **Step 5: 커밋**

```bash
git add skills/korean-ebook-typst/scripts/infographic/lint.py skills/korean-ebook-typst/tests/test_infographic_lint.py
git commit -m "feat: I1 린트 — 전수 보고·위치 계약·숫자-evidence 교차검증·G3 불변식"
```

---

### Task 9: build.py 통합 — render 호출·include 치환·검수 시트·리셋

**Files:**
- Modify: `skills/korean-ebook-typst/scripts/build.py` (assemble 내부, 480~556행 영역 + 상단 sys.path 1줄)
- Modify: `skills/korean-ebook-typst/scripts/qc_gate.py` (검수 시트 WARN — 아래 Step 3b)
- Create: `skills/korean-ebook-typst/scripts/infographic/render.py`
- Test: `skills/korean-ebook-typst/tests/test_infographic_build_integration.py`

**Interfaces:**
- Consumes: Task 2~8 전부. `build.py`의 `assemble(cfg, book_dir)`·`subprocess md2typst 호출`(508~511행)·`converted` 리스트(523행).
- Produces:
  - `render.render_book_fences(book_dir: Path, build: Path, cfg: dict) -> dict[int, dict[int, str]]` — `{챕터idx: {펜스index: emit 파일명}}`. 내부: 각 챕터의 `build/fences/<stem>.fences.json`(Task 3이 --fences-out로 생성)을 읽어 parse→layout.dispatch→lint.check→emit. **I1 findings가 1건이라도 있으면 `render.I1Error` 상향 — `.findings: list[LintFinding]`, `.report() -> str`**(전건 목록, 스펙 §5.2 전수 중단).
  - 검수 시트: `build/infographic/{idx:03d}-fig{nn}.review.md` — 표 `| 요소 | 문구 | evidence | 교차검증 | 확인란 |`, 미검증 플래그 행 포함, 상단에 DEFAULT_NOTE 원문.
  - `build.py assemble()` 수정 4곳:
    1. 리셋: `shutil.rmtree(build / "infographic", ignore_errors=True)` + `build/infographic.mkdir` (487행 assets 리셋 뒤)
    2. md2typst 서브프로세스 인자에 `--fences-out {build}/fences` 추가 (509행) — fences 디렉터리도 assemble에서 mkdir/리셋
    3. 챕터 변환 루프 뒤: `render.render_book_fences(...)` 호출. I1Error면 `_fail(report)` — 전체 findings 출력
    4. 각 namespaced .typ의 `⟦IG:N⟧` 마커를 `#include "../infographic/{idx:03d}-fig{N:02d}.typ"`로 치환 (rebase_images 호출 후, converted.append 전). 치환 누락 마커(펜스 JSON 파싱은 됐는데 emit 파일 없음)가 남으면 `_fail`
  - helper.typ 복사: `shutil.copy2(SKILL_DIR / "templates" / "infographic" / "helper.typ", build / "helper.typ")` (492행 base.typ 복사 뒤) — 컴파일 root가 build/이므로 fig .typ의 `#import "helper.typ"`가 해석된다(fig는 build/infographic/에, helper는 build/에 — typst import는 **root 기준 절대처럼 동작하는 상대경로**가 아니므로 fig .typ에서 `#import "../helper.typ"`… 가 아니라: typst 0.15.1의 import는 *파일 기준* 상대경로다. 따라서 emit(Task 6)의 import 문은 `#import "../helper.typ"` 여야 한다 — **Task 6 구현 시 이 1행을 반드시 `#import "../helper.typ": …`로 쓴다**(build/infographic/fig.typ → build/helper.typ). preview(Task 10)는 같은 디렉터리 구조를 만들어 재사용.)
- emit 파일명 규칙: `{챕터idx:03d}-fig{펜스index:02d}.typ` — ch 순번은 cfg["chapters"]의 enumerate 순서.
- **qc_gate WARN(스펙 §5.4 집행 장치)**: `qc_gate.check_review_sheets(build: Path) -> list[str]` — `build/infographic/*.review.md` 중 `- [ ] 원문 대조 완료` 체크박스가 비어 있는(미완료) 시트의 파일명 목록 반환. qc_gate run이 이를 WARN으로 리포트에 남긴다(에러 아님 — 검수는 사람 판단, final/ 생성은 기존 규칙 그대로).

- [ ] **Step 1: 실패 테스트 작성**

```python
"""test_infographic_build_integration.py — 스펙 §2 [2]: 조립 통합·경로·검수 시트."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[1]


def _make_book(tmp_path: Path) -> Path:
    book = tmp_path / "book"
    (book / "manuscript").mkdir(parents=True)
    (book / "manuscript" / "ch01.md").write_text("""## 첫째 장

대응은 5단계로 수렴한다.

```infographic
{"layout": "flow", "title": "5단계로 수렴한다", "evidence": "§1", "steps": [
  {"title": "접수", "text": "등록"},
  {"title": "폐쇄", "text": "확정"}
]}
```

뒤 본문.
""", encoding="utf-8")
    (book / "typst-build.yaml").write_text(
        'style: practical\n' 'title: "테스트책"\n' 'subtitle: "부"\n'
        'author: "KLIC"\n' 'date: "2026-08"\n'
        "chapters:\n  - manuscript/ch01.md\n", encoding="utf-8")
    return book


def test_assemble_emits_fig_include_and_review_sheet(tmp_path):
    book = _make_book(tmp_path)
    build = book / "build"
    r = subprocess.run([sys.executable, str(SKILL / "scripts" / "build.py"), str(book)],
                       capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stderr
    fig = build / "infographic" / "000-fig01.typ"
    assert fig.exists(), "emit 파일 없음"
    typ = (build / "typ" / "000-ch01.typ").read_text(encoding="utf-8")
    assert '#include "../infographic/000-fig01.typ"' in typ
    assert "⟦IG:1⟧" not in typ
    assert (build / "helper.typ").exists()
    review = build / "infographic" / "000-fig01.review.md"
    body = review.read_text(encoding="utf-8")
    assert "확인란" in body and "steps[0].title" in body
    assert "교차검증" in body and "I1 통과" in body        # 5열 계약(§5.4)
    pdf = book / "draft" / "테스트책.pdf"                  # sanitize_filename은 공백 유지(실증)
    assert pdf.exists() and pdf.stat().st_size > 10_000, "최종 PDF 없음"


def test_i1_blocks_build_with_full_report(tmp_path):
    book = _make_book(tmp_path)
    ch = book / "manuscript" / "ch01.md"
    ch.write_text(ch.read_text(encoding="utf-8").replace(
        '"title": "5단계로 수렴한다"',
        '"title": "777단계로 수렴한다"'), encoding="utf-8")   # 원문에 없는 숫자
    r = subprocess.run([sys.executable, str(SKILL / "scripts" / "build.py"), str(book)],
                       capture_output=True, text=True, timeout=120)
    assert r.returncode != 0
    assert "number-evidence" in (r.stdout + r.stderr)
    assert "ch01.md #1" in (r.stdout + r.stderr)          # 위치 계약


def test_qc_gate_warns_on_unreviewed_sheets(tmp_path):
    from scripts.qc_gate import check_review_sheets
    igdir = tmp_path / "build" / "infographic"; igdir.mkdir(parents=True)
    (igdir / "000-fig01.review.md").write_text(
        "| 요소 |\n- [ ] 원문 대조 완료", encoding="utf-8")          # 미완료
    (igdir / "000-fig02.review.md").write_text(
        "| 요소 |\n- [x] 원문 대조 완료", encoding="utf-8")          # 완료
    pending = check_review_sheets(tmp_path / "build")
    assert pending == ["000-fig01.review.md"]


def test_rebuild_resets_infographic_dir(tmp_path):
    book = _make_book(tmp_path)
    subprocess.run([sys.executable, str(SKILL / "scripts" / "build.py"), str(book)],
                   capture_output=True, text=True, timeout=120)
    stale = book / "build" / "infographic" / "zzz-stale.typ"
    stale.write_text("garbage", encoding="utf-8")
    subprocess.run([sys.executable, str(SKILL / "scripts" / "build.py"), str(book)],
                   capture_output=True, text=True, timeout=120)
    assert not stale.exists()
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `cd /mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook-typst && python3 -m pytest tests/test_infographic_build_integration.py -v`
Expected: FAIL — emit 파일 없음 / include 없음

- [ ] **Step 3: 최소 구현**

`scripts/infographic/render.py`:

```python
"""render.py — 책 단위 펜스 렌더 오케스트레이션(스펙 §2 [2]).
I1 치명 위반은 전건 모아 중단. ParseError·FlowLayoutError도 finding으로 변환해
전수 집계한다(초판은 첫 위반 traceback 크래시였다 — 적대 검토 정정)."""
from __future__ import annotations

import json
from pathlib import Path

from . import emit, layout, lint
from .archetypes.flow import FlowLayoutError
from .parse import DEFAULT_NOTE, ParseError, parse_fence


class I1Error(Exception):
    def __init__(self, findings):
        self.findings = findings      # super()보다 먼저 — report()가 self.findings를 참조한다
        super().__init__(self.report())

    def report(self) -> str:
        lines = ["[I1] 인포그래픽 린트 위반 — 전건:"]
        for f in self.findings:
            lines.append(f"  [{f.kind}] {f.loc} — {f.measured} → 제안: {', '.join(f.levers)}")
        return "\n".join(lines)


def render_book_fences(book_dir: Path, build: Path, cfg: dict) -> dict[int, dict[int, str]]:
    fences_dir = build / "fences"
    out_dir = build / "infographic"
    out_dir.mkdir(parents=True, exist_ok=True)
    tokens = json.loads((build / "tokens.json").read_text(encoding="utf-8"))
    all_findings: list[lint.LintFinding] = []
    parsed_by_chapter: dict[int, tuple] = {}

    for idx, ch in enumerate(cfg["chapters"]):
        stem = Path(ch).stem
        side = fences_dir / f"{stem}.fences.json"
        if not side.exists():
            continue
        chapter_md = (book_dir / ch).read_text(encoding="utf-8")
        chapter_name = Path(ch).name
        fences = []
        for raw in json.loads(side.read_text(encoding="utf-8")):
            try:
                fences.append(parse_fence(raw["index"], raw["line"], raw["body"]))
            except ParseError as e:
                all_findings.append(lint.LintFinding(
                    "schema", f"{chapter_name} #{e.fence_index}", e.detail,
                    ("펜스 JSON 스키마 수정",)))
        figs = {}
        for f in fences:
            try:
                figs[f.index] = layout.dispatch(f, tokens)
            except FlowLayoutError as e:
                all_findings.append(lint.LintFinding(
                    "layout", f"{chapter_name} #{f.index}", e.detail,
                    ("글자 축약", "요소 수 감소", "펜스 분할")))
        all_findings.extend(lint.check(fences, figs, tokens, chapter_md, chapter_name))
        parsed_by_chapter[idx] = (fences, figs, chapter_name)

    fatal = [f for f in all_findings if f.fatal]
    if fatal:
        raise I1Error(fatal)

    result: dict[int, dict[int, str]] = {}
    for idx, (fences, figs, chapter_name) in parsed_by_chapter.items():
        emits: dict[int, str] = {}
        for f in fences:
            fig = figs[f.index]
            name = f"{idx:03d}-fig{f.index:02d}.typ"
            (out_dir / name).write_text(emit.render_typ(fig, tokens), encoding="utf-8")
            unverified = [x for x in all_findings
                          if x.kind == "number-unverified"
                          and x.loc.startswith(f"{chapter_name} #{f.index} ")]
            (out_dir / name.replace(".typ", ".review.md")).write_text(
                _review_sheet(f, unverified), encoding="utf-8")
            emits[f.index] = name
        result[idx] = emits
    return result


def _review_sheet(f, unverified: list) -> str:
    # 5열 계약(스펙 §5.4) — 요소|문구|evidence|교차검증|확인란 + 미검증 상단 경고.
    rows = [("title", f.title), ("kicker", f.kicker or "—"), ("thesis", f.thesis or "—")]
    for i, s in enumerate(f.data["steps"]):
        rows.append((f"steps[{i}].title", s["title"]))
        rows.append((f"steps[{i}].text", s["text"]))
    lines = [f"# 검수 시트 — 펜스 #{f.index}", ""]
    if unverified:
        lines.append("**⚠ 미검증 숫자 — 사람 대조 필수:**")
        lines += [f"- {u.loc}: {u.measured}" for u in unverified]
        lines.append("")
    lines += [
        f"> 고지: {f.note or DEFAULT_NOTE}",
        f"> evidence: {f.evidence or '—'}",
        "",
        "| 요소 | 문구 | evidence | 교차검증 | 확인란 |",
        "|---|---|---|---|---|",
    ]
    ev = f.evidence or "—"
    for p, t in rows:
        flag = "미검증" if any(f" {p}" in u.loc for u in unverified) else "I1 통과"
        lines.append(f"| {p} | {t} | {ev} | {flag} |  |")
    lines += ["", "- [ ] 원문 대조 완료"]
    return "\n".join(lines) + "\n"
```

`build.py assemble()` 수정 — 487행(`shutil.rmtree(build / "assets", ...)` ) 뒤에:

```python
    shutil.rmtree(build / "infographic", ignore_errors=True)
    (build / "infographic").mkdir(parents=True, exist_ok=True)
    shutil.rmtree(build / "fences", ignore_errors=True)
    (build / "fences").mkdir(parents=True, exist_ok=True)
```

492행(base.typ 복사) 뒤에:

```python
    shutil.copy2(SKILL_DIR / "templates" / "infographic" / "helper.typ", build / "helper.typ")
```

509행 서브프로세스 인자 확장:

```python
        r = subprocess.run(
            [sys.executable, str(MD2TYPST), str(src), "--out", str(build / "typ"),
             "--fences-out", str(build / "fences")],
            capture_output=True, text=True,
        )
```

챕터 루프(523행 `converted.append` 후, 526행 불변식 검사 전)에:

```python
    # 인포그래픽: 펜스 → emit + include 치환(스펙 §2 [2])
    from infographic import render as ig_render
    try:
        figs = ig_render.render_book_fences(book_dir, build, cfg)
    except ig_render.I1Error as exc:
        _fail(str(exc))
    for idx, name in enumerate(converted):
        p = build / "typ" / name
        text = p.read_text(encoding="utf-8")
        import re as _re
        def _sub(m):
            n = int(m.group(1))
            fname = figs.get(idx, {}).get(n)
            if not fname:
                _fail(f"{name}: 펜스 #{n} emit 결과 없음(마커 ⟦IG:{n}⟧)")
            return f'#include "../infographic/{fname}"'
        text = _re.sub(r"⟦IG:(\d+)⟧", _sub, text)
        p.write_text(text, encoding="utf-8")
```

**build.py 상단 수정(필수 — 조건부 아님)**: `from infographic import render`가 동작하려면 `scripts/`가 sys.path에 있어야 한다. 기존 테스트들이 `from scripts.build import assemble`로 **직접 import**하는 컨텍스트에서는 scripts/ 디렉터리가 sys.path에 없다 — 이 줄이 없으면 기존 스모크 스위트 전체가 ModuleNotFoundError로 깨진다(적대 검토 지적). build.py의 import 블록 뒤에 명시한다(SKILL_DIR은 build.py 상단에 실존한다):

```python
sys.path.insert(0, str(SKILL_DIR / "scripts"))
```

- [ ] **Step 3b: qc_gate 검수 시트 WARN (스펙 §5.4 집행 장치)**

`qc_gate.py`에 함수 추가 후 run()의 리포트 생성 지점(warning 성 로그를 남기는 기존 위치 — G3 관련 출력 부분)에서 호출한다:

```python
def check_review_sheets(build: Path) -> list[str]:
    """미완료 검수 시트 파일명 반환(스펙 §5.4 — 확인란 미완료 시 WARN, 에러 아님)."""
    igdir = build / "infographic"
    if not igdir.exists():
        return []
    incomplete = []
    for sheet in sorted(igdir.glob("*.review.md")):
        if "- [ ] 원문 대조 완료" in sheet.read_text(encoding="utf-8"):
            incomplete.append(sheet.name)
    return incomplete
```

run() 내 리포트 출력부에(기존 로그 형식에 맞춰):

```python
    unreviewed = check_review_sheets(build)
    if unreviewed:
        print(f"[WARN] 미확인 인포그래픽 검수 시트 {len(unreviewed)}건: "
              + ", ".join(unreviewed))
```

(qc_gate의 기존 pass/warn 구조를 먼저 읽고, WARN이 final/ 생성을 막지 않는 기존 채널로 출력한다 — 새 에러 경로를 만들지 않는다.)

- [ ] **Step 4: 테스트 통과 확인**

Run: `cd /mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook-typst && python3 -m pytest tests/test_infographic_build_integration.py tests/ -q`
Expected: 전체 PASS (typst 바이너리 필요 — 없으면 build 통합 3건 SKIP 처리: `pytest.mark.skipif`로 `shutil.which("typst")` 가드)

- [ ] **Step 5: 수동 눈검 (비주얼 스모크 선행)**

Run: `cd /tmp && python3 /mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook-typst/scripts/infographic/cli.py preview` 는 아직(Task 10)이므로, 여기선 방금 만든 tmp 책의 `draft/*.pdf`를 열어 flow 카드 2장·제목·고지문·화살표가 정상 렌더됐는지 눈으로 확인한다. 깨지면 helper.typ(Task 6)를 고치고 골든을 재확정한다.

- [ ] **Step 6: 커밋**

```bash
git add skills/korean-ebook-typst/scripts/build.py skills/korean-ebook-typst/scripts/infographic/render.py skills/korean-ebook-typst/tests/test_infographic_build_integration.py
git commit -m "feat: build 통합 — 펜스 렌더·include 치환·검수 시트·디렉터리 리셋"
```

---

### Task 10: cli.py — `lint` / `preview` 단독 실행

**Files:**
- Create: `skills/korean-ebook-typst/scripts/infographic/cli.py`
- Test: `skills/korean-ebook-typst/tests/test_infographic_cli.py`

**Interfaces:**
- Consumes: Task 2~8 (parse/layout/lint/emit), `styles/<pack>/tokens.json`
- Produces:
  - `cli.main(argv) -> int` — 서브커맨드:
    - `lint <ch.md> [--style practical]`: 챕터 md에서 펜스 추출(`md2typst.extract_fences`) → parse → layout → lint. findings 전건을 stderr에 리포트 형식으로 출력, 있으면 exit 1, 없으면 `OK (N fences)` exit 0. **렌더 없음.**
    - `preview <ch.md> --fig 2 [--style practical] [--out out.pdf]`: 해당 펜스만 standalone 1페이지 PDF. 임시 디렉터리에 `tokens.json`+`helper.typ`+`fig.typ`를 `build/`와 동일 배치(helper는 fig 상위 디렉터리)로 복사해 컴파일. 챕터 md의 다른 내용은 포함하지 않는다.
  - 사용법 문자열은 `--help`에 위 계약 그대로.

- [ ] **Step 1: 실패 테스트 작성**

```python
"""test_infographic_cli.py — 스펙 §5.5: lint/preview 단독 실행."""
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[1]
CLI = SKILL / "scripts" / "infographic" / "cli.py"
from scripts.build import typst_binary                # noqa: E402
TYPST = typst_binary()

MD = """## 장

원문에 5단계가 있다.

```infographic
{"layout": "flow", "title": "5단계 수렴", "evidence": "§1", "steps": [
  {"title": "접수", "text": "등록"},
  {"title": "폐쇄", "text": "확정"}
]}
```
"""


def test_lint_ok_exit_zero(tmp_path):
    ch = tmp_path / "ch01.md"; ch.write_text(MD, encoding="utf-8")
    r = subprocess.run([sys.executable, str(CLI), "lint", str(ch)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert "OK" in r.stdout and "1" in r.stdout


def test_lint_violation_exit_one_with_report(tmp_path):
    ch = tmp_path / "ch01.md"
    ch.write_text(MD.replace("5단계 수렴", "9단계 수렴"), encoding="utf-8")  # 원문엔 9 없음
    r = subprocess.run([sys.executable, str(CLI), "lint", str(ch)], capture_output=True, text=True)
    assert r.returncode == 1
    assert "number-evidence" in r.stderr and "ch01.md #1" in r.stderr


@pytest.mark.skipif(not TYPST, reason="typst 없음")
def test_preview_compiles_single_fig(tmp_path):
    ch = tmp_path / "ch01.md"; ch.write_text(MD, encoding="utf-8")
    out = tmp_path / "fig.pdf"
    r = subprocess.run([sys.executable, str(CLI), "preview", str(ch), "--fig", "1",
                        "--out", str(out)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert out.exists() and out.stat().st_size > 1000
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `cd /mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook-typst && python3 -m pytest tests/test_infographic_cli.py -v`
Expected: FAIL — cli.py 없음

- [ ] **Step 3: 최소 구현**

```python
#!/usr/bin/env python3
"""cli.py — 인포그래픽 단독 검증(스펙 §5.5). 책 전체 빌드 없이 도식 하나를 검사·렌더."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from md2typst import extract_fences                     # noqa: E402
from build import typst_binary                          # noqa: E402 — 탐지 단일화(Global Constraints)
from infographic import emit, layout, lint              # noqa: E402
from infographic.parse import ParseError, parse_fence   # noqa: E402


def _tokens(style: str) -> dict:
    p = SKILL_DIR / "styles" / style / "tokens.json"
    if not p.exists():
        raise SystemExit(f"스타일 팩 없음: {style}")
    return json.loads(p.read_text(encoding="utf-8"))


def _load(md_path: Path, style: str):
    md = md_path.read_text(encoding="utf-8")
    _, fences_raw = extract_fences(md)
    tokens = _tokens(style)
    fences = [parse_fence(r["index"], r["line"], r["body"]) for r in fences_raw]
    figs = {f.index: layout.dispatch(f, tokens) for f in fences}
    return md, fences, figs, tokens


def cmd_lint(md_path: Path, style: str) -> int:
    md, fences, figs, tokens = _load(md_path, style)
    findings = lint.check(fences, figs, tokens, md, md_path.name)
    if findings:
        print(lint_report(findings), file=sys.stderr)
        return 1
    print(f"OK ({len(fences)} fences)")
    return 0


def lint_report(findings) -> str:
    lines = ["[I1] 위반 — 전건:"]
    lines += [f"  [{f.kind}] {f.loc} — {f.measured} → 제안: {', '.join(f.levers)}"
              for f in findings]
    return "\n".join(lines)


def cmd_preview(md_path: Path, fig_no: int, style: str, out: Path) -> int:
    md, fences, figs, tokens = _load(md_path, style)
    if fig_no not in figs:
        print(f"펜스 #{fig_no} 없음 (존재: {sorted(figs)})", file=sys.stderr)
        return 2
    findings = lint.check(fences, figs, tokens, md, md_path.name)
    keep = [x for x in findings if f" #{fig_no} " in x.loc]
    if keep:
        print(lint_report(keep), file=sys.stderr)
        return 1
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        igdir = tdp / "infographic"; igdir.mkdir()
        (tdp / "tokens.json").write_text(json.dumps(tokens, ensure_ascii=False), encoding="utf-8")
        shutil.copy2(SKILL_DIR / "templates" / "infographic" / "helper.typ", tdp / "helper.typ")
        f = next(x for x in fences if x.index == fig_no)
        (igdir / "fig.typ").write_text(
            emit.render_typ(figs[fig_no], tokens), encoding="utf-8")
        # 1페이지: 판형 크기 페이지에 도식 하나를 상단 배치
        main = (igdir / "fig.typ").read_text(encoding="utf-8")
        page = (f'#set page(width: {tokens["trim"]["width_mm"]}mm, '
                f'height: {tokens["trim"]["height_mm"]}mm, margin: 12mm)\n'
                '#set text(font: ' + json.dumps(tokens["fonts"]["body"]["stack"], ensure_ascii=False)
                + f', size: {tokens["fonts"]["body"]["size_pt"]}pt, lang: "ko")\n'
                + main)
        (igdir / "fig.typ").write_text(page, encoding="utf-8")
        r = subprocess.run([typst_binary(), "compile",
                            str(igdir / "fig.typ"), str(out), "--root", str(tdp)],
                           capture_output=True, text=True, timeout=120)
        if r.returncode != 0:
            print(r.stderr, file=sys.stderr)
            return 3
    print(f"preview → {out}")
    return 0


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="infographic")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("lint", help="I1 린트만 (렌더 없음)")
    p1.add_argument("md"); p1.add_argument("--style", default="practical")
    p2 = sub.add_parser("preview", help="펜스 1개 standalone PDF")
    p2.add_argument("md"); p2.add_argument("--fig", type=int, required=True)
    p2.add_argument("--style", default="practical"); p2.add_argument("--out", default="fig-preview.pdf")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "lint":
            return cmd_lint(Path(a.md), a.style)
        return cmd_preview(Path(a.md), a.fig, a.style, Path(a.out))
    except ParseError as e:
        print(f"[parse] 펜스 {e.fence_index}: {e.detail}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: 테스트 통과 확인**

Run: `cd /mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook-typst && python3 -m pytest tests/test_infographic_cli.py -v`
Expected: PASS (preview는 typst 있을 때만)

- [ ] **Step 5: 커밋**

```bash
git add skills/korean-ebook-typst/scripts/infographic/cli.py skills/korean-ebook-typst/tests/test_infographic_cli.py
git commit -m "feat: infographic CLI — lint/preview 단독 실행"
```

---

### Task 11: 저작 가이드 최소판 + SKILL.md 갱신 + 전체 회귀

**Files:**
- Create: `skills/korean-ebook-typst/references/infographic/authoring.md`
- Modify: `skills/korean-ebook-typst/SKILL.md` (워크플로우 섹션에 인포그래픽 사용법 요약 10줄 내외)
- Test: 기존 전체 스위트 (신규 테스트 파일 없음 — 문서 Task)

**Interfaces:**
- Consumes: Task 1~10 전부 확정된 계약
- Produces: 저작 가이드 — 라우팅 표(Phase 1: flow 행만, 나머지 Phase 2~4 예정 표기), 펜스 JSON 스키마 전문, CLI 사용법, 예산 치트시트(practical 기준 수치), 검수 절차

- [ ] **Step 1: authoring.md 작성**

필수 섹션(전문은 구현 시 작성하되 아래 골격의 모든 항목을 채운다 — 빈 항목 남기면 이 Task 실패):

```markdown
# 인포그래픽 저작 가이드 (Phase 1 — flow)

## 언제 도식을 넣나
- 장의 핵심 흐름이 2~8단계 순차 절차일 때 flow 1개.
- 라우팅 표: | 콘텐츠 신호 | layout | 상태 |
  | 순차 단계·절차·전환 | flow | Phase 1 사용 가능 |
  | (cards/matrix/… 8종 | Phase 2~4 예정) |

## 펜스 규약
- 언어 `infographic`, 내용 JSON. 위치가 곧 삽입 위치.
- 필수: layout, title(결론형), steps 2~8({title, text}).
- 선택: thesis, kicker, note, evidence("§N" — 같은 챕터 N번째 ## 절).
- 근거 경계: 모든 문구는 원문에 대응. 숫자는 evidence 필요(자동 교차검증).

## 예산 치트시트 (practical 기준 초기값 — 골든 교정 전)
- 카드 제목(11pt): 줄당 KO ~10자 · 카드 본문(9pt): ~13자 · 도식 제목(13.5pt): ~22자
- 상한 근거: `(카드폭−16)×0.9 ÷ 크기pt` (스펙 §4.3 계수). 팩별 보정 계수는
  `scripts/infographic/budget.py: PACK_KO_FACTOR`(초기값 1.0).

## 골든 교정 절차 (스펙 §7 — Phase 1 수립, archetype 추가 시마다 반복)
1. fixture 펜스(치트시트 상한 근처 문구)를 `cli.py preview`로 팩별 렌더.
2. PDF에서 카드 텍스트 오버플로 한계를 눈검으로 실측(잘리는 시작 지점).
3. 실측/예상 비율을 `PACK_KO_FACTOR[팩]`에 반영하고 치트시트 표 갱신.
4. 골든 스냅샷 재확정: `IG_REGEN_GOLDEN=1 pytest` → 눈검 → 커밋.

## 도식 하나 만들기 (빌드 없이)
python3 scripts/infographic/cli.py lint <ch.md>          # I1만
python3 scripts/infographic/cli.py preview <ch.md> --fig 1   # 눈검 PDF

## 검수
- build/infographic/*.review.md 확인란 채우기 — 원문 대조.
- I1 "미검증" 플래그는 사람 대조 필수.
```

- [ ] **Step 2: SKILL.md 갱신**

`## 워크플로우` 섹션 뒤에 짧은 섹션 추가(10줄 내외):

```markdown
## 챕터 도식 (인포그래픽 — Phase 1)

챕터 md에 ```infographic 펜스(JSON)를 넣으면 출판 품질 벡터 도식이 그
자리에 삽입된다. Phase 1 layout: `flow`(순차 2~8단계). 좌표는 Python이
계산하고 I1 린트(텍스트 예산·잉크 컨테인먼트·숫자-evidence 교차검증)를
통과해야 빌드된다. 도식 하나 검사·미리보기:
`python3 scripts/infographic/cli.py lint|preview …`. 저작 규약·라우팅 표는
`references/infographic/authoring.md`.
```

- [ ] **Step 3: 전체 회귀 + 수동 눈검**

Run: `cd /mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook-typst && python3 -m pytest tests/ -q`
Expected: 전부 PASS.

Run: Task 9의 tmp 책을 다시 빌드해 최종 PDF를 열고 스크린샷 수준으로 확인: 카드 2장, 제목, 고지 note, 화살표(가로), 페이지 안 잘림.

- [ ] **Step 4: 커밋**

```bash
git add skills/korean-ebook-typst/references/infographic/authoring.md skills/korean-ebook-typst/SKILL.md
git commit -m "docs: 인포그래픽 저작 가이드 최소판 + SKILL.md 요약"
```

---

## Phase 2~5 예고 (별도 플랜)

본 플랜 착지 후 작성: Phase 2(cards+matrix)·Phase 3(before_after+ladder+roadmap)·Phase 4(topology+approval+layers)·Phase 5(composite+가이드 완성+`infographic_pages` 리포트 필드). 각 플랜은 본 플랜의 Task 5 패턴(archetype 모듈+지오메트리 테스트+런타임 라우팅 등록)을 따른다.

## Self-Review 결과 (개정 2판)

- **적대 검토 22건 반영 확인**: A그룹(테스트↔구현 불일치 7건) — helper.typ 재작성(pt 셈·top+left rect·center+horizon 절대좌표 환산·open-V 절대 대각선), 배치 결정론 재합의(세로 제거·판형 상한+2행 랩·수학 검증 표기), Task 4 산수 2건 정정, Task 6 방출물/helper 단언 분리, Task 3 1차 마커 기대 정정. B그룹 — Task 7 배치 build/ 동일 구조, I1Error 할당 순서, `테스트책` 파일명, `sys.path.insert` 명시 코드 블록, `_esc @<>` 확장. C그룹 — I1 9항목: 커넥터 산술·판형 상한(§6.2)·펜스 위장·미검증 비치명·검수 시트 5열·qc_gate WARN·팩별 예산표 구조+교정 절차·ParseError/FlowLayoutError 전수 집계. D그룹 — 골든 IG_REGEN_GOLDEN 확정 절차, TextOp.field loc, typst_binary 단일화, timeout, FigModel 인터페이스 표기 통일.
- **스펙 커버리지**: §2(Task 3·9), §3(Task 2), §4(Task 1·4·5 — 팩별 계수·leading·크기 불변식), §5 I1 9항목(Task 8·9 — #6 복합은 Phase 5 이관), §6.2 상한표 flow 행(layout PACK_LIMITS), §6.3(Task 5), §7(각 Task TDD·Task 7 컴파일·Task 11 교정 절차), §8-Phase1(Task 1~11). `infographic_pages` 리포트 필드·상한표 잔여 종은 Phase 2~5 플랜 이관(스펙 §8 배분과 일치).
- **플레이스홀더 스캔**: "적절히/나중에/유사히" 류 없음. 골든 재확정·교정 절차가 절차문으로 정의됨.
- **타입 일관성**: `Fence` 필드 — Task 2 정의 = Task 5·8·9·10 소비. `FigModel(width,height,ops,source_index)`. `TextOp(…, max_w, field)` — Task 5 정의 = Task 8 소비. `render_book_fences(book_dir,build,cfg)` — Task 9. `_card_texts(…, idx, pack)`. emit import `#import "../helper.typ"` 전 Task 단일. `budget.line_count(…, pack=)`·`width_units(text, pack)` — Task 4 정의 = Task 5 소비. `check_review_sheets(build)` — Task 9 Interfaces = 구현 = 테스트.
- **잔여 위험(의도적 수용)**: helper.typ·flow.py의 방출 좌표는 계획 단계 산수이며 Task 7 컴파일·Task 9 눈검이 1차 검증한다. 골든 교정 전 예산표는 근사(스펙 §4.3 명시).
