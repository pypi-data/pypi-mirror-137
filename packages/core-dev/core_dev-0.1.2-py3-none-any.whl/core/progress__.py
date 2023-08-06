
from pyppeteer import launch
import asyncio
from bs4 import BeautifulSoup

from core.aesthetics import *
import itertools
import sys
import asyncio as asc
from rich.progress import *
from time import sleep

# progress = Progress(
#     SpinnerColumn(),
#     " loading ...",
# )

# with progress:
#     for _ in progress.track(range(100)):
#         sleep(0.1)


async def not_async_func():
    print("started")
    print("smoething very interesting about life")
    # await asyncio.sleep(0)
    # without this sleep of 0 it will not work
    for _ in range(1000000): await asc.sleep(0)
    # for _ in range(1000000000): pass
    print("done" + " " * 80)
    return {"data": 123}


async def render_dots_spinner(message: str, color: str = "yellow") -> None:
    # write = sys.stdout.write
    # flush = sys.stdout.flush
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    for dot in itertools.cycle(frames):
        line = f"{green(dot)} {yellow(message)}"
        print(line, end="\r")
        # write(line)
        # flush()
        # write('\x08' * len(line))
        try:
            await asc.sleep(0.1)  # <3>
        except asc.CancelledError:  # <4>
            # print()
            # write(" " * len(line))
            # flush()
            # write('\x08' * len(line))
            # print("i was interrupted from async mother")
            break
    # write(' ' * len(line) + '\x08' * len(line))


async def __run_spinner_with_background_task():
    job_task = asc.create_task(not_async_func())
    spinner_task = asc.create_task(render_dots_spinner("loading ,,,"))

    response = await job_task
    print(response)


def run_spinner_with_background_task():
    asc.run(__run_spinner_with_background_task())



async def __get_dynamic_soup_async(url: str) -> BeautifulSoup:
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)
    page_content = await page.content()
    soup = BeautifulSoup(page_content, "html.parser")
    await browser.close()
    return soup


async def get_dynamic_soup_async(url: str):
    spinner = asyncio.create_task(render_dots_spinner('awaiting beautiful soup ...'))
    return await asyncio.create_task(__get_dynamic_soup_async(url))





import itertools
from time import sleep
from core.aesthetics import *
from threading import Thread


class SpinnerThread():
    def __init__(self, message: str, color: str = "yellow"):
        self.message = message
        self.color = color
        self.is_active = False
        self.frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.__spinner_thread = Thread(target=self.__render, args=())


    def start(self) -> None:
        self.is_active = True
        self.__spinner_thread.start()


    def __render(self) -> None:
        for dot in itertools.cycle(self.frames):
            if self.is_active:
                line = f"{green(dot)} {ConsoleColored(self.message, self.color)}"
                print(line, end="\r")
                sleep(0.1)
            else:
                self.__print_completed()
                break

    def __print_completed(self):
        print("done" + " " * (len(self.message) - 3), end="\r")
        print()


    def run_task_in_background(self, function, *args, **kwargs):
        self.start()
        function(*args, **kwargs)
        self.stop()



    def stop(self):
        self.is_active = False


def simple_job(some_parameter):
    if some_parameter == "some_parameter":
        print(f"trying to do some job in the background: {some_parameter}")
        for i in range(100000000):
            # print('asd')
            pass
    else:
        print("i will not respect the paramater")
        for i in range(10000000000000):
            pass


if __name__ == "__main__":
    spinner = SpinnerThread(" loading ... ")
    spinner.run_task_in_background(simple_job, "some_parameter")