#!/usr/bin/env bash
# pdf-to-md 스킬을 ~/.claude/skills 에 심볼릭링크.
# 사용: bash scripts/install.sh
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_HOME="${CLAUDE_SKILLS_HOME:-$HOME/.claude/skills}"
TARGET="$SKILLS_HOME/pdf-to-md"

mkdir -p "$SKILLS_HOME"
ln -sfn "$SKILL_DIR" "$TARGET"

echo "pdf-to-md linked → $TARGET"
echo "의존성 설치(필요 시): pip install -r $(dirname "${BASH_SOURCE[0]}")/requirements.txt"
echo "  PEP 668 환경: python3 -m venv .venv && source .venv/bin/activate && pip install ..."
