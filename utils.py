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


def Singleton(cls):
    instances = {}

    @wraps(cls)
    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return getinstance


class Banner:

    def __init__(self) -> None:
        with open('./banner.txt', "r", encoding="utf-8") as f:
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
        path = "./post_data.json"
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
        if (config.getProperty("args.no_email") is False):
            self.__send(title=title, html=html)


@Singleton
class Configuration:

    def __init__(self) -> None:
        with open('./config.yml', mode="r", encoding="utf-8") as f:
            self.__config = load(f, Loader=FullLoader)
        if (os.path.exists("./config_custom.yml")):
            with open('./config_custom.yml', mode="r", encoding="utf-8") as f:
                customConfig = load(f, Loader=FullLoader)
                self.__config = DictUtil.deepMerge(self.__config, customConfig)
                print(self.__config)
        self.__cache = {}

    def addProperty(self, key: str, value: any) -> None:
        self.__config[key] = value

    def getProperty(self, item: str) -> None:
        if (item in self.__cache):
            return self.__cache[item]
        config = deepcopy(self.__config)
        try:
            for segment in item.split("."):
                config = config[segment]
        except KeyError:
            logger.exception(f"错误的配置属性:{item}")
        else:
            logger.debug(f"读取配置:{item}={config}")
            self.__cache[item] = config
        return config


class DictUtil:

    @staticmethod
    def deepMerge(a, b, path=None):
        if path is None:
            path = []
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    DictUtil.deepMerge(a[key], b[key], path + [str(key)])
                elif a[key] == b[key]:
                    pass  # a和b中有相同的键，且值相同
                else:
                    a[key] = b[key]  # a和b中有相同的键，覆盖a的值
            else:
                a[key] = b[key]  # b有a没有的键，添加到a
        return a


class MyLogger:

    @staticmethod
    def startLogging() -> None:
        config = Configuration()
        if (config.getProperty("args.log_no_file") is False):
            dateNow = datetime.datetime.now().strftime('%Y-%m-%d')
            logPath = os.path.join(os.getcwd(), "logs")
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
