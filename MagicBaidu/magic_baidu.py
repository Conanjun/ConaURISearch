import requests
import chardet
import random
import os
import sys
import time
from tld import get_tld
from pyquery import PyQuery as pq
from MagicBaidu.config import USER_AGENT, DOMAIN, BLACK_DOMAIN, URL_SEARCH, URL_SEARCH_FULL, LOGGER, \
    Search_URL_Filter_DOMAIN
from proxy_pool.ProxyGetter.getFreeProxy import GetFreeProxy

# if sys.version_info[0] > 2:
#    from urllib.parse import quote_plus, urlparse, parse_qs
# else:
from urllib import quote_plus
from urlparse import urlparse, parse_qs


class MagicBaidu():
    def __init__(self, proxies=None):
        self.available_proxies = proxies
        self.proxies = random.choice(proxies) if proxies else None

    def search(self, query, rn=None, pn=0, pause=2):
        success_flag = False
        max_try_counts = 5  # change proxy times
        while not success_flag and max_try_counts:
            content = self.search_page(query, rn, pn, pause)
            pq_content = self.pq_html(content)
            if len(pq_content('div.result')) != 0:
                LOGGER.debug(len(pq_content('div.result')))
                success_flag = True
            else:
                max_try_counts = max_try_counts - 1
                if max_try_counts == 0:
                    print 'exceed max try proxies in search page'
                self.update_proxies()
        for item in pq_content('div.result').items():
            result = {}
            result['title'] = item('h3.t>a').eq(0).text()
            href = item('h3.t>a').eq(0).attr('href')
            if href:
                realurl = self.get_realurl(href)
                url = self.filter_link(realurl)
                if url != 'filter':
                    result['url'] = url
                else:
                    continue
            title = item('h3.t>a').text()
            result['title'] = title
            yield result

    def search_page(self, query, rn=None, pn=0, pause=2):
        # if you have many proxies , this is not necessary
        # time.sleep(pause)
        LOGGER.info(str(self.proxies))
        domain = DOMAIN
        if rn is None:
            url = URL_SEARCH
            url = url.format(
                domain=domain, query=quote_plus(query))
        else:
            url = URL_SEARCH_FULL
            url = url.format(
                domain=domain, query=quote_plus(query), rn=quote_plus(str(rn).encode('utf-8')),
                pn=quote_plus(str(pn).encode('utf-8')))
        LOGGER.info(url)

        # Add headers
        headers = {'Connection': 'keep-alive',
                   'Cache-Control': 'max-age=0',
                   'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, sdch',
                   'Accept-Language': 'zh-CN,zh;q=0.8',
                   }
        try:
            r = requests.get(url=url,
                             proxies=self.proxies,
                             headers=headers,
                             timeout=10
                             )
            assert r.status_code == 200
            charset = chardet.detect(r.content)
            content = r.content.decode(charset['encoding'])
            return content
        except requests.RequestException as e:
            print (e)

    def search_url(self, query, rn=None, pn=0, pause=2):
        success_flag = False
        max_try_counts = 5
        while not success_flag and max_try_counts:
            print max_try_counts
            content = self.search_page(query, rn, pn, pause)
            pq_content = self.pq_html(content)
            if len(pq_content('div.result')) != 0:
                LOGGER.debug(len(pq_content('div.result')))
                success_flag = True
            else:
                max_try_counts = max_try_counts - 1
                if max_try_counts == 0:
                    print 'exceed max try proxies in search_url'
                self.update_proxies()
        for item in pq_content('h3.t').items():
            href = item('a').attr('href')
            if href:
                real_url = self.get_realurl(href)
                url = self.filter_link(real_url)
                if url != 'filter':
                    yield url

    def filter_link(self, link):
        domain = get_tld(link)
        if domain in Search_URL_Filter_DOMAIN:
            return 'filter'
        else:
            return link

    def get_realurl(self, redirect_url):
        LOGGER.info('trying '+redirect_url)
        headers = {'Connection': 'keep-alive',
                   'Cache-Control': 'max-age=0',
                   'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, sdch',
                   'Accept-Language': 'zh-CN,zh;q=0.8',
                   }

        try:
            r = requests.get(url=redirect_url,
                             proxies=self.proxies,
                             headers=headers,timeout=10)
            assert r.status_code == 200
            return r.url
        except Exception as e:
            return redirect_url

    def pq_html(self, content):
        return pq(content)

    def get_random_user_agent(self):
        return random.choice(self.get_data('user_agents.txt', USER_AGENT))

    def get_data(self, filename, default=''):
        """
        Get data from a file
        :param filename: filename
        :param default: default value
        :return: data
        """
        root_folder = os.path.dirname(__file__)
        user_agents_file = os.path.join(
            os.path.join(root_folder, 'data'), filename)
        try:
            with open(user_agents_file) as fp:
                data = [_.strip() for _ in fp.readlines()]
        except:
            data = [default]
        return data

    def update_proxies(self):
        self.available_proxies.remove(self.proxies)
        self.proxies = random.choice(self.available_proxies)
        assert len(self.available_proxies) != 0


if __name__ == '__main__':
    proxies = [{"https": "https://{proxy}".format(proxy=i)} for i in GetFreeProxy().available_ip]
    print proxies
    mb = MagicBaidu(proxies)
    result = list(mb.search(query='inurl:php?uid=', rn=20, pn=10))
    print result
    print len(result)
    mb2 = MagicBaidu(proxies)
    result2 = list(mb.search_url(query='inurl:asp?uid=', rn=20, pn=10))
    print result2
    print len(result2)
