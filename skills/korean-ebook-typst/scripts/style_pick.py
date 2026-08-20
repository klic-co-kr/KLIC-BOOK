#!/usr/bin/env python3
"""style: auto — 원고 콘텐츠 밀도에서 판형을 고르는 휴리스틱.

판단 규칙(챕터당 시각 요소 밀도 + 문단 길이):
- 시각 요소(표·이미지·수식·코드펜스)가 챕터당 1.5건 이상 → lecture (A4)
  논문 해설·IT 생태계·도표 중심 원고. 표가 A4 폭에서만 제대로 펼쳐진다.
- 문단이 길고(평균 400자+) 표가 챕터당 0.5건 미만 → essay (B6 산문)
- 그 외(중간 밀도 실용서) → practical (신국판)
business(백서)는 정형 리포트용으로 자동 판단 대상 아님 — 명시 지정만.
"""
import re
from pathlib import Path

TABLE_SEP = re.compile(r"^\|[\s:\-|]+\|?\s*$")
FENCE = re.compile(r"^```")
IMAGE = re.compile(r"^!\[")
MATH_BLOCK = re.compile(r"^\$\$")

def analyze(md_path: Path) -> dict:
    """챕터 md 하나에서 시각 요소·문단 통계."""
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    in_fence = False
    tables = fences = images = math = 0
    para_buf, paras = [], []
    for ln in lines:
        if FENCE.match(ln):
            if not in_fence:
                fences += 1  # 여는 펜스에서 블록 1개 — 닫는 펜스는 세지 않음
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if TABLE_SEP.match(ln):
            tables += 1
        elif IMAGE.match(ln):
            images += 1
        elif MATH_BLOCK.match(ln):
            math += 1
        elif not ln.strip() and para_buf:
            paras.append(sum(len(p) for p in para_buf))
            para_buf = []
        elif ln.strip() and not ln.startswith(("#", ">", "|", "- ", "* ")):
            para_buf.append(ln.strip())
    if para_buf:
        paras.append(sum(len(p) for p in para_buf))
    return {
        "tables": tables, "fences": fences, "images": images, "math": math,
        "paras": len(paras),
        "avg_para": (sum(paras) / len(paras)) if paras else 0,
    }


def pick(book_dir: Path, chapters: list) -> tuple:
    """(style, 판단 사유) 반환."""
    stats = [analyze(book_dir / ch) for ch in chapters]
    n = max(len(stats), 1)
    visual = sum(s["tables"] + s["images"] + 0.5 * s["math"] + 0.3 * s["fences"]
                 for s in stats) / n
    tables = sum(s["tables"] for s in stats) / n
    avg_para = (sum(s["avg_para"] for s in stats) / n) if stats else 0
    if visual >= 1.5:
        return "lecture", (f"시각 요소 {visual:.1f}건/챕터(표 {tables:.1f}) — "
                           "도표·논문형 원고는 A4 lecture")
    if avg_para >= 400 and tables < 0.5:
        return "essay", (f"문단 평균 {avg_para:.0f}자·표 {tables:.1f}건/챕터 — "
                         "장문 산문은 B6 essay")
    return "practical", (f"시각 요소 {visual:.1f}건/챕터·문단 평균 {avg_para:.0f}자 — "
                         "중간 밀도 실용서는 신국판 practical")


if __name__ == "__main__":
    import sys
    d = Path(sys.argv[1])
    chs = [l.strip() for l in sys.stdin if l.strip()]
    print(pick(d, chs))
