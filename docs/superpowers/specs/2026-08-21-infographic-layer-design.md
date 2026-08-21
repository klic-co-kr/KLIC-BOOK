# korean-ebook-typst 인포그래픽 레이어 설계

- 날짜: 2026-08-21
- 상태: 승인 대기
- 범위: korean-ebook-typst 파이프라인에 챕터별 인포그래픽(도식) 생성 계층 추가

## 1. 배경과 목표

### 배경

- 구 WeasyPrint 스킬(korean-ebook)에는 8종 고정 레이아웃 시각 요약 계약
  (`references/visual-editorial-layer.md`)이 있었으나, 현행 파이프라인인
  korean-ebook-typst에는 이미지 통과(`![](path)` → `#figure(image())`)만 존재하고
  도식 저작 능력이 없다.
- 외부 스킬 skillstead `svg-infographic` v0.11.0을 검토했고(2026-08-21),
  설계 철학을 계승하되 도입(설치)하지 않고 자체 개발하기로 했다.
  - 계승 대상: "숫자 먼저" 레이아웃 산술, 기계 린트 게이트, 결론형 제목,
    텍스트 예산(한글 축소 계수), 색 역할 토큰, 복합 씬 상한, 검증 게이트 문화.
  - 미계승 대상: SVG 저작·Chromium 렌더·폰트 서브셋 임베딩(Node 의존,
    WSL2 미검증) — 책 PDF 안에서만 쓰므로 불필요.

### 목표

- 챕터 md 안에서 펜스 블록 한 개로 출판 품질 벡터 도식을 책 PDF에 삽입한다.
- 도식은 원고의 편집적 재배열이다 — 원문 근거를 벗어나지 않는다.
- 판형 5종(practical/essay/business/lecture/b5)에 자동 대응한다.
- 빌드 타임에 좌표·텍스트 예산을 산술로 증명하고, 위반은 빌드를 중단한다.

### 비목표

- 책 밖 재사용용 SVG/PNG 파일 출력 (슬라이드·SNS)
- 정량 통계 차트(막대·선·원형·히트맵) — 데이터 부정확 날조 위험, 금지
- 사진·일러스트·마스코트·브랜드 로고 제작
- 외부 패키지 의존(cetz 등) 추가

## 2. 아키텍처

korean-ebook-typst 안에 모듈로 추가한다(신규 스킬 아님).

```
skills/korean-ebook-typst/
  scripts/infographic/
    __init__.py      # render() 진입점
    parse.py         # ```infographic 펜스 → 데이터 모델 + 스키마 검증
    layout.py        # archetype별 격자 산술 → 좌표 모델
    lint.py          # 텍스트 예산·컨테인먼트·숫자-evidence 검사 (I1 게이트)
    emit.py          # 좌표 모델 → typst 코드 방출
    archetypes/      # 종류별 순수 함수(데이터+판폭 → 좌표): flow, cards, ...
  templates/infographic/helper.typ   # 색·폰트 공통 함수 (방출 코드가 참조)
  tests/
    test_infographic_parse.py
    test_infographic_layout_*.py     # archetype별
    test_infographic_lint.py
    test_infographic_emit.py         # 골든 스냅샷
    fixtures/infographic/            # 9종+복합 펜스 fixture
```

### 데이터 흐름

```
챕터 md 펜스 (```infographic ... ```)
  → md2typst.py가 펜스 추출 → parse.py (스키마 검증)
  → layout.py (격자 산술: 카드 폭·간격·마지막 엣지 증명)
  → lint.py 게이트 — 위반 시 빌드 중단 (측정값+수정 제안)
  → emit.py → build/infographic/chNN-figK.typ (정확 좌표 typst)
  → 펜스 자리에 #include → build.py 조립 → PDF (벡터)
