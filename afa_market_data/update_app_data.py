#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
Class responsible for keep the market information updated in internal data base
'''
import pandas as pd
from .read_csv_file_util import ReadCSVFileUtil
from .read_table_html_util import ReadPagesUtil


class REIT:
    def __init__(self):
        print("REIT")

    # Update REIT information daily about the fund and update the BD
    def update_daily(self):
        df1 = ReadCSVFileUtil.read_file_csv('inf_cadastral_fie.csv', ['TP_FUNDO', 'CNPJ_FUNDO', 'SIT', 'DENOM_SOCIAL'], '')
        df2 = ReadCSVFileUtil.read_file_csv('medidas_mes_fie_201903.csv', ['TP_FUNDO', 'CNPJ_FUNDO', 'VL_PATRIM_LIQ'], '')

        self.funds = pd.merge(df1, df2)
        self.funds = self.funds.loc[self.funds['SIT'] != 'CANCELADA']
        self.funds = self.funds.loc[self.funds['TP_FUNDO'] == 'F.I.I.']
        self.funds = self.funds.loc[self.funds['VL_PATRIM_LIQ'] > 0]

        #####update Dataframe file from bmf
        reits = ReadPagesUtil().load_table_reit_bmf()
        ticker = []
        company_id = []
        quotas = []
        isin = []
        last_dividend = []
        year_dividend_average = []
        ticker_value = []
        for row in reits.iterrows():
            # print(row[1][1])
            detail_all_table = ReadPagesUtil().load_fund_detail(row[1][1])
            # print(detailAllTable)

            table_detail = detail_all_table[0].fillna("")
            table_detail.columns = [0, 1]
            # print(tableDetail)
            if table_detail[1][0]:
                tick = table_detail[1][0].split()
                ticker.append(tick[0])
                ##### GET ACTUAL PRICE MARKET FOR THIS ticker
                ticker_value.append(ReadPagesUtil().load_last_ticker_value(tick[0]))
                print(row[1][1], tick, ticker_value[-1])
            else:
                ticker.append('')
                ticker_value.append(0)
            #####

            company_id.append(table_detail[1][1])

            table_quotas = detail_all_table[4]
            table_quotas.columns = [0, 1]
            # print(table_quotas)
            quotas.append(table_quotas[1][0])

            table_dividend = []
            for table in detail_all_table:
                if 'Proventos' in table.columns:
                    table_dividend = table.fillna("")

            if len(table_dividend) > 0:
                # print(table_dividend)
                year_dividend = 0
                num = 0
                str_isin = ''
                for row in table_dividend.iterrows():
                    str_isin = row[1][1]
                    if row[1][0] == 'RENDIMENTO':
                        year_dividend += row[1][4]
                        num += 1
                isin.append(str_isin)
                if num > 0:
                    year_dividend_average.append(round(year_dividend / num, 2))
                else:
                    year_dividend_average.append('')
            else:
                isin.append('')
                year_dividend_average.append('')

            # print(ticker, company_id, quotas, isin, yearDividendAverage)
        reits['TICKER'] = ticker
        reits['COMPANY_ID'] = company_id
        reits['QUOTAS'] = quotas
        reits['ISIN'] = isin
        reits['YEAR_DIV_AVERAGE'] = year_dividend_average
        reits['PRICE_MARKET'] = ticker_value

        reits.to_csv("files/df3.csv", sep=";", index=False)

        ##########
        ##df1 = ReadCSVFileUtil.readFileCSV('df3.csv', "ALL")
        self.funds = pd.merge(self.funds, reits, left_on="COMPANY_ID", right_on="COMPANY_ID")
        self.funds['PRICE_COTA_PATRIM'] = round(self.funds['VL_PATRIM_LIQ'] / self.funds['QUOTAS'], 2)

        print(self.funds)
        self.funds.to_csv("files/funds.csv", sep=";", index=False, encoding='ISO-8859-1', decimal=',')
