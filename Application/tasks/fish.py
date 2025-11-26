#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import threading
import time

from Application.tasks.chaosDungeon import ChaosDungeon
from Application.tasks.chaosGate import ChaosGate
from Application.tasks.unit import go_to_repair
from Application.tools import *

from Application.tasks.pathFinder import *
from Application.tasks.game_action import *

current_path = os.path.dirname(__file__)


class Fish:
    def __init__(self):
        self.tool_img_path = ""
        self.tool_pos_list = []
        self.fish_cursor_pos = None
        self.fish_pos_list = None
        self.no_tools = False

    def fish(self):
        # switch_char_ingame(0)
        # go_to_city()
        # go_to_repair()
        # cd = ChaosDungeon()
        # cd.repair()

        if if_bigMapCoord_exist([1445, 303], [952, 555], [197, 109, 107]):
            # T4钓鱼
            board_ocean_liner((1259, 428))
            move_to_triport([1445, 303], [952, 555], [1309, 460])

            ride_mount()
            path = [462.0, 295.0], [443.0, 293.0], [419.0, 294.0], [388.0, 300.0], [363.0, 305.0], [351.0, 297.0], [
                333.0, 286.0], [321.0, 285.0], [309.0, 296.0], [302.0, 305.0], [293.0, 306.0],
            fish_finder_t4.node_finder(path)
            disMount()
            self.fish_pos_list = [[493, 731], [652, 895]]
        else:
            # T3钓鱼
            # return
            board_ocean_liner((892, 523))
            move_to_triport([886, 483], [823, 581], [1043, 740])

            path = [276.0, 195.0], [273.0, 202.0], [256.0, 206.0], [235.0, 224.0], [218.0, 230.0], [195.0, 226.0], [
                189.0, 241.0], [191.0, 254.0], [210.0, 254.0], [215.0, 262.0], [232.0, 280.0]
            fish_finder_t3.node_finder(path)

            self.fish_pos_list = [[1275, 353], [1416, 727]]

        # 获取cursor坐标
        self.fish_cursor_pos = random.choice(self.fish_pos_list)
        move_mouse(self.fish_cursor_pos)
        click_right_mouse_pynput(delay=5)

        self.get_all_tool_pos()
        # 开始钓鱼：循环钓鱼，并检测鱼竿耐久度、体力；体力耗尽下线
        self._change_to_b_ui()
        cg = ChaosGate() # 可能要参加混沌之门
        while not self.if_energy_runOut() and self.no_tools == False:
            if self.if_net_fishing():
                self.net_fishing()
            else:
                self._fish_once()
            self._change_to_b_ui()

            # 判断是不是要去参加混沌之门
            if cg.if_chaosgate() and gl_info.chaosGate:
                gl_info.chaosGate = False
                cg.main_loop()
                self.fish()

    def get_all_tool_pos(self):
        def merge_coordinates(list_1, list_2):
            # 合并两个列表
            combined_list = list_1 + list_2

            # 定义一个函数，用于判断两个点是否在10以内
            def is_within_threshold(point1, point2, threshold=10):
                return abs(point1[0] - point2[0]) <= threshold and abs(point1[1] - point2[1]) <= threshold

            # 用于存储合并后的结果
            merged_list = []

            for point in combined_list:
                # 检查当前点是否已经在合并后的列表中
                found = False
                for merged_point in merged_list:
                    if is_within_threshold(point, merged_point):
                        found = True
                        print("同一个工具，合并")
                        break
                # 如果当前点不在合并后的列表中，添加它
                if not found:
                    merged_list.append(point)

            return merged_list

        path_1 = img_path + "tool\\fish_tool_1.png"
        path_2 = img_path + "tool\\fish_tool_2.png"
        path_3 = img_path + "tool\\fish_tool_3.png"
        path_4 = img_path + "tool\\fish_tool_4.png"
        open_inventory()
        list_1 = find_all_img_low_threshold(path_1)
        list_2 = find_all_img_low_threshold(path_2)
        list_3 = find_all_img_low_threshold(path_3)
        list_4 = find_all_img_low_threshold(path_4)
        self.tool_pos_list = merge_coordinates(list_1, list_2)
        self.tool_pos_list = merge_coordinates(self.tool_pos_list, list_3)
        self.tool_pos_list = merge_coordinates(self.tool_pos_list, list_4)

        close_inventory()

    def net_fishing(self):
        t = time.time()
        while ppocr((59, 21, 96, 42)) != "Exit":
            if time.time() - t < 6:
                press_key('e')
            else:
                print("net fishing tool")
                self.change_tool()
                return

        # 获取完美区域
        offset_colors = [
            [[0, 60], [255, 220, 51]],
        ]
        t = time.time()
        while time.time() - t < 6:
            perfect_pos = match_points((508, 121, 509, 546), (255, 220, 51), (50, 50, 50), *offset_colors)
            if perfect_pos != [0, 0]:
                break

        print("perfect", perfect_pos)
        # 获取指针位置
        offset_colors = [
            [[4, -1], [189, 57, 42]],
            [[9, -2], [255, 230, 219]],
        ]
        start_time = time.time()
        last_cursor_pos = match_points((517, 123, 542, 542), (175, 29, 19), (30, 30, 30), *offset_colors)
        while time.time() - start_time < 7:
            det_time = time.time()  # 钓鱼的一次判断时间
            cursor_pos = match_points((517, 123, 542, 542), (175, 29, 19), (30, 30, 30), *offset_colors)
            print("cursor", cursor_pos)
            # # 判断是否失败，失败则退出重新进入
            # if last_cursor_pos[1] - 3 < cursor_pos[1] < last_cursor_pos[1] + 3 and cursor_pos != [0, 0]:
            #     print("位置重叠，开始判断是否失败")
            #     if cursor_pos[1] < 125 or cursor_pos[1] > 540:  # 掉到最下面或最上面
            #         print("钓鱼失败了")
            #         press_key('esc', delay=0.5)
            #         press_key('esc', delay=0.5)
            #         time.sleep(2)
            #         clear_interface()
            #         return
            #     elif time.time() - start_time > 5:  # 结束了，判断是不是完美收杆
            #         perfect_offset_color_1 = [
            #             # [[0, 22 + 10], [215, 80, 8]],
            #             [[20, 0], [177, 30, 20]],
            #             [[24, 0], [168, 16, 10]],
            #         ]
            #         perfect_offset_color_2 = [
            #             # [[0, 22 + 10], [215, 80, 8]],
            #             [[20, 0], [180, 35, 24]],
            #             [[24, 0], [168, 19, 13]],
            #         ]
            #         perfect_offset_color_3 = [
            #             # [[0, 22 + 10], [215, 80, 8]],
            #             [[20, 0], [188, 48, 37]],
            #             [[24, 0], [170, 29, 21]],
            #         ]
            #         # 没有在完美区域，base_color x坐标：505
            #         if not \
            #                 (match_points((503, 119, 535, 546), (252, 134, 8), (30, 30, 30),
            #                               *perfect_offset_color_1) != [0, 0]
            #                  or match_points((503, 119, 535, 546), (252, 134, 8), (30, 30, 30),
            #                                  *perfect_offset_color_2) != [0, 0]
            #                  or match_points((503, 119, 535, 546), (252, 134, 8), (30, 30, 30),
            #                                  *perfect_offset_color_3) != [0, 0]):
            #             print("不在完美区域")
            #             press_key('esc', delay=0.5)
            #             press_key('esc', delay=0.5)
            #             time.sleep(2)
            #             clear_interface()
            #             return

            delay = 0
            if cursor_pos[1] > perfect_pos[1] + 20:
                delay = 0.13
                print("50")
                if cursor_pos[1] > last_cursor_pos[1] or cursor_pos[1] > perfect_pos[1] + 40:
                    press_key_pynput(pynput_key_val.space, duration=0.05, delay=0)
                t_2 = time.time()
                if t_2 - det_time < delay:
                    print("等待时间", delay - (t_2 - det_time))
                    time.sleep(delay - (t_2 - det_time))
            # elif cursor_pos[1] > perfect_pos[1]:
            #     delay = 0.25
            #     print("40")
            #     press_key_pynput(pynput_key_val.space, duration=0.05, delay=0)
            #     t_2 = time.time()
            #     if t_2 - det_time < delay:
            #         print("等待时间", delay - (t_2 - det_time))
            #         time.sleep(delay - (t_2 - det_time))
            # elif cursor_pos[1] > perfect_pos[1] + 20:
            #     delay = 0.25
            #     print("40")
            #     press_key_pynput(pynput_key_val.space, duration=0.05, delay=0)
            #     t_2 = time.time()
            #     if t_2 - det_time < delay:
            #         print("等待时间", delay - (t_2 - det_time))
            #         time.sleep(delay - (t_2 - det_time))
            last_cursor_pos = cursor_pos

        time.sleep(7)

    def change_tool(self):
        if len(self.tool_pos_list) == 0:
            # self.no_tools = True
            return
        open_inventory()
        move_mouse(self.tool_pos_list[0])
        self.tool_pos_list.append(self.tool_pos_list[0])
        self.tool_pos_list.pop(0)
        click_right_mouse()
        close_inventory()

        move_mouse(self.fish_cursor_pos)

    def if_net_fishing(self):
        move_mouse(self.fish_cursor_pos)
        if match_point((802, 995), (162, 215, 225), (30, 30, 30)):
            return True
        return False

    def _change_to_b_ui(self):
        while ppocr((630, 1037, 642, 1049)) != "B":
            press_key('b', delay=1)
        time.sleep(2)

    # 获取体力值
    def if_energy_runOut(self):
        while not match_point((882, 922), (96, 184, 16)):  # 等待成就界面结束
            time.sleep(1)

        if match_point((896, 919), (53, 136, 74)):
            return False
        return True

    # 钓鱼一次
    def _fish_once(self):
        move_mouse(self.fish_cursor_pos)

        fish_mark_pos = (9, 17)
        fish_mark_rgb = (175, 161, 104)
        fish_mark_rect = (950, 461, 970, 506)
        fish_mark_cast = (30, 30, 30)
        # 帅干
        press_key('w')
        t = time.time()
        time.sleep(5)
        while not match_point(point=fish_mark_pos, color=fish_mark_rgb, region=fish_mark_rect,
                              tolerance=fish_mark_cast):
            if time.time() - t > 20:
                self.change_tool()
                return
        if time.time() - t < 18:
            time.sleep(0.3)
            press_key('w')
            time.sleep(5)
