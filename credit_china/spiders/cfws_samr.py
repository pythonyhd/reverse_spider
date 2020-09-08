# -*- coding: utf-8 -*-
import base64
import json
import logging
import os
import re

import jsonpath
import scrapy

from credit_china.config import cfws_settings
from credit_china.work_utils.process_js import process_cfws

logger = logging.getLogger(__name__)


class CfwsSamrSpider(scrapy.Spider):
    name = 'cfws_samr'
    allowed_domains = ['cfws.samr.gov.cn']

    search_url = 'http://cfws.samr.gov.cn/queryDoc'  # 列表搜索链接
    index_url = 'http://cfws.samr.gov.cn/getDoc'  # 详情页url
    file_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + r'/files/'

    custom_settings = cfws_settings

    def start_requests(self):
        """搜索入口"""
        ciphertext = process_cfws()
        form_data = {
            "pageSize": "5",
            "pageNum": "1",
            "queryCondition": '[]',  # 搜素条件，需要添加各种条件
            "sortFields": "23_s:asc,16_s:asc",
            "ciphertext": str(ciphertext),
        }
        yield scrapy.FormRequest(url=self.search_url, formdata=form_data, meta={'form_data': form_data})

    def parse(self, response):
        """列表解析，翻页请求"""
        form_data = response.meta.get('form_data')
        # 解析
        results = json.loads(response.text)
        resultList = results.get('result').get('queryResult').get('resultList')
        if resultList:
            for result in resultList:
                cf_content = result.get('7', '')  # 处罚内容
                oname = result.get('30', '').strip()  # 当事人名称
                ws_nr_txt = json.dumps(result, ensure_ascii=False)
                rowkey = result.get('rowkey')  # PDF详情
                first_item = dict(oname=oname, cf_content=self.process_result(cf_content), ws_nr_txt=ws_nr_txt)
                ciphertext = process_cfws()
                form_data = {
                    'ciphertext': str(ciphertext),
                    'docid': str(rowkey),
                }
                meta_data = {'first_item': first_item}
                yield scrapy.FormRequest(url=self.index_url, formdata=form_data, callback=self.parse_detail, meta=meta_data, priority=5)

        else:
            logger.info('列表页获取失败')
        # 列表翻页，一个条件最多只能到第5页
        is_first = response.meta.get('is_first', True)
        resultCount = jsonpath.jsonpath(results, expr=r'$..result.queryResult.resultCount')
        if is_first and int(resultCount[0]) > 1:
            total_page = int(int(resultCount[0]) / 5) if int(resultCount[0]) % 5 == 0 else int(int(resultCount[0]) / 5) + 1
            total_page = 5 if total_page > 5 else total_page
            for page in range(2, total_page + 1):
                ciphertext = process_cfws()
                form_data['pageNum'] = str(page)
                form_data['ciphertext'] = str(ciphertext)
                _meta = {'is_first': False, 'form_data': form_data}
                yield scrapy.FormRequest(url=self.search_url, formdata=form_data, meta=_meta, priority=3)

    def parse_detail(self, response):
        """解析详情页"""
        first_item = response.meta.get('first_item')
        # 解析
        results = json.loads(response.text)
        result = results.get('result')
        cf_wsh = result.get('i0', '')  # 文书号
        cf_jdrq = result.get('i1', '')  # 处罚日期
        cf_xzjg = result.get('i3', '')  # 处罚机关
        cf_cflb = result.get('i4', '')  # 处罚种类
        cf_yj = result.get('i5', '')  # 处罚依据
        content = result.get('i7', '')  # pdf文件内容
        files = self.get_pdf(cf_wsh, content)
        second_item = dict(cf_wsh=cf_wsh, cf_jdrq=cf_jdrq, cf_xzjg=cf_xzjg, cf_cflb=cf_cflb, cf_yj=cf_yj, file_path=self.file_path + cf_wsh)
        item = {**first_item, **second_item}
        yield item

    def process_result(self, text: str) -> str:
        """处理特殊字符"""
        if text:
            text = re.sub('\r|\n|\t|\s', '', text)
            return text

    def get_pdf(self, filename: str, string: str):
        """存储PDF文件"""
        content = base64.b64decode(string)
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)
        with open(self.file_path + filename + r'.pdf', 'wb') as file:
            file.write(content)


# PDF解析方法，字体文件不全解析容易报错，根据情况下载所需的字体
'''
from pdfminer.pdfparser import PDFParser, PDFDocument, PDFSyntaxError
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox


def parse_pdf(self, response):
    """解析PDF文件"""
    # 用文件对象来创建一个pdf文档分析器
    praser = PDFParser(BytesIO(response.body))
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器 与文档对象
    praser.set_document(doc)
    doc.set_parser(praser)
    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()
    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf 资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        contents_list = []
        # 循环遍历列表，每次处理一个page的内容
        for page in doc.get_pages():  # doc.get_pages() 获取page列表
            # 接受该页面的LTPage对象
            interpreter.process_page(page)
            # 这里layout是一个LTPage对象 里面存放着
            # 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
            # 想要获取文本就获得对象的text属性
            layout = device.get_result()
            for index, out in enumerate(layout):
                if isinstance(out, LTTextBox):
                    contents = out.get_text().strip()
                    contents_list.append(contents)
        return contents_list
    
        
@classmethod
def process_datetime(cls, timestamp):
    """
    处理10位时间戳的静态方法
    :param timestamp:时间戳
    :return:格式化的时间
    """
    time_local = time.localtime(timestamp)
    result = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return result
    
    
# md5加密方法
def get_md5_value(_str):
    if isinstance(_str, str):
        code_url = _str.encode("utf-8")
        m = hashlib.md5()
        m.update(code_url)
        return m.hexdigest()
    else:
        return None
'''