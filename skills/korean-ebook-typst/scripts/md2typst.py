#!/usr/bin/env python3
"""md2typst.py <md_dir|md_file> --out <typ_dir> — Markdown → Typst 변환.

- ## / ### → = / == (typst 헤딩)
- ![](path) → #image("path")
- $$...$$ 블록 수식 → #mitex[`...`] (LaTeX 그대로, typst mitex 패키지)
- $...$ 인라인 수식 → #mitex[`...`]
- 그 외 본문 그대로
"""
import re, sys
from pathlib import Path

def convert(md: str) -> str:
    protected = []
    def stash(m):
        protected.append(m.group(0))
        return f"\x00{len(protected) - 1}\x00"
    # 1. 화폐 $<숫자>/<단위|통화> → escape
    md = re.sub(r'\$(\d[\d,.]*(?:\s*/\s*\w+|\s*(?:원|엔|달러|USD|시간)))',
                lambda m: r'\$' + m.group(1), md)
    # 2. 이미지
    md = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'#figure(image("\2"))', md)
    # 3. 블록 수식 $$...$$ → #mitex
    md = re.sub(r'\$\$(.+?)\$\$', lambda m: f'#mitex[`{m.group(1).strip()}`]',
                md, flags=re.S)
    # 4. typst 요소 보호 (인라인 변환 전)
    md = re.sub(r'#(?:figure|image|mitex|ref|link|page)\b[^\n]*', stash, md)
    md = re.sub(r'`[^`]*`', stash, md)
    # 5. 인라인 수식 $...$ — \ / 알파벳 / ( 시작(숫자=화폐 제외), 한국어 \text 포함 허용
    md = re.sub(r'(?<!\\)(?<!\$)\$([\\A-Za-z(][^\$\n]{0,250})\$(?<!\\)(?!\$)',
                lambda m: f'#mitex[`{m.group(1).strip()}`]', md)
    # 새 #mitex 보호
    md = re.sub(r'#mitex\b[^\n]*', stash, md)
    # 6. 본문 typst 특수 이스케이프 (남은 $ 포함)
    md = md.replace('\\', r'\\').replace('#', r'\#').replace('[', r'\[').replace(']', r'\]')
    md = md.replace('$', r'\$').replace('<', r'\<').replace('>', r'\>').replace('@', r'\@')
    md = md.replace('*', r'\*').replace('_', r'\_')
    # 7. 보호 복원
    md = re.sub(r'\x00(\d+)\x00', lambda m: protected[int(m.group(1))], md)
    # 8. 헤딩
    md = re.sub(r'^\\?####\s+(.+)$', r'=== \1', md, flags=re.M)
    md = re.sub(r'^\\?###\s+(.+)$', r'== \1', md, flags=re.M)
    md = re.sub(r'^\\?##\s+(.+)$', r'= \1', md, flags=re.M)
    md = re.sub(r'^\\?#\s+(.+)$', r'= \1', md, flags=re.M)
    # 9. 남은 비헤딩 ## (markdown 잔재) escape
    md = re.sub(r'(?<!\\)##(?=\w)', r'\#\#', md)
    return md


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    src = Path(a.input)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    targets = [src] if src.is_file() else sorted(src.glob('*.md'))
    for md in targets:
        t = convert(md.read_text(encoding='utf-8'))
        (out / (md.stem + '.typ')).write_text(
            '#import "@preview/mitex:0.2.7": mitex\n\n' + t, encoding='utf-8')
        print(f'{md.name} → {md.stem}.typ')


if __name__ == '__main__':
    main()
