import requests

url = 'http://127.0.0.1:5000/product/20'

PARAMS = {'num': 6}
r = requests.post(url=url, params=PARAMS)
