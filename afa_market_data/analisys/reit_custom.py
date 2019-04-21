#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
Class responsible for Real Estate Investments Trust custom analisys
'''
import pandas as pd
import chardet


def read_file_csv(filename, usecols, encoding):

    if not encoding:
        with open('market_data/files/'+filename, 'rb') as f:
            result = chardet.detect(f.read())
        encoding = result['encoding']

    if usecols == "ALL":
        return pd.read_csv('market_data/files/'+filename, encoding=encoding,
                    sep=";", header=0, keep_default_na=False)
    return pd.read_csv('market_data/files/'+filename, encoding=encoding,
                    sep=";", header=0, usecols=usecols, keep_default_na=False)

def best_funds():

    # load file with funds data
    funds = read_file_csv('reits-today.csv', 'ALL', '')
    funds = funds[funds['TICKER'] != '']

    # order funds by DY Greater to Smaller
    funds = funds.sort_values('DY_LAST', ascending=False)
    # order funds by PRICE_MARKET Smaller to Greater
    funds = funds.sort_values('PRICE_MARKET')
    # filter for only funds with PRICE_MARKET is Smaller
    # to PRICE_QUOTA_EQUITY or until 10% Greater PRICE_QUOTA_EQUITY
    print(type(funds['PRICE_QUOTA_EQUITY'][0]))
    funds = funds.query('PRICE_MARKET > PRICE_QUOTA_EQUITY')

    funds = funds.reset_index(drop=True)
    print(funds['PRICE_MARKET'], funds['PRICE_QUOTA_EQUITY'])
