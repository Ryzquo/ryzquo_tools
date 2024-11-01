#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# 信号相关工具

import os
import sys

from scipy import signal

# 添加根目录
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import ryzquo_tools.math_tools as rmt


def derivative(x):
    """
    计算离散信号导数
    H(z) = (1/8T)(-z^(-2) - 2z^(-1) + 2z + z^(2))
    :param x:数据
    :return:
    """
    coef = [-1, -2, 0, 2, 1]
    return rmt.conv_1d(x, kernel=coef)


def bandpass_filter(data, fs, low=5, high=15):
    """
    带通滤波
    :param data:数据
    :param fs:采样率
    :param low:低截止频率
    :param high:高截止频率
    :return:滤波后信号
    """
    b, a = signal.butter(3, [low, high], btype='bandpass', fs=fs)
    return signal.filtfilt(b, a, data)


if __name__ == '__main__':
    import numpy as np

    fs = 360  # 采样频率
    t = np.linspace(0, 1, fs, endpoint=False)
    signal_data = (
            0.5 * np.sin(2 * np.pi * 5 * t) +
            0.5 * np.sin(2 * np.pi * 50 * t) +
            1.0 * np.sin(2 * np.pi * 120 * t) +
            0.5 * np.sin(2 * np.pi * 300 * t)
    )

    print(signal_data.shape)
    res = bandpass_filter(data=signal_data, fs=fs)
    print(res)
