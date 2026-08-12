# 호출 프롬프트 예시

## Book — 출판형 PDF

```text
$korean-ebook
첨부 ZIP의 Markdown만 CONTENT로 사용해 A4 출판형 PDF로 만들어. 함께 첨부한 PDF는 디자인 REFERENCE이므로 문장이나 목차를 합치지 마. 1단 목차, 원문 근거 도형, 전 페이지 렌더링과 검수 보고서까지 만들어.
```

## Manual — 운영 가이드

```text
$korean-ebook
공식 운영 문서와 실제 확인 화면을 EVIDENCE로 사용해 신규 운영자용 정적 HTML 매뉴얼을 만들어. 화면 목록이 아니라 요청 접수부터 완료 확인까지 업무 흐름으로 구성하고, 각 단계에 행동·근거·성공 판정을 넣어. 미확인 UI는 발명하지 말고 provisional로 표시해.
```

## Manual — 고위험 작업 포함

```text
korean-ebook의 manual 모드로 관리자 권한 변경 SOP를 작성해. 실제 운영 계정은 바꾸지 말고 sandbox fixture와 승인 경계를 명시해. 변경 전후 권한 readback과 감사 기록을 완료 조건으로 넣어.
```

## Hybrid — PDF와 웹 매뉴얼

```text
$korean-ebook
승인된 원고와 제품 근거에서 교육용 PDF 책과 운영용 HTML 매뉴얼을 모두 만들어. 근거 ID는 공유하되 book과 manual은 각각 빌드·검증하고 결과 보고서를 분리해.
```

## 사용하면 안 되는 요청

```text
스캔 계약서에서 도장만 지워 줘.
```

단순 PDF 편집·레드액션은 이 스킬의 범위가 아니다.
