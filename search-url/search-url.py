# -*- coding: utf-8 -*-
# Author: Conan0xff
# Date: 8/8/2017

import os, sys
import datetime
import random
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)

from proxy_pool.ProxyGetter.getFreeProxy import GetFreeProxy
from MagicBaidu import MagicBaidu
from MagicGoogle import MagicGoogle

all_totals = 0
all_checked_totals = 0
all_filter_totals = 0
all_delete_totals = 0

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

def conasearch(engine='google',key='python', page_num=0,page_size=30, savefile=1):
    result=[]
    if savefile == 'yes':
        logfile = open(key + '.txt', 'a')
    print ("\033[1;37;40m==========================第%s页采集开始================\n" % (page_num))
    if engine=='google':
        PROXIES = [{
            'http': '192.168.1.159:1080',
            'https': '192.168.1.159:1080'
        }]
        mg=MagicGoogle(PROXIES)
        sleep = random.randint(2, 15)
        for i in mg.search_url(query=key, num=page_size, pause=sleep,start=page_num*page_size):
            print '[URL]',i
            result.append(i)
            if savefile=='yes':
                logfile.writelines(i+'\n')
    elif engine=='baidu':
        proxies = [{"https":"https://{proxy}".format(proxy=i)} for i in GetFreeProxy().available_ip]
        print proxies
        mb = MagicBaidu(proxies)
        for i in mb.search(query=key, pn=page_size*(page_num-1), rn=page_size):
            print '[URL]',i['url'],': ','[TITLE]',i['title']
            result.append(i)
            if savefile=='yes':
                logfile.writelines(i['url']+'\n')
    else:
        print('invalid engine')
        exit(1)
    print ("==========================第%s页采集结束================\n" % (page_num))
    if savefile == 1:
        logfile.close()
    return result


if __name__ == '__main__':
    starttime = datetime.datetime.now()
    show_logo()
    engine = raw_input("Search Engine[baidu / google]:")
    key = raw_input('Keyword:')
    key = key.encode('utf-8')
    start_page = int(raw_input("Search number of start pages:"))
    end_page = int(raw_input("Search number of end pages:"))
    page_size = int(raw_input("Page size:"))
    savefile=raw_input("Save with file: [yes / not]:")
    for i in range(start_page, end_page+1):
        try:
            conasearch(engine=engine,key=key,page_num=i,page_size=page_size,savefile=savefile)
        except:
            continue
    endtime = datetime.datetime.now()
    runtime = (endtime - starttime).seconds
    print 'Used Time: ',runtime,' seconds'
