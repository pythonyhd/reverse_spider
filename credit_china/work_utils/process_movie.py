# -*- coding: utf-8 -*-
import base64
import hashlib
import time


def get_token(args: list):
    """
    列表页token加密逻辑
    先将 /api/movie 放到一个列表里面；
    列表中加入当前时间戳，10位；
    将列表内容用逗号拼接；
    将拼接的结果进行 SHA1 编码；
    将编码的结果和时间戳再次拼接；
    将拼接后的结果进行 Base64 编码。
    """
    timestamp = str(int(time.time()))
    args.append(timestamp)
    sign = hashlib.sha1(','.join(args).encode('utf-8')).hexdigest()
    return base64.b64encode(','.join([sign, timestamp]).encode('utf-8')).decode('utf-8')


def get_id(uuid):
    """详情页参数加密逻辑"""
    _str = 'ef34#teuq0btua#(-57w1q5o5--j@98xygimlyfxs*-!i-0-mb'
    return base64.b64encode((_str + str(uuid)).encode('utf-8')).decode('utf-8')


if __name__ == '__main__':
    args = ['/api/movie']
    token = get_token(args)
    print(f'token={token}')
    uuid = get_id(1)
    print(f'uuid={uuid}')


"""
HOOK 在代码运行过程中对某个方法进行重写，在原有方法前后加上自定义的代码，相当于在系统没有调用该函数前，钩子程序先捕获该消息
可以先得到控制权，这是钩子程序就可以加工处理该函数的执行行为。
"""
