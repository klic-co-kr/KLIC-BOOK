---
id: fig-ch23-01
chapter: ch23
kind: technical-diagram
generator: direct-svg
status: specified
output: assets/figures/fig-ch23-01.svg
canvas_preset: chapter-wide
aspect_ratio: "16:9"
---

# fig-ch23-01 — SVG 제작 명세

## 목적

effect·ack·crash 순서에 따라 유실·중복이 생기는 세 시나리오를 비교한다.

## 필수 한글 라벨

- Producer
- Broker
- Consumer
- DB/API
- ACK
- Crash
- 중복
- 유실

## 정보 구조

- 장 제목의 개념을 한 장에서 읽을 수 있도록 좌→우 또는 상→하 흐름을 사용한다.
- 각 노드는 책임 단위로 묶고, 동일 계층은 크기와 간격을 일관되게 맞춘다.
- 정상 경로와 실패·복구 경로가 함께 있으면 실선/점선과 범례로 구분한다.
- 출처에 없는 제품명·수치·기관명은 추가하지 않는다.

## 공통 SVG 계약

- 순수 SVG만 사용한다. `<image>`, base64, 외부 URL, JavaScript, 외부 CSS를 금지한다.
- 캔버스는 기본 `viewBox="0 0 1600 900"`, 흰색 배경, 인쇄 친화적인 가로형이다.
- 모든 한글은 실제 `<text>`와 `<tspan>`으로 작성하고 path로 변환하지 않는다.
- `<title>`과 `<desc>`를 포함하고 의미 단위마다 편집 가능한 `<g id="...">` 그룹을 사용한다.
- 화살표는 노드 내부를 통과하지 않고 도형 경계에 정확히 접한다. 교차를 최소화한다.
- 최소 본문 글자 22px, 최소 선 굵기 2px, 충분한 여백을 지킨다.
- 색상만으로 의미를 구분하지 않고 선 모양·라벨·범례를 병행한다.
- 임의 IP, 제품 로고, 회사명, 처리량, 성능 수치를 생성하지 않는다.
- 출력은 설명 없는 완전한 `<svg>...</svg>` 파일이어야 한다.

## 모델에 전달할 완성 프롬프트

```text
Create one production-quality, fully editable SVG technical diagram for a Korean system-design book.

Subject and learning goal:
effect·ack·crash 순서에 따라 유실·중복이 생기는 세 시나리오를 비교한다.

Required Korean labels, written exactly as provided:
- Producer
- Broker
- Consumer
- DB/API
- ACK
- Crash
- 중복
- 유실

Use a clean editorial architecture-diagram style on a white 1600×900 canvas. Establish a strong hierarchy, generous whitespace, consistent rounded cards, precise orthogonal or gently curved connectors, and readable legends. Make the information structure accurate before adding decoration. Clearly separate normal flow, control flow, failure flow and recovery flow when they appear. Do not invent measurements, company names, product logos, IP addresses or implementation claims.

Hard output contract:
- 순수 SVG만 사용한다. `<image>`, base64, 외부 URL, JavaScript, 외부 CSS를 금지한다.
- 캔버스는 기본 `viewBox="0 0 1600 900"`, 흰색 배경, 인쇄 친화적인 가로형이다.
- 모든 한글은 실제 `<text>`와 `<tspan>`으로 작성하고 path로 변환하지 않는다.
- `<title>`과 `<desc>`를 포함하고 의미 단위마다 편집 가능한 `<g id="...">` 그룹을 사용한다.
- 화살표는 노드 내부를 통과하지 않고 도형 경계에 정확히 접한다. 교차를 최소화한다.
- 최소 본문 글자 22px, 최소 선 굵기 2px, 충분한 여백을 지킨다.
- 색상만으로 의미를 구분하지 않고 선 모양·라벨·범례를 병행한다.
- 임의 IP, 제품 로고, 회사명, 처리량, 성능 수치를 생성하지 않는다.
- 출력은 설명 없는 완전한 `<svg>...</svg>` 파일이어야 한다.
```

## 대체 텍스트

effect·ack·crash 순서에 따라 유실·중복이 생기는 세 시나리오를 비교한다.

## 근거

- `kafka-docs` — Apache Kafka Documentation
- `rabbitmq-reliability` — RabbitMQ Reliability Guide
- `kafka-transactions` — Apache Kafka — Design: Transactions

## 검수 체크리스트

- [ ] 필수 라벨이 정확히 한글 텍스트로 존재한다.
- [ ] 화살표 방향이 본문 흐름과 일치한다.
- [ ] 노드 겹침·텍스트 오버플로·선 교차가 없다.
- [ ] 색을 제거해도 의미를 구분할 수 있다.
- [ ] 출처 없는 숫자·제품·브랜드가 없다.
- [ ] `<title>`, `<desc>`, 의미 단위 `<g>`가 있다.
