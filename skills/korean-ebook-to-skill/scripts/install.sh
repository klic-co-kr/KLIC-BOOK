#!/usr/bin/env bash
# korean-ebook-to-skill 설치: $CLAUDE_SKILLS_HOME/korean-ebook-to-skill 심볼릭링크 생성
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$(dirname "${BASH_SOURCE[0]}")")" && pwd)"   # scripts/ → 스킬 루트 (절대경로)
NAME="korean-ebook-to-skill"
CLAUDE_SKILLS_HOME="${CLAUDE_SKILLS_HOME:-$HOME/.claude/skills}"
TARGET="$CLAUDE_SKILLS_HOME"

mkdir -p "$TARGET"
ln -sfn "$SKILL_DIR" "$TARGET/$NAME"

echo "installed: $TARGET/$NAME -> $SKILL_DIR"
