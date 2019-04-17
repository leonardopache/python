#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#import io, os, sys
import pandas as pd
import pandas_datareader as pdr

from datetime import datetime, timedelta
from .constants import TESOURO_DIRETO_TITULO_TAX, FII_BMF_URL_BASE, FII_BMF_LIST_ALL, FII_BMF_EVENTS_TAB, YAHOO_FINANCE_TICKER_HISTORY


class ReadPagesUtil:

    # for specific site a specific method to load table and return
    # only the necessary information. Take care to avoid many page loads
    @staticmethod
    def load_table_TD():
        data_frame = pd.read_html(TESOURO_DIRETO_TITULO_TAX, header=0, encoding="utf-8")[3]
        return data_frame.dropna().to_json(orient='records', date_format='iso', force_ascii=False )

    @staticmethod
    def load_table_reit_bmf():
        data_frame = pd.read_html(FII_BMF_URL_BASE+FII_BMF_LIST_ALL, header=0, encoding="utf-8",
                        keep_default_na=False)[0]
        data_frame.drop('Fundo',axis=1, inplace=True)
        data_frame.drop('Segmento',axis=1, inplace=True)
        data_frame.columns = ['RAZAO_SOCIAL', 'CODIGO']
        return data_frame

    #load informations like codigo de negociacao (stock),CNPJ
    #load informations like isin, DY, dividend date, dividend value
    @staticmethod
    def load_fund_detail(cod):
        data_frame = pd.read_html(FII_BMF_URL_BASE+FII_BMF_EVENTS_TAB.format(cod),
                    header=0, encoding='utf-8', keep_default_na=False)
        return data_frame

    @staticmethod
    def load_last_ticker_value(ticker):
        value = 0
        list_tables = []
        try:
            list_tables = pd.read_html(YAHOO_FINANCE_TICKER_HISTORY.format(ticker), header=0, encoding='utf-8', decimal=',')
            value = list_tables[0]['Close*'].iloc[0]
        except:
            # nothing for now
            print(list_tables)
        return value


#if __name__ == '__main__':
#    rpu = ReadPagesUtil()
#    print(rpu.load_fund_detail('ITSA4'))
