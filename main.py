# -*- coding: utf-8 -*-
from scrapy.cmdline import execute


# 信用陕西-行政处罚-更新前5页
# execute("scrapy crawl credit_shanxi".split())
# 中国市场监管行政处罚文书网
# execute("scrapy crawl cfws_samr".split())
# 阿里巴巴文学小说
# execute("scrapy crawl aliwx".split())
# 电影网站，利用webpack前后端分离打包
# execute("scrapy crawl scrape_movie".split())
# 二郎查，简单的MD5请求头参数加密
# execute("scrapy crawl erlangcha".split())
# 夜幕论坛，集成selenium
# execute("scrapy crawl nightteam".split())
# 80电影网，简单的分布式
# execute("scrapy crawl erlangcha".split())
# 毛毛租
execute("scrapy crawl maomaozu".split())
# 一次运行所有spider
# execute("scrapy crawlall".split())