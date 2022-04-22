'''
Author: Yaaprogrammer
Date: 2022-04-15 18:59:49
LastEditors: Yaaprogrammer
LastEditTime: 2022-04-22 20:03:36

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
import random
from time import sleep

import regex as re
import requests
from loguru import logger
from tenacity import retry, retry_if_exception_type, stop_after_attempt

from utils import Configuration


class Crawler:
    retryTimes = Configuration().getProperty("crawler.retry.times")

    def __init__(self) -> None:
        self.__session = requests.Session()
        self.__response = requests.Response()
        self.__config = Configuration()

    @property
    def response(self):
        return self.__response.content.decode('utf-8')

    @retry(retry=retry_if_exception_type(requests.exceptions.RequestException),
           stop=stop_after_attempt(retryTimes))
    def get(self, url: str) -> None:
        self.__randomDelay()
        verify = self.__whetherVerify()
        timeout = self.__getTimeOut()
        headers = self.__getHeaders()
        self.__response = self.__session.get(url=url,
                                             verify=verify,
                                             timeout=timeout,
                                             headers=headers)
        logger.info(f"Get: {url}")

    @retry(retry=retry_if_exception_type(requests.exceptions.RequestException),
           stop=stop_after_attempt(retryTimes))
    def post(self, url: str, data: dict) -> None:
        self.__randomDelay()
        verify = self.__whetherVerify()
        timeout = self.__getTimeOut()
        headers = self.__getHeaders()
        self.__response = self.__session.post(url=url,
                                              data=data,
                                              verify=verify,
                                              timeout=timeout,
                                              headers=headers)
        logger.info(f"Post: {url}")

    def __getHeaders(self):
        return self.__config.getProperty('crawler.headers')

    def __getTimeOut(self) -> int:
        return self.__config.getProperty("crawler.timeout")

    def __whetherVerify(self) -> bool:
        return self.__config.getProperty("crawler.verify")

    def __randomDelay(self) -> None:
        min = self.__config.getProperty("crawler.delay.min")
        max = self.__config.getProperty("crawler.delay.max")
        delay = random.randint(min, max)
        logger.info(f"Random delay: {delay}")
        sleep(delay)

    def regSearchFromResponse(self, pattern: str) -> str:
        return re.search(
            pattern,
            self.__response.content.decode('utf-8'),
        ).group()

    def existInResponse(self, searchFor: str) -> bool:
        return self.__response.content.decode('utf-8').find(searchFor) != -1
