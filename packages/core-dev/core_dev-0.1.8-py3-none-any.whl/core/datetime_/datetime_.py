
"""

    powerful time, date, and datetime module
    useful in development of programs that
    work with the concept of time

    upgraded version of time.py and datetime.py

    %Y  - year: 2022
    %m  - month: [01, 12]
    %d  Day of the month as a decimal number [01,31].
    %H  Hour(24-hour clock) as a decimal number [00,23].
    %M  Minute as a decimal number [00,59].
    %S  Second as a decimal number [00,61].
    %z  Time zone offset from UTC.
    %a  Locale's abbreviated weekday name.
    %A  Locale's full weekday name.
    %b  Locale's abbreviated month name.
    %B  Locale's full month name.
    %c  Locale's appropriate date and time representation.
    %I  Hour(12-hour clock) as a decimal number [01,12].
    %program  Locale's equivalent of either AM or PM.

    author: @alexzader
"""


# WHY YOU CANT NAME YOUR MODULES AS _MODULE.PY
"""
ImportError while importing test module '/home/alexzander/Alexzander__/programming/dev/
python3/_core/_core/tests/test_datetime.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
../../../../../.local/share/virtualenvs/_core-2r4s7-gL/lib/python3.10/site-packages/_py
test/python.py:578: in _importtestmodule
    mod = import_path(self.fspath, mode=importmode)
../../../../../.local/share/virtualenvs/_core-2r4s7-gL/lib/python3.10/site-packages/_py
test/pathlib.py:524: in import_path
    importlib.import_module(module_name)
/usr/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
<frozen importlib._bootstrap>:1050: in _gcd_import
    ???
<frozen importlib._bootstrap>:1027: in _find_and_load
    ???
<frozen importlib._bootstrap>:1006: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:688: in _load_unlocked
    ???
../../../../../.local/share/virtualenvs/_core-2r4s7-gL/lib/python3.10/site-packages/_py
test/assertion/rewrite.py:170: in exec_module
    exec(co, module.__dict__)
_core/tests/test_datetime.py:4: in <module>
    from _datetime import is_valid_date_format
E   ImportError: cannot import name 'is_valid_date_format' from '_datetime' (/usr/lib/p
ython3.10/lib-dynload/_datetime.cpython-310-x86_64-linux-gnu.so)
"""

# python
from time import time
from time import sleep
import calendar
from datetime import datetime
from datedelta import datedelta
from collections import namedtuple


# core package ( pip install python-core )
from core._math import fixed_set_precision_float
from core._math import fixed_set_precision_str
from core import aesthetics


__date_format = "%d.%m.%Y"
__time_format = "%H:%M:%S"

__datetime_format = "{}-{}".format(__date_format, __time_format)
__timedate_format = "{}-{}".format(__time_format, __date_format)


def is_valid_date_format(
    date_str: str,
    _date_format: str = __date_format) -> bool:
    """
        >>> is_valid_date_format("12.12.2021")
        >>> True

        >>> is_valid_date_format("12.14.2021")
        >>> False
    """
    try:
        datetime.strptime(date_str, _date_format)
    except:
        return False
    return True


def is_valid_time_format(
    time_str: str,
    _time_format: str = __time_format) -> bool:
    """
        # 3 AM 12 minutes and 23 seconds
        >>> is_valid_time_format("03:12:23")
        >>> True

        >>> is_valid_time_format("03:12:123")
        >>> False
    """
    try:
        # strptime takes no keyword arguments
        datetime.strptime(time_str, _time_format)
    except:
        return False
    return True


def is_valid_datetime_format(
    datetime_str: str,
    _datetime_format: str = __datetime_format) -> bool:
    try:
        datetime.strptime(datetime_str, _datetime_format)
    except:
        return False
    return True


def get_current_date(__format=__date_format):
    return datetime.now().strftime(__format)


def get_current_time(__format=__time_format):
    return datetime.now().strftime(__format)


def get_current_time_obj(__format=__time_format):
    return datetime.strptime(get_current_time(), __format)


def get_current_hour():
    return datetime.now().strftime("%H")

def get_current_minute():
    return datetime.now().strftime("%M")


def get_current_datetime(__format=__datetime_format):
    return datetime.now().strftime(__format)

def get_current_datetime_obj(__format=__datetime_format):
    return datetime.strptime(datetime.now().strftime(__format), __format)


def get_current_timedate(__format=__timedate_format):
    return datetime.now().strftime(__format)


def get_current_timestamp():
    return datetime.timestamp(datetime.now())


def get_date_from_timestamp(_timestamp: float):
    datetime.fromtimestamp(_timestamp).strftime(__date_format)


def get_time_from_timestamp(_timestamp: float):
    datetime.fromtimestamp(_timestamp).strftime(__time_format)


def get_datetime_from_timestamp(_timestamp: float):
    datetime.fromtimestamp(_timestamp).strftime(__datetime_format)


def timestamp_to_date(seconds: int, __format=__date_format):
    return datetime.fromtimestamp(seconds).strftime(__format)


def timestamp_to_time(seconds: int, __format=__time_format):
    return datetime.fromtimestamp(seconds).strftime(__format)


