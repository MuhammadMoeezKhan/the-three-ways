"""Ask the same question two ways: plain keyword retrieval, and a shallow
dependency graph layered on top of it.

    python demo.py
"""

import graph_search
import rag_search

QUERY = "balance"


def main() -> None:
    print(f"=== Keyword search (RAG-style) for '{QUERY}' ===")
    hits = rag_search.search(QUERY)
    for name, score in hits:
        print(f"  found: {name}  (shares {score} word(s) with the query)")
    print("  missed: overdraft.py")
    print("  it depends on the balance completely, through ledger.get_current(),")
    print("  but never uses the word 'balance' anywhere in its own code.\n")

    print(f"=== Graph search (RAG + one-hop dependency expansion) for '{QUERY}' ===")
    hits = graph_search.search(QUERY)
    for name in hits:
        flag = "  <- caught, RAG alone missed this" if name == "overdraft.py" else ""
        print(f"  found: {name}{flag}")
    print()
    print("Same seed files, same query. The only difference: the graph search")
    print("also asks 'what else in this codebase actually depends on the files")
    print("I already found?' (a question keyword similarity can't answer).")


if __name__ == "__main__":
    main()
