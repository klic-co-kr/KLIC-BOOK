# Changelog

## 0.2.0 (2026-09-02) - 실행 상태(SKILL.state) 프로토콜

- SKILL.state 논문(arXiv 2608.26263) 적용: Step 2 청크 순회를 append-only
  히스토리 대신 구조화 실행 상태 `work/state.json` 으로 운반.
- Step 1 종료 시 상태 초기화, 청크 1개 판정마다 상태 패치, 재개 시
  `state.json` → `next` 부터 재시작(히스토리 유추 금지).
- merge-not-replace / null-삭제 / 재개 규칙 명시 — premature overwrite
  (소형 모델 최다 실패 모드) 방어.

## 0.1.0 (2026-08-10) - 스캐폴드

- 패키지 스캐폴드 (`korean_ebook_to_skill/`, `pyproject.toml`, `VERSION`)
- pytest 루트 설정 (`conftest.py`, `tests/conftest.py`)
- `scripts/install.sh` → `~/.claude/skills/korean-ebook-to-skill` 심볼릭링크
- 정적 파일: `LICENSE`(MIT, book-to-skill 계승), `README.ko.md`, `.gitignore`
