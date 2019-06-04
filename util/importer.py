"""
用于录入用户输入的城市/职位信息
"""
import json
# 请求的URL
from util.position import PositionSpider

url = "https://www.zhipin.com/job_detail/?query={position}&city={city_code}&industry=&position="


def get_city_code(city_name):
    """
    根据用户输入的城市名称获取对应的城市代码
    :param city_name: 城市名称
    :return: 城市代码
    """
    path = r'G:\工作\招聘网站爬虫\Boss\City.json'
    with open(path, 'r', encoding="utf-8") as f:
        data = json.loads(f.read(), encoding="utf-8")
    return data.get(city_name)


def generate_req(req, sep="/"):
    """
    获取用户的输入转换成URL请求
    :param req: 用户输入信息----字符串
    :param sep: 分割符
    :return:
    """
    city, position = req.split(sep)
    print("城市：", city, "职位：", position)
    # 调用方法获取用户输入城市的对应城市代码
    city_code = get_city_code(city)
    return url.format(position=position, city_code=city_code)


def scan():
    print("请输入城市/职位组合（使用/分隔），输入exit退出读入")
    while True:
        req = input()
        if req == "exit":
            break
        # 将用户输入转换成URL请求
        print("根据你的输入正在生成请求")
        url = generate_req(req)
        # 创建Positionp爬虫对象
        p = PositionSpider()
        # 发起请求
        html = p.process_requests(url)
        # 解析页面
        p.parse_html(html)
        print("采集完成")
        p.close_csv()
        break


# 测试代码
if __name__ == "__main__":
    scan()
