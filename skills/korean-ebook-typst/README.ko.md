# korean-ebook-typst

## 정체성

Markdown 원고 → 출판형 PDF. **typst 엔진** 기반. `korean-ebook`(WeasyPrint)의
한국어 자모 분리·수식 한계를 근본 해결.

- 한국어 CJK 네이티브(자모 분리 없음)
- 수식 `$$...$$`/`$...$` → typst mitex(LaTeX 호환) 고품질 렌더
- **스타일 팩 4종** — 숫자 계약(tokens.json) + 문서 계약(STYLE.md) + 렌더 규칙(theme.typ)
- QC 게이트 통과 시에만 final/ 생성

## 설치

typst 바이너리 필요(0.15+, PATH 또는 `~/.local/bin/typst`).
```bash
# typst 설치(바이너리)
curl -sL https://github.com/typst/typst/releases/latest/download/typst-x86_64-unknown-linux-musl.tar.xz | tar xJ
mv typst-x86_64-unknown-linux-musl/typst ~/.local/bin/
pip install -r requirements.txt   # pymupdf, pyyaml
```
mitex 패키지는 첫 빌드 시 자동 다운로드(@preview/mitex:0.2.7).

## 워크플로우

책 디렉터리에 `typst-build.yaml`을 작성한다.

```yaml
style: practical        # practical | essay | business | lecture
title: "책 제목"
author: "저자"
date: "2026-08"
chapters:
  - manuscript/ch01.md  # 목록 순서가 책 순서
cover: assets/cover.png   # 선택. 없으면 타이포그래픽 표지
```

```bash
python3 scripts/build.py <책dir>     # 조립+컴파일 → <책dir>/draft/<제목>.pdf
python3 scripts/qc_gate.py <책dir>   # PASS 시에만 → <책dir>/final/
```

- `build.py`: 스타일 팩(base.typ + theme.typ + tokens.json) 복사 → md2typst 변환 →
  main.typ 조립 → typst 컴파일
- `qc_gate.py`: 게이트 검사 → PASS면 final/ 복사. FAIL이면 기존 final/ PDF를
  폐기(낡은 PASS 결과 방지). draft에 pdf가 2개 이상이면 경고
- 빌드 산물(`build/`·`draft/`·`final/`·`gate-report.json`)은 gitignore

## 스타일 팩

| 스타일 | 판형 | G3 밴드(자/줄) | 대상 |
|---|---|---|---|
| practical | 153×225 신국판 | 30–40 | IT 실용서·가이드 |
| essay | 128×188 사륙판 | 22–26 | 산문·회고 |
| business | 200×280 백서판 | 36–48 | 백서·컨설팅 리포트 |
| lecture | 210×297 A4 | 40–52 | 강의자료 |

새 스타일 작성은 `docs/style-authoring.md` 참조.

## 원고 헤딩 규약 (중요)

md2typst 매핑: `##`→H1(`=`), `###`→H2(`==`), `####`→H3(`===`).
**`#` 단독도 H1로 변환된다** — `#`와 `##`를 혼용하면 둘 다 H1으로 개면(장마다
pagebreak)해 충돌한다. **챕터 md는 장 제목에 `##`를 쓰고 `#`를 쓰지 않는다.**
절 제목은 `###`, 소절은 `####`.

## md2typst 변환 규칙

- 헤딩: 위 규약 참조
- 선두 YAML frontmatter(`---` 쌍) 제거 — 메타데이터 누출 방지
- HTML 주석(`<!-- ... -->`) 제거 — 코드 스팬 내부는 보존
- markdown 강조 `**굵게**`/`*기울임*` → typst `*strong*`/`_emph_` (코드 스팬은 리터럴)
- `![](path)` → `#figure(image("path"))` — build.py가 경로를 재작성
- `$$...$$` / `$...$` 수식 → `#mitex[`...`]` (LaTeX 그대로, 한국어 \text 포함)
- `>` 블록 인용 → `#quote[...]`
- 헤딩 중간점(`·`) 뒤 줄바꿈 기회 삽입(typst는 U+00B7을 break 기회로 안 씀)
- 화폐 `$<숫자>/<단위>` escape, 본문 typst 특수(`# [ ] < > @ * _ \ $`) escape,
  비헤딩 `##` 잔재 escape

## QC 게이트

| 게이트 | 검사 | 판정 |
|---|---|---|
| G1 | 본문 잉크 bbox가 body_frame_pt 판면 내 (±3pt 허용, 표지 제외, 푸터 쪽번호 면제) | FAIL |
| G2 | 실사용(임베드) 폰트 ⊆ tokens fonts 계약(stack + ps 별칭, 수식 폰트 allowlist) | FAIL |
| G3 | 본문 한 줄 자수가 스타일 밴드 내 (표지·목차 제외, 정렬 줄만) | WARN |

PASS 조건은 G1·G2 무위반. `gate-report.json`을 참조해 지적된 면만 수정 후 재빌드.

## 한계

- 인라인 `$...$` 중 한국어 \text + 복잡 매크로 혼재 시 일부 깨짐 → 블록 `$$` 권장
- 표·복잡 레이아웃은 typst 수동 작업 영역
- 폰트 폴백 경고: 빌드 머신에 스택 하위 폰트가 없다는 typst 경고는 폴백 설계상
  무해 — 단 임베드 폰트가 바뀌면 G2 ps 별칭 등록 필요

## 역사 노트 (레거시 수동 워크플로)

스타일 팩 도입 전에는 수동으로 빌드했다:

```bash
python3 scripts/md2typst.py <원고dir> --out build/typ
cp templates/book.typ build/
typst compile build/book.typ build/책.pdf --root build
```

`templates/book.typ`는 레거시로 유지되지만 신규 빌드는 `build.py`를 사용한다.

## 연계

- 입력: 정제 MD(`pdf-to-md` 또는 직접)
- 레거시: `korean-ebook`(WeasyPrint), `templates/book.typ`
