# -*- coding: utf-8 -*-
import json
import logging
import re
from functools import reduce
from urllib.parse import urljoin

import scrapy

from credit_china.config import aliwx_settings
from credit_china.work_utils.process_js import process_aliwx

logger = logging.getLogger(__name__)


class AliwxSpider(scrapy.Spider):
    name = 'aliwx'
    start_urls = ['https://www.aliwx.com.cn/store']

    custom_settings = aliwx_settings

    def parse(self, response):
        """获取所有小说链接"""
        selector = scrapy.Selector(text=response.text)
        # 列表到详情url
        index_url = selector.css('a[class=clear]::attr(href)').getall()
        for link in index_url:
            url = urljoin(response.url, link)
            yield scrapy.Request(url=url, callback=self.parse_index)

        # 翻页
        next_url = selector.css('a:contains("下一页")::attr(href)').get()
        if next_url:
            url = urljoin(response.url, next_url)
            yield scrapy.Request(url=url)

    def parse_index(self, response):
        """获取立即阅读页"""
        read_url = response.xpath('//a[contains(., "立即阅读")]/@href').get()
        if read_url:
            url = urljoin(response.url, read_url)
            yield scrapy.Request(url=url, callback=self.parse_detail, priority=3)
        else:
            logger.info('该书未授权')

    def parse_detail(self, response):
        """获取小说"""
        # 详情解析
        selector = scrapy.Selector(text=response.text)
        base_data = selector.css('i[class*=js-dataChapters]::text').get()
        base_data = json.loads(base_data)
        book_name = base_data.get('bookName')  # 书名
        author_name = base_data.get('authorName')  # 作者
        chapter_num = base_data.get('chapterNum')  # 章节数
        img_url = base_data.get('imgUrl')  # 图书图片
        word_count = base_data.get('wordCount')  # 文章字数
        cp_name = base_data.get('cpName')  # 是否原创
        any_uptime = base_data.get('anyUpTime')  # 开始更新时间
        last_instime = base_data.get('lastInsTime')  # 最后更新
        chapterList = base_data.get('chapterList')  # 所有章节
        for data in chapterList:
            volume_name = data.get('volumeName')  # 第几卷
            volumeList = data.get('volumeList')  # 所有章节列表
            for item in volumeList:
                chapter_name = item.get('chapterName').strip()  # 章节名
                chapter_word_count = item.get('wordCount')  # 章节字数
                contUrlSuffix = item.get('contUrlSuffix')  # 免费文章地址
                shortContUrlSuffix = item.get('shortContUrlSuffix')  # 收费文章地址
                novel_item = dict(
                    book_name=book_name, author_name=author_name, volume_name=volume_name,
                    chapter_name=chapter_name, cp_name=cp_name, chapter_num=chapter_num,
                    img_url=img_url, word_count=word_count, any_uptime=any_uptime,
                    last_instime=last_instime, chapter_word_count=chapter_word_count,
                )
                isFreeRead = item.get('isFreeRead')
                if isFreeRead:
                    free_url = urljoin('https://c13.shuqireader.com/pcapi/chapter/contentfree/', contUrlSuffix)
                    yield scrapy.Request(url=free_url, callback=self.parse_chapter, meta={'novel_item': novel_item}, priority=5)
                else:
                    money_url = urljoin('https://c13.shuqireader.com/sapi/chapter/contentshort/', shortContUrlSuffix)
                    yield scrapy.Request(url=money_url, callback=self.parse_chapter, meta={'novel_item': novel_item}, priority=5)

    def parse_chapter(self, response):
        """解析小说内容页"""
        novel_item = response.meta.get('novel_item')
        results = json.loads(response.text)
        novel_item['url'] = response.url
        re_parttern = re.compile(r'\r|\n|\t|\s')
        ChapterContent = results.get('ChapterContent')
        if ChapterContent:
            content = process_aliwx(ChapterContent)
            content = reduce(lambda x, y: x + y, [re_parttern.sub('', i) for i in content])
            novel_item['content'] = content.replace('<br/>', '')
            print(novel_item)
            # yield novel_item
        else:
            logger.info('数据获取失败')