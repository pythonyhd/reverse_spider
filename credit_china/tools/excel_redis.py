# -*- coding: utf-8 -*-
import os
import pandas as pd
import redis


HOST = '114.115.201.98'
PORT = 6379
PWD = 'axy@2019'
DB = 3
excel_path = os.path.dirname(os.path.abspath(__file__))


class ExcelRedis(object):
    redis_client = redis.StrictRedis(host=HOST, port=PORT, password=PWD, db=DB)

    @classmethod
    def read_excel(cls):
        """pandas读取excel数据，存储到redis"""
        results = os.walk(excel_path)  # generator对象
        for parents, dirnames, filenames in results:
            for filename in filenames:
                file_path_generator = pd.ExcelFile(os.path.join(parents, filename))
                for i in range(len(file_path_generator.sheet_names)):
                    # print(file_path_generator.sheet_names)
                    sheet_name = file_path_generator.sheet_names[int("{}".format(i))]
                    # print(sheet_name)
                    data = file_path_generator.parse(sheet_name)
                    for item in data.values:
                        # print(item)
                        cls.redis_client.sadd('court:name', item[0])


if __name__ == '__main__':
    # print(excel_path)
    ExcelRedis.read_excel()