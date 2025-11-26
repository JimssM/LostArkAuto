import ctypes
import threading

from Application.Model.model import gl_info
from Application.tools import *

'''
调用实例
thread = ThreadManager(func=lambda: _run_one_account(line, thread=thread),
                       callback=lambda: _call_back(thread=thread), max_time=999999)
thread.start()
thread.join()

'''


class ThreadControl(threading.Thread):
    '''
    ThreadControl.start()
    ThreadControl.join()
    :param func:要执行的方法
    :param callback:结束时调用回调函数
    :param max_time:最长运行时间，默认10分钟
    '''

    def __init__(self, func=lambda: None, callback=lambda: None, max_time=600):
        threading.Thread.__init__(self)

        self.func = func
        self.callback = callback
        self.max_time = max_time

        self.execution_time = 0

    def run(self):
        #启动计时器
        self.timer_thr = threading.Thread(target=self.__timer, daemon=True)
        self.timer_thr.start()
        try:
            self.func()
        except SystemExit:
            pass
        finally:
            if self.callback is not None:
                self.callback()
            else:
                pass

    def stop(self):
        if not self.is_alive():  # 父线程不存在
            return
        exc = ctypes.py_object(SystemExit)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(self.ident), exc)
        if res == 0:
            raise ValueError("找不到线程ID")
        elif res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(self.ident, None)
            raise SystemError("线程已停止")

    def __timer(self):
        while self.is_alive():
            if self.execution_time < self.max_time:
                self.execution_time = self.execution_time + 1
                print(self.execution_time)
                time.sleep(1)
            else:
                "timer计时达到"
                gl_info.interrupt = True
                self.stop()
                break
