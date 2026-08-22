# 인포그래픽 저작 가이드 (Phase 5 — +composite·검수 렌더·리포트)

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
| 구성·관계망 | `topology` | **Phase 4 사용 가능** |
| 결재·승인 경로 | `approval` | **Phase 4 사용 가능** |
| 계층 구조 | `layers` | **Phase 4 사용 가능** |
| 복합 씬(주+보조) | `composite` | **Phase 5 사용 가능** |

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
| topology 노드 | 5 | 6 | 7 | 8 | 8 |
| ladder 단계 | 4 | 5 | 5 | 5 | 5 |

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
- ladder 단계는 절대 3~5에 더해 **판형 상한이 우선** 적용된다(개정 5판 —
  표대로 essay 4, 나머지 팩 5). essay 5단계는 프레임 높이 391.2pt에서 1줄
  단계 문구로도 5상자+최소 단 간격이 85% 예산을 넘기 때문에 상한 4로
  못박은 것이다 — 초과 시 "판형 상한" 에러가 계단 지오메트리 에러에 앞선다.
- roadmap 위상 수는 절대 범위 2~5보다 **판형 상한이 우선** 적용되고, 항목은
  위상당 1~4(전 팩 공통 — 높이 예산 보호).
- topology 노드 수는 판형 상한표(절대 3~8보다 우선)이며, 간선이 있으면 열수는
  **층위(최장경로 깊이)** 로 늘어난다 — 상한만 지키고 연쇄 간선을 걸면 노드
  폭 하상수 에러가 난다(아래 topology 섹션).
- approval·layers는 **판형 상한 표가 없다** — 스텝 폭·스택 높이의 하상수
  검사(각 48pt·프레임 높이 예산)가 상한 역할을 한다. 초과 시 "폭 하상수"
  에러 — 경로 축약 또는 펜스 분할이 레버다.

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

계단식 상승 — `stages[0]`가 최하단, x·y가 함께 증가한다. 단계 수는 절대
3~5에 더해 **판형 상한이 우선**이다(상한표 — essay 4, 나머지 팩 5).

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
- **essay는 4단계까지**(상한표) — 5단계는 "판형 상한" 에러로 즉시 거부된다.
  근거는 프레임 높이 391.2pt에서 1줄 문구로도 5상자+최소 단 간격이 85%
  예산을 넘는다는 실측이다. practical·b5·business·lecture는 5단계까지 가능.
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

### topology — 구성 관계

노드·간선 그래프. `nodes`는 `{id, label}` 배열(3~상한), `edges`는 선택 —
`{from, to, dashed}` 배열. 간선이 없으면 정사각 grid, 있으면 유방향
비순환(DAG) 최장경로 층위 배치(왼쪽→오른쪽)다.

```infographic
{
  "layout": "topology",
  "kicker": "구성",
  "title": "구성 요소는 흐름을 따라 연결된다",
  "thesis": "변환을 거친 자료만 질의에 쓰인다.",
  "evidence": "§2",
  "nodes": [
    { "id": "a", "label": "입력 수집" },
    { "id": "b", "label": "전처리" },
    { "id": "c", "label": "변환" },
    { "id": "d", "label": "저장" },
    { "id": "e", "label": "질의" }
  ],
  "edges": [
    { "from": "a", "to": "b" },
    { "from": "b", "to": "c" },
    { "from": "c", "to": "d" },
    { "from": "c", "to": "e", "dashed": true }
  ],
  "note": "편집 요약: §2의 구성 관계를 재배열한 도식이다."
}
```

- **간선 설계 규칙 — 층위 ≤ 4 (essay는 층위 ≤ 3).** 노드 5개로 연쇄(a→b→c→d→e)를 걸면 층위 5
  → 열 5개 → 노드 폭이 하상수(54pt)를 밑돌아 에러난다. 간선은 최장경로
  깊이 4 이내로 설계한다(예: a→b, a→c, c→d, c→e → 층위 3열). 순환·자기
  간선·미참조 id는 parse 에러다.
