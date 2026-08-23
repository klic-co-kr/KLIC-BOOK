#import "@preview/mitex:0.2.7": mitex

// 페이지: A4, 여백, 헤더·푸터(페이지번호)
#set page(
  paper: "a4",
  margin: (top: 28mm, bottom: 22mm, left: 23mm, right: 23mm),
  footer: context align(center)[#counter(page).display("1")],
)

// 본문: 한국어 CJK 폰트
#set text(
  font: ("Noto Sans CJK KR", "NanumSquare_ac", "NanumGothic", "Noto Sans KR"),
  size: 10pt,
  lang: "ko",
  region: "kr",
)
#set par(leading: 0.85em, justify: true)

// 헤딩 스타일 (장)
#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  v(3em)
  block(width: 100%)[
    #text(size: 9pt, fill: gray)[DAY]
    #v(0.3em)
    #text(size: 20pt, weight: "bold")[#it.body]
  ]
  v(1.5em)
}
#show heading.where(level: 2): it => {
  v(0.8em)
  text(size: 13pt, weight: "bold")[#it.body]
  v(0.3em)
}

// 표지
#page(margin: 0pt)[
  #image("cover.png", width: 100%, height: 100%)
]

// 목차
#page[
  #text(size: 16pt, weight: "bold")[목차]
  #v(1em)
  #outline(indent: 1.5em, depth: 1)
]

// 본문 (day1-8)
#include "typ/day1.typ"
#include "typ/day2.typ"
#include "typ/day3.typ"
#include "typ/day4.typ"
#include "typ/day5.typ"
#include "typ/day6.typ"
#include "typ/day7.typ"
#include "typ/day8.typ"
