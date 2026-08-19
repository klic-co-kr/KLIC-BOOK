// templates/base.typ — 공통 프리미티브. 스타일 값은 tokens.json에서.
//
// typst 0.15.1 검증: set/show 규칙은 include된 파일 스코프에만 적용되어
// include만으로는 본문에 스타일이 전파되지 않는다. 따라서 전역 스타일은
// main.typ에서 `#show: base` / `#show: theme` 함수 적용으로 발동한다
// (base가 먼저, theme가 나중 — 나중 규칙이 헤딩을 오버라이드).
#let tokens = json("tokens.json")
#let mm(n) = n * 1mm
#let pt(n) = n * 1pt
#let em(n) = n * 1em

#let base(body) = {
  set page(
    width: mm(tokens.trim.width_mm),
    height: mm(tokens.trim.height_mm),
    margin: (top: mm(tokens.margin.top_mm), bottom: mm(tokens.margin.bottom_mm),
             left: mm(tokens.margin.inner_mm), right: mm(tokens.margin.outer_mm)),
    footer: context align(center)[#text(size: pt(tokens.fonts.label.size_pt),
      fill: rgb(tokens.colors.at("ink-mute")))[#counter(page).display("1")]],
  )
  set text(font: tokens.fonts.body.stack, size: pt(tokens.fonts.body.size_pt),
    lang: "ko", region: "kr", fill: rgb(tokens.colors.ink))
  set par(leading: em(tokens.leading_em), justify: true)

  // 헤딩은 양쪽정렬 대상이 아니다 — justify를 상속하면 여러 줄 제목에서
  // 공백·제로폭공백이 늘어나 안쪽여백을 침범한다(실전시스템설계 ch20
  // 실측 +3.2pt). theme의 헤딩 오버라이드와도 조합된다.
  show heading: set par(justify: false)

  // 코드(raw) — mono 스택 + body 폴백. 미지정 시 typst 기본 DejaVu Sans
  // Mono로 렌더링되고 코드 내 한글이 Unifont 마지막 폴백으로 떨어져
  // 폰트 계약(G2) 위반이 된다(실전시스템설계 코드 블록 실측).
  show raw: set text(font: tokens.fonts.at("mono", default: tokens.fonts.body).stack
    + tokens.fonts.body.stack)

  // 공통 헤딩 — theme.typ의 show 규칙이 뒤에서 오버라이드 가능
  show heading.where(level: 1): it => {
    pagebreak(weak: true)
    v(2em)
    text(size: pt(tokens.fonts.heading1.size_pt), weight: "bold")[#it.body]
    v(1em)
  }
  show heading.where(level: 2): it => {
    v(0.8em)
    text(size: pt(tokens.fonts.heading2.size_pt), weight: "bold")[#it.body]
    v(0.3em)
  }
  body
}

// 표지(타이포그래픽 기본형 — theme.typ가 오버라이드)
#let make-cover(title, subtitle, author, cover: none) = {
  page(margin: 0pt)[
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

// 목차 — toc_depth 토큰(기본 1=장급). 스타일 팩이 절급(2)으로 확장 가능.
#let make-toc() = {
  page[
    #v(0.4em)
    #text(size: pt(tokens.fonts.heading1.size_pt), weight: "bold")[차례]
    #v(1em)
    // title: none — outline 기본 제목이 lang별 헤딩으로 붙어 theme H1 규칙과
    // 중복 렌더링되므로(make-toc가 직접 제목을 냄) 억제.
    #outline(title: none, indent: 1.5em, depth: tokens.at("toc_depth", default: 1))
  ]
}
