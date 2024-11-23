#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys

from glob import glob

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def path_format(path: str, is_dir=False):
    """
    路径格式化
    :return:
    """
    return path.replace('\\', '/') + ("/" if is_dir else "")


def get_root(file_path: str):
    """
    获取当前文件所在的根目录
    :param file_path:
    :return:
    """
    return path_format(os.path.dirname(os.path.abspath(file_path)))


def join_2_base_path(base_file_path, *paths, is_dir=False) -> str:
    """
    以 base_file_path 所在目录为根目录, 拼接路径
    :param base_file_path:
    :param paths:
    :param is_dir:
    :return:
    """
    return path_format(join_path(get_root(base_file_path), *paths), is_dir=is_dir)


def join_path(*paths, is_dir=False) -> str:
    """
    拼接路径并格式化
    :param paths:
    :param is_dir:
    :return:
    """
    # return path_format(os.path.join(*paths), is_dir=is_dir)
    # return path_format(
    #     os.path.join(*[(path[1:] if path and path[0] == '/' else path) for path in paths]),
    #     is_dir=is_dir
    # )
    return path_format(
        os.path.join(*paths),
        is_dir=is_dir
    )


def create_dir(path):
    """
    创建目录
    :param path:
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)


def get_file_name(file_path: str):
    """
    获取文件名与文件拓展名
    :param file_path: 文件路径
    :return:
    """
    file_name = os.path.basename(file_path)
    file_extension = None
    if "." in file_name:
        file_name, file_extension = file_name.split(".")

    return file_name, file_extension


def get_filepaths_without_extension(files_dir: str, file_format=None):
    """
    获取目录下所有指定格式的文件
    :param files_dir: 指定目录
    :param file_format: 指定格式
    :return:
    """
    if not isinstance(file_format, list):
        file_format = [file_format]

    all_file = []
    for ff in file_format:
        if '.' in ff:
            files = glob(join_path(files_dir, ff))
        else:
            files = glob(join_path(files_dir, f"*.{ff}"))
        files = [path_format(file) for file in files]
        # files = os.listdir(files_dir)
        all_file += files

    return all_file


if __name__ == '__main__':
    print(get_file_name(get_root(__file__)))
