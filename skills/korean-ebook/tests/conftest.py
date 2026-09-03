"""tests/conftest.py — 스킬 루트를 import 경로에 추가"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
