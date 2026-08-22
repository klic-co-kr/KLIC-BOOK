# korean-ebook-typst 인포그래픽 레이어 설계 (개정 6판)

- 날짜: 2026-08-21 (초판) / 2026-08-21 (개정 2판 — 적대 검토 3관점 24건 반영) / 2026-08-22 (개정 3판 — 구현 계획 적대 검토 반영 정합화) / 2026-08-22 (개정 4판 — Phase 2 플랜 적대 검토) / 2026-08-22 (개정 5판 — Phase 4 플랜·ladder 단계 상한 정식화) / 2026-08-22 (개정 6판 — Phase 5 플랜·composite 축소 제거·에러 스키마 확정)
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
  - 계승: "숫자 먼저" 레이아웃 산술, 기계 린트 게이트, 결론형 제목,
    텍스트 예산, 색 역할 토큰, 복합 씬 상한, 검증 게이트 문화.
  - 미계승: SVG 저작·Chromium 렌더·폰트 서브셋 임베딩(Node 의존,
    WSL2 미검증) — 책 PDF 안에서만 쓰므로 불필요.

### 목표

- 챕터 md 안에서 펜스 블록 한 개로 출판 품질 벡터 도식을 책 PDF에 삽입한다.
- 도식은 원고의 편집적 재배열이다 — 원문 근거를 벗어나지 않는다.
- 판형 5종(practical/essay/business/lecture/b5)에 자동 대응한다.
- 빌드 타임에 좌표·텍스트 예산을 **기계 검증 가능한 범위까지** 산술
  검사하고, 위반은 빌드를 중단한다. 근사의 한계는 아래 §4.3에 명시한다.

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
    parse.py         # 펜스 → 데이터 모델 + 스키마 검증(엣지 상태 포함, §3.4)
    layout.py        # archetype별 격자 산술 → 좌표 모델
    lint.py          # I1 게이트(§5.2) — 전수 검사·리포트 중단
    emit.py          # 좌표 모델 → typst 코드 방출 (래퍼 계약 §5.1)
    cli.py           # infographic lint <ch.md> / infographic preview <ch.md> --fig K
    archetypes/      # 종류별 순수 함수(데이터+판폭 → 좌표): flow, cards, ...
  templates/infographic/helper.typ   # 색·폰트 공통 함수
  references/infographic/
    authoring.md     # 저작 가이드: 라우팅 표·스키마·예산 치트시트(§8 각 Phase 동반 갱신)
  tests/
    test_infographic_parse.py
    test_infographic_layout_*.py     # archetype별
    test_infographic_lint.py
    test_infographic_emit.py         # 골든 스냅샷
    fixtures/infographic/            # 9종+복합 펜스 fixture
```

### 데이터 흐름 (실제 조립 구조에 맞춤 — 개정판 핵심 수정)

현행 구조 사실: build.py는 md2typst를 **챕터별 서브프로세스**로 실행하고
챕터 인덱스 prefix는 변환 **후** 개명한다. md2typst는 tokens.json을
읽지 않는다. 따라서 렌더 주체는 **build.py**다.

```
[1] md2typst.py (기존 CLI에 --fences-out <path> 인자 추가)
      변환 스텝 0.5(코드펜스 stash) 이전에 ```infographic 펜스를 먼저 추출:
        - 펜스 자리 → 플레이스홀더 문자열 ⟦IG:NN⟧ (NN=챕터 내 펜스 순번)
        - 플레이스홀더는 stash_str() 플레이스홀더로 보호
          (step 6 '#' 이스케이프가 #include 를 깨는 것을 원천 차단 — 실험 실증됨)
        - 펜스 JSON 원문 + 순번을 --fences-out 사이드 파일에 기록
[2] build.py
      각 챕터 변환 후 사이드 파일 수집 → infographic.render(펜스, style_tokens, idx)
        parse → layout → lint(I1) → emit
        → build/infographic/chNN-figK.typ 방출 + 검수 시트 chNN-figK.review.md (§5.4)
      조립 시 .typ의 ⟦IG:NN⟧ 플레이스홀더를
        #include "../infographic/chNN-figK.typ" 로 치환
        (챕터 .typ은 build/typ/에 있으므로 ../ — rebase_images의 ../assets/ 선례,
         infographic/ 상대경로는 실험에서 file not found 확인됨)
      assemble()에 helper.typ 복사 추가 + build/infographic/ rmtree 리셋 추가
        (stale emit 잔존 방지 — 스냅샷·디버깅 오염 차단)
[3] compile → PDF (도식은 벡터)
```

