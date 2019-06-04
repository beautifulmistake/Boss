"""
boss直聘网站爬虫，只要采集两方面的信息：
1、一个是根据提供的公司花名录进行搜索采集
2、一个是根据职位进行搜索相关的公司信息，主要采集的有哪些公司在招聘相关的职位（这个单独分离开实现，详见util包
3、目前缺一个根据全国各地区来抓取（从搜索公司的角度讲应该是跟目前处于哪个地区应该没关系，故暂时未修正）
"""
import json
import os
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.signals import spider_closed
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy_redis.spiders import RedisSpider
from twisted.internet.error import TCPTimedOutError, DNSLookupError

from Boss.items import BossItem


class BossSpider(RedisSpider):
    name = "Boss"
    redis_key = "BossSpider:start_urls"

    def __init__(self, settings):
        super().__init__()
        self.record_file = open(os.path.join(settings.get("JSON_PATH"), f'{self.name}.json'), "a+", encoding="utf8")
        self.record_file.write('[')
        self.keyword_file_list = os.listdir(settings.get("KEYWORD_PATH"))
        # 公司/职位搜索的请求地址
        self.base_url = "https://www.zhipin.com/job_detail/?query={company_name}&city=101010100&industry=&position="
        # 设置请求头
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
        }
        # 拼接详情页的链接
        self.url = "https://www.zhipin.com"

    def parse_err(self, failure):
        """
        处理各种异常
        :param failure:
        :return:
        """
        if failure.check(TimeoutError, TCPTimedOutError, DNSLookupError):
            request = failure.request
            self.server.rpush(self.redis_key, request)
        if failure.check(HttpError):
            response = failure.value.response
            self.server.rpush(self.redis_key, response.url)
        return

    def start_requests(self):
        # 判断关键字文件是否存在
        if not self.keyword_file_list:
            # 抛出异常，关闭爬虫
            raise CloseSpider("需要关键字文件")
        # 遍历关键字文件
        for keyword_file in self.keyword_file_list:
            # 获取关键字文件路径
            file_path = os.path.join(self.settings.get("KEYWORD_PATH"), keyword_file)
            # 读取关键字文件
            with open(file_path, 'r', encoding='utf-8') as f:
                for keyword in f.readlines():
                    # 消除末尾的空格
                    keyword = keyword.strip()
                    print("查看获取的关键字：", keyword)
                    # 发起请求
                    yield scrapy.Request(url=self.base_url.format(company_name=keyword),
                                         meta={'search_key': keyword,
                                               "current_url": self.base_url.format(company_name=keyword)},
                                         headers=self.headers, callback=self.parse,
                                         errback=self.parse_err, dont_filter=True)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        # 获取配置信息
        settings = crawler.settings
        # 爬虫信息
        spider = super(BossSpider, cls).from_crawler(crawler, settings, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=spider_closed)
        return spider

    def spider_closed(self, spider):
        # 输出日志关闭爬虫
        self.logger.info('Spider closed：%s', spider.name)
        spider.record_file.write("]")
        spider.record_file.close()

    def parse(self, response):
        if response.status == 200:
            # 详情页的链接中间部分
            middle = response.xpath('//div[@class="company-list"]/div/a/@href').extract_first()
            # 详情页链接末尾部分
            ka = response.xpath('//div[@class="company-list"]/div/a/@ka').extract_first()
            # 获取search_key
            search_key = response.meta['search_key']
            if middle and ka:
                # 完整的url
                url = self.url + middle + "?" + ka
                # 请求详情页
                yield scrapy.Request(url=url, meta={'search_key': search_key, 'current_url': url},
                                     headers=self.headers, callback=self.parse_detail,
                                     errback=self.parse_err, dont_filter=True)
            # 将搜索结果写入文件
            self.record_file.write(json.dumps({'search_key': response.meta['search_key'],
                                               'result': "True" if middle else "False"}, ensure_ascii=False))
            self.record_file.write(",\n")
            self.record_file.flush()

    def parse_detail(self, response):
        """
        解析详情页：获取公司规模等相关信息
        :param response:
        :return:
        """
        if response.status == 200:
            # print("查看获取的响应：", response.text)
            # 创建item
            item = BossItem()
            # 搜索关键字
            search_key = response.meta['search_key']
            # 公司名称
            company_name = response.xpath('//div[@class="inner home-inner"]'
                                          '/div[1]//div[@class="info"]/h1/text()').extract()
            # 公司信息的标题
            company_info_title = ["is_listed", "company_size", "company_type"]
            # 获取公司上市情况/公司规模/公司类型
            company_info = response.xpath('//div[@class="info-primary"]/'
                                          'div[@class="info"]/p/descendant-or-self::text()').extract()
            # 将公司信息打包成字典
            info = dict(zip(company_info_title, company_info))
            item['search_key'] = search_key
            item['info'] = info
            item['company_name'] = "".join(company_name)
            yield item
