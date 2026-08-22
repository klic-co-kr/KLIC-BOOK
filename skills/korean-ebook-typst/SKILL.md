---
name: korean-ebook-typst
description: "Markdown 원고를 한국어 출판형 PDF로 빌드 — 스타일 팩 4종(practical 신국판/essay 46판(B6)/business 백서판/lecture A4). typst 엔진(한국어 CJK + 수식 mitex 네이티브). QC 게이트(판면 오버플로 G1·폰트 계약 G2·글자수 밴드 G3) 통과 시에만 final/ 생성. korean-ebook(WeasyPrint) 대체."
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

## 챕터 도식 (인포그래픽 — Phase 5)

챕터 md에 ```infographic 펜스(JSON)를 넣으면 출판 품질 벡터 도식이 그
자리에 삽입된다. layout: `flow`(순차 2~8단계)·`cards`(병렬
강조)·`matrix`(2축 비교)·`before_after`(전환 대비)·`ladder`(성숙도
계단)·`roadmap`(시간 전개)·`topology`(구성 관계)·`approval`(결재
흐름)·`layers`(계층 구조)·`composite`(복합 씬 — 주+보조). 좌표는 Python이 계산하고 I1 린트(텍스트
예산·잉크 컨테인먼트·숫자-evidence 교차검증)를 통과해야 빌드된다. 도식
하나 검사·미리보기:
`python3 scripts/infographic/cli.py lint|preview …`. 저작 규약·라우팅 표는
`references/infographic/authoring.md`.

## 자동화 (2026-08)

**`style: auto`** — 원고 콘텐츠에서 판형을 자동 판단(`scripts/style_pick.py`).
챕터당 시각 요소(표 1.0 + 이미지 1.0 + 수식 0.5 + 코드펜스 0.3)가 1.5건 이상이면
**lecture(A4)** — 논문·도표형 원고. 문단 평균 400자+·표 0.5건 미만이면
**essay(B6)** 산문. 그 외 **practical(신국판)** 실용서. business는 정형
리포트용이라 명시 지정만. 판단 사유는 빌드 로그에 출력된다.

**`cover: auto`(또는 생략)** — 4변형 벡터 표지 문법에서 자동 선택한다.
변형은 제목 해시로 결정적 분배(같은 책 = 같은 표지, 책마다 상이)하며
`cover_variant: 1|2|3|4`으로 직접 지정할 수 있다.
V1 비대칭 좌측(엣지 바·두 원·바텀 앵커) · V2 이중 프레임 문고형(괘선·중앙
타이포·코너 틱) · V3 수평 밴드형(브랜드 밴드 타이틀·원 클러스터) ·
V4 엣지 포인트(우상단 하프톤 도트 필드 감쇠 + 도트 언더라인).
모든 변형이 마지막 단어 강조 타이포·'지음'·발행 락업을 공유하고 판형 크기에 맞춘다.
`cover_series`(상단 시리즈 라벨, 기본 "KLIC BOOKS")와
`cover_notes`(하단 불릿 목록)로 원고별 안내문을 넣는다.
명시 경로(`cover: assets/x.png`)를 주면 그 파일을 쓴다.

**G2 변형 접미사 매칭** — 임베드 PS명이 스택 가족명 + 짧은 스타일 접미사
(NanumSquare_ac → NanumSquare_acR 등 4자 이하)면 같은 가족으로 통과.
매 책마다 tokens.json에 ps 별칭을 손으로 추가하던 일이 필요없어졌다.

## 원고 헤딩 규약 (중요)

md2typst 매핑: `##`→H1(`=`), `###`→H2(`==`), `####`→H3(`===`). **`#` 단독도 H1(`=`)로 변환된다.**

따라서 **챕터 md는 장 제목에 `##`를 쓰고 `#`를 쓰지 않는다** — `#`와 `##`를 혼용하면
둘 다 H1으로 개면(장마다 pagebreak)해 충돌한다. 절 제목은 `###`, 소절은 `####`.

