"""Three agents in a legacy-to-new-format migration pipeline: an Analyzer
that plans the work, a Migrator that does it (with a real bug), and two
Validators: one that's independent verification in name only, and one
that actually is.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LegacyRecord:
    id: str
    raw: str  # e.g. "1200.00" or "75.00 CR" (CR = credit, i.e. negative)


@dataclass
class MigratedRecord:
    id: str
    new_balance: float
    self_reported_success: bool


LEGACY_RECORDS = [
    LegacyRecord("A1", "1200.00"),
    LegacyRecord("A2", "50.00 CR"),
    LegacyRecord("A3", "300.00"),
    LegacyRecord("A4", "75.00 cr"),  # lowercase "cr", the trap
    LegacyRecord("A5", "0.00"),
]


class Analyzer:
    """Plans the migration: which records need to move, in what order."""

    def plan(self) -> list[LegacyRecord]:
        return list(LEGACY_RECORDS)


class Migrator:
    """Converts each legacy record to the new numeric format.

    Bug: the credit-marker check is case-sensitive. It correctly handles
    'CR' but silently mishandles 'cr', so a credit balance written in
    lowercase comes out positive instead of negative. The migrator has
    no idea this happened, it never raises, so it reports success on
    every record, including the wrong one.
    """

    def migrate(self, record: LegacyRecord) -> MigratedRecord:
        raw = record.raw.strip()
        is_credit = raw.endswith("CR")  # bug: doesn't also check "cr"
        numeric_part = raw.removesuffix("CR").removesuffix("cr").strip()
        amount = float(numeric_part)
        if is_credit:
            amount = -amount
        return MigratedRecord(id=record.id, new_balance=amount, self_reported_success=True)


class FakeIndependentValidator:
    """What most 'validator' stages actually are: trust in a costume.
    It only ever looks at what the previous stage said about itself.
    """

    def check(self, migrated: list[MigratedRecord]) -> tuple[bool, list[str]]:
        problems = [m.id for m in migrated if not m.self_reported_success]
        return (len(problems) == 0, problems)


class RealIndependentValidator:
    """Actual independent verification: re-derive the correct answer from
    the original source, without looking at what the migrator claimed.
    """

    @staticmethod
    def _expected(raw: str) -> float:
        raw = raw.strip()
        if raw.upper().endswith("CR"):  # case-insensitive, the correct rule
            return -float(raw[:-2].strip())
        return float(raw)

    def check(
        self, legacy: list[LegacyRecord], migrated: list[MigratedRecord]
    ) -> tuple[bool, list[str]]:
        by_id = {m.id: m for m in migrated}
        problems = []
        for record in legacy:
            expected = self._expected(record.raw)
            actual = by_id[record.id].new_balance
            if abs(expected - actual) > 1e-9:
                problems.append(
                    f"{record.id}: expected {expected:.2f}, migrator produced {actual:.2f}"
                )
        return (len(problems) == 0, problems)
