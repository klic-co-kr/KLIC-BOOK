# korean_ebook_to_skill/content_type.py
import re
from .models import ChapterFile, ContentType

# 부록C 제1부 챕터 헤더: N장 / N장 N.M절 / N~M장, 괄호 안 텍스트+건
INDEX_CASES_RE = re.compile(r"###\s*\d+(?:[~–-]\d+)?장(?:\s+\d+\.\d+절)?\s*\([^)]*\d+건[^)]*\)")
ROSTER_KEYWORDS = ("인물", "명단")
INDEX_KEYWORDS = ("사례 색인", "사례색인")
GLOSSARY_METRIC_RE = re.compile(r"\*\*[^*]{2,40}[:：]")  # **메트릭명:**

def classify_content_type(cf: ChapterFile) -> ContentType:
    name = cf.path; text = cf.raw_text
    if cf.kind == "afterword": return ContentType.AFTERWORD
    if any(k in name for k in INDEX_KEYWORDS) or INDEX_CASES_RE.search(text):
        return ContentType.INDEX
    if any(k in name for k in ROSTER_KEYWORDS): return ContentType.ROSTER
    if cf.kind == "appendix" and len(GLOSSARY_METRIC_RE.findall(text)) >= 3:
        return ContentType.GLOSSARY
    if cf.kind == "chapter" and re.search(r"^### 방법론 환원", text, re.MULTILINE):
        return ContentType.ANTHOLOGY
    if cf.kind in ("chapter", "appendix"):
        return ContentType.PROSE
    return ContentType.UNKNOWN
