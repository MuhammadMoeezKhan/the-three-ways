"""Overdraft protection: block a withdrawal if it would breach the
customer's approved threshold.
"""

from ledger import get_current

OVERDRAFT_LIMIT = -500.00


def check_limit(account: dict, withdrawal: float) -> bool:
    """Return True if a withdrawal is allowed under the approved threshold."""
    current = get_current(account)
    return (current - withdrawal) >= OVERDRAFT_LIMIT
