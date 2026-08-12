---
name: korean-ebook
description: Use when producing Korean publication-ready books, whitepapers, long reports, evidence-grounded operator manuals, admin guides, onboarding tutorials, SOPs, or hybrid PDF and static-HTML documentation from Markdown, ZIP, documents, official sources, repositories, or verified product screens. Do not use for simple PDF merge, OCR-only extraction, marketing landing pages, pure API references, or fictional click paths.
license: MIT
metadata:
  author: KLIC
  version: "26.08.12"
  language: ko
  compatibility: Python 3.11+. Book mode recommends WeasyPrint 68.x and Poppler. Manual mode requires PyYAML and BeautifulSoup; browser and media tools are optional.
---

# Korean Book and Manual Publishing

한국어 장문 콘텐츠를 **검증 가능한 책 또는 운영 매뉴얼**로 출판한다. 원고와 실제 시스템 근거를 보존하고, 참고자료는 스타일·절차에만 사용한다.

## 0. 산출물 형식 게이트

본문을 쓰거나 화면을 캡처하기 전에 모드를 확정한다.

| 모드 | 기본 산출물 | 선택 기준 |
| --- | --- | --- |
| `book` | A4 PDF, HTML, 소스 매니페스트, 검증 보고서 | 실용서, 백서, 전자책, 장문 보고서 |
| `manual` | 정적 HTML, overview, lesson, 근거 맵, QA, STATUS, HANDOFF | 운영·관리자 매뉴얼, 온보딩, SOP, UI 튜토리얼 |
| `hybrid` | 동일 근거에서 book과 manual을 각각 생성 | 인쇄용 책과 웹 운영 가이드가 모두 필요함 |

요청이 단순히 “매뉴얼”이고 형식을 좁히지 않았다면 `manual`을 기본값으로 한다. 인쇄·배포 PDF를 명시하면 `book`, 둘 다 명시하면 `hybrid`를 사용한다. 두 파이프라인은 입력 근거만 공유하며 렌더러와 검증기를 섞지 않는다.

## 1. 공통 입력 경계

모든 입력을 다음 역할로 분류한다.

- `CONTENT`: 최종 산출물에 포함할 승인된 원고·설명·이미지
- `EVIDENCE`: 공식 문서, 저장소, UI, 런타임, 운영자 확인처럼 주장을 증명하는 근거
- `REFERENCE`: 디자인·타이포·작업 절차 예시. 문장·주장·목차는 가져오지 않는다.
- `CONFIG`: 제목, 판본, 파일 순서, 스타일, 산출물 설정
- `EXCLUDE`: 이전 결과물, 임시 파일, 중복 사본, 개인 메모

혼합 입력은 즉시 빌드하지 않는다. 파일명·크기·SHA-256·역할·포함 여부를 먼저 기록한다. 상세 기준은 `references/input-contract.md`와 `references/content-boundary.md`를 읽는다.

### 공통 금지

- 참고자료 내용을 원고나 매뉴얼 설명에 합치기
- 확인하지 않은 화면·상태·버튼·수치·부작용을 사실처럼 쓰기
- 누락을 숨기려고 문장·증거를 발명하기
- 실제 결제·청구·재고·삭제·권한 변경을 승인 없이 실행하기
- 자동 검사만 통과하고 시각·사용성 검수까지 통과했다고 보고하기

## 2. Book 모드

Book 모드는 기존 결정론적 출판 파이프라인을 사용한다.

1. 원고 순서, 제목 계층, 표·목록·각주·이미지를 프리플라이트한다.
2. `assets/book-config.example.yaml`을 프로젝트 설정으로 복사해 표지, 1단 목차, 장 표제지, 시각 요약, 스타일을 정한다.
3. 시각화 문구는 해당 장 원문에서 추출하거나 충실하게 축약한다. 근거가 없으면 생략한다.
4. `publish_book.py`로 PDF와 HTML을 만든다.
5. `verify_pdf.py`로 구조·글꼴·원문 표본·참고자료 오염을 검사한다.
6. 모든 페이지를 이미지로 렌더하고 접촉표와 고위험 페이지를 확인한다.

