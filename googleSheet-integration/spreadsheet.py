import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)


client = gspread.authorize(creds)

sheet = client.open('Plan of Investment')
worksheet = sheet.worksheet("Dashboard")

aux = worksheet.acell('H6').value

# pp = pprint.PrettyPrinter()
# pp.pprint(aux)
print(aux)
