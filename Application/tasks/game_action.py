import re
import time

from Application.Control.configControl import Config
from Application.tools import *
from Application.public import *
from Application.Model.model import *
from Application.tools.file_tools import get_all_files_name


def click_OK(threshold=0.05, delay=1):
    click_image(img_path + "OK_mark.png", threshold=threshold, delay=delay)


def select_server():
    move_mouse(0, 0)
    time.sleep(1)
    while True:
        # set_window_top(find_window_handle("EFLaunchUnrealUWindowsClient", None))  # 置顶游戏窗口
        if ppocr((586, 366, 712, 410)) == "GAME":
            click(963, 679)
            move_mouse(0, 0, delay=1)
        elif ppocr((913, 866, 1009, 902)) == "Accept":
            click(968, 881)
            move_mouse(0, 0, delay=1)
        # 切换到欧服
        if gl_info.region == 'c' and not match_point((702, 535), (242, 233, 167)) and "Select Server" in \
                ppocr((888, 444, 1025, 469)):
            while not if_image_exists(img_path + "OK_mark.png"):
                if match_point((702, 535), (242, 233, 167)):
                    break
                click(702, 535, delay=0.2)
                move_mouse(0, 0, delay=1)
            while if_image_exists(img_path + "OK_mark.png"):
                click_OK(delay=0.2)
                move_mouse(0, 0, delay=3)
        # 切换到美西
        if gl_info.region == 'w' and not match_point((874, 537), (243, 241, 200)) and "Select Server" in \
                ppocr((888, 444, 1025, 469)):
            while not if_image_exists(img_path + "OK_mark.png"):
                if match_point((874, 537), (243, 241, 200)):
                    break
                click(874, 537, delay=0.2)
                move_mouse(0, 0, delay=1)
            while if_image_exists(img_path + "OK_mark.png"):
                click_OK(delay=0.2)
                move_mouse(0, 0, delay=3)
        # 切换到美东
        elif gl_info.region == 'e' and not match_point((1045, 537), (243, 241, 200)) and "Select Server" in \
                ppocr((888, 444, 1025, 469)):
            while not if_image_exists(img_path + "OK_mark.png"):
                if match_point((1045, 537), (243, 241, 200)):
                    break
                # click_image(current_path + "/../data/mark/app_manager/select_server/east_mark.png", delay=0.2)
                click(1045, 537, delay=0.2)
                move_mouse(0, 0, delay=1)
            while if_image_exists(img_path + "OK_mark.png"):
                click_OK(delay=0.2)
                move_mouse(0, 0, delay=3)

        # 进入对应服务器，只支持第一个
        if gl_info.region == 'w' and match_point((874, 537), (243, 241, 200)) and "Select Server" in \
                ppocr((888, 444, 1025, 469)):
            break
        elif gl_info.region == 'e' and match_point((1045, 537), (243, 241, 200)) and "Select Server" in \
                ppocr((888, 444, 1025, 469)):
            break
        elif gl_info.region == 'c' and match_point((702, 535), (242, 233, 167)) and "Select Server" in \
                ppocr((888, 444, 1025, 469)):
            break

        # 被封
        if if_image_exists(img_path + "banned_mark.png"):
            gl_info.log = gl_info.log + ", " + "封禁"
            gl_info.if_banned = True
            return

        # OK错误
        pos = find_img_low_threshold(img_path + "OK_mark.png")
        if pos != [0, 0]:
            # 如果出现OK是因为被封号
            if if_image_exists(img_path + "banned_mark.png"):
                gl_info.log = gl_info.log + ", " + "封禁"
                gl_info.if_banned = True
                return
            # 如果是错误弹窗
            else:
                click_OK(delay=0.5)

    # 等待进入游戏
    # wait_for_image(current_path + "/../data/mark/app_manager/select_server/enter_mark.png")
    while True:
        if ppocr((933, 913, 982, 934)) == "Enter":
            break
    # OK错误
    click_OK(delay=0.5)

    # 选择服务器
    # 四个服务器识别区域
    r1 = (751, 582, 885, 615)
    r2 = (751, 618, 885, 651)
    r3 = (751, 654, 885, 689)
    r4 = (751, 694, 885, 724)

    rlist = []
    rlist.append(r1)
    rlist.append(r2)
    rlist.append(r3)
    rlist.append(r4)

    for r in rlist:
        if ppocr(r, det=True) == gl_info.server:
            pos = ((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)  # 计算点击坐标
            click(pos)
            click(pos)
            break
    # 进入角色选择
    while ppocr((933, 913, 982, 934)) == "Enter":
        click(959, 926)
        move_mouse(0, 0, delay=3)
    while ppocr((365, 12, 431, 42)) != "Event":
        time.sleep(1)
    # 清理弹窗
    time.sleep(2)
    while match_point((385, 27), (84, 95, 103)) and ppocr((365, 12, 431, 42)) == "Event":
        press_key('esc', delay=4)


def choose_character(char_coord):
    click(char_coord)
    # wait_for_image(current_path + "/../data/mark/game_action/launch.png")
    while True:
        if ppocr((365, 12, 431, 42)) == "Event":
            break
    # while if_image_exists(current_path + "/../data/mark/game_action/launch.png"):
    while ppocr((365, 12, 431, 42)) == "Event":
        click(char_coord)
        # click_image(current_path + "/../data/mark/game_action/launch.png")
        click(912, 1013)
        move_mouse(960, 540)
        time.sleep(10)
    while if_trans():
        time.sleep(1)


def if_trans(threshold=0.05):
    '''

    :param threshold:
    :return: true为在传送《false为没有传送
    '''
    template_path_1 = img_path + "if_trans_mark.png"
    template_path_2 = img_path + "if_trans_mark_roster.png"
    template_path_3 = img_path + "home_mark.png"
    return not (rect_match_sqdiff(template_path_1, threshold) or
                rect_match_sqdiff(template_path_2, threshold) or
                rect_match_sqdiff(template_path_3, threshold))


def whitch_area(threshold=0.05):
    '''
    0为都不是，1为正常地方，2为家园
    :param threshold:
    :return:
    '''
    template_path_1 = img_path + "if_trans_mark.png"
    template_path_2 = img_path + "if_trans_mark_roster.png"
    template_path_3 = img_path + "home_mark.png"
    if (rect_match_sqdiff(template_path_1, threshold) or
            rect_match_sqdiff(template_path_2, threshold)):
        return 1
    elif rect_match_sqdiff(template_path_3, threshold):
        return 2
    return 0


def leave_home():
    if whitch_area() == 2:
        song_leave_simple()
        time.sleep(10)
        wait_for_trans()


def wait_for_trans():
    # while finder.get_current_coordinate() == [0, 0] or if_trans():
    while if_trans():
        time.sleep(1)


def open_gamemenu_ui():
    while ppocr((1022, 260, 1080, 280)) != "Game":
        press_key('esc', delay=1.5)


def close_gamemenu_ui():
    while ppocr((1022, 260, 1080, 280)) == "Game":
        press_key('esc', delay=1)


def clear_interface():
    open_gamemenu_ui()
    close_gamemenu_ui()


# 在gamemenu切换角色
def switch_char_ingame(pos=0):
    diffX = 8  # 窗口位置移动后偏差
    diffY = 2  # 窗口位置移动后偏差

    move_mouse(0, 0)
    open_gamemenu_ui()
    time.sleep(5)
    open_gamemenu_ui()

    select_color = (140, 223, 255)

    # 打开切换角色
    while ppocr((1164, 739, 1218, 759)) != "Cancel":
        click(409, 745, delay=0.5)

    # 切换到第一个角色
    if match_point((1370, 345), (181, 155, 109)):
        print("需要滚轮")
        move_mouse(961 + diffX, 519 + diffY)
        while match_point((1370, 345), (181, 155, 109)):
            scroll(1)
            time.sleep(1)
    move_mouse(961 + diffX, 519 + diffY)

    # 计算要滚轮多少下
    if pos > 8:
        scroll_time = 1 + ((pos - 9) // 3)  # 滚轮次数
        pos = pos - 3 * scroll_time  # 窗口九个角色的实际点击位置

        for i in range(scroll_time):
            scroll(-1)
            time.sleep(1)

        # result = pos - 8
        # print(pos)
        # quotient = result // 3  # 滚轮次数
        # remainder = result % 3  # 点击位置
        # print("remainder: ", remainder)
        #
        # if remainder != 0:
        #     quotient += 1
        # for i in range(quotient):
        #     scroll(-1)
        #     time.sleep(1)
        # pos = remainder + 5

    # 选中角色, 如果已经是目标角色，退出; 否则点击目标点位
    if match_point((char_select_color_pos_ingame[pos][0] + diffX, char_select_color_pos_ingame[pos][1] + diffY),
                   select_color):
        clear_interface()
        return
    while not match_point((char_select_color_pos_ingame[pos][0] + diffX, char_select_color_pos_ingame[pos][1] + diffY),
                          select_color):
        click(char_pos_ingame[pos][0] + diffX, char_pos_ingame[pos][1] + diffY)

    # 点击传送
    while ppocr((882, 451, 942, 472)) != "Switch":
        click(1059, 749)
    while ppocr((882, 451, 942, 472)) == "Switch":
        click_OK()

    # 等待传送结束
    while True:
        if not if_trans():
            clear_interface()
            leave_home()
            break


# def count_char_number():#统计角色数量
#     select_color = (140, 223, 255)
#     count = 0
#
#     move_mouse(0, 0)
#     open_gamemenu_ui()
#
#     select_color = (140, 223, 255)
#     # 打开切换角色
#     while ppocr((1165, 723, 1220, 742)) != "Cancel":
#         click(407, 727, delay=0.5)
#     # 切换到第一个角色
#     if match_point((1361, 345), (182, 156, 109)):
#         print("需要滚轮")
#         move_mouse(961, 519)
#         while match_point((1361, 345), (182, 156, 109)):
#             scroll(1)
#             time.sleep(1)
#     move_mouse(961, 519)
#     while count<9:
#         click(char_pos_ingame[count])
#         if match_point((char_select_color_pos_ingame[count]), select_color):
#             count+=1
#         else:
#             return count
#     #大于九个角色，处理方法
#     scroll(-1)
#     if not  match_point((1361, 345), (182, 156, 109)):
#         return count
#     else:
#

def if_bigMapCoord_exist(world_map_coord, big_map_coord, big_map_color):
    move_mouse(960, 540)
    while ppocr((1601, 900, 1646, 918)) != "Memo":
        press_key('m')
    while ppocr((650, 472, 683, 498)) != "Sea":  # 缩小到小地图
        click_right_mouse()

    while ppocr((650, 472, 683, 498)) == "Sea":
        click(world_map_coord)

    res = None
    if match_point(big_map_coord, big_map_color):
        res = True
    else:
        res = False

    clear_interface()

    return res


def move_to_triport(world_map_coord, big_map_coord, triport_coord):
    move_mouse(960, 540)
    while ppocr((1601, 900, 1646, 918)) != "Memo":
        press_key('m')
    while ppocr((650, 472, 683, 498)) != "Sea":  # 缩小到小地图
        click_right_mouse()

    while ppocr((650, 472, 683, 498)) == "Sea":
        click(world_map_coord)
    while not match_point((258, 901), (205, 185, 132)):
        click(big_map_coord)

    while not if_image_exists(img_path + "OK_mark.png"):
        click(triport_coord, delay=0.1)
        move_mouse(0, 0, delay=1)
    while if_image_exists(img_path + "OK_mark.png"):
        click_OK()
    time.sleep(12)
    wait_for_trans()


def leave_NPC_chat():
    if ppocr((1786, 1017, 1849, 1041)) == "Leave":
        while ppocr((1786, 1017, 1849, 1041)) == "Leave":
            press_key('esc')


def song_leave_simple():  # 避免卡点
    move_mouse(1509, 549)
    press_key("f2", delay=3)

    click(1414, 217)
    click(1414, 217)
    type_text('escape')
    time.sleep(2)
    press_key('enter')
    click(1488, 315)
    click(1488, 315)

    # 点ok
    click(1461, 855, delay=2)
    click(1461, 855, delay=2)
    click(1461, 855, delay=2)
    click(1461, 855, delay=2)


# 清空背包蓝色、紫色的书
def remove_trash():
    clear_interface()
    open_inventory()
    # 蓝色紫色书
    while True:
        pos = find_img_low_threshold(img_path + "trash/blue.png")
        if pos != [0, 0]:
            move_mouse(pos)
            hold_left_mouse()
            move_mouse(994, 572)
            release_left_mouse()
            time.sleep(1)
            click_OK(delay=0.1)
            move_mouse(994, 572, delay=1)
        else:
            break

    while True:
        pos = find_img_low_threshold(img_path + "trash/purple.png")
        if pos != [0, 0]:
            move_mouse(pos)
            hold_left_mouse()
            move_mouse(994, 572)
            release_left_mouse()
            time.sleep(1)
            click_OK(delay=0.1)
            move_mouse(0, 0, delay=1)
        else:
            break

    # 卡片
    for i in range(3):
        i += 1
        while True:
            pos = find_img_low_threshold(img_path + f"trash/card_{i}.png", rect=(1318, 213, 1872, 799), threshold=0.1)
            if pos != [0, 0]:
                move_mouse(pos)
                hold_left_mouse()
                move_mouse(994, 572)
                release_left_mouse()
                time.sleep(1)
                click_OK(delay=0.1)
                move_mouse(0, 0, delay=1)
            else:
                break

    close_inventory()


def song_home_simple():  # 避免卡点
    if whitch_area() == 2:
        return
    move_mouse(1509, 549)
    press_key("f2", delay=3)

    click(1414, 217)
    click(1414, 217)
    type_text('home')
    time.sleep(2)
    press_key('enter')
    click(1488, 315)
    click(1488, 315)

    click(1461, 855)
    click(1461, 855)


def if_have_home():
    if whitch_area() == 2:
        return
    move_mouse(1509, 549)
    press_key("f2", delay=3)

    click(1414, 217)
    click(1414, 217)
    type_text('home')
    time.sleep(2)
    press_key('enter')
    if match_point((1344, 310), (245, 221, 119)):
        clear_interface()
        return True
    else:
        clear_interface()
        return False


# 重置设置
def reset_setting():
    open_gamemenu_ui()
    while ppocr((1022, 260, 1080, 280)) == "Game":
        click(1022, 751, delay=1.5)  # 点击设置
    while ppocr((555, 801, 599, 822), det=False) != "Reset":
        time.sleep(1)

    # 等待一秒，点reset
    move_mouse(585, 815, delay=1)
    click_left_mouse()
    time.sleep(1)
    move_mouse(903, 583)
    click_left_mouse()
    # wait_for_image(current_path + "/../data/mark/OK_mark.png")  # 等待OK
    # click_OK()

    # 更改画质为低
    move_mouse(1091, 629, delay=1)  # 展开画质列表
    click_left_mouse()
    move_mouse(1075, 749, delay=1)  # 选择低
    click_left_mouse()

    # 更改攻击为左键
    move_mouse(650, 378, delay=1)  # 打开gameplay
    click_left_mouse()
    move_mouse(651, 452, delay=1)  # 选择control
    click_left_mouse()
    ##检测设置是否为右键走路
    if match_point((1041, 300), (212, 183, 114)):
        move_mouse(1041, 300, delay=1)  # 取消左键走路
        click_left_mouse()

    # 检测光敏模式
    ## 打开acc
    move_mouse(636, 340, delay=1)
    click_left_mouse()
    ## 下滑滚轮
    move_mouse(1341, 431)
    for i in range(5):
        scroll(-1)
        time.sleep(0.1)
    ## 打开光敏开关
    if not match_point((1043, 656), (211, 182, 112)):
        move_mouse(1043, 656, delay=1)
        click_left_mouse()

    # 确认设置
    while ppocr((555, 801, 599, 822), det=False) == "Reset":
        click(1223, 815, delay=1)
        click_OK()


def adjust_transparency():
    ##OK报错
    click_OK(delay=0.5)

    # 改透明度
    move_mouse(1905, 91, delay=0.5)
    click_left_mouse(duration=0.05, delay=1.0)
    move_mouse(1874, 90, delay=0.5)
    click_left_mouse(duration=0.05, delay=0.5)


def open_inventory():
    # while ppocr((1552, 194, 1641, 220), det=True) != "Inventory":
    move_mouse(100, 100)
    while not if_image_exists(img_path + "inventory.png"):
        press_key('i')
    if not match_point((1409, 259), (239, 228, 148)):
        click(1409, 259)


def close_inventory():
    clear_interface()


def open_character_profile():
    while ppocr((590, 197, 651, 217)) != "Profile":
        press_key('p')


def close_character_profile():
    while ppocr((590, 197, 651, 217)) == "Profile":
        press_key('p')


def get_gold_amount():
    open_inventory()

    move_mouse(1845, 809, delay=3)
    rect = (1454, 820, 1730, 847)
    try:
        gold_amount = ppocr(rect, det=True)
        parts = gold_amount.split('/')

        # 提取第一个部分中的纯数字
        first_part = parts[0]
        numbers = re.sub(r'\D', '', first_part)  # 只保留数字字符
        close_inventory()

        if numbers == None or numbers == '':
            numbers = -1
        numbers = int(numbers)
        gl_info.gold = numbers
        return numbers
    except:
        return -2


def get_equip_level():
    move_mouse(0, 0)
    open_character_profile()

    rect = (930, 358, 1061, 396)
    level = ppocr(rect=rect, det=True)
    gl_info.equip_level = level

    close_character_profile()


def dismantle_inventory():
    settings = Config(config_path)
    open_inventory()
    click(1441, 805)

    click(841, 745)
    click(924, 748)
    click(1004, 748)
    click(1096, 750)
    click(1180, 746)
    if not int(settings.get_value("全局配置", "不分解古代")):
        click(1266, 746)  # 古代

    click(1233, 804)
    click(993, 581)
    time.sleep(1)
    close_inventory()


def close_altQ():
    while ppocr((982, 126, 1029, 154)) == "List":
        combine_keys('alt', 'q', delay=2)


def chat_with_NPC():
    while ppocr((1783, 1018, 1852, 1042)) != "Leave":
        press_key('g')

    time.sleep(3)


def if_die():
    if if_image_exists(img_path + "died.png"):
        return True
    return False


def resurrection(method=1):
    '''
    复活
    :param method: 1为羽毛，0为免费
    :return:
    '''
    if not match_point((679, 972), (14, 12, 10), tolerance=(50, 50, 50)):
        return
    if if_die():
        pos = find_img_low_threshold(img_path + "died.png")
        if method == 1:  # 羽毛
            pos = [pos[0], pos[1] + 311 - 70]  # 复活按键坐标
        if method == 0:  # 免费
            pos = [pos[0], pos[1] + 311]  # 复活按键坐标
        while if_image_exists(img_path + "died.png"):
            click(pos)
            time.sleep(2)
        move_mouse(960, 533)


def board_ocean_liner(port_coord=(1048, 661)):
    """
    乘坐渡轮传送，默认前往卢特兰
    :param port_coord:
    :return:
    """
    move_mouse(960, 540)
    while ppocr((1601, 900, 1646, 918)) != "Memo":
        press_key('m')

    while ppocr((765, 897, 812, 918), det=False) == "Board" and match_point((784, 913), (254, 254, 254)):
        click(825, 904, delay=1.0)
    # wait_for_image(current_path + "/../data/mark/OK_mark.png")
    time.sleep(2)
    click_OK()
    # click(899, 601)  # 点击OK
    wait_for_image(img_path + "ship_mark.jpg")
    time.sleep(1)
    click(port_coord)
    click(958, 871, delay=1.0)
    time.sleep(5)
    # wait_for_image(img_path + "OK_mark.png")
    click_OK()
    time.sleep(5)
    # click(905, 650)  # 点击OK
    while if_trans():
        time.sleep(1)
    clear_interface()
    # time.sleep(2)


def go_to_city(use_triport=False):
    # 打开地图
    move_mouse(960, 540)
    while ppocr((1601, 900, 1646, 918)) != "Memo":
        press_key('m')

    time.sleep(2)
    # 在海上
    if ppocr((789, 890, 835, 910), det=False) == "Auto":
        # 缩小到世界地图
        while ppocr((650, 472, 683, 498)) != "Sea":  # 缩小到小地图
            click_right_mouse()
        # 去路特兰港口
        move_mouse(1109, 675, delay=1)
        combo_key_mouse('alt', 'left')
        # 等待到达
        while ppocr((789, 890, 835, 910), det=False) != "Auto":
            time.sleep(1)
        time.sleep(2)
        # 抛锚
        while ppocr((1588, 1018, 1646, 1049), det=False) != "Dock":
            press_key('z')
            time.sleep(5)
        # 进入z
        while ppocr((1588, 1018, 1646, 1049), det=False) == "Dock":
            click(1621, 1030)
        wait_for_trans()
        clear_interface()
    # 在天界
    elif ppocr((262, 126, 516, 165), det=False) == "Elgacia":
        while ppocr((1601, 900, 1646, 918)) != "Memo":
            press_key('m')
        return
    # 在岛上
    elif match_point((818, 913), (150, 150, 150)):
        song_leave_simple()
        time.sleep(10)
        wait_for_trans()
        clear_interface()
        # 打开地图
        move_mouse(960, 540)
        while ppocr((1601, 900, 1646, 918)) != "Memo":
            press_key('m')
        time.sleep(2)
        # 缩小到世界地图
        while ppocr((650, 472, 683, 498)) != "Sea":  # 缩小到小地图
            click_right_mouse()
        # 去路特兰港口
        move_mouse(1109, 675, delay=1)
        move_mouse_w32(1109, 675)
        combo_key_mouse('alt', 'left')
        # 等待到达
        while ppocr((789, 890, 835, 910), det=False) != "Auto":
            time.sleep(1)
        time.sleep(2)
        # 抛锚
        while ppocr((1588, 1018, 1646, 1049), det=False) != "Dock":
            press_key('z')
            time.sleep(5)
        # 进入z
        while ppocr((1588, 1018, 1646, 1049), det=False) == "Dock":
            click(1621, 1030)
        wait_for_trans()
        clear_interface()
    # 在卢特兰同一大陆
    elif ppocr((262, 126, 516, 165), det=False) == "Rethramis" or ppocr((262, 126, 516, 165),
                                                                        det=False) == "Yudia" or ppocr(
        (262, 126, 516, 165), det=False) == "West Luterra" or ppocr((262, 126, 516, 165),
                                                                    det=False) == "East Luterra":
        pass
    # 在港口大陆
    elif not match_point((818, 913), (150, 150, 150)) and ppocr((765, 897, 812, 918), det=False) == "Board":
        board_ocean_liner()
    clear_interface()
    if use_triport == True:  # 去初始主城
        move_to_triport([900, 703], [827, 520], [897, 525])
        wait_for_trans()
        clear_interface()


def ride_mount():
    while ppocr((1623, 879, 1661, 900)) != "Ride":
        combine_keys('alt', ',')
        time.sleep(1)

    # 点坐骑
    click(1567, 411)
    click(1567, 411)
    # 点ride
    click(1640, 891)
    click(1640, 891)
    clear_interface()


def disMount():
    if if_image_exists(img_path + "gameAction/dismount.png"):
        press_key('r', delay=2)


def take_mail():
    # 进入邮件人对话
    for i in range(10):
        if i == 9:  # 超时直接结束
            return
        if ppocr((940, 880, 981, 899), det=True) != "Mail":
            press_key('g')
        else:  # 识别到mail正确退出
            break
    # 点击自动删除
    while not match_point((265, 209), (213, 184, 115)):
        click(265, 209)
    # 循环领邮件
    while True:
        while not match_point((135, 208), (217, 189, 117)):  # 点击select all
            click(135, 208)
        if match_point((296, 720), (245, 245, 245)):  # 有邮件则领取
            click(296, 720, delay=1)
            wait_for_color((139, 253), (15, 17, 18))
        else:
            break
    # 退出邮件人对话
    while ppocr((940, 880, 981, 899), det=True) == "Mail":
        click(1818, 1025)


class MailStopException(Exception):
    pass


def mail_material():
    """给指定角色发送邮件

    :return:
    """

    def write_name():
        # 写名字
        click(357, 244)
        combine_keys('ctrl', 'a')
        type_text(name, delay=1)
        click(100, 100)

    def send_mail():
        # 发邮件
        while match_point((334, 725), (255, 255, 255)):
            click(343, 727, delay=2)
        if if_image_exists(img_path + "OK_mark.png"):
            if ppocr((394, 330, 446, 348), det=True) != "amount":  # 邮寄数量上限了？
                raise MailStopException
            else:  # 邮寄金币
                click_OK(delay=2)

    def type_gold(leave_gold=100):
        """输入金币信息

        :param leave_gold: 余留多少金币
        :return:
        """

        def click_rect():
            click(502, 639)
            combine_keys('ctrl', 'a')

        if not match_point((132, 640), (225, 199, 145)):
            click(132, 640)
        click_rect()
        type_text("999999")

        gold_num = int(ppocr((629, 628, 693, 647), det=True, num_only=True))
        gold_num -= leave_gold

        click_rect()
        if gold_num > 0:
            type_text(str(gold_num))
        else:
            type_text("0")

    def send_all(if_type_num=False):  # 要先写名字
        """

        :param if_type_num: 是否需要数量
        :return:
        """
        # 判断哪些需要邮寄
        config = Config(config_path)
        ## 邮寄材料选择
        if_gem = int(config.get_value("全局配置", "宝石"))
        if_fish = int(config.get_value("全局配置", "鱼"))
        if_chaosGate = int(config.get_value("全局配置", "混沌之门材料"))
        ## 根据选择添加检索的子文件
        sub_dir_list = []
        if if_gem:
            sub_dir_list.append("gem")
        if if_fish:
            sub_dir_list.append("fish")
        if if_chaosGate:
            sub_dir_list.append("chaosGate")

        mat_img_path_list = []  # 总的文件路径
        all_mats_path = img_path + "mailMat"
        print("game_action.py sub_dir_list:", sub_dir_list)
        for sub_dir in sub_dir_list:
            mat_img_path_list += get_all_files_name(all_mats_path + f"\\{sub_dir}", sub_dir)

        find_rect = (739, 113, 1274, 750)
        mat_count = 0  # 一次最多寄七个
        for mat in mat_img_path_list:
            move_mouse(100, 100)  # 鼠标移开
            mat_path = all_mats_path + f"/{mat}"
            print("game_action.py mat_path:", mat_path)
            all_pos = find_all_img_low_threshold(mat_path, rect=find_rect, threshold=0.08)
            for pos in all_pos:
                move_mouse(pos)
                click_right_mouse(delay=2)
                if if_type_num:
                    type_text("99999", delay=1)
                    move_mouse(100, 100)
                    click_OK(delay=2)
                mat_count += 1
                if mat_count >= 7:
                    send_mail()
                    write_name()
                    mat_count = 0
        send_mail()
        write_name()

    try:
        config = Config(config_path)
        name = config.get_value("全局配置", "收件角色名称")
        # 进入邮件人对话
        for i in range(10):
            if i == 9:  # 超时直接结束
                return
            if ppocr((940, 880, 981, 899), det=True) != "Mail":
                press_key('g')
            else:  # 识别到mail正确退出
                break
        # 寄邮件
        ## 打开寄件界面
        if match_point((493, 189), (78, 85, 92)):
            click(496, 182)
        ## 选择快速邮件
        if match_point((283, 210), (17, 21, 22)):
            click(283, 210)
        ## 寄背包所有材料
        while not match_point((793, 187), (231, 203, 120)):
            click(820, 170)
        write_name()
        # 第一次写名字，检查是不是自己
        if ppocr((635, 238, 676, 253)) == "Name":
            clear_interface()
            return
        # 第一次邮寄金币
        # type_gold()
        send_all()
        ### 再寄鱼
        # 打开storage
        while not match_point((914, 187), (231, 204, 122)):
            click(936, 170)
        # 打开stronghold
        while not match_point((882, 269), (107, 154, 206)):
            click(942, 254)
        # 搜索并邮寄每一项
        item_list = [
            "fish",
            "Oreha",
            "abidos",
        ]
        for item in item_list:
            click(799, 294)
            combine_keys('ctrl', 'a')
            type_text(item)
            press_key('enter')
            while not match_point((1221, 336), (244, 217, 160)):
                click(1221, 336)
            send_all(if_type_num=True)
            # 右侧有滚轮
            while match_point((1255, 698), (197, 170, 121)):
                move_mouse(1255, 375)
                for i in range(5):
                    scroll(-1)
                    time.sleep(0.3)
                send_all(if_type_num=True)

        # 退出邮件人对话
        while ppocr((940, 880, 981, 899), det=True) == "Mail":
            click(1818, 1025)
    except MailStopException:
        clear_interface()


def refresh_inventory():
    open_inventory()
    l = [
        (1410, 249),
        (1468, 247),
        (1523, 247),
        (1530, 329),
        (1582, 252),
        (1410, 249),
    ]
    for item in l:
        click(item)
    close_inventory()


def get_unaToken():
    """
    获取una币
    :return:
    """
    move_mouse(100, 100)

    while ppocr((77, 151, 163, 183)) != "Roster":
        combine_keys('alt', 'j', delay=2)
    if match_point((186, 800), (255, 255, 255)):
        click(186, 800)
        click_OK()

    clear_interface()


def exit_game():
    open_gamemenu_ui()
    while find_img_low_threshold(img_path + "OK_mark.png") == [0, 0]:
        click(1475, 745)
    click_OK()
