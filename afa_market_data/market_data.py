#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from market_data import ManagerREIT
from analisys import reit_custom
from datetime import datetime


class MarketData:

    def __init__(self):
        print("Market Data")

    # execute monthly function to generate new file with cadastre information of Real Estate Funds
    @staticmethod
    def update_reit_cad_information():
        ManagerREIT.update_monthly()

    # execute function to download updated list of Real Estate Funds

    # function to update daily information from REIT's
    @staticmethod
    def update_reit_daily(file_name):
        ManagerREIT.update_daily(file_name)

    @staticmethod
    # execute my custom analisys for REITs
    def run_reits_custom_analisys():
        reit_custom.best_funds()


if __name__ == '__main__':
    print(datetime.now())
    try:
        #MarketData.update_reit_cad_information()
        #MarketData.update_reit_daily('COTAHIST_D12042019.TXT')
        MarketData.run_reits_custom_analisys()
    except Exception as e:
        print(e)
        print('error  '+str(datetime.now()))
    print(datetime.now())
