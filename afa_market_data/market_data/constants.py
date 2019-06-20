#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# list os constant links to consult values
FILE_PATH = 'market_data/files/'
BMF_URL_BASE = 'http://bvmf.bmfbovespa.com.br/'

TESOURO_DIRETO_TITULO_TAX = 'http://www.tesouro.fazenda.gov.br/tesouro-direto-precos-e-taxas-dos-titulos'

GOOGLE_SHEETS_HOME = 'https://spreadsheets.google.com/feeds'
GOOGLE_DRIVE_AUTH = 'https://www.googleapis.com/auth/drive'

YAHOO_FINANCE_TICKER_HISTORY = 'https://finance.yahoo.com/quote/{0}.SA/history?p={0}.SA&.tsrc=fin-srch'

FII_CVM_BASE = 'http://fnet.bmfbovespa.com.br/fnet/publico/'
FII_CVM_DOCS_LIST = 'abrirGerenciadorDocumentosCVM?cnpjFundo={}'
FII_CVM_CAD_URL = 'http://dados.cvm.gov.br/dados/FIE/CAD/DADOS/'

FII_BMF_EVENTS_TAB = 'FundosListadosDetalhe.aspx?Sigla={}&tipoFundo=Imobiliario&aba=abaEventosCorporativos&idioma=en-us'
FII_BMF_URL_BASE = BMF_URL_BASE+'Fundos-Listados/'
FII_BMF_LIST_ALL = 'FundosListados.aspx?tipoFundo=imobiliario&Idioma=pt-br'

BMF_SERIES_HIST_YEAR = BMF_URL_BASE+'InstDados/SerHist/COTAHIST_A2019.ZIP'

BMF_CIA_INF_BASE_URL = BMF_URL_BASE+'cias-Listadas/Empresas-Listadas/'
BMF_CIA_TAB_RESUME = 'ResumoEmpresaPrincipal.aspx?codigoCvm={}&idioma=pt-br'

CIA_CVM_CAD_URL = 'http://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/'
