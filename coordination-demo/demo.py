"""Run the same buggy migration through two pipelines: one where the
validator just trusts the migrator's self-report, one where it
independently re-checks the source data.

    python demo.py
"""

import pipeline


def main() -> None:
    print("=== Pipeline with FAKE independent validation ===")
    result = pipeline.run(independent_validation=False)
    for record in result.migrated:
        print(f"  {record.id}: migrated to {record.new_balance:.2f}  (self-reported: success)")
    print(f"  validator verdict: {'PASSED' if result.validation_passed else 'FAILED'}")
    print(f"  status: {result.status}")
    print("  -> A4 shipped as +75.00. It should be -75.00. Nobody caught it,")
    print("     the validator only ever asked the migrator how it felt.\n")

    print("=== Pipeline with REAL independent validation ===")
    result = pipeline.run(independent_validation=True)
    for record in result.migrated:
        print(f"  {record.id}: migrated to {record.new_balance:.2f}")
    print(f"  validator verdict: {'PASSED' if result.validation_passed else 'FAILED'}")
    for problem in result.problems:
        print(f"    - {problem}")
    print(f"  status: {result.status}")
    print("  -> Same bug, same migrator. The only difference is the validator")
    print("     re-derived the expected answer instead of trusting a flag.")


if __name__ == "__main__":
    main()
