"""
工具类
"""
import requests
from requests.exceptions import ConnectionError

base_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}


def get_page(url, options={}):
    """
    抓取代理
    :param url:
    :param options:
    :return:
    """
    headers = dict(base_headers, **options)
    # proxy = get_random_proxy()
    # proxies = proxy.split(":")
    # proxies = [proxies[0], proxies[1].split("//")[1] + ':' + proxies[2]]
    # proxies = {
    #     proxies[0]: proxies[1]
    # }
    print('正在抓取', url)
    try:
        # response = requests.get(url, headers=headers, proxies=proxies)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print('抓取成功', url, response.status_code)
            return response.text
    except ConnectionError:
        print('抓取失败', url)
        return None

# def get_random_proxy():
#         '''随机从文件中读取proxy'''
#         while 1:
#             with open("proxypool\proxies.txt", 'r') as f:
#             # with open("proxies.txt", 'r') as f:
#                 proxies = f.readlines()  # readline()返回所有行
#             if proxies:
#                 break
#             else:
#                 time.sleep(1)
#         proxy = random.choice(proxies).strip()  # strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
#         return proxy
