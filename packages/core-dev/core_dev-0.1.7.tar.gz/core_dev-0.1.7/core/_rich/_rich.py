"""
    core/_rich.py

    a wrapper around a very good module _rich

    @author: alexzander
    started development at: 03.01.2022
    editor used: sublime text 4
"""

# 3rd party
# pip install rich
from rich.console import Console
from rich.theme import Theme
from rich.text import Text


# python
from typing import Callable


# locals
__warning_message = Text("  WARNING  ")
__warning_message.stylize("black on yellow")

__error_message = Text("  ERROR  ")
__error_message.stylize("black on red")

__success_message = Text("  SUCCESS  ")
__success_message.stylize("black on green")

_con = Console()
_print = _con.print


def rich_exception_decorator(
    _function: Callable = None,
    *,
    show_locals=True,
    word_wrap=True
) -> Callable:
    """
        wraps a function and prints rich exception
        if it raises error
    """
    def _inner_decorator(_function: Callable):
        def _inner_wrapper(*args, **kwargs):
            try:
                _function(*args, **kwargs)
            except Exception:
                _con.print_exception(
                    show_locals=show_locals,
                    word_wrap=word_wrap
                )
        return _inner_wrapper

    if _function is None:
        return _inner_decorator
    return _inner_decorator(_function=_function)


@rich_exception_decorator
def warning(_message: str = None):
    """
    Function: warn
    Summary: just a warning
    Examples: InsertHere
    Returns: InsertHere
    """
    if _message:
        if not isinstance(_message, str):
            try:
                _message = str(_message)
            except ValueError as __error:
                raise ValueError(
                    f"cant convert @_message to 'str'. _message => {_message}")

        _con.print(__warning_message, _message)



@rich_exception_decorator
def error(_message: str = None):
    """
    Function: warn
    Summary: just a warning
    Examples: InsertHere
    Returns: InsertHere
    """
    if _message:
        if not isinstance(_message, str):
            try:
                _message = str(_message)
            except ValueError as __error:
                raise ValueError(
                    f"cant convert @_message to 'str'. _message => {_message}")

        _con.print(__error_message, _message)





@rich_exception_decorator
def success(_message: str = None):
    """
    Function: warn
    Summary: just a warning
    Examples: InsertHere
    Returns: InsertHere
    """
    if _message:
        if not isinstance(_message, str):
            try:
                _message = str(_message)
            except ValueError as __error:
                raise ValueError(
                    f"cant convert @_message to 'str'. _message => {_message}")

        _con.print(__success_message, _message)



if __name__ == '__main__':

    @rich_exception_decorator
    def func():
        # pass
        raise ValueError(123)

