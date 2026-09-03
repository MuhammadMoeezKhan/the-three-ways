"""The analyzer -> migrator -> validator pipeline, with the validation
boundary as a single on/off switch: same bug either way, only the
checking stage changes.
"""

from __future__ import annotations

from dataclasses import dataclass

from agents import (
    Analyzer,
    FakeIndependentValidator,
    Migrator,
    MigratedRecord,
    RealIndependentValidator,
)


@dataclass
class PipelineResult:
    migrated: list[MigratedRecord]
    validation_passed: bool
    problems: list[str]
    status: str  # "SHIPPED" or "BLOCKED_FOR_HUMAN_SIGNOFF"


def run(independent_validation: bool) -> PipelineResult:
    legacy = Analyzer().plan()
    migrator = Migrator()
    migrated = [migrator.migrate(record) for record in legacy]

    if independent_validation:
        passed, problems = RealIndependentValidator().check(legacy, migrated)
    else:
        passed, problems = FakeIndependentValidator().check(migrated)

    status = "SHIPPED" if passed else "BLOCKED_FOR_HUMAN_SIGNOFF"
    return PipelineResult(
        migrated=migrated, validation_passed=passed, problems=problems, status=status
    )
