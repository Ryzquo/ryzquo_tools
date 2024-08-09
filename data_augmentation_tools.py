#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import cv2
import random

import numpy as np

from paddle import to_tensor
from paddle.io import Dataset, DataLoader, ComposeDataset
from PIL import Image


def color_filter_autumn(img):
    im_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    im_color = cv2.applyColorMap(im_gray, cv2.COLORMAP_AUTUMN)
    return im_color


def color_filter_bone(img):
    im_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    im_color = cv2.applyColorMap(im_gray, cv2.COLORMAP_BONE)
    return im_color


def color_filter_winter(img):
    im_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    im_color = cv2.applyColorMap(im_gray, cv2.COLORMAP_WINTER)
    return im_color


def apply_hue(img):

    low, high, prob = [-18, 18, 0.5]
    if np.random.uniform(0., 1.) < prob:
        return img


    delta = np.random.uniform(low, high)
    u = np.cos(delta * np.pi)
    w = np.sin(delta * np.pi)
    bt = np.array([[1.0, 0.0, 0.0], [0.0, u, -w], [0.0, w, u]])
    tyiq = np.array([[0.299, 0.587, 0.114], [0.596, -0.274, -0.321],
                     [0.211, -0.523, 0.311]])
    ityiq = np.array([[1.0, 0.956, 0.621], [1.0, -0.272, -0.647],
                      [1.0, -1.107, 1.705]])
    t = np.dot(np.dot(ityiq, bt), tyiq).T
    img = np.dot(img, t)
    img = np.array(img).astype(np.uint8)
    return img


def apply_saturation(img):
    low, high, prob = [0.5, 1.5, 0.5]
    if np.random.uniform(0., 1.) < prob:
        return img
    delta = np.random.uniform(low, high)

    gray = img * np.array([[[0.299, 0.587, 0.114]]], dtype=np.float32)
    gray = gray.sum(axis=2, keepdims=True)
    gray *= (1.0 - delta)
    img *= delta
    img += gray
    img = np.array(img).astype(np.uint8)
    return img


def apply_contrast(img):
    low, high, prob = [0.5, 1.5, 0.5]
    if np.random.uniform(0., 1.) < prob:
        return img
    delta = np.random.uniform(low, high)

    img *= delta
    img = np.array(img).astype(np.uint8)
    return img


def apply_brightness(img):
    low, high, prob = [0.5, 1.5, 0.5]
    if np.random.uniform(0., 1.) < prob:
        return img
    delta = np.random.uniform(low, high)

    img += delta
    img = np.array(img).astype(np.uint8)
    return img


def apply_h_flip(img):
    """
    图像水平翻转
    :param img:
    :return:
    """
    img = cv2.flip(img, 1)
    return img


def gen_random_ind():
    seed = random.random()
    if seed < 1 / 5:
        return 0
    elif 1 / 5 <= seed < 2 / 5:
        return 1
    elif 2 / 5 <= seed < 3 / 5:
        return 2
    elif 3 / 5 <= seed < 4 / 5:
        return 3
    else:
        return 4


color_maps = [
    apply_hue,
    apply_saturation,
    apply_contrast,
    apply_brightness,
    apply_h_flip
]


if __name__ == '__main__':
    pass
