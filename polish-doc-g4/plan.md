# polish-doc G4 확장 — 구현 계획 (M티어)

- 과업: korean-ebook 스킬 G4 문체 게이트에 polish-doc 문체 인사이트 4건 도입
- 단계: plan (state.json 기준) → next: implement
- 작성: 2026-09-04 (planner) · 정정: 기존 test_korean_lint.py 테스트 수 9 → **8** (pytest 8 passed·함수 8개 실측 — 초판 보고 오기)
- 원천 인사이트: https://github.com/albertrim/polish-doc (팀장 전달 4건 기준 — 원문 재검증은 범위 밖)

## 0. 조사로 확정된 전제

| 확인 항목 | 결과 |
|---|---|
| 스킬 사본 2곳 동기화 | 소스 레벨 동일 — `diff -rq --exclude=__pycache__` 차이 0. 차이는 `__pycache__`(.pyc)뿐. 과거 "저장소 낙후"는 커밋 cbd5a86·f67b257로 해소. **진본 = 저장소 사본** (git 이력 존재·VERSION 0.1.0 양쪽 동일) |
| 라이터 계약 문서 | 별도 문서 없음. **`docs/korean-style.md`가 라이터 계약 그 자체** — 5행 "챕터 집필·번역 프롬프트에 이 문서 경로를 넣고 시작한다", 57행 "경고가 나면 집필 에이전트가 위 표에 따라 고친다". style-authoring.md는 스타일 팩 저작 문서(무관), SKILL.md는 빌드 스킬 서술 |
| 축약 교정 계약 문서 | 전용 문서 없음 — 교정 지침은 SKILL.md:147-148 "gate-report.json 참조해 지정된 면만 수정 후 재빌드"와 korean-style.md:56-57에 분산. Never-cut 조항 삽입점 = **korean-style.md 신설 절** |
| qc_gate.py G4 결합 | G4는 qc_gate.py:255-266에서 `korean_lint.lint_manuscript()`만 호출 — **qc_gate.py 수정 불필요**. 신규 경고는 자동 WARN 채널 유입. test_qc_gate.py에 G4 어설션 없음 |
| VERSION bump | 불필요 — style-authoring.md §7 "스타일 팩 추가·계약 변경(스키마·밴드·폰트)시 patch bump". G4 WARN 패턴은 해당 밖 |
| 테스트 방식 | tests/test_korean_lint.py — 순수 함수 `lint_text()` 단위, `_w()` 헬퍼 부분문자열 assert. **기존 8테스트**. 실행: `cd skills/korean-ebook && python3 -m pytest -q` |

## 1. 임계값 캘리브레이션 (출간 7권 원고 실측, 2026-09-04)

SKIP_LINE 필터 적용 후 본문 기준 — korean_lint가 보는 경로와 동일:

| 책 | 자수 | 조사 합계/1000자 | '이 아니라' 파일당 최대 | 문두 스캐폴딩 | 헤지 |
|---|---|---|---|---|---|
| agent-papers-2026-ko | 80,662 | 0.2 | 12 | 1 | 2 |
| ai-agent-book-ko | 342,936 | 0.3 | 24 | 1 | 0 |
| evoharness-rl-ko | 21,521 | 0.5 | 3 | 0 | 0 |
| persuasion-structure-ko | 164,970 | 0.2 | 12 | 1 | 0 |
| skill-state-ko | 31,245 | 0.3 | 5 | 0 | 0 |
| system-design-interview-notes-ko | 96,068 | 0.3 | 3 | 6 | 0 |
| harness-of-harness-ko | 10,630 | 0.4 | 2 | 0 | 0 |

도출 임계값:
- **번역투 조사**("에 대한"+"을 통해"+"의 경우" 합계): 1000자당 **2.0 초과** — 자연 분포 최대 0.5의 4배 여유, 출간 코퍼스 오탐 0건
- **"이 아니라"**: 문서(챕터 파일)당 **20회 초과** — 실측 최대 24(장문책 1파일만 상회). 스펙 요구 "문서당 상한" 방식 유지
- **문두 스캐폴딩·헤지**: 밀도 아님 **출현마다 경고** (CLICHE 방식 동일) — 실측 자연 빈도 책 전체 0~6회, 출현 = 수정 대상

