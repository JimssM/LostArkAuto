import math
import time

import numpy as np
import pyautogui
import pynput
import win32api
import random
from pynput.keyboard import Key as pynput_key_val
from pynput.mouse import Button as pynput_button_val

pyautogui.FAILSAFE = False  # 关闭安全模式

pynput_key = pynput.keyboard.Controller()  # pynput键盘控制器
pynput_mouse = pynput.mouse.Controller()  # pynput鼠标控制器

'''
滚轮
'''


def scroll(val, method=1):  # 负数向下
    '''
    移动滚轮，负数向下
    :param val:滚动的值，1方法时为鼠标滚动一次的实际距离，2方法为像素
    :param method:默认1，1为pynput，2为pyautogui
    :return:无
    '''
    if method == 1:
        pynput_mouse.scroll(0, val)  # 第一个参数水平滚动，第二个垂直滚动
    elif method == 2:
        pyautogui.scroll(val)


'''
pyautogui键鼠
'''


def hold_key(key: str, delay=0.05):
    '''
    pyautogui方法
    :param key:
    :param delay:
    :return:
    '''
    pyautogui.keyDown(key)
    if delay != 0:
        time.sleep(delay)


def release_key(key: str, delay=0.05):
    '''
    pyautogui方法
    :param key:
    :param delay:
    :return:
    '''
    pyautogui.keyUp(key)
    if delay != 0:
        time.sleep(delay)


def press_key(key: str, duration=0.05, delay=1.0):
    '''
    pyautogui方法
    :param key:
    :param duration:
    :param delay:
    :return:
    '''
    hold_key(key, duration)
    release_key(key, delay)


def combine_keys(key1: str, key2: str, duration=0.05, delay=1.0):
    '''
    pyautogui方法
    :param key1:
    :param key2:
    :param duration:
    :param delay:
    :return:
    '''
    hold_key(key1, duration)
    hold_key(key2, duration)
    release_key(key2, duration)
    release_key(key1, delay)


def hold_left_mouse(delay=0.05):
    '''
    pyautogui方法
    :param delay:
    :return:
    '''
    pyautogui.mouseDown(button="left")
    if delay != 0:
        time.sleep(delay)


def release_left_mouse(delay=0.05):
    '''
    pyautogui方法
    :param delay:
    :return:
    '''
    pyautogui.mouseUp(button="left")
    if delay != 0:
        time.sleep(delay)


def click_left_mouse(duration=0.05, delay=1.0):
    '''
    pyautogui方法
    :param duration:
    :param delay:
    :return:
    '''
    hold_left_mouse(duration)
    release_left_mouse(delay)


def hold_right_mouse(delay=0.05):
    pyautogui.mouseDown(button="right")
    if delay != 0:
        time.sleep(delay)


def release_right_mouse(delay=0.05):
    pyautogui.mouseUp(button="right")
    if delay != 0:
        time.sleep(delay)


def click_right_mouse(duration=0.05, delay=1.0):
    hold_right_mouse(duration)
    release_right_mouse(delay)


def click(x_or_xy: int, y: int = None, duration=0.05, delay=1.0):
    if isinstance(x_or_xy, (list, tuple)):
        x, y = x_or_xy
    else:
        x, y = x_or_xy, y
    move_mouse(x, y)
    click_left_mouse(duration=duration, delay=delay)


def double_click(x_or_xy: int, y: int = None, duration=0.05, delay=1.0):
    if isinstance(x_or_xy, (list, tuple)):
        x, y = x_or_xy
    else:
        x, y = x_or_xy, y
    move_mouse(x, y)
    click_left_mouse(duration=duration, delay=duration)
    click_left_mouse(duration=duration, delay=delay)


def move_mouse(x_or_xy: int, y: int = None, delay=0.1):
    if isinstance(x_or_xy, (list, tuple)):
        x, y = x_or_xy
    else:
        x, y = x_or_xy, y
    # pyautogui.moveTo(x, y)
    move_mouse_bezier([x, y])
    time.sleep(delay)


def combo_key_mouse(key: str, mouse_button: str, duration=0.05, delay=1.0):
    if mouse_button not in ["left", "right"]:
        raise ValueError("mouse_button must be 'left' or 'right'")
    hold_key(key, delay=duration)
    if mouse_button == "left":
        hold_left_mouse(delay=duration)
        release_left_mouse(delay=duration)
    elif mouse_button == "right":
        hold_right_mouse(delay=duration)
        release_right_mouse(delay=duration)
    release_key(key, delay=delay)


def type_text(text: str, delay=0.5):
    pyautogui.typewrite(text)
    if delay != 0:
        time.sleep(delay)


