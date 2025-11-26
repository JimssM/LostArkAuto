#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import time
import fastdeploy as fd
import cv2
from Application.tools import *
from Application.public import *
import threading

current_path = os.path.dirname(__file__)


class YOLO:
    def __init__(self, path, size=(640, 640)):
        self.path = path
        print("path:", path)
        option = fd.RuntimeOption()
        option.use_cpu()
        # option.use_gpu()
        # option.use_trt_backend()

        # 载入模型
        yolov8 = fd.vision.detection.YOLOv8(path, runtime_option=option)
        yolov8.preprocessor.size = list(size)
        self.yolo: fd.vision.detection.YOLOv8 = yolov8

    def img_predict(self, img):
        """
        :param img:
        :return: boxes,scores,label_ids
        """
        image = cv2.imread(img)
        image_np = np.array(image)
        out = str(self.yolo.predict(image_np))
        # 处理数据为二维列表
        lines = out.split('\n')
        # 创建一个空的二维列表
        result = []
        # 遍历每一行字符串，跳过第一行
        for i, line in enumerate(lines):
            # 跳过第一行（索引为0的行）
            if i == 0:
                continue
            # 按逗号 , 分割当前行，得到列列表
            columns = line.split(',')
            # 将列列表添加到二维列表中
            result.append(columns)
        result.pop(-1)
        # print("yolo结果:",result)
        return result

    def screen_predict(self, label_id, score=0.8):
        """
        yolo对屏幕截屏推测
        DetectionResult: [xmin, ymin, xmax, ymax, score, label_id]
        :param label_id: 对应的模型标签id
        :param score:识别阈值
        :return:识别的位置，若未识别到则为[0, 0]
        """
        img = ImageGrab.grab()
        img.save(static_path + "model/y.jpg")
        pos = [0, 0]
        out = self.img_predict(static_path + "model/y.jpg")
        if out != []:
            if float(out[0][4]) >= score and int(out[0][5]) == label_id:
                pos = [int((float(out[0][0]) + float(out[0][2])) / 2), int((float(out[0][1]) + float(out[0][3])) / 2)]
        return pos

    def screen_predict_raw(self, label_id, score=0.8):
        """
        yolo对屏幕截屏推测并返回原始坐标数据
        DetectionResult: [xmin, ymin, xmax, ymax, score, label_id]
        :param label_id: 对应的模型标签id
        :param score:识别阈值
        :return:识别的位置，x1, y1, x2, y2, 怪物数量count
        """
        img = ImageGrab.grab()
        img.save(static_path + "model/y.jpg")
        out = self.img_predict(static_path + "model/y.jpg")
        if out != []:
            if float(out[0][4]) >= score and int(out[0][5]) == label_id:
                return [float(out[0][0]), float(out[0][1]), float(out[0][2]), float(out[0][3]), len(out)]
        return [0, 0, 0, 0, 0]


yo_gate_core = YOLO(path=static_path + "model/1.onnx")
yo_monster_spirit = YOLO(path=static_path + "model/2.onnx")
