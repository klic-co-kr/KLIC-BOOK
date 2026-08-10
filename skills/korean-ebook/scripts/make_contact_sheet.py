#!/usr/bin/env python3
"""Create one or more labeled contact sheets from rendered PDF pages."""

from __future__ import annotations

import argparse
import math
import re
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
except ImportError as exc:  # pragma: no cover
    print("Missing Pillow. Install scripts/requirements.txt", file=sys.stderr)
    raise SystemExit(2) from exc


def page_number(path: Path) -> int:
    match = re.search(r"(\d+)$", path.stem)
    return int(match.group(1)) if match else 0


def choose_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "C:/Windows/Fonts/malgun.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def output_path(base: Path, index: int, total: int) -> Path:
    if total == 1:
        return base
    return base.with_name(f"{base.stem}-{index:02d}{base.suffix}")


def build_sheet(files: list[Path], output: Path, columns: int, thumb_width: int, label_height: int, quality: int) -> None:
    font = choose_font(max(13, label_height - 8))
    gap = 16
    border = 1
    samples: list[tuple[Path, Image.Image]] = []
    thumb_height = 0
    for path in files:
        with Image.open(path) as source:
            image = source.convert("RGB")
            ratio = thumb_width / image.width
            resized = image.resize((thumb_width, max(1, round(image.height * ratio))), Image.Resampling.LANCZOS)
            thumb_height = max(thumb_height, resized.height)
            samples.append((path, resized))
    rows = math.ceil(len(samples) / columns)
    cell_width = thumb_width + gap * 2
    cell_height = thumb_height + label_height + gap * 2
    canvas = Image.new("RGB", (cell_width * columns, cell_height * rows), "#D9DEE1")
    draw = ImageDraw.Draw(canvas)
    for idx, (path, image) in enumerate(samples):
        row, col = divmod(idx, columns)
        x = col * cell_width + gap
        y = row * cell_height + gap + label_height
        framed = ImageOps.expand(image, border=border, fill="#AAB3B8")
        canvas.paste(framed, (x - border, y - border))
        label = f"PAGE {page_number(path):03d}"
        draw.text((x, row * cell_height + gap), label, fill="#25323B", font=font)
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.suffix.casefold() in {".jpg", ".jpeg"}:
        canvas.save(output, quality=quality, optimize=True)
    else:
        canvas.save(output)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--columns", type=int, default=4)
    parser.add_argument("--thumb-width", type=int, default=260)
    parser.add_argument("--pages-per-sheet", type=int, default=36)
    parser.add_argument("--quality", type=int, default=88)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    files = sorted(args.input_dir.resolve().glob("page-*.png"), key=page_number)
    if not files:
        print(f"No page PNGs found in {args.input_dir}", file=sys.stderr)
        return 2
    chunks = [files[i : i + args.pages_per_sheet] for i in range(0, len(files), args.pages_per_sheet)]
    outputs: list[Path] = []
    for idx, chunk in enumerate(chunks, start=1):
        target = output_path(args.output.resolve(), idx, len(chunks))
        build_sheet(chunk, target, max(1, args.columns), max(100, args.thumb_width), 30, args.quality)
        outputs.append(target)
    print(f"Created {len(outputs)} contact sheet(s):")
    for output in outputs:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
