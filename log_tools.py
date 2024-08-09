#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import glob
import logging
import datetime

from logging.handlers import RotatingFileHandler

# 添加根目录
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import ryzquo_tools.path_tools as rpt


def logger_file(dir):
    for i in range(10):
        str_date = "2024-03-1" + str(i)
        path = os.path.join(dir, str_date + "-all" + ".log")
        # 创建文件
        file = open(path, "w")
        # file.write("这是一个新创建的文件。\n")
        file.close()
        # now_time = datetime.datetime.strptime(time.strftime("%Y-%m-%d"), "%Y-%m-%d")
        # print(time.strftime("%Y-%m-%d"))

        # now_time = datetime.datetime.now().strftime('%Y-%m-%d')
        # print(now_time)
        time.sleep(1)


def logger_file_remove_by_day(dir, day=10):
    """
    删除指定天数前的日志
    """
    # print(dir)
    # 删除10天前的日志
    error_file_list = glob.glob(dir + "/*all.log")
    error_file_list.sort()
    for i in range(len(error_file_list) - day):
        time_file_lists = glob.glob(error_file_list[i][:-7] + "*")
        for file_name in time_file_lists:
            print(file_name)
            os.remove(file_name)


def logger_handler(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 当前文件路径
    cur_path = rpt.get_root(__file__)

    # 日志存放目录 log_path
    log_dir = rpt.join_path(cur_path, 'logs')

    # 创建日志存放目录
    rpt.create_dir(log_dir)

    # 只保留10天次的日志
    logger_file_remove_by_day(log_dir)

    # 当前日期格式化
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    # 收集所有日志信息文件
    __all_log_path = rpt.join_path(log_dir, now_time + "-all" + ".log")
    # 收集错误日志信息文件
    __error_log_path = rpt.join_path(log_dir, now_time + "-error" + ".log")
    formatter = logging.Formatter('%(asctime)s-%(filename)s-[line:%(lineno)d]-%(levelname)s-[log]:%(message)s')
    handler_cfgs = [
        {'type': 'file', 'filename': __all_log_path, 'level': logging.INFO, 'formatter': formatter},
        {'type': 'file', 'filename': __error_log_path, 'level': logging.ERROR, 'formatter': formatter},
        {'type': 'console', 'level': logging.DEBUG, 'formatter': formatter}
    ]

    for handler_cfg in handler_cfgs:
        if handler_cfg['type'] == 'file':
            handler = RotatingFileHandler(
                filename=handler_cfg['filename'],
                maxBytes=1 * 1024 * 1024,
                backupCount=3,
                encoding='utf-8'
            )
        elif handler_cfg['type'] == 'console':
            handler = logging.StreamHandler()

        handler.setFormatter(handler_cfg['formatter'])
        handler.setLevel(level=handler_cfg['level'])
        logger.addHandler(handler)

    return logger


logger = logger_handler("my_logger")


if __name__ == '__main__':
    logger.info("test")