- **경유 간선만 두거나 다이렉트 간선 제거** — 두 노드 사이 경유 노드가 있으면
  다이렉트 간선을 함께 두지 않는다(화살표가 경유 상자를 관통해 렌더된다).
- `dashed: true` = 참조 간선(점선) — 흐름과 참조를 시각적으로 구분한다.
- 노드 라벨은 초단문이다 — essay 무간선 grid에서 라벨 상자 39.2pt(줄당
  실측 4자), practical 3열 라벨 상자 67.5pt(~11자). 3줄 밀도 상한(I1)이
  곧바로 걸린다.
- I1: `nodes[i].label` 전부 숫자-evidence 검사 대상이다(숫자 없으면 면제).

### approval — 결재 흐름

가로 결재 경로. `path`는 `{title, text, gate}` 배열 — 각 스텝 상자가 왼쪽에서
오른쪽으로 이어지고 `gate: true` 스텝에만 승인 관문 마커가 붙는다.

```infographic
{
  "layout": "approval",
  "kicker": "결재",
  "title": "결재는 검토를 거쳐 집행으로 이어진다",
  "thesis": "두 관문을 통과해야 집행이 성립한다.",
  "evidence": "§2",
  "path": [
    { "title": "기획", "text": "방향 확정" },
    { "title": "부서 검토", "gate": true },
    { "title": "예산 승인", "gate": true },
    { "title": "집행", "text": "실행" }
  ],
  "note": "편집 요약: §2의 결재 절차를 재배열한 도식이다."
}
```

- **게이트 마커 해석 근거**: 스텝 상단변 중심의 45° 회전 사각(한 변 12pt) =
  승인 관문 — `gate: true` 스텝에만 그려진다. 저자는 **게이트=결재선,
  비게이트=준비·집행**으로 읽는다(스펙 §6.3 다이아몬드 표현). 게이트는
  상한 4개.
- **팩별 최대 스텝 수(실질 상한 — 스텝 폭 하상수 48pt 도달 한계)**:
  essay 3 / practical 4 / b5 5 / business 5 / lecture 6. 판형 상한 표는
  없다 — 초과하면 "스텝 폭 하상수" 에러다.
- `title`은 필수·`text`는 선택이지만, 최다 스텝 팩에서 스텝 상자가
  49~56pt로 좁아지므로 제목은 ~5자·본문은 ~6자 수준의 초단문으로 쓴다.
- I1: `path[i].title`·`path[i].text` 전부 숫자-evidence 검사 대상이다.

### layers — 계층 구조

수평 스택(기본) 또는 동심원(변형). `stack`은 `{label}` 배열 — 전폭 행이
위에서 아래로 쌓인다. `rings`를 쓰면 `{label}` 배열이 바깥→안쪽 동심원이
된다(둘은 배타).

```infographic
{
  "layout": "layers",
  "kicker": "구조",
  "title": "계층은 표현에서 자료로 내려간다",
  "thesis": "각 계층은 바로 아래 계층에만 의존한다.",
  "evidence": "§2",
  "stack": [
    { "label": "표현 계층" },
    { "label": "응용 계층" },
    { "label": "도메인 계층" },
    { "label": "자료 계층" }
  ],
  "note": "편집 요약: §2의 계층 구조를 재배열한 도식이다."
}
```

- 스택 라벨은 행 전폭(practical 306.5pt)을 쓰므로 문장형도 수용한다(~47자).
  계층 수 상한은 표가 아니라 프레임 높이 예산이 잡는다.
- `rings` **링 라벨 상한**: 라벨은 12시 방향 현(chord) 폭 안에서 실측
  줄바꿈된다 — 최내곽 링일수록 현이 좁다(practical 4링: 최외곽 102.2pt
  ~14자 · 최내곽 39.4pt ~4자). 링 라벨은 노드 라벨보다 더 짧게
  (**음절 4 이내 권장**) — 저작 계약 초단문이다.
