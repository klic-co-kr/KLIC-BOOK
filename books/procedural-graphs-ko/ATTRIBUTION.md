# ATTRIBUTION — procedural-graphs-ko

- 원문: "Procedural Graphs: Self-Evolving Execution Structures for LLM Agents"
  - 저자: Yuxing Lu (Google·Georgia Tech·Peking University), Yicheng Chen (Google), Shanchan Wu (Google), Sercan Ö. Arık (Google, 교신저자)
  - 식별자: arXiv:2609.09153v1 [cs.AI], 2026-09-08 공개
  - 원문: https://arxiv.org/abs/2609.09153
- 본 위키(책)의 성격: 원문 논문의 한국어 정독서(요약·재구성 아닌 전 장 충실 번역 계열). 36쪽 원문 전체(본문 §1–6 + 부록 A–F)를 12개 장으로 재구성했다.
- 번역 범위·매핑:
  - 00-들어가며 ← 초록·전체
  - 01-왜-절차-그래프인가 ← §1 (pp.1–2), Figure 1 서술 재현(도면)
  - 02-관련-연구 ← §2 (p.3) + 부록 A (pp.16–18, 8차원 비교표 요약 수록)
  - 03-절차-그래프-프레임워크 ← §3 (pp.3–6), 식 (1)–(6) LaTeX 전재
  - 04-실험-설계 ← §4 (p.6) + 부록 B 핵심 (pp.19–24)
  - 05-주요-결과 ← §5.1 (pp.7–8), Table 1 재구성(축약)
  - 06-장기-의사결정과-생존 ← §5.2 (p.8) + 부록 C (pp.24–28)
  - 07-그래프-구축-전략 ← §5.3 (p.9) + 부록 D (pp.29–30), Table 2 전재
  - 08-자기진화-10라운드 ← §5.4 (pp.9–10) + 부록 E (pp.31–34)
  - 09-효율성-분석 ← §5.5 (p.10), Table 3 전재
  - 10-결론-실무-시사점 ← §6 (p.11) + 실무 시사점(해설)
  - 11-부록-프롬프트와-알고리즘 ← 부록 B.5–B.6 (pp.21–24) + 부록 F (pp.35–36)
- 그림: 원문 그림 4종을 본문에서 고해상도(4배) 추출해 assets/에 두고 재수록했다.
  - assets/fig1-kg-pg.png ← 원문 Figure 1 (p.2) — 그림 1-1로 재수록
  - assets/fig2-framework.png ← 원문 Figure 2 (p.4) — 그림 3-1로 재수록
  - assets/fig3-survival.png ← 원문 Figure 3 (p.8) — 그림 6-1로 재수록
  - assets/fig4-evolution.png ← 원문 Figure 4 (p.9) — 그림 8-1로 재수록
  추출 이미지의 저작권은 원 저자에게 귀속된다(인용·재수록 목적).
  이와 별개로 책 도면 규약(```diagram 펜스)으로 한국어 라벨 보조 도면 4종을
  저작해 삽입했다(그림 3-2 온라인 흐름, 그림 3-3 자기진화 루프,
  그림 6-2 선제적 자금조달, 그림 8-2 채택·거부 타임라인).
- 표: Table 1은 4모델×7기법×6벤치마크 원형을 축약 재구성했고, Table 2·3은 전재했다.
  신뢰구간 대괄호 표기는 축약 과정에서 생략한 것도 있다.
