

import pytest

from pytest_steps.steps import test_steps
from _core._math import fixed_set_precision_str
from _core._math import get_total_decimals


@pytest.mark.parametrize(
    "real_number, precision, expected_result",
    # testcases
    [
        (123.123, 2, "123.12"),
        ("123.123", 2, "123.12"),
        ("123.1231111111123123123123123", 2, "123.12"),
        (777, 2, "777.00"),
        (777.3333, 4, "777.3333"),
    ]
)
@test_steps(
    "correct number of decimals ?",
    "is type str ?",
    "result == expected ?"
)
def test_fixed_set_precision_str(
    real_number: float | str,
    precision: int,
    expected_result: float,
):
    try:
        # we know that this raises if the @real_number its not valid
        result = fixed_set_precision_str(real_number, precision)
        print(result)

    except TypeError as error:
        yield
        yield
        yield
    except ValueError as error:
        print(error)
        print("mario")
        print(str(error)) # str on error gives you the message
        yield
        yield
        yield

    else:
        _decimals = get_total_decimals(result)

        # correct number of decimals ?
        assert _decimals == precision
        yield

        # is type str ?
        assert isinstance(result, str)
        yield

        # result == expected ?
        assert result == expected_result
        yield





@pytest.mark.parametrize(
    "real_number, precision",
    # testcases
    [
        (TypeError("asd"), 2),
        (TypeError("asd"), 2),
        (TypeError("asd"), 2),
        (tuple([1, 2, 3]), 2),
    ]
)
def test_fixed_set_precision_str_exception_typeerror(
    real_number: float | str,
    precision: int,
):
    with pytest.raises(
        (TypeError),
        match="real_number: '.*' must be integer, float or string"
    ):
        fixed_set_precision_str(real_number, precision)


@pytest.mark.parametrize(
    "real_number, precision",
    # testcases
    [
        ("123123x.123123x", 2),
        ("123123x.x123", 2),
        ("xasd123b.x", 2),
        ("x.x", 2),
    ]
)
def test_fixed_set_precision_str_exception_valueerror(
    real_number: float | str,
    precision: int,
):
    with pytest.raises(
        (ValueError),
        match="cannot convert @real_number: '.*' to float"
    ):
        fixed_set_precision_str(real_number, precision)