- I1: `stack[i].label`·`rings[i].label` 전부 숫자-evidence 검사 대상이다.

### composite — 복합 씬

한 장에서 대비·근거(주)와 절차(보조)를 **함께** 보여야 할 때 — 모듈 2~3개를
세로로 쌓는다. `modules`는 `{slot, layout, …}` 배열이고 각 모듈 페이로드는
독립 펜스와 동일한 스키마 검증을 받는다(개수 상한·I1 전수 승계).

```infographic
{
  "layout": "composite",
  "kicker": "한 장 요약",
  "title": "근거와 절차를 한 장에 담는다",
  "evidence": "§2",
  "modules": [
    { "slot": "primary", "layout": "cards", "title": "확정판의 세 요소",
      "cards": [
        { "title": "요소 1", "text": "근거 문장 1." },
        { "title": "요소 2", "text": "근거 문장 2." },
        { "title": "요소 3", "text": "근거 문장 3." } ] },
    { "slot": "supporting", "layout": "flow", "title": "적용은 두 단계로 끝난다",
      "steps": [
        { "title": "준비", "text": "전제를 확인한다." },
        { "title": "실행", "text": "절차를 수행한다." } ],
      "note": "위 카드의 적용 절차" } ]
}
```

- **slot 규칙**: `primary` 정확히 1개 + `supporting` 1~2개(모듈 총 2~3).
  모듈 `layout`에 `composite`은 올 수 없다(재귀 금지). 모듈 `layout`에도
  구별칭이 최상위와 같은 규칙으로 정규화된다(경고도 동일 — 아래 검수).
  composite은 최상위 `title`이 선택인 유일한 layout이다 — 모듈 제목들이
  장 구성을 대신한다.
- **모듈은 각자 결론형 제목을 가진다** — 모듈 `title`은 필수이고 "구성"·
  "절차" 같은 주제 라벨이 아닌 명제로 쓴다. 모듈 `note`도 각자 렌더된다
  (생략 시 기본 고지문이 모듈마다 붙는다 — 고지 중복이 싫으면 모듈 `note`를
  짧게 준다).
- **배분 규칙 — 측정 우선, 자동 축소 없음(개정 6판)**: 도식 헤더(kicker·
  title) 높이를 먼저 빼고(헤더 선차감), 가용높이 = 프레임 85% − 헤더에서
  주 ≤ 60%, 보조는 잔여 균분, 슬롯 사이 간격(GAP) 24pt. 각 모듈은 단독
  펜스와 동일하게 먼저 측정되며, 배분을 넘으면 축소하지 않고 에러다:
  - 주 초과: `primary {layout} 측정높이 {h}pt > 배분 {H}pt — 주 모듈 요소 수 감소 또는 펜스 분할 권장`
  - 보조 초과: `supporting {layout} 측정높이 {h}pt > 배분 {H}pt — 보조 모듈 {n}을(를) 별도 펜스로 분할 권장`
  - 총량 초과: `도식 높이 {y}pt > 프레임 {H}pt(85%) — 펜스 분할 권장`
- 해결 레버는 기존과 같다 — 글자 축약·요소 수 감소·펜스 분할. 배분이
  닿지 않으면 모듈을 억지로 넣지 말고 아예 별도 펜스로 나눈다.
- I1: 모듈 내부 필드 전부(`modules[j].` prefix) 숫자-evidence 검사 대상이다.
  모듈 `evidence`가 있으면 모듈 숫자는 그 근거로 검증되고, 없으면 상위 펜스
  `evidence`로 폴백된다 — 어느 쪽도 없으면 치명(검수 시트의 evidence 열이
  행마다 실제 검증에 쓰인 근거를 보여준다).

### 공통 필드

