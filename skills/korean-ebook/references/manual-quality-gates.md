# 운영 매뉴얼 품질 게이트

## Gate 1 — 입력·근거

- [ ] CONTENT, EVIDENCE, REFERENCE, EXCLUDE가 분리되었다.
- [ ] 제품 버전과 근거 확인일이 기록되었다.
- [ ] source와 media의 SHA-256이 입력 원장과 실제 파일에서 일치한다.
- [ ] 화면·런타임 미확인 동작이 `provisional` 또는 `inference`로 표시되었다.
- [ ] 근거 파일 경로가 패키지 루트를 벗어나지 않는다.

실패하면 본문 제작을 중단한다.

## Gate 2 — 업무 흐름

- [ ] 기능 목록이 아니라 업무 목표와 결과를 기준으로 흐름을 나눴다.
- [ ] trigger, 준비, 실행, 검토/승인, 결과/감사가 연결된다.
- [ ] 분기·건너뛰기·실패·되돌리기 경계가 설명된다.
- [ ] workflow의 모든 lesson ID가 실제 lesson과 연결된다.

## Gate 3 — 초보자 개요

- [ ] 시스템 정의, 역할, 구성요소, 생명주기, 오해 교정이 있다.
- [ ] 상세 절차 전에 읽을 수 있다.
- [ ] 내부 구현명 대신 독자가 보는 용어를 사용한다.
- [ ] 정신 모형이 실제 상태 변화와 모순되지 않는다.

## Gate 4 — Lesson 깊이

- [ ] 목적·사용 시점·선행 조건이 있다.
- [ ] 모든 단계에 operation/action/evidence/success와 근거 ID가 있다.
- [ ] 주의·흔한 실수·완료 확인·다음 분기가 있다.
- [ ] index 카드의 짧은 문구를 반복한 페이지가 아니다.

## Gate 5 — 안전

- [ ] 상태 변경 위험도가 기록되었다.
- [ ] high/critical은 명시적 승인과 안전 fixture가 있다.
- [ ] write 단계는 readback으로 변경 후 ID·상태·부작용을 다시 확인한다.
- [ ] 실제 실행 전후 ID·상태·부작용을 readback한다.
- [ ] 전문 영역의 UI 안내와 전문 판단을 분리했다.

## Gate 6 — 기술 검증

- [ ] index, overview, 모든 lesson, CSS, 매니페스트, 근거 맵, STATUS, HANDOFF가 있다.
- [ ] HTML이 파싱되고 H1·title·main 구조가 있다.
- [ ] 내부 링크와 매체 경로가 모두 존재한다.
- [ ] 이미지 alt와 영상 접근 가능한 설명이 있다.
- [ ] 입력 매니페스트와 패키지 매니페스트가 일치한다.
- [ ] HTML step 텍스트, 근거 파일, 패키지 매체가 빌드 후 변조되지 않았다.
- [ ] symlink, active content, 외부 CSS·매체가 없다.

## Gate 7 — 내용·근거 검증

- [ ] 단계 수와 lesson HTML의 단계 수가 일치한다.
- [ ] 근거 ID가 원장에 존재한다.
- [ ] final 핵심 절차가 inference만으로 구성되지 않았다.
- [ ] 사용자 화면에 TODO/TBD/UI_CAPTURE_REQUIRED가 없다.
- [ ] 원시 Markdown 링크·HTML 태그·템플릿 변수가 노출되지 않는다.

## Gate 8 — 시각·사용성 검증

- [ ] 데스크톱과 모바일 대표 폭에서 잘림·겹침이 없다.
- [ ] 키보드로 탐색하고 포커스를 확인했다.
- [ ] overview → workflow → lesson → index 이동이 자연스럽다.
- [ ] 화면 증거의 필드·상태·강조가 설명과 일치한다.
- [ ] 영상이 있다면 재생, 자막/설명, 초점, 길이, 화면 근거를 확인했다.
- [ ] open/accepted high·critical finding이 없다.

자동 검증은 Gate 8을 대신하지 않는다. 실제 브라우저 검수 증거가 없으면 `visual: not_run`으로 보고한다.

## 판정

- `pass`: high issue 0
- `fail`: high issue 1개 이상
- `manual.status=final`: pass이면서 핵심 동작 근거와 시각·사용성 검수 범위가 기록됨
- `provisional`: 자동 검증은 통과할 수 있지만 미확인 UI·런타임·시각 범위가 남음
