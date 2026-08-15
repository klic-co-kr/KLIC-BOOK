#!/usr/bin/env python3
"""korean-ebook-typst 빌드 — typst-build.yaml → 스타일 팩 조립 → PDF."""
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
