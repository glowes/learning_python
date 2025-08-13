import pandas as pd
import requests as rq
import sqlite3 as sql
from bs4 import BeautifulSoup

#CREATE CONNECTION
conn = sql.connect('STAFF.db')
table_name = 'INSTRUCTOR'
columns_list = ['ID','FNAME','LNAME','CITY','CCODE']

#READ FILE
file_path = 'INSTRUCTOR.csv'
df = pd.read_csv(file_path, names = columns_list)

#LOAD DATA TO THE DATABASE
df.to_sql(table_name, conn, if_exists = 'replace', index =False)
print('Table is ready')


#query the values loaded examples:
query_statement = f"SELECT * FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

query_statement = f"SELECT FNAME FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

query_statement = f"SELECT COUNT(*) FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

#insert data
data_dict = {'ID' : [100],
            'FNAME' : ['John'],
            'LNAME' : ['Doe'],
            'CITY' : ['Paris'],
            'CCODE' : ['FR']}
data_append = pd.DataFrame(data_dict)

data_append.to_sql(table_name, conn, if_exists = 'append', index =False)
print('Data appended successfully')


query_statement = f"SELECT COUNT(*) FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

conn.close()