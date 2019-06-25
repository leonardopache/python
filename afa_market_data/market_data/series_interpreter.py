#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
    Class responsible to read the historic series from a file and return a list of shares.
    Be careful with huge files!!!! just joking, this is Python
'''
import pandas as pd
import re, math, datetime
from .constants import FILE_PATH


class SeriesInterpreter():

    def split_position_value(self, line):
        self.shares['TIPREG'].append(line[0:2])
        self.shares['DATA'].append(datetime.date(int(line[2:6]), int(line[6:8]), int(line[8:10])))
        self.shares['CODBDI'].append(line[10:12])
        self.shares['CODNEG'].append(str(line[12:24]).strip())
        self.shares['TPMERC'].append(line[24:27])
        self.shares['NOMRES'].append(line[27:39])
        self.shares['ESPECI'].append(line[39:49])
        self.shares['PRAZOT'].append(line[49:52])
        self.shares['MODREF'].append(line[52:56])
        self.shares['PREABE'].append(line[56:67]+'.'+line[67:69])
        self.shares['PREMAX'].append(line[69:80]+'.'+line[80:82])
        self.shares['PREMIN'].append(line[82:93]+'.'+line[93:95])
        self.shares['PREMED'].append(line[95:106]+'.'+line[106:108])
        self.shares['PREULT'].append(math.ceil(float(re.sub('[^\S]+', '0', line[108:119]+'.'+line[119:121]))))
        self.shares['PREOFC'].append(line[121:132]+'.'+line[132:134])
        self.shares['PREOFV'].append(line[134:145]+'.'+line[145:147])
        self.shares['TOTNEG'].append(line[147:152])
        self.shares['QUATOT'].append(line[152:170])
        self.shares['VOLTOT'].append(math.ceil(float(re.sub('[^\S]+', '0', line[170:186]+'.'+line[186:188]))))
        self.shares['PREEXE'].append(line[188:199]+'.'+line[199:201])
        self.shares['INDOPC'].append(line[201:202])
        self.shares['DATVEN'].append(line[202:210])
        self.shares['FATCOT'].append(line[210:217])
        self.shares['PTOEXE'].append(line[217:230])
        self.shares['CODISI'].append(str(line[230:242]).strip())
        self.shares['DISMES'].append(line[242:245])
        #print(self.shares)


    #TODO should return a DataFrame
    def read_file_path(self, file_name):

        with open(FILE_PATH+file_name, 'r') as f:
            for line in f:
                if not line.startswith('00') and not line.startswith('99'):
                    self.split_position_value(line)

        data_frame = pd.DataFrame(self.shares)
        # first and last line is about header of the file
        # data_frame = data_frame.drop([0,len(data_frame)-1], axis=0)
        return data_frame.reset_index(drop=True)

    def get_series(self):
        return self.data_frame

    def get_historic_isin_df(self, isin):
        return self.data_frame[self.data_frame['CODISI'] == isin][['CODISI', 'PREULT', 'VOLTOT', 'CODNEG', 'CODBDI',
                                                                   'TPMERC', 'DATA']]

    def get_daily_value(self, isin):
        value = self.data_frame[self.data_frame['CODISI'] == isin].PREULT
        if not value.empty:
            return value.item()
        else:
            return 0

    def get_daily_volume(self, isin):
        value = self.data_frame[self.data_frame['CODISI'] == isin].VOLTOT
        if not value.empty:
            return value.item()
        else:
            return 0

    def get_ticker(self, isin):
        value = self.data_frame[self.data_frame['CODISI'] == isin].CODNEG
        if not value.empty:
            return value.item()
        else:
            return ''

    def __init__(self, path_file):
        self.shares = {'TIPREG': [], 'DATA': [],
        'CODBDI': [], 'CODNEG': [], 'TPMERC': [], 'NOMRES': [],
        'ESPECI': [], 'PRAZOT': [], 'MODREF': [], 'PREABE': [],
        'PREMAX': [], 'PREMIN': [], 'PREMED': [], 'PREULT': [],
        'PREOFC': [], 'PREOFV': [], 'TOTNEG': [], 'QUATOT': [],
        'VOLTOT': [], 'PREEXE': [], 'INDOPC': [], 'DATVEN': [],
        'FATCOT': [], 'PTOEXE': [], 'CODISI': [], 'DISMES': []}

        self.data_frame = self.read_file_path(path_file)


'''if __name__ == '__main__':
    si = SeriesInterpreter()
    df = si.read_file_path('isinp/COTAHIST_D12042019.TXT')
    print(df)
'''
