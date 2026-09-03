"""The general ledger: posting transactions and reading account state."""

from balance import calculate_balance


def post_transaction(account: dict, amount: float, memo: str) -> dict:
    """Append a transaction to an account's ledger."""
    account.setdefault("transactions", []).append({"amount": amount, "memo": memo})
    return account


def get_current(account: dict) -> float:
    """Read an account's current standing."""
    return calculate_balance(account)
