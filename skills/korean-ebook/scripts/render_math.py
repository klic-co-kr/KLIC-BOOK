#!/usr/bin/env python3
"""render_math.py <md_file|dir> — $$...$$ / $...$ LaTeX 수식 → PNG 이미지 치환 (typst+mitex).

matplotlib mathtext(한글·품질 한계) 대신 typst mitex 로 LaTeX 수식 고품정 렌더.
WeasyPrint 가 JS(KaTeX) 못 돌리는 한계 우회.

전제: typst 바이너리(PATH 또는 ~/.local/bin/typst), @preview/mitex:0.2.7(자동 다운).
"""
import re, sys, hashlib, subprocess, shutil
from pathlib import Path

BLOCK = re.compile(r'\$\$(.+?)\$\$', re.S)
INLINE = re.compile(r'(?<!\$)\$([^\$\n]{3,})\$(?!\$)')
TYPST = shutil.which('typst') or str(Path.home() / '.local/bin/typst')
MITEX = '0.2.7'


def deitalicize(latex: str) -> str:
    """수학 Unicode(U+1D400-1D7FF) 이탤릭/볼드 → 보통 라틴. mitex 호환."""
    out = []
    for c in latex:
        cp = ord(c)
        # 볼드 대문자 U+1D400-1D419 / 소문자 U+1D41A-1D433
        if 0x1D400 <= cp <= 0x1D419:
            out.append(chr(cp - 0x1D400 + 0x41))
        elif 0x1D41A <= cp <= 0x1D433:
            out.append(chr(cp - 0x1D41A + 0x61))
        # 이탤릭 대문자 U+1D434-1D44D / 소문자 U+1D44E-1D467
        elif 0x1D434 <= cp <= 0x1D44D:
            out.append(chr(cp - 0x1D434 + 0x41))
        elif 0x1D44E <= cp <= 0x1D467:
            out.append(chr(cp - 0x1D44E + 0x61))
        else:
            out.append(c)
    return ''.join(out)


def render_one(latex: str, png_path: Path, root: str) -> bool:
    latex = deitalicize(latex)
    src = (
        f'#import "@preview/mitex:{MITEX}": mitex\n'
        f'#set page(width: auto, height: auto, margin: 2pt)\n'
        f'#set text(size: 8.5pt, font: ("NanumSquare_ac", "Noto Sans CJK KR", "NanumGothic"))\n'
        f'#mitex(`{latex}`)\n'
    )
    typ_file = png_path.with_suffix('.typ')
    typ_file.write_text(src, encoding='utf-8')
    try:
        subprocess.run(
            [TYPST, 'compile', str(typ_file), str(png_path), '--root', root],
            capture_output=True, text=True, timeout=30)
    except Exception:
        pass
    finally:
        typ_file.unlink(missing_ok=True)
    return png_path.exists()


def process(md_path: Path, png_dir: Path) -> int:
    text = md_path.read_text(encoding='utf-8')
    root = str(md_path.parent)
    changed = 0

    def repl(m):
        nonlocal changed
        latex = m.group(1).strip()
        h = hashlib.md5(latex.encode()).hexdigest()[:10]
        png = png_dir / f'eq-{h}.png'
        if render_one(latex, png, root):
            changed += 1
            rel = png.relative_to(md_path.parent)
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
        png_dir = md.parent / 'eq-svg'   # 기존 디렉토리 재사용(png 아님 유지)
        png_dir.mkdir(exist_ok=True)
        n = process(md, png_dir)
        if n:
            print(f'{md.name}: {n}개 수식 typst 렌더')
            total += n
    print(f'총 {total}개 수식')


if __name__ == '__main__':
    main()
