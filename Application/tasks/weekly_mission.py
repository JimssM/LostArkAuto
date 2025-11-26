# import os
# import threading
# import time
#
# import pytz
# import state_machine
#
# from interface.chaosDungeon import ChaosDungeon
# from library.game_action import *
# from library.path_finder import *
# from vars import state
# from library.honing_tools import *
# from vars.record import WEEKDAY
#
# current_path = os.path.dirname(__file__)
#
#
# class ChaosGate:
#     def __init__(self, thread: ThreadManager):
#         self.thread = thread
#
#         self.finder = chaosgate_valley_finder
#         self.darkness_center = [294.0, 270.0]
#         self.valley_center = [295.0, 307.0]
#         self.phantom_center = [320.0, 318.0]
#         self.plague_center = [352.0, 359.0]
#         self.center = None
#
#         self.move_func = None
#         self.cd = ChaosDungeon()
#
#     def main_loop(self):
#         self.thread.execution_timer = -1200  # 30分钟
#
#         # 切换到第一个角色
#         switch_character_2()
#         # 去帕普你卡
#         # 打开地图
#         move_mouse(960, 540)
#         while not if_image_exists(current_path + "/../data/mark/game_action/move_to_triport/map_ui_mark.png"):
#             press_key('m')
#         time.sleep(2)
#         if normal_ocr((262, 126, 516, 165)) == "Punika":  # 在帕普你卡就不去了
#             while if_image_exists(current_path + "/../data/mark/game_action/move_to_triport/map_ui_mark.png"):
#                 press_key('m')
#         else:
#             board_ocean_liner((764, 658))
#
#         # 去星星沙滩
#         move_to_triport([666, 702], [1050, 365], [697, 440])
#         wait_for_trans()
#         clear_interface()
#
#         ride_mount()
#         path = [291.0, 407.0], [307.0, 394.0], [316.0, 379.0], [325.0, 367.0], [345.0, 366.0], [360.0, 363.0], [382.0,
#                                                                                                                 347.0], [
#             375.0, 337.0], [364.0, 311.0], [358.0, 297.0], [330.0, 297.0],
#         punika_starbeach_finder.node_finder(path)
#
#         # 加入混沌之门
#         if not self.join_chaosgate():
#             clear_interface()
#             board_ocean_liner()
#             return  # 没加入直接结束
#
#         self.thread.execution_timer = -600  # 20分钟
#         # 战斗，循环进战场、战斗、判断结束
#         self.move_func()
#         # combine_keys('alt', ',')  # 启动脚本
#         self.finder.move_to_center(self.center, run_time=5)
#         # press_key('pause')  # 暂停
#         while not self._if_end():
#             # 战斗
#             # press_key('pause')  # 暂停
#             self.use_skill()
#             # press_key('pause')
#             if if_die():  # 放技能死
#                 resurrection()
#                 # self.move_func()
#                 self.finder.move_to_center(self.center)
#                 continue
#             self.finder.move_to_center(self.center)
#             if if_die():  # 走路死
#                 resurrection()
#                 # self.move_func()
#                 self.finder.move_to_center(self.center)
#                 continue
#         if if_die():  # 领东西之前不能死
#             resurrection()
#             # self.move_func()
#             self.finder.move_to_center(self.center, run_time=5)
#         # press_key('f11')
#         song_leave_simple()
#         time.sleep(10)  # 把歌唱完
#         wait_for_trans()
#         clear_interface()
#         board_ocean_liner()
#
#     # 判断是否结束战斗
#     def _if_end(self):
#         if normal_ocr((126, 165, 175, 188)) == "Exit":
#             return True
#         return False
#
#     # 跳进战场
#     def _jump_to_battleField(self):
#         wait_for_image(current_path + "/../data/mark/weekly_mission/chaosgate/jump_to_battleField.png")
#         while if_image_exists(current_path + "/../data/mark/weekly_mission/chaosgate/jump_to_battleField.png"):
#             press_key('g')
#         time.sleep(1)
#
#     def use_skill(self):  # 放技能
#         for i in range(8):
#             if if_die():
#                 return
#             # 屏幕中心点坐标
#             center_x, center_y = 960, 533
#
#             # 定义半径
#             radius = 200
#
#             # 生成随机的极坐标角度（弧度制）
#             if (i - 1) % 4 == 1:
#                 theta = random.uniform(0, np.pi / 2)
#             elif (i - 1) % 4 == 2:
#                 theta = random.uniform(np.pi / 2, np.pi)
#             elif (i - 1) % 4 == 3:
#                 theta = random.uniform(np.pi, 3 * np.pi / 2)
#             else:
#                 theta = random.uniform(3 * np.pi / 2, 2 * np.pi)
#
#             # 将极坐标转换为直角坐标
#             random_x = center_x + radius * np.cos(theta)
#             random_y = center_y + radius * np.sin(theta)
#             move_mouse(random_x, random_y,delay=0)
#             self.cd.use_random_skill()
#             # time.sleep(1)
#
#     def _move_in_valley(self):
#         # valley
#         move_mouse(529, 241)
#         click_right_mouse_2()
#         time.sleep(3)
#         move_mouse(330, 207)
#         click_right_mouse_2()
#         time.sleep(5)
#         move_mouse(563, 549)
#         click_right_mouse_2()
#         self._jump_to_battleField()
#
#     def _move_in_plague(self):
#         # plague
#         move_mouse(539, 887)
#         click_right_mouse_2()
#         time.sleep(3)
#         move_mouse(578, 921)
#         click_right_mouse_2()
#         time.sleep(5)
#         move_mouse(74, 673)
#         click_right_mouse_2()
#         time.sleep(4)
#         move_mouse(755, 435)
#         click_right_mouse_2()
#         time.sleep(4)
#         move_mouse(659, 200)
#         click_right_mouse_2()
#         self._jump_to_battleField()
#
#     def _move_in_darkness(self):
#         # darkness
#         move_mouse(943, 41)
#         click_right_mouse_2()
#         time.sleep(4)
#         move_mouse(875, 148)
#         click_right_mouse_2()
#
#         # move_mouse(888,40)
#         # click_right_mouse_2()
#         # time.sleep(3)
#         # press_key('t')
#         # wait_for_image(current_path + "/../data/mark/weekly_mission/chaosgate/jump_to_battleField.png")
#         # press_key('t')
#         self._jump_to_battleField()
#
#     def _move_in_phantom(self):  # 未完成
#         # phantom
#         move_mouse(897, 78)
#         click_right_mouse_2()
#         time.sleep(4)
#         move_mouse(898, 63)
#         click_right_mouse_2()
#         time.sleep(3)
#         move_mouse(951, 422)
#         click_right_mouse_2()
#
#         # move_mouse(923, 146)
#         # click_right_mouse_2()
#         # time.sleep(3)
#         # press_key('t')
#         # wait_for_image(current_path + "/../data/mark/weekly_mission/chaosgate/jump_to_battleField.png")
#         # press_key('t')
#         self._jump_to_battleField()
#
#     # 等待混沌之门出现
#     def join_chaosgate(self):
#         # 打开匹配界面
#         while True:
#             if normal_ocr((895, 169, 968, 194)) == "Chaos":  # 打开了匹配界面
#                 break
#             if if_image_exists(current_path + "/../data/mark/weekly_mission/chaosgate/enter_chaosgate.png"):  # G键进入
#                 press_key('g')
#
#         # 获取地图
#         str = normal_ocr((855, 198, 1062, 222))
#         if "Phantom" in str:
#             self.finder = chaosgate_phantom_finder
#             self.center = self.phantom_center
#             self.move_func = self._move_in_phantom
#         elif "Darkness" in str:
#             self.finder = chaosgate_darkness_finder
#             self.center = self.darkness_center
#             self.move_func = self._move_in_darkness
#         elif "Plague" in str:
#             self.finder = chaosgate_plague_finder
#             self.center = self.plague_center
#             self.move_func = self._move_in_plague
#         elif "Valley" in str:
#             self.finder = chaosgate_valley_finder
#             self.center = self.valley_center
#             self.move_func = self._move_in_valley
#
#         # 等待随机90秒
#         self._wait_random_time()
#
#         # 点击匹配
#         while normal_ocr((895, 169, 968, 194)) == "Chaos":
#             if normal_ocr((976, 809, 1019, 830), det=False) == "Apply":
#                 click(997, 820)
#
#         time.sleep(1)
#         if if_trans():  # 成功匹配
#             wait_for_trans()
#             time.sleep(4)
#             return True
#         else:  # 没匹配到
#             return False
#
#     # 判断是否需要打混沌之门
#     def if_chaosgate(self):  # 判断是否需要打混沌之门
#         """
#         判断是否需要打混沌之门
#         :return: 是否需要打
#         """
#         # 获取当前时间
#         # 获取美国西部的时区对象
#         pacific = pytz.timezone('US/Pacific')
#         # 获取美国东部的时区对象
#         eastern = pytz.timezone('US/Eastern')
#         # 获取当前时间
#         current_time = datetime.datetime.now()
#         # 将当前时间转换为美国西部时间
#         west_time = current_time.astimezone(pacific)
#         # 将当前时间转换为美国东部时间
#         east_time = current_time.astimezone(eastern)
#
#         print("current_time", current_time)
#         print("west_time", west_time)
#         print("east_time", east_time)
#
#         # 根据大区判断
#         if state.CURRENT_REGION == 'w':
#             current_time = west_time
#             print(current_time)
#         elif state.CURRENT_REGION == 'e':
#             current_time = east_time
#
#         weekday = current_time.weekday()  # 星期
#         hour = current_time.hour  # 小时
#         minute = current_time.minute  # 分钟
#
#         # 1490以上才参加
#         if float(state.ITEM_LEVEL) < 1490:
#             return False
#         if minute < 40:#开始时间
#             return False
#         if weekday == 4 or weekday == 1:
#             if hour < 5:
#                 return True
#         elif weekday == 3 or weekday == 5:
#             if hour >= 10:
#                 return True
#         elif weekday == 6 or weekday == 0:
#             if hour >= 10 or hour < 5:
#                 return True
#
#         return False
#
#     # 进入混沌之门前，等待随机时间
#     def _wait_random_time(self):  # 进入混沌之门前，等待随机时间
#         """
#         进入混沌之门前，等待随机时间
#         :return:
#         """
#         # 获取当前时间
#         current_time = datetime.datetime.now()
#
#         # 提取当前时间的分钟和秒
#         minutes = current_time.minute
#         seconds = current_time.second
#
#         # 计算分钟和秒转换为总秒数
#         total_seconds = minutes * 60 + seconds
#
#         random_number = random.randint(1, 90)  # 生成1到90之间的随机整数
#         if random_number - total_seconds > 0:
#             time.sleep(random_number - total_seconds)
#
#
# def task_1():
#     """
#     任务一，救病人
#     :return:
#     """
#     task_bar = (1588, 410, 1908, 488)
#
#     patient_coords = [300.0, 506.0], [338.0, 534.0], [368.0, 531.0], [366.0, 498.0], [365.0, 474.0]
#     npc_coords = [355.0, 422.0]
#     world_map_coord = [900, 707]
#     big_map_coord = [1087, 364]
#     triport_coord = [1008, 476]
#     # reach destination
#     _deselect_all_task()
#     move_to_triport(world_map_coord, big_map_coord, triport_coord)
#     finder = PathFinder(current_path + "/../data/map/task_1.png", resize=2.5)
#     finder.load_node_file(current_path + "/../data/map/task_1_astar.txt")
#     wait_for_trans()
#     clear_interface()
#     # do task
#     set_mount()
#     ride_mount()
#     _accept_task([1294, 353])
#     patient_path = [168.0, 169.0], [178.0, 168.0], [192.0, 162.0], [208.0, 162.0], [219.0, 168.0], [228.0, 178.0], [
#         240.0, 192.0], [247.0, 199.0], [252.0, 204.0], [257.0, 208.0], [264.0, 216.0], [271.0, 223.0], [277.0,
#                                                                                                         228.0], [
#         283.0, 234.0], [289.0, 240.0], [293.0, 245.0], [301.0, 258.0], [310.0, 267.0], [319.0, 282.0], [301.0,
#                                                                                                         308.0], [
#         272.0, 326.0], [256.0, 349.0], [248.0, 374.0], [259.0, 401.0], [278.0, 416.0], [295.0, 435.0], [298.0,
#                                                                                                         460.0], [
#         302.0, 479.0],
#     finder.node_finder(patient_path)
#
#     # save patients
#     counter = 0
#     task_len = len(patient_coords)
#     finished = False
#     while not finished:
#         point = counter % task_len
#         finder.astar_finder(patient_coords[point])
#         press_key('g', delay=3)
#         if find_one_point_color((1610, 427), (131, 172, 71)):
#             finished = True
#         # if screen_match_ccoeff(current_path + "/../data/mark/weekly_mission/task_1/stage_2.png", rect=task_bar):
#         #     finished = True
#         counter = counter + 1
#
#     # finder.astar_finder(npc_coords,
#     #                     quit_img="data/mark/weekly_mission/finish_task_talk/talk_mark.png")
#     finder.astar_finder(npc_coords)
#     _finish_task_talk()
#
#
# def task_2():
#     move_to_triport([1063, 678], [1104, 460], [891, 526])
#     finder = PathFinder(current_path + "/../data/map/task_2_port.png", resize=1.4)
#     wait_for_trans()
#     clear_interface()
#
#     set_mount()  # 添加坐骑
#     ride_mount()
#     _accept_task([1290, 430])
#     # go to bag
#     bag_path = [290.0, 309.0], [290.0, 299.0], [292.0, 286.0], [296.0, 276.0], [310.0, 278.0], [
#         321.0, 282.0], [
#         325.0, 284.0], [332.0, 285.0], [336.0, 287.0], [347.0, 293.0], [357.0, 300.0], [367.0, 310.0], [371.0,
#                                                                                                         333.0], [
#         377.0, 353.0], [387.0, 368.0], [400.0, 378.0], [418.0, 383.0], [444.0, 392.0], [469.0, 399.0], [490.0,
#                                                                                                         404.0], [
#         516.0, 412.0], [536.0, 419.0], [565.0, 432.0], [579.0, 436.0],
#     finder.node_finder(bag_path)
#
#     _move_bag(finder)
#
#     _move_to_room()
#
#
# def task_2_take_mail():
#     move_to_triport([1063, 678], [1104, 460], [891, 526])
#     finder = PathFinder(current_path + "/../data/map/task_2_port.png", resize=1.4)
#     wait_for_trans()
#     clear_interface()
#
#     ride_mount()
#     _accept_task([1290, 430])
#     # take mail
#     mail_path = [290.0, 309.0], [290.0, 299.0], [296.0, 291.0],
#     finder.node_finder(mail_path)
#     take_mail()
#     move_mouse(513, 384)
#     click_right_mouse()
#     # go to bag
#     bag_path = [285.0, 284.0], [296.0, 274.0], [310.0, 278.0], [
#         321.0, 282.0], [
#         325.0, 284.0], [332.0, 285.0], [336.0, 287.0], [347.0, 293.0], [357.0, 300.0], [367.0, 310.0], [371.0,
#                                                                                                         333.0], [
#         377.0, 353.0], [387.0, 368.0], [400.0, 378.0], [418.0, 383.0], [444.0, 392.0], [469.0, 399.0], [490.0,
#                                                                                                         404.0], [
#         516.0, 412.0], [536.0, 419.0], [565.0, 432.0], [579.0, 436.0],
#     finder.node_finder(bag_path)
#
#     _move_bag(finder)
#
#     _move_to_room()
#
#
# def _move_bag(finder: PathFinder):
#     # take bag
#     # take_bag_path = [582.0, 430.0], [594.0, 424.0]
#     # finder.node_finder(take_bag_path)
#     _take_bag()
#     # 有传送就用，没有就老实走
#     open_bifrost()
#     pos = screen_match_with_coordinates_sqdiff(current_path + "/../data/mark/weekly_mission/task_2/bifrost.png")
#     if if_image_exists(current_path + "/../data/mark/weekly_mission/task_2/destination.png") and normal_ocr(
#             (pos[0] + 46, pos[1] + 53, pos[0] + 46 + 88, pos[1] + 53 + 49)) == None:
#         _use_bifrost()
#     else:
#         close_bifrost()
#         # move bag
#         thr = threading.Thread(target=_use_speed_up_skill)
#         thr.start()
#         move_bag_path = [584.0, 430.0], [561.0, 426.0], [529.0, 417.0], [495.0, 407.0], [461.0, 395.0], [427.0,
#                                                                                                          386.0], [
#             395.0,
#             375.0], [
#             379.0, 359.0], [369.0, 333.0], [362.0, 311.0], [354.0, 297.0], [336.0, 287.0], [330.0, 284.0], [323.0,
#                                                                                                             283.0], [
#             317.0, 281.0], [302.0, 275.0], [288.0, 256.0], [285.0, 248.0], [278.0, 236.0], [268.0, 222.0], [259.0,
#                                                                                                             204.0], [
#             255.0, 194.0], [248.0, 188.0],
#         finder.node_finder(move_bag_path, distance_to_target=3)
#         _regist_pos()
#     # drop bag
#     press_key('r', delay=1.5)
#     # talk to npc
#     room_path = [251.0, 189.0], [264.0, 194.0],
#     finder.node_finder(room_path)
#     # time.sleep(0.5)
#
#
# def _move_to_room():
#     move_mouse(1149, 98)
#     click_right_mouse(duration=0)
#     finder = PathFinder(current_path + "/../data/map/task_2_room.png", resize=1.8)
#     wait_for_reached(finder)
#     npc_path = [223.0, 326.0], [237.0, 273.0], [255.0, 219.0], [308.0, 210.0], [340.0, 235.0], [384.0, 243.0],
#     finder.node_finder(npc_path, distance_to_target=8)
#     _finish_task_talk()
#
#
# def _take_bag():
#     while not if_image_exists(current_path + "/../data/mark/weekly_mission/task_2/take_bag_mark.png"):
#         press_key('g', delay=2.5)
#
#
# def _use_speed_up_skill():
#     press_key('e', delay=0)
#     for i in range(2):
#         time.sleep(17)
#         press_key('e', delay=0)
#
#
# def _accept_task(task_coord):
#     while not if_image_exists(current_path + "/../data/mark/game_action/task_ui_mark.png"):
#         combine_keys('alt', 'j')
#     while not if_image_exists(current_path + "/../data/mark/game_action/accept_task/daily_task_mark.png"):
#         click(424, 161, delay=0.5)
#     while not if_image_exists(current_path + "/../data/mark/game_action/accept_task/reputation_quests_mark.png"):
#         click(436, 242, delay=0.1)
#     while if_image_exists(current_path + "/../data/mark/game_action/accept_task/reputation_quests_mark.png"):
#         click(412, 330, delay=0.1)
#     while not if_image_exists(current_path + "/../data/mark/game_action/accept_task/abandon_mark.png"):
#         click(task_coord, delay=2)
#         if if_image_exists(current_path + "/../data/mark/game_action/accept_task/cancel_mark.png"):
#             click(1013, 627, delay=2)
#     while if_image_exists(current_path + "/../data/mark/game_action/accept_task/abandon_mark.png") or \
#             if_image_exists(current_path + "/../data/mark/game_action/accept_task/cancel_mark.png"):
#         if if_image_exists(current_path + "/../data/mark/game_action/accept_task/abandon_mark.png"):
#             click(1856, 118, delay=0.5)
#         elif if_image_exists(current_path + "/../data/mark/game_action/accept_task/cancel_mark.png"):
#             click(1013, 627, delay=2)
#
#
# def _deselect_all_task():
#     move_mouse(960, 540)
#     while not if_image_exists(
#             current_path + "/../data/mark/weekly_mission/deselect_all_task/quests_journal_ui_mark.png"):
#         press_key('j')
#     while if_image_exists(current_path + "/../data/mark/weekly_mission/deselect_all_task/select_quest_mark.png"):
#         click_image(current_path + "/../data/mark/weekly_mission/deselect_all_task/deselect_button_mark.png", delay=0.5)
#     while if_image_exists(current_path + "/../data/mark/weekly_mission/deselect_all_task/quests_journal_ui_mark.png"):
#         press_key('j', delay=0.5)
#
#
# def _finish_task_talk():
#     count = 0
#     while not if_image_exists(current_path + "/../data/mark/weekly_mission/finish_task_talk/talk_mark.png",
#                               threshold=0.01):
#         press_key('g', delay=1)
#         move_mouse(960, 540)
#         count+=1
#         if count > 15:
#             move_mouse(960,540)
#             return
#     # while if_image_exists(current_path + "/../data/mark/weekly_mission/finish_task_talk/talk_mark.png", threshold=0.01):
#     #     combine_keys('shift', 'g', delay=0.1)
#     #     move_mouse(960, 540)
#     #完成任务
#     while not (find_one_point_color((51,1030),(157, 233, 84)) and find_one_point_color((51,1017),(121, 169, 41))):
#         time.sleep(1)
#     while find_one_point_color((51,1030),(157, 233, 84)) and find_one_point_color((51,1017),(121, 169, 41)):
#         combine_keys('shift','g')
#     while if_image_exists(current_path + "/../data/mark/weekly_mission/finish_task_talk/leave_talk_mark.png"):
#         click(1822, 1024, delay=0.1)
#         move_mouse(960, 540)
#
#
# def _regist_pos():
#     open_bifrost()
#     pos = screen_match_with_coordinates_sqdiff(current_path + "/../data/mark/weekly_mission/task_2/bifrost.png")
#     click(pos[0] + 204, pos[1] + 109, delay=0.5)
#     wait_for_image(current_path + "/../data/mark/OK_mark.png", delay=0.5)
#     click_OK()
#     close_bifrost()
#
#
# def _use_bifrost():
#     # open_bifrost()
#     pos = screen_match_with_coordinates_sqdiff(current_path + "/../data/mark/weekly_mission/task_2/bifrost.png")
#     while True:
#         # 找出OK窗口
#         while not if_image_exists(current_path + "/../data/mark/OK_mark.png", threshold=0.02):
#             if normal_ocr((pos[0] + 46, pos[1] + 53, pos[0] + 46 + 88, pos[1] + 53 + 49)) != None:
#                 break
#             click(pos[0] + 204, pos[1] + 75, delay=0.5)
#             # wait_for_image(current_path + "/../data/mark/OK_mark.png", delay=0.5)
#         click_OK()
#         time.sleep(1)
#         wait_for_trans()
#         # if find_one_point_color((1317,399),(127, 156, 165)):
#         if normal_ocr((pos[0] + 46, pos[1] + 53, pos[0] + 46 + 88, pos[1] + 53 + 49)) != None:
#             close_bifrost()
#             break
#
#
# def task_1_2():
#     # 前往anikka
#     board_ocean_liner((1194, 511))
#     # 接任务
#     _accept_task([1287, 354])
#     # 前往上方坐标点(改move_to_triport)
#     move_mouse(960, 540)
#     while not if_image_exists(current_path + "/../data/mark/game_action/move_to_triport/map_ui_mark.png"):
#         press_key('m')
#     while not if_image_exists(current_path + "/../data/mark/OK_mark.png"):
#         click(798, 397, delay=0.1)  # 点击坐标
#         move_mouse(960, 540, delay=1)
#     while if_image_exists(current_path + "/../data/mark/OK_mark.png"):
#         click(905, 551, delay=0.1)  # 点击OK
#         move_mouse(960, 540, delay=1)
#     time.sleep(9)
#     # 5个兔子的路径
#     rabbit_road_1 = [362.0, 349.0], [374.0, 361.0], [389.0, 365.0], [417.0, 334.0], [411.0, 321.0], [383.0, 293.0], [
#         370.0, 280.0], [362.0, 271.0], [353.0, 258.0], [363.0, 238.0], [373.0, 229.0],
#     rabbit_road_2 = [360.0, 243.0], [353.0, 264.0], [362.0, 273.0], [370.0, 281.0], [384.0, 297.0], [402.0, 311.0], [
#         416.0, 330.0], [391.0, 359.0], [362.0, 386.0], [347.0, 396.0], [336.0, 405.0], [325.0, 409.0],
#     rabbit_road_3 = [307.0, 434.0], [276.0, 462.0], [241.0, 485.0], [229.0, 489.0], [218.0, 500.0]
#     rabbit_road_31 = [231.0, 515.0],
#     rabbit_road_4 = [219.0, 506.0], [204.0, 520.0], [210.0, 542.0], [226.0, 565.0],
#     rabbit_road_5 = [219.0, 548.0], [210.0, 527.0], [214.0, 506.0], [221.0, 497.0], [228.0, 488.0], [246.0, 481.0], [
#         271.0, 486.0], [286.0, 508.0], [302.0, 530.0], [316.0, 547.0], [324.0, 563.0], [322.0, 578.0], [328.0, 595.0], [
#         361.0, 588.0],
#
#     finder = PathFinder(current_path + "/../data/map/cangtiangang.jpg", resize=1.4)
#
#     def take_rabbit():  # 摸兔子
#         press_key('g')
#         time.sleep(4)
#         ride_mount()
#
#     # 摸5只兔子
#     ride_mount()
#     finder.node_finder(rabbit_road_1)
#     take_rabbit()
#     finder.node_finder(rabbit_road_2)
#     take_rabbit()
#     finder.node_finder(rabbit_road_3)
#     finder.node_finder(rabbit_road_31, 3)
#     take_rabbit()
#     finder.node_finder(rabbit_road_4)
#     take_rabbit()
#     finder.node_finder(rabbit_road_5)
#     take_rabbit()
#
#     NPC_road = [372.0, 602.0], [390.0, 618.0], [411.0, 618.0], [440.0, 618.0], [463.0, 633.0], [484.0, 647.0], [516.0,
#                                                                                                                 660.0], [
#         534.0, 660.0], [550.0, 659.0], [567.0, 659.0], [578.0, 658.0], [602.0, 665.0], [625.0, 679.0],
#     finder.node_finder(NPC_road)
#     _finish_task_talk()
#     # 回到luttera
#     board_ocean_liner((1048, 655))
#
#
# def only_chaosdungeon(thread: ThreadManager):
#     # 去城市
#     go_to_city()
#     # 准备地牢
#     thread.execution_timer = 0
#     ##买药
#     get_signIn_material()
#     # buy_potion()
#     go_to_mail()
#     go_to_repair()
#     press_key('f8')  # 启动地牢
#     # 给半个小时打地牢
#     thread.execution_timer = 600 - 1500  # 默认超时时间-1800秒
#
#     ##检测结束按键，开始日常
#     def listen(key):
#         if key == pynput.keyboard.Key.f12:
#             return False  # 返回 False 终止监听
#         return True
#
#     # 创建 Listener 对象，设置回调函数
#     listener = pynput.keyboard.Listener(on_press=listen)
#     # 启动监听器
#     listener.start()
#     while listener.is_alive():
#         if if_image_exists(
#                 current_path + "/../data/mark/weekly_mission/switch_char/gamemenu_ui_mark.png") and normal_ocr(
#             (1658, 485, 1721, 506), det=False) == "0/50":
#             for i in range(90):
#                 if not listener.is_alive():
#                     break
#                 time.sleep(1)
#             listener.stop()
#         time.sleep(1)
#
#
# def chaosdungeon_and_daily_task(thread: ThreadManager, potion=True):
#     # 获取角色等级
#     clear_interface()
#     get_item_level()
#     # 去城市
#     go_to_city(use_triport=False)
#     #清背包多的书
#     remove_trash()
#     # 准备混沌之门
#     cg = ChaosGate(thread)
#     cg_state = True  # 是否可以打混沌之门
#
#     # 是否混沌
#     if cg.if_chaosgate() and cg_state:
#         cg_state = False
#         cg.main_loop()
#
#     # 准备地牢
#     thread.execution_timer = 0
#     ##买药
#     get_signIn_material()
#     if potion == True:
#         buy_potion()
#     go_to_mail()
#     go_to_repair()
#     press_key('f8')  # 启动地牢
#     # 给半个小时打地牢
#     thread.execution_timer = 600 - 1800  # 默认超时时间-1800秒
#     cd = ChaosDungeon()
#     cd.two_daily_chaosDungeon(get_chaosDungeon_level=True)
#     # ##检测结束按键，开始日常
#     # def listen(key):
#     #     if key == pynput.keyboard.Key.f12:
#     #         return False  # 返回 False 终止监听
#     #     return True
#     #
#     # # 创建 Listener 对象，设置回调函数
#     # listener = pynput.keyboard.Listener(on_press=listen)
#     # # 启动监听器
#     # listener.start()
#     # trig = True
#     # while listener.is_alive():
#     #     #获得混沌地牢等级
#     #     if normal_ocr((869,120,941,146),det=False)=="Chaos"and trig ==True:
#     #         str = normal_ocr((1259,340,1318,369))
#     #         if str != None:
#     #             database_dic["chaosDungeon_level"]=str
#     #         trig=False
#     #     #卡点
#     #     if if_image_exists(
#     #             current_path + "/../data/mark/weekly_mission/switch_char/gamemenu_ui_mark.png") and normal_ocr(
#     #         (1658, 485, 1721, 506), det=False) == "0/50":
#     #         for i in range(90):
#     #             if not listener.is_alive():
#     #                 break
#     #             time.sleep(1)
#     #         listener.stop()
#     #     time.sleep(1)
#
#     thread.execution_timer = 0
#     # clear_interface_2()  # 清理ui
#     # # song_leave()#退出地牢
#     # song_leave_simple()
#     # time.sleep(10)  # 把歌唱完
#     # wait_for_trans()
#
#     # if WEEKDAY < 2:  # 周一到周三
#     #     exchange_eventShop_reward()  # 兑换奖励
#
#     # 是否混沌
#     if cg.if_chaosgate() and cg_state:
#         cg_state = False
#         cg.main_loop()
#
#     # 日常
#     whitch_char = check_whitch_char()
#     daily_num = 2 - whitch_char
#
#     for i in range(daily_num):
#         thread.execution_timer = 0
#         switch_character_2(i)
#         task_1()
#         task_2()
#         if cg.if_chaosgate() and cg_state:
#             cg_state = False
#             cg.main_loop()
#
#     # ##第一个角色日常
#     # _deselect_all_task()  # 取消选择所有任务
#     # task_1()
#     # task_2()
#     # # task_1_2()
#     # ##如果后面还有角色，继续做
#     # for i in range(daily_num - 1):
#     #     thread.execution_timer = 0
#     #     switch_character(six_char_pos_in_gameMenu[i + 1])
#     #     task_1()
#     #     task_2()
#     #     # task_1_2()
#
#
# if __name__ == "__main__":
#     thr = ThreadManager()
#     # cg = ChaosGate(thr)
#     # cg.use_skill()
#     chaosdungeon_and_daily_task(thr)
