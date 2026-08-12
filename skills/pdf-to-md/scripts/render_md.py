#!/usr/bin/env python3
"""render_md.py --work <dir> --out <dir> --book-slug <slug> [--title --author] — Step 5 렌더.

승인된 chapters.json(approval 필수) → 챕터별 MD + meta.yaml + README.
approval 없거나 approved:false 챕터는 건너뛴다(사람 게이트 준수).
"""
import sys, json, re
from pathlib import Path


def _slugify(heading: str) -> str:
    """헤딩 → 파일명 slug. 한국어 보존, 기호 공백화."""
    s = re.sub(r'[\\/:*?"<>|]', "", heading)
    s = re.sub(r"\s+", "-", s.strip())
    return s[:60] or "untitled"


def render(work_dir: str, out_dir: str, book_slug: str,
           title: str = "", author: str = "") -> int:
    work = Path(work_dir)
    out = Path(out_dir)
    cf = json.loads((work / "chapters.json").read_text(encoding="utf-8"))
    if not cf.get("approval"):
        sys.exit("ERROR: approval 없음 — 사람 게이트 미통과. chapter-gate.md 검토 후 chapters.json 의 approval 채울 것.")

    out.mkdir(parents=True, exist_ok=True)
    pages_dir = work / "pages"
    page_texts = {int(p.stem): p.read_text(encoding="utf-8")
                  for p in pages_dir.glob("*.md")} if pages_dir.is_dir() else {}
    total_pages = max(page_texts) if page_texts else 0

    approved = [c for c in cf["chapters"] if c.get("approved")]
    if not approved:
        sys.exit("ERROR: approved 챕터 0 — 게이트에서 approved:true 설정 필요.")

    # 챕터별 본문 집합 (start_page ~ 다음 챕터 start_page-1)
    starts = sorted(c["start_page"] for c in approved)
    rendered = []
    for i, ch in enumerate(approved):
        end = (starts[i + 1] - 1) if i + 1 < len(starts) else total_pages
        body_chunks = [page_texts[p] for p in range(ch["start_page"], end + 1)
                       if p in page_texts]
        body = "\n\n".join(body_chunks).strip()
        slug = _slugify(ch["heading"])
        fname = f"{ch['n']:02d}-chapter-{slug}.md"
        (out / fname).write_text(f"# {ch['heading']}\n\n{body}\n", encoding="utf-8")
        rendered.append({"n": ch["n"], "file": fname, "title": ch["heading"],
                         "start_page": ch["start_page"], "end_page": end})

    # meta.yaml
    meta = (f"title: \"{title or book_slug}\"\n"
            f"author: \"{author}\"\n"
            f"book_slug: {book_slug}\n"
            f"n_pages: {total_pages}\n"
            f"n_chapters: {len(rendered)}\n"
            f"source_pdf: \"\"\n"
            f"converted_date: \"\"\n"
            f"chapters:\n")
    for r in rendered:
        meta += f"  - {{n: {r['n']}, file: {r['file']}, start: {r['start_page']}, end: {r['end_page']}}}\n"
    (out / "meta.yaml").write_text(meta, encoding="utf-8")

    # README 색인
    lines = [f"# {title or book_slug}", "", "## 목차", ""]
    for r in rendered:
        lines.append(f"- [{r['title']}]({r['file']}) (p.{r['start_page']}-{r['end_page']})")
    (out / "README.md").write_text("\n".join(lines), encoding="utf-8")

    return len(rendered)


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--book-slug", required=True)
    ap.add_argument("--title", default="")
    ap.add_argument("--author", default="")
    a = ap.parse_args()
    n = render(a.work, a.out, a.book_slug, a.title, a.author)
    print(f"rendered {n} chapters → {a.out}")


if __name__ == "__main__":
    main()
