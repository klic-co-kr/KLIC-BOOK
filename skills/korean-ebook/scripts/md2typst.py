#!/usr/bin/env python3
"""md2typst.py <md_dir|md_file> --out <typ_dir> — Markdown → Typst 변환.

- ## / ### → = / == (typst 헤딩)
- ![](path) → #image("path")
- $$...$$ 블록 수식 → #mitex[`...`] (LaTeX 그대로, typst mitex 패키지)
- $...$ 인라인 수식 → #mitex[`...`]
- 그 외 본문 그대로
"""
import json, re, sys
from pathlib import Path

# 0.4 infographic 펜스 추출 — step 0.5(코드펜스 통째 stash)보다 먼저.
# 펜스 원문은 build.py가 render하고, 본문에는 마커 ⟦IG:N⟧만 남는다.
# 마커는 stash_str()에 넣어 이중 보호한다(스펙 §2 [1]).
IG_RE = re.compile(r'^```infographic[ \t]*\n(.*?)^```[ \t]*$', re.S | re.M)


def extract_fences(md: str) -> tuple[str, list[dict]]:
    fences = []
    def _take(m):
        fences.append({
            "index": len(fences) + 1,
            "line": md[:m.start()].count("\n") + 1,
            "body": m.group(1),
        })
        return f"⟦IG:{len(fences)}⟧"                    # 백틱 없음 — IG_RE 재매치 불가
    md = IG_RE.sub(_take, md)
    return md, fences


def unwrap_quoted_fences(md: str) -> str:
    """인용구(> ) 안의 코드펜스를 최상위로 언랩.

    펜스가 인용 안에 남으면 step 0.5 스태시가 매치를 > 접두 뒤에서 시작해
    펜스를 인용 괄호 안에 조각내고, typst에서 unclosed delimiter가 된다
    (ai-agent-book-ko ch02 `> ```xml` 실측). 펜스 시작·내부·종료 행의
    > 접두를 벗겨 top-level 펜스로 만든다 — 앞뒤 산문 인용은 그대로 둔다.
    """
    out = []
    in_fence = False
    for line in md.split('\n'):
        m_open = re.match(r'^>[ \t]?(```+)', line)
        if not in_fence and m_open:
            in_fence = True
            out.append(line[m_open.start(1):])
            continue
        if in_fence:
            m_close = re.match(r'^>[ \t]?(```+)[ \t]*$', line)
            if m_close:
                in_fence = False
                out.append(line[m_close.start(1):])
                continue
            out.append(re.sub(r'^>[ \t]?', '', line))
            continue
        out.append(line)
    return '\n'.join(out)


def _restore_ig_markers(md: str, stash_str) -> str:
    # 가시 마커 ⟦IG:n⟧ → stash 보호. 변환 중간 단계 보호가 목적이고
    # step 7 복원으로 최종 .typ에는 ⟦IG:n⟧가 그대로 남는다(build.py 치환 대상).
    return re.sub(r'⟦IG:(\d+)⟧',
                  lambda m: stash_str(m.group(0)), md)


