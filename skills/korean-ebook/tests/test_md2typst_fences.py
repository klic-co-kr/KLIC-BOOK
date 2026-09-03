"""test_md2typst_fences.py — 스펙 §2 [1]: 펜스 추출·마커 치환·사이드 파일."""
import json
import subprocess
import sys
from pathlib import Path

from scripts.md2typst import convert, extract_fences

MD = """# 서론

본문 문단이다. ```code``` 인라인도 있다.

```infographic
{"layout": "flow", "title": "결론 제목", "steps": [
  {"title": "접수", "text": "등록"},
  {"title": "폐쇄", "text": "확정"}
]}
```

뒤 본문.
"""


def test_extract_fences_returns_marker_and_payload():
    md2, fences = extract_fences(MD)
    assert len(fences) == 1
    assert fences[0]["index"] == 1
    assert fences[0]["line"] == 5                      # 1부터 시작 라인
    assert "flow" in fences[0]["body"]
    assert "⟦IG:1⟧" in md2
    assert '"layout"' not in md2                       # 원문 잔류 없음


def test_convert_leaves_marker_not_yaml():
    out = convert(MD)
    assert "⟦IG:1⟧" in out
    assert '"layout": "flow"' not in out               # YAML이 코드로 인쇄되지 않음
    assert "\\#include" not in out                     # 마커는 이스케이프 대상 아님


def test_code_fence_without_infographic_untouched():
    md2, fences = extract_fences("일반\n\n```\ncode block\n```\n")
    assert fences == []
    assert "```\ncode block\n```" == md2 or "code block" in md2


def test_cli_fences_out_sidecar(tmp_path):
    src = tmp_path / "ch01.md"
    src.write_text(MD, encoding="utf-8")
    out_dir = tmp_path / "typ"
    r = subprocess.run(
        [sys.executable, str(Path(__file__).resolve().parents[1] / "scripts" / "md2typst.py"),
         str(src), "--out", str(out_dir), "--fences-out", str(tmp_path / "fences")],
        capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    side = tmp_path / "fences" / "ch01.fences.json"
    data = json.loads(side.read_text(encoding="utf-8"))
    assert data[0]["index"] == 1 and "flow" in data[0]["body"]
    typ = out_dir / "ch01.typ"
    assert "⟦IG:1⟧" in typ.read_text(encoding="utf-8")
