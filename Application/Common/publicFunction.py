#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os.path
import sqlite3
import time

from Application.Model.model import gl_info, td_info
from Application.Common.SignalUnit import signal
from Application.public import log_dir, log_path, database_path
import os
import zipfile
import shutil
import atexit

def get_task_list():
    task_list = []
    count = gl_info.mainView.listWidget_yixuanrenwu.count()
    for i in range(count):
        text = gl_info.mainView.listWidget_yixuanrenwu.item(i).text()
        task_list.append(text)
    return task_list


def update_log(content: object) -> object:
    now_time = time.localtime(time.time())
    now_time = time.strftime("%H:%M:%S", now_time)
    signal.log.emit(f"{now_time}:{content}")
    # 写入日志
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    with open(log_path, "a+", encoding="utf-8") as fp:
        fp.write(f"{now_time}:{content}\n")


def update_finish_log():
    update_log("=======本次运行情况=======")
    update_log(f"剩余账号：{gl_info.rest_account_amount}")
    update_log(f"完成账号：{gl_info.finished_account_amount}")
    update_log(f"封禁：{gl_info.banned_account_amount}")
    update_log(f"中途中断：{gl_info.terminate_account_amount}")
    update_log(f"进入游戏失败：{gl_info.open_game_failed_amout}")


# 更新连接到的机器信息
def update_table(row, col, content, table_id,row_count):  # 0 machine,1 info
    signal.table.emit(row, col, str(content), table_id,row_count)


def shutdown_client_pc():
    tri = True
    while True:
        if gl_info.process == "跑完关机":
            print("test")
            break
        if tri ==False:
            break
        time.sleep(1)
        if gl_info.process == "未启动":
            for i in range(100):
                if td_info[i].process != "未启动":
                    break
                if i == 99 and td_info[i].process == "未启动":
                    gl_info.process = "跑完关机"
                    tri=False
                    break
    tri = True

    while True:
        if tri ==False:
            break
        time.sleep(1)
        for i in range(100):
            if td_info[i].thread_ID != None:
                print("iD",i,td_info[i].thread_ID)
                break
            if i == 99 and td_info[i].thread_ID == None:
                gl_info.process = "未启动"
                tri = False
                update_log("全部关闭")

                break


# '''
# 处理资源图片
# '''
# def unzip_file(zip_path, extract_to):
#     """解压zip文件到指定目录"""
#     with zipfile.ZipFile(zip_path, 'r') as zip_ref:
#         zip_ref.extractall(extract_to)
#     print(f'文件已解压到 {extract_to}')
#
# def cleanup():
#     """删除解压出来的文件和目录"""
#     if os.path.exists(extract_dir):
#         shutil.rmtree(extract_dir)
#         print(f'{extract_dir} 已被删除')
#
# zip_path = 'img.zip'
#     unzip_file(zip_path, extract_dir)

if __name__ == "__main__":
    t = time.time()
    data = "22,password,region,server,fffff,2,gold,last_update_time"
    # data = "22,password,region,server,fffff,3,gold,last_update_time"
    # update_database(data)
    print(time.time() - t)
