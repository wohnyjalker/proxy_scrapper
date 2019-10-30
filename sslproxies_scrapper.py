import requests
# from bs4 import BeautifulSoup
from typing import Union
from lxml.html import fromstring
from user_agent import generate_user_agent
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


IP_XPATH = '/html/body/center/div/div/div/center/div/table/tbody/tr/td/abbr/script/text()'
PORT_XPATH = '/html/body/center/div/div/div/center/div/table/tbody/tr/td/a/@href'
COUNTRIES_XPATH = '/html/body/center/div/div/div/center/div/select/option/@value'

COUNTRY_URL = 'https://www.proxynova.com/proxy-server-list/country-{}/'


def make_session():
    headers = {
        'User-Agent': generate_user_agent()
    }
    with requests.Session() as s:
        s.headers.update(**headers)
    return s


def normalize_port(_str) -> Union[str, None]:
    port = _str.split('-')[-1][:-1]
    if port.isdigit():
        return port
    pass


def return_ip(silly_protection_or_js) -> Union[str, None]:
    _str = silly_protection_or_js[24:29] + silly_protection_or_js[45:-4]
    return _str


def get_countries_list():
    session = make_session()

    response = session.get(
        'https://www.proxynova.com/proxy-server-list/country-ar/')

    if response.status_code:
        tree = fromstring(response.text)
        countries_list = [x for x in tree.xpath(COUNTRIES_XPATH)]

    return countries_list[1:-3]


def proxy_from_country(country):
    session = make_session()

    response = session.get(COUNTRY_URL.format(country))

    if response.status_code:
        tree = fromstring(response.text)
        ip_list = [return_ip(x) for x in tree.xpath(IP_XPATH)]
        port_list = [normalize_port(x) for x in tree.xpath(PORT_XPATH)]
        port_list = [x for x in port_list if x is not None]

    proxy_in_country = list()
    for ip, port in zip(ip_list, port_list):
        print(f'{ip}:{port}')
        proxy_in_country.append(f'{ip}:{port}')

    return proxy_in_country


proxy = list()
print(get_countries_list())
for country in get_countries_list():
    proxy.extend(proxy_from_country(country))
    print(*proxy, sep='\n')
    with open('proxylist', 'a') as f:
        for p in proxy:
            f.write(f'{p}\n')

        # f.write(proxy_from_country(country)) <- zle kurtwa


print(len(proxy))

# for country in countries_list[:-3]:
#     print(country)

# for ip, port in zip(ip_list, port_list):
#     print(f'{ip}:{port}')
