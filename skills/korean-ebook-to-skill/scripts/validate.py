#!/usr/bin/env python3
"""validate.py <skill_dir> [--strict] — 생성된 지식층 스키마 점검.

검사 항목:
- SKILL.md 존재
- frontmatter(---) 존재
- description: 필드 존재 (스킬 발견 가능성)
- 원문 § 근거 형식 chNN§ (위반 시 WARN)
--strict 는 WARN 도 non-zero 종료.
"""
import sys, re, argparse
from pathlib import Path

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("skill_dir"); ap.add_argument("--strict", action="store_true")
    a = ap.parse_args(); d = Path(a.skill_dir); errs, warns = [], []
    sk = d / "SKILL.md"
    if not sk.exists(): errs.append("SKILL.md 없음")
    else:
        md = sk.read_text(encoding="utf-8")
        if not md.startswith("---"): warns.append("frontmatter 없음")
        if "description:" not in md: warns.append("description 없음(스킬 미발견)")
        for line in md.splitlines():
            if "원문 §" in line and "—" not in line and not re.search(r"ch\d+§", line):
                warns.append(f"근거 형식 위반: {line[:60]}"); break
    am = d / "appendix-c-map.md"
    print(am.read_text(encoding="utf-8") if am.exists() else "WARN: appendix-c-map 없음(부록C 없는 책 가능)")
    for e in errs: print(f"ERROR: {e}")
    for w in warns: print(f"WARN: {w}")
    sys.exit(1 if (errs or (a.strict and warns)) else 0)

if __name__ == "__main__": main()
