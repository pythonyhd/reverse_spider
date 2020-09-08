# -*- coding: utf-8 -*-
import json

import scrapy

from credit_china.config import erlang_settings
from credit_china.work_utils.process_js import process_headers


class ErlangchaSpider(scrapy.Spider):
    name = 'erlangcha'

    custom_settings = erlang_settings

    def start_requests(self):
        """请求列表页"""
        url = 'https://www.erlangcha.com/api/storiesList?page=1'
        headers = process_headers('page=1')
        yield scrapy.Request(url, headers=headers)

    def parse(self, response):
        """解析列表页，列表页翻页"""
        # 数据解析
        results = json.loads(response.text)
        data = results.get('data', {})
        if not data:
            return
        content = data.get('content', [])
        for result in content:
            stories_logo = result.get('stories_logo', '')  # 店铺商标
            stories_name = result.get('stories_name', '')  # 店铺
            of_company = result.get('of_company', '')  # 所属公司
            source = result.get('source', '1')  # 来源
            source = '鲁班' if str(source) == '1' else ''
            shop_num = result.get('shop_num', '')  # 在售商品
            today_sales = result.get('today_sales', '')  # 昨日销量
            three_sales = result.get('three_sales', '')  # 前三天
            seven_sales = result.get('seven_sales', '')  # 前七天
            month_sales = result.get('month_sales', '')  # 累计销量
            new_five = result.get('new_five')  # 店铺新品
            stories_link = result.get('stories_link', '')  # 店铺链接
            first_item = dict(
                stories_logo=stories_logo, stories_name=stories_name, of_company=of_company, source=source,
                shop_num=shop_num, today_sales=today_sales, three_sales=three_sales, seven_sales=seven_sales,
                month_sales=month_sales, new_five=new_five, stories_link=stories_link,
            )
            yield first_item
        # 列表翻页
        pageNum = data.get('pageNum')  # 总页码数
        is_first = response.meta.get('is_first', True)
        if is_first and int(pageNum) > 1:
            for page in range(2, int(pageNum) + 1):
                url = 'https://www.erlangcha.com/api/storiesList?page={}'.format(page)
                headers = process_headers('page={}'.format(page))
                yield scrapy.Request(url=url, headers=headers, meta={'is_first': False})