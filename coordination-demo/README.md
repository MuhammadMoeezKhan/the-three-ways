# Coordination Demo (Layer 3: No-Cascade Coordination)

Status: planned, not yet implemented. Part of the-three-ways.

## What this will show

A minimal 3-agent pipeline: analyzer, migrator, validator.

Without a boundary: the analyzer produces a subtly wrong result. The migrator builds on it. The validator trusts the stage before it instead of independently checking, and rubber-stamps the error through. The whole pipeline looks healthy the entire time.

With a boundary: a real validation check at the seam between stages, plus a gated human sign-off on the one irreversible step. The same bad analyzer output gets caught and contained instead of cascading.

Two versions of the pipeline, boundary on and boundary off, so you can see the failure cascade vs. contained side by side.

See the top-level FAILURE_MAP.md for the full Layer 3 diagnostic, and the talk deck and write-up linked in the root README for the full walkthrough.
