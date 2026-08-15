#!/usr/bin/env python3
"""korean-ebook-typst 빌드 — typst-build.yaml → 스타일 팩 조립 → PDF."""
import shutil
import subprocess
import sys
from pathlib import Path
import yaml

SKILL_DIR = Path(__file__).resolve().parent.parent
STYLES = ("practical", "essay", "business", "lecture")

def _fail(msg: str) -> None:
    print(f"[build] 오류: {msg}", file=sys.stderr)
    raise SystemExit(1)

def load_config(path: Path) -> dict:
    if not path.exists():
        _fail(f"설정 파일 없음: {path}")
    cfg = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    for key in ("style", "title", "chapters"):
        if key not in cfg:
            _fail(f"필수 필드 누락: {key}")
    if cfg["style"] not in STYLES:
        _fail(f"알 수 없는 스타일: {cfg['style']} (허용: {', '.join(STYLES)})")
    if not isinstance(cfg["chapters"], list) or not cfg["chapters"]:
        _fail("chapters는 1개 이상의 파일 목록이어야 함")
    base = path.parent
    for ch in cfg["chapters"]:
        if not (base / ch).exists():
            _fail(f"챕터 파일 없음: {base / ch}")
    return {
        "style": cfg["style"],
        "title": cfg["title"],
        "subtitle": cfg.get("subtitle", ""),
        "author": cfg.get("author", ""),
        "date": cfg.get("date", ""),
        "chapters": list(cfg["chapters"]),
        "cover": cfg.get("cover"),
    }

MD2TYPST = SKILL_DIR / "scripts" / "md2typst.py"
STYLE_DIR = SKILL_DIR / "styles"

def assemble(cfg: dict, book_dir: Path) -> Path:
    """스타일 팩 + 변환된 챕터를 build/에 조립해 main.typ 생성."""
    build = book_dir / "build"
    (build / "typ").mkdir(parents=True, exist_ok=True)

    style = STYLE_DIR / cfg["style"]
    shutil.copy2(style / "tokens.json", build / "tokens.json")
    shutil.copy2(style / "theme.typ", build / "theme.typ")
    shutil.copy2(SKILL_DIR / "templates" / "base.typ", build / "base.typ")

    for ch in cfg["chapters"]:
        src = book_dir / ch
        r = subprocess.run(
            [sys.executable, str(MD2TYPST), str(src), "--out", str(build / "typ")],
            capture_output=True, text=True,
        )
        if r.returncode != 0:
            _fail(f"md2typst 실패 ({src}): {r.stderr.strip()}")
        if not (build / "typ" / (src.stem + ".typ")).exists():
            _fail(f"변환 결과 없음: {src.stem}.typ")

    typ_files = sorted((build / "typ").glob("*.typ"))
    # typst 0.15.1: set/show 규칙은 include 밖으로 전파되지 않으므로
    # 함수 템플릿을 #show: 로 적용(base 먼저, theme이 나중 — 헤딩 오버라이드).
    lines = [
        '#import "base.typ": base, make-cover, make-toc',
        '#import "theme.typ": theme',
        "#show: base",
        "#show: theme",
        '#include "base.typ"',
        '#include "theme.typ"',
        "",
    ]
    if cfg["cover"]:
        cover = f'#image("{cfg["cover"]}", width: 100%, height: 100%)'
        lines.append(f'#make-cover("{cfg["title"]}", "{cfg["subtitle"]}", '
                     f'"{cfg["author"]}", cover: [{cover}])')
    else:
        lines.append(f'#make-cover("{cfg["title"]}", "{cfg["subtitle"]}", '
                     f'"{cfg["author"]}", cover: none)')
    lines.append("#make-toc()")
    lines.append("")
    lines += [f'#include "typ/{p.name}"' for p in typ_files if p.name != "main.typ"]

    main = build / "main.typ"
    main.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return main

def compile_pdf(main: Path, out_name: str) -> Path:
    """main.typ → draft/<out_name>.pdf 컴파일."""
    draft = main.parent.parent / "draft"
    draft.mkdir(exist_ok=True)
    out = draft / f"{out_name}.pdf"
    r = subprocess.run(
        ["typst", "compile", str(main), str(out), "--root", str(main.parent)],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        _fail(f"typst compile 실패: {r.stderr.strip()}")
    return out

def main() -> None:
    if len(sys.argv) != 2:
        _fail("사용법: build.py <책디렉터리>")
    book_dir = Path(sys.argv[1]).resolve()
    cfg = load_config(book_dir / "typst-build.yaml")
    main_typ = assemble(cfg, book_dir)
    pdf = compile_pdf(main_typ, cfg["title"])
    print(f"[build] draft 산출: {pdf}")

if __name__ == "__main__":
    main()
