"""
    _core/spinners.py
"""

# python packages
import sys
import asyncio
import itertools
from threading import Thread
from time import sleep

# typing
from typing import List
from typing import Callable
from typing import Dict
from typing import Tuple
from typing import Any
from typing import TypeVar, Type

from inspect import isfunction


# _core package
# pip install _core
from core.aesthetics import *


SpinnerDotsType = TypeVar('SpinnerDotsType', bound='SpinnerDots')
BackgroundThreadType = TypeVar("BackgroundThreadType", bound="BackgroundThread")


class BackgroundThread:
    def __init__(self, _function: Callable, *args, **kwargs) -> None:
        self._function: Callable = _function
        self.__background_thread = Thread(target=self._function, args=args, kwargs=kwargs)
        self.name = self.__background_thread.name


    def start(self):
        self.__background_thread.start()


    def is_done(self):
        return not self.__background_thread.is_alive()



class SpinnerDots:
    def __init__(self,
        identifier: str,
        message: str,
        color: str = "yellow",
        _background_job: Callable = None,
        *args,
        **kwargs
    ) -> None:
        self.identifier = identifier
        self.message = message
        self.color = color
        self.frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.len_frames = len(self.frames)
        self.index = 0
        self.completed = False

        if _background_job and isfunction(_background_job):
            self._background_job_thread = BackgroundThread(_background_job, *args, **kwargs)


        # self.state = f"[{green(self.identifier)}] pending ..."


    def animate(self, _sleep: float = 0.1) -> None:
        while 1:
            self.next()
            self.print_state()

            if self._background_job_thread.is_done():
                self.done()
                break

            sleep(_sleep)


    def start(self) -> None:
        self._background_job_thread.start()
        self.animate()

    def is_done(self) -> bool:
        return self._background_job_thread.is_done()


    def next(self) -> "SpinnerDots":
        if self.completed:
            return self

        self.state = f"{green(self.frames[self.index % self.len_frames])} {ConsoleColored(self.message, self.color)}"
        # self.state = f"{self.frames[self.index % self.len_frames]} {self.message}"
        self.index += 1
        return self


    def done(self) -> "SpinnerDots":
        self.state = f"[{yellow(self.identifier)}] {green('completed')}"
        # self.state = f"[{self.identifier}] {'completed'}"
        self.completed = True
        return self


    def print_state(self, __end="\r"):
        """
        Function: print_state
        Summary:
            this function must always be run after self.next()
        Examples: InsertHere
        Attributes:
            @param (self):InsertHere
            @param (__end) default="\r": InsertHere
        Returns: InsertHere
        """
        print(self.state, end=__end)


    def get_state(self) -> str:
        return self.state






def background_job1(param: str):
    print(f"job 1 with '{param}' started")
    # sleep(10)
    for i in range(50):
        sleep(0.1)
        pass


def background_job2(param: str):
    print(f"job 2 with '{param}' started")
    # sleep(10)
    for i in range(100):
        sleep(0.01)
        pass






class TasksList:
    def __init__(self,
        tasks_and_spinners:
            Tuple[
                List[SpinnerDots],
                List[BackgroundThread]
            ] = None,
        /,
        name=None,
        spinners_list=None,
        tasks_list=None) -> None:

        self.name = name

        if tasks_and_spinners is None:
            assert spinners_list != None, f"@spinners_list must not be None if @tasks_and_spinners is None"
            assert tasks_list != None, f"@tasks_list must not be None if @tasks_and_spinners is None"

            self.tasks_list = tasks_list
            self.spinners_list = spinners_list
        else:
            assert isinstance(tasks_and_spinners, tuple)
            assert isinstance(tasks_and_spinners[0], list)
            assert isinstance(tasks_and_spinners[1], list)

            for spinner, task in zip(tasks_and_spinners[0], tasks_and_spinners[1]):
                assert isinstance(spinner, SpinnerDots)
                assert isinstance(task, BackgroundThread)

            self.spinners_list = tasks_and_spinners[0]
            self.tasks_list = tasks_and_spinners[1]


    def all_tasks_done(self) -> bool:
        for task in self.tasks_list:
            if not task.is_done():
                return False
        return True


    def _terminate_spinners(self):
        line = ""
        for spinner in self.spinners_list:
            spinner.done()
            if self.multiline:
                line += spinner.get_state() + "\n"
            else:
                line += spinner.get_state() + " "
        print(line)

    def start(self, _sleep=0.1, multiline=False):
        self.multiline = multiline

        for task in self.tasks_list:
            task.start()

        # main thread its used for animations
        while 1:
            # if at least one background task is done
            # its spinner should be updated to completed
            if self.all_tasks_done():
                self._terminate_spinners()
                break

            total_done = 0
            line = ""
            for (index, spinner), task in zip(enumerate(self.spinners_list), self.tasks_list):
                if task.is_done():
                    total_done += 1
                    self.spinners_list[index].done()
                else:
                    spinner.next()

                if multiline:
                    line += spinner.get_state() + "\n"
                else:
                    line += spinner.get_state() + " "

                print(line, end="\r")

            if total_done == len(self.tasks_list):
                break


            # ce treaba are loading spinnerul
            # cu 2 threaduri care merg in background ?????
            # daca sunt threaduri in background
            # se misca foarte prost pentru ca aparent
            # acest while loop este influentat de cate threaduri sunt active in background
            # atata timp cat folosesti python
            # daca rulezi cu pypy3, se misca foarte bine
            #
            # asta pentru ca in python daca ai un for care nu face nimic
            # python aloca resurse multe pentru acel for
            # si de-aia se misca prost
            # print(spinners_list[0].next().get_state(), end="\r")
            sleep(_sleep)




def _test_spinner_py():
    """
        this function is synchronous
    """

    spinners_list = [
        SpinnerDots("1", "its me mario", "red"),
        SpinnerDots("2", "loading time", "yellow"),
        SpinnerDots("3", "third", "cyan"),
        SpinnerDots("4", "fourth", "cyan"),
    ]
    tasks_list = [
        BackgroundThread(background_job1, "Andrew is here"),
        BackgroundThread(background_job2, "Andrew is NOT here"),
        BackgroundThread(background_job1, "Andrew"),
        BackgroundThread(background_job2, "yeaaaaah"),
    ]

    tasks_list = TasksList(
        spinners_list=spinners_list,
        tasks_list=tasks_list)
    tasks_list.start()






if __name__ == '__main__':
    _test_spinner_py()


