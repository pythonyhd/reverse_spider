# -*- coding: utf-8 -*-
from functools import singledispatch


def connect_basic(address):
    """原始简单粗暴的写法，需要众多if-elif-else结构"""
    if isinstance(address, str):
        ip, port = address.split(':')
        print(f'字符串格式，IP是：{ip}, 端口是：{port}')
    elif isinstance(address, tuple):
        ip, port = address
        print(f'元组格式，IP是：{ip}, 端口是：{port}')
    else:
        print('地址格式不正确')


@singledispatch
def connect(address):
    print(f'传输的参数类型为:{type(address)}--不是有效的类型')


@connect.register
def _(address: str):
    ip, port = address.split(":")
    print(f'参数为字符串，IP是：{ip}, 端口是：{port}')


@connect.register
def _(address: tuple):
    ip, port = address
    print(f'参数为元组，IP是：{ip}, 端口是：{port}')


if __name__ == '__main__':
    # connect_basic('110.110.110.110:8888')
    # connect_basic(('110.110.110.110', 8888))
    # connect_basic(8888)
    connect('123.45.32.18:8080')
    connect(('123.45.32.18', 8080))
    connect(123)