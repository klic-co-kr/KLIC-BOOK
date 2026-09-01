// templates/base.typ — 공통 프리미티브. 스타일 값은 tokens.json에서.
//
// typst 0.15.1 검증: set/show 규칙은 include된 파일 스코프에만 적용되어
// include만으로는 본문에 스타일이 전파되지 않는다. 따라서 전역 스타일은
// main.typ에서 `#show: base` / `#show: theme` 함수 적용으로 발동한다
// (base가 먼저, theme가 나중 — 나중 규칙이 헤딩을 오버라이드).
//
// 판형 디자인 시스템(2026-08-24, 구 WeasyPrint판 publish_book.py CSS 이식):
// 러닝헤드(좌 단축제목·우 장제목·전폭 헤어라인), 다크 패널 장 오프너,
// 번호열 목차, 다크 콘솔 코드블록, wash 인용·표 헤더·h2 액센트바.
// 팩별 색은 tokens.colors의 panel/wash/accent로 조정 — 토큰 없는 팩은
// 디폴트 팔레트로 폴백한다. 하이픈 키(ink-mute 등)는 .at() 접근.
#let tokens = json("tokens.json")
#let mm(n) = n * 1mm
#let pt(n) = n * 1pt
#let em(n) = n * 1em

// klic-flat-dark — 코드 블록 전용 syntect 테마(templates/klic-flat-dark.tmTheme,
// build.py가 build/로 복사). typst 0.15.1 실측: bytes 임베드는 무시되고
// 파일 경로만 유효하며, 테마 전역 foreground는 plain 토큰에 안 닿는다 —
// scope "source" 접두 매칭으로 언어 펜스 전체를 단색 평탄화한다.
// 무언어 펜스는 아래 블록 raw show의 set text(fill)이 담당.

// 장번호(2자리) — 오프너·목차 공용. numbering 없는 heading 내장 counter는
// show 규칙 시점에 0(essay 실측)이라 H1 show에서 step하는 전용 카운터로
// 계산한다(essay theme와 동일 패턴).
#let _ch = counter("klic-chapter")
#let _rank1(el) = context {
  let n = _ch.at(el.location()).first()
  if n < 10 { "0" + str(n) } else { str(n) }
}

// 머리말 좌측 단축제목 — build.py가 tokens.book.short로 주입.
#let _book-short() = {
  tokens.at("book", default: none).at("short", default: "BOOK")
}

