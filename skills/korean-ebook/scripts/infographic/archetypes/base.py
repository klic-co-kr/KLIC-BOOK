"""base.py — archetype 공통 예외(스펙 §5.2 전수 집계·§5.5 CLI 리포트가 베이스로 catch)."""


class LayoutError(Exception):
    def __init__(self, detail: str):
        super().__init__(detail)
        self.detail = detail


def sizes(tokens: dict) -> dict:
    """공용 텍스트 크기 산출(스펙 §4.3·Phase 2 cards 관례) — archetype 공통 단일 진실."""
    f = tokens["fonts"]
    body = f["body"]["size_pt"]
    title = f["heading2"]["size_pt"]
    if abs(title - body) <= 0.3:
        title = body + 1.5
    return {"body": body, "kicker": f["label"]["size_pt"], "title": title,
            "ph_title": body + 1, "item": body - 1}
