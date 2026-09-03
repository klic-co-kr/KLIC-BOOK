# 스타일 팩 저작 가이드

새 스타일 팩(`styles/<이름>/`)을 작성하는 절차. 스타일 = **숫자 계약(tokens.json) +
문서 계약(STYLE.md) + 렌더 규칙(theme.typ)** — 세 파일이 하나의 팩이다.

기존 4종 참조: `practical`(신국판 실용서)·`essay`(46판(B6) 산문)·`business`(백서판)·
`lecture`(A4 강의자료).

---

## 1. 파일 구성

### 1.1 tokens.json — 숫자 계약

모든 스타일이 동일 스키마를 공유한다. build.py가 `build/tokens.json`으로 복사해
base.typ가 `json()`으로 읽고, qc_gate.py가 G1 프레임·G2 폰트·G3 밴드의 기준으로 쓴다.

```json
{
  "style": "practical",
  "trim":       { "width_mm": 153, "height_mm": 225 },
  "margin":     { "top_mm": 22, "bottom_mm": 20, "inner_mm": 20, "outer_mm": 15 },
  "body_frame_pt": { "x0": 56.69, "y0": 62.36, "x1": 391.18, "y1": 581.10 },
  "label-top":  "",
  "fonts": {
    "body":     { "stack": ["Noto Serif CJK KR", "Noto Serif KR", "KoPubWorld바탕"],
                  "ps": ["NotoSerifCJKkr", "KoPubWorldBatang"], "size_pt": 10 },
    "heading1": { "stack": ["Noto Sans KR"], "size_pt": 18 },
    "heading2": { "stack": ["Noto Sans KR"], "size_pt": 13 },
    "label":    { "stack": ["Noto Sans KR"], "size_pt": 8.5 }
  },
  "leading_em": 1.7,
  "colors": { "paper": "#FFFFFF", "ink": "#1A1A1A", "ink-soft": "#3A3630",
              "ink-mute": "#6E6A66", "rule": "#DAD5CE", "accent": "#1F4E79" },
  "chars_per_line": { "min": 30, "max": 40 }
}
```

| 필드 | 용도 | 비고 |
|---|---|---|
| `style` | 스타일명 = 디렉터리명 | build.py 허용 목록 등록 필요(`STYLES` 튜플) |
| `trim` | 재단 크기 mm | base.typ page 설정 |
| `margin` | 판면 top/bottom/inner/outer mm | inner=안쪽(left), outer=바깥(right) |
| `body_frame_pt` | 본문 프레임 pt | **G1 검출 기준**. trim/margin 유도값과 일치해야 함: `x0=inner`, `y0=top`, `x1=width−outer`, `y1=height−bottom`(mm→pt = ×72/25.4) — frame/margin 정합성 유닛 테스트로 검증 |
| `label-top` | H1 위 라벨(예: business "SECTION") | 빈 문자열이면 미렌더. 하이픈 키는 theme.typ에서 `.at("label-top")` 접근 |
| `fonts.*` | role별 폰트 | `body`/`heading1`/`heading2`/`label` 4 role |
| `fonts.*.stack` | 1순위부터 나열 | **1순위는 빌드 머신에 설치된 폰트로** — 폴백 임베드 없이 G2가 성립. 하위 항목은 폰트 있는 환경용 후순위(미설치 경고는 무해) |
| `fonts.*.ps` | (선택) 임베드 PostScript명 별칭 | 스택 표기("KoPubWorld바탕")와 임베드명("KoPubWorldBatang")이 어긋나는 폰트를 G2 정규화 매칭에 등록. 실제 임베드되는 폰트가 바뀌면 여기에 추가 |
| `fonts.*.size_pt` | pt 크기 | |
| `leading_em` | 행간 em | |
| `colors` | paper·ink·ink-soft·ink-mute·rule·accent | 하이픈 키는 theme.typ에서 `.at()` 접근 |
| `chars_per_line` | G3 밴드(min/max 자/줄) | **판형별 물리값** — 판면 폭 × 본문 pt의 전각 환산 기준(예: 신국판 118mm 10pt ≈ 33자 → 30–40). 전 스타일 공유 값 아님 |

### 1.2 STYLE.md — 문서 계약

사람이 읽는 규칙서. 섹션 구성(4종 공통):

1. **정체성** — 판형, 장르, 타이포그래픽 성격(명조/고딕, 위계 수단)
2. **규칙** — 판면 수치, 본문/헤딩/쪽번호 스펙, G3 밴드와 그 물리 근거
3. **폰트 계약 참고** — 스택 순위의 이유, ps 별칭 등록 근거, 폴백 시 G2 대응
4. **금지 사항** — 자간 조정, 배경색 박스(허용 지점 명시 시 예외 표기), 크기 하한 등
5. **근거 표기** — 수치 출처(설계 참고값인지 우리 실측인지) — 우리 책 빌드 축적 후 치환

