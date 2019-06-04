import json
import requests


def get_proxies():
    """
    连接API获取付费的代理IP
    :return: 代理IP
    """
    # 鹏鹏代理池的接口
    url = 'your proxy url'
    # 发送请求获取响应
    results = json.loads(requests.get(url).text)['RESULT']
    print("查看获取的响应：", results)
    return results


if __name__ == "__main__":
    get_proxies()
