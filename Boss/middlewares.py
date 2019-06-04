# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import requests
from scrapy import signals

from Boss.proxy.db import REDISCLIENT


class BossSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BossDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyMiddleware(object):

    def __init__(self):
        self.db = REDISCLIENT()

    def get_random_proxy(self):
        """
        连接数据库
        保证获取随机有效的proxy
        :return: proxy
        """
        # 获取代理ip
        try:
            # 获取随机的代理
            proxy = self.db.random()
            # 顺便检查一下代理数量是否达到阈值
            self.db.check()
            # 增加添加代理前的检测环节，保证获取的代理有效
            if proxy:
                ip = proxy.split(":")[0]
                port = proxy.split(":")[1]
                if self.db.check_proxy(ip, port):
                    print("代理可以使用<login--get_proxy>")
                    return proxy
            else:  # 回调自己重新获取代理
                self.get_random_proxy()
        except requests.ConnectionError:
            return False

    def process_request(self, request, spider):
        """
        每个请求都会经过这里，在此添加代理IP
        :param request:
        :param spider:
        :return:
        """
        spider.logger.info("即将给请求添加代理")
        # 代理不会冲突，请求每次经过时添加代理
        proxy = self.get_random_proxy()
        if proxy:
            uri = 'https://{proxy}'.format(proxy=proxy)
            # 将使用代理信息打印在控制台中
            spider.logger.info("使用代理[%s]访问[%s]" % (proxy, request.url))
            request.meta['proxy'] = uri

    def process_response(self, request, response, spider):
        """
        如果响应中出现重定向则需要重新更换proxy
        :param request:
        :param response:
        :param spider:
        :return:
        """
        if response.status == 403:
            spider.logger.info("被重定向**********")
            # 获取被重定向的url
            current_url = request.meta['current_url']
            print("查看被重定向的原始url:", current_url)
            spider.logger.info("代理失效")
            # 设置代理IP=None
            request.meta['proxy'] = None
            return request.replace(url=current_url, dont_filter=True)
        return response
