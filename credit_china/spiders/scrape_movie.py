# -*- coding: utf-8 -*-
import json

import scrapy

from credit_china.config import movie_settings
from credit_china.work_utils.process_movie import get_token, get_id


class ScrapeMovieSpider(scrapy.Spider):
    name = 'scrape_movie'
    custom_settings = movie_settings

    def start_requests(self):
        """请求列表页"""
        token = get_token(['/api/movie'])
        url = 'https://dynamic6.scrape.cuiqingcai.com/api/movie/?limit=10&offset=0&token={}'.format(token)
        yield scrapy.Request(url)

    def parse(self, response):
        """列表页解析+列表页翻页"""
        # 列表解析
        results = json.loads(response.text)
        if not results:
            return
        res_list = results.get('results')
        for data in res_list:
            uuid = data.get('id', '')
            detail_arg = get_id(uuid)
            token = get_token(['/api/movie/{}'.format(detail_arg)])
            link = 'https://dynamic6.scrape.cuiqingcai.com/api/movie/{id}/?token={token}'.format(id=detail_arg, token=token)
            yield scrapy.Request(link, callback=self.parse_detail, priority=3)

        # 列表翻页
        count = results.get('count')
        is_first = response.meta.get('is_first', True)
        page_count = int(int(count) / 10) if int(count) % 10 == 0 else int(int(count) / 10) + 1
        if is_first and page_count > 1:
            for page in range(1, page_count):
                url = response.url.replace('offset=0', 'offset={}'.format(page * 10))
                yield scrapy.Request(url, meta={'is_first': False}, priority=2)

    def parse_detail(self, response):
        """解析详情页"""
        results = json.loads(response.text)
        name = results.get('name', '')
        alias = results.get('alias', '')
        score = results.get('score', '')
        print(dict(name=name, alias=alias, score=score))
