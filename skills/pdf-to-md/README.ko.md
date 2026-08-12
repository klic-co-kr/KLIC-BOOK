# pdf-to-md

## 정체성

PDF 책(텍스트·스캔 혼합) → 챕터별 정제 Markdown 변환 스킬. `korean-ebook`(MD→PDF)의 역방향 입력층. 외부 PDF 책에 MD 원본이 없을 때, 이 스킬이 챕터 MD를 만들어 `korean-ebook-to-skill` 판단추출 파이프라인의 입력으로.

## 설치

```bash
bash scripts/install.sh   # → $CLAUDE_SKILLS_HOME/pdf-to-md (심볼릭링크)
```

의존성(PEP 668 환경은 venv 권장):
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r scripts/requirements.txt   # pymupdf paddleocr paddlepaddle pyyaml
```

## 사용 (5단계)

```bash
PDF=book.pdf; WORK=.cache/work; OUT=book-md

# 1. 페이지 분류
python3 scripts/classify_pages.py $PDF $WORK
# 2. 텍스트/OCR 추출 (paddleocr 미설치 시 --ocr skip)
python3 scripts/extract_text.py $PDF --work $WORK --ocr paddle
# 3. 이미지·표 추출
python3 scripts/extract_assets.py $PDF --out $OUT
# 4. 챕터 분할 (사람 게이트 보고서 생성)
python3 scripts/split_chapters.py --work $WORK
#    → $WORK/chapter-gate.md 검토 → $WORK/chapters.json 의 approval + approved:true 채우기
# 5. MD 렌더
python3 scripts/render_md.py --work $WORK --out $OUT --book-slug <slug> --title "제목"
```

## 모드

- **Full**(기본): OCR 포함. 스캔 페이지 PaddleOCR PP-Structure.
- **Text-only**(`--ocr skip`): paddle 미설치 시. scan 페이지는 이미지로 남기고 경고.
- **Chapter-only**: 페이지 MD 있으면 Step 4-5만(재분할).

## 게이트 (절대)

Step 4 챕터 분할은 사람 확인 필수. `chapter-gate.md` 보고 후 `chapters.json`의 `approval` + 각 챕터 `approved:true` 확정. 자동화 금지 — 오감지가 산출물 전체 망침.

## 산출 구조

```
<book-slug>/
├── meta.yaml          # title, author, n_pages, chapters[]
├── README.md          # 색인
├── 00-frontmatter.md  # 표지·목차(감지 시)
├── 01-chapter-*.md
└── assets/
    ├── images/        # fig-NNN-MM.png
    └── tables/
```

## 테스트

```bash
cd skills/pdf-to-md && python3 -m pytest tests/ -v
```
14 tests (classify 2 + extract 3 + assets 2 + split 4 + render 2 + e2e 1).

## 한계

- OCR 품질: 스캔 상태 가변 → 게이트 보정
- 표·차트: PP-Structure 정확도 가변; 복잡표는 이미지 fallback
- 수식: 이미지로 남김(LaTeX 재생성 아님)
- paddleocr 무거움(~수백MB + 모델) → Text-only 모드 우회
- 저작권: 사용자 소유 책에만 적용

## 연계

- 역방향 짝: `korean-ebook`(MD→PDF)
- 다음 단계: 산출 MD → `korean-ebook-to-skill`(판단추출 스킬 생성)
- 설계: `docs/superpowers/specs/2026-08-12-pdf-to-md-design.md`
