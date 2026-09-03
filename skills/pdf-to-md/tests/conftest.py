import sys, pathlib
# 스킬 루트를 sys.path 에 추가 (scripts 모듈 import 용)
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
