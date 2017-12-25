# -*- coding: utf-8 -*-
# Author: Conan0xff
# Date: 8/8/2017

import os, sys
import datetime
import random
import threading
import Queue

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)

from proxy_pool.ProxyGetter.getFreeProxy import GetFreeProxy
from MagicBaidu import MagicBaidu
from MagicGoogle import MagicGoogle


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


q = Queue.Queue()


def conasearch(engine='google', key='python', page_num=0, page_size=30):
    result = []
    if engine == 'google':
        PROXIES = [{
            'http': '192.168.1.159:1080',
            'https': '192.168.1.159:1080'
        }]
        mg = MagicGoogle(PROXIES)
        sleep = random.randint(2, 15)

        for i in mg.search_url(query=key, num=page_size, pause=sleep, start=page_num * page_size):
            # print '[URL]', i
            result.append(i)
    elif engine == 'baidu':
        proxies = [{"https": "https://{proxy}".format(proxy=i)} for i in GetFreeProxy().available_ip]
        print ('Got %d proxies' % len(proxies))
        mb = MagicBaidu(proxies)
        for i in mb.search(query=key, pn=page_size * (page_num - 1), rn=page_size):
            print '[URL]', i['url'], ': ', '[TITLE]', i['title']
            result.append(i['url'])
    else:
        print 'invalid engine :', engine
        exit(1)
    q.put(result)


def run():
    starttime = datetime.datetime.now()
    show_logo()
    engine = raw_input("Search Engine[baidu / google]:")
    key = raw_input('Keyword:')
    key = key.encode('utf-8')
    start_page = int(raw_input("Search number of start pages:"))
    end_page = int(raw_input("Search number of end pages:"))
    page_size = int(raw_input("Page size:"))
    savefile = raw_input("Save with file: [yes / not]:")

    result_set = set()

    threads = []
    for i in range(start_page, end_page + 1):
        threads.append(threading.Thread(target=conasearch, args=(engine, key, i, page_size),
                                        name='thread-' + str(i)))
    for i in threads:
        i.setDaemon(True)
        i.start()
    for i in threads:
        i.join()

    while not q.empty():
        result_set = result_set | set(q.get())

    if savefile == 'yes':
        with open(key + '.txt', 'a+') as f:
            for i in result_set:
                f.write(i + '\n')

    endtime = datetime.datetime.now()
    runtime = (endtime - starttime).seconds
    print 'Used Time: ', runtime, ' seconds'


if __name__ == '__main__':
    run()
