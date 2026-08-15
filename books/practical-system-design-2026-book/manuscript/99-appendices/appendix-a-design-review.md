## 부록 A. 시스템 설계 리뷰 체크리스트

### 문제와 경계

- [ ] 핵심 사용자 여정과 비목표가 한 문장으로 설명된다.
- [ ] 데이터별 단일 쓰기 소유자와 원장이 명확하다.
- [ ] 기능, 품질, 규모, 규제, 팀 제약이 분리돼 있다.
- [ ] 정상 경로뿐 아니라 timeout, 중복, 부분 성공, 취소, 복구가 정의돼 있다.

### 수치와 성능

- [ ] 모든 숫자에 단위, 시간 창, 근거, 계산식이 있다.
- [ ] 평균과 피크·burst·p95·p99가 분리돼 있다.
- [ ] 논리 저장량과 복제·색인·로그·백업을 포함한 물리량이 구분된다.
- [ ] 부하 테스트가 실제 key·tenant·payload 분포를 반영한다.

### 데이터와 일관성

- [ ] 불변조건이 DB 제약·상태 기계·reconciliation 중 어디에서 보호되는지 명확하다.
- [ ] read-after-write, staleness, 충돌, idempotency 의미가 API에 드러난다.
- [ ] replica, cache, search index, vector index의 재구축 경로가 있다.
- [ ] schema·model·index version 변경과 rollback이 설계돼 있다.

### 장애와 운영

- [ ] 장애 도메인과 공통 원인 실패가 표시돼 있다.
- [ ] deadline·retry budget·load shedding·degradation이 연결돼 있다.
- [ ] RTO/RPO와 restore/failover/failback의 실제 검증 증거가 있다.
- [ ] SLO와 error budget이 배포·용량·우선순위 정책에 연결돼 있다.

### 보안과 비용

- [ ] 주체·tenant·resource·action·context가 모든 신뢰 경계에서 검증된다.
- [ ] 개인정보가 저장·cache·event·telemetry·backup에 어떻게 복제되는지 추적된다.
- [ ] secret·artifact·관리 권한이 최소화되고 회전·감사된다.
- [ ] 단위당 비용, 운영 인력, 데이터 전송, 탈출 비용이 비교됐다.
