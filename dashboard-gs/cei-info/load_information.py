#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import pandas as pd


def load_information(broker, account):
    # get authorization

    # open report

    # convert to data frame
    data = [['10/02/2020', 'C', 'Merc. Fracionário', '', 'IRBR3F', 'IRBBRASIL REON NM', '29', '35,00', '1.015,00', '1'],
            ['17/02/2020', 'C', 'Merc. Fracionário', '', 'STBP3F', 'SANTOS BRP ON NM', '34', '6,52', '221,68', '1']]
    columns = ['Data do Negócio', 'Compra/Venda', 'Mercado', 'Prazo/Vencimento', 'Código Negociação',
               'Especificação do Ativo', 'Quantidade', 'Preço (R$)', 'Valor Total(R$)', 'Fator de Cotação']
    df_traders = pd.DataFrame(data, columns=columns, dtype=float)
    return df_traders
