#!/usr/bin/env python3
"""korean-ebook-typst 빌드 — typst-build.yaml → 스타일 팩 조립 → PDF."""
import re
import shutil
import subprocess
import sys
from pathlib import Path
import yaml

SKILL_DIR = Path(__file__).resolve().parent.parent
STYLES = ("practical", "essay", "business", "lecture", "b5")
PAGE_MM = {"practical": (153, 225), "essay": (128, 188),
           "business": (200, 280), "lecture": (210, 297),
           "b5": (176, 250)}

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
    base = path.parent
    if not isinstance(cfg["chapters"], list) or not cfg["chapters"]:
        _fail("chapters는 1개 이상의 파일 목록이어야 함")
    for ch in cfg["chapters"]:
        if not (base / ch).exists():
            _fail(f"챕터 파일 없음: {base / ch}")
    style = cfg["style"]
    if style == "auto":
        # 원고 콘텐츠 밀도(표·수식·이미지·문단 길이)에서 판형 자동 판단.
        # 논문·도표형 → lecture(A4), 장문 산문 → essay(B6), 실용서 → practical.
        import style_pick
        style, why = style_pick.pick(base, list(cfg["chapters"]))
        print(f"[build] style: auto → {style} — {why}")
    elif style not in STYLES:
        _fail(f"알 수 없는 스타일: {cfg['style']} (허용: {', '.join(STYLES)}, auto)")
    return {
        "style": style,
        "title": cfg["title"],
        "subtitle": cfg.get("subtitle", ""),
        "author": cfg.get("author", ""),
        "date": cfg.get("date", ""),
        "chapters": list(cfg["chapters"]),
        "cover": cfg.get("cover"),
        "cover_series": cfg.get("cover_series", "KLIC BOOKS"),
        "cover_notes": cfg.get("cover_notes"),
    }

MD2TYPST = SKILL_DIR / "scripts" / "md2typst.py"
STYLE_DIR = SKILL_DIR / "styles"

IMAGE_RE = re.compile(r'#figure\(image\("([^"]+)"\)\)')

def _esc(s: str) -> str:
    """make-cover 문자열 리터럴용 이스케이프 — \·" 만 main.typ을 깨뜨린다."""
    return s.replace("\\", "\\\\").replace('"', '\\"')

def sanitize_filename(name: str) -> str:
    """PDF 파일명 sanitize — 경로 구분자 등 파일시스템 위험 문자 치환."""
    out = re.sub(r'[\\/:*?"<>|]', "_", name).strip()
    return out or "book"

def typst_binary() -> str:
    """typst 바이너리 해석 — PATH → ~/.local/bin/typst 폴백."""
    found = shutil.which("typst")
    if found:
        return found
    fallback = Path.home() / ".local" / "bin" / "typst"
    if fallback.exists():
        return str(fallback)
    _fail("typst 바이너리 없음 — PATH 등록 또는 ~/.local/bin/typst 설치")

def rebase_images(typ_file: Path, src_md: Path, build: Path, idx: int) -> None:
    """원고 이미지 경로를 build/ 루트로 재배치(복사 + 경로 재작성).

    원고 ![](path)는 md 파일 위치 기준 상대경로다. typst --root가
    build/라 변환 결과를 그대로 두면 root를 탈출해 컴파일이 실패한다.
    이미지를 build/assets/로 복사하고 typ/ 기준 상대경로로 다시 쓴다.
    챕터 인덱스 prefix로 네임스페이스화 — 동명 이미지(pic.png)가 챕터별로
    존재해도 덮어쓰지 않는다(2회차 검토 Important).
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
        dst = f"{idx:03d}-{src.name}"
        shutil.copy2(src, assets / dst)
        return f'#figure(image("../assets/{dst}"))'
    typ_file.write_text(IMAGE_RE.sub(rewrite, text), encoding="utf-8")

COVER_AUTO = """// 자동 표지 v3 — KLIC 자체 문법: 비대칭 좌측 정렬 + 두 겹치는 원(마음×마음)
// 모티프. 교훈만 채택(대형 타이포 스케일·락업 문법), 배치는 자체 설계.
#set page(width: {w}mm, height: {h}mm, margin: 0pt)
#set text(font: {font_stack}, lang: "ko")
#let paper = rgb("{paper}")
#let ink = rgb("{ink}")
#let brand = rgb("{brand}")
#let soft = rgb("{soft}")
#let mute = rgb("{mute}")
#let pale = rgb("{pale}")
#place(top + left, rect(width: 100%, height: 100%, fill: paper))
// 좌측 에지 수직 액센트 — 책등 은유
#place(left + top, dx: 0mm, dy: 0mm,
  rect(width: 6mm, height: 100%, fill: brand))
