# 인포그래픽 저작 가이드 (Phase 3 — +before_after·ladder·roadmap)

챕터 md에 ` ```infographic ` 펜스(JSON)를 넣으면 그 자리에 출판 품질 벡터
도식이 삽입된다. 도식은 원고의 **편집적 재배열**이다 — 원문 근거를 벗어나지
않으며 원문을 대체하지 않는다(기본 고지문이 이를 명시). 설계 전반은 저장소
루트의 `docs/superpowers/specs/2026-08-21-infographic-layer-design.md` 참조.

## 언제 도식을 넣나

- 장의 핵심 흐름이 **2~8단계 순차 절차**일 때 flow 1개. 단계마다 담당 주체가
  갈리면 flow lanes(swimlane).
- 항목 나열·**3~6개 병렬 강조**(요건·원칙·지표 카드)일 때 cards 1개.
- **2축 비교·분류**(표 또는 2×2 정성 사분면)일 때 matrix 1개.
- **전후 대비·전환**(개선 이전·이후 조건 나열)이 핵심 논증일 때 before_after 1개.
- 수준·성숙도의 **단계적 상승**(3~5단계 계단)일 때 ladder 1개.
- **시간 전개**(연도·분기 위상 + 세부 항목)일 때 roadmap 1개.
- 정량 통계 차트(막대·선·원형·히트맵)는 금지 — 데이터 날조 위험(스펙 비목표).

라우팅 표 — layout은 저작 시점 명시(빌드 자동판단 없음, 스펙 §2 원칙 3):

| 콘텐츠 신호 | layout | 상태 |
|---|---|---|
| 순차 단계·절차·전환 | `flow` | **Phase 2 사용 가능** |
| 배역별 진행(swimlane) | `flow` + `lanes` | **Phase 2 사용 가능** |
| 항목 나열·카드형 요약 | `cards` | **Phase 2 사용 가능** |
| 2축 비교·분류 | `matrix` | **Phase 2 사용 가능** |
| 전후 대비·전환 | `before_after` | **Phase 3 사용 가능** |
| 단계적 수준 상승 | `ladder` | **Phase 3 사용 가능** |
| 일정·위상 타임라인 | `roadmap` | **Phase 3 사용 가능** |
| 구성·관계망 | `topology` | Phase 4 예정 |
| 결재·승인 경로 | `approval` | Phase 4 예정 |
| 계층 구조 | `layers` | Phase 4 예정 |
| 복합 씬(주+보조) | `composite` | Phase 5 예정 |

요소 수 판형 상한(스펙 §6.2 — 초과 시 I1 에러). 상한 내 배치 결정론:
flow는 가로 1행(카드폭 ≥ 80pt) → 2행 랩 → 에러. cards는 팩 열수 그리드 →
2행 랩 → 에러. matrix는 항상 1그리드. **세로 배치는 없다.** 공간 부족·판형
초과는 I1 에러로 막히며, 해결 레버는 저작자 몫이다 — 글자 축약, 요소 수 감소,
펜스 분할. 글자 축소는 레버가 아니다.

| 요소 | essay | practical | b5 | business | lecture |
|---|---|---|---|---|---|
| flow steps | 4 | 6 | 6 | 8 | 8 |
| flow lanes 레인 셀 | 2 | 3 | 4 | 4 | 4 |
| cards 카드(=열수×2행) | 4 | 6 | 6 | 6 | 6 |
| matrix 격자 열 | 3 | 4 | 4 | 5 | 5 |
| before_after 항목/측 | 3 | 4 | 4 | 5 | 5 |
| roadmap 위상 | 3 | 4 | 4 | 5 | 5 |

- cards 카드 수 하한 2, 상한 6(격자 상한은 표대로 열수×2행). matrix 격자는
  2열×2행~상한, 행 상한 6. matrix 정성은 **2×2 고정**(축 low·high).
- cards 팩 열수: essay 2 / practical·b5·business 3 / **lecture 3 고정** —
  스펙 §6.2가 lecture를 "3~4"로 범위 제시했으나 구현은 3으로 고정한다
  (§2 결정론 원칙: 범위를 남기면 같은 입력에 다른 배치가 가능해져 골든
  재현성이 깨진다 — 하나의 값만 기록·재현 대상이 된다).
- lanes의 레인(행) 수 자체는 상한표가 아닌 85% 높이 검사가 잡는다.
- before_after 항목은 각 측 하한 1·절대 상한 5이며, 판형 상한은 **많은 쪽
  항목 수** 기준으로 적용된다. 양측 항목 수는 달라도 된다(패널 높이는 많은
  쪽에 맞춘다).
- ladder 단계는 판형 상한 없음(절대 3~5)이지만 **essay에서 5단계는 렌더
  불가**하다(프레임 높이 391.2pt에서 1줄 단계 문구로도 5상자+최소 단 간격이
  85% 예산을 넘는다) — essay는 4단계까지, 5단계는 practical·b5·business·
  lecture만.
- roadmap 위상 수는 절대 범위 2~5보다 **판형 상한이 우선** 적용되고, 항목은
  위상당 1~4(전 팩 공통 — 높이 예산 보호).

## 펜스 규약

언어 `infographic`, 내용은 **표준 JSON**(더블쿼트, 주석 없음). 펜스 위치가 곧
도식 삽입 위치다.

### flow — 순차 절차

```infographic
{
  "layout": "flow",
  "kicker": "CHAPTER MAP",
  "title": "원고 교정은 3판을 거쳐 확정된다",
  "thesis": "각 판의 역할이 다르다 — 한 판에서 전부 하려 하지 않는다.",
  "evidence": "§2",
  "steps": [
    { "title": "초안", "text": "구조와 논점을 확정하는 판" },
    { "title": "중간판", "text": "근거와 문장을 다듬는 판" },
    { "title": "확정판", "text": "판면과 고지를 검증하는 판" }
  ],
  "note": "편집 요약: §2의 교정 절차를 재배열한 도식이다."
}
```

주체별 진행(swimlane) — `steps` 대신 `lanes`. **둘은 배타**이며 같이 쓰면
I1 에러다. 가로 진행만 있고 세로 화살표는 없다.

```infographic
{
  "layout": "flow",
  "kicker": "ROLES",
  "title": "주체별 교정 책임",
  "thesis": "저자와 편집자의 역할이 판마다 나뉜다.",
  "lanes": [
    { "actor": "저자", "steps": [
      { "title": "초안", "text": "구조와 논점 확정" },
      { "title": "수정", "text": "지시 반영" } ] },
    { "actor": "편집자", "steps": [
      { "title": "교정", "text": "문장 다듬기" },
      { "title": "검증", "text": "판면 확인" } ] }
  ],
  "note": "편집 요약: §2의 역할 분담을 재배열한 도식이다."
}
```

### cards — 병렬 강조

```infographic
{
  "layout": "cards",
  "kicker": "PRINCIPLES",
  "title": "확정판의 세 요소",
  "thesis": "세 요소가 갖춰져야 확정판이 성립한다.",
  "cards": [
    { "title": "구조 확정", "text": "목차와 논점이 고정된다", "value": "기준" },
    { "title": "근거 확정", "text": "인용과 수치가 대조된다" },
    { "title": "판면 확정", "text": "조판과 고지가 검증된다" }
  ],
  "note": "편집 요약: §2의 확정 조건을 재배열한 도식이다."
}
```

`value`는 선택 — 카드 제목 위 강조 라벨(제목+2pt). 모든 카드에 넣을 필요는
없지만 첫 카드에만 두면 시선이 쏠리므로, 강조하지 않을 거면 생략한다.

### matrix — 2축 비교·분류

격자(표형). 첫 열이 행 라벨(굵게)으로 쓰인다.

```infographic
{
  "layout": "matrix",
  "kicker": "CHECKLIST",
  "title": "단계별 준비 요소",
  "headers": ["단계", "문서", "도구", "확인"],
  "rows": [
    ["기획", "목차 초안", "편집 노트", "독자 정의"],
    ["집필", "원고 초안", "버전 기록", "근거 노트"]
  ],
  "note": "편집 요약: §1의 준비 요소를 재배열한 도식이다."
}
```

정성 매트릭스(2×2 사분면). `x_axis`·`y_axis`는 각각 low·high 라벨이고
`cells` 4개는 **[y low-x low, y low-x high, y high-x low, y high-x high]**
순서다.

```infographic
{
  "layout": "matrix",
  "kicker": "DIAGNOSIS",
  "title": "교정 개입은 문제 유형으로 결정된다",
  "x_axis": { "low": "저개입", "high": "고개입" },
  "y_axis": { "low": "구조 문제", "high": "문장 문제" },
  "cells": [
    { "title": "구조·저", "text": "목차 단계에서 정리한다" },
    { "title": "문장·저", "text": "표현만 다듬는다" },
    { "title": "구조·고", "text": "재구성이 필요하다" },
    { "title": "문장·고", "text": "전면 퇴고 대상이다" }
  ],
  "note": "편집 요약: §3의 진단 기준을 재배열한 도식이다."
}
```

### before_after — 전환 대비

좌우 패널 + 중앙 전환 화살표. `before`·`after`는 문자열 배열(조건·지표
문구 나열), `center`는 중앙 화살표 위 라벨(선택), `before_label`·
`after_label`은 패널 라벨(선택, 기본 "이전"/"이후").

```infographic
{
  "layout": "before_after",
  "kicker": "TRANSFORM",
  "title": "AI 도입은 리드타임을 2주에서 3일로 줄인다",
  "thesis": "반복 수작업이 자동화되면서 인도 시간이 단축된다.",
  "evidence": "§2",
  "before": ["리드타임 2주", "수작업 5단계"],
  "after": ["리드타임 3일", "자동화 1단계"],
  "center": "AI 도입",
  "note": "편집 요약: §2의 전후 비교를 재배열한 도식이다."
}
```

- 항목은 **짧은 문구**다(practical 패널 폭 111.2pt에서 줄당 ~15자) — 근거
  문장은 `thesis`에 넣고 패널에는 조건·지표 라벨만 나열한다.
- `center` 라벨은 초단문이다 — 중앙 라벨 폭 68pt(kicker 크기 8.5~9pt에서
  줄당 ~7~9자).
- 양측 패널은 동일 폭·동일 높이(많은 쪽 항목에 맞춤)로 통일된다. 항목 수
  상한은 판형 상한표(많은 쪽 기준, 하한 1·절대 5).
- I1: `before[i]`·`after[i]`·`center`·패널 라벨 전부 숫자-evidence 검사
  대상이다. `thesis`·`note`는 제외(공통 규약).

### ladder — 성숙도 계단

계단식 상승 — `stages[0]`가 최하단, x·y가 함께 증가한다. 단계 수 3~5
(절대 범위 — 판형 상한 없음).

```infographic
{
  "layout": "ladder",
  "kicker": "MATURITY",
  "title": "성숙도는 네 단계를 거쳐 올라간다",
  "thesis": "각 단계는 이전 단계의 확립을 전제로 한다.",
  "evidence": "§2",
  "stages": [
    { "title": "단계 1", "text": "근거 문장" },
    { "title": "단계 2", "text": "근거 문장" },
    { "title": "단계 3", "text": "근거 문장" },
    { "title": "단계 4", "text": "근거 문장" }
  ],
  "note": "편집 요약: §2의 성숙 단계를 재배열한 도식이다."
}
```

- 단계 문구가 길면 상자 높이가 커져 **"계단 단 간격" 에러**가 난다(단 사이
  최소 시각 간격 16pt 미달 — 85% 높이 예산 소진). 레버는 문구 축약·단계 수
  감소·펜스 분할뿐이다.
- **essay는 4단계까지** 쓴다 — 5단계는 essay 프레임 높이 예산에서 단 간격
  하한을 만족하지 못해 렌더 자체가 불가능하다(판형 상한표 각주). practical·
  b5·business·lecture는 5단계까지 가능.
- 모든 상자는 가장 높은 단계 기준 동일 높이로 통일된다(제목+본문 실측).
- I1: `stages[i].title`·`stages[i].text` 모두 숫자-evidence 검사 대상이다.

### roadmap — 시간 전개

상단 가로 타임라인 + 위상 밴드. `phases`는 `{period, title, items}` 배열 —
`period`는 기간 라벨(짧게), `items`는 문자열 배열(위상당 1~4).

```infographic
{
  "layout": "roadmap",
  "kicker": "ROADMAP",
  "title": "도입은 세 위상으로 전개된다",
  "thesis": "각 위상의 준비 항목이 다르다.",
  "evidence": "§2",
  "phases": [
    { "period": "2025년", "title": "위상 1", "items": ["항목 0", "항목 1"] },
    { "period": "2026년", "title": "위상 2", "items": ["항목 0", "항목 1"] },
    { "period": "2027년", "title": "위상 3", "items": ["항목 0", "항목 1"] }
  ],
  "note": "편집 요약: §2의 전개 계획을 재배열한 도식이다."
}
```

- 위상 수는 **판형 상한표가 우선**(절대 2~5보다 먼저 적용). 상한 도달 시
  밴드 폭은 최소 54~55pt까지 내려간다(essay 3위상 55.2pt·practical 4위상
  55.6pt — 밴드 폭 하한 54pt의 실측 근거).
- **항목은 초단문**이다 — 최협 밴드에서 실측 줄당 4~5자 수준. 세부 근거는
  본문에 두고 밴드에는 키워드만 넣는다.
- 모든 밴드는 동일 폭·가장 높은 위상 기준 동일 높이로 통일된다.
- I1: `phases[i].period`·`phases[i].title`·`phases[i].items[j]` 전부
  숫자-evidence 검사 대상이다 — 연도·분기 숫자에도 evidence가 필요하다.

### 공통 필드

| 필드 | 필수 | 규약 |
|---|---|---|
| `layout` | O | `flow`·`cards`·`matrix`·`before_after`·`ladder`·`roadmap` (구별칭 `process`→flow, `principles`·`dashboard`→cards, `quadrant`→matrix 정성, `bridge`→before_after — 자동 변환) |
| `title` | O | 결론형 명제 — 주제 라벨 금지 |
| `steps` | flow | 2~8개(판형 상한표), 각 `{title, text}` — 둘 다 필수 |
| `lanes` | flow | `steps`와 배타. 각 `{actor, steps}` — 레인 셀 수는 판형 상한표 |
| `cards` | cards | 2~6개(판형 상한표), 각 `{title, text, 선택 value}` |
| `headers`+`rows` | matrix 격자 | 열 2~상한·행 2~6. 셀은 문자열 |
| `x_axis`·`y_axis`·`cells` | matrix 정성 | 축은 `{low, high}`, cells 4개 각 `{title, text}` — 격자 키와 배타 |
| `before`+`after` | before_after | 각 1~5개(하한 1·절대 상한 5)의 문자열 배열 — 판형 상한은 많은 쪽 기준 |
| `center` | before_after | 선택 — 중앙 전환 라벨(초단문, 폭 68pt) |
| `before_label`/`after_label` | before_after | 선택 — 패널 라벨(기본 "이전"/"이후") |
| `stages` | ladder | 3~5개(절대 — 판형 상한 없음, essay는 4까지), 각 `{title, text}` |
| `phases` | roadmap | 2~5개(판형 상한 우선), 각 `{period, title, items 1~4}` |
| `thesis` | | 한두 문장 설명 |
| `kicker` | | 짧은 영문·한국어 라벨(도식 상단) |
| `note` | | 고지문. 생략 시 기본문: "편집 요약: 본문의 장·절 구조와 핵심 문장을 재배열한 도식이며, 원문을 대체하지 않습니다." |
| `evidence` | | `"§N"` — 같은 챕터 md의 N번째 `## ` 헤딩 범위(보통 §1 = 장 전체). 숫자가 있으면 필수(아래) |

