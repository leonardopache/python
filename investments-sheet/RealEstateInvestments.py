#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import time
from readCSVFileUtil import ReadCSVFileUtil
from readPagesUtil import ReadPagesUtil

class RealEstateInvestments:

    def __init__(self):
        df1 = ReadCSVFileUtil.readFileCSV('df1.csv', ['TP_FUNDO', 'CNPJ_FUNDO', 'SIT', 'DENOM_SOCIAL'])
        df2 = ReadCSVFileUtil.readFileCSV('df2.csv', ['TP_FUNDO', 'CNPJ_FUNDO', 'VL_PATRIM_LIQ'])

        self.funds = pd.merge(df1, df2)
        self.funds = self.funds.loc[self.funds['SIT'] != 'CANCELADA']
        self.funds = self.funds.loc[self.funds['TP_FUNDO'] == 'F.I.I.']
        self.funds = self.funds.loc[self.funds['VL_PATRIM_LIQ'] > 0]

        df1 = ReadPagesUtil().loadPageTableFII()
        ticker = []
        cnpj = []
        for row in df1.iterrows():
            print(row[1][1])
            detail = ReadPagesUtil().loadFundDetailByCod(row[1][1])
            print(detail)
            ticker.append(detail[1][1])
            cnpj.append(detail[1][2])

        df1['TICKER'] = ticker
        df1['CNPJ'] = cnpj
        print(df1)
        df1.to_csv("files/df3.csv", sep=";", index=False)


if __name__ == '__main__':
    #print(RealEstateInvestments().funds)
    rei = RealEstateInvestments()
