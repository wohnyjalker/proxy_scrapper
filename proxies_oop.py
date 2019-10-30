import requests
from typing import Union
from lxml.html import fromstring
from user_agent import generate_user_agent


class ProxyCollector:
    '''
        proxy collector
    '''

    IP_XPATH = '/html/body/center/div/div/div/center/div/table/tbody/tr/td/abbr/script/text()'
    PORT_XPATH = '/html/body/center/div/div/div/center/div/table/tbody/tr/td/a/@href'
    COUNTRIES_XPATH = './/select[@id="proxy_country"]/option/@value'

    COUNTRY_URL = 'https://www.proxynova.com/proxy-server-list/country-{}/'

    def __init__(self):
        self.session = self.make_session()
        self.countries = None
        self.proxy_set = set()

    def make_session(self):
        headers = {
            'User-Agent': generate_user_agent()
        }
        with requests.Session() as s:
            s.headers.update(**headers)
        return s

    def get_countries_list(self):
        '''
            builds countries list
        '''
        session = self.session

        response = session.get(
            'https://www.proxynova.com/proxy-server-list/country-ar/')

        if response.status_code:
            tree = fromstring(response.text)
            countries_list = [x for x in tree.xpath(self.COUNTRIES_XPATH)]
            countries_list = countries_list[1:-3]

        self.countries = countries_list

    @staticmethod
    def normalize_port(_str) -> Union[str, None]:
        port = _str.split('-')[-1][:-1]
        if port.isdigit():
            return port
        pass

    @staticmethod
    def return_ip(silly_protection_or_js) -> Union[str, None]:
        _str = silly_protection_or_js[24:29] + silly_protection_or_js[45:-4]
        return _str

    def proxy_from_country(self, country):
        session = self.session

        response = session.get(self.COUNTRY_URL.format(country))

        if response.status_code:
            tree = fromstring(response.text)
            ip_list = [self.return_ip(x) for x in tree.xpath(self.IP_XPATH)]
            port_list = [self.normalize_port(x)
                         for x in tree.xpath(self.PORT_XPATH)]
            port_list = [x for x in port_list if x is not None]
        else:
            print('proxy_from_country error')

        proxy_in_country = list()
        for ip, port in zip(ip_list, port_list):
            proxy_in_country.append(f'{ip}:{port}')

        self.proxy_set.update(set(proxy_in_country))
        print(*self.proxy_set, sep='\n')

    def build_proxy_set(self):
        for _ in map(self.proxy_from_country, self.countries):
            pass

    def run(self):
        self.get_countries_list()
        self.build_proxy_set()


p = ProxyCollector()
p.run()
print(p.countries)
print(p.proxy_set)
print(len(p.proxy_set))
