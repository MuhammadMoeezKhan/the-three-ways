"""Balance math for a customer account."""


def calculate_balance(account: dict) -> float:
    """Sum posted transactions minus pending holds for one account."""
    posted = sum(t["amount"] for t in account.get("transactions", []))
    holds = sum(h["amount"] for h in account.get("holds", []))
    return posted - holds
