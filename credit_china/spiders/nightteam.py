# -*- coding: utf-8 -*-
import logging
from urllib.parse import urljoin

import scrapy
from pydispatch import dispatcher
from scrapy import signals
from selenium import webdriver

logger = logging.getLogger(__name__)


class NightteamSpider(scrapy.Spider):
    name = 'nightteam'
    start_urls = ['https://bbs.nightteam.cn/']

    def __init__(self):
        self.browser = webdriver.Chrome()
        super(NightteamSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse(self, response):
        # 解析
        titles = response.xpath('//div[@class="media-body"]/div/a/text()').getall()
        print(titles)
        # 翻页
        link = response.xpath('//li[contains(.,"▶")]/a/@href').get()
        next_url = urljoin('https://bbs.nightteam.cn/', link)
        if next_url:
            yield scrapy.Request(next_url)
        else:
            logger.info('翻页完成')

    # 当爬虫关闭的时候关闭chrome
    def spider_closed(self, spider):
        logger.info("spider closed")
        self.browser.close()
