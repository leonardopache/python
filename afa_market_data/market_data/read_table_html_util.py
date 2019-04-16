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
    def load_table_TD(self):
        dataframe = pd.read_html(TESOURO_DIRETO_TITULO_TAX, header=0, encoding="utf-8")[3]
        return dataframe.dropna().to_json(orient='records', date_format='iso', force_ascii=False )

    def load_table_reit_bmf(self):
        dataframe = pd.read_html(FII_BMF_URL_BASE+FII_BMF_LIST_ALL, header=0, encoding="utf-8")[0]
        #print(dataframe)
        dataframe.drop('Fundo',axis=1, inplace=True)
        dataframe.drop('Segmento',axis=1, inplace=True)
        dataframe.fillna("")
        dataframe.columns = ['RAZAO_SOCIAL', 'CODIGO']
        return dataframe

    #load informations like codigo de negociacao (stock),CNPJ
    #load informations like isin, DY, dividend date, dividend value
    def load_fund_detail(self, cod):
        data_frame = pd.read_html(FII_BMF_URL_BASE+FII_BMF_EVENTS_TAB.format(cod), header=0, encoding='utf-8', decimal=',')
        return data_frame

    def load_last_ticker_value(self, ticker):
        value = 0
        try:
            df = pdr.get_data_yahoo(ticker+'.sa', (datetime.now() - timedelta(1)).date(), datetime.now().date())
            value = round(df['Adj Close'].iloc[0], 4)
        except Exception as err:
            print(err)

        return value
            #list_tables = []
            #try:
            #    list_tables = pd.read_html(YAHOO_FINANCE_TICKER_HISTORY.format(ticker), header=0, encoding='utf-8', decimal=',')
            #    value = list_tables[0]['Close*'].iloc[0]
            #except:
            #    # nothing for now
            #    print(list_tables)
            #return value


#if __name__ == '__main__':
#    rpu = ReadPagesUtil()
#    print(rpu.load_last_ticker_value('ITSA4'))
