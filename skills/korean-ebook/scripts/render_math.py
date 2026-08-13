#!/usr/bin/env python3
"""render_math.py <md_file|dir> — $$...$$ LaTeX 수식 → SVG 이미지 치환.

WeasyPrint가 JS(KaTeX/MathJax)를 돌릴 수 없어, 빌드 전 MD의 $$...$$ 수식을
matplotlib mathtext로 SVG 렌더 → ![](svg) 로 치환. mathtext 미지원 수식(일부
매크로·정렬환경)은 원문 그대로 유지(빌드 시 $$ 텍스트로 나감).

사용: python3 render_math.py manuscript-ko/
"""
import re, sys, hashlib
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 한글 폰트(mathtext \text{한글} 렌더용)
_kr = [f for f in font_manager.fontManager.ttflist
       if 'Nanum' in f.name or 'Noto Sans KR' in f.name or 'Noto Sans CJK' in f.name]
if _kr:
    plt.rcParams['font.family'] = _kr[0].name

BLOCK = re.compile(r'\$\$(.+?)\$\$', re.S)
INLINE = re.compile(r'(?<!\$)\$([^\$\n]{3,})\$(?!\$)')


def render_one(latex: str, svg_path: Path) -> bool:
    try:
        fig = plt.figure(figsize=(0.01, 0.01))
        t = fig.text(0, 0, f'${latex}$', fontsize=11)
        fig.canvas.draw()
        bbox = t.get_window_extent()
        fig.set_size_inches(max(bbox.width / 72, 0.5), max(bbox.height / 72, 0.3))
        fig.savefig(str(svg_path), format='svg', transparent=True,
                    bbox_inches='tight', pad_inches=0.05)
        plt.close(fig)
        return True
    except Exception:
        plt.close('all')
        return False


def process(md_path: Path, svg_dir: Path) -> int:
    text = md_path.read_text(encoding='utf-8')
    changed = 0

    def repl(m):
        nonlocal changed
        latex = m.group(1).strip()
        h = hashlib.md5(latex.encode()).hexdigest()[:10]
        svg = svg_dir / f'eq-{h}.svg'
        if render_one(latex, svg):
            changed += 1
            rel = svg.relative_to(md_path.parent)
            return f'\n\n![수식]({rel})\n\n'
        return m.group(0)

    text = BLOCK.sub(repl, text)
    text = INLINE.sub(repl, text)
    md_path.write_text(text, encoding='utf-8')
    return changed


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: render_math.py <md_file|dir>")
    target = Path(sys.argv[1])
    targets = [target] if target.is_file() else sorted(target.glob('*.md'))
    total = 0
    for md in targets:
        svg_dir = md.parent / 'eq-svg'
        svg_dir.mkdir(exist_ok=True)
        n = process(md, svg_dir)
        if n:
            print(f'{md.name}: {n}개 수식 SVG 렌더')
            total += n
    print(f'총 {total}개 수식')


if __name__ == '__main__':
    main()
