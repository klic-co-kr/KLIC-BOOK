# 대규모 언어모델(LLM) 강좌 2025

### 동경대학교 마츠오·이와사와 연구실

---

## 저작권

本資料は © 2025 東京大学 松尾・岩澤研究室 が CC BY-NC-ND 4.0 라이선스로 공개한 「LLM 大規模言語モデル講座 講義資料」를 한국어로 번역한 교육 목적 자료다.

- 원저작자: 東京大学 松尾・岩澤研究室 (MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO)
- 원문 라이선스: CC BY-NC-ND 4.0 (저작자표시 — 비영리 — 변경금지)
- 번역: 원문의 의미를 변경하거나 추가하지 않았다. 번역본 역시 동일 라이선스를 따른다.
- 원문 출처: https://weblab.iii.u-tokyo.ac.jp/lecture/

> CC BY-NC-ND 의 '변경금지(ND)' 조건에 따라, 번역은 원문 의미 보존 범위에서 슬라이드 단문을 자연스러운 한국어 서술로 가다듬은 것이다. 내용 추가·삭제·변경은 없다.

## 역자 서문

이 자료는 2025년 동경대학교 마츠오·이와사와 연구실이 공개한 LLM 대규모 언어모델 강좌(8일 과정)의 강의 슬라이드를 한국어로 번역한 것이다. 일본어 LLM 교육 자료 중 가장 체계적이고 깊이 있는 자료 중 하나로, 사전학습부터 평가·얼라인먼트까지 전 과정을 다룬다.

번역은 PDF 슬라이드 → 텍스트 추출(`pdf-to-md` 스킬) → 한국어 번역·가다듬기 파이프라인으로 진행했다. 슬라이드 특유의 단편적 단문을 문맥이 통하는 서술로 합쳤고, ML/AI 전문 용어는 영문 보존 또는 한국어 관례를 따랐다. 코드·수식·참고문헌·그림 참조는 원문 그대로 유지했다.

## 강좌 구성 (전 8일)

| 일차 | 주제 |
|------|------|
| [Day 1](day1.md) | LLM 개요 — 언어모델 역사, GPT·트랜스포머, 스케일링 법칙, 멀티모달·로봇 응용, 일본 LLM 환경 |
| [Day 2](day2.md) | 추론·프롬프팅 — Decoding, Prompting, Few-shot, Chain-of-Thought, RAG, Tool-use, 모델 선택 |
| [Day 3](day3.md) | 사전학습(1) — 토크나이저, 트랜스포머 구조(Attention, FFN, 정규화), 학습 |
| [Day 4](day4.md) | 사전학습(2) — 스케일링 법칙, 데이터, 분산 학습, MoE |
| [Day 5](day5.md) | 사전학습(3) — 효율화(FlashAttention, 양자화), 최신 동향(Chinchilla, BitNet) |
| [Day 6](day6.md) | 파인튜닝 — Instruction Tuning, RLHF, DPO, PEFT(LoRA 등) |
| [Day 7](day7.md) | 강화학습·얼라인먼트 — RLHF 심화, GRPO, 보상 모델, 평가 |
| [Day 8](day8.md) | 학습 데이터·평가 — 데이터 필터링·확장, SFT, 벤치마크(MMLU, Chatbot Arena), LLM-as-a-Judge |

## 사용 안내

- 각 일차는 원문 슬라이드 순서를 그대로 따른다.
- 슬라이드 그림은 `../assets/images/dayN-fig-NNN-MM.png`에 있다.
- 전문 용어(Layer Normalization, Cross-Entropy, Instruction Tuning, RLHF 등)는 영문을 우선 보존했다.
- 원문의 수식·코드·참고문헌은 변경하지 않았다.
