#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os.path
import sqlite3
import subprocess
import threading

import keyboard
import requests
import winsound
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox

from Application.Common.processControl import process_control, switch_account_control, switch_account_control_main
from Application.Control.threadControl import ThreadControl
from Application.Model.model import gl_info
from Application.View.mainView import MainView
from Application.Common.SignalUnit import signal

from Application.Control.configControl import Config
from Application.Common.publicFunction import get_task_list, update_log, update_table, shutdown_client_pc
from Application.public import *


class MainController:
    def __init__(self):
        self.ini = config_path

        self.mainView = MainView()
        self.event_init()
        self.load_setting()
        self.load_account()

        refresh_machine_table_thr = threading.Thread(target=self.refresh_machine_table, daemon=True)
        refresh_machine_table_thr.start()

        refresh_info_table_thr = threading.Thread(target=self.refresh_info_table, daemon=True)
        refresh_info_table_thr.start()

        # 更新数据库
        refresh_database_table_thr = threading.Thread(target=self.refresh_acc_state_table, daemon=True)
        refresh_database_table_thr.start()

        keyboard.add_hotkey('f11', self.f11_hotkey)
        keyboard.add_hotkey('f8', self.f8_hotkey)

        gl_info.mainView = self.mainView
        self.mainView.show()
        # open_app_verify()

    def event_init(self):
        # 事件
        self.mainView.pushButton_allAdd.clicked.connect(lambda: self.task_select("allAdd"))
        self.mainView.pushButton_add.clicked.connect(lambda: self.task_select("add"))
        self.mainView.pushButton_del.clicked.connect(lambda: self.task_select("del"))
        self.mainView.pushButton_delAll.clicked.connect(lambda: self.task_select("delAll"))
        self.mainView.pushButton_up.clicked.connect(lambda: self.task_select("up"))
        self.mainView.pushButton_down.clicked.connect(lambda: self.task_select("down"))
        self.mainView.pushButton_saveConfig.clicked.connect(self.saveConfig)
        self.mainView.pushButton_start.clicked.connect(self.start)
        self.mainView.pushButton_stop.clicked.connect(self.stop)

        self.mainView.pushButton_open_source_file.clicked.connect(self.open_source_file)
        self.mainView.pushButton_open_account_file.clicked.connect(self.open_account_file)

        settings = Config(config_path)
        # checkbox
        # 创建多个QCheckBox
        self.checkboxes = {
            "滚号": self.mainView.checkBox_gunhao,
            "滚角色": self.mainView.checkBox_gunjuese,
            "混沌之门": self.mainView.checkBox_chaosGate,
            "钓鱼": self.mainView.checkBox_fish,
            "不分解古代": self.mainView.checkBox_noAncient,
            "工会银币捐献": self.mainView.checkBox_unionSilverDonation,
            "只进入游戏": self.mainView.checkBox_onlyEnterGame,
            "坐车模式": self.mainView.checkBox_takeBusMode,
            "魔方派遣": self.mainView.checkBox_cube,
            "加迪恩派遣": self.mainView.checkBox_guardian,
            "家园种植": self.mainView.checkBox_homeFarm,
            "新活动任务": self.mainView.checkBox_newEventTask,
            "宝石": self.mainView.checkBox_gem,
            "鱼": self.mainView.checkBox_fishMat,
            "混沌之门材料": self.mainView.checkBox_chaosGateMat,
        }

        for key, checkbox in self.checkboxes.items():
            checkbox.setChecked(int(settings.get_value("全局配置", key)))
            checkbox.stateChanged.connect(lambda state, k=key: self.update_config(k, state))

        # 第二页
        self.mainView.search_btn.clicked.connect((self.search_in_acc_state))

        # 表头排序功能
        self.mainView.acc_state_table.horizontalHeader().sectionClicked.connect(self.sortTable)

        # 信号
        signal.table.connect(self.display_table)
        signal.log.connect(self.display_log)

    def task_select(self, flag):
        if flag == "allAdd":
            self.mainView.listWidget_yixuanrenwu.clear()
            count = self.mainView.listWidget_daixuanrenwu.count()
            for i in range(count):
                text = self.mainView.listWidget_daixuanrenwu.item(i).text()
                self.mainView.listWidget_yixuanrenwu.addItem(text)

        elif flag == "add":
            now_row = self.mainView.listWidget_daixuanrenwu.currentRow()
            if now_row > -1:
                text = self.mainView.listWidget_daixuanrenwu.item(now_row).text()
                if text not in get_task_list():
                    self.mainView.listWidget_yixuanrenwu.addItem(text)


        elif flag == "del":
            now_row = self.mainView.listWidget_yixuanrenwu.currentRow()
            if now_row > -1:
                self.mainView.listWidget_yixuanrenwu.takeItem(now_row)
        elif flag == "delAll":
            self.mainView.listWidget_yixuanrenwu.clear()
        elif flag == "up":
            now_row = self.mainView.listWidget_yixuanrenwu.currentRow()
            if now_row > 0:
                one_text = self.mainView.listWidget_yixuanrenwu.item(now_row - 1).text()
                two_text = self.mainView.listWidget_yixuanrenwu.item(now_row).text()
                self.mainView.listWidget_yixuanrenwu.item(now_row - 1).setText(two_text)
                self.mainView.listWidget_yixuanrenwu.item(now_row).setText(one_text)
                self.mainView.listWidget_yixuanrenwu.setCurrentRow(now_row - 1)

        elif flag == "down":
            now_row = self.mainView.listWidget_yixuanrenwu.currentRow()
            count = self.mainView.listWidget_yixuanrenwu.count()
            if now_row < count - 1:
                one_text = self.mainView.listWidget_yixuanrenwu.item(now_row).text()
                two_text = self.mainView.listWidget_yixuanrenwu.item(now_row + 1).text()
                self.mainView.listWidget_yixuanrenwu.item(now_row).setText(two_text)
                self.mainView.listWidget_yixuanrenwu.item(now_row + 1).setText(one_text)
                self.mainView.listWidget_yixuanrenwu.setCurrentRow(now_row + 1)

    def start(self):
        # 判断是否可以开始
        # 判断是否有任务运行中
        if gl_info.process != "未启动":
            update_log("运行中，请勿操作")
            return
        # 判断任务
        task = get_task_list()
        if len(task) == 0:
            update_log("未选择任务")
            return
        # 加载账户
        gl_info.clear_all()
        self.load_account()
        if len(gl_info.account_list) == 0:
            update_log("账号为0，请放入账号")
            return

        winsound.Beep(800, 400)

        # 执行任务
        update_log(f"开始: {task}")
        gl_info.task_list = task
        gl_info.process = str(task[0])

        settings = Config(config_path)
        if int(settings.get_value("全局配置", "滚号")):
            process = switch_account_control_main
            process_thr = threading.Thread(target=process)
            gl_info.thread = process_thr  # 父线程
            process_thr.start()

        else:
            process = process_control
            process_thr = ThreadControl(func=process)
            gl_info.thread_main = process_thr
            process_thr.start()

    def stop(self):
        if gl_info.thread_main is not None:
            update_log("正在停止")
            gl_info.thread_main.stop()
        else:
            update_log("已全部停止")
        gl_info.clear_all()
        winsound.Beep(1000, 500)

    def f11_hotkey(self):
        self.mainView.pushButton_stop.click()

    def f8_hotkey(self):
        self.mainView.pushButton_start.click()

    def open_source_file(self):
        # subprocess.Popen(['start', '', static_path], shell=True)
        os.startfile(log_dir)

    def saveConfig(self):  # 保存配置
        settings = Config(config_path)
        # lineEdit内容
        steam_path = self.mainView.lineEdit_steamPath.text()
        char_num = self.mainView.lineEdit_steamPath_charNum.text()
        receive_mail_char_name = self.mainView.lineEdit_receiveMailCharName.text()
        settings.set("全局配置", "Steam路径", steam_path)
        settings.set("全局配置", "角色数量", char_num)
        settings.set("全局配置", "收件角色名称", receive_mail_char_name)

        settings.write()

        update_log("保存配置成功")

    def open_account_file(self):
        subprocess.Popen(['start', '', account_path], shell=True)

    def search_in_acc_state(self):
        search_text = self.mainView.lineEdit_search.text()
        self.mainView.acc_state_table.clearSelection()
        found = False

        # 记录第一次找到的项的行列索引
        first_found_row = -1
        first_found_column = -1

        # 遍历表格查找内容
        for row in range(self.mainView.acc_state_table.rowCount()):
            for column in range(self.mainView.acc_state_table.columnCount()):
                item = self.mainView.acc_state_table.item(row, column)
                if item and search_text.lower() in item.text().lower():
                    if not found:
                        # 如果是第一次找到匹配项，记录其位置
                        first_found_row = row
                        first_found_column = column
                    # item.setBackground(Qt.yellow)
                    item.setSelected(True)
                    found = True
                    # # 找到第一个匹配项后，退出循环
                    # break

        if found:
            # 调整窗口到第一个匹配项的位置
            self.mainView.acc_state_table.scrollToItem(
                self.mainView.acc_state_table.item(first_found_row, first_found_column))
        else:
            QMessageBox.information(self.mainView, "查找结果", "未找到匹配项")

    def load_setting(self):
        if not os.path.exists(self.ini):
            update_log("配置文件不存在")
        update_log("加载配置")
        secion = "全局配置"

        settings = Config(config_path)
        # 更新界面
        self.mainView.lineEdit_steamPath.setText(settings.get_value(secion, "Steam路径"))
        self.mainView.lineEdit_steamPath_charNum.setText(settings.get_value(secion, "角色数量"))
        self.mainView.lineEdit_receiveMailCharName.setText(settings.get_value(secion, "收件角色名称"))

    def update_config(self, key, state):
        settings = Config(config_path)
        print(state)
        settings.set("全局配置", key, str(state))
        settings.write()

    # 加载账户
    def load_account(self):
        gl_info.account_list = []
        i = 0
        with open(account_path, 'r') as fp:
            for line in fp:
                fp = line.strip()
                if line:
                    gl_info.account_list.append(line)
                    i = i + 1
        gl_info.rest_account_amount = i
        gl_info.finished_account_amount = 0
        gl_info.banned_account_amount = 0
        gl_info.terminate_account_amount = 0
        gl_info.open_game_failed_amout = 0

        update_log(f"加载账户{i}个")

        # self.mainView.tableWidget.clearContents()
        # self.mainView.tableWidget.setRowCount(1)
        # update_table(0, "未知线程")
        # update_table(1, "未启动")

    # 日志显示
    def display_log(self, content):
        self.mainView.textBrowser_log.append(str(content))
        self.mainView.textBrowser_log.ensureCursorVisible()

    # 机器表格更新
    def display_table(self, row, col, content, table_id, row_count):

        if table_id == 0:  # machine
            Item = QTableWidgetItem(content)
            if self.mainView.tableWidget.rowCount != row_count:
                self.mainView.tableWidget.setRowCount(row_count)
            self.mainView.tableWidget.setItem(row, col, Item)
            Item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        elif table_id == 1:  # info
            Item = QTableWidgetItem(content)
            if self.mainView.tableWidget_info.rowCount != row_count:
                self.mainView.tableWidget_info.setRowCount(row_count)
            self.mainView.tableWidget_info.setItem(row, col, Item)
            Item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        elif table_id == 2:  # state
            if col == 6 and content != "None":  # 金币列
                # 创建一个 QTableWidgetItem 对象，使用 setData 方法传入整数
                Item = QTableWidgetItem()
                Item.setData(Qt.DisplayRole, float(content))
            elif col == 4 and content != "None":  # 装备等级列
                # 创建一个 QTableWidgetItem 对象，使用 setData 方法传入整数
                Item = QTableWidgetItem()
                try:
                    Item.setData(Qt.DisplayRole, float(content))
                except:
                    Item.setData(Qt.DisplayRole, float(0))
            elif col == 5 and content != "None":  # 混沌等级列
                # 创建一个 QTableWidgetItem 对象，使用 setData 方法传入整数
                Item = QTableWidgetItem()
                Item.setData(Qt.DisplayRole, float(content))
            else:
                Item = QTableWidgetItem(content)
            if self.mainView.acc_state_table.rowCount != row_count:
                self.mainView.acc_state_table.setRowCount(row_count)
            self.mainView.acc_state_table.setItem(row, col, Item)
            Item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def refresh_machine_table(self):
        while True:
            time.sleep(1)
            update_table(0, 0, gl_info.process, 0, 1)

    def refresh_info_table(self):
        while True:
            time.sleep(1)
            update_table(0, 0, gl_info.rest_account_amount, 1, 5)
            update_table(0, 1, gl_info.finished_account_amount, 1, 5)
            update_table(0, 2, gl_info.banned_account_amount, 1, 5)
            update_table(0, 3, gl_info.terminate_account_amount, 1, 5)
            update_table(0, 4, gl_info.open_game_failed_amout, 1, 5)

    def refresh_acc_state_table(self):
        # 连接到数据库
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        while True:

            sql = '''select * from acc_state'''
            cursor.execute(sql)
            result = cursor.fetchall()

            num_rows = len(result)
            # self.mainView.acc_state_table.setRowCount(num_rows)

            for row_number, row_data in enumerate(result):
                for column_number, data in enumerate(row_data):
                    update_table(row_number, column_number, data, 2, num_rows)
                    # self.mainView.acc_state_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            time.sleep(300)

    def sortTable(self, logicalIndex):
        currentOrder = self.mainView.acc_state_table.horizontalHeader().sortIndicatorOrder()
        if currentOrder == Qt.AscendingOrder:
            self.mainView.acc_state_table.sortItems(logicalIndex, Qt.AscendingOrder)
        elif currentOrder == Qt.DescendingOrder:
            self.mainView.acc_state_table.sortItems(logicalIndex, Qt.DescendingOrder)
