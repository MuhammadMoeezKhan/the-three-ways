"""Internal ops reporting, unrelated to any single account."""


def daily_transaction_count(accounts: list[dict]) -> int:
    return sum(len(a.get("transactions", [])) for a in accounts)
