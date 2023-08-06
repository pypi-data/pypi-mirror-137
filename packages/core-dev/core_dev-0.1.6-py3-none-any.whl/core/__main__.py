

from ._json import *
# translates to
# from core._json import *
# i would use like this in other python projects

x = {123: 123, "list": [1, 2, 3, 4, 5, 6, 7, 8, 9]}
print_json(x)

from ._rich import *

warning("salutare")