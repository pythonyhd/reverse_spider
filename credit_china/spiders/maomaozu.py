# -*- coding: utf-8 -*-
import json
import time

import scrapy

from credit_china.config import maomao_settings
from credit_china.work_utils.process_js import process_maomaozu


class MaomaozuSpider(scrapy.Spider):
    name = 'maomaozu'
    url = 'https://www.maomaozu.com/index/build.json'

    custom_settings = maomao_settings

    def start_requests(self):
        """爬虫入口"""
        expire = int(round(time.time() * 1000))
        form_data = {"Type": "0", "page": "1", "expire": str(expire)}
        _meta = {'form_data': form_data}
        yield scrapy.FormRequest(self.url, formdata=form_data, meta=_meta)

    def parse(self, response):
        """解析列表，列表翻页"""
        form_data = response.meta.get('form_data')
        # 解析
        datas = json.loads(process_maomaozu(response.text))
        lists = datas.get('list')
        for result in lists:
            SourceID = result.get('SourceID', '')  # 详情页参数
            Name = result.get('Name', '')  # 名称
            first_item = dict(name=Name, detail_id=SourceID)
            print(first_item)
        # 翻页
        total = datas.get('total')  # 所有房源，总数，每页10条
        pages = int(int(total) / 10) if int(total) % 10 == 0 else int(int(total) / 10) + 1
        is_first = response.meta.get('is_first', True)
        if is_first and pages > 1:
            for page in range(2, pages + 1):
                form_data['page'] = str(page)
                meta_data = {'form_data': form_data, 'is_first': False}
                yield scrapy.FormRequest(self.url, formdata=form_data, meta=meta_data)