### 핵심 원칙

1. **좌표는 전부 Python이 계산한다.** 방출된 typst는 칠하기만 한다
   (조건 분기·계산 없음). 같은 입력 = 같은 방출(결정론). 배치 변형
   선택도 규칙으로 고정한다(§6 — "랩 또는 세로" 같은 자유 재량 금지).
2. **텍스트 폭은 근사다.** Python은 폰트 메트릭을 직접 읽지 않고
   팩별 예산표(§4.3)로 검증한다. 이는 "증명"이 아니라 골든 교정된
   근사이며, 오차 마진과 검증 한계를 명시한다(§4.3, §5.2).
3. **archetype 라우팅은 저작 시점 선택.** 빌드 타임 자동판단 없음.
   SKILL.md 라우팅 표를 보고 Claude(또는 사람)가 펜스에 `layout:`을
   명시한다. 빌드는 결정론을 유지한다.
4. **의존성 추가 없음.** 순수 Python 표준 라이브러리 + typst 바이너리.

## 3. 데이터 계약 (펜스 스키마)

**저작 형식 확정(개정 3판)**: 펜스 언어는 `infographic`, 내용은 **JSON**이다.
§2 원칙 4(의존성 추가 없음)와 YAML 파싱(비표준 파서 의존)이 양립하지
않는 내재 모순을 JSON으로 해소한다. 초판·2판의 YAML 표기는 전부 JSON으로 읽는다.

### 3.1 공통 필드

```json
{
  "layout": "flow",          // 필수. 9종 키워드 + composite (§3.5 별칭 참조)
  "title": "결론형 제목",      // 필수. 주제 라벨 금지, 핵심 명제
  "thesis": "한두 문장 설명",   // 선택 (구시스템 계승)
  "kicker": "CHAPTER MAP",   // 선택. 영문 또는 짧은 한국어
  "note": "...",             // 선택. 기본값 아래 고정 원문 사용
  "evidence": "§2"           // 숫자 규칙(§3.3)용 근거 앵커 — 같은 챕터 내 헤딩
}
```

기본 고지문(note 생략 시): "편집 요약: 본문의 장·절 구조와 핵심 문장을
재배열한 도식이며, 원문을 대체하지 않습니다."

### 3.2 9종 archetype별 데이터

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

**요소 수 하한·상한** (판형 조건부 상한은 §6.2):

| layout | 하한 | 절대 상한 |
|---|---|---|
| flow steps | 2 | 8 (swimlane 레인 2~4) |
| cards | 2 | 6 |
| matrix | 2열×2행 | 5열×6행 |
| before_after | 항목 1/측 | 5/측 |
| ladder | 3 | 5 |
| layers | 2 | 6 |
| roadmap | 2 | 5 위상 |
| topology | 노드 3 | 8 |
| approval | 경로 3 | 게이트 4 |

### 3.3 근거 경계 — 기계 검증 범위 명시

**숫자 규칙(기계, I1)**:

1. 검사 대상: `title`·`kicker`·각 요소의 `title`/`text`/`value`·표
   `headers`·`rows`·정성 매트릭스 축 라벨(`x_axis`/`y_axis`의 low·high)
   ·swimlane `actor`(개정 4판). `note`·`thesis`는 제외(편집자 문구).
2. 숫자 토큰 렉시콘: `[0-9][0-9.,%]*` (아라비아숫자 시작 — "3", "50%",
   "1.5", "v0.11"의 "0.11"). 한글 수사(삼, 셋), 원형 숫자(①),
   "제N장/제N절"의 서수는 **면제 렉시콘**으로 제외.
