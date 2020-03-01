#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

from constants import LOGIN

class Authorization:
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'X-MicrosoftAjax': 'Delta=true'
    }

    def __init__(self, user, pwd):
        self.payload = {
            'ctl00$ContentPlaceHolder1$smLoad': 'ctl00$ContentPlaceHolder1$UpdatePanel1 | ctl00$ContentPlaceHolder1$btnLogar',
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATEGENERATOR': '803C878C',
            'ctl00$ContentPlaceHolder1$txtLogin': user,
            'ctl00$ContentPlaceHolder1$txtSenha': pwd,
            '__ASYNCPOST': 'true',
            'ctl00$ContentPlaceHolder1$btnLogar': 'Entrar'
        }

    def login(self):
        with requests.Session() as s:
            s.verify = False
            result = s.get(LOGIN, headers=self.header)
            soup = BeautifulSoup(result.content, 'html5lib')
            hiddenInputs = soup.findAll(name='input', type='hidden')
            for hidden in hiddenInputs:
                name = hidden['name']
                value = hidden['value']
                self.payload[name] = value

            s.post(LOGIN, data=self.payload, headers=self.header)
            return s




