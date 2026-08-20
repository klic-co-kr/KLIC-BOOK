#import "base.typ": tokens, pt

// practical — 신국판 IT 실용서. 명조 본문 + 고딕 제목 + navy 액센트.
// main.typ의 `#show: theme`로 적용 — base 이후에 적용되어 base 헤딩을 오버라이드.
// 하이픈 키(label-top, ink-mute 등)는 .at() 접근 — 마이너스 파싱 방지.
#let theme(body) = {
  // 러닝헤드 — 해당 면이 속한 장(H1) 제목. 표지·차례 직후 첫 장 앞 면은
  // 컨텍스트 헤딩이 없어 빈 값이 된다(의도).
  show: set page(header: context {
    let cur = here().page()
    let hs = query(heading.where(level: 1)).filter(h => h.location().page() <= cur)
    // 장 오프너 면(이 면에서 시작한 H1 존재)은 헤더 없음 — 제목과 중복.
    let opener = query(heading.where(level: 1)).any(h => h.location().page() == cur)
    if hs.len() > 0 and cur > 4 and not opener [
      #set text(size: pt(tokens.fonts.label.size_pt),
        fill: rgb(tokens.colors.at("ink-mute")))
      #align(right)[
        #hs.last().body
        #h(0.6em)
        #v(-0.15em)
        #box(width: 8mm, height: 0.4pt, fill: rgb(tokens.colors.accent))
      ]
    ]
  })
  show heading.where(level: 1): it => {
    pagebreak(weak: true)
    v(3.5em)
    block(width: 100%)[
      #if tokens.at("label-top") != "" [
        #text(size: pt(tokens.fonts.label.size_pt), tracking: 1.5pt,
          fill: rgb(tokens.colors.accent))[#upper(tokens.at("label-top"))]
        #v(0.5em)
      ]
      #box(width: 16mm, height: 2.2pt, fill: rgb(tokens.colors.accent))
      #v(0.8em)
      #text(size: pt(tokens.fonts.heading1.size_pt), weight: "bold",
        fill: rgb(tokens.colors.ink))[#it.body]
      #v(0.6em)
      #line(length: 100%, stroke: 0.4pt + rgb(tokens.colors.rule))
    ]
    v(2.2em)
  }
  show heading.where(level: 2): it => {
    v(1.1em)
    // Pretendard 어센더가 em박스를 초과해 페이지 상단 v-붕괴 시 잉크가
    // body_frame 위로 3.3pt 넘는다(G1 ±3pt 초과). 상단 패드로 상습 방지.
    pad(top: 3.5pt)[#text(size: pt(tokens.fonts.heading2.size_pt), weight: "bold",
      fill: rgb(tokens.colors.accent))[#it.body]]
    v(0.4em)
  }
  body
}
