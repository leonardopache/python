#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
l = list(range(20, 30))

for __ in l:
    print('Just iterate')
else:
    print('loop finished')

for i, val in enumerate(l):
    print(i, val)

#set comprehensions
s = {i for i in l if not i % 2}
print(s)

# 3 x 3 matrix
zero_matrix = [[0 for _ in range(3)] for _ in range(3)]
for row in zero_matrix:
    print(row)

#recursion
def string_p(s):
    if s:
        print(s[-1], s[0])
        string_p(s[:-1])

string_p('Leonardo')


####################### threading
import threading
import pandas as pd
import re

funds_cad_df = pd.read_csv('../afa_market_data/market_data/files/inf_cadastral_fie.csv', encoding='ISO-8859-1', sep=';', header=0, keep_default_na=False)
funds_cad_df = funds_cad_df.loc[funds_cad_df['SIT'] == 'EM FUNCIONAMENTO NORMAL']
data = {'COMPANY_ID': []}


def execute_rule(data, df):
    for index, row in df.iterrows():
        cnpj = re.sub('[^A-Za-z0-9]+', '', row['CNPJ_FUNDO'])
        data['COMPANY_ID'].append(cnpj)


def prepare_df_to_threading(num_threads, funds_cad_df):
    size = len(funds_cad_df)
    split_size = int(size / num_threads)
    ini =0
    pivot = 0
    arr = []
    for i in range(num_threads-1):
        pivot += split_size
        arr.append(funds_cad_df.iloc[ini:pivot])
        ini = pivot
    arr.append(funds_cad_df.iloc[ini:])
    return arr


def thread_run(data, arr_values, method_target):
    threads = []
    index = 0
    for df in arr_values:
        index += 1
        t = threading.Thread(name='T' + str(index), target=method_target, args=(data, df))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return threads


arr_df = prepare_df_to_threading(5, funds_cad_df)
thread_run(data, arr_df, execute_rule)

print(len(data['COMPANY_ID']), len(funds_cad_df))

"""

import pandas as pd


d1 = {'CL1': [0, 1], 'CL2':['test index 1', 'Arya']}
df1 = pd.DataFrame(d1)



d2 = {'CL8': ['leo'], 'CL9':[]}
d2['CL9'].append('value')

df1['CL_df'] = pd.MultiIndex.from_arrays(d2, names =('Number', 'Names'))

print(df1)