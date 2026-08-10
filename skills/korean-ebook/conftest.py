"""Pytest bootstrap for the korean-ebook skill.

Adds ``scripts/`` to ``sys.path`` so test modules can import the skill's
helper scripts directly (e.g. ``import generate_summary``) for fast unit
testing, complementing end-to-end runs that invoke the CLI as a subprocess.
"""

import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent
SCRIPTS_DIR = SKILL_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
