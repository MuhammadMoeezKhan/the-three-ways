"""Customer-facing alerts."""


def send_alert(customer_id: str, message: str) -> None:
    """Stub: would call an email/SMS provider in a real system."""
    print(f"[alert to {customer_id}] {message}")
