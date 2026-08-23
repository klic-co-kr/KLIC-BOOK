"""test_infographic_cli.py — 스펙 §5.5: lint/preview 단독 실행."""
import subprocess
import sys
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[1]
CLI = SKILL / "scripts" / "infographic" / "cli.py"
from scripts.build import typst_binary                # noqa: E402
# typst 부재 시 typst_binary()는 falsy가 아니라 SystemExit(1)(build.py _fail)을
# 던진다 — 잡아서 빈 문자열로 돌려야 skipif가 도달한다(컴파일 스모크와 동일 가드).
try:
    TYPST = typst_binary()      # PATH → ~/.local/bin/typst 폴백 단일화(Global Constraints)
except SystemExit:
    TYPST = ""

MD = """## 장

원문에 5단계가 있다.

```infographic
{"layout": "flow", "title": "5단계 수렴", "evidence": "§1", "steps": [
  {"title": "접수", "text": "등록"},
  {"title": "폐쇄", "text": "확정"}
]}
```
"""


def test_lint_ok_exit_zero(tmp_path):
    ch = tmp_path / "ch01.md"; ch.write_text(MD, encoding="utf-8")
    r = subprocess.run([sys.executable, str(CLI), "lint", str(ch)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert "OK" in r.stdout and "1" in r.stdout


def test_lint_violation_exit_one_with_report(tmp_path):
    ch = tmp_path / "ch01.md"
    ch.write_text(MD.replace("5단계 수렴", "9단계 수렴"), encoding="utf-8")  # 원문엔 9 없음
    r = subprocess.run([sys.executable, str(CLI), "lint", str(ch)], capture_output=True, text=True)
    assert r.returncode == 1
    assert "number-evidence" in r.stderr and "ch01.md #1" in r.stderr


def test_lint_layout_error_one_line_no_traceback(tmp_path):
    # practical 상한 6단계 초과(7단계) — traceback 크래시 대신 [layout] 한 줄
    # 지적으로 끝나야 한다(최종 리뷰 Important).
    steps = ",\n  ".join(f'{{"title": "{t}", "text": "내용"}}'
                         for t in "가나다라마바사")
    md = ("## 장\n\n흐름이 길다.\n\n```infographic\n"
          '{"layout": "flow", "title": "일곱단계 절차", "steps": [\n  '
          + steps + "]}\n```\n")
    ch = tmp_path / "ch07.md"; ch.write_text(md, encoding="utf-8")
    r = subprocess.run([sys.executable, str(CLI), "lint", str(ch)], capture_output=True, text=True)
    assert r.returncode == 1
    assert "[layout]" in r.stderr
    assert "Traceback" not in r.stderr


@pytest.mark.skipif(not TYPST, reason="typst 없음")
def test_preview_compiles_single_fig(tmp_path):
    ch = tmp_path / "ch01.md"; ch.write_text(MD, encoding="utf-8")
    out = tmp_path / "fig.pdf"
    r = subprocess.run([sys.executable, str(CLI), "preview", str(ch), "--fig", "1",
                        "--out", str(out)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert out.exists() and out.stat().st_size > 1000
