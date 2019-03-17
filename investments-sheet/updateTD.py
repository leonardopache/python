from gSheetUtil import GSheetUtil

# get defined cells from worksheet 'FixedData' in sheet opened in gspread
def dataToUpdate(googleSheet):
    #open worksheet FixedDate
    #load the values of cell that have to be updtated
    cells = {'H5','H6','H7','H8'}
    return {'Tesouro Prefixado 2025': cells}

# get values for specific title from readPageUtil.py in mapper formatter
# 'key':'value'
def valuesToUpdate():
    return {'Tesouro Prefixado 2025': '8%','Tesouro Prefixado 2024': '5.6%'}

# update defined cells with actual values
def update(fieldsToUpdate, percent, worksheet):
    #loop in dataToUpdate
    #if dataToUpdate key == valuesToUpdate key -> update valuesToUpdate.value on dataToUpdate.value
    print(fieldsToUpdate.items())
    for key in fieldsToUpdate.keys():
        for value in percent.keys():
            if(key == value):
                for x in fieldsToUpdate[key]:
                    worksheet.update_acell(x, percent[value])



if __name__ == '__main__':
    gs = GSheetUtil().getSheet()
    worksheet = gs.worksheet("Dashboard")
    update(dataToUpdate(gs), valuesToUpdate(), worksheet)
    aux = worksheet.acell('H6').value
    print(aux)
