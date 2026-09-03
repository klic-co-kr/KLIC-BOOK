#!/usr/bin/env python3
"""korean-ebook 빌드 — typst-build.yaml → 스타일 팩 조립 → PDF."""
import json as _json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
import yaml

SKILL_DIR = Path(__file__).resolve().parent.parent
# scripts/를 import 경로에 추가 — from infographic import render가 동작하는 조건.
# 기존 테스트가 scripts.build를 직접 import하는 컨텍스트에선 scripts/가
# sys.path에 없어 이 줄이 없으면 ModuleNotFoundError로 스위트 전체가 깨진다.
sys.path.insert(0, str(SKILL_DIR / "scripts"))
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
        "cover_variant": cfg.get("cover_variant"),
        "cover_composition": cfg.get("cover_composition"),
        "opener_composition": cfg.get("opener_composition"),
        "cover_series": cfg.get("cover_series", "KLIC BOOKS"),
        "cover_notes": cfg.get("cover_notes"),
        "cover_imprint": cfg.get("cover_imprint", "KLIC BOOKS"),
        "short_title": cfg.get("short_title"),
    }

MD2TYPST = SKILL_DIR / "scripts" / "md2typst.py"
STYLE_DIR = SKILL_DIR / "styles"

IMAGE_RE = re.compile(r'#figure\(image\("([^"]+)"\)(, caption: \[[^\n]*?\])?\)')

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

def _rasterize_svg(svg_path: Path) -> Path:
    """SVG → PNG(resvg, 4배 래스터화). 원본 svg는 지우고 png 경로 반환.

    SVG를 typst에 그대로 넘기면 내부 <text>의 폰트 해석이 typst 폰트
    스택을 타고 계약 외 폰트(NotoColorEmoji·NotoSansKR-Thin 등)를
    임베드해 G2가 깨진다(ai-agent-book-ko 이미지 133개 실측). resvg가
    fontconfig로 한 번 베이크하면 폰트 문제가 이미지 픽셀로 닫힌다.
    """
    import subprocess
    png_path = svg_path.with_suffix(".png")
    resvg = shutil.which("resvg")
    if not resvg:
        _fail("SVG 이미지가 있는데 resvg 없음 — cargo install resvg 후 재빌드")
    proc = subprocess.run(
        [resvg, "--zoom", "4", str(svg_path), str(png_path)],
        capture_output=True, text=True)
    if proc.returncode != 0 or not png_path.exists():
        _fail(f"resvg 래스터화 실패: {svg_path}\n{proc.stderr}")
    svg_path.unlink()
    return png_path


def rebase_images(typ_file: Path, src_md: Path, build: Path, idx: int) -> None:
    """원고 이미지 경로를 build/ 루트로 재배치(복사 + 경로 재작성).

    원고 ![](path)는 md 파일 위치 기준 상대경로다. typst --root가
    build/라 변환 결과를 그대로 두면 root를 탈출해 컴파일이 실패한다.
    이미지를 build/assets/로 복사하고 typ/ 기준 상대경로로 다시 쓴다.
    챕터 인덱스 prefix로 네임스페이스화 — 동명 이미지(pic.png)가 챕터별로
    존재해도 덮어쓰지 않는다(2회차 검토 Important). SVG는 PNG로 베이크.
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
        if src.suffix.lower() == ".svg":
            dst = _rasterize_svg(assets / dst).name
        # 캡션 절(md2typst alt 텍스트)은 재배치 뒤에도 보존한다
        return f'#figure(image("../assets/{dst}"){m.group(2) or ""})'
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
// 모티프 — 변조 프로파일(또는 기본 겹치는 원)
{motif_src}
// 시리즈 라벨 — 좌측 상단, 세로 액센트 옆
#place(top + left, dx: 20mm, dy: 18mm)[
  #text(size: 9pt, fill: mute, tracking: 3.2pt, weight: "semibold")[{series}]
]
// 주제목 — 좌측 하단부 비대칭 스택. 마지막 단어 brand색.
#place({title_side} + left, dx: 26mm, dy: {title_dy}mm)[
  #align(left, stack(dir: ttb, spacing: 6mm,
    ..if "{head}" != "" {{ (
      align(left, text(size: {head_pt}pt, weight: "bold", fill: ink,
        tracking: -0.03em)[{head}]),) }} else {{ () }},
    align(left, text(size: {emph_pt}pt, weight: "bold", fill: brand,
      tracking: -0.03em)[{emph}])))
]
// 부제 — 주제목 위에 두는 역배치(비대칭 강조)
#place({sub_side} + left, dx: 26mm, dy: {sub_dy}mm)[
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
{imprint}
"""




