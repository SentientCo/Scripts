import time, json, os


def Log_Buy(data):
    log_file = open("./logs/logs.json", "r")
    _log_file = json.load(log_file)
    log_file.close()

    
    log_file = open("./logs/logs.json", "w+")
    log_file.write(json.dumps(_log_file))
    log_file.close()

    print("inside logger.buy")
    return

def Log_Sell(data):
    log_file = open("./logs/logs.json", "r")
    _log_file = json.load(log_file)
    log_file.close()


    log_file = open("./logs/logs.json", "w+")
    log_file.write(json.dumps(_log_file))
    log_file.close()

    print("inside logger.sell")
    return
#Log_Sell()

