#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from market_data import ManagerREIT
from analisys import reit_custom
import datetime


class MarketData:

    def __init__(self):
        print("Market Data")

    # execute monthly function to generate new file with cadastre information of Real Estate Funds
    def update_REIT_cad_information(self):
        ManagerREIT.update_monthly()

    # execute function to download updated list of Real Estate Funds

    # function to update daily information from REIT's
    def update_REIT_daily(self, file_name):
        ManagerREIT.update_daily(file_name)

    # execute my custom analisys for REITs
    def run_reits_custom_analisys(self):
        reit_custom.best_funds()

if __name__ == '__main__':
    print(datetime.datetime.now())
    try:
        md = MarketData()
        md.update_REIT_cad_information()
        md.update_REIT_daily('COTAHIST_D12042019.TXT')
        md.run_reits_custom_analisys()
    except Exception as e:
        print(e)
        print('error  '+str(datetime.datetime.now()))
    print(datetime.datetime.now())
