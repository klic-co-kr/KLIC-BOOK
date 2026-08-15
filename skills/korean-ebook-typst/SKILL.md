---
name: korean-ebook-typst
description: "Markdown 원고를 한국어 출판형 PDF로 빌드 — 스타일 팩 4종(practical 신국판/essay 사륙판/business 백서판/lecture A4). typst 엔진(한국어 CJK + 수식 mitex 네이티브). QC 게이트(판면 오버플로 G1·폰트 계약 G2·글자수 밴드 G3) 통과 시에만 final/ 생성. korean-ebook(WeasyPrint) 대체."
---

# korean-ebook-typst

## 정체성

MD → 출판형 PDF. **typst 엔진**. 한국어 CJK + 수식(LaTeX mitex) 네이티브.

**스타일 = 숫자 계약(tokens.json) + 문서 계약(STYLE.md) + 렌더 규칙(theme.typ)**.
스타일 팩 4종이 `styles/`에 상주하며, build.py가 조립 시 `build/`로 복사한다.

## 워크플로우

```bash
# 책 디렉터리에 typst-build.yaml 작성 후:
python3 scripts/build.py <책dir>     # → <책dir>/draft/<제목>.pdf
python3 scripts/qc_gate.py <책dir>   # PASS 시에만 → <책dir>/final/
```

(final/은 qc_gate.py만 생성한다. 빌드 산물 `build/`·`draft/`·`final/`·`gate-report.json`은 gitignore.)

## 원고 헤딩 규약 (중요)

md2typst 매핑: `##`→H1(`=`), `###`→H2(`==`), `####`→H3(`===`). **`#` 단독도 H1(`=`)로 변환된다.**

따라서 **챕터 md는 장 제목에 `##`를 쓰고 `#`를 쓰지 않는다** — `#`와 `##`를 혼용하면
둘 다 H1으로 개면(장마다 pagebreak)해 충돌한다. 절 제목은 `###`, 소절은 `####`.

> 참고: `tests/fixtures/sample-manuscript/`는 `#`를 사용해 실제로 이 충돌 상태다.
> 스모크 테스트용 fixture이며 실제 원고 규약이 아니다.

## typst-build.yaml

```yaml
style: practical        # practical | essay | business | lecture
title: "책 제목"
subtitle: "부제"
author: "저자"
date: "2026-08"
chapters:
  - manuscript/ch01.md  # 목록 순서가 책 순서(파일명 정렬 아님)
cover: assets/cover.png   # 선택. 없으면 타이포그래픽 표지
```

기존 book-config.yaml(WeasyPrint 계약)과 별개 파일 — 공존, 간섭 없음.

## 스타일 선택

| 스타일 | 판형 | G3 밴드(자/줄) | 대상 |
|---|---|---|---|
| practical | 153×225 신국판 | 30–40 | IT 실용서·가이드 |
| essay | 128×188 사륙판 | 22–26 | 산문·회고 |
| business | 200×280 백서판 | 36–48 | 백서·컨설팅 리포트 |
| lecture | 210×297 A4 | 40–52 | 강의자료 |

G3 밴드는 판형별 물리값(판면 폭 × 본문 pt의 전각 환산 기준) — 스타일 간 공유 값이 아니다.

## QC 게이트

| 게이트 | 검사 | 판정 |
|---|---|---|
| G1 | 본문 잉크 bbox가 body_frame_pt 판면 내 (±3pt 허용, 표지 제외, 푸터 쪽번호 면제) | FAIL |
| G2 | 실사용(임베드) 폰트 ⊆ tokens fonts 계약(stack + ps 별칭, 수식 폰트 allowlist) | FAIL |
| G3 | 본문 한 줄 자수가 스타일 밴드 내 (표지·목차 제외, 정렬 줄만) | WARN |

PASS 조건은 G1·G2 무위반. `gate-report.json`(책 디렉터리에 생성)을 참조해
지적된 면만 수정 후 재빌드한다.

## 새 스타일 작성

`docs/style-authoring.md` 참조 — 스모크 테스트, 핵심 심볼 프로브, aesthete 기하 검사
게이트 포함(텍스트 측정·aislop은 aesthete v1 한계로 제외).

## md2typst 변환 규칙

- 헤딩: 위 규약 참조(`#`·`##`→`=`, `###`→`==`, `####`→`===`)
- `![](img)` → `#figure(image("img"))`
- `$$...$$`(블록)·`$...$`(인라인) → `#mitex[...]` (LaTeX 그대로, 한국어 \text 포함)
- 화폐 `$<숫자>/<단위>` escape
- `>` 블록 인용 → `#quote[...]`
- 본문 typst 특수(`# [ ] < > @ * _ \ $`) escape, 비헤딩 `##` 잔재 escape

## 의존성

- typst 바이너리(0.15+, PATH / ~/.local/bin/typst)
- python3 + `requirements.txt` (pymupdf>=1.23, pyyaml>=6.0) — `pip install -r requirements.txt`
- @preview/mitex:0.2.7(첫 빌드 시 자동 다운)
- aesthete 스킬(스타일 저작 시에만, bun)

## 한계

- 인라인 `$...$` 한국어 \text + 복잡 매크로 혼재 시 일부 깨짐 → `$$` 권장
- 표·복잡 레이아웃은 typst 수동 작업
- 레거시 수동 빌드: `templates/book.typ` 유지(신규 빌드는 build.py 사용)
- 폰트 폴백 경고: 빌드 머신에 Pretendard·KoPubWorld바탕·Noto Serif KR 등
  스택 하위 폰트가 없다는 typst 경고는 **폴백 설계상 무해**(2순위 이후 미설치는
  정상 동작) — 무시해도 된다. 단 임베드 폰트가 바뀌면 G2 ps 별칭 등록 필요.

## 연계

- 입력: 정제 MD(pdf-to-md 또는 직접)
- 레거시: korean-ebook(WeasyPrint), templates/book.typ
