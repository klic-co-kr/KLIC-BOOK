"""base.py — archetype 공통 예외(스펙 §5.2 전수 집계·§5.5 CLI 리포트가 베이스로 catch)."""


class LayoutError(Exception):
    def __init__(self, detail: str):
        super().__init__(detail)
        self.detail = detail
