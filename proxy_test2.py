import requests
from concurrent.futures import ProcessPoolExecutor
from user_agent import generate_user_agent


def make_session():
    headers = {
        'User-Agent': generate_user_agent()
    }
    with requests.Session() as s:
        s.headers.update(**headers)
    return s


def build_proxies_list():
    http = 'http://{}'

    proxy_list = list()
    with open('proxylist', 'r') as f:
        for ip in f:
            proxy_list.append({
                'http': http.format(ip.strip()),
                'https': http.format(ip.strip())
            })
    return proxy_list


def get_ip(proxies):
    url = 'http://api.ipify.org?format=json'
    session = make_session()
    # r = session.get(url)
    # print(r.json())
    try:
        r = session.get(url=url, proxies=proxies)
        print(r.json())
    except requests.exceptions.ProxyError as e:
        print(e)
        pass
    finally:
        return True


def run_executor():
    proxy_list = build_proxies_list()
    print(proxy_list)
    with ProcessPoolExecutor(max_workers=10) as executor:
        executor.map(get_ip, proxy_list)


def run():
    proxy_list = build_proxies_list()
    for proxy in proxy_list:
        get_ip(proxy)


run_executor()
