# 산출물 계약

기본 출력 폴더는 다음 구조를 갖는다.

```text
out/
├── <제목>_<output_name>.pdf
├── book.html
├── source_manifest.json
├── build_report.json
├── verification/
│   ├── verification.json
│   └── verification.md
├── rendered/
│   ├── page-001.png
│   └── ...
├── contact-sheet.jpg
└── summary/                      # (summary.enabled 시)
    ├── glossary.md               # 용어 후보 스캐폴드 (H2 + **굵은 용어**)
    └── chapters/
        ├── ch01-<slug>.md        # 장별 요약 스캐폴드 (핵심 아이디어·절 구성·주요 개념·핵심 요약)
        └── ...
```

## 최종 사용자 제공 권장 파일

- 최종 PDF
- 검수 보고서 Markdown
- 전체 패키지 ZIP
- SHA-256 파일

HTML과 전 페이지 PNG는 사용자가 편집 추적이나 시각 검수를 요청했을 때 함께 제공한다.

## 파일명 규칙

- 운영체제 금지문자를 제거한다.
- 제목을 임의 약어로 줄이지 않는다.
- `final`, `최종`, `진짜최종2` 같은 누적 이름 대신 판본 또는 날짜를 쓴다.
- 예: `포워드_디플로이드_엔지니어_한국어판_2026-08-04.pdf`
