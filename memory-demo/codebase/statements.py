"""Monthly statement generation."""


def render_statement(account: dict, month: str) -> str:
    """Format a plain-text summary of a month's transactions."""
    lines = [f"Statement for {month}"]
    for t in account.get("transactions", []):
        lines.append(f"  {t['memo']}: {t['amount']:.2f}")
    return "\n".join(lines)
