import random
import time

import selenium.webdriver
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from requests.cookies import RequestsCookieJar

"""
- Переходим по рандомной ссылке из массива модуля Requests
- Прокручиваем страницу с рандомной задержкой
- Сохраняем Cookie в SQLite (обновляем значения профиля)
- Закрываем сессию"""

class Selenium_worker:
    __browsers = {'Firefox': (webdriver.Firefox, webdriver.firefox)}
    __browser: webdriver.Firefox = None
    __browser_type: str
    __options_str:  str | None
    __url: str
    __cookie: RequestsCookieJar

    def __init__(self, options_str: str | None, browser_type: str, url: str, cookie: RequestsCookieJar | None):
        self.__browser_type = browser_type
        self.__options_str = options_str
        self.__url = url
        self.__cookie = cookie
    def __options_str_parser(self) -> str:
        arr = self.__options_str.split(' -')

        yield arr[0]
        for opt in arr[1:]:
            yield f'-{opt}'


    def __set_browser(self):
        if not isinstance(self.__browser_type, str):
            raise TypeError('expected str')
        if self.__browser_type in self.__browsers:
            try:
                options = None
                if self.__options_str is not None:

                    options = self.__browsers[self.__browser_type][1].options.Options()
                    for opt in self.__options_str_parser():
                        options.add_argument(opt)
                self.__browser = self.__browsers[self.__browser_type][0](options)
            except WebDriverException as e:
                print(f'error in option setting: {e}')

        else:
            raise ValueError(f'expected value from{list(self.__browsers.keys())}')

    def __add_cookie(self):

        # RequestsCookieJar from requests to webdriver.{}.add_cookie() specific format
        if isinstance(self.__cookie, RequestsCookieJar):
            for key in self.__cookie.keys():
                self.__browser.add_cookie({'name': key, 'value': self.__cookie[key]})
        #todo

    def __scroll(self):
        script_scrolling = 'window.scrollBy(0, {});'
        script_get_height = 'return document.documentElement.scrollHeight'
        height_before_scroll = self.__browser.execute_script(script_get_height)

        scroll_pointer = 0
        height_page = height_before_scroll
        scroll_count = 500
        time_left_interval_sec = 0.1
        time_right_interval_sec = 0.5

        while scroll_pointer < height_page:
            scroll_pointer+=scroll_count
            self.__browser.execute_script(script_scrolling.format(scroll_count))
            current_height_page = self.__browser.execute_script(script_get_height)
            if height_before_scroll < current_height_page < height_before_scroll *2:
                # attempt to solve the problem with infinite scrolling,
                # if as a result of scrolling the height of the page will increase,
                # then the border for scrolling will move, but not more than twice from the initial one
                height_page = current_height_page

            time.sleep(random.uniform(time_left_interval_sec, time_right_interval_sec))

    def run(self):
        self.__set_browser()
        #self.__add_cookie()
        self.__browser.get(self.__url)
        self.__scroll()

    def get_cookies(self):
        return self.__browser.get_cookies()
    def close(self):
        self.__browser.quit()
        pass


