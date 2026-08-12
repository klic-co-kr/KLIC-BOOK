from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_DOWNLOADS = {
    "books/forward-deployed-engineer/FDE_포워드_디플로이드_엔지니어_한국어판_최종편집본.pdf?raw=1",
    "books/github-guide/GitHub_협업_실무_가이드.pdf?raw=1",
    "books/practical-system-design-2026-book/build/실전_시스템_설계_2026_practical-system-design-2026-ko.pdf?raw=1",
    "books/ai-agent-book-ko/build/AI_에이전트_깊이_이해하기_ai-agent-book-ko.pdf?raw=1",
    "books/factoryx-ai-infrastructure/build/NHN_FactoryX_실전_설계_nhn-factoryx-ai-infrastructure-ko.pdf?raw=1",
}


def _pdf_download_links(markdown: str) -> set[str]:
    return set(re.findall(r"\[[^]]*PDF 다운로드[^]]*\]\(([^)]+\.pdf\?raw=1)\)", markdown))


def _git_tracks(path: Path) -> bool:
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", path.relative_to(ROOT).as_posix()],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def test_root_readme_links_every_published_book_pdf():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert _pdf_download_links(readme) == EXPECTED_DOWNLOADS

    for link in EXPECTED_DOWNLOADS:
        pdf = ROOT / link.removesuffix("?raw=1")
        assert pdf.is_file(), f"PDF 다운로드 대상이 없습니다: {pdf.relative_to(ROOT)}"
        assert pdf.read_bytes().startswith(b"%PDF-"), f"PDF 형식이 아닙니다: {pdf.relative_to(ROOT)}"
        assert _git_tracks(pdf), f"Git 추적 PDF가 아닙니다: {pdf.relative_to(ROOT)}"


def test_factoryx_readme_has_direct_pdf_download():
    readme = (ROOT / "books/factoryx-ai-infrastructure/README.md").read_text(
        encoding="utf-8"
    )

    expected = (
        "build/NHN_FactoryX_실전_설계_nhn-factoryx-ai-infrastructure-ko.pdf?raw=1"
    )
    assert _pdf_download_links(readme) == {expected}
