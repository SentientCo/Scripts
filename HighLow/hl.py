import time, os, requests, json
from urllib.request import HTTPError
from cbauth import CoinbaseExchangeAuth
from to_order import BuyBot, SellBot
from grab_price import Price

with open('config.json') as config_file:
    APIs = json.load(config_file)
    
API_URL = APIs['api_url']
API_SPOT = APIs['api_spot']
API_KEY = os.getenv('CB_API_KEY')
API_SECRET = os.getenv('CB_API_SECRET')
API_PASS = os.getenv('CB_API_PASS')
ALG = "829019b7-4630-460c-bcdb-d272bc7e7dc1"
USD = "2ed00cea-6975-4296-8501-34ee89b3a4d6"
auth = CoinbaseExchangeAuth(API_KEY, API_SECRET, API_PASS)
crypto = "ALGO"
fiat = "USD"


def HL():
    status = open(status.json, "r")
    _status = json.load(status)
    status.close()
    init_price = _status['init_price']
    init_investment = _status['init_investment']
    while True:
        try:
            print("")
            print("Checking against ", init_price)
            Price(crypto, fiat)
