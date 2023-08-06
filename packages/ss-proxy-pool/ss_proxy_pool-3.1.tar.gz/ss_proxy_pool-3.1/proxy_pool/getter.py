'''

爬取免费代理ip，返回ip
'''
import requests
from lxml import etree


# 设定一个元类
# 第一步：继承type
class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        """
        定义一个属性__crawlfuncs__=[]
        __crawlcount__=int---爬取方法的数量
        :param name: 类的名称
        :param bases: 类的继承元组
        :param attrs: 类的属性字典
        :return:
        """
        __crawlfuncs__ = []
        count = 0
        for k, v in attrs.items():
            if 'crawl_' in k:
                __crawlfuncs__.append(k)
                count += 1
        attrs['__crawlfuncs__'] = __crawlfuncs__
        attrs['__crawlcount__'] = count

        # 最终还是由type来创建这个类的。
        # 调用父类的方法来创建
        # 父类type他也是通过—__new__来创建的
        # d
        return type.__new__(cls, name, bases, attrs)
        # return super().__new__(name,bases,attrs)


class FreeProxyGetter(object, metaclass=ProxyMetaclass):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
        }

    # ['crawl_66ip', 'crawl_ip3366', 'crawl_ip8877', 'crawl_ip8899']
    def get_proxies(self, crawl_func):
        # crawl_66ip
        proxies = []
        # self.crawl_ip3366()
        # proxies = eval('self.{}()'.format(crawl_func))
        for proxy in eval('self.{}()'.format(crawl_func)):
            # 设定取得个数
            # if len(proxies)<1000:
            #     proxies.append(proxy)
            # else:
            #     yield proxies
            #     #清空proxies
            proxies.append(proxy)
        return proxies

    def crawl_66ip(self):
        # global headers
        """
        url:http://www.66ip.cn/
        :return:list[proxy]
        """
        proxies = []
        base_url = 'http://www.66ip.cn/%s.html'
        for i in range(1, 20):
            response = requests.get(base_url % i, headers=self.headers)
            html = etree.HTML(response.text)
            ips = html.xpath('//tr[position()>1]/td[1]/text()')
            ports = html.xpath('//tr[position()>1]/td[2]/text()')
            if len(ips) == len(ports) and ips and ports:
                for i, ip in enumerate(ips):
                    port = ports[i]
                    # print(ip,port)
                    proxies.append(ip.strip() + ':' + port.strip())
                    yield ip.strip() + ':' + port.strip()
            # print(proxies)
        # return proxies

    def crawl_xiciIP(self):
        url = 'https://www.xicidaili.com/nn/{}'
        proxies = []
        for i in range(1, 2):
            response = requests.get(url.format(i), headers=self.headers)
            html = etree.HTML(response.text)
            ips = html.xpath('//tr[position()>1]/td[1]/text()')
            ports = html.xpath('//tr[position()>1]/td[2]/text()')
            if len(ips) == len(ports) and ips and ports:
                for i, ip in enumerate(ips):
                    port = ports[i]
                    proxies.append(ip.strip() + ':' + port.strip())
                    # print(proxies)
                    yield ip.strip() + ':' + port.strip()

    def crawl_ipkuai(self):
        '''
       url:http://www.ip3366.net/?stype=1&page=1
       :return:list[proxy]
       '''
        # global headers
        proxies = []
        base_url = 'https://www.kuaidaili.com/free/inha/{}/'
        for i in range(1, 20):
            response = requests.get(base_url.format(i), headers=self.headers)
            html = etree.HTML(response.text)
            ips = html.xpath('//*[@id="list"]/table/tbody/tr/td[1]/text()')
            ports = html.xpath('//*[@id="list"]/table/tbody/tr/td[2]/text()')
            if len(ips) == len(ports) and ips and ports:
                for i, ip in enumerate(ips):
                    port = ports[i]
                    # print(ip,port)
                    proxies.append(ip.strip() + ':' + port.strip())
                    yield ip.strip() + ':' + port.strip()
        # return proxies


if __name__ == '__main__':
    f = FreeProxyGetter()
    # f.crawl_ipkuai()
    attrs_crawl = dir(f)
    crawl_methods = [x for x in attrs_crawl if 'crawl_' in x]
    print(crawl_methods)
    attrs = dir(f)
    print(attrs)
    print(f.__crawlfuncs__)