3. 숫자 토큰이 있으면 `evidence:` 필드 필수 (펜스 단위 1개).
4. **교차검증**: evidence 앵커가 같은 챕터 md 내 헤딩(또는 장 전체)을
   가리키면, lint가 해당 원문 범위에 각 숫자 토큰이 **부분 문자열로
   존재**하는지 검사한다. 존재하지 않으면 I1 에러 — 가짜 evidence·
   원문 부재 숫자를 빌드 타임에 차단한다. 앵커 해석 불가·범위 밖
   인용(다른 챕터)이면 검사를 건너뛰고 **검수 시트에 "미검증" 플래그**를
   남긴다(사람 게이트로 이관, 무음 통과 금지).

**사람 게이트(검수 시트로 집행 — §5.4)**: 문구의 원문 대응은 기계가
증명 못 한다. 검수 시트 + 완료 표시로 집행 장치를 둔다.

**정량 차트 금지**: archetype 세트에 통계 차트가 없다. `value:` 표시값은
숫자 규칙의 교차검증 대상이다.

### 3.4 파싱 상태 계약 (거부·기본값·정규화)

거부(I1 에러): unknown `layout` 키워드 · `title` 누락 · 요소 수
하한 미만/상한 초과 · 빈 펜스 · composite에서 `slot` 누락·오타 ·
composite 보조 모듈의 재귀 composite.

별칭 수용(경고 로그, 자동 변환 — 구시스템 마이그레이션):
`process`→flow · `bridge`→before_after · `quadrant`→matrix(정성 변형) ·
`principles`/`dashboard`→cards · `network`→topology.

정규화: BOM 제거, CRLF→LF(/mnt/d Windows 편집 현실).
JSON 파싱 실패·빈 펜스: 챕터·펜스 순번·라인·키 경로 명시.

### 3.5 복합 씬

```json
{
  "layout": "composite",
  "modules": [
    { "slot": "primary",    "layout": "cards", "…": "…" },
    { "slot": "supporting", "layout": "flow",  "…": "…" }
  ]
}
```

- 상한: 주 1 + 보조 1~2. 보조 모듈의 composite 금지.
- 최상위 title/kicker는 선택(모듈이 각자 아키타입 헤더를 렌더한다 — 모듈
  title은 각 아키타입 스키마 준수).
- 모듈 layout에 composite는 전 슬롯(primary 포함) 금지.
- 슬롯 배치: 세로 분할, 슬롯 간 24pt. 주 모듈 기본 60% — 단 **주 모듈
  콘텐츠 산출 높이가 60% 미만이면 실측치를 쓰고 잔여를 보조에 배분**
  (높이=콘텐츠 산출 원칙이 우선, 60%는 상한선).
- 공간 부족 시: **모듈 단위 분할 에러**(자동 축소 없음 — 글자·화살표
  축소 금지와 모순되는 레버가 없다. 개정 6판).
  메시지 스키마: `{모듈 슬롯} {layout} 측정높이 {h}pt > 배분 {H}pt
  — 보조 모듈 n을 별도 펜스로 분할 권장`(보조) /
  `… — 주 모듈 요소 수 감소 또는 펜스 분할 권장`(주).

## 4. 판형·스타일 토큰

### 4.1 캔버스 = 책 계약 소비

- 도식 폭 = tokens.json `body_frame_pt` 폭(x1−x0). 판형별 실측:
  essay 249.45 / practical 334.49 / b5 385.51 / business 453.55 /
  lecture 464.88 pt. 좁은 판형에서는 격자 산술이 카드 열수를 줄인다.
- 높이 = 콘텐츠 산출. body_frame 높이 85% 초과 시 I1 에러 → 모듈
  분할 권고. 글자 축소로 해결하지 않는다.
