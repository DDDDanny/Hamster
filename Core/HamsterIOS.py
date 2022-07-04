# -*- coding: utf-8 -*-
# @Time    : 2021/10/27 14:57:31
# @Author  : DannyDong
# @File    : HamsterIOS.py
# @Describe: Core Hamster For IOS

import time

from Utils.Log import MintBlueLogger
from Core.Driver import InitDriver
from Utils.EleAnalysis import EleAnalysis


class HamsterIOS:
    """ Operate Croe 以 Hamster（仓鼠🐹）命名

    HamsterIOS作为IOS端核心操作类，负责获取元素、操作元素以及操作设备

    Public Attributes:
        - driver: 该属性为操作元素以及设备的驱动器
        - device: 设备ID

    Public Functions:
        - get_element: 该方法为获取元素方法
        - get_screen_size: 该方法为获取手机屏幕大小方法
        - app_click: 该方法为元素点击事件
        - app_input: 该方法为元素输入事件
        - get_app_text: 该方法为获取元素文本信息
        - get_device_info: 该方法为获取设备信息
        - light_screen: 该方法为点亮屏幕
        - is_screen_lock: 该方法为判读是否锁屏
        - screen_unlock: 该方法为屏幕解锁
    """

    def __init__(self, driver, device) -> None:
        """__init__ 构造函数

        Args:
            driver (object): 设备驱动对象，用于之后所有的操作
            device (str): 设备ID，用于重起wda
        """
        self.driver = driver
        self.device = device
        self.connet_ios = InitDriver()

    def get_element(self, location, key, wait_time=30):
        """get_element 获取元素对象

        支持定位参数：
            text, textMatches, id, className，name, label, value, enabled, visible, xpath

        Args:
            location ([dict, str, list]): 用于确定定位方式
            key ([str, list]): 定位关键字
            wait_time (int): 轮询持续时间, 默认30s

        Return:
            若元素存在，返回元素对象; 若元素不存在，返回False;
        """
        if isinstance(location, dict):
            element = EleAnalysis(location['fileName'], location['node'])
            target = element.get_parameter(key)
        elif isinstance(location, str):
            target = {location: key}
        elif isinstance(location, list) and isinstance(key, list):
            target = {}
            for i in range(location.__len__()):
                target[location[i]] = key[i]
        elif location == None or key == None:
            return False
        else:
            raise Exception('location or key 参数错误')
        # 新增计时器，轮询查找元素是否存在
        timer = 0
        while timer <= wait_time:
            try:
                exists_res = self.driver(**target)
                if exists_res.exists:
                    return self.driver(**target)
                else:
                    timer += 1
            except ConnectionError:
                MintBlueLogger.info('出现链接异常，重新连接IOS设备')
                # 由于WDA会意外链接错误
                self.driver = self.connet_ios.connect_device_ios(self.device)
                time.sleep(5)
        return False

    # 单击操作
    def app_click(self, location, key, opt=None) -> None:
        # 单击事件时，获取元素并进行延时调整处理
        if opt is not None and 'wait' in opt.keys():
            element = self.get_element(location, key, opt['wait'])
        else:
            element = self.get_element(location, key)
        if opt is not None and 'position' in opt.keys():
            self.driver.click(opt['position'][0], opt['position'][1])
        else:
            element.click()

    # 输入事件
    def app_input(self, location, key, content, opt=None) -> None:
        self.app_click(location, key, opt)
        self.get_element(location, key).clear_text()
        # IOS端必须一个一个字输入
        for word in content:
            self.get_element(location, key).set_text(word)

    # 表单项输入
    def form_item_input(self, location, key, content, opt):
        # 获取表单想的Y轴坐标
        y_point = self.get_element('text', opt['fieldName']).get().bounds.y
        # 获取所有的输入框
        field_elements = self.get_element(location, key).find_elements()
        target_element = None
        # 找到表单项对应的输入框
        for field_element in field_elements:
            if field_element.bounds.y == y_point:
                target_element = field_element
                break
        # 判断是否找到元素
        if target_element is None:
            raise Exception('未找到元素')
        # 清除文本
        target_element.clear_text()
        # 输入文本信息
        for word in content:
            target_element.set_text(word)

    # 表单项选择
    def form_item_selector(self, location, key, opt):
        # 获取表单想的Y轴坐标
        y_point = self.get_element(
            'text', opt['fieldName']).find_elements()[-1].bounds.y
        # 获取所有的输入框
        field_elements = self.get_element(location, key).find_elements()
        target_element = None
        # 找到表单项对应的输入框
        for field_element in field_elements:
            if field_element.bounds.y == y_point:
                target_element = field_element
                break
        # 判断是否找到元素
        if target_element is None:
            raise Exception('未找到元素')
        target_element.click()

    # 获取文本信息
    def get_app_text(self, location, key, opt=None) -> str:
        if opt is not None and 'wait' in opt.keys():
            return self.get_element(location, key, opt['wait']).text
        return self.get_element(location, key).text

    # 滚动屏幕
    def swipe_screen(self, start_x, start_y, end_x, end_y) -> None:
        self.driver.swipe(start_x, start_y, end_x, end_y)

    # 拖动元素
    def element_drag(self, location, key, direction, opt=None) -> None:
        if 'wait' in opt.keys():
            target_element = self.get_element(location, key, opt['wait'])
        else:
            target_element = self.get_element(location, key)
        target_element.find_elements()[0].scroll(direction, 0.5)

    # 获取设备信息
    @property
    def get_device_info(self):
        return self.driver.info


if __name__ == '__main__':
    pass
