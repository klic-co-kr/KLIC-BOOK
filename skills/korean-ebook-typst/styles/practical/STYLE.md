# Practical — 신국판 IT 실용서

## 정체성
- 153×225 신국판. 단계별 가이드·용어집·기술 개론서. 시스템 설계·github-guide 계열.
- 명조 본문 + 고딕 제목. 위계는 크기·굵기·헤어라인으로만. 박스 배경색 금지.

## 규칙
- 판면: top 22 / bottom 20 / inner 20 / outer 15 mm — 본문 118×183mm
- 본문: Noto Serif CJK KR 10pt / 행간 1.7em / 양끝맞춤 / 첫줄 들여쓰기 없음
- H1: 장마다 개면, 18pt bold, 하단 헤어라인 0.4pt
- H2: 13pt bold accent(navy #1F4E79)
- 쪽번호: 하단 중앙 label 8.5pt ink-mute
- 한 줄 30–40자(밴드, WARN 게이트) — 118mm 판면 폭 × 10pt 전각 물리 약 33자 기준

## 폰트 계약 참고
- body 스택 1순위는 빌드 머신에 설치된 "Noto Serif CJK KR" — 폴백 임베드 없이
  G2가 성립한다. "Noto Serif KR"·"KoPubWorld바탕"은 폰트 있는 환경용 후순위.
- "KoPubWorld바탕"의 임베드 PostScript명은 "KoPubWorldBatang"("NotoSerifCJKkr"도
  임베드명 사례) — G2 정규화 매칭을 위해 `ps` 필드로 임베드명을 별칭 등록했다
  (qc_gate allowed_fonts).
- 빌드 머신에 스택 전체가 없으면 typst가 임베드 폰트를 폴백시킨다.
  이때 G2를 통과하려면 실제 임베드되는 폰트도 ps에 추가 등록할 것.

## 금지 사항
- 자간(tracking) 조정 금지 (Noto Serif KR −25/1000em 잉크 겹침 보고 사례 있음)
- 본문 10pt 미만, 행간 1.5em 미만
- 배경 채색 박스·라운드 코너·그림자·이모지
- 페이지당 강조(bold) 2회 초과

## 근거 표기
설계 참고값. 우리 자체 실측 아님 — 우리 책 빌드 축적 후 치환.
