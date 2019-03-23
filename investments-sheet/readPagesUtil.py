#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import io, os, sys
import pandas as pd
import pprint
from constants import TESOURO_DIRETO_TITULO_TAX

class ReadPagesUtil:

    # for specific site a specific method to load table and return
    # only the necessary information. Take care to avoid many page loads
    def loadIndexTable(self):
        dataframe = pd.read_html(TESOURO_DIRETO_TITULO_TAX, header=0, encoding="utf-8")[3]
        return dataframe.dropna().to_json(orient='records', date_format='iso', force_ascii=False )

    #if __name__ == '__main__':
    #    loadIndexTable()
