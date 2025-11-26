#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time

from Application.public import img_path
from Application.tasks.yolo import yo_gate_core
from Application.tools import find_img_low_threshold
print("\n\n\n\n\n\n\n\n\n\n\n\n")
print("耗时越短，性能越好，推荐值：小于0.4")
t = time.time()
find_img_low_threshold(img_path + "died.png")
yo_gate_core.screen_predict(1)
print("测试耗时：",time.time()-t)
time.sleep(999)