#!/usr/local/bin/python# -*- coding: utf-8 -*-import pandas as pdimport re, mathfrom .manage_threads import prepare_df_to_threading, create_threadsfrom .manage_csv_file_util import ManageFileUtilfrom .read_table_html_util import ReadPagesUtilfrom .series_interpreter import SeriesInterpreterfrom datetime import datetime, timedeltafrom tqdm import tqdmclass ManagerREIT:    """        Class responsible for keep the market information updated in internal data base    """    reits_df = pd.DataFrame(data=None)    @staticmethod    def collect_all_reit_info():        """            Based on csv inf_cadastral_fie.csv for each fund cnpj load all necessary information for analysis. Many of this            information can be updated monthly.        :return:            reits_df (funds_cad.csv)        """        funds_cad_df = ManageFileUtil.read_file_csv('inf_cadastral_fie.csv', ['TP_FUNDO', 'CNPJ_FUNDO',                                                                                 'SIT', 'DENOM_SOCIAL', 'DT_REG'],                                                    encoding='ISO-8859-1')        funds_cad_df = funds_cad_df.loc[funds_cad_df['SIT'] == 'EM FUNCIONAMENTO NORMAL']        funds_cad_df = funds_cad_df.loc[funds_cad_df['TP_FUNDO'] == 'F.I.I.']        splited_df = prepare_df_to_threading(4, funds_cad_df)        with tqdm(range(len(funds_cad_df))) as pbar:            pbar.set_description("Processing Funds")            threads = create_threads(splited_df, pbar, ManagerREIT.update_reit_from_reports)            for t in threads:                t.start()            for t in threads:                t.join()        ManageFileUtil.data_frame_to_csv('funds_cad.csv', ManagerREIT.reits_df.reset_index(drop=True), 'ISO-8859-1')    def update_reit_from_reports(funds_cad_df, pbar):        data = {'COMPANY_ID': [], 'NAME': [], 'DATE_INI': [], 'EXCLUSIVE': [], 'CLASS': [],            'REFERENCE': [], 'TARGET': [], 'EQUITY': [], 'OWNERS': [], 'ASSETS': [],            'QUOTA': [], 'DY_LAST': [], 'PRICE_QUOTA_EQUITY': [], 'ISIN': []}        for index, row in funds_cad_df.iterrows():            df_all_docs = ReadPagesUtil.load_html_page_all_docs(re.sub('[^A-Za-z0-9]+', '', row['CNPJ_FUNDO']))            if not df_all_docs.empty:                df_inf_estruturado = ManagerREIT.get_last_inf_estruturado(df_all_docs)                ManagerREIT.fill_informe_estruturado(data, df_inf_estruturado)                if "BR" not in data['ISIN'][-1]:                    df_general = ManagerREIT.get_last_inf_general(df_all_docs)                    if not df_general.empty:                        doc_df = ReadPagesUtil.load_tables_doc(df_general['Ações'])                        table_1df = doc_df[0]                        data['ISIN'][-1] = table_1df[1][3]            pbar.update(1)        #TODO- VERIFY CONCURRENCY DURING ACCESS AND WRITE BY THE THREADS        ManagerREIT.reits_df = ManagerREIT.reits_df.append(pd.DataFrame(data))    def get_last_inf_estruturado(df_all_docs):        df = df_all_docs.loc[df_all_docs['Tipo'] == 'Informe Mensal Estruturado']        df = df.reset_index(drop=True)        if not df.empty:            return df.loc[df['Data de Referência'].idxmax()]        else:            return df    def get_last_inf_general(df_all_docs):        df = df_all_docs.loc[df_all_docs['Tipo'] == 'Rendimentos e Amortizações']        df = df.reset_index(drop=True)        if not df.empty:            return df.loc[df['Data de Referência'].idxmax()]        else:            return df    def fill_informe_estruturado(data, df_all_docs):        if not df_all_docs.empty:            doc_df = ReadPagesUtil.load_tables_doc(df_all_docs['Ações'])            table_1df = doc_df[0]            # nome            data['NAME'].append(table_1df[1][0])            # data funcionamento            data['DATE_INI'].append(table_1df[1][1])            # ISIN            data['ISIN'].append(table_1df[1][2])            data['EXCLUSIVE'].append(True if (table_1df[1][3]) == 'Sim' else False)            data['CLASS'].append(table_1df[1][4])            data['REFERENCE'].append(table_1df[1][10])            data['COMPANY_ID'].append(table_1df[3][0])            data['TARGET'].append(table_1df[3][1])            data['QUOTA'].append(int(re.sub('[^A-Za-z0-9]+', '', table_1df[3][2])[:-2]))            table_2df = doc_df[1]            # qnt cotistas            data['OWNERS'].append(re.sub('[^A-Za-z0-9]+', '', table_2df[1][1]))            table_3df = doc_df[2]            # ativos            data['ASSETS'].append(re.sub('[^A-Za-z0-9]+', '', table_3df[2][0])[:-2])            # patrim_liq            data['EQUITY'].append(int(re.sub('[^A-Za-z0-9]+', '', table_3df[2][1])[:-2]))            # DY Mensal            data['DY_LAST'].append((table_3df[2][8]))            quota = data['QUOTA'][-1]            if quota > 0:                data['PRICE_QUOTA_EQUITY'].append(int(math.ceil(data['EQUITY'][-1] / quota)))            else:                data['PRICE_QUOTA_EQUITY'].append(0)    def collect_REIT_daily_stock(file_name):        """            Update REIT information that can be changed every day like Stock Price and Volume.        :param            file_name: Name of the file with historic data from B3.        :return:        """        funds = ManageFileUtil.read_file_csv('funds_cad.csv')        funds = funds[funds['ISIN'] != '']        funds = funds.reset_index(drop=True)        series = SeriesInterpreter(file_name)        # iterate funds and search for daily value ticker volume        historic_df = pd.DataFrame(data=None, columns=['CODISI', 'PREULT', 'VOLTOT', 'CODNEG', 'DATA'])        for index, row in funds.iterrows():            historic_isin_df = series.get_historic_isin_df(row['ISIN'])            historic_df = historic_df.append(historic_isin_df)        funds = pd.merge(funds, historic_df, how='inner', left_on='ISIN', right_on='CODISI')        # save in new file all information        # rename reits-today.cvs to 'reits-'+str((datetime.now() - timedelta(1)).date()        ManageFileUtil.rename_file('reits-today.csv', 'reits-' + re.sub('[^A-Za-z0-9]+', '', str((datetime.now() - timedelta(1)))) + '.csv')        ManageFileUtil.data_frame_to_csv('reits-today.csv', funds, 'ISO-8859-1')        return funds