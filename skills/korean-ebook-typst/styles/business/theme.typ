#import "base.typ": tokens, pt, em

// business — 컨설팅 백서 200×280. navy 시스템 + 액션 타이틀 헤딩.
// main.typ의 `#show: theme`로 적용 — base 이후에 적용되어 base 헤딩을 오버라이드.
// 하이픈 키(label-top, ink-mute 등)는 .at() 접근 — 마이너스 파싱 방지.
// label-top은 이미 대문자 SECTION — upper() 없이 직접 렌더.
#let theme(body) = {
  show heading.where(level: 1): it => {
    pagebreak(weak: true)
    v(2em)
    block(width: 100%, inset: (x: 0pt))[
      #text(size: pt(tokens.fonts.label.size_pt), weight: "bold",
        fill: rgb(tokens.colors.accent))[#tokens.at("label-top")]
      #v(0.4em)
      #text(size: pt(tokens.fonts.heading1.size_pt), weight: "bold",
        fill: rgb(tokens.colors.accent))[#it.body]
    ]
    v(1em)
    line(length: 100%, stroke: 2pt + rgb(tokens.colors.accent))
    v(1em)
  }
  show heading.where(level: 2): it => {
    v(1em)
    box(fill: rgb(tokens.colors.accent), inset: (x: 6pt, y: 3pt))[
      #text(size: pt(tokens.fonts.heading2.size_pt), weight: "bold",
        fill: white)[#it.body]
    ]
    v(0.6em)
  }
  body
}