```

### 핵심 원칙

1. **좌표는 전부 Python이 계산한다.** 방출된 typst는 칠하기만 한다
   (조건 분기·계산 없음). 같은 입력 = 같은 방출(결정론).
2. **텍스트 길이는 보수적 글자폭 표로 예산 검증.** 폰트 크기별
   한글 글자수/줄 상한표를 lint가 검사한다. 골든 렌더 테스트로
   표를 교정한다.
3. **archetype 라우팅은 저작 시점 선택.** 빌드 타임 자동판단 없음.
   SKILL.md의 라우팅 표를 보고 Claude(또는 사람)가 펜스에 `layout:`을
   명시한다. 도식은 원문의 편집적 재배열이라 콘텐츠 판단이 필요하고,
   빌드는 결정론을 유지해야 한다(style: auto와 대비되는 설계 의도).
4. **의존성 추가 없음.** 순수 Python 표준 라이브러리 + typst 바이너리.

## 3. 데이터 계약 (펜스 스키마)

### 공통 필드

```yaml
layout: process        # 필수. 9종 키워드 + composite
title: "결론형 제목"     # 주제 라벨 금지, 핵심 명제
kicker: "CHAPTER MAP"  # 선택
note: "..."            # 선택 — 기본값 원문 비대체 고지 문구
evidence: "ch01 §2"    # 숫자 규칙(아래) 충족용 근거 위치
```

### 9종 archetype별 데이터

| layout | 데이터 | 구시스템 대응 |
|---|---|---|
| `flow` | `steps[]`(title, text) 또는 `lanes[]`(actor, steps[]) — swimlane 변형 | process |
| `matrix` | `headers[]`, `rows[][]` — 또는 `x_axis`/`y_axis`/`cells[]` 정성 매트릭스 | matrix·quadrant |
| `cards` | `cards[]`(title, text, 선택 value) | principles·dashboard |
| `before_after` | `before[]`, `after[]`, `center` 라벨 | bridge |
| `ladder` | `stages[]` 3~5단 (하→상) | ladder |
| `layers` | `stack[]` 또는 `rings[]` (중첩 변형) | — |
| `roadmap` | `phases[]`(period, title, items) | — |
| `topology` | `nodes[]`, `edges[]` | network |
| `approval` | `path[]`, 게이트 표시 | — |

### 복합 씬

```yaml
layout: composite
modules:
  - { slot: primary,    layout: cards, ... }
  - { slot: supporting, layout: flow,  ... }
```

- 상한: 주 1 + 보조 1~2 (skillstead 계승)
- 공간 부족 시 보조 모듈 축소 또는 펜스 분할 — 글자·화살표 축소 금지

### 근거 경계 — 기계 검증과 사람 게이트 분리

1. **숫자 규칙(기계)**: 요소 텍스트에 숫자가 있으면 `evidence:` 필드
   필수. 없으면 lint 에러. 원문에 없는 숫자 날조를 빌드 타임에 차단한다
   (구시스템 최대 금지항목의 자동화).
2. **문구 대조(사람)**: 도식 문구가 원문에 대응하는지는 검수 절차에서
   사람이 확인한다. 대응 근거가 없으면 삭제하거나 원문 문구로 수정.
3. **정량 차트 금지**: archetype 세트 자체에 통계 차트가 없다.
   `value:` 표시값은 evidence가 명시될 때만 허용.

## 4. 판형·스타일 토큰

### 캔버스 = 책 계약 소비

- 도식 폭 = tokens.json `body_frame_pt` 폭(x1−x0). 판형 5종 자동 대응.
  좁은 판형에서는 격자 산술이 카드 열수를 줄인다(마지막 엣지 증명).
- 높이 = 콘텐츠 산출. body_frame 높이 85% 초과 시 lint 에러 →
  복합이면 모듈 분할 권고. 글자 축소로 해결하지 않는다.
- 폰트 = 책 폰트 계약 그대로(Pretendard 정적). 도식 전용 폰트 없음.
  G2 폰트 게이트가 구조적으로 상속된다.

### 색 — tokens.json에 `infographic` 섹션 추가

```json
"infographic": {
  "surface-tint": "#…", "focus": "#…", "positive": "#…",
  "warning": "#…", "on-focus": "#…"
}
```

- 기존 6색(paper/ink/ink-soft/ink-mute/rule/accent) 재사용 + 5역할 추가.
  skillstead 11역할의 책 축소판.
- emit은 토큰 참조만 허용, hex 하드코딩 금지 → 스타일 팩 교체 시
  도식도 자동 재색(skin resolver 개념 계승).
- 5개 팩 모두에 역할 정의 필수 — 없는 팩은 lint 에러.

### 타입 스케일

- 도식 제목 = 본문 H2급, 카드 제목 = 본문+1pt, 카드 본문 = 본문−1pt,
  캡션 = 기존 `label` 크기 재사용.
- 텍스트 예산표: 크기별 한글 글자수/줄 상한(skillstead "KO ≈ 라틴 60%"
  계승, 실측 표로 구체화하여 lint가 사용).

### 인쇄 제약 (ai-tells.md 연동)

- 색만의 구분 금지 — 색+모양 이중 코딩(solid/dashed 라인, 뱃지).
- tint 채도 절제, 무지개 구분색·gradient·이모지 금지.
- 헤어라인 최소 0.5pt.

## 5. 빌드 통합 + QC 게이트

### 게이트 2층

| 게이트 | 시점 | 검사 | 실패 시 |
|---|---|---|---|
| **I1** (신규 `lint.py`) | 빌드 중 emit 직전 | 스키마 · 텍스트 예산 · 컨테인먼트 산술(마지막 엣지 증명) · 숫자-evidence 규칙 · 복합 모듈 상한 · 토큰 존재 | 빌드 중단. 에러 메시지에 측정값+수정 제안 (예: "28자 > 예산 22자 — 글자 줄이거나 카드 폭 확장") |
| **기존 게이트 상속** | qc_gate | G1 판면 오버플로(도식도 본문 콘텐츠라 자동 적용) · G2 폰트(책 폰트만 사용해 구조적 통과) · G3 글자수 밴드(도식 블록은 집계 제외 — 비본문) | 기존 규칙 |

### 빌드 흐름 상세

```
build.py
  → md2typst 변환 중 ```infographic 펜스 감지
  → infographic.render(펜스YAML, style_tokens)
      parse → layout → lint → emit
      → build/infographic/chNN-figK.typ
  → 펜스 자리에 #include "infographic/chNN-figK.typ"
  → compile → PDF
```

