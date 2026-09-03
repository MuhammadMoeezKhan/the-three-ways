# the-three-ways

Companion repo for "The Three Ways AI Agents Fail. Here's How to Fix Yours.", a talk at Commit Your Code 2026 (Sept 3).

Talk deck: https://www.moeezkhan.com/decks/cyc-2026.html
Full write-up: https://www.moeezkhan.com/writing/agentic-systems-fail-in-production

## Status

Launched alongside the talk (Sept 3, 2026). The Failure Map checklist below is complete and ready to use today. The three runnable demos are being built out over the following days, each is marked below.

| Piece | Status |
|---|---|
| FAILURE_MAP.md | Done |
| tools-demo | Planned, not yet implemented |
| memory-demo | Planned, not yet implemented |
| coordination-demo | Planned, not yet implemented |

## The Failure Map

FAILURE_MAP.md, a one-page checklist for locating which of the three layers is breaking your agent, and the fix for each. Start here.

## Layer 1: Tools, Reliable Tool Calls

tools-demo: a loose vs. strict tool schema (typed inputs, an explicit error contract, idempotency), and a script showing the strict schema catching a bad call the loose one would silently accept.

## Layer 2: Memory, RAG vs. Knowledge Graph

memory-demo: a toy legacy codebase with a deliberately buried cross-file dependency, one script using plain retrieval (misses it), one using a shallow one-hop graph (catches it).

## Layer 3: Coordination, No-Cascade Coordination

coordination-demo: a minimal 3-agent pipeline (analyzer, migrator, validator) with a validation boundary and a gated human sign-off step, plus a version with the boundary removed, so you can see the failure cascade vs. contained.

## License

MIT, see LICENSE.

---

The opinions, insights, and perspectives in this repo and the accompanying talk are solely my own and do not reflect those of my current or past employers, nor do they convey any confidential information by any means.
