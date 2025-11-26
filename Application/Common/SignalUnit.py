# !/usr/bin/env python
# -*-coding:utf-8 -*-

from PyQt5.Qt import QObject, pyqtSignal

class SignalUnit(QObject):
    table = pyqtSignal(int, int, str, int,int)
    log = pyqtSignal(str)
signal = SignalUnit()

