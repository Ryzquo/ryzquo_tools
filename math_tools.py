#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 数学计算相关工具

import math

import numpy as np


def conv_1d(x, kernel):
    """
    一维卷积
    :param x: 一维数据
    :param kernel: 卷积核
    :return:
    """
    len_x = len(x)
    len_k = len(kernel)

    if len(kernel) > len(x):
        x = np.concatenate((x, np.zeros(len_k-len_x)))

    result = []
    for i in range(len(x)):
        if i+len_k <= len(x):
            temp = x[i:i+len_k]
        else:
            temp = np.concatenate((x[i:len(x)-1], x[:len_k-len(x)+1+i]))
        result.append(-sum(temp*kernel))

    return np.array(result[:len_x])


def inc(x, limit):
    """
    自增[0, limit)
    :param x: 值
    :param limit: 临界
    :return:
    """
    return (x + 1) % limit


def dec(x, limit):
    """
    自减[0, limit)
    :param x: 值
    :param limit: 临界
    :return:
    """
    return (x - 1) % limit


def angle2radian(angle):
    """
    角度转弧度
    """
    return angle * (math.pi / 180)


def radian2angle(radians):
    """
    角度转弧度
    """
    return radians * (180 / math.pi)


if __name__ == '__main__':
    # 测试一维卷积
    import numpy as np
    from matplotlib import pyplot as plt
    fs = 360
    t = np.linspace(0, 1, fs, endpoint=False)
    signal_data = np.array([
        0.5 * np.sin(2 * np.pi * 5 * t) +
        0.5 * np.sin(2 * np.pi * 50 * t) +
        1.0 * np.sin(2 * np.pi * 120 * t) +
        0.5 * np.sin(2 * np.pi * 300 * t)
    ])[0]
    # coef = [-2, -1, 0, 1, 2]
    coef = [-1, -2, 0, 2, 1]
    res = conv_1d(signal_data, coef)
    print(res)
    print(len(res))
    plt.figure(1)
    plt.plot(t, signal_data, 'r')
    plt.figure(2)
    plt.plot(t, res, 'b')
    plt.show()

    # # 测试自增, 自减
    # j = 0
    # for i in range(20):
    #     j = inc(j, 5)
    #     # j = dec(j, 5)
    #     print(j)
