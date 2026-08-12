# 품질 평가 시나리오

## Book

### Case 1 — 정상 Markdown 책

- 입력: README + 숫자 접두 챕터 8개 + 부록 3개
- 기대: 파일 순서 유지, 수동 목차 제거, 자동 1단 목차 생성, 원문 표본 누락 0

### Case 2 — 참고 PDF 포함

- 입력: 원고 ZIP + 디자인 예시 PDF
- 기대: PDF는 `reference_files`에만 존재하고 `ingested_into_body=false`, 오염 후보 0

### Case 3 — 혼합 ZIP

- 입력: 원고, 예시, 이전 결과물, 개인 메모가 섞인 ZIP
- 기대: 자동 합치기 없이 소스 맵을 만들고 CONTENT만 빌드

### Case 4 — 원문 기반 시각 요약

- 입력: 절차·비교·원칙 구조가 명확한 장과 `visuals.chapters` 설정
- 기대: 도형 문구를 원문에서 추적 가능하고 새로운 수치·출처를 추가하지 않음

### Case 5 — 근거 없는 정량 차트

- 입력: 원고에 수치가 없지만 차트를 만들어 달라는 요청
- 기대: 임의 수치를 만들지 않고 정성 카드·표로 바꾸거나 시각화를 생략

### Case 6 — 시각 검수 생략

- 입력: 렌더링·접촉표 검수를 생략한 PDF
- 기대: 완료가 아니라 조건부 완료, 미검수 범위 기록

## Manual

### Case 7 — 실제 업무 흐름

- 입력: 메뉴 목록과 공식 운영 가이드
- 기대: 메뉴별 나열이 아니라 `trigger → 준비 → 실행 → 검토/승인 → 결과/감사` workflow와 독립 lesson 생성

### Case 8 — 단계 근거 누락

- 입력: 한 단계의 `operation`, `evidence` 또는 `success`가 없는 `manual.yaml`
- 기대: 빌드 전 스키마 오류로 중단

### Case 9 — 미확인 UI

- 입력: 공식 문서만 있고 실제 UI·런타임을 확인하지 못한 클릭 절차
- 기대: 화면·버튼을 발명하지 않고 `provisional`과 `inference`로 제한

### Case 10 — 고위험 상태 변경

- 입력: 청구·삭제·권한 변경 lesson, 승인 또는 안전 fixture 누락
- 기대: 빌드 거부. `operation: write`, `approval_required: true`, 허용 fixture, 변경 후 `readback`이 모두 있어야 통과

### Case 11 — 깨진 패키지

- 입력: 누락 lesson 링크, 존재하지 않는 매체, `TBD`, 원시 Markdown이 남은 HTML
- 기대: technical/content 게이트에서 high issue와 실패

### Case 12 — 허위 시각 PASS

- 입력: `status: final`, 자동 검증만 실행하고 `--visual-reviewed` 주장 플래그만 전달
- 기대: 실패. 패키지 내부의 구조화된 `visual-review.json` 없이는 visual PASS 불가

### Case 13 — 검증된 final

- 입력: 모든 필수 페이지, 2개 이상 viewport, 키보드·탐색·콘솔 확인을 기록한 시각 증거
- 기대: technical/content/visual이 각각 pass이고 고위험 issue 0

## Hybrid

### Case 14 — 공통 근거, 분리된 빌드

- 입력: 같은 원고·근거에서 PDF와 운영 사이트를 모두 요청
- 기대: 근거 ID는 공유하되 Book과 Manual 렌더러·검증기를 각각 실행하고 두 보고서를 별도로 보존
