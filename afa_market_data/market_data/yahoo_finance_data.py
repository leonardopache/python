#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import pandas_datareader as pdr
import fix_yahoo_finance as yf
from datetime import datetime, timedelta

class YahooFinance:

    def __init__(self, ticker):
        try:
            self.share = yf.Ticker(ticker)
        except Exception as err:
            print(err)


    def get_previous_close_value(self):
        try:
            return self.share.info['regularMarketPreviousClose']
        except Exception as err:
            print(err)
            return 0

    def get_daily_volume(self):
        try:
            return self.share.info['regularMarketVolume']
        except Exception as err:
            print(err)
            return 0
