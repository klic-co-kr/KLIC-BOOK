#!/usr/bin/env python3
"""split_chapters.py --work <dir> — Step 4 챕터 분할 (사람 게이트 필수).

work/pages/<NNN>.md 에서 챕터 표지 정규식(references/chapter_patterns.md)으로
후보 경계 감지 → work/chapters.json(approved:false) + work/chapter-gate.md(보고서).

**게이트**: 사람이 chapter-gate.md 검토 후 chapters.json에 approved:true 추가.
승인 없으면 render_md.py 가 non-zero 종료. 자동화 금지.
"""
import sys, re, json
from pathlib import Path

# 한국어·영어 챕터 표지 (chapter_patterns.md 준용)
CHAPTER_RE = re.compile(
    r'^##\s+(제\s*\d+\s*부|제\s*\d+\s*장|\d+\s*장(?![\w\d])|Chapter\s+\d+|Ch\.?\s*\d+|Part\s+\d+|부록|Appendix|후기|에필로그|서문|들어가며)\b.*$',
    re.MULTILINE,
)


def split(work_dir: str) -> list[dict]:
    work = Path(work_dir)
    pages_dir = work / "pages"
    if not pages_dir.is_dir():
        sys.exit(f"ERROR: {pages_dir} 없음 — Step 2(extract_text) 먼저 실행")

    raw = []  # (page, matched_heading_line)
    for md_file in sorted(pages_dir.glob("*.md")):
        page_num = int(md_file.stem)
        text = md_file.read_text(encoding="utf-8")
        for m in CHAPTER_RE.finditer(text):
            heading = m.group(0).lstrip('#').strip()
            raw.append({"start_page": page_num, "heading": heading})

    # 같은 페이지 중복 제거 + 번호 부여
    seen, chapters = set(), []
    for r in raw:
        key = (r["start_page"], r["heading"])
        if key in seen:
            continue
        seen.add(key)
        chapters.append(r)
    for i, c in enumerate(chapters, 1):
        c["n"] = i
        c["approved"] = False

    cf = {
        "source": str(work),
        "n_detected": len(chapters),
        "approval": None,   # 사람 게이트 전까지 None
        "chapters": chapters,
    }
    (work / "chapters.json").write_text(
        json.dumps(cf, ensure_ascii=False, indent=2), encoding="utf-8")

    # 게이트 보고서
    lines = [
        "# 챕터 분할 게이트 보고",
        "",
        f"감지된 챕터 후보: {len(chapters)}개",
        "",
        "사람이 검토 후 `chapters.json`의 `approval` 필드를 채우고(또는 항목 수정),",
        "각 챕터 `approved: true`로 확정. **자동화 금지** — 오감지가 산출물 전체를 망친다.",
        "",
        "| n | 시작페이지 | 헤딩 |",
        "|---|---|---|",
    ]
    for c in chapters:
        lines.append(f"| {c['n']} | p.{c['start_page']} | {c['heading']} |")
    lines += ["", "## 검토 체크", "- [ ] 챕터 경계 정확?", "- [ ] 누락/과잉?",
              "- [ ] 부록·후기 분리?", "- [ ] 승인 시 approval + approved:true"]
    (work / "chapter-gate.md").write_text("\n".join(lines), encoding="utf-8")

    return chapters


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    chapters = split(a.work)
    print(f"detected {len(chapters)} chapters → {a.work}/chapters.json")
    print(f"게이트 보고서: {a.work}/chapter-gate.md (사람 승인 필수)")


if __name__ == "__main__":
    main()
