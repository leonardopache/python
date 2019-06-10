#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
Responsible for Real Estate Investments Trust custom analysis
"""
from ..manage_csv_file_util import ManageCSVFileUtil
import pandas as pd


def best_funds():
    # load file with funds data
    funds = ManageCSVFileUtil.read_file_csv('reits-today.csv', encoding='ISO-8859-1')
    #funds = funds[funds['TICKER'] != '']

    # pd.to_numeric(funds.PRICE_MARKET, errors='coerce')
    # filter for only funds with PRICE_MARKE is Smaller
    # to PRICE_QUOTA_EQUITY or until 10% Greater PRICE_QUOTA_EQUITY
    funds = funds.loc[funds['PREULT'] < funds['PRICE_QUOTA_EQUITY']]

    # order funds by DY Greater to Smaller
    # order funds by PRICE_MARKET Smaller to Greater
    # funds = funds.sort_values(['DY_LAST', 'PRICE_MARKET'], ascending=[1,0])
    # funds.loc[]
    funds['DATA'] = pd.to_datetime(funds['DATA'])
    xpto = []
    aux = funds.groupby(['CODNEG'])
    for ticker in aux.groups.keys():
        print(ticker)
        # filtrar do df pelo ticker # pegar row com maior DATA
        isin = funds.loc[funds['CODNEG'] == ticker]
        isin = isin.loc[isin['DATA'].idxmax()]
        # adicionar no novo df
        xpto.append(isin)
    funds = pd.DataFrame(xpto)
    funds.reset_index(drop=True, inplace=True)
    ManageCSVFileUtil.data_frame_to_csv('xpto.csv', funds)
