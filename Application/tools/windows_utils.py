import ctypes
import os
import subprocess

import psutil
import win32con
import win32gui
import win32process


def find_window_handle(cls: str, title: str):
    return win32gui.FindWindow(cls, title)


def close_window_by_handle(hwnd):
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)


def set_window_top_left(hwnd):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, right - left, bottom - top,
                          win32con.SWP_SHOWWINDOW)


def set_window_top(hwnd):
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

def set_window_no_top(hwnd):
    win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

def find_cls_and_title_by_pid(pid):
    def callback(hwnd, hwnds):
        if all([win32process.GetWindowThreadProcessId(hwnd)[1] == pid, win32gui.IsWindowVisible(hwnd)]):
            print(win32gui.GetClassName(hwnd), win32gui.GetWindowText(hwnd))
            hwnds.append(hwnd)
        return True

    hwnd_list = []
    win32gui.EnumWindows(callback, hwnd_list)

def start_process(process_path):
    command = f'powershell -command "Start-Process \'{process_path}\'"'
    subprocess.run(command, shell=True)

def start_process_2(process_path):
    # 指定目录
    working_directory = os.path.dirname(process_path)


    # 切换工作目录
    os.chdir(working_directory)

    # 使用ctypes隐藏cmd窗口启动应用程序
    SW_HIDE = 0
    STARTF_USESHOWWINDOW = 1

    class STARTUPINFO(ctypes.Structure):
        _fields_ = [("cb", ctypes.c_ulong),
                    ("lpReserved", ctypes.c_void_p),
                    ("lpDesktop", ctypes.c_void_p),
                    ("lpTitle", ctypes.c_void_p),
                    ("dwX", ctypes.c_ulong),
                    ("dwY", ctypes.c_ulong),
                    ("dwXSize", ctypes.c_ulong),
                    ("dwYSize", ctypes.c_ulong),
                    ("dwXCountChars", ctypes.c_ulong),
                    ("dwYCountChars", ctypes.c_ulong),
                    ("dwFillAttribute", ctypes.c_ulong),
                    ("dwFlags", ctypes.c_ulong),
                    ("wShowWindow", ctypes.c_ushort),
                    ("cbReserved2", ctypes.c_ushort),
                    ("lpReserved2", ctypes.c_void_p),
                    ("hStdInput", ctypes.c_void_p),
                    ("hStdOutput", ctypes.c_void_p),
                    ("hStdError", ctypes.c_void_p)]

    class PROCESS_INFORMATION(ctypes.Structure):
        _fields_ = [("hProcess", ctypes.c_void_p),
                    ("hThread", ctypes.c_void_p),
                    ("dwProcessId", ctypes.c_ulong),
                    ("dwThreadId", ctypes.c_ulong)]

    startupinfo = STARTUPINFO()
    startupinfo.cb = ctypes.sizeof(startupinfo)
    startupinfo.dwFlags = STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = SW_HIDE

    process_information = PROCESS_INFORMATION()

    creation_flags = 0x08000000  # CREATE_NO_WINDOW

    ctypes.windll.kernel32.CreateProcessW(None, process_path, None, None, False, creation_flags, None, None,
                                          ctypes.byref(startupinfo), ctypes.byref(process_information))

    # 继续运行其他程序
    print("启动了进程，继续执行其他程序")

def start_process_3(process_path):
    return subprocess.Popen(process_path)
def start_process_4(process_path):
    command = [f"{process_path}", "--console"]
    subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)


def close_process( process_name):
    os.system(f"taskkill /F /IM {process_name}")

def close_process_2(process_name):
    for process in psutil.process_iter(attrs=['name']):
        if process.info['name'] == process_name:
            try:
                process.kill()
                # process.terminate()
                # 或者使用 process.kill() 来强制关闭
            except psutil.NoSuchProcess:
                pass
def is_process_running(process_name):
    """
    检查指定名称的进程是否正在运行
    """
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            return True
    return False

def count_processes_by_name(process_name):
    count = 0
    for process in psutil.process_iter(['name']):
        if process.info['name'] == process_name:
            count += 1
    return count