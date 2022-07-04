# -*- coding: utf-8 -*-
# @Time    : 2022/07/04 15:05:53
# @Author  : DannyDong
# @File    : Demo.py
# @Describe: Demo 

from Utils.Log import MintBlueLogger
from Test.Page.Demo import WeChatPage


class HandleWeChat:
    def __init__(self, launch, device_type):
        self.process = WeChatPage(launch, device_type)
    
    def get_wechat_my_elements(self):
        self.process.click_wx_home()
        MintBlueLogger.info('进入微信「我」页面')
        wording = self.process.get_wx_home_ele()
        MintBlueLogger.info('获取文字成功')
        return wording


if __name__ == '__main__':
    pass
