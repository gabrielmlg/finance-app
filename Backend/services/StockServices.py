import requests
import json
from datetime import datetime
import pandas as pd
import os
from Backend import config

headers = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': config.RAPIDAPI_KEY # "8143eb5be3msha39ece65bb5d21ap1af72fjsn9d1f7333f8cd"
    }

def parseTimestamp(inputdata):
    timestamplist = []
    timestamplist.extend(inputdata)
    calendertime = []
    
    for ts in timestamplist:
        dt = datetime.fromtimestamp(ts)
        # print(dt.date())
        calendertime.append(dt.strftime("%m/%d/%Y"))
        
        #dt.datetime.strptime(date, '"%Y-%m-%d"').date()

    return calendertime

def load_stock(symbol='MGLU3.SA'):
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-charts"
    querystring = {"region":"Brasil","lang":"en","symbol":symbol,"interval":"1d","range":"5y"}

    response = requests.request("GET", url, headers=headers, params=querystring)
    ibov = json.loads(response.text)
    return convert_stock_to_dataframe(ibov)


def convert_stock_to_dataframe(json_):
    meta = json_['chart']['result'][0]['meta']
    timestamp = json_['chart']['result'][0]['timestamp']
    indicators = json_['chart']['result'][0]['indicators']

    date = parseTimestamp(timestamp)
    cot_close = indicators['quote'][0]['close']
    cot_open = indicators['quote'][0]['open']
    cot_low = indicators['quote'][0]['low']
    cot_high = indicators['quote'][0]['high']


    return pd.DataFrame({'date': date, 
                                'open': cot_open, 
                                'close': cot_close, 
                                'low': cot_low, 
                                'high': cot_high})

