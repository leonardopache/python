import pandas as pd

#Pandas
#https://medium.com/@ageitgey/quick-tip-the-easiest-way-to-grab-data-out-of-a-web-page-in-python-7153cecfca58
def panda_load_tables():
	#Brasilian Companies (https://quotes.wsj.com/company-list/country/brazil)

	tables = pd.read_html("https://www.infomoney.com.br/mercados/acoes-e-indices/noticia/7849586/as-23-acoes-que-podem-pagar-os-maiores-dividendos-de-2019",header=0, encoding="Latin-1")
	print(tables[1])

	#Brazilian Funds(http://infofundos.com.br/fundos)
	tables, = pd.read_html("http://infofundos.com.br/fundos", header=0, index_col="CNPJ")
	print(tables.to_json(orient="records", date_format="iso"))
