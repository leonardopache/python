#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#import io, os, sys
import pandas as pd
from constants import TESOURO_DIRETO_TITULO_TAX, FII_BMF_URL_BASE, FII_BMF_LIST_ALL, FII_BMF_EVENTS_TAB

class ReadPagesUtil:

    # for specific site a specific method to load table and return
    # only the necessary information. Take care to avoid many page loads
    def loadPageTableTD(self):
        dataframe = pd.read_html(TESOURO_DIRETO_TITULO_TAX, header=0, encoding="utf-8")[3]
        return dataframe.dropna().to_json(orient='records', date_format='iso', force_ascii=False )

    def loadPageTableFII(self):
        dataframe = pd.read_html(FII_BMF_URL_BASE+FII_BMF_LIST_ALL, header=0, encoding="utf-8")[0]
        #print(dataframe)
        dataframe.drop('Fundo',axis=1, inplace=True)
        dataframe.drop('Segmento',axis=1, inplace=True)
        dataframe.fillna("")
        return dataframe

    #load informations like codigo de negociacao (stock),CNPJ
    #load informations like isin, DY, dividend date, dividend value
    def loadFundDetailByCod(self, cod):
        dataframe = pd.read_html(FII_BMF_URL_BASE+FII_BMF_EVENTS_TAB.format(cod), header=0, encoding='UTF-8', decimal=',')
        #dataframe.fillna("")
        return dataframe


    #if __name__ == '__main__':
    #    loadIndexTable()
