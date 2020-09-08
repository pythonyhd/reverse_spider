# -*- coding: utf-8 -*-
import logging
import threading
import re
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin

import pymongo
import redis
import requests
from fake_useragent import UserAgent
from pyquery import PyQuery as pq

from credit_china import settings

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


class ScrapeSpider(object):
    headers = {"User-Agent": UserAgent().random}
    redis_client = redis.StrictRedis(host=settings.REDIS_PROXIES_HOST, port=settings.REDIS_PROXIES_PORT, password=settings.REDIS_PROXIES_PASSWORD, db=settings.REDIS_PROXIES_DB)
    redis_key = 'proxies'
    mongo_client = pymongo.MongoClient('mongodb://localhost:27017')
    db = mongo_client['movies']
    collection = db['movies']

    def download(self, url, max_retry=20):
        """通用爬取方法"""
        while max_retry > 0:
            proxy = self.get_proxy()
            try:
                resp = requests.get(url, headers=self.headers, proxies=proxy, timeout=15, allow_redirects=False)
                if resp.status_code in [200, 201, 202]:
                    return resp.text
                logging.error(f'响应不是200:{resp.status_code}')
            except Exception as e:
                logging.error(f'获取失败原因:{repr(e.args)}--开始重试')
                times = 20
                max_retry -= 1
                logging.info(f'抓取失败，开始第{times - max_retry}次重试--当前ip{proxy}--失败原因:{repr(e.args)}')
                if max_retry == 0:
                    logging.info('达到最大重试次数仍然失败')

    def scrape_index(self, page):
        """列表页抓取"""
        index_url = 'https://static1.scrape.cuiqingcai.com/page/{}'.format(page)
        logging.debug(f'列表url:{index_url}')
        return self.download(index_url)

    def parse_index(self, html):
        """列表解析，获取详情url，以生成器的方式返回详情url"""
        doc = pq(html)
        links = doc('.el-card .name')
        for link in links.items():
            href = link.attr('href')
            detail_url = urljoin('https://static1.scrape.cuiqingcai.com/', href)
            logging.debug(f'详情url:{detail_url}')
            yield detail_url

    def scrape_detail(self, url):
        """详情页抓取"""
        return self.download(url)

    def parse_deatil(self, html):
        """解析详情页"""
        doc = pq(html)
        cover = doc('img.cover').attr('src')
        name = doc('a > h2').text()
        categories = [item.text() for item in doc('.categories button span').items()]
        publish_date = doc('.info:contains(上映)').text()
        publish_date = re.search(r'(\d{4}-\d{2}-\d{2})', publish_date)
        publish_date = publish_date.group(1) if publish_date else None
        drama = doc('.drama p').text()
        score = doc('p.score').text()
        score = float(score) if score else None
        item = dict(name=name, cover=cover, categories=categories, publish_date=publish_date, score=score, drama=drama)
        return item

    def get_proxy(self):
        """获取代理IP"""
        proxy = self.redis_client.srandmember(self.redis_key)
        if proxy:
            proxies = {
                'http': 'http://{}'.format(proxy.decode('utf-8')),
                'https': 'https://{}'.format(proxy.decode('utf-8')),
            }
            return proxies
        else:
            logging.error('代理池枯竭')
            time.sleep(10)

    def main(self):
        for page in range(1, 11):
            index_html = self.scrape_index(page)
            detail_urls = self.parse_index(index_html)
            for detail_url in list(detail_urls):
                detail_html = self.scrape_detail(detail_url)
                item = self.parse_deatil(detail_html)
                self.save_data(item)
                print(item)

    def main_speed(self, page):
        print(f'{threading.current_thread().getName()}--正在爬取第：{page}页')
        index_html = self.scrape_index(page)
        detail_urls = self.parse_index(index_html)
        for detail_url in list(detail_urls):
            detail_html = self.scrape_detail(detail_url)
            item = self.parse_deatil(detail_html)
            self.save_data(item)
            # print(item)

    def save_data(self, item):
        """存储到mongodb数据库"""
        self.collection.update_one({'name': item.get('name')}, {'$set': item}, upsert=True)


if __name__ == '__main__':
    spider = ScrapeSpider()
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(spider.main_speed, range(1, 11))
    end_time = time.time()
    print(f'耗时:{end_time - start_time}')