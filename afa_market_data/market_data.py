#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
from afa_market_data.market_data import ManagerREIT, reit_custom, ManageFileUtil, ReadPagesUtil, FII_CVM_CAD_URL, \
    BMF_SERIES_HIST_YEAR


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
        last_cvs_file = ReadPagesUtil.load_table_FI_cadastre(FII_CVM_CAD_URL)

        # for the latest row download url + column name
        # CSV file is downloaded and if valid file swap with actual inf_cadastral_fie.csv
        ManageFileUtil.download_file(FII_CVM_CAD_URL + last_cvs_file, 'inf_cadastral_fie.csv')

    @staticmethod
    def update_reit_cad_information():
        """
            Execute monthly function to generate new file with information of Real Estate Funds
        :return:
        """
        ManagerREIT.collect_all_REIT_info()

    # function to update daily information from REIT's
    @staticmethod
    def update_last_daily_price():
        ManageFileUtil.download_file(BMF_SERIES_HIST_YEAR, 'file.zip')

        file_name = 'COTAHIST_A2019.TXT'
        # if contains file_name in folde
        # rename to old
        ManageFileUtil.unzip_file('file.zip')
        # if contains file_name in folder
        # delete file_name old and zip file

        ManagerREIT.collect_REIT_daily_stock(file_name)

    @staticmethod
    # execute my custom analysis for REITs
    def run_reits_custom_analisys():
        reit_custom.best_funds()


if __name__ == '__main__':
    print(datetime.now())
    try:
        # todos os dias uteis depois das 7
        #MarketData.download_files_daily()

        # monthly
        #MarketData.update_reit_cad_information()

        # sempre que for avaliar os fundos
        MarketData.update_last_daily_price()
        MarketData.run_reits_custom_analisys()

        # send cvs to google drive

        print(datetime.now())
    except Exception as e:
        print(e)
        print('error  '+str(datetime.now()))
