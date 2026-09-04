# polish-doc G4 후속 — 리뷰 LOW 2건 수정 계획 (S티어)

- 과업: LOW-2 문두 스캐폴딩 여는 괄호·따옴표 recall 공백 + LOW-3 '~ 아니라' 변형 미계수
- 단계: plan(본 문서) → next: implement
- 작성: 2026-09-05 (planner) · 전제 커밋: a6e0eb7 (G4 polish-doc 4텔 도입 완료)
- 정정: 2026-09-05 — 팀장 리컨 반영(§1 측정 무결성 각주·원시 grep 대조표·§10 glob 함정 행)
- 이전 계획: `polish-doc-g4/plan.md` (§1 캘리브레이션 방식 계승)

## 0. 조사로 확정된 전제

| 확인 항목 | 결과 |
|---|---|
| 용어 통일 지점 3곳 | korean_lint.py:89 경고 메시지 · korean-style.md:81 G4 표 행 · SKILL.md:144 G4 행 — 모두 "'이 아니라' 빈도" 계열 사용 중 |
| 기존 테스트 수 | **15건**(pytest 함수 15개 실측) · `cd skills/korean-ebook && python3 -m pytest -q` |
| cap 암묵 고정 | `test_ianira_cap_detected`(21회 → 경고)·`test_ianira_at_cap_not_warned`(20회 → 무경고)가 **cap=20을 정확히 고정**. cap 변경 시 기존 테스트 수정 불가피 — D1 참조 |
| LOW-2 문서 영향 | korean-style.md:78 스캐폴딩 표 행은 예문 나열("먼저," 등)이라 새 검출 범위에도 그대로 유효 — **변경 불필요**(스펙에 없는 범위 확장 금지) |
| 메시지 명칭 충돌 | `test_ianira_cap_detected`가 출력에 `"'이 아니라'"` 부분문자열을 assert — 명칭 교체 시 미통과. 해법 = D2(메시지에 신구 용어 병기) |

## 1. 재실측 (2026-09-05, 출간 7권)

방식: 각 책 `typst-build.yaml` chapters의 md에 korean_lint와 동일한 prose 필터(코드펜스 토글 + SKIP_LINE) 적용 후 본문 기준 — 이전 plan §1과 동일 경로.

측정 무결성(팀장 리컨 경고 반영): 챕터는 **chapters의 문자열 경로(manuscript/… 포함)를 직접 순회** — `books/<이름>/*.md` glob은 manuscript/ 서브디렉터리를 놓치는 함정이 있어 미사용. lint_manuscript()가 chapters만 보므로 lint 관점 완전 일치. 원시 grep은 인용 블록(>)을 세므로 금지 — 상한 산정은 아래 표(prose 필터 후) 기준.

### LOW-3 — '~ 아니라' 변형 포함 재실측

정규식 `(?:이|가|은|는)\s*아니라` findall:

| 책 | 구 계수 최대("이 아니라") | 신 계수 최대(변형 합산) |
|---|---|---|
| agent-papers-2026-ko | 12 | 21 |
| ai-agent-book-ko | 24 | 42 |
| evoharness-rl-ko | 3 | 6 |
| persuasion-structure-ko | 12 | 14 |
| skill-state-ko | 5 | 10 |
| system-design-interview-notes-ko | 3 | 4 |
| harness-of-harness-ko | 2 | 3 |

파일 단위 상위: 42(ai-agent 5장) · 25(2장) · 22(6장) · 21(10장) · 21(9장) · 21(agent-papers 8장).
cap별 상회 파일 수: **cap 20 → 6건**, cap 25/30/35/40 → 1건(42 파일만).
구 상한 20의 경고 프로파일(구 24>20 → 상회 1파일)과 동일 프로파일을 내는 신 cap은 25~41 구간(2위 25 < cap < 최대 42).

