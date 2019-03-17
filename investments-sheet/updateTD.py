#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import simplejson as json

from gSheetUtil import GSheetUtil
from readPagesUtil import ReadPagesUtil


# get defined cells from worksheet 'FixedData' in sheet opened in gspread
def dataToUpdate(googleSheet):
    #open worksheet FixedDate
    #load the values of cell that have to be updtated
    cells = {'H5','H6','H7','H8'}
    return {'Tesouro Prefixado 2025': cells}

# get values for specific title from readPageUtil.py in mapper formatter
# 'key':'value'
def valuesToUpdate():
    rp = ReadPagesUtil();
    return rp.loadIndexTable()

# update defined cells with actual values
def update(fieldsToUpdate, valuesFromPage, worksheet):
    #loop in dataToUpdate
    #if dataToUpdate key == valuesToUpdate key -> update valuesToUpdate.value on dataToUpdate.value
    for key in fieldsToUpdate.keys():
        for value in valuesFromPage:
            if(key == value['Título']):
                percent = value['Taxa de Rendimento (% a.a.)']/100
                for x in fieldsToUpdate[key]:
                    worksheet.update_acell(x, str(percent)+"%")



if __name__ == '__main__':
    gs = GSheetUtil().getSheet()
    worksheet = gs.worksheet("Dashboard")
    #print(tdJson)
    update(dataToUpdate(gs), json.loads(valuesToUpdate()), worksheet)
    aux = worksheet.acell('H6').value
    print(aux)
