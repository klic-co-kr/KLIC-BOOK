"""색 역할 조회(스펙 §4.2). emit·layout은 hex를 직접 다루지 않는다."""
REQUIRED_INFO_ROLES = ("surface-tint", "focus", "positive", "warning", "on-focus")


def color(tokens: dict, role: str) -> str:
    if role in tokens.get("colors", {}):
        return tokens["colors"][role]
    return tokens["infographic"][role]
