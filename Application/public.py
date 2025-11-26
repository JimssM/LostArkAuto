#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import getpass
import os
import time

project_path = os.path.join(os.path.dirname(__file__), )  # 项目根目录
ocr_model_path = project_path + "\\Resources\\ocr\\"
static_path = project_path + "\\Resources\\static\\"
img_path = static_path + "img\\"
ui_path = static_path+"ui\\"


data_path = project_path + "\\data\\"

database_path = f"{static_path}/account_state.db"

log_dir = f"{data_path}/log"
log_path = f"{log_dir}/{time.strftime('%Y-%m-%d', time.localtime(time.time()))}.txt"
config_path = data_path + "config.ini"
# config_path_key = data_path +"卡密.ini"
config_path_key = os.path.join("C:\\Users", getpass.getuser(),"xgfz_token.ini")
account_path = f"{data_path}/account.txt"

# post_url = "http://192.168.0.101:12344"
post_url = "http://47.111.128.232:12344"
ntp_server = "ntp.tencent.com"
'''
游戏内数据
'''
# 改角色在主菜单排序的界面
six_char_pos_in_change_slot = [
    (361, 123),
    (620, 122),
    (861, 120),
    (1101, 126),
    (1352, 125),
    (1591, 122),
]
# 选择角色界面的角色坐标
six_char_pos = [(348, 922),
                (607, 919),
                (853, 926),
                (1081, 919),
                (1326, 919),
                (1579, 920)]

# 游戏内切换角色菜单栏的坐标
char_pos_ingame = [
    (703, 405),
    (961, 409),
    (1227, 403),
    (696, 528),
    (962, 522),
    (1226, 528),
    (697, 641),
    (965, 639),
    (1222, 643),
]

# 游戏内选中的角色，识别颜色坐标
char_select_color_pos_ingame = [
    [574, 374],
    [834, 374],
    [1095, 374],
    [574, 491],
    [834, 491],
    [1095,491],
    [574,608],
    [835,608],
    [1095,608],
]


