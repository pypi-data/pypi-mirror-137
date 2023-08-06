
import sys
import os
import logging
# from core._datetime import *
from core.aesthetics import *

colors = RGBColors()

from core.drive import *

from typing import Literal

sep_dimension = 30
exception_message = f"[{yellow_bold('DONT PANIC')}][this is your of {lime_green_bold('CATCHED')} exception]\n"
exception_message += f"[{lime_green_bold('VISUAL REPRESENTATION')}]"
exception_separator = f"[{lime_green_bold('=' * sep_dimension)}]"

def get_formatter(datetime_format="%d.%m.%Y-%H:%M:%S"):
    formatter = logging.Formatter(
        "[ %(asctime)s.%(msecs)04d - %(name)s - %(levelname)s ]\n%(message)s\n",
        datefmt=datetime_format
    )
    return formatter


def get_stream_handler(_level=logging.DEBUG):
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(_level)
    stream_handler.setFormatter(logging.Formatter(""))

    return stream_handler


def get_file_handler_with_datetime(folder=None, logfilename=None):
    current_datetime = get_current_datetime(__format="%d.%m.%Y__%H_%M_%S")
    if folder:
        if not os.path.exists(folder):
            os.makedirs(folder)

        if logfilename:
            log_file_name = os.path.join(folder, f"{logfilename}_{current_datetime}.log")
        else:
            log_file_name = os.path.join(folder, f"{current_datetime}.log")
    else:
        if logfilename:
            log_file_name = f"{logfilename}_{current_datetime}.log"
        else:
            log_file_name = f"{current_datetime}.log"

    # it takes over the file
    # and if you want to delete it
    # PermissionError: [WinError 32]
    # The process cannot access the file because it is being used by another process: 'logs\\test1.log'
    file_handler = logging.FileHandler(log_file_name)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(get_formatter())

    return file_handler

class TTYNotFoundError(Exception):
    pass

