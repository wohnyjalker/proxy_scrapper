import requests
import time
from lxml.html import fromstring
from user_agent import generate_user_agent
from concurrent.futures import ProcessPoolExecutor
'''
           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                   Version 2, December 2004

Everyone is permitted to copy and distribute verbatim or modified
copies of this license document, and changing it is allowed as long
as the name is changed.

           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

 0. You just DO WHAT THE FUCK YOU WANT TO.
'''


class ProxyCollector:
    '''
    Info:
    Simple collector with validation if you are secure behind proxy
    Usage:
    just python3 collector_validator.py and wait for valid_proxy_list.txt
    '''

    URL = 'https://free-proxy-list.net/'
    IP_API_URL = 'http://api.ipify.org?format=json'
    MY_IP = ''

    def __init__(self, verbose=True):
        self.verbose = verbose
        self.ip = self.get_ip()
        self.session = self.make_session()
        self.proxy_set = set()
        self.valid_proxy_set = set()

    def __len__(self):
        return len(self.proxy_set)

    def get_ip(self):
        r = requests.get(self.IP_API_URL)
        print(f'**********Your IP: {r.json()}**********')
        return r.json()

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

            for i, p in zip(ip_list, port_list):
                self.proxy_set.add(f'{i}:{p}')
        else:
            print(response.status_code)

    def validate_ip(self, proxy_ip):
        session = self.make_session()

        try:
            response = session.get(
                url=self.IP_API_URL,
                proxies={'http': proxy_ip, 'https': proxy_ip},
                timeout=15
            )
            if response.json() != self.ip:
                if self.verbose:
                    print(f'Response from {proxy_ip} -> {response.json()}')
                else:
                    print(proxy_ip)
                return proxy_ip
            else:
                if self.verbose:
                    print(
                        f'Response {response.json()} so {proxy_ip} is not secure')
                pass
        except Exception as e:  # <-- to many exceptions to validate
            if self.verbose:
                print(f'ERROR:\n{e}')
            pass
        return None
        # except requests.exceptions.ProxyError as e:
        #     # if self.verbose:
        #     #     print(f'Error:\n{e}')
        #     pass
        # except requests.exceptions.TooManyRedirects as e:
        #     pass

    def write_to_file(self):
        with open('valid_proxy_list.txt', 'w') as f:
            f.write('\n'.join(self.valid_proxy_set))
            print('valid_proxy_list.txt created.')

    def run(self):
        self.get_proxy_list()
        print(len(self))
        for _ in map(self.validate_ip, self.proxy_set):
            pass

    def run_collector(self):
        start_time = time.time()
        self.get_proxy_list()
        print(f'{len(self)} proxy servers.')

        if self.verbose:
            print('Validating...')

        with ProcessPoolExecutor(max_workers=100) as executor:
            results = executor.map(
                self.validate_ip,
                self.proxy_set,
                timeout=15
            )
        self.valid_proxy_set = [ip for ip in results if ip is not None]
        print(f'Ther are {len(self.valid_proxy_set)} secure proxy servers')
        self.write_to_file()
        print("Script runtime %s seconds." % (time.time() - start_time))


collector = ProxyCollector(verbose=False)
collector.run_collector()
