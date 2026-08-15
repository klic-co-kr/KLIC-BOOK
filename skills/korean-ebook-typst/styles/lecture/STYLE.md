# Lecture — A4 강의자료

## 정체성
- 레거시 book.typ(llm-lecture 시절 A4 디자인)의 토큰화. 강의·세미나 배포용.
- 세로 촬영 판형 아님 — A4 210×297. 프린트·스크린 공용.

## 규칙 (근거: 레거시 book.typ 실측값)
- 판면: top 28 / bottom 22 / inner 23 / outer 23 mm
- 본문: Noto Sans CJK KR 10pt, 행간 0.85em, 양끝맞춤
- H1: 장마다 개면, 20pt bold, 위에 accent 라벨(label-top 토큰)
- H2: 13pt bold accent
- 쪽번호: 하단 중앙, label 9pt, ink-mute

## 금지 사항
- 자간(tracking) 조정 금지 — bookforge 실측에서 Noto Serif KR −25/1000em에서 잉크 겹침 보고(참고: bookforge references/pagination.md)
- 본문 폰트 크기 10pt 미만 축소 금지
- 한 줄 26자 초과 지속(밴드 22–26, WARN 게이트)

## 근거 표기
수치는 레거시 book.typ 실측 + bookforge 참고값. 우리 자체 상업본 실측 아님.
