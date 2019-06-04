"""
获取BOSS直聘上城市与相应城市代码的对应关系
"""

# 请求地址,获取的为Json串
import json

import requests

# 请求
base_url = "https://www.zhipin.com/common/data/city.json"
# 请求头
headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
        }


def get_city_code():
    """
    请求链接获取城市与城市代码的对应关系
    :return:
    """
    # 获取响应
    result = requests.get(url=base_url, headers=headers)
    # 将Json--->python dict
    data = transfer_dict(result.text)
    # 获取省/直辖市的数据列表------>数据结构：[{ },{ }.....]
    cityList = data.get("data").get("cityList")
    # 此时暂时先将城市的列表信息写入文件
    record_result(cityList)
    print("城市信息记录完成")


def transfer_dict(j):
    """
    将json数据转换为python字典
    :param j: json数据
    :return: dict
    """
    return json.loads(j, encoding='utf-8')


def transfer_json(d):
    """
    将字典转为json数据
    :param d:
    :return:
    """
    return json.dumps(d, ensure_ascii=False)


def record_result(data):
    """
    将结果写入文件
    :param data:
    :return:
    """
    path = r'G:\工作\招聘网站爬虫\Boss\City.json'
    with open(path, 'a+', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")

#######################################################################################


# 创建列表存储城市的名称
city = list()
# 创建列表存储城市的代码
city_code = list()


def get_():
    path = r'G:\工作\招聘网站爬虫\Boss\CityList.json'
    with open(path, 'r', encoding="utf-8") as f:
        datas = json.loads(f.read(), encoding="utf-8")
    for data in datas:
        dd = data.get("subLevelModelList")
        # 获取的每一条数据为一个省或者直辖市的
        if len(dd) == 1:
            for d in dd:
                # 直接获取城市的名称和代码
                city_name = d.get("name")
                code = d.get("code")
                # 添加到列表
                city.append(city_name)
                city_code.append(code)
        else:
            # 先获取省的名称
            s = data.get("name")
            s_code = data.get("code")
            city.append(s)
            city_code.append(s_code)
            for d in dd:
                # 获取的还是一个字典
                name = d.get("name")
                code_ = d.get("code")
                city.append(name)
                city_code.append(code_)
    r = dict(zip(city, city_code))
    # 写入文件
    record_result(r)


# 测试代码
if __name__ == "__main__":
    # get_city_code()
    get_()