의존성 확인:

```bash
python scripts/publish_book.py --check-deps
```

```bash
python scripts/publish_book.py \
  --input <CONTENT> \
  --output-dir <OUT> \
  --config <BOOK_CONFIG>

python scripts/verify_pdf.py \
  --pdf <OUT/BOOK.pdf> \
  --source-manifest <OUT/source_manifest.json> \
  --report-dir <OUT/verification>

python scripts/render_pdf.py --pdf <OUT/BOOK.pdf> --out-dir <OUT/rendered> --dpi 160
python scripts/make_contact_sheet.py --input-dir <OUT/rendered> --output <OUT/contact-sheet.jpg>
```

참고자료는 빌더와 검증기의 `--reference`에 전달하되 본문 입력에서는 제외한다. 장별 도형·표, 표지 이미지, 장 분류, 설정 계약은 `references/editorial-system.md`, `references/visual-editorial-layer.md`, `references/ai-tells.md`를 따른다.

원고 기반 용어집·장별 요약 스캐폴드가 필요하면 PDF와 별도의 선택 산출물로 생성한다. 스크립트는 LLM을 호출하지 않으며, 생성 후 원문 근거를 붙여 채운다.

```bash
python scripts/generate_summary.py <MANUSCRIPT_DIR> <OUT>
python scripts/generate_summary.py <MANUSCRIPT_DIR> <OUT> --no-auto-terms
python scripts/generate_summary.py <MANUSCRIPT_DIR> <OUT> --note <GUIDANCE>
```

`summary.auto_terms: false`는 `--no-auto-terms`, `summary.default_note`는 `--note`에 대응한다.

## 3. Manual 모드

Manual 모드는 화면 설명문이 아니라 **실제 업무를 수행하고 완료를 판정하는 운영 산출물**을 만든다. 시작 전에 `references/manual-production.md`를 완전히 읽는다.

### 3.1 실제 업무 인벤토리

다음을 먼저 확인한다.

- 누가 이 작업을 수행하는가
- 어떤 입력·상태가 작업을 시작시키는가
- 어떤 메뉴·문서·데이터가 흐름에 참여하는가
- 어떤 상태 변화와 읽기 결과가 성공을 증명하는가
- 어떤 분기·예외·승인·되돌리기·전문가 검토가 필요한가
- 근거가 `source`, `ui`, `runtime`, `operator-confirmed`, `inference` 중 무엇인가

화면 목록이 아니라 `trigger → 준비 → 실행 → 검토/승인 → 결과/감사` 업무 흐름으로 구성한다. 실제 UI를 확인하지 못한 click path는 `provisional`이다.

### 3.2 초보자 개요

상세 절차보다 `overview.html`을 먼저 설계한다. 다음을 포함한다.

- 시스템이 무엇이고 누가 사용하는가
- 주요 구성요소와 역할
- 데이터·요청·문서가 이동하는 생명주기
- 처음 접하는 사람이 자주 하는 오해와 교정
- 매뉴얼을 읽는 순서와 한 줄 정신 모형

### 3.3 독립 lesson 계약

각 lesson은 index 카드의 반복이 아니라 단독으로 실행 가능한 교육 단위여야 한다.

- 목적, 대상, 사용 시점, 선행 조건
- 단계별 `operation`, `action`, 독자가 봐야 할 `evidence`, `success` 판정
- 위험도, 승인 필요 여부, 안전 fixture
- 주의, 흔한 실수, 완료 확인
- 근거 ID, 다음 분기
- 화면·영상이 있으면 설명 가능한 alt와 근거 ID

### 3.4 매니페스트와 빌드

`assets/manual-config.example.yaml`을 복사해 `manual.yaml`을 만든다. 실제 예시는 `examples/minimal-manual/`을 사용한다.

