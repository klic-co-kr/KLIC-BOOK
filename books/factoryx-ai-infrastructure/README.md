# NHN FactoryX 실전 설계

GPU 데이터센터에서 AI 에이전트 실행 환경까지, NHN FactoryX의 공개 `Infrastructure–Platform–Service` 구조를 따라 AI 인프라를 종단 간으로 설명하는 KLIC 독립 실무서다.

## 다운로드

- [최종 100쪽 PDF 다운로드](build/NHN_FactoryX_실전_설계_nhn-factoryx-ai-infrastructure-ko.pdf?raw=1)

## 출판 목표

- A4 물리 PDF 정확히 100쪽
- 본문 12장과 1단 자동 목차
- 장별 시각 요약 12쪽
- 독립 기술 도형 12개 이상
- 근거형 데이터 차트 8개 이상
- 공개 1차 자료와 공식 자료의 주장·수치 추적
- 전 페이지 렌더링과 구조·글꼴·한글 검수

## 자료 경계

- `manuscript/`, `assets/figures/`, `assets/charts/`: 최종 책의 CONTENT
- `research/`: 출처·주장·입력 경계 원장
- 기존 KLIC 네 책과 `tmp/factoryx-book-workers/`: 조사 질문과 편집 절차의 REFERENCE
- `book-config.yaml`: CONFIG
- `build/`: 생성 산출물이며 본문 입력에서 제외

신청형 《NHN FactoryX 기술 백서》 원문은 제공되지 않았으므로 공개 안내 페이지 밖의 내용을 추정하지 않는다. 제품 내부 구현으로 확인되지 않은 기술은 업계 설계 대안으로만 설명한다.

## 빌드

```bash
/mnt/d/DEV/KLIC-BOOK/.venv/bin/python \
  skills/korean-ebook/scripts/publish_book.py \
  --input books/factoryx-ai-infrastructure/manuscript \
  --output-dir books/factoryx-ai-infrastructure/build \
  --config books/factoryx-ai-infrastructure/book-config.yaml
```

## 검증

```bash
/mnt/d/DEV/KLIC-BOOK/.venv/bin/python \
  books/factoryx-ai-infrastructure/scripts/validate_book.py \
  --root books/factoryx-ai-infrastructure --require-build
```

공개 자료 확인 기준일은 2026년 8월 12일이다.
