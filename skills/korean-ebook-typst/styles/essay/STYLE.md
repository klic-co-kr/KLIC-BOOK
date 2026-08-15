# Essay — 46판 미니멀 에세이

## 정체성
- 128×188 46판. 여백이 주인공. 위계는 크기·여백·정렬로만. 먹 1도 + 포인트 1색(terracotta).

## 규칙 (근거: 설계 참고값 + 우리 프로브 실측)
- 판면: top 24 / bottom 26 / inner 20 / outer 20 mm — 하단 2mm 크게(시각 중심 보정). 본문 88×138mm
- 본문: Noto Serif CJK KR 10pt / 행간 1.9em / 양끝맞춤 / 들여쓰기 없음
- 장 시작: 여백 낙차형 — 판면 상단 52mm 비우고 제목(theme.typ `mm(52) - mm(margin.top)` 산식)
- 장번호: label 8.5pt accent terracotta, 2자리("01"). 내장 heading counter는
  show 규칙 시점에 0이라(0.15.1 프로브 실측) 전용 카운터 사용
- H1: 15pt Regular(굵기 아님) — 위계는 크기·여백으로만
- H2: 10pt medium 고딕
- 색: paper #FBFAF7(순백 금지, 페이지 fill) / ink #1A1A1A(순흑 금지) / accent #A2604A — 면적 2% 이하
- 한 줄 22–26자(밴드, WARN 게이트) — 88mm 판면 폭 × 10pt 전각 물리 약 25자 기준

## 폰트 계약 참고
- 빌드 머신 실측: "Noto Serif CJK KR"·"Noto Sans KR" 설치, "Noto Serif KR" 미설치.
  body·heading1 스택 1순위를 설치 폰트로 — 폴백 임베드 없이 G2가 성립한다.
- ttc 임베드 basefont "NotoSerifCJKkr-Regular-..."의 임베드명 사례를
  `ps: ["NotoSerifCJKkr"]`로 별칭 등록(qc_gate allowed_fonts).
- Nanum 계열은 임베드 PostScript명 정규화 불일치 리스크로 사용하지 않는다.

## 금지 사항
- 괘선·박스·배경색(페이지 paper 제외)·드롭캡·한글 이탤릭·밑줄·형광
- 볼드 페이지당 1회 초과, 러닝헤드 금지
- 자간 조정 금지(전 스타일 공통)
- 목차 리더 점선

## 근거 표기
설계 참고값 + typst 0.15.1 프로브 실측(장번호 카운터). 우리 자체 조판 실측 아님.
