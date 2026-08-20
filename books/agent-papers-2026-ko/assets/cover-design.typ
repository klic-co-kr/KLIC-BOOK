// 표지 디자인 — 많이 줄수록, 여럿일수록 정말 더 잘할까 (210×297 A4 lecture)
#set page(width: 210mm, height: 297mm, margin: 0pt)
#set text(font: ("Noto Sans KR", "Noto Serif CJK KR"), lang: "ko")

#let navy = rgb("16283F")
#let navy-deep = rgb("0F1C2E")
#let accent = rgb("4A9EDA")
#let accent-soft = rgb("2E5E8C")

// 배경 — 심해 네이비
#place(top + left, rect(width: 100%, height: 100%, fill: navy))

// 배경 모티프 — 에이전트 네트워크 노드·엣지 (우하단)
#place(bottom + right, dx: -26mm, dy: 40mm)[
  #{
    let nodes = ((0mm, 0mm, 6mm), (28mm, 10mm, 4mm), (13mm, 30mm, 7mm),
                 (40mm, 38mm, 5mm), (3mm, 43mm, 4mm), (30mm, 58mm, 6mm),
                 (55mm, 23mm, 4mm), (8mm, 65mm, 4.5mm), (48mm, 70mm, 5mm),
                 (62mm, 52mm, 3.5mm))
    for (a, b) in ((0,1), (0,2), (1,2), (1,3), (2,4), (2,5), (3,5), (3,6),
                   (5,7), (5,8), (1,6), (4,7), (8,3), (8,9), (6,9)) {
      let (xa, ya, _) = nodes.at(a)
      let (xb, yb, _) = nodes.at(b)
      place(dx: xa + nodes.at(a).at(2), dy: ya + nodes.at(a).at(2),
            line(end: (xb - xa, yb - ya),
                  stroke: (paint: accent-soft, thickness: 0.6pt, cap: "round")))
    }
    for (x, y, r) in nodes {
      place(dx: x, dy: y, circle(radius: r, fill: rgb(74%, 82%, 92%, 18%), stroke: accent + 0.8pt))
    }
  }
]

// 상단 여백 기둥
#place(top + left, dy: 34mm, dx: 24mm)[
  #box(width: 14mm, height: 1.2pt, fill: accent)
]

// 시리즈 라벨
#place(top + left, dy: 39mm, dx: 24mm)[
  #text(size: 11pt, fill: rgb("8FB4D4"), tracking: 2.6pt, weight: "medium")[AGENT PAPERS · 2026.08]
]

// 주제목 — 3행
#place(top + left, dy: 66mm, dx: 24mm)[
  #text(size: 44pt, fill: white, weight: "bold")[많이 줄수록, 여럿일수록#linebreak()정말 더 잘할까]
]

// 부제
#place(top + left, dy: 128mm, dx: 24mm)[
  #text(size: 15pt, fill: rgb("C9D8E6"))[에이전트 논문 10편 읽기#linebreak()alphaXiv 2026년 8월 피드 · 153편에서 고른 10편]
]

// 액센트 롤룰
#place(top + left, dy: 172mm, dx: 24mm)[
  #box(width: 162mm, height: 0.5pt, fill: accent-soft)
]

// 네 가지 질문 요약
#place(top + left, dy: 182mm, dx: 24mm)[
  #text(size: 12pt, fill: rgb("AEBFD0"))[
    · A. 무엇을, 얼마나 줄 것인가 — 하네스 · 상태 · 작업공간#linebreak()· B. 얼마나 쪼갤 것인가 — 경계의 거버넌스 · 조율 비용#linebreak()· C. 무엇을 기억할 것인가 — 기억의 형태와 정책#linebreak()· D. 어떻게 잴 것인가 — 프롬프트의 값 · 과정 지표 · 명세
  ]
]

// 하단 — 저자·발행 정보
#place(bottom + left, dy: -30mm, dx: 24mm)[
  #text(size: 11pt, fill: rgb("9FB2C6"))[논문 alphaXiv 각 저자 · 해설 KLIC]
]
#place(bottom + left, dy: -21mm, dx: 24mm)[
  #text(size: 10pt, fill: rgb("6E8299"), tracking: 1pt)[한국어판 KLIC · 2026]
]
