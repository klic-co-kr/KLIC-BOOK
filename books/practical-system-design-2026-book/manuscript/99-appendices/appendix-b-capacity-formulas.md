## 부록 B. 용량 계산 공식

이 부록의 식은 입력이 명시될 때만 의미가 있다. 결과에는 10진/2진 단위, 압축, 복제, 색인, 여유를 별도로 표시한다.

```text
평균 RPS = 하루 요청 수 / 86,400
피크 RPS = 평균 RPS × 관측된 피크 계수
동시성 ≈ 도착률(request/s) × 평균 체류 시간(s)
대역폭(bytes/s) = 요청률 × 평균 전송 bytes
논리 저장량 = 이벤트율 × 객체 bytes × 보존 시간
복제 포함 저장량 = 논리 저장량 × 복제 계수
Cache origin QPS = 전체 QPS × (1 - hit ratio)
비동기 복제 손실 노출 record ≈ 쓰기율 × 복제 지연
Error budget = 관측 창 × (1 - SLO)
계층 재시도 최악 수 = 계층별 시도 수 ^ 호출 깊이
```

실제 capacity는 평균 식에 p99 latency, queue, compaction, rebuild, backup, failover 동시 부하를 더해 검증한다.
