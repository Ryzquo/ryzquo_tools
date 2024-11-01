#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# 信号相关工具
import math
import os
import sys

import numpy as np

from scipy import signal

# 添加根目录
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import ryzquo_tools.math_tools as rmt


def find_peaks(data, min_distance=None, fs=360):
    """
    寻找峰值(峰值检测)
    :param data:数据
    :param min_distance:两具峰之间的最短距离默认 0.1*fs
    :param fs:采样率
    :return: 峰值和其位置
    """
    if min_distance is None:
        min_distance = math.ceil(0.1 * fs)

    peaks, locs = [], []

    # 开始找下一个峰值后的计数器, 也可以表示峰的间隔, 大于min_distance就认为已找到一个峰
    peak_interval = 0
    last_val = 0
    temp_val, temp_idx = 0, 0
    for idx, val in enumerate(data):
        # 如果找到峰就开始累加, 但实际开始累加是在找到真峰值(找到峰值的if不成立)后
        if peak_interval > 0:
            peak_interval += 1
        # 找到峰值
        if val > last_val and val > temp_val:
            temp_val = val
            temp_idx = idx
            peak_interval = 1
        # 无更大值且当前值小于峰值的一半, 则记录一个峰值
        elif val < temp_val//2 or peak_interval > min_distance:
            peaks.append(temp_val)
            locs.append(temp_idx)
            temp_val = 0
            temp_idx = 0
            peak_interval = 0
        last_val = val

    return peaks, locs


def moving_window_average(data, fs=360):
    """
    移动窗口积分均值
    y(nT) = (1/N)[x(nT-(N - 1)T)+ x(nT - (N - 2)T)+...+x(nT)]
    :param data:数据
    :param fs:采样率
    :return:
    """
    # 150ms的窗口
    win_width = math.ceil(0.15 * fs)
    # 卷积后除窗口大小, 得到平均值
    return np.array([
        val / win_width for val in rmt.conv_1d(data, [1] * win_width)
    ])


def derivative(data):
    """
    计算离散信号导数
    H(z) = (1/8T)(-z^(-2) - 2z^(-1) + 2z + z^(2))
    :param x:数据
    :return:
    """
    coef = [-1, -2, 0, 2, 1]
    return rmt.conv_1d(data, kernel=coef)


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
    return np.array(signal.filtfilt(b, a, data))


if __name__ == '__main__':
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

    res = moving_window_average(res, fs=fs)

    peaks, locs = find_peaks(res)
    print(peaks)
    print(locs)

    # print(res)
    # print(len(res))
