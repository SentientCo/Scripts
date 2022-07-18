import time, os, requests, json

from urllib.request import HTTPError
from cbauth import CoinbaseExchangeAuth
from to_order import BuyBot, SellBot
from grid import Grid
from order_book import BuyMenu

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


def Start():
    try:
        status = open("status.json", "r")        
        _status = json.load(status)            
        status.close()

        r = requests.get(API_URL + 'accounts/' + USD, auth=auth) #Grabs USD accounts
        p = r.json()
        #for x in p:
            #if x['currency'] == "ALGO": #Used to find the coin ID for account
                #print(x)
        balance = float('{:.4f}'.format(float(p['balance']))) # balance, hold, available are strings
        hold = float('{:.4f}'.format(float(p['hold'])))       # need to convert to floats
        available = float('{:.4f}'.format(float(p['available'])))

        r = requests.get(API_URL + 'accounts/' + ALG, auth=auth) #Grabs ALGO accounts
        p = r.json()
        crypto_balance = float('{:.4f}'.format(float(p['balance']))) # balance, hold, available are strings
        crypto_hold = float('{:.4f}'.format(float(p['hold'])))       # need to convert to floats
        crypto_available = float('{:.4f}'.format(float(p['available'])))

        s = requests.get(API_SPOT + "prices/ALGO-USD/spot") #grabs current algo spot price
        sp = s.json()
        spot = float(sp['data']['amount'])


        total_investment = float(balance) # dollars - change to an input 10% is held in bank
        investment_used = float('{:.4f}'.format(total_investment - (float(total_investment) * .25))) #using 75% of total investment for security/buy dips
        USD_in_crypto = float('{:.4f}'.format((float(crypto_available) * spot))) # crypto_amount x price 
        bank = float(available)
        lower_limit = float('{:.4f}'.format(spot - (float(.07 * spot)))) #grab coin price and do maths to find initial lower limit per coin # initially will set around 7% below current market price - may change 
        print("USD on Hand       :",available)
        print("Crypto on Hand    :",crypto_available)
        print("Crypto Bal in USD :",USD_in_crypto)
        print("Total USD Balance :",total_investment) 

        if _status['init_price'] == 0:
            print("First run! Writing init_price to file!")
            _status['init_price'] = spot

        if _status['init_investment'] == 0:
            print("Setting dollar value coins will be held at!")
            #Use this to do first buy in. Buy crypto equal to 75% of USD account balance. Also set _status['bank'] value initially here. _status['bank'] = 25% of init balance
            if _status['crypto_available'] == 0:
                print(available)
                USD_prep_for_first_buy = float('{:.2f}'.format(available * .99))
                print("Buying",USD_prep_for_first_buy,"worth of crypto to start trading with!")
                _status['init_investment'] = USD_prep_for_first_buy
                init_investment = _status['init_investment']
                order_size = float('{:.1f}'.format(init_investment / spot))
                status = open("status.json", "w+")
                status.write(json.dumps(_status))
                status.close()
                _status['crypto_available'] = order_size
                print("Setting how much crypto is available to trade! This bot trades ALGO only currently!")
                BuyBot(order_size)
        

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