def timestamp_to_datetime(seconds: int, __format=__datetime_format):
    return datetime.fromtimestamp(seconds).strftime(__format)


def is_leap_year(year) -> bool: #):
    if type(year) not in [int, str]:
        raise TypeError(f"year: {year} is invalid type: {type(year)}")

    if 1 <= year <= 9999:
        if year % 400 == 0:
            return True
        elif year % 100 == 0:
            return False
        elif year % 4 == 0:
            return True
    return False


def GetOrthodoxPasteDate(year):
    if year in range(1900, 2100):
        a = year % 19
        b = year % 4
        c = year % 7
        d = (19 * a + 15) % 30
        e = (2 * b + 4 * c + 6 * d + 6) % 7
        day = 4 + d + e
        month = "April"
        if day > 30:
            day = day - 30
            month = "May"

        from collections import namedtuple
        PasteOrthodox = namedtuple("PasteOrthodox", ["year", "month", "day"])
        return PasteOrthodox(year, month, day)





def seconds_to_time(seconds: float | str | int):
    """
        >>> seconds_to_time(123761273612)
        Time(
            millennials=0,
            centuries=0,
            decades=5,
            years=1,
            weeks=9,
            days=2,
            hours=0,
            minutes=38,
            seconds=5
        )
        you can select whatever you want from this named tuple
    """
    if not isinstance(seconds, (str, int, float)):
        raise TypeError(f"seconds: '{seconds}' must be string, integer or float")

    seconds = int(seconds)

    time_intervals_as_seconds = {
        "millennia": 60 * 60 * 24 * 365 * 1000,
        "century": 60 * 60 * 24 * 365 * 100,
        "decade": 60 * 60 * 24 * 365 * 10,
        "year": 60 * 60 * 24 * 365,
        "week": 60 * 60 * 24 * 7,
        "day": 60 * 60 * 24,
        "hour": 60 * 60,
        "minute": 60,
        "second": 1
    }

    intervals = [
        "millennials",
        "centuries",
        "decades",
        "years",
        "weeks",
        "days",
        "hours",
        "minutes",
        "seconds"
    ]
    time_intervals_values = {
        "millennials": 0,
        "centuries": 0,
        "decades": 0,
        "years": 0,
        "weeks": 0,
        "days": 0,
        "hours": 0,
        "minutes": 0,
        "seconds": 0,
    }


    for _seconds, _interval in zip(time_intervals_as_seconds.values(), intervals):
        result = seconds // _seconds # type: ignore
        seconds -= result * _seconds
        time_intervals_values[_interval] = result

    return namedtuple("Time", intervals)(*time_intervals_values.values())



def get_execution_time(__function, *params):
    before = time()
    result = __function(*params)
    if result != None:
        print(result)

    duration = time() - before
    duration = fixed_set_precision_str(duration, 2)
    return duration


def print_execution_time(__function, *params):
    print("execution time: [ {} second(s) ]".format(get_execution_time(__function, *params)))



class Time(object):
    """ contains date and time attributes"""
    def __init__(self,
        _timestamp=None,
        _date=None,
        _time=None,
        _datetime=None):

        if _timestamp:
            if not isinstance(_timestamp, float):
                raise TypeError()

            self.timestamp = _timestamp
            self.date = get_date_from_timestamp(self.timestamp)
            self.time = get_time_from_timestamp(self.timestamp)
            self.datetime = get_datetime_from_timestamp(self.timestamp)





def datetime_object_to_str(datetime_object, __format=__datetime_format):
    return datetime_object.strftime(__format)



def VisualTimer(seconds=None, minutes=None, hours=None):
    _seconds = 0
    if seconds:
        _seconds += seconds
    if minutes:
        _seconds += minutes * 60
    if hours:
        _seconds += hours * 3600

    for _seconds in range(_seconds, -1, -1):
        time_left = seconds_to_time(_seconds)

        minutes = time_left.minutes
        if minutes < 10:
            minutes = f"0{minutes}"

        hours = time_left.hours
        if hours < 10:
            hours = f"0{hours}"

        _seconds = time_left.seconds
        if _seconds < 10:
            _seconds = f"0{_seconds}"

        time_left = aesthetics.yellow_bold(f"{hours}:{minutes}:{_seconds}")
        print(f"Time Left: [  {time_left}  ]", end="\r")
        sleep(1)


def days_difference(start_date, stop_date=get_current_date()) -> int:
    if stop_date == get_current_date():
        if type(start_date) == str:
            _start_date = datetime.strptime(start_date, __date_format)
        else:
            _start_date = start_date
    return (stop_date - _start_date).days



def get_current_month_name() -> str:
    return datetime.now().strftime("%B")

def get_current_year() -> int:
    return int(datetime.now().strftime("%Y"))


# TESTING
if __name__ == '__main__':
    # seconds_from_epoch = 1613990285.4035895
    # inputs = [
    #     seconds_from_epoch,
    #     3601,
    #     time.time(),
    #     54786.123952345
    # ]
    # for _input in inputs:
    #     result = seconds_to_time(_input)
    #     print(result)
    result = seconds_to_time(3600)
    attrs = [item for item in dir(result) if "_" not in item and item != "count" and item != "index"]

    for name, value in zip(attrs, result):
        print(name, value)