'''
pynput键鼠
'''


def hold_key_pynput(key, delay=0.05):
    '''
    pynput方法
    :param key: pynput_key_val,单字母按键用字符串
    :param delay:
    :return:
    '''

    pynput_key.press(key)
    time.sleep(delay)


def release_key_pynput(key, delay=0.05):
    '''
    pynput方法
    :param key: pynput_key_val,单字母按键用字符串
    :param delay:
    :return:
    '''
    pynput_key.release(key)
    time.sleep(delay)


def press_key_pynput(key, duration=0.05, delay=1.0):
    '''
    pyautogui方法
    :param key: pynput_key_val,单字母按键用字符串
    :param duration:
    :param delay:
    :return:
    '''
    hold_key_pynput(key, duration)
    release_key_pynput(key, delay)


def combine_keys_pynput(key1, key2, duration=0.05, delay=1.0, random_duration=True):
    '''
    pyautogui方法
    :param key: pynput_key_val,单字母按键用字符串
    :param key: pynput_key_val,单字母按键用字符串
    :param duration:
    :param delay:
    :return:
    '''
    hold_key_pynput(key1, duration)
    hold_key_pynput(key2, duration)
    if random_duration == True:
        time.sleep(random.uniform(duration, duration + 0.02))
    else:
        time.sleep(duration)
    release_key_pynput(key2, duration)
    release_key_pynput(key1, delay)


def hold_left_mouse_pynput(delay=0.05):
    pynput_mouse.press(pynput_button_val.left)
    time.sleep(delay)


def release_left_mouse_pynput(delay=0.05):
    pynput_mouse.release(pynput_button_val.left)
    time.sleep(delay)


def click_left_mouse_pynput(duration=0.05, delay=1.0, random_duration=True):
    hold_left_mouse_pynput(duration)
    if random_duration == True:
        time.sleep(random.uniform(duration, duration + 0.02))
    else:
        time.sleep(duration)
    release_left_mouse_pynput(delay)


def hold_right_mouse_pynput(delay=0.05):
    pynput_mouse.press(pynput_button_val.right)
    time.sleep(delay)


def release_right_mouse_pynput(delay=0.05):
    pynput_mouse.release(pynput_button_val.right)
    time.sleep(delay)


def click_right_mouse_pynput(duration=0.05, delay=1.0, random_duration=True):
    hold_right_mouse_pynput(duration)
    if random_duration == True:
        time.sleep(random.uniform(duration, duration + 0.02))
    else:
        time.sleep(duration)
    release_right_mouse_pynput(delay)


def click_pynput(x_or_xy: int, y: int = None, duration=0.05, delay=1.0, random_duration=True):
    if isinstance(x_or_xy, (list, tuple)):
        x, y = x_or_xy
    else:
        x, y = x_or_xy, y
    move_mouse_pynput(x, y)
    click_left_mouse_pynput(duration=duration, delay=delay, random_duration=random_duration)


def double_click_pynput(x_or_xy: int, y: int = None, duration=0.05, delay=1.0, random_duration=True):
    if isinstance(x_or_xy, (list, tuple)):
        x, y = x_or_xy
    else:
        x, y = x_or_xy, y
    move_mouse_pynput(x, y)
    click_left_mouse_pynput(duration=duration, delay=delay, random_duration=random_duration)
    click_left_mouse_pynput(duration=duration, delay=delay, random_duration=random_duration)


def move_mouse_pynput(x_or_xy: int, y: int = None, delay=0):
    if isinstance(x_or_xy, (list, tuple)):
        x, y = x_or_xy
    else:
        x, y = x_or_xy, y
    # pynput_mouse.position = (x, y)
    move_mouse_bezier([x, y])
    time.sleep(delay)


def combo_key_mouse_pynput(key, mouse_button, duration=0.05, delay=1.0, random_duration=True):
    if mouse_button not in ["left", "right"]:
        raise ValueError("mouse_button must be 'left' or 'right'")
    if random_duration == True:
        duration = random.uniform(duration, duration + 0.02)
    hold_key_pynput(key, delay=duration)
    if mouse_button == "left":
        hold_left_mouse(delay=duration)
        release_left_mouse(delay=duration)
    elif mouse_button == "right":
        hold_right_mouse(delay=duration)
        release_right_mouse(delay=duration)
    release_key(key, delay=delay)


def type_text_pynput(text: str, delay=0.5):
    '''
        使用pynput输入文本
        :param text: 要输入的文本
        :param interval: 每个字符之间的间隔时间，默认0.1秒
        '''
    pyautogui.typewrite(text)
    if delay != 0:
        time.sleep(delay)


