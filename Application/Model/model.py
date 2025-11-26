#!/usr/bin/env python
# -*- coding: UTF-8 -*-
class Custom:
    def __init__(self):
        self.mainView = None
        # 全局变量
        self.account_list = []
        self.rest_account_amount = 0
        self.finished_account_amount = 0
        self.banned_account_amount = 0
        self.terminate_account_amount = 0
        self.open_game_failed_amout = 0
        self.thread_main = None
        self.thread = None
        self.thread_son = None


        #任务
        self.chaosGate = True
        self.fish = True
        self.home_cube = True
        self.home_task_count = 0
        self.home_guardian=True
        self.home_farm = True

        self.interrupt = False#TrehadControl超时

        self.key = None  # 按键监控
        self.hwnd = None
        self.process = "未启动"
        self.task_list = []
        self.finished_task = []
        self.log = "启动脚本"

        self.username = None
        self.password = None
        self.region = None
        self.server = None
        self.equip_level = None
        self.chaosDungeon_level = None
        self.gold = None
        self.last_update_time = None

        self.process_1 = None

        self.if_banned = False
        self.char_count = None
        self.char_number = 1

    def clear(self):
        account_list = self.account_list
        mainView = self.mainView
        rest_account_amount = self.rest_account_amount
        finished_account_amount = self.finished_account_amount
        banned_account_amount = self.banned_account_amount
        terminate_account_amount = self.terminate_account_amount
        open_game_failed_amout = self.open_game_failed_amout
        thread_main = self.thread_main
        thread = self.thread
        thread_son = self.thread_son
        task_list = self.task_list

        self.__init__()
        self.account_list = account_list
        self.mainView = mainView
        self.rest_account_amount = rest_account_amount
        self.finished_account_amount = finished_account_amount
        self.banned_account_amount = banned_account_amount
        self.terminate_account_amount = terminate_account_amount
        self.open_game_failed_amout = open_game_failed_amout
        self.thread_main = thread_main
        self.thread = thread
        self.thread_son = thread_son
        self.task_list = task_list

    def clear_all(self):
        mainView = self.mainView
        self.__init__()
        self.mainView = mainView

def tdi():
    re = []
    for i in range(100):
        re.append(Custom())
    return re


gl_info = Custom()  # 全局数据
td_info = tdi()  # 线程数据
