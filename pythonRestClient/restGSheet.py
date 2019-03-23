#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import gspread
import pandas as pd

from oauth2client.service_account import ServiceAccountCredentials
from IPython.display import display_html

GOOGLE_SHEETS_HOME = 'https://spreadsheets.google.com/feeds'
GOOGLE_DRIVE_AUTH = 'https://www.googleapis.com/auth/drive'

class Dashboard:
    def __init__(self):
        scope = [GOOGLE_SHEETS_HOME, GOOGLE_DRIVE_AUTH]
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)
        sheet = client.open('Plan of Investment')
        worksheet = sheet.worksheet("Dashboard")
        display_html(worksheet.range('A1:N53'))

if __name__ == '__main__':
    dash = Dashboard();
