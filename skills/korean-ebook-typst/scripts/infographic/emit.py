"""emit.py — FigModel → typst 방출(스펙 §5.1). 칠하기만 한다: 조건 분기 금지, 좌표는 2자리 반올림."""
from __future__ import annotations

from .model import ArrowOp, CircleOp, FigModel, RectOp, TextOp


def _n(v: float) -> str:
    return f"{v:.2f}"


def _esc(s: str) -> str:
    # md2typst step 6 기준과 동일하게 @·<·>까지 — "SLA @team"이 label로 해석돼
    # 빌드가 깨지는 것을 막는다(적대 검토 실증).
    for a, b in (("\\", "\\\\"), ("#", "\\#"), ("[", "\\["), ("]", "\\]"),
                 ("$", "\\$"), ("*", "\\*"), ("_", "\\_"),
                 ("@", "\\@"), ("<", "\\<"), (">", "\\>")):
        s = s.replace(a, b)
    return s


def render_typ(fig: FigModel) -> str:
    # ig-circle는 CircleOp가 있는 도식에만 임포트한다(ops 순수 함수 — 결정론 유지).
    # 무조건 포함하면 원이 없는 기존 골든 전부의 헤더 바이트가 바뀐다(브리프 §Step 4
    # "기존 골든 방출 바이트 불변" 요건과 충돌 — 컨트롤러 판정으로 조건화).
    helpers = ["ig-rect", "ig-text", "ig-arrow"]
    if any(isinstance(op, CircleOp) for op in fig.ops):
        helpers.append("ig-circle")
    helpers.append("ig-figure")
    lines = [
        "// 자동 생성 — scripts/infographic/emit.py. 수정 금지(원본은 펜스에 있다).",
        f'#import "../helper.typ": {", ".join(helpers)}',
        f"#ig-figure({_n(fig.width)}, {_n(fig.height)})[",
    ]
    for op in fig.ops:
        if isinstance(op, RectOp):
            rt = f", rot: {op.rot:g}deg" if op.rot != 0.0 else ""
            lines.append(
                f"  #ig-rect({_n(op.x)}, {_n(op.y)}, {_n(op.w)}, {_n(op.h)}, "
                f"rx: {_n(op.rx)}pt, fill-role: \"{op.fill_role}\", "
                f"stroke-role: \"{op.stroke_role}\", stroke-w: {_n(op.stroke_w)}pt{rt})")
        elif isinstance(op, CircleOp):
            lines.append(
                f"  #ig-circle({_n(op.x)}, {_n(op.y)}, {_n(op.r)}, "
                f"fill-role: \"{op.fill_role}\", stroke-role: \"{op.stroke_role}\", "
                f"stroke-w: {_n(op.stroke_w)}pt)")
        elif isinstance(op, ArrowOp):
            lines.append(f"  #ig-arrow({_n(op.x1)}, {_n(op.y1)}, {_n(op.x2)}, {_n(op.y2)}, "
                         f"style: \"{op.style}\")")
        elif isinstance(op, TextOp):
            w = f", weight: \"{op.weight}\"" if op.weight != "regular" else ""
            mw = f", max-w: {_n(op.max_w)}pt" if op.max_w > 0 else ""
            # ig-text는 컨테이너 중심 앵커라 절대좌표 환산에 fw·fh가 필요하다(helper 참조).
            lines.append(f"  #ig-text({_n(op.x)}, {_n(op.y)}, {_n(fig.width)}, "
                         f"{_n(fig.height)}, {_n(op.size)}, \"{op.role}\"{w}{mw})[{_esc(op.text)}]")
    lines.append("]")
    return "\n".join(lines) + "\n"
