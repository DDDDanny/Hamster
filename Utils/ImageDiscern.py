# -*- coding: utf-8 -*-
# @Time    : 2021/12/16 15:11:42
# @Author  : DannyDong
# @File    : ImageDiscern.py
# @Describe: 处理图片识别

import os
import cv2
import numpy as np

class ImageDiscern:
    def __init__(self, target_image, grade, gauss_num) -> None:
        """__init__ [处理图片识别]

        Args:
            target_image (str): 被识别的目标图片
            grade (float, optional): 分数. Defaults to 0.8.
            gauss_num (int, optional): 过滤值. Defaults to 111.
        """
        self.source_image = os.path.join(os.path.abspath('./Images'), 'SourceImage.png')
        self.target_image = os.path.join(os.path.abspath('./Images'), target_image)
        self.grade = grade
        self.gauss_num = gauss_num
    
    # 降噪处理（高斯滤波）
    def __coordinate(self, image):
        return cv2.GaussianBlur(image, (self.gauss_num, self.gauss_num), 0)
    
    # 获取坐标图片坐标
    def get_coordinate(self):
        # 这里不用imread，解决中文目录无法读取的问题
        screen = cv2.imdecode(np.fromfile(self.source_image, dtype=np.uint8), 1)
        target = cv2.imdecode(np.fromfile(self.target_image, dtype=np.uint8), 1)
        result = cv2.matchTemplate(self.__coordinate(screen), self.__coordinate(target), cv2.TM_CCOEFF_NORMED)
        min, max, min_loc, max_loc = cv2.minMaxLoc(result)
        if max <= self.grade:
            return False
        else:
            x = max_loc[0] + int(target.shape[1]/2)
            y = max_loc[1] + int(target.shape[0]/2)
            return (x, y)
        

if __name__ == '__main__':
    ImageDiscern('ConfirmImage.png', 0.8, 111).get_coordinate()
