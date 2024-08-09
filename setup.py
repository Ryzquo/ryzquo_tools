#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="ryzquo_tools",
    version="1.0",
    author="ryzquo",
    author_email="ryzquo@gmail.com",
    description="工具集",
    packages=find_packages(),
    # 希望被打包的文件
    package_data={
        '': ['*.txt'],
        'bandwidth_reporter': ['*.txt']
    },
    # 不打包某些文件
    exclude_package_data={
        'bandwidth_reporter': ['*.txt']
    },
    # 表明当前模块依赖哪些包，若环境中没有，则会从pypi中下载安装
    install_requires=[],
)

if __name__ == '__main__':
    # print(find_packages())
    pass
