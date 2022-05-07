import datetime
import json
import os
import smtplib
from copy import deepcopy
from email.header import Header
from email.mime.text import MIMEText
from functools import wraps

from loguru import logger
from yaml import FullLoader, load


class Banner:

    def __init__(self) -> None:
        with open('banner.txt', "r", encoding="utf-8") as f:
            rows = f.readlines()
            self.content = self.__CombineRows(rows)

    def printBanner(self) -> str:
        print(self.content)

    def __CombineRows(self, rows) -> str:
        result = ""
        for row in rows:
            result += row
        return result


class PostDataLoader:

    def loadByKey(self, key: str) -> dict:
        path = "post_data.json"
        with open(path, encoding='utf-8') as f:
            file = json.load(f)
        logger.info(f"Load json: {path}")
        try:
            data = file[key]
        except KeyError:
            logger.exception(f"{path}中不存在键: {key}")
        return data


class EmailController:

    def __setUpSmtpConnection(self) -> smtplib.SMTP_SSL:
        config = Configuration()
        host = config.getProperty("smtp.host")
        port = config.getProperty("smtp.port")
        user = config.getProperty("smtp.user")
        password = config.getProperty("smtp.password")

        smtpObj = smtplib.SMTP_SSL(host) if config.getProperty(
            "smtp.ssl") else smtplib.SMTP(host)
        smtpObj.connect(host, port)
        smtpObj.login(user, password)
        return smtpObj

    def __buildHtmlMessage(self, title: str, html: str) -> MIMEText:
        config = Configuration()
        message = MIMEText(html, 'html', 'utf-8')
        message['From'] = Header(config.getProperty("smtp.message.from"),
                                 'utf-8')
        message['To'] = Header(config.getProperty("smtp.message.to"), 'utf-8')
        timeNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message['Subject'] = Header(f"{title}-{timeNow}", 'utf-8')
        return message

    def __sendMessage(self, smtpObj: smtplib.SMTP_SSL,
                      message: MIMEText) -> None:
        config = Configuration()
        sender = config.getProperty("smtp.user")
        receivers = config.getProperty("smtp.message.receivers")
        smtpObj.sendmail(sender, receivers, message.as_string())

    def __send(self, title: str, html: str):
        try:
            smtpObj = self.__setUpSmtpConnection()
            message = self.__buildHtmlMessage(title, html)
            self.__sendMessage(smtpObj, message)
            logger.success(f"邮件发送成功:{title}")
        except smtplib.SMTPException:
            logger.exception("无法发送邮件")

    def send(self, title: str, html: str) -> None:
        config = Configuration()
        if (config.getProperty("smtp.enable") is True):
            self.__send(title=title, html=html)


def Singleton(cls):
    instances = {}

    @wraps(cls)
    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return getinstance


@Singleton
class Configuration:

    def __init__(self) -> None:
        with open('config.yml', mode="r", encoding="utf-8") as f:
            self.__config = load(f, Loader=FullLoader)
        if (os.path.exists("config_custom.yml")):
            with open('config_custom.yml', mode="r", encoding="utf-8") as f:
                customConfig = load(f, Loader=FullLoader)
                self.__config = self.deepMerge(self.__config, customConfig)
        self.__cache = {}

    def addProperty(self, key: str, value: any) -> None:
        self.__config[key] = value

    def deepMerge(self, a, b, path=None):
        if path is None:
            path = []
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    self.deepMerge(a[key], b[key], path + [str(key)])
                elif a[key] == b[key]:
                    pass
                else:
                    a[key] = b[key]
            else:
                a[key] = b[key]
        return a

    def setProperty(self, key: str, value: any) -> None:
        config = self.__config
        try:
            segments = key.split(".")
            for segment in segments:
                if (not isinstance(config[segment], dict)):
                    config[segment] = value
                config = config[segment]
        except KeyError:
            logger.exception(f"wrong property key:{key}")
        else:
            logger.debug(f"set property:{key}={config}")
            self.__cache[key] = config
        pass

    def getProperty(self, key: str) -> None:
        if (key in self.__cache):
            return self.__cache[key]
        config = deepcopy(self.__config)
        try:
            for segment in key.split("."):
                config = config[segment]
        except KeyError:
            logger.exception(f"wrong property key:{key}")
        else:
            logger.debug(f"read property:{key}={config}")
            self.__cache[key] = config
        return config


class MyLogger:

    @staticmethod
    def startLogging() -> None:
        config = Configuration()
        if (config.getProperty("logger.enable") is True):
            dateNow = datetime.datetime.now().strftime('%Y-%m-%d')
            logPath = os.path.join(os.getcwd(), "log")
            if not os.path.isdir(logPath):
                os.makedirs(logPath)
            logFilePath = os.path.join(logPath, f"{dateNow}.log")
            logger.add(
                logFilePath,
                format="{time:YYYY-MM-DD HH:mm:ss}  |\
{level}> {elapsed}  | {message}",
                encoding='utf-8',
                retention='7 days',
                backtrace=True,
                diagnose=True,
            )
            logger.info('Logging started')
