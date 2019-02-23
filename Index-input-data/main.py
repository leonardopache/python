import pymongo

def post_data(array):
  #print(array)
  from pymongo import MongoClient
  #client = MongoClient('mongodb://lpache:senha123@ds133961.mlab.com:33961/stock-mongodb')
  client = MongoClient('mongodb://localhost:27017/stock-mongodb')
  db = client['stock-mongodb']
  #print(db)
  
  stock_data = {
    'date' : array[0] ,
	  'action' : array[1] ,
	  'isinp' : array[2] ,
    'emissor' :  array[3],
    'CFI' :  array[4],
    'description' :  array[5],
    'emition_date' :  array[6],
    'emition_year' :  array[7],
    'expiration_date' :  array[8],
    'expiration_year' :  array[9],
    'value_nominal' :  array[12],
    'value_exercicio' :  array[13],
    'indexator' : array[14] 
  }
  #print(stock_data)
  result = db.stock.insert_one(stock_data)
  print('One post: {0}'.format(result.inserted_id))


def split_line(line):
  line = line.rstrip().replace('"','')
  splited = line.split(',')
  post_data(splited)

if __name__ == '__main__':
  filename='isinp/NUMERACA.txt'
  with open(filename,'r') as fh:
    for line in fh:
      split_line(line)
  

