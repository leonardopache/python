#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from trader import Trader
from cei_integration.load_information import load_information
from g_sheet_integration import update_dashboard


if __name__ == '__main__':
    print('################### Start ###################')
    # connect to CEI
    # 1099 - INTER DTVM LTDA
    df_traders = load_information(1099)

    # connect to GSheet
    update_dashboard.update_sheet(df_traders)
    print('################### Finish ###################')