COVER_V2 = """// 자동 표지 변형2 — 이중 프레임 문고형: 얇은 이중 괘선 안 중앙 정렬
// 타이포. 코너 틱 + 상하 캡 라벨. 차분한 고전 문법.
#set page(width: {w}mm, height: {h}mm, margin: 0pt)
#set text(font: {font_stack}, lang: "ko")
#let paper = rgb("{paper}")
#let ink = rgb("{ink}")
#let brand = rgb("{brand}")
#let soft = rgb("{soft}")
#let mute = rgb("{mute}")
#place(top + left, rect(width: 100%, height: 100%, fill: paper))
// 이중 괘선 — 외괘 10mm 오프셋, 내괘 14mm
#place(top + left, dx: 10mm, dy: 10mm,
  rect(width: {w}mm - 20mm, height: {h}mm - 20mm, stroke: 1.1pt + ink))
#place(top + left, dx: 14mm, dy: 14mm,
  rect(width: {w}mm - 28mm, height: {h}mm - 28mm, stroke: 0.4pt + soft))
// 코너 틱 — 내괘 모서리에 브랜드 사각
#place(top + left, dx: 12.4mm, dy: 12.4mm, rect(width: 3.2mm, height: 3.2mm, fill: brand))
#place(top + right, dx: -12.4mm - 3.2mm, dy: 12.4mm, rect(width: 3.2mm, height: 3.2mm, fill: brand))
#place(bottom + left, dx: 12.4mm, dy: -12.4mm - 3.2mm, rect(width: 3.2mm, height: 3.2mm, fill: brand))
#place(bottom + right, dx: -12.4mm - 3.2mm, dy: -12.4mm - 3.2mm, rect(width: 3.2mm, height: 3.2mm, fill: brand))
// 상단 시리즈 — 괘선 안 중앙
#place(top + center, dy: 24mm)[
  #text(size: 9pt, fill: mute, tracking: 3pt, weight: "semibold")[{series}]
]
// 주제목 — 중앙 스택, 마지막 단어 brand색
#place(top + center, dy: {title_y}mm)[
  #align(center, stack(dir: ttb, spacing: 7mm,
    ..if "{head}" != "" {{ (
      align(center, text(size: {head_pt}pt, weight: "bold", fill: ink,
        tracking: -0.02em)[{head}]),) }} else {{ () }},
    align(center, text(size: {emph_pt}pt, weight: "bold", fill: brand,
      tracking: -0.02em)[{emph}])))
]
// 부제 — 이중 가는 괘선 사이
#place(top + center, dy: {sub_y}mm)[
  #align(center)[
    #box(width: 34mm, height: 0.4pt, fill: soft)
    #v(3.5mm, weak: true)
    #box(width: {w}mm - 64mm)[
      #align(center, text(size: 12pt, fill: soft)[{subtitle}])
    ]
    #v(3.5mm, weak: true)
    #box(width: 34mm, height: 0.4pt, fill: soft)
  ]
]
{notes}
// 저자·발행 — 하단 중앙 수직 스택
#place(bottom + center, dy: -22mm)[
  #align(center, stack(dir: ttb, spacing: 2.2mm,
    text(size: 10.5pt, fill: ink)[{author_bold} #text(fill: mute)[ 지음]]{imprint_items}))
]
"""

COVER_V3 = """// 자동 표지 변형3 — 수평 밴드형: 상단 브랜드 컬러 밴드에 타이틀,
// 밴드 우측 원 클러스터. 하부 지면은 노트·락업. 강한 대비 문법.
#set page(width: {w}mm, height: {h}mm, margin: 0pt)
#set text(font: {font_stack}, lang: "ko")
#let paper = rgb("{paper}")
#let ink = rgb("{ink}")
#let brand = rgb("{brand}")
#let soft = rgb("{soft}")
#let mute = rgb("{mute}")
#place(top + left, rect(width: 100%, height: 100%, fill: paper))
// 브랜드 밴드 — 상단에서 band_h 만큼
#place(top + left, rect(width: 100%, height: {band_h}mm, fill: brand))
// 밴드 내 원 클러스터(백색 스트로크, 마음 은유)
#place(top + right, dx: -14mm, dy: {cluster_y}mm)[
  #box(width: {cl}mm, height: {cl}mm)[
    #place(dx: 0mm, dy: {cl_off}mm, circle(radius: {cl_r}mm, stroke: 1.6pt + white.transparentize(35%), fill: none))
    #place(dx: {cl_off}mm, dy: 0mm, circle(radius: {cl_r}mm, stroke: 1.6pt + white.transparentize(35%), fill: none))
  ]
]
// 시리즈 — 밴드 안 좌측 상단
#place(top + left, dx: 24mm, dy: 14mm)[
  #text(size: 9pt, fill: white.transparentize(25%), tracking: 3pt, weight: "semibold")[{series}]
]
// 주제목 — 밴드 안 좌측 스택
#place(top + left, dx: 24mm, dy: {title_y}mm)[
  #align(left, stack(dir: ttb, spacing: 5mm,
    ..if "{head}" != "" {{ (
      align(left, text(size: {head_pt}pt, weight: "bold", fill: white.transparentize(8%),
        tracking: -0.03em)[{head}]),) }} else {{ () }},
    align(left, text(size: {emph_pt}pt, weight: "bold", fill: white,
      tracking: -0.03em)[{emph}])))
]
// 부제 — 밴드 바로 아래 지면에
#place(top + left, dx: 24mm, dy: {band_h}mm + 12mm)[
  #box(width: {w}mm - 56mm)[
    #text(size: 12.5pt, fill: soft)[{subtitle}]
  ]
]
{notes}
// 저자 좌·발행 우
#place(bottom + left, dx: 24mm, dy: -16mm)[
  #text(size: 10.5pt, fill: ink)[{author_bold} #text(fill: mute)[ 지음]]
]
{imprint}
"""


