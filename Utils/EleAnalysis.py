# -*- coding: utf-8 -*-
# @Time    : 2021/04/28 14:18:32
# @Author  : DannyDong
# @File    : EleAnalysis.py
# @Describe: 处理元素解析

import os

from Utils.ReadConfig import ReadIni


# 处理元素解析
class EleAnalysis:
    def __init__(self, file_name, node):
        self.file_name = file_name
        # 获取当前页面元素配置的绝对路径
        ele_path = os.path.join(os.path.dirname(os.path.abspath(file_name)), 'EleConfig.ini')
        # 实例化元素解析器
        self.element_analysis = ReadIni(file_name=ele_path, node=node)

    # 获取参数（解析过后的Value)
    def get_parameter(self, key_word):
        return eval(self.element_analysis.get_value(key_word))


if __name__ == '__main__':
    pass
