#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
Class responsible for keep the market information updated in internal data base
'''
import pandas as pd
from .manage_csv_file_util import ManageCSVFileUtil
from .read_table_html_util import ReadPagesUtil


class REIT:

    def __init__(self):
        print("REIT")


    def update_fund_detail(self):
        reits = ReadPagesUtil().load_table_reit_bmf()
        ticker = []
        company_id = []
        quotas = []
        isin = []
        last_dividend = []
        year_dividend_average = []
        ticker_value = []

        for row in reits.iterrows():
            detail_all_table = ReadPagesUtil().load_fund_detail(row[1][1])

            # get ticker and company id
            detail_all_table[0].fillna("")
            table_detail = detail_all_table[0]
            table_detail.columns = [0, 1]
            company_id.append(table_detail[1][1])

            if table_detail[1][0]:
                tick = table_detail[1][0].split()
                ticker.append(tick[0])
                ##### GET ACTUAL PRICE MARKET FOR THIS ticker
                ticker_value.append(ReadPagesUtil().load_last_ticker_value(tick[0]))
                print(row[1][1], tick, ticker_value[-1])
            else:
                ticker.append('')
                ticker_value.append(0)

            # get quotas
            table_quotas = detail_all_table[4]
            table_quotas.columns = [0, 1]
            quotas.append(table_quotas[1][0])

            # get dividend
            table_dividend = []
            for table in detail_all_table:
                if 'Proventos' in table.columns:
                    table_dividend = table.fillna("")

            if len(table_dividend) > 0:
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

        reits['TICKER'] = ticker
        reits['COMPANY_ID'] = company_id
        reits['QUOTAS'] = quotas
        reits['ISIN'] = isin
        reits['YEAR_DIV_AVERAGE'] = year_dividend_average
        reits['PRICE_MARKET'] = ticker_value

        #ManageCSVFileUtil.data_frame_to_csv('df3.csv', reits, 'ISO-8859-1')
        return reits

    # Update REIT information daily about the fund and update the BD
    def update_daily(self):
        df1 = ManageCSVFileUtil.read_file_csv('inf_cadastral_fie.csv', ['TP_FUNDO', 'CNPJ_FUNDO', 'SIT', 'DENOM_SOCIAL'], '')
        #melhorar e buscar informacao de patrimonio de outro lugar e nao ler um csv so por uma coluna
        df2 = ManageCSVFileUtil.read_file_csv('medidas_mes_fie_201903.csv', ['TP_FUNDO', 'CNPJ_FUNDO', 'VL_PATRIM_LIQ'], '')

        funds = pd.merge(df1, df2)
        funds = funds.loc[funds['SIT'] != 'CANCELADA']
        funds = funds.loc[funds['TP_FUNDO'] == 'F.I.I.']
        funds = funds.loc[funds['VL_PATRIM_LIQ'] > 0]

        #####update Dataframe file from bmf
        reits = self.update_fund_detail()

        funds = pd.merge(funds, reits, left_on="CNPJ_FUNDO", right_on="COMPANY_ID")
        funds['PRICE_COTA_PATRIM'] = round(funds['VL_PATRIM_LIQ'] / funds['QUOTAS'], 2)

        ManageCSVFileUtil.data_frame_to_csv('funds.csv', funds, 'ISO-8859-1')
        print(funds)
