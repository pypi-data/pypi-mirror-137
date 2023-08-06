"""
    core/_random.py

    useful random stuff to import in your scripts
    contents (random):
        lowchar
        upperchar
        digit
        number
        lowerstring
        upperstring
        string
        date str
        date struct

    author: @alexzander
"""



# python
import time
from datetime import datetime
from random import randint, choice, random



# a-z 97-122
random_lowerchar = lambda : chr(randint(97, 122))
# A-Z 65-90
random_upperchar = lambda : chr(randint(65, 90))
# 0-9 48 57
random_digit = lambda : randint(0, 9)


def random_digits(_size: int = 1) -> str:
    if not isinstance(_size, int):
        raise TypeError(f"_size: '{_size}' must be type integer")
    if _size <= 0:
        raise ValueError("_size: '{_size}' cannot be <= 0")

    return "".join([str(random_digit()) for _ in range(_size)])


def random_number(_size: int = 1) -> int:
    if not isinstance(_size, int):
        raise TypeError(f"_size: '{_size}' must be type integer")
    if _size <= 0:
        raise ValueError("_size: '{_size}' cannot be <= 0")

    return int(str(randint(1, 9)) + "".join([str(random_digit()) for _ in range(_size - 1)]))


def random_lower_str(_size: int = 1):
    if not isinstance(_size, int):
        raise TypeError(f"_size: '{_size}' must be type integer")
    if _size <= 0:
        raise ValueError("_size: '{_size}' cannot be <= 0")

    return "".join([
        random_lowerchar() for _ in range(_size)
    ])


def random_upper_str(_size: int = 1):
    if not isinstance(_size, int):
        raise TypeError(
            f"_size: '{_size}' must be type integer")
    if _size <= 0:
        raise ValueError(
            "_size: '{_size}' cannot be <= 0")

    return "".join([
        random_upperchar() for _ in range(_size)
    ])


def random_str(_size: int = 1):
    if not isinstance(_size, int):
        raise TypeError(f"_size: '{_size}' must be type integer")
    if _size <= 0:
        raise ValueError("_size: '{_size}' cannot be <= 0")
    return "".join([
        choice([
            random_lowerchar(),
            random_upperchar(),
        ]) for _ in range(_size)
    ])


def random_date_str(
    starting_date="01.01.1971",
     ending_date=datetime.now().strftime("%d.%m.%Y")
):
    if starting_date is None or ending_date is None:
        raise TypeError

    datetime_format = "%d.%m.%Y"
    start_time = time.mktime(time.strptime(starting_date, datetime_format))
    stop_time = time.mktime(time.strptime(ending_date, datetime_format))
    random_time = start_time + random() * (stop_time - start_time)

    return time.strftime(datetime_format, time.localtime(random_time))


def random_date_struct(
    starting_date="01.01.1971",
    ending_date=datetime.now().strftime("%d.%m.%Y")
):
    if starting_date is None or ending_date is None:
        raise TypeError

    datetime_format = "%d.%m.%Y"
    start_time = time.mktime(time.strptime(starting_date, datetime_format))
    stop_time = time.mktime(time.strptime(ending_date, datetime_format))
    random_time = start_time + random() * (stop_time - start_time)

    return time.strptime(time.strftime(datetime_format, time.localtime(random_time)), datetime_format)