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
    dfFundPage = ReadPagesUtil().loadFundDetailByCod(dfRow[1])[0].fillna("")
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

def insertFundDetailInGSheet(fundDetail, index):
    for ticker in fundDetail['ticker'].split():
        gsu.renewAccessToken()
        worksheet.update_acell(f'A{index}', fundDetail['name'])
        worksheet.update_acell(f'B{index}', fundDetail['cod'])
        worksheet.update_acell(f'C{index}', ticker)
        worksheet.update_acell(f'D{index}', fundDetail['cnpj'])
        index += 1
    time.sleep(10)


# update defined cells with actual values
def updateFunds(gsu, valuesFromPage, worksheet):
    #loop in dataToUpdate
    #if dataToUpdate key == valuesToUpdate key -> update valuesToUpdate.value on dataToUpdate.value
    index = 1
    dic = []
    for row in valuesFromPage.iterrows():
        fundDetail = getFundDetail(row[1])
        #insertFundDetailInGSheet(fundDetail)
        dic.append(fundDetail)
        print(dic)



if __name__ == '__main__':
    gsu = GSheetUtil()
    worksheet = gsu.getSheet().worksheet("FII")
    #print(tdJson)
    updateFunds(gsu, valuesToUpdate(), worksheet)
