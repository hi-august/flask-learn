# coding=utf-8

import hashlib
import redis
from flask import current_app

_redis_pool_list = {}

def get_redis(name):
    if name not in _redis_pool_list:
        info = current_app.config["REDIS_SETTIGNS"][name]
        pool = redis.ConnectionPool(host=info["host"],
                                    port=info["port"],
                                    db=info["db"],
                                    socket_timeout=5)
        _redis_pool_list[name] = pool
    return redis.Redis(connection_pool=_redis_pool_list[name])

def md5(msg):
    md5 = hashlib.md5(msg.encode('utf-8')).hexdigest()
    return md5


