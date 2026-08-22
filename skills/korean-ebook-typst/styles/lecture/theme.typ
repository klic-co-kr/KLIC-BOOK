#import "base.typ": tokens, pt

// lecture — A4 강의자료. 레거시 book.typ 헤딩 문법 계승(DAY 라벨 → date 슬롯으로 일반화)
// main.typ의 `#show: theme`로 적용 — base 이후에 적용되어 base 헤딩을 오버라이드.
#let theme(body) = {
  show heading.where(level: 1): it => {
    pagebreak(weak: true)
    v(3em)
    block(width: 100%)[
      #text(size: pt(tokens.fonts.label.size_pt), fill: rgb(tokens.colors.accent))[#tokens.at("label-top")]
      #v(0.3em)
      #text(size: pt(tokens.fonts.heading1.size_pt), weight: "bold")[#it.body]
    ]
    v(1.5em)
  }
  show heading.where(level: 2): it => {
    v(0.8em)
    // 페이지 상단에서 선행 v는 면 경계에서 소멸한다(weak 불문 — strong로도
    // 실측 불변). Pretendard 계열 어센더 잉크가 프레임 상단을 3.2pt 넘어
    // G1 오버플로가 되므로 상단 패드로 방어(b5/practical과 동일 패턴).
    pad(top: 3.5pt)[#text(size: pt(tokens.fonts.heading2.size_pt), weight: "bold",
      fill: rgb(tokens.colors.accent))[#it.body]]
    v(0.3em)
  }
  body
}
