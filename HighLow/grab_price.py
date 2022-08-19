import time, os, requests, json
from urllib.request import HTTPError

with open('config.json') as config_file:
    APIs = json.load(config_file)

API_URL = APIs['api_url']
API_SPOT = APIs['api_spot']

def Price(crypto, fiat):
    try:
        #Script currently grabs selected crypto and fiat pair spot price
        #Formats it to a float to .0001
        #Need to make it so it adjusts per crypto as they don't all use the same
        #decimal limit
        r = requests.get(API_SPOT + "prices/" + crypto + "-" + fiat + "/spot")
        p = r.json()
        spot = float('{:.4f}'.format(float(p['data']['amount'])))
        print("Current spot price for " + crypto + ":", spot)
        return spot

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


    