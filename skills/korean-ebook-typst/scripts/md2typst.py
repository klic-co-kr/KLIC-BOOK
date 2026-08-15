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
    # 0. 선두 YAML frontmatter 제거 — 표준 markdown 관행. 미제거 시
    # id/order/status 메타데이터가 본문 산문으로 인쇄된다(실전시스템설계 실측).
    # 파일 시작의 --- 쌍만 취급(파일 중간 ---는 수평선 등 다른 용법).
    md = re.sub(r'\A---[ \t]*\n.*?\n---[ \t]*\n', '', md, count=1, flags=re.S)
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
    # 4.5 HTML 주석 제거 — 그림 생산 메타데이터(<!-- figure-spec ... -->) 등.
    # 코드 스팬은 step 4에서 이미 보호되어 있다.
    md = re.sub(r'<!--.*?-->', '', md, flags=re.S)
    # 5. 인라인 수식 $...$ — \ / 알파벳 / ( 시작(숫자=화폐 제외), 한국어 \text 포함 허용
    md = re.sub(r'(?<!\\)(?<!\$)\$([\\A-Za-z(][^\$\n]{0,250})\$(?<!\\)(?!\$)',
                lambda m: f'#mitex[`{m.group(1).strip()}`]', md)
    # 새 #mitex 보호
    md = re.sub(r'#mitex\b[^\n]*', stash, md)
    # 6. 본문 typst 특수 이스케이프 (남은 $ 포함)
    md = md.replace('\\', r'\\').replace('#', r'\#').replace('[', r'\[').replace(']', r'\]')
    md = md.replace('$', r'\$').replace('<', r'\<').replace('>', r'\>').replace('@', r'\@')
    md = md.replace('*', r'\*').replace('_', r'\_')
    # 6.5 markdown 강조 (step 6에서 * → \* escape되므로 escape된 형태에 매치).
    # 미변환 시 **굵게**가 리터럴 별표로 인쇄된다(실전시스템설계 머리말 실측).
    # 굵게는 임시 마커(\x02)로 변환해 기울임 변환과 충돌하지 않게 한다.
    md = re.sub(r'\\\*\\\*(?=\S)([^\n]+?)(?<=\S)\\\*\\\*', '\x02\\1\x02', md)
    md = re.sub(r'(?<![\w\\])\\\*(?=\S)([^\\\n]+?)(?<=\S)\\\*(?!\*)', '_\\1_', md)
    md = md.replace('\x02', '*')
    # 7. 보호 복원
    md = re.sub(r'\x00(\d+)\x00', lambda m: protected[int(m.group(1))], md)
    # 8. 헤딩 (step 6에서 # → \# escape되므로 escape된 형태에 매치)
    md = re.sub(r'^\\#\\#\\#\\#\s+(.+)$', r'=== \1', md, flags=re.M)
    md = re.sub(r'^\\#\\#\\#\s+(.+)$', r'== \1', md, flags=re.M)
    md = re.sub(r'^\\#\\#\s+(.+)$', r'= \1', md, flags=re.M)
    md = re.sub(r'^\\#\s+(.+)$', r'= \1', md, flags=re.M)
    # 8.5 블록 인용 (step 6에서 > → \> escape되므로 escape된 형태에 매치)
    md = re.sub(r'^\\>\s?(.+)$', r'#quote[\1]', md, flags=re.M)
    # 8.7 헤딩 중간점(·) 뒤 줄바꿈 기회 — typst는 U+00B7을 break 기회로
    # 쓰지 않아 justify 헤딩에서 긴 라틴 ·연쇄 토큰이 프레임 밖으로 넘친다
    # (실전시스템설계 ch25 실측). 제로폭 공백(U+200B)을 심어 분량은 그대로
    # 두고 줄바꿈만 허용한다. 수식·코드가 섞인 헤딩은 보호 대상이라 제외.
    md = re.sub(r'^(=+ .+)$',
                lambda m: m.group(1).replace('·', '·​')
                if '#mitex' not in m.group(1) and '`' not in m.group(1)
                else m.group(1),
                md, flags=re.M)
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
