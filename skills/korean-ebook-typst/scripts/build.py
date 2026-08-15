#!/usr/bin/env python3
"""korean-ebook-typst 빌드 — typst-build.yaml → 스타일 팩 조립 → PDF."""
import re
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

IMAGE_RE = re.compile(r'#figure\(image\("([^"]+)"\)\)')

def rebase_images(typ_file: Path, src_md: Path, build: Path) -> None:
    """원고 이미지 경로를 build/ 루트로 재배치(복사 + 경로 재작성).

    원고 ![](path)는 md 파일 위치 기준 상대경로다. typst --root가
    build/라 변환 결과를 그대로 두면 root를 탈출해 컴파일이 실패한다.
    이미지를 build/assets/로 복사하고 typ/ 기준 상대경로로 다시 쓴다.
    """
    text = typ_file.read_text(encoding="utf-8")
    if not IMAGE_RE.search(text):
        return
    def rewrite(m):
        rel = m.group(1)
        if re.match(r"[a-z]+://", rel) or rel.startswith("/"):
            return m.group(0)  # URL·절대경로는 그대로
        src = (src_md.parent / rel).resolve()
        if not src.exists():
            _fail(f"이미지 파일 없음: {src}")
        assets = build / "assets"
        assets.mkdir(exist_ok=True)
        shutil.copy2(src, assets / src.name)
        return f'#figure(image("../assets/{src.name}"))'
    typ_file.write_text(IMAGE_RE.sub(rewrite, text), encoding="utf-8")

def assemble(cfg: dict, book_dir: Path) -> Path:
    """스타일 팩 + 변환된 챕터를 build/에 조립해 main.typ 생성."""
    build = book_dir / "build"
    # 재빌드 시 삭제·개명된 챕터의 stale .typ이 include에 섞이지 않도록 리셋
    shutil.rmtree(build / "typ", ignore_errors=True)
    (build / "typ").mkdir(parents=True, exist_ok=True)

    style = STYLE_DIR / cfg["style"]
    shutil.copy2(style / "tokens.json", build / "tokens.json")
    shutil.copy2(style / "theme.typ", build / "theme.typ")
    shutil.copy2(SKILL_DIR / "templates" / "base.typ", build / "base.typ")

    # 표지: typst --root가 build/이므로 build/로 복사 후 파일명만 삽입
    cover_name = None
    if cfg["cover"]:
        cover_src = book_dir / cfg["cover"]
        if not cover_src.exists():
            _fail(f"표지 파일 없음: {cover_src}")
        cover_name = Path(cfg["cover"]).name
        shutil.copy2(cover_src, build / cover_name)

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
        rebase_images(build / "typ" / (src.stem + ".typ"), src, build)

    # typst 0.15.1: set/show 규칙은 include 밖으로 전파되지 않으므로
    # 함수 템플릿을 #show: 로 적용(base 먼저, theme이 나중 — 헤딩 오버라이드).
    lines = [
        '#import "base.typ": base, make-cover, make-toc',
        '#import "theme.typ": theme',
        "#show: base",
        "#show: theme",
        "",
    ]
    if cover_name:
        cover = f'#image("{cover_name}", width: 100%, height: 100%)'
        lines.append(f'#make-cover("{cfg["title"]}", "{cfg["subtitle"]}", '
                     f'"{cfg["author"]}", cover: [{cover}])')
    else:
        lines.append(f'#make-cover("{cfg["title"]}", "{cfg["subtitle"]}", '
                     f'"{cfg["author"]}", cover: none)')
    lines.append("#make-toc()")
    lines.append("")
    # 챕터 순서는 cfg["chapters"] 순서를 따른다(파일명 정렬 아님)
    lines += [f'#include "typ/{Path(ch).stem}.typ"' for ch in cfg["chapters"]]

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