> 참고: `tests/fixtures/sample-manuscript/`는 `#`를 사용해 실제로 이 충돌 상태다.
> 스모크 테스트용 fixture이며 실제 원고 규약이 아니다.

## typst-build.yaml

```yaml
style: practical        # practical | essay | business | lecture | auto(원고에서 자동판단)
title: "책 제목"
subtitle: "부제"
author: "저자"
date: "2026-08"
chapters:
  - manuscript/ch01.md  # 목록 순서가 책 순서(파일명 정렬 아님)
cover: auto             # auto/생략 = 벡터 표지 자동생성, 경로 = 해당 파일 사용
cover_series: "KLIC BOOKS"   # 선택 — 표지 상단 시리즈 라벨
cover_notes:                 # 선택 — 표지 하단 불릿 목록
  - "· 구성 요약 첫 줄"
  - "· 구성 요약 둘째 줄"
```

기존 book-config.yaml(WeasyPrint 계약)과 별개 파일 — 공존, 간섭 없음.

## 스타일 선택

| 스타일 | 판형 | G3 밴드(자/줄) | 대상 |
|---|---|---|---|
| practical | 153×225 신국판 | 30–40 | IT 실용서·가이드 |
| essay | 128×188 46판(B6) | 22–26 | 산문·회고 |
| business | 200×280 백서판 | 36–48 | 백서·컨설팅 리포트 |
| lecture | 210×297 A4 | 40–52 | 강의자료 |

G3 밴드는 판형별 물리값(판면 폭 × 본문 pt의 전각 환산 기준) — 스타일 간 공유 값이 아니다.

## QC 게이트

| 게이트 | 검사 | 판정 |
|---|---|---|
| G1 | 본문 잉크 bbox가 body_frame_pt 판면 내 (±3pt 허용, 표지 제외, 푸터 쪽번호 면제) | FAIL |
| G2 | 실사용(임베드) 폰트 ⊆ tokens fonts 계약(stack + ps 별칭 + 변형 접미사 매칭, 수식 폰트 allowlist) | FAIL |
| G3 | 본문 한 줄 자수가 스타일 밴드 내 (표지·목차 제외, 정렬 줄만) | WARN |
| G4 | 한글 문체 — 기계 한국어·번역투 패턴(명사형 종결·조각문·되어지·상투구·'의' 연쇄·엠대시 밀도). 원고 md에서 검사, [fluent-korean](https://github.com/snflkd/fluent-korean) 규칙 기계화 | WARN |

PASS 조건은 G1·G2 무위반. `gate-report.json`(책 디렉터리에 생성)을 참조해
지적된 면만 수정 후 재빌드한다.

## 새 스타일 작성

`docs/style-authoring.md` 참조 — 스모크 테스트, 핵심 심볼 프로브, aesthete 기하 검사
게이트 포함(텍스트 측정·aislop은 aesthete v1 한계로 제외).

## md2typst 변환 규칙

- 헤딩: 위 규약 참조(`#`·`##`→`=`, `###`→`==`, `####`→`===`)
- 선두 YAML frontmatter(`---` 쌍) 제거 — 메타데이터 누출 방지
- HTML 주석(`<!-- ... -->`) 제거 — 코드 스팬 내부는 보존
- markdown 강조 `**굵게**`/`*기울임*` → typst `*strong*`/`_emph_` (코드 스팬은 리터럴)
- `![](img)` → `#figure(image("img"))` — build.py가 에셋을 build/assets/로
  복사(챕터 인덱스 prefix)하고 경로를 재작성
- `$$...$$`(블록)·`$...$`(인라인) → `#mitex[...]` (LaTeX 그대로, 한국어 \text 포함)
- 화폐 `$<숫자>/<단위>` escape
- `>` 블록 인용 → `#quote[...]`
- 헤딩 중간점(`·`) 뒤 줄바꿈 기회 삽입(U+200B ZWSP) — typst는 U+00B7을
  break 기회로 안 씀. 수식·코드 헤딩 제외
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