근거 경계(스펙 §3.3):

- **모든 문구는 원문에 대응**시켜 쓴다 — 도식 언어로 새로 창작하지 않는다.
- **숫자는 evidence가 필요하다.** title·kicker·steps·cards·matrix 셀·
  before/after·center·stages·phases 문구에 아라비아숫자 토큰(`3`, `50%`,
  `1.5`)이 있으면 evidence 필수이고, I1이 각 숫자가 §N 원문에 부분 문자열로
  존재하는지 **자동 교차검증**한다. 면제: `제N장/제N절` 서수, 원형 숫자
  ①②③, 한글 수사. `thesis`·`note`는 검사 제외(편집자 문구). 정성 매트릭스
  축 라벨(`x_axis`/`y_axis`)도 검사 대상이다.
- 펜스 자신의 JSON은 근거로 쓰이지 않는다 — 본문에서 펜스를 떼고 검사한다
  (자기참조 방지).
- evidence 해석 불가·범위 밖 인용이면 **"미검증" 플래그**(빌드는 계속) →
  검수 시트에서 사람 대조 필수.
- 펜스 언어를 `infographics` 등으로 오타내면 I1이 "펜스 위장"으로 지적한다
  (JSON에 `layout` 키가 있는데 다른 언어 펜스 — 코드블록으로 인쇄되는
  무음 실패 방지).
