

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

import os
from pathlib import Path
from pprint import pprint


def load_yaml_from_file(_path: Path | str):
    if isinstance(_path, Path):
        return load(
            stream=_path.read_text(),
            Loader=Loader
        )
    elif isinstance(_path, str):
        return load(
            stream=Path(_path).read_text(),
            Loader=Loader
        )

    raise TypeError("_path is not Path or string")


def convert_yaml_to_string(_data: dict, _indent=4):
    if not isinstance(_data, dict):
        raise TypeError()

    return dump(_data, Dumper=Dumper, indent=_indent)

