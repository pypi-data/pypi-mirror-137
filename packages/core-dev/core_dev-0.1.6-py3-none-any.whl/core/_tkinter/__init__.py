

import tkinter
from pathlib import Path

def window_add_logo(window: tkinter.Tk, logo: Path | str):
    if not isinstance(window, tkinter.Tk):
        raise TypeError(f"@window: '{window}' must be of type tkiner.Tk (a Tk window)")

    if isinstance(logo, str):
        app_logo = tkinter.PhotoImage(file=logo)
    elif isinstance(logo, Path):
        app_logo = tkinter.PhotoImage(file=str(logo.absolute()))
    else:
        raise TypeError(f"@logo: '{logo}' must be of type string or Path object")


    window.tk.call("wm", "iconphoto", window._w, app_logo)

