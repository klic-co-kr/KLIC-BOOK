#!/usr/bin/env python3
"""G5 콘텐츠 정합성 검사 — 원고 md의 정제 잔존·교차참조를 게이트로.

설득의 구조(OCR→LLM 정제 원고) 파생. G4가 '문체'를 본다면 G5는 '내용
정합성'을 본다 — downstream 보고서(재제작 품질 보고)가 gate-report.json의
g5_content_warns·g5_rescan을 그대로 인용할 수 있게 구조화해 남긴다.

검사(전부 WARN — PASS 조건에 안 들음):
  latin    — 미해결 라틴 시퀀스(OCR 잔존 후보). allowlist 외 ALL-CAPS
  markers  — 판독불능 표기(○○·＿＿·？？)
  xref     — "N장" 교차참조가 실제 장 파일 밖을 가리키는 경우
  comments — 변환 후에도 남은 HTML 주석(스타일러가 지우지만 안전망)
  rescan   — ⚠️ 보강 마커 인벤토리(미스캔 면 — 경고가 아니라 보고서 자산)
"""
import re
from pathlib import Path

# 실제 쓰이는 약어·식별자 허용집. 책마다 늘어나면 여기에 추가(토큰 아님 —
# 스킬 공통 상수로 둔다. 도메인 약어가 allowlist에 없으면 오탐이 아니라
# '확인 필요' 채널로 나오는 게 의도에 맞다).
LATIN_ALLOW = {
    "RAS", "CTA", "CEO", "DNA", "WHO", "QSC", "CPC", "DRM", "TED", "ROI",
    "SB7", "MP3", "DDB", "FBI", "GPS", "GM", "HBO", "ABS", "TGF", "UN",
    "US", "UK", "PC", "IT", "AI", "ML", "LLM", "API", "CSS", "HTML", "PDF",
    "QC", "A/B", "OO", "NSAIDs",
    # 일상 약어·미디어·학술 이니셜(설득의 구조 G5 실전 보정)
    "TV", "OK", "GB", "DVD", "CD", "VR", "AR", "PV", "ID", "IP", "URL",
    "RAZR",
}

# ALL-CAPS 2자 이상 — 뒤에 한글이 붙은 OCR 침입(RASS, WAS 같은)도 잡는다.
_RE_LATIN = re.compile(r"\b[A-Z]{2,}\b")
_RE_MARKER = re.compile(r"○○|＿{2,}|_{3,}|[?？]{2,}")
_RE_XREF = re.compile(r"(\d+)장")
_RE_COMMENT = re.compile(r"<!--")
_RE_RESCAN = re.compile(r"⚠️")


def _ctx(line: str, seq: str) -> str:
    i = line.find(seq)
    lo, hi = max(0, i - 12), min(len(line), i + len(seq) + 12)
    return line[lo:hi].strip()


def scan_latin(text: str) -> list:
    hits = []
    for ln, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            continue  # 코드펜스는 원문 영역
        clean = re.sub(r"`[^`]*`", "", line)  # 인라인 코드스팬 제외
        for m in _RE_LATIN.finditer(clean):
            seq = m.group(0)
            if seq in LATIN_ALLOW or re.fullmatch(r"STEP", seq):
                continue
            hits.append(f"L{ln} '{seq}' …{_ctx(clean, seq)}")
    return hits


def scan_markers(text: str) -> list:
    hits = []
    for ln, line in enumerate(text.splitlines(), 1):
        for m in _RE_MARKER.finditer(line):
            hits.append(f"L{ln} 판독불능 '{m.group(0)}' …{_ctx(line, m.group(0))}")
    return hits


def scan_xref(text: str, chapter_nums: set) -> list:
    hits = []
    for ln, line in enumerate(text.splitlines(), 1):
        for m in _RE_XREF.finditer(line):
            n = m.group(1)
            if n not in chapter_nums:
                hits.append(f"L{ln} {n}장 참조 — 장 파일 없음 …{_ctx(line, f'{n}장')}")
    return hits


def scan_comments(text: str) -> list:
    return [f"L{ln}" for ln, line in enumerate(text.splitlines(), 1)
            if _RE_COMMENT.search(line)]


def _chapter_numbers(chapters: list) -> set:
    """yaml chapters 경로에서 'NN-*.md' 접두 번호를 뽼는다(프롤로그 00 포함)."""
    nums = set()
    for c in chapters:
        m = re.match(r"(\d+)", Path(c).name)
        if m:
            nums.add(m.group(1).lstrip("0") or "0")
    return nums


def lint(chapters: list, book_dir: Path) -> tuple:
    """(파일별 경고 dict, 재스캔 인벤토리 list) 반환."""
    warns, rescan = {}, []
    nums = _chapter_numbers(chapters)
    for rel in chapters:
        p = book_dir / rel
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        found = (scan_latin(text) + scan_markers(text)
                 + scan_xref(text, nums) + scan_comments(text))
        if found:
            warns[rel] = found
        rescan.extend(f"{rel}: {l.strip('>')}" for l in text.splitlines()
                      if _RE_RESCAN.search(l))
    return warns, rescan
