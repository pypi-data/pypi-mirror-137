#!/usr/bin/python3

import os
import subprocess
import sys
import curses
from curses import textpad, wrapper
from threading import Thread
from time import time, sleep
from textwrap import wrap
from copy import copy
from time import sleep
import pyperclip

# _curses
from _screen import NCursesScreen


class Application:
    def __init__(self, ncurses_screen: "curses._CursesWindow",) -> None:
        self.screen = NCursesScreen(ncurses_screen)
        self.text_wrap_width = self.screen.width - 3
        self.padding = 4
        self.y_codes = 4

        self.index = 0
        self.total_codes = len(self.auth_client.get_all_codes())

        curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_GREEN)
        self.selected_color = curses.color_pair(9)



    def print_otp_codes(self):
        codes_list = self.auth_client.get_all_codes()

        for index, code in enumerate(codes_list):
            line = code[0] + ": " + code[1]

            if index == self.index:
                self.screen.print_text(
                    self.y_codes + index, 0, code[0] + ": ", self.selected_color)
                self.screen.print_text(
                    self.y_codes + index, len(code[0] + ": "), code[1], self.selected_color)
            else:
                self.screen.print_text(
                    self.y_codes + index, 0, code[0] + ": ", self.screen.red_background)
                self.screen.print_text(
                    self.y_codes + index, len(code[0] + ": "), code[1], self.screen.yellow_foreground)




    def main(self):
        while 1:
            self.screen.draw_rectangle(0, 0, 2, 20)
            self.screen.print_text(1, 1, "Linux Authenticator")


            self.print_otp_codes()

            self.screen.print_text(10, 0, "use <up> / <down> to navigate")

            key = self.screen.get_char()
            self.key_entered = chr(key)
            self.screen.print_text(
                9, 0, str(key), self.screen.yellow_foreground)
            self.screen.print_text(
                9, 5, f"({self.key_entered.__repr__()})  ", self.screen.yellow_foreground)


            # up arrow key
            if key == 259:
                if self.index == 0:
                    self.index = self.total_codes - 1
                else:
                    self.index -= 1
            # down arrow key
            elif key == 258:
                if self.index == self.total_codes - 1:
                    self.index = 0
                else:
                    self.index += 1

            elif self.key_entered == "\n":
                self.print_otp_codes()
                self.screen.refresh()

                codes_list = self.auth_client.get_all_codes()
                for index, code in enumerate(codes_list):
                    if self.index == index:
                        self.screen.print_text(
                            12, 0, code[1], self.screen.yellow_foreground)
                        self.screen.print_text(
                            13, 0, "OTP token copied to clipbooard", self.screen.white_foreground)
                        pyperclip.copy(code[1])
                        break
            # q
            elif key == 113:
                os.system("clear")
                break


                # pressed enter to copy the code



                # if self.key_entered == "KEY_RESIZE":
                #     self.screen.resize()
                #     self.screen.refresh()

                # if not self.key_entered.isascii():
                #     continue

                # backspace part
                # if self.key_entered in ('KEY_BACKSPACE', '\b', '\x7f'):
                #     pass
                # else:
                #     pass

            self.screen.refresh()
            # sleep(1)



def NCursesApplication():
    """
        main application of the program
    """
    # Initialize curses
    ncurses_screen = curses.initscr()

    # Turn off echoing of keys, and enter cbreak mode,
    # where no buffering is performed on keyboard input
    curses.noecho()
    curses.cbreak()

    # In keypad mode, escape sequences for special keys
    # (like the cursor keys) will be interpreted and
    # a special value like curses.KEY_LEFT will be returned
    ncurses_screen.keypad(True)

    # Start color, too.  Harmless if the terminal doesn't have
    # color; user can test with has_color() later on.  The try/catch
    # works around a minor bit of over-conscientiousness in the curses
    # module -- the error return from C start_color() is ignorable.
    try:
        curses.start_color()
    except:
        pass

    #  block_cursor = "\x1b[\x32 q"
    #  beam_cursor = "\x1b[\x36 q"
    #  run_control_sequence(block_cursor)

    # setting up cursor
    # (3, 3, 3, 3)
    curses.curs_set(0)
    try:
        application = Application(ncurses_screen=ncurses_screen)
        application.main()

    # use BaseException to catch keyboard interrupt
    # if you dont clean up the ncurses app the terminal text
    # will be broken
    except BaseException as error:
        _, _, exc_traceback = sys.exc_info()
        error.with_traceback(exc_traceback)

        print(error)
        print(type(error))
        print("app stopped")



    # Set everything back to normal
    ncurses_screen.keypad(False)
    curses.echo()
    curses.nocbreak()
    curses.endwin()



    # https://stackoverflow.com/questions/11753909/clean-up-ncurses-mess-in-terminal-after-a-crash
    subprocess.call("stty sane", shell=True)


if __name__ == "__main__":
    NCursesApplication()
    #  ParseProgramArguments()
