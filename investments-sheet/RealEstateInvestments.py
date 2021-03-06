#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import time
import numpy as np
from readCSVFileUtil import ReadCSVFileUtil
from readPagesUtil import ReadPagesUtil


class RealEstateInvestments:

    def __init__(self):
        df1 = ReadCSVFileUtil.readFileCSV('df1.csv', ['TP_FUNDO', 'CNPJ_FUNDO', 'SIT', 'DENOM_SOCIAL'], '')
        df2 = ReadCSVFileUtil.readFileCSV('df2.csv', ['TP_FUNDO', 'CNPJ_FUNDO', 'VL_PATRIM_LIQ'], '')

        self.funds = pd.merge(df1, df2)
        self.funds = self.funds.loc[self.funds['SIT'] != 'CANCELADA']
        self.funds = self.funds.loc[self.funds['TP_FUNDO'] == 'F.I.I.']
        self.funds = self.funds.loc[self.funds['VL_PATRIM_LIQ'] > 0]

        #####update Dataframe file from bmf

        df1 = ReadPagesUtil().loadPageTableFII()
        ticker = []
        cnpj = []
        cotas = []
        isin = []
        lastDividend = []
        yearDividendAverage = []
        tickerValue = []
        for row in df1.iterrows():
            # print(row[1][1])
            detailAllTable = ReadPagesUtil().loadFundDetailByCod(row[1][1])
            # print(detailAllTable)

            tableDetail = detailAllTable[0].fillna("")
            tableDetail.columns = [0, 1]
            # print(tableDetail)
            if tableDetail[1][0]:
                tick = tableDetail[1][0].split()
                ticker.append(tick[0])
                ##### GET ACTUAL PRICE MARKET FOR THIS ticker
                tickerValue.append(ReadPagesUtil().loadLastTickerValueYahooFinance(tick[0]))
                print(row[1][1], tick, tickerValue[-1])
            else:
                ticker.append('')
                tickerValue.append(0)
            #####

            cnpj.append(tableDetail[1][1])

            tableCotas = detailAllTable[4]
            tableCotas.columns = [0, 1]
            # print(tableCotas)
            cotas.append(tableCotas[1][0])

            tableDividend = []
            for table in detailAllTable:
                if 'Proventos' in table.columns:
                    tableDividend = table.fillna("")

            if len(tableDividend) > 0:
                # print(tableDividend)
                yearDividend = 0
                num = 0
                strIsin = ''
                for row in tableDividend.iterrows():
                    strIsin = row[1][1]
                    if row[1][0] == 'RENDIMENTO':
                        yearDividend += row[1][4]
                        num += 1
                isin.append(strIsin)
                if num > 0:
                    yearDividendAverage.append(round(yearDividend / num, 2))
                else:
                    yearDividendAverage.append('')
            else:
                isin.append('')
                yearDividendAverage.append('')

            # print(ticker, cnpj, cotas, isin, yearDividendAverage)
        df1['TICKER'] = ticker
        df1['CNPJ_FUNDO'] = cnpj
        df1['COTA'] = cotas
        df1['ISIN'] = isin
        df1['YEAR_DIV_AVERAGE'] = yearDividendAverage
        df1['PRICE_MARKET'] = tickerValue

        df1.to_csv("files/df3.csv", sep=";", index=False)

        ##########
        ##df1 = ReadCSVFileUtil.readFileCSV('df3.csv', "ALL")
        self.funds = pd.merge(self.funds, df1, left_on="CNPJ_FUNDO", right_on="CNPJ_FUNDO")
        self.funds['PRICE_COTA_PATRIM'] = round(self.funds['VL_PATRIM_LIQ'] / self.funds['COTA'], 2)

        print(self.funds)
        self.funds.to_csv("files/funds.csv", sep=";", index=False, encoding='ISO-8859-1', decimal=',')


if __name__ == '__main__':
    # print(RealEstateInvestments().funds)
    rei = RealEstateInvestments()
