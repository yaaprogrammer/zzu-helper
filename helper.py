'''
Author: Yaaprogrammer
Date: 2022-04-14 19:10:04
LastEditors: Yaaprogrammer
LastEditTime: 2022-09-25 08:55:07

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''

from loguru import logger

from crawler import Crawler
from utils import Configuration, EmailController, PostDataLoader


class Helper:

    def __init__(self) -> None:
        self.__crawler = Crawler()
        self.__config = Configuration()

    def __get(self, url: str) -> None:
        self.__crawler.get(url)

    def __post(self, url: str, data: dict) -> None:
        self.__crawler.post(url, data)

    def __getTwoId(self) -> dict:
        sidPattern = self.__config.getProperty("pattern.sid")
        sid = self.__crawler.regSearchFromResponse(sidPattern)
        logger.info(f"sid: {sid}")
        ptoidPattern = self.__config.getProperty("pattern.ptopid")
        ptopid = self.__crawler.regSearchFromResponse(ptoidPattern)
        logger.info(f"ptopid: {ptopid}")
        return {"ptopid": ptopid, "sid": sid}

    def __regSearchByPatternKey(self, patternKey: str) -> str:
        pattern = self.__config.getProperty("pattern." + patternKey)
        value = self.__crawler.regSearchFromResponse(pattern)
        logger.info(f"{patternKey}: {value}")
        return value

    def __searchLoginIframeUrl(self) -> str:
        return self.__regSearchByPatternKey("login_iframe")

    def __searchUnknownPair(self) -> dict:
        unknownKey = self.__regSearchByPatternKey("unknown_key")
        unknownValue = self.__regSearchByPatternKey("unknown_value")
        return {unknownKey: unknownValue}

    def __searchLoginPostUrl(self) -> str:
        return self.__regSearchByPatternKey("login_url")

    def __searchRedirectUrl(self) -> str:
        return self.__regSearchByPatternKey("redirect_url")

    def __searchUserProfileIframeUrl(self) -> str:
        return self.__regSearchByPatternKey("user_profile_url")

    def __setFun18Pair(self):
        self.__fun18Pair = {"fun18": self.__regSearchByPatternKey("fun18")}

    def __getIndexPage(self) -> None:
        logger.info("Start")
        baseUrl = self.__config.getProperty("url.base")
        self.__get(baseUrl)

    def __getLoginIframePage(self) -> None:
        iframeUrl = self.__searchLoginIframeUrl()
        self.__get(iframeUrl)

    def __fillLoginPostData(self) -> dict:
        dataLoader = PostDataLoader()
        loginFixedData = dataLoader.loadByKey("login")
        username = self.__config.getProperty("zzu.username")
        password = self.__config.getProperty("zzu.password")
        unknownPair = self.__searchUnknownPair()
        loginData = {}
        loginData.update(loginFixedData)
        loginData.update({"uid": username})
        loginData.update({"upw": password})
        loginData.update(unknownPair)
        logger.debug(f"login data: {loginData}")
        return loginData

    def __fillEntryPostData(self) -> dict:
        dataLoader = PostDataLoader()
        entryFixedData = dataLoader.loadByKey("entry")
        entryData = {}
        entryData.update(entryFixedData)
        entryData.update(self.__getTwoId())
        # self.__setFun18Pair()
        # entryData.update(self.__fun18Pair)
        return entryData

    def __fillSubmitPostData(self) -> dict:
        dataLoader = PostDataLoader()
        submitFixedData = dataLoader.loadByKey("submit")
        submitData = {}
        submitData.update(submitFixedData)
        submitData.update(self.__getTwoId())
        return submitData

    def __login(self) -> None:
        postUrl = self.__searchLoginPostUrl()
        loginData = self.__fillLoginPostData()
        self.__post(postUrl, loginData)
        logger.success("Login success")

    def __getUserProfile(self) -> None:
        redirectUrl = self.__searchRedirectUrl()
        self.__get(redirectUrl)
        userProfileUrl = self.__searchUserProfileIframeUrl()
        self.__get(userProfileUrl)

    def __isFilledToday(self) -> bool:
        flag = self.__config.getProperty("flag.profile")
        return self.__crawler.existInResponse(flag)

    def __checkFilled(self):
        checkOnly = self.__config.getProperty("args.check_only")
        if (self.__isFilledToday()):
            logger.info("今日已经填报过了")
            if (checkOnly):
                emailController = EmailController()
                emailController.send("今日已经填报过", self.__crawler.response)
        else:
            logger.info("今日还没有填报过")
            if (checkOnly):
                emailController = EmailController()
                emailController.send("今日还没有填报", self.__crawler.response)

    def __entryFillTable(self):
        data = self.__fillEntryPostData()
        url = self.__config.getProperty("url.post")
        self.__post(url, data)
        logger.debug(self.__crawler.response)

    def __submitTable(self):
        data = self.__fillSubmitPostData()
        url = self.__config.getProperty("url.post")
        self.__post(url, data)

    def __checkIfSucceeded(self):
        successFlag = self.__config.getProperty("flag.submit")
        resubmitFlag = self.__config.getProperty("flag.resubmit")
        failFlag = self.__config.getProperty("flag.fail")
        if (self.__crawler.existInResponse(successFlag)):
            logger.success("提交成功")
        elif (self.__crawler.existInResponse(resubmitFlag)):
            logger.success("你今日的健康状态上报信息已通过审核")
        elif (self.__crawler.existInResponse(failFlag)):
            logger.error("提交失败")
            logger.info("response: " + self.__crawler.response)
            emailController = EmailController()
            emailController.send("填报失败", self.__crawler.response)
        else:
            logger.error("未知错误")
            logger.info("response: " + self.__crawler.response)
            emailController = EmailController()
            emailController.send("未知错误", self.__crawler.response)

    def run(self) -> None:
        self.__getIndexPage()
        self.__getLoginIframePage()
        self.__login()
        self.__getUserProfile()
        self.__checkFilled()
        self.__entryFillTable()
        self.__submitTable()
        self.__checkIfSucceeded()

    def check(self) -> None:
        self.__getIndexPage()
        self.__getLoginIframePage()
        self.__login()
        self.__getUserProfile()
        self.__checkFilled()
