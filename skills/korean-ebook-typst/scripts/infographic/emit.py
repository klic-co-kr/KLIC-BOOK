"""emit.py — FigModel → typst 방출(스펙 §5.1). 칠하기만 한다: 조건 분기 금지, 좌표는 2자리 반올림."""
from __future__ import annotations

from .model import ArrowOp, FigModel, RectOp, TextOp


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
    lines = [
        "// 자동 생성 — scripts/infographic/emit.py. 수정 금지(원본은 펜스에 있다).",
        '#import "../helper.typ": ig-rect, ig-text, ig-arrow, ig-figure',
        f"#ig-figure({_n(fig.width)}, {_n(fig.height)})[",
    ]
    for op in fig.ops:
        if isinstance(op, RectOp):
            lines.append(
                f"  #ig-rect({_n(op.x)}, {_n(op.y)}, {_n(op.w)}, {_n(op.h)}, "
                f"rx: {_n(op.rx)}pt, fill-role: \"{op.fill_role}\", "
                f"stroke-role: \"{op.stroke_role}\", stroke-w: {_n(op.stroke_w)}pt)")
        elif isinstance(op, ArrowOp):
            lines.append(f"  #ig-arrow({_n(op.x1)}, {_n(op.y1)}, {_n(op.x2)}, {_n(op.y2)}, "
                         f"style: \"{op.style}\")")
        elif isinstance(op, TextOp):
            w = f", weight: \"{op.weight}\"" if op.weight != "regular" else ""
            # ig-text는 컨테이너 중심 앵커라 절대좌표 환산에 fw·fh가 필요하다(helper 참조).
            lines.append(f"  #ig-text({_n(op.x)}, {_n(op.y)}, {_n(fig.width)}, "
                         f"{_n(fig.height)}, {_n(op.size)}, \"{op.role}\"{w})[{_esc(op.text)}]")
    lines.append("]")
    return "\n".join(lines) + "\n"
