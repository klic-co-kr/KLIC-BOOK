---
name: pdf-to-md
description: "PDF 책(텍스트·스캔 혼합)을 챕터별 정제 Markdown으로 변환한다. 텍스트 페이지는 pymupdf, 스캔/이미지 페이지는 PaddleOCR PP-Structure(한국어)로 텍스트·표·레이아웃을 분석. 산출 = <book-slug>/ 디렉토리(meta.yaml + 챕터 MD + assets/). korean-ebook-to-skill 파이프라인의 입력층(역방향). 챕터 분할은 사람 게이트 필수."
---

# pdf-to-md

## 정체성

**PDF 책 → 정제 MD 변환 스킬**. korean-ebook(MD→PDF)의 역방향 입력층. 외부 PDF 책(스캔·구매본·디자인본)에 MD 원본이 없을 때, 이 스킬이 챕터별 MD를 만들어 `korean-ebook-to-skill` 판단추출 파이프라인의 입력으로 쓴다.

- 텍스트 PDF → pymupdf(빠름·정확)
- 스캔/이미지 PDF → PaddleOCR PP-Structure(텍스트·표·레이아웃 구조)
- 챕터 분할 → 사람 게이트(자동 확정 금지 — `korean-ebook-to-skill` 교훈)

## 워크플로우 (5단계)

```bash
PDF → [1]페이지 분류 → [2]텍스트/OCR 추출 → [3]에셋 추출 → [4]챕터 분할(게이트) → [5]MD 렌더
```

### Step 1 — 페이지 분류

```bash
python3 scripts/classify_pages.py <pdf> <work_dir>
```
페이지별 텍스트 레이어 문자수 + 이미지 면적비 산출 → 분류:
- `text`(문자 ≥100/페이지)
- `scan`(텍스트 거의 없음, 이미지 면적 과반)
- `mixed`(중간)

산출: `work/pages.json` = `[{page, kind, n_chars, image_ratio}]`.

### Step 2 — 텍스트/OCR 추출

```bash
python3 scripts/extract_text.py <pdf> --work <work_dir> [--ocr paddle|skip]
```
- `text` 페이지 → pymupdf `get_text("dict")` + 헤딩 감지(폰트크기 상위)
- `scan`/`mixed` 페이지 → PaddleOCR PP-Structure(이미지 300 DPI 렌더 → 영역별 구조 + 텍스트 + 표)
- `--ocr skip`: paddleocr 미설치 시 Text-only 모드(scan 페이지는 이미지로 남기고 경고)

산출: `work/pages/<NN>.md`(페이지별 원시 MD).

### Step 3 — 에셋 추출

```bash
python3 scripts/extract_assets.py <pdf> --work <work_dir> --out <out_dir>
```
- 이미지 → `assets/images/fig-<page>-<idx>.png`(pymupdf 추출)
- 표 → `assets/tables/table-<page>.md`(PP-Structure 표 구조) 또는 `.png`(fallback)

### Step 4 — 챕터 분할 (사람 게이트 필수)

```bash
python3 scripts/split_chapters.py --work <work_dir>
```
- 목차 페이지 감지 + 본문 헤딩 정규식(`references/chapter_patterns.md`)으로 후보 경계
- 산출: `work/chapters.json`(후보) + `work/chapter-gate.md`(보고서)

**게이트**: 사람이 `chapter-gate.md` 검토 → `chapters.json`에 `approved: true` 추가(또는 경계 수정). `approval` 없으면 Step 5가 non-zero 종료. **자동화 금지** — 챕터 분할 오감지가 산출물 전체를 망친다.

### Step 5 — MD 렌더

```bash
python3 scripts/render_md.py --work <work_dir> --out <out_dir> --book-slug <slug>
```
- `chapters.json`(승인) → 챕터별 `0N-chapter-<slug>.md`(헤딩 + 본문 + 이미지 링크 `![](assets/images/...)`)
- `meta.yaml`(title·author·n_pages·chapters·source_pdf·converted_date)
- `README.md`(색인)

## 산출 구조

```
<book-slug>/
├── meta.yaml
├── README.md
├── 00-frontmatter.md     # 표지·목차(감지 시)
├── 01-chapter-<slug>.md
├── 02-chapter-<slug>.md
└── assets/
    ├── images/           # fig-NN-MM.png
    └── tables/           # table-NN.md|.png
```

