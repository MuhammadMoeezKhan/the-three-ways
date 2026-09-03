# tools-demo

Layer 1 from the talk: Reliable Tool Calls.

Two versions of the same tool, `search_code`, backed by the exact same (deliberately buggy) data: it paginates internally but only returns page one. The difference between them is entirely in the contract, not the logic.

- [`loose_tool.py`](./loose_tool.py): untyped input, returns a plain string, no error state. Truncated results and empty results look identical to the caller.
- [`strict_tool.py`](./strict_tool.py): typed input (`KnownFunction`, an enum, so a malformed query never runs), and a real `Success | LowConfidence | Failure` result. `LowConfidence` is the state most tool schemas can't express: "it worked, but I'm not sure it's the whole answer."

## Run it

Requires Python 3.10+ (uses `match` and `X | Y` union types).

```bash
python demo.py
```

```bash
pip install pytest
pytest
```

## What to look at

`demo.py` runs both tools against the same underlying bug and prints the difference: the loose tool returns 5 of 14 real call sites with no indication anything is missing; the strict tool returns the same 5 items wrapped in `LowConfidence`, telling the caller explicitly that the answer is incomplete. A separate call with a malformed query is rejected on the spot by the strict tool, where the loose tool would silently return `""`, indistinguishable from a genuine "no results."

Part of [the-three-ways](../).
