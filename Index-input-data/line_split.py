#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
    Class responsible to read the historic series from a file and return a list of shares.
    Be careful with huge files!!!! just joking, this is Python
'''
import pandas as pd
class SeriesHistoricInterpreter:

    @staticmethod
    def read_file_path(file_path):
        shares = []
        with open(file_path, 'r') as f:
            for line in f:
                shares.append(SeriesHistoricInterpreter.split_position_value(line))
        del shares[0]                   #first line is about header of the file
        del shares[len(shares)-1]       #las line is about footer of the file
        return shares

    @staticmethod
    def split_position_value(line):
        str = line
        share = {
            "TIPREG" : str[0:2],
            'DATA' : str[2:10],
            'CODBDI' : str[10:12],
            'CODNEG' : str[12:24],
            'TIPMERC' : str[24:27],
            'NOMRES' : str[27:39],
            'ESPECI' : str[39:49],
            'PRAZOT' : str[49:52],
            'MODREF' : str[52:56],
            'PREABE' : str[56:67]+'.'+str[67:69],
            'PREMAX' : str[69:80]+'.'+str[80:82],
            'PREMIN' : str[82:93]+'.'+str[93:95],
            'PREMED' : str[95:106]+'.'+str[106:108],
            'PREULT' : str[108:119]+'.'+str[119:121],
            'PREOFC' : str[121:132]+'.'+str[132:134],
            'PREOFV' : str[134:145]+'.'+str[145:147],
            'TOTNEG' : str[147:152],
            'QUATOT' : str[152:170],
            'VOLTOT' : str[170:186]+'.'+str[186:188],
            'PREEXE' : str[188:199]+'.'+str[199:201],
            'INDOPC' : str[201:202],
            'DATVEN' : str[202:210],
            'FATCOT' : str[210:217],
            'PTOEXE' : str[217:230],
            'CODISI' : str[230:242],
            'DISMES' : str[242:245]
        }
        return share

if __name__ == '__main__':
    list = SeriesHistoricInterpreter.read_file_path('isinp/COTAHIST_A2018.TXT')
    print(list[len(list)-1])
