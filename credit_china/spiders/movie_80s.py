# -*- coding: utf-8 -*-
from urllib.parse import urljoin

import scrapy

from credit_china.config import movies80_settings


class Movie80sSpider(scrapy.Spider):
    name = 'movie_80s'
    redis_key = "movies:start_urls"
    custom_settings = movies80_settings

    def parse(self, response):
        # 解析
        name = response.xpath('//ul[@class="me1 clearfix"]/li/a/@title').getall()
        print(name)
        # 翻页
        next_url = response.xpath('//a[contains(.,"下一页")]/@href').get()
        if next_url:
            url = urljoin('https://www.80s.tw/', next_url)
            yield scrapy.Request(url)