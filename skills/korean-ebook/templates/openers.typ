// templates/openers.typ — 장 오프너 변조 기본값(비활성).
// base.typ가 무조건 import하므로 이 파일이 항상 함께 존재해야 한다.
// build.py는 조립 시 이 파일을 덮어써 책별 프로파일(openers 배열)을 내놓는다.
#let opener-enabled = false
#let opener-paper = none
#let opener-brand = none
#let openers = ()
