#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#import io, os, sys
import pandas as pd
import bs4 as bs
import requests
from .constants import TESOURO_DIRETO_TITULO_TAX, \
    FII_BMF_URL_BASE, FII_BMF_LIST_ALL, FII_BMF_EVENTS_TAB, \
    YAHOO_FINANCE_TICKER_HISTORY, FII_CVM_BASE, FII_CVM_DOCS_LIST

def do_request(url):
    try:
        return requests.get(url)
    except Exception as err:
        print(err)
        return False

def read_html(url):
    try:
        return pd.read_html(url, header=None, encoding="utf-8", keep_default_na=False)
    except Exception as err:
        print(err)
        return False


class ReadPagesUtil:

    # for specific site a specific method to load table and return
    # only the necessary information. Take care to avoid many page loads
    @staticmethod
    def load_table_TD():
        data_frame = pd.read_html(TESOURO_DIRETO_TITULO_TAX, header=0, encoding="utf-8")[3]
        return data_frame.dropna().to_json(orient='records', date_format='iso', force_ascii=False )

    @staticmethod
    def load_table_reit_bmf():
        data_frame = pd.read_html(FII_BMF_URL_BASE+FII_BMF_LIST_ALL, header=0, encoding="utf-8",
                        keep_default_na=False)[0]
        data_frame.drop('Fundo',axis=1, inplace=True)
        data_frame.drop('Segmento',axis=1, inplace=True)
        data_frame.columns = ['RAZAO_SOCIAL', 'CODIGO']
        return data_frame

    #load informations like codigo de negociacao (stock),CNPJ
    #load informations like isin, DY, dividend date, dividend value
    @staticmethod
    def load_fund_detail(cod):
        data_frame = pd.read_html(FII_BMF_URL_BASE+FII_BMF_EVENTS_TAB.format(cod),
                    header=0, encoding='utf-8', keep_default_na=False)
        return data_frame

    @staticmethod
    def load_last_ticker_value(ticker):
        value = 0
        list_tables = []
        try:
            list_tables = pd.read_html(YAHOO_FINANCE_TICKER_HISTORY.format(ticker), header=0, encoding='utf-8', decimal=',')
            value = list_tables[0]['Close*'].iloc[0]
        except:
            # nothing for now
            print(list_tables)
        return value


    @staticmethod
    def load_html_page_all_docs(cnpj):
        loop = True
        while(loop):
            response = do_request(FII_CVM_BASE+FII_CVM_DOCS_LIST.format(cnpj))
            if response :
                loop = False

        #response = requests.get(FII_CVM_BASE+FII_CVM_DOCS_LIST.format(cnpj))
        soup = bs.BeautifulSoup(response.text, 'lxml')
        tables = soup.find_all('table')
        if len(tables) > 0:
            parsed_table = tables[0]
            data = [[str(td.a['href']).replace('visualizarDocumento','exibirDocumento') if td.find('a')
                        else ''.join(td.stripped_strings)
                     for td in row.find_all('td')] for row in parsed_table.find_all('tr')]
            df_all_docs = pd.DataFrame(data[1:], columns=['Nome do Fundo', 'Categoria', 'Tipo',
                                'Espécie', 'Data de Referência', 'Data de Entrega', 'Status',
                                'Versão', 'Modalidade de Envio', 'Ações'])

            df_all_docs = df_all_docs.loc[df_all_docs['Tipo'] == 'Informe Mensal Estruturado']
            df_all_docs = df_all_docs.loc[df_all_docs['Status'] == 'Ativo']
            df_all_docs = df_all_docs.loc[df_all_docs['Data de Referência'] == '03/2019']
            df_all_docs = df_all_docs.reset_index(drop=True)
            return df_all_docs
        else:
            return ''

    @staticmethod
    def load_tables_doc(link):
        loop = True
        while(loop):
            data_frame = read_html(FII_CVM_BASE+link)
            if data_frame:
                loop = False

        return data_frame


    @staticmethod
    def load_table_FI_cadastre(url):
        data_frame = pd.read_html(url, header=0, encoding="utf-8", keep_default_na=False, parse_dates=[2])[0]
        return data_frame.loc[data_frame['Last modified'].idxmax()]['Name']

#if __name__ == '__main__':
    # data = {'key1' : ['t1', 't2', 't3'], 'key2':['a1', 'a2', 'a3']}
    # data['key1'].append('t4')
    # data['key2'].append('a4')
    # df = pd.DataFrame(data)
    # print(df)
