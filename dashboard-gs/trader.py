#!/usr/local/bin/python
# -*- coding: utf-8 -*-


class Trader():
    date = ''
    action = ''
    type = ''
    isin = ''
    full_name = ''
    number = ''
    value_unit = ''
    value_total = ''

    def __init__(self, date, action, type, isin, full_name, number, value_unit, value_total):
        self.date = date
        self.action = action
        self.type = type
        self.isin = isin
        self.full_name = full_name
        self.number = number
        self.value_unit = value_unit
        self.value_total = value_total