COVER_V4 = """// 자동 표지 변형4 — 엣지 포인트: 우상단 코너에서 멀어질수록 작아지는
// 하프톤 도트 필드. 인쇄 망점 문법, 결정적 수식 생성(난수 없음).
#set page(width: {w}mm, height: {h}mm, margin: 0pt)
#set text(font: {font_stack}, lang: "ko")
#let paper = rgb("{paper}")
#let ink = rgb("{ink}")
#let brand = rgb("{brand}")
#let soft = rgb("{soft}")
#let mute = rgb("{mute}")
#place(top + left, rect(width: 100%, height: 100%, fill: paper))
// 하프톤 도트 필드 — 우상단 코너 기준 거리 감쇠
#place(top + left, dx: 0mm, dy: 0mm)[
  #{{let step = {step}mm
    let cols = int({w}mm / step) + 2
    let rows = int({h}mm * {field} / step) + 2
    for i in range(cols) {{
      for j in range(rows) {{
        // 우상단 코너에서의 거리(mm 단위 실수)로 반지름 감쇠
        let fx = ({w}mm - i * step) / 1mm
        let fy = (j * step) / 1mm
        let d = calc.sqrt(fx * fx + fy * fy)
        let t = 1 - d / {reach}
        if t > 0.04 {{
          let r = {maxr}mm * calc.pow(t, 1.5)
          place(dx: i * step - r, dy: j * step - r,
            circle(radius: r, fill: brand.transparentize(30%)))
        }}
      }}
    }}}}
]
// 시리즈 — 좌측 상단
#place(top + left, dx: 26mm, dy: 18mm)[
  #text(size: 9pt, fill: mute, tracking: 3pt, weight: "semibold")[{series}]
]
// 주제목 — 좌측 수직 중앙 스택 + 도트 언더라인 + 부제(스택 내)
#place(top + left, dx: 26mm, dy: {title_y}mm)[
  #align(left, stack(dir: ttb, spacing: 7mm,
    ..if "{head}" != "" {{ (
      align(left, text(size: {head_pt}pt, weight: "bold", fill: ink,
        tracking: -0.03em)[{head}]),) }} else {{ () }},
    align(left, text(size: {emph_pt}pt, weight: "bold", fill: brand,
      tracking: -0.03em)[{emph}]),
    // 도트 언더라인 — 크기 감쇠 점 12개
    align(left, box(height: 3mm)[#{{for k in range(12) {{
      place(dx: k * {dstep}mm, circle(radius: (0.95mm - k * 0.06mm),
        fill: brand))
    }}}}]),
    // 부제 — 타이틀 스택 안(고정 dy 겹침 원천 차단, 설득의 구조 실측)
    align(left, box(width: {w}mm - 70mm)[
      #text(size: 12.5pt, fill: soft)[{subtitle}]])
  ))
]
// 부제 — 타이틀 스택 안(고정 dy 겹침 원천 차단, 설득의 구조 실측)
{notes}
// 저자 좌·발행 우
#place(bottom + left, dx: 26mm, dy: -16mm)[
  #text(size: 10.5pt, fill: ink)[{author_bold} #text(fill: mute)[ 지음]]
]
{imprint}
"""

