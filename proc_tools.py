#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import psutil
import subprocess

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import ryzquo_tools.path_tools as rpt


def check_back_python(file_name, python_path=None):
    """
    后台启动指定python程序
    """
    if python_path is None:
        python_path = "python3"

    file_path = rpt.join_path(rpt.get_root(__file__), file_name)

    if not os.path.exists(file_path):
        raise Exception("后台脚本文件不存在")

    # 获取正在运行的python脚本
    py_lists = get_python_processes()
    for py_iter in py_lists:
        # 检测是否存在后台运行的脚本
        if file_name in py_iter[1]:
            return
    else:
        # 使用subprocess开启后台脚本，后台运行, 忽略输入输出
        print("开启{}脚本, 后台运行中, 请等待".format(file_name))
        cmd_str = f"{python_path} {file_path} &"
        # shell=True告诉subprocess模块在运行命令时使用系统的默认shell.
        # 这使得可以像在命令行中一样执行命令，包括使用通配符和其他shell特性
        subprocess.Popen(cmd_str, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1)
        # 这里的> /dev/null 2>&1将标准输出和标准错误都重定向到/dev/null，实现与之前subprocess.Popen相同的效果
        # os.system(cmd_str + " > /dev/null 2>&1")


def get_python_processes():
    """
    获取所有python进程
    """
    python_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if 'python' in proc.info['name'].lower() \
                    and proc.info['cmdline'] is not None \
                    and len(proc.info['cmdline']) > 1 \
                    and len(proc.info['cmdline'][1]) < 100:
                info = [proc.info['pid'], proc.info['cmdline'][1]]
                python_processes.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # for process in python_processes:
    #     print(process)
    # print("    ")

    return python_processes


if __name__ == '__main__':
    pass