팀장 리컨 원시 grep 실측(find 스캔·인용 블록 포함·draft/final 제외)과의 대조 — 원시 파일당 최대: agent-papers 21 / ai-agent 48 / evoharness 7 / persuasion 23 / skill-state 10 / sdi-notes 4 / hoh 4. 원시치는 lint가 보지 않는 인용문(> 블록)까지 세므로 본 표와 같거나 큼(ai-agent 48↔42, persuasion 23↔14, hoh 4↔3, evoharness 7↔6, 나머지 동일). 인용문 비중이 큰 책일수록 격차 확대 — **상한 산정 근거는 본 표(lint 경로)만**. 비계열 추가책 원시치(forward-deployed 21·factoryx 12·product-design 6 등, 2026-09-05 팀장 전달)는 7권 계열 밖이라 캘리브레이션 기준에서 제외.

### LOW-2 — 여는 괄호 허용 신규 정규식의 코퍼스 영향

§4.1의 신규 SCAFFOLD_START로 7권 재스캔: **신규 매치 0건**(구 정규식 매치 수와 전권 동일). 기존 출간 코퍼스 회귀 없음 — recall 확장은 신규 원고(따옴표·괄호로 열리는 대화체)에만 작동. 행두 부사 앞 실존 접두사는 ' * ' 1건뿐(앵커 대상 밖, 미검출 유지가 정상).

## 2. 결정 게이트 (기본안 확정 — 팀장 이견 시 D1/D2만 스위치)

- **D1 상한 = 기존 20 유지(기본)**. 근거: ① 기존 테스트 15건 무변경과 양립하는 유일한 값(경고 테스트 21회>cap, 무경고 테스트 20회≤cap ⇒ cap=20 강제) ② WARN은 PASS 판정 무관, 기존 책 재빌드 없음 — 6파일 상회는 재빌드 시에만 표시 ③ 신간 기준 엄격 유지는 polish-doc "대조 재구성 줄이기" 취지에 부합.
  **대안 cap 30**(2위 25·최대 42 사이 round number, 상회 1파일로 구 프로파일 동일): 테스트 2건의 `range(21)`→`range(31)`, `range(20)`→`range(30)` 수정을 수반 → 보존 제약 위반이므로 팀장 명시 승인 시에만 채택. 본 계획은 기본안으로 작성. 팀장 원시 실측(인용 포함 최대 48)도 상향 여지를 시사하나, 산정 기준은 lint 경로 prose 실측(최대 42·2위 25) — 기본·대안 안 모두 이 표 기준.
- **D2 경고 메시지에 신구 용어 병기**: `"'~ 아니라' 대조 …(문서 상한 20, '이 아니라' 포함) — …"` — 신 명칭 선행 + 구 용어를 괄호 내 병기. 기존 테스트 assertion(`"'이 아니라'"`)을 무수정 통과시키는 유일한 명칭 설계. 메시지 순수화(구 용어 제거) 원하면 테스트 1행 수정이 불가피 — 기본안은 병기.

## 3. 변경 파일 목록 (우선순위순)

| # | 파일 | 변경 요약 |
|---|---|---|
| 1 | `skills/korean-ebook/scripts/korean_lint.py` | SCAFFOLD_START 정규식 교체(여는 괄호·따옴표 허용) + IANIRA_RE 신설·계수 방식 교체 + 경고 메시지 명칭 갱신 + 주석 2건 (121줄 → 약 123줄) |
| 2 | `skills/korean-ebook/tests/test_korean_lint.py` | 신규 테스트 4건 추가(기존 15건 무변경 → 총 19). **TDD: 테스트 먼저(RED) → 구현(GREEN)** |
| 3 | `skills/korean-ebook/docs/korean-style.md` | G4 표 81행 "'이 아니라' 빈도" → "'~ 아니라' 대조 빈도"(어형 합산 병기) — 1행 |
| 4 | `skills/korean-ebook/SKILL.md` | 144행 G4 패턴 나열 내 "'이 아니라' 빈도" → "'~ 아니라' 대조 빈도" — 1행 |
| 5 | `~/.claude/skills/korean-ebook/` | 위 4파일 저장소→설치본 복사(§8 절차) |

4파일(≤5)이므로 Phase 분해 불필요. 검증 단위 2개: **A = 기계(1→2, TDD)**, **B = 문서(3→4)+동기화(5)**. B의 표 문구는 A에서 확정된 메시지 명칭과 일치해야 하므로 A 선행.

## 4. korean_lint.py 변경 상세 (구현자는 verbatim 사용)

