#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import re
from .manage_csv_file_util import ManageCSVFileUtil
from .read_table_html_util import ReadPagesUtil
from .series_interpreter import SeriesInterpreter
from datetime import datetime, timedelta


def load_reit_values(isin, series):
    return series.get_daily_value(isin), series.get_daily_volume(isin), series.get_ticker(isin)


class ManagerREIT:
    """
        Class responsible for keep the market information updated in internal data base
    """

    @staticmethod
    def collect_all_REIT_info():
        """
            Based on csv inf_cadastral_fie.csv for each fund cnpj load all necessary information for analysis. Many of this
            information can be updated monthly.
        :return:
            reits_df (funds_cad.csv)
        """
        funds_cad_df = ManageCSVFileUtil.read_file_csv('inf_cadastral_fie.csv',
                                                       ['CNPJ_FUNDO', 'SIT', 'DENOM_SOCIAL', 'DT_REG'])
        funds_cad_df = funds_cad_df.loc[funds_cad_df['SIT'] == 'EM FUNCIONAMENTO NORMAL']
        #funds_cad_df = funds_cad_df.loc[funds_cad_df['TP_FUNDO'] == 'F.I.I.']

        data = {'COMPANY_ID': [], 'QUOTA': [], 'ISIN': [], 'NAME': [],
                'DATE_INI': [], 'EXCLUSIVE': [], 'CLASS': [],
                'REFERENCE': [], 'TARGET': [], 'OWNERS': [], 'ASSETS': [], 'EQUITY': [],
                'DY_LAST': [], 'PRICE_QUOTA_EQUITY': []}

        for index, row in funds_cad_df.iterrows():
            cnpj = re.sub('[^A-Za-z0-9]+', '', row['CNPJ_FUNDO'])
            print('====CNPJ====> ', cnpj)

            df_all_docs = ReadPagesUtil.load_html_page_all_docs('22003469000117')
            if  not df_all_docs.empty:
                df_inf_estruturado = ManagerREIT.get_last_inf_estruturado(df_all_docs)
                ManagerREIT.fill_informe_estruturado(data, df_inf_estruturado)

                if "BR" not in data['ISIN'][-1]:
                    pass

        reits_df = pd.DataFrame(data)
        ManageCSVFileUtil.data_frame_to_csv('funds_cad.csv', reits_df, 'ISO-8859-1')
        return reits_df

    @staticmethod
    def get_last_inf_estruturado(df_all_docs):
        df = df_all_docs.loc[df_all_docs['Tipo'] == 'Informe Mensal Estruturado']
        df = df.loc[df['Status'] == 'Ativo']
        df['Data de Referência'] = pd.to_datetime(df['Data de Referência'])
        df = df.reset_index(drop=True)
        if not df.empty:
            return df.loc[df['Data de Referência'].idxmax()]
        else:
            return df

    @staticmethod
    def fill_informe_estruturado(data, df_all_docs):
        if not df_all_docs.empty:
            doc_df = ReadPagesUtil.load_tables_doc(df_all_docs['Ações'])
            # print(doc_df)
            table_1df = doc_df[0]
            # nome
            data['NAME'].append(table_1df[1][0])
            # data funcionamento
            data['DATE_INI'].append(table_1df[1][1])
            # ISIN
            data['ISIN'].append(table_1df[1][2])
            data['EXCLUSIVE'].append(True if (table_1df[1][3]) == 'Sim' else False)
            data['CLASS'].append(table_1df[1][4])
            data['REFERENCE'].append(table_1df[1][10])
            data['COMPANY_ID'].append(table_1df[3][0])
            data['TARGET'].append(table_1df[3][1])
            data['QUOTA'].append(re.sub('[^A-Za-z0-9]+', '', table_1df[3][2])[:-2])

            table_2df = doc_df[1]
            # qnt cotistas
            data['OWNERS'].append(re.sub('[^A-Za-z0-9]+', '', table_2df[1][1]))

            table_3df = doc_df[2]
            # ativos
            data['ASSETS'].append(re.sub('[^A-Za-z0-9]+', '', (table_3df[2][0]))[:-2])
            # patrim_liq
            data['EQUITY'].append(re.sub('[^A-Za-z0-9]+', '', (table_3df[2][1]))[:-2])
            # DY Mensal
            data['DY_LAST'].append((table_3df[2][8]))

            quota = int(data['QUOTA'][-1])
            if quota > 0:
                data['PRICE_QUOTA_EQUITY'].append(round(int(data['EQUITY'][-1]) / quota, 2))
            else:
                data['PRICE_QUOTA_EQUITY'].append(round(0, 2))

    @staticmethod
    def collect_REIT_daily_stock(file_name):
        """
            Update REIT information that can be changed every day like Stock Price and Volume.
        :param
            file_name: Name of the file with historic data from B3.
        :return:
        """

        funds = ManageCSVFileUtil.read_file_csv('funds_cad.csv')
        funds = funds[funds['ISIN'] != '']
        funds = funds.reset_index(drop=True)

        series = SeriesInterpreter(file_name)

        # iterate funds and search for daily value ticker volume
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
        # rename reits-today.cvs to 'reits-'+str((datetime.now() - timedelta(1)).date()
        ManageCSVFileUtil.rename_file('reits-today.csv', 'reits-'+str((datetime.now() - timedelta(1)).date())+'.csv')

        ManageCSVFileUtil.data_frame_to_csv('reits-today.csv', funds, 'ISO-8859-1')
        return funds