- 색·폰트는 저작자가 지정하지 않는다 — 스타일 팩 tokens.json의
  `infographic` 5역할 색과 책 폰트 계약을 그대로 쓴다(팩 교체 시 자동 재색).

## 예산 치트시트 (practical 기준 — 골든 교정 1·2주기 실측 반영)

타입 스케일(스펙 §4.3): 도식 제목 13.5pt(본문 H2급) · 카드 제목 11pt(본문+1) ·
카드 본문 9pt(본문−1) · value 13pt(제목+2) · kicker·격자 헤더·축 라벨 8.5pt.
도식 텍스트는 본문 크기와 ±0.3pt 밖이어야 한다(G3 불변식 — I1이 방출 ops에서
검증).

줄당 한글 자수 상한. 폭 종류(practical 본문폭 334.5pt 기준): 카드폭 139.2pt
(flow n=2·4, cards n=2) / 83.5pt(flow n=3·5·6, cards n=3~6) · 격자 셀 76.6pt
(4열) · 정성 셀 119.2pt · 레인 셀 66.2pt(3열) · actor 열 60pt · 전환 패널
111.2pt · 계단 상자 171.6pt(가용폭 56%) · 로드맵 밴드 139.2pt(위상 2) /
83.5pt(3) / 55.6pt(4).

