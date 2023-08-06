

import pytest

from _core.random_ import random_digits
from _core.random_ import random_number
from _core.random_ import random_str
from _core.random_ import random_lower_str
from _core.random_ import random_upper_str
from _core.random_ import random_date_str
from _core.random_ import random_date_struct


@pytest.mark.parametrize("_size, expected_len", [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
    (11, 11),
    (12, 12),
    (13, 13),
    (14, 14),
    (15, 15),
    (16, 16),
    (17, 17),
    (18, 18),
    (19, 19),
    (20, 20),
    (21, 21),
])
def test_random_digits(_size, expected_len):
    result = random_digits(_size)
    assert isinstance(result, str)
    assert len(result) == expected_len

@pytest.mark.parametrize("_size, expected_len", [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
    (11, 11),
    (12, 12),
    (13, 13),
    (14, 14),
    (15, 15),
    (16, 16),
    (17, 17),
    (18, 18),
    (19, 19),
    (20, 20),
    (21, 21),
])
def test_random_number(_size, expected_len):
    result = random_number(_size)
    assert isinstance(result, int)
    assert len(str(result)) == expected_len

