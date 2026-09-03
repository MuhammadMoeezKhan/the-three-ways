# Memory Demo (Layer 2: RAG vs. Knowledge Graph)

Status: planned, not yet implemented. Part of the-three-ways.

## What this will show

A toy legacy codebase with a deliberately buried cross-file dependency.

Plain retrieval (RAG): pulls the files that are textually similar to the query, and misses a real dependency that shares little wording with it, several hops away in the dependency chain.

Shallow knowledge graph: a one-hop dependency graph layered on top of RAG. It catches the same missed dependency, because most silent misses are one hop away, not ten.

Two scripts will run the same query against both memory strategies and show the difference in what gets caught.

See the top-level FAILURE_MAP.md for the full Layer 2 diagnostic, and the talk deck and write-up linked in the root README for the full walkthrough.
