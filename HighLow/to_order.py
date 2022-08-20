import json, requests, time, os
from order_book import SellMenu, BuyMenu
from urllib.request import HTTPError
from cbauth import CoinbaseExchangeAuth
from grab_price import Price
#from logger import Log_Buy, Log_Sell

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

def BuyBot(order_size):
    try:       
        status = open("status.json", "r")        
        _status = json.load(status)            
        status.close()

        now_time = time.asctime(time.localtime(time.time()))
        print(now_time)

        spot = float('{:.4f}'.format(Price(crypto, fiat) * 1.001))
        print("Attempting to buy ", order_size, " ALGO at: $", spot )

        _status['crypto_available'] = order_size + _status['crypto_available']
        _status['buy_price'] = spot
        _status['order_size'] = order_size
        _status['side'] = "buy"
        
        status = open("status.json", "w+")
        status.write(json.dumps(_status))
        status.close()

        BuyMenu()

        return

    except KeyboardInterrupt:
        pass
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

def SellBot(order_size):
    try:       
        now_time = time.asctime(time.localtime(time.time()))
        print(now_time) 

        status = open("status.json", "r")
        _status = json.load(status)
        status.close() 

        sell_price = float('{:.4f}'.format(Price(crypto, fiat) * .999))
        print("Attempting to sell at: $", sell_price)

        _status['crypto_available'] = _status['crypto_available'] - order_size
        _status['order_size'] = order_size
        _status['sell_price'] = sell_price
        _status['side'] = "sell"

        status = open("status.json", "w+")
        status.write(json.dumps(_status))
        status.close()

        SellMenu()
        
        return

    except KeyboardInterrupt:
        pass
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
        

