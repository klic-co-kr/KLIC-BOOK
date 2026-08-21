// templates/infographic/helper.typ — 인포그래픽 공통 프리미티브(스펙 §4.2·§5.1).
// 색은 역할명만 받는다. hex는 tokens.json이 SSoT.
// 검증 이력(적대 검토 실측): pt() 셤·place 앵커 절대좌표 환산·open-V 절대 대각선 —
// typst 0.15.1 실컴파일 + PyMuPDF 좌표 실측으로 교정된 형태다. 임의 수정 금지.
#let tokens = json("tokens.json")
#let pt(n) = n * 1pt

#let ig-color(role) = {
  if tokens.colors.at(role, default: none) != none { rgb(tokens.colors.at(role)) }
  else { rgb(tokens.infographic.at(role)) }
}

#let ig-figure(w, h, body) = block(
  width: pt(w), height: pt(h), breakable: false, clip: true,
  stroke: none, inset: 0pt,
)[#box(width: 100%, height: 100%)[#body]]

// rect — place(top+left)는 박스 좌상단을 (x,y)에 놓는다(실측 정확).
#let ig-rect(x, y, w, h, rx: 8pt, fill-role: "surface-tint",
             stroke-role: "rule", stroke-w: 0.5pt) = place(
  top + left, dx: pt(x), dy: pt(y),
  rect(width: pt(w), height: pt(h), radius: rx,
       fill: ig-color(fill-role),
       stroke: if stroke-w == 0pt { none } else {
         (paint: ig-color(stroke-role), thickness: stroke-w) }),
)

// text — x,y는 텍스트 블록 중심의 절대좌표, fw·fh는 도식 전체 폭·높이.
// place(center+horizon)는 "컨테이너 중심 + (dx,dy)"에 블록 중심을 놓는다(실측:
// raw dx 전달 시 전 텍스트가 (+W/2, +H/2) 치우침). 절대좌표 (x,y)에 놓으려면
// dx = x − fw/2, dy = y − fh/2 를 전달해야 한다 — emit이 항상 이 환산을 수행한다.
#let ig-text(x, y, fw, fh, size, role, weight: "regular", body) = place(
  center + horizon, dx: pt(x - fw / 2), dy: pt(y - fh / 2),
  box(inset: 0pt)[#set par(leading: 1.3em)
    #text(size: pt(size), fill: ig-color(role),
          weight: if weight == "bold" { "bold" } else { "regular" })[#body]],
)

// arrow — 샤프트(상대 종점) + open-V 헤드(tip에서 뒤꿈치±수직 날개, 절대 대각선).
// 초판의 벡터식은 대수적으로 퇴화해 수평 화살표가 0-길이 선이 됐다(실측) —
// 아래 "tip에서 날개 끝점으로" 상대 벡터 형태가 실측 교정본이다.
#let ig-arrow(x1, y1, x2, y2, style: "solid") = {
  let stroke = (paint: ig-color("ink-soft"), thickness: 1.2pt,
                dash: if style == "dashed" { "dashed" } else { none })
  place(top + left, dx: pt(x1), dy: pt(y1),
        line(end: (pt(x2 - x1), pt(y2 - y1)), stroke: stroke))
  let dx = x2 - x1
  let dy = y2 - y1
  let len = calc.sqrt(dx * dx + dy * dy)
  let ux = dx / len
  let uy = dy / len
  let hw = 4.0                                  // ARROW_HEAD_W — 비율 4.0/1.2 = 3.33
  let bx = x2 - ux * hw                         // 뒤꿈치(shaft 방향 hw 뒤)
  let by = y2 - uy * hw
  let px = -uy                                  // 단위 수직벡터
  let py = ux
  place(top + left, dx: pt(x2), dy: pt(y2),     // 날개 1: tip → heel + perp·hw/2
        line(end: (pt(bx + px * hw / 2 - x2), pt(by + py * hw / 2 - y2)), stroke: stroke))
  place(top + left, dx: pt(x2), dy: pt(y2),     // 날개 2: tip → heel − perp·hw/2
        line(end: (pt(bx - px * hw / 2 - x2), pt(by - py * hw / 2 - y2)), stroke: stroke))
}
