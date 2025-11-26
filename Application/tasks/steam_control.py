import time
import webbrowser

from Application.Control.configControl import Config
from Application.public import *
from Application.tools import *
from Application.Model.model import *


class SteamControl:
    config = Config(config_path)
    steam_path = config.get_value("全局配置", "Steam路径")
    steam_login_cls = 'SDL_app'
    steam_login_title = '登录 Steam'

    game_id = 1599340  # 失落的方舟

    @staticmethod
    def login_steam():
        for i in range(5):
            print("尝试登陆")
            for i in range(10):#启动应用只尝试5次
                if not is_process_running("Steam.exe"):
                        start_process_4(SteamControl.steam_path)
                print("启动")
                if not find_window_handle(SteamControl.steam_login_cls, SteamControl.steam_login_title):
                    print("检测窗口")
                    time.sleep(5)
                else:
                    break
                if i ==9:
                    return False
            print("登陆成功")
            time.sleep(5)
            set_window_top_left(find_window_handle(SteamControl.steam_login_cls, SteamControl.steam_login_title))
            time.sleep(1)
            click(160, 140, delay=0.1)
            type_text(gl_info.username, delay=1)
            press_key('tab', delay=0.1)
            type_text(gl_info.password, delay=1)
            press_key('enter')
            for i in range(5):
                print("检测登陆中")
                if find_window_handle(SteamControl.steam_login_cls, SteamControl.steam_login_title):
                    time.sleep(5)
                else:
                    print("登陆成功")
                    return True
            SteamControl.close_all()
            time.sleep(1)

        return False


    @staticmethod
    def start_game():
        SteamControl.close_all()
        success = False
        while True:
            login_state = SteamControl.login_steam()
            if not login_state:
                gl_info.log = gl_info.log + ", " + "登陆Steam失败"
                return

            SteamControl.__launch_steam_game()
            SteamControl.clear_interface()

            max_range = 60
            for i in range(max_range):
                time.sleep(1)
                if find_window_handle(None, "Lost Ark") or\
                        find_window_handle("SplashScreenClass", "SplashScreen") or\
                    is_process_running("LOSTARK.exe"):
                    time.sleep(0.05)
                    success = True
                    break
                if i == (max_range - 1):
                    SteamControl.close_all()

        while True:
            # 没有成功启动游戏则发送启动指令
            if success == False:
                SteamControl.__launch_steam_game()
                SteamControl.clear_interface()
            # 游戏窗口成功打开，且加载窗口不存在
            if find_window_handle('EFLaunchUnrealUWindowsClient', None):
                time.sleep(5)
                if (not find_window_handle("SplashScreenClass", "SplashScreen")) and (
                        not find_window_handle(None, 'Error')):
                    print("启动成功")
                    break
            # eac错误窗口
            if find_window_handle('eac_bugreport', None):
                close_process('Launch_Game.exe')
                success = False
                time.sleep(10)
            # Error错误窗口
            if find_window_handle(None, 'Error'):
                close_window_by_handle(find_window_handle(None, 'Error'))
                success = False
                time.sleep(10)

    @staticmethod
    def __launch_steam_game():
        steam_url = f'steam://run/{SteamControl.game_id}'
        webbrowser.open(steam_url)

    @staticmethod
    def clear_interface():
        time.sleep(1)
        t = time.time()
        while time.time() - t < 50:
            if find_window_handle('SDL_app', '好友列表'):
                close_window_by_handle(find_window_handle('SDL_app', '好友列表'))
            elif find_window_handle('SDL_app', '特惠'):
                close_window_by_handle(find_window_handle('SDL_app', '特惠'))
            elif find_window_handle(None, 'Easy Anti-Cheat'):
                close_window_by_handle(find_window_handle(None, 'Easy Anti-Cheat'))
            elif find_window_handle(None, "客服消息"):
                close_window_by_handle(find_window_handle(None, "客服消息"))
            elif find_window_handle(None, "Valve 硬件调查"):
                close_window_by_handle(find_window_handle(None, "Valve 硬件调查"))
            elif find_window_handle(None,"Easy Anti-Cheat"):
                close_window_by_handle(find_window_handle(None,"Easy Anti-Cheat"))
            SteamControl.detect_agreement()
            time.sleep(1)

    @staticmethod
    def detect_agreement():
        pos = find_img_low_threshold(img_path + "accept_mark.png")
        print("图片路径：", img_path + "agreement_mark.png")
        if pos != [0, 0] and if_image_exists(img_path + "agreement_mark.png", threshold=0.03):
            click(pos, delay=0.1)

    @staticmethod
    def close_all():
        close_process_2('LOSTARK.exe')
        time.sleep(1)
        close_process_2('LOSTARKWeb64.ark')
        time.sleep(1)
        close_process_2('steam.exe')
        time.sleep(1)
        close_process_2('steamwebhelper.exe')
        time.sleep(1)
        close_process_2('steamservice.exe')
        time.sleep(1)
        close_process_2('GameOverlayUI.exe')
        time.sleep(1)
        close_process_2('gameoverlayui.exe')
        time.sleep(7)

    @staticmethod
    def callback():
        SteamControl.close_all()
        # move_mouse(1919,0)
        # release_all_keys_pynput()
        # click(1919,549)
        gl_info.log = gl_info.log + ", " + "进入游戏失败"
        print("steam control callback")

