# The Failure Map

A one-page checklist for finding where an agent is actually breaking, before assuming it's the model.

Companion to "The Three Ways AI Agents Fail. Here's How to Fix Yours." at Commit Your Code 2026.

## The core idea

Every one of these failures is silent by default. The fix in each layer is the same move: making the failure loud on purpose.

## Diagnostic: which layer is it?

### Layer 1, Tools
Ask: did a tool return a partial, empty, or wrong result with no error?
Symptom: the agent's plan looks confident but was built on incomplete data. No stack trace, no red flag, just drift.
Fix: typed inputs, explicit error contracts (Result or Failure), idempotent retries, a third state for "succeeded, but low confidence."

### Layer 2, Memory
Ask: did the agent miss a fact that was true, but not textually similar to what it searched for?
Symptom: retrieval (RAG) finds what's worded like the query, and misses what's connected to it. The output looks complete. It compiles. It's wrong.
Fix: a shallow, one-hop dependency graph layered on top of RAG. You don't need a perfect graph, most silent misses are one hop away.

### Layer 3, Coordination
Ask: did one agent's bad output get trusted and built on by the next agent, unchecked?
Symptom: each stage in a pipeline looks like it did its job. The failure only becomes visible once it's already shipped.
Fix: bounded autonomy (narrow scope per agent), failure isolation (a real check at every seam), human sign-off gated to the roughly 5% of steps that are irreversible, not everywhere.

## The one rule

If you remember nothing else: every layer's failure is silent by default, and every fix is the same move, making failure loud on purpose.

---

Full talk: https://www.moeezkhan.com/decks/cyc-2026.html
Full write-up: https://www.moeezkhan.com/writing/agentic-systems-fail-in-production
Part of the-three-ways.
