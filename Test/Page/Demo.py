# -*- coding: utf-8 -*-
# @Time    : 2022/07/04 14:52:11
# @Author  : DannyDong
# @File    : Demo.py
# @Describe: Demo-Page 


from Utils.CatchError import catcherr


class WeChatPage:
    def __init__(self, launch, device_type):
        self.element = launch
        self.dt = device_type
        self.config = {
            'fileName': __file__,
            'node': 'WeChat',
        }

    @catcherr
    def click_wx_home(self):
        """ 点击微信「我」 """
        self.element.app_click(self.config, 'MyButton')
        
    def get_wx_home_ele(self):
        """ 获取微信「我」页面元素 """
        return self.element.get_app_text(self.config, 'MyTitle')
    

if __name__ == '__main__':
    pass
