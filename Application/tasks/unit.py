#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time

from Application.Control.configControl import Config
from Application.tasks.game_action import *
from Application.tasks.pathFinder import *


def go_to_repair():  # 去港口维修处
    go_to_city()
    move_to_triport([1063, 678], [1104, 460], [891, 526])
    finder = luterra_triport_finder
    wait_for_trans()
    clear_interface()
    ride_mount()
    repair_path = [267.0, 328.0], [256.0, 327.0], [247.0, 334.0], [252.0, 350.0], [259.0, 358.0], [266.0, 364.0], [
        271.0, 370.0], [277.0, 375.0], [291.0, 386.0], [303.0, 401.0], [319.0, 409.0], [338.0, 401.0], [352.0, 406.0],
    finder.node_finder(repair_path)
    leave_NPC_chat()


def go_to_mail():
    go_to_city()
    move_to_triport([1063, 678], [1104, 460], [891, 526])
    finder = luterra_triport_finder
    wait_for_trans()
    clear_interface()
    mail_path = [290.0, 309.0], [290.0, 299.0], [296.0, 291.0],
    finder.node_finder(mail_path)


def go_to_take_mail():
    go_to_mail()
    take_mail()


def go_to_mail_material():
    go_to_mail()
    clear_interface()
    refresh_inventory()
    mail_material()


def only_enter_game_mode():
    gl_info.thread_main.execution_time = -999999
    with pynput.keyboard.Listener(
            on_press=lambda key: False if key == pynput.keyboard.Key.end else True) as listener:
        listener.join()


def take_bus_mode():
    gl_info.thread_main.execution_time = -999999

    def listen(key):
        if key == pynput.keyboard.Key.end:
            return False  # 返回 False 终止监听
        return True

    # 创建 Listener 对象，设置回调函数
    listener = pynput.keyboard.Listener(on_press=listen)

    # 启动监听器
    listener.start()
    while listener.is_alive():
        if rect_match_sqdiff(rect=(594, 229, 1301, 910),
                             big_img_path=img_path + "OK_mark.png"):
            click_OK()
            move_mouse(0, 0)
        if rect_match_sqdiff(rect=(1564, 830, 1920, 1080),
                             big_img_path=img_path + "esc_mark.png",
                             threshold=0.02):
            click(960, 540)
            press_key('esc', delay=0.2)
        close_gamemenu_ui()
        time.sleep(1)


def home_main():
    # 检测家园是否存在：
    if not if_have_home():
        print("没有家园")
        return False

    settings = Config(config_path)
    song_home_simple()
    time.sleep(10)
    wait_for_trans()

    clear_interface()
    get_mission_reward()
    while not ppocr((942, 123, 979, 145)) == "Exit":
        combine_keys('ctrl', '1')
        time.sleep(2)
    if int(settings.get_value("全局配置", "魔方派遣")) and gl_info.home_cube:
        home_cube_guardian(0)
    if int(settings.get_value("全局配置", "加迪恩派遣")) and gl_info.home_guardian:
        home_cube_guardian(1)
    if int(settings.get_value("全局配置", "家园种植")) and gl_info.home_farm:
        gl_info.home_farm = False
        home_farm()
    clear_interface()
    song_leave_simple()
    time.sleep(10)
    wait_for_trans()


def get_mission_reward():
    while not ppocr((942, 123, 979, 145)) == "Exit":
        combine_keys('ctrl', '1')
        time.sleep(2)
    click(855, 62, delay=4)
    clear_interface()
    while not ppocr((942, 123, 979, 145)) == "Exit":
        combine_keys('ctrl', '1')
        time.sleep(2)
    click(855, 62, delay=4)
    click(676, 195, delay=4)
    clear_interface()


