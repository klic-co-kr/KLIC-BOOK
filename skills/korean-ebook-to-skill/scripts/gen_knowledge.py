#!/usr/bin/env python3
"""gen_knowledge.py <book_dir> --candidates <yaml> --work <dir> --out <dir>

승인된 candidates.yaml → 지식층 산출물 렌더:
- out/SKILL.md             지식층 본문 (frontmatter+description)
- out/chapters/            챕터 헤딩 트리 (prose/anthology/glossary)
- out/appendix-c-map.md    부록C 회상 보고 (INDEX 챕터 있을 때)
- out/extraction-report.md 게이트 가시화 (루브릭/승인이력)

게이트: approval_log 비어있으면 사람 게이트 미통과로 간주, sys.exit(non-zero).
v1 대비 수정: judgment_cases.json 대신 candidates.yaml 소비 + extraction-report 추가.
"""
import sys, argparse, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from korean_ebook_to_skill.candidates import load_candidates
from korean_ebook_to_skill.chapters import parse_chapter_file
from korean_ebook_to_skill.appendix_c import parse_cases, compute_recall, RecallResult
from korean_ebook_to_skill.render import (render_skill_md, render_chapter_md,
    render_appendix_c_map, render_extraction_report)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book_dir"); ap.add_argument("--candidates", required=True)
    ap.add_argument("--work", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    cf = load_candidates(a.candidates)
    if not cf.approval_log:
        sys.exit("ERROR: approval_log 없음 — 사람 게이트 미통과. extraction-report 확인 후 approval_log 추가.")
    chapters = json.loads((Path(a.work) / "chapters.json").read_text(encoding="utf-8"))
    out = Path(a.out); (out / "chapters").mkdir(parents=True, exist_ok=True)
    # 회상 — INDEX 챕터(부록C)에서 사례 추출 후 candidates 와 교집합
    idx = next((c for c in chapters if c["content_type"] == "index"), None)
    recall = None; score = 0.0
    if idx:
        cases = parse_cases(parse_chapter_file(idx["path"]))
        recall = compute_recall([c.model_dump() for c in cf.candidates], cases)
        score = recall.coverage
    # 챕터 헤딩 트리 렌더 (prose/anthology/glossary 만)
    for c in chapters:
        if c["content_type"] not in ("prose", "anthology", "glossary"): continue
        ch_cf = parse_chapter_file(c["path"])
        num = c["number"] or c["slug"]
        (out / "chapters" / f"ch{num}-{c['slug']}.md").write_text(render_chapter_md(ch_cf), encoding="utf-8")
    (out / "SKILL.md").write_text(render_skill_md(cf, [], score), encoding="utf-8")
    if recall:
        (out / "appendix-c-map.md").write_text(render_appendix_c_map(recall, cf), encoding="utf-8")
    else:
        # spec §8 위험완화: 부록C(INDEX)가 없으면 회상 기준 자체가 부재.
        # 산출물을 아예 생략하면 게이트 표면이 보이지 않으므로 노트로 명시.
        (out / "appendix-c-map.md").write_text(
            f"# 부록C 회상 보고 — {cf.book_title}\n\n"
            "**회상 기준 부재**: 이 책에 부록C 사례 색인이 없어 사례 회상율을 산출할 수 없다. "
            "판단 품질은 사람 게이트에 전적으로 의존한다.\n",
            encoding="utf-8")
    # recall 이 None 이어도 render_extraction_report 는 실제 RecallResult 로 호출 —
    # 구 type("R",...) 익명 shim 은 .covered/.uncovered 접근 시 AttributeError 위험이어서 제거.
    (out / "extraction-report.md").write_text(
        render_extraction_report(cf, recall if recall else RecallResult(0.0, [], [])),
        encoding="utf-8")
    print(f"generated skill → {out}")

if __name__ == "__main__": main()
