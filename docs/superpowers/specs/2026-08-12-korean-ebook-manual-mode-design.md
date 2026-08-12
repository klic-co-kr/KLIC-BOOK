# Korean Ebook Manual Mode Design

## 목적

`korean-ebook`을 한국어 장문 출판 스킬에서 **근거 기반 책·운영 매뉴얼 출판 스킬**로 확장한다. `backup/manual-production`을 복사하거나 별도 스킬로 설치하지 않는다. 검증된 원칙만 추출해 KLIC의 입력 경계, 결정론적 빌드, 자체 검증 체계에 맞게 다시 구현한다.

## 산출물 라우팅

작업 시작 시 산출물을 먼저 고른다.

| 모드 | 기본 산출물 | 적용 대상 |
| --- | --- | --- |
| `book` | A4 PDF, HTML, 소스 매니페스트, 검증 보고서 | 실용서, 백서, 전자책, 장문 보고서 |
| `manual` | 정적 HTML 패키지, lesson, 증거 맵, 상태·인계, QA 보고서 | 운영 매뉴얼, 관리자 가이드, 온보딩, SOP, UI 튜토리얼 |
| `hybrid` | 같은 근거 원장에서 `book`과 `manual`을 각각 생성 | 인쇄용 책과 웹 운영 가이드가 모두 필요한 경우 |

모드를 섞어 하나의 렌더러로 만들지 않는다. 공통 입력 경계와 근거 원장만 공유하고 빌더와 검증기는 분리한다.

## 선별 흡수

### 유지할 원칙

- 실제 시스템·공식 문서·저장소를 먼저 조사하고 화면 이름만 나열하지 않는다.
- 사용자 역할, 시작 조건, 입력, 상태 변화, 성공 증거, 위험·승인 경계를 업무 흐름으로 구조화한다.
- 비전문가용 시스템 개요와 용어·정신 모형을 상세 절차보다 먼저 제공한다.
- 독립 lesson은 목적, 대상, 사용 시점, 선행 조건, 단계, 화면·문서 증거, 주의, 흔한 실수, 완료 판정, 출처, 다음 분기를 포함한다.
- 상태 변경 작업은 기본적으로 읽기 전용이다. 사용자 승인과 안전한 fixture가 있을 때만 실행하고 식별자·상태·부작용을 재확인한다.
- 기술 검증, 내용·근거 검증, 시각·사용성 검증을 별도 판정으로 기록한다.
- 화면 캡처나 영상이 없으면 그 한계를 숨기지 않고 `provisional`로 표시한다.

### KLIC 방식으로 다시 만들 것

- `manual.yaml`: 제품 개요, 역할, 업무 흐름, lesson, 근거, 위험, 매체를 담는 단일 입력 계약
- `build_manual.py`: 외부 SaaS 없이 정적 HTML 패키지를 결정론적으로 생성
- `verify_manual.py`: 스키마, 링크, 매체, lesson 깊이, 증거, 금지 placeholder, 최종 상태를 검증
- `manual-template.html`과 `manual.css`: 접근 가능한 반응형 HTML/CSS 기반 디자인
- `manual-production.md`, `manual-quality-gates.md`, `manual-media.md`: 필요한 때만 읽는 레퍼런스

### 버릴 것

- Hermes, peer, oracle, broker, workflow-ops 전용 명령
- 설치돼 있지 않은 `manual-verification`, `html-for-beginners`, `dogfood` 강제 의존
- Cloudflare Pages 배포를 기본 완료 조건으로 두는 규칙
- ERPNext, Print Station, DW, Onyx 등 특정 프로젝트의 사건 기록과 반복 규칙
- Driver.js, HyperFrames, OBS, ffmpeg를 모든 매뉴얼에 강제하는 규칙
- 백업의 `__pycache__`, 중복 템플릿, 중복 레퍼런스

## Manual 패키지 계약

```text
out/
├── index.html
├── overview.html
├── lessons/<lesson-id>.html
├── assets/manual.css
├── media/                         # manifest가 참조한 로컬 매체만 복사
├── sources/evidence-map.md
├── qa/build-report.json
├── qa/verification.json
├── qa/verification.md
├── manual-manifest.json
├── STATUS.md
└── HANDOFF.md
```

`index.html`은 전체 업무 흐름과 lesson 순서를 보여준다. `overview.html`은 시스템의 목적, 사용자 역할, 주요 구성요소, 데이터·작업의 생명주기, 초보자 혼동을 설명한다. 각 lesson은 index 카드의 반복이 아니라 독립 실행 가능한 교육 단위여야 한다.

## 증거와 상태

각 주장·단계는 `source`, `ui`, `runtime`, `operator-confirmed`, `inference` 중 하나의 증거 등급을 가진다. `final` 패키지는 핵심 실행 단계에 `inference`만 사용할 수 없다. 화면·런타임을 검증하지 못한 click path는 `provisional`로 남긴다.

상태 변경 단계에는 `risk`, `approval_required`, `fixture`를 명시한다. 승인되지 않은 실제 결제·청구·재고·삭제·권한 변경을 문서 제작 과정에서 실행하지 않는다.

## 검증

- 기존 PDF 출판 회귀 테스트가 그대로 통과해야 한다.
- 매뉴얼 샘플은 빌더 재실행 시 같은 텍스트 산출물과 구조를 만들어야 한다.
- 모든 내부 링크와 로컬 매체가 존재해야 한다.
- lesson 필수 필드와 단계별 `action/evidence/success`를 검사한다.
- `TODO`, `TBD`, `UI_CAPTURE_REQUIRED`, 원시 Markdown 링크·HTML 누출을 최종 패키지에서 금지한다.
- `final`은 high issue 0일 때만 허용한다.
- 브라우저·시각 검수를 실행하지 않았다면 자동 검증 PASS와 시각 PASS를 동일시하지 않는다.

## 호환성

- 기존 `publish_book.py`, `verify_pdf.py`, PDF 설정 파일과 출력 계약을 유지한다.
- 새 매뉴얼 도구는 Python 3.11+, PyYAML, BeautifulSoup만 사용한다.
- `backup/manual-production`은 비교 자료로만 남기고 원격 스킬 패키지에는 넣지 않는다.
