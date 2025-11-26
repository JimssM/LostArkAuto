#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os

def get_all_files_name(directory, parent_dir=None):
    files = []
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            if parent_dir is not None:
                files.append(os.path.join(parent_dir, file))  # 添加父目录
            else:
                files.append(file)  # 仅添加文件名
    return files