#let base(body) = {
  set page(
    width: mm(tokens.trim.width_mm),
    height: mm(tokens.trim.height_mm),
    margin: (top: mm(tokens.margin.top_mm), bottom: mm(tokens.margin.bottom_mm),
             left: mm(tokens.margin.inner_mm), right: mm(tokens.margin.outer_mm)),
    // 러닝헤드 — 좌: 단축제목(트래킹), 우: 현재 장 제목, 전폭 헤어라인.
    // 구판 @page @top-left/@top-right + border-bottom 이식. 표지는
    // make-cover가 margin 0·header none으로, 차례 면은 선행 H1이 없어
    // 비고, 장 오프너 면은 제목과 중복되지 않도록 억제된다.
    header: context {
      let cur = here().page()
      let h1s = query(heading.where(level: 1))
      let opener = h1s.any(h => h.location().page() == cur)
      let prior = h1s.filter(h => h.location().page() < cur)
      if prior.len() > 0 and not opener [
        #set text(size: pt(tokens.fonts.label.size_pt),
          fill: rgb(tokens.colors.at("ink-mute")))
        #grid(columns: (1fr, auto), align: (left + horizon, right + horizon),
          text(tracking: 1.2pt)[#upper(_book-short())],
          [#prior.last().body])
        #v(2.5pt)
        #line(length: 100%, stroke: 0.45pt + rgb(tokens.colors.rule))
      ]
    },
    footer: context align(center)[#text(size: pt(tokens.fonts.label.size_pt),
      fill: rgb(tokens.colors.at("ink-mute")))[#counter(page).display("1")]],
  )
  set text(font: tokens.fonts.body.stack, size: pt(tokens.fonts.body.size_pt),
    lang: "ko", region: "kr", fill: rgb(tokens.colors.ink))
  set par(leading: em(tokens.leading_em), justify: true)

  // 디스플레이 수식 — 급진(√)·분수 기호 잉크가 라인 박스를 8.9pt 초과해
  // 올라간다. 면 상단에 배치되면 G1 프레임 초과(ai-agent p218 실측)이므로
  // 블록 수식에 상단 패드로 상습 방어. 인라인 수식은 해당 없음.
  show math.equation.where(block: true): it => pad(top: 9pt, bottom: 1pt, it)

  // 그림 캡션의 번호는 원고가 붙인다("그림 2-1 …" — 장-일련 체계).
  // typst 자동 번호("그림 2:")를 그대로 두면 이중 번호가 된다
  // (skill-state-ko 캡션 도입 실측). 표는 #table이라 영향 없음.
  set figure(numbering: none)

  // 헤딩은 양쪽정렬 대상이 아니다 — justify를 상속하면 여러 줄 제목에서
  // 공백·제로폭공백이 늘어나 안쪽여백을 침범한다(실전시스템설계 ch20
  // 실측 +3.2pt). theme의 헤딩 오버라이드와도 조합된다.
  show heading: set par(justify: false)

  // 코드(raw) — mono 스택 + body 폴백. 미지정 시 typst 기본 DejaVu Sans
  // Mono로 렌더링되고 코드 내 한글이 Unifont 마지막 폴백으로 떨어져
  // 폰트 계약(G2) 위반이 된다(실전시스템설계 코드 블록 실측).
  show raw: set text(font: tokens.fonts.at("mono", default: tokens.fonts.body).stack
    + tokens.fonts.body.stack)
  // 구문 강조 — klic-flat-dark 테마(모든 토큰 무장식 단색 #E8EEF3).
  // typst 기본 라이트 테마의 어두운 토큰색은 다크 배경(panel) 위에서
  // 읽히지 않는다(2026-08 사용자 지적). 범용 다크 테마는 italic 코멘트가
  // 변형 폰트를 임베드해 G2 계약이 깨진다.
  set raw(theme: "klic-flat-dark.tmTheme")

  // 코드 블록 상자 — 구판 pre{#101D28/#E8F0F3} 다크 콘솔 이식. 산문과의
  // 구분은 배경 명도차가 담당(2026-08 사용자 지적: 회색 물탄색은 퇴보).
  // 행간은 본문 leading_em을 물려받으면 코드가 아래로 퍼져 보이므로
  // 블록 안에서만 조이고, 글자도 표 계열보다 1pt 더 줄여 콘솔 밀도를 낸다.
  show raw.where(block: true): it => block(
    width: 100%, fill: rgb(tokens.colors.at("panel", default: "#101D28")),
    radius: 3pt, inset: (x: 8pt, y: 7pt))[
      #set par(leading: 0.65em)
      // fill은 무언어 펜스용 — 언어 펜스는 테마 토큰색(단색)이 우선.
      #set text(size: pt(tokens.fonts.body.size_pt - 2.5), fill: rgb("#E8EEF3"))
      #it
    ]
  // 인라인 코드(`...`) — 같은 계열 칩이되 box가 아니라 highlight로.
  // box는 내용이 줄바꿈이 안 돼 원고의 긴 인라인 코드(한국어 문장을
  // 백틱에 통째로 싼 경우, ai-agent-book ch9·ch10 — 연속 #quote가 한
  // 문단으로 병합되는 typst 기본 동작과 만나)가 프레임 밖으로 60pt+
  // 돌출한다(실측 2026-08). highlight는 채움이 줄바꿈을 따라간다.
  show raw.where(block: false): it => highlight(
    fill: rgb(tokens.colors.at("wash", default: "#EFF3F4")), radius: 2pt,
    extent: 2.5pt, it)

  // 인용구 — 구판 blockquote{wash 배경 + cyan-dark 좌변} 이식.
  // 병합된 인용 문단도 하나의 블록으로 감싸져 시각 경계가 생긴다.
  show quote: it => block(width: 100%,
    fill: rgb(tokens.colors.at("wash", default: "#EFF3F4")),
    stroke: (left: 2.4pt + rgb(tokens.colors.accent)), radius: 2pt,
    inset: (top: 8pt, bottom: 8pt, left: 12pt, right: 10pt), it)

  // 표(md 파이프 표 → md2typst #table). 구판 editorial 표 이식 —
  // 헤더 wash 배경 + 상단 액센트 1.1pt, 본문 행 바닥 헤어라인만(세로선
  // 없음). 전폭(width: 100%)과 1fr 균등 열·table.header(첫 행)는 md2typst가.
  set table(inset: (x: 7pt, y: 5pt),
    stroke: (x, y) => if y == 0 {
        (top: 1.1pt + rgb(tokens.colors.accent),
         bottom: 0.5pt + rgb(tokens.colors.rule))
      } else {
        (bottom: 0.5pt + rgb(tokens.colors.rule))
      },
    fill: (x, y) => if y == 0 { rgb(tokens.colors.at("wash", default: "#EFF3F4")) }
      else if calc.even(y) {
        rgb(tokens.colors.at("wash", default: "#EFF3F4")).lighten(70%)
      } else { none })
  // 표 글자는 본문보다 1.5pt(≈2px) 작게 — 표가 본문 산문과 같은 크기면
  // 행이 촘촘해져 페이지를 누른다(사용자 지시).
  show table.cell: set text(size: pt(tokens.fonts.body.size_pt - 1.5))
  show table.cell.where(y: 0): set text(weight: "bold")

  // 장 오프너 — 구판 chapteropener(네이비 전면 + eyebrow + 고스트 번호 +
  // 백색 제목 + 하단 액센트 바) 이식. 본문은 다음 면에서 시작한다.
  show heading.where(level: 1): it => {
    pagebreak(weak: true)
    // 무번호 H1 — <part>(제N부 divider)·<nonum>(프롤로그·에필로그 등 부속 장)는
    // 장번호 카운터에서 제외. md2typst 8.2가 라벨을 붙인다. heading 요소에는
    // label 필드가 없어 query+location으로 자기 라벨을 확인한다.
    let here-loc = it.location()
    let is-part = query(label("part")).any(h => h.location() == here-loc)
    let is-nonum = query(label("nonum")).any(h => h.location() == here-loc)
    if not is-part and not is-nonum { _ch.update(n => n + 1) }
    let eyebrow = if tokens.at("label-top") != "" { tokens.at("label-top") }
                  else if is-part { "PART" }
                  else { "CHAPTER" }
    page(margin: 0pt, fill: rgb(tokens.colors.at("panel", default: "#101D28")),
      header: none, footer: none)[
      #place(bottom + left,
        dx: mm(tokens.margin.inner_mm + 4), dy: -mm(20))[
        #rect(width: mm(30), height: mm(1.4),
          fill: rgb(tokens.colors.accent), radius: 1pt)]
      #pad(top: mm(tokens.margin.top_mm + 8), bottom: mm(24),
           left: mm(tokens.margin.inner_mm + 4),
           right: mm(tokens.margin.outer_mm + 4))[
        #text(size: pt(tokens.fonts.label.size_pt), tracking: 2pt,
          fill: rgb(tokens.colors.accent))[#upper(eyebrow)]
        #v(9mm)
        // 고스트 장번호 — 백색 16% 대형 숫자(구판 .number 46pt).
        // 무번호 H1은 숫자 대신 제목만.
        #if not is-part and not is-nonum [
          #text(size: pt(tokens.fonts.heading1.size_pt * 2.1), weight: "bold",
            fill: rgb(255, 255, 255, 16%))[#_rank1(it)]
          #v(7mm)
        ]
        #text(size: pt(tokens.fonts.heading1.size_pt), weight: "bold",
          fill: white)[#it.body]
      ]
    ]
  }
  // 절 헤딩 — 구판 h2{좌 액센트바 2.3pt + 들여쓰기} 이식. 상단 3.5pt 패드는
  // 페이지 상단 v-붕괴 시 Pretendard/SUIT 어센더 잉크가 body_frame 위로
  // 넘는 G1 오버플로 방어(기존 팩에서 이월).
  show heading.where(level: 2): it => {
    v(1.0em)
    block(width: 100%, stroke: (left: 2.3pt + rgb(tokens.colors.accent)),
      inset: (top: 3.5pt, bottom: 0pt, left: 8pt, right: 0pt))[
      #text(size: pt(tokens.fonts.heading2.size_pt), weight: "bold",
        fill: rgb(tokens.colors.ink))[#it.body]]
    v(0.4em)
  }
  show heading.where(level: 3): it => {
    v(0.8em)
    pad(top: 3.5pt)[#text(size: pt(tokens.fonts.heading2.size_pt - 1),
      weight: "bold", fill: rgb(tokens.colors.at("ink-soft")))[#it.body]]
    v(0.3em)
  }

  body
}

// 표지(타이포그래픽 기본형 — theme.typ가 오버라이드)
#let make-cover(title, subtitle, author, cover: none) = {
  // 표지엔 러닝헤드·쪽번호가 없다 — 전역 footer를 이 면에서만 끈다.
  page(margin: 0pt, header: none, footer: none)[
    #if cover != none [#cover] else [
      #v(mm(tokens.trim.height_mm * 0.30))
      #align(left)[
        #text(size: pt(tokens.fonts.heading1.size_pt), weight: "bold")[#title]
        #v(0.8em)
        #text(size: pt(tokens.fonts.heading2.size_pt), fill: rgb(tokens.colors.at("ink-soft")))[#subtitle]
        #v(1.6em)
        #text(size: pt(tokens.fonts.label.size_pt))[#author]
      ]
    ]
  ]
}