## 2. 변경 파일 목록 (우선순위순)

| # | 파일 | 변경 요약 |
|---|---|---|
| 1 | `skills/korean-ebook/scripts/korean_lint.py` | 신규 상수 4종 + 검사 4건 추가(97줄 → 약 125줄). docstring 원천에 polish-doc 추가 |
| 2 | `skills/korean-ebook/tests/test_korean_lint.py` | 신규 테스트 5건 추가(기존 8건 무변경 → 총 13). **TDD: 테스트 먼저(RED) → 구현(GREEN)** |
| 3 | `skills/korean-ebook/docs/korean-style.md` | 원천 표기 추가 + 신설 절 3개 + G4 표 4행(57줄 → 약 85줄) |
| 4 | `skills/korean-ebook/SKILL.md` | 144행 G4 행 패턴 나열 갱신 — 1줄 수정 |
| 5 | `~/.claude/skills/korean-ebook/` | 위 4파일 저장소→설치본 복사(§8 절차) |

4파일(≤5)이므로 Phase 분해 불필요. 검증 단위 2개: **A = 기계(1→2), B = 문서(3→4)+동기화(5)**. B의 G4 표 문구는 A에서 확정된 경고 메시지와 일치해야 하므로 A 선행.

## 3. korean_lint.py 변경 상세

### 3.1 모듈 상수 (기존 CLICHE·EM_DASH_PER_1K 선언 뒤에 추가)

```python
# 문두 스캐폴딩 — 접속 부사로 여는 기계 구조 (polish-doc)
SCAFFOLD_START = re.compile(r"(?:^|[.!?…]\s+)(먼저|또한|마지막으로)\s*,")
# 헤지 — 근거 없는 한정·지시 남설 (polish-doc)
HEDGE = {
    "라고 할 수 있": "근거 없는 한정 — 단정 '~다' 또는 근거 숫자 병기",
    "라는 점입니": "지시 명사 남설 — 직설 서술로 풀기",
}
# 번역투 직역 조사 밀도 (polish-doc) — 출간 7권 실측 0.2~0.5/1000자의 4배
TRANSLATION_PARTICLE = ("에 대한", "을 통해", "의 경우")
PARTICLE_PER_1K = 2.0
# '이 아니라' 대조 재구성 남발 (polish-doc) — 실측 파일당 최대 24
IANIRA_CAP = 20
```

### 3.2 lint_text() 루프 내 — 기존 CLICHE 검사 뒤(줄 단위)

```python
if m := SCAFFOLD_START.search(s):
    warns.append(f"L{i+1} 문두 스캐폴딩 '{m.group(1)},' — 접속 없이 본론 직진")
for pat, fix in HEDGE.items():
    if pat in ln:
        warns.append(f"L{i+1} 헤지 '{pat}' — {fix}")
```

### 3.3 루프 후 밀도 섹션 — 기존 '의' 연쇄 검사 뒤·`return warns` 앞(문서 단위)

```python
ptot = sum(body.count(p) for p in TRANSLATION_PARTICLE)
if ptot / chars * 1000 > PARTICLE_PER_1K:
    warns.append(f"번역투 조사 {ptot}곳({ptot/chars*1000:.1f}/1000자) — 직역 조사 풀기")
if (ianira := body.count("이 아니라")) > IANIRA_CAP:
    warns.append(f"'이 아니라' {ianira}회(문서 상한 {IANIRA_CAP}) — 대조 재구성 줄이기")
```

### 3.4 경고 메시지 렌더 예시 (전문)

- `L3 문두 스캐폴딩 '먼저,' — 접속 없이 본론 직진`
- `L5 헤지 '라고 할 수 있' — 근거 없는 한정 — 단정 '~다' 또는 근거 숫자 병기`
- `번역투 조사 27곳(2.3/1000자) — 직역 조사 풀기`
- `'이 아니라' 24회(문서 상한 20) — 대조 재구성 줄이기`

