#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import ctypes
import random
import string
import sys
import shutil
import getpass
import tempfile
import win32event
import win32api
import winerror

from Application.public import static_path

# 检测单个文件锁
def check_single_instance():
    # 创建全局互斥锁
    mutex_name = "Global\\MyXGAUTO"
    mutex = win32event.CreateMutex(None, False, mutex_name)
    if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
        print("程序已经在运行，不能重复启动！")
        sys.exit(1)
    return mutex


# 生成随机进程名
def random_process_name():
    # 生成随机进程名
    process_name = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    if sys.platform == "win32":
        # Windows 平台修改进程名
        ctypes.windll.kernel32.SetConsoleTitleW(process_name)
    elif sys.platform in ["linux", "darwin"]:
        # Linux/Unix 平台修改进程名
        libc = ctypes.CDLL('libc.so.6')
        libc.prctl(15, process_name.encode('utf-8'), 0, 0, 0)
    return process_name

def copy_ppocr_file(source_directory):
    # 获取当前用户名
    current_user = getpass.getuser()

    # 目标目录
    destination_directory = os.path.join("C:\\Users", current_user,".paddleocr")
    # 如果目标目录存在，则先删除
    if os.path.exists(destination_directory):
        shutil.rmtree(destination_directory)
        print(f"Deleted existing directory {destination_directory}")

    # 检查目标目录是否存在，如果不存在则创建
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # 遍历源目录中的所有文件并进行复制
    for item in os.listdir(source_directory):
        source_item = os.path.join(source_directory, item)
        destination_item = os.path.join(destination_directory, item)

        if os.path.isfile(source_item):
            shutil.copy2(source_item, destination_item)
            print(f"Copied {source_item} to {destination_item}")
        elif os.path.isdir(source_item):
            shutil.copytree(source_item, destination_item)
            print(f"Copied directory {source_item} to {destination_item}")

def create_token_file(source_directory):
    # 获取当前用户名
    current_user = getpass.getuser()

    # 目标目录
    destination_directory = os.path.join("C:\\Users", current_user)

    # 目录存在则返回
    if os.path.exists(os.path.join(destination_directory, "xgfz_token.ini")):
        return

    # 遍历源目录中的所有文件并进行复制
    for item in os.listdir(source_directory):
        source_item = os.path.join(source_directory, item)
        destination_item = os.path.join(destination_directory, item)

        if os.path.isfile(source_item):
            shutil.copy2(source_item, destination_item)
            print(f"Copied {source_item} to {destination_item}")
        elif os.path.isdir(source_item):
            shutil.copytree(source_item, destination_item)
            print(f"Copied directory {source_item} to {destination_item}")
