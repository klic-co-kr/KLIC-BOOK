---
name: korean-ebook-typst
description: "Markdown 원고를 한국어 출판형 A4 PDF로 빌드. typst 엔진(한국어 CJK + 수식 mitex 네이티브). korean-ebook(WeasyPrint)의 한국어 자모 분리·수식 한계 근본 해결. 슬라이드/강의 자료 원고도 책 품질로 재구성 가능."
---

# korean-ebook-typst

## 정체성

MD → A4 PDF. **typst 엔진**. 한국어 CJK + 수식(LaTeX mitex) 네이티브. `korean-ebook`(WeasyPrint) 대체.

## 워크플로우

```bash
# 1. MD → typst 변환
python3 scripts/md2typst.py <원고dir> --out build/typ
# 2. 템플릿·표지 배치
cp templates/book.typ build/ && cp <책>/assets/cover.png build/cover.png
# 3. book.typ 의 include 목록을 책 챕터에 맞게 수정
# 4. 빌드
typst compile build/book.tex build/<책>.pdf --root build
```

## 변환 규칙 (md2typst)

- `##/###` → `=/==` 헤딩
- `![](img)` → `#figure(image("img"))`
- `$$...$$`/`$...$` → `#mitex[`...`]` (LaTeX 그대로)
- 화폐 `$<숫자>/<단위>` escape
- 본문 typst 특수 escape
- `##` markdown 잔재 escape

## 의존성

- typst 바이너리(PATH / ~/.local/bin/typst)
- @preview/mitex:0.2.7(자동 다운)

## 한계

- 인라인 `$...$` 한국어 \text + 복잡 매크로 혼재 시 일부 깨짐 → `$$` 권장
- 표·복잡 레이아웃은 typst 수동 작업

## 연계

- 입력: 정제 MD(`pdf-to-md` 또는 직접)
- 레거시: `korean-ebook`(WeasyPrint)
