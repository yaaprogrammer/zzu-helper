'''
Author: Yaaprogrammer
Date: 2022-04-14 20:54:28
LastEditors: Yaaprogrammer
LastEditTime: 2022-04-22 19:47:32

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
import argparse
import traceback

import urllib3
from tenacity import retry, stop_after_attempt

from helper import Helper
from utils import Banner, Configuration, EmailController, MyLogger, logger


def run():
    config = Configuration()
    helper = Helper()
    if (config.getProperty("args.check_only") is True):
        helper.check()
    else:
        helper.run()


def parseArgs():
    args = argparse.ArgumentParser(description='ZZU疫情填报小助手 ')
    args.add_argument("-n",
                      '--no-email',
                      help=u"不发送邮件",
                      default=False,
                      action='store_true')
    args.add_argument('-l',
                      "--log-no-file",
                      help='不输出日志到文件',
                      default=False,
                      action='store_true')
    args.add_argument("-c",
                      "--check-only",
                      help="仅进行检查，不进行填报",
                      default=False,
                      action='store_true')
    args = args.parse_args()
    config = Configuration()
    argDict = vars(args)
    config.addProperty('args', argDict)
    if (config.getProperty("args.no_email") is True):
        logger.info("命令行参数: 不发送邮件")
    if (config.getProperty("args.log_no_file") is True):
        logger.info("命令行参数: 不输出日志到文件")
    if (config.getProperty("args.check_only") is True):
        logger.info("命令行参数: 仅进行检查，不进行填报")


def disableSSLWarning():
    config = Configuration()
    if (not config.getProperty("crawler.verify")):
        urllib3.disable_warnings()


def getRetryTimes():
    config = Configuration()
    return config.getProperty("retry.times")


@retry(stop=stop_after_attempt(getRetryTimes()))
@logger.catch
def main():
    banner = Banner()
    banner.printBanner()
    logger.success("Start main process")
    parseArgs()
    MyLogger.startLogging()
    disableSSLWarning()
    run()


if (__name__ == "__main__"):
    try:
        main()
    except Exception:
        message = traceback.format_exc()
        emailController = EmailController()
        emailController.send(title="未知异常", html=message)
        logger.exception("未知异常")
