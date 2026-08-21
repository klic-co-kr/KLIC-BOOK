"""test_infographic_lint.py — 스펙 §5.2: 전수 보고·위치·레버·교차검증."""
import json
from pathlib import Path

from scripts.infographic.archetypes import flow as flow_arch
from scripts.infographic.lint import check
from scripts.infographic.parse import parse_fence

SKILL = Path(__file__).resolve().parents[1]
TOKENS = json.loads((SKILL / "styles" / "practical" / "tokens.json").read_text(encoding="utf-8"))

CH = """## 개요

대응은 5단계로 수렴한다. 영향도 기반 분류 후 30분 임시 조치를 시행한다.

## 상세

추가 설명.
"""


def _fences(specs: list[dict]):
    out = []
    for i, s in enumerate(specs, 1):
        out.append(parse_fence(i, 1, json.dumps(s, ensure_ascii=False)))
    return out


def _figs(fences):
    return {f.index: flow_arch.layout(f, TOKENS) for f in fences}


def test_all_findings_collected_not_first_only():
    # 펜스 1: 숫자+evidence 없음 / 펜스 2: 숫자+원문에 없는 값 — 둘 다 보고
    fs = _fences([
        {"layout": "flow", "title": "3단계로 수렴한다", "steps": [
            {"title": "접수", "text": "등록"}, {"title": "폐쇄", "text": "확정"}]},
        {"layout": "flow", "title": "t", "evidence": "§1", "steps": [
            {"title": "분류", "text": "999시간 조치"}, {"title": "폐쇄", "text": "확정"}]},
    ])
    found = check(fs, _figs(fs), TOKENS, CH, "ch01.md")
    kinds = [f.kind for f in found]
    assert "number-evidence" in kinds
    assert sum(1 for f in found if f.kind == "number-evidence") == 2   # 전수
    assert any(f.loc == "ch01.md #1 title" for f in found)             # 위치 계약
    assert any(f.loc == "ch01.md #2 steps[0].text" for f in found)


def test_number_with_valid_evidence_passes():
    fs = _fences([{"layout": "flow", "title": "30분 내 임시 조치", "evidence": "§1", "steps": [
        {"title": "분류", "text": "영향도 분류"}, {"title": "대응", "text": "조치"}]}])
    found = check(fs, _figs(fs), TOKENS, CH, "ch01.md")
    assert not [f for f in found if f.kind == "number-evidence"]


def test_ordinal_exempt():
    fs = _fences([{"layout": "flow", "title": "제2장에서 다루는 흐름", "steps": [
        {"title": "접수", "text": "등록"}, {"title": "폐쇄", "text": "확정"}]}])
    found = check(fs, _figs(fs), TOKENS, CH, "ch01.md")
    assert not [f for f in found if f.kind == "number-evidence"]


def test_unresolvable_evidence_nonfatal():
    fs = _fences([{"layout": "flow", "title": "3단계", "evidence": "§9", "steps": [
        {"title": "접수", "text": "등록"}, {"title": "폐쇄", "text": "확정"}]}])
    found = check(fs, _figs(fs), TOKENS, CH, "ch01.md")
    ev = [f for f in found if f.kind == "number-unverified"]
    assert ev and "미검증" in ev[0].measured
    assert ev[0].fatal is False                    # 빌드 안 막음 — 검수 시트 이관(§3.3)


def test_budget_density_violation_reported_with_field_loc():
    long_title = "아주 긴 단계 제목이라 밀도 상한을 초과하는 텍스트가 이곳에 있다 " * 3
    fs = _fences([{"layout": "flow", "title": "t", "steps": [
        {"title": long_title, "text": "가"}, {"title": "B", "text": "나"}]}])
    found = check(fs, _figs(fs), TOKENS, CH, "ch01.md")
    b = [f for f in found if f.kind == "budget"]
    assert b, "밀도 초과(예상 4줄+)가 보고돼야 한다 — 초판 ×10 문턱은 무검사였다(실증)"
    assert b[0].loc == "ch01.md #1 steps[0].title"   # 필드 경로 loc(§5.2 계약)
    assert "줄" in b[0].measured and b[0].levers     # 측정값 + 레버


def test_fence_impostor_detected():
    md = CH + "\n```infographics\n{\"layout\": \"flow\", \"title\": \"x\"}\n```\n"
    fs = _fences([{"layout": "flow", "title": "t", "steps": [
        {"title": "A", "text": "가"}, {"title": "B", "text": "나"}]}])
    found = check(fs, _figs(fs), TOKENS, md, "ch01.md")
    imp = [f for f in found if f.kind == "fence-impostor"]
    assert imp and imp[0].fatal and "infographics" in imp[0].measured


def test_connector_shaft_visibility_checked():
    from scripts.infographic.model import ArrowOp, FigModel
    fs = _fences([{"layout": "flow", "title": "t", "steps": [
        {"title": "A", "text": "가"}, {"title": "B", "text": "나"}]}])
    figs = _figs(fs)
    f0 = figs[1]
    # 공격: 8pt 샤프트(<12)로 교체 — §6.1 위반 감지
    short = tuple(ArrowOp(x1=o.x1, y1=o.y1, x2=o.x1 + 8.0, y2=o.y1, style=o.style)
                  if isinstance(o, ArrowOp) else o for o in f0.ops)
    figs[1] = FigModel(width=f0.width, height=f0.height, ops=short, source_index=1)
    found = check(fs, figs, TOKENS, CH, "ch01.md")
    assert any(f.kind == "connector" and "12" in f.measured for f in found)


def test_missing_token_roles():
    bad = json.loads(json.dumps(TOKENS)); del bad["infographic"]
    fs = _fences([{"layout": "flow", "title": "t", "steps": [
        {"title": "A", "text": "가"}, {"title": "B", "text": "나"}]}])
    found = check(fs, _figs(fs), bad, CH, "ch01.md")
    assert any(f.kind == "tokens" for f in found)


def test_g3_invariant_checked_from_fig_ops():
    fs = _fences([{"layout": "flow", "title": "t", "steps": [
        {"title": "A", "text": "가"}, {"title": "B", "text": "나"}]}])
    figs = _figs(fs)
    # 공격: 도식 텍스트 하나를 본문 크기로 바꿔치기 — G3 위반 감지 확인
    from scripts.infographic.model import TextOp
    f0 = figs[1]
    tampered = tuple(
        TextOp(x=o.x, y=o.y, size=TOKENS["fonts"]["body"]["size_pt"], text=o.text,
               role=o.role, weight=o.weight, max_w=o.max_w, field=o.field)
        if isinstance(o, TextOp) else o for o in f0.ops)
    figs[1] = type(f0)(width=f0.width, height=f0.height, ops=tampered, source_index=f0.source_index)
    found = check(fs, figs, TOKENS, CH, "ch01.md")
    assert any(f.kind == "g3-invariant" for f in found)
