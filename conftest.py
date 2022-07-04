# -*- coding: utf-8 -*-
# @Time    : 2021/04/18 21:16:36
# @Author  : DannyDong
# @File    : conftest.py
# @Describe: None

import pytest


# 动态添加命令行参数
def pytest_addoption(parser):
    parser.addoption("--device", action="store",
                     default="type1", help="my option: type1 or type2")
    parser.addoption("--wx", action="store", default="0",
                     help="my option: 0 or 1")
    parser.addoption("--deviceType", action="store", default="android",
                     help="android or ios")


# 获取DeviceInfo
@pytest.fixture(scope='session')
def device(request):
    return request.config.getoption("--device")

# 获取DeviceType
@pytest.fixture(scope='session')
def device_type(request):
    return request.config.getoption("--deviceType")


# 是否重启微信
@pytest.fixture(scope='session')
def is_wx(request):
    return request.config.getoption("--wx")

# 获取用例Mark
@pytest.fixture(scope='session')
def get_mark(request):
    return request.config.option.markexpr


# 动态注册Mark
def pytest_configure(config):
    config.addinivalue_line("markers", 'Test01_获取微信信息')
    


if __name__ == '__main__':
    pass
