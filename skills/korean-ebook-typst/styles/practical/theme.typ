#import "base.typ": tokens, pt

// practical — 신국판 IT 실용서. 명조 본문 + 고딕 제목 + navy 액센트.
// main.typ의 `#show: theme`로 적용 — base 이후에 적용되어 base 헤딩을 오버라이드.
// 하이픈 키(label-top, ink-mute 등)는 .at() 접근 — 마이너스 파싱 방지.
#let theme(body) = {
  show heading.where(level: 1): it => {
    pagebreak(weak: true)
    v(2.5em)
    block(width: 100%)[
      #if tokens.at("label-top") != "" [
        #text(size: pt(tokens.fonts.label.size_pt),
          fill: rgb(tokens.colors.accent))[#tokens.at("label-top")]
        #v(0.3em)
      ]
      #text(size: pt(tokens.fonts.heading1.size_pt), weight: "bold",
        fill: rgb(tokens.colors.ink))[#it.body]
      #v(0.4em)
      #line(length: 100%, stroke: 0.4pt + rgb(tokens.colors.rule))
    ]
    v(1.5em)
  }
  show heading.where(level: 2): it => {
    v(1em)
    text(size: pt(tokens.fonts.heading2.size_pt), weight: "bold",
      fill: rgb(tokens.colors.accent))[#it.body]
    v(0.4em)
  }
  body
}
