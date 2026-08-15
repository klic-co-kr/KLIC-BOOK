"""Task 2 — 조립기(assemble) 테스트."""
import shutil
from pathlib import Path

import pytest

from scripts.build import load_config, assemble

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "sample-manuscript"


def _write_config(book: Path, *, style="lecture", title="샘플",
                  chapters=("ch01.md", "ch02.md"), cover=None) -> None:
    lines = [f"style: {style}", f"title: {title}", "chapters:"]
    lines += [f"  - {ch}" for ch in chapters]
    if cover:
        lines.append(f"cover: {cover}")
    (book / "typst-build.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _copy_chapters(book: Path, names) -> None:
    for name in names:
        shutil.copy(FIXTURE_DIR / name, book / name)


def test_assemble_copies_style_and_converts(tmp_path):
    _write_config(tmp_path)
    _copy_chapters(tmp_path, ("ch01.md", "ch02.md"))

    cfg = load_config(tmp_path / "typst-build.yaml")
    main = assemble(cfg, tmp_path)

    assert main == tmp_path / "build" / "main.typ"
    assert (tmp_path / "build" / "tokens.json").exists()
    assert (tmp_path / "build" / "theme.typ").exists()
    assert (tmp_path / "build" / "base.typ").exists()
    assert (tmp_path / "build" / "typ" / "000-ch01.typ").exists()
    assert (tmp_path / "build" / "typ" / "001-ch02.typ").exists()

    text = main.read_text(encoding="utf-8")
    assert "#show: base" in text
    assert "#show: theme" in text
    assert '#include "typ/000-ch01.typ"' in text
    assert '#include "typ/001-ch02.typ"' in text


def test_assemble_missing_chapter_aborts(tmp_path):
    _write_config(tmp_path, chapters=("ghost.md",))
    cfg = None
    with pytest.raises(SystemExit):
        # load_config가 챕터 존재 검사에서 먼저 중단(방어적 중복)하므로
        # assemble까지 도달하지 못해도 파이프라인 중단 의도는 동일.
        cfg = load_config(tmp_path / "typst-build.yaml")
        assemble(cfg, tmp_path)


def test_assemble_copies_cover_into_build(tmp_path):
    (tmp_path / "cover.png").write_bytes(b"\x89PNG fake")
    _write_config(tmp_path, cover="cover.png")
    _copy_chapters(tmp_path, ("ch01.md", "ch02.md"))

    cfg = load_config(tmp_path / "typst-build.yaml")
    main = assemble(cfg, tmp_path)

    assert (tmp_path / "build" / "cover.png").exists()
    text = main.read_text(encoding="utf-8")
    assert '#image("cover.png"' in text
    assert str(tmp_path) not in text  # 책 디렉터리 절대경로 유출 없음


def test_assemble_preserves_chapter_order(tmp_path):
    # 파일명 정렬(ch01→ch02)과 다른 순서로 지정
    _write_config(tmp_path, chapters=("ch02.md", "ch01.md"))
    _copy_chapters(tmp_path, ("ch01.md", "ch02.md"))

    cfg = load_config(tmp_path / "typst-build.yaml")
    main = assemble(cfg, tmp_path)

    text = main.read_text(encoding="utf-8")
    assert text.index('#include "typ/000-ch02.typ"') < text.index('#include "typ/001-ch01.typ"')


def test_assemble_removes_stale_typ_on_rebuild(tmp_path):
    _write_config(tmp_path)
    _copy_chapters(tmp_path, ("ch01.md", "ch02.md"))

    cfg = load_config(tmp_path / "typst-build.yaml")
    assemble(cfg, tmp_path)
    stale = tmp_path / "build" / "typ" / "removed-chapter.typ"
    stale.write_text("= 삭제된 챕터\n", encoding="utf-8")

    main = assemble(cfg, tmp_path)
    assert not stale.exists()
    assert (tmp_path / "build" / "typ" / "000-ch01.typ").exists()
    assert '#include "typ/removed-chapter.typ"' not in main.read_text(encoding="utf-8")

def test_assemble_rebases_manuscript_images_into_build(tmp_path):
    # 원고 ![](path)는 md 기준 상대경로 → typst --root가 build/라
    # 그대로면 root 탈출. build/assets/로 복사해 재작성해야 한다.
    (tmp_path / "img").mkdir()
    (tmp_path / "img" / "pic.png").write_bytes(b"\x89PNG fake")
    (tmp_path / "ch01.md").write_text(
        "# 1장\n\n![그림](img/pic.png)\n", encoding="utf-8")
    _write_config(tmp_path, chapters=("ch01.md",))

    cfg = load_config(tmp_path / "typst-build.yaml")
    assemble(cfg, tmp_path)

    assert (tmp_path / "build" / "assets" / "pic.png").exists()
    typ = (tmp_path / "build" / "typ" / "000-ch01.typ").read_text(encoding="utf-8")
    assert '#figure(image("../assets/pic.png"))' in typ

def test_assemble_missing_image_aborts(tmp_path):
    (tmp_path / "ch01.md").write_text(
        "# 1장\n\n![깨진 그림](img/ghost.png)\n", encoding="utf-8")
    _write_config(tmp_path, chapters=("ch01.md",))

    cfg = load_config(tmp_path / "typst-build.yaml")
    with pytest.raises(SystemExit):
        assemble(cfg, tmp_path)


def _typ_name(idx: int, ch: str) -> str:
    return f"{idx:03d}-{Path(ch).stem}.typ"


def test_assemble_same_stem_chapters_preserved(tmp_path):
    # 서로 다른 디렉터리의 동명 챕터(예: */00-part-introduction.md)가
    # md2typst 출력명 stem.typ에서 서로 덮어써 유실되던 결함(2026-08-15
    # 최종 리뷰 Critical 1). 인덱스 prefix 개명으로 각각 보존되어야 한다.
    for part, body in (("p1", "첫 번째 파트 서문 고유 내용"),
                       ("p2", "두 번째 파트 서문 고유 내용")):
        (tmp_path / part).mkdir()
        (tmp_path / part / "00-part-introduction.md").write_text(
            f"## {part}\n\n{body}\n", encoding="utf-8")
    _write_config(tmp_path, chapters=("p1/00-part-introduction.md",
                                      "p2/00-part-introduction.md"))

    cfg = load_config(tmp_path / "typst-build.yaml")
    main = assemble(cfg, tmp_path)

    typ0 = (tmp_path / "build" / "typ" / _typ_name(0, "p1/00-part-introduction.md"))
    typ1 = (tmp_path / "build" / "typ" / _typ_name(1, "p2/00-part-introduction.md"))
    assert typ0.exists() and typ1.exists()
    assert "첫 번째 파트 서문 고유 내용" in typ0.read_text(encoding="utf-8")
    assert "두 번째 파트 서문 고유 내용" in typ1.read_text(encoding="utf-8")

    text = main.read_text(encoding="utf-8")
    assert f'#include "typ/{typ0.name}"' in text
    assert f'#include "typ/{typ1.name}"' in text


def test_assemble_output_count_and_include_uniqueness(tmp_path):
    # 콘텐츠 정합 불변식: 변환 산출 .typ 수 == 챕터 수, include 대상 중복 0.
    # (동일 stem 2챕터 — 개명 없이는 둘 다 성립 불가)
    for part in ("p1", "p2"):
        (tmp_path / part).mkdir()
        (tmp_path / part / "same.md").write_text(f"## {part}\n", encoding="utf-8")
    _write_config(tmp_path, chapters=("p1/same.md", "p2/same.md"))

    cfg = load_config(tmp_path / "typst-build.yaml")
    main = assemble(cfg, tmp_path)

    typs = list((tmp_path / "build" / "typ").glob("*.typ"))
    assert len(typs) == len(cfg["chapters"]) == 2
    includes = [ln for ln in main.read_text(encoding="utf-8").splitlines()
                if ln.startswith("#include")]
    assert len(includes) == len(set(includes)) == 2
