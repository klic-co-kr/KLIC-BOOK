"""korean_lint — fluent-korean 기계화 규칙 테스트."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from korean_lint import lint_text  # noqa: E402


def _w(text):
    return "\n".join(lint_text(text))


def test_noun_ending_detected():
    assert "명사형 종결" in _w("설정을 마쳤습니다. 결과는 성공함.")


def test_fragment_detected():
    assert "조각문" in _w("원인을 찾았지만. 다음 단계입니다.")


def test_double_passive_detected():
    assert "피동 중복" in _w("이 값은 계산되어지고 저장됩니다.")


def test_cliche_detected():
    assert "번역투" in _w("성능에 있어서 개선이 필요합니다.")


def test_possessive_chain_detected():
    out = _w("팀의 리더의 결정의 근거의 문서를 읽었습니다.")
    assert "3연쇄" in out


def test_code_fence_and_table_excluded():
    text = "```\n확인함. 되어지.\n```\n\n| a |\n|---|\n| 수정됨. |\n\n본문은 정상입니다."
    assert lint_text(text) == []


def test_heading_list_quote_excluded():
    text = "## 수정됨\n\n- 확인함.\n\n> 되어지.\n\n본문은 정상입니다."
    assert lint_text(text) == []


def test_clean_prose_no_warns():
    assert lint_text("에이전트는 도구를 호출하고, 결과를 검증한 뒤 상태를 전진시킵니다.") == []