// 목차 — 구판 .toc 이식: 대형 제목 + 잉크 하단선, 항목별 헤어라인,
// 액센트 2자리 장번호열, 소절은 소형 뮤트. link()는 SVG 내보내기에서
// 글자보다 큰 투명 히트영역을 만들어 인접 엔트리와 collision 오탐을
// 유발하므로 쓰지 않는다(essay 실측 이관 — 프린트 우선).
#let make-toc() = {
  // 목차 엔트리 재구성 — 기본 점선 리더 대신 번호열·헤어라인 레이아웃.
  // show 규칙은 선언 이후 콘텐츠에만 적용되므로 page 블록 앞에 둔다.
  show outline.entry.where(level: 1): it => {
    v(1.0em, weak: true)
    line(length: 100%, stroke: 0.5pt + rgb(tokens.colors.rule))
    v(0.55em)
    // 무번호 H1(파트·프롤로그 등)은 번호열을 비운다 — 카운터가 아직
    // 올라가지 않아 엉터리 값(00·직전 장 번호)이 찍힌다(설득의 구조 실측).
    let here-loc = it.element.location()
    let unnum = query(label("part")).any(h => h.location() == here-loc) or query(label("nonum")).any(h => h.location() == here-loc)
    let rank1txt = if unnum { none } else { _rank1(it.element) }
    // 다음 면 첫 엔트리에서 Pretendard-Bold 어센더 잉크가 프레임 상단을
    // 3.1pt 넘는다(ai-agent 목차 p3 실측) — h2와 동일 패드 방어.
    pad(top: 3.5pt)[#grid(columns: (14mm, 1fr, auto), column-gutter: 3mm,
      align: (right + horizon, left + horizon, right + horizon),
      text(size: pt(tokens.fonts.heading1.size_pt * 0.62), weight: "bold",
        fill: rgb(tokens.colors.accent))[#rank1txt],
      text(size: pt(tokens.fonts.body.size_pt + 0.8), weight: "bold")[#it.element.body],
      text(fill: rgb(tokens.colors.at("ink-mute")))[
        #context str(counter(page).at(it.element.location()).first())])]
  }
  show outline.entry.where(level: 2): it => {
    v(0.15em, weak: true)
    pad(top: 3.5pt)[#grid(columns: (14mm, 1fr, auto), column-gutter: 3mm,
      align: (right, left + horizon, right + horizon),
      [],
      text(size: pt(tokens.fonts.body.size_pt - 1.5),
        fill: rgb(tokens.colors.at("ink-mute")))[#it.element.body],
      text(size: pt(tokens.fonts.body.size_pt - 1.5),
        fill: rgb(tokens.colors.at("ink-mute")))[
        #context str(counter(page).at(it.element.location()).first())])]
  }
  page[
    #v(0.4em)
    #text(size: pt(tokens.fonts.heading1.size_pt), weight: "bold")[차례]
    #v(0.5em)
    #line(length: 100%, stroke: 1.2pt + rgb(tokens.colors.ink))
    #v(0.9em)
    // title: none — outline 기본 제목이 lang별 헤딩으로 붙어 H1 규칙과
    // 중복 렌더링되므로(make-toc가 직접 제목을 냄) 억제.
    #outline(title: none, indent: 1.5em, depth: tokens.at("toc_depth", default: 1))
  ]
}