def convert(md: str) -> str:
    protected = []
    def stash_str(s: str) -> str:
        protected.append(s)
        return f"\x00{len(protected) - 1}\x00"
    def stash(m):
        return stash_str(m.group(0))
    # -1.5 인용구 내부 펜스 언랩 — infographic/스태시보다 먼저(위 함수 주석).
    md = unwrap_quoted_fences(md)
    # -1. infographic 펜스 — 다른 어떤 변환보다 먼저(스펙 §2 [1]).
    md, _fences = extract_fences(md)
    md = _restore_ig_markers(md, stash_str)
    # 0. 선두 YAML frontmatter 제거 — 표준 markdown 관행. 미제거 시
    # id/order/status 메타데이터가 본문 산문으로 인쇄된다(실전시스템설계 실측).
    # 파일 시작의 --- 쌍만 취급(파일 중간 ---는 수평선 등 다른 용법).
    md = re.sub(r'\A---[ \t]*\n.*?\n---[ \t]*\n', '', md, count=1, flags=re.S)
    # 0.5 코드펜스(```...```) 통째로 stash — typst도 ``` 를 raw block으로
    # 쓰므로 내용은 한 글자도 건드리지 않고 전달한다. 미보호 시 인라인
    # 코드스팬 regex(step 4)가 우연히 삼켜 "우발적 보호"되는데, 펜스 내부에
    # 백틱이 있으면 페어링이 어긋나 내용이 step 6 이스케이프에 오염된다
    # (system-design-notes ch16·22 SQL 블록 실측).
    md = re.sub(r'```.*?```', stash, md, flags=re.S)
    # 0.7 markdown 체크리스트 → 인쇄 글리프. typst에 체크박스 없어
    # 미변환 시 "[ ] 첫 항목"이 리터럴로 인쇄된다(설득의 구조 부록3 실측).
    md = re.sub(r'^(\s*[-*])\s\[ \]\s+', r'\1 □ ', md, flags=re.M)
    md = re.sub(r'^(\s*[-*])\s\[[xX]\]\s+', r'\1 ☑ ', md, flags=re.M)
    # 1. 화폐 $<숫자>/<단위|통화> → escape
    md = re.sub(r'\$(\d[\d,.]*(?:\s*/\s*\w+|\s*(?:원|엔|달러|USD|시간)))',
                lambda m: r'\$' + m.group(1), md)
    # 2. 이미지 — alt 텍스트가 있으면 figure 캡션으로 올린다. 미변환 시
    # 캡션이 통째로 사라진다(skill-state-ko 그림 8종 무캡션 실측).
    # 캡션 본문은 step 6 규칙으로 미리 escape해 stash 보호한다.
    def _esc_cap(s: str) -> str:
        for a, b in (("\\", "\\\\"), ("#", "\\#"), ("[", "\\["), ("]", "\\]"),
                     ("$", "\\$"), ("<", "\\<"), (">", "\\>"), ("@", "\\@"),
                     ("*", "\\*"), ("_", "\\_"), ("~", "\\~")):
            s = s.replace(a, b)
        return s
    def _img(m):
        cap = m.group(1).strip()
        if not cap:
            return f'#figure(image("{m.group(2)}"))'
        return (f'#figure(image("{m.group(2)}"), '
                f'caption: [{stash_str(_esc_cap(cap))}])')
    md = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', _img, md)
    # 2.5 md 파이프 표 → typst #table(). 미변환 시 | A | B | 가 리터럴
    # 파이프 문자로 인쇄된다(system-design-notes 표 148줄 실측).
    # 구분행(|---|---|)이 있는 블록만 표로 판정 — 본문의 홑파이프 줄은
    # 그대로 둔다. 셀 내부는 강조 변환 + typst 특수 escape를 여기서
    # 수행하고 결과를 stash해 step 6이 다시 건드리지 않게 한다.
    def _table_cell(c: str) -> str:
        c = c.replace('\\', r'\\').replace('#', r'\#').replace('[', r'\[').replace(']', r'\]')
        c = c.replace('$', r'\$').replace('<', r'\<').replace('>', r'\>').replace('@', r'\@')
        c = c.replace('_', r'\_').replace('~', r'\~')
        c = re.sub(r'\*\*(.+?)\*\*', '\x02\\1\x02', c)
        c = re.sub(r'(?<!\w)\*(?=\S)([^*]+?)(?<=\S)\*(?!\*)', '_\\1_', c)
        # 강조 변환 후 남은 홑 *(와일드카드 등)은 escape — [*]는 typst에서
        # 강조 마커 미닫음 컴파일 오류다(ch04 규칙 표 실측). \x02 마커
        # 복원 전에 수행해 변환된 굵게를 다시 escape하지 않는다.
        c = re.sub(r'(?<!\\)\*', r'\\*', c)
        return c.replace('\x02', '*')
    def _table_block(m):
        block = m.group(0)
        if not re.search(r'^\s*\|?[\s:|-]*-[\s:|-]*\|?\s*$', block, flags=re.M):
            return block  # 구분행 없음 — 표 아님
        rows = []
        for line in block.split('\n'):
            if not line.strip() or re.match(r'^\s*\|?[\s:|-]*-[\s:|-]*\|?\s*$', line):
                continue
            rows.append([c.strip() for c in line.strip().strip('|').split('|')])
        if not rows:
            return block
        ncols = max(len(r) for r in rows)

        def _wlen(s: str) -> float:
            # 렌더 폭 가중 길이 — 한국어 음절은 라틴 대문자 대비 약 1.8배 폭.
            return sum(1.8 if ord(ch) > 0x2E7F else 1.0 for ch in s)

        _num_cell = re.compile(r'^[0-9.,+\-–—±∗▲†‡%~x×\s]*$')

        def _col_fr(cells: list[str]) -> str:
            # 콘텐츠 인지 열 폭. 균등 1fr에서는 무분할 라틴 토큰
            # (Qwen3-8B 등)이 좁은 열을 넘쳐 인접 열 잉크 위에 인쇄된다
            # (evoharness-rl 표1 p16 실측). 숫자 전용 열은 좁게, 텍스트
            # 열은 최장 셀·최장 토큰 가중으로 넓게.
            nonempty = [c for c in cells if c]
            if not nonempty:
                return '1fr'
            if all(_num_cell.match(c) for c in nonempty):
                w = max(0.55, min(0.8, max(_wlen(c) for c in nonempty) / 7.0))
            else:
                cellw = max(_wlen(c) for c in nonempty) / 9.0
                tokw = max(_wlen(t) for c in nonempty for t in re.split(r'[\s·()/]+', c)) / 6.0
                w = min(2.4, max(1.2, cellw, tokw))
            return f'{w:.2f}'.rstrip('0').rstrip('.') + 'fr'

        col_fr = []
        for c in range(ncols):
            # 헤더는 분류에서 제외 — 본문 셀로 숫자열 판정(헤더 "평균"은
            # 한국어라 텍스트로 오분류된다).
            col_fr.append(_col_fr([r[c] for r in rows[1:] if len(r) > c]))

        def _row(r: list[str]) -> str:
            # 짧은 행은 빈 셀 패딩 — 열 수와 셀 수가 어긋나면 typst가
            # 남는 셀을 다음 행으로 흘린다.
            r = r + [''] * (ncols - len(r))
            return ', '.join(f'[{_table_cell(c)}]' for c in r)
        # 첫 행은 table.header로, block(width: 100%)로 전폭.
        # 내용 폭 자동(columns: n)이면 표마다 폭이 제각각(들쭉날쭉)해지고
        # 블록이 중앙에 놓인다(agent-papers 본문 표 실측). typst 0.15는
        # table에 width 인자가 없어 block으로 감싼다. 헤더 채움·줄무늬·굵게는
        # base.typ의 set/show 규칙이 담당.
        body_cells = ', '.join(_row(r) for r in rows[1:])
        return stash_str(
            f'#block(width: 100%)[#table(columns: ({", ".join(col_fr)}), '
            f'table.header({_row(rows[0])}), {body_cells})]')
    md = re.sub(r'(?:^[ \t]*\|.*\|[ \t]*$\n?)+', _table_block, md, flags=re.M)
    # 3. 블록 수식 $$...$$ → #mitex
    md = re.sub(r'\$\$(.+?)\$\$', lambda m: f'#mitex[`{m.group(1).strip()}`]',
                md, flags=re.S)
    # 4. typst 요소 보호 (인라인 변환 전)
    md = re.sub(r'#(?:figure|image|mitex|ref|link|page)\b[^\n]*', stash, md)
    md = re.sub(r'`[^`]*`', stash, md)
    # 4.5 HTML 주석 제거 — 그림 생산 메타데이터(<!-- figure-spec ... -->) 등.
    # 코드 스팬은 step 4에서 이미 보호되어 있다.
    md = re.sub(r'<!--.*?-->', '', md, flags=re.S)
    # 5. 인라인 수식 $...$ — \ / 알파벳 / ( / | 시작(숫자=화폐 제외), 한국어 \text 포함 허용.
    #    #mi는 mitex의 block:false 변형 — #mitex 기본값이 block: true라 인라인
    #    수식이 문단 한가운데 디스플레이 줄로 분리된다(skill-state-ko p16 실측).
    #    첫 글자 | 허용은 $|C_t|$ 같은 절댓값 표기 누출 방지(같은 책 p28 실측).
    md = re.sub(r'(?<!\\)(?<!\$)\$([\\A-Za-z(|][^\$\n]{0,250})\$(?<!\\)(?!\$)',
                lambda m: f'#mi[`{m.group(1).strip()}`]', md)
    # 새 #mi/#mitex 보호 직전 — `#mi[...]` 뒤에 곧바로 '('가 오면 typst가
    # 함수 추가 인자로 파싱해 "expected comma" 컴파일 오류가 난다
    # (ai-agent-book-ko ch07 `$\pi_\theta$(훈련 중인 모델)` 실측).
    # 공백을 하나 넣어 코드 모드를 끊고 마크업 텍스트 괄호로 만든다.
    md = re.sub(r'(#(?:mi|mitex)\[`[^`\n]*`\])\(', r'\1 (', md)
    # 새 #mi/#mitex 보호 — 백틱 괄호(`...`)까지만. [^\n]*로 줄 끝까지 삼키면
    # 같은 행의 한국어 산문 **굵게**가 step 6.5를 우회해 리터럴 별표로
    # 인쇄된다(ai-agent-book-ko ch07 실측). 변환기가 만드는 mitex는 전부
    # 백틱 래핑이라 [^`\n]*이 정확한 경계다.
    md = re.sub(r'#(?:mi|mitex)\[`[^`\n]*`\]', stash, md)
    # 6. 본문 typst 특수 이스케이프 (남은 $ 포함)
    md = md.replace('\\', r'\\').replace('#', r'\#').replace('[', r'\[').replace(']', r'\]')
    md = md.replace('$', r'\$').replace('<', r'\<').replace('>', r'\>').replace('@', r'\@')
    md = md.replace('*', r'\*').replace('_', r'\_').replace('~', r'\~')
    # ~는 typst 마크업에서 줄바꿈 없는 공백으로 해석된다 — 범위 표기
    # "5~8턴"이 "5 8턴"으로 인쇄되는 것을 막는다(skill-state-ko 실측).
    # 6.5 markdown 강조 (step 6에서 * → \* escape되므로 escape된 형태에 매치).
    # 미변환 시 **굵게**가 리터럴 별표로 인쇄된다(실전시스템설계 머리말 실측).
    # 굵게는 임시 마커(\x02)로 변환해 기울임 변환과 충돌하지 않게 한다.
    md = re.sub(r'\\\*\\\*(?=\S)([^\n]+?)(?<=\S)\\\*\\\*', '\x02\\1\x02', md)
    md = re.sub(r'(?<![\w\\])\\\*(?=\S)([^\\\n]+?)(?<=\S)\\\*(?!\*)', '_\\1_', md)
    md = md.replace('\x02', '*')
    # 7. 보호 복원 — 중첩 스태시까지 푼다. 이미지 캡션 마커가 step 4의
    # #figure 줄 스태시 안에 들어가 이중으로 숨는 경우(캡션 도입 실측),
    # 단일 패스로는 안쪽 마커가 남는다. 마커가 없어질 때까지 반복.
    prev = None
    while prev != md:
        prev = md
        md = re.sub(r'\x00(\d+)\x00', lambda m: protected[int(m.group(1))], md)
    # 8. 헤딩 (step 6에서 # → \# escape되므로 escape된 형태에 매치)
    md = re.sub(r'^\\#\\#\\#\\#\\#\s+(.+)$', r'==== \1', md, flags=re.M)
    md = re.sub(r'^\\#\\#\\#\\#\s+(.+)$', r'=== \1', md, flags=re.M)
    md = re.sub(r'^\\#\\#\\#\s+(.+)$', r'== \1', md, flags=re.M)
    # 8.2 무번호 H1 — 파트 divider(제N부)와 전·후기 부속 장은 장번호
    # 카운터에서 제외한다. 라벨 <part>/<nonum>을 붙이고 base.typ가
    # 분기한다(설득의 구조 — 프롤로그·서막·6개 파트 때문에 1장이 "07"로
    # 찍힌 실측).
    def _h1(m):
        t = m.group(1)
        if re.match(r'^제\s*\d+\s*부\b', t):
            return f'= {t} <part>'
        if re.match(r'^(프롤로그|서막|서문|머리말|들어가며|나가며|에필로그|저자의 당부|'
                    r'작가의 말|감사의 글|옮긴이의 말|특별부록|부록|appendix)\b', t, re.I):
            return f'= {t} <nonum>'
        return f'= {t}'
    md = re.sub(r'^\\#\\#\s+(.+)$', _h1, md, flags=re.M)
    md = re.sub(r'^\\#\s+(.+)$', r'= \1', md, flags=re.M)
    # 8.5 블록 인용 (step 6에서 > → \> escape되므로 escape된 형태에 매치).
    # 빈 인용행(>)은 먼저 지운다 — \s?가 개행을 삼켜 다음 행(언랩된 펜스 등)을
    # 인용 괄호로 끌어들이는 원인이며(ai-agent-book-ko 실측), 남으면 리터럴
    # '>'로 인쇄된다. 내용 매치는 [ \t]?로 한정해 행을 넘지 않게 한다.
    md = re.sub(r'^\\>[ \t]*$\n?', '', md, flags=re.M)
    md = re.sub(r'^\\>[ \t]?(.+)$', r'#quote[\1]', md, flags=re.M)
    # 8.7 헤딩 중간점(·) 뒤 줄바꿈 기회 — typst는 U+00B7을 break 기회로
    # 쓰지 않아 justify 헤딩에서 긴 라틴 ·연쇄 토큰이 프레임 밖으로 넘친다
    # (실전시스템설계 ch25 실측). 제로폭 공백(U+200B)을 심어 분량은 그대로
    # 두고 줄바꿈만 허용한다. 수식·코드가 섞인 헤딩은 보호 대상이라 제외.
    md = re.sub(r'^(=+ .+)$',
                lambda m: m.group(1).replace('·', '·​')
                if '#mitex' not in m.group(1) and '#mi[' not in m.group(1) and '`' not in m.group(1)
                else m.group(1),
                md, flags=re.M)
    # 9. 남은 비헤딩 ## (markdown 잔재) escape
    md = re.sub(r'(?<!\\)##(?=\w)', r'\#\#', md)
    return md


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--out", required=True)
    ap.add_argument("--fences-out", default=None,
                    help="펜스 페이로드를 <stem>.fences.json으로 저장")
    a = ap.parse_args()
    src = Path(a.input)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    targets = [src] if src.is_file() else sorted(src.glob('*.md'))
    fences_dir = Path(a.fences_out) if a.fences_out else None
    if fences_dir:
        fences_dir.mkdir(parents=True, exist_ok=True)
    for md in targets:
        raw = md.read_text(encoding='utf-8')
        _, fences = extract_fences(raw)
        if fences_dir:
            (fences_dir / (md.stem + '.fences.json')).write_text(
                json.dumps(fences, ensure_ascii=False, indent=1), encoding='utf-8')
        t = convert(raw)
        (out / (md.stem + '.typ')).write_text(
            '#import "@preview/mitex:0.2.7": mitex, mi\n\n' + t, encoding='utf-8')
        print(f'{md.name} → {md.stem}.typ')


if __name__ == '__main__':
    main()