- **폰트 = 책 폰트 계약 그대로** (팩별 1순위: practical/b5=Freesentation,
  essay=SUIT, business=Wanted Sans Std, lecture=Pretendard — 정적 폰트
  계약은 유지되나 팩마다 다르다. 초판의 "Pretendard 정적" 일괄 문구는
  오류이므로 폐기). G2 폰트 게이트가 구조적으로 상속된다.

### 4.2 색 — tokens.json에 `infographic` 섹션 5역할 추가

```json
"infographic": {
  "surface-tint": "#…", "focus": "#…", "positive": "#…",
  "warning": "#…", "on-focus": "#…"
}
```

- 기존 6색(paper/ink/ink-soft/ink-mute/rule/accent) 재사용 + 5역할.
- emit은 토큰 참조만 허용, hex 하드코딩 금지 → 팩 교체 시 자동 재색.
- 5개 팩 모두 정의 필수 — 없는 팩은 I1 에러. 각 팩의 5역할 값 설계는
  Phase 1 과업(토큰 파일에 값 명시까지가 Phase 1 완료 조건).

### 4.3 타입 스케일·텍스트 예산 — 근사의 명시

- 도식 제목 = 본문 H2급 · 카드 제목 = 본문+1pt · 카드 본문 = 본문−1pt ·
  캡션 = 기존 `label` 크기. **예외**: H2 크기가 본문과 ±0.3pt 이내인
  팩(essay, H2=10pt=본문)은 도식 제목을 **본문+1.5pt**로 대체한다(개정
  3판 기록 — G3 불변식 유지가 목적).
- **도식 텍스트 크기는 본문 크기와 ±0.3pt 차이가 보장되도록 설계**한다
  (G3 글자수 밴드 필터가 도식 텍스트를 우연이 아닌 설계로 제외시키는
  불변식 — I1이 emit 결과 ops에서 검증).
- **leading**: 도식 텍스트는 emit이 `1.3em`을 명시 방출한다(본문
  1.7em 상속 차단 — 카드 높이 남계산 방지, 실험 실증 반영).
  세로 예산 공식: `줄수 × (크기 × 1.3) + 상하 패딩`.
- **텍스트 예산표(근사)**: 팩 × 크기 × 한글 글자수/줄 상한.
  - 근거: skillstead "KO ≈ 라틴 60%"를 출발점으로 하되, **팩별 1순위
    폰트로 fixture 카드의 오버플로 한계를 실측(G3.7 골든 교정 절차)해
    표를 교정**한다. 폰트가 팩마다 다르므로 단일 전역표를 쓰지 않는다.
  - 라틴/혼용 계수: 라틴 장토큰(eGovFrame·URL·약어)은 한글 1자의
    0.55배 폭으로 환산해 예산에 반영한다.
  - **오차 마진**: 예산표 상한에서 10% 여유를 둔다. 이 근사는 "오버플로
    없음의 증명"이 아니라 "오버플로 위험의 사전 차단"이다. 근사가
    놓치는 잔여 위험은 §5.2의 emit 후 검증과 §5.4 검수로 이중 방어.

### 4.4 인쇄 제약 (ai-tells.md 연동)

- 색만의 구분 금지 — 색+모양 이중 코딩(solid/dashed 라인, 뱃지).
- tint 채도 절제, 무지개 구분색·gradient·이모지 금지.
- 헤어라인 최소 0.5pt.

## 5. 빌드 통합 + QC 게이트

### 5.1 emit 래퍼 계약 (배치 정책 — 실험 실증 반영)

- 도식 전체를 `block(breakable: false, ...)`로 감싼다. breakable 기본값은
  (a) 페이지 경계 분할 + 바텀 앵커 왜곡을 실험로 확인했으므로 금지.
- 큰 도식이 다음 페이지로 밀릴 때 앞면 공백은 허용된 비용이다(최대
  프레임 85% 상한이 공백 상한을 간접 제한). 래퍼는 `block` 하나로
  충분하다(개정 3판 — 2판의 `figure(placement: none)` 문구는 폐기:
  figure 캡션·번호화가 불필요하고 block이 본문 흐름 배치를 그대로 준다).
  배치 자동 최적화는 하지 않는다(결정론).
