# -*- coding: utf-8 -*-


def iter_x(x):
    """遍历字典或者列表"""
    if isinstance(x, dict):
        for key, value in x.items():
            yield (key, value)
    elif isinstance(x, list):
        for index, value in enumerate(x):
            yield (index, value)


def flat(x):
    """压平字典"""
    for key, value in iter_x(x):
        if isinstance(value, (dict, list)):
            for k, v in flat(value):
                k = f'{key}_{k}'
                yield (k, v)
        else:
            yield (key, value)