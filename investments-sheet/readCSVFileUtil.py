#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#import io, os, sys
import pandas as pd
import chardet
from constants import FILE_PATH

class ReadCSVFileUtil:

    def readFileCSV(fileName, usecols, encoding):

        if not encoding:
            with open(FILE_PATH+fileName, 'rb') as f:
                result = chardet.detect(f.read())
            print(result['encoding'])
            encoding = result['encoding']

        print(encoding)
        if usecols == "ALL":
            return pd.read_csv(FILE_PATH+fileName, encoding=encoding,
                        sep=";", header=0)
        return pd.read_csv(FILE_PATH+fileName, encoding=encoding,
                        sep=";", header=0, usecols=usecols)
