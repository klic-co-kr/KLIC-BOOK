# Attribution

이 책은 다음 논문의 한국어 해설서(정독서)다. 원문 내용을 요약·재구성하여 한국어로
서술했으며, 원문의 문장을 그대로 옮기지 않았다.

- **EvoHarness-RL: Learning Self-Evolving Runtime Harness for Long-Horizon LLM
  Agents** — Xuying Ning, Dongqi Fu, Tianxin Wei, Hanqing Zeng, Yuanchen Bei,
  Bingxuan Li, Zihao Li, Qifan Wang, Xiang Shen, Yifan Wu, Jiayi Liu, Hong Li,
  Yinglong Xia, Xiangjun Fan, Hanghang Tong, Jingrui He. University of Illinois
  Urbana–Champaign · Meta AI, 2026. arXiv:2608.05446.
- 원문: <https://arxiv.org/abs/2608.05446> (HTML: <https://arxiv.org/html/2608.05446v1>)
- 코드: 논문에 공개 코드 저장소 링크 없음(v1 기준).

## 그림

본문에 실린 그림 5장(fig-1 ~ fig-5)은 위 논문의 Figure 1–5를 arXiv HTML판에서
확보한 것이다. 원 저자들에게 감사드린다. 그림 내부의 영어는 원문이며, 본문 한글
캡션은 이 책이 덧붙인 해설이다.

- fig-1 ← 원문 Figure 1 (EvoHarness-RL 개관 — 하니스를 BPE 세 상태로 추상화)
  — arXiv HTML 임베드 PNG 원본 그대로 (1969×750)
- fig-2 ← 원문 Figure 2 (2단계 학습 파이프라인 — SFT → cost-aware GRPO)
  — arXiv HTML 임베드 PNG 원본 그대로 (1739×540)
- fig-3 ← 원문 Figure 3 (GRPO 진행에 따른 하니스 호출 수 감소 — 담금질)
  — arXiv HTML 임베드 PNG 원본 그대로 (631×367)
- fig-4 ← 원문 Figure 4 (경험 저장소 진화 — 기술 은행의 팽창 후 수렴)
  — arXiv HTML 임베드 SVG(skill_counts_gray_gold.svg)를 2032px 폭으로 래스터화
- fig-5 ← 원문 Figure 5 (액션별 하니스 담금질 — BPE 액션별 감소 속도 차이)
  — arXiv HTML 임베드 SVG(harness_action_distribution.svg)를 1950px 폭으로 래스터화

표(Table 1–3)는 원문 수치를 책용 마크다운 표로 재조판한 것이다.

## 유의

- 원문은 2026-08-05 공개 v1 기준. 인용 수치·표기는 모두 v1 실측치다.
- 논문 저자명·소속은 원문 HTML 저자 블록에서 확인한 그대로다.