- helper.typ은 tokens.json을 `json("tokens.json")` 상대참조로 읽되
  assemble()이 helper.typ을 build/ 루트에 복사하므로 경로는 유지된다.

### 5.2 게이트 — I1 (신규, `lint.py`)

**시점**: 빌드 중 emit 직전. **동작: 전수 검사 — 모든 펜스의 모든 위반을
하나의 리포트로 모은 뒤 중단**(첫 위반 즉시 중단 아님. gate-report.json
문화 계승). CLI 단독 실행 지원(§5.3).

**검사 항목**:

1. 스키마·엣지 상태(§3.4 전체)
2. 텍스트 예산(§4.3 — 팩별 표, 라틴 환산, 10% 마진)
3. **잉크 컨테인먼트**: 좌표가 아니라 잉크 bbox — 좌표 + 스트로크
   절반 + 마커 돌출 + 그림자 없음. `마지막 엣지 + 스트로크/2 ≤ 영역 우단 − 패딩`.
4. **커너터 산술**: 복도 ≥ 마커 발판 + tip-gap(8~12pt) + 샤프트 가시
   (≥12pt). 헤드 가시폭/샤프트 비 **2.5~3.5배 허용 오차**(목표 3배 —
   초판의 ≈를 검증 가능한 범위로 교체).
