#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
Class responsible for Real Estate Investments Trust custom analisys
"""
from ..manage_csv_file_util import ManageCSVFileUtil


def best_funds():
    # load file with funds data
    funds = ManageCSVFileUtil.read_file_csv('reits-today.csv', 'ALL', '')
    funds = funds[funds['TICKER'] != '']

    # order funds by PRICE_MARKET Smaller to Greater
    funds = funds.sort_values('PRICE_MARKET')

    #pd.to_numeric(funds.PRICE_MARKET, errors='coerce')
    # filter for only funds with PRICE_MARKE is Smaller
    # to PRICE_QUOTA_EQUITY or until 10% Greater PRICE_QUOTA_EQUITY
    funds = funds.query('PRICE_MARKET < PRICE_QUOTA_EQUITY')
    funds = funds.reset_index(drop=True)

    # order funds by DY Greater to Smaller
    funds = funds.sort_values('DY_LAST', ascending=False)

    ManageCSVFileUtil.data_frame_to_csv('xpto.csv', funds, '')