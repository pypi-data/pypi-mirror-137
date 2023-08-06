

from _core.servers import is_ip_address_valid
# from pytest_steps.steps import test_steps

# @test_steps(
#     "is result bool ?",
#     "result == expected ?"
# )
import pytest
@pytest.mark.parametrize("ip_address, expected_result", [
    ("0.0.0.0", True),
    (123, False),
    ("192.168.1.123", True),
    ("256.123.123.123", False),
])
def test_is_ip_address_valid(
    ip_address: str,
    expected_result: bool
):
    # print(ip_address)
    assert is_ip_address_valid(ip_address) == expected_result