| 필드 | 필수 | 규약 |
|---|---|---|
| `layout` | O | `flow`·`cards`·`matrix`·`before_after`·`ladder`·`roadmap`·`topology`·`approval`·`layers`·`composite` (구별칭 `process`→flow, `principles`·`dashboard`→cards, `quadrant`→matrix 정성, `bridge`→before_after, `network`→topology — 자동 변환, composite 모듈 layout에서도 동일) |
| `title` | O (composite 최상위는 선택) | 결론형 명제 — 주제 라벨 금지. composite 모듈 `title`은 필수 |
| `modules` | composite | 2~3개 `{slot, layout, …}` 배열. `slot`(`primary` 1 + `supporting` 1~2)은 **모듈 전용 필수 필드** — 모듈 layout에 `composite`은 금지(재귀) |
| `steps` | flow | 2~8개(판형 상한표), 각 `{title, text}` — 둘 다 필수 |
| `lanes` | flow | `steps`와 배타. 각 `{actor, steps}` — 레인 셀 수는 판형 상한표 |
| `cards` | cards | 2~6개(판형 상한표), 각 `{title, text, 선택 value}` |
| `headers`+`rows` | matrix 격자 | 열 2~상한·행 2~6. 셀은 문자열 |
| `x_axis`·`y_axis`·`cells` | matrix 정성 | 축은 `{low, high}`, cells 4개 각 `{title, text}` — 격자 키와 배타 |
| `before`+`after` | before_after | 각 1~5개(하한 1·절대 상한 5)의 문자열 배열 — 판형 상한은 많은 쪽 기준 |
| `center` | before_after | 선택 — 중앙 전환 라벨(초단문, 폭 68pt) |
| `before_label`/`after_label` | before_after | 선택 — 패널 라벨(기본 "이전"/"이후") |
| `stages` | ladder | 3~5개(절대 범위 + 판형 상한 — essay 4, 나머지 5), 각 `{title, text}` |
| `phases` | roadmap | 2~5개(판형 상한 우선), 각 `{period, title, items 1~4}` |
| `nodes`+`edges` | topology | 노드 3~상한(판형 상한표), 각 `{id, label}`. 간선은 선택 `{from, to, dashed}` — 층위 ≤ 4 |
| `path` | approval | 3~6개(팩별 실질 상한 — 스텝 폭 하상수), 각 `{title, 선택 text, 선택 gate}` — 게이트 ≤ 4 |
| `stack`/`rings` | layers | `{label}` 배열 — 스택(전폭 행) 또는 동심원(배타). 계층 수는 높이 예산이 상한 |
| `thesis` | | 한두 문장 설명 |
| `kicker` | | 짧은 영문·한국어 라벨(도식 상단) — **초단문 1줄 계약**(줄바꿈 없음) |
| `note` | | 고지문. 생략 시 기본문: "편집 요약: 본문의 장·절 구조와 핵심 문장을 재배열한 도식이며, 원문을 대체하지 않습니다." |
| `evidence` | | `"§N"` — 같은 챕터 md의 N번째 `## ` 헤딩 범위(보통 §1 = 장 전체). 숫자가 있으면 필수(아래). composite 모듈은 모듈 `evidence` 우선·상위 펜스 값 폴백 |

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
- emit은 모든 상자 텍스트 ops에 `max_w`(상자 텍스트 폭)를 강제한다 — 문구가
  상자 폭을 초과하면 상자 밖으로 흘러나가는 대신 **상자 안에서 줄바꿈**된다.
  따라서 아래 예산 치트시트와 렌더 결과가 일치한다(밀도 상한 3줄은 I1이
  검사).
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
83.5pt(3) / 55.6pt(4) · 구성 노드 83.5pt(무간선 grid 3열) / 55.6pt(층위 4열)
· 결재 스텝 83.5pt(3스텝) / 55.6pt(4스텝) · 계층 스택 행 306.5pt(전폭−28)
· 링 12시 현 102.2pt(최외곽 4링) / 39.4pt(최내곽).

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
| 구성 노드 라벨 | 9pt | ~11자(83.5pt) · ~6자(55.6pt) |
| 결재 경로 제목 | 11pt | ~9자(83.5pt) · ~5자(55.6pt) |
| 결재 경로 본문 | 9pt | ~11자(83.5pt) · ~6자(55.6pt) |
| 계층 스택 라벨 | 9pt | ~47자(스택 행 306.5pt) |
| 링 라벨 | 9pt | ~14자(최외곽 102.2pt) · ~4자(최내곽 39.4pt) |

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
- **composite 배분**(practical 기준): 주 모듈 ≤ 가용높이의 60%(가용높이 =
  프레임 85% − 헤더, 헤더 선차감) · 보조 모듈은 잔여 균분 · 슬롯 간 GAP
  24pt · 총 도식 높이 상한 프레임 85%. 모듈 텍스트 예산은 각 모듈 레이아웃의
  위 표 행을 그대로 적용한다.