class CoreLogger(logging.Logger):
    """
        in order to achieve what you want to need to
        name the screen_logger and file_logger differently
    """

    def __init__(self, name: str = "CoreLogger", _level=logging.INFO, tty=None, file=None) -> None:
        super().__init__(name, level=_level)

        self._asctime_format = colors.red("%(asctime)s.%(msecs)04d")
        self._name_format = colors.yellow_bright("%(name)s")
        self._levelname_format = colors.red("%(levelname)s")
        self._message_format = colors.red("%(message)s")
        self._lineno_format = colors.red("%(lineno)d")
        self._module_format = colors.red("%(module)s")

        stream_formatter = logging.Formatter(
            f"[{self._asctime_format}] - [{self._levelname_format}] - [{self._name_format}] - [{self._message_format}] - {self._module_format}.py:{self._lineno_format}",
            # datefmt is the format for 'asctime'
            datefmt="%d.%m.%Y-%H:%M:%S")

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(self.level)
        stream_handler.setFormatter(stream_formatter)

        self.addHandler(stream_handler)

        if tty:
            if not os.path.exists(tty):
                raise TTYNotFoundError(f"tty: {tty} not found on the disk")


            tty_handler = logging.FileHandler(tty)
            tty_handler.setLevel(self.level)
            tty_handler.setFormatter(stream_formatter)

            self.addHandler(tty_handler)

        if file:
            if isinstance(file, str):
                self.file = Path(file)
            elif isinstance(file, Path):
                self.file = file
            else:
                raise TypeError("file must be type str or Path")

            self.file.parent.mkdir(parents=True, exist_ok=True)
            self.file_logger = logging.Logger("core-file-logger")

            file_formatter = logging.Formatter(
                f"[%(asctime)s.%(msecs)04d] - [%(name)s] - [%(levelname)s] - [%(message)s] - [%(module)s.py:%(lineno)d]",
                # datefmt is the format for 'asctime'
                datefmt="%d.%m.%Y-%H:%M:%S")

            file_handler = logging.FileHandler(self.file.absolute().as_posix())
            file_handler.setLevel(self.level)
            file_handler.setFormatter(file_formatter)

            self.file_logger.addHandler(file_handler)

        # _formatter = logging.Formatter(
        #     "%(asctime)s.%(msecs)04d - PID: %(process)d - %(name)s - %(levelname)s - %(message)s - line: %(lineno)d - module: %(module)s - pname: %(processName)s - thread id: %(thread)d - tname: %(threadName)s",
        #     datefmt="[%d.%m.%Y]-[%H:%M:%S]")

    def info(self, message: str) -> None:
        super().info(message)
        try:
            # this may not exist
            self.file_logger.info(message)
        except AttributeError:
            pass

    def error(self, message: str) -> None:
        super().error(message)
        try:
            # this may not exist
            self.file_logger.error(message)
        except AttributeError:
            pass

    def exception(self, message: str) -> None:
        _con = Console(record=True)
        _con.print_exception(show_locals=True, word_wrap=True)
        super().error(message + "\n" + _con.export_text(styles=True, clear=False))
        try:
            # this may not exist
            self.file_logger.error(message + "\n" + _con.export_text(styles=False, clear=False))
        except AttributeError:
            print("ia sa vedem")
            pass


    def __init2__(self, name,
        file_handler=None,
        stream_handler=None,
        foldername="logs",
        filename="log",
        clear_regularly=True # this will clear more than 10 logs in folder
    ):

        self.name = name
        self.folder_name = foldername
        self.clear_regularly = clear_regularly

        self.original_formatter = get_formatter()

        # exception logger
        self.exception_logger = logging.getLogger("exception." + self.name)
        # file logger
        self.file_logger = logging.getLogger(self.name)
        self.file_logger.setLevel(20)

        if file_handler:
            self.file_handler = file_handler
            self.file_logger.addHandler(file_handler)
            self.exception_logger.addHandler(file_handler)
        else:
            fh = get_file_handler_with_datetime(foldername, filename)
            self.file_logger.addHandler(fh)
            self.exception_logger.addHandler(fh)
            self.file_handler = fh

        self.log_file = str(self.file_logger.handlers[0])
        self.log_file = self.log_file.split(os.path.sep)
        self.log_file = self.log_file[-1].split()[0]
        # print(self.log_file)

        # screen logger
        self.screen_logger = logging.getLogger("stdout." + self.name)
        self.screen_logger.setLevel(20)

        if stream_handler:
            self.screen_logger.addHandler(stream_handler)
        else:
            self.screen_logger.addHandler(get_stream_handler())

        self.clear()


    def _info(self, message, print__=True, *args, **kwargs):
        self.file_logger.info(delete_ansi_codes(message))
        if print__:
            self.screen_logger.info(message.strip())



    def _exception(self, message, print__=True, *args, **kwargs):
        if print__:
            self.file_logger.info("")
            self.file_handler.setFormatter("")

            print(exception_message)
            self.file_logger.info(delete_ansi_codes(exception_message))

            print(exception_separator)
            self.file_logger.info(delete_ansi_codes(exception_separator) + "\n")

            exc_type, exc_value, exc_traceback = sys.exc_info()
            c = Colorizer("dark")
            c.colorize_traceback(exc_type, exc_value, exc_traceback)

        self.exception_logger.exception(message, *args, **kwargs)

        if print__:
            print(exception_separator)
            self.file_logger.info("\n" + delete_ansi_codes(exception_separator))

            self.file_logger.info("\n")
            self.file_handler.setFormatter(self.original_formatter)


    def clear(self):
        if self.clear_regularly:
            if self.folder_name:
                if len(os.listdir(self.folder_name)) > 10:
                    # print(self.log_file)
                    delete_folder_contents(self.folder_name, ignore=[self.log_file])
            else:
                handler = str(self.file_logger.handlers[0])
                items = handler.split(os.path.sep)
                self.logs_folder = items[-2]
                del items

                if len(os.listdir(self.logs_folder)) > 10:
                    # print(self.log_file)
                    # print(self.logs_folder)
                    delete_folder_contents(self.logs_folder, ignore=[self.log_file])



if __name__ == '__main__':
    log = CoreLogger("core",
        tty="/dev/pts/109",
        file="logs/_logging.log"
    )
    log.info("m-am scos")
    try:
        raise ValueError("hello world from /dev/pts/109")
    except ValueError:

        log.exception("naisu")
