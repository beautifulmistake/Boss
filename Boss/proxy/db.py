from telnetlib import Telnet
import redis

from Boss.proxy.get_proxies import get_proxies
from Boss.proxy.setting import *


class REDISCLIENT(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD):
        """
        初始化获取数据库连接对象
        :param host: 地址
        :param port: 端口
        :param db: 数据库
        :param password: 密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, db=db, decode_responses=True)

    def add(self, proxy):
        """
        proxy存入数据库,成队列
        :param proxy: IP
        :return: IP
        """
        return self.db.rpush(REDIS_KEY, proxy)

    def random(self):
        """
        随机的获取代理proxy
        :return: proxy
        """
        return self.db.lpop(REDIS_KEY)

    def size(self):
        """
        获取redis队列中的数量
        :return:
        """
        return self.db.llen(REDIS_KEY)

    def check(self):
        """
        检测代理IP数量是否低于阈值
        如果低于阈值，则执行添加任务
        :return:
        """
        if self.size() <= THRESHOLD:
            # 低于阈值，添加proxy
            results = get_proxies()
            for result in results:
                proxy = result['ip'] + ':' + result['port']
                self.add(proxy)
        elif self.size() > THRESHOLD:
            print("还有至少三个proxy可使用")

    def delete_proxy(self, p):
        """
        根据值删除指定的失效的proxy
        :param p:
        :return:
        """
        return self.db.lrem(REDIS_KEY, 0, p)

    def delete_all(self):
        """
        一键删除key的所有值
        :return:
        """
        return self.db.delete(REDIS_KEY)

    def check_proxy(self, ip, port):
        """
        检测代理是否失效
        :param ip:
        :param port:
        :return:
        """
        try:
            Telnet().open(ip, port, timeout=3)
            return True
        except Exception:
            return False


if __name__ == "__main__":
    db = REDISCLIENT()
    dict_ = get_proxies()
    for result in dict_:
        proxy = result['ip'] + ":" + result['port']
        db.add(proxy)
    db.check()
