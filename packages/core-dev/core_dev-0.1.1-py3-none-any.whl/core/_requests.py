
"""
    use get_dynamic_soup_async() function because its works on youtube which is dynamic and huge

    i dont understand why it isnt working with the chromium launch

    references:
        https://scrapingant.com/blog/scrape-dynamic-website-with-python
"""
from pyppeteer import launch
import asyncio
from bs4 import BeautifulSoup
import requests
from playwright.sync_api import sync_playwright

__DEBUG__ = False

def is_valid_url(url: str) -> None:
    if not isinstance(url, str):
        raise TypeError(f"url: {url} is not type [str]")

    if not url.startswith("http://") and \
       not url.startswith("https://"):
           raise ValueError(f"url: {url} its NOT a valid URL")

    __items = url.split("/")
    if len(__items) < 3:
        raise ValueError("url its NOT a valid URL")

    # protocol
    # domain name
    # urls params




def debug_print(message):
    if __DEBUG__:
        print(message)


def get_dynamic_soup(url: str, __debug=False) -> BeautifulSoup:
    is_valid_url(url)

    global __DEBUG__

    if __debug:
        __DEBUG__ = True

    with sync_playwright() as p:
        # Launch the browser
        debug_print("creating browser with 'p.chromium.launch()'")
        browser = p.chromium.launch()

        # Open a new browser page
        debug_print("creating 'page' variable with 'browser.new_page()'")
        page = browser.new_page()

        # Open our test file in the opened page
        debug_print(f"making get request to url: {url}")
        page.goto(url)

        # Process extracted content with BeautifulSoup
        debug_print("creating beautiful soup object with rendered html")
        soup = BeautifulSoup(page.content(), "html.parser")

        debug_print("browser was closed")
        browser.close()


        debug_print(f"soup of url: {url} returned with code=0")
        debug_print("__DEBUG__ set to False")
        __DEBUG__ = False
        return soup



# def get_dynamic_soup(url: str) -> BeautifulSoup:

#     with sync_playwright() as p:
#         browser = p.chromium.launch()

#         page = browser.new_page()

#         page.goto(url)

#         soup = BeautifulSoup(page.content(), "html.parser")

#         browser.close()

#         return soup





async def __get_dynamic_soup_async(url: str) -> BeautifulSoup:

    # Launch the browser
    browser = await launch()

    # Open a new browser page
    page = await browser.newPage()

    # Open our test file in the opened page
    await page.goto(url)
    page_content = await page.content()

    # Process extracted content with BeautifulSoup
    soup = BeautifulSoup(page_content, "html.parser")

    # Close browser
    await browser.close()

    return soup


def get_dynamic_soup_async(url: str) -> BeautifulSoup:
    is_valid_url(url)
    return asyncio.get_event_loop().run_until_complete(__get_dynamic_soup_async(url))


linux_user_agent = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0"
}


def get_static_soup(url: str, __debug=False) -> BeautifulSoup:
    global __DEBUG__

    if __debug:
        __DEBUG__ = True

    debug_print(
        f"making get request to url: {url}\nwith user agent: {linux_user_agent['User-Agent']}")
    response = requests.get(url, headers=linux_user_agent)

    if response.status_code != 200:
        debug_print(f"response from url is {response.status_code}")
        response.raise_for_status()

    debug_print("soup object created")
    soup = BeautifulSoup(response.text, "html.parser")

    debug_print(f"soup of url: {url} returned with code=0")
    debug_print("__DEBUG__ set to False")
    __DEBUG__ = False
    return soup


# testing
if __name__ == "__main__":
    url = "https://to-do.live.com/tasks/AQMkADAwATM0MDAAMS0wNWEyLTUwZmYALTAwAi0wMAoALgAAA0CfyhOovjZMnUDCre5DgecBAMZL-uR6QaxCoBkWelPVmtAAArZw4uwAAAA="
    url = "https://www.youtube.com/watch?v=qCZd757chzs"

    # s = get_dynamic_soup(url, True)
    # # print(s)
    # span = s.find("div", attrs={
    #     "class": "style-scope ytd-watch-flexy"
    # })
    # print(span)
    # print(span.get_text())

    s = get_dynamic_soup_async(url)
    print(s.find("h1", attrs={
        "class": "title style-scope ytd-video-primary-info-renderer"
    }).get_text())


