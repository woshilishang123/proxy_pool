import re
import json
import time
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from fake_useragent import UserAgent

from lxml import etree

# ua = UserAgent()
# print(ua.random)  #随机打印任意厂家的浏览器
import requests


class Crawler:
    def __init__(self):
        # 初始化selenium
        option = ChromeOptions()
        # option.add_argument('--headless')
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.browser = Chrome(options=option)
        self.browser.implicitly_wait(1)  # 等待1秒
        self.browser.maximize_window()

    def __del__(self):
        self.browser.close()
        # self.browser.quit()

    def getHtml(self, url):
        self.browser.get(url=url)
        response = self.browser.find_element_by_xpath("//*").get_attribute("outerHTML")
        # print(response)
        return etree.HTML(response)

    def craler_66ip(self):
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
                print(ip.strip())
                # yield ip.strip()
            time.sleep(5)
            self.browser.refresh()

        time.sleep(2)

    def craler_goubanjia(self):
        url = 'http://www.goubanjia.com'
        html = self.getHtml(url=url)
        proxy_list = html.xpath('//td[@class="ip"]')
        print(proxy_list)
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
            print(true_ip)
            # yield '{}:{}'.format(ip_addr, int(port))
        time.sleep(2)

    def crawler_xiciwang(self):
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
                print(true_proxy)
            page += 1

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
                print(true_proxy)
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
                print(true_proxy)
            page += 1


if __name__ == '__main__':
    c = Crawler()
    # c.craler_goubanjia()
    # c.craler_66ip()
    # c.get_proxies_nn()
    # c.crawl_kuaiDaiLi()
    c.crawl_JiangXianLi()




