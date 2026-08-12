# 대규모 언어모델(LLM) 강좌 2025 — 한국어 번역판

동경대학교 마츠오·이와사와 연구실 LLM 강좌(8일 과정) 슬라이드의 한국어 번역.

> © 2025 東京大学 松尾・岩澤研究室, CC BY-NC-ND 4.0. 교육 목적 번역. 원문 의미 변경 없음.

## 파이프라인

```
원문 PDF (day1-8 슬라이드) ──pdf-to-md──▶ manuscript/ (일본어 원문)
                                       └─ 일→한 번역·가다듬기 ──▶ manuscript-ko/ (한국어 출간 원고)
```

## 폴더

- `manuscript/` — 일본어 원문(`pdf-to-md` 변환)
- `manuscript-ko/` — 한국어 번역·가다듬기 출간 원고
  - [`00-frontmatter.md`](manuscript-ko/00-frontmatter.md) — 표지·저작권·서문·목차
  - [`day1.md`](manuscript-ko/day1.md) ~ [`day8.md`](manuscript-ko/day8.md) — 일차별 번역
- `assets/images/` — 슬라이드 그림(1733장)

## 목차

| 일차 | 주제 | 크기 |
|------|------|------|
| [Day 1](manuscript-ko/day1.md) | LLM 개요 · 스케일링 법칙 · 멀티모달 | 63K |
| [Day 2](manuscript-ko/day2.md) | 추론 · 프롬프팅 · Decoding · RAG | 41K |
| [Day 3](manuscript-ko/day3.md) | 사전학습(1) — 토크나이저 · 트랜스포머 구조 | 110K |
| [Day 4](manuscript-ko/day4.md) | 사전학습(2) — 스케일링 법칙 · 분산학습 · MoE | 70K |
| [Day 5](manuscript-ko/day5.md) | 사전학습(3) — 효율화 · 양자화 · 최신동향 | 76K |
| [Day 6](manuscript-ko/day6.md) | 파인튜닝 — Instruction · RLHF · DPO · PEFT | 47K |
| [Day 7](manuscript-ko/day7.md) | 강화학습·얼라인먼트 심화 | 118K |
| [Day 8](manuscript-ko/day8.md) | 학습 데이터 · 평가 · 벤치마크 | 107K |

번역 원고 합: 약 633KB.

## 원문 출처

- 강좌 페이지: https://weblab.iii.u-tokyo.ac.jp/lecture/
- 라이선스: CC BY-NC-ND 4.0 (비영리 · 변경금지). 번역은 원문 의미 보존 범위의 가다듬기만.
