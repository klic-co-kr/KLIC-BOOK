# 입력 계약

## 1. 역할 분리

모든 입력은 다음 네 역할 가운데 하나여야 한다.

| 역할 | 의미 | 최종 본문 사용 |
|---|---|---:|
| CONTENT | 책에 실제로 수록할 원고, 표, 이미지, 각주 | 예 |
| REFERENCE | 시각 구성, 편집 방식, 품질 수준의 예시 | 아니오 |
| CONFIG | 제목, 저자, 순서, 색상, 판본 정보 | 메타데이터만 |
| EXCLUDE | 이전 결과물, 임시 파일, 중복 사본, 개인 메모 | 아니오 |

`REFERENCE`를 `CONTENT`로 바꾸려면 사용자의 명시적인 지시가 필요하다. “예시로 첨부했다”, “이런 식으로 만들어 달라”, “참고해서 편집해 달라”는 말은 콘텐츠 통합 허가가 아니다.

## 2. 권장 프로젝트 구조

```text
project/
├── content/
│   ├── README.md
│   ├── 01-chapter.md
│   └── 02-chapter.md
├── references/
│   ├── layout-example.pdf
│   └── workflow-example.md
├── book.yaml
└── output/
```

## 3. 혼합 ZIP 처리

혼합 ZIP은 다음 순서로 다룬다.

1. 안전한 임시 폴더에 압축을 푼다.
2. 파일 목록, 크기, 해시를 기록한다.
3. 파일명·본문·사용자 설명을 근거로 역할을 제안한다.
4. 불명확한 파일은 `EXCLUDE` 또는 `REFERENCE`로 둔다.
5. `content/`에 복사된 파일만 빌드 입력으로 사용한다.

## 4. 소스 맵 예시

```yaml
content:
  - path: content/README.md
    reason: 책 소개와 저작권 안내를 포함한 원고
  - path: content/01-chapter.md
    reason: 본문 1장
reference:
  - path: references/ui-guide.pdf
    reason: 편집 흐름과 검수 형식 예시
exclude:
  - path: old-output.pdf
    reason: 이전 결과물
```

## 5. 원고 순서

우선순위는 다음과 같다.

1. `book.yaml`의 `files.order`
2. README의 명시적 목차 링크
3. 숫자 접두 파일명
4. 자연 정렬 파일명

순서를 추측해야 한다면 빌드 보고서에 추론 근거를 기록한다.

## 6. README 편집 변환

README에는 책 본문과 저장소 화면용 문구가 섞일 수 있다. 다음 조건을 모두 만족할 때만 일부 블록을 이동하거나 제외한다.

1. 대상 문구가 `files.strip_front_matter_sections` 또는 `files.front_matter_drop_paragraphs`에 정확히 지정되어 있다.
2. 이동 대상이라면 표지·속표지·편집본 안내 등 대체 위치가 설정에 명시되어 있다.
3. 사실 주장과 본문 서술은 변경하지 않는다.
4. 빌드 보고서에 변환 설정이 기록된다.

자동으로 “불필요해 보이는 문장”을 지우지 않는다. FDE 전용 변환은 `references/fde-regression-profile.md`에만 정의되며 범용 설정에는 적용하지 않는다.
