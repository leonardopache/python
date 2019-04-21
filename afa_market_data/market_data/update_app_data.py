#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
Class responsible for keep the market information updated in internal data base
'''
import pandas as pd
import re
from .manage_csv_file_util import ManageCSVFileUtil
from .read_table_html_util import ReadPagesUtil
from .yahoo_finance_data import YahooFinance
from .series_interpreter import SeriesInterpreter
from datetime import datetime, timedelta
from decimal import *


def load_reit_values(isin, series):
    return series.get_daily_value(isin), series.get_daily_volume(isin), series.get_ticker(isin)


class ManagerREIT:
    @staticmethod
    def update_monthly():
        funds_cad_df = ManageCSVFileUtil.read_file_csv('inf_cadastral_fie.csv', ['TP_FUNDO', 'CNPJ_FUNDO', 'SIT', 'DENOM_SOCIAL', 'DT_REG'], '')
        funds_cad_df = funds_cad_df.loc[funds_cad_df['SIT'] == 'EM FUNCIONAMENTO NORMAL']
        funds_cad_df = funds_cad_df.loc[funds_cad_df['TP_FUNDO'] == 'F.I.I.']

        data = {'COMPANY_ID': [], 'QUOTA': [], 'ISIN': [],'NAME': [],
                'DATE_INI': [], 'EXCLUSIVE': [], 'CLASS': [],
                'REFERENCE': [], 'TARGET': [], 'OWNERS': [], 'ASSETS': [], 'EQUITY': [],
                'DY_LAST': [], 'PRICE_QUOTA_EQUITY': [] }
        getcontext().prec = 2
        for index, row in funds_cad_df.iterrows():
            cnpj = re.sub('[^A-Za-z0-9]+', '', row['CNPJ_FUNDO'])
            print('=========================> ',cnpj)
            df_all_docs = ReadPagesUtil.load_html_page_all_docs(cnpj)

            if not df_all_docs.empty:
                doc_df = ReadPagesUtil.load_tables_doc(df_all_docs['Ações'][0])
                table_1df = doc_df[0]
                #nome
                data['NAME'].append(table_1df[1][0])
                #data funcionamento
                data['DATE_INI'].append(table_1df[1][1])
                #ISIN
                data['ISIN'].append(table_1df[1][2])
                data['EXCLUSIVE'].append(True if (table_1df[1][3]) == 'Sim' else False)
                data['CLASS'].append(table_1df[1][4])
                data['REFERENCE'].append(table_1df[1][10])
                data['COMPANY_ID'].append(table_1df[3][0])
                data['TARGET'].append(table_1df[3][1])
                data['QUOTA'].append(re.sub('[^A-Za-z0-9]+', '', table_1df[3][2])[:-2])

                table_2df = doc_df[1]
                #qnt cotistas
                data['OWNERS'].append(re.sub('[^A-Za-z0-9]+', '', table_2df[1][1]))

                table_3df = doc_df[2]
                #ativos
                data['ASSETS'].append(re.sub('[^A-Za-z0-9]+', '', (table_3df[2][0]))[:-2])
                #patrim_liq
                data['EQUITY'].append(re.sub('[^A-Za-z0-9]+', '', (table_3df[2][1]))[:-2])
                #DY Mensal
                data['DY_LAST'].append((table_3df[2][8]))

                data['PRICE_QUOTA_EQUITY'].append(Decimal(int(data['EQUITY'][-1]) / int(data['QUOTA'][-1])))

        reits_df = pd.DataFrame(data)
        #reits_df['PRICE_QUOTA_EQUITY'] = round(reits_df['EQUITY'] / reits_df['QUOTA'], 2)
        ManageCSVFileUtil.data_frame_to_csv('funds_cad.csv', reits_df, 'ISO-8859-1')
        return reits_df

    # Update REIT information daily about the fund and update the BD
    @staticmethod
    def update_daily(file_name):

        funds = ManageCSVFileUtil.read_file_csv('funds_cad.csv', 'ALL', '')
        funds = funds[funds['ISIN'] != '']
        #funds['PRICE_QUOTA_EQUITY'] = Decimal(funds['EQUITY'] / funds['QUOTA'])

        series = SeriesInterpreter(file_name)

        # iterar funds and search for daily value ticker volume
        value = []
        volume = []
        ticker = []
        for index, row in funds.iterrows():
            value_a, volume_a, ticker_a = load_reit_values(row['ISIN'], series)
            value.append(value_a)
            volume.append(volume_a)
            ticker.append(ticker_a)

        # create new columns for PRICE_MARKET VOLUME TICKER
        funds['PRICE_MARKET'] = value
        funds['VOLUME'] = volume
        funds['TICKER'] = ticker

        # save in new file all information
        # rename reits-today.cvs to reits-'str((datetime.now() - timedelta(1)).date()'
        ManageCSVFileUtil.data_frame_to_csv('reits-today.csv', funds, 'ISO-8859-1')
        return funds

        #####update Dataframe file from bmf
        #reits = self.update_fund_detail()
        #funds = pd.merge(funds, reits, left_on="CNPJ_FUNDO", right_on="COMPANY_ID")
        #funds['PRICE_COTA_PATRIM'] = round(funds['VL_PATRIM_LIQ'] / funds['QUOTAS'], 2)

    '''def update_fund_detail(self):
        reits = ReadPagesUtil.load_table_reit_bmf()
        ticker = []
        company_id = []
        quotas = []
        isin = []
        last_dividend = []
        year_dividend_average = []
        ticker_value = []
        volume = []

        for row in reits.iterrows():
            detail_all_table = ReadPagesUtil.load_fund_detail(row[1][1])

            # get ticker and company id
            table_detail = detail_all_table[0]
            table_detail.columns = [0, 1]
            company_id.append(table_detail[1][1])

            if table_detail[1][0]:
                tick = table_detail[1][0].split()
                share = YahooFinance(tick[0]+'.SA')
                ticker.append(tick[0]+'.SA')
                ##### GET ACTUAL PRICE MARKET FOR THIS ticker
                ticker_value.append(share.get_previous_close_value())
                ##### GET DAILY VOLUME NEGOTIATE
                volume.append(share.get_daily_volume())
            else:
                ticker.append('')
                ticker_value.append(0)
                volume.append(0)

            print(row[1][1], ticker[-1], ticker_value[-1])
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
        reits['VOLUME'] = volume

        #ManageCSVFileUtil.data_frame_to_csv('df3.csv', reits, 'ISO-8859-1')
        return reits
    '''
