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

def grabAccountData(data):
    try:
        #Grabs available balances given the correct currency id
        r = requests.get(API_URL + "accounts/" + data, auth=auth)
        p = r.json()
        balance = float('{:.4f}'.format(float(p['balance']))) # balance, hold, available are floats .0001
        hold = float('{:.4f}'.format(float(p['hold'])))       
        available = float('{:.4f}'.format(float(p['available'])))
        return (balance, hold, available)

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
