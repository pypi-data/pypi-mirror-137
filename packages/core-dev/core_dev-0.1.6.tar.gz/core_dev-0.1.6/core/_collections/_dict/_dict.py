
"""
    core/_collections/_dict/_dict.py

    This module contains an upgraded version of the
        primitive built-in dict from python.
    This module also contains a custom-built error
        used only for the class Dict.

    Current state: in development.
"""

# python
# from sys import getsizeof


# core/_collections/_dict
# from exceptions import DictException
from .exceptions import EmptyDictError


class Dict(dict):
    def __init__(self, *arguments, **keywordArguments):
        self.container = {}
        if len(arguments) == 1:
            if type(arguments[0]) != dict:
                raise TypeError
            self.container.update(arguments[0])

        elif len(arguments) > 1:
            if not all(type(x) == dict for x in arguments):
                raise TypeError

            for argument in arguments:
                self.container.update(argument)

        if keywordArguments != {}:
            temporary = {}
            for key, argument in keywordArguments.items():
                temporary.update({key: argument})
            self.container.update(temporary)


    def update(self, *arguments, **keywordArguments):
        if not all(type(x) == dict for x in arguments):
            raise TypeError

        for argument in arguments:
            self.container.update(argument)

        if keywordArguments != {}:
            temporary = {}
            for key, argument in keywordArguments.items():
                temporary.update({key: argument})
            self.container.update(temporary)


    def is_empty(self):
        return self.container == {}


    def copy(self):
        if self.is_empty():
            raise EmptyDictError(self.container)
        return Dict(self.container.copy())


    def clear(self):
        self.container.clear()