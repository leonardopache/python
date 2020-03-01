#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
from bs4 import BeautifulSoup
from constants import TRADE_REPORT, LOGOUT
from cei_integration.authorization import Authorization


def load_information(broker):
    # get authorization
    #TODO remove password and login to env variable
    session = Authorization('', '').login()

    # open report
    neg_get = session.get(TRADE_REPORT)
    payload2 = {
        'ctl00$ContentPlaceHolder1$ToolkitScriptManager1': 'ctl00$ContentPlaceHolder1$updFiltro|ctl00$ContentPlaceHolder1$btnConsultar',
        'ctl00_ContentPlaceHolder1_ToolkitScriptManager1_HiddenField': '',
        'ctl00$ContentPlaceHolder1$hdnPDF_EXCEL': '',
        'ctl00$ContentPlaceHolder1$ddlAgentes': broker,
        'ctl00$ContentPlaceHolder1$ddlContas': '0',
        'ctl00$ContentPlaceHolder1$txtDataDeBolsa': '',
        'ctl00$ContentPlaceHolder1$txtDataAteBolsa': '',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': '',
        '__VIEWSTATEGENERATOR': '',
        '__EVENTVALIDATION': '',
        '__ASYNCPOST': 'true',
        'ctl00$ContentPlaceHolder1$btnConsultar': 'Consultar'
    }
    soup = BeautifulSoup(neg_get.content, 'html5lib')
    hiddenInputs = soup.findAll(name='input', type='hidden')
    for hidden in hiddenInputs:
        name = hidden['name']
        try:
            value = hidden['value']
        except:
            value = ''
        payload2[name] = value

    neg = session.post(TRADE_REPORT, data=payload2, headers=Authorization.header)
    soup = BeautifulSoup(neg.content, 'html5lib')

    #TODO change this for the periodo of last import until today
    payload2['ctl00$ContentPlaceHolder1$txtDataDeBolsa'] = soup.find('span', attrs={
        'id': 'ctl00_ContentPlaceHolder1_lblPeriodoInicialBolsa'}).text
    payload2['ctl00$ContentPlaceHolder1$txtDataAteBolsa'] = soup.find('span', attrs={
        'id': 'ctl00_ContentPlaceHolder1_lblPeriodoFinalBolsa'}).text
    neg = session.post(TRADE_REPORT, data=payload2, headers=Authorization.header)

    soup = BeautifulSoup(neg.content, 'lxml')
    tables = soup.findAll('table')
    #tables = get_tables()

    #TODO clear irrelevant lines in DF and filter the table referent only to traders
    df = pd.read_html(str(tables), header=None, encoding="utf-8", keep_default_na=False, decimal=',', thousands='.')[0]
    df.drop(df.tail(1).index, inplace=True)
    session.get(LOGOUT)
    return df

