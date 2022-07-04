# -*- coding: utf-8 -*-
# @Time    : 2021/03/30 20:34:23
# @Author  : DannyDong
# @File    : Run.py
# @Describe: 小程序自动化测试-执行入口

import pytest


if __name__ == '__main__':
    pytest.main(['-s', '-m Test01_获取微信信息', '--device=AndroidMaster1', '--wx=1'])
