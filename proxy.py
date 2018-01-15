import requests
from bs4 import BeautifulSoup

HEADER = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}


class Proxy(object):
    proxy_list = []

    def parse_proxy(self):
        proxy_url = 'https://www.ip-adress.com/proxy-list'
        r = requests.get(proxy_url)
        soap = BeautifulSoup(r.text, 'lxml')
        res = soap.select('table.htable tr td')
        i = 0
        while i < len(res):
            self.proxy_list.append(res[i].text)
            i += 4


    def __init__(self):
        self.parse_proxy()

    def get_proxy(self):
        ok_proxy = []
        i = 1
        print(len(self.proxy_list))
        for proxy in self.proxy_list:
            url = 'http://' + proxy
            proxies = {'http' : url,
                       'https' : url}
            try:
                r = requests.get('http://cs13.imyz.me/dl/69/6706110/19435099/0/1/0/d1b55b61b0ff070bd51c3f85c625449c/12_franz_ferdinand_fade_together_myzuka.mp3', headers=HEADER, proxies=proxies, timeout=5)
                print(r.status_code)
                if r.status_code == 200:
                    ok_proxy.append(proxy)
                #print('Num - {}    Proxy - {}'.format(i, proxy))
            except requests.exceptions.ConnectionError:
                #print('{} ERROR'.format(i))
                pass
            except requests.exceptions.ReadTimeout:
                #print('{} ERROR'.format(i))
                pass
            finally:
                i += 1
        return ok_proxy

proxy = Proxy()
proxy = proxy.get_proxy()
with open('proxy.txt', 'w') as f:
    for i in proxy:
        f.write('\n' + i)

