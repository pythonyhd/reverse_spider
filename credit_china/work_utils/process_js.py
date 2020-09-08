# -*- coding: utf-8 -*-
import os
import time

import execjs

credit_path = os.path.dirname(os.path.dirname(__file__)) + r'/templates/js/credit_shanxi.js'
cfws_path = os.path.dirname(os.path.dirname(__file__)) + r'/templates/js/cfws_samr.js'
aliwx_path = os.path.dirname(os.path.dirname(__file__)) + r'/templates/js/aliwx.js'
erlang_path = os.path.dirname(os.path.dirname(__file__)) + r'/templates/js/erlangcha.js'
mao_path = os.path.dirname(os.path.dirname(__file__)) + r'/templates/js/maomaozu.js'


def statistic_time(function):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = function(*args, **kwargs)
        end_time = time.time()
        print('Function:{name} Finished, spent time: {time:.2f}'.format(name=function.__name__,
                                                                        time=end_time - start_time))
        return result

    return wrapper


def process_resp(_str: str):
    """信用陕西响应信息解密"""
    with open(credit_path, 'r', encoding='utf-8') as f:
        pattern = execjs.compile(f.read())
        result = pattern.call('decode_response_test', _str)
        return result


def process_params(_id: str):
    """信用陕西加密详情页参数"""
    with open(credit_path, 'r', encoding='utf-8') as f:
        pattern = execjs.compile(f.read())
        result = pattern.call('encrypt_params', _id)
        return result


@statistic_time
def process_cfws():
    """中国市场监管行政处罚文书网cipher参数"""
    with open(cfws_path, 'r', encoding='utf-8') as f:
        pattern = execjs.compile(f.read())
        result = pattern.call('cipher')
        return result


def process_aliwx(content: str) -> str:
    """阿里文学详情JS解析"""
    with open(aliwx_path, 'r', encoding='utf-8') as f:
        pattern = execjs.compile(f.read())
        result = pattern.call('_decodeCont', content)
        return result


def process_headers(page: str):
    """
    处理二郎查请求头参数
    :param page: ；"page=1"
    :return: MD5加密值
    """
    with open(erlang_path, 'r', encoding='utf-8') as f:
        pattern = execjs.compile(f.read())
        return pattern.call('getHeaders', page)


def process_maomaozu(data: str):
    """
    处理毛毛租响应结果
    :param data: 响应内容
    :return: 解密后的json数据
    """
    with open(mao_path, 'r', encoding='utf-8') as f:
        pattern = execjs.compile(f.read())
        return pattern.call('get_response', data)


if __name__ == '__main__':
    _str = "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\nbNnRldjsqiI="
    resp = process_resp(_str)
    # print(f'解密：{resp}')
    _id = '35b4ba3a60f5bcc4b982138aaa5437cd'
    p = process_params(_id)
    print(p)

    cipher = process_cfws()
    print(f'cipher参数:{cipher}')

    headers = process_headers('page=1')
    print(f'二郎查headers={headers}')
