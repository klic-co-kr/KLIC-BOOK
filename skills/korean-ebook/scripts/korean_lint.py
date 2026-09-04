#!/usr/bin/env python3
"""한글 문체 린트 — 기계 한국어·번역투 패턴 검출 (fluent-korean 규칙 기계화).

원천 규칙: https://github.com/snflkd/fluent-korean (output-style 지침)
          https://github.com/albertrim/polish-doc (문체 텔 — 2026-09 채택)
적용 제외: 코드펜스·인용블록(>)·표(|)·헤딩(#)·목록 항목 — 지침 원문이
인용·코드를 제외하고, 헤더·목록의 명사구 종결을 허용하기 때문.

모든 결과는 WARN — PASS/FAIL 판정에 영향 없음(G3와 동급 참고용).
"""
import re
from pathlib import Path

# 문장 끝 명사형 종결 — "확인함." "수정됨." "사용자임." 류 기계 어미
NOUN_END = re.compile(r"(?:함|됨|임|음|김|림|심|키움|그럼)\.(?:\s|$)")
# 연결어미로 끝난 조각문 — 종결어미가 아니라 문장이 열려 있다
FRAGMENT_END = re.compile(r"(?:며|면서|지만|은데|는데|는데도|려면|러|니까|므로)\.(?:\s|$)")
# 피동 중복 — 번역투 대표 오류
DOUBLE_PASSIVE = re.compile(r"되어지")
# 번역투 상투구
CLICHE = {
    "에 있어서": "범위를 나타내는 조사로 직역 — '~에서'·'~ 가운데'",
    "이라는 것을": "지시 명사 남발 — '~임을'",
    "하게 된다": "남발 피동 — '~한다'",
    "해주시기 바랍니다": "기계 공문투 — '~해 주세요'",
    "있으니 참고 바랍니다": "기계 공문투 — '~습니다'(문장 통째로 다듬기)",
    "드리겠습니다": "과잉 존대 — 맥락에 따라 '~합니다'",
}
# 보조사 '의' 3연쇄 — "A의 B의 C의 D" (소유 관계 계단)
POSSESSIVE_CHAIN = re.compile(r"\S*의\s+\S*의\s+\S*의\s+\S")
EM_DASH = "—"
EM_DASH_PER_1K = 6.0   # 1000자당 엠대시 상한 — fluent-korean "엠대시 자제"
CHAIN_PER_1K = 1.0     # 1000자당 '의' 3연쇄 상한
# 문두 스캐폴딩 — 접속 부사로 여는 기계 구조 (polish-doc) · 여는 따옴표·괄호 직후 포함
SCAFFOLD_START = re.compile(r"(?:^|[.!?…]\s+)(?:[\"'“‘『「(\[]{1,2}[ \t]*)?(먼저|또한|마지막으로)\s*,")
# 헤지 — 근거 없는 한정·지시 남설 (polish-doc)
HEDGE = {
    "라고 할 수 있": "근거 없는 한정 — 단정 '~다' 또는 근거 숫자 병기",
    "라는 점입니": "지시 명사 남설 — 직설 서술로 풀기",
}
# 번역투 직역 조사 밀도 (polish-doc) — 출간 7권 실측 0.2~0.5/1000자의 4배
TRANSLATION_PARTICLE = ("에 대한", "을 통해", "의 경우")
PARTICLE_PER_1K = 2.0
# '~ 아니라' 대조 재구성 남발 (polish-doc) — 이·가·은·는 어형 합산, 실측 파일당 최대 42
IANIRA_RE = re.compile(r"(?:이|가|은|는)\s*아니라")
IANIRA_CAP = 20

SKIP_LINE = re.compile(r"^(#|>|\||-\s|\*\s|\d+\.\s|```)")


def lint_text(text: str) -> list:
    """md 본문 하나 검사 → [경고문, ...]"""
    warns = []
    prose, in_fence = [], False
    for ln in text.splitlines():
        if ln.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or SKIP_LINE.match(ln):
            continue
        prose.append(ln)
    body = "\n".join(prose)
    chars = max(len(re.sub(r"\s", "", body)), 1)
    for i, ln in enumerate(prose):
        s = ln.rstrip()
        if m := NOUN_END.search(s):
            warns.append(f"L{i+1} 명사형 종결(기계 어미) '…{m.group(0)}' — 서술어로 완결")
        if m := FRAGMENT_END.search(s):
            warns.append(f"L{i+1} 연결어미 조각문 '…{m.group(0)}' — 종결어미 필요")
        if DOUBLE_PASSIVE.search(ln):
            warns.append(f"L{i+1} 피동 중복 '되어지' — '된다'로")
        for pat, fix in CLICHE.items():
            if pat in ln:
                warns.append(f"L{i+1} 번역투 '{pat}' — {fix}")
        if m := SCAFFOLD_START.search(s):
            warns.append(f"L{i+1} 문두 스캐폴딩 '{m.group(1)},' — 접속 없이 본론 직진")
        for pat, fix in HEDGE.items():
            if pat in ln:
                warns.append(f"L{i+1} 헤지 '{pat}' — {fix}")
    chains = len(POSSESSIVE_CHAIN.findall(body))
    dashes = body.count(EM_DASH)
    if dashes / chars * 1000 > EM_DASH_PER_1K:
        warns.append(f"엠대시 {dashes}개({dashes/chars*1000:.1f}/1000자) — 콜론·접속사로 대체 검토")
    if chains / chars * 1000 > CHAIN_PER_1K:
        warns.append(f"'의' 3연쇄 {chains}곳({chains/chars*1000:.1f}/1000자) — 소유 계단 정리")
    ptot = sum(body.count(p) for p in TRANSLATION_PARTICLE)
    if ptot / chars * 1000 > PARTICLE_PER_1K:
        warns.append(f"번역투 조사 {ptot}곳({ptot/chars*1000:.1f}/1000자) — 직역 조사 풀기")
    if (ianira := len(IANIRA_RE.findall(body))) > IANIRA_CAP:
        warns.append(f"'~ 아니라' 대조 {ianira}회(문서 상한 {IANIRA_CAP}, '이 아니라' 포함) — 대조 재구성 줄이기")
    return warns


def lint_manuscript(chapters: list, base: Path) -> dict:
    """챕터 목록 린트 → {파일: [경고]}"""
    out = {}
    for ch in chapters:
        p = base / ch
        if not p.exists():
            continue
        w = lint_text(p.read_text(encoding="utf-8"))
        if w:
            out[ch] = w
    return out


if __name__ == "__main__":
    import sys, json
    d = Path(sys.argv[1]).resolve()
    cfg = json.loads("{}")
    yml = d / "typst-build.yaml"
    if yml.exists():
        import yaml
        cfg = yaml.safe_load(yml.read_text(encoding="utf-8")) or {}
    res = lint_manuscript(cfg.get("chapters", []), d)
    total = sum(len(v) for v in res.values())
    for f, ws in res.items():
        print(f"== {f} ({len(ws)}건)")
        for w in ws[:10]:
            print("  ", w)
    print(f"총 {total}건 (WARN — PASS 판정 무관)")
