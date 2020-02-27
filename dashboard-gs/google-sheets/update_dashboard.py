#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from .authorization import GSheetUtil


def update_sheet(df_traders):
    gs = GSheetUtil().getSheet()

    worksheet = gs.worksheet("Dashboard")
