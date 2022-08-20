import time, os, requests, json
from urllib.request import HTTPError
from cbauth import CoinbaseExchangeAuth
from to_order import BuyBot, SellBot
from grab_price import Price
from grab_account_data import grabAccountData

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
sell_gap = -.223 #Adjust this as needed 1
sell_place = .075 #Adjust this as needed 2
buy_gap = .2 #Adjust this as needed 3
buy_place = -.13 #Adjust this as needed 4


def HL():
    status = open('status.json', "r")
    _status = json.load(status)
    status.close()
    init_price = _status['init_price']
    init_investment = _status['init_investment']
    while True:
        try:
            #First needs to check if market is good to buy
            #Start comparing the cryptos price difference, waiting until it falls
            print("")
            print("Checking against", init_price)
            spot = Price(crypto, fiat)
            print("Current spot price", spot)

            #Compares old price to new price and outputs a percentage difference
            diff = float('{:.4f}'.format(((spot - init_price) * 100) / init_price))
            old_diff = diff

            if _status['crypto_available'] <= 1: # Shouldnt look to sell if you dont have crypto to sell
                if spot > init_price:
                    print(crypto + " is up by %", diff)
                    if difference > 1:
                        flipper = True
                    else:
                        flipper = False
                
                    while flipper: 
                        spot = Price(crypto, fiat)
                        to_purchase = float('{:.4f}'.format(_status['init_investment'] / spot))
                        diff = float('{:.4f}'.format(((spot - init_price) * 100) / init_price)) 
                        order_size = abs(float('{:.1f}'.format(to_purchase - .1)))
   
                        perc_gap = float('{:.4f}'.format(diff - old_diff))
                        print("Gap of %",perc_gap,"between",old_diff,"and",diff)

                        if perc_gap <= sell_gap: #Adjust this as needed 1
                            print("Crypto has dropped .223% while above the",old_diff,"mark.")
                            print("Going to sell at market price for %",diff,"profit(with .6% fee currently)")
                            print("Going to buy",order_size, "" + crypto + "!\n")
                            SellBot(order_size)
                            Rebase()
                            flipper = False 
                            break
                        if percentage_gap >= .075:
                            print("Crypto has rose above the",old_diff,"mark by .075%!")
                            print("Upping the floor for higher profit margins!\n")
                            old_diff = diff
                            pass
                        TimeKeeper(abs(diff))
                        pass



            elif spot < init_price:
                print("Crypto is down by $", difference)
                if abs(difference) > .8:
                    flipper = True
                else:
                    flipper = False
                
                while flipper:
                    spot = Price(crypto, fiat)
                    to_purchase = float('{:.4f}'.format(_status['init_investment'] / spot))
                    diff = float('{:.4f}'.format(((spot - init_price) * 100) / init_price)) 
                    order_size = abs(float('{:.1f}'.format(to_purchase - .1)))

                    perc_gap = float('{:.4f}'.format(diff - old_diff))
                    print("Gap of %",perc_gap,"between",old_diff,"and",diff)
                    if perc_gap >= buy_gap: #Adjust this as needed 3
                        print(crypto + " has rose .2% while below the",old_diff,"mark.")
                        print("Going to buy at market price for %",diff,".")
                        print("Going to buy",order_size,"" + crypto + "!\n")
                        BuyBot(order_size)
                        Rebase()
                        flipper = False
                        break
                    if perc_gap <= buy_place: #Adjust this as needed 4
                        print("Crypto has dropped below the",old_diff,"mark by .13%!")
                        print("Lowering the floor for a larger buy!\n")
                        old_diff = diff
                        pass
                    
                    TimeKeeper(abs(diff))
                    pass
            else:
                print("Crypto is staying even!") #Add reporting to this later on

            TimeKeeper(abs(diff))
        
        except KeyboardInterrupt:
            break
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')


def Rebase():
    status = open("status.json", "r")        
    _status = json.load(status)            
    status.close()
    spot = Price(crypto, fiat)
    balance, hold, available = grabAccountData(USD)
    crypto_balance, crypto_hold, crypto_available = grabAccountData(ALG)
    print("Going to rebase at current market price to prevent trading on a decline")
    print("And usage of all the crypto/USD currently in use.")
    if _status['side'] == 'sell':
        _status['init_price'] = spot
        _status['init_investment'] = available
        _status['crypto_available'] = crypto_available
        _status['buy_order_id'] = ""
        _status['sell_order_id'] = ""
        _status['side'] = ""
        _status['buy_price'] = 0.0
        #_status['sell_price'] = 0.0
        _status['order_size'] = 0.0
    elif _status['side'] == 'buy':
        _status['init_price'] = spot
        _status['init_investment'] = available
        _status['crypto_available'] = crypto_available
        _status['buy_order_id'] = ""
        _status['sell_order_id'] = ""
        _status['side'] = ""
        #_status['buy_price'] = 0.0
        _status['sell_price'] = 0.0
        _status['order_size'] = 0.0

    status = open("status.json", "w+")
    status.write(json.dumps(_status))
    status.close()

    return







def TimeKeeper(difference):
    if difference > 1:
        time_diff = .5
        print("Checking every",time_diff,"seconds.")
    elif difference > .8:
        time_diff = 1
        print("Checking every",time_diff,"seconds.")
    elif difference > .6:
        time_diff = 2
        print("Checking every",time_diff,"seconds.")
    elif difference > .4:
        time_diff = 3
        print("Checking every",time_diff,"seconds.")
    elif difference > .2:
        time_diff = 4
        print("Checking every",time_diff,"seconds.")
    else:
        time_diff = 5
        print("Checking every",time_diff,"seconds.")

    time.sleep(time_diff)
    return