def release_all_keys_pynput():
    # 定义所有需要释放的键
    all_keys = [
        pynput_key_val.alt, pynput_key_val.alt_l, pynput_key_val.alt_r, pynput_key_val.backspace,
        pynput_key_val.caps_lock, pynput_key_val.cmd,
        pynput_key_val.cmd_l, pynput_key_val.cmd_r, pynput_key_val.ctrl, pynput_key_val.ctrl_l, pynput_key_val.ctrl_r,
        pynput_key_val.delete,
        pynput_key_val.down, pynput_key_val.end, pynput_key_val.enter, pynput_key_val.esc, pynput_key_val.f1,
        pynput_key_val.f2, pynput_key_val.f3, pynput_key_val.f4,
        pynput_key_val.f5, pynput_key_val.f6, pynput_key_val.f7, pynput_key_val.f8, pynput_key_val.f9,
        pynput_key_val.f10, pynput_key_val.f11, pynput_key_val.f12,
        pynput_key_val.home, pynput_key_val.insert, pynput_key_val.left, pynput_key_val.media_next,
        pynput_key_val.media_play_pause,
        pynput_key_val.media_previous, pynput_key_val.media_volume_down, pynput_key_val.media_volume_mute,
        pynput_key_val.media_volume_up, pynput_key_val.menu, pynput_key_val.num_lock, pynput_key_val.page_down,
        pynput_key_val.page_up,
        pynput_key_val.pause, pynput_key_val.print_screen, pynput_key_val.right, pynput_key_val.scroll_lock,
        pynput_key_val.shift,
        pynput_key_val.shift_l, pynput_key_val.shift_r, pynput_key_val.space, pynput_key_val.tab, pynput_key_val.up
    ]

    # 添加数字键0-9
    all_keys.extend([str(i) for i in range(10)])

    # 添加字母键a-z
    all_keys.extend([chr(i) for i in range(ord('a'), ord('z') + 1)])

    # 释放所有键盘按键
    for key in all_keys:
        try:
            pynput_key.release(key)
        except ValueError:
            pass  # 如果按键未被按下，会抛出ValueError，忽略即可

    # 释放所有鼠标按键
    all_buttons = [pynput_button_val.left, pynput_button_val.right, pynput_button_val.middle,
                   # pynput_button_val.x1,pynput_button_val.x2
                   ]
    for button in all_buttons:
        try:
            pynput_mouse.release(button)
        except ValueError:
            pass  # 如果按键未被按下，会抛出ValueError，忽略即可


'''
贝塞尔
'''


# 使用贝塞尔曲线移动鼠标

def move_mouse_bezier(point):
    bezier = bezierTrajectory()
    start = np.array(pynput_mouse.position)
    end = np.array(point)
    distance = math.sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2)
    number_list = int((distance / 2200) * 150)
    trajectory = bezier.trackArray(list(start), list(end), numberList=max(100, number_list))
    if distance < 200:
        offset_range = int(distance / 10)
        # offset_range = 0
        t = np.random.rand()

        # 计算在 start 和 end 之间的直线上的点
        line_point = start + t * (end - start)

        # 计算方向向量
        direction = end - start

        # 找到垂直于方向向量的两个向量
        if direction[0] != 0 or direction[1] != 0:
            perpendicular1 = np.array([-direction[1], direction[0]])
            perpendicular2 = np.array([direction[1], -direction[0]])
        else:
            perpendicular1 = np.array([1, 0])
            perpendicular2 = np.array([0, 1])

        # 归一化垂直向量
        perpendicular1 = perpendicular1 / np.linalg.norm(perpendicular1)
        perpendicular2 = perpendicular2 / np.linalg.norm(perpendicular2)

        # 随机生成偏移量
        offset1 = (np.random.rand() - 0.5) * 2 * offset_range
        offset2 = (np.random.rand() - 0.5) * 2 * offset_range

        # 计算最终的控制点
        control_point = line_point + offset1 * perpendicular1 + offset2 * perpendicular2
        interpolation_num = max(10, int(distance / 10))
        # print(interpolation_num)
        move_mouse_along_bezier_to_targets([start, control_point, end], interpolation_num=interpolation_num)
    else:
        # print(distance)
        fil = int((1 / ((distance / 2200))))
        # print(fil)
        fil = max(2, fil)

        # 模拟鼠标沿着贝塞尔曲线移动
        move_mouse_along_trajectory(trajectory['trackArray'], fil)


