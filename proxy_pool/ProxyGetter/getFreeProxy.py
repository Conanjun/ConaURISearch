# -*- coding: utf-8 -*-
# !/usr/bin/env python

import os,sys
parentdir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)

"""
-------------------------------------------------
   File Name：     GetFreeProxy.py
   Description :  抓取免费代理
   Author :       JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25:
-------------------------------------------------
"""
import re
import requests

try:
    from importlib import reload  # py3 实际不会实用，只是为了不显示语法错误
except:
    import sys  # py2

    reload(sys)
    sys.setdefaultencoding('utf-8')

from Util.utilFunction import robustCrawl, getHtmlTree
from Util.WebRequest import WebRequest

# for debug to disable insecureWarning
requests.packages.urllib3.disable_warnings()


class GetFreeProxy(object):
    """
    proxy getter
    """

    def __init__(self):
        pass

    #@staticmethod
    @robustCrawl  # decoration print error if exception happen
    def freeProxyFirst(self,page=10):
        """
        抓取无忧代理 http://www.data5u.com/
        :param page: 页数
        :return:
        """
        url_list = ['http://www.data5u.com/',
                    'http://www.data5u.com/free/',
                    'http://www.data5u.com/free/gngn/index.shtml',
                    'http://www.data5u.com/free/gnpt/index.shtml']
        for url in url_list:
            html_tree = getHtmlTree(url)
            ul_list = html_tree.xpath('//ul[@class="l2"]')
            for ul in ul_list:
                yield ':'.join(ul.xpath('.//li/text()')[0:2])

    #@staticmethod
    @robustCrawl
    def freeProxySecond(self,proxy_number=100):
        """
        抓取代理66 http://www.66ip.cn/
        :param proxy_number: 代理数量
        :return:
        """
        url = "http://www.66ip.cn/mo.php?sxb=&tqsl={}&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=".format(
                proxy_number)
        request = WebRequest()
        html = request.get(url).content
        for proxy in re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', html):
            yield proxy

    #@staticmethod
    @robustCrawl
    def freeProxyThird(self,days=1):
        """
        抓取ip181 http://www.ip181.com/
        :param days:
        :return:
        """
        url = 'http://www.ip181.com/'
        html_tree = getHtmlTree(url)
        tr_list = html_tree.xpath('//tr')[1:]
        for tr in tr_list:
            yield ':'.join(tr.xpath('./td/text()')[0:2])

    
    #@staticmethod
    @robustCrawl
    def freeProxyFourth(self):
        """
        抓取西刺代理 http://api.xicidaili.com/free2016.txt
        :return:
        """
        url_list = ['http://www.xicidaili.com/nn',  # 高匿
                    'http://www.xicidaili.com/nt',  # 透明
                    ]
        for each_url in url_list:
            tree = getHtmlTree(each_url)
            proxy_list = tree.xpath('.//table[@id="ip_list"]//tr')
            for proxy in proxy_list:
                yield ':'.join(proxy.xpath('./td/text()')[0:2])

    
    #@staticmethod
    @robustCrawl
    def freeProxyFifth(self):
        """
        抓取guobanjia http://www.goubanjia.com/free/gngn/index.shtml
        :return:
        """
        url = "http://www.goubanjia.com/free/gngn/index{page}.shtml"
        for page in range(1, 10):
            page_url = url.format(page=page)
            tree = getHtmlTree(page_url)
            proxy_list = tree.xpath('//td[@class="ip"]')
            for each_proxy in proxy_list:
                yield ''.join(each_proxy.xpath('.//text()'))

    @property
    def available_ip(self):
        available_ip=[]
        # for e in self.freeProxyFirst():
        #     available_ip.append(e)
        #
        # for e in self.freeProxySecond():
        #     available_ip.append(e)

        # for e in self.freeProxyThird():
        #     available_ip.append(e)
        for e in self.freeProxyFourth():
            available_ip.append(e)

        for e in self.freeProxyFifth():
            available_ip.append(e)
        return available_ip

if __name__ == '__main__':
    gg = GetFreeProxy()
    print gg.available_ip
    #for e in gg.freeProxyFirst():
    #    print e
    
    #for e in gg.freeProxySecond():
    #    print e

    #for e in gg.freeProxyThird():
    #    print e

    #for e in gg.freeProxyFourth():
    #    print e

    #for e in gg.freeProxyFifth():
    #    print(e)
