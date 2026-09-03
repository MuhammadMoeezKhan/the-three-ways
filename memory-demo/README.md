# memory-demo

Layer 2 from the talk: RAG vs. Knowledge Graph.

A toy nine-file "Ledger" billing codebase (in [`codebase/`](./codebase)) with one dependency buried on purpose: [`overdraft.py`](./codebase/overdraft.py) depends completely on [`balance.py`](./codebase/balance.py) through [`ledger.py`](./codebase/ledger.py), but never uses the word "balance" anywhere in its own code.

- [`rag_search.py`](./rag_search.py): plain keyword-overlap retrieval, a simplified stand-in for embedding-similarity search (same blind spot, no API key needed). Finds files worded like the query.
- [`graph_search.py`](./graph_search.py): the same retrieval, plus a shallow expansion along the codebase's real import graph (parsed with Python's `ast`, no external deps). Finds files *connected* to the query, worded like it or not.

## Run it

Requires Python 3.10+.

```bash
python demo.py
```

```bash
pip install pytest
pytest
```

## What to look at

Both searches run the query `"balance"` against the same nine files. Keyword search finds `balance.py` and `ledger.py`, both of which literally contain the word, and stops there, `overdraft.py` never surfaces no matter how central it is to the actual answer. Graph search finds the same two files, then asks one extra question keyword similarity can't: "what else in this codebase depends on what I just found?" That one hop is enough to catch `overdraft.py`, and `test_memory.py` locks in that graph search is always a superset of keyword search here, plus that neither approach ever pulls in one of the five genuinely unrelated files.

You don't need a perfect graph. A one-hop expansion on top of ordinary retrieval catches most silent drops like this one, for a fraction of the cost of hand-building a full knowledge graph.

Part of [the-three-ways](../).
