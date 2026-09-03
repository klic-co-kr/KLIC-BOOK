# korean_ebook_to_skill/models.py
from dataclasses import dataclass
from enum import Enum

class ContentType(Enum):
    PROSE = "prose"; INDEX = "index"; ROSTER = "roster"
    ANTHOLOGY = "anthology"; AFTERWORD = "afterword"
    GLOSSARY = "glossary"; UNKNOWN = "unknown"

@dataclass
class Segment:
    title: str; level: int; start: int; end: int

@dataclass
class ChapterFile:
    path: str; slug: str; number: str | None; kind: str
    raw_text: str; segments: list
    content_type: "ContentType | None" = None

@dataclass
class Case:
    case_id: str    # "1장-1"
    chapter: str    # "1장"
    section: str | None
    index: int
    title: str

@dataclass
class Chunk:
    id: str; heading: str; title: str; text: str
