
import pytest

from _core.datetime_ import is_valid_date_format
@pytest.mark.parametrize("date_str, expected_result", [
    ("12.12.1202", True),
    ("12.12.3202", True),
    ("12.12.3202123", False),
    ("12.122.2023", False),
    ("121.12.2023", False),
    ("121.x.2023", False),
    ("x.x.2023", False),
    ("x.x.y", False),
])
def test_is_valid_date_format(
    date_str: str,
    expected_result: bool):
    assert is_valid_date_format(date_str) == expected_result


from _core.datetime_ import is_valid_time_format
@pytest.mark.parametrize("time_str, expected_result", [
    ("03:12:23", True),
    ("03:12:1013", False),
    ("0x:1x:13", False),
    ("00:00:00", True),
    ("23:59:59", True),
    ("24:59:59", False),
    ("60:60:70", False),
])
def test_is_valid_time_format(
    time_str: str,
    expected_result: bool):
    assert is_valid_time_format(time_str) == expected_result