줄 단위 메시지는 기존 `L{i+1} 유형 '패턴' — 권고` 형식, 밀도 메시지는 기존 엠대시 밀도 형식(행 번호 없음) 준수.

### 3.5 docstring 원천 추가 (4행 뒤)

```
원천 규칙: https://github.com/snflkd/fluent-korean (output-style 지침)
          https://github.com/albertrim/polish-doc (문체 텔 — 2026-09 채택)
```

**구조적 보증**: 신규 4패턴 모두 기존 prose 필터(`in_fence`/`SKIP_LINE`) 통과 후의 `prose` 리스트·`body` 문자열에만 작동 — 인용문>·표|·목록·헤딩·코드펜스 제외가 별도 코드 없이 자동 적용.

## 4. 문서 변경 상세

### 4.1 korean-style.md — 상단 원천 갱신 (3~4행)

```markdown
원천: [fluent-korean](https://github.com/snflkd/fluent-korean) (Claude Code output-style,
국문과 전공 저자), [polish-doc](https://github.com/albertrim/polish-doc) (문체 텔·축약
원칙 — 2026-09 채택). 이 문서는 KLIC-BOOK 원고 작성 에이전트·번역 작업에 맞게 채택한 버전.
```

### 4.2 korean-style.md — 신설 절 3개 ("## 용어" 뒤·"## 적용 제외" 앞, 기존 규칙 8번에 이어 번호)

```markdown
## 문체 텔 (polish-doc)

9. **문장 길이에 천장이 있다.** 한국어 문장은 평균 40자 안팎, 상한 2줄(약 80자).
   넘는 문장은 쪼갠다 — 길다는 것은 절이 겹겹이라는 뜻이다.
10. **결론부터 쓴다(answer-first).** 문단·섹션의 첫 문장이 그 단위의 결론이다.
    배경을 깔고 결론을 나중에 꺼내면 독자는 근거를 저장 없이 들어야 한다.
11. **형용사 주장 대신 숫자·사실.** "크게 개선되었다"는 증명이 아니다 — "3.2배
    빨라졌다"로 바꾼다. 수치가 없으면 사실 관계로 대체한다.
12. **볼드 강조는 문단당 1개.** 강조가 셋 이상이면 아무것도 강조가 아니다.
```

```markdown
## 축약 교정 원칙 (Never-cut)

- 숫자·날짜·측정값·파일경로·ID·커맨드·사람이 내려야 할 선택은 글자수 밴드(G3)를
  맞추려고 자르지 않는다. 데이터 버리면서 줄이기는 실패다.
- 밴드 초과의 해법은 문장 재구성·어순 정리·조사 정리이지 정보 삭제가 아니다.
```

※ "데이터 버리면서 줄이기는 실패다"는 팀장 전달 문구 verbatim — grep 검증 기준점(§7 claim 7).

```markdown
## 납품 전 자기 리비전 (라이터 계약)

챕터를 납품하기 전에 이 문서로 원고를 한 번 자가 점검한다 — 특히 아래 G4 표와
'문체 텔' 절. 발견한 텔은 고쳐서 납입하고, 고치지 못한 것은 납품 노트에 이유를
붙인다. 자가 점검 없이 납품하지 않는다.
```

### 4.3 korean-style.md — G4 표에 4행 추가 (기존 표 마지막 행 뒤)

```markdown
| 문두 스캐폴딩 | "먼저," "또한," "마지막으로," | 접속 없이 본론 직진 |
| 헤지 | "라고 할 수 있" "라는 점입니" | 단정·직술 서술 |
| 번역투 조사 밀도 | "에 대한" "을 통해" "의 경우" 1000자당 2개 초과(합계) | 직역 조사 풀기 |
| '이 아니라' 빈도 | 문서당 20회 초과 | 대조 재구성 줄이기 |
```

### 4.4 SKILL.md 144행 G4 행 수정 문구 (기존 → 신규)

