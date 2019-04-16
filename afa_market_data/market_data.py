#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from market_data import REIT


class MarketData:

    def __init__(self):
        print("Market Data")

    #execute function to download new file with cadastre information of Real Estate Funds

    #execute function to download updated list of Real Estate Funds

    # function to update daily information from REIT's
    def update_REIT_basic_info(self):
        reit = REIT()
        reit.update_daily()

if __name__ == '__main__':
    md = MarketData()
    md.update_REIT_basic_info()
