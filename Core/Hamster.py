# -*- coding: utf-8 -*-
# @Time    : 2021/03/30 20:55:29
# @Author  : DannyDong
# @File    : Hamster.py
# @Describe: Core Hamster

import os
import re
import time

from Utils.Log import MintBlueLogger
from Utils.GlobalVal import GlobalVal
from Utils.OCRDiscern import OCRDiscern
from Utils.EleAnalysis import EleAnalysis
from Utils.ImageDiscern import ImageDiscern


class Hamster:
    """ Operate Croe 以 Hamster（仓鼠🐹）命名

    Hamster作为核心操作类，负责获取元素、操作元素以及操作设备

    Public Attributes:
        - driver: 该属性为操作元素以及设备的驱动器

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

    def __init__(self, driver):
        """ 构造函数

        实例化类时，进行调用

        Parameters:
            - driver: Driver的实例化对象

        Return:
            None
        """
        # 获取 Driver
        self.driver = driver
        # 控件查找默认等待时间(默认5s)
        self.driver.settings['wait_timeout'] = 5
        # 配置点击前延时0.5s，点击后延时1s
        self.driver.settings['operation_delay'] = (.5, .5)

    # 获取元素
    def get_element(self, location, key, wait_time=30):
        """
        target支持参数：
            text，textContains，textMatches，textStartsWithclassName， classNameMatchesdescription，descriptionContains，
            descriptionMatches，descriptionStartsWithcheckable，checked，clickable，longClickablescrollable，enabled，
            focusable，focused，selectedpackageName， packageNameMatchesresourceId， resourceIdMatchesindex， instance
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
        else:
            raise Exception('location or key 参数错误')
        # 新增计时器，轮询查找元素是否存在
        timer = 0
        while timer <= wait_time:
            # 获取UI结构
            _ui = self.driver.dump_hierarchy(compressed=True)
            MintBlueLogger.debug(_ui)
            if 'xpth' in target.keys():
                exists_res = self.driver.xpath(target['xpth']).wait(timeout=1)
                if exists_res:
                    return self.driver.xpath(target['xpth'])
            else:
                exists_res = self.driver(**target).wait(timeout=1)
                if exists_res:
                    return self.driver(**target)
            timer += 1
            if timer == 20:
                GlobalVal.exception_flag = False
                MintBlueLogger.info('长时间未定位到元素，进入异常处理逻辑')
                except_timer = 0
                while GlobalVal.exception_flag is False:
                    MintBlueLogger.info('Hamster正在等待异常处理结果...')
                    time.sleep(2)
                    except_timer += 2
                    if except_timer > 60:
                        MintBlueLogger.info(_ui)
                        break
        return False

    # 点击事件
    def app_click(self, location, key, opt=None):
        # 单击事件时，获取元素并进行延时调整处理
        if opt is None or 'wait' not in opt.keys():
            element = self.get_element(location, key)
        else:
            element = self.get_element(location, key, opt['wait'])
        # 单击事件处理
        if opt is None:
            element.click()
        else:
            if 'offset' in opt.keys():
                element.click(offset=opt['offset'])
            elif 'position' in opt.keys():
                ele_pos = element.center()
                x_point, y_point = ele_pos[0] + \
                    opt['position'][0], ele_pos[1] + opt['position'][1]
                self.driver.click(x_point, y_point)
            else:
                raise Exception('opt参数错误')

    # 输入事件
    def app_input(self, location, key, content, opt=None):
        self.app_click(location, key, opt)
        self.driver.clear_text()
        self.driver.send_keys(content)

    # 获取文本信息
    def get_app_text(self, location, key) -> str:
        return self.get_element(location, key).get_text()

    # 滑动屏幕
    def swipe_screen(self, start_x, start_y, end_x, end_y):
        size = self.get_screen_size()
        time.sleep(2)
        self.driver.swipe(size[0] * start_x, size[1] *
                          start_y, size[0] * end_x, size[1] * end_y)

    # 拖动元素
    def element_drag(self, location, key, direction, steps=20):
        self.get_element(location, key).swipe(direction, steps)

    # 重启U2
    def restart_u2(self):
        MintBlueLogger.info('关闭「uiautomator」')
        self.driver.uiautomator.stop()
        time.sleep(1)
        MintBlueLogger.info('uiautomator process status: {}'.format(
            self.driver.uiautomator.running()))
        MintBlueLogger.info('开启「uiautomator」')
        self.driver.uiautomator.start()
        time.sleep(1)
        MintBlueLogger.info('uiautomator process status: {}'.format(
            self.driver.uiautomator.running()))
        MintBlueLogger.info('uiautomator starting...... ')
        time.sleep(10)

    # 获取屏幕宽&高
    def get_screen_size(self) -> tuple:
        return self.driver.window_size()

    # 获取设备信息
    @property
    def get_device_info(self):
        return self.driver.info

    # 点亮屏幕
    def light_screen(self):
        self.driver.shell('input keyevent 26')

    # 判断是否锁屏
    @property
    def is_screen_lock(self):
        lock_screen_re = re.compile(
            '(?:mShowingLockscreen|isStatusBarKeyguard|showing)=(true|false)')
        res = lock_screen_re.search(
            self.driver.shell('dumpsys window policy')[0])
        if not res:
            raise Exception("Couldn't determine screen lock state")
        return (res.group(1) == 'true')

    # 屏幕解锁
    def screen_unlock(self):
        self.driver.shell('input swipe 300 800 300 50')

    # 判断图片元素是否存在
    def get_element_from_image(self, target_image, grade=0.8, gauss_num=111):
        self.driver.screenshot(os.path.join(os.path.join(
            os.path.abspath('./Images/'), 'SourceImage.png')))
        MintBlueLogger.info('完成屏幕截图')
        res = ImageDiscern(target_image, grade, gauss_num).get_coordinate()
        return True if isinstance(res, tuple) else False

    # 图片点击操作
    def app_click_image(self, target_image, grade=0.8, gauss_num=111):
        self.driver.screenshot(os.path.join(os.path.join(
            os.path.abspath('./Images/'), 'SourceImage.png')))
        MintBlueLogger.info('完成屏幕截图')
        res = ImageDiscern(target_image, grade, gauss_num).get_coordinate()
        if isinstance(res, tuple):
            self.driver.click(res[0], res[1])
        else:
            raise Exception('为识别到图片，无法进行点击')

    # 判断文字元素是否存在
    def get_element_from_ocr(self, target_wording):
        """get_element_from_ocr 判断文字元素是否存在
        Args:
            target_wording (str, list): 目标文字信息
        """
        MintBlueLogger.info('实例化OCR')
        self.driver.screenshot(os.path.join(os.path.join(
            os.path.abspath('./Images/'), 'SourceImage.png')))
        MintBlueLogger.info('完成屏幕截图')
        res = OCRDiscern().get_coordinate(target_wording)
        if isinstance(target_wording, str):
            return True if isinstance(res, tuple) else False
        elif isinstance(target_wording, list):
            return True if False not in res else False

    # 点击文字
    def app_click_from_ocr(self, target_wording: str):
        """app_click_from_ocr 判断文字元素是否存在
        Args:
            target_wording (str, list): 目标文字信息
        """
        MintBlueLogger.info('实例化OCR')
        self.driver.screenshot(os.path.join(os.path.join(
            os.path.abspath('./Images/'), 'SourceImage.png')))
        MintBlueLogger.info('完成屏幕截图')
        res = OCRDiscern().get_coordinate(target_wording)
        if isinstance(res, tuple):
            self.driver.click(res[0], res[1])
            return
        else:
            raise Exception('通过OCR未识别指定文字或置信度过低，无法进行点击操作！')


if __name__ == '__main__':
    pass
