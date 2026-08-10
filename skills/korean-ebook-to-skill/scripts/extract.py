#!/usr/bin/env python3
"""extract.py <book_dir> <work_dir> — 책 원문을 전처리 산출물로 추출.

출력:
- work/full_text.txt      전체 본문 (실행마다 truncate — v1 append 중복 버그 수정)
- work/chapters.json      챕터 메타 (path/slug/number/kind/content_type/n_segments)
- work/chunks/            ANTHOLOGY 서브청크 (ch8 케이스별 .md)
- work/candidates.template.yaml  에이전트가 채울 후보 뼈대 (id/title/source_refs)

README 는 glob [0-9]*.md 로 스킵. 추출 대상 = {PROSE, ANTHOLOGY, GLOSSARY}.
"""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from korean_ebook_to_skill.chapters import parse_chapter_file
from korean_ebook_to_skill.content_type import classify_content_type
from korean_ebook_to_skill.anthology import subchunk_anthology
from korean_ebook_to_skill.models import ContentType

EXTRACTABLE = {ContentType.PROSE, ContentType.ANTHOLOGY, ContentType.GLOSSARY}

def main(book_dir, work_dir):
    bdir, wdir = Path(book_dir).resolve(), Path(work_dir)
    wdir.mkdir(parents=True, exist_ok=True)
    (wdir / "chunks").mkdir(exist_ok=True)
    full = wdir / "full_text.txt"; full.write_text("", encoding="utf-8")  # truncate
    chapters, template = [], {"book_slug": bdir.name, "candidates": []}
    for mf in sorted(bdir.glob("[0-9]*.md")):          # README 스킵
        cf = parse_chapter_file(mf); cf.content_type = classify_content_type(cf)
        chapters.append({"path": str(mf), "slug": cf.slug, "number": cf.number,
                         "kind": cf.kind, "content_type": cf.content_type.value,
                         "n_segments": len(cf.segments)})
        if cf.content_type == ContentType.ANTHOLOGY:
            for ch in subchunk_anthology(cf):
                (wdir / "chunks" / f"{ch.id}.md").write_text(ch.text, encoding="utf-8")
                with full.open("a", encoding="utf-8") as f:
                    f.write(f"\n\n===== {ch.id} {ch.title} =====\n{ch.text}\n")
                template["candidates"].append({"id": ch.id, "category": "", "title": ch.title,
                    "source_refs": [f"ch{cf.number}§{ch.heading}"]})
        elif cf.content_type in EXTRACTABLE:
            with full.open("a", encoding="utf-8") as f:
                f.write(f"\n\n===== {cf.slug} =====\n{cf.raw_text}\n")
            template["candidates"].append({"id": cf.slug, "category": "", "title": cf.slug,
                "source_refs": [f"ch{cf.number or cf.slug}"]})
    (wdir / "chapters.json").write_text(json.dumps(chapters, ensure_ascii=False, indent=2), encoding="utf-8")
    (wdir / "candidates.template.yaml").write_text(
        json.dumps(template, ensure_ascii=False, indent=2), encoding="utf-8")  # 에이전트 채울 뼈대
    print(f"extracted {len(chapters)} files → {wdir}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
