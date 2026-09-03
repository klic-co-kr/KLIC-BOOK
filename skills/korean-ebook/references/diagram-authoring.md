# 다이어그램 저작 가이드 — ```diagram 펜스

인포그래픽(```infographic — 상자+문장의 편집 재배열)과 정량 차트(금지) 사이의
빈 자리를 채우는 선언적 벡터 도식 엔진. 구조·흐름·공간 관계를 전달하는
그림이 필요할 때 쓴다. 좌표는 엔진이 계산하고 저자는 노드·간선·레인만 쓴다.

## 언제 무엇을 쓰나

| 신호 | 도구 |
|---|---|
| 절차·승인 흐름 (순차·게이트·분기) | `diagram` flow |
| 순환 구조 (매 턴 반복) | `diagram` cycle |
| 사건·구간의 시간 전개 (회복·지연 비교) | `diagram` timeline |
| 누적·성장 비교 (쌓이는 것 대 고정된 것) | `diagram` stack |
| 자유 배치 씬 (아키텍처·대비 장면) | `diagram` scene |
| 항목 나열·카드형 요약 | infographic cards |
| 2축 비교·분류 | infographic matrix |
| 정량 통계 차트 | 금지 (데이터 날조 위험 — 책별 스크립트로 실측치만) |

## 펜스 규약

언어 `diagram`, 내용은 표준 JSON. 펜스 위치가 곧 그림 삽입 위치다.
빌드가 SVG를 `assets/diagrams/`에 내고 이미지로 치환한다 — 원고 md는
불변, resvg 래스터화·캡션 파이프라인은 기존 이미지 경로를 그대로 탄다.

```diagram
{
  "layout": "flow",
  "title": "결론형 명제 (40자 이내)",
  "sub": "보조 설명 (선택)",
  "caption": "그림 N-M 캡션 — alt 텍스트로 figure 캡션에 오른다",
  "nodes": [
    {"id": "a", "label": "관찰 수신"},
    {"id": "v", "label": "검증", "kind": "gate", "tone": "blue"},
    {"id": "c", "label": "상태 병합", "tone": "green"},
    {"id": "r", "label": "롤백 · 재시도", "tone": "red"}
  ],
  "edges": [
    {"from": "a", "to": "v"},
    {"from": "v", "to": "c", "kind": "ok", "label": "통과"},
    {"from": "v", "to": "r", "kind": "fail", "label": "실패", "side": "right"},
    {"from": "r", "to": "a", "kind": "back", "side": "left"}
  ]
}
```

### 공통 필드

| 필드 | 필수 | 규약 |
|---|---|---|
| `layout` | O | `flow`·`cycle`·`timeline`·`scene`·`stack` |
| `title` | O | 결론형 명제, 40자 이내 |
| `sub` | | 보조 설명 한 줄 |
| `caption` | | figure 캡션(미지정 시 title) |
| `tone` | | `blue`·`green`·`red`·`gray`·`amber` — 노드·레인·구간의 채색 |

### flow — 세로 플로우차트

- `nodes`: 2~8개 `{id, label(34자 이내), kind: box|gate|note, tone}`.
  `gate`는 다이아몬드(결정 관문), `note`는 점선 보조 상자.
- `edges`: `{from, to, kind: ok|fail|back, label, side: left|right}`.
  `side`가 있으면 해당 쪽으로 우회 루프. `fail`·`back`은 점선.

### cycle — 원형 순환

- `nodes`: 3~8개 `{label(12자 이내), tone}`, `center`: 중앙 라벨.

### timeline — 가로 타임라인

- `lanes`: 2~3개 `{name(12자 이내), tone, events, spans}`.
- `events`: 1~8개 `{label, major}` — `major`는 큰 마커+강조.
- `spans`: `{from, to, label, tone}` — 이벤트 인덱스 구간의 음영 띠.
- `axis`: 하단 축 이름.

### scene — 자유 배치 (탈출구)

- `nodes`: 2~12개 `{id, label(24자 이내), x, y, w, h, tone, sub, dash, size}`.
  좌표 직접 지정 — 다른 레이아웃으로 안 잡히는 씬(아키텍처 등)용.
- `edges`: `{from, to, kind, label, dash}` — 중심 간 직선.

### stack — 성장 스택

- `cols`: 2~6개 `{label, layers 1~12}`, `legend`: 층 범례 라벨(5종 색 순환).

## 검사·미리보기

```bash
python3 scripts/diagram.py lint manuscript/ch01.md
python3 scripts/diagram.py render manuscript/ch01.md --out /tmp
```

스키마 위반(키 누락·라벨 초과·없는 노드 참조)은 빌드에서 즉시 실패한다.

## 근거 경계

- 도식 언어로 새 사실을 창작하지 않는다 — 본문이 이미 말한 구조를
  공간·화살표로 재배열한다. 문구는 본문과 대응시켜 쓴다.
- 숫자를 도식에 넣을 때는 본문에 근거 문장이 있어야 한다.
