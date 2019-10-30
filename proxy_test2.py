import requests

url = 'http://api.ipify.org?format=json'

r = requests.get(url)

print(r.json())

proxies = {
    'http': 'http://95.209.155.91:8080',
    'https': 'http://95.209.155.91:8080',
}

r = requests.get(url=url, proxies=proxies)

print(r.json())
