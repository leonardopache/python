#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import chardet
import os
import requests
from .constants import FILE_PATH


class ManageCSVFileUtil:

    @staticmethod
    def read_file_csv(filename, usecols='ALL', encoding='None'):

        if encoding is 'None':
            with open(FILE_PATH + filename, 'rb') as f:
                result = chardet.detect(f.read())
            encoding = result['encoding']

        if usecols == 'ALL':
            return pd.read_csv(FILE_PATH + filename, encoding=encoding,
                               sep=';', header=0, keep_default_na=False)
        return pd.read_csv(FILE_PATH + filename, encoding=encoding,
                           sep=';', header=0, usecols=usecols, keep_default_na=False)

    @staticmethod
    def data_frame_to_csv(filename, data_frame, encoding='utf-8'):
        data_frame.to_csv(FILE_PATH + filename, encoding=encoding, sep=';', index=False)

    @staticmethod
    def rename_file(source, target):
        """
            Rename the file source with the target name.

            :param source:
            :param target:

            :return
                File with the new name:
        """
        os.rename(FILE_PATH + source, FILE_PATH + target)

    @staticmethod
    def download_file(url, name):
        """
            Download the content of url in the file name parameter
        :param url:
        :param name:
        :return:
            None
        """
        r = requests.get(url, allow_redirects=True)
        open(FILE_PATH + name, 'wb').write(r.content)
