# korean-ebook

Markdown·ZIP·문서·검증된 제품 근거를 한국어 **출판형 책 또는 운영 매뉴얼**로 만드는 KLIC Agent Skill입니다. 기존 A4 PDF 출판 파이프라인과 새 정적 HTML 매뉴얼 파이프라인을 분리해 운영하며, 둘이 필요할 때만 같은 근거 원장을 공유하는 `hybrid` 모드를 사용합니다.

## 산출물 모드

| 모드 | 결과 | 대상 |
| --- | --- | --- |
| `book` | A4 PDF, HTML, 북마크, 검증·렌더 보고서 | 실용서, 백서, 전자책, 장문 보고서 |
| `manual` | 정적 HTML 사이트, overview, lesson, 근거 맵, QA·인계 문서 | 운영·관리자 가이드, 온보딩, SOP, UI 튜토리얼 |
| `hybrid` | 같은 근거에서 book과 manual을 각각 빌드 | 인쇄본과 웹 운영 가이드가 모두 필요한 경우 |

핵심 원칙은 다음과 같습니다.

- `CONTENT`, `EVIDENCE`, `REFERENCE`, `CONFIG`, `EXCLUDE`를 빌드 전에 분리
- 참고자료의 문장·주장·목차는 본문에 합치지 않음
- 책의 도형·표는 원문에서, 매뉴얼의 절차·화면은 검증 근거에서 추적
- 고위험 상태 변경은 승인과 안전 fixture 없이는 계약 단계에서 거부
- 기술·내용·시각 검증을 분리하고 자동 검사만으로 시각 PASS를 주장하지 않음

## 구조

```text
korean-ebook/
├── SKILL.md
├── agents/openai.yaml
├── assets/
│   ├── book-config.example.yaml
│   ├── manual-config.example.yaml
│   ├── manual-template.html
│   └── visual-review.example.json
├── examples/minimal-manual/
├── references/
├── scripts/
└── tests/
```

## 설치

프로젝트 전용 위치는 `<repo>/.agents/skills/korean-ebook/`, 사용자 전역 위치는 `~/.agents/skills/korean-ebook/`입니다. Codex CLI·IDE에서는 `$korean-ebook`, ChatGPT 데스크톱에서는 `@korean-ebook`로 명시 호출할 수 있습니다.

Linux/macOS:

```bash
bash scripts/install.sh
source .venv/bin/activate
```

Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1
.\.venv\Scripts\Activate.ps1
```

## Book 모드

한 번에 실행:

```bash
python scripts/run_pipeline.py \
  --input /path/to/manuscript.zip \
  --output-dir /path/to/out \
  --config assets/book-config.example.yaml \
  --reference /path/to/layout-example.pdf
```

단계별 실행:

```bash
python scripts/publish_book.py --input manuscript.zip --output-dir out --config book.yaml
python scripts/verify_pdf.py --pdf out/book.pdf --source-manifest out/source_manifest.json --report-dir out/verification
python scripts/render_pdf.py --pdf out/book.pdf --out-dir out/rendered --dpi 160
python scripts/make_contact_sheet.py --input-dir out/rendered --output out/contact-sheet.jpg
```

`--reference`는 디자인·절차 참고와 오염 검사에만 사용하며 본문 입력으로 파싱하지 않습니다. `visuals.enabled: true`이면 원문에 근거가 있는 `process`, `bridge`, `quadrant`, `ladder`, `principles`, `dashboard`, `network`, `matrix` 레이아웃을 사용할 수 있습니다. 설정과 편집 기준은 `references/visual-editorial-layer.md`를 따릅니다.

원고 기반 용어집·장별 요약 스캐폴드는 별도 선택 산출물로 생성합니다.

```bash
python scripts/generate_summary.py /path/to/manuscript out
python scripts/generate_summary.py /path/to/manuscript out --no-auto-terms
python scripts/generate_summary.py /path/to/manuscript out --note "원문 근거를 표시하세요."
```

결과 예:

```text
out/
├── <제목>_<판본>.pdf
├── book.html
├── source_manifest.json
├── build_report.json
├── verification/
├── rendered/
├── contact-sheet-01.jpg
└── <제목>_<판본>_패키지.zip
```

## Manual 모드

`assets/manual-config.example.yaml`을 프로젝트로 복사해 실제 근거 경로와 업무 흐름을 채웁니다. 즉시 실행 가능한 최소 예시는 `examples/minimal-manual/`에 있습니다.

```bash
python scripts/build_manual.py \
  --manifest examples/minimal-manual/manual.yaml \
  --output-dir out/manual

python scripts/verify_manual.py \
  --manifest examples/minimal-manual/manual.yaml \
  --package-dir out/manual
```

`--output-dir`은 새 폴더 또는 빈 폴더여야 합니다. 안전을 위해 기존 패키지나 사용자 파일이 든 폴더를 자동 삭제·덮어쓰지 않습니다.

매뉴얼은 화면 목록이 아니라 `trigger → 준비 → 실행 → 검토/승인 → 결과/감사` 업무 흐름으로 설계합니다. 모든 단계에 `operation`, `action`, `evidence`, `success`, 근거 ID가 있어야 합니다. `operation: write`에는 승인·안전 fixture·변경 후 `readback`이 추가로 필요하며, 검증하지 못한 실제 UI·런타임 동작은 `provisional`로 표시합니다.

`final` 상태는 구조화된 브라우저 검수 증거가 필요합니다. `assets/visual-review.example.json`을 패키지의 `qa/visual-review.json`으로 작성한 뒤 전달합니다.

```bash
python scripts/verify_manual.py \
  --manifest manual.yaml \
  --package-dir out/manual \
  --visual-evidence out/manual/qa/visual-review.json
```

결과 예:

```text
out/manual/
├── index.html
├── overview.html
├── lessons/*.html
├── assets/manual.css
├── media/
├── sources/evidence-map.md
├── qa/build-report.json
├── qa/verification.json
├── qa/verification.md
├── manual-manifest.json
├── STATUS.md
└── HANDOFF.md
```

## Hybrid 모드

`hybrid`는 하나의 혼합 렌더러가 아닙니다. 공통 근거 ID를 정한 뒤 Book과 Manual 명령을 각각 실행하고 각 검증기를 따로 통과시킵니다. PDF 페이지 구조와 웹 lesson 구조를 서로 대신 사용하지 않습니다.

## ChatGPT·OpenAI API용 ZIP

배포 ZIP은 단일 최상위 폴더를 포함해야 합니다.

```text
korean-ebook.zip
└── korean-ebook/
    └── SKILL.md
```

```bash
curl -X POST "https://api.openai.com/v1/skills" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F "files=@./korean-ebook.zip;type=application/zip"
```

## 스킬 검증

```bash
python scripts/validate_skill.py
python -m pytest -q tests
```

`validate_skill.py`는 메타데이터, 필수 파일, 파일 수·크기, 금지된 외부 런타임 결합을 검사합니다. 품질 게이트는 책은 `references/quality-gates.md`, 매뉴얼은 `references/manual-quality-gates.md`를 확인합니다.
