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
    def stash_str(s: str) -> str:
        protected.append(s)
        return f"\x00{len(protected) - 1}\x00"
    def stash(m):
        return stash_str(m.group(0))
    # 0. 선두 YAML frontmatter 제거 — 표준 markdown 관행. 미제거 시
    # id/order/status 메타데이터가 본문 산문으로 인쇄된다(실전시스템설계 실측).
    # 파일 시작의 --- 쌍만 취급(파일 중간 ---는 수평선 등 다른 용법).
    md = re.sub(r'\A---[ \t]*\n.*?\n---[ \t]*\n', '', md, count=1, flags=re.S)
    # 0.5 코드펜스(```...```) 통째로 stash — typst도 ``` 를 raw block으로
    # 쓰므로 내용은 한 글자도 건드리지 않고 전달한다. 미보호 시 인라인
    # 코드스팬 regex(step 4)가 우연히 삼켜 "우발적 보호"되는데, 펜스 내부에
    # 백틱이 있으면 페어링이 어긋나 내용이 step 6 이스케이프에 오염된다
    # (system-design-notes ch16·22 SQL 블록 실측).
    md = re.sub(r'```.*?```', stash, md, flags=re.S)
    # 1. 화폐 $<숫자>/<단위|통화> → escape
    md = re.sub(r'\$(\d[\d,.]*(?:\s*/\s*\w+|\s*(?:원|엔|달러|USD|시간)))',
                lambda m: r'\$' + m.group(1), md)
    # 2. 이미지
    md = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'#figure(image("\2"))', md)
    # 2.5 md 파이프 표 → typst #table(). 미변환 시 | A | B | 가 리터럴
    # 파이프 문자로 인쇄된다(system-design-notes 표 148줄 실측).
    # 구분행(|---|---|)이 있는 블록만 표로 판정 — 본문의 홑파이프 줄은
    # 그대로 둔다. 셀 내부는 강조 변환 + typst 특수 escape를 여기서
    # 수행하고 결과를 stash해 step 6이 다시 건드리지 않게 한다.
    def _table_cell(c: str) -> str:
        c = c.replace('\\', r'\\').replace('#', r'\#').replace('[', r'\[').replace(']', r'\]')
        c = c.replace('$', r'\$').replace('<', r'\<').replace('>', r'\>').replace('@', r'\@')
        c = c.replace('_', r'\_')
        c = re.sub(r'\*\*(.+?)\*\*', '\x02\\1\x02', c)
        c = re.sub(r'(?<!\w)\*(?=\S)([^*]+?)(?<=\S)\*(?!\*)', '_\\1_', c)
        # 강조 변환 후 남은 홑 *(와일드카드 등)은 escape — [*]는 typst에서
        # 강조 마커 미닫음 컴파일 오류다(ch04 규칙 표 실측). \x02 마커
        # 복원 전에 수행해 변환된 굵게를 다시 escape하지 않는다.
        c = re.sub(r'(?<!\\)\*', r'\\*', c)
        return c.replace('\x02', '*')
    def _table_block(m):
        block = m.group(0)
        if not re.search(r'^\s*\|?[\s:|-]*-[\s:|-]*\|?\s*$', block, flags=re.M):
            return block  # 구분행 없음 — 표 아님
        rows = []
        for line in block.split('\n'):
            if not line.strip() or re.match(r'^\s*\|?[\s:|-]*-[\s:|-]*\|?\s*$', line):
                continue
            rows.append([c.strip() for c in line.strip().strip('|').split('|')])
        if not rows:
            return block
        ncols = max(len(r) for r in rows)
        cells = ', '.join(f'[{_table_cell(c)}]' for r in rows for c in r)
        return stash_str(f'#table(columns: {ncols}, {cells})')
    md = re.sub(r'(?:^[ \t]*\|.*\|[ \t]*$\n?)+', _table_block, md, flags=re.M)
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
