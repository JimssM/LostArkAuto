#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import multiprocessing
import time

import winsound

from Application.Common.publicFunction import update_log
from Application.Control.configControl import Config
from Application.Control.databaseControl import update_database
from Application.tasks.chaosDungeon import *
from Application.Control.threadControl import *
from Application.tasks.chaosGate import ChaosGate
from Application.tasks.event import *
from Application.tasks.fish import Fish
from Application.tasks.steam_control import SteamControl


def switch_account_control_main():
    while len(gl_info.account_list) > 0:
        acc_line = ((gl_info.account_list[0])).strip()
        process_thr = ThreadControl(func=switch_account_control,
                                    callback=lambda: switch_account_callback(acc_line=acc_line))
        gl_info.thread_main = process_thr  # 主线程
        process_thr.start()
        process_thr.join()


def switch_account_callback(acc_line):  # 控制
    if gl_info.interrupt:
        move_mouse(1919, 0)
        release_all_keys_pynput()
        click(1919, 526)
        SteamControl.close_all()
        if len(gl_info.account_list) > 0:
            gl_info.account_list.pop(0)

        # 日志处理
        gl_info.rest_account_amount -= 1
        gl_info.terminate_account_amount += 1
        # 更新数据库
        gl_info.last_update_time = datetime.datetime.now().strftime("%Y-%m-%d")
        update_database()
        # update_log(acc_line.strip() + gl_info.log)
        update_log(acc_line.strip() + "超时中断")
        gl_info.clear()
    gl_info.interrupt = False


def switch_account_control():
    print("开始滚号")
    print(gl_info.account_list)
    while len(gl_info.account_list) > 0:
        acc_line = ((gl_info.account_list[0])).strip()

        data = acc_line.split('--')
        # if len(data) < 4:
        #     data += [None]  # 如果缺少proxy_id，为其提供一个默认值None
        gl_info.username, gl_info.password, gl_info.region, gl_info.server, gl_info.char_count = data
        gl_info.char_count = int(gl_info.char_count)

        gl_info.thread_main.execution_time = -300  # 重置时间
        # gl_info.thread_main.callback=SteamControl.callback#设置回调函数

        # # test
        # SteamControl.close_all()
        # SteamControl.login_steam()

        SteamControl.start_game()
        select_server()
        if gl_info.if_banned:
            pass
        else:
            # 选角色，进游戏
            ## 若一个角色没有，退出
            if ppocr((269,915,331,939)) == "Create":
                pass
            else:
                # 初始账号设置
                choose_character(six_char_pos[0])
                reset_setting()
                adjust_transparency()
                get_equip_level()
                get_gold_amount()

                # 依次滚号
                # for num in range(int(gl_info.char_count)):
                #     if num != 0:
                #         switch_char_ingame(num)
                # 任务流程
                process_control()

        SteamControl.close_all()
        # gl_info.thread_main.callback()

        if len(gl_info.account_list) > 0:
            gl_info.account_list.pop(0)

        # 日志处理
        tail = ""

        gl_info.rest_account_amount -= 1
        if "进入游戏失败" in gl_info.log:
            gl_info.open_game_failed_amout += 1
        elif "混沌地牢第" in gl_info.log:
            gl_info.terminate_account_amount += 1
        elif gl_info.if_banned:
            gl_info.banned_account_amount += 1
            tail += "封禁"
        else:
            gl_info.finished_account_amount += 1
            tail += "完成"

        # 更新数据库
        gl_info.last_update_time = datetime.datetime.now().strftime("%Y-%m-%d")
        update_database()
        # update_log(acc_line.strip() + gl_info.log)
        update_log(acc_line.strip() + tail)
        gl_info.clear()
    update_log("=======本次运行情况=======")
    update_log(f"剩余账号：{gl_info.rest_account_amount}")
    update_log(f"完成账号：{gl_info.finished_account_amount}")
    update_log(f"封禁：{gl_info.banned_account_amount}")
    update_log(f"中途中断：{gl_info.terminate_account_amount}")
    update_log(f"2次重跑失败：{gl_info.open_game_failed_amout}")
    gl_info.clear_all()


def process_control():
    print("process_control")
    settings = Config(config_path)
    if int(settings.get_value("全局配置", "滚角色")):
        # 不滚号，获取角色数量
        if gl_info.char_count == None:
            try:
                num = int(settings.get_value("全局配置", "角色数量"))
            except:
                update_log("角色数量设置错误")
                gl_info.clear_all()
                return

            gl_info.char_count = num
            print("滚角色模式角色数量：",gl_info.char_count)
        # 滚角色
        for char in range(gl_info.char_count):
            print("角色数量")
            # 家园任务
            if (int(settings.get_value("全局配置", "魔方派遣")) and gl_info.home_cube) or \
                    (int(settings.get_value("全局配置", "加迪恩派遣")) and gl_info.home_guardian) or \
                    (int(settings.get_value("全局配置", "家园种植")) and gl_info.home_farm):
                switch_char_ingame(char)
                home_main()
            for task in gl_info.task_list:  # 滚任务
                gl_info.process = task

                # 只进入游戏
                if int(settings.get_value("全局配置", "只进入游戏")):
                    print("只进入游戏模式")
                    only_enter_game_mode()
                    print("切换账号")
                    time.sleep(3)
                    return

                # 坐车模式
                if int(settings.get_value("全局配置", "坐车模式")):
                    take_bus_mode()
                    print("切换账号")
                    time.sleep(3)
                    return

                leave_home()
                #新活动任务，做完跳过账号
                if int(settings.get_value("全局配置", "新活动任务")):
                    new_event_task()
                    return
                # 每次开启任务前，判断是不是要混沌之门
                if int(settings.get_value("全局配置", "混沌之门")):
                    cg = ChaosGate()
                    if cg.if_chaosgate() and gl_info.chaosGate:
                        gl_info.chaosGate = False
                        cg.main_loop()
                if int(settings.get_value("全局配置", "钓鱼")) and gl_info.fish:
                    gl_info.fish = False
                    gl_info.thread_main.execution_time = 600 - 7200  # 120分钟
                    fish = Fish()
                    fish.fish()

                task_func=None
                task_arg=None
                if task == "混沌地牢2次":
                    cd = ChaosDungeon()
                    task_func = cd.two_daily_chaosDungeon
                    if char != 0:#记录主角色的混沌地牢等级
                        print("无需记录混沌等级")
                        task_arg=False
                    task_max_time = 1500
                elif task == "领取邮件":
                    task_func = go_to_take_mail
                    task_max_time = 600
                elif task=="兑换魔方票":
                    task_func = get_cube_ticket
                    task_max_time = 600
                elif task=="扔蓝紫书和卡片":
                    task_func = remove_trash
                    task_max_time = 600
                elif task=="工会捐献":
                    task_func = sign_in_union
                    task_max_time = 600
                elif task=="邮寄材料":
                    task_func = go_to_mail_material
                    task_max_time = 900

                # 设置终止时间
                gl_info.thread_main.execution_time = 600 - task_max_time
                # 换角色，开始任务
                switch_char_ingame(char)
                print("task list", gl_info.task_list)
                if task_arg!=None:
                    task_func(task_arg)
                else:
                    task_func()

        # 退出游戏前领una token
        # get_unaToken()
        # exit_game()
        # if len(gl_info.task_list)>0:
        #     gl_info.finished_task.append(task)
        # gl_info.log = gl_info.log + ", " + gl_info.process
    print("process 执行完毕")
    if not int(settings.get_value("全局配置", "滚号")):
        gl_info.clear_all()
        update_log("执行完毕")
        winsound.Beep(1000, 400)
