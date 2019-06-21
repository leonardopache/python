#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm

from .manage_csv_file_util import ManageFileUtil
from .read_table_html_util import ReadPagesUtil
from .manage_threads import prepare_df_to_threading, create_threads

cia_df = pd.DataFrame(data=None)

def update_cia_from_bmf(cia_cad_df, pbar):
    data = {'COMPANY_ID': [], 'NAME': [], 'EQUITY': [], 'TICKER': [],
            'QUOTA': [], 'DY_LAST': [], 'PRICE_QUOTA_EQUITY': [], 'ISIN': []}

    for index, row in cia_cad_df.iterrows():
        tables_tab_resume = ReadPagesUtil.load_bmf_cia_tab_resume(row['CD_CVM'])
        if tables_tab_resume:
            print(tables_tab_resume)
            # df_inf_estruturado = ManagerREIT.get_last_inf_estruturado(df_all_docs)
            # fill_informe_estruturado(data, df_inf_estruturado)

        pbar.update(1)
    # TODO- VERIFY CONCURRENCY DURING ACCESS AND WRITE BY THE THREADS
    cia_df = cia_df.append(pd.DataFrame(data))


def collect_all_cia_info():
    """
        Based on csv inf_cadastral_cia_aberta.csv for each CVM cod load all necessary information for analysis. Many of this
        information can be updated monthly.
    :return:
        reits_df (funds_cad.csv)
    """
    cia_cad_df = ManageFileUtil.read_file_csv('inf_cadastral_cia_aberta.csv',
                                              ['CNPJ_CIA', 'UF', 'DT_REG', 'SIT', 'DENOM_COMERC',
                                               'SIT_EMISSOR', 'CD_CVM', 'SETOR_ATIV'],
                                              encoding='ISO-8859-1')

    cia_cad_df = cia_cad_df.loc[cia_cad_df['SIT'] == 'ATIVO']
    splited_df = prepare_df_to_threading(1, cia_cad_df)

    with tqdm(range(len(cia_cad_df))) as pbar:
        pbar.set_description("Processing CIA's")
        threads = create_threads(splited_df, pbar, update_cia_from_bmf)
        # TODO[do start and join inside of manage_threads as method run(threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    ManageFileUtil.data_frame_to_csv('cias_cad.csv', cia_df.reset_index(drop=True), 'ISO-8859-1')


