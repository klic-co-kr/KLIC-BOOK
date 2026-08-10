# 실전 시스템 설계 2026 — Markdown 원고 패키지

이 패키지는 계획서가 아니라 **38장 전체 실제 1차 초고**다.

## 바로 볼 파일

- `BOOK.md` — 전 장을 합친 단일 Markdown 책
- `TABLE_OF_CONTENTS.md` — 38개 장과 부록을 연결한 링크형 목차
- `manuscript/` — 7부 38장과 머리말·부록으로 분리한 원고
- `book.manifest.yaml` — 책의 단일 진입 manifest
- `manifests/assets.yaml` — 119개 시각자료의 종류·상태·경로
- `IMAGE_PLAN.md` — 장별 이미지 배치표
- `IMAGE2_PROMPTS.md` — 19개 Image2.0 프롬프트 합본
- `assets/specs/svg/` — 88개 순수 SVG 제작 명세
- `assets/specs/charts/` — 12개 차트 제작 명세
- `REPORT.md` — 생성·검증 결과

## 현재 정확한 상태

- 본문: 38장 모두 1차 초고 작성
- 시각자료: 119개 모두 상세 명세 작성, 실제 binary는 미생성
- 출처: 장별 citation key와 URL 등록, 출판 전 current/volatile 재검증 필요
- 출판 준비: 기술·문장·접근성·저작권 최종 검수 전

## 검증

```bash
python scripts/validate_package.py
```

## 원본 계보

The System Design Primer의 기준 revision은 `ae9bbd7`이며, 변경·추가 관계는 `manifests/upstream-map.yaml`에 기록했다. 자세한 고지는 `ATTRIBUTION.md`를 참조한다.
