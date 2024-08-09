#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import ryzquo_tools.path_tools as rpt


def rename_file(file_path: str, old_name: str, new_name: str):
    """
    重命名文件
    :param file_path
    :param old_name:
    :param new_name:
    :return:
    """
    old_name = rpt.join_path(file_path, old_name)
    new_name = rpt.join_path(file_path, new_name)
    os.rename(old_name, new_name)
    
    
def move_files(source_path, destination_path):
    """
    移动文件, 单文件传字符串, 多文件传列表
    :param source_path: 源文件路径或源文件路径列表
    :param destination_path: 目标文件路径或目标文件路径列表
    :return:
    """
    if not isinstance(source_path, list):
        source_path = [source_path]
    
    if not isinstance(destination_path, list):
        destination_path = [destination_path]
    
    if len(source_path) != len(destination_path):
        raise ValueError("source_path and destination_path must be the same length")
    
    for old_path, new_path in zip(source_path, destination_path):
        shutil.move(old_path, new_path)


def copy_files(source_path, destination_path):
    """
    复制文件, 单文件传字符串, 多文件传列表
    :param source_path: 源文件路径或源文件路径列表
    :param destination_path: 目标文件路径或目标文件路径列表
    :return:
    """
    if not isinstance(source_path, list):
        source_path = [source_path]
    
    if not isinstance(destination_path, list):
        destination_path = [destination_path]
    
    if len(source_path) != len(destination_path):
        raise ValueError("source_path and destination_path must be the same length")
    
    for old_path, new_path in zip(source_path, destination_path):
        shutil.copy(old_path, new_path)


if __name__ == "__main__":
    pass
