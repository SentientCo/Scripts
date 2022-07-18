import time, os, requests, json
from urllib.request import HTTPError
from cbauth import CoinbaseExchangeAuth
from to_order import BuyBot, SellBot

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


def Grid():
    status = open("status.json", "r")        
    _status = json.load(status)            
    status.close()
    init_price = float('{:.4f}'.format(float(_status['init_price'])))
    init_investment = float(_status['init_investment'])
    while True:
        try:
            print("")
            print("Init:",init_price)
            s = requests.get(API_SPOT + "prices/ALGO-USD/spot") #grabs current algo spot price
            sp = s.json()
            spot = float('{:.4f}'.format(float(sp['data']['amount'])))
            print("Spot:",spot)
            new_balance = float('{:.4f}'.format(float(_status['crypto_available'] * spot)))
            print(new_balance)
            difference = float('{:.4f}'.format(((new_balance - init_investment) * 100) / float(init_investment))) #Compares old balance vs. new balance
            #print(difference) #This commented out code compares the new price vs. old price
            #difference =  float('{:.4f}'.format(((spot - init_price) * 100) / init_price))

            old_difference = difference # Use old to compare to new

            if new_balance > init_investment:     
                print("Crypto is up by %",difference) #When conditions are met, sell crypto to keep balance in wallet(Holding $48 worth of algo all times) #profit will be total_sell_amountUSD - USD balance
                if difference > 1:
                    flipper = True
                else:
                    flipper = False
                    
                while flipper: 
                    s = requests.get(API_SPOT + "prices/ALGO-USD/spot") #grabs current algo spot price
                    sp = s.json()
                    spot = float('{:.4f}'.format(float(sp['data']['amount'])))
                    new_balance = float('{:.4f}'.format(float(_status['crypto_available'] * spot)))
                    #print(new_balance)
                    diff = float('{:.4f}'.format(((new_balance - init_investment) * 100) / float(init_investment)))
                    #diff =  float('{:.4f}'.format(((spot - init_price) * 100) / init_price))
                    order_size = float('{:.1f}'.format((new_balance - init_investment)/spot))

                    percentage_gap = float('{:.4f}'.format(diff - old_difference))
                    print("Gap of %",percentage_gap,"between",old_difference,"and",diff)
                    
                    range_upper = int(init_investment + .5)
                    range_lower = int(init_investment - .5)
                    trade_range = range(range_lower, range_upper) #Anyhwere within .50$ of the init_investment, do not trade
                    if percentage_gap <= -.2: #Adjust this as needed 
                        print("Crypto has dropped .2% while above the",old_difference,"mark.")
                        print("Going to sell at market price for %",diff,"profit(with .6% fee currently)")
                        
                        profit_gap = new_balance - init_investment
                        print("Profit Gap:",profit_gap)
                        if profit_gap >= 1.01:
                            if new_balance not in trade_range:
                                print("Going to sell at market price for %",diff,"profit(with .6% fee currently)")
                                print("Going to buy",order_size,"ALGO!")
                                SellBot(order_size)
                                flipper = False
                                Rebase()
                            break
                        else:
                            print("Not over the 1$ minimum for Coinbase!")
                        break
                    if percentage_gap >= .075:
                        print("Crypto has rose above the",old_difference,"mark by .075%!")
                        print("Upping the floor for higher profit margins!")
                        old_difference = diff
                        pass
                    #if price drops .2% after being above 1%, sell off the right amount of crypto to bring balance to init_investment
                    TimeKeeper(abs(diff))
            elif new_balance < init_investment:
                print("Crypto is down by $",difference) #When conditions are met, buy crypto to keep balance in wallet(Holding $48 worth of algo all times)
                if abs(difference) > .8:
                    flipper = True
                else:
                    flipper = False
                while flipper: 
                    s = requests.get(API_SPOT + "prices/ALGO-USD/spot") #grabs current algo spot price
                    sp = s.json()
                    spot = float('{:.4f}'.format(float(sp['data']['amount'])))
                    new_balance = float('{:.4f}'.format(float(_status['crypto_available'] * spot)))
                    diff = float('{:.4f}'.format(((new_balance - init_investment) * 100) / float(init_investment)))
                    order_size = abs(float('{:.1f}'.format((new_balance - init_investment)/spot)))
                    
                    percentage_gap = float('{:.4f}'.format(diff - old_difference))
                    print("Gap of %",percentage_gap,"between",old_difference,"and",diff)
                    if spot < _status['lower_limit']:
                        print("No longer buying! Price has reached your lower limit!")
                        Grid()
                    if percentage_gap >= .2:
                        print("Crypto has rose .2% while below the",old_difference,"mark.")
                        profit_gap = init_investment - new_balance
                        print("Profit Gap:",profit_gap)
                        if profit_gap >= 1.01:
                            print("Going to buy at market price for %",diff,"to bring balance back to init_investment.")
                            print("Going to buy",order_size,"ALGO!")
                            BuyBot(order_size)
                            flipper = False
                            Rebase()
                            break
                        else:
                            print("Not over the 1$ minimum for Coinbase!")
                        break
                    if percentage_gap <= -.15:
                        print("Crypto has dropped below the",old_difference,"mark by .15%!")
                        print("Lowering the floor for a larger rebuy!")
                        old_difference = diff
                        pass

                    TimeKeeper(abs(diff))
                    pass
            else:
                print("Crypto is staying even!") #Do nothing for now. Later add reporting.
                
            TimeKeeper(abs(difference))


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
    s = requests.get(API_SPOT + "prices/ALGO-USD/spot") #grabs current algo spot price
    sp = s.json()
    spot = float('{:.4f}'.format(float(sp['data']['amount'])))
    print("Going to rebase at current market price to prevent trading on a decline")
    print("And usage of all the crypto/USD currently in use.")
    if _status['side'] == 'sell':
        _status['init_price'] = spot
        #_status['init_investment'] = 0.0
        #_status['lower_limit'] = 0.0
        #_status['max_bank'] = 0.0
        #_status['init_bank] = 0.0
        #_status['crypto_available'] = 0.0
        _status['buy_order_id'] = ""
        _status['sell_order_id'] = ""
        _status['side'] = ""
        _status['buy_price'] = 0.0
        #_status['sell_price'] = 0.0
        _status['order_size'] = 0.0
        _status['order_size_usd_buy'] = 0.0
        #_status['order_size_usd_sell'] = 0.0
        _status['time_started'] = ""
        _status['time_completed'] = ""
        #_status['margin'] = 0.0
        #_status['profit'] = 0.0
    elif _status['side'] == 'buy':
        _status['init_price'] = spot
        #_status['init_investment'] = 0.0
        #_status['lower_limit'] = 0.0
        #_status['max_bank'] = 0.0
        #_status['init_bank] = 0.0
        #_status['crypto_available'] = 0.0
        _status['buy_order_id'] = ""
        _status['sell_order_id'] = ""
        _status['side'] = ""
        #_status['buy_price'] = 0.0
        _status['sell_price'] = 0.0
        _status['order_size'] = 0.0
        #_status['order_size_usd_buy'] = 0.0
        _status['order_size_usd_sell'] = 0.0
        _status['time_started'] = ""
        _status['time_completed'] = ""
        #_status['margin'] = 0.0
        #_status['profit'] = 0.0

    status = open("status.json", "w+")
    status.write(json.dumps(_status))
    status.close()

    Grid()


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




    #needs to loop to continuously check how much in percent i am from my floor price. floor price = initial buy in
    #when over 1% get ready to sell, check the percentage faster when ready to sell, when price drops .2% after being up then sell

    #create script that'll write the init price to a json file and hold the price in memory for the program to use
    #After price is grabbed, keep checking price every 5 seconds, if price is higher than 1% of floor price, check every 1.2s -- .2%:4s - .4%:3s - .6%:2s .8%:1s - 1%:.5s
    #Keep in mind throttling happens after 10 requests happen in a second or 15 requests per second in bursts

#if __name__ == "__main__":
    #print("Running Bot...")
    #Grid()