def move_mouse_along_trajectory(trajectory_points, fil: int):
    mouse = pynput_mouse
    for point in trajectory_points[::fil]:
        # mouse.move(int(point[0]), int(point[1]))
        mouse.position = (int(point[0]), int(point[1]))
        # win32api.SetCursorPos((int(point[0]), int(point[1])))
        time.sleep(0.0000001)  # 调整时间间隔以控制移动速度


class bezierTrajectory:

    def _bztsg(self, dataTrajectory):
        lengthOfdata = len(dataTrajectory)

        def staer(x):
            t = ((x - dataTrajectory[0][0]) / (dataTrajectory[-1][0] - dataTrajectory[0][0]))
            y = np.array([0, 0], dtype=np.float64)
            for s in range(len(dataTrajectory)):
                y += dataTrajectory[s] * ((math.factorial(lengthOfdata - 1) / (
                        math.factorial(s) * math.factorial(lengthOfdata - 1 - s))) * math.pow(t, s) * math.pow(
                    (1 - t), lengthOfdata - 1 - s))
            return y[1]

        return staer

    def _type(self, type, x, numberList):
        numberListre = []
        pin = (x[1] - x[0]) / numberList
        if type == 0:
            for i in range(numberList):
                numberListre.append(i * pin)
            if pin >= 0:
                numberListre = numberListre[::-1]
        elif type == 1:
            for i in range(numberList):
                numberListre.append(1 * ((i * pin) ** 2))
            numberListre = numberListre[::-1]
        elif type == 2:
            for i in range(numberList):
                numberListre.append(1 * ((i * pin - x[1]) ** 2))

        elif type == 3:
            dataTrajectory = [np.array([0, 0]), np.array([(x[1] - x[0]) * 0.8, (x[1] - x[0]) * 0.6]),
                              np.array([x[1] - x[0], 0])]
            fun = self._bztsg(dataTrajectory)
            numberListre = [0]
            for i in range(1, numberList):
                numberListre.append(fun(i * pin) + numberListre[-1])
            if pin >= 0:
                numberListre = numberListre[::-1]
        numberListre = np.abs(np.array(numberListre) - max(numberListre))
        biaoNumberList = ((numberListre - numberListre[numberListre.argmin()]) / (
                numberListre[numberListre.argmax()] - numberListre[numberListre.argmin()])) * (x[1] - x[0]) + x[0]
        biaoNumberList[0] = x[0]
        biaoNumberList[-1] = x[1]
        return biaoNumberList

    def getFun(self, s):
        '''

        :param s: 传入P点
        :return: 返回公式
        '''
        dataTrajectory = []
        for i in s:
            dataTrajectory.append(np.array(i))
        return self._bztsg(dataTrajectory)

    def simulation(self, start, end, le=2, deviation=10, bias=0.5):
        '''

        :param start:开始点的坐标 如 start = [0, 0]
        :param end:结束点的坐标 如 end = [100, 100]
        :param le:几阶贝塞尔曲线，越大越复杂 如 le = 4
        :param deviation:轨迹上下波动的范围 如 deviation = 10
        :param bias:波动范围的分布位置 如 bias = 0.5
        :return:返回一个字典equation对应该曲线的方程，P对应贝塞尔曲线的影响点
        '''
        start = np.array(start)
        end = np.array(end)
        cbb = []
        if le != 1:
            e = (1 - bias) / (le - 1)
            cbb = [[bias + e * i, bias + e * (i + 1)] for i in range(le - 1)]

        dataTrajectoryList = [start]

        t = random.choice([-1, 1])
        w = 0
        for i in cbb:
            px1 = start[0] + (end[0] - start[0]) * (random.random() * (i[1] - i[0]) + (i[0]))
            p = np.array([px1, self._bztsg([start, end])(px1) + t * deviation])
            dataTrajectoryList.append(p)
            w += 1
            if w >= 2:
                w = 0
                t = -1 * t

        dataTrajectoryList.append(end)
        return {"equation": self._bztsg(dataTrajectoryList), "P": np.array(dataTrajectoryList)}

    def trackArray(self, start, end, numberList, le=2, deviation=10, bias=0.5, type=3, cbb=0, yhh=10):
        '''

        :param start:开始点的坐标 如 start = [0, 0]
        :param end:结束点的坐标 如 end = [100, 100]
        :param numberList:返回的数组的轨迹点的数量 numberList = 150
        :param le:几阶贝塞尔曲线，越大越复杂 如 le = 4
        :param deviation:轨迹上下波动的范围 如 deviation = 10
        :param bias:波动范围的分布位置 如 bias = 0.5
        :param type:0表示均速滑动，1表示先慢后快，2表示先快后慢，3表示先慢中间快后慢 如 type = 1
        :param cbb:在终点来回摆动的次数
        :param yhh:在终点来回摆动的范围
        :return:返回一个字典trackArray对应轨迹数组，P对应贝塞尔曲线的影响点
        '''
        if start[0] == end[0]:
            start[0] = start[0] + 1
            end[0] = end[0] - 1
        s = []
        fun = self.simulation(start, end, le, deviation, bias)
        w = fun['P']
        fun = fun["equation"]
        if cbb != 0:
            numberListOfcbb = round(numberList * 0.2 / (cbb + 1))
            numberList -= (numberListOfcbb * (cbb + 1))

            xTrackArray = self._type(type, [start[0], end[0]], numberList)
            for i in xTrackArray:
                s.append([i, fun(i)])
            dq = yhh / cbb
            kg = 0
            ends = np.copy(end)
            for i in range(cbb):
                if kg == 0:
                    d = np.array([end[0] + (yhh - dq * i),
                                  ((end[1] - start[1]) / (end[0] - start[0])) * (end[0] + (yhh - dq * i)) + (
                                              end[1] - ((end[1] - start[1]) / (end[0] - start[0])) * end[0])])
                    kg = 1
                else:
                    d = np.array([end[0] - (yhh - dq * i),
                                  ((end[1] - start[1]) / (end[0] - start[0])) * (end[0] - (yhh - dq * i)) + (
                                              end[1] - ((end[1] - start[1]) / (end[0] - start[0])) * end[0])])
                    kg = 0
                # print(d)
                y = self.trackArray(ends, d, numberListOfcbb, le=2, deviation=0, bias=0.5, type=0, cbb=0, yhh=10)
                s += list(y['trackArray'])
                ends = d
            y = self.trackArray(ends, end, numberListOfcbb, le=2, deviation=0, bias=0.5, type=0, cbb=0, yhh=10)
            s += list(y['trackArray'])

        else:
            xTrackArray = self._type(type, [start[0], end[0]], numberList)
            for i in xTrackArray:
                s.append([i, fun(i)])
        return {"trackArray": np.array(s), "P": w}


