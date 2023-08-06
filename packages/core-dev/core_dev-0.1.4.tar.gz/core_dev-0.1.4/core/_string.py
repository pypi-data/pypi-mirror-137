

import string

def update_char(string, position, character):
    return string[ :position] + character + string[position + 1: ]


def find_all(string: str, pattern: str):
    return [index for index in range(len(string)) if string.startswith(pattern, index)]

def find_total(string: str, pattern: str):
    return len(find_all(string, pattern))
