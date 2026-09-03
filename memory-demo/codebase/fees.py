"""Monthly maintenance fee schedule."""

MONTHLY_FEE = 4.99


def waive_fee(account: dict) -> bool:
    """Accounts with direct deposit set up skip the monthly fee."""
    return account.get("direct_deposit", False)
