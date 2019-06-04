"""
在Boss直聘中以职位进行搜索，比如：知识产权，商标代理人等等，将抓取的结果写入csv文件
职位          工资         工作经验         学历            公司名称         公司类型        是否上市      公司规模
position----->salary------>experience------>education------>companyName----->companyType----->isListed---->companySize
------------------->增加了公司地点
"""
import csv
import json
import requests
from lxml import etree


class PositionSpider(object):

    def __init__(self):
        # 请求头，不添加获取不到数据
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
        }
        # 拼接下一页的链接
        self.base = "https://www.zhipin.com"
        # 全局默认值
        self.default_value = "暂无"
        self.path = r'G:\工作\招聘网站爬虫\Boss\Position.xls'
        # 文件对象
        self.csvfile = open(self.path, 'a+', newline='', encoding='utf-8', errors='ignore')  # python3下需要这样写
        # 文件写入对象
        self.writer = csv.writer(self.csvfile, delimiter='\t')
        # csv文件的标题
        self.title = ["position", "salary", "companyLocation", "experience",
                      "education", "companyName", "companyType",	"isListed",	"companySize"]
        # 将列标题写入文件
        self.writer.writerow(self.title)

    def process_requests(self, url):
        """
        输入向要搜索的职位，开始搜索
        :param url:
        :return:
        """
        # 请求搜索
        result = requests.get(url, headers=self.headers)
        # 将搜索结果转换成可以使用xpath解析的HTML
        html = self.parse_response(result)
        return html

    def get_next(self, req):
        """
        用于请求下一页的数据
        :param req:
        :return:
        """
        # 请求下一页
        result = requests.get(url=req, headers=self.headers)
        # 将搜索结果转换为能使用xpath解析的HTML
        html = self.parse_response(result)
        return html

    def parse_html(self, html):
        """
        解析HTML获取目标字段，并实现全页号的循环抓取
        :param html:
        :return:
        """
        # 所有搜索结果的列表
        info_list = html.xpath('//div[@class="job-list"]/ul/li')
        # 判断是否有下一页，根据ka的属性值判断
        is_next = html.xpath('//div[@class="page"]/a[last()]/@class')
        # 获取每一条搜索结果，包含职位信息和公司信息
        for info in info_list:
            # 创建字典
            dd = dict()
            # 职位
            dd['position'] = info.xpath('./div/div/h3/a/div[@class="job-title"]/text()')[0]
            # 工资
            dd['salary'] = info.xpath('./div/div/h3/a/span/text()')[0]
            # 公司地点/工作经验/学历的列表
            list_1 = [x for x in info.xpath('./div/div[@class="info-primary"]/p/text()') if x]
            # 公司地点
            dd['companyLocation'] = list_1[0]
            # 工作经验
            dd['experience'] = list_1[1]
            # 学历
            dd['education'] = list_1[2]
            # 公司名称
            dd['companyName'] = info.xpath('./div/div[@class="info-company"]/div[@class="company-text"]/h3/a/text()')[0]
            # 公司类型/是否上市/公司规模的列表
            list_2 = [x for x in info.xpath('./div/div[@class="info-company"]/div[@class="company-text"]/p/text()') if
                      x]
            if len(list_2) == 2:
                # 公司类型
                dd['companyType'] = list_2[0]
                # 是否上市
                dd['isListed'] = self.default_value
                # 公司规模
                dd['companySize'] = list_2[1]
            else:
                # 公司类型
                dd['companyType'] = list_2[0]
                # 是否上市
                dd['isListed'] = list_2[1]
                # 公司规模
                dd['companySize'] = list_2[2]
            # 将数据写入json文件
            # record_result(dd)
            # 将数据写入csv文件
            self.record_result_csv(dd)
        try:
            # 判断是否有下一页
            if is_next[0] == "next":
                # 有下一页，获取href属性值
                middle = html.xpath('//div[@class="page"]/a[last()]/@href')[0]
                # 拼接完整的URL
                url = self.base + middle + "&ka=page-next"
                # 发起请求
                html_ = self.get_next(url)
                # 调用自身解析
                self.parse_html(html_)
        except IndexError:
            print("总共一页数据")

    @staticmethod
    def record_result(data):
        """
        将结果写入文件
        :param data:
        :return:
        """
        path = r'G:\工作\招聘网站爬虫\Boss\Position.json'
        with open(path, 'a+', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")

    def record_result_csv(self, data):
        """
        将结果写入文件，增加一种文件方式：csv
        :param data: dict
        :return:
        """
        if isinstance(data, dict):
            # 将values数据一次一行的写入csv中
            self.writer.writerow(list(data.values()))

    def close_csv(self):
        """
        关闭文件
        :return:
        """
        # 写入完成关闭文件
        self.csvfile.close()

    @staticmethod
    def parse_response(res):
        """
        将获取的响应转换为HTML
        :param res: 响应（text）
        :return: HTML
        """
        try:
            if res.status_code == 200:
                # 测试时使用
                res.encoding = res.apparent_encoding
                return etree.HTML(res.text, etree.HTMLParser())
            else:
                print("响应的状态码不是200")
                return False
        except Exception as e:
            print(e)