- 라틴 장토큰(URL·약어)은 한글 1자의 0.55배 폭으로 환산된다.

## 골든 교정 절차 (스펙 §7 — 1~3주기 완료 2026-08-22, archetype 추가·계수 드리프트 의심 시 반복)

1. calib fixture(경계 문구 고정 세트 — 1주기 `calib-cards.md`, 2주기
   `calib-before-after.md`·`calib-ladder.md`·`calib-roadmap.md`, 3주기
   `calib-topology.md`·`calib-approval.md`·`calib-layers.md`)를
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
7. 3주기 결과(2026-08-22, Phase 4 archetype 3종 추가 후 — fixture 3종 ×
   5팩 전수 15렌더, 동일 2중화 프로브): 팩 평균 비율 practical 0.594(드리프트
   −0.016) · essay 0.626(−0.034) · b5 0.608(−0.022) · business 0.700(−0.000) ·
   lecture 0.707(+0.007) — 전 팩 |드리프트| < 0.05 데드밴드 내,
   **PACK_KO_FACTOR 유지**(budget.py·골든 9종 불변). regular 자당폭 실측은
   2주기와 동일(practical/b5 6.759 · essay 7.866 · business 8.208 ·
   lecture 7.776pt). 스팬 매칭은 preview 여백 12mm(34.02pt) 기하 보정.

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

- 빌드 직후 `gate-report.json`의 `infographic_pages`를 읽는다 — `count`(PDF에서
  `ig-fig` metadata로 실측한 도식 페이지 수) · `expected`(manifest 총 도식
  수) · `match`(count == expected). `match`가 거짓이면 도식이 인쇄물에서
  누락·중복된 것이다 — 펜스와 빌드 로그를 재확인 후 재빌드한다.
- qc_gate은 도식 페이지를 `build/infographic/review-p*.png`(170 DPI)로
  렌더해 둔다. 시트 대조와 함께 **PNG 눈검**을 한다(스펙 §5.4): 카드 내부
  줄바꿈 · 표 셀 잘림 · 화살표 충돌 · 작은 글씨 · 텍스트 카드 밖 이탈.
- 빌드 시 도식마다 `build/infographic/NNN-figNN.review.md` 검수 시트가 생성된다
  — 5열: 요소 | 문구 | evidence | 교차검증 | 확인란. 원문 대조와 위 PNG
  눈검을 마친 뒤 요소별 확인란과 하단 `- [ ] 원문 대조 완료` 체크박스를
  채운다(`- [x]`) — 눈검은 체크의 전제 절차다.
- qc_gate은 미완료 검수 시트가 남아 있으면 **WARN**을 출력한다(에러 아님 —
  검수는 사람 판단. final/ 생성은 기존 규칙 그대로).
- I1 "미검증" 플래그(타 챕터 인용·evidence 불해석 숫자)는 기계 교차검증을
  건너뛴 것이다 — **사람 대조 필수**. 해당 도식 시트 상단에 경고로 표시된다.
- 구별칭(`process`→flow 등 — composite 모듈 layout 포함)로 쓴 펜스는 빌드는
  되지만 콘솔 경고와 함께 검수 시트 상단에 `별칭 … — 정식 키워드 권장` 줄이
  남는다 — 다음 펜스부터 정식 키워드로 바꾼다.
