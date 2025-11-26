#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import random
import string

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QMessageBox, QHeaderView, QPushButton, QDialog, QLabel, QVBoxLayout

from Application.Common.publicFunction import update_log
from Application.Model.model import gl_info
from Application.public import ui_path
from Application.ui.untitled import Ui_Form
from Application.ui.style_sheet import *


class MainView(Ui_Form, QWidget):
    def __init__(self):
        super(MainView, self).__init__()
        self.setupUi(self)
        self.ui_init()

    def ui_init(self):
        """ ui自定义样式 """
        # 客户机信息界面：第0行和标题加横杠--
        self.tableWidget.horizontalHeader().setStyleSheet(
            "border-bottom-width: 0.5px;border-style: outset;border-color: rgb(229,229,229);"
        )
        # self.tableWidget.verticalHeader().hide()  # 隐藏左侧序号

        self.tableWidget_info.setColumnCount(1)
        self.tableWidget_info.horizontalHeader().hide()

        # 设置标题
        title_length = 10  # 标题长度
        characters = string.ascii_letters + string.digits  # 包含字母和数字的字符集
        title = ''.join(random.choice(characters) for _ in range(title_length))
        self.setWindowTitle(title)

        # table设置自动调整宽度
        header = self.acc_state_table.horizontalHeader()
        # header.setSectionResizeMode(QHeaderView.ResizeToContents)#根据内容改变宽度
        header.setSectionResizeMode(QHeaderView.Stretch)  # 自动填充

    # 错误告警框
    def show_message(self, title, content):
        update_log(content)
        # msg_box = QMessageBox(self)
        # # msg_box.setIcon(QMessageBox.Question)
        # msg_box.setText(content)
        # msg_box.setWindowTitle(title)
        # msg_box.setStandardButtons(QMessageBox.Yes)
        #
        # # 获取标准按钮对象
        # yes_button = msg_box.button(QMessageBox.Yes)
        # yes_button.setText("确认")
        #
        # # 设置样式表
        # msg_box.setStyleSheet("""
        #             QMessageBox {
        #                 font-size: 14px; /* 消息框字体大小 */
        #             }
        #
        #             QPushButton {
        #                 min-width: 40px; /* 按钮最小宽度 */
        #                 min-height: 30px; /* 按钮最小高度 */
        #                 font-size: 14px; /* 按钮字体大小 */
        #             }
        #         """)
        #
        # # 单独设置 "Yes" 按钮的样式
        # yes_button.setStyleSheet(style_sheet_close_button)
        #
        # self.setWindowIcon((QIcon(ui_path+"watermelon.ico")))
        # msg_box.exec_()

    def closeEvent(self, event):
        msg_box = QMessageBox(self)
        # msg_box.setIcon(QMessageBox.Question)
        msg_box.setText("确认退出吗？")
        msg_box.setWindowTitle("确认")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        # 获取标准按钮对象
        yes_button = msg_box.button(QMessageBox.Yes)
        no_button = msg_box.button(QMessageBox.No)
        yes_button.setText("确认")
        no_button.setText("取消")

        # 设置样式表
        msg_box.setStyleSheet("""
                    QMessageBox {
                        font-size: 14px; /* 消息框字体大小 */
                    }
                    QPushButton {
                        min-width: 40px; /* 按钮最小宽度 */
                        min-height: 30px; /* 按钮最小高度 */
                        font-size: 14px; /* 按钮字体大小 */
                    }
                """)

        # 单独设置 "Yes" 按钮的样式
        yes_button.setStyleSheet(style_sheet_close_button)

        # 单独设置 "No" 按钮的样式
        no_button.setStyleSheet(style_sheet_close_button)
        # 显示消息框并获取用户响应
        response = msg_box.exec_()

        if response == QMessageBox.Yes:
            # 如果用户点击了“是”，则接受关闭事件
            if gl_info.thread_main != None:
                print("关闭应用")
                gl_info.thread_main.stop()
            gl_info.clear_all()
            event.accept()
            # gl_info.database_conn.close()#关闭数据库
        else:
            print("User clicked No")
            event.ignore()


