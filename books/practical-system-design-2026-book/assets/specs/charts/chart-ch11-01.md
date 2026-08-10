---
id: chart-ch11-01
chapter: ch11
kind: data-chart
generator: python-matplotlib
status: specified
synthetic: true
output: assets/charts/chart-ch11-01.svg
data_file: data/chart-ch11-01.csv
source_file: assets/src/charts/chart-ch11-01.py
---

# chart-ch11-01 — 차트 제작 명세

## 목적

평균 QPS는 같아도 hot tenant 때문에 상위 shard가 과부하되는 분포를 보여준다.

## 축과 계열

- X축: Shard ID
- Y축: QPS
- 계열:
  - 균등 분포
  - Skew 분포

## 데이터 성격

파티션 skew 설명용 synthetic chart.

이 차트에는 실제 서비스의 성능값을 임의로 넣지 않는다. 예시 데이터는 `synthetic: true`로 표시하고, 산식 또는 생성 규칙을 CSV와 Python script에 함께 기록한다. 실제 측정값으로 교체할 경우 환경, 날짜, hardware, software version, sample 수, warm-up, 오류 범위를 manifest에 추가한다.

## 시각화 규칙

- matplotlib를 사용하고 SVG로 출력한다.
- 하나의 차트만 사용하며 subplot을 만들지 않는다.
- 축 단위·범례·데이터 출처·synthetic 표기를 명확히 한다.
- 0을 잘라 오해를 만드는 축이나 장식용 3D 효과를 금지한다.
- 색상만으로 계열을 구분하지 않고 선 모양·marker·직접 라벨을 함께 사용한다.
- 본문 흑백 인쇄에서도 읽혀야 한다.

## 대체 텍스트

평균 QPS는 같아도 hot tenant 때문에 상위 shard가 과부하되는 분포를 보여준다.

## 검수 체크리스트

- [ ] 계산식과 CSV가 재현 가능하다.
- [ ] 단위와 synthetic 여부가 그림 안 또는 caption에 표시된다.
- [ ] 본문 설명과 축 방향이 모순되지 않는다.
- [ ] 숫자를 실제 벤치마크처럼 오해하게 하지 않는다.
