import time, os, requests, json
from urllib.request import HTTPError
from cbauth import CoinbaseExchangeAuth

with open('config.json') as config_file:
    APIs = json.load(config_file)
    
API_URL = APIs['api_url']
API_KEY = os.getenv('CB_API_KEY')
API_SECRET = os.getenv('CB_API_SECRET')
API_PASS = os.getenv('CB_API_PASS')
auth = CoinbaseExchangeAuth(API_KEY, API_SECRET, API_PASS)

def grabCoinIds():
    coin_file = open("./coinids.json", "r")
    _coin_file = json.load(coin_file)
    coin_file.close()

    r = requests.get(API_URL + 'accounts/', auth=auth)
    p = r.json()

    for x in p:
        print(x['currency'] + " : " + x['id'])
        _coin_file[x['currency']] = {}
        _coin_file[x['currency']] = x['id']

    coin_file = open("./coinids.json", "w+")
    coin_file.write(json.dumps(_coin_file))
    coin_file.close()

    print("Coin Id pairs dumped!")

if __name__ == "__main__":
    grabCoinIds()