| 텍스트 | 크기 | 줄당 KO 상한 |
|---|---|---|
| 도식 제목 | 13.5pt | ~33자(패널 내부 전폭 306.5pt) |
| 카드 제목 | 11pt | ~16자(139.2pt) · ~9자(83.5pt) |
| 카드 본문 | 9pt | ~20자(139.2pt) · ~11자(83.5pt) |
| 카드 value | 13pt | ~7자(83.5pt) |
| 격자 헤더 | 8.5pt | ~11자(셀폭 76.6pt) |
| 격자 셀 본문 | 9pt | ~10자(76.6pt) |
| 정성 셀 제목 | 11pt | ~13자(정성 셀 119.2pt) |
| 정성 셀 본문 | 9pt | ~16자(119.2pt) |
| 레인 셀 제목 | 11pt | ~6자(셀폭 66.2pt) |
| 레인 셀 본문 | 9pt | ~8자(66.2pt) |
| actor 라벨 | 11pt | ~5자(열폭 60pt) |
| 전환 패널 항목 | 9pt | ~15자(패널 111.2pt) |
| 전환 center 라벨 | 8.5pt | ~9자(중앙 라벨 폭 68pt) |
| 계단 단계 제목 | 11pt | ~20자(상자 171.6pt) |
| 계단 단계 본문 | 9pt | ~25자(171.6pt) |
| 로드맵 period 라벨 | 8.5pt | ~21자(139.2pt) · ~11자(83.5pt) · ~6자(55.6pt) |
| 로드맵 위상 제목 | 11pt | ~16자(139.2pt) · ~9자(83.5pt) · ~5자(55.6pt) |
| 로드맵 항목 | 9pt | ~20자(139.2pt) · ~11자(83.5pt) · ~6자(55.6pt) |

