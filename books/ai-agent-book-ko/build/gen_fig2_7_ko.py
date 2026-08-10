#!/usr/bin/env python3
"""fig2-7 한국어 재생성: 멀티헤드 어텐션 가중치 히트맵 (예시/합성).

원본은 중문 토큰 라벨의 어텐션 히트맵. 번역판용으로 한국어 토큰과
합성 어텐션 패턴으로 동일한 시각화 형태를 재현한다. 실제 모델의
가중치가 아니며 '예시(합성 데이터)'로 표기한다.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import numpy as np
from pathlib import Path

FONT_PATH = "/home/aministrator/.local/share/fonts/NotoSansKR-VF.ttf"
font_manager.fontManager.addfont(FONT_PATH)
rc("font", family="Noto Sans KR")
plt.rcParams["axes.unicode_minus"] = False

# 한국어 토큰 예시 (ch2 컨텍스트/압축 주제에 부합)
tokens = ["나", "는", "에이전트", "가", "도구", "를", "호출", "한다", "."]
n = len(tokens)
rng = np.random.default_rng(7)


def attn(head: int) -> np.ndarray:
    """헤드별로 특징이 다른 합성 어텐션 패턴(softmax 근사)."""
    m = rng.random((n, n)) * 0.15
    if head == 0:  # 인접 토크 중심(지역적)
        for i in range(n):
            for j in range(n):
                m[i, j] += np.exp(-abs(i - j) * 1.1)
    elif head == 1:  # 핵심어 '도구'(idx 4)로 수렴
        for i in range(n):
            m[i, 4] += 1.4
        m[4, :] += 0.6
    elif head == 2:  # 시작 토큰(0)으로 수렴
        for i in range(n):
            m[i, 0] += 1.2
    else:  # 넓게 분산
        m += 0.5
    # 행 단위 softmax
    e = np.exp(m - m.max(axis=1, keepdims=True))
    return e / e.sum(axis=1, keepdims=True)


heads = [attn(h) for h in range(4)]
titles = ["헤드 1: 지역", "헤드 2: 핵심어", "헤드 3: 시작점", "헤드 4: 분산"]

fig, axes = plt.subplots(1, 4, figsize=(13.6, 3.46))
for ax, mat, t in zip(axes, heads, titles):
    im = ax.imshow(mat, cmap="cividis", vmin=0, vmax=1, aspect="equal")
    ax.set_title(t, fontsize=11)
    ax.set_xticks(range(n))
    ax.set_xticklabels(tokens, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(n))
    ax.set_yticklabels(tokens, fontsize=8)
    ax.set_xlabel("Key 토큰", fontsize=9)
    if mat is heads[0]:
        ax.set_ylabel("Query 토큰", fontsize=9)

fig.suptitle("어텐션 가중치 시각화 — 헤드별 패턴 차이", fontsize=13, y=1.02)
fig.text(0.99, 0.01, "예시(합성 데이터)", ha="right", va="bottom", fontsize=7, color="#666666")
fig.tight_layout()

out = Path("/mnt/d/DEV/KLIC-BOOK/books/ai-agent-book-ko/manuscript/images/fig2-7.png")
fig.savefig(out, dpi=260, bbox_inches="tight", facecolor="white")
print("saved", out, out.stat().st_size, "bytes")
