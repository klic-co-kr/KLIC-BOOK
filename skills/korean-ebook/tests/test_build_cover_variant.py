"""tests/test_build_cover_variant.py — 자동 표지 변형5(위계 격자형) 계약

make_auto_cover는 cover-auto.typ을 빌드 디렉터리에 쓰고 png을 컴파일한다 —
검증은 생성된 .typ 소스로 한다.
"""
import pytest
from scripts.build import make_auto_cover

CFG = dict(
    style="lecture", title="에이전트는 하니스를 배운다",
    subtitle="외부 실행 하니스를 학습하는 에이전트 정책", author="KLIC",
    cover_series="AGENT RUNTIME PAPERS", cover_notes=["· A. 문제", "· B. 설계"],
    cover_imprint="KLIC BOOKS", date="2026-09",
)

def _typ(cfg, d):
    d.mkdir(parents=True, exist_ok=True)
    make_auto_cover(cfg, d)
    return (d / "cover-auto.typ").read_text(encoding="utf-8")

def test_cover_v5_frame_and_dotgrid(tmp_path):
    # 변형5: 외곽 프레임 괘선(9mm 오프셋) + 점 격자 모티프 + 연도 정보행.
    out = _typ(dict(CFG, cover_variant=5), tmp_path)
    assert 'dx: 9mm, dy: 9mm' in out          # 프레임 괘선
    assert 'circle(radius' in out             # 점 격자
    assert '[2026]' in out                    # 상단 연도
    assert '[AGENT RUNTIME PAPERS]' in out    # 시리즈 라벨

def test_cover_v5_deterministic_per_title(tmp_path):
    # 같은 책 = 같은 표지 — 점 격자 배치는 제목 해시로 결정적.
    a = _typ(dict(CFG, cover_variant=5), tmp_path / "a")
    b = _typ(dict(CFG, cover_variant=5), tmp_path / "b")
    c = _typ(dict(CFG, cover_variant=5, title="다른 제목"), tmp_path / "c")
    assert a == b and a != c

def test_cover_invalid_variant_falls_back(tmp_path):
    # 변형 지정이 1~5 밖이면 해시 분포로 회귀 — 변형5 마커 없음.
    out = _typ(dict(CFG, cover_variant=9), tmp_path)
    assert 'dx: 9mm, dy: 9mm' not in out

def test_cover_composition_optin_changes_motif(tmp_path):
    # cover_composition: true → 프로파일 모티프가 기본 점 격자를 대체.
    from scripts.cover_compositions import pick_profile
    off = _typ(dict(CFG, cover_variant=5), tmp_path / "off")
    on = _typ(dict(CFG, cover_variant=5, cover_composition=True),
              tmp_path / "on")
    assert on != off
    p = pick_profile(CFG["title"])
    if p[2] != "none":
        assert 'rgb("' in on  # 모티프 조각은 팔레트 리터럴 사용

def test_cover_composition_deterministic(tmp_path):
    # 프로파일 경로도 결정적 — 같은 책 = 같은 표지.
    a = _typ(dict(CFG, cover_variant=5, cover_composition=True), tmp_path / "a")
    b = _typ(dict(CFG, cover_variant=5, cover_composition=True), tmp_path / "b")
    assert a == b
