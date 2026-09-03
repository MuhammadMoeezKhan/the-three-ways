"""Plain retrieval over the toy codebase: rank files by how much of their
text overlaps with the query. This is a simplified stand-in for RAG's
embedding-similarity search: same blind spot, no API key required.

RAG finds what's WORDED like the query. It has no notion of what's
CONNECTED to it.
"""

from __future__ import annotations

import re
from pathlib import Path

CODEBASE = Path(__file__).parent / "codebase"


def _tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-z_]+", text.lower()))


def search(query: str, top_k: int = 3) -> list[tuple[str, int]]:
    """Return the top_k files ranked by keyword overlap with the query,
    keyword-search style. Files with zero overlap are never returned,
    no matter how structurally important they are."""
    query_tokens = _tokenize(query)
    scores: list[tuple[str, int]] = []

    for path in sorted(CODEBASE.glob("*.py")):
        file_tokens = _tokenize(path.read_text())
        overlap = len(query_tokens & file_tokens)
        if overlap > 0:
            scores.append((path.name, overlap))

    scores.sort(key=lambda pair: pair[1], reverse=True)
    return scores[:top_k]


if __name__ == "__main__":
    for name, score in search("balance"):
        print(f"{name}: overlap={score}")
