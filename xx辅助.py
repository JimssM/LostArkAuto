#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import time


from Application.Control.fileControl import *

random_process_name()
mutex = check_single_instance()
copy_ppocr_file(static_path + ".paddleocr")
create_token_file(static_path + "xgfz_token")

from PyQt5.QtGui import QIcon

if sys.platform == "win32":
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("7777")

from PyQt5.QtWidgets import QApplication, QMessageBox
from Application.Control.mainControl import MainController
from Application.public import ui_path, static_path
from Application.tools import is_process_running, count_processes_by_name

if __name__ == '__main__':
    def clean_up():
        print("清理资源")
        win32api.CloseHandle(mutex)

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(ui_path + "watermelon.ico"))
    main_ui = MainController()

    app.aboutToQuit.connect(clean_up)  # 绑定退出信号
    print("移动文件夹中")
    sys.exit(app.exec_())