#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import chardet
from .constants import FILE_PATH


class ManageCSVFileUtil:

    @staticmethod
    def read_file_csv(filename, usecols, encoding):

        if not encoding:
            with open(FILE_PATH+filename, 'rb') as f:
                result = chardet.detect(f.read())
            encoding = result['encoding']

        print(encoding)
        if usecols == "ALL":
            return pd.read_csv(FILE_PATH+filename, encoding=encoding,
                        sep=";", header=0, keep_default_na=False)
        return pd.read_csv(FILE_PATH+filename, encoding=encoding,
                        sep=";", header=0, usecols=usecols, keep_default_na=False)

    @staticmethod
    def data_frame_to_csv(filename, data_frame, encoding):
        data_frame.to_csv(FILE_PATH+filename, encoding=encoding, sep=";", index=False)
