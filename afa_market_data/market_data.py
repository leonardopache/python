#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
from afa_market_data.market_data import ManagerREIT, reit_custom, ManageCSVFileUtil
import os


class MarketData:

    def __init__(self):
        print("Market Data")

    @staticmethod
    def download_files_daily():
        """
            Execute function to download updated list of Real Estate Funds
        :return:
            None
        """
        # download csv Inf. Cad. FIE
        url = 'http://dados.cvm.gov.br/dados/FI/CAD/DADOS/'

        # scraping table with pandas

        # df ordered by column last modification

        # for the latest row download url + column name

        # CSV file is downloaded and if valid file swap with actual inf_cadastral_fie.csv


        # download .TXT day historic file has captcha find a way to download
        # if url.find('/'):
        #    name = url.rsplit('/', 1)[1]
        # ManageCSVFileUtil.download_file(url, 'new.csv')

    # execute monthly function to generate new file with cad information of Real Estate Funds
    @staticmethod
    def update_reit_cad_information():
        ManagerREIT.update_monthly()

    # function to update daily information from REIT's
    @staticmethod
    def update_reit_daily(file_name):
        ManagerREIT.update_daily(file_name)

    @staticmethod
    # execute my custom analysis for REITs
    def run_reits_custom_analisys():
        reit_custom.best_funds()


if __name__ == '__main__':
    print(datetime.now())
    try:
        MarketData.update_reit_cad_information()
        MarketData.update_reit_daily('COTAHIST_D12042019.TXT')
        MarketData.run_reits_custom_analisys()
        MarketData.download_files_daily()

        print(datetime.now())
    except Exception as e:
        print(e)
        print('error  '+str(datetime.now()))
