# -*- coding: utf-8 -*-
# @Time    : 2022/07/04 15:27:54
# @Author  : DannyDong
# @File    : Demo.py
# @Describe: Demo 

import pytest

from Utils.Log import MintBlueLogger


@pytest.mark.Test01_获取微信信息
class TestGetWeChatElement:
    
    def test_01(self, get_wechat_element):
        """ 查看微信「我」元素 """
        wording = get_wechat_element.get_wechat_my_elements()
        assert wording == '服务'
        MintBlueLogger.info('查看微信「我」元素测试用例 - 通过')


if __name__ == '__main__':
    pass
