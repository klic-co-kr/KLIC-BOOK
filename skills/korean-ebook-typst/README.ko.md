# korean-ebook-typst

## 정체성

Markdown 원고 → 출판형 A4 PDF. **typst 엔진** 기반. `korean-ebook`(WeasyPrint)의 한국어 자모 분리·수식 한계를 근본 해결.

- 한국어 CJK 네이티브(자모 분리 없음)
- 수식 `$$...$$`/`$...$` → typst mitex(LaTeX 호환) 고품정 렌더
- typst 조판(표지·목차·장표제·헤더·페이지번호)

## 설치

typst 바이너리 필요(PATH 또는 `~/.local/bin/typst`).
```bash
# typst 설치(바이너리)
curl -sL https://github.com/typst/typst/releases/latest/download/typst-x86_64-unknown-linux-musl.tar.xz | tar xJ
mv typst-x86_64-unknown-linux-musl/typst ~/.local/bin/
```
mitex 패키지는 첫 빌드 시 자동 다운로드(@preview/mitex:0.2.7).

## 사용

```bash
# 1. 원고 MD → typst 변환
python3 scripts/md2typst.py <원고dir> --out build/typ
# 2. 책 템플릿 복사(표지·목차·include)
cp templates/book.typ build/
cp <책>/assets/cover.png build/cover.png
# 3. typst 빌드
typst compile build/book.typ build/책.pdf --root build
```

`templates/book.typ`의 `#include "typ/day1.typ"` 부분을 책 챕터에 맞게 수정.

## md2typst 변환 규칙

- `## / ###` → `= / ==` (typst 헤딩)
- `![](path)` → `#figure(image("path"))`
- `$$...$$` / `$...$` 수식 → `#mitex[`...`]` (LaTeX 그대로, 한국어 \text 포함)
- 화폐 `$<숫자>/<단위>` → escape
- 본문 typst 특수(`# [ ] < > @ * _`) escape
- `##` markdown 잔재 escape

## 한계

- 인라인 `$...$` 중 한국어 \text + 복잡 매크로 혼재 시 일부 깨짐 가능 → 블록 `$$` 권장
- typst 자체 수식 문법 아닌 mitex(LaTeX 호환) 사용 — LaTeX 원고 그대로
- 표·복잡 레이아웃은 typst 수동 작업 영역

## 연계

- 입력: 정제 MD(`pdf-to-md` 또는 직접)
- 짝: `korean-ebook`(WeasyPrint, 레거시)