def home_cube_guardian(target=0):
    '''

    :param target: 0为cube，1为guardian
    :return:
    '''
    while gl_info.home_task_count < 2:
        mission_OK_img_path = img_path + "home/mission_OK.png"  # 任务完成标志
        while ppocr((218, 174, 334, 218), det=True) != "Station":  # 打开station
            click(855, 62, delay=4)
            if if_image_exists(mission_OK_img_path):  # 任务弹窗
                press_key("esc")
        while not match_point((673, 201), (241, 243, 195)):  # 打开派遣界面
            click(676, 195, delay=4)
            if if_image_exists(mission_OK_img_path):  # 任务弹窗
                press_key("esc")
        # 点开魔方任务
        while ppocr((379, 488, 419, 504)) != "Cube":
            click(471, 352, delay=3)
        while ppocr((379, 488, 419, 504)) == "Cube":
            if target == 0:
                click(417, 493, delay=3)
            else:
                click(410, 468, delay=3)
        # 领奖励
        if match_point((958, 340), (37, 37, 37)):  # 没有奖励
            pass
        else:
            click(982, 349, delay=3)
            click(982, 349, delay=3)
            click(962, 886, delay=3)
            click(962, 886, delay=3)
            click(957, 727, delay=3)
            click(957, 727, delay=3)
            click(1655, 866, delay=3)
        # 点击列表
        task_click_list = [
            [460, 462],
            [480, 525],
            [447, 607],
            [457, 675],
            [447, 747],
            [469, 814],
        ]
        for pos in task_click_list:  # 判断哪个可以做
            click(pos, delay=3)
            # 修船
            if ppocr((1817, 424, 1866, 442)) == "Repair":
                while ppocr((873, 417, 914, 436)) != "Ships":  # 打开修理界面
                    click(1841, 396, delay=3)
                # while not match_point((1105, 428), (238, 199, 49)):#点击全部修理
                #     click(1105, 428, delay=3)
                # 点击维修
                click(960, 734, delay=3)
                # 点击关闭
                click(1118, 328, delay=3)
            if match_point((1717, 892), (137, 104, 20)):
                break
            if pos == task_click_list[-1]:  # 都没有就不做
                return
        # 开始任务
        click(1586, 651, delay=3)
        click(1779, 893, delay=3)
        click_OK()
        gl_info.home_task_count += 1
        if gl_info.home_task_count >= 2:
            gl_info.home_cube = False
            gl_info.home_guardian = False


def home_farm():
    while ppocr((761, 287, 819, 307)) != "Settings":
        click(1066, 65, delay=3)
    # # 修工具
    # click(1291, 924, delay=3)
    # click(1291, 924, delay=3)
    # click(729, 819, delay=3)
    # click(729, 819, delay=3)
    # click_OK()
    # click(1344, 270, delay=3)
    # click(1344, 270, delay=3)

    # 收集
    click(870, 914, delay=3)
    click(870, 914, delay=3)
    click_OK()
    time.sleep(4)
    click(959, 720, delay=3)


def get_cube_ticket():
    go_to_city()
    # move_to_triport([1061,688],[930,611],[850,335])
    # path = [245.0, 165.0] ,[231.0, 186.0] ,[208.0, 203.0] ,[185.0, 206.0] ,[173.0, 199.0] ,
    # cube_ticket_finder_1.node_finder(path)
    # time.sleep(2)
    # move_mouse(692,218)
    # click_right_mouse_pynput(delay=8)
    # path = [308.0, 236.0] ,[280.0, 235.0] ,[251.0, 259.0] ,[230.0, 279.0] ,[223.0, 296.0] ,[238.0, 306.0] ,
    # cube_ticket_finder_2.node_finder(path)
    # chat_with_NPC()

    # #点第三栏
    # click(689,185,delay=3)
    # #换票
    # click(1002,545,delay=3)
    # click(684,673,delay=3)
    # time.sleep(1)
    # click(998,631,delay=3)
    # click(684,673,delay=3)
    # time.sleep(1)
    # click(1001,725,delay=3)
    # click(684,673,delay=3)
    # time.sleep(1)
    #
    # leave_NPC_chat()

    # 2024 10 10
    clear_interface()
    click(1824, 1044)
    click(1789, 955, delay=4)
    click(1248, 184, delay=3)
    click(722, 283, delay=3)
    click(714, 371, delay=3)
    click(1150, 227, delay=3)
    click(1628, 364, delay=3)
    click_OK(delay=3)
    click(1624, 452, delay=3)
    click_OK(delay=3)
    clear_interface()


def sign_in_union():
    clear_interface()
    click(1824, 1044)
    click(1789, 955, delay=4)
    setting = Config(config_path)
    if int(setting.get_value("全局配置", "工会银币捐献")):
        click(702, 184, delay=3)
        click(1620, 287, delay=3)
        click(687, 544, delay=3)
    clear_interface()

# def do_chaosGate():
#     """
#     每次开启任务前，判断是不是要混沌之门
#     :return:
#     """
#     settings = Config(config_path)
#     if int(settings.get_value("全局配置", "混沌之门")):
#         cg = ChaosGate()
#         if cg.if_chaosgate() and gl_info.chaosGate:
#             gl_info.chaosGate = False
#             cg.main_loop()

# def exchange_eventShop_reward():
#
# def
