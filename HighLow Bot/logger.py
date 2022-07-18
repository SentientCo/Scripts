import time, json, os


def Log_Buy():

    status = open("status.json", "r")        
    _status = json.load(status)            
    status.close()

    log_file = open("./logs/logs.json", "r")
    _log_file = json.load(log_file)
    log_file.close()

    order_id = _status['buy_order_id']
    _log_file[order_id] = {}
    _log_file[order_id]['buy_price'] = _status['buy_price']
    _log_file[order_id]['order_size'] = _status['order_size']
    _log_file[order_id]['order_size_usd'] = _status['order_size_usd_buy']
    _log_file[order_id]['time_started'] = _status['time_started']

    log_file = open("./logs/logs.json", "w+")
    log_file.write(json.dumps(_log_file))
    log_file.close()

    print("inside logger.buy")
    return

def Log_Sell():

    status = open("status.json", "r")        
    _status = json.load(status)            
    status.close()

    log_file = open("./logs/logs.json", "r")
    _log_file = json.load(log_file)
    log_file.close()

    order_id = _status['buy_order_id'] #changed to buy_order_id, trying to keep more
    _log_file[order_id] = {}           #data within one json block, pairing 1 buy 1 sell
    _log_file[order_id]['sell_order_id'] = _status['sell_order_id']
    _log_file[order_id]['sell_price'] = _status['sell_price']
    _log_file[order_id]['order_size'] = _status['order_size']
    _log_file[order_id]['order_size_usd'] = _status['order_size_usd_sell']
    _log_file[order_id]['time_completed'] = _status['time_completed']
    _log_file[order_id]['profit'] = _status['profit']
    _log_file[order_id]['margin'] = _status['margin']

    profits = '{:.4f}'.format(float(_status['order_size_usd_sell']) - float(_status['order_size_usd_buy']))
    _log_file[order_id]['profits'] = profits

    log_file = open("./logs/logs.json", "w+")
    log_file.write(json.dumps(_log_file))
    log_file.close()

    print("inside logger.sell")
    return
#Log_Sell()