### 1.3 theme.typ — 렌더 규칙

**반드시 `#let theme(body) = { show ...; body }` 함수 패턴**을 쓴다. typst 0.15+에서
set/show 규칙은 include된 파일 스코프에만 적용되므로, 베어 `#show` + `#include`는
본문에 전파되지 않는다. build.py가 생성하는 main.typ이 `#show: base` 다음 `#show: theme`
로 적용한다(base가 먼저, theme이 나중 — 나중 규칙이 헤딩을 오버라이드).

```typst
#import "base.typ": tokens, pt, mm, em   // 필요한 헬퍼만

#let theme(body) = {
  show heading.where(level: 1): it => { ... }   // theme 고유 H1
  show heading.where(level: 2): it => { ... }   // theme 고유 H2
  body
}
```

실측으로 얻은 작성 규칙:

- 하이픈 키(`label-top`, `ink-mute`)는 `tokens.at("label-top")` 접근 — dot-access는 마이너스 파싱 실패
- show 규칙 내부 코드 모드에서 `#line(...)`처럼 `#` 접두를 붙이면 컴파일 에러 — `line(...)`으로
- 표지 오버라이드는 base의 `make-cover` 기본형을 그대로 쓰거나 theme에서 별도 정의
- 목차 커스텀은 `show outline.entry`(0.15+ entry 필드는 level/element/fill뿐 — 엔트리 재구성 필요. essay 참조)
- 자간 `tracking` 조정 금지(공통 금지 사항)

---

## 2. 작성 순서

1. **tokens.json** — 판형·판면·폰트·밴드 결정. body_frame_pt는 margin/trim 유도값으로 계산
2. **theme.typ** — H1/H2(필요시 outline) 규칙. `theme(body)` 함수 패턴
3. **STYLE.md** — 규칙·근거 문서화
4. **스모크 테스트**(§3) → 5. **핵심 심볼 프로브**(§4) → 6. **aesthete 게이트**(§5) → 7. VERSION bump(§7)

실패 시 게이트가 지적하는 면만 수정해 재실행한다.

---

## 3. 스모크 테스트

`tests/test_style_<이름>.py` — 기존 4종(`test_style_practical.py` 등) 구조를 따른다:

1. **frame/margin 정합 유닛**: body_frame_pt == trim/margin 유도값(mm→pt, abs=0.05)
2. **폰트 계약 유닛**: `qc_gate.allowed_fonts(tokens)`에 스택 정규화명·ps 별칭 포함
3. **스모크**: fixture 복사 → `load_config` → `assemble` → `compile_pdf` → `check_overflow == []`
4. **QC 풀 패스**: `qc_gate.run()` → final/ 생성, G3 WARN 확인

```bash
cd skills/korean-ebook && python3 -m pytest tests/test_style_<이름>.py -v
```

(typst 미설치 환경은 skip. 전체 스위트 회귀도 실행 — 기존 테스트 깨지지 않는지.)

### fixture의 알려진 한계 — 스위트가 H2(`==`)를 만들지 못한다

md2typst 매핑이 `#`·`##` **둘 다** `=`(H1)로 변환하므로(원고 규약상 장 제목은 `##`,
`#`는 원고에 없다는 전제), `tests/fixtures/sample-manuscript/`의 `## 절 제목`이 H1으로
렌더된다. fixture에 `###`가 없어 `==`(H2) 헤딩이 변환 결과에 전혀 등장하지 않는다.

따라서 **H2 스타일(business의 navy 배경 박스 등)은 스위트 테스트로 검증되지 않는다** —
반드시 다음 §4 프로브로 보완한다.

---

## 4. 핵심 심볼 프로브 검증

스위트가 발동 못 시키는 심볼(H2 박스, 라벨, 괘선 등)은 **독립 .typ 프로브를 컴파일해
PDF에서 직접 측정**한다. business H2 박스 검증 실측 예:

```bash
mkdir -p /tmp/style-check-<이름>/h2probe && cd /tmp/style-check-<이름>/h2probe
# tokens.json, theme.typ, base.typ 복사 후 프로브 typ 작성:
#   #import "base.typ": base
#   #import "theme.typ": theme
#   #show: base; #show: theme
#   == 박스가 렌더되는지 확인할 절 제목
typst compile probe.typ probe.pdf --root .
python3 -   # fitz로 rect fill 색·inset·텍스트 색/크기 실측 (styles/*/tokens 계약값과 대조)
```

프로브는 스크래치북에서만(커밋 X). 판정: fill 색 = accent 헥스, 텍스트 색·size_pt,
inset이 계약값과 일치하는지. 프로브로 검증된 사실은 STYLE.md 또는 저작 기록에 남긴다.

---

## 5. aesthete 저작 게이트

스타일 팩 완성 후 기하 검사. **텍스트 축 측정·aislop은 aesthete v1 한계로 이 경로에서
제외된다**(§6) — 검사 대상은 기하(collision·balance 등 측정 가능 축).

