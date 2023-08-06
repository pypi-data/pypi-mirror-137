
import pytest
from pytest_steps.steps import test_steps

from _core._math import fixed_set_precision_float
from _core._math import get_total_decimals

@pytest.mark.parametrize(
    "real_number, precision, expected_result",
    # testcases
    [
        (123.123, 2, 123.12),
        ("123.123", 2, 123.12),
        ("123.1231111111123123123123123", 2, 123.12),
    ]
)
@test_steps(
    "correct number of decimals ?",
    "is type float ?",
    "result == expected ?"
)
def test_fixed_set_precision_float(
    real_number: float | str,
    precision: int,
    expected_result: float
):
    result = fixed_set_precision_float(real_number, precision)
    _decimals = get_total_decimals(result)

    # "correct number of decimals ?"
    assert _decimals == precision
    yield

    # "is type float ?",
    assert isinstance(result, float)
    yield

    # "result == expected ?"
    assert result == expected_result
    yield


@pytest.mark.parametrize(
    "real_number, precision",
    # testcases
    [
        ("x.x", 2),
        ("xasd123b.x", 3),
        ("123123x.x123", 4),
        ("123123x.123123x", 5),
    ]
)
def test_fixed_set_precision_float_exception(
    real_number: float | str,
    precision: int,
):
    with pytest.raises(
        ValueError,
        match="cannot convert @real_number: '.*' to float"
    ) as error:
        fixed_set_precision_float(real_number, precision)