COVER_V5 = """// 자동 표지 변형5 — 위계 격자형: 얇은 외곽 프레임 안에 대제목 판면과
// 점 격자 모티프. 상단은 열린 정보행(시리즈·연도), 하단은 마감 행으로
// 닫는다. 점 격자 배치는 제목 해시로 결정적(같은 책 = 같은 표지).
#set page(width: {w}mm, height: {h}mm, margin: 0pt)
#set text(font: {font_stack}, lang: "ko")
#let paper = rgb("{paper}")
#let ink = rgb("{ink}")
#let brand = rgb("{brand}")
#let soft = rgb("{soft}")
#let mute = rgb("{mute}")
#let pale = rgb("{pale}")
#place(top + left, rect(width: 100%, height: 100%, fill: paper))
// 외곽 프레임 — 9mm 오프셋 얇은 괘선, 격식의 테
#place(top + left, dx: 9mm, dy: 9mm,
  rect(width: {w}mm - 18mm, height: {h}mm - 18mm, stroke: 0.7pt + soft))
// 모티프 — 변조 프로파일(또는 기본 점 격자)
{motif_src}
// 상단 정보행 — 좌 시리즈 · 우 연도
#place(top + left, dx: 26mm, dy: 22mm)[
  #text(size: 9pt, fill: mute, tracking: 3.2pt, weight: "semibold")[{series}]
]
#place(top + right, dx: -26mm, dy: 22mm)[
  #text(size: 9pt, fill: mute, tracking: 2pt)[{year}]
]
// 좌측 모듈 축 — 시리즈와 노트 사이 여백을 지지하는 가는 기준선
// (0.7pt — 표지는 150ppi 래스터화되므로 그 이하 가는 선은 AA로 소멸)
#place(top + left, dx: 26mm, dy: 36mm,
  rect(width: 0.7pt, height: {axis_h}mm, fill: soft))
// 주제목 — 좌측 하단부 대형 스택. 마지막 단어 brand색.
#place({title_side} + left, dx: 26mm, dy: {title_dy}mm)[
  #align(left, stack(dir: ttb, spacing: 6mm,
    ..if "{head}" != "" {{ (
      align(left, text(size: {head_pt}pt, weight: "bold", fill: ink,
        tracking: -0.03em)[{head}]),) }} else {{ () }},
    align(left, text(size: {emph_pt}pt, weight: "bold", fill: brand,
      tracking: -0.03em)[{emph}])))
]
// 부제 — 제목 블록 위, 짧은 브랜드 룰과 함께
#place({sub_side} + left, dx: 26mm, dy: {sub_dy}mm)[
  #align(left)[
    #rect(width: 12mm, height: 1.2pt, fill: brand)
    #v(4mm, weak: true)
    #box(width: {w}mm - 60mm)[
      #text(size: 12.5pt, fill: soft)[{subtitle}]
    ]
  ]
]
// 안내 노트 — 부제 위
{notes}
// 저자 — 하단 좌측
#place(bottom + left, dx: 26mm, dy: -16mm)[
  #text(size: 10.5pt, fill: ink)[{author_bold} #text(fill: mute)[ 지음]]
]
{imprint}
"""


