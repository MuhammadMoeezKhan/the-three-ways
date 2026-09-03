"""Interest accrual on savings products."""


def accrue_interest(principal: float, apr: float, days: int) -> float:
    """Simple daily accrual, not compounded."""
    return principal * (apr / 365) * days
