# coordination-demo

Layer 3 from the talk: No-Cascade Coordination.

A minimal analyzer → migrator → validator pipeline in [`agents.py`](./agents.py), migrating five legacy account balances (a plain `"1200.00"` format, or `"75.00 CR"` for a credit/negative balance) into a new numeric format. The migrator has one real bug: the credit-marker check is case-sensitive, so a balance written as `"75.00 cr"` (lowercase) comes out positive instead of negative. It never raises, so it reports success regardless.

[`pipeline.py`](./pipeline.py) wires the three stages together with the validation boundary as a single switch:

- **`FakeIndependentValidator`**: what most "independent verification" stages actually are. It only checks whether the migrator reported success.
- **`RealIndependentValidator`**: re-derives the correct answer from the original source data itself, without looking at what the migrator claimed.

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

Same migrator, same bug, both runs. With the fake validator, the corrupted record ships silently, the pipeline reports `SHIPPED` and nobody knows account A4 is off by $150. With the real validator, the pipeline reports `BLOCKED_FOR_HUMAN_SIGNOFF` and names exactly which record and why. `test_coordination.py` locks in both: the bug exists and self-reports success either way, and only the real validator catches it, on exactly the one record that's actually wrong, not a false-positive on the four that are fine.

Bounded autonomy and failure isolation only work if the check at the seam is real. A validator that just asks the previous stage "are you okay?" is not a validator, it's a rubber stamp with an official-sounding name.

Part of [the-three-ways](../).
