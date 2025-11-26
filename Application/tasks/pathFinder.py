#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import math
import random
import time

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from Application.tasks.game_action import *

from Application.tools import *
from Application.public import *


class PathFinder:
    def __init__(self, map_path, resize,
                 max_val=0.6):
        self.resize = resize
        self.max_val = max_val  # 寻路相似度阈值
        self.move_center = (960, 533)  # 脚底
        self.move_radius = 120
        self.grab_center = (1742, 166)
        self.grab_radius = 124
        self.grab_rect = (
            self.grab_center[0] - self.grab_radius, self.grab_center[1] - self.grab_radius,
            self.grab_center[0] + self.grab_radius,
            self.grab_center[1] + self.grab_radius)
        self.astar_grid_size = 2
        self.astar_grid_size_half = int((self.astar_grid_size / 2) // 1)
        self.map = self.__load_map(map_path)
        self.trigger = True

    def astar_finder(self, destination, distance_to_target=6):
        self.__init_astar()  # init
        # set start coordinate
        map_coord = self.get_current_coordinate()
        x, y = self.__convert_map_coord_to_array_coord(map_coord[0], map_coord[1])
        self.__set_astar_start(x, y)
        # set end coordinate
        x, y = self.__convert_map_coord_to_array_coord(destination[0], destination[1])
        self.__set_astar_end(x, y)
        path = self.__calculate_astar_path()
        self.trigger = True
        for i in path:
            resized_coord = [i[0] * self.astar_grid_size - self.astar_grid_size_half,
                             i[1] * self.astar_grid_size - self.astar_grid_size_half]
            self.navigate(resized_coord, distance_to_target)
        release_right_mouse(delay=0)

    def node_finder(self, coord_array, distance_to_target=6):
        self.trigger = True
        for i in coord_array:
            self.navigate(i, distance_to_target)
        release_right_mouse(delay=0)
        move_mouse_pynput(self.move_center, delay=0)
        click_right_mouse()

    def go_to(self, pos, max_time=99999, func=None):
        t = time.time()
        while time.time() - t < max_time:
            ...

    def if_this_map(self, threshold=0.7):
        """
        根据小地图判断是否为本地图
        :param threshold:
        :return: 没有匹配到返回0， 匹配到了返回max_val
        """
        self.__grab_mini_map()
        result = cv2.matchTemplate(self.map, self.mini_map, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val > threshold:
            return max_val
        return 0

    def get_current_coordinate(self):
        self.__grab_mini_map()
        result = cv2.matchTemplate(self.map, self.mini_map, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        current_coordinate = [0, 0]
        print(max_val)
        if max_val > self.max_val:
            width, height = self.mini_map.shape[:2]
            current_coordinate[0] = int(max_loc[0] + width / 2)
            current_coordinate[1] = int(max_loc[1] + height / 2)
        else:
            current_coordinate = [0, 0]
        return current_coordinate

    def load_node_file(self, file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()
            rows = len(lines)
            cols = len(lines[0].split())
            array = np.zeros((rows, cols), dtype=int)
            for i in range(rows):
                line = lines[i].split()
                for j in range(cols):
                    array[i][j] = int(line[j])
            self.node_array = array

    def __init_astar(self):
        self.astar_node = Grid(matrix=self.node_array)
        self.astar = AStarFinder(diagonal_movement=DiagonalMovement.always)

    def __calculate_astar_path(self):
        path, runs = self.astar.find_path(self.start, self.end, self.astar_node)
        return path

    def __set_astar_start(self, x, y):
        self.start = None
        self.start = self.astar_node.node(y, x)

    def __set_astar_end(self, x, y):
        self.end = None
        self.end = self.astar_node.node(y, x)

    def __convert_map_coord_to_array_coord(self, x, y):  # 地图坐标转换为数组
        i = y // self.astar_grid_size
        j = x // self.astar_grid_size
        return int(i), int(j)

    def move_to_center(self, destination, run_time=2):  # 混沌之门使用
        t = time.time()
        timer = 0
        while True:
            timer = time.time() - t
            current_coord = self.get_current_coordinate()
            if current_coord[0] == 0:
                release_right_mouse()
                click_left_mouse(delay=0.5)
                self.__random_move()
                press_key('space', delay=0.5)
                hold_right_mouse()
                time.sleep(0.5)
                t = time.time()
            elif timer > run_time:  # 超时退出
                release_right_mouse()
                break
            else:
                mouse_pos = self.__calculate_mouse_offset(current_coord, destination)
                distance = math.sqrt(
                    (current_coord[0] - destination[0]) ** 2 + (current_coord[1] - destination[1]) ** 2)
                if distance < 15:
                    release_right_mouse()
                    break
                else:
                    move_mouse_pynput(mouse_pos, delay=0)
                    hold_right_mouse()

    def navigate(self, destination, distance_to_target, max_time=99999, random_move_time=10, func=None):  # 寻路
        """
        基本寻路
        :param destination:目的坐标
        :param distance_to_target:当前位置与目的坐标的距离
        :param max_time:最大时间
        :param func:寻路中需要执行的函数
        :return: True: 到达地点; False: 未到达地点
        """
        print("navigate")
        t = time.time()
        timer = 0
        while time.time() - t < max_time:
            if func is not None:
                func()
            timer = time.time() - t
            current_coord = self.get_current_coordinate()
            # 移动超时或寻找不到位置坐标
            if current_coord[0] == 0 or timer > random_move_time:
                print("找不到当前坐标或超时")
                clear_interface()
                release_right_mouse()
                click_left_mouse(delay=0.5)
                self.__random_move()
                press_key('space', delay=0.5)
                hold_right_mouse()
                time.sleep(0.5)
                t = time.time()
            # 正常移动
            else:
                mouse_pos = self.__calculate_mouse_offset(current_coord, destination)
                distance = math.sqrt(
                    (current_coord[0] - destination[0]) ** 2 + (current_coord[1] - destination[1]) ** 2)
                if distance < distance_to_target:
                    # release_right_mouse(delay=0)
                    return True
                else:
                    move_mouse_pynput(mouse_pos)
                    if self.trigger:
                        self.trigger = False
                        hold_right_mouse()
        print("寻路失败")
        return False

    def __load_map(self, path):  # 加载地图
        map = cv2.imread(path, 0)
        return cv2.resize(map, (0, 0), fx=self.resize, fy=self.resize)

    def __grab_mini_map(self):  # 截图小地图
        # 截图
        image = grab_rect_to_cv2(self.grab_rect)
        # # 处理
        # r = 5
        # image[self.grab_radius-r:self.grab_radius+r,self.grab_radius-r:self.grab_radius+r] = 0
        # # cv2.imshow('结果图像', image)
        # # cv2.waitKey(0)

        self.mini_map = image

    def __calculate_mouse_offset(self, current, destination):  # 计算鼠标偏移
        print("test", destination)
        a = {'x': int(current[0]), 'y': int(current[1])}
        b = {'x': int(destination[0]), 'y': int(destination[1])}
        # 角度 = (math.atan2(b['y'] - a['y'], b['x'] - a['x']) * 180 / math.pi - 90) % 360
        radian = math.atan2(b['y'] - a['y'], b['x'] - a['x'])
        # 距离 = math.sqrt((b['y'] - a['y']) ** 2 + (b['x'] - a['x']) ** 2)
        coord = [0, 0]
        coord[0] = self.move_center[0] + self.move_radius * math.cos(radian)
        coord[1] = self.move_center[1] + self.move_radius * math.sin(radian)
        return coord

    def __random_move(self):  # 卡点时随机移动
        a = {'x': random.randint(10, 360), 'y': random.randint(10, 360)}
        b = {'x': random.randint(10, 360), 'y': random.randint(10, 360)}
        radian = math.atan2(b['y'] - a['y'], b['x'] - a['x'])
        coord = [0, 0]
        coord[0] = self.move_center[0] + self.move_radius * math.cos(radian)
        coord[1] = self.move_center[1] + self.move_radius * math.sin(radian)
        move_mouse_pynput(coord, delay=0)


punika_starbeach_finder = PathFinder(img_path + "map/starbeach.png", resize=2.2)  # T3混沌之门
kurzan_s1_finder = PathFinder(img_path + "map/kurzanS1.png", resize=1.9, max_val=0.5)  # T4混沌之门

luterra_triport_finder = PathFinder(img_path + "map/task_2_port.png", resize=1.4)  # 卢特兰港口

cube_ticket_finder_1 = PathFinder(img_path + "map/get_cube_ticket_1.png", resize=1)
cube_ticket_finder_2 = PathFinder(img_path + "map/get_cube_ticket_2.png", resize=1)
fish_finder_t3 = PathFinder(img_path + "map/fish/fish.png", resize=2.1, max_val=0.45)
fish_finder_t4 = PathFinder(img_path + "map/fish/fish_t4.png", resize=1.3, max_val=0.45)
# 混沌之门寻路
chaosgate_darkness_finder = PathFinder(img_path + "map/chaosgate/darkness.png", resize=2.1, max_val=0.5)
chaosgate_valley_finder = PathFinder(img_path + "map/chaosgate/Valley.png", resize=1.8, max_val=0.5)
chaosgate_phantom_finder = PathFinder(img_path + "map/chaosgate/Phantom.png", resize=1.8, max_val=0.5)
chaosgate_plague_finder = PathFinder(img_path + "map/chaosgate/Plague.png", resize=2.2, max_val=0.5)
# T4CD
t4cd_1_finder = PathFinder(img_path + "map/T4CD/T4CD_1.png", resize=1.4, max_val=0.5)
t4cd_2_finder = PathFinder(img_path + "map/T4CD/T4CD_2.png", resize=1, max_val=0.43)
t4cd_3_finder = PathFinder(img_path + "map/T4CD/T4CD_3.png", resize=1, max_val=0.55)
