"""test_infographic_parse.py — 스펙 §3.1·§3.4 상태 기계."""
import pytest

from scripts.infographic.parse import (
    Fence, ParseError, parse_fence, normalize, DEFAULT_NOTE,
)

FLOW_BODY = """
{
  "layout": "flow",
  "title": "장애 대응은 접수에서 폐쇄까지 5단계로 수렴한다",
  "thesis": "대응 흐름을 단계화하면 인계 누락이 사라진다",
  "kicker": "CHAPTER MAP",
  "steps": [
    {"title": "접수", "text": "장애 접수 등록"},
    {"title": "분류", "text": "영향도 기반 분류"},
    {"title": "대응", "text": "임시 조치 시행"},
    {"title": "폐쇄", "text": "재발 방지 확정"}
  ]
}
"""


def test_valid_flow_fence():
    f = parse_fence(1, 10, FLOW_BODY)
    assert isinstance(f, Fence)
    assert f.layout == "flow"
    assert f.index == 1 and f.line == 10
    assert len(f.data["steps"]) == 4
    assert f.note is None           # 생략 시 None — emit이 DEFAULT_NOTE 사용
    assert f.evidence is None


def test_alias_process_normalized():
    f = parse_fence(2, 1, FLOW_BODY.replace('"flow"', '"process"'))
    assert f.layout == "flow"
    assert f.data["_alias"] == "process"


def test_note_and_evidence_kept():
    body = FLOW_BODY.replace('"kicker"', '"note": "커스텀 고지",\n  "evidence": "§2",\n  "kicker"')
    f = parse_fence(1, 1, body)
    assert f.note == "커스텀 고지" and f.evidence == "§2"


def test_invalid_json_rejected():
    with pytest.raises(ParseError) as e:
        parse_fence(1, 3, "{ not json")
    assert e.value.fence_index == 1
    assert "JSON" in e.value.detail or "json" in e.value.detail


def test_empty_fence_rejected_with_line():
    with pytest.raises(ParseError, match="빈 펜스") as e:
        parse_fence(2, 41, "   \n")
    assert e.value.line == 41


def test_unknown_layout_rejected():
    with pytest.raises(ParseError, match="(?i)layout"):
        parse_fence(1, 1, FLOW_BODY.replace('"flow"', '"railroad"'))


def test_missing_title_rejected():
    import json
    d = json.loads(FLOW_BODY); del d["title"]
    with pytest.raises(ParseError, match="(?i)title"):
        parse_fence(1, 1, json.dumps(d, ensure_ascii=False))


def test_step_count_bounds():
    import json
    d = json.loads(FLOW_BODY)
    d["steps"] = [{"title": "s", "text": "t"}]           # 1개 — 하한 위반
    with pytest.raises(ParseError, match="steps"):
        parse_fence(1, 1, json.dumps(d, ensure_ascii=False))
    d["steps"] = [{"title": f"s{i}", "text": "t"} for i in range(9)]  # 9개 — 상한
    with pytest.raises(ParseError, match="steps"):
        parse_fence(1, 1, json.dumps(d, ensure_ascii=False))


def test_empty_step_text_rejected():
    import json
    d = json.loads(FLOW_BODY)
    d["steps"][0]["text"] = "   "
    with pytest.raises(ParseError, match="steps\\[0\\]"):
        parse_fence(1, 1, json.dumps(d, ensure_ascii=False))


def test_normalize_strips_bom_and_crlf():
    assert normalize("﻿a\r\nb") == "a\nb"


def test_default_note_text_defined():
    assert "원문을 대체하지 않습니다" in DEFAULT_NOTE
