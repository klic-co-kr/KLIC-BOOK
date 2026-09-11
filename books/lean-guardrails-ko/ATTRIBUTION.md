# 결정론적 가드레일 — 출처 기록

## 기반 논문 (1부·3부: 00~09, 14장)

- Type-Checked Compliance: Deterministic Guardrails for Agentic Financial Systems Using Lean 4 Theorem Proving — arXiv 2604.01483v1(2026) · Devakh Rashie·Veda Rashi(Thomas Jefferson High School for Science and Technology) · https://arxiv.org/html/2604.01483v1
- 원문 사본(집필용): docs/task-id/guardrails-book/sources/base-paper-2604.01483.md
- 그림 추출: 없음(이미지 자산 미사용 — 표 1개 재구성, 벡터 도식 5개는 원고 내 펜스에서 생성)
- 원문 오류 정정 1건: 원문 §3.1은 Knight Capital(2012)을 15c3-5 도입의 후행 사건처럼 서술했으나 실제 채택은 2010년(SEC Release 34-63241). 6장에서 연대 단서와 함께 교정 서술(②위험 렌즈 H1).

## 추가 논문 (2부: 10~13장 — 배치 D·E 실물 확인 완료, ②기술 오류 렌즈 10/10 대조 일치)

- 10장: Position: AI Governance Needs ISO-like Interoperability Protocols, Not Just Laws — arXiv 2608.14568(2026) · Azmine Toushik Wasi 외 5인(ICML 2026 Position Track Spotlight — abs 페이지에 소속 미기재, 소속 표기 생략) / Digital Transformation in the Public Administrations: a Guided Tour For Computer Scientists — arXiv 2305.05551(2023) · Paolo Ciancarini, Raffaele Giancarlo, Gennaro Grimaudo(소속 미기재, 표기 생략)
- 11장: Enabling Content Management Systems as an Information Source in Model-driven Projects — arXiv 2508.19797(2025 게시, 원저 RCIS 2022) · Joan Giner-Miguelez, Abel Gómez, Jordi Cabot / From Chatbot to Digital Colleague: The Paradigm Shift Toward Persistent Autonomous AI — arXiv 2606.14502(2026) · Yongheng Zhang 외 19인
- 12장: From Logic to Toolchains: An Empirical Study of Bugs in the TypeScript Ecosystem — arXiv 2601.21186(2026) · TianYi Tang, Saba Alimadadi, Nick Sumner(사이먼 프레이저 대학교) / MobileDev-Bench: A Comprehensive Benchmark for Evaluating Language Models on Mobile Application Development — arXiv 2603.24946(2026) · Moshood A. Fakorede, Krishna Upadhyay, A. B. Siddique, Umar Farooq(루이지애나 주립대·켄터키 대학교) / Developing Accessible Mobile Applications with Cross-Platform Development Frameworks — arXiv 2005.06875(2020) · Sergio Mascetti, Mattia Ducci, Niccolò Cantù, Paolo Pecis, Dragan Ahmetovic(밀라노 대학교)
- 13장: Memory-Safety Challenge Considered Solved? An In-Depth Study with All Rust CVEs — arXiv 2003.03296(2020) · Hui Xu, Zhuangbin Chen, Mingshen Sun, Yangfan Zhou, Michael R. Lyu(푸단대·홍콩중문대·바이두 보안) / A Study of Real-World Data Races in Golang — arXiv 2204.00764(2022) · Milind Chabbi, Murali Krishna Ramanathan(Uber) / Getting Python Types Right with RightTyper — arXiv 2507.16051(2025) · Juan Altmayer Pizzorno, Emery D. Berger(매사추세츠 대학교 애머스트)

## 도식

- 05장 approval·08장 layers·09장 matrix·14장 roadmap — ```infographic 엔진(원고 펜스, lint --style lecture 통과)
- 11장 flow — ```diagram 엔진(원고 펜스, diagram.py lint 통과)
- 도식-페이지 매핑 WARN은 typst shim이 `query` 미지원인 환경 한계(도식 실재는 PDF p19-20·29·31·39·49 수동 검증 완료 — 11장 도식은 p39)
