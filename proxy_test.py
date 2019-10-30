import requests
from user_agent import generate_user_agent


def make_session():
    headers = {
        'User-Agent': generate_user_agent()
    }
    with requests.Session() as s:
        s.headers.update(**headers)
    return s


proxies = {
    'http': 'http://109.196.229.23:8080',
    'https': 'http://109.196.229.23:8080',
}

url = 'http://wykop.pl'

session = make_session()

# header = session.head(url, proxies=proxies, allow_redirects=False)
# print(header.status_code)
# if header.status_code == 200:
#     print(header.text)

try:
    response = session.get(url, proxies=proxies,
                           allow_redirects=True, verify=True)
except Exception as e:
    print(f'Error:\n{e}\n')
# print(response.status_code)
else:
    print(response.text)


# if response.status_code:
#     print(response.text)
