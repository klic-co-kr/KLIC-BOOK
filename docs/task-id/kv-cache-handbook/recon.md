# kv-cache-handbook 리컨 — 2026-09-07

## 원본 프로파일

- 원본: `Understanding_KV_Cache_Handbook_02_zh-CN.pdf` (33면, 514.8×720pt, 텍스트 레이어 有, 래스터 이미지 0 — 도표 전부 벡터)
- 원문 시리즈: @techNmak 「Understanding AI」 핸드북 02, 중문판(zh-CN)
- 부제: 从自回归解码到现代大语言模型推理 = "자기회귀 디코딩에서 최신 대언어모델 추론까지"
- 독자: AI 엔지니어·개발자·심화 학습자 대상 간명 기술 핸드북
- 분할 소스: `books/kv-cache-handbook-ko/references/source-zh/{0..31}-*.txt` (푸터 제거 완료, 32파일)
- 챕터당 283~586자(중문) — 소형·고밀도. 총 본문 약 12K자.

## 구조 지도

| 소스 | 내용 | 비고 |
|---|---|---|
| 00 | 导读 (들어가며) | 학습 목표 불릿 6, 선수지식 |
| 01–30 | 30개 챕터 | 각 1면 분량, 장마다 말미 `参考资料：[n]` |
| 31 | 参考文献 | [1]~[11] (Vaswani, Shazeer MQA, GQA, DeepSeek-V2, PagedAttention, NVIDIA TE, vLLM×4, KVQuant) |

### 표 (마크다운 표로 변환) — 4건
- 05장: 사전채움 vs 디코딩 비교 (4행)
- 08장: MHA/GQA/MQA 메모리 실측 (KiB/token, GiB)
- 09장: 문맥길이 8K/32K/128K × 아키텍처 메모리
- 13장: MHA/GQA/MQA 헤드 구조 비교

### 수식 — mitex 변환 대상
- 01: p(x_{t+1}|x_{1:t})
- 02: q_i=h_iW^Q …
- 03: K_{1:t-1}=[k_1;…;k_{t-1}] … softmax(q_t K^T V)
- 04: K,V ∈ B×H_KV×T×D_h
- 07: M_KV = 2LTH_KV D_h b (핵심 공식)
- 08: 2·32·8192·8·128·2 = 1GiB 검산
- 09: M_KV ∝ T
- 11: H_KV = H_Q / 12: H_Q>1, H_KV=1 / 13: 1<H_KV<H_Q / 14: M_KV ∝ H_KV
- 30: 2LTH_KV D_h b 재등장

### 도식 (diagram 펜스로 재작성 후보) — 텍스트 레이어 라벨 기준
- 01: 프롬프트→사전채움→디코딩→디코딩 시계열
- 04: 층별 캐시 스택 (第1层 K,V / 第2层 / 第L层)
- 06: 캐시됨 K1:3,V1:3 + 신규 k4,v4 → K1:4,V1:4
- 11: MHA 헤드 Q1..Q6/K1..K6/V1..V6 3행
- 14: MHA/GQA/MQA Q→KV 공유 구조 3열
- 19: 논리 시퀀스 B0-B3 → 물리 블록 매핑 + 블록 테이블
- 비전 서브에이전트 인벤토리 도착 시 `recon-vision.md`로 보강 (레이아웃·색·누락 요소 확인)

## 채택 결정사항 (리컨 단계)

- 스타일: `practical` (신국판 153×225) — IT 실용서·핸드북. 원본 514.8×720pt 비율(~1:1.40)도 신국판(~1:1.47)에 근접
- 제목(안): 「KV 캐시의 이해」 / 부제 "자기회귀 디코딩에서 최신 대언어모델 추론까지 — Understanding AI 핸드북 02 한국어판"
- 저자: "원문 techNmak · 한국어판 KLIC"
- 부 구성(안) 6부: ①원리(1–6) ②비용(7–10) ③아키텍처(11–16) ④블록 관리(17–20) ⑤재사용·계층·정밀도(21–27) ⑥종합(28–30). 부 인트로는 짧은 편역자 프레이밍(2~3문단). 실례: system-design-interview-notes-ko 00-part-introduction.md
- 도식: 중문 라벨 → 한국어 재작성 필요하므로 원본 크롭 불채택, `diagram` 펜스로 재작성 (스킬 규약: 근거 경계 — 본문이 말한 구조만 재배열)
- 표지: `cover: auto` + `cover_composition: true` + `opener_composition: true` (옵션은 plan에서 확정)
- 저작권: LICENSE-NOTE.md + 00-들어가며 머리 원문 표기 블록 (system-design-interview-notes-ko 실례 준용). 원본 무료 배포 핸드북 — 저장소 추적 유지(안)

## 제약

- 엔진·스킬 스크립트·기존 책 무변경 (본 과업은 신규 콘텐츠 생산만)
- korean-style.md 라이터 계약 준수 (G4 0건 목표)
- Never-cut: 수치·참고문헌 식별자·명령어 절약형 생략 금지
- 참고문헌 [1]–[11] 전량 수록, 장마다 `참고자료 [n]` 행 보존
- 원문 주장 경계 보존 ("~는 논문 보고 사례이며 일반 보장 아님" 류의 한정 문장 유지)

## 검증 인프라

- 빌드: `python3 skills/korean-ebook/scripts/build.py books/kv-cache-handbook-ko`
- 게이트: `python3 skills/korean-ebook/scripts/qc_gate.py books/kv-cache-handbook-ko` (G1·G2 FAIL 조건, G3·G4·G5 WARN — 신간은 G4 0건 목표)
- 도식: `python3 skills/korean-ebook/scripts/diagram.py lint|render manuscript/*.md`
- 대조: references/source-zh/*.txt 원문 대조 교정
