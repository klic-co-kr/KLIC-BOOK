# 책 PDF 다운로드 링크 설계

## 목표

GitHub 저장소 첫 화면에서 출판 완료된 책 다섯 권의 PDF를 바로 내려받을 수 있게 하고, 새 FactoryX 책의 전체 출판 패키지를 원격 저장소에 공개한다.

## 구조

- 루트 `README.md`의 책 표에 `PDF 다운로드` 열을 둔다.
- 다운로드 링크는 각 책에 커밋된 PDF의 상대경로 뒤에 `?raw=1`을 붙여 GitHub 원본 응답을 사용한다.
- `books/factoryx-ai-infrastructure/README.md` 상단에도 최종 PDF 다운로드 링크를 둔다.
- FactoryX의 원고, 조사 원장, 도형·차트, 빌드 산출물, 검증 보고서를 함께 커밋해 PDF의 재현성과 근거 추적성을 보존한다.

## 검증

- README에 등록한 다섯 링크가 모두 `?raw=1`을 사용한다.
- 각 링크에서 쿼리 문자열을 제거한 상대경로가 실제 Git 추적 PDF 파일과 일치한다.
- FactoryX PDF는 100쪽이며 기존 SHA-256과 일치한다.

## 범위 제외

- GitHub Release 생성과 별도 CDN 배포는 하지 않는다.
- 기존 책 PDF를 다시 빌드하거나 내용·파일명을 바꾸지 않는다.
