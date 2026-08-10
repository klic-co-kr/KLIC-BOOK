# korean_ebook_to_skill/chapters.py
import re
from pathlib import Path
from .models import Segment, ChapterFile

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
FILENAME_RE = re.compile(r"^(\d+)-(.+)\.md$")

def slugify(text: str) -> str:
    # NOTE: brief's regex `[\s:：·,，.]+` -> `-` dashes the period (2.2 -> 2-2),
    # but the intended/tested outcome is 2.2 -> 22 (period stripped, not dashed).
    # Period is therefore removed in a dedicated step; the dash class omits it.
    t = re.sub(r"[\s:：·,，]+", "-", text.strip())
    t = re.sub(r"\.", "", t)
    return re.sub(r"-+", "-", t).strip("-").lower()

def detect_chapters(text: str) -> list:
    ms = list(HEADING_RE.finditer(text)); segs = []
    for i, m in enumerate(ms):
        start = m.start()
        end = ms[i+1].start() if i+1 < len(ms) else len(text)
        segs.append(Segment(m.group(2).strip(), len(m.group(1)), start, end))
    return segs

def _kind_number(name: str) -> tuple[str, str | None]:
    m = FILENAME_RE.match(name)
    if not m: return "chapter", None
    num, rest = m.group(1), m.group(2)
    if rest.startswith("부록"):
        am = re.match(r"부록\s*([A-Za-z가-힣0-9])", rest)
        return "appendix", am.group(1) if am else None
    if rest.startswith("후기"): return "afterword", "후기"
    return "chapter", num

def parse_chapter_file(path) -> ChapterFile:
    p = Path(path); text = p.read_text(encoding="utf-8")
    kind, number = _kind_number(p.name)
    segs = detect_chapters(text)
    title = segs[0].title if segs else p.stem
    return ChapterFile(str(p), slugify(title), number, kind, text, segs)
