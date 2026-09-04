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


def test_scaffold_detected():
    assert "문두 스캐폴딩" in _w("먼저, 이 방법을 살펴봅시다.")


def test_hedge_detected():
    assert "헤지" in _w("이것이 핵심이라고 할 수 있습니다.")


def test_particle_density_detected():
    filler = "이 장의 논증은 앞선 실험 결과와 일치한다. "
    spiked = filler * 45 + "값에 대한 검증을 통해 오류의 경우 무시한다."
    assert "번역투 조사" in _w(spiked)


def test_particle_density_below_threshold_not_warned():
    filler = "이 장의 논증은 앞선 실험 결과와 일치한다. "
    clean = filler * 150 + "값에 대한 검증을 통해 오류의 경우 무시한다."
    assert "번역투 조사" not in _w(clean)


def test_ianira_cap_detected():
    text = " ".join(f"이것은 {i}번이 아니라 {i+1}번 시도다." for i in range(21))
    assert "'이 아니라'" in _w(text)


def test_ianira_at_cap_not_warned():
    text = " ".join(f"이것은 {i}번이 아니라 {i+1}번 시도다." for i in range(20))
    assert "'이 아니라'" not in _w(text)


def test_new_patterns_respect_skip_lines():
    assert lint_text("## 먼저, 시작\n\n- 또한, 둘\n\n> 마지막으로, 셋\n\n본문은 정상입니다.") == []
