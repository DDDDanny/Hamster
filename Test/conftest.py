# -*- coding: utf-8 -*-
# @Time    : 2021/03/31 10:58:23
# @Author  : DannyDong
# @File    : conftest.py
# @Describe: 全局Conftest

import os
import time
import _thread

import pytest
from _pytest.runner import runtestprotocol

from Utils.Log import MintBlueLogger
from Utils.ReadConfig import ReadIni
from Core.Hamster import Hamster
from Core.HamsterIOS import HamsterIOS
from Core.Driver import InitDriver
from Utils.GlobalVal import GlobalVal
from Test.Process.Demo import HandleWeChat


# 全局Driver
driver = None


# 处理用例失败时自动截图
def pytest_runtest_protocol(item, nextitem):
    reports = runtestprotocol(item, nextitem=nextitem)
    # 获取当前目录的绝对路径
    cur_path = os.path.abspath(__file__)
    # 获取logs文件夹的绝对路径
    logs_path = os.path.join(os.path.abspath(
        os.path.dirname(cur_path) + os.path.sep + '../Report'), '')
    case_mark = item.instance.pytestmark[0].name
    for report in reports:
        if report.outcome != 'passed':
            if '::' in report.nodeid:
                file_name = report.nodeid.split(
                    '/')[-1].replace("::", "_") + ".png"
                # 特殊处理字符集
                file_name = file_name.encode('utf-8').decode('unicode_escape')
            else:
                file_name = report.nodeid + ".png"
            MintBlueLogger.info(file_name)
            folder = os.path.exists(logs_path + case_mark)
            # 判断是否存在文件夹如果不存在则创建为文件夹
            if not folder:
                os.makedirs(logs_path + case_mark)
            MintBlueLogger.info(os.path.join(logs_path + case_mark, file_name))
            driver.screenshot(os.path.join(logs_path + case_mark, file_name))
    return True


# Android启动处理
def handle_launch_android(device, is_wx):
    global driver
    driver = InitDriver().connect_device(device)
    # 解决元素定位偏移的问题
    driver.jsonrpc.setConfigurator({"waitForIdleTimeout": 500})
    MintBlueLogger.info('初始化「Driver」成功')
    # 实例化Hamster
    hamster = Hamster(driver)
    MintBlueLogger.info('实例化「Hamster」成功')
    # 判断设备是否为屏幕状态
    if not hamster.get_device_info['screenOn']:
        hamster.light_screen()
        MintBlueLogger.info('点亮屏幕成功')
    time.sleep(2)
    # 判断设备是否为锁屏状态
    if hamster.is_screen_lock:
        hamster.screen_unlock()
        MintBlueLogger.info('解锁屏幕成功')
    # 根据uiautomator运行状态判断是否启动
    if not driver.uiautomator.running():
        # 启动uiautomator服务
        driver.uiautomator.start()
        MintBlueLogger.info('「uiautomator」服务正在启动......')
        time.sleep(10)
    if is_wx == '1':
        MintBlueLogger.info('正在启动微信......')
        # 读配置文件，获取AppPackage信息
        package_info = ReadIni(node='App')
        app_package = package_info.get_value('AppPackage')
        app_activity = package_info.get_value('AppActivity')
        MintBlueLogger.info('App Package: 「{}」'.format(app_package))
        MintBlueLogger.info('App Activity: 「{}」'.format(app_activity))
        # 打开WeChat，session的用途是操作的同时监控应用是否闪退，当闪退时操作，会抛出SessionBrokenError
        driver.app_start(package_name=app_package,
                         activity=app_activity, stop=True, use_monkey=True)
        # 判断微信是否开启
        timer = 0
        while timer <= 20:
            if driver(text='发现').exists():
                break
            else:
                timer += 1
        MintBlueLogger.info('微信启动成功，准备进入小程序......')
    return hamster


# IOS启动处理
def handle_launch_ios(device, is_wx):
    global driver
    driver = InitDriver().connect_device_ios(device)
    MintBlueLogger.info('初始化「Driver」成功')
    hamster = HamsterIOS(driver, device)
    MintBlueLogger.info('实例化「HamsterIOS」成功')
    # 读配置文件，获取AppPackage信息
    package_info = ReadIni(node='App')
    bundle_id = package_info.get_value('BundleID')
    # 执行前做一次健康检查，解决执行速度变慢的问题
    driver.healthcheck()
    driver.app_start(bundle_id)
    if is_wx == '1':
        driver.app_stop(bundle_id)
        driver.app_start(bundle_id)
        MintBlueLogger.info('打开微信App')
        time.sleep(10)
    return hamster


# 异常监听函数
def exception_watcher(threadName, timer, hamster, device_type):
    # 实例化
    hb = HandleWeChat(hamster, device_type)
    while 1:
        if GlobalVal.exception_flag is False:
            MintBlueLogger.info('Owl开始进行异常处理'.format(threadName))
            # 处理异常
            hb.handle_exception()
            GlobalVal.exception_flag = True
            MintBlueLogger.info('异常处理完成，可以继续执行用例'.format(threadName))
        else:
            MintBlueLogger.info('Owl正在进行异常监听，目前用例执行正常'.format(threadName))
        time.sleep(timer)


# 设备连接及启动器
@pytest.fixture(scope='session', autouse=True)
def launch(is_wx, device, env, get_mark, device_type, record_testsuite_property):
    if device_type == 'android':
        MintBlueLogger.info('开始启动Android，准备发射...')
        hamster = handle_launch_android(device, is_wx)
    elif device_type == 'ios':
        # IOS端启动前，需要等待蓄能
        timer = 15
        while timer >= 0:
            time.sleep(1)
            MintBlueLogger.info('设备正在积蓄能量，还剩「{}」秒完成，请耐心等待……'.format(timer))
            timer -= 1
        MintBlueLogger.info('开始启动IOS，准备发射...')
        hamster = handle_launch_ios(device, is_wx)
    else:
        raise Exception('Device Type Error!')
    # 开启自动化测试输入法
    driver.set_fastinput_ime(True)
    MintBlueLogger.info('「FastInput」输入法开启成功！')
    # 新增XML参数
    record_testsuite_property("Env", env)
    # 开启守卫
    _thread.start_new_thread(
        exception_watcher, ("Owl", 3, hamster, device_type))
    yield hamster


# 设置pytest执行结果说明
def pytest_itemcollected(item):
    if '[' not in item.name:
        par = item.parent.obj
        node = item.obj
        pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
        suf = node.__doc__.strip() if node.__doc__ else node.__name__
        if pref or suf:
            item._nodeid = ' '.join((pref, suf))
    else:
        pass


if __name__ == '__main__':
    pass
