# 제품 디자인 심리학

Wouter de Bres 의 웹북 [Product Design Psychology](https://productdesignpsychology.com/)
한국어 번역판. 디자이너·사용자·조직의 마음을 다루는 심리학 에세이 40장.

- 원문: 서문 1편 + 본문 40장 (4부), 2026-08 시점 전체 수집
- 번역: KLIC — fluent-korean 문체 규칙 준수 (G4 문체 경고 0건)
- 판형: 신국판 153×225 (style: auto 판정), 통권 319면
- 삽화: 장별 원문 삽화 40장 원본 그대로 수록
- 참고 자료: 각 장 말미 영문 서지사항 원문 보존

## 구성

| 부 | 범위 | 주제 |
|---|---|---|
| 제1부 | 1–10장 | 디자이너의 마음 — 거짓 합의, 에고, 착각, 취향과 창의성 |
| 제2부 | 11–20장 | 디자인을 다루는 마음 — 첫인상, 어포던스, 인지 부하, 기억, 레이아웃 |
| 제3부 | 21–30장 | 사용자의 마음 — 멘탈 모델, 현재 편향, 습관, 선택 과부하, 이탈 |
| 제4부 | 31–40장 | 조직의 마음 — 회의실, 지표, 로드맵, 매몰비용, 리서치 남용 |

## 빌드

```bash
python3 fetch_site.py                                              # 원문 갱신 (manuscript-en/)
python3 ../../skills/korean-ebook-typst/scripts/build.py .         # → draft/
python3 ../../skills/korean-ebook-typst/scripts/qc_gate.py .       # PASS → final/
```

QC: G1 판면 오버플로 무위반 · G2 폰트 계약 통과 · G4 문체 0건.
G3 밴드 경고는 참고 자료의 영문 서지사항·URL 줄에서 발생한다 (한글 밴드
계약과 본질적으로 불일치 — 무해).

## 파일

- `manuscript/` — 한국어 번역 원고 (45파일: 서문 + 4부 표지 + 40장)
- `manuscript-en/` — 영문 원문 대조본 (fetch_site.py 수집)
- `assets/` — 장별 삽화 40장
- `제품_디자인_심리학_product-design-psychology-ko.pdf` — 통권 PDF

저작권 고지는 [ATTRIBUTION.md](ATTRIBUTION.md) — 개인 학습용, 재배포 불가.
