

import os
from core.shell import get_output
from core.shell import run_shell

from string import Template

def _exa_exists():
    _exit_code = run_shell("which exa", devnull=True)
    return _exit_code == 0


class BinaryNotFoundError(Exception):
    pass

exa_command_template = Template("exa ${__icons} ${__all}")


"""
❱  exa --long --header --git --icons --all --created --modified --inode --extended
   inode Permissions Size User       Date Modified Date Created Git Name
 2889758 drwxr-xr-x     - alexzander  9 Jan 19:18   3 Jan 18:56  --  .git
 2759072 .rw-r--r--   121 alexzander  8 Jan 20:11   3 Jan 19:00  --  .gitignore
 6819543 drwxr-xr-x     - alexzander  3 Jan 19:23   3 Jan 19:23  -I  .pytest_cache
 3284306 drwxr-xr-x     - alexzander  9 Jan 19:06   3 Jan 20:42  -N  _core
 2759116 .rw-r--r--    45 alexzander  6 Jan 16:11   6 Jan 16:11  -I  _core.sublime-project
 2759117 .rw-r--r--  407k alexzander  8 Jan 18:27   6 Jan 16:11  -I  _core.sublime-workspace
 3284457 .rw-r--r--   747 alexzander  6 Jan 17:14   6 Jan 17:13  --  conftest.py
 2759080 .rw-r--r--     0 alexzander  3 Jan 20:43   3 Jan 20:43  --  Dockerfile
11930943 drwxr-xr-x     - alexzander  8 Jan 19:54   8 Jan 19:54  -I  logs
 2759075 .rw-r--r--   590 alexzander  6 Jan 18:20   3 Jan 19:22  --  Makefile
 2759088 .rwxr-xr-x  1.4k alexzander  6 Jan 17:35   4 Jan 14:23  --  pepe
 2759086 .rw-r--r--   680 alexzander  8 Jan 18:46   4 Jan 14:01  --  Pipfile
 2758699 .rw-r--r--   71k alexzander  8 Jan 18:47   8 Jan 18:47  --  Pipfile.lock
 2759052 .rw-r--r--   324 alexzander  6 Jan 19:00   3 Jan 18:50  --  pyrightconfig.json
 2759073 .rw-r--r--   125 alexzander  6 Jan 17:08   3 Jan 19:21  --  pytest.ini
 2759074 .rw-r--r--   285 alexzander  6 Jan 20:27   3 Jan 19:00  --  readme.md
 2759085 .rw-r--r--  1.6k alexzander  6 Jan 20:27   4 Jan 13:56  --  requirements.txt
 2758407 .rw-r--r--     0 alexzander  8 Jan 20:11   8 Jan 20:11  --  setup.py
 3020288 drwxr-xr-x     - alexzander  3 Jan 20:31   3 Jan 20:29  --  test_core
 2759015 .rw-r--r--    82 alexzander  7 Jan 23:00   7 Jan 22:59  --  TODO.md

"""

def exa(cwd=os.getcwd(), icons=True, _all=True, ):
    if not _exa_exists():
        raise BinaryNotFoundError("exa not found on system")

    __icons = ""
    if icons:
        __icons = "--icons"

    __all = ""
    if _all:
        __all = "--all"
    return get_output(exa_command_template.safe_substitute(
        __icons=__icons,
        __all=__all)).split("\n")