def make_auto_cover(cfg: dict, build: Path) -> str:
    """표지 자동 생성 — 3변형 문법에서 책마다 하나를 정해 재현 가능하게.

    변형 선택: cover_variant 지정이 우선, 없으면 제목 해시로 결정적 분포
    (같은 책 = 같은 표지, 책마다 달라짐).
      V1 비대칭 좌측(엣지 바·두 원·바텀 앵커)
      V2 이중 프레임 문고형(괘선·중앙 타이포·코너 틱)
      V3 수평 밴드형(브랜드 밴드 타이틀·원 클러스터)
      V4 엣지 포인트(우상단 하프톤 도트 필드·도트 언더라인)
      V5 위계 격자형(외곽 프레임·점 격자 모티프·대제목 하단 앵커)
    """
    import hashlib
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
    limit = w - 50
    head_pt = min(72, limit / (0.353 * head_c)) if head_c else 72
    emph_pt = 1.5 * head_pt
    emph_max = limit / (0.353 * emph_c)
    if emph_pt > emph_max:
        k = emph_max / emph_pt
        head_pt, emph_pt = head_pt * k, emph_pt * k
    # 행 높이 근사 0.42(캡 높이)는 실제 라인박스(어센더+디센더)보다 작아
    # 부제 고정 dy가 타이틀과 겹쳤다(설득의 구조 V4 실측). 0.55로 여유.
    block_h = (head_pt * 0.55 if head_word else 0) + 7 + emph_pt * 0.55
    # block_h는 pt 단위 — dy 체인은 mm이므로 환산해 더한다(적대검토:
    # 단위 혼합으로 sub_dy가 의도보다 +16mm 벌어졌다).
    block_h_mm = block_h * 0.3528

    def _anchor_layout(title_dy_bottom: float, block_mm: float):
        """앵커별 (타이틀 side·dy, 부제 side·dy, 노트 bottom dy).

        bottom = 현행 하단 앵커(부제·노트가 위로 쌓임). top/mid는 상단
        체인 — 노트는 하단 고정으로 남겨 지면 양끝을 잡는다. dy는
        side에 맞는 부호를 포함한다(bottom 음수, top 양수)."""
        if anchor == "bottom":
            tb = -(title_dy_bottom + block_mm + 12)
            return (("bottom", f"-{title_dy_bottom:.0f}"), ("bottom", f"{tb:.0f}"),
                    title_dy_bottom + block_mm + 28)
        if anchor == "top":
            return (("top", "30"), ("top", f"{30 + block_mm + 14:.0f}"),
                    max(60.0, title_dy_bottom + 20))
        t0 = max(30.0, (h - block_mm) / 2 - 20)
        return (("top", f"{t0:.0f}"), ("top", f"{t0 + block_mm + 14:.0f}"),
                max(60.0, title_dy_bottom + 20))

    variant = cfg.get("cover_variant")
    if variant not in (1, 2, 3, 4, 5, "1", "2", "3", "4", "5"):
        variant = int(hashlib.sha1(cfg["title"].encode()).hexdigest(), 16) % 4 + 1
    variant = int(variant)

    series = cfg.get("cover_series") or ""
    sub = _esc((cfg["subtitle"] or "").replace("\n", "#linebreak()"))
    author = _esc(cfg["author"] or "")
    # 발행 임프린트 — 기본 KLIC BOOKS. cover_imprint: ""로 숨긴다
    # (저작권 노출 우려 재제작 — 설득의 구조). 비면 우하단 락업 전체 생략.
    pub = _esc(str(cfg.get("cover_imprint", "KLIC BOOKS") or ""))
    imprint_r = ""
    if pub:
        imprint_r = (
            "#place(bottom + right, dx: -{dx}mm, dy: -16mm)[\n"
            "  #align(right)[\n"
            "    #rect(width: 10mm, height: 0.8pt, fill: brand)\n"
            "    #v(2mm, weak: true)\n"
            '    #text(size: 8.5pt, weight: "semibold", fill: mute,'
            f" tracking: 2pt)[{pub}]\n"
            "  ]\n]"
        )
    imprint_items = (
        ",\n    rect(width: 9mm, height: 0.8pt, fill: brand),\n"
        '    text(size: 8.5pt, weight: "semibold", fill: mute,'
        f" tracking: 2pt)[{pub}]"
    ) if pub else ""
    def _imprint(dx: int) -> str:
        return imprint_r.replace("{dx}", str(dx))
    base = dict(
        w=w, h=h, font_stack=font_stack, paper="F7F4EE",
        ink=tokens["colors"]["ink"], brand=tokens["colors"]["accent"],
        soft=tokens["colors"]["ink-soft"], mute=tokens["colors"]["ink-mute"],
        series=_esc(series.upper()), head=_esc(head_word),
        head_pt=f"{head_pt:.1f}", emph=_esc(emph_word),
        emph_pt=f"{emph_pt:.1f}", subtitle=sub,
        author_bold=author,
    )

    composition = bool(cfg.get("cover_composition"))
    profile = None
    anchor = "bottom"
    if composition:
        import cover_compositions as cc
        profile = cc.pick_profile(cfg["title"])
        anchor = profile[1]
        print(f"[build] 표지 구성 프로파일: {profile[0]} — "
              f"{profile[1]} 앵커 · {profile[2]} 모티프 · 밀도 {profile[3]:.2f}")
        if variant in (2, 3):
            print("[build] 경고: 표지 변형 V2/V3는 구성 프로파일(모티프·앵커)을"
                  " 반영하지 않는다 — 오프너만 변조된다. V5 권장.")

    if variant == 1:
        motif_r = min(26, w * 0.14)
        motif_off = motif_r * 0.62
        tint_d = motif_r + motif_off / 2 - motif_r * 0.45
        (t_side, t_dy), (s_side, s_dy), notes_dy = _anchor_layout(44, block_h_mm)
        if cfg["cover_notes"]:
            lines = ",\n    ".join(
                f'text(size: 10pt, fill: mute)[{_esc(str(x))}]'
                for x in cfg["cover_notes"])
            notes = (f'#place(bottom + left, dx: 26mm, dy: -{notes_dy:.0f}mm)[\n'
                     f'  #stack(spacing: 3mm,\n    {lines})\n]')
        else:
            notes = ""
        if composition:
            motif_src = cc.motif_block(
                profile, variant=1, w=w, h=h, brand=accent, pale=pale.lstrip("#"))
        else:
            motif_src = (
                f'#place(top + right, dx: -18mm, dy: {h * 0.09:.0f}mm)[\n'
                f'  #box(width: {motif_off + 2 * motif_r:.1f}mm, '
                f'height: {motif_off + 2 * motif_r:.1f}mm)[\n'
                f'    #place(dx: 0mm, dy: {motif_off:.1f}mm,\n'
                f'      circle(radius: {motif_r:.1f}mm, stroke: 2.2pt + brand, fill: none))\n'
                f'    #place(dx: {motif_off:.1f}mm, dy: 0mm,\n'
                f'      circle(radius: {motif_r:.1f}mm, stroke: 2.2pt + pale, fill: none))\n'
                f'    #place(dx: {tint_d:.1f}mm, dy: {tint_d:.1f}mm,\n'
                f'      circle(radius: {motif_r:.1f}mm, fill: brand.transparentize(88%)))\n'
                f'  ]\n]')
        base.update(
            pale=pale, motif_src=motif_src,
            title_side=t_side, title_dy=t_dy, sub_side=s_side, sub_dy=s_dy,
            notes=notes, imprint=_imprint(18))
        template = COVER_AUTO
    elif variant == 2:
        title_y = h * 0.30
        sub_y = title_y + block_h + 16
        if cfg["cover_notes"]:
            lines = ",\n    ".join(
                f'text(size: 10pt, fill: mute)[{_esc(str(x))}]'
                for x in cfg["cover_notes"])
            notes = (f'#place(bottom + center, dy: -52mm)[\n'
                     f'  #align(center, stack(spacing: 3mm, {lines}))\n]')
        else:
            notes = ""
        base.update(title_y=f"{title_y:.0f}", sub_y=f"{sub_y:.0f}", notes=notes,
                     imprint_items=imprint_items)
        template = COVER_V2
    elif variant == 3:
        band_h = h * 0.34
        cl_r = min(20, w * 0.10)
        cl_off = cl_r * 0.6
        cl = cl_off + 2 * cl_r
        if cfg["cover_notes"]:
            lines = ",\n    ".join(
                f'text(size: 10pt, fill: mute)[{_esc(str(x))}]'
                for x in cfg["cover_notes"])
            notes = (f'#place(bottom + left, dx: 24mm, dy: -44mm)[\n'
                     f'  #stack(spacing: 3mm,\n    {lines})\n]')
        else:
            notes = ""
        base.update(
            band_h=f"{band_h:.0f}", cluster_y=f"{band_h - cl - 12:.0f}",
            cl=f"{cl:.1f}", cl_off=f"{cl_off:.1f}", cl_r=f"{cl_r:.1f}",
            title_y=30, notes=notes, imprint=_imprint(16))
        template = COVER_V3
    elif variant == 4:
        title_y = h * 0.34
        sub_y = title_y + block_h + 12
        if cfg["cover_notes"]:
            lines = ",\n    ".join(
                f'text(size: 10pt, fill: mute)[{_esc(str(x))}]'
                for x in cfg["cover_notes"])
            notes = (f'#place(bottom + left, dx: 26mm, dy: -44mm)[\n'
                     f'  #stack(spacing: 3mm,\n    {lines})\n]')
        else:
            notes = ""
        if composition:
            # 프로파일 밀도·피치 → 도트 필드 규모
            base.update(
                step=max(4, round(7 * profile[5])),
                field=min(0.9, 0.35 + profile[3] * 0.5),
                reach=f"{w * 0.92:.0f}",
                maxr=round(2.0 + profile[3] * 2.0, 1),
                dstep=f"{4.6 * profile[5]:.1f}", title_y=f"{title_y:.0f}",
                sub_y=f"{sub_y:.0f}", notes=notes,
                imprint=_imprint(18))
        else:
            base.update(
                step=7, field=0.62, reach=f"{w * 0.92:.0f}", maxr=3.2,
                dstep="4.6", title_y=f"{title_y:.0f}",
                sub_y=f"{sub_y:.0f}", notes=notes,
                imprint=_imprint(18))
        template = COVER_V4
    elif variant == 5:
        # 위계 격자형 제목 스케일 — 대제목 판문법의 0.7배(프레임·정보행과
        # 균형). 블록 높이도 축소 치수로 재계산해 부제·노트 간격 유지.
        head5 = head_pt * 0.7
        emph5 = emph_pt * 0.7
        block5 = (head5 * 0.55 if head_word else 0) + 7 + emph5 * 0.55
        block5_mm = block5 * 0.3528
        (t_side, t_dy), (s_side, s_dy), notes_dy = _anchor_layout(46, block5_mm)
        if cfg["cover_notes"]:
            lines = ",\n    ".join(
                f'text(size: 10.5pt, fill: soft)[{_esc(str(x))}]'
                for x in cfg["cover_notes"])
            notes = (f'#place(bottom + left, dx: 26mm, dy: -{notes_dy:.0f}mm)[\n'
                     f'  #stack(spacing: 3.5mm,\n    {lines})\n]')
        else:
            notes = ""
        if composition:
            motif_src = cc.motif_block(
                profile, variant=5, w=w, h=h, brand=accent, pale=pale.lstrip("#"))
        else:
            import random as _random
            # 점 격자 — 제목 해시 시드. 같은 책은 같은 배치, 책마다 고유.
            rng = _random.Random(
                "cover-grid:" + hashlib.sha1(cfg["title"].encode()).hexdigest())
            dg_cols, dg_rows, dg_pitch = 6, 8, 4.2
            dots = []
            for r_ in range(dg_rows):
                for c_ in range(dg_cols):
                    u = rng.random()
                    if u < 0.30:
                        dots.append(f'    #place(dx: {c_ * dg_pitch:.1f}mm, '
                                    f'dy: {r_ * dg_pitch:.1f}mm, '
                                    f'circle(radius: 0.75mm, fill: brand))')
                    elif u < 0.58:
                        dots.append(f'    #place(dx: {c_ * dg_pitch:.1f}mm, '
                                    f'dy: {r_ * dg_pitch:.1f}mm, '
                                    f'circle(radius: 0.5mm, fill: pale))')
            dotgrid = "\n".join(dots)
            motif_src = (
                '#place(top + right, dx: -30mm, dy: 36mm)[\n'
                f'  #box(width: {dg_cols * dg_pitch:.1f}mm, '
                f'height: {dg_rows * dg_pitch:.1f}mm)[\n'
                f'{dotgrid}\n  ]\n]')
        base.update(
            pale=pale, motif_src=motif_src,
            head_pt=f"{head5:.1f}", emph_pt=f"{emph5:.1f}",
            axis_h=f"{h * 0.28:.0f}",
            year=_esc(str(cfg.get("date", ""))[:4]),
            title_side=t_side, title_dy=t_dy, sub_side=s_side, sub_dy=s_dy,
            notes=notes, imprint=_imprint(26))
        template = COVER_V5

    src = template.format(**base)
    typ = build / "cover-auto.typ"
    typ.write_text(src, encoding="utf-8")
    png = build / "cover-auto.png"
    r = subprocess.run(
        [typst_binary(), "compile", str(typ), str(png),
         "--root", str(build), "--ppi", "150"],
        capture_output=True, text=True)
    if r.returncode != 0 or not png.exists():
        _fail(f"자동 표지 생성 실패: {r.stderr.strip()[:300]}")
    _pinned = str(cfg.get("cover_variant", "")).strip() in ("1", "2", "3", "4", "5")
    print(f"[build] 표지 변형 V{variant} ({'지정' if _pinned else '제목 해시 결정적'})")
    return png.name


