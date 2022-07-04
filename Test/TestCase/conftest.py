# -*- coding: utf-8 -*-
# @Time    : 2021/04/18 21:05:29
# @Author  : DannyDong
# @File    : conftest.py
# @Describe: 业务注册中心

import pytest

from Test.Process.Demo import HandleWeChat


"""
业务注册中心
"""
@pytest.fixture(scope='session')
def get_wechat_element(launch, device_type):
    return HandleWeChat(launch, device_type)


if __name__ == '__main__':
    pass
