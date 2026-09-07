# KV 캐시 핸드북 한국어판 — Phase 4 대조 교정 기록

32개 중문 소스 ↔ 번역 원고 1:1 전수 대조. 결함은 번역문만 수정(소스 불변), 수치·식별자·한정문 절삭 없음(Never-cut 준수).

| 소스 스템 | 번역 파일 | 대조 결과 | 비고 |
|---|---|---|---|
| 0-00-导读 | 00-frontmatter/01-preface.md | 수정 1건 | 용어 통일: 본문 "인과 Transformer"→"인과 트랜스포머"(ch02·ch30 본문 표기와 통일, 라틴 표기는 참고문헌 제목에만 유지) |
| 1-01-自回归生成 | 01-principles/ch01-autoregressive/index.md | ok | 공식 p(x_{t+1}‖x_{1:t})·의존 사슬·도면 4노드(프롬프트→사전채움→디코딩×2) 대응 |
| 2-02-重复计算 | 01-principles/ch02-recompute/index.md | ok | "어떤 발견적 추측도 아니다" 한정 보존 |
| 3-03-工作机制 | 01-principles/ch03-mechanism/index.md | ok | softmax 수식·"저장하지 않는 것" 절 대응 |
| 4-04-每层缓存 | 01-principles/ch04-per-layer/index.md | ok | 도면 노드(1·2·…·L층) 대응, 장제 축약은 plan.md 4-04행 수용 |
| 5-05-预填充与解码 | 01-principles/ch05-prefill-decode/index.md | ok | 4행 비교표 전수 대응 |
| 6-06-逐步解码 | 01-principles/ch06-stepwise-decode/index.md | ok | 6단계 번호목록·도면 라벨 K₁:₃→K₁:₄ 대응 |
| 7-07-内存公式 | 02-cost/ch07-memory-formula/index.md | 수정 1건 | 용어 통일: 스케일 인자→스케일 팩터(缩放因子, ch26·27과 통일). "런타임에 소비되는 모든 바이트를 담지는 않는다" 한정 보존 |
| 8-08-内存计算实例 | 02-cost/ch08-memory-worked-example/index.md | ok | 표 3행·1,073,741,824 bytes = 1 GiB·"모든 32층 모델에 통용되는 크기가 아니다" 한정 보존 |
| 9-09-上下文长度 | 02-cost/ch09-context-length/index.md | ok | 3×3 표 수치(4/16/64·1/4/16·0.125/0.5/2 GiB) 전수 일치 |
| 10-10-KV缓存节省了什么 | 02-cost/ch10-what-it-saves/index.md | ok | 3자원(계산·용량·대역폭) 불릿·MQA 동기 문장 대응 |
| 11-11-多头注意力 | 03-architecture/ch11-mha/index.md | 수정 1건 | 용어 통일: 소제목 "기준 방안"→"기준선"(基线, 전서 통일) |
| 12-12-多查询注意力 | 03-architecture/ch12-mqa/index.md | ok | "수학적 보장은 없다" 한정 보존, 1/32 수치 |
| 13-13-分组查询注意力 | 03-architecture/ch13-gqa/index.md | ok | 3행 비교표·"논문이 보고한 모델과 실험 설정 안으로 한정" 보존 |
| 14-14-一个公式三种架构 | 03-architecture/ch14-one-formula/index.md | ok | 소스 도면 3열(MHA/GQA/MQA)을 펜스 3건으로 1:1 대응 |
| 15-15-多头潜在注意力 | 03-architecture/ch15-mla/index.md | ok | 93.3% "해당 논문의 특정 결과" 한정 보존, RoPE 복잡성 절 대응 |
| 16-16-位置信息 | 03-architecture/ch16-rope/index.md | ok | "보편 정의로 삼지 않는다" 한정 보존 |
| 17-17-从请求到服务器 | 04-block-management/ch17-requests/index.md | ok | 5불릿·PagedAttention 논문 지적 문장 대응 |
| 18-18-碎片化 | 04-block-management/ch18-fragmentation/index.md | ok | 예약 낭비·외부 단편화 소제목, FlashAttention 구분 문장 보존 |
| 19-19-PagedAttention | 04-block-management/ch19-paged-attention/index.md | ok | 도면 10노드(논리 4·물리 6, 빈 2)·블록 테이블 B0→2, B1→5, B2→0, B3→3 전수 일치 |
| 20-20-块大小 | 04-block-management/ch20-block-size/index.md | ok | "논리 토큰 역사 ≠ 연속 물리 메모리" 인용·축출 용어 통일 확인 |
| 21-21-前缀缓存 | 05-reuse-tiering-precision/ch21-prefix-cache/index.md | ok | "정확한 상태 재사용, RAG 아님" 한정 보존 |
| 22-22-前缀缓存的局限 | 05-reuse-tiering-precision/ch22-prefix-limits/index.md | ok | vLLM 문서 한정("디코딩 단계 시간은 줄이지 못한다") 보존 |
| 23-23-前缀缓存安全 | 05-reuse-tiering-precision/ch23-prefix-security/index.md | ok | cache_salt·비암호학적 해시 경고 대응 |
| 24-24-淘汰 | 05-reuse-tiering-precision/ch24-eviction/index.md | ok | 4불릿·vLLM/TensorRT-LLM 문서 병기 대응 |
| 25-25-卸载 | 05-reuse-tiering-precision/ch25-offload/index.md | 수정 1건 | 용어 통일: 소제목 "트레이드오프"→"절충"(取舍, ch20과 통일) |
| 26-26-KV缓存量化 | 05-reuse-tiering-precision/ch26-quantization/index.md | ok | "실제 절감은 이상적 비율과 정확히 일치하지 않을 수 있다" 한정 보존 |
| 27-27-量化的代价 | 05-reuse-tiering-precision/ch27-quant-cost/index.md | ok | 5불릿·vLLM 부분 비양자화 허용 문장 대응 |
| 28-28-常见误解 | 06-synthesis/ch28-misconceptions/index.md | ok | 6쌍 오해·반박 전수, "대개 그렇지 않다" 한정 보존 |
| 29-29-生产环境理解框架 | 06-synthesis/ch29-production-frame/index.md | 수정 1건 | 용어 통일: "어텐션 윈도 규칙"→"어텐션 창 규칙"(注意力窗口, ch17·ch09과 통일) |
| 30-30-完整的理解框架 | 06-synthesis/ch30-full-frame/index.md | ok | M_KV ≈ 2LTH_KVD_hb·참고자료 [1]—[11] 대응 |
| 31-31-参考文献 | 07-backmatter/00-references.md | 수정 3건 | [8]·[9]·[10] "현행 문서" 상정어 복원(소스 现行文档查阅于, [7] 표기와 정합. [6]은 소스도 상정어 없어 그대로) |

