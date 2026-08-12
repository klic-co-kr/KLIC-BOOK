# 입력 계약

## 1. 역할 분리

모든 입력은 다음 역할 가운데 하나여야 한다.

| 역할 | 의미 | 최종 산출물 사용 |
| --- | --- | --- |
| CONTENT | 책·매뉴얼에 실제로 수록할 승인 원고, 설명, 표, 이미지 | 예 |
| EVIDENCE | 공식 문서, 저장소, UI, 런타임, 운영자 확인처럼 주장을 증명하는 근거 | 인용·추적에 사용 |
| REFERENCE | 시각 구성, 편집 방식, 품질 수준, 작업 절차의 예시 | 내용에는 사용하지 않음 |
| CONFIG | 제목, 판본, 순서, 스타일, 산출물 설정 | 메타데이터·렌더링에 사용 |
| EXCLUDE | 이전 결과물, 임시 파일, 중복 사본, 개인 메모 | 아니오 |

`REFERENCE`를 `CONTENT` 또는 `EVIDENCE`로 바꾸려면 사용자의 명시적 지시가 필요하다. “예시”, “이런 느낌”, “참고해서”는 내용 통합 허가가 아니다.

## 2. 산출물별 구조

### Book 모드

```text
project/
├── content/
│   ├── README.md
│   ├── 01-chapter.md
│   └── 02-chapter.md
├── references/
│   └── layout-example.pdf
├── book.yaml
└── output/
```

### Manual 모드

```text
project/
├── manual.yaml
├── sources/                       # 공식 문서·코드·설정 사본
├── evidence/                      # 검증된 화면·다이어그램·매체
└── output/
```

`manual.yaml`은 다음 최상위 키를 사용한다.

- `schema_version: 1`
- `manual`: ID, 제목, 독자, 상태, 판본, 근거 기준, 목적
- `overview`: 요약, 정신 모형, 역할, 구성요소, 생명주기, 초보자 오해
- `workflows`: trigger, 목표, 결과, lesson 순서
- `lessons`: 독립 교육 단위와 단계별 operation/action/evidence/success, write 단계의 readback
- `sources`: 근거 ID, 제목, 등급, 로컬 경로, 확인일, 소문자 SHA-256

기본 예제는 `assets/manual-config.example.yaml`, 실행 가능한 최소 패키지는 `examples/minimal-manual/`을 사용한다.

## 3. 혼합 입력 처리

1. 안전한 임시 폴더에 압축을 푼다.
2. 파일 목록, 크기, SHA-256을 기록한다.
3. 파일명·본문·사용자 설명을 근거로 역할을 제안한다.
4. 불명확한 파일은 `REFERENCE` 또는 `EXCLUDE`로 둔다.
5. Book은 CONTENT만 본문 빌더에 전달한다.
6. Manual은 `manual.yaml`이 참조한 EVIDENCE와 매체만 사용한다.

## 4. 근거 등급

| 등급 | 의미 |
| --- | --- |
| `source` | 공식 문서, 코드, 설정, 버전 고정 저장소 |
| `ui` | 실제 제품 화면·캡처·표시 값 |
| `runtime` | API, 로그, 상태, 데이터 readback |
| `operator-confirmed` | 책임 있는 운영자의 명시적 확인 |
| `inference` | 앞 근거에서 추론했지만 직접 확인하지 못함 |

`final` 매뉴얼의 각 실행 단계는 `inference`만으로 구성할 수 없다. 모든 단계는 `operation: read|write`를 선언하며, `write`는 high/critical 위험도, 승인, 안전 fixture, 변경 후 `readback`이 필수다.

## 5. 경로와 매체

- `manual.yaml`의 모든 로컬 경로는 매니페스트 폴더 상대경로다.
- 절대경로와 `..`로 루트를 벗어나는 경로를 금지한다.
- source와 media의 `sha256`은 빌드 시 실제 파일과 일치해야 하며 검증 시 다시 대조한다.
- 매체는 lesson이 실제로 참조한 파일만 출력 패키지에 복사한다.
- 실제 UI가 필요한 자리에 임의 mock을 실제 화면처럼 넣지 않는다.
- 매체가 없으면 빈 placeholder 대신 근거 기반 다이어그램을 쓰거나 상태를 `provisional`로 제한한다.

## 6. Book 원고 순서와 README 변환

Book 파일 순서는 다음 우선순위를 따른다.

1. `book.yaml`의 `files.order`
2. README의 명시적 목차 링크
3. 숫자 접두 파일명
4. 자연 정렬 파일명

README 블록을 이동하거나 제외하려면 `files.strip_front_matter_sections` 또는 `files.front_matter_drop_paragraphs`에 정확히 기록한다. 사실 주장과 본문 서술은 변경하지 않는다.