```bash
python scripts/build_manual.py \
  --manifest <PROJECT/manual.yaml> \
  --output-dir <OUT>

python scripts/verify_manual.py \
  --manifest <PROJECT/manual.yaml> \
  --package-dir <OUT>
```

`--output-dir`은 존재하지 않거나 비어 있어야 한다. 빌더는 기존 폴더를 자동 삭제·덮어쓰지 않는다.

브라우저에서 전 페이지·탐색·반응형·키보드·화면 증거를 직접 검수했다면 `assets/visual-review.example.json` 형식으로 패키지 안에 증거를 저장한 뒤 `--visual-evidence`로 전달한다.

```bash
python scripts/verify_manual.py \
  --manifest <PROJECT/manual.yaml> \
  --package-dir <OUT> \
  --visual-evidence <OUT/qa/visual-review.json>
```

## 4. 위험 작업 게이트

읽기 전용 조사와 화면 확인을 기본값으로 한다.

`high` 또는 `critical` lesson은 다음을 모두 만족하기 전에는 빌드 계약을 통과하지 못한다.

- `approval_required: true`
- `fixture`: `demo`, `staging`, `local`, `sandbox`, `dedicated-test-data` 중 하나
- 상태 변경 단계의 `operation: write`와 변경 후 확인할 `readback`
- 실제 실행 시 사용자 승인 범위 안에서 고유 테스트 식별자를 사용
- 실행 후 ID, 상태, 감사 기록, 재고·원장·권한 같은 부작용을 다시 읽어 확인

규제·회계·세무·법률·의료·보안 판단은 UI 사용법과 전문적 판단을 구분하고 전문가 검토 범위를 표시한다.

## 5. 매체 단계 상승

화면·영상은 장식이 아니라 단계의 증거다. 핵심 경로는 다음 순서로 상승시킨다.

1. 공식 문서·저장소 근거
2. 실제 화면 캡처 또는 신뢰 가능한 다이어그램
3. 단계별 강조·설명 카드
4. 사용자가 요청하고 도구가 준비된 경우에만 안내 영상

화면 캡처가 불가능하면 placeholder를 배포하지 않는다. 근거 기반 다이어그램을 사용하거나 lesson을 `provisional`로 제한한다. 영상·브라우저 검수 기준은 필요할 때만 `references/manual-media.md`를 읽는다.

## 6. 검증과 완료 조건

Book은 `references/quality-gates.md`, Manual은 `references/manual-quality-gates.md`를 따른다.

Manual 검증은 세 축을 분리한다.

- `technical`: 파일, HTML 구조, 내부 링크, 매체, alt, 매니페스트 동기화
- `content`: 업무 흐름, lesson 깊이, 단계 근거, 위험 게이트, placeholder·원시 마크업 누출
- `visual`: 브라우저에서 실제로 본 레이아웃, 탐색, 반응형, 키보드, 매체 가독성

`final`은 고위험 오류가 0이고 실제 동작 근거가 inference뿐이 아니며 시각·사용성 검수 범위가 기록됐을 때만 사용한다. 자동 검증 PASS와 시각 PASS를 합치지 않는다.

## 7. 완료 보고

다음을 짧고 구체적으로 보고한다.

```text
Goal — 책/매뉴얼 제작
모드: book / manual / hybrid
상태: 완료 / 조건부 완료 / 실패

입력 경계
- CONTENT / EVIDENCE / REFERENCE / EXCLUDE

산출물
- 최종 PDF 또는 index.html
- 매니페스트·근거 맵
- 검증 보고서·STATUS·HANDOFF

검증
- 기술 / 내용·근거 / 시각·사용성
- 고위험 오류와 미확인 범위
- SHA-256
```

## 8. 사용하지 않는 경우

- PDF 단순 병합·분할 또는 OCR만 필요한 작업
- 상품 판매용 랜딩페이지·마케팅 카피
- 사용자 업무 흐름이 없는 순수 API 레퍼런스
- 실제 근거 없이 만드는 가상 UI·클릭 경로
- 계약서 입력·서명·레드액션, 슬라이드 발표자료
