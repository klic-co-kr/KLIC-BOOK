// 표지 디자인 — 시스템 디자인 인터뷰 핵심 노트 (153×225 신국판)
#set page(width: 153mm, height: 225mm, margin: 0pt)
#set text(font: ("Noto Sans KR", "Noto Serif CJK KR"), lang: "ko")

#let navy = rgb("16283F")
#let navy-deep = rgb("0F1C2E")
#let accent = rgb("4A9EDA")
#let accent-soft = rgb("2E5E8C")

// 배경 — 심해 네이비, 하단으로 갈수록 어둡게
#place(top + left, rect(width: 100%, height: 100%, fill: navy))

// 배경 모티프 — 분산 시스템 노드·엣지 (우하단, 은은하게)
#place(bottom + right, dx: -18mm, dy: 30mm)[
  #{
    let nodes = ((0mm, 0mm, 5mm), (22mm, 8mm, 3.5mm), (10mm, 24mm, 6mm),
                 (32mm, 30mm, 4mm), (2mm, 34mm, 3mm), (24mm, 46mm, 5mm),
                 (44mm, 18mm, 3mm), (6mm, 52mm, 3.5mm), (38mm, 56mm, 4mm))
    // 엣지
    for (a, b) in ((0,1), (0,2), (1,2), (1,3), (2,4), (2,5), (3,5), (3,6),
                   (5,7), (5,8), (1,6), (4,7), (8,3)) {
      let (xa, ya, _) = nodes.at(a)
      let (xb, yb, _) = nodes.at(b)
      place(dx: xa + nodes.at(a).at(2), dy: ya + nodes.at(a).at(2),
            line(end: (xb - xa, yb - ya),
                  stroke: (paint: accent-soft, thickness: 0.6pt, cap: "round")))
    }
    // 노드
    for (x, y, r) in nodes {
      place(dx: x, dy: y, circle(radius: r, fill: rgb(74%, 82%, 92%, 18%), stroke: accent + 0.8pt))
    }
  }
]

// 상단 여백 기둥
#place(top + left, dy: 26mm, dx: 18mm)[
  #box(width: 12mm, height: 1.2pt, fill: accent)
]

// 시리즈 라벨
#place(top + left, dy: 30mm, dx: 18mm)[
  #text(size: 10pt, fill: rgb("8FB4D4"), tracking: 2.4pt, weight: "medium")[SYSTEM DESIGN NOTES]
]

// 주제목 — 3행
#place(top + left, dy: 52mm, dx: 18mm)[
  #text(size: 34pt, fill: white, weight: "bold")[시스템 디자인#linebreak()인터뷰 핵심 노트]
]

// 부제
#place(top + left, dy: 108mm, dx: 18mm)[
  #text(size: 12pt, fill: rgb("C9D8E6"))[Alex Xu 『System Design Interview』#linebreak()Vol.1·2 학습 노트 한국어판]
]

// 액센트 롤룰
#place(top + left, dy: 138mm, dx: 18mm)[
  #box(width: 117mm, height: 0.5pt, fill: accent-soft)
]

// 챕터 구성 요약
#place(top + left, dy: 146mm, dx: 18mm)[
  #text(size: 10.5pt, fill: rgb("AEBFD0"))[
    · 규모 확장과 개략적 추정, 설계 프레임워크#linebreak()· 처리율 제한 · 일관성 해시 · 키-값 저장소#linebreak()· URL 단축기부터 주식 거래소까지 28개 설계 사례
  ]
]

// 하단 — 저자·발행 정보
#place(bottom + left, dy: -24mm, dx: 18mm)[
  #text(size: 10pt, fill: rgb("9FB2C6"))[원작 Alex Xu · 노트 liquidslr]
]
#place(bottom + left, dy: -16mm, dx: 18mm)[
  #text(size: 9pt, fill: rgb("6E8299"), tracking: 1pt)[한국어판 KLIC · 2026]
]
