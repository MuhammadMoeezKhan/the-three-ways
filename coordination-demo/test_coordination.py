import pipeline


def test_migrator_has_a_real_bug_on_lowercase_credit_marker():
    result = pipeline.run(independent_validation=True)
    a4 = next(r for r in result.migrated if r.id == "A4")
    assert a4.new_balance == 75.00  # wrong: should be -75.00
    assert a4.self_reported_success is True  # and it doesn't know it


def test_fake_validation_lets_the_bug_ship():
    result = pipeline.run(independent_validation=False)
    assert result.validation_passed is True
    assert result.status == "SHIPPED"


def test_real_validation_catches_the_bug():
    result = pipeline.run(independent_validation=True)
    assert result.validation_passed is False
    assert result.status == "BLOCKED_FOR_HUMAN_SIGNOFF"
    assert any("A4" in problem for problem in result.problems)


def test_real_validation_only_flags_the_actually_wrong_record():
    result = pipeline.run(independent_validation=True)
    assert len(result.problems) == 1
