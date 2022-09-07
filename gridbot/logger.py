import time, json, os


def Log_Buy(data):
    log_file = open("./logs/logs.json", "r")
    _log_file = json.load(log_file)
    log_file.close()
    ID = data['id']
    
    _log_file[ID] = {}
    _log_file[ID] = data
    
    log_file = open("./logs/logs.json", "w+")
    log_file.write(json.dumps(_log_file))
    log_file.close()

    print("Logging Buy in ./logs/logs.json")
    return

def Log_Sell(data):
    log_file = open("./logs/logs.json", "r")
    _log_file = json.load(log_file)
    log_file.close()
    ID = data['id']
    
    _log_file[ID] = {}
    _log_file[ID] = data

    log_file = open("./logs/logs.json", "w+")
    log_file.write(json.dumps(_log_file))
    log_file.close()

    print("Logging Sell in ./logs/logs.json")
    return
#Log_Sell()

