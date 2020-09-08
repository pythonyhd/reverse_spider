# -*- coding: utf-8 -*-
import redis


class RedisClient(object):
    def __init__(self, host, port, password, db):
        self.redis_pool = redis.ConnectionPool(host=host, port=port, password=password, db=db)
        self.redis = redis.Redis(connection_pool=self.redis_pool)

    def redis_client(self):
        return self.redis