기존:
```markdown
| G4 | 한글 문체 — 기계 한국어·번역투 패턴(명사형 종결·조각문·되어지·상투구·'의' 연쇄·엠대시 밀도). 원고 md에서 검사, [fluent-korean](https://github.com/snflkd/fluent-korean) 규칙 기계화 | WARN |
```
신규:
```markdown
| G4 | 한글 문체 — 기계 한국어·번역투 패턴(명사형 종결·조각문·되어지·상투구·'의' 연쇄·엠대시 밀도·문두 스캐폴딩·헤지·번역투 조사 밀도·'이 아니라' 빈도). 원고 md에서 검사, [fluent-korean](https://github.com/snflkd/fluent-korean)·[polish-doc](https://github.com/albertrim/polish-doc) 규칙 기계화 | WARN |
```

## 5. 신규 테스트 (test_korean_lint.py — 기존 방식 준수, 기존 8건 무변경)

```python
def test_scaffold_detected():
    assert "문두 스캐폴딩" in _w("먼저, 이 방법을 살펴봅시다.")


def test_hedge_detected():
    assert "헤지" in _w("이것이 핵심이라고 할 수 있습니다.")


def test_particle_density_detected():
    text = "값에 대한 검증을 통해 확증하고 오류의 경우 무시한다. " * 8
    assert "번역투 조사" in _w(text)


def test_ianira_cap_detected():
    text = " ".join(f"이것은 {i}번이 아니라 {i+1}번 시도다." for i in range(21))
    assert "'이 아니라'" in _w(text)


def test_new_patterns_respect_skip_lines():
    assert lint_text("## 먼저, 시작\n\n- 또한, 둘\n\n> 마지막으로, 셋\n\n본문은 정상입니다.") == []
```

기존 `test_clean_prose_no_warns` 문장("에이전트는 도구를 호출하고…")은 신규 패턴 미발 — 회귀 없음 확인 완료. 총 8 + 5 = **13테스트**.

## 6. 보존 제약 (구현 프롬프트에 verbatim 복사)

- 기존 6패턴 검사(NOUN_END·FRAGMENT_END·DOUBLE_PASSIVE·CLICHE 6키·POSSESSIVE_CHAIN·EM_DASH 밀도)의 정규식·메시지·임계값 동작 불변 — 신규 패턴은 추가만
- G4는 WARN 유지, PASS/FAIL 영향 없음 유지 — **qc_gate.py 미수정**
- korean_lint.py SKIP_LINE 제외 규칙(인용문>·표|·목록·헤딩·코드펜스) 신규 패턴에도 동일 적용 — prose 필터 통과 후 검사로 구조적으로 보장, 별도 필터 분기 금지
- 기존 테스트 8건 수정·삭제 금지 — 신규 추가만
- 원천 표기: korean-style.md 상단에 polish-doc 원천 추가 표기
- **저장소 사본(/mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook)이 진본** — 설치본(~/.claude/skills/korean-ebook)은 저장소에서 복사(반대 방향 금지, __pycache__ 제외)
- 빌드·QC 자동화 플로우(build.py·qc_gate.py·style_pick.py) 불변 — G4 경고 수 증가는 WARN 채널 유입만
- VERSION bump 불필요 (style-authoring.md §7 — 스타일 팩·계약 변경 아님)

## 7. 검증 요구 claims (구현 완료 후 리뷰가 검증)

1. `grep -c "SCAFFOLD_START\|HEDGE\|PARTICLE_PER_1K\|IANIRA_CAP" scripts/korean_lint.py` ≥ 4 — 신규 심볼 존재
2. `git diff`에서 기존 6패턴 정의줄(NOUN_END~EM_DASH_PER_1K = 6.0)과 기존 경고 메시지 무변경
3. `python3 -m pytest tests/test_korean_lint.py -q` **13테스트(기존 8 + 신규 5)** 전량 pass
4. `python3 -m pytest -q` 스킬 전체 스위트 회귀 0 fail
5. `git diff --stat`에 qc_gate.py 없음 — G4 WARN 채널 무변경
6. `grep "polish-doc" docs/korean-style.md` 상단 원천 표기 존재
7. `grep -F "데이터 버리면서 줄이기는 실패다" docs/korean-style.md` 1행 — Never-cut 문구 verbatim 존재
8. `grep "자기 리비전" docs/korean-style.md` 라이터 절 존재, `grep "문두 스캐폴딩" SKILL.md` G4 행 갱신 존재
9. `diff -rq skills/korean-ebook ~/.claude/skills/korean-ebook --exclude=__pycache__` 차이 0 — 4파일 byte-identical 동기화
10. korean-style.md G4 표 신규 4행의 용어가 §3.4 경고 메시지 용어와 일치 (문두 스캐폴딩·헤지·번역투 조사·'이 아니라')