import numpy as np
from pynput.mouse import Controller
import time


class Bezier:
    def __init__(self, Points, InterpolationNum):
        self.demension = Points.shape[1]
        self.order = Points.shape[0] - 1
        self.num = InterpolationNum
        self.pointsNum = Points.shape[0]
        self.Points = Points

    def getBezierPoints(self, method):
        if method == 0:
            return self.DigitalAlgo()
        if method == 1:
            return self.DeCasteljauAlgo()

    def DigitalAlgo(self):
        PB = np.zeros((self.pointsNum, self.demension))
        pis = []
        for u in np.arange(0, 1 + 1 / self.num, 1 / self.num):
            for i in range(0, self.pointsNum):
                PB[i] = (np.math.factorial(self.order) / (np.math.factorial(i) * np.math.factorial(self.order - i))) * (
                        u ** i) * (1 - u) ** (self.order - i) * self.Points[i]
            pi = sum(PB).tolist()
            pis.append(pi)
        return np.array(pis)

    def DeCasteljauAlgo(self):
        pis = []
        for u in np.arange(0, 1 + 1 / self.num, 1 / self.num):
            Att = self.Points.copy()
            for i in np.arange(0, self.order):
                for j in np.arange(0, self.order - i):
                    Att[j] = (1.0 - u) * Att[j] + u * Att[j + 1]
            pis.append(Att[0].tolist())
        return np.array(pis)


def move_mouse_to_target(target_point):
    mouse = Controller()
    mouse.position = (target_point[0], target_point[1])


def move_mouse_along_bezier_to_targets(target_points, interpolation_num=5, method=0):
    bezier_curve = Bezier(np.array(target_points), interpolation_num)
    bezier_points = bezier_curve.getBezierPoints(method)
    for point in bezier_points:
        move_mouse_to_target(point)
        time.sleep(0.00001)  # Adjust sleep time as needed for smoother movement


# Example usage
if __name__ == "__main__":
    # Define target points
    t = time.time()
    target_points = [[100, 100], [200, 100]]

    # Move mouse along the Bezier curve passing through the target points
    move_mouse_along_bezier_to_targets(target_points)
    print(time.time() - t)

'''
win32
'''


def move_mouse_w32(x_or_xy: int, y: int = None, delay=0.1):
    # print("move mouse w32")
    if isinstance(x_or_xy, (list, tuple)):
        x, y = x_or_xy
    else:
        x, y = x_or_xy, y
    win32api.SetCursorPos((int(x), int(y)))
    time.sleep(delay)
