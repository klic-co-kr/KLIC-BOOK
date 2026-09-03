#!/usr/bin/env python3
"""eval_metrics.py — 책→스킬 판단 품질 메트릭 (논문 Human-AI Synergy 시사점).

recall(부록C 회상)만으로는 AI 판단의 '정확도'를 잴 수 없다. 인간 정답(golden)
대비 정량 메트릭을 추가한다:

- precision: AI 후보 중 골든 매칭 비율 (AI 제안 정확도 — 논문: AI 제안 반가 부정확)
- recall:    골든 중 AI 후보 커버 비율 (인간 정답 재현)
- adoption:  승인(approved) 후보 / 전체 (게이트 통과율 — 논문: 채택률)
- rounds:    approval_log 라운드 수 (인간 개입 — 논문: 피드백 라운드)

매칭: id 일치 OR source_ref 겹침 OR title_keyword 포함.

사용: python3 eval_metrics.py <candidates.yaml> <golden.json>
"""
import sys, json


def _match(cand: dict, golden: dict) -> bool:
    if cand.get("id") == golden.get("id"):
        return True
    sr = golden.get("source_ref", "")
    if sr and sr in cand.get("source_refs", []):   # 정확 매칭 (부분문자열 오탐 방지)
        return True
    kw = golden.get("title_keyword", "")
    if kw and kw in cand.get("title", ""):
        return True
    return False


def compute_metrics(candidates_path: str, golden_path: str) -> dict:
    import yaml
    cf = yaml.safe_load(open(candidates_path, encoding="utf-8"))
    gj = json.load(open(golden_path, encoding="utf-8"))
    golden = gj["golden_must_extract"]
    chapter = gj.get("chapter_under_test")  # e.g. "02" — precision 을 해당 장 후보로 한정
    all_cands = cf.get("candidates", [])
    if chapter:
        prefix = f"ch{chapter}§"
        cands = [c for c in all_cands
                 if any(r.startswith(prefix) for r in c.get("source_refs", []))]
    else:
        cands = all_cands
    n_c, n_g = len(cands), len(golden)
    matched_c = sum(any(_match(c, g) for g in golden) for c in cands)
    matched_g = sum(any(_match(c, g) for c in cands) for g in golden)
    approved = sum(1 for c in cands if c.get("approved"))
    rounds = len(cf.get("approval_log") or [])
    p = matched_c / n_c if n_c else 0.0
    r = matched_g / n_g if n_g else 0.0
    f1 = 2 * p * r / (p + r) if (p + r) else 0.0
    return {
        "precision": round(p, 3),
        "recall": round(r, 3),
        "f1": round(f1, 3),
        "adoption": round(approved / n_c, 3) if n_c else 0.0,
        "rounds": rounds,
        "n_golden": n_g,
        "n_candidates": n_c,
    }


def main(argv):
    if len(argv) != 3:
        sys.exit("usage: eval_metrics.py <candidates.yaml> <golden.json>")
    m = compute_metrics(argv[1], argv[2])
    for k, v in m.items():
        print(f"{k}: {v}")
    # 경고
    if m["n_golden"] < 5:
        print(f"WARN: golden {m['n_golden']}개 — 통계적 의미 낮. 5-10+ 권장.")
    if m["precision"] < 0.3:
        print("WARN: precision < 0.3 — AI 후보 노이즈 다수. 게이트 라운드 증가 권장.")
    if m["adoption"] == 1.0 and m["n_candidates"] > 3:
        print("WARN: adoption 1.0(전부 승인) — 게이트 가감 없음. precision 낮으면 노이즈 승인 의심.")
    gj = json.load(open(argv[2], encoding="utf-8"))
    if not gj.get("chapter_under_test"):
        print("WARN: chapter_under_test 없음 — 전책 precision(왜곡 가능).")


if __name__ == "__main__":
    main(sys.argv)