5. 숫자-evidence 규칙 + 원문 교차검증(§3.3)
6. 복합 모듈 상한·높이 배분(§3.5)
7. 토큰 존재(팩 `infographic` 5역할)
8. **펜스 위장 감지**: 미등록 펜스 언어라도 내용 JSON에 `layout:` 키가
   있으면 경고(```infographics 오타 → 코드블록 인쇄 무음 통과 방지)
9. **G3 크기 불변식**: 방출 코드의 도식 텍스트 크기가 본문±0.3pt 밖인지

**에러 메시지 계약**:

- 위치: 모든 위반에 `챕터md #펜스순번 필드경로` (예: `ch05.md #2 cards[1].title`)
- 측정값: `28자 > 예산 22자` 형식
- 수정 제안: **저작자 레버만** — ①글자 축약 ②요소 수 감소 ③변형 전환
  (예: cards→flow, 2행 랩) ④복합 분할. 폭·간격 확장 등 산술 결과
  파라미터는 제안하지 않는다(저작자 권한 밖 — 초판 모순 수정).

### 5.3 기존 게이트 관계 (정직한 서술로 개정)

| 게이트 | 실제 적용 범위 |
|---|---|
| G1 판면 오버플로 | **텍스트 잉크만** 검사한다(qc_gate의 실구현). 도식 벡터 잉크의 프레임 이탈 방어선은 I1 잉크 컨테인먼트가 독점한다. |
| G2 폰트 | 책 폰트만 사용하므로 구조적 통과. |
| G3 글자수 밴드 | 도식 텍스트는 크기 사다리의 설계적 차이(±0.3pt 밖)로 제외되며, I1 불변식(§5.2-9)이 이를 보증한다. 우연한 부산물이 아니다. |

### 5.4 검수 집행 — 검수 시트 (구시스템 절차 회수·강화)

- 빌드 시 도식마다 `build/infographic/chNN-figK.review.md` 생성:
  표 형식 `요소 | 문구 | evidence 앵커 | 교차검증(통과/미검증) | 확인란( )`.
  미검증 플래그(§3.3)가 있는 도식은 시트 상단에 경고로 표시.
- 검수자는 시트의 확인란을 채운다(원문 대조 — 구 계약의 절차 계승).
- **qc_gate**: 확인란 미완료 검수 시트가 있으면 WARN(에러 아님 —
  검수는 사람 판단). final/ 생성은 기존 규칙 그대로.
- **검수 렌더 절차(구 계약 회수)**: 도식 페이지를 160~180 DPI로 별도
  렌더링. gate-report.json에 `infographic_pages`(도식 수·페이지
  대응) 필드 추가 — 실제 페이지 수와의 일치 검사 포함. 확인 항목:
  카드 내부 줄바꿈·표 셀 잘림·화살표 충돌·작은 글씨·텍스트 카드 밖
  이탈(§4.3 근사의 잔여 위험을 여기서 포착).

### 5.5 CLI (Phase 1 제공 — 반복 매체를 책 전체 빌드에서 분리)

```
python3 scripts/infographic/cli.py lint <ch.md>        # I1만, 렌더 없음
python3 scripts/infographic/cli.py preview <ch.md> --fig 2 [--style practical]
                                                        # 해당 펜스만 standalone PDF
```

- `preview`는 tokens.json을 읽어 도식 하나를 1페이지 PDF로 컴파일한다.
  저작 루프: 펜스 초안 → lint → preview 눈검 → 다음. 책 전체 빌드는
  최종 확인 시에만.

## 6. archetype 지오메트리

### 6.1 공통 커넥터 규칙

- 화살표 = open-V 스트로크. 헤드 가시폭/샤프트 비 목표 3배, 허용 2.5~3.5.
- tip-gap 8~12pt, 샤프트 가시 ≥12pt — I1 커넥터 산술(§5.2-4)이 증명.
- solid = 순차/요청, dashed = 비동기/참조(색+모양 이중 코딩).
- 커넥터 복도 = 목표 좌 − 소스 우 − 마커 발판. 가독 샤프트가 안 남으면
  compact 화살표·전환 글리프·재배치 중 **규칙 우선순위순** 선택:
  compact → 전환 글리프 → 세로 재배치. 계산 단계에서 결정.

### 6.2 판형 조건부 상한 (실행가능성 매트릭스 — 절대 상한과 별개)

본문폭 실측 기반. 이 표를 초과하면 I1 에러(절대 상한보다 우선 적용).

| layout | essay(249pt) | practical(334pt) | b5(386pt) | business(454pt) | lecture(465pt) |
|---|---|---|---|---|---|
| flow steps(가로) | 4 | 6 | 6 | 8 | 8 |
| flow swimlane 레인 셀 수(개정 4판) | 2 | 3 | 4 | 4 | 4 |
| cards 열수 | 2 | 3 | 3 | 3 | 3~4 |
| matrix 최대열 | 3 | 4 | 4 | 5 | 5 |
| before_after 항목/측 | 3 | 4 | 4 | 5 | 5 |
| ladder 단계(개정 5판) | 4 | 5 | 5 | 5 | 5 |
| topology 노드 | 5 | 6 | 7 | 8 | 8 |
| roadmap 위상 | 3 | 4 | 4 | 5 | 5 |

- flow 결정론 규칙(개정 3판): ①표 초과 → 즉시 I1 에러 ②가로 1행(카드폭
  ≥ 80pt) ③2행 랩(랩 후 카드폭 ≥ 80pt) ④둘 다 아니면 I1 에러(공간 부족).
  **세로 변형은 제거**한다 — 근거: 2판의 "랩 아니면 세로"는 세로 배치가
  높이 한계(프레임 85%)를 수학적으로 초과하는 조합이 존재하고(8단계 세로
  571pt > 한계 441pt 실증), 세로 전용 간격에서 샤프트 가시 최소 12pt를
  보증할 수 없다. 최소 카드폭 문지방 80pt는 판형 상한 내 모든 n이 ②또는
  ③에 수학적으로 합법함을 실측 폭으로 검증했다.
- 각 셀의 값은 §4.3 예산표로 검증 가능해야 하며, Phase별 골든 교정에서
  실측 정정한다.

### 6.3 종류별 배치 산술

| layout | 배치 산술 |
|---|---|
| `flow` | 가로 n카드, 간격 24~32pt. 폭 부족 시 §6.2 결정론 규칙(가로→랩→에러) |
| `flow`(swimlane) | 레인 행 × 순서 셀 |
| `cards` | n열 그리드 `(W−(n−1)g)/n` |
| `matrix` | 격자 rect — §6.2 열수 표 |
| `before_after` | 좌우 패널 + 중앙 전환 화살표 |
| `ladder` | 계단식 — x·y 동시 증가 오프셋 |
| `layers` | 수평 스택 기본, `rings` 동심원 변형 |
| `roadmap` | 가로 타임라인 + 위상 밴드 |
| `topology` | grid 배치 기본. 방향 간선 있으면 계층(DAG 층위) 자동 배치 |
| `approval` | 가로 경로 + 게이트 다이아몬드 |
| `composite` | §3.5 — 세로 슬롯, 주/보조 배분, 슬롯 간 24pt |

## 7. 테스트 전략 (TDD)

- **단위**: archetype별 좌표 모델 pytest. 예: flow 4단계 → 카드 x좌표
  정확값 + 잉크 bbox 우단 ≤ 영역 우단 − 패딩.
- **골든 스냅샷**: emit typst 코드(결정론 검증) + 파서 상태 기계
  (별칭·엣지 거부 목록).
- **골든 교정 절차(예산표)**: 팩 × 크기 × archetype fixture 카드를
  실렌더 → 오버플로 한계 실측 → 예산표 갱신. 표의 근사 오차를
  측정에 뿌리내리는 절차이며 Phase 1에서 수립, 각 archetype 추가 시 반복.
- **통합**: 9종+복합 펜스 fixture 책 → build → PDF 생성·`infographic_pages`
  일치 확인. 펜스 오타·unknown layout·숫자-evidence 위반이 각각
  올바른 I1 리포트를 내는지(전수 집계 포함).
- **비주얼 스모크**: §5.4 검수 렌더 절차 — fixture 책 전 도식 페이지
  PNG + 사람 눈검수 체크리스트.

## 8. 개발 순序 (단계별 증분, 각 단계 TDD)

1. **인프라 + flow** — parse/lint/emit 골격, **CLI(lint/preview)**,
   tokens `infographic` 5역할 값 설계(5팩 전부), emit 래퍼
   (breakable:false·leading 1.3em), 빌드 통합(펜스 추출·플레이스홀더·
   `../infographic/` 경로·helper 복사·리셋), **references/infographic/
   authoring.md 최소판**(flow 스키마·예산 치트시트·라우팅 행) — 
   엔드투엔드 관통.
2. **cards + matrix** — archetype 2종 + authoring.md 동반 갱신 +
   골든 교정 1주기.
3. **before_after + ladder + roadmap** — 동일 구조.
4. **topology + approval + layers(rings 변형)** — 동일 구조.
5. **composite + 가이드 완성** — 복합 씬, authoring.md 전체
   (라우팅 표 9종·검수 절차·치트시트 practical 기준 — 전 팩형 수치
   확장은 본 플랜 범위 밖), SKILL.md 요약 갱신,
   통합 테스트 마무리.

각 Phase 종료 조건: 해당 archetype의 단위·골든·통합 테스트 통과 +
authoring.md 해당 섹션 존재 + 검수 시트 생성 확인.

## 9. 결정 기록

| 결정 | 내용 | 대안과 거절 사유 |
|---|---|---|
| 출력 경로 | typst 네이티브 벡터 (책 PDF 안) | SVG→PNG: Node/Chromium 의존, WSL2 미검증, 인쇄 래스터화 |
| 데이터 위치 | 챕터 md 펜스 블록 | typst-build.yaml: 위치 고정·비대. 사이드카: 파일 2배 |
| 레이아웃 지능 | Python 계산 + raw typst 방출 | cetz: 외부 의존·린트 불가. typst 함수: 사전 검증 불가 |
| archetype 범위 | 9종 + 복합 | MVP 4종: 사용자 요청으로 전체 |
| 라우팅 시점 | 저작 시점 명시 | 빌드 자동판단: 콘텐츠 판단은 저작자 몫, 결정론 유지 |
| 렌더 주체 | build.py (md2typst는 펜스 추출·사이드 파일만) | md2typst 내 렌더: idx·tokens 접근 불가(서브프로세스 구조) |
| 텍스트 폭 검증 | 팩별 예산표 = 골든 교정 근사, 10% 마진, 이중 방어(emit 후 검증+검수) | "산술 증명" 주장: 폰트 메트릭 없이 불가 — 적대 검토로 허위 판명 |
| 게이트 상속 | G1은 텍스트 한정 서술, G3은 크기 불변식으로 보증 | "자동 적용" 주장: 실제 qc_gate 구조와 불일치 — 적대 검토로 판명 |
| 검수 집행 | 검수 시트 + WARN | 무연료 사람 게이트: 건너뛰기 무음 — 집행 장치 필요 |
| 저작 루프 | lint/preview CLI Phase 1 | 책 전체 빌드만: 도식당 2~4회 전체 빌드 — 루프 비용 과다 |

## 10. 개정 이력

- 초판: 2026-08-21 — 승인용 최초 작성 (커밋 d4eb9f8)
- 개정 2판: 2026-08-21 — 적대 검토 3관점(기술 실행가능성·계약 완전성·
  저작 워크플로) 24건 반영. 주요 변경: 렌더 주체 build.py 확정(§2),
  파이프라인 실증 4건 반영(펜스 추출·플레이스홀더·`../infographic/`
  경로·helper 복사), I1 항목 5건 추가(잉크 bbox·커넥터 산술·교차검증·
  펜스 위장 감지·G3 불변식) + 전수 보고·위치·저작자 레버 메시지 계약,
  근거 경계 교차검증(§3.3), 검수 시트 집행(§5.4), CLI(§5.5), 판형
  조건부 상한 매트릭스(§6.2), 폰트 표기 정정(§4.1), leading 1.3em
  (§4.3), emit 래퍼(§5.1), 엣지 상태·별칭 마이그레이션(§3.4),
  각 Phase 가이드 동반(§8).
- 개정 3판: 2026-08-22 — Phase 1 구현 계획 적대 검토(코드 실행 실증·
  스펙 충실성·실행가능성 22건)의 스펙 측 반영. **JSON 확정**(§2·§3 —
  무의존 원칙과 YAML 양립 불가 모순 해소), flow 결정론에서 **세로 변형
  제거**(§6.2 — 세로 571pt>한계 441pt 불가·샤프트 가시 보증 불가 실증),
  최소 카드폭 문지방 80pt 명시, essay 도식 제목 예외 본문+1.5pt 기록
  (§4.3), `figure(placement:none)` 폐기·block 단일 래퍼(§5.1).
- 개정 4판: 2026-08-22 — Phase 2 플랜 적대 검토 반영. §6.2에 **flow swimlane
  레인 셀 수 행 추가**(essay 2 / practical 3 / b5·business·lecture 4) —
  셀 간격 GS=24에서 샤프트 가시 ≥12pt(§6.1)와 MIN_CELL_W=45가 동시에
  성립하는 최대 셀 수로 유도(Phase 2 플랜 수학 검증). §6.2 cards 열수의
  lecture "3~4"는 구현이 3으로 고정(§2 결정론 원칙 — authoring.md에 근거
  기록). §3.3 숫자 검사 대상에 정성 매트릭스 축 라벨(x_axis/y_axis
  low·high) 포함 명시.
- 개정 5판: 2026-08-22 — Phase 4 플랜과 함께. §6.2에 **ladder 단계 행 추가**
  (essay 4 / practical·b5·business·lecture 5) — Phase 3 실측(essay 5단계
  계단 단 간격 3.0pt < 16pt 최소)을 판형 상한으로 정식화. 기존 절대 상한
  3~5(§3.2)와 별개로 layout이 판형 행을 우선 검사한다.
- 개정 6판: 2026-08-22 — Phase 5 플랜과 함께. composite 자동 축소 제거·
  에러 스키마 2종 확정, 최상위 title 선택·모듈 재귀 전 슬롯 금지 명시,
  리포트 명칭 gate-report 정합, 치트시트 practical 기준 명시.
