import loose_tool
import strict_tool


def test_loose_tool_silently_truncates():
    result = loose_tool.search_code("calculate_interest")
    returned = len(result.split(", "))
    total = len(loose_tool._CALL_SITE_INDEX["calculate_interest"])
    assert returned < total  # it's wrong...
    assert result != ""  # ...and gives no signal that it's wrong


def test_loose_tool_empty_and_missing_look_identical():
    assert loose_tool.search_code("this_function_does_not_exist") == ""


def test_strict_tool_flags_incomplete_results():
    result = strict_tool.search_code(strict_tool.KnownFunction.CALCULATE_INTEREST)
    assert isinstance(result, strict_tool.LowConfidence)
    assert "incomplete" in result.reason


def test_strict_tool_rejects_malformed_query():
    result = strict_tool.search_code("not a real function")
    assert isinstance(result, strict_tool.Failure)


def test_strict_tool_same_underlying_data_as_loose_tool():
    # Same bug, same data. The only difference is whether the caller
    # is told about it.
    loose = loose_tool.search_code("calculate_interest")
    strict = strict_tool.search_code(strict_tool.KnownFunction.CALCULATE_INTEREST)
    assert isinstance(strict, strict_tool.LowConfidence)
    assert len(strict.items) == len(loose.split(", "))
