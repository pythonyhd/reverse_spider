# -*- coding: utf-8 -*-


BOT_NAME = 'credit_china'

SPIDER_MODULES = ['credit_china.spiders']
NEWSPIDER_MODULE = 'credit_china.spiders'
COMMANDS_MODULE = 'credit_china.commands'


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
scrapy 基本配置
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
ROBOTSTXT_OBEY = False
LOG_LEVEL = "INFO"
RANDOM_UA_TYPE = "random"

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
数据存储 相关配置
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# 存储到mongodb
MONGODB_HOST = '127.0.0.1'
MONGODB_NAME = 'credit_china'  # 数据库名

# 存储到MySQL
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_NAME = 'credit_china'  # 数据库名
MYSQL_CHARSET = 'utf8'

# redis 基础配置
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = ""
REDIS_DB = 4
REDIS_PARAMS = {
    "password": "",
    "db": 4,
}

# redis 代理池配置
REDIS_PROXIES_HOST = '117.78.35.12'
REDIS_PROXIES_PORT = 6379
REDIS_PROXIES_PASSWORD = ''
REDIS_PROXIES_DB = 15