// 두 겹치는 원 — 디자이너의 마음 × 사용자의 마음(부제 은유), 우상단
#place(top + right, dx: -18mm, dy: {motif_y}mm)[
  #box(width: {motif}mm, height: {motif}mm)[
    #place(dx: 0mm, dy: {motif_off}mm,
      circle(radius: {motif_r}mm, stroke: 2.2pt + brand, fill: none))
    #place(dx: {motif_off}mm, dy: 0mm,
      circle(radius: {motif_r}mm, stroke: 2.2pt + pale, fill: none))
    #place(dx: {motiv_c}mm, dy: {motiv_c}mm,
      circle(radius: {motif_r}mm, fill: brand.transparentize(88%)))
  ]
]
// 시리즈 라벨 — 좌측 상단, 세로 액센트 옆
#place(top + left, dx: 20mm, dy: 18mm)[
  #text(size: 9pt, fill: mute, tracking: 3.2pt, weight: "semibold")[{series}]
]
// 주제목 — 좌측 하단부 비대칭 스택. 마지막 단어 brand색.
#place(bottom + left, dx: 26mm, dy: -{title_block_h}mm)[
  #align(left, stack(dir: ttb, spacing: 6mm,
    ..if "{head}" != "" {{ (
      align(left, text(size: {head_pt}pt, weight: "bold", fill: ink,
        tracking: -0.03em)[{head}]),) }} else {{ () }},
    align(left, text(size: {emph_pt}pt, weight: "bold", fill: brand,
      tracking: -0.03em)[{emph}])))
]
// 부제 — 주제목 위에 두는 역배치(비대칭 강조)
#place(bottom + left, dx: 26mm, dy: -{sub_dy}mm)[
  #box(width: {w}mm - 60mm)[
    #text(size: 12.5pt, fill: soft)[{subtitle}]
  ]
]
// 안내 노트 — 부제 위
{notes}
// 저자·발행 — 하단 한 줄, 좌우 분할(비대칭 마감)
#place(bottom + left, dx: 26mm, dy: -16mm)[
  #text(size: 10.5pt, fill: ink)[{author_bold} #text(fill: mute)[ 지음]]
]
#place(bottom + right, dx: -18mm, dy: -16mm)[
  #align(right)[
    #rect(width: 10mm, height: 0.8pt, fill: brand)
    #v(2mm, weak: true)
    #text(size: 8.5pt, weight: "semibold", fill: mute, tracking: 2pt)[{publisher}]
  ]
]
"""



def make_auto_cover(cfg: dict, build: Path) -> str:
    """표지 v3 — KLIC 자체 문법: 좌측 액센트 에지 + 두 겹치는 원 모티프 +
    비대칭 좌측 정렬 대형 타이포. pt 크기는 판폭 전각 자폭으로 피팅."""
    import json as _json
    w, h = PAGE_MM[cfg["style"]]
    tokens = _json.loads(
        (STYLE_DIR / cfg["style"] / "tokens.json").read_text(encoding="utf-8"))
    stack = tokens["fonts"]["body"]["stack"]
    font_stack = "(" + ", ".join(f'"{f}"' for f in stack) + ")"
    accent = tokens["colors"]["accent"].lstrip("#")
    rgb = tuple(int(accent[i:i + 2], 16) for i in (0, 2, 4))
    pale = "#" + "".join(f"{int(c + (255 - c) * 0.78):02X}" for c in rgb)

    words = cfg["title"].split(" ")
    emph_word = words[-1]
    head_word = " ".join(words[:-1])
    head_c = (len(head_word.replace(" ", ""))
              + head_word.count(" ") * 0.55)
    emph_c = len(emph_word)
    limit = w - 50  # 좌측 26mm + 우측 여백
    head_pt = min(72, limit / (0.353 * head_c)) if head_c else 72
    emph_pt = 1.5 * head_pt
    emph_max = limit / (0.353 * emph_c)
    if emph_pt > emph_max:
        k = emph_max / emph_pt
        head_pt, emph_pt = head_pt * k, emph_pt * k

    # 두 겹치는 원(마음×마음) — 우상단
    motif_r = min(26, w * 0.14)
    motif_off = motif_r * 0.62
    motif_box = motif_off + 2 * motif_r
    motif_y = h * 0.09
    tint_d = motif_r + motif_off / 2 - motif_r * 0.45

    # 하단에서부터: 저자 16mm ↑, 타이틀 블록 bottom 44mm, 부제는 그 위
    title_dy = 44
    block_h = (head_pt * 0.42 if head_word else 0) + 6 + emph_pt * 0.42
    sub_dy = title_dy + block_h + 10
    notes_dy = sub_dy + 16

    series = cfg.get("cover_series") or ""
    sub = _esc((cfg["subtitle"] or "").replace("\n", "#linebreak()"))
    if cfg["cover_notes"]:
        note_lines = ",\n    ".join(
            f'text(size: 10pt, fill: mute)[{_esc(str(x))}]'
            for x in cfg["cover_notes"])
        notes = (f'#place(bottom + left, dx: 26mm, dy: -{notes_dy:.0f}mm)[\n'
                 f'  #stack(spacing: 3mm,\n    {note_lines})\n]')
    else:
        notes = ""

    src = COVER_AUTO.format(
        w=w, h=h, font_stack=font_stack,
        paper="F7F4EE", ink=tokens["colors"]["ink"], brand=tokens["colors"]["accent"],
        soft=tokens["colors"]["ink-soft"], mute=tokens["colors"]["ink-mute"],
        pale=pale,
        motif_y=f"{motif_y:.0f}", motif_r=f"{motif_r:.1f}",
        motif_off=f"{motif_off:.1f}", motif=f"{motif_box:.1f}",
        motiv_c=f"{tint_d:.1f}",
        series=_esc(series.upper()), head=_esc(head_word),
        head_pt=f"{head_pt:.1f}", emph=_esc(emph_word),
        emph_pt=f"{emph_pt:.1f}",
        title_block_h=title_dy, sub_dy=f"{sub_dy:.0f}",
        subtitle=sub, notes=notes,
        author_bold=_esc(cfg["author"] or ""),
        publisher="KLIC BOOKS",
    )
    typ = build / "cover-auto.typ"
    typ.write_text(src, encoding="utf-8")
    png = build / "cover-auto.png"
    r = subprocess.run(
        [typst_binary(), "compile", str(typ), str(png),
         "--root", str(build), "--ppi", "150"],
        capture_output=True, text=True)
    if r.returncode != 0 or not png.exists():
        _fail(f"자동 표지 생성 실패: {r.stderr.strip()[:300]}")
    return png.name


def assemble(cfg: dict, book_dir: Path) -> Path:
    """스타일 팩 + 변환된 챕터를 build/에 조립해 main.typ 생성."""
    build = book_dir / "build"
    # 재빌드 시 삭제·개명된 챕터의 stale .typ이 include에 섞이지 않도록 리셋
    shutil.rmtree(build / "typ", ignore_errors=True)
    (build / "typ").mkdir(parents=True, exist_ok=True)
    # stale 에셋도 동일하게 리셋(2회차 검토 Important)
    shutil.rmtree(build / "assets", ignore_errors=True)

    style = STYLE_DIR / cfg["style"]
    shutil.copy2(style / "tokens.json", build / "tokens.json")
    shutil.copy2(style / "theme.typ", build / "theme.typ")
    shutil.copy2(SKILL_DIR / "templates" / "base.typ", build / "base.typ")

    # 표지: 명시 경로 > auto/생략(파라미터형 벡터 자동 생성)
    cover_name = None
    if cfg["cover"] and cfg["cover"] != "auto":
        cover_src = book_dir / cfg["cover"]
        if not cover_src.exists():
            _fail(f"표지 파일 없음: {cover_src}")
        cover_name = Path(cfg["cover"]).name
        shutil.copy2(cover_src, build / cover_name)
    else:
        cover_name = make_auto_cover(cfg, build)

    converted = []
    for idx, ch in enumerate(cfg["chapters"]):
        src = book_dir / ch
        r = subprocess.run(
            [sys.executable, str(MD2TYPST), str(src), "--out", str(build / "typ")],
            capture_output=True, text=True,
        )
        if r.returncode != 0:
            _fail(f"md2typst 실패 ({src}): {r.stderr.strip()}")
        raw = build / "typ" / (src.stem + ".typ")
        if not raw.exists():
            _fail(f"변환 결과 없음: {src.stem}.typ")
        # md2typst 출력명은 stem.typ이라 동명 챕터(*/00-part-introduction.md
        # 7개)가 서로 덮어써 유실됐다(2026-08-15 최종 리뷰 Critical 1).
        # 챕터 인덱스 prefix로 개명해 네임스페이스화 — md2typst 자체 불변.
        namespaced = build / "typ" / f"{idx:03d}-{src.stem}.typ"
        raw.rename(namespaced)
        rebase_images(namespaced, src, build, idx)
        converted.append(namespaced.name)

    # 콘텐츠 정합 불변식: 산출 파일 수 == 챕터 수, include 대상 중복 0.
    typs = list((build / "typ").glob("*.typ"))
    if len(typs) != len(cfg["chapters"]):
        _fail(f"변환 산출 {len(typs)}개 != 챕터 {len(cfg['chapters'])}개 — 덮어쓰기 의심")
    if len(set(converted)) != len(converted):
        _fail(f"include 대상 중복: {converted}")

    # typst 0.15.1: set/show 규칙은 include 밖으로 전파되지 않으므로
    # 함수 템플릿을 #show: 로 적용(base 먼저, theme이 나중 — 헤딩 오버라이드).
    lines = [
        '#import "base.typ": base, make-cover, make-toc',
        '#import "theme.typ": theme',
        "#show: base",
        "#show: theme",
        "",
    ]
    title, subtitle, author = (_esc(cfg[k]) for k in ("title", "subtitle", "author"))
    if cover_name:
        cover = f'#image("{cover_name}", width: 100%, height: 100%)'
        lines.append(f'#make-cover("{title}", "{subtitle}", '
                     f'"{author}", cover: [{cover}])')
    else:
        lines.append(f'#make-cover("{title}", "{subtitle}", '
                     f'"{author}", cover: none)')
    lines.append("#make-toc()")
    lines.append("")
    # 챕터 순서는 cfg["chapters"] 순서를 따른다(파일명 정렬 아님)
    lines += [f'#include "typ/{name}"' for name in converted]

    main = build / "main.typ"
    main.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return main

def compile_pdf(main: Path, out_name: str) -> Path:
    """main.typ → draft/<out_name>.pdf 컴파일."""
    draft = main.parent.parent / "draft"
    draft.mkdir(exist_ok=True)
    out = draft / f"{out_name}.pdf"
    r = subprocess.run(
        [typst_binary(), "compile", str(main), str(out), "--root", str(main.parent)],
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
    pdf = compile_pdf(main_typ, sanitize_filename(cfg["title"]))
    print(f"[build] draft 산출: {pdf}")

if __name__ == "__main__":
    main()
