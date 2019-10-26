# -*- coding: utf-8 -*-
# !/usr/bin/env python

import time
import re
import requests
from lxml import etree
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

requests.packages.urllib3.disable_warnings()


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def __init__(self):
        # 初始化selenium
        option = ChromeOptions()
        option.add_argument('--headless')
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.browser = Chrome(options=option)
        self.browser.maximize_window()
        self.browser.implicitly_wait(1)  # 等待1秒

    def __del__(self):
        self.browser.close()
        # self.browser.quit()

    def getHtml(self, url):
        self.browser.get(url=url)
        response = self.browser.find_element_by_xpath("//*").get_attribute("outerHTML")
        # print(response)
        return etree.HTML(response)

    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_66ip(self):
        self.browser.get("https://www.kuaidaili.com/free/inha")
        time.sleep(1)
        self.browser.get("http://www.66ip.cn/nmtq.php?getnum=30"
                         "&isp=0&anonymoustype=0&start=&ports="
                         "&export=&ipaddress=&area=1&proxytype=2&api=66ip"
                         )
        time.sleep(2)
        for i in range(1, 3):
            response = self.browser.find_element_by_xpath("//*").get_attribute("outerHTML")
            ip_list = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}", response)

            for ip in ip_list:
                yield ip.strip()
            time.sleep(5)
            self.browser.refresh()
        time.sleep(2)

    def crawl_goubanjia(self):
        self.browser.get('http://www.goubanjia.com')
        response = self.browser.find_element_by_xpath("//*").get_attribute("outerHTML")
        # print(response)
        tree = etree.HTML(response)
        proxy_list = tree.xpath('//td[@class="ip"]')
        # print(proxy_list)
        xpath_str = ".//*[not(contains(@style, 'display: none'))" \
                    "and not(contains(@style, 'display:none'))" \
                    "and not(contains(@class, 'port'))" \
                    "]/text()"
        for proxy in proxy_list:
            ip_addr = ''.join(proxy.xpath(xpath_str))
            port = 0
            for i in proxy.xpath(".//span[contains(@class, 'port')]"
                                 "/attribute::class")[0]. \
                    replace("port ", ""):
                port *= 10
                port += (ord(i) - ord('A'))
            port /= 8
            true_ip = '{}:{}'.format(ip_addr, int(port))
            # print(true_ip)
            yield true_ip
        time.sleep(2)

    def crawl_xiciwang(self):
        page = 1
        page_stop = 5
        while page < page_stop:
            time.sleep(3)
            url = 'https://www.xicidaili.com/nn/%d' % page
            html = self.getHtml(url)
            proxy_list = html.xpath('//*[@id="ip_list"]/tbody/tr')
            for i in range(1, len(proxy_list)):
                flag = proxy_list[i].xpath('./td[9]/text()')
                if "天" not in flag[0]:
                    continue
                ip = proxy_list[i].xpath('./td[2]/text()')[0]
                port = proxy_list[i].xpath('./td[3]/text()')[0]
                true_proxy = ip + ":" + port
                # print(true_proxy)
                yield true_proxy
            page += 1
        time.sleep(2)

    def crawl_kuaiDaiLi(self):
        page = 1
        page_stop = 5
        while page < page_stop:
            time.sleep(3)
            url = 'https://www.kuaidaili.com/free/inha/%d' % page
            html = self.getHtml(url)
            proxy_list = html.xpath('//*[@id="list"]/table/tbody/tr')
            for proxy in proxy_list:
                ip = proxy.xpath('./td[1]/text()')[0]
                port = proxy.xpath('./td[2]/text()')[0]
                true_proxy = ip + ":" + port
                # print(true_proxy)
                yield true_proxy
            page += 1

    def crawl_JiangXianLi(self):
        page = 1
        page_stop = 5
        while page < page_stop:
            time.sleep(3)
            url = 'http://ip.jiangxianli.com/?page=%d' % page
            html = self.getHtml(url)
            proxy_list = html.xpath('/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr')
            for proxy in proxy_list:
                # print(proxy.xpath('./td[6]/text()'))
                if not len(proxy.xpath('./td[6]/text()')):
                    continue
                ip = proxy.xpath('./td[2]/text()')[0]
                port = proxy.xpath('./td[3]/text()')[0]
                true_proxy = ip + ":" + port
                # print(true_proxy)
                yield true_proxy
            page += 1

if __name__ == '__main__':
    c = Crawler()
    c.crawl_daili66()