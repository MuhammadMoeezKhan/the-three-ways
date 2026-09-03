"""The STRICT version: typed input, an explicit error contract (a real
Result/Failure/LowConfidence shape), and idempotent retries. Same
underlying data and the same pagination bug as loose_tool.py. The fix
is entirely in the contract, not the logic.
"""

from dataclasses import dataclass, field
from enum import Enum

from loose_tool import _CALL_SITE_INDEX, _PAGE_SIZE


class KnownFunction(str, Enum):
    """Typed input: only functions we actually indexed are legal queries.
    A malformed or unknown query is rejected before it ever runs."""

    CALCULATE_INTEREST = "calculate_interest"


@dataclass
class Success:
    items: list
    complete: bool = True


@dataclass
class LowConfidence:
    """The state most loose schemas can't express: 'it worked, but I'm
    not sure it's the whole answer.'"""

    items: list
    reason: str


@dataclass
class Failure:
    reason: str


ToolResult = Success | LowConfidence | Failure


def search_code(query: KnownFunction, *, idempotency_key: str | None = None) -> ToolResult:
    """Same lookup as the loose tool, but honest about pagination and
    rejecting bad input up front.

    idempotency_key is accepted but unused here on purpose: this call is a
    pure read, so it's naturally idempotent. A write-side tool would use
    the key to make a retried call a no-op instead of a double-apply,
    see the "elevator button" bit in the talk.
    """
    if not isinstance(query, KnownFunction):
        return Failure(reason=f"unknown or malformed query: {query!r}")

    sites = _CALL_SITE_INDEX.get(query.value, [])
    page_one = sites[:_PAGE_SIZE]

    if not sites:
        return Success(items=[], complete=True)

    if len(sites) > len(page_one):
        return LowConfidence(
            items=page_one,
            reason=(
                f"only {len(page_one)} of {len(sites)} call sites returned "
                f"(page 1 of {-(-len(sites) // _PAGE_SIZE)}), treat as incomplete"
            ),
        )

    return Success(items=page_one, complete=True)