### 4.1 SCAFFOLD_START 교체 (35행)

기존:
```python
# 문두 스캐폴딩 — 접속 부사로 여는 기계 구조 (polish-doc)
SCAFFOLD_START = re.compile(r"(?:^|[.!?…]\s+)(먼저|또한|마지막으로)\s*,")
```
신규:
```python
# 문두 스캐폴딩 — 접속 부사로 여는 기계 구조 (polish-doc) · 여는 따옴표·괄호 직후 포함
SCAFFOLD_START = re.compile(r"(?:^|[.!?…]\s+)(?:[\"'“‘『「(\[]{1,2}[ \t]*)?(먼저|또한|마지막으로)\s*,")
```

- 여는 클래스 8자 `"'“‘『「([` — 닫는 괄호·따옴표("』」)])는 문두에 등장하지 않으므로 미포함
- `{1,2}`: 1~2개 중첩 허용 — 리드 예시 `("또한,`가 2중. 코퍼스에 3중 이상 없음(실측)
- `[ \t]*`: 괄호와 부사 사이 공백 허용. **0개 경로(괄호 없음)는 기존과 완전 동일** — 들여쓰기 행 새로 검출하는 확장 없음
- Python 리터럴 주의: 클래스 내 `\"`, `\[` 이스케이프 필수(미이스케이프 시 SyntaxError — 계획 작성 중 실제 확인)
- `m.group(1)`은 여전히 부사 — 루프 내 메시지 코드(74-75행) 무변경

검증 완료(2026-09-05 실행): `"먼저,`·`“먼저,`·`("또한,`·`『먼저,`·`. "마지막으로,`·`('먼저,` 6케이스 신규 검출 / `이는 또한,`(어절 중간)·`먼저 이것은`(쉼표 없음)·`. 이는 또한,`(문장부호 직후 비부사) 3케이스 미검출.

### 4.2 IANIRA 계수 교체 (44-45행 상수, 88-89행 검사)

기존 상수:
```python
# '이 아니라' 대조 재구성 남발 (polish-doc) — 실측 파일당 최대 24
IANIRA_CAP = 20
```
신규 상수:
```python
# '~ 아니라' 대조 재구성 남발 (polish-doc) — 이·가·은·는 어형 합산, 실측 파일당 최대 42
IANIRA_RE = re.compile(r"(?:이|가|은|는)\s*아니라")
IANIRA_CAP = 20
```
기존 검사:
```python
    if (ianira := body.count("이 아니라")) > IANIRA_CAP:
        warns.append(f"'이 아니라' {ianira}회(문서 상한 {IANIRA_CAP}) — 대조 재구성 줄이기")
```
신규 검사:
```python
    if (ianira := len(IANIRA_RE.findall(body))) > IANIRA_CAP:
        warns.append(f"'~ 아니라' 대조 {ianira}회(문서 상한 {IANIRA_CAP}, '이 아니라' 포함) — 대조 재구성 줄이기")
```

- 메시지 골격(`'{용어}' {n}회(문서 상한 {cap}) — 대조 재구성 줄이기`) 유지, 괄호 내 `, '이 아니라' 포함` 추가(D2)
- IANIRA_CAP = 20 무변경(D1 기본안)
- `\s*`는 "이아니라"(무공백)·행 경계 연속도 흡수 — 모두 유효한 대조 구문 계수
- 조사 없는 단독 "아니라"(예: "그냥 아니라")는 미계수(실측 확인)

### 4.3 경고 메시지 렌더 예시 (전문)

- `L1 문두 스캐폴딩 '먼저,' — 접속 없이 본론 직진` (여는 괄호 케이스도 동일 — 부사만 출력)
- `'~ 아니라' 대조 42회(문서 상한 20, '이 아니라' 포함) — 대조 재구성 줄이기`

## 5. 문서 변경 상세

### 5.1 korean-style.md:81 (G4 표 행)

기존:
```markdown
| '이 아니라' 빈도 | 문서당 20회 초과 | 대조 재구성 줄이기 |
```
신규:
```markdown
| '~ 아니라' 대조 빈도 | 문서당 20회 초과(이·가·은·는 어형 합산) | 대조 재구성 줄이기 |
```

### 5.2 SKILL.md:144 (G4 행 내 나열)

`…번역투 조사 밀도·'이 아니라' 빈도)` → `…번역투 조사 밀도·'~ 아니라' 대조 빈도)` — 해당 단어만 교체, 행 나머지 무변경.

### 5.3 비변경 명시

- korean-style.md:78 스캐폴딩 표 행 — 예문 나열이 신 검출 범위에도 유효(LOW-2는 기계 recall 수정이며 문서 요구 없음)
- korean_lint.py docstring — 개별 패턴 미서술이라 무관

## 6. 신규 테스트 (test_korean_lint.py 끝에 추가 — 기존 15건 무변경)

```python
def test_scaffold_quoted_open_detected():
    assert "문두 스캐폴딩" in _w("“먼저, 이 방법을 살펴봅시다.")


def test_scaffold_paren_quote_open_detected():
    assert "문두 스캐폴딩" in _w("('또한, 둘째 축이다.')")


def test_scaffold_mid_sentence_still_ignored():
    assert "문두 스캐폴딩" not in _w("이는 또한, 다른 문제와 이어진다.")


def test_ianira_variant_counted():
    text = " ".join(f"결과는 {i}의 문제가 아니라 {i+1}의 문제다." for i in range(21))
    assert "'~ 아니라' 대조" in _w(text)
```

- test_ianira_variant_counted는 "가 아니라" 21회·"이 아니라" 0회 — 구 계수로는 무경고(RED 증명), 신 계수로 21>20 경고(GREEN)
- 기존 test_ianira_cap_detected(21회 "이 아니라")는 신 계수 21>20 경고 + 병기 명칭이 `"'이 아니라'"` 부분문자열 충족 → 무수정 통과
- 기존 test_ianira_at_cap_not_warned(20회)는 20≤20 무경고 유지 → 무수정 통과
- 총 15 + 4 = **19테스트**

## 7. 보존 제약 (구현 프롬프트에 verbatim 복사)

- 기존 패턴·테스트 15건 동작 불변 — 단 IANIRA 계수 방식 변경(`body.count("이 아니라")` → IANIRA_RE findall)은 본 과업 목적이며 메시지 골격은 유지
- IANIRA_CAP = 20 무변경 (기존 테스트가 20에 고정 — 변경 금지, 이견 시 팀장 확인)
- 기존 9패턴(NOUN_END·FRAGMENT_END·DOUBLE_PASSIVE·CLICHE·POSSESSIVE_CHAIN·EM_DASH·HEDGE·TRANSLATION_PARTICLE·SKIP_LINE)의 정규식·메시지·임계값 무변경 — SCAFFOLD_START 앵커 `^|[.!?…]\s+` 유지, 어절 중간 "이는 또한,"은 미검출 유지
- G4 WARN 유지, PASS/FAIL 영향 없음 — **qc_gate.py 미수정**
- SKIP_LINE 제외 구조 유지 — 신규 검출도 prose 필터 통과 후에만 적용
- **저장소 사본(/mnt/d/DEV/acc0mplish/KLIC-BOOK/skills/korean-ebook)이 진본** — 설치본(~/.claude/skills/korean-ebook)은 저장소에서 복사(반대 방향 금지, __pycache__ 제외)
- 한국어 문자열 전부 UTF-8 리터럴(\uXXXX 이스케이프 금지)
- 커밋 없음(메인 권한) — 작업 디렉터리 수정만

## 8. 검증 요구 claims (구현 완료 후 리뷰가 검증)

1. `grep -c "IANIRA_RE" scripts/korean_lint.py` ≥ 2(정의+사용) — 변형 계수 정규식 존재
2. `grep -F 'body.count("이 아니라")' scripts/korean_lint.py` 0행 — 구 계수 방식 제거
3. `grep -n '{1,2}' scripts/korean_lint.py` SCAFFOLD_START 1행 — 여는 괄호·따옴표 클래스 반영
4. `cd skills/korean-ebook && python3 -m pytest tests/test_korean_lint.py -q` **19 passed**(기존 15 + 신규 4)
5. `git diff skills/korean-ebook/tests/test_korean_lint.py` 추가 전용 — 기존 15 함수 본문에 삭제·수정 라인 없음(append)
6. `grep "'~ 아니라' 대조" scripts/korean_lint.py docs/korean-style.md SKILL.md` 3파일 각 1행 이상 + `grep -F "'이 아니라' 빈도" docs/korean-style.md SKILL.md` 0행 — 3곳 용어 통일
7. `grep -F "IANIRA_CAP = 20" scripts/korean_lint.py` 1행 — 상한 무변경
8. `git diff --stat`에 qc_gate.py·build.py·style_pick.py 부재
9. `diff -rq skills/korean-ebook ~/.claude/skills/korean-ebook --exclude=__pycache__` 출력 없음(차이 0) + 설치본에서도 19 pass
10. 기존 검사 라인의 git diff 무변경 — NOUN_END~EM_DASH_PER_1K 정의·루프 내 기존 메시지 8종·SKIP_LINE

## 9. 동기화 절차 (구현 마지막 단계 — 저장소 → 설치본)

```bash
cd /mnt/d/DEV/acc0mplish/KLIC-BOOK
for f in scripts/korean_lint.py tests/test_korean_lint.py docs/korean-style.md SKILL.md; do
  cp "skills/korean-ebook/$f" "$HOME/.claude/skills/korean-ebook/$f"
done
diff -rq skills/korean-ebook "$HOME/.claude/skills/korean-ebook" --exclude=__pycache__   # 출력 없음 확인
cd "$HOME/.claude/skills/korean-ebook" && python3 -m pytest tests/test_korean_lint.py -q  # 19 pass 확인
```

## 10. 위험과 검증

| 위험 | 검증/완화 |
|---|---|
| opener 허용 regex 오탐(기존 코퍼스) | 7권 재실측 신규 매치 0건(§1) + 어절 중간 가드 테스트(test_scaffold_mid_sentence_still_ignored) |
| 변형 계수로 WARN 증가(출간 6파일 >20) | WARN은 PASS 무관·기존 책 재빌드 없음. 임계 품질 이견 시 D1 대안 cap 30(상회 1파일) — 팀장 승인 게이트 |
| cap 변경 욕구와 테스트 무변경 충돌 | 기존 테스트 2건이 cap=20 고정(§0) — cap 21 이상은 테스트 수정 수반, 보존 제약으로 봉쇄 |
| 정규식 리터럴 이스케이프 실수 | §4.1 코드 블록 verbatim 사용(`\"`·`\[` 필수 — 미이스케이프 시 즉시 SyntaxError로 발견) |
| 재실측 glob 함정·원시 grep 혼용 | §1 방식 고정 — typst-build.yaml chapters 경로 직접 순회(glob은 manuscript/ 누락)·prose 필터 후 기준(원시 grep은 인용문 포함이라 상한 근거 불가) |
| 동기화 누락·방향 오류 | §9 diff -q로 봉쇄, 진본 방향은 §7 보존 제약에 명시 |

## 11. 롤백 판단

완전 가역·저위험. 정규식 1줄 교체 + 상수 1줄 추가 + 검사 2줄 교체 + 테스트 append + 문서 2줄 — `git checkout -- skills/korean-ebook` 후 §9 절차 재실행(또는 설치본도 원복 복사)으로 전량 원복. 커밋 불필요(메인 권한), 되돌릴 수 없는 조작 없음.

## 12. 가정 (스펙 불확실분)

1. D1 cap 20 유지 — 리드 제시 양예("기존 20 유지 또는 조정 근거 제시") 중 테스트 무변경과 양립하는 쪽. 조정 원하면 §2 대안 30 + 테스트 2건 상수 수정가 본 계획의 파생 변경으로 필요
2. D2 메시지에 구 용어 병기 — 순수 명칭만 원하면 test_ianira_cap_detected assertion 1행 수정이 전제되어야 함(기본안은 무수정)
3. 여는 클래스 8자·{1,2} 중첩 상한 — 리드 스케치 + 코퍼스 실측 기준. 3중 중첩 원고 등장 시 `{1,3}` 1글자 상향
4. 정밀 재실측치(42·25·21…)는 2026-09-05 원고 기준 — 원고 수정 후 재활 시 §1 표 갱신 필요
