# korean-ebook

Markdown·ZIP 원고를 **한국어 출판형 A4 PDF**로 편집하고, 1단 목차와 원문 기반 도형·흐름도·비교표·장별 시각 요약을 선택적으로 구성하며, 원문 무결성·참고자료 오염·글꼴·북마크·링크·전 페이지 렌더링을 검수하는 Agent Skill입니다.

이 스킬은 FDE 한국어판 편집 작업에서 성공한 방식을 재사용 가능하게 고정합니다. 참고자료의 **내용**을 합치는 스킬이 아니라, 원고와 참고자료의 경계를 지킨 상태에서 편집·렌더링·검수 절차를 반복 실행하는 스킬입니다.

- 표지, 속표지, 편집본 안내, **1단 자동 목차**, 장 표제지, 본문, 부록 구성
- 장별 개념도·프로세스·비교표·판단표를 넣는 선택형 시각 편집 레이어
- 명조 본문 + 고딕 제목의 한국어 타이포그래피
- 짙은 네이비와 청록 포인트의 `fde-midnight` 프리셋
- 참고자료는 스타일·절차에만 사용하고 본문에 섞지 않는 강제 경계
- WeasyPrint 기반 PDF, 북마크, 내부 링크, 글꼴 임베딩
- 원문 문단 표본 대조, 참고자료 고유 문구 오염 검사
- 전 페이지 PNG 렌더와 접촉표 생성

## 폴더 구조

```text
korean-ebook/
├── SKILL.md
├── agents/openai.yaml
├── assets/book-config.example.yaml          # 범용 설정·시각 레이어는 기본 비활성
├── assets/book-config.fde-example.yaml      # FDE 120쪽 시각 편집 프로필
├── assets/book-config.fde-text-only.yaml    # FDE 108쪽 본문 중심 프로필
├── references/
├── scripts/
├── evals/
└── examples/
```

## Codex 설치

프로젝트 전용:

```text
<repo>/.agents/skills/korean-ebook/
```

사용자 전체 적용:

```text
~/.agents/skills/korean-ebook/
```

Codex CLI·IDE에서는 `$korean-ebook`, ChatGPT 데스크톱에서는 `@korean-ebook`로 명시 호출할 수 있습니다. “원고를 출판형 PDF로 편집해”처럼 설명하면 설정에 따라 자동 선택될 수도 있습니다.

## ChatGPT·OpenAI API용 ZIP

배포 ZIP은 반드시 **단일 최상위 폴더**를 포함해야 합니다.

```text
korean-ebook.zip
└── korean-ebook/
    └── SKILL.md
```

OpenAI API 업로드 예:

```bash
curl -X POST "https://api.openai.com/v1/skills" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F "files=@./korean-ebook.zip;type=application/zip"
```

## 설치

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

## 한 번에 실행

```bash
python scripts/run_pipeline.py \
  --input /path/to/manuscript.zip \
  --output-dir /path/to/out \
  --config assets/book-config.example.yaml \
  --reference /path/to/layout-example.pdf
```

FDE 시각 편집본 재현:

```bash
python scripts/run_pipeline.py \
  --input /path/to/FDE-manuscript.zip \
  --output-dir /path/to/out \
  --config assets/book-config.fde-example.yaml
```

`--reference`는 여러 번 사용할 수 있습니다. 참고 파일은 매니페스트와 오염 검사에만 쓰이며 본문 입력으로 파싱되지 않습니다.

## 단계별 실행

```bash
python scripts/publish_book.py --input manuscript.zip --output-dir out --config book.yaml
python scripts/verify_pdf.py --pdf out/book.pdf --source-manifest out/source_manifest.json --report-dir out/verification
python scripts/render_pdf.py --pdf out/book.pdf --out-dir out/rendered --dpi 160
python scripts/make_contact_sheet.py --input-dir out/rendered --output out/contact-sheet.jpg
```

## 설정

범용 원고는 `assets/book-config.example.yaml`을 프로젝트 폴더로 복사한 뒤 수정합니다. `book.title: auto`는 README 또는 첫 번째 원고의 H1을 책 제목으로 사용합니다.

이번 FDE 한국어판을 1단 목차와 도형·표가 포함된 실무서형으로 재현하려면 `assets/book-config.fde-example.yaml`을 사용합니다. 시각 요약을 빼고 본문 중심으로 제작하려면 `assets/book-config.fde-text-only.yaml`을 사용합니다.

제공 원고 13개와 동일한 렌더링 환경에서 확인한 회귀 기준은 다음과 같습니다.

### 시각 편집 프로필

- A4 120쪽
- 목차 6~8쪽, **1단 구성**
- 장·후기·부록 시각 요약 12쪽
- PDF 북마크 140개, 상위 북마크 16개
- 1장 9쪽, 8장 82쪽, 후기 97쪽
- 부록 A 101쪽, 부록 B 106쪽, 부록 C 111쪽
- 원문 문단 표본·제목 누락 0건
- 자동 검수 high 0 / medium 0

### 본문 중심 프로필

- A4 108쪽
- 목차는 동일하게 1단
- 시각 요약 페이지 없음
- 자동 검수 high 0 / medium 0

이 값은 동일 원고의 회귀 검증값입니다. 다른 원고에서는 분량과 구조에 따라 페이지 수가 달라집니다. PDF 파일 자체가 회귀본과 바이트 단위로 동일하다는 뜻은 아닙니다.

중요 항목:

- `book`: 제목, 부제, 저자, 판본, 출력 파일명
- `files`: README, 파일 순서, 제외 패턴, 저장소용 목차·안내 문구의 명시적 편집 변환
- `editorial`: 표지·1단 목차·장 표제지, 표지 워터마크, 속표지 인용문, 편집본 안내
- `visuals`: 장별 시각 요약 사용 여부, 레이아웃, 도형 문구, 비교표와 판단표
- `style`: 글꼴, 색상, 여백, 본문 크기, 필요한 경우 장별 밀도 보정 CSS
- `quality`: 문단 표본과 오염 검사 기준

## 시각 편집 레이어

`visuals.enabled: true`로 켜고, `visuals.chapters`에 장 제목 또는 장 순번별 사양을 적습니다. 지원 레이아웃은 `process`, `bridge`, `quadrant`, `ladder`, `principles`, `dashboard`, `network`, `matrix`입니다.

시각화는 원고 외 지식을 보강하는 기능이 아닙니다. 도형과 표의 모든 문구는 해당 장의 원문에서 추적 가능해야 하며, 근거가 없으면 만들지 않습니다. 각 시각 페이지에는 “원문을 대체하지 않는 편집 요약” 고지가 자동으로 들어갑니다. 상세 사양은 `references/visual-editorial-layer.md`를 확인합니다.

## 결과물

```text
out/
├── <제목>_<판본>.pdf
├── book.html
├── source_manifest.json
├── build_report.json
├── verification/
├── rendered/
├── contact-sheet-01.jpg
├── completion_report.md
└── <제목>_<판본>_패키지.zip
```

## 경계 원칙

“예시”, “참고”, “이런 느낌”으로 제공된 파일은 CONTENT가 아닙니다. 참고자료의 원칙·평가표·목차·문장을 최종 원고에 합치는 행위는 이 스킬의 실패로 판정합니다.

## 스킬 자체 검증

```bash
python scripts/validate_skill.py
```

`SKILL.md` 메타데이터, 폴더명, 파일 수, 크기 제한, 필수 파일, 글꼴 파일 미포함 여부를 검사합니다.
