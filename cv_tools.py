#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import cv2
import base64

import numpy as np

from typing import Tuple, Union, List, Any
from PIL import Image

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import ryzquo_tools.path_tools as rpt


# ==== opencv <--> base64
def cv2base64(image):
    """
    opencv 转 base64
    """
    return str(base64.b64encode(cv2.imencode(".jpg", image)[1]))[2:-1]


def base642cv(base64_code):
    """
    base64 转 opencv
    """
    return cv2.imdecode(
        np.fromstring(base64.b64decode(base64_code), np.uint8),
        cv2.COLOR_RGB2BGR
    )


# ==== opencv <--> PIL Image
def cv2PIL(image):
    """
    opencv 转 PIL Image
    :param image:
    :return:
    """
    return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))


def PIL2cv(image):
    """
    PIL Image 转 opencv
    :param image:
    :return:
    """
    if image.mode != 'RGB':
        image = image.convert('RGB')
    return cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)


def capture_video(
        cap_num=None,
        visualize=True,
        callback=None,
) -> None:
    """
    调用相机, 执行回调函数
    :param cap_num: 相机号
    :param visualize: 是否可视化
    :param callback: 回调函数
    :return:
    """
    if cap_num is None:
        cap_num = 0

    cap = cv2.VideoCapture(cap_num)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if callback:
            frame = callback(frame)

        if visualize:
            cv2.imshow('frame', frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


def record_video(
        cap_num=None,
        save_name=None,
        save_path=None,
        fourcc=None,
        visualize=False,
        is_horizontally_flipped=True
) -> None:
    if cap_num is None:
        cap_num = 0
    if save_name is None:
        save_name = "video"
    if save_path is None:
        save_path = rpt.get_root(__file__)
    if fourcc is None:
        fourcc = "mp4v"

    cap = cv2.VideoCapture(0)

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(
        f"{rpt.join_path(save_path, save_name)}.mp4",
        cv2.VideoWriter_fourcc(*f"{fourcc}"),
        fps, (width, height)
    )

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        if is_horizontally_flipped:
            frame = cv2.flip(frame, 1)

        out.write(frame)

        if visualize:
            cv2.imshow("frame", frame)

        if cv2.waitKey(fps) == 27:
            break

    out.release()
    cap.release()
    cv2.destroyAllWindows()


def get_contours(
        img_ori: np.ndarray,
        threshold_canny: tuple = (100, 100),
        kernel_size: tuple = (5, 5),
        threshold_area: 'int>0' = 1000, filter: 'int>0' = 0,
        visualize: bool = False
) -> Union[Tuple[List[Tuple[int, Any, Any, Any, Any]], Any], Tuple[List[Tuple[int, Any, Any, Any, Any]], None]]:
    """
    查找图像中的轮廓
    :param img_ori: 图像
    :param threshold_canny: canny的两个阈值
    :param kernel_size: 高斯模糊卷积核大小
    :param threshold_area: 轮廓面积阈值, 大于0
    :param filter: 按点数过滤, 大于0
    :param visualize: 可视化
    :return:
        contours: [(len(approx), area, approx, bbox, contour), ...]
            过滤后的轮廓
        img:
            如果可视化为画出轮廓的图像, 否则为None
    """
    img = np.copy(img_ori)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, kernel_size, sigmaX=1)
    img_canny = cv2.Canny(img_blur, *threshold_canny)

    # cv2.imshow("canny", img_canny)

    kernel = np.ones(kernel_size)
    img_dial = cv2.dilate(img_canny, kernel, iterations=3)
    img_thre = cv2.erode(img_dial, kernel, iterations=2)

    contours = cv2.findContours(img_thre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    final_contours = []
    for contour in contours:
        # 面积
        area = cv2.contourArea(contour)
        if area > threshold_area:
            arc_length = cv2.arcLength(contour, True)
            # 多边形拟合
            approx = cv2.approxPolyDP(contour, 0.02 * arc_length, True)
            # 最小外接矩阵
            bbox = cv2.boundingRect(approx)
            # 过滤
            if filter > 0:
                if len(approx) == filter:
                    final_contours.append((len(approx), area, approx, bbox, contour))
            else:
                final_contours.append((len(approx), area, approx, bbox, contour))
    # 按面积大小排序
    final_contours = sorted(final_contours, key=lambda x: x[1], reverse=True)

    rets = (final_contours, None)

    # 可视化
    if visualize:
        for contour in final_contours:
            cv2.drawContours(img, contour[4], -1, (0, 255, 0), 2)
        rets = (final_contours, img)

    return rets


def reorder(points):
    """
    提取四个角点
    :param points: 点集
    :return: 四个角点: 左上, 右上, 右下, 左下
    """
    # 转为若干个坐标
    points = points.reshape((-1, 2))

    # 计算每个坐标x与y的和
    add = points.sum(1)
    # 和最小的为左上角，最大为右下角
    left_top = points[np.argmin(add)]
    right_bottom = points[np.argmax(add)]

    # 计算每个坐标x与y的差值
    diff = np.diff(points, axis=1)
    # 差值最小的为右上角，最大的为左下角
    right_top = points[np.argmin(diff)]
    left_bottom = points[np.argmax(diff)]

    return np.array([left_top, right_top, right_bottom, left_bottom], np.int32)


def warp_img(
        img, points, points_target=None,
        img_size: tuple = None, pad=None
):
    """
    透视变换
    :param img: 源图像
    :param points: 点集
    :param points_target: 目标图像四个角点 [[0, 0], [iw, 0], [iw, ih], [0, ih]]
    :param img_size: 目标图像大小
    :param pad: 左上角不需要的区域
    :return: 变换后的图像
    """
    iw, ih = img_size[:2]

    if points_target is None:
        points_target = [[0, 0], [iw, 0], [iw, ih], [0, ih]]

    if img_size is None:
        img_size = (100, 100)

    if pad is None:
        pad = 20

    # 取四个角点
    points = reorder(points)

    # 获取变换矩阵
    pts1 = np.float32(points)
    pts2 = np.float32(points_target)
    matrix = cv2.getPerspectiveTransform(pts1, pts2)

    img_warp = cv2.warpPerspective(img, matrix, img_size)
    img_warp = img_warp[pad:ih - pad, pad:ih - pad]

    return img_warp


def calculated_distance(
        pts1: Tuple[(int, int)],
        pts2: Tuple[(int, int)]
) -> float:
    """
    计算两点间的距离
    :param pts1: 点1, (x, y)
    :param pts2: 点2, (x, y)
    :return: 距离
    """
    return ((pts2[0] - pts1[0]) ** 2 + (pts2[1] - pts1[1]) ** 2) ** 0.5


def filter_color_hsv(img, hsv):
    """
    通过hsv过滤颜色
    :param img: 图像 BGR
    :param hsv: hsv值
    :return:
    """
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([*hsv[:3]])
    upper = np.array([*hsv[3:]])
    mask = cv2.inRange(img_hsv, lower, upper)
    img_result = cv2.bitwise_and(img, img, mask=mask)
    return img_result


def get_roi(img, contours):
    """
    根据传入的轮廓返回roi区域
    :param img: 图像
    :param contours: 轮廓
    :return: roi区域列表
    """
    roi_list = []
    for contour in contours:
        x, y, w, h = contour[3]
        roi_list.append(img[y:y + h, x:x + w])
    return roi_list


if __name__ == '__main__':
    record_video(
        cap_num=0, save_name="test"
    )