## 8. 동기화 절차 (구현 마지막 단계 — 저장소 → 설치본)

```bash
cd /mnt/d/DEV/acc0mplish/KLIC-BOOK
for f in scripts/korean_lint.py tests/test_korean_lint.py docs/korean-style.md SKILL.md; do
  cp "skills/korean-ebook/$f" "$HOME/.claude/skills/korean-ebook/$f"
done
diff -rq skills/korean-ebook "$HOME/.claude/skills/korean-ebook" --exclude=__pycache__   # 출력 없음(차이 0) 확인
cd "$HOME/.claude/skills/korean-ebook" && python3 -m pytest tests/test_korean_lint.py -q  # 설치본에서도 13 pass 확인
```

- 설치본 `__pycache__`의 낡은 .pyc는 Python이 mtime으로 자동 무효화 — 삭제 불필요
- 반대 방향(설치본→저장소) 복사 금지

## 9. 위험과 검증

| 위험 | 검증/완화 |
|---|---|
| 임계값 과민(기존 책 오탐) | 7권 실측 근거 — 조사 2.0/1000은 최대 실측 0.5의 4배, 오탐 0. 이견 시 상수 1줄 조정(롤백 단위 최소) |
| WARN 증가로 리포트 변화 | G4는 WARN — PASS 판정 무관. "신간 0건 목표"는 신간에만 적용(기존 책 재빌드 없음) |
| 스캐폴딩 오탐(문장 경계 밖) | 정규식이 문두(행 시작·문장부호 직후)에만 앵커 — 어절 중간 "이는 또한," 미발 |
| 동기화 누락·방향 오류 | claim 9의 diff -q로 봉쇄, 진본 방향은 §6 보존 제약에 명시 |
| 인코딩 | 한국어 문자열 전부 UTF-8 리터럴(\uXXXX 이스케이프 금지 — 전역 규칙) |

## 10. 롤백 판단

완전 가역·저위험. ① 코드 — 추가 전용(상수+분기), 커밋 revert 한 번으로 원복, WARN-only라 롤백 전까지도 빌드 파괴 없음 ② 문서 — doc-only revert ③ 설치본 — 저장소 revert 후 §8 절차 재실행. 되돌릴 수 없는 조작 없음.

## 11. 가정 (스펙 불확실분 — 구현 중 이견 시 팀장 확인)

1. "§6 스타일 텔" = polish-doc 원문의 절 번호. 우리 문서에는 절 번호가 없으므로 자가 점검 대상을 "G4 표 + '문체 텔' 절"로 치환해 문서화
2. 라이터 계약 = korean-style.md(별도 계약 문서 부재 — §0 참조). SKILL.md는 계약이 아니라 빌드 서술이므로 G4 행 갱신만
3. Never-cut 삽입점 = korean-style.md 신설 절(교정 프롬프트 전용 문서 부재 — 교정자도 korean-style.md를 프롬프트로 받음 → 단일 소스)
4. 조사 밀도 2.0/1000·'이 아니라' 20/문서는 실측 기반 잠정값 — 구현 중 근거 이견 시 상수 조정 후 본 계획 §1·§4.3 갱신
5. polish-doc 인사이트 4건 문구는 팀장 전달 내용 기준 — 원문 URL 표기만 추가

## 12. 커밋 제안

```
feat: korean-ebook G4 문체 게이트 확장 — polish-doc 텔 4종 도입
```

본 plan.md 포함 1커밋. 대상 경로: `skills/korean-ebook/`(4파일) + `polish-doc-g4/plan.md`.
