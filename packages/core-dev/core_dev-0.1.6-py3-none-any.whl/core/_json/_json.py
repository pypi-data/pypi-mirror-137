
"""
    core/_json.py

    upgraded version of json.py
    useful in work with jsons

    author: @alexzander
"""


# python imports
import json
from pathlib import Path
from typing import Callable
from typing import Any
from typing import Dict
from typing import List


# 3rd party
# pip install rich
# or
# python3.10 -m pip install rich
from rich.console import Console


# locals
_con = Console()


def load_json_from_file(_path: Path | str) -> dict:
    """
        reads .json from @_path
    """

    if isinstance(_path, str):
        with open(_path, "r+", encoding="utf-8") as _json:
            return json.loads(_json.read())

    elif isinstance(_path, Path):
        return json.loads(_path.read_text())

    else:
        raise TypeError(
            f"{_path} is not type str;"
            " type({__path})=={type(__path)}")



def load_json_from_string(_string: str) -> dict:
    """
    Function: load_json_from__string
    Summary: loads json from _string
    Examples: InsertHere
    Attributes:
        @param (_string:str):InsertHere
    Returns: InsertHere
    """
    if not isinstance(_string, str):
        try:
            _string = str(_string)
        except Exception:
            raise ValueError(
                f"cannot convert parameter"
                " @_string: {_string} to type 'str'")

    return json.loads(_string)


def write_json_to_file(
    __collection: dict,
    destination: str,
    __indent=4
):

    if isinstance(destination, str):
        with open(destination, "w+", encoding="utf-8") as _json:
            _json.truncate(0)
            if isinstance(__collection, dict) or isinstance(__collection, list):
                _json.write(json.dumps(__collection, indent=__indent))
            else:
                _json.write(json.dumps(
                    __collection,
                    indent=__indent,
                    default=lambda custom_object: custom_object.__dict__
                ))

    elif isinstance(destination, Path):
        if isinstance(__collection, dict) or isinstance(__collection, list):
            destination.write_text(json.dumps(
                __collection,
                indent=4
            ))
        else:
            destination.write_text(json.dumps(
                __collection,
                indent=4,
                default=lambda custom_object: custom_object.__dict__
            ))


def prettify(__collection, __indent=4):
    if isinstance(__collection, dict) or isinstance(__collection, list):
        return json.dumps(__collection, indent=__indent)

    # this default is useful when you want
    # to make your class JSON Serializable
    return json.dumps(
        __collection,
        indent=__indent,
        default=lambda custom_object: custom_object.__dict__
    )


def pretty_print(__collection, __indent=4):
    print(prettify(__collection, __indent=__indent))





def print_json(_data: Dict[Any, Any] | str, _indent: int = 4) -> None:
    """
        Function: print_json
        Summary: prints json to stdout/console/terminal/screen
        Examples:
            >>> _dict = {
            >>>     "a": "asd",
            >>>     "list": [
            >>>         1, 12, 123, 123, 123, 123, 123
            >>>     ]
            >>> }
            >>> print_json(_dict)

        Attributes:
            @param (_data:Dict[Any):InsertHere
            @param (Any]|str):InsertHere
            @param (_indent:int) default=4: InsertHere

        Returns: None
    """
    if not isinstance(_indent, int):
        raise TypeError(_indent)

    if isinstance(_data, str):
        _con.print_json(_data, indent=_indent)

    elif isinstance(_data, dict):
        _con.print_json(data=_data, indent=_indent)

    else:
        raise TypeError(
            f"param @_data should only get 'str' or 'dict'. _data => '{_data}'")




# TESTING locally
if __name__ == '__main__':
    _dict = {
        "a": "asd",
        "list": [
            1, 12, 123, 123, 123, 123, 123
        ]
    }

    print_json(_dict)
