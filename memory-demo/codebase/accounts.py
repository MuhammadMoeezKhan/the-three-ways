"""Account lookup and creation."""

_ACCOUNTS: dict[str, dict] = {}


def open_account(customer_id: str) -> dict:
    account = {"customer_id": customer_id, "transactions": [], "holds": []}
    _ACCOUNTS[customer_id] = account
    return account


def find_account(customer_id: str) -> dict | None:
    return _ACCOUNTS.get(customer_id)
