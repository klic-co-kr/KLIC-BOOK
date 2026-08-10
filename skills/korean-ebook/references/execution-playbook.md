# 실행 플레이북

## A. 가장 빠른 정상 경로

```bash
python scripts/publish_book.py --input manuscript.zip --output-dir out --config book.yaml
python scripts/verify_pdf.py --pdf out/*.pdf --source-manifest out/source_manifest.json --report-dir out/verification
python scripts/render_pdf.py --pdf out/*.pdf --out-dir out/rendered --dpi 160
python scripts/make_contact_sheet.py --input-dir out/rendered --output out/contact-sheet.jpg
```

접촉표를 확인한 뒤 문제가 있는 페이지를 개별 PNG로 연다. 수정 후 위 네 단계를 다시 수행한다.

## B. 참고 PDF가 있는 경로

참고 PDF는 빌드 입력이 아니다. 에이전트가 시각적으로 분석한 뒤 `book.yaml`의 색상·여백·표지 구성만 조정한다.

```bash
python scripts/publish_book.py \
  --input manuscript.zip \
  --reference example-layout.pdf \
  --output-dir out \
  --config book.yaml
```

검수 시 참고 오염 검사도 실행한다.

## C. 표가 잘릴 때

1. 열 수와 가장 긴 셀을 확인한다.
2. `table-layout: fixed`와 `overflow-wrap: anywhere`를 유지한다.
3. 특정 표에만 `.compact-table` 클래스를 적용한다.
4. 그래도 안 되면 해당 부록을 가로 A4 named page로 분리한다.
5. 글자 크기 8pt 미만은 마지막 수단이다.

## D. 목차 페이지가 어긋날 때

- 목차는 WeasyPrint의 `target-counter()`로 생성해야 한다.
- 수동 페이지 번호를 넣지 않는다.
- CSS 수정 후 전체 PDF를 다시 생성한다.
- PDF 북마크와 화면 목차의 제목 구조가 같은지 확인한다.

## E. 글꼴이 빠질 때

- `fc-match NanumMyeongjo` 또는 운영체제의 글꼴 목록을 확인한다.
- CSS에 설치된 가족 이름을 정확히 쓴다.
- `pdffonts`에서 `emb=yes`, `uni=yes`인지 확인한다.
- 글꼴 파일을 결과 패키지에 포함하지 않는다.
