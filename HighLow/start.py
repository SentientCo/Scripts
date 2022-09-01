import time, os, requests, json

from urllib.request import HTTPError
from cbauth import CoinbaseExchangeAuth
from hl import HL
from grab_price import Price
from grab_account_data import grabAccountData

with open('config.json') as config_file:
    APIs = json.load(config_file)

with open('coinids.json') as coin_file:
    coins = json.load(coin_file)
    
API_URL = APIs['api_url']
API_SPOT = APIs['api_spot']
API_KEY = os.getenv('CB_API_KEY')
API_SECRET = os.getenv('CB_API_SECRET')
API_PASS = os.getenv('CB_API_PASS')
auth = CoinbaseExchangeAuth(API_KEY, API_SECRET, API_PASS)

ALG = coins['ALGO'] #At some point will change this to user input.
USD = coins['USD']  #Going to remain static for testing
crypto = "ALGO"
fiat = "USD"


def Start():
    try:
        status = open("status.json", "r")        
        _status = json.load(status)            
        status.close()
        
        balance, hold, available = grabAccountData(USD)
        crypto_balance, crypto_hold, crypto_available = grabAccountData(ALG)
        spot = Price(crypto, fiat)

        USD_in_crypto = float('{:.4f}'.format((float(crypto_available) * spot))) # crypto_amount x price 
        print("USD on Hand       :",available)
        print("Crypto on Hand    :",crypto_available)
        print("Crypto Bal in USD :",USD_in_crypto)
        print("Total USD Balance :",balance) 

        # set init_price, init_available. start checking difference against init_price
        # when price drops x amount buy as much crypto as possbile
        # then if price rises over init_available, check faster and use alg to secure higher profits
        # if price rises before it dips then hold onto USD, rebase after a 3% rise, then ^^
        if _status['init_price'] == 0:
            print("Performing first time setup!\n")
            print("Attempting to set init_price to ", spot)
            _status['init_price'] = spot
        if _status['init_investment'] == 0:
            print("Attempting to set init_investment to ", available)
            _status['init_investment'] = available
        if _status['crypto_available'] == 0:
            print("Attempting to set crypto_available to ", crypto_available)
            _status['crypto_available'] = crypto_available
            

        status = open("status.json", "w+")
        status.write(json.dumps(_status))
        status.close()
        if _status['init_price'] or _status['init_investment'] or _status['crypto_available'] != 0:
            print("init_price has been set!")
            print("init_investment has been set!")
            print("crypto_available has been set!")
        else:
            print("ERROR: Failed to set init variables!")

        HL() #Always start with Start() to perform first time setup, then should kick into Grid() without problem even if not first time setup
        

    except KeyboardInterrupt:
        pass
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')



if __name__ == "__main__":
    print("Starting up High/Low Bot!")
    Start()