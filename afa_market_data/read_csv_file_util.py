#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import chardet
from .constants import FILE_PATH


class ReadCSVFileUtil:

    def read_file_csv(filename, usecols, encoding):

        if not encoding:
            with open(FILE_PATH+filename, 'rb') as f:
                result = chardet.detect(f.read())
            encoding = result['encoding']

        print(encoding)
        if usecols == "ALL":
            return pd.read_csv(FILE_PATH+filename, encoding=encoding,
                        sep=";", header=0)
        return pd.read_csv(FILE_PATH+filename, encoding=encoding,
                        sep=";", header=0, usecols=usecols)
