
"""
    system.py

    useful module in accesing and using system stuff

    author: @alexzander
"""

# python
import os
import sys
import platform
from pathlib import Path

# core package ( pip installpython-core )
from core.exceptions import *
from core.aesthetics import *


def get_operating_system():
    return platform.system().lower()


def get_python_path():
    """ return folder path """
    if os.environ["PYTHONPATH"].endswith(";"):
        return os.environ["PYTHONPATH"][:-1]
    return os.environ["PYTHONPATH"]


def get_computer_name():
    return platform.node()


def get_tesseract_path():
    """ return executable of tesseract engine (if installed) """
    if "TESS" not in os.environ.keys():
        raise NotFoundError("TESS is not environment variables")
    return os.environ["TESS"]


def clearscreen():
    """ clears the shell screen depending on the opearting system """
    o = get_operating_system()
    if o == "windows":
        os.system("cls")
    else:
        os.system("clear")


def pauseprogram(
        message=f"[ press {green_bold('<enter>')} to continue... ]\n"):
    input(message)


def get_arhitecture():
    return platform.architecture()[0]


def get_python_version():
    return platform.python_version()


def get_python_implementation():
    return platform.python_implementation()


def get_processor():
    return platform.processor()


def get_python_interpreter_path():
    return sys.executable

from core._math import fixed_set_precision_float

cpu_system_file = Path("/proc/stat")
def get_CPU_percentage():
    cpu_line = cpu_system_file.read_text().split("\n")[0]
    items = list(map(int, cpu_line.split()[1:]))

    idle_percentage = (items[3] * 100) / sum(items)
    idle_percentage = fixed_set_precision_float(idle_percentage, 2)
    cpu_usage_percentage = 100 - idle_percentage
    
    return cpu_usage_percentage


def is_running_with_sudo():
    try:
        os.environ["SUDO_UID"]
    except KeyError:
        return False

    return True

# TESTING
if __name__ == '__main__':
    o = get_operating_system()
    print(o)