def _expand_diagrams(src: Path, idx: int) -> tuple[Path, Path | None]:
    """챕터 md의 ```diagram 펜스를 SVG 에셋 + 이미지 마크다운으로 펼친다.

    원고 파일은 불변 — 확장판을 같은 디렉터리의 임시 파일(점두어)로 쓰고
    변환 뒤 지운다. 같은 디렉터리여야 이미지 상대경로 해석(rebase_images
    의 src_md.parent 기준)이 원문과 일치한다. 반환 (변환입력, 임시파일).
    """
    import diagram as dg
    text = src.read_text(encoding="utf-8")
    if not dg.FENCE_RE.search(text):
        return src, None
    out_dir = src.parent.parent / "assets" / "diagrams"
    out_dir.mkdir(parents=True, exist_ok=True)
    counter = [0]

    def repl(m):
        fence = _json.loads(m.group(1))
        counter[0] += 1
        svg = out_dir / f"{idx:03d}-{src.stem}-dg{counter[0]:02d}.svg"
        try:
            svg.write_text(dg.render_fence(fence), encoding="utf-8")
        except ValueError as exc:
            _fail(f"diagram 펜스 위반 ({src.name} #{counter[0]}): {exc}")
        cap = fence.get("caption") or fence["title"]
        rel = os.path.relpath(svg, src.parent).replace(os.sep, "/")
        return f"![{cap}]({rel})"

    expanded = dg.FENCE_RE.sub(repl, text)
    tmp = src.parent / f".tmp-diag-{idx:03d}-{src.stem}.md"
    tmp.write_text(expanded, encoding="utf-8")
    return tmp, tmp


