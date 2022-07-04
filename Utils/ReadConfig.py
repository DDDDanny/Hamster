# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 17:32
# @Author  : DannyDong
# @File    : ReadConfig.py
# @describe: 读取配置文件

import os
import configparser


class ReadIni:
    # 构造函数
    def __init__(self, file_name=None, node=None):
        # 获取当前目录的绝对路径
        cur_path = os.path.abspath(__file__)
        # 获取config.ini的绝对路径
        config_path = os.path.join(os.path.abspath(os.path.dirname(cur_path) + os.path.sep + '../Config'), 'SysConfig.ini')
        if file_name is None:
            file_name = config_path
        if node is None:
            self.node = 'Device'
        else:
            self.node = node
        self.conf = self.load_ini(file_name)

    # 加载文件
    @staticmethod
    def load_ini(file_name):
        conf = configparser.ConfigParser()
        conf.read(file_name, encoding='UTF-8')
        return conf

    # 获取Value值
    def get_value(self, key):
        data = self.conf.get(self.node, key)
        return data


if __name__ == '__main__':
    read = ReadIni(node='HTTP')
    print(read.get_value('base_url'))
