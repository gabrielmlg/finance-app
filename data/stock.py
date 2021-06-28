import pandas as pd
import numpy as np
import yfinance as yf

class Ticker:
    
    def __init__(self, tickerCode: str):
        self.ticker_code = tickerCode # 'MGLU3.SA'
        self.averageMovingList = ['m_7d', 'm_21d', 'm_60d', 'm_180d']

    def getTicker(self):
        stock = yf.Ticker(ticker=self.ticker_code)
        return stock


    def history(self, ticker):
        return ticker.history(period="max")
        

    def extractStockInfo(self, ticker):
        ''' Nem todos os tickers tem estas informações como ibov '''
        info_dict = ticker.info
        #zip_code = info_dict['zip']
        sector = info_dict['sector']
        return sector

    def calculateYield(self, hist):
        hist['revenue'] = hist['Close'] / hist['Close'].shift() * 100 - 100
        hist['revenue'].fillna(0, inplace=True)
        return hist


    def calculateYield(self, hist):
        hist['revenue'] = hist['Close'] / hist['Close'].shift() * 100 - 100
        hist['revenue'].fillna(0, inplace=True)
        return hist


    def calculateMovingAverage(self, hist):
        hist['m_7d'] = hist['Close'].rolling(7).mean()
        hist['m_21d'] = hist['Close'].rolling(21).mean()
        hist['m_60d'] = hist['Close'].rolling(50).mean()
        hist['m_180d'] = hist['Close'].rolling(50).mean()
        hist['mm_vol_60d'] = hist['Volume'].rolling(60).mean()
        return hist


    def setCrossUpMovingAverage(self, df_):
        df_.loc[:,'isCrossUp_21d'] = df_.apply(lambda x: 1 if x['m_7d'] > x['m_21d'] else 0, axis=1)
        df_.loc[:,'isCrossUp_60d'] = df_.apply(lambda x: 1 if x['m_7d'] > x['m_60d'] else 0, axis=1)