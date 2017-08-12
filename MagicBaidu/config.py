import logging

# Define some constants

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
BLACK_DOMAIN = []
DOMAIN = 'www.baidu.com'
#'http://www.baidu.com/s?wd=key&rn=' + str(baidu_page_size) + '&pn=' + str(page_pn)
URL_SEARCH = "http://{domain}/s?wd={query}"
URL_SEARCH_FULL = "http://{domain}/s?wd={query}&rn={rn}&pn={pn}"

Search_URL_Filter_DOMAIN=['baidu.com','youku.com']

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("chardet").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s: %(message)s')
LOGGER = logging.getLogger('magic_baidu')
