# Tools Demo (Layer 1: Reliable Tool Calls)

Status: planned, not yet implemented. Part of the-three-ways.

## What this will show

A loose vs. strict tool schema for an agent's code-search tool.

Loose: a tool contract that just says "returns a string." A partial or wrong result looks identical to a correct one, no error, no signal.

Strict: typed inputs, an explicit error contract (Result or Failure), idempotent retries, and a third state for "succeeded, but low confidence."

A runnable script will call both versions against a deliberately bad call and show the strict schema catching what the loose one silently accepts.

See the top-level FAILURE_MAP.md for the full Layer 1 diagnostic, and the talk deck and write-up linked in the root README for the full walkthrough.
