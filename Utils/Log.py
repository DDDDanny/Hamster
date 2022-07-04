# -*- coding: utf-8 -*-
# @Time    : 2019/8/21 23:18
# @Author  : DannyDong
# @File    : Log.py
# @describe: 生成日志信息

import logging
import logzero


# 日志生成器
class Logger:
    def __init__(self):
        # 定义MintBlueLogger
        self.MintBlueLogger = logging.getLogger("MintBlueLogger")
        log_format = '[MiniProgramLog]%(color)s[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d]%(end_color)s [pid:%(process)d] %(message)s'
        formatter = logzero.LogFormatter(fmt=log_format)
        # 设置控制台日志信息
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        # 设置级别日志级别,Logging中有NOTSET < DEBUG < INFO < WARNING < ERROR < CRITICAL这几种级别，日志会记录设置级别以上的日志
        console.setLevel(logging.DEBUG)
        self.MintBlueLogger.addHandler(console)

    def get_logger(self):
        return self.MintBlueLogger


# 单例
MintBlueLogger = Logger().get_logger()
MintBlueLogger.setLevel(logging.INFO)


if __name__ == '__main__':
    pass
