#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import Application.tasks.chaosGate
from Application.public import *
from Application.tasks.game_action import *
from Application.tasks.pathFinder import *
from Application.tasks.chaosDungeon import *
def new_event_task():
    gl_info.thread_main.execution_time = -2400

    switch_char_ingame(0)
    go_to_city()
    move_to_triport([1013, 719], [921, 651], [968, 472])

    ride_mount()
    finder = PathFinder(img_path + "map/event/event.png", resize=2.5, max_val=0.6)
    path = [431.0, 288.0], [424.0, 271.0], [404.0, 268.0], [375.0, 271.0], [360.0, 295.0], [345.0, 311.0], [328.0,
                                                                                                            327.0], [
        303.0, 346.0],
    finder.node_finder(path)

    press_key('g')

    time.sleep(10)
    wait_for_trans()
    cd = ChaosDungeon()
    while ppocr((106, 185, 161, 209)) != "100%":
        cd.use_random_skill(num=8)


    # while not if_die():
    #     time.sleep(10)
    # switch_char_ingame(1)
    # time.sleep(400)
    # switch_char_ingame(0)