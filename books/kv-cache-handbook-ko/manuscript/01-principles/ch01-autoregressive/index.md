---
id: ch01
title: "자기회귀 생성"
part: principles
order: 1
source: "1-01-自回归生成"
status: translated
---

## 제1장 — 자기회귀 생성

### 디코딩은 왜 순서대로 이루어져야 하는가

디코더 전용 언어모델은 이미 있는 토큰을 바탕으로 다음 토큰의 확률 분포를 다음과 같이 낸다.

$$p(x_{t+1} \mid x_{1:t})$$

토큰 하나를 고르고 나면 그 토큰을 시퀀스 끝에 덧붙이며, 이것이 다음 단계의 문맥이 된다. 따라서 생성 과정은 하나의 의존 사슬을 이룬다.

$$x_1, \dots, x_t \to x_{t+1} \to x_{t+2}$$

### 두 가지 실행 단계

여러 토큰으로 이루어진 프롬프트에 대해, 모델은 인과 마스크(causal mask) 제약 안에서 이 프롬프트 위치들을 동시에 처리할 수 있다. 이를 보통 사전채움(prefill)이라고 부른다. 생성이 시작된 뒤에는, 모델이 보통 매 디코딩 단계에서 시퀀스 하나당 새로 생성된 토큰 하나를 진행한다. 이것이 디코딩(decode) 단계다.

```diagram
{
  "layout": "flow",
  "title": "순차 디코딩 구조가 캐시를 필수로 만든다",
  "caption": "그림 1-1 생성의 두 단계 — 프롬프트가 사전채움으로 초기 캐시를 만들고, 디코딩이 토큰을 하나씩 진행한다",
  "nodes": [
    {"id": "prompt", "label": "프롬프트", "tone": "gray"},
    {"id": "prefill", "label": "사전채움", "tone": "blue"},
    {"id": "decode1", "label": "디코딩", "tone": "gray"},
    {"id": "decode2", "label": "디코딩", "tone": "gray"}
  ],
  "edges": [
    {"from": "prompt", "to": "prefill"},
    {"from": "prefill", "to": "decode1"},
    {"from": "decode1", "to": "decode2"}
  ]
}
```

바로 이 순차 디코딩 구조가 KV 캐시를 결정적으로 중요하게 만든다.

참고자료: [1], [6]
