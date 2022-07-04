# -*- coding: utf-8 -*-
# @Time    : 2022/05/11 10:08:00
# @Author  : DannyDong
# @File    : OCRDiscern.py
# @Describe: OCR

import os
import ssl
import easyocr
from Utils.Log import MintBlueLogger

os.environ["CUDA_VISIBLE_DEVICES"] = "True"
os.environ["KMP_DUPLICATE_LIB_OK"] = "True"

ssl._create_default_https_context = ssl._create_unverified_context


class OCRDiscern:
    """
        通过OCR进行文字识别，获取相应坐标值
    """

    def __init__(self) -> None:
        self.image_path = './images/SourceImage.png'
        self.model = ['ch_sim']
        self.coordinate_set = self.__ocr_read_wording()
        MintBlueLogger.debug(self.coordinate_set)

    # 进行OCR识别
    def __ocr_read_wording(self):
        # 实例化读取器
        reader = easyocr.Reader(self.model)
        # 读取图像
        result = reader.readtext(self.image_path)
        MintBlueLogger.info(result)
        return result

    # 处理坐标数据
    def __handle_coordinate_data(self, coordinate_set, target_wording):
        search_res_coordinate = None
        MintBlueLogger.debug(coordinate_set)
        MintBlueLogger.debug(target_wording)
        for item in coordinate_set:
            if item[1] == target_wording:
                search_res_coordinate = item
                break
        if search_res_coordinate is None or search_res_coordinate[2] < 0.9:
            MintBlueLogger.warning(
                '没有搜索到元素「{0}」或元素「{0}」置信度过低'.format(target_wording))
            return False
        else:
            MintBlueLogger.info('识别到元素「{}」, 置信度为：{}'.format(
                search_res_coordinate[1], search_res_coordinate[2]))
            coordinates = search_res_coordinate[0]
            MintBlueLogger.info(coordinates)
            x_coordinate = coordinates[0][0] + \
                (coordinates[1][0] - coordinates[0][0]) / 2
            y_coordinate = coordinates[0][1] + \
                (coordinates[2][1] - coordinates[1][1]) / 2
            MintBlueLogger.info("X坐标：{}，Y坐标：{}".format(
                x_coordinate, y_coordinate))
            return x_coordinate, y_coordinate

    # 获取坐标信息
    def get_coordinate(self, target_wording):
        """get_coordinate 获取指定文字的坐标

        Args:
            target_wording (str): 目标文字

        Returns:
            tuple: x轴坐标 & y轴坐标
        """
        MintBlueLogger.info('开始进行OCR识别🔍')
        if isinstance(target_wording, str):
            return self.__handle_coordinate_data(self.coordinate_set, target_wording)
        elif isinstance(target_wording, list):
            coordinates = []
            for item in target_wording:
                res = self.__handle_coordinate_data(self.coordinate_set, item)
                coordinates.append(res)
            MintBlueLogger.info(coordinates)
            return coordinates
        else:
            raise Exception('目标信息类型错误，无法进行搜索！')


if __name__ == '__main__':
    OCRDiscern().get_coordinate(['哈哈哈哈哈哈', '确定'])
