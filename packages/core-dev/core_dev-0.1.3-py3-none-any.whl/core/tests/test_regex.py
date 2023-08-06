

import pytest
from _core.regex import is_ip_address_valid_regex

@pytest.mark.parametrize("ip_address, expected_result", [
    ('23.45.12.56', True),
    ('I.Am.not.an.ip', False),
    ("192.168.1.101", True),
])
def test_is_ip_address_valid_regex(ip_address: str, expected_result: bool):
    assert is_ip_address_valid_regex(ip_address) == expected_result