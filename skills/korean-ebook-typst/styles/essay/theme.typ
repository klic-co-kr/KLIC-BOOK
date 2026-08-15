#import "base.typ": tokens, pt, mm, em

// essay — 사륙판 미니멀 에세이. 여백 낙차형 장 시작(bookforge essay 계승 적응).
// main.typ의 `#show: theme`로 적용 — base 이후에 적용되어 base 헤딩을 오버라이드.
// typst 0.15.1 실측: numbering 없는 heading 내장 counter는 show 규칙 시점에
// 아직 0이다(프로브: 00/00/00). 전용 카운터를 step해 2자리 장번호를 낸다.
#let chapter-counter = counter("essay-chapter")

#let theme(body) = {
  set page(fill: rgb(tokens.colors.paper))
  show heading.where(level: 1): it => {
    pagebreak(weak: true)
    chapter-counter.update(n => n + 1)
    // 판면 상단에서 52mm 낙차 — base가 이미 띄운 top margin은 차감
    v(mm(52) - mm(tokens.margin.top_mm))
    text(size: pt(tokens.fonts.label.size_pt),
      fill: rgb(tokens.colors.accent))[#context chapter-counter.display("01")]
    v(mm(3))
    // H1 15pt Regular — 굵기 없음(위계는 크기·여백으로만)
    text(size: pt(tokens.fonts.heading1.size_pt), weight: "regular",
      fill: rgb(tokens.colors.ink))[#it.body]
    v(mm(19) - em(4))
  }
  show heading.where(level: 2): it => {
    v(em(1.5))
    text(size: pt(tokens.fonts.heading2.size_pt),
      weight: "medium")[#it.body]
    v(em(0.5))
  }
  body
}
