import graph_search
import rag_search


def test_keyword_search_finds_direct_mentions():
    hits = {name for name, _score in rag_search.search("balance")}
    assert "balance.py" in hits
    assert "ledger.py" in hits


def test_keyword_search_misses_the_indirect_dependency():
    hits = {name for name, _score in rag_search.search("balance")}
    assert "overdraft.py" not in hits


def test_graph_search_catches_what_keyword_search_misses():
    hits = set(graph_search.search("balance"))
    assert "overdraft.py" in hits


def test_graph_search_is_a_superset_of_keyword_search():
    keyword_hits = {name for name, _score in rag_search.search("balance")}
    graph_hits = set(graph_search.search("balance"))
    assert keyword_hits <= graph_hits


def test_unrelated_files_never_surface():
    graph_hits = set(graph_search.search("balance"))
    for unrelated in ("interest.py", "statements.py", "fees.py", "notifications.py", "reports.py"):
        assert unrelated not in graph_hits