- 상한 근거: `(박스폭−16)×0.9 ÷ 크기pt`(좌우 패딩 8pt씩, 여유 10% — 격자
  셀은 패딩 6pt). 도식 제목은 패딩 없이 패널 내부 전폭 `본문폭−28`을 쓴다.
- 상한은 **골든 교정 1주기(2026-08-22) 실측** 반영 — 예상수용자수를 팩 계수
  practical 0.61(예상 5.52자 ÷ 실측 9자, 경계 = 카드폭 83.5pt에서 실제
  수용되는 KO 자수)로 나눈 값. 팩별 계수: practical 0.61 · essay 0.66 ·
  business 0.70 · lecture 0.70 · b5 0.63 — `scripts/infographic/budget.py`
  `PACK_KO_FACTOR` 참조. 2주기(Phase 3 3종 추가 후, 아래)에서도 전 팩
  유지 판정 — 계수 불변.
- 로드맵 최협 밴드(위상 상한 도달, 55.6pt)는 실측 줄당 4~5자로 예산표
  (~5~6자)보다 1자 좁다(교정 2주기 실측) — 밴드 항목은 표보다 더 짧게
  쓴다.
- 박스당 **3줄 상한**(I1) — 초과하면 글자 축약·요소 수 감소·펜스 분할.
- 라틴 장토큰(URL·약어)은 한글 1자의 0.55배 폭으로 환산된다.