- 방출 파일을 build/에 보존 → 골든 스냅샷 테스트·디버깅에 사용.
- 펜스 파싱 실패 에러는 챕터·라인·필드를 명시한다.
- 빌드 산물(build/·draft/·final/)은 기존처럼 gitignore.

## 6. archetype 지오메트리

### 공통 커넥터 규칙

- 화살표 = open-V 스트로크. 헤드 가시폭 ≈ 샤프트 굵기 3배.
- tip-gap 8~12pt, 샤프트 가시 ≥12pt — 좌표 계산 단계에서 증명.
- solid = 순차/요청, dashed = 비동기/참조(색+모양 이중 코딩).
- 커넥터 복도 산술: `복도 = 목표 좌 − 소스 우 − 마커 발판`.
  가독 샤프트가 안 남으면 compact 화살표·전환 글리프·재배치 중
  선택 — 렌더 후가 아니라 계산 단계에서.

### 종류별 배치 산술과 상한

| layout | 배치 산술 | 상한 |
|---|---|---|
| `flow` | 가로 n카드, 간격 24~32pt. 폭 부족 시 2행 랩 또는 세로 변형 | 단계 ≤8 |
| `flow`(swimlane) | 레인 행 × 순서 셀 | 레인 ≤4 |
| `cards` | n열 그리드 `(W−(n−1)g)/n` | 카드 ≤6 |
| `matrix` | 격자 rect — 신국판 4열 / A4 5열 | 5열×6행 |
| `before_after` | 좌우 패널 + 중앙 전환 화살표 | 항목 ≤5/측 |
| `ladder` | 계단식 — x·y 동시 증가 오프셋 | 3~5단 |
| `layers` | 수평 스택 기본, `rings` 동심원 변형 | ≤6층 |
| `roadmap` | 가로 타임라인 + 위상 밴드 | 위상 ≤5 |
| `topology` | grid 배치 기본. 방향 간선 있으면 계층(DAG 층위) 자동 배치 | 노드 ≤8 |
| `approval` | 가로 경로 + 게이트 다이아몬드 | 게이트 ≤4 |
| `composite` | 세로 슬롯 분할 — 주 모듈 상단(높이 ≥60%), 보조 하단. 슬롯 간 24pt. 각 모듈은 자체 archetype 산술 재사용 | 모듈 ≤3 (주 1 + 보조 1~2) |

## 7. 테스트 전략 (TDD)

- **단위**: archetype별 좌표 모델 pytest.
  예: process 4단계 → 카드 x 좌표 정확값, 마지막 엣지 ≤ 영역 우단.
- **골든**: emit typst 코드 스냅샷(결정론 검증).
- **통합**: 9종+복합 펜스를 담은 fixture 책 → build → PDF 생성·페이지 수 확인.
- **비주얼 스모크**: fixture PDF 페이지 PNG 렌더 → 사람 눈검수 절차 문서화
  (기존 검수 계약 연장). 텍스트 오버플로·화살표 충돌·잘림 확인.

## 8. 개발 순서 (단계별 증분, 각 단계 TDD)

1. **인프라 + flow** — parse/lint/emit 골격, tokens `infographic` 섹션
   5팩 추가, flow 1종으로 엔드투엔드 관통.
2. **cards + matrix** — 책 사용률 최상.
3. **before_after + ladder + roadmap**.
4. **topology + approval + layers(rings 변형)**.
5. **composite + SKILL.md 저작 가이드** — 라우팅 표(콘텐츠 신호→archetype),
   근거 경계, 펜스 규약, 검수 절차. 통합 테스트 마무리.

## 9. 결정 기록

| 결정 | 내용 | 대안과 거절 사유 |
|---|---|---|
| 출력 경로 | typst 네이티브 벡터 (책 PDF 안) | SVG→PNG: Node/Chromium 의존, WSL2 미검증, 인쇄 래스터화 — 책 전용이므로 불필요 |
| 데이터 위치 | 챕터 md 펜스 블록 | typst-build.yaml: 위치 고정·비대. 사이드카: 파일 2배 |
| 레이아웃 지능 | Python 계산 + raw typst 방출 | cetz: 외부 패키지 의존·린트 불가. typst 함수: 사전 검증 불가 |
| archetype 범위 | 9종 + 복합 (skillstead식 전체) | MVP 4종: 사용자 요청으로 전체 범위 선택 |
| 라우팅 시점 | 저작 시점 명시 (build 자동판단 없음) | style: auto식 빌드 판단: 콘텐츠 재배열 판단은 저작자 몫, 결정론 유지 |
