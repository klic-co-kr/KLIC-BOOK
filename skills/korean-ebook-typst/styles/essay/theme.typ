#import "base.typ": tokens, pt, mm, em

// essay — 46판(B6) 미니멀 에세이. 여백 낙차형 장 시작.
// main.typ의 `#show: theme`로 적용 — base 이후에 적용되어 base 헤딩을 오버라이드.
// typst 0.15.1 실측: numbering 없는 heading 내장 counter는 show 규칙 시점에
// 아직 0이다(프로브: 00/00/00). 전용 카운터를 step해 2자리 장번호를 낸다.
#let chapter-counter = counter("essay-chapter")

#let theme(body) = {
  set page(fill: rgb(tokens.colors.paper))
  // 목차 리더 점선 금지 — outline.entry 필드는 level/element/fill뿐(0.15.1
  // 실측)이라 엔트리를 재구성한다: 제목 + 1fr + 쪽수. link()는 SVG 내보내기에서
  // 글자보다 큰 투명 히트영역 rect(26pt)를 만들어 인접 엔트리와 P0 collision
  // 오탐을 유발하므로 쓰지 않는다(프린트 우선 46판(B6) — TOC 하이퍼링크 포기).
  show outline.entry: it => {
    v(2.5pt, weak: true)
    box(width: 100%)[
      #it.element.body
      #h(1fr)
      #context str(counter(page).at(it.element.location()).first())
    ]
  }
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
    // 페이지 상단에서 선행 v는 면 경계에서 소멸한다(weak 불문 — strong로도
    // 실측 불변). SUIT 계열 어센더 잉크가 프레임 상단을 2.7pt 넘어 G1
    // 오버플로가 되므로 상단 패드로 방어(b5/practical과 동일 패턴).
    pad(top: 3.5pt)[#text(size: pt(tokens.fonts.heading2.size_pt),
      weight: "medium")[#it.body]]
    v(em(0.5))
  }
  body
}
