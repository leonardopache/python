#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import simplejson as json
import time
from gSheetUtil import GSheetUtil
from readPagesUtil import ReadPagesUtil


# get values for specific title from readPageUtil.py in mapper formatter
# 'key':'value'
def valuesToUpdate():
    rp = ReadPagesUtil();
    return rp.loadPageTableFII()

def getFundDetail(dfRow):
    #print(dfRow[1])
    dfFundPage = ReadPagesUtil().loadFundDetailByCod(dfRow[1]).fillna("")
    print(dfFundPage)
    # create class and initialize with this values
    fundDetail = {}
    fundDetail["cod"] = dfRow[1]
    fundDetail["name"] = dfRow[0]
    fundDetail["ticker"] = dfFundPage[1][1]
    fundDetail["cnpj"] = dfFundPage[1][2]
    #fundDetail["page"] = dfFundPage[1][4]
    ##############################

    return fundDetail
# update defined cells with actual values
def updateFunds(gsu, valuesFromPage, worksheet):
    #loop in dataToUpdate
    #if dataToUpdate key == valuesToUpdate key -> update valuesToUpdate.value on dataToUpdate.value
    i = 1
    for row in valuesFromPage.iterrows():
        #print(row[1])
        fundDetail = getFundDetail(row[1])
        #print(fundDetail)
        if fundDetail['ticker']:
            gsu.renewAccessToken()
            worksheet.update_acell(f'A{i}', fundDetail['name'])
            worksheet.update_acell(f'B{i}', fundDetail['cod'])
            worksheet.update_acell(f'C{i}', fundDetail['ticker'])
            worksheet.update_acell(f'D{i}', fundDetail['cnpj'])
            i += 1
            time.sleep(10)


if __name__ == '__main__':
    gsu = GSheetUtil()
    worksheet = gsu.getSheet().worksheet("FII")
    #print(tdJson)
    updateFunds(gsu, valuesToUpdate(), worksheet)
