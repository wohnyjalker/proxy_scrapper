import requests
from typing import Union
from lxml.html import fromstring
from user_agent import generate_user_agent
from concurrent.futures import ProcessPoolExecutor


class FreeProxyCollector:
    '''
    free-proxy-list.net proxy collector
    '''

    URL = 'https://free-proxy-list.net/'
    # with open('test/my_ip', 'r') as f:
    #     MY_IP = f.readline()
    response = requests.get('http://api.ipify.org?format=json')
    if response.status_code:
        MY_IP = response.json()['ip']
        print(f'**********Your IP: {MY_IP}**********')

    def __init__(self):
        self.session = self.make_session()
        # self.ip = self.get_my_ip()
        self.proxy_list = set()
        self.valid_proxy_list = set()

    def __len__(self):
        return len(self.proxy_list)

    def make_session(self):
        headers = {
            'User-Agent': generate_user_agent()
        }
        with requests.Session() as s:
            s.headers.update(**headers)
        return s

    def get_proxy_list(self):

        response = self.session.get(self.URL)

        if response.status_code:
            tree = fromstring(response.text)

            ip_list = [x for x in tree.xpath('.//tbody/tr/td[1]/text()')]
            port_list = [x for x in tree.xpath('.//tbody/tr/td[2]/text()')]

            output = list()
            for i, p in zip(ip_list, port_list):
                output.append(f'{i}:{p}')

            self.proxy_list.update(set(output))

        else:
            print(response.status_code)

    def run_executor(self):
        with ProcessPoolExecutor(max_workers=100) as executor:
            executor.map(FreeProxyCollector.check_if_secure,
                         self.proxy_list, timeout=5)

    @staticmethod
    def get_my_ip():
        '''
            return your ip <--- sthing 
        '''
        url = 'http://api.ipify.org?format=json'
        session = FreeProxyCollector.make_session(FreeProxyCollector)
        response = session.get(url=url)
        if response.status_code:
            ip = response.json()['ip']
            print(f'**********Your IP:{ip}**********')
            print(type(ip))
            print(len(ip))
            return ip

    @staticmethod
    def check_if_secure(proxy_ip):
        url = 'http://api.ipify.org?format=json'
        session = FreeProxyCollector.make_session(FreeProxyCollector)
        # r = session.get(url)
        # print(r.json())
        try:
            response = session.get(
                url=url, proxies={'http': proxy_ip, 'https': proxy_ip})
            if response.json()['ip'] != FreeProxyCollector.MY_IP:
                # print(response.json())
                print(proxy_ip)
            # else:
            #     print('Equal to my ip')
            #     return False
        except requests.exceptions.ProxyError as e:
            pass
            # print(f'{proxy_ip} server error')
            #     return False
            # return True

    def run(self):
        self.get_proxy_list()
        print(f'{len(self)} proxy servers.\nSecure proxy list:')
        self.run_executor()
        # print(self.proxy_list)

        # print(self.proxy_list)
        # for x in self.proxy_list:
        #     if self.get_ip(x):
        #         with open('freeproxy', 'a') as f:
        #             f.write(f'{x}\n')


f = FreeProxyCollector()
f.run()
# print(f.proxy_list)
# print(len(f))
