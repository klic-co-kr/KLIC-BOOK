# b5 — B5판 실용서 (176×250)

## 정체성

practical(신국판)의 B5 확장판. 같은 실용서 성격 — 산세리프 본문, 장별
오프너, 절급 목차 — 를 더 넓은 판면에 담는다. 도서관·강의 배포용 처럼
한 면에 더 많은 본문을 싣는 판형.

## 규칙

| 항목 | 값 |
|---|---|
| 재단 | 176 × 250 mm (ISO B5) |
| 판면 | top 24 · bottom 22 · inner 22 · outer 18 mm |
| 본문 프레임 | 136 × 204 mm (x0 62.36, y0 68.03, x1 447.87, y1 646.30 pt) |
| 본문 | 10pt · 행간 1.7em |
| 헤딩1 | 22pt bold · 장 오프너(액센트 바) |
| 헤딩2 | 14pt bold · 액센트색 |
| 쪽번호 | 하단 중앙 |
| G3 밴드 | 35–45자/줄 — 판면 136mm × 10pt 전각(≈3.53mm) ≈ 38.5자 중심 |

## 폰트 계약

5폰트 라인업과 동일 — practical과 같이 Freesentation 선행(2026-08-20
사용자 지정 스왑), label은 Montserrat 선행. 정적 웨이트만 사용
(typst VF Thin 버그 — memory `typst-vf-thin-font-bug`).

## 렌더 규칙

theme.typ는 practical 것을 공유 구조로 복제했다. H2 pad(top: 3.5pt)
가드 포함 — Pretendard 계열 어센더의 페이지 상단 G1 초과 방지.
