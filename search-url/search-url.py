# -*- coding: utf-8 -*-
# Author: Conan0xff
# Date: 8/8/2017 

import re
import urllib2
from tld import get_tld
import requests

import os, sys

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)

import datetime
import random
# the baidu page size

from proxy_pool.ProxyGetter.getFreeProxy import GetFreeProxy

proxy_ip = GetFreeProxy().available_ip

all_totals = 0
all_checked_totals = 0
all_filter_totals = 0
all_delete_totals = 0

baidu_page_size = 50

filter_array1 = ['baidu.com']
# filter_array1 = ['baidu.com', 'sina.com.cn', 'sohu.com', 'taobao.com', 'douban.com', '163.com', 'tianya.cn', 'qq.com',
#                 '1688.com']
# filter_array2 = ['ganji.com', '58.com', 'baixing.com']
# filter_array3 = ['zhihu.com', 'weibo.com', 'iqiyi.com', 'kugou.com', '51.com', 'youku.com', 'soku.com', 'acfun.cn',
#                 'verycd.com']
# filter_array4 = ['google.cn', 'youdao.com', 'iciba.com', 'cdict.net']
# filter_array5 = ['pconline.com.cn', 'zcool.com.cn', 'csdn.net', 'lofter.com']

# filter_array_dede =['dedecms.com']

# filter_array_all = filter_array1 + filter_array2 + filter_array3 + filter_array4 + filter_array5 + filter_array_dede
# filter_array_all = filter_array1 + filter_array_dede
filter_array_all = filter_array1


def show_logo():
    logostr = """
    
#####          #     #          #####  #     # ######    ###
#     #   ####  ##    #    ##   #     # #     # #     #    #
#        #    # # #   #   #  #  #       #     # #     #    #
#        #    # #  #  #  #    #  #####  #     # ######     #
#        #    # #   # #  ######       # #     # #   #      #
#     #  #    # #    ##  #    # #     # #     # #    #     #
 #####    ####  #     #  #    #  #####   #####  #     #   ###

 Author:Conan0xff   Version 1.0.0   Email:1526840124@qq.com            

"""
    print logostr


headers = {'Connection': 'keep-alive',
           'Cache-Control': 'max-age=0',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, sdch',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           }


# Get the web page source code
def get_pagehtml(url, proxy):
    try:
        global headers
        response = requests.get(url, headers=headers, proxies=proxy, timeout=3)
        assert response.status_code == 200
        return response.text
    except requests.RequestException as e:
        print (e)


# Get the real url
def get_realurl(target_url):
    try:
        global headers
        cur_proxy_ip = random.choice(proxy_ip)
        proxy = {"https": "https://{proxy}".format(proxy=cur_proxy_ip)}
        response = requests.get(target_url, headers=headers, proxies=proxy, timeout=3)
        assert response.status_code == 200
        return response.url
    except Exception, e:
        return target_url


# Filter the real URL
def filter_url(target_url, urlparam):
    domain = get_tld(target_url)
    if domain in filter_array_all:
        return 'filter'
    else:
        if urlparam == 1:
            reg = r'^https?:\/\/([a-z0-9\-\.]+)[\/\?]?'
            m = re.match(reg, target_url)
            if m:
                uri = m.groups()[0]
                return uri[uri.rfind('//', 0, uri.rfind('.')) + 1:]
            else:
                return target_url
        else:
            return target_url


def baidu_search(key, page_pn=50, filter=1, savefile=1, urlparam=0):
    page_num = str(page_pn / baidu_page_size + 1)

    search_url = 'http://www.baidu.com/s?wd=key&rn=' + str(baidu_page_size) + '&pn=' + str(page_pn)
    search_url = search_url.replace('key', key)

    # if the result_node=[],then use another proxy and delete the proxy from the proxy_ips
    get_success_flag = False
    while not get_success_flag and len(proxy_ip) > 0:
        cur_proxy_ip = random.choice(proxy_ip)
        proxy = {"https": "https://{proxy}".format(proxy=cur_proxy_ip)}
        htmlcontent = get_pagehtml(search_url, proxy)
        # use xpath
        from lxml import etree
        htmltree = etree.HTML(str(htmlcontent))
        result_nodes = htmltree.xpath(u'//div[@id="content_left"]/div[@class="result c-container "]/h3[@class="t"]/a')
        if result_nodes == []:
            print "Proxy: " + cur_proxy_ip + " not available"
            proxy_ip.remove(cur_proxy_ip)
        else:
            print 'Use Proxy:', cur_proxy_ip
            get_success_flag = True

    if savefile == 1:
        logfile = open(key + '.txt', 'a')

    print ("\033[1;37;40m==========================第%s页采集开始================\n" % (page_num))
    for i in result_nodes:
        redirect_url = i.xpath(u'@href')[0]
        title = i.xpath(u'text()')[0]
        realurl = get_realurl(redirect_url)
        print realurl, ': ', title.encode('utf-8')

        global all_totals
        all_totals += 1

        if filter == 1:
            realurl = filter_url(realurl, urlparam)

        if realurl != "filter":
            global all_checked_totals
            all_checked_totals += 1

            print ("[URL]:%s  [TITLE]:%s" % (realurl, title))
            if savefile == 1:
                have_url = 0
                with open(key + '.txt', 'r') as foo:
                    for line in foo.readlines():
                        if realurl in line:
                            have_url = 1
                    if have_url == 0:
                        logfile.write(realurl + '\n')
                    else:
                        global all_delete_totals
                        all_delete_totals += 1
        else:
            global all_filter_totals
            all_filter_totals += 1

    print ("==========================第%s页采集结束================\n" % (page_num))
    if savefile == 1:
        logfile.close()


if __name__ == '__main__':
    # Get the start time
    starttime = datetime.datetime.now()
    show_logo()
    # print proxy_ip
    print 'get proxy ips count: ', len(proxy_ip)
    key = raw_input('\033[1;33;40mplease input keyword:')
    key = key.encode('utf-8')
    key = urllib2.quote(key)

    start_page = int(raw_input("Search Number of start pages:"))
    end_page = int(raw_input("Search Number of end pages:"))

    for i in range(start_page - 1, end_page):
        page_pn = (i * baidu_page_size)
        baidu_search(key, page_pn)
    # Get the end time
    endtime = datetime.datetime.now()
    runtime = (endtime - starttime).seconds

    print(
        "\033[1;36;40m%d found | %d checked | %d filter | %d delete      The program runs in %s seconds\033[1;37;40m" % (
            all_totals, all_checked_totals, all_filter_totals, all_delete_totals, runtime))