```bash
# 5-1. 스크래치북에 QC PASS 책 빌드 후 SVG 샘플 렌더 (파일명 템플릿 {p} — 실증됨)
cd /tmp/style-check-<이름>/book/build
typst compile main.typ sample-{p}.svg --root . --pages 1-4 && cd -
# 표지(1)·목차(2)·장 시작(3)·본문(4) 면 확보

# 5-2. intent brief 작성 /tmp/style-check-<이름>/brief.json
#      주의: 키는 "brief" (스키마에 goal 없음 — additionalProperties: false 거부됨)
{
  "artifact_type": "report",
  "format": "svg",
  "brief": "<이 스타일 페이지의 검증 목표 한 문장>",
  "must_preserve": ["body_frame_pt 판면 내 모든 콘텐츠", "헤딩-본문 결속"],
  "must_not_assume": ["텍스트 기반 가독성 지표"]
}

# 5-3. aesthete 실행 (aesthete 스킬 디렉터리에서, bun 필요)
cd ~/.claude/skills/aesthete
bun lib/skill-pre.mjs /tmp/style-check-<이름>/brief.json --out-dir /tmp/style-check-<이름>/PRE
for p in 1 2 3 4; do
  bun lib/skill-post.mjs /tmp/style-check-<이름>/book/build/sample-$p.svg \
    --contract /tmp/style-check-<이름>/PRE/contract.json \
    --intent /tmp/style-check-<이름>/PRE/intent.json \
    --out-dir /tmp/style-check-<이름>/POST-$p
done
```

**판정 분기**: 전 면 `hardIntegrity=1.0`이면 통과. 위반이면:

- **측정 아티팩트/규칙-범주 불일치** → §6 예외 규칙에 따라 기록으로 종결
- **실결함** → theme.typ/tokens.json 수정 후 5-1부터 재실행
- `fix_geometry`의 fix_cmd(SVG 변형) 자동 적용 **금지** — typst 소스 역추적 불가

---

## 6. 예외 규칙 · v1 한계

### 예외: SVG 링크 히트영역 rect = 측정 아티팩트

`link()`가 SVG 내보내기에서 글리프보다 큰 **투명 히트영역 rect**(실측 26pt)를 만들어
인접 요소와 P0 collision으로 판정될 수 있다. 히트영역은 잉크가 아니므로 이는 collision
측정의 아티팩트다. **P0로 판정되어도 링크 제거가 아닌 예외 기록으로 종결**한다.
(단, 링크를 새로 도입한 결과 hard 회귀가 생겼다면 — essay 사례 — 소스에서 링크를
제거하거나 예외를 명시적으로 기록할지 판단한다. 인쇄 우선 판형은 링크 제거가 기본.)

### 예외: 목차 balance.BM = 규칙-범주 불일치

BM 광학 균형(대시보드/마케팅 프로필 기대치)은 책 목차 면의 읽기 중심 의도적 비대칭과
범주가 다르다. 제안 fix("shift-heaviest toward center")는 판면 고정 계약(body_frame_pt)과
양립 불가. **기록 종결** — 무점선 목차 재구성(essay)이 측정 축도 개선할 수 있으므로
1회 시도는 유효.

### aesthete v1 한계 (이 경로에서 제외되는 검사)

- **텍스트 축 측정 불가**: typst SVG는 글리프가 path라 fluency/hierarchy/proximity/
  similarity가 전부 CONTRACT_UNMEASURABLE → human 분기. 게이트의 실질 검사 대상은
  기하 축(collision·balance)뿐
- **aislop(slop) 검사는 HTML 전용** — SVG 경로에서 동작 안 함
- **fix_geometry 부적용**: fix는 SVG 파일 직접 변형이어서 typst 소스로 역추적 불가
- **regenerate 무의미**: 빌드가 결정론적 컴파일이라 재생성은 같은 출력 — 재생성 루프 미진입

---

## 7. VERSION bump

`skills/korean-ebook/VERSION`(현재 0.1.0). 스타일 팩 추가·계약 변경(스키마 필드·
밴드·폰트 계약)시 patch bump(0.1.0 → 0.1.1). 문서만의 변경은 bump 불필요.

---

## 8. 완료 체크리스트

- [ ] tokens.json — frame/margin 정합, 설치 폰트 1순위, ps 별칭, 판형별 G3 밴드
- [ ] theme.typ — `theme(body)` 함수 패턴, `.at()` 하이픈 접근, `#` 접두 없는 코드 모드
- [ ] STYLE.md — 5 섹션 + 근거 표기
- [ ] 스모크 테스트 PASS + 전체 스위트 회귀 PASS
- [ ] 핵심 심볼 프로브(H2 등 스위트 미커버 심볼) 실측 검증
- [ ] aesthete 게이트 — 전 면 hard 1.0 또는 예외 기록 종결
- [ ] VERSION bump
