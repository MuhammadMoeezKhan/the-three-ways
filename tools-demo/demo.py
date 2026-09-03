"""Run both tool schemas against the same underlying (buggy) data and watch
one fail silently while the other flags exactly what's wrong.

    python demo.py
"""

import loose_tool
import strict_tool


def main() -> None:
    print("=== LOOSE tool: search_code('calculate_interest') ===")
    result = loose_tool.search_code("calculate_interest")
    print(f"  returned: {result!r}")
    print("  looks like a complete answer. It is not: 9 of 14 real call")
    print("  sites never made it into the response, and nothing said so.\n")

    print("=== STRICT tool: search_code(KnownFunction.CALCULATE_INTEREST) ===")
    result = strict_tool.search_code(strict_tool.KnownFunction.CALCULATE_INTEREST)
    print(f"  returned: {result!r}")
    match result:
        case strict_tool.LowConfidence(items=items, reason=reason):
            print(f"  -> caller is told explicitly: {reason}")
        case strict_tool.Success(items=items):
            print(f"  -> {len(items)} item(s), reported complete")
        case strict_tool.Failure(reason=reason):
            print(f"  -> rejected: {reason}")
    print()

    print("=== STRICT tool: a malformed query ===")
    result = strict_tool.search_code("drop table users")  # not a KnownFunction
    print(f"  returned: {result!r}")
    print("  -> rejected on the spot. The loose tool would have silently")
    print("     returned an empty string, indistinguishable from a real")
    print("     'no results found'.")


if __name__ == "__main__":
    main()
