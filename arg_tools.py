#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse


def get_argparse(description, **parsers):
    """
    获取命令行参数
    :param description: 描述
    :param parsers: 调用方式为 --参数名=参数值
        参数列表, 格式如下
        参数名={
            "type": str,
            "default": "train",
            "choices": ["train", "save", "infer"],
            "help": "model: train, save, infer",
            "required": False,
        }
    :return:
    """
    parser = argparse.ArgumentParser(description=description)

    for name, value in parsers.items():
        parser.add_argument(f"--{name}", **value)

    return parser


if __name__ == '__main__':
    args = get_argparse(
        description="cruise_cnn",
        model={
            "type": str,
            "default": "train",
            "choices": ["train", "save", "infer"],
            "help": "model: train, save, infer",
            "required": False,
        }
    ).parse_args()
    print(args.model)
