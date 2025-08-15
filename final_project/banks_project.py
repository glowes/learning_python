import requests
import sqlite3
import pandas as pd 
import numpy as np 
from bs4 import BeautifulSoup
from datetime import datetime



url = "https://web.archive.org/web/20230908091635 /https://en.wikipedia.org/wiki/List_of_largest_banks"
table_attribs = ["Name","MC_USD_Billion"]
table_attribs_final = ["Name","MC_USD_Billion","MC_GBP_Billion","MC_EUR_Billion","MC_INR_Billion"]

output_file =  "Largest_banks_data.csv"
exchange_file = "exchange_rate.csv"
db_name = "Banks.db"
table_name = "Largest_banks"
output_log = "code_log.txt"




#----extract-----
def extract(url,table_attribs):
    r = requests.get(url)
    html_parser = BeautifulSoup(r.text,"html.parser")
    tables = html_parser.find_all('table')
    table  = tables[0]
    df = pd.DataFrame(columns = table_attribs)
    rows = table.find_all('tr')


    for row in rows:
        col = row.find_all('td')
        if len(col)!= 0 and row.find('a') is not None:
             data_dict = {"Name":col[1].get_text(strip=True), 
             "MC_USD_Billion":float(col[2].contents[0])}     
             df1 = pd.DataFrame(data_dict,index=[0])   
             df = pd.concat([df,df1],ignore_index=True)

    #test
    #df.to_csv("test.csv")
    #print(df)

    return df




#---Transform----
def transform(df, csv_path):
    ''' This function accesses the CSV file for exchange rate
    information, and adds three columns to the data frame, each
    containing the transformed version of Market Cap column to
    respective currencies'''

    a_rate = pd.read_csv(csv_path)
    new_attribs = list(set(table_attribs)  ^ set(table_attribs_final))
    currencies = list(a_rate['Currency'])


    for coluna_nova in new_attribs:                                                                      
         for moeda in currencies:
                if moeda in coluna_nova:
                        df[coluna_nova] = np.round(df["MC_USD_Billion"] * a_rate[a_rate["Currency"] == moeda]["Rate"].values[0],2)

    #df.to_csv("test_result.csv")
    print(df)
    print("df['MC_EUR_Billion'][4]:",df['MC_EUR_Billion'][4])
    return df

#------Load------
def load_to_csv(df, output_path):
    ''' This function saves the final data frame as a CSV file in
    the provided path. Function returns nothing.'''
    df.to_csv(output_path)



def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final data frame to a database
    table with the provided name. Function returns nothing.'''
    df.to_sql(table_name,sql_connection,if_exists = 'replace',index=False)

#Log
def log_process(message):
    time_stamp_format = '%Y-%h-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(time_stamp_format)

    with open(output_log,"a") as file:
        file.write(f"{timestamp} : {message} \n")




#queries
def run_queries(query_statement, sql_connection):
    ''' This function runs the stated query on the database table and
    prints the output on the terminal. Function returns nothing. '''
    print(query_statement)
    query_output = pd.read_sql(query_statement,sql_connection)
    print(query_output)
    

#functions calling:

#log
log_process("webscrapping started!")
#call extract
a_df = extract(url,table_attribs)
#log
log_process("Webscrapping end!")

#log
log_process("Data transform started!")
#call transform
a_df = transform(a_df,exchange_file)
#log
log_process("Data transform Ended!")

#log
log_process("Data Load into CSV file Started!")
#call load_to_csv
load_to_csv(a_df,output_file)
#log
log_process("Data Load into CSV file Ended!")

#log
log_process("Data Load into database Started!")
#start database connection
sql_conn = sqlite3.connect(db_name)
load_to_db(a_df,sql_conn,table_name)
#log
log_process("Data Load into database Ended!")



#call queries
sql_statement  = f"SELECT * FROM {table_name}"
run_queries(sql_statement,sql_conn)

sql_statement  = f"SELECT AVG(MC_GBP_Billion) FROM {table_name}"
run_queries(sql_statement,sql_conn)

sql_statement  =f"SELECT Name from {table_name} LIMIT 5"
run_queries(sql_statement,sql_conn)

sql_conn.close()