def assemble(cfg: dict, book_dir: Path) -> Path:
    """스타일 팩 + 변환된 챕터를 build/에 조립해 main.typ 생성."""
    build = book_dir / "build"
    # 재빌드 시 삭제·개명된 챕터의 stale .typ이 include에 섞이지 않도록 리셋
    shutil.rmtree(build / "typ", ignore_errors=True)
    (build / "typ").mkdir(parents=True, exist_ok=True)
    # stale 에셋도 동일하게 리셋(2회차 검토 Important)
    shutil.rmtree(build / "assets", ignore_errors=True)
    shutil.rmtree(build / "infographic", ignore_errors=True)
    (build / "infographic").mkdir(parents=True, exist_ok=True)
    shutil.rmtree(build / "fences", ignore_errors=True)
    (build / "fences").mkdir(parents=True, exist_ok=True)
    # diagram 펜스 에셋도 빌드마다 재생성 — 삭제된 펜스의 잔여 SVG 방지
    shutil.rmtree(book_dir / "assets" / "diagrams", ignore_errors=True)

    style = STYLE_DIR / cfg["style"]
    # tokens에 책 메타 주입 — base.typ 러닝헤드 좌측 단축제목이 읽는다.
    # short는 config.short_title > 제목 첫 어절(구판 book.short_title 규칙).
    tk = _json.loads((style / "tokens.json").read_text(encoding="utf-8"))
    short = str(cfg.get("short_title") or " ".join(str(cfg["title"]).split()[:1])
                or "BOOK")
    tk["book"] = {"short": short[:20], "title": str(cfg["title"])}
    (build / "tokens.json").write_text(
        _json.dumps(tk, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    shutil.copy2(style / "theme.typ", build / "theme.typ")
    shutil.copy2(SKILL_DIR / "templates" / "base.typ", build / "base.typ")
    # raw 테마 — set raw(theme:)은 파일 경로만 받는다(bytes 무시 실측).
    shutil.copy2(SKILL_DIR / "templates" / "klic-flat-dark.tmTheme",
                 build / "klic-flat-dark.tmTheme")
    shutil.copy2(SKILL_DIR / "templates" / "infographic" / "helper.typ", build / "helper.typ")

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
        conv_src, tmp_diag = _expand_diagrams(src, idx)
        try:
            r = subprocess.run(
                [sys.executable, str(MD2TYPST), str(conv_src), "--out", str(build / "typ"),
                 "--fences-out", str(build / "fences")],
                capture_output=True, text=True,
            )
            if r.returncode != 0:
                _fail(f"md2typst 실패 ({src}): {r.stderr.strip()}")
            raw = build / "typ" / (conv_src.stem + ".typ")
            if not raw.exists():
                _fail(f"변환 결과 없음: {conv_src.stem}.typ")
            # md2typst 출력명은 stem.typ이라 동명 챕터(*/00-part-introduction.md
            # 7개)가 서로 덮어써 유실됐다(2026-08-15 최종 리뷰 Critical 1).
            # 챕터 인덱스 prefix로 개명해 네임스페이스화 — md2typst 자체 불변.
            namespaced = build / "typ" / f"{idx:03d}-{src.stem}.typ"
            raw.rename(namespaced)
            rebase_images(namespaced, src, build, idx)
            converted.append(namespaced.name)
        finally:
            if tmp_diag is not None:
                tmp_diag.unlink(missing_ok=True)

    # 인포그래픽: 펜스 → emit + include 치환(스펙 §2 [2])
    from infographic import render as ig_render
    try:
        figs = ig_render.render_book_fences(book_dir, build, cfg)
    except ig_render.I1Error as exc:
        _fail(str(exc))
    for idx, name in enumerate(converted):
        p = build / "typ" / name
        text = p.read_text(encoding="utf-8")
        def _sub(m):
            n = int(m.group(1))
            fname = figs.get(idx, {}).get(n)
            if not fname:
                _fail(f"{name}: 펜스 #{n} emit 결과 없음(마커 ⟦IG:{n}⟧)")
            return f'#include "../infographic/{fname}"'
        text = re.sub(r"⟦IG:(\d+)⟧", _sub, text)
        p.write_text(text, encoding="utf-8")

    # 콘텐츠 정합 불변식: 산출 파일 수 == 챕터 수, include 대상 중복 0.
    typs = list((build / "typ").glob("*.typ"))
    if len(typs) != len(cfg["chapters"]):
        _fail(f"변환 산출 {len(typs)}개 != 챕터 {len(cfg['chapters'])}개 — 덮어쓰기 의심")
    if len(set(converted)) != len(converted):
        _fail(f"include 대상 중복: {converted}")

    # 장 오프너 변조 — base.typ가 build/openers.typ을 import한다(코드 문자열은
    # json 경로로는 텍스트로 인쇄될 뿐 평가되지 않으므로 typst 모듈로 내놓는다).
    # opt-out이면 enabled: false — 현행 네이비 오프너 그대로.
    # 오프너 변조는 opener_composition 키가 우선, 미지정 시 표지 키를
    # 따른다(적대검토 — 표지 키 하나로 본문까지 지배하던 결합 분리).
    # 이전 설계 잔존물(composition.json)은 매 조립 때 정리한다.
    (build / "composition.json").unlink(missing_ok=True)
    # None 결정판: load_config가 미지정 키를 None으로 싣으므로
    # dict.get 기본값은 작동하지 않는다 — None일 때 표지 키를 밟는다.
    _opener_on = (cfg.get("opener_composition")
                  if cfg.get("opener_composition") is not None
                  else cfg.get("cover_composition"))
    if _opener_on:
        import cover_compositions as cc
        toks = _json.loads(
            (STYLE_DIR / cfg["style"] / "tokens.json").read_text(encoding="utf-8"))
        acc = toks["colors"]["accent"].lstrip("#")
        rgbv = tuple(int(acc[i:i + 2], 16) for i in (0, 2, 4))
        pale_h = "".join(f"{int(c + (255 - c) * 0.78):02X}" for c in rgbv)
        prof = cc.pick_profile(cfg["title"])
        frags = [cc.opener_strip(prof, i, brand=acc, pale=pale_h)
                 for i in range(len(cfg["chapters"]))]
        opener_typ = (
            '#let opener-enabled = true\n'
            '#let opener-paper = rgb("F7F4EE")\n'
            f'#let opener-brand = rgb("{acc}")\n'
            '#let openers = (\n  ' + ',\n  '.join(frags) + ',\n)\n')
    else:
        opener_typ = ('#let opener-enabled = false\n'
                      '#let opener-paper = none\n'
                      '#let opener-brand = none\n'
                      '#let openers = ()\n')
    (build / "openers.typ").write_text(opener_typ, encoding="utf-8")

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
