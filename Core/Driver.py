# -*- coding: utf-8 -*-
# @Time    : 2021/04/25 14:12:54
# @Author  : DannyDong
# @File    : Driver.py
# @Describe: 驱动引擎初始化

import subprocess

import wda
import uiautomator2 as u2

from Utils.ReadConfig import ReadIni


class InitDriver:
    def __init__(self) -> None:
        self.read_ini = ReadIni()
    
    # 启动装置（Android）
    def connect_device(self, device):
        # 获取设备ID
        device_id = self.read_ini.get_value(device)
        # 连接设备
        return u2.connect(device_id)
    
    # 启动装置（IOS）
    def connect_device_ios(self, device):
        # 获取设备信息
        device_info = eval(self.read_ini.get_value(device))
        # 强制启动wda-tidevice
        wda._start_wda_xctest(device_info['id'])
        # 连接设备
        return wda.USBClient(device_info['id'], port=device_info['port'])

    # 设备池
    def devices_pool(self):
        """ 设备池 """
        cmd = r'adb devices'
        res = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        res.wait()
        out = res.stdout.readlines()
        devices = list()
        for i in (out)[1:-1]:
            device = str(i).split("\\")[0].split("'")[-1]
            devices.append(device)
        return devices


if __name__ == '__main__':
    pass
