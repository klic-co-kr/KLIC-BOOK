import os, subprocess, pathlib
HERE = pathlib.Path(__file__).resolve()
SCRIPT = HERE.parents[1] / "scripts" / "install.sh"
def test_install_creates_symlink(tmp_path, monkeypatch):
    target = tmp_path / "skills"
    monkeypatch.setenv("CLAUDE_SKILLS_HOME", str(target))
    subprocess.run(["bash", str(SCRIPT)], check=True)
    assert (target / "korean-ebook-to-skill").is_symlink()
    assert os.readlink(target / "korean-ebook-to-skill") == str(SCRIPT.parents[1])
