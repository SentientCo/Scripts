import time, os, requests, json

from urllib.request import HTTPError
from cbauth import CoinbaseExchangeAuth
from grid import Grid
from grab_price import Price
from grab_account_data import grabAccountData
from to_order import BuyBot

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



#Part out this script to the correct places. Is meant to be the main loop handler sending out requests to methods in different files

def Start():
    try:
        status = open("status.json", "r")        
        _status = json.load(status)            
        status.close()

        balance, hold, available = grabAccountData(USD) #Grabs USD accounts
        crypto_balance, crypto_hold, crypto_available = grabAccountData(ALG) #Grabs ALGO accounts
        spot = Price(crypto, fiat) #Grabs current ALGO spot price

        total_investment = float(balance) # dollars - change to an input 10% is held in bank
        investment_used = float('{:.4f}'.format(total_investment - (float(total_investment) * .25))) #using 75% of total investment for security/buy dips
        USD_in_crypto = float('{:.4f}'.format((float(crypto_available) * spot))) # crypto_amount x price 
        bank = float(available)
        lower_limit = float('{:.4f}'.format(spot - (float(.07 * spot)))) #grab coin price and do maths to find initial lower limit per coin # initially will set around 7% below current market price - may change 
        print("USD on Hand       :",available)
        print("Crypto on Hand    :",crypto_available)
        print("Crypto Bal in USD :",USD_in_crypto)
        print("Cash on Hand      :",bank)
        print("Total USD Balance :",total_investment) 
        print("Grid Usage        :",investment_used) # polish - change into input()
        print("Lower Limit       :",lower_limit)  # polish - change into input()

        if _status['init_price'] == 0:
            print("First run! Writing init_price to file!")
            _status['init_price'] = spot

        if _status['lower_limit'] == 0:
            print("Setting the lower limit! Will not trade below $",lower_limit,"!")
            _status['lower_limit'] = lower_limit

        if _status['init_investment'] == 0:
            print("Setting dollar value coins will be held at!")
            if USD_in_crypto != 0:
                _status['init_investment'] = float('{:.2f}'.format(float(USD_in_crypto) * .75))
            #Use this to do first buy in. Buy crypto equal to 75% of USD account balance. Also set _status['bank'] value initially here. _status['bank'] = 25% of init balance
            if _status['crypto_available'] == 0:
                print(available)
                USD_prep_for_first_buy = float('{:.2f}'.format(available * .85))
                print("Buying",USD_prep_for_first_buy,"worth of crypto to start trading with!")
                _status['init_investment'] = USD_prep_for_first_buy
                USD_in_crypto = USD_prep_for_first_buy #Setting this so bank can setup
                init_investment = _status['init_investment']
                order_size = float('{:.1f}'.format(init_investment / spot))
                status = open("status.json", "w+")
                status.write(json.dumps(_status))
                status.close()
                _status['crypto_available'] = order_size
                print("Setting how much crypto is available to trade! This bot trades ALGO only currently!")
                BuyBot(order_size)
                
        if _status['init_bank'] == 0:
            balance, hold, available = grabAccountData(USD) #Grabs USD accounts
            print("Setting how much USD to use if price drops!")
            _status['max_bank'] = float('{:.2f}'.format(bank))
            _status['init_bank'] = float('{:.2f}'.format(bank))
        

        status = open("status.json", "w+")
        status.write(json.dumps(_status))
        status.close()

        Grid() #Always start with Start() to perform first time setup, then should kick into Grid() without problem even if not first time setup
        

    except KeyboardInterrupt:
        pass
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')



if __name__ == "__main__":
    print("Starting up Grid Bot!")
    Start()