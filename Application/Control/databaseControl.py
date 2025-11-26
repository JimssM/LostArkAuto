#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sqlite3

from Application.Model.model import gl_info
from Application.public import database_path


def update_database():
    # 连接到数据库
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # 对应的键
    keys = ["username", "password", "region", "server", "equip_level", "chaosDungeon_level", "gold", "last_update_time"]

    data_list = []
    data_list.append(gl_info.username)
    data_list.append(gl_info.password)
    data_list.append(gl_info.region)
    data_list.append(gl_info.server)
    data_list.append(gl_info.equip_level)
    data_list.append(gl_info.chaosDungeon_level)
    data_list.append(gl_info.gold)
    data_list.append(gl_info.last_update_time)

    #记录日志到服务器
    data = {
        keys[0]: gl_info.username,
        keys[1]: gl_info.password,
        keys[2]: gl_info.region,
        keys[3]: gl_info.server,
        keys[4]: gl_info.equip_level,
        keys[5]: gl_info.chaosDungeon_level,
        keys[6]: gl_info.gold,
        keys[7]: gl_info.last_update_time,
        "if_banned": gl_info.if_banned, # 额外记录封号信息
        "char_count": gl_info.char_count,
    }
    # log_to_server(data)

    # 准备有效的键和值
    valid_keys = []
    valid_values = []
    placeholders = []

    for key, value in zip(keys, data_list):
        if value != "-1":
            valid_keys.append(key)
            valid_values.append(value)
            placeholders.append('?')

    keys_str = ', '.join(valid_keys)
    placeholders_str = ', '.join(placeholders)

    # 生成UPSERT SQL语句
    update_str = ', '.join([f"{key}=excluded.{key}" for key in valid_keys if key not in ['username', 'server']])
    sql = f'''
        INSERT INTO acc_state ({keys_str}) VALUES ({placeholders_str})
        ON CONFLICT(username, server) DO UPDATE SET {update_str}
        '''
    # 执行插入或更新操作
    try:
        cursor.execute(sql, valid_values)
        conn.commit()
        print("数据插入或更新成功")
    except sqlite3.IntegrityError as e:
        print("数据插入或更新失败:", e)
    except sqlite3.OperationalError as e:
        print("SQL语句错误:", e)
