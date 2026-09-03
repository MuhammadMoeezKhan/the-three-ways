"""A shallow dependency graph on top of the same retrieval: instead of
stopping at whatever's worded like the query, follow the codebase's real
import structure a few hops out from those seed files.

You don't need a perfect graph. A one- or two-hop expansion catches most
of the silent drops RAG alone misses, for a fraction of the effort of a
full knowledge graph.
"""

from __future__ import annotations

import ast
from collections import defaultdict
from pathlib import Path

from rag_search import search as keyword_search

CODEBASE = Path(__file__).parent / "codebase"


def _local_imports(path: Path, known_modules: set[str]) -> set[str]:
    """Module-level `import X` / `from X import Y` targets, restricted to
    modules that actually live in this codebase (skip stdlib etc.)."""
    tree = ast.parse(path.read_text())
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            found.add(node.module)
    return found & known_modules


def build_dependents_graph() -> dict[str, set[str]]:
    """Reverse dependency graph: dependents[X] = every module that
    imports X, directly. This is the 'one hop' unit we expand along."""
    files = sorted(CODEBASE.glob("*.py"))
    known_modules = {f.stem for f in files}
    dependents: dict[str, set[str]] = defaultdict(set)

    for path in files:
        for target in _local_imports(path, known_modules):
            dependents[target].add(path.stem)

    return dependents


def search(query: str, max_hops: int = 2, top_k: int = 3) -> list[str]:
    """Keyword-match to find seed files, then walk the reverse-dependency
    graph outward up to max_hops to pull in files that depend on a seed
    but never mention the query term themselves."""
    dependents = build_dependents_graph()
    seeds = {name for name, _score in keyword_search(query, top_k=top_k)}

    found = set(seeds)
    frontier = set(seeds)
    for _ in range(max_hops):
        next_frontier: set[str] = set()
        for module in frontier:
            stem = module.removesuffix(".py")
            next_frontier |= {f"{m}.py" for m in dependents.get(stem, set())}
        next_frontier -= found
        if not next_frontier:
            break
        found |= next_frontier
        frontier = next_frontier

    return sorted(found)


if __name__ == "__main__":
    for name in search("balance"):
        print(name)
