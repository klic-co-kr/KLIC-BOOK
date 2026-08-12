# 산출물 계약

## Book 모드

```text
out/
├── <제목>_<판본>.pdf
├── book.html
├── source_manifest.json
├── build_report.json
├── verification/
│   ├── verification.json
│   └── verification.md
├── rendered/
├── contact-sheet*.jpg
└── summary/                       # 선택
```

최종 사용자에게는 PDF, 검증 보고서, SHA-256을 우선 제공한다. HTML·렌더 PNG·접촉표는 편집 추적과 시각 검수에 사용한다.

## Manual 모드

```text
out/
├── index.html
├── overview.html
├── lessons/
│   └── <lesson-id>.html
├── assets/
│   └── manual.css
├── media/                         # manual.yaml이 참조한 파일만
├── sources/
│   └── evidence-map.md
├── qa/
│   ├── build-report.json
│   ├── visual-review.json          # 실제 브라우저 검수를 수행한 경우
│   ├── verification.json
│   └── verification.md
├── manual-manifest.json
├── STATUS.md
└── HANDOFF.md
```

- `index.html`: 전체 업무 흐름, trigger, 목표, 결과, lesson 순서
- `overview.html`: 역할, 구성요소, 생명주기, 정신 모형, 초보자 오해
- `lessons/*.html`: 목적, 사용 시점, 준비, 안전, operation/action/evidence/success, write readback, 주의, 실수, 완료, 근거, 다음 분기
- `evidence-map.md`: 근거 등급·경로·확인일·사용 lesson 추적
- `verification.json`: technical/content/visual을 분리한 판정과 근거·DOM 변조 검사 결과
- `visual-review.json`: 검수자, 날짜, viewport, 방문 페이지, 키보드·탐색·콘솔 결과, finding의 severity/status
- `STATUS.md`: 현재 상태와 자동 검증 외 미확인 범위
- `HANDOFF.md`: 시작점, 판본, 근거, QA 경로, 완료 주장 경계

`provisional` 패키지는 사용자 화면에 상태 배너를 포함한다. `final`은 고위험 오류가 0이고 핵심 동작이 inference-only가 아니며 시각·사용성 검수 범위가 기록된 경우에만 사용한다.
`findings`의 severity는 `low|medium|high|critical`, status는 `open|resolved|accepted`를 사용한다. high/critical은 `resolved`가 아니면 final 검증에 실패한다.

## Hybrid 모드

같은 근거 원장을 사용하되 Book과 Manual 산출물을 별도 출력 폴더에 생성한다.

```text
out/
├── book/
└── manual/
```

PDF의 장 구조를 HTML lesson으로 기계적으로 복사하지 않는다. 독자 목적과 업무 흐름에 맞게 각각 구성하고 공통 주장만 같은 근거 ID로 추적한다.

## 파일명 규칙

- 운영체제 금지문자를 제거한다.
- 제목을 임의 약어로 줄이지 않는다.
- `final`, `최종`, `진짜최종2` 같은 누적 이름 대신 판본 또는 날짜를 쓴다.
- URL과 파일명은 고정된 slug를 사용한다.