## 모드

- **Full**(기본): Step 1-5, OCR 포함
- **Text-only**(`--ocr skip`): scan/mixed 페이지는 이미지로 남기고 경고(paddleocr 미설치 시)
- **Chapter-only**: 페이지 MD가 이미 있으면 Step 4-5만(재분할)
- **Recompose**(선택 후속): Step 5 산출이 슬라이드·강의 자료 원고(## 단문 다수)면 → Step 6 재구성

## Step 6 — 책 재구성 (슬라이드/강의 자료 원고 → 책 서술)

PDF가 슬라이드·강의 자료인 경우 Step 5 산출이 슬라이드 단문(## 헤딩 수백 개) 나열이 된다. 그대로 빌드하면 페이지 폭발(슬라이드 1장≈1페이지) + 가독성 저하. **책 장으로 재구성**한다.

이 단계는 **에이전트가 수행**(LLM 판단), 결정론 스크립트 아님.

재구성 원칙:
1. 관련 슬라이드들을 **4-7개 큰 절(## )로 통합** — 슬라이드 1개 = ## 1개 금지
2. 불릿·단문 → **연결된 서술 단락** (책처럼 읽히게)
3. 중복·반복·페이지번호·구분자·라이선스 푸터(Step 2에서 자동 제거되나 잔여분) 전부 제거
4. 분량 **40-50% 압축** 목표 — 단, 원문 의미·수식·코드·전문용어·그림 참조·인용번호·References는 **보존**
5. 도입 → 본문 → 정리 흐름. 헤딩 한국어(또는 원문 언어)
6. 의미 변경·추가 **금지** (CC 라이선스 ND 준수 시 특히)

절차: 각 챕터(또는 일차) MD를 에이전트가 읽고 위 원칙으로 재작성 → 같은 파일 덮어쓰기 → 게이트(사람 샘플 검토).

> **실제 사례**: 마츠오 LLM 강의(8일 슬라이드)에서 Step 1-5 산출이 1043페이지 폭발. Step 6 재구성으로 40-55% 압축·4-7절/일자 통합 → 책 품질. 각 일자별 에이전트 병렬 처리.

## 의존성

```bash
pip install -r scripts/requirements.txt   # pymupdf paddleocr paddlepaddle pyyaml
```
> **paddleocr 3.x 주의**: 3.x는 CPU 환경에서 PIR/onednn 추론 버그(NotImplementedError). **2.x 안정선 사용**(`paddleocr>=2.7,<3`). requirements.txt에 상한 고정.
**PEP 668 환경**(externally-managed): venv 권장
```bash
python3 -m venv .venv && source .venv/bin/activate && pip install -r scripts/requirements.txt
```
paddleocr 첫 실행 시 한국어 모델 다운로드(~수백MB).

## 한국어 처리

- 챕터 표지: `제N장`/`N장`/`Chapter N`/`N. 제목` 정규식(`references/chapter_patterns.md`)
- 산출 한국어(원문 언어 보존)
- OCR 한국어 모델(`korean`)

## 게이트 규칙 (절대)

- **Step 4 챕터 분할**: 사람 확인 없이 `chapters.json` 확정 금지. `chapter-gate.md` 보고 후 사람 승인.
- **메타(제목·저자)**: 에이전트 판단 후 사람 게이트.
- 게이트 자동화 = 산출물 전체 오염. `korean-ebook-to-skill`가 사람 게이트에서 실패를 잡은 선례 준용.

## 한계

- **OCR 품질**: 스캔 품질 가변. 오인식 → 게이트 보정.
- **표 구조**: PP-Structure 정확도 가변. 복잡표는 이미지+텍스트 fallback.
- **차트**: 구조 재생성 불가(이미지 + 내부 텍스트 OCR). 의미 해석은 사람.
- **수식·화학식**: 이미지로 남김(LaTeX 재생성 아님).
- **paddleocr 무거움**: Text-only 모드로 우회 가능.
- **저작권**: 사용자 소유 책에만 적용. 스킬은 도구, 책임은 사용자.

## 연계

- 역방향 짝: `korean-ebook`(MD→PDF 빌드)
- 다음 단계: 산출 MD → `korean-ebook-to-skill`(판단추출 스킬 생성)
