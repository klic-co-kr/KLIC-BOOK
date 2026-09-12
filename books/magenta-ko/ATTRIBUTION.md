# 루프를 닫다 — 출처 기록

## 기반 논문 (전 장)

- Magenta: Closing the Loop Between Mathematical Reasoning and Lean Verification — arXiv 2609.11319v1(2026) · Joshua Ong Jun Leang·Haonan Li·Zheng Zhao·Xinyi Shang·Wenda Li·Zhengzhong Liu·Eric Xing·Shay B. Cohen·Eleonora Giunchiglia(MBZUAI Institute of Foundation Models·University of Edinburgh·University College London·Imperial College London) · https://arxiv.org/html/2609.11319v1
- 원문 사본(집필용·보존): docs/task-id/magenta-ko/sources/magenta-2609.11319v1.md(HTML→텍스트 변환 + 검증 수치표 부록 Tables 1·2·3·5·6·7·8)
- 본문 수치는 전부 원문 표와 실험 설정 절에서 확인한 값만 인용(계획 번들 §4 수치 계약·§0 G-1~G-5 준수).

## 그림 (9면 — 원문 Figure 1~6 원본 이미지 삽입, 사용자 지정)

- 사용자 요청("그래프 도식표등 스크린샷하고 책 제작")에 따라 원문 그림을 원본 해상도로 수록했다. 그림 1(x1.png 원본 PNG)과 그림 2~6(원문 HTML 내장 SVG 8종)을 arXiv 서버에서 직접 확보했고, SVG는 resvg 4배 랜스터화로 인쇄 품질을 확보했다(크롬 브라우저가 다운 상태라 원본 이미지 직접 확보로 동일 결과를 얻음 — 해상도는 스크린샷보다 우수).
- 매핑(원문 파일명 → 책 파일명): x1.png → fig1-overview.png · 07_self_corrections_per_problem.svg → fig2-self-corrections.png · 01_goedel_vs_codex_formal_statement_calls_notitle_enhanced_v2.svg → fig3-statement-calls.png · 01_pass_rate_vs_internal_calls_enhanced_v2.svg → fig4-internal-calls.png · 07_codex_external_vs_leanstral_internal_plus_external_calls_log_enhanced_v2.svg → fig5a-total-calls.png · external_02_codex_vs_leanstral_code_failure_rounds_enhanced_v2.svg → fig5b-failure-rounds.png · 05_codex_vs_leanstral_reasoner_tokens_enhanced_v2.svg → fig5c-reasoner-tokens.png · 06_codex_vs_leanstral_final_lean_code_tokens_enhanced_v2.svg → fig5d-lean-code-length.png · 01_final_k3_solution_tokens_iclr.svg → fig6-imo-tokens.png
- 캡션 번호는 원문 Figure 번호를 그대로 사용(그림 1~6, 그림 5는 (a)~(d) 패널) — 독자가 원문과 대조할 수 있게 하는 설계.
- 원문 저작권(arXiv 비독점 라이선스) 하의 정독 해설서로, 그림은 학술 인용 목적 수록.

## 표 (원문 Tables 1·2·3·5·6·7·8 한국어 재구성)

- 전 셀 수치는 원문과 1:1. 컬럼 ≤5·행 ≤9 압축(Table 6은 19→8행, Table 7은 11→8행) — 미수록 행은 본문 서술로 커버.

## 각색 범위

- 14장 '한국 현장에서 읽는 Magenta'만 필자 각색이며, 장 머리에 각색임을 명시. 나머지 전 장은 원문 정독·해설.
