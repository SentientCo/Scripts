import json, requests, os
from urllib.request import HTTPError
from cbauth import CoinbaseExchangeAuth
from logger import Log_Buy, Log_Sell

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

#ALL TRANSACTION DATA IS STORED IN 2 AREAS.
#1. IN ITS OWN FILE IN ./logs/cblog/{transaction_id}/ <------Redundancy
#2. IN A GROUPED FILE IN ./logs/logs.json <------This allows easier parsing

def BuyMenu():
    try:            
        status = open("status.json", "r")
        _status = json.load(status)
        status.close()
        #Place an order
        order = {
            'size': _status['order_size'],
            'price': _status['buy_price'],
            'side': 'buy',
            'product_id': 'ALGO-USD',
        }
        r = requests.post(API_URL + 'orders', json=order, auth=auth)
        p = r.json()
        print(p)
        filename = "./logs/cblog/" + p['id'] + ".json"
        new_file = open(filename, "w")
        new_file.write(json.dumps(p))
        new_file.close()
        _status['buy_order_id'] = p['id']
        status = open("status.json", "w+")
        status.write(json.dumps(_status))
        status.close()

        Log_Buy(p)
        #print("inside order_book.buy")
        return

    except KeyboardInterrupt:
        pass
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}') 


def SellMenu():
    try:      
        status = open("status.json", "r")
        _status = json.load(status)
        status.close()
        #Place an order
        order = {
            'size': _status['order_size'],
            'price': _status['sell_price'],
            'side': 'sell',
            'product_id': 'ALGO-USD',
        }
        r = requests.post(API_URL + 'orders', json=order, auth=auth)
        p = r.json()
        print(p) #Store this transaction data
        filename = "./logs/cblog/" + p['id'] + ".json"
        new_file = open(filename, "w")
        new_file.write(json.dumps(p))
        new_file.close
        #_status['profit'] = float('{:.2f}'.format((_status['sell_price'] * _status['order_size']) - (_status['buy_price'] * _status['order_size'])))
        _status['sell_order_id'] = p['id']
        status = open("status.json", "w+")
        status.write(json.dumps(_status))
        status.close()

        Log_Sell(p) 
        #print("inside order_book.sell")
        return

    except KeyboardInterrupt:
        pass
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