## 골든 교정 절차 (스펙 §7 — 1·2주기 완료 2026-08-22, archetype 추가·계수 드리프트 의심 시 반복)

1. calib fixture(경계 문구 고정 세트 — 1주기 `calib-cards.md`, 2주기
   `calib-before-after.md`·`calib-ladder.md`·`calib-roadmap.md`)를
   팩별로 `cli.py preview --style <팩>` 렌더.
2. PDF에서 스팬 폭 실측(PyMuPDF) — 측정 단위 KO 환산 pt, **경계는 카드 폭**
   (텍스트가 카드를 벗어나기 직전까지 실제 수용되는 KO 자수).
3. 비율 = 예상수용KO자수(max_units 식) ÷ 실측수용KO자수, 소수 2자리
   반올림 → `PACK_KO_FACTOR[팩]`. |비율−1| < 0.05면 데드밴드(기존값 유지).
4. 치트시트 표 갱신. 계수가 실제로 바뀐 팩의 골든이 있으면
   `IG_REGEN_GOLDEN=1 pytest` 재확정 → 눈검 → 커밋.
5. 1주기 결과(2026-08-22): practical 0.61 · essay 0.66 · business 0.70 ·
   lecture 0.70 · b5 0.63 — 전 팩 |비율−1| ≥ 0.30으로 데드밴드 밖, 전 팩
   갱신. 이후 골든은 바이트 안정(경계를 넘는 문구 없음 — 재확정 불필요).
6. 2주기 결과(2026-08-22, Phase 3 archetype 3종 추가 후 — fixture 3종 ×
   5팩 전수 15렌더, 실측은 regular 본문−1pt 요소 기준): 팩 평균 비율
   practical 0.593 · essay 0.647 · b5 0.613 · business 0.713 · lecture
   0.720 — 드리프트 ≤ 0.020으로 전 팩 데드밴드 내, **PACK_KO_FACTOR 유지**
   (골든 바이트 불변). regular 자당폭 실측: practical/b5 6.759 · essay
   7.866 · business 8.208 · lecture 7.776pt. 로드맵 개별 0.56(essay·
   practical)은 최협 밴드 floor 양자화(±1자 = 7~14%) — 팩 평균으로 판정.

## 도식 하나 만들기 (빌드 없이)

저작 루프: 펜스 초안 → lint → preview 눈검 → 다음. 책 전체 빌드는 최종 확인
시에만.

```bash
python3 scripts/infographic/cli.py lint manuscript/ch01.md              # I1만(렌더 없음)
python3 scripts/infographic/cli.py preview manuscript/ch01.md --fig 1   # 펜스 #1 눈검 PDF
# --style practical|essay|business|lecture|b5 (기본 practical) · --out fig-preview.pdf (기본)
```

`--fig N`은 챕터 내 펜스 등장 순번(1부터). preview는 팩 tokens.json으로 판형
크기 1페이지 PDF를 컴파일한다 — 해당 펜스에 I1 위반이 남아 있으면 렌더 대신
위반을 출력하고 중단한다.

## 검수

- 빌드 시 도식마다 `build/infographic/NNN-figNN.review.md` 검수 시트가 생성된다
  — 5열: 요소 | 문구 | evidence | 교차검증 | 확인란. 원문과 대조해 확인란과
  하단 `- [ ] 원문 대조 완료` 체크박스를 채운다(`- [x]`).
- qc_gate은 미완료 검수 시트가 남아 있으면 **WARN**을 출력한다(에러 아님 —
  검수는 사람 판단. final/ 생성은 기존 규칙 그대로).
- I1 "미검증" 플래그(타 챕터 인용·evidence 불해석 숫자)는 기계 교차검증을
  건너뛴 것이다 — **사람 대조 필수**. 해당 도식 시트 상단에 경고로 표시된다.
