#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from .trader import Trader


if __name__ == '__main__':
    print("welcome to dashboard manager")
    print("Chose the options")
    print("1 - Upload values from CEI")

    value = int(input())
    if value == 1:
        # connect to CEI
        # 1099 - INTER DTVM LTDA
        # 5927703
        df_traders = cei.load_information(1099, 5927703)
        # connect to GSheet

        #

