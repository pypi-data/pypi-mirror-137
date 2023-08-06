'''
db组件，主要用操作redis
'''
import redis
from proxy_pool.settings import *


class Reidis_client(object):
    def __init__(self):
        """
        考虑到：是否有密码
        """
        if PASSWORD:
            self.__db = redis.Redis(host=HOST, port=PORT, password=PASSWORD)
        else:
            self.__db = redis.Redis(host=HOST, port=PORT)

    def put(self, proxy):
        """
        添加一个代理到代理池
        :return:
        """
        self.__db.rpush(PROXYPOOL, proxy)

    def get(self, count=1):
        '''
        获取多个count个代理
        :return:
        '''
        proxies = self.__db.lrange(PROXYPOOL, 0, count - 1)
        self.__db.ltrim(PROXYPOOL, count, -1)
        return proxies

    def pop(self):
        # redis中存储的是bytes，用的时候必须是字符串。
        return self.__db.rpop(PROXYPOOL).decode('utf-8')

    @property
    def queue_len(self):
        return self.__db.llen(PROXYPOOL)


if __name__ == '__main__':
    redis_client = Reidis_client()
    print(redis_client.pop())
