#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import io, os, sys
import pandas as pd
import pprint

from IPython.display import display_html

TESOURO_DIRETO_TITULO_TAX = 'http://www.tesouro.fazenda.gov.br/tesouro-direto-precos-e-taxas-dos-titulos'
# list os constant links to consult values

# for specific site a specific method to load table and return
# only the necessary information. Take care to avoid many page loads
#
def loadIndexTable():
    dataframe = pd.read_html(TESOURO_DIRETO_TITULO_TAX, header=0, encoding="utf-8")[3]
    print(dataframe)


if __name__ == '__main__':
    loadIndexTable()
