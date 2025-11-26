#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time

import pytz

from Application.Control.threadControl import ThreadControl
from Application.tasks.chaosDungeon import ChaosDungeon
from Application.tasks.game_action import *
from Application.tasks.pathFinder import *
from Application.tools import *


class ChaosGate:
    def __init__(self):

        self.finder = chaosgate_valley_finder
        self.darkness_center = [294.0, 270.0]
        self.valley_center = [295.0, 307.0]
        self.phantom_center = [320.0, 318.0]
        self.plague_center = [352.0, 359.0]
        self.center = None

        self.move_func = None
        self.cd = ChaosDungeon()

    def main_loop(self):
        gl_info.thread_main.execution_time = -1800  # 40分钟

        # 切换到第一个角色
        switch_char_ingame(0)
        # 打开地图
        move_mouse(960, 540)
        while ppocr((1601, 900, 1646, 918)) != "Memo":
            press_key('m')

        # T3或T4
        # get_equip_level()
        # if float(gl_info.equip_level) >= 1640:
        #     # T3去帕普你卡
        #     time.sleep(2)
        #     if ppocr((345, 130, 440, 162), det=True) == "Kurzan":  # 在库尔赞就不去了
        #         while ppocr((1601, 900, 1646, 918)) == "Memo":
        #             press_key('m')
        #     else:
        #         board_ocean_liner((1258, 428))
        #
        #     # 去传送点
        #     move_to_triport([1402, 378], [806, 566], [1017, 545])
        #     wait_for_trans()
        #     clear_interface()
        #
        #     ride_mount()
        #     path = [235.0, 509.0], [259.0, 489.0], [277.0, 476.0], [282.0, 461.0], [287.0, 452.0], [290.0, 443.0], [
        #         295.0, 432.0], [302.0, 413.0], [311.0, 394.0], [319.0, 373.0], [330.0, 346.0], [337.0, 333.0], [343.0,
        #                                                                                                         317.0], [
        #         355.0, 290.0], [365.0, 273.0], [371.0, 256.0], [378.0, 252.0],
        #     kurzan_s1_finder.node_finder(path)
        # else:
        # T3去帕普你卡
        time.sleep(2)
        if ppocr((262, 126, 516, 165), det=True) == "Punika":  # 在帕普你卡就不去了
            while ppocr((1601, 900, 1646, 918)) == "Memo":
                press_key('m')
        else:
            board_ocean_liner((764, 658))

        # 去星星沙滩
        move_to_triport([666, 702], [1050, 365], [697, 440])
        wait_for_trans()
        clear_interface()

        # ride_mount()
        path = [291.0, 407.0], [307.0, 394.0], [316.0, 379.0], [325.0, 367.0], [345.0, 366.0], [360.0, 363.0], [
            382.0,
            347.0], [
            375.0, 337.0], [364.0, 311.0], [358.0, 297.0], [329.0, 289.0],
        punika_starbeach_finder.node_finder(path, distance_to_target=3)

        # 加入混沌之门
        if not self.join_chaosgate():
            clear_interface()
            board_ocean_liner()
            return  # 没加入直接结束

        gl_info.thread_main.execution_time = -600  # 20分钟
        # 战斗，循环进战场、战斗、判断结束
        self.move_func()
        self.finder.move_to_center(self.center, run_time=5)
        while not self._if_end():
            ## 战斗
            self.use_skill()
            if if_die():  # 放技能死
                resurrection()
                self.finder.move_to_center(self.center)
                continue
            self.finder.move_to_center(self.center)
            if if_die():  # 走路死
                resurrection()
                self.finder.move_to_center(self.center)
                continue
        if if_die():  # 领东西之前不能死
            resurrection()
            self.finder.move_to_center(self.center, run_time=5)
        song_leave_simple()
        time.sleep(10)  # 把歌唱完
        wait_for_trans()
        clear_interface()
        board_ocean_liner()

    # 判断是否结束战斗
    def _if_end(self):
        end_img = img_path + "home/mission_OK.png"  # 任务完成标志

        if ppocr((126, 165, 175, 188), det=True) == "Exit":  # 全部战斗完毕
            return True
        elif if_image_exists(end_img):  # 战斗完毕出结算窗口，可能有隐藏门
            clear_interface()
        elif gl_info.thread_main.execution_time > 300:  # 超时
            return True
        return False

    # 跳进战场
    def _jump_to_battleField(self):
        wait_for_image(img_path + "jump_to_battleField.png")
        while if_image_exists(img_path + "jump_to_battleField.png"):
            press_key('g')
        time.sleep(1)

    def use_skill(self):  # 放技能
        for i in range(3):
            if if_die():
                return
            # 屏幕中心点坐标
            center_x, center_y = 960, 533

            # 定义半径
            radius = 200

            # 生成随机的极坐标角度（弧度制）
            if (i - 1) % 4 == 1:
                theta = random.uniform(0, np.pi / 2)
            elif (i - 1) % 4 == 2:
                theta = random.uniform(np.pi / 2, np.pi)
            elif (i - 1) % 4 == 3:
                theta = random.uniform(np.pi, 3 * np.pi / 2)
            else:
                theta = random.uniform(3 * np.pi / 2, 2 * np.pi)

            # 将极坐标转换为直角坐标
            random_x = center_x + radius * np.cos(theta)
            random_y = center_y + radius * np.sin(theta)
            move_mouse(random_x, random_y, delay=0)
            self.cd.use_random_skill(5)
            self.cd.use_potion(use_1=True)
            # time.sleep(1)

    def _move_in_valley(self):
        # valley
        move_mouse(529, 241)
        click_right_mouse_pynput()
        time.sleep(3)
        move_mouse(330, 207)
        click_right_mouse_pynput()
        time.sleep(5)
        move_mouse(563, 549)
        click_right_mouse_pynput()
        self._jump_to_battleField()

    def _move_in_plague(self):
        # plague
        move_mouse(539, 887)
        click_right_mouse_pynput()
        time.sleep(3)
        move_mouse(578, 921)
        click_right_mouse_pynput()
        time.sleep(5)
        move_mouse(74, 673)
        click_right_mouse_pynput()
        time.sleep(4)
        move_mouse(755, 435)
        click_right_mouse_pynput()
        time.sleep(4)
        move_mouse(659, 200)
        click_right_mouse_pynput()
        self._jump_to_battleField()

    def _move_in_darkness(self):
        # darkness
        move_mouse(943, 41)
        click_right_mouse_pynput()
        time.sleep(4)
        move_mouse(875, 148)
        click_right_mouse_pynput()

        # move_mouse(888,40)
        # click_right_mouse_pynput()
        # time.sleep(3)
        # press_key('t')
        # wait_for_image(current_path + "/../data/mark/weekly_mission/chaosgate/jump_to_battleField.png")
        # press_key('t')
        self._jump_to_battleField()

    def _move_in_phantom(self):  # 未完成
        # phantom
        move_mouse(897, 78)
        click_right_mouse_pynput()
        time.sleep(4)
        move_mouse(898, 63)
        click_right_mouse_pynput()
        time.sleep(3)
        move_mouse(951, 422)
        click_right_mouse_pynput()

        # move_mouse(923, 146)
        # click_right_mouse_pynput()
        # time.sleep(3)
        # press_key('t')
        # wait_for_image(current_path + "/../data/mark/weekly_mission/chaosgate/jump_to_battleField.png")
        # press_key('t')
        self._jump_to_battleField()

    # 等待混沌之门出现
    def join_chaosgate(self):
        # 打开匹配界面
        while True:
            if ppocr((895, 169, 968, 194), det=True) == "Chaos":  # 打开了匹配界面
                break
            if if_image_exists(img_path + "enter_gate.png"):  # G键进入
                press_key('g')

        # 获取地图
        str = ppocr((855, 198, 1062, 222), det=True)
        if "Phantom" in str:
            self.finder = chaosgate_phantom_finder
            self.center = self.phantom_center
            self.move_func = self._move_in_phantom
        elif "Darkness" in str:
            self.finder = chaosgate_darkness_finder
            self.center = self.darkness_center
            self.move_func = self._move_in_darkness
        elif "Plague" in str:
            self.finder = chaosgate_plague_finder
            self.center = self.plague_center
            self.move_func = self._move_in_plague
        elif "Valley" in str:
            self.finder = chaosgate_valley_finder
            self.center = self.valley_center
            self.move_func = self._move_in_valley

        # # 等待随机90秒
        # self.wait_random_time()

        # 点击匹配
        while ppocr((895, 169, 968, 194), det=True) == "Chaos":
            if ppocr((976, 809, 1019, 830), det=False) == "Apply":  # and match_point((1027, 821), (134, 101, 19))
                click(997, 820)
                # 超过次数
                time.sleep(1)
                # if if_image_exists(image_path=img_path + "entry_count.png"):
                if ppocr((960, 408, 1003, 426)) == "Count":
                    clear_interface()
                    print("超过次数")
                    return False
        if if_trans():  # 成功匹配
            wait_for_trans()
            time.sleep(4)
            return True
        else:  # 没匹配到
            # 检查10秒内有没有传送，可能是界面卡了
            t = time.time()
            while time.time() - t < 10:
                if if_trans():
                    return True
            return False

    def if_chaosgate(self, wait_time=10):
        """
        判断是否需要打混沌之门
        :param wait_time: 提前判断的时间
        :return: 是否需要打
        """
        # 获取当前时间
        # 获取美国西部的时区对象
        pacific = pytz.timezone('US/Pacific')
        # 获取美国东部的时区对象
        eastern = pytz.timezone('US/Eastern')
        # 获取欧洲中部的时区对象
        central_european = pytz.timezone('Europe/Paris')
        # 获取当前时间
        current_time = datetime.datetime.now()
        # 将当前时间转换为欧洲中部时间
        eucnetral_time = current_time.astimezone(central_european)
        # 将当前时间转换为美国西部时间
        west_time = current_time.astimezone(pacific)
        # 将当前时间转换为美国东部时间
        east_time = current_time.astimezone(eastern)

        print("current_time", current_time)
        print("west_time", west_time)
        print("east_time", east_time)

        # 根据大区判断
        if gl_info.region == 'w':
            current_time = west_time
            print(current_time)
        elif gl_info.region == 'e':
            current_time = east_time
        elif gl_info.region == 'c':
            current_time = eucnetral_time

        weekday = current_time.weekday()  # 星期
        hour = current_time.hour  # 小时
        minute = current_time.minute  # 分钟

        # # 1490以上才参加
        # if float(gl_info.equip_level) < 1490:
        #     return False
        if minute < 60 - wait_time:  # 开始时间
            return False
        if weekday == 4 or weekday == 1:
            if hour < 5:
                return True
        elif weekday == 3 or weekday == 5:
            if hour >= 10:
                return True
        elif weekday == 6 or weekday == 0:
            if hour >= 10 or hour < 5:
                return True

        return False

    # 进入混沌之门前，等待随机时间
    def wait_random_time(self):  # 进入混沌之门前，等待随机时间
        """
        进入混沌之门前，等待随机时间
        :return:
        """
        # 获取当前时间
        current_time = datetime.datetime.now()

        # 提取当前时间的分钟和秒
        minutes = current_time.minute
        seconds = current_time.second

        # 计算分钟和秒转换为总秒数
        total_seconds = minutes * 60 + seconds
        random_number = random.randint(1, 90)  # 生成1到90之间的随机整数
        if random_number - total_seconds > 0:
            time.sleep(random_number - total_seconds)
