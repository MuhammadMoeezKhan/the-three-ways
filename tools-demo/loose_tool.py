"""The LOOSE version: a tool contract with no typed input, no explicit error
state, and pagination that silently drops results. This is what most
hand-rolled tool schemas look like by default.
"""

# Pretend this is a real codebase index: every call site of every function.
_CALL_SITE_INDEX = {
    "calculate_interest": [
        f"billing/module_{i}.py:{10 + i * 3}" for i in range(14)
    ],
}
_PAGE_SIZE = 5


def search_code(query: str) -> str:
    """'Find every call site of a function.' Returns a plain string.

    Bug: paginates internally but only ever returns page one. Nothing about
    the return value indicates truncation, so a caller (human or agent) has
    no way to tell "found 5 of 5" apart from "found 5 of 14".
    """
    sites = _CALL_SITE_INDEX.get(query, [])
    page_one = sites[:_PAGE_SIZE]
    if not page_one:
        return ""  # indistinguishable from "genuinely no results"
    return ", ".join(page_one)
