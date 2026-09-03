"""tests/test_cover_compositions.py — 표지 변조 프로파일 엔진 계약"""
from scripts.cover_compositions import PROFILES, pick_profile, motif_block

PICK = ("위계 격자", "bottom", "dots", 0.30, 3, 1.1)

def test_profiles_schema():
    # 50종 전부 6필드 스키마 — 이름·앵커·모티프·밀도·액센트·피치.
    anchors = {"top", "mid", "bottom"}
    motifs = {"dots", "circles", "lines", "squares", "none"}
    assert len(PROFILES) == 50
    assert len({p[0] for p in PROFILES}) == 50  # 이름 중복 없음
    for name, anchor, motif, density, accent, pitch in PROFILES:
        assert anchor in anchors and motif in motifs
        assert 0.0 <= density <= 1.0 and 2 <= accent <= 5
        assert 0.8 <= pitch <= 1.6

def test_pick_deterministic_and_varied():
    # 같은 제목 = 같은 프로파일. 제목 따라 흩어짐.
    assert pick_profile("에이전트는 하니스를 배운다") == \
        pick_profile("에이전트는 하니스를 배운다")
    picks = {pick_profile(f"책 제목 {i}") for i in range(30)}
    assert len(picks) >= 8  # 30책이 8프로파일 이상으로 흩어짐

def test_motif_none_is_empty_and_others_emit_typst():
    # none → 빈 문자열. 나머지 → place 조각.
    assert motif_block(("x", "mid", "none", 0.0, 2, 1.0), variant=5,
                       w=210, h=297, brand="1F3A5F",
                       pale="C9D4E4") == ""
    for m in ("dots", "circles", "lines", "squares"):
        out = motif_block(("x", "mid", m, 0.5, 3, 1.0), variant=5,
                          w=210, h=297, brand="1F3A5F",
                          pale="C9D4E4")
        assert "#place(" in out and "#box(" in out

def test_motif_deterministic():
    # 모티프 배치 재현성 — 같은 입력 = 같은 조각.
    a = motif_block(PICK, variant=5, w=210, h=297,
                    brand="1F3A5F", pale="C9D4E4")
    b = motif_block(PICK, variant=5, w=210, h=297,
                    brand="1F3A5F", pale="C9D4E4")
    assert a == b
