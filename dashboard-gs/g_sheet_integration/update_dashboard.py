#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import pandas as pd

from g_sheet_integration.authorization import GSheetUtil
from trader import Trader


def trades_list_converter(df_trades):
    list = []
    for index, row in df_trades.iterrows():
        t = Trader(row['Data do Negócio'],
                   row['Compra/Venda'],
                   row['Mercado'],
                   row['Código Negociação'],
                   row['Especificação do Ativo'],
                   int(row['Quantidade']),
                   float(row['Preço (R$)']),
                   float(row['Valor Total(R$)']))
        list.append(t)
    return list


def update_sheet(df_trades):
    gs = GSheetUtil().get_sheet()
    worksheet = gs.worksheet("Historico")

    # pegar maior data da panilha
    # get all lines worksheet.get_all_values()
    worksheet_list = worksheet.get_all_values()
    df_sheet = pd.DataFrame(worksheet_list[1:], columns=worksheet_list[0])

    # filtrar DF apartir da ultima data da planilha , format="%d/%m/%Y %H:%M"
    #TODO refatorar number of date convertion
    df_sheet['Data Negócio'] = pd.to_datetime(df_sheet['Data Negócio'], dayfirst=True)
    df_sheet = df_sheet.loc[df_sheet['OP'] == 'M']
    last_import = df_sheet['Data Negócio'].max()
    df_trades['Data do Negócio'] = pd.to_datetime(df_trades['Data do Negócio'], dayfirst=True)
    if not df_sheet.empty:
        df_trades = df_trades.loc[df_trades['Data do Negócio'] > last_import]
    df_trades['Data do Negócio'] = df_trades['Data do Negócio'].dt.strftime('%d/%m/%Y')

    # iterar lista do DF adicionando nova linha a planilha
    for item in trades_list_converter(df_trades):
        worksheet.append_row([item.date,
                              item.action,
                              item.type,
                              'M',
                              item.isin[:-1] if item.isin[-1] == 'F' else item.isin,
                              item.full_name,
                              item.number,
                              item.value_unit,
                              item.value_total])