요약: 32행 중 ok 26 / 수정 6행(수정점 8곳 — 전부 용어 통일·상정어 복원, 문장 누락·추가 0건).

## 게이트 판정 기록

### G3 WARN 175건 수용 (FAIL 0)

- 출간 전례 대비 최저: system-design-interview-notes-ko 500 · 설득의 구조 225 · skill-state-ko 190 → 본서 175.
- 45자+ 초과 줄은 라틴 식별자(arXiv ID·DOI·vLLM·TensorRT-LLM·FlashAttention·PagedAttention 등 기술 고유명)와 인용블록·수식 주석이 대부분. 절삭 시 Never-cut 계약(수치·식별자·한정문 보존) 위반 → 보존 우선.
- 밴드는 조판 결과물이며 우선순위 계약상 보존 > 밴드(plan.md Phase 5 종료 조건 주석 준용).

### G5 잔여 179행 수용 (FAIL 0, gate-report pass=true)

- '제N장' 헤딩 자기참조 오폭 29표제(31행 — ch10·ch26 표제는 KV 병기라 ALL-CAPS 오폭과 중복 계수). 챕터 오프너 표기 관례상 정상 표기.
- 나머지 148행은 ALL-CAPS 기술용어(KV·MHA·GQA·MQA·MLA·RoPE·vLLM·FP8·LRU·HBM·CPU·GPU·IO·arXiv 등) 오폭 — 고유명 보존.
- 둘 다 WARN 채널이며 FAIL 조건 없음.

## 기계 검증 이력 (Phase 4 시점)

- `python3 skills/korean-ebook/scripts/korean_lint.py books/kv-cache-handbook-ko/manuscript` → 총 0건, exit 0 (39파일 개별 실행도 전부 0건)
- 한자 잔여: frontmatter `source:` 필드 외 0건. 전각문호(U+FF01–FF5E·CJK 구두점) 0건, 중점은 U+00B7 36건뿐(한국어 인터펑트, 허용)
- 경어체(습니다/입니다) 0건 — 전서 등록 한다체 유지
- 라틴 식별자 전수 스윕: arXiv 7종·DOI 1종·NeurIPS/EMNLP/SOSP·KiB/GiB·FP8·cache_salt·CacheConfig·@techNmak 전부 존재 (DOI "DOI: 10.1145/3600006.3613165" 공백 표기, 1,073,741,824는 LaTeX 천단위 `1{,}073{,}741{,}824` 형식 — 수치 자체 동일)
- 불릿·번호목록 개수 대조: 소스 합계 42항목 ↔ 번역 42항목 일치 (0-00:6, 6-06:6, 7-07:6, 10-10:3, 15-15:3, 16-16:3, 17-17:5, 21-21:2, 24-24:4, 27-27:5, 29-29:5 …)
