#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import math
import random
import time

from Application.tasks.yolo import *
from Application.tasks.unit import *


class ChaosDungeonMode:
    t3Mode = "T3"
    t4Mode = "T4"
    t3Consumed = 100  # T3消耗的体力
    t4Consumed = 100  # T4 消耗的体力


class ChaosDungeon:
    skill_state_pos_list = [
        (704, 983),
        (751, 984),
        (798, 983),
        (845, 984),
        (726, 1031),
        (773, 1031),
        (820, 1032),
        (867, 1031),
    ]
    potion_switch = False
    last_f1_time = time.time()

    def __init__(self):
        self.grab_center = (1742, 166)
        self.grab_rect = (1628, 61, 1852, 275)  # 小地图区域
        self.move_center = (960, 533)  # 脚底
        self.move_radius = 50
        setting = Config(config_path)

        # 不清除的属性
        self.times = 0  # T3地牢打的次数 已弃用
        self.level = 0  # T3地牢阶层
        self.mode = ChaosDungeonMode.t3Mode  # T3或T4
        self.loop = None  # T3 或 T4 战斗

        # 技能相关
        self.can_use_V = True
        self.skill_characters_list = "qwerasdf"
        self.recent_chars = []
        self.skill_count = 0
        self.use_skillZ = False
        self.skill_can_use_state = []
        # 技能速度
        self.key_speed = 1

        # 卡点
        self.dont_find_monser_list = 0
        self.core_coord_list = []
        self.core_dir = 0  # 1为右侧，0为左侧

        # 随即移动
        self.random_move_pos_list = []

        self.time_end = False

    def clear(self):
        times = self.times
        level = self.level
        mode = self.mode
        loop = self.loop
        self.__init__()
        self.times = times
        self.level = level
        self.mode = mode
        self.loop = loop

    def two_daily_chaosDungeon(self, get_chaosDungeon_level=False):
        adjust_transparency()
        self.close_quest_journal()
        print("两次地牢开始")
        go_to_repair()
        self.repair()
        # 进入副本前先下马
        clear_interface()
        disMount()
        self.get_weeklyTask_reward()
        self.get_weekly_task()

        # 战斗
        if_start = self.start_chaosDungeon(get_chaosDungeon_level, open_ui=True)
        if if_start == True:
            # 确定战斗tier
            if self.mode == ChaosDungeonMode.t3Mode:
                self.loop = self.tier3_loop
            else:
                # clear_interface()
                # return
                self.loop = self.tier4_loop

            self.loop()
            dismantle_inventory()

            self.leave_chaosDungeon()

        # 领取两次周长任务
        self.get_weeklyTask_reward()
        self.get_weeklyTask_reward()

    def tier4_loop(self):
        """
        试用新T4地牢
        :return:
        """
        NAVIGATE_MAX_TIME = 4  # 单次寻路的最大时长
        MAX_TIME = 240  # 4分钟最大时间移动至终点

        # 所有路径
        road_1 = [245.0, 523.0], [226.0, 508.0], [217.0, 495.0], [223.0, 478.0], [235.0, 470.0], [242.0, 459.0], [251.0,
                                                                                                                  452.0], [
            263.0, 442.0], [275.0, 426.0], [280.0, 408.0], [284.0, 394.0], [288.0, 380.0], [292.0, 368.0], [304.0,
                                                                                                            348.0], [
            319.0, 340.0], [336.0, 333.0], [351.0, 311.0], [412.0, 257.0], [427.0, 236.0], [441.0, 222.0], [454.0,
                                                                                                            209.0],
        # road_1 = [336.0, 333.0], [351.0, 311.0], [412.0, 257.0], [427.0, 236.0], [441.0, 222.0], [454.0, 209.0],
        road_2 = [463.0, 248.0], [458.0, 233.0], [454.0, 219.0], [451.0, 206.0], [443.0, 195.0], [428.0, 192.0], [413.0,
                                                                                                                  198.0], [
            399.0, 201.0], [388.0, 205.0], [371.0, 207.0], [356.0, 209.0], [337.0, 211.0], [318.0, 215.0], [305.0,
                                                                                                            216.0], [
            289.0, 219.0], [277.0, 226.0],

        road_3 = [411.0, 315.0], [398.0, 305.0], [383.0, 296.0], [365.0, 299.0], [348.0, 300.0], [335.0, 304.0], [323.0,
                                                                                                                  305.0], [
            310.0, 300.0], [293.0, 297.0], [277.0, 293.0], [270.0, 288.0], [261.0, 288.0], [249.0, 281.0], [234.0,
                                                                                                            273.0], [
            225.0, 264.0], [223.0, 243.0], [209.0, 229.0], [196.0, 214.0], [186.0, 205.0], [174.0, 192.0], [164.0,
                                                                                                            180.0], [
            163.0, 159.0], [173.0, 149.0], [181.0, 144.0],

        # 路径的列表
        road_list = [
            road_1,
            road_2,
            road_3,
        ]
        # 地图列表
        finder_list = [
            t4cd_1_finder,
            t4cd_2_finder,
            t4cd_3_finder,
        ]
        # 寻路偏差列表
        distance_to_target_list = [
            6,
            7,
            6,
        ]
        # 进入地图后识别小地图，确定对应路径和地图的序号
        self.get_skill_can_use_state()
        time.sleep(3)  # 等待加载
        road_index = 0  # 路径序号
        best_match = 0  # 最匹配的地图相似度
        index = 0
        for finder in finder_list:
            this_match = finder.if_this_map(threshold=finder.max_val) - finder.max_val
            if best_match < this_match:
                best_match = this_match
                road_index = index
            index += 1
        print("地图为", road_index)
        # 根据序号，边移动边打怪
        start_time = time.time()

        def get_used_time():
            return time.time() - start_time

        def if_move():
            """
            根据经过的时间比例和走过的路径比例判断是否需要移动，时间比例更大则移动
            :param coordinate_index: 进行到路径的序号
            :return:
            """
            print("if_move")
            if get_used_time() / MAX_TIME > coordinate_index / len(road_list[road_index]):
                return True
            return False

        coordinate_index = 0  # 路径内坐标序号
        no_obj_count = 0
        while True:
            # 复活
            resurrection()
            # 副本后期重置一次大招
            if get_used_time() > 240:
                self.can_use_V = True
            # 打怪
            pos = self.tier4_find_monster_in_screen()
            if pos:
                self.target_object(pos, radius=200)
                self.use_random_skill_quick(2, random_move_mouse=False)
            else:
                pos = self.tier4_find_spirit_in_screen()
                # 打精灵
                if pos:
                    self.target_object(pos, radius=300)
                    self.use_random_skill_quick(2, random_move_mouse=False)
                    click_right_mouse_pynput(delay=0.2)
                    pos = self.tier4_find_spirit_in_screen()
                    if pos:
                        self.target_object(pos, radius=50)
                        self.use_random_skill_quick(2, random_move_mouse=False)
                # 有boss
                elif self.find_boss_in_screen():
                    print("有boss")
                    self.use_random_skill_quick(2, random_move_mouse=True)
                # 什么都没有，移动
                else:
                    no_obj_count += 1
                    if no_obj_count < 2:
                        continue
                    no_obj_count = 0
                    # 移动
                    finder_list[road_index].trigger = True
                    if if_move():
                        # # 进行下一个坐标前，先移动到上一个坐标
                        # if coordinate_index > 0:
                        #     finder_list[road_index].navigate(
                        #         destination=road_list[road_index][coordinate_index - 1],
                        #         distance_to_target=distance_to_target_list[road_index],
                        #         max_time=NAVIGATE_MAX_TIME,
                        #         func=self.use_potion,
                        #     )
                        # # 0号图需要跳悬崖
                        # print(road_list[road_index][coordinate_index - 1])
                        # if road_index == 0 and \
                        #         (road_list[road_index][coordinate_index - 1] == [351.0, 311.0] or
                        #          road_list[road_index][coordinate_index] == [351.0, 311.0]):
                        #         # if_image_exists(img_path + "jump_to_battleField.png"):
                        #     release_right_mouse(delay=0)
                        #     print("jump_to_battleField")
                        #     time.sleep(1.5)
                        #     press_key('g', delay=0.5)
                        #     press_key('g', delay=5)
                        #     hold_right_mouse()
                        # 移动到下一个坐标，若成功还将坐标序号增加
                        if finder_list[road_index].navigate(
                                destination=road_list[road_index][coordinate_index],
                                distance_to_target=distance_to_target_list[road_index],
                                max_time=NAVIGATE_MAX_TIME,
                                random_move_time=NAVIGATE_MAX_TIME,
                                func=self.use_potion,
                        ) and \
                                coordinate_index < len(road_list[road_index]) - 1:
                            print("坐标增加成功")
                            coordinate_index += 1
                        # 0号图需要跳悬崖
                        print(road_list[road_index][coordinate_index - 1])
                        if road_index == 0 and \
                                road_list[road_index][coordinate_index - 1] == [351.0, 311.0]:
                            release_right_mouse(delay=0)
                            print("jump_to_battleField")
                            time.sleep(1.5)
                            if if_image_exists(img_path + "jump_to_battleField.png"):
                                press_key('g', delay=0.5)
                                press_key('g', delay=5)
                                # hold_right_mouse()
                            else:
                                coordinate_index -= 1
                    release_right_mouse(delay=0)
                    # 放技能
                    self.use_random_skill_quick(num=2, random_move_mouse=True)
            # 是否结束
            if self.if_finish():
                while self.if_finish():
                    click(949, 969)
                break
            # 是否超时
            if self.if_time_out():  # 超时
                print("超时")
                break

    def tier4_find_monster_in_screen(self):
        """
        返回屏幕T4怪兽坐标
        :return:
        """
        pos_raw = yo_monster_spirit.screen_predict_raw(label_id=0, score=0.25)
        if pos_raw != [0, 0, 0, 0, 0]:
            x1, y1, x2, y2, count = pos_raw
            if count <= 2:
                return 0
            pos = [0, 0]
            pos[0] = (x1 + x2) / 2
            pos[1] = y2 - (y2 - y1) * 0.2
            return pos
        return 0

    def tier4_find_spirit_in_screen(self):
        """
        返回屏幕T4精灵坐标
        :return:
        """
        pos_raw = yo_monster_spirit.screen_predict_raw(label_id=1, score=0.25)
        if pos_raw != [0, 0, 0, 0, 0]:
            x1, y1, x2, y2, count = pos_raw
            pos = [0, 0]
            pos[0] = (x1 + x2) / 2
            pos[1] = y2 - (y2 - y1) * 0.2
            return pos
        return 0

    def tier3_loop(self):
        """
        试用老T3地牢
        :return:
        """
        self.clear()
        self.times += 1
        while True:
            self.use_random_skill(self.key_speed)
            if self.find_core():
                print("找到核心")
                self.move_to_core()
            self.use_random_skill(self.key_speed)
            self.find_monster()  # 怪
            self.use_random_skill(self.key_speed)
            if self.find_core():
                print("找到核心")
                self.move_to_core()
            self.use_random_skill(self.key_speed)
            if self.find_gate() != [0, 0]:
                print("找到门")
                self.move_to_gate()  # 门
            self.use_random_skill(self.key_speed)
            if self.find_boss_in_screen():
                print("找到boss")
                self.find_boss_in_screen()  # boss
                self.find_boss_in_screen()  # boss
            self.use_random_skill(self.key_speed)
            if self.if_time_out():  # 超时
                print("超时")
                break
            self.use_random_skill(self.key_speed)
            self.find_monster()  # 怪
            self.use_random_skill(self.key_speed)
            if self.if_finish():
                while self.if_finish():
                    click(949, 969)
                break
        print("END")

    def if_finish(self):
        while ppocr((949, 949, 972, 967), det=False) == 'OK':
            return True
        return False

    def random_move_mouse(self, radius=50):  # 卡点时随机移动
        a = {'x': random.randint(10, 360), 'y': random.randint(10, 360)}
        b = {'x': random.randint(10, 360), 'y': random.randint(10, 360)}
        radian = math.atan2(b['y'] - a['y'], b['x'] - a['x'])
        coord = [0, 0]
        coord[0] = self.move_center[0] + radius * math.cos(radian)
        coord[1] = self.move_center[1] + radius * math.sin(radian)
        move_mouse(coord, delay=0)

    def random_move_twice(self, radius=150):
        a = {'x': random.randint(10, 360), 'y': random.randint(10, 360)}
        b = {'x': random.randint(10, 360), 'y': random.randint(10, 360)}
        radian = math.atan2(b['y'] - a['y'], b['x'] - a['x'])
        coord1 = [0, 0]
        coord2 = [0, 0]
        coord1[0] = self.move_center[0] + radius * math.cos(radian)
        coord1[1] = self.move_center[1] + radius * math.sin(radian)
        coord2[0] = self.move_center[0] - radius * math.cos(radian)
        coord2[1] = self.move_center[1] - radius * math.sin(radian)
        self.random_move_pos_list.append(coord1)
        self.random_move_pos_list.append(coord2)
        return coord1, coord2

    def use_potion(self, use_1=False):
        if match_point((812, 972), (18, 17, 18), tolerance=(50, 50, 50)):
            if ChaosDungeon.potion_switch:
                press_key('f1', delay=0)
            elif use_1:
                used_time = time.time() - ChaosDungeon.last_f1_time  # 吃下F1药的时间，需要大于
                press_key('1', delay=0)
                press_key('1', delay=0)
            ChaosDungeon.potion_switch = not ChaosDungeon.potion_switch

    def if_time_out(self):
        if ppocr((363, 70, 453, 101)) == "00:00":
            self.time_end = True
            time.sleep(2)
            return True
        return False

    # 复活
    def res(self):
        if if_die():
            # 判断用什么复活
            try:
                percentage = int(ppocr((103, 185, 163, 210), num_only=True, model="en", det=True))
            except:
                percentage = 70
            if percentage >= 60:
                resurrection(method=1)
            else:
                resurrection(method=0)

    def target_object(self, pos, radius=50):
        """
        移动鼠标瞄准目标
        :param pos: 目标坐标
        :param radius: 移动地点与角色中心距离的最大半径
        :return:
        """
        coord = pos
        if self.euclidean_distance(self.move_center, pos) < radius:
            # print(pos)
            move_mouse(pos)
            return
        radian = math.atan2(pos[1] - self.move_center[1], pos[0] - self.move_center[0])
        coord[0] = self.move_center[0] + radius * math.cos(radian)
        coord[1] = self.move_center[1] + radius * math.sin(radian)
        # print(coord)
        move_mouse(coord, delay=0)

    def use_random_skill(self, num=2, random_move=False, random_move_mouse=True):
        """
        释放随机技能
        :param num: 放技能次数
        :param random_move: 随机行走
        :param random_move_mouse: 随机移动鼠标
        :return:
        """
        if match_point((20, 1061), (0, 0, 0)):  # 黑屏自动跳过
            time.sleep(1)
            return
        setting = Config(config_path)
        for i in range(num):
            # 随机行动
            if random_move:
                if len(self.random_move_pos_list) == 0:
                    self.random_move_twice()
                move_mouse(self.random_move_pos_list[0], delay=1.2)
                click_right_mouse(delay=0.3)
                self.random_move_pos_list.pop(0)
            # 随机移动鼠标
            if random_move_mouse:
                self.random_move_mouse()

            self.use_potion()

            # 选择技能按键
            while True:
                random_character = random.choice(self.skill_characters_list)
                if random_character not in self.recent_chars:
                    break

            # 更新最近使用的技能按键
            self.recent_chars.append(random_character)
            if len(self.recent_chars) > 6:
                self.recent_chars.pop(0)

            # 放技能
            press_key(random_character, delay=0)
            press_key(random_character, delay=0)

            # 使用Z技能
            if self.use_skillZ:
                self.skill_count += 1
                if self.skill_count >= 30:
                    time.sleep(0.8)
                    press_key('z', delay=0)
                    self.skill_count = 0

    def get_skill_can_use_state(self):
        self.skill_can_use_state = []
        for i in range(len(ChaosDungeon.skill_state_pos_list)):
            self.skill_can_use_state.append(get_point_color(ChaosDungeon.skill_state_pos_list[i]))

    def use_random_skill_quick(self, num=2, random_move=False, random_move_mouse=False):
        """
        释放随机技能,并自动判断冷却
        :param num: 放技能次数
        :param random_move: 随机行走
        :param random_move_mouse: 随机移动鼠标
        :return:
        """
        if match_point((20, 1061), (0, 0, 0)):  # 黑屏自动跳过
            time.sleep(1)
            return
        for i in range(num):
            # 随机行动
            if random_move:
                if len(self.random_move_pos_list) == 0:
                    self.random_move_twice()
                move_mouse(self.random_move_pos_list[0], delay=1.2)
                click_right_mouse(delay=0.3)
                self.random_move_pos_list.pop(0)
            # 随机移动鼠标
            if random_move_mouse:
                self.random_move_mouse()

            self.use_potion()

            # 选择技能按键
            # random_character = None
            # for i in range(len(self.skill_can_use_state)):
            #     if match_point(ChaosDungeon.skill_state_pos_list[i], self.skill_can_use_state[i], tolerance=(0, 0, 0)):
            #         random_character = self.skill_characters_list[i]
            #         break

            # if random_character is None:
            for i in range(10):
                random_index = random.randint(0, len(self.skill_characters_list) - 1)
                if self.if_skill_available(random_index) or i == 9:
                    random_character = self.skill_characters_list[random_index]
                    break

            # 更新最近使用的技能按键
            self.recent_chars.append(random_character)
            if len(self.recent_chars) > 6:
                self.recent_chars.pop(0)

            # 放技能
            press_key(random_character, delay=0)
            press_key(random_character, delay=0)

            # 使用Z技能
            if self.use_skillZ:
                self.skill_count += 1
                if self.skill_count >= 30:
                    time.sleep(0.8)
                    press_key('z', delay=0)
                    self.skill_count = 0

    def if_spirit_in_miniMap(self):
        match_data_list = [
            [
                (2, 0),
                (255, 188, 30),
            ],
            [
                (2, 2),
                (255, 188, 30),
            ]
        ]
        pos = match_points(
            self.grab_rect,
            (255, 188, 30),
            (0, 0, 0),
            *match_data_list,
        )

        if pos != [0, 0]:
            return pos
        return False

    def if_skill_available(self, skill_char_index):
        if match_point(
                ChaosDungeon.skill_state_pos_list[skill_char_index],
                self.skill_can_use_state[skill_char_index],
                tolerance=(0, 0, 0)
        ):
            return True
        return False

    # def find_boss_in_miniMap(self):

    def find_boss_in_screen(self):
        rect = self.grab_rect
        if self.can_use_V:
            if rect_match_sqdiff(img_path + "boss_2.png", threshold=0.1, rect=(500, 7, 679, 165)):
                print("释放V")
                move_mouse(self.move_center)
                press_key('v')
                press_key('v')
                self.can_use_V = False
        first_color_list = [
            [107, 12, 8],  # 右侧
            [91, 11, 14],  # 左侧
            [150, 24, 23],  # 左上
        ]
        color_list = [
            [
                [[3, 0], [109, 110, 109]],
                [[0, 3], [132, 16, 16]],
            ],
            [
                [[-5, 0], [129, 128, 128]],
                [[-1, 4], [111, 113, 111]],
            ],
            [
                [[-2, 3], [138, 139, 138]],
                [[2, -3], [171, 174, 175]],
            ],
        ]

        for i in range(len(first_color_list)):
            # print("list", color_list[i][0], color_list[i][1])
            boss_pos = match_points(rect, first_color_list[i], (20, 20, 20), color_list[i][0], color_list[i][1])
            # boss_pos = find_multi_color(rect, first_color_list[i], (20, 20, 20), color_list[i][0], color_list[i][1])
            if boss_pos != [0, 0]:
                print("move to boss")
                pos = self.map_point(boss_pos, self.grab_center, self.move_center, 15, min=300, max=300)
                move_mouse(pos, delay=0)
                click_right_mouse_pynput(delay=0.6)
                return boss_pos
        return 0

    def find_monster(self):
        self.res()
        rect = self.grab_rect
        color = (208, 24, 24)
        pos_list = match_all_points(rect, color, (5, 5, 5),
                                    [(-1, 0), color],
                                    [(0, -1), color]
                                    )  # 找地图红色小怪

        print(pos_list)

        closest_point = pos_list[0]
        if closest_point != [0, 0]:
            self.go_to_monster(closest_point)
            self.dont_find_monser_list -= 2
        else:
            self.dont_find_monser_list += 1
            # 找怪兽卡点
            if self.dont_find_monser_list >= 10:
                if find_img_high_threshold(img_path=img_path + "chaosDungeon/monsterKaDian_1.png",
                                           rect=(1596, 39, 1893, 299), threshold=0.70) != [0, 0]:
                    time.sleep(4)
                    move_mouse(1371, 526, delay=0)
                    click_right_mouse_pynput(delay=2)
                    move_mouse(967, 233, delay=0)
                    click_right_mouse_pynput(delay=2)
                    move_mouse(1371, 526, delay=0)
                    click_right_mouse_pynput(delay=2)
                    move_mouse(967, 233, delay=0)
                    click_right_mouse_pynput(delay=2)
                elif find_img_high_threshold(img_path=img_path + "chaosDungeon/monsterKaDian_2.png",
                                             rect=(1596, 39, 1893, 299), threshold=0.7) != [0, 0]:
                    time.sleep(4)
                    move_mouse(597, 515, delay=0)
                    click_right_mouse_pynput(delay=2)
                    move_mouse(968, 182, delay=0)
                    click_right_mouse_pynput(delay=2)
                    move_mouse(597, 515, delay=0)
                    click_right_mouse_pynput(delay=2)
                    move_mouse(968, 182, delay=0)
                    click_right_mouse_pynput(delay=2)
                self.dont_find_monser_list -= 5
        return closest_point

    def go_to_monster(self, point):
        print("go to monst")
        # pos = self.map_point(point, self.grab_center, self.move_center, 15)
        new_pos = self.map_point(point, self.grab_center, self.move_center, 15, min=200, max=300)
        print("new_pos", new_pos)
        # 最少50px
        limit = 70
        if -limit < new_pos[0] - self.move_center[0] < 0:
            new_pos[0] = self.move_center[0] - limit
        if 0 <= new_pos[0] - self.move_center[0] < limit:
            new_pos[0] = self.move_center[0] + limit
        if -limit < new_pos[1] - self.move_center[1] < 0:
            new_pos[1] = self.move_center[1] - limit
        if 0 <= new_pos[1] - self.move_center[1] < limit:
            new_pos[1] = self.move_center[1] + limit

        move_1 = (new_pos[0], self.move_center[1])
        move_2 = (self.move_center[0], new_pos[1])
        move_mouse(move_1, delay=0)
        click_right_mouse(delay=0)
        move_mouse(move_2, delay=0)
        click_right_mouse(delay=0)

    def find_gate_in_screen(self):
        # yolo
        pos = yo_gate_core.screen_predict(0)
        return pos

    def find_gate(self):
        # yolo
        pos = yo_gate_core.screen_predict(0)
        if pos != [0, 0]:
            print("屏幕上找到门")
            return pos

        # opencv
        rect = self.grab_rect
        first_color_list = [
            [97, 161, 255],  # 左
            [112, 193, 255],  # 右上
            [84, 143, 255],  # 右下
        ]
        color_list = [
            [
                [[1, -4], [107, 185, 255]],
                [[0, 3], [87, 150, 255]],
            ],
            [
                [[-4, -2], [127, 214, 255]],
                [[2, 5], [98, 161, 255]],
            ],
            [
                [[-4, 2], [84, 143, 255]],
                [[1, -3], [91, 155, 255]],
            ],
        ]

        for i in range(len(first_color_list)):
            # print("list", color_list[i][0], color_list[i][1])
            pos = match_points(rect, first_color_list[i], (40, 40, 40), *color_list[i])
            # pos = find_multi_color(rect, first_color_list[i], (20, 20, 20), color_list[i][0], color_list[i][1])
            if pos != [0, 0]:
                print("小地图上找到门")
                return pos
        if if_image_exists(img_path + "enter_gate.png", threshold=0.1):
            press_key('g')
            return self.move_center
        return [0, 0]

    def move_to_gate(self):
        print("向门移动")
        count = 0
        while self.find_gate_in_screen() == [0, 0] and count < 7:
            print("向小地图门移动")
            count += 1
            if if_image_exists(img_path + "enter_gate.png", threshold=0.1):
                press_key('g')
            # 回血
            self.use_potion()
            pos = self.find_gate()
            if pos == [0, 0]:
                time.sleep(0.2)
                continue
            new_pos = self.map_point(pos, self.grab_center, self.move_center, 15, max=200)
            move_mouse(new_pos[0], self.move_center[1])
            click_right_mouse(delay=0.3)
            move_mouse(self.move_center[0], new_pos[1])
            click_right_mouse(delay=0.3)
        count = 0

        while self.find_gate_in_screen() != [0, 0] and count < 7:
            print("向屏幕门移动")
            count += 1
            pos = yo_gate_core.screen_predict(0)
            if pos != [0, 0]:
                move_mouse(self.get_move_direction(pos), delay=0)
                click_right_mouse_pynput(delay=0.5)
                if if_image_exists(img_path + "enter_gate.png", threshold=0.1):
                    press_key('g')
                    time.sleep(0.3)
            time.sleep(0.5)

    def find_core(self):
        pos = find_img_low_threshold(img_path + "chaosDungeon/core_1.png", rect=(self.grab_rect), threshold=0.07)
        if pos != [0, 0]:
            print("小地图上找到核心图片")
            return True

        pos = self.find_core_in_miniMap()
        if pos != [0, 0]:
            print("小地图上找到核心")
            return True
        pos = self.find_core_in_screen()
        if pos != [0, 0]:
            print("屏幕上找到核心")
            return True
        return False

    def move_to_core(self):
        resurrection(method=max(self.level - 2, 0))
        # 回血
        self.use_potion()

        count = 0
        pos = find_img_low_threshold(img_path + "chaosDungeon/core_1.png", rect=(self.grab_rect), threshold=0.13)
        if pos == [0, 0]:
            pos = find_img_low_threshold(img_path + "chaosDungeon/core_2.png", rect=(self.grab_rect),
                                         threshold=0.13)
        if pos != [0, 0]:
            while self.find_core_in_screen() == [0, 0] and count < 15:
                print("向小地图核心图片移动")
                count += 1
                self.use_potion()
                pos = find_img_low_threshold(img_path + "chaosDungeon/core_1.png", rect=(self.grab_rect),
                                             threshold=0.13)
                if pos == [0, 0]:
                    pos = find_img_low_threshold(img_path + "chaosDungeon/core_2.png", rect=(self.grab_rect),
                                                 threshold=0.13)
                if pos == [0, 0]:
                    continue
                new_pos = self.map_point(pos, self.grab_center, self.move_center, 15, min=200, max=200)
                # 最少50px
                limit = 70
                if -limit < new_pos[0] - self.move_center[0] < 0:
                    new_pos[0] = self.move_center[0] - limit
                if 0 <= new_pos[0] - self.move_center[0] < limit:
                    new_pos[0] = self.move_center[0] + limit
                if -limit < new_pos[1] - self.move_center[1] < 0:
                    new_pos[1] = self.move_center[1] - limit
                if 0 <= new_pos[1] - self.move_center[1] < limit:
                    new_pos[1] = self.move_center[1] + limit

                # 记录坐标防止卡点
                self.core_coord_list.append(pos)
                print("test")
                if len(self.core_coord_list) > 30:
                    self.core_coord_list.pop(0)
                ##卡点
                if len(self.core_coord_list) == 30:
                    # if len(self.core_coord_list) == 20 and \
                    #         self.euclidean_distance(self.core_coord_list[0], self.core_coord_list[2]) < 30 and \
                    #         self.euclidean_distance(self.core_coord_list[2], self.core_coord_list[4]) < 30:
                    #     卡点方位距离
                    time.sleep(5)
                    # 卡点1
                    if find_img_high_threshold(img_path=img_path + "chaosDungeon/chaosDungeon_1.png",
                                               rect=(1596, 39, 1893, 299), threshold=0.75) != [0, 0]:
                        move_mouse(1396, 205)
                        click_right_mouse_pynput(delay=3)
                        move_mouse(1919, 447)
                        click_right_mouse_pynput(delay=4)
                        move_mouse(963, 703)
                        click_right_mouse_pynput(delay=0.5)
                        click_right_mouse_pynput(delay=0.5)
                        click_right_mouse_pynput(delay=0.5)
                        click_right_mouse_pynput(delay=0.5)
                        click_right_mouse_pynput(delay=0.5)
                    elif find_img_high_threshold(img_path=img_path + "chaosDungeon/chaosDungeon_2.png",
                                                 rect=(1596, 39, 1893, 299), threshold=0.75) != [0, 0]:
                        move_mouse(1456, 527)
                        click_right_mouse_pynput(delay=5)
                        move_mouse(963, 728)
                        click_right_mouse_pynput(delay=1.5)
                        click_right_mouse_pynput(delay=1.5)
                        move_mouse(0, 467)
                        click_right_mouse_pynput(delay=5)
                    elif find_img_high_threshold(img_path=img_path + "chaosDungeon/chaosDungeon_3.png",
                                                 rect=(1596, 39, 1893, 299), threshold=0.75) != [0, 0]:
                        move_mouse(1919, 473)
                        click_right_mouse_pynput(delay=5)
                        move_mouse(961, 696)
                        click_right_mouse_pynput(delay=1.5)
                        click_right_mouse_pynput(delay=1.5)
                        click_right_mouse_pynput(delay=1.5)
                    elif find_img_high_threshold(img_path=img_path + "chaosDungeon/chaosDungeon_4.png",
                                                 rect=(1596, 39, 1893, 299), threshold=0.75) != [0, 0]:
                        move_mouse(959, 808)
                        click_right_mouse_pynput(delay=3)
                        click_right_mouse_pynput(delay=3)
                        move_mouse(0, 550)
                        click_right_mouse_pynput(delay=5)
                    elif find_img_high_threshold(img_path=img_path + "chaosDungeon/chaosDungeon_5.png",
                                                 rect=(1596, 39, 1893, 299), threshold=0.75) != [0, 0]:
                        move_mouse(957, 690)
                        click_right_mouse_pynput(delay=2)
                        click_right_mouse_pynput(delay=2)
                        move_mouse(1919, 503)
                        click_right_mouse_pynput(delay=5)
                        move_mouse(941, 123)
                        click_right_mouse_pynput(delay=3)
                    elif find_img_high_threshold(img_path=img_path + "chaosDungeon/chaosDungeon_6.png",
                                                 rect=(1596, 39, 1893, 299), threshold=0.75) != [0, 0]:
                        move_mouse(981, 70)
                        click_right_mouse_pynput(delay=4)
                        move_mouse(0, 426)
                        click_right_mouse_pynput(delay=4)
                    else:
                        top = 430
                        bottom = 300
                        right = 1000
                        left = 1000

                        # x向右或左
                        if self.core_dir == 0:
                            self.core_dir = 1
                        else:
                            self.core_dir = 0
                        if new_pos[1] < self.move_center[1]:  # y坐标对比
                            move_mouse(self.move_center[0], self.move_center[1] + bottom)
                            click_right_mouse_pynput(delay=2)
                        else:
                            move_mouse(self.move_center[0], self.move_center[1] - top)
                            click_right_mouse_pynput(delay=2)

                        # if new_pos[0] < self.move_center[0]:  # x坐标对比
                        if self.core_dir == 0:
                            move_mouse(self.move_center[0] - left, self.move_center[1])
                            click_right_mouse_pynput(delay=2)
                        else:
                            move_mouse(self.move_center[0] + right, self.move_center[1])
                            click_right_mouse_pynput(delay=2)

                        if new_pos[1] < self.move_center[1]:  # y坐标对比
                            move_mouse(self.move_center[0], self.move_center[1] - top)
                            click_right_mouse_pynput(delay=2)
                        else:
                            move_mouse(self.move_center[0], self.move_center[1] + bottom)
                            click_right_mouse_pynput(delay=2)
                    self.core_coord_list = []  # 清空
                else:
                    move_1 = (new_pos[0], self.move_center[1])
                    move_2 = (self.move_center[0], new_pos[1])
                    move_mouse(move_1, delay=0)
                    click_right_mouse(delay=0)
                    move_mouse(move_2, delay=0)
                    click_right_mouse(delay=0)
        count = 0
        while self.find_core_in_screen() == [0, 0] and count < 9:
            print("向小地图核心移动")
            count += 1
            self.use_potion()
            pos = self.find_core_in_miniMap()
            if pos == [0, 0]:
                time.sleep(0.2)
                continue
            new_pos = self.map_point(pos, self.grab_center, self.move_center, 15, min=200, max=200)
            # 最少50px
            limit = 70
            if -limit < new_pos[0] - self.move_center[0] < 0:
                new_pos[0] = self.move_center[0] - limit
            if 0 <= new_pos[0] - self.move_center[0] < limit:
                new_pos[0] = self.move_center[0] + limit
            if -limit < new_pos[1] - self.move_center[1] < 0:
                new_pos[1] = self.move_center[1] - limit
            if 0 <= new_pos[1] - self.move_center[1] < limit:
                new_pos[1] = self.move_center[1] + limit

            # 记录坐标防止卡点
            self.core_coord_list.append(pos)
            print("test")
            if len(self.core_coord_list) > 30:
                self.core_coord_list.pop(0)
            ##卡点
            if len(self.core_coord_list) == 30:
                # if len(self.core_coord_list) == 20 and \
                #         self.euclidean_distance(self.core_coord_list[0], self.core_coord_list[2]) < 30 and \
                #         self.euclidean_distance(self.core_coord_list[2], self.core_coord_list[4]) < 30:
                #     卡点方位距离
                time.sleep(5)
                # 卡点1
                if find_img_high_threshold(img_path=img_path + "chaosDungeon/chaosDungeon_1.png",
                                           rect=(1596, 39, 1893, 299), threshold=0.75) != [0, 0]:
                    move_mouse(1396, 205)
                    click_right_mouse_pynput(delay=3)
                    move_mouse(1919, 447)
                    click_right_mouse_pynput(delay=4)
                    move_mouse(963, 703)
                    click_right_mouse_pynput(delay=0.5)
                    click_right_mouse_pynput(delay=0.5)
                    click_right_mouse_pynput(delay=0.5)
                    click_right_mouse_pynput(delay=0.5)
                    click_right_mouse_pynput(delay=0.5)
                elif find_img_high_threshold(img_path=img_path + "chaosDungeon/chaosDungeon_2.png",
                                             rect=(1596, 39, 1893, 299), threshold=0.75) != [0, 0]:
                    move_mouse(1456, 527)
                    click_right_mouse_pynput(delay=5)
                    move_mouse(963, 728)
                    click_right_mouse_pynput(delay=1.5)
                    click_right_mouse_pynput(delay=1.5)
                    move_mouse(0, 467)
                    click_right_mouse_pynput(delay=5)
                elif find_img_high_threshold(img_path=img_path + "chaosDungeon/chaosDungeon_3.png",
                                             rect=(1596, 39, 1893, 299), threshold=0.75) != [0, 0]:
                    move_mouse(1919, 473)
                    click_right_mouse_pynput(delay=5)
                    move_mouse(961, 696)
                    click_right_mouse_pynput(delay=1.5)
                    click_right_mouse_pynput(delay=1.5)
                    click_right_mouse_pynput(delay=1.5)
                elif find_img_high_threshold(img_path=img_path + "chaosDungeon/chaosDungeon_4.png",
                                             rect=(1596, 39, 1893, 299), threshold=0.75) != [0, 0]:
                    move_mouse(959, 808)
                    click_right_mouse_pynput(delay=3)
                    click_right_mouse_pynput(delay=3)
                    move_mouse(0, 550)
                    click_right_mouse_pynput(delay=5)
                elif find_img_high_threshold(img_path=img_path + "chaosDungeon/chaosDungeon_5.png",
                                             rect=(1596, 39, 1893, 299), threshold=0.75) != [0, 0]:
                    move_mouse(957, 690)
                    click_right_mouse_pynput(delay=2)
                    click_right_mouse_pynput(delay=2)
                    move_mouse(1919, 503)
                    click_right_mouse_pynput(delay=5)
                    move_mouse(941, 123)
                    click_right_mouse_pynput(delay=3)
                elif find_img_high_threshold(img_path=img_path + "chaosDungeon/chaosDungeon_6.png",
                                             rect=(1596, 39, 1893, 299), threshold=0.75) != [0, 0]:
                    move_mouse(981, 70)
                    click_right_mouse_pynput(delay=4)
                    move_mouse(0, 426)
                    click_right_mouse_pynput(delay=4)
                else:
                    top = 430
                    bottom = 300
                    right = 1000
                    left = 1000

                    # x向右或左
                    if self.core_dir == 0:
                        self.core_dir = 1
                    else:
                        self.core_dir = 0
                    if new_pos[1] < self.move_center[1]:  # y坐标对比
                        move_mouse(self.move_center[0], self.move_center[1] + bottom)
                        click_right_mouse_pynput(delay=2)
                    else:
                        move_mouse(self.move_center[0], self.move_center[1] - top)
                        click_right_mouse_pynput(delay=2)

                    # if new_pos[0] < self.move_center[0]:  # x坐标对比
                    if self.core_dir == 0:
                        move_mouse(self.move_center[0] - left, self.move_center[1])
                        click_right_mouse_pynput(delay=2)
                    else:
                        move_mouse(self.move_center[0] + right, self.move_center[1])
                        click_right_mouse_pynput(delay=2)

                    if new_pos[1] < self.move_center[1]:  # y坐标对比
                        move_mouse(self.move_center[0], self.move_center[1] - top)
                        click_right_mouse_pynput(delay=2)
                    else:
                        move_mouse(self.move_center[0], self.move_center[1] + bottom)
                        click_right_mouse_pynput(delay=2)
                self.core_coord_list = []  # 清空
            else:
                move_1 = (new_pos[0], self.move_center[1])
                move_2 = (self.move_center[0], new_pos[1])
                move_mouse(move_1, delay=0)
                click_right_mouse(delay=0)
                move_mouse(move_2, delay=0)
                click_right_mouse(delay=0)

        count = 0
        while self.find_core_in_screen() != [0, 0] and count < 6:
            print("向屏幕核心移动")
            pos = self.find_core_in_screen()
            if pos == [0, 0]:
                time.sleep(0.4)
                continue
            move_mouse(self.get_move_direction(pos), delay=0)
            click_right_mouse_pynput(delay=0.5)
            move_mouse(self.get_move_direction(pos), delay=0)
            self.use_random_skill(num=1, random_move_mouse=False)
            time.sleep(1)

    def euclidean_distance(self, point1, point2):
        """
        计算两点距离
        :param point1:
        :param point2:
        :return:
        """
        # print(point1,point2)
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

    def get_move_direction(self, pos, radius=200):  # 提供一个方向，向其移动
        # 计算方向向量
        direction_vector = (pos[0] - self.move_center[0], pos[1] - self.move_center[1])

        # 计算方向向量的长度
        distance = math.sqrt(direction_vector[0] ** 2 + direction_vector[1] ** 2)

        # 归一化方向向量
        if distance == 0:
            raise ValueError("Position and move_center cannot be the same point")
        normalized_vector = (direction_vector[0] / distance, direction_vector[1] / distance)

        # 将方向向量乘以 radius
        new_vector = (normalized_vector[0] * radius, normalized_vector[1] * radius)

        # 计算新的坐标
        new_pos = (self.move_center[0] + new_vector[0], self.move_center[1] + new_vector[1])

        return new_pos

    def find_core_in_screen(self):
        # yolo写法
        pos = yo_gate_core.screen_predict(1)
        if pos != [0, 0]:
            if self.core_coord_list != []:
                self.core_coord_list.pop(0)

        return pos

    def close_quest_journal(self):
        move_mouse(100, 100)
        if if_image_exists(img_path + "questJournal.png"):
            print("找到任务图标")
            click_image(img_path + "questJournal.png", delay=2)
            press_key('esc', delay=2)
        move_mouse(100, 100)
        if if_image_exists(img_path + "addSkill.png"):
            print("找到技能图标")
            click_image(img_path + "addSkill.png", delay=2)
            press_key('esc', delay=2)

    def find_core_in_miniMap(self):
        rect = self.grab_rect
        first_color_list = [
            [164, 120, 117],  # 左侧
            [190, 127, 124],  # 右侧
            [252, 123, 134],  # 上
        ]
        color_list = [
            [
                [[4, -5], [231, 146, 157]],
                [[-1, 4], [143, 126, 102]],
            ],
            [
                [[-3, -3], [231, 83, 81]],
                [[1, 2], [155, 132, 114]],
            ],
            [
                [[0, -3], [236, 188, 196]],
                [[0, 3], [242, 75, 73]],
            ],
        ]
        for i in range(len(first_color_list)):
            # print("list", color_list[i][0], color_list[i][1])
            pos = match_points(rect, first_color_list[i], (30, 30, 30), *color_list[i])
            # pos = find_multi_color(rect, first_color_list[i], (20, 20, 20), color_list[i][0], color_list[i][1])
            if pos != [0, 0]:
                if i == 0:
                    print("左侧")
                print("找到小地图核心")
                return pos
        return [0, 0]

    def map_point(self, pos, reference_point_old, reference_point_new, n, min=100, max=200):
        # 计算pos相对于旧参考点的偏移
        offset_x = pos[0] - reference_point_old[0]
        offset_y = pos[1] - reference_point_old[1]

        # 将偏移放大n倍
        offset_x_new = offset_x * n
        offset_y_new = offset_y * n

        # 计算新点相对于新参考点的坐标
        new_pos_x = reference_point_new[0] + offset_x_new
        new_pos_y = reference_point_new[1] + offset_y_new

        # 计算新偏移的欧几里得距离
        new_offset_distance = math.sqrt(offset_x_new ** 2 + offset_y_new ** 2)

        # 限制新偏移的距离在100到300之间
        if new_offset_distance < min:
            scale_factor = min / new_offset_distance
            offset_x_new *= scale_factor
            offset_y_new *= scale_factor
        elif new_offset_distance > max:
            scale_factor = max / new_offset_distance
            offset_x_new *= scale_factor
            offset_y_new *= scale_factor

        # 重新计算新点相对于新参考点的坐标
        new_pos_x = reference_point_new[0] + offset_x_new
        new_pos_y = reference_point_new[1] + offset_y_new

        return [new_pos_x, new_pos_y]

    def get_weeklyTask_reward(self):
        click(1650, 396)
        click(359, 744)
        clear_interface()

    def repair(self):
        chat_with_NPC()
        # 修装备，
        while match_point((1110, 681), (255, 255, 255)):
            click(1110, 681)
        # 生活工具
        click(1030, 860, delay=3)
        click(887, 749, delay=3)
        click_OK()

        leave_NPC_chat()

    def get_weekly_task(self):
        while ppocr((73, 206, 161, 239), det=True) != "Roster":
            combine_keys('alt', 'j', delay=2)

        while not match_point((538, 204), (236, 225, 162)):
            click(538, 204)

        click(602, 357)
        click(1281, 356)

        clear_interface()

    def start_chaosDungeon(self, get_chaosDungeon_level=True, open_ui=False):
        if open_ui:
            self.go_to_chaosDungeon_and_get_mode()

        # 获得可以挑战的次数
        if self.mode == ChaosDungeonMode.t3Mode:
            str = ppocr((1695, 770, 1770, 791), det=True)
            consumed = ChaosDungeonMode.t3Consumed
        elif self.mode == ChaosDungeonMode.t4Mode:
            str = ppocr((1690, 758, 1766, 780), det=True)
            consumed = ChaosDungeonMode.t4Consumed
        # print(str)
        if str == None:
            clear_interface()
            return 0
        rest_bonus = int(str.split('/')[0])

        times = int(rest_bonus / consumed)
        if times < 1:
            return False

        # T3进入副本
        if self.mode == ChaosDungeonMode.t3Mode:
            while ppocr((867, 118, 941, 146)) == "Chaos":
                if get_chaosDungeon_level:
                    str = ppocr((1259, 340, 1318, 369))
                    if str != None:
                        gl_info.chaosDungeon_level = str

                click(1598, 864, delay=3)  # start
                click(886, 604)  # get checkbox
                click_OK()  # get ok button
                click_OK()
                time.sleep(6)

            wait_for_trans()
        # T4进入副本
        else:
            while ppocr((971, 156, 1038, 179), det=True) == "Front":
                if get_chaosDungeon_level:
                    str = ppocr((1257, 324, 1317, 348))
                    if str != None:
                        gl_info.chaosDungeon_level = str

                click(1588, 857)
                click(886, 604)  # get checkbox
                click_OK()  # get ok button
                click_OK()
                time.sleep(6)

            wait_for_trans()

        return True

    def leave_chaosDungeon(self):
        song_leave_simple()
        time.sleep(10)
        wait_for_trans()

    def go_to_chaosDungeon_and_get_mode(self):
        """
        打开混沌地牢界面
        :return:
        """
        move_mouse(100, 100)

        # 打开界面
        while not if_image_exists(img_path + "gameUi/SelectUi.png"):
            combine_keys('alt', 'q', delay=2)

        # 判断是T3还是T4 mode
        self.mode = ChaosDungeonMode.t3Mode
        if ppocr((1405, 188, 1450, 207)) == "Select":  # 选取按钮为T3界面
            click_image(img_path + "gameUi/SelectUi.png", delay=3)  # 打开切换UI界面
            if ppocr((1185, 438, 1225, 456)) == "Tier":  # 识别T4
                self.mode = ChaosDungeonMode.t4Mode
                # 切换至T4面板
                if not match_point((1141, 490), (239, 198, 2)):
                    click(1141, 490)
                if ppocr((937, 703, 981, 722)) == "Apply":
                    click(961, 713)
        else:
            self.mode = ChaosDungeonMode.t4Mode

        # 根据mode切换至T3或T4对应的界面
        if self.mode == ChaosDungeonMode.t3Mode:
            # 切换至旧UI
            if not match_point((793, 446), (246, 203, 1)):
                click(793, 446)
            if ppocr((938, 662, 981, 681)) == "Apply":
                click(958, 670)
            # 打开地牢
            if ppocr((983, 126, 1029, 152)) == "List":
                mark_pos = find_img_low_threshold(img_path + "chaosDungeon/T3CDMark.png")  # 打过的匹配不到，不会打
                diff = [402, 41]
                click_pos = [mark_pos[0] + diff[0], mark_pos[1] + diff[1]]
                click(click_pos, delay=2)
        else:
            # 打开地牢
            if ppocr((970, 139, 1040, 168)) != "Front":
                click(786, 757, delay=2)
            ## 切换至对应等级
            first_pos = [490, 590]
            len = 64
            for i in range(5):
                if not match_point((1400, 775), (77, 65, 27)):
                    click(first_pos)
                    first_pos[1] += len
            first_pos[1] -= len * 2
            click(first_pos)

    def callback(self):
        # move_mouse(1919,0)
        # release_all_keys_pynput()
        # click(1919,549)
        gl_info.log = gl_info.log + ", " + f"混沌地牢第{gl_info.char_number}个角色第{self.times}次第{self.level}层失败"
        print("chaosDungeon callback")


if __name__ == "__main__":
    cd = ChaosDungeon()

    pos = [1919, 1079]
    cd.target_object(pos, radius=200)
