#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import re

from datetime import datetime, timedelta
from tqdm import tqdm

from .series_interpreter import SeriesInterpreter
from .manage_csv_file_util import ManageFileUtil
from .read_table_html_util import ReadPagesUtil
from .manage_threads import prepare_df_to_threading, create_threads

cia_df = pd.DataFrame(data=None)

def update_cia_from_bmf(cia_cad_df, pbar):
    data1 = {'COMPANY_ID': [], 'EQUITY': [], 'TICKER': [],
            'QUOTA': [], 'DY_LAST': []}
    data2 = {'COMPANY_ID': [], 'ISIN': []}
    for index, row in cia_cad_df.iterrows():

        tables_tab_resume = ReadPagesUtil.load_bmf_cia_tab_resume(row['CD_CVM'])
        if tables_tab_resume:
            # cria df com isins e cnpj
            for isin in [tables_tab_resume[0].values[0][1][m.start():m.start() + 12] for m in
                                 re.finditer('[A-z0-9]{10,12}', tables_tab_resume[0].values[0][1])]:
                data2['COMPANY_ID'].append(row['CNPJ_CIA'])
                data2['ISIN'].append(isin)

            # scraping data from tables to our data structure
            data1['COMPANY_ID'].append(row['CNPJ_CIA'])
            data1['EQUITY'].append('')
            data1['TICKER'].append('')
            data1['QUOTA'].append('')
            data1['DY_LAST'].append('')
        pbar.update(1)
    # TODO- VERIFY CONCURRENCY DURING ACCESS AND WRITE BY THE THREADS
    df_ = pd.merge(pd.DataFrame(data1), pd.DataFrame(data2), how='inner', left_on='COMPANY_ID', right_on='COMPANY_ID')
    global cia_df
    cia_df = cia_df.append(pd.DataFrame(df_), sort=True)


def collect_all_cia_info():
    """
        Based on csv inf_cadastral_cia_aberta.csv for each CVM cod load all necessary information for analysis. Many of this
        information can be updated monthly.
    :return:
        reits_df (funds_cad.csv)
    """
    cia_cad_df = ManageFileUtil.read_file_csv('inf_cadastral_cia_aberta.csv',
                                              ['CNPJ_CIA', 'UF', 'DT_REG', 'SIT', 'DENOM_SOCIAL',
                                               'SIT_EMISSOR', 'CD_CVM', 'SETOR_ATIV'],
                                              encoding='ISO-8859-1')

    cia_cad_df = cia_cad_df.loc[cia_cad_df['SIT'] == 'ATIVO']
    # cia_cad_df = cia_cad_df.loc[cia_cad_df['SIT_EMISSOR'] == 'FASE_OPERACIONAL']
    splited_df = prepare_df_to_threading(5, cia_cad_df)

    with tqdm(range(len(cia_cad_df))) as pbar:
        pbar.set_description("Processing CIA's")
        threads = create_threads(splited_df, pbar, update_cia_from_bmf)
        # TODO[do start and join inside of manage_threads as method run(threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
    global cia_df
    df_ = pd.merge(cia_cad_df, cia_df, how='inner', left_on='CNPJ_CIA', right_on='COMPANY_ID')
    ManageFileUtil.data_frame_to_csv('cias_cad.csv', df_, 'ISO-8859-1')

def collect_cia_daily_stock(file_name):
    """
        Update CIA's information that can be changed every day like Stock Price and Volume.
    :param
        file_name: Name of the file with historic data from B3.
    :return:
    """

    cias = ManageFileUtil.read_file_csv('cias_cad.csv')
    series = SeriesInterpreter(file_name)

    # iterate funds and search for daily value ticker volume
    # TODO create static method in series to create load and return a data_frame with historic data.
    historic_df = pd.DataFrame(data=None, columns=['CODISI', 'PREULT', 'VOLTOT', 'CODNEG', 'CODBDI', 'TPMERC', 'DATA'])

    for index, row in cias.iterrows():
        historic_isin_df = series.get_historic_isin_df(row['ISIN'])
        historic_df = historic_df.append(historic_isin_df, sort=True)

    cias = pd.merge(cias, historic_df, how='inner', left_on='ISIN', right_on='CODISI')

    # save in new file all information
    # rename reits-today.cvs to 'reits-'+str((datetime.now() - timedelta(1)).date()
    ManageFileUtil.rename_file('cias-today.csv',
                               'cias-' + re.sub('[^A-Za-z0-9]+', '', str((datetime.now() - timedelta(1)))) + '.csv')

    ManageFileUtil.data_frame_to_csv('cias-today.csv', cias, 'ISO-8859-1')

