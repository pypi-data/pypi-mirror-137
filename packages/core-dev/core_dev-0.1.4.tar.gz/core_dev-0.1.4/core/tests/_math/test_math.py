

import pytest

# pip install pytest_steps
from pytest_steps.steps import test_steps




from _core._math import hex_to_int

@pytest.mark.parametrize(
    "hex_string, expected_result",
    # testcases
    [
        (0x000000000, 0),
        (0x0, 0),
        (0x00, 0),
        ("0x000000000", 0),
        ("0x0", 0),
        ("0x00", 0),
    ]
)
def test_hex_to_int(
    hex_string: int | str,
    expected_result: float
):

    result = hex_to_int(hex_string)
    assert isinstance(result, int)
    assert result == expected_result


@pytest.mark.parametrize("_hex", [
    (12.12),
    (TypeError("asd")),
])
def test_hex_to_int_exception(_hex):
    with pytest.raises(
        (TypeError),
        match="@hex_string: '.*' should be type string or integer"
    ) as error:
        hex_to_int(_hex)
