"""
    _core/linux.py
"""

# python
import os
from string import Template
from pathlib import Path

# _core package
from core.shell import run_shell
from core.shell import get_output




def get_tty() -> str:
    """
        Function: get_tty()
        Summary:
            gets current tty of the terminal on
                which current python script is running
        Examples:
            >>> get_tty()
            '/dev/pts/40'

        Returns: tty path as string
    """
    return get_output("tty")



def ls(cwd=os.getcwd()):
    return get_output(f"ls {cwd}").split("\n")

def la(cwd=os.getcwd()):
    return get_output(f"la {cwd}").split("\n")

def ll(cwd=os.getcwd()):
    return get_output(f"ls -la {cwd}").split("\n")





def append_line_on_tty(_tty: str, line: str | bytes) -> None:
    if not isinstance(line, (str, bytes)):
        raise TypeError(f"@line: '{line}' must be of type string or bytes like object")

    # https://bugs.python.org/issue20074
    # how i got tihs
    with open(_tty, "+ba", buffering=0) as tty:
        if isinstance(line, bytes):
            tty.write(line)
        else:
            tty.write(f"\n".encode("utf-8"))



# WARNING
# you cannot read text from tty
# def readlines_from_tty(_tty: str):


notify_send_template = Template(
    "notify-send \"${title}\" \"${message}\" --icon=${icon} --expire-time=${expire_time}"
)

def notification(title: str, message: str, icon: Path | str = None, exp=5) -> None:
    """
        Function: notification
        Summary: runs notify-send as subprocess from python, sends linux notification
        Examples:
            # this is now you would run on linux shell
            >>> shell > notify-send '202020Rule' 'ITS TIME NOW !!!' --icon=/home/alexzander/Alexzander__/programming/python/202020_order/assets/icons/202020-order-icon.png

            # this is now you would run from python code
            >>> notification("timer", "message", "~/Alexzander__/programming/python3/projects/timer/icons/timer.png", 5)


        Attributes:
            @param (title:str):InsertHere
            @param (message:str):InsertHere
            @param (icon:Path|str) default=None: icon must be located at cwd or can be full path
            @param (exp) default=5: InsertHere
        Returns: None
    """

    if icon:
        if isinstance(icon, str):
            icon = Path(icon)

        if not icon.exists():
            raise NotImplementedError("icon doesnt exist on the disk")

        icon = icon.absolute().as_posix()
    else:
        icon = ""

    # if i dont specify exp, the default value its not working
    # the notification will last more than 5 seconds
    # even if exp=5, .... :(
    run_shell(notify_send_template.safe_substitute(
        title=title,
        message=message,
        icon=icon,
        expire_time=exp * 1000 # cuz its miliseconds
    ))



# if __name__ == '__main__':
#     linux_notification(
#         "title from code",
#         "message from code",
#         "/home/alexzander/Alexzander__/programming/python/202020_order/assets/icons/202020-order-icon.png